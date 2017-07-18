####### SKIPOLE WEB FRAMEWORK #######
#
# editsection.py of skilift package  - functions for editing a section
#
# This file is part of the Skipole web framework
#
# Date : 20160509
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


"""Functions for editing a section"""

import sys, traceback

from ..ski import skiboot
from ..ski.excepts import ServerError

from . import project_loaded

def _raise_server_error(message=''):
    "Raises a ServerError, and if debug mode on, adds taceback to message"
    if skiboot.get_debug():
        # append traceback to message
        if message:
            message += "/n"
        else:
            message = ''
        exc_type, exc_value, exc_traceback = sys.exc_info()
        str_list = traceback.format_exception(exc_type, exc_value, exc_traceback)
        for item in str_list:
            message += item
    raise ServerError(message)


def sectionchange(project, section_name):
    "Returns None if section_name is not found, otherwise returns the integer section change number"
    # raise error if invalid project
    project_loaded(project)
    if not isinstance(section_name, str):
         raise ServerError(message="Given section_name is invalid")
    proj = skiboot.getproject(project)
    section = proj.section(section_name, makecopy=False)
    if section is None:
        return
    return section.change
