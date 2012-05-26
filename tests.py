import unittest
import json
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
        '''load test json into memory for mock responses'''
        f = open('fixtures/view_z8bn-74gv.json', 'r')
        self.test_view_data = json.loads(f.read())
        f.close()
        f = open('fixtures/views_named_police_stations.json', 'r')
        self.test_views_named_police_stations = json.loads(f.read())
        f.close()
        f = open('fixtures/views.json', 'r')
        self.test_all_views = json.loads(f.read())
        f.close()

    def test_socrata_python_adapter_init(self):
        '''should init with url, user, password, and token'''
        self.assertEqual(self.adapter.url, self.valid_url)
        self.assertEqual(self.adapter.user, self.user)
        self.assertEqual(self.adapter.password, self.password)
        self.assertEqual(self.adapter.token, self.token)

    def test_get_view_by_id(self):
        '''should return a distinct view for a given id if that id exists'''
        mock_adapter = Mock()
        mock_adapter.find_by_id.return_value = self.test_view_data
        windy = WindyPie(mock_adapter)
        view = windy.views('z8bn-74gv')
        self.assertEqual(len(view.rows), 24)

    def test_get_views_by_name(self):
        '''should return all views with view_name in the name field'''
        mock_adapter = Mock()
        mock_adapter.query_views.return_value = self.test_views_named_police_stations 
        windy = WindyPie(mock_adapter)
        police_station_views = windy.views(view_name='Police Stations')
        self.assertEqual(len(police_station_views), 3)
        self.assertEqual(police_station_views[0]['id'], 'z8bn-74gv')

    def test_get_all_views(self):
        '''should return all available views when given no id or filters'''
        mock_adapter = Mock()
        mock_adapter.query_views.return_value = self.test_all_views
        windy = WindyPie(mock_adapter)
        all_views = windy.views()
        self.assertEqual(len(all_views), 50)

    def test_version(self):
        self.assertEqual(WindyPie(None).version, '0.0.1')

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(CoreTests)
    unittest.TextTestRunner(verbosity=2).run(suite)
