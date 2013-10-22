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

LOG = logging.getLogger(__name__)

class CeilometerApiTests(ceilometeramnager.CeilometerBaseTest):

    """
    TestClass contains tests that check basic Compute functionality.
    """

    def test_list_meters(self):
        """List resources
        Test checks that the list of images is available.
        Duration: 1s.
        """
        fail_msg = "meter list unavailable"

        list_meters_resp = self.verify(20, self.list_meters,
                                        1, fail_msg, "meter listing")


    def test_list_alarms(self):
        """List alarms
        Test checks that the list of images is available.
        Duration: 1s.
        """
        fail_msg = "alarm list unavailable"

        list_alarms_resp = self.verify(20, self.list_alarm,
                                        1, fail_msg, "alarm listing")


    def test_list_resources(self):
        """Resource list availability
        Test checks that the list of resources is available.
        Target component: Ceilometer
        Scenario:
            1. Request the list of resources.
        Duration: 5 s.
        """
        fail_msg = 'Resource list is unavailable. '

        list_resources_resp = self.verify(5, self.list_resources,
                                         1, fail_msg, "resource listing")
