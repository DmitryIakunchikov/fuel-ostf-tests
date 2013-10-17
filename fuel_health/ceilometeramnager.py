
import logging

from fuel_health.common.utils.data_utils import rand_name
from fuel_health import config
import fuel_health.nmanager
import fuel_health.test


class CeilometerBaseTest(fuel_health.nmanager.OfficialClientTest):


    def setUp(self):
        super(CeilometerBaseTest, self).setUp()
        if self.ceilometer_client is None:
            self.fail('Ceilometer is unavailable.')

    def list_meters(self):
        """
            This method allows to get the list of environments.
            Returns the list of environments.
        """
        return self.ceilometer_client.meters.list()

    def list_alarm(self):
        """
        This method list alarms
        """
        return self.ceilometer_client.alarms.list()

