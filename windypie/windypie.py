import ConfigParser
from socrata_python.Socrata import *

'''
WindyPie is a Python module that allows you to easily interact with
ALL the Socrata Data Portals

Copyright (C) 2012, Code for America
This is open source software, released under a standard 2-clause
BSD-style license; see the file LICENSE for details.
'''

class WindyPie(object):
    '''Wraps all interaction with Socrata API'''
    def __init__(self, url=None, socrata_adapter=None):
        if not socrata_adapter:
            socrata_adapter = SocrataPythonAdapter(url)
        self._views = WindyPie.Views(socrata_adapter)
        self._version = '0.0.3'

    @property
    def views(self):
        '''list of views'''
        return self._views

    @property
    def version(self):
        '''return version number of this software'''
        return self._version

    class View(object):
        '''A model object that represents a socrata view'''
        def __init__(self, data):
            self._data = data
            self._field_names = []
            self._collection = self.__init_collection()

        def __init_collection(self):
            '''load raw socrata data into more managable collections of columns and rows'''
            # socrata view meta data is lengthy! we load only the filed (aka column) string
            # values into our fields property
            for column in self.columns:
                self._field_names.append(str(column['fieldName']))
            # socrata rows include only the data, this creates a list of dictionary objects
            # (keyed by field name) so that rows can be output in an easier to manage 
            # format such as json
            document_collection = []
            for row in self.rows:
                document = DotDict() # using DotDict class for dot notation of row fields
                for i in range(0,len(row)):
                    document[self.fields[i]] = str(row[i])
                document_collection.append(document)
            return document_collection

        @property
        def fields(self):
            '''all field name strings from columns'''
            return self._field_names

        @property
        def rows(self):
            '''the list of raw, socrata row objects for the view'''
            return self._data['data']

        @property
        def columns(self):
            '''the list of raw, socrata column objects for the view'''
            return self._data['meta']['view']['columns']

        @property
        def collection(self):
            '''the list of row objects for the view as python dicts'''
            return self._collection

        def __search_for_rows(self, field, value):
            '''find subset of rows with fields equal to value'''
            collection = []
            for row in self.collection:
                if value == row[str(field)]:
                    collection.append(row)
            return collection

        def __getattr__(self, name):
            '''handle requests to search for rows by field name dynamically'''
            # if the request is not in the ballpark then reject it
            if not name.startswith('collection_by_'):
                raise AttributeError
            def method(*args):
                field = name[len('collection_by_'):]
                return self.__search_for_rows(field, args[0])
            return method

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

class DotDict(dict):
    '''
    dict that supports dot notation for elements
    this is a cherry pick of more comprehensive solutions
    see: https://github.com/vkuznet/DotDict
    '''
    def __getattr__(self, attr):
        return self.get(attr, None)
    __setattr__= dict.__setitem__
    __delattr__= dict.__delitem__
