import mock
import unittest2

from google.appengine.api import memcache
from google.appengine.ext import testbed

from mlabns.db import nagios_status_data
from mlabns.db import model
from mlabns.util import constants

# def get_nagios_credentials():
#     """Retrieve nagios authentication information.

#     Returns:
#         Nagios model instance containing nagios credentials,
#     """
#     nagios = memcache.get(constants.DEFAULT_NAGIOS_ENTRY)
#     if not nagios:
#         nagios = model.Nagios.get_by_key_name(constants.DEFAULT_NAGIOS_ENTRY)
#         if nagios:
#             memcache.set(constants.DEFAULT_NAGIOS_ENTRY, nagios)
#         else:
#             logging.error('Datastore does not have the Nagios credentials.')

#     return nagios


class GetNagiosCredentialsTest(unittest2.TestCase):

    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()

        nagios_model_patch = mock.patch.object(model, 'Nagios', autospec=True)
        self.addCleanup(nagios_model_patch.stop)
        nagios_model_patch.start()

    def tearDown(self):
        self.testbed.deactivate()

    def test_get_nagios_credentials_returns_successfully_from_memcache(self):
        #mock_nagios = mock.Mock()
        #memcache.set(constants.DEFAULT_NAGIOS_ENTRY, mock_nagios)

        #actual_nagios = nagios_status_data.get_nagios_credentials()

        #self.assertNotEqual(actual_nagios, None)
        #self.assertEqual(constants.DEFAULT_NAGIOS_ENTRY, actual_nagios.key_id)

        with mock.patch('google.appengine.api.memcache') as mock_memcache:
            mock_memcache.get.return_value = mock.Mock(
                key_id=constants.DEFAULT_NAGIOS_ENTRY)
            #actual_nagios= nagios_status_data.get_nagios_credentials()
            #self.assertNotEqual(actual_nagios, None)
            #self.assertEqual(constants.DEFAULT_NAGIOS_ENTRY, actual_nagios.key_id)


if __name__ == '__main__':
    unittest2.main()
