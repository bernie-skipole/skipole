
"""A WSGI application generator

skilift is an associated python package used to develop an application.

Typically a developer's PC would have both the skilift and the skipole Python packages installed. Skilift includes a development web server and provides a web admin interface, which together with your own code and the skipole functions, enables the developer to create a WSGI application.

Once created, your application and its support files can be moved to your deployment server, which also needs a WSGI compatible web server, and the skipole package. 

The deployment server does not need the skilift application.

Skipole and skilift require python 3.8 or later, and can be installed with:

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

widget_modules() - Return a tuple of widget module names

widgets_in_module(module_name) - Returns a tuple of widget names present in the module


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

proj_ident - project identifier, normally None which auto sets it to the PROJECT value

You would typically define your functions, and then create an instance:

my_application = WSGIApplication(project=PROJECT,
                                 projectfiles=PROJECTFILES,
                                 proj_data=PROJ_DATA,
                                 start_call=start_call,
                                 submit_data=submit_data,
                                 end_call=end_call,
                                 url="/",
                                 proj_ident=None)

If the argument proj_ident is left at its default None value, then it will be automatically
set to the project name. However it can be set to a different string here which may be useful
if multiple instances of this project are to be created and added to a parent 'root' project.
Each unique proj_ident will then define each of the sub applications.

This my_application is then a callable WSGI application.

The WSGIApplication class has method:

add_project(self, proj, url, check_cookies=None) - adds other projects to the 'root' project.

Where proj is another instance of a WSGIApplication and will be served at the path
given by argument url.

The optional check_cookies argument can be set to a function which you would create, with signature:
def my_check_cookies_function(received_cookies, proj_data):
Before the call is routed to the subapplication, your my_check_cookies_function is called, with the
received_cookies dictionary, and with your application's proj_data dictionary. If your function
returns None, the call proceeds unhindered to the subapplication. If however your function returns
an ident tuple, of the form (proj_ident, pagenumber), then the call is routed to that page instead.

The skis module has the function makeapp() which creates a project providing needed javascript
files which should be added to your application, for example:

from skipole import skis
skis_application = skis.makeapp()
my_application.add_project(skis_application, url='/lib')

Which causes the skis project to be served at /lib.

"""

import sys, traceback, inspect, pkgutil

from functools import wraps
from importlib import import_module

from .ski import skiboot, widgets

from .ski.project_class_definition import SkipoleProject, PageData, SectionData
from .ski.excepts import ValidateError, ServerError, GoTo, FailPage, ServeFile

version = skiboot.version()


__all__ = ['WSGIApplication', 'ValidateError', 'ServerError', 'GoTo', 'FailPage', 'ServeFile',
           'set_debug', 'use_submit_list', 'version', 'PageData', 'SectionData', 'widget_modules', 'widgets_in_module']


class WSGIApplication(object):
    """The WSGIApplication - an instance being a callable WSGI application"""

    def __init__(self, project, projectfiles, proj_data={}, start_call=None, submit_data=None, end_call=None, url="/", proj_ident=None):
        """An instance of this class is a callable WSGI application.

Arguments are:

project - the project name

projectfiles - the directory containing your projects

proj_data - an optional dictionary, passed as an attribute of skicall,
            which is an object passed to your functions during the progress of a call

start_call - a function you should create, called at the start of a call

submit_data - a function you should create, called by responders

end_call - a function you should create, called at the end of the call, prior to returning the page

url - path where this project will be served, typically '/'

proj_ident - generally set to None, in which case it will be auto set to the project name
"""
        self._skipoleproject = SkipoleProject(project, projectfiles, proj_data, start_call, submit_data, end_call, url, proj_ident)


    @property
    def project(self):
        """The project name"""
        return self._skipoleproject.proj_name

    @property
    def proj_ident(self):
        """The project ident"""
        return self._skipoleproject.proj_ident

    @property
    def projectfiles(self):
        """The projectfiles path"""
        return self._skipoleproject.projectfiles

    @property
    def proj_data(self):
        """The proj_data dictionary"""
        return self._skipoleproject.proj_data

    @property
    def start_call(self):
        """The start_call function"""
        return self._skipoleproject.start_call

    @property
    def submit_data(self):
        """The submit_data function"""
        return self._skipoleproject.submit_data

    @property
    def end_call(self):
        """The end_call function"""
        return self._skipoleproject.end_call

    @property
    def url(self):
        """This project path"""
        return self._skipoleproject.url

    @property
    def brief(self):
        """This project brief description"""
        return self._skipoleproject.brief

    @property
    def version(self):
        """This project version string"""
        return self._skipoleproject.version

    def __call__(self, environ, start_response):
        "The instance is callable"
        return self._skipoleproject(environ, start_response)

    def add_project(self, proj, url=None, check_cookies=None):
        """Add a sub project to this root project, returns the sub project url
           proj is the sub project WSGIApplication object."""
        return self._skipoleproject.add_project(proj._skipoleproject, url, check_cookies)

    def set_accesstextblocks(self, accesstextblocks):
        """Set an instance of a class which reads and writes TextBlocks. The default class is defined in the skipole.textblocks module,
           which simply stores TextBlocks in memory after reading them from a JSON file, and is not suitable for the dynamic creation
           of TextBlocks. It is sufficient for the single user of Skiadmin, but is essentially read only when serving your pages.
           If required, your own object could be created which should support the methods of the default class, and could read and write
           from your own database. This opens the possibility of dynamic creation and alteration of TextBlocks."""
        self._skipoleproject.textblocks = accesstextblocks


def set_debug(mode):
    "If mode is True, this sets increased debug error messages to be displayed"
    skiboot.set_debug(mode)



# This 'use_submit_list' is available to wrap the submit_data function if required

def use_submit_list(submit_data):
    "Used to decorate submit_data to enable submit_list to define package,module,function"
    @wraps(submit_data)
    def submit_function(skicall):
        "This function replaces submit_data, if skicall.submit_list has two or more elements"
        if not skicall.submit_list:
            # do nothing, simply return the original submit_data
            return submit_data(skicall)
        if len(skicall.submit_list) < 2:
            # do nothing, simply return the original submit_data
            return submit_data(skicall)
        # get the module where submit_data is defined
        sdmodule = inspect.getmodule(submit_data)
        if sdmodule.__name__ == "__main__":
            # absolute path
            submitpath = ".".join(skicall.submit_list[:-1])
            sdpackage = None
        else:
            # relative path
            submitpath = "." + ".".join(skicall.submit_list[:-1])
            sdpackage = sdmodule.__name__
        try:
            submitmodule = import_module(submitpath, sdpackage)
        except Exception as e:
            raise ServerError("Unable to import project module defined as %s in submit list" % (submitpath,)) from e
        # now obtain and run the specified function
        try:
            submitfunc = getattr(submitmodule, skicall.submit_list[-1])
        except Exception as e:
            raise ServerError("submit_list package %s found, but the required function %s is not recognised" % (submitpath, skicall.submit_list[-1])) from e
        return submitfunc(skicall)
    return submit_function


def widget_modules():
    "Return a tuple of widget module names"
    return tuple(name for (module_loader, name, ispkg) in pkgutil.iter_modules(widgets.__path__))


def widgets_in_module(module_name):
    "Returns a tuple of widget names present in the module"
    module = import_module('.ski.widgets.' + module_name, __name__)
    widget_list = []
    for classname,obj in inspect.getmembers(module, lambda member: inspect.isclass(member) and (member.__module__ == module.__name__)):
        widget_list.append(classname)
    return tuple(widget_list)


