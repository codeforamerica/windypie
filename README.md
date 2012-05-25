This is so totally under construction!

Inspired by the Ruby [Windy Socrata API wrapper](https://github.com/Chicago/windy) and the souls of Django ponies.

Installation Instructions
-------------------------
These instructions assume that you have git (and GitHub), Python, [virtualenvwrapper](http://www.doughellmann.com/projects/virtualenvwrapper/). Install them on your development environment if you have not done so already before continuing. If you are on a Mac, you should be able to use [Homebrew](http://mxcl.github.com/homebrew/) to install almost everything you need. Ubuntu users can use [apt-get](https://help.ubuntu.com/8.04/serverguide/C/apt-get.html). For reference, this applications works and was tested with the following software versions:
Python 2.7

First, using virtualenvwrapper, create a working directory with mkvirtualenv and cdvirtualenv into it. Then, clone this repo:

    $ git clone https://github.com/codeforamerica/windypie
    $ cd windypie

This application uses a submodule for [socrata python](https://github.com/socrata/socrata-python) to handle actual calls to a socrata instance (the original plan was to attempt to improve this library, too, but we will probably just rewrite it). So, this requirement will be removed in the future but, for now, you must include it by running the following commands:

    $ git submodule init
    $ git submodule update

This pulls a forked socrata python repo from cfa's github into your dev environment.
