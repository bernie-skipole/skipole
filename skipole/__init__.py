
import sys, traceback

from functools import wraps
from importlib import import_module

from .ski import skiboot

from .ski.project_class_definition import SkipoleProject
from .ski.excepts import ValidateError, ServerError, GoTo, FailPage

version = skiboot.version()


__all__ = ['WSGIApplication', 'ValidateError', 'ServerError', 'GoTo', 'FailPage', 'set_debug', 'use_submit_list', 'version']


class WSGIApplication(object):
    """The WSGIApplication - an instance being a callable WSGI application"""

    def __init__(self, project, projectfiles=None, proj_data={}, start_call=None, submit_data=None, end_call=None, url="/"):
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


    def __call__(self, environ, start_response):
        "Defines this projects callable as the wsgi application"
        return self._skipoleproject(environ, start_response)


    def add_project(self, proj, url=None):
        """Add a sub project to this root project, returns the sub project url
           proj is the sub project WSGIApplication object."""
        return self._skipoleproject.add_project(proj._skipoleproject, url)


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
        submitpath = ".".join(skicall.submit_list[:-1])
        try:
            submitmodule = import_module(submitpath)
        except Exception:
            if skiboot.get_debug():
                exc_type, exc_value, exc_traceback = sys.exc_info()
                str_list = traceback.format_exception(exc_type, exc_value, exc_traceback)
                message = ''
                for item in str_list:
                    message += item
                raise ServerError(message)
            raise ServerError("Unable to import project module defined as %s in submit list" % (submitpath,))
        # now obtain and run the specified function
        try:
            submitfunc = getattr(submitmodule, skicall.submit_list[-1])
        except Exception:
            raise ServerError("submit_list package %s found, but the required function %s is not recognised" % (submitpath, skicall.submit_list[-1]))
        return submitfunc(skicall)
    return submit_function





