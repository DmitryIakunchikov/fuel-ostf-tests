#    Copyright 2013 Mirantis, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import logging
import os
import pecan

from nose import plugins

from fuel_plugin.ostf_adapter.nose_plugin import nose_test_runner
from fuel_plugin.ostf_adapter.nose_plugin import nose_utils
from fuel_plugin.ostf_adapter.storage import engine, models


CORE_TESTS = 'fuel_health'
#path to debug tests if it given
CORE_PATH = CORE_TESTS or getattr(pecan.conf, 'debug_tests', None)

LOG = logging.getLogger(__name__)


class DiscoveryPlugin(plugins.Plugin):

    enabled = True
    name = 'discovery'
    score = 15000

    def __init__(self, deployment_info):
        self.test_sets = {}
        self.deployment_info = deployment_info
        super(DiscoveryPlugin, self).__init__()

    def options(self, parser, env=os.environ):
        pass

    def configure(self, options, conf):
        pass

    def afterImport(self, filename, module):
        module = __import__(module, fromlist=[module])
        LOG.info('Inspecting %s', filename)
        if hasattr(module, '__profile__'):
            profile = module.__profile__

            if set(profile.get('deployment_tags', []))\
               .issubset(self.deployment_info['deployment_tags']):

                profile['cluster_id'] = self.deployment_info['cluster_id']

                session = engine.get_session()
                with session.begin(subtransactions=True):
                    LOG.info('%s discovered.', module.__name__)
                    test_set = models.TestSet(**profile)
                    test_set = session.merge(test_set)
                    session.add(test_set)
                    self.test_sets[test_set.id] = test_set

    def addSuccess(self, test):
        test_id = test.id()
        for test_set_id in self.test_sets.keys():
            if test_set_id in test_id:
                session = engine.get_session()
                with session.begin(subtransactions=True):

                    data = dict()
                    data['cluster_id'] = self.deployment_info['cluster_id']
                    (data['title'], data['description'],
                     data['duration'], data['deployment_tags']) = \
                        nose_utils.get_description(test)

                    if set(data['deployment_tags'])\
                       .issubset(self.deployment_info['deployment_tags']):

                        LOG.info('%s added for %s', test_id, test_set_id)

                        data.update(
                            {
                                'test_set_id': test_set_id,
                                'name': test_id
                            }
                        )

                        test_obj = models.Test(**data)
                        test_obj = session.merge(test_obj)
                        session.add(test_obj)


def discovery(deployment_info={}, path=CORE_PATH):
    """Will discover all tests on provided path and save info in db
    """
    LOG.info('Starting discovery for %r.', path)

    nose_test_runner.SilentTestProgram(
        addplugins=[DiscoveryPlugin(deployment_info)],
        exit=False,
        argv=['tests_discovery', '--collect-only', '--nocapture', path]
    )
