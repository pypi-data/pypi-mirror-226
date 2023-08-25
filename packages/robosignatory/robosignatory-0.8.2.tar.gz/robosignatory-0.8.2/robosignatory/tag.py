import logging
import re

import koji

import robosignatory.utils as utils


log = logging.getLogger("robosignatory.tagconsumer")

KNOWN_TAG_TYPES = ['plain', 'modular']


class TagSigner:

    def __init__(self, config):
        self.config = config

        signing_config = self.config['signing']
        self.signer = utils.get_signing_helper(**signing_config)

        self.koji_clients = {}
        for instance, instance_info in self.config['koji_instances'].items():
            url = instance_info['url']
            client = koji.ClientSession(url, instance_info['options'])

            if instance_info['options']['authmethod'] == 'ssl':
                client.ssl_login(instance_info['options']['cert'],
                                 None,
                                 instance_info['options']['serverca'])
            elif instance_info['options']['authmethod'] == 'kerberos':
                kwargs = {}
                for opt in ('principal', 'keytab', 'ccache'):
                    if opt in instance_info['options']:
                        value = instance_info['options'][opt]
                        kwargs[opt] = value
                client.gssapi_login(**kwargs)
            else:
                raise Exception('Only SSL and kerberos authmethods supported')

            instance_obj = {'client': client,
                            'sidetags': {},
                            'tags': {}}
            if 'mbs_user' in instance_info:
                instance_obj['mbs_user'] = instance_info['mbs_user']
            for tag in instance_info['tags']:
                if tag['from'] in instance_obj['tags']:
                    raise Exception('From detected twice: %s' % tag['from'])
                instance_obj['tags'][tag['from']] = {
                    'to': tag['to'],
                    'key': tag['key'],
                    'keyid': tag['keyid'],
                    'file_signing_key': tag.get('file_signing_key'),
                }

                tag_type = tag.get('type')
                if tag_type is None:
                    tag_type = 'plain'
                elif tag_type not in KNOWN_TAG_TYPES:
                    raise Exception('Invalid tag type detected: %s' % tag_type)
                instance_obj['tags'][tag['from']]['type'] = tag_type

                skip_untagging = tag.get('skip_untagging')
                if skip_untagging is None:
                    skip_untagging = False
                elif not isinstance(skip_untagging, bool):
                    raise Exception('The "skip_untagging" option must be bool')
                instance_obj['tags'][tag['from']]['skip_untagging'] = skip_untagging

                sidetags = tag.get('sidetags')
                if not sidetags:
                    continue

                # Fill in from, to tags in placeholders, this will be the key
                # in instance_obj['sidetags'].
                pattern_filled_in = sidetags['pattern'].replace(
                    '<from>', tag['from']
                ).replace(
                    '<to>', tag['to']
                )

                # Escape and construct regex to match the
                # '<sidetag>-pending-signing' tag to which we should react.
                from_tag_re = re.compile(
                    sidetags['from'].replace(
                        '<sidetag>',
                        r'(?P<sidetag>'
                        + re.escape(pattern_filled_in)
                        + r')'
                    ).replace(re.escape('<seq_id>'), r'(?P<seq_id>[1-9][0-9]*)')
                )

                # We don't want to accept '<sidetag>-pending-signing' tagged
                # builds from just anyone.

                # The 'trusted_taggers' option is a list which defines the user
                # ids from which we want to accept builds tagged into the
                # '<sidetag>-pending-signing' tag.
                trusted_taggers = sidetags['trusted_taggers']
                if (
                    not isinstance(trusted_taggers, list)
                    or not all(isinstance(x, str) for x in trusted_taggers)
                ):
                    raise TypeError("`trusted_taggers` must be a list of strings, not %r."
                                    % trusted_taggers)

                instance_obj['sidetags'][pattern_filled_in] = {
                    'pattern': sidetags['pattern'],
                    'from_tag_re': from_tag_re,
                    'from': sidetags['from'],
                    'to': sidetags['to'],
                    'tags_key': tag['from'],
                    'trusted_taggers': trusted_taggers,
                }

            self.koji_clients[instance] = instance_obj

            log.info('TagSigner ready for service')

    @classmethod
    def is_enabled(cls, config):
        return "koji_instances" in config

    def consume(self, msg):
        if not msg.topic.endswith(".buildsys.tag"):
            return

        #  {u'build_id': 799208,
        #   u'name': u'python-fmn-rules',
        #   u'tag_id': 374,
        #   u'instance': u'primary',
        #   u'tag': u'epel7-infra',
        #   u'user': u'puiterwijk',
        #   u'version': u'0.9.1',
        #   u'owner': u'sayanchowdhury',
        #   u'release': u'1.el7'}}

        build_nvr = '{name}-{version}-{release}'.format(**msg.body)
        build_id = msg.body['build_id']
        tag = msg.body['tag']
        koji_instance = msg.body['instance']

        log.info('Build %s (%s) tagged into %s on %s',
                 build_nvr, build_id, tag, koji_instance)

        if koji_instance not in self.koji_clients:
            log.info('Koji instance not known, skipping')
            return

        self.dowork(build_nvr, build_id, tag, koji_instance,
                    skip_tagging=False)

    def match_sidetag(self, build_nvr, build_id, tag, koji_instance):
        instance = self.koji_clients[koji_instance]

        for sidetag_matched in instance['sidetags'].values():
            from_tag_re = sidetag_matched['from_tag_re']

            m = from_tag_re.match(tag)
            if not m:
                continue

            sidetag = m.group('sidetag')

            # Verify that the build was tagged into the tag by one of the
            # trusted taggers.
            for hist_event in sorted(instance['client'].queryHistory(build=build_id)['tag_listing'],
                                     key=lambda ev: ev['create_ts'],
                                     reverse=True):
                # We want to verify the latest matching tagging event only.
                if (
                    hist_event['active']
                    and hist_event['tag.name'] == tag
                ):
                    if hist_event['creator_name'] in sidetag_matched['trusted_taggers']:
                        # This is how it should be, break out of the loop.
                        break

                    log.error("Side tag build not tagged into %s by trusted user (%s)"
                              " but by '%s'!",
                              tag, ", ".join(sidetag_matched['trusted_taggers']),
                              hist_event['creator_name'])
                    raise Exception('Side tag build tagged by untrusted user')
            else:
                # We should find the tag as active in the tagging history
                # of the build. Bail out because we didn't find it above
                # i.e. didn't break out of the loop.
                log.error("Couldn't find tag %s in history of build %s (%s)!",
                          tag, build_nvr, build_id)
                raise Exception("Tag not found in build history")

            tag_info = instance['tags'][sidetag_matched['tags_key']]
            tag_to = sidetag_matched['to'].replace('<sidetag>', sidetag)

            tag_matched = True

            return tag_matched, tag_info, tag_to

        return False, None, None

    def dowork(self, build_nvr, build_id, tag, koji_instance,
               skip_tagging=False):
        instance = self.koji_clients[koji_instance]

        if not build_id:
            build_id = instance['client'].findBuildID(build_nvr)

        tag_matched = False

        if tag in instance['tags']:
            tag_matched = True
            tag_info = instance['tags'][tag]
            tag_to = tag_info['to']
        else:
            tag_matched, tag_info, tag_to = self.match_sidetag(build_nvr, build_id, tag,
                                                               koji_instance)

        if not tag_matched:
            log.info('Tag not autosigned, skipping')
            return

        if tag_info['file_signing_key']:
            log.info(
                'Going to sign %s with %s (%s) and file signing key %s and move to %s',
                build_nvr, tag_info['key'], tag_info['keyid'], tag_info['file_signing_key'], tag_to)
        else:
            log.info(
                'Going to sign %s with %s (%s) and move to %s',
                build_nvr, tag_info['key'], tag_info['keyid'], tag_to
            )

        if tag_info['type'] == 'plain':
            self.signwrite_single_build(build_nvr, build_id, tag_info, instance, koji_instance)
        elif tag_info['type'] == 'modular':
            self.signwrite_module(build_nvr, build_id, tag_info, instance, koji_instance)
        else:
            raise NotImplementedError('Tag type %s not implemented' % tag_info['type'])

        if skip_tagging:
            log.info('Tagging skipped, done')
        else:
            log.info('Packages correctly signed, moving to %s' % tag_to)
            if tag == tag_to:
                log.info('Non-gated, not moving')
            else:
                if tag_info['skip_untagging']:
                    log.info('Keeping the original tag as well')
                    instance['client'].tagBuild(tag_to, build_id, False, None)
                else:
                    instance['client'].tagBuild(tag_to, build_id, False, tag)

    def signwrite_module(self, build_nvr, build_id, tag_info, instance, koji_instance):
        log.info('Signing module build %s', build_nvr)
        buildinfo = instance['client'].getBuild(build_id)
        if not buildinfo:
            raise Exception('No build object found?')
        content_koji_tag = buildinfo['extra']['typeinfo']['module']['content_koji_tag']
        log.info('Content tag: %s', content_koji_tag)
        log.info('Signing all module content')
        for build in instance['client'].listTagged(content_koji_tag):
            if build['owner_name'] != instance['mbs_user']:
                log.error(
                    'Build {build_id} has owner {owner_name}, which is NOT mbs_user!'.format(
                        **build
                    )
                )
                raise Exception('Modular content tag contains invalid owned build')
            self.signwrite_single_build(build['nvr'], build['build_id'], tag_info, instance,
                                        koji_instance)

    def signwrite_single_build(self, build_nvr, build_id, tag_info, instance, koji_instance):
        log.info('Signing and writing build %s', build_nvr)
        rpms = utils.get_rpms(instance['client'],
                              build_nvr=build_nvr,
                              build_id=build_id,
                              sigkey=tag_info['keyid'])
        log.info('RPMs to sign and move: %s',
                 ['{} ({}, signed: {})'.format(key, rpm['id'], rpm['signed'])
                  for key, rpm in rpms.items()])
        if len(rpms) < 1:
            log.info('Build contains no rpms, skipping signing and writing')

        if all([rpm['signed'] for rpm in rpms.values()]) or len(rpms) < 1:
            log.debug('All RPMs are already signed')
        else:
            to_sign = [key for key, rpm in rpms.items() if not rpm['signed']]
            log.debug('RPMs needing signing: %s' % to_sign)
            cmdline = self.signer.build_sign_cmdline(
                tag_info['key'],
                to_sign,
                koji_instance,
                tag_info.get('file_signing_key'),
            )
            log.debug('Signing command line: %s' % cmdline)

            ret, stdout, stderr = utils.run_command(cmdline)
            if ret != 0:
                log.error('Error signing! Signing output: %s, stdout: '
                          '%s, stderr: %s', ret, stdout, stderr)
                raise Exception('Signing failed')

        if len(rpms) > 1:
            log.info('Build was successfully signed, telling koji to write with key'
                     ' %s', tag_info['keyid'])

            for rpm in rpms.values():
                instance['client'].writeSignedRPM(rpm['id'], tag_info['keyid'])

            log.info('Signed RPMs written out')
