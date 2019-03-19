####### SKIPOLE WEB FRAMEWORK #######
#
# __init__.py  - The Skipole web site builder
#
# This file is part of the Skipole web framework
#
# Date : 20130205
#
# Author : Bernard Czenkusz
# Email  : bernie@skipole.co.uk
#
#
#   Copyright 2013 Bernard Czenkusz
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import sys, traceback

from functools import wraps
from importlib import import_module

from .ski import skiboot

from .ski.project_class_definition import WSGIApplication
from .ski.excepts import ValidateError, ServerError, GoTo, FailPage

version = skiboot.version()


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
            submitmodule = import_module(submitpath, __name__)
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



