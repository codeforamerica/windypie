import ConfigParser
from socrata_python.Socrata import *

""" 
WindyPie is a Python module that allows you to easily interact with the City of Chicago's Data Portal
"""

class WindyPie:
    """Wraps all interaction with Socrata API"""
    def __init__(self, socrata_adapter):
        self.adapter = socrata_adapter

    @property
    def views(self):
        """list of views"""
        return self.adapter.get_views()

class SocrataPythonAdapter:
    """Manage working with Socrata's odd python library until it is rewritten"""
    def __init__(self, url, user='', password='', token=''):
        self.url = url
        self.user = user
        self.password = password 
        self.token = token
        self.set_configuration()

    def get_views(self):
        """polls through all available views in the socrata db and returns thier ids in a list"""
        dataset = Dataset(self.config)
        #XXX this is a blocking call, polling 200 at a time could take time to complete!
        return dataset.find_datasets({'limit': 200}, 1)

    def set_configuration(self):
        self.config = ConfigParser.ConfigParser()
        self.config.add_section('credentials')
        self.config.add_section('server')
        self.config.set('credentials', 'app_token', self.token)
        self.config.set('credentials', 'user', self.user)
        self.config.set('credentials', 'password', self.password)
        self.config.set('server', 'host', self.url)
