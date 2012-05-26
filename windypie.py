import ConfigParser
from socrata_python.Socrata import *

'''
WindyPie is a Python module that allows you to easily interact with
all the Socrata Data Portals
'''

class WindyPie(object):
    '''Wraps all interaction with Socrata API'''
    def __init__(self, socrata_adapter):
        self._views = WindyPie.Views(socrata_adapter)
        self._version = '0.0.1'

    @property
    def views(self):
        '''list of views'''
        return self._views

    @property
    def version(self):
        return self._version

    class View(object):
        def __init__(self, data):
            self._data = data

        @property
        def rows(self):
            '''all the objects from a view's data field'''
            return self._data['data']

    class Views(object):
        '''Represents collection of Socrata views'''
        def __init__(self, adapter):
            self._adapter = adapter

        def __call__(self, view_id=None, view_name=None):
            '''Get views from Socrata'''
            if None == view_id:
                return self.query(view_name)
            else:
                return WindyPie.View(self._adapter.find_by_id(view_id))

        def query(self, view_name):
            '''query socrata views table and return based on paramter filter values'''
            params = {}
            if None != view_name:
                params['name'] = view_name
            views = []
            return self._adapter.query_views(params) 

class SocrataPythonAdapter:
    '''Manage working with Socrata's odd python library until it is rewritten'''
    def __init__(self, url, user='', password='', token=''):
        self.url = url
        self.user = user
        self.password = password 
        self.token = token
        self.set_configuration()
        self.dataset = Dataset(self.config)

    def find_by_id(self, view_id):
        '''query socrata instance to return view with passed in id'''
        return self.dataset.find_view_detail(view_id)

    def query_views(self, params={}):
        '''polls through all available views in the socrata db and returns them in a list'''
        #XXX this is a blocking call, polling 200 at a time could take time to complete!
        params['limit'] = 200
        return self.dataset.find_datasets(params, 1)

    def set_configuration(self):
        '''socrata python library uses ConfigParser, so must we'''
        self.config = ConfigParser.ConfigParser()
        self.config.add_section('credentials')
        self.config.add_section('server')
        self.config.set('credentials', 'app_token', self.token)
        self.config.set('credentials', 'user', self.user)
        self.config.set('credentials', 'password', self.password)
        self.config.set('server', 'host', self.url)
