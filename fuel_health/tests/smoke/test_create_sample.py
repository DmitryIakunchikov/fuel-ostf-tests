# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2013 Mirantis, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import logging
from fuel_health import ceilometeramnager
from nose.plugins.attrib import attr
from fuel_health import nmanager

LOG = logging.getLogger(__name__)


""" Test module contains tests for sample creation. """


class SampleTest(nmanager.SmokeChecksTest):
    def setUp(self):
        self.ceilometer_client = ceilometeramnager.CeilometerBaseTest()

    _interface = 'json'

    @attr(type=["fuel", "smoke"])
    def test_create_sample(self):
        """Create sample metric
        Target component: Ceilometer

        Scenario:
            1. Create sample for existing resource (the default image).
            2. Check that created sample has the expected resource.
            3. Check that the sample has the statistic.
        Duration: 40 s.
        """
        fail_msg_1 = 'Sample can not be created'
        sample = self.verify(30, self.ceilometer_client.create_sample, 1,
                             fail_msg_1,
                             "Sample creating",
                             nmanager.get_image_from_name())
        fail_msg_2 = 'Sample resource is absent'
        sample_resource = self.verify_response_body_value(body_structure=sample.resource_id,
                                                          value=nmanager.get_image_from_name(),
                                                          msg=fail_msg_2,
                                                          failed_step=2)
        fail_msg_3 = 'Sample statistic list is unavailable. '

        sample_statistic = self.verify(5, self.ceilometer_client.list_statistics,
                                          3, fail_msg_3, "sample statistic",sample.name.startswith('ost1_test-sample'))
