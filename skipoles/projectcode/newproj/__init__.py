"""
This package will be called by the Skipole framework to access your data.
"""


# These exception classes are available to be imported

from .. import FailPage, GoTo, ValidateError, ServerError

# This optional decorator function can be used to wrap submit_data if required
from .. import use_submit_list

##############################################################################
#
# Your code needs to provide your own version of the following functions
#
##############################################################################


def start_project(project, projectfiles, path, option):
    """On a project being loaded, and before the wsgi service is started, this is called once,
       Note: it may be called multiple times if your web server starts multiple processes.
       This function should return a dictionary (typically an empty dictionary if this value is not used).
       Can be used to set any initial parameters, and the dictionary returned will be passed as
       the attribute 'skicall.proj_data'."""
    proj_data = {}
    return proj_data


def start_call(called_ident, skicall):
    "When a call is initially received this function is called."
    return called_ident


# if this submit_data function is decorated with use_submit_list, the skicall.submit_list attribute will be used to specify
# the module and function (or package, module and function) to use when submit_data is requested
# If skicall.submit_list is empty, or only has one element, then this submit_data function will be called

# if not decorated, then this function is called, and the skicall.submit_list attribute could be used in any other way you prefer

# @use_submit_list
def submit_data(skicall):
    "This function is called when a Responder wishes to submit data for processing in some manner"
    return


def end_call(page_ident, page_type, skicall):
    """This function is called at the end of a call prior to filling the returned page with skicall.page_data,
       it can also return an optional session cookie string."""
    return
