import unittest
from mock import Mock
from mock import MagicMock

from windypie import WindyPie
from windypie import SocrataPythonAdapter

class CoreTests(unittest.TestCase):

    def setUp(self):
        self.valid_url = 'http://valid.com'
        self.user = 'username'
        self.password = 'password'
        self.token = 'abc123'
        self.adapter = SocrataPythonAdapter(self.valid_url, self.user, self.password, self.token)
        self.mock_adapter = Mock()
        self.mock_adapter.get_views.return_value = ['view1', 'view2', 'view3']

    def test_socrata_python_adapter_init(self):
        """instance object should init with url, user, password, and token"""
        self.assertEqual(self.adapter.url, self.valid_url)
        self.assertEqual(self.adapter.user, self.user)
        self.assertEqual(self.adapter.password, self.password)
        self.assertEqual(self.adapter.token, self.token)

    def test_views_for_unauthenticated_public_call(self):
        """views should return mock object results"""
        windy = WindyPie(self.mock_adapter)
        views_count = len(windy.views)
        self.assertEqual(views_count, 3)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(CoreTests)
    unittest.TextTestRunner(verbosity=2).run(suite)
