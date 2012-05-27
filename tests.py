import sys
import unittest
import json
from mock import Mock
from mock import MagicMock

from windypie.windypie import WindyPie
from windypie.windypie import SocrataPythonAdapter

'''
Unit tests for WindyPie module

Copyright (C) 2012, Code for America
This is open source software, released under a standard 2-clause
BSD-style license; see the file LICENSE for details.
'''

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

    def test_default_init_with_no_adapter_passed_in(self):
        '''if no socrata adapter is passed in then one should be created'''
        windy = WindyPie(self.valid_url)
        self.assertEqual(windy.views._adapter.url, self.valid_url)

    def test_get_view_by_id(self):
        '''should return a distinct view for a given id if that id exists'''
        mock_adapter = Mock()
        mock_adapter.find_by_id.return_value = self.test_view_data
        windy = WindyPie(socrata_adapter=mock_adapter)
        # get a specific view
        view = windy.views('z8bn-74gv')
        # counts of "raw" socrata data are as expected
        self.assertEqual(len(view.rows), 24)
        self.assertEqual(len(view.columns), 18)
        # the "WindyPie" version of the data, formatted in a list of python dicts
        self.assertEqual(len(view.collection), 24)
        expected_fields = ['sid', 'id', 'position', 'created_at', \
                           'created_meta', 'updated_at', 'updated_meta', \
                           'meta', 'district', 'address', 'city', \
                           'state', 'zip', 'website', 'phone', \
                           'fax', 'tty', 'location']
        # make sure it has the right fields
        self.assertEqual(view.fields, expected_fields)
        # filter the collection on a specific id
        id_collection = view.collection_by_id('65FCCC12-E3B1-4BB8-8584-71A815E14289')
        self.assertEqual(len(id_collection), 1)
        self.assertEqual(id_collection[0].id, '65FCCC12-E3B1-4BB8-8584-71A815E14289')
        # we can filter on any field (it's dynamic!), let's try position
        position_collection = view.collection_by_position('6')
        self.assertEqual(len(position_collection), 1)
        self.assertEqual(position_collection[0].position, '6')
        # and address
        address_collection = view.collection_by_address('5701 W Madison St')
        self.assertEqual(len(address_collection), 1)
        self.assertEqual(address_collection[0].address, '5701 W Madison St')
        # and, for good measure, let's filter by zip to see if more than one row has the same value
        zip_collection = view.collection_by_zip('60630')
        self.assertEqual(len(zip_collection), 2) # (there are 2 with the same zip)

    def test_get_views_by_name(self):
        '''should return all views with view_name in the name field'''
        mock_adapter = Mock()
        mock_adapter.query_views.return_value = self.test_views_named_police_stations 
        windy = WindyPie(socrata_adapter=mock_adapter)
        police_station_views = windy.views(view_name='Police Stations')
        self.assertEqual(len(police_station_views), 3)
        self.assertEqual(police_station_views[0]['id'], 'z8bn-74gv')

    def test_get_all_views(self):
        '''should return all available views when given no id or filters'''
        mock_adapter = Mock()
        mock_adapter.query_views.return_value = self.test_all_views
        windy = WindyPie(socrata_adapter=mock_adapter)
        all_views = windy.views()
        self.assertEqual(len(all_views), 50)

    def test_version(self):
        self.assertEqual(WindyPie(None).version, '0.0.3')

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(CoreTests)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    # this is not required but allows for custom exit codes and analysis fo failures
    if len(result.failures) > 0:
        print 'falures count %s' % len(result.failures)
        sys.exit(1)
