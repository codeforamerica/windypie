from socrata_python.Socrata import *
import ConfigParser
import inspect
import pymongo
from pymongo import Connection

def socrata_to_mongo(host, view_id, mongo_table_name):
    config = ConfigParser.ConfigParser()
    config.add_section('credentials')
    config.add_section('server')
    config.set('credentials', 'app_token', '3DS3oNv6SDpZcZM18XtHSAdMm')
    config.set('credentials', 'user', '3DS3oNv6SDpZcZM18XtHSAdMm')
    config.set('credentials', 'password', '3DS3oNv6SDpZcZM18XtHSAdMm')
    config.set('server', 'host', host)

    dataset = Dataset(config) 
    connection = Connection()
    db = connection['socrata']
    
    view_detail = dataset.find_view_detail(view_id)
    columns = view_detail['meta']['view']['columns']
    print 'there are {0} columns'.format(len(columns))
    fieldNames = []
    for column in columns:
        fieldNames.append(column['fieldName'])
    for row in view_detail['data']:
        document = {}
        for i in range(0,len(row)):
            document[fieldNames[i]] = row[i]
        # insert into mongo
        db[mongo_table_name].save(document)

socrata_to_mongo('http://data.sfgov.org', 'tmnf-yvry', 'sf_crime')

#config = ConfigParser.ConfigParser()
#config.add_section('credentials')
#config.add_section('server')
#config.set('credentials', 'app_token', '3DS3oNv6SDpZcZM18XtHSAdMm')
#config.set('credentials', 'user', '3DS3oNv6SDpZcZM18XtHSAdMm')
#config.set('credentials', 'password', '3DS3oNv6SDpZcZM18XtHSAdMm')
#config.set('server', 'host', 'http://data.cityofchicago.org')
#
#dataset = Dataset(config)
#
## stub views.count
#views = dataset.find_datasets({'limit': 200}, 1)
#print 'found {0} views!'.format(len(views))
#print "first view id = {0}".format(views[0]['view']['id'])
#print "first view id = {0}".format(views[0]['view']['name'])
#
## stub print column names for a view
#view_id = views[0]['view']['id']
#view_detail = dataset.find_view_detail(view_id)
#columns = view_detail['meta']['view']['columns']
#print 'there are {0} columns'.format(len(columns))
#fieldNames = []
#for column in columns:
#    fieldNames.append(column['fieldName'])
#
#connection = Connection()
#db = connection['socrata']
#
## stub see all rows for a view
#print 'there are {0} rows'.format(len(view_detail['data']))
#for row in view_detail['data']:
#    document = {}
#    for i in range(0,len(row)):
#        document[fieldNames[i]] = row[i]
#    # insert into mongo
#    db[view_id].save(document)
