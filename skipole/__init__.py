
"""A WSGI application generator

The package makes the following available:

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


WSGIApplication
---------------

An instance of this class should be created, and is a callable WSGI application.

The WSGIApplication has the following arguments which should be provided to create
an instance:

PROJECT - the project name

PROJECTFILES - the directory containing your projects

PROJ_DATA - An optional dictionary you may whish to provide

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

Sub-projects (such as skis above) cannot have further sub projects added - all
sub-projects can only be added to the 'root' project.


python3 -m skipole
------------------

skipole can be run from the command line with the python -m option

Usage is

python3 -m skipole mynewproj /path/to/projectfiles

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

"""

import sys, traceback, inspect

from functools import wraps
from importlib import import_module

from .ski import skiboot

from .ski.project_class_definition import SkipoleProject, PageData, SectionData
from .ski.excepts import ValidateError, ServerError, GoTo, FailPage, ServeFile

version = skiboot.version()


__all__ = ['WSGIApplication', 'ValidateError', 'ServerError', 'GoTo', 'FailPage', 'ServeFile', 'set_debug', 'use_submit_list', 'version', 'PageData', 'SectionData']


class WSGIApplication(object):
    """The WSGIApplication - an instance being a callable WSGI application"""

    def __init__(self, project, projectfiles, proj_data={}, start_call=None, submit_data=None, end_call=None, url="/"):
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
"""
        self._skipoleproject = SkipoleProject(project, projectfiles, proj_data, start_call, submit_data, end_call, url)


    @property
    def project(self):
        """The project name"""
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



