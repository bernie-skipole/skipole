####### SKIPOLE WEB FRAMEWORK #######
#
# Directs the responder to user data functions
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


"""Converts idents to tuples, and directs calls to the correct
   project code"""

import sys, traceback, re, os

#if sys.version_info[0] == 3 and sys.version_info[1] < 4:
#    from imp import reload
#else:
#    from importlib import reload

from importlib import reload, import_module

# a search for anything none-alphanumeric and not an underscore
_AN = re.compile('[^\w]')

from ..ski.excepts import FailPage, GoTo, ValidateError, ServerError
from ..ski import skiboot

# as project code is imported, it is stored in _PROJECTS
_PROJECTS = {}

# The textblocks modules are installed in _TEXTBLOCKS
_TEXTBLOCKS = {}


# set this projectcode directory into skiboot
skiboot.set_projectcode(os.path.dirname(os.path.realpath(__file__)))


def _import_project_code(proj_ident):
    global _PROJECTS
    try:
        if proj_ident  not in _PROJECTS:
            _PROJECTS[proj_ident] = import_module("."+proj_ident, __name__)
    except:
        if skiboot.get_debug():
            exc_type, exc_value, exc_traceback = sys.exc_info()
            str_list = traceback.format_exception(exc_type, exc_value, exc_traceback)
            message = ''
            for item in str_list:
                message += item
            raise ServerError(message)
        raise ServerError("Unable to import project code")
    return _PROJECTS[proj_ident]


def make_AccessTextBlocks(project, projectfiles, default_language):
    "Returns an AccessTextBlocks object"
    global _TEXTBLOCKS
    try:
        if project  not in _TEXTBLOCKS:
            _TEXTBLOCKS[project] = import_module("."+project+".textblocks", __name__)
    except:
        if skiboot.get_debug():
            exc_type, exc_value, exc_traceback = sys.exc_info()
            str_list = traceback.format_exception(exc_type, exc_value, exc_traceback)
            message = ''
            for item in str_list:
                message += item
            raise ServerError(message)
        raise ServerError("Unable to import %s.textblocks" % (project,))
    textblocks_module = _TEXTBLOCKS[project]
    return textblocks_module.AccessTextBlocks(project, projectfiles, default_language)


def code_reload(proj_ident):
    "Re-loads user code"
    global _PROJECTS
    try:
        if proj_ident in _PROJECTS:
            _PROJECTS[proj_ident] = reload(_PROJECTS[proj_ident])
        else:
            _PROJECTS[proj_ident] = import_module("."+proj_ident, __name__)
    except:
        if skiboot.get_debug():
            exc_type, exc_value, exc_traceback = sys.exc_info()
            str_list = traceback.format_exception(exc_type, exc_value, exc_traceback)
            message = ''
            for item in str_list:
                message += item
            raise ServerError(message)
        raise ServerError("Unable to reload module")


def start_project(proj_ident, path, option):
    """On a project being loaded, and before the wsgi service is started, this is called once, and in
          turn calls the appropriate  project start_project function. It can be used to initiate any required service.
          Should return the proj_data dictionary"""
    global _PROJECTS
    if proj_ident  not in _PROJECTS:
        _PROJECTS[proj_ident] = import_module("."+proj_ident, __name__)
    project_code =  _PROJECTS[proj_ident]

    proj_data = project_code.start_project(proj_ident, skiboot.projectfiles(), path, option)
    return proj_data


def start_call(environ, path, proj_ident, ident, caller_ident, received_cookies, ident_data, lang, option, proj_data):
    """Calls the appropriate project start_call function
       ident is the ident of the page being called, could be None if not recognised
       Returns new called_ident, dictionaries 'call_data', 'page_data' and new tuple lang"""

    if not caller_ident:
        tuple_caller_ident = ()
    else:
        tuple_caller_ident = caller_ident.to_tuple()

    if ident is None:
        called_ident = None
    else:
        called_ident = ident.to_tuple()

    if (ident_data is not None) and _AN.search(ident_data):
        ident_data = None
    try:
        project_code = _import_project_code(proj_ident)
        new_called_ident, call_data, page_data, new_lang = project_code.start_call(environ,
                                                                                   path,
                                                                                   proj_ident,
                                                                                   called_ident,
                                                                                   tuple_caller_ident,
                                                                                   received_cookies,
                                                                                   ident_data,
                                                                                   lang,
                                                                                   option,
                                                                                   proj_data)
        # convert returned tuple to an Ident object
        if isinstance(new_called_ident, int):
            new_called_ident = (proj_ident, new_called_ident)
        if isinstance(new_called_ident, tuple):
            new_called_ident = skiboot.make_ident(new_called_ident, proj_ident)
        # could be a label
    except ServerError as e:
        raise e
    except:
        if skiboot.get_debug():
            exc_type, exc_value, exc_traceback = sys.exc_info()
            str_list = traceback.format_exception(exc_type, exc_value, exc_traceback)
            message = ''
            for item in str_list:
                message += item
            raise ServerError(message)
        raise ServerError("Error in start_call")
    return new_called_ident, call_data, page_data, new_lang

def submit_data(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Calls the appropriate submit_data function"
    if not caller_ident:
        tuple_caller_ident = ()
    else:
        tuple_caller_ident = caller_ident.to_tuple()
    proj_ident = ident_list[-1].proj
    this_project = skiboot.getproject(proj_ident)
    if this_project is None:
        raise FailPage()
    # add project name to submit_dict
    submit_dict['project'] = proj_ident
    # add project proj_data to submit_dict
    submit_dict['proj_data'] = this_project.proj_data
    # add project option to submit_dict
    submit_dict['option'] = this_project.option
    # add boolean rootproject flag to submit_dict, True if this is the root project
    submit_dict['rootproject'] = this_project.rootproject
    # add project brief to submit_dict
    submit_dict['brief'] = this_project.brief
    tuple_ident_list = [ ident.to_tuple() for ident in ident_list ]
    try:
        project_code = _import_project_code(proj_ident)
        result = project_code.submit_data(tuple_caller_ident,
                                             tuple_ident_list,
                                             submit_list,
                                             submit_dict,
                                             call_data,
                                             page_data,
                                             lang)
    except (GoTo, FailPage, ServerError, ValidateError) as e:
        raise e
    except:
        message = 'Error in submit_data called by responder ' + str(tuple_ident_list[-1]) + '\n'
        if skiboot.get_debug():
            exc_type, exc_value, exc_traceback = sys.exc_info()
            str_list = traceback.format_exception(exc_type, exc_value, exc_traceback)
            for item in str_list:
                message += item
        raise ServerError(message)
    return result


def end_call(proj_ident, page, call_data, page_data, proj_data, lang):
    """Calls the project end_call function"""
    try:
        project_code = _import_project_code(proj_ident)
        page_ident = page.ident
        if not isinstance(page_ident, tuple):
            page_ident = page_ident.to_tuple()
        session_string = project_code.end_call(page_ident, page.page_type, call_data, page_data, proj_data, lang)
        if session_string:
            # set cookie in target_page
            page.session_cookie = ("Set-Cookie", "%s=%s; Path=%s" % (proj_ident, session_string, skiboot.root().url))
    except GoTo as e:
        raise ServerError("Invalid GoTo exception in end_call")
    except FailPage as e:
        page.show_error([e.errormessage])
    except (ServerError, ValidateError) as e:
        raise e



