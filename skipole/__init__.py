
"""A WSGI application generator

The package makes the following available:

version - a version string of the form a.b.c

WSGIApplication - an instance of this class is a callable WSGI application (see below)

set_debug(mode) - a function to turn on debugging (if mode is True), or off (if mode is False)

use_submit_list - is available to optionally wrap the user defined submit_data function
                  Enables a responder 'submit list' to define package,module,function to
                  be called as the responder's submit_data function, where package,module
                  is relative to the users code.


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

project - the project name

projectfiles - the directory containing your projects

start_call - a function you should create, called at the start of a call

submit_data - a function you should create, called by responders

end_call - a function you should create, called at the end of the call, prior to returning the page

url - path where this project will be served, typically '/'

The WSGIApplication class has the methods:

__call__(self, environ, start_response) - which sets the instance as callable

set_accesstextblocks(self, accesstextblocks) - Set an instance of a class which reads and writes TextBlocks.

Normally not used, as a default class (defined in the skipole.textblocks module) is used. If required, your
own object could be created and set into the WSGIApplication with this method. If you do this, your object
should support the same methods of the default class.

add_project(self, proj, url) - adds other projects to the 'root' project.

Where proj is another instance of a WSGIApplication and will be served at the path
given by argument url. At the minimum, your project should add the 'skis' sub project
which provides needed javascript files. For example:

my_application.add_project(skis_application, url='/lib')

Which causes the skis project to be served at /lib.

Sub-projects (such as skis above) cannot have further sub projects added - all
sub-projects can only be added to the 'root' project.


python3 -m skipole
------------------

skipole can also be run from the command line with the python -m option

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

from collections.abc import MutableMapping

from .ski import skiboot

from .ski.project_class_definition import SkipoleProject
from .ski.excepts import ValidateError, ServerError, GoTo, FailPage

version = skiboot.version()


__all__ = ['WSGIApplication', 'ValidateError', 'ServerError', 'GoTo', 'FailPage', 'set_debug', 'use_submit_list', 'version', 'PageData', 'SectionData']


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


# An instance of this PageData is set into a skicall object to provide data for page widgets

class PageData(MutableMapping):

    page_variables = skiboot.PAGE_VARIABLES

    @classmethod
    def from_dict(cls, pagedict):
        "Returns an instance of this class given a dictionary as produced by the to_dict method"
        pd = cls()
        for key,val in pagedict.items():
            if "/" in key:
                # sectionalias/attribute
                sectionalias,att = key.split("/")
                pd.sections.add(sectionalias)
                pd._page_data[sectionalias, att] = val
            elif ":" in key:
                front,fld = key.split(":")
                if "-" in front:
                    # sectionalias-widget:field
                    sectionalias, widg = front.split("-")
                    pd.sections.add(sectionalias)
                    pd._page_data[sectionalias, widg, fld] = val
                else:
                    # widget:field
                    pd._page_data[front, fld] = val
            else:
                # a single string without / or : must be a page attribute
                pd._page_data[key] = val
        return pd


    def __init__(self):
        "_page_data will become the skicall.page_data when this object is set into skicall"
        self._page_data = {}
        self.sections = set()

    def clear(self):
        self._page_data.clear()
        self.sections.clear()

    def to_dict(self):
        """Returns a dictionary containing the data held in this object, with keys as strings
           possibly useful for storage or caching if this data is to be re-used"""
        # introduce field delimiters / : - 
        pagedict = {}
        for key, val in self._page_data.items():
            if isinstance(key,str):
                # keys are strings - page attributes, leave as strings
                pagedict[key] = val
            elif isinstance(key, tuple):
                if len(key) == 2:
                    if key[0] in self.sections:
                        # keys are (sectionalias, attribute) set as "sectionalias/attribute"
                        pagedict[key[0]+'/'+key[1]] = val
                    else:
                        # or keys are (widgetname, fieldname) set as "widgetname:fieldname"
                        pagedict[key[0]+':'+key[1]] = val
                elif len(key) == 3:
                    # keys will be of the form sectionalias-widgetname:fieldname
                    pagedict[key[0]+'-'+key[1]+':'+key[2]] = val
        return pagedict
        

    def get_section(self, sectionalias):
        "Retrieve a section, if it has not been added to the page, return None"
        if sectionalias not in self.sections:
            # it does not exist
            return None
        s = SectionData(sectionalias)
        for key, val in self._page_data.items():
            if not isinstance(key, tuple):
                continue
            if key[0] == sectionalias:
                if len(key) == 2:
                    s._section_data[key[1]] = val
                else:
                    s._section_data[key[1], key[2]] = val
        return s


    def delete_section(self, sectionalias):
        "Deletes a section"
        if sectionalias not in self.sections:
            return
        self.sections.remove(sectionalias)
        newdict = {}
        for key, val in self._page_data.items():
            if isinstance(key, tuple) and (len(key) >= 2) and (key[0] == sectionalias):
                continue
            newdict[key] = val
        self._page_data = newdict


    def update(self, item):
        "Update with either a two tuple widgfield dictionary or a SectionData object"
        if isinstance(item, SectionData):
            # update from SectionData
            sectionalias = item.sectionalias
            if sectionalias not in self.sections:
                # test no widget clash
                for key in self.keys():
                    if isinstance(key, tuple) and (len(key) == 2) and (sectionalias == key[0]):
                        # sectionalias clashes with a widget
                        raise KeyError
            self._add_section(item)
            return
        if not isinstance(item, dict):
            raise KeyError
        for key in item.keys():
            if not self._valid_widgfield(key):
                raise KeyError
        self._page_data.update(item)


    def _add_section(self, section):
        "Add section data"
        sectionalias = section.sectionalias
        self.sections.add(sectionalias)
        for at, val in section._section_data.items():
            if isinstance(at, str):
                # A section attribute
                if val is None:
                    continue
                self._page_data[sectionalias, at] = val
        # add items from section
        for key,val in section.items():
            self._page_data[sectionalias, key[0], key[1]] = val
                

    def __getattr__(self, name):
        "Get a page attribute from the _page_data dictionary"
        if name not in self.page_variables:
            raise AttributeError
        if name in self._page_data:
            return self._page_data[name]


    def __setattr__(self, name, value):
        "Sets a page attribute"
        if name in self.page_variables:
            if value is None:
                if name in self._page_data:
                    del self._page_data[name]
            else:
                self._page_data[name] = value
            return
        # for all other values
        super().__setattr__(name, value)


    def _valid_widgfield(self, key):
        if not isinstance(key, tuple):
            return False
        if len(key) != 2:
            # All widgfields have a two element tuple as key
            return False
        if key[0] in self.sections:
            # this key name is used as a section alias
            return False
        return True


    def __setitem__(self, key, value):
        if self._valid_widgfield(key):
            if (value is None) and (key in self._page_data):
                del self._page_data[key]
            else:
                self._page_data[key] = value
        else:
            raise KeyError


    def __delitem__(self, key):
        if self._valid_widgfield(key):
            if key in self._page_data:
                del self._page_data[key]
        else:
            raise KeyError


    def __getitem__(self, key):
        if self._valid_widgfield(key):
            return self._page_data[key]
        else:
            raise KeyError


    def __iter__(self):
        page_data = self._page_data
        for key in page_data.keys():
            if self._valid_widgfield(key):
                yield key


    def __len__(self):
        "Returns the number of widgfields associated with the page"
        page_data = self._page_data
        length = 0
        for key in page_data.keys():
            if self._valid_widgfield(key):
                length += 1
        return length


# instances of this SectionData is used with the update method of a PageData object to provide data for sections

class SectionData(MutableMapping):

    section_variables = skiboot.SECTION_VARIABLES

    @classmethod
    def from_dict(cls, sectiondict, sectionalias):
        "Returns an instance of this class given a dictionary as produced by the to_dict method"
        sd = cls(sectionalias)
        newdict = {}
        for key,val in sectiondict.items():
            if not isinstance(key, str):
                raise KeyError
            if "/" in key:
                alias, att = key.split("/")
                # discard alias, as it is to be replaced by sectionalias
                if att not in cls.section_variables:
                    raise KeyError
                newdict[att] = val
            elif ":" in key:
                section_widg, fld = key.split(":")
                if "-" in section_widg:
                    alias,widg = section_widg.split("-")
                    newdict[widg,fld] = val
                else:
                    raise KeyError
            else:
                # not an attribute or widget
                raise KeyError
        # assign newdict to the new class
        sd._section_data = newdict
        return sd


    def __init__(self, sectionalias):
        """sectionalias is the name of this section as set in the page"""
        self._section_data = {}
        self._sectionalias = sectionalias

    def clear(self):
        self._section_data = {}

    def to_dict(self):
        """Returns a dictionary containing the data held in this object, with keys as strings
           possibly useful for storage or caching if this data is to be re-used"""
        # introduce field delimiter :  
        sectiondict = {}
        for key, val in self._section_data.items():
            if isinstance(key,str):
                # keys are strings - section attributes, introduce sectionalias/attribute
                if val is None:
                    continue
                sectiondict[self._sectionalias + "/" + key] = val
            elif isinstance(key, tuple):
                if len(key) == 2:
                    # keys are (widgetname, fieldname) set as "sectionalias-widgetname:fieldname"
                    sectiondict[self._sectionalias + "-" + key[0]+':'+key[1]] = val
        return sectiondict


    def copy(self, newalias):
        "Return a copy of this section with a new sectionalias"
        s = self.__class__(newalias)
        s._section_data = self._section_data.copy()
        return s


    def multiply(self, number):
        """Sets the multiplier to number and returns the given number of SectionData objects
           each with sectionalias of sectionalias_0, sectionalias_1,.. etc"""
        if number <= 1:
            return []
        sectionlist = []
        for n in range(number):
            newalias = self.sectionalias+ "_" + str(n)
            newsection = self.copy(newalias)
            newsection.multiplier = 0
            sectionlist.append(newsection)
        self.multiplier = number
        return sectionlist


    def __getattr__(self, name):
        "Get a section attribute from the _section_data dictionary"
        if name == "sectionalias":
            return self._sectionalias
        if name not in self.section_variables:
            raise AttributeError
        return self._section_data[name]


    def __setattr__(self, name, value):
        "Sets a section attribute"
        if name == '_section_data':
            # this is required to insert values into self._section_data
            super().__setattr__(name, value)
            return
        if name == '_sectionalias':
            # this is required to insert the section name into self._sectionalias
            super().__setattr__(name, value)
            return
        if name not in self.section_variables:
            raise AttributeError
        self._section_data[name] = value


    def _valid_widgfield(self, key):
        if not isinstance(key, tuple):
            return False
        if len(key) != 2:
            # All widgfields have a two element tuple as key
            return False
        return True

    def __setitem__(self, key, value):
        if self._valid_widgfield(key):
            self._section_data[key] = value
        else:
            raise KeyError

    def __delitem__(self, key):
        if self._valid_widgfield(key):
            del self._section_data[key]
        else:
            raise KeyError

    def __getitem__(self, key):
        if self._valid_widgfield(key):
            return self._section_data[key]
        else:
            raise KeyError

    def __iter__(self):
        for key in self._section_data.keys():
            if self._valid_widgfield(key):
                yield key

    def __len__(self):
        "Returns the number of widgfields associated with the section"
        length = 0
        for key in self._section_data.keys():
            if self._valid_widgfield(key):
                length += 1
        return length


