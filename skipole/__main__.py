
# If called using 
#
# python3 -m skipole
#
#

import sys

from . import version


if len(sys.argv) == 2:
    # if called with "python3 -m skipole --version"
    if sys.argv[1] == "--version":
        print(version)
        sys.exit(0)

print(f"""skipole version {version}

skipole is a WSGI application generator.

skilift is an associated python package used to develop an application.

Typically a developer's PC would have both the skilift and the skipole Python packages installed. Skilift includes a development web server and provides a web admin interface, which together with your own code and the skipole functions, enables the developer to create a WSGI application.

Once created, your application and its support files can be moved to your deployment server, which also needs a WSGI compatible web server, and the skipole package. 

The deployment server does not need the skilift application.

Skipole and skilift require python 3.6 or later, and can be installed with:

python3 -m pip install skipole

python3 -m pip install skilift


skilift
-------

To generate a new project, and use a web admin interface to develop it, the package skilift is required.

skilift can be run from the command line with the python -m option

Usage is

python3 -m skilift mynewproj /path/to/projectfiles

Which creates a directory /path/to/projectfiles
containing sub directory mynewproj - containing project data, and file
mynewproj.py where your code will be developed.

You should replace 'mynewproj' with your preferred name for a new project.

The path "/path/to/projectfiles" is the path to a directory where you will
develop your project. Multiple projects can be created in one 'projectfiles'
directory, or you could have multiple such directories holding different
projects.

If mynewproj already exists in the directory, it will not be changed.

You should then inspect the file

/path/to/projectfiles/mynewproj.py

where your code will be developed.


skipole
-------

skipole is intended to be imported, if it is run using

python3 -m skipole

this text is displayed.

If it is run using

python3 -m skipole --version

Then a version string is displayed.

When imported skipole makes the following available:

version - a version string of the form a.b.c

WSGIApplication - an instance of this class is a callable WSGI application (see below)

set_debug(mode) - a function to turn on debugging (if mode is True), or off (if mode is False)

use_submit_list - is available to optionally wrap the user defined submit_data function
                  Enables a responder 'submit list' to define package,module,function to
                  be called as the responder's submit_data function, where package,module
                  is relative to the users code.

PageData - An instance of this class is used to update page widgets.

SectionData - An instance of this class is used to update section widgets


Exceptions
----------

These are also provided, and can be raised within the users code:

ValidateError - returns the project validation error page

ServerError - returns the project server error page

GoTo - diverts the call to another page

FailPage - diverts the call to the calling Responder's 'Fail page'

ServeFile - sends a static server file to the client browser


WSGIApplication
---------------

An instance of this class should be created, and is a callable WSGI application.

The WSGIApplication has the following arguments which should be provided to create
an instance:

PROJECT - the project name

PROJECTFILES - the directory containing your projects

PROJ_DATA - An optional dictionary you may wish to provide

start_call - a function you should create, called at the start of a call

submit_data - a function you should create, called by responders

end_call - a function you should create, called at the end of the call, prior to returning the page

url - path where this project will be served, typically '/'

You would typically define your functions, and then create an instance:

my_application = WSGIApplication(project=PROJECT,
                                 projectfiles=PROJECTFILES,
                                 proj_data=PROJ_DATA,
                                 start_call=start_call,
                                 submit_data=submit_data,
                                 end_call=end_call,
                                 url="/")

This my_application is then a callable WSGI application.

The WSGIApplication class has method:

add_project(self, proj, url) - adds other projects to the 'root' project.

Where proj is another instance of a WSGIApplication and will be served at the path
given by argument url.

The skis module has the function makeapp() which creates a project providing needed javascript
files which should be added to your application, for example:

from skipole import skis
skis_application = skis.makeapp()
my_application.add_project(skis_application, url='/lib')

Which causes the skis project to be served at /lib.

""")


