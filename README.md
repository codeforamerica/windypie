#WindyPie
[![Build Status](https://secure.travis-ci.org/codeforamerica/windypie.png?branch=master)](http://travis-ci.org/codeforamerica/windypie)

![WindyPie icon](https://s3.amazonaws.com/rebounds-dev/github/windypie.png) 

A command line API wrapper for Socrata's SODA API inspired by the Ruby [Windy Socrata API wrapper](https://github.com/Chicago/windy) that makes working with the Socrata API easier in ALL Socrata instances (not just your city).

`This is unfinished, BETA software!`

### Why WindyPie?
WindyPie insulates the Socrata developer and client from many of the annoyances of the Socrata [Open Data API 1.0 (SODA 1.0)](http://dev.socrata.com/). There are already a few great SODA API wrappers in existence like the aforementioned Windy for Chicago, this [PHP program for Chicago](https://github.com/pdweinstein/PHP-Wrapper-for-Chicago-s-Data-Portal/blob/master/class.windy.php), and now [Dillo](https://github.com/phillipsj/dillo) which is an Austin, TX specific fork of Windy.

WindyPie is different from these other programs in two significant ways:

1. It uses Python
2. It works for all the Socrata servers because the host is configurable instead of hardcoded

Although WindyPie is pretty handy for pulling down Socrata views and manipulating their data, we are still very much in Beta so **feature requests, issue reports, and pull requests are very much appreciated**. Also, with SODA 2.0 from Socrata on the horizon, there are plans to modify this library significantly to take advantage of the new, planned, cleaner API.


Installation Instructions
-------------------------
### No Brainer Package Install
Just install using pip:

    $ pip install WindyPie

### Use the Source
These instructions assume that you have git (and GitHub), Python, and [virtualenvwrapper](http://www.doughellmann.com/projects/virtualenvwrapper/). Install them on your development environment if you have not done so already before continuing. If you are on a Mac, you should be able to use [Homebrew](http://mxcl.github.com/homebrew/) to install almost everything you need. Ubuntu users can use [apt-get](https://help.ubuntu.com/8.04/serverguide/C/apt-get.html). For reference, this applications works and was tested with the following software versions:
Python 2.7

First, using virtualenvwrapper, create a working directory with mkvirtualenv and cdvirtualenv into it. Then, clone this repo:

    $ git clone https://github.com/codeforamerica/windypie
    $ cd windypie

This application uses a submodule for [socrata python](https://github.com/socrata/socrata-python) to handle actual calls to a socrata instance (the original plan was to attempt to improve this library, too, but we will probably just rewrite it). So, this requirement will be removed in the future but, for now, you must include it by running the following commands:

    $ git submodule init
    $ git submodule update

This pulls a forked socrata python repo from cfa's github into your dev environment.

Usage Instructions
-------------------------
#### A View to a Property

In your browser, go to [Chicago's data portal](https://data.cityofchicago.org/) and find a view that you fancy. I, for one, would like to know where the Police Stations are in Chicago: [https://data.cityofchicago.org/Public-Safety/Police-Stations/z8bn-74gv](https://data.cityofchicago.org/Public-Safety/Police-Stations/z8bn-74gv). Have a look at that view in Socrata - nice, but it's not in our console window so who cares about it? Let's fix that problem.

Fire up a python interpreter and then type:

    $ from windypie import WindyPie
    $ wp = WindyPie('https://data.cityofchicago.org')

Then, find the Police Stations view with the find_by_id syntax (note: the view id was taken from the URL of the view itself)

    $ view = wp.views.find_by_id('z8bn-74gv')
    
On the Socrata view page, we can see the name of the view is "Police Stations", we can also get the same view as above with the friendlier name value:

    $ view = wp.views.find_by_name('Police Stations')
    
One way or another, we've got our view. Let's count the rows:

    $ row_count = len(view.rows)

And the columns:

    $ column_count = len(view.columns)
    
It's important to point out that, although the WindyPie view object's rows and columns hold the same data that Socrata provides, they may not be that useful. This is because Socrata returns back a ton of meta data that is almost always just throw away for a consumer of the data. WindyPie's solution for this is to package everything in an object called a "collection". Let's take a look at that.

Before we examine the collection, note that there is also a friendlier version of columns called "fields". Check it out:

    $ print view.fields
    [u'sid', u'id', u'position', u'created_at', u'created_meta', u'updated_at', u'updated_meta', u'meta', u'district', u'address', u'city', u'state', u'zip', u'website', u'phone', u'fax', u'tty', u'location']
    
Now, let's use the collection property and get the very first row of the view:

    $ first_row = view.collection[0]
    $ print first_row
    {u'website': [u'https://portal.chicagopolice.org/portal/page/portal/ClearPath', None], u'city': u'Chicago', u'fax': None, u'tty': None, u'zip': u'60653', u'district': u'Headquarters', u'created_at': 1331574120, u'updated_meta': u'386464', u'created_meta': u'386464', u'updated_at': 1331574153, u'phone': [None, None], u'state': u'IL', u'meta': u'{\n}', u'location': [u'{"address":"3510 S Michigan Ave Chicago, IL 60653 (41.83086072588734, -87.62330200626332)","city":"","state":"","zip":""}', None, None, None, True], u'sid': 1, u'position': 1, u'id': u'65FCCC12-E3B1-4BB8-8584-71A815E14289', u'address': u'3510 S Michigan Ave'}
    
What if we want to print just the address field? That's easy with WindyPie:

    $ print first_row.address
    3510 S Michigan Ave
    
This is important actually. You'll note that we used dot notation to grab an individual field value for this row. We can do that for any field value that we saw in the print output of view.fields above:

    $ print first_row.website
    [u'https://portal.chicagopolice.org/portal/page/portal/ClearPath', None]
    
    $ print first_row.city
    Chicago
    …
    and so on
    
But what about search you ask? Well, WindyPie has you covered there, too:

    $ zip_collection = view.collection_by_zip('60630')

This will create a subset collection with only rows that have a zip value of 60630. All the same "view.row.property" commands will work on this subset. And again, you can search for any value in any field from the fields list in the view. WindyPie dynamically responds to your "collection_by_*(value)" queries!

#### Chile, Armadillos, and Rodeos!

This is all great for Chicago and all. But, what about San Francsico, New Orleans, and Austin? WindyPie is your passport to all these fabulous locations. So, let's go to [Austin, TX](https://data.austintexas.gov/)!

    $ wp = WindyPie('https://data.austintexas.gov')
    
Looking at Austin's data portal in the browser, it seems like Restaurant Inspection Scores might be interesting: [https://data.austintexas.gov/dataset/Restaurant-Inspection-Scores/ecmv-9xxi]( https://data.austintexas.gov/dataset/Restaurant-Inspection-Scores/ecmv-9xxi). Let's load that view:
 
    $ view = wp.views.find_by_name('Restaurant Inspection Scores')
    
That took a few seconds to return, how much data did we just download?

    $ len(view.collection) 
    20324 <- that's a lot!
    
With so much data, we decide we only want to deal with places that have perfect inspections:

    $ perfect = view.collection_by_score('100')
    $ len(perfect)
    3194 <- that's better
    
In any case, there is a lot you can do with the beta version of WindyPie. We are planning a lot more features including better search and the ability to upload files, too. Stay tuned. 

Finally, WindyPie software is tested and the tests are really the best documentation. Check out the [tests file](https://github.com/codeforamerica/windypie/blob/master/tests.py) in this repo for details.
    







