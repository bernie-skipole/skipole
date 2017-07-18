####### SKIPOLE WEB FRAMEWORK #######
#
# edittextblocks.py of skilift package  - functions for editing textblocks
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


"""Functions for editing textblocks"""

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


def textref_exists(textref, project):
    "Return True if textref exists"
    proj = skiboot.getproject(project)
    if proj is None:
        return False
    return proj.textblocks_textref_exists(textref)


def get_textrefs(project):
    "Return list of textrefs"
    proj = skiboot.getproject(project)
    if proj is None:
        return []
    return proj.textblocks_get_textrefs()


def get_textref_languages(project):
    "Return a dictionary {textref: [languages],...}"
    proj = skiboot.getproject(project)
    if proj is None:
        return {}
    return proj.textrefs.copy()

def get_exact_text(textref, language, project):
    "Get text with given textref and language, gets exact value, does not seek nearest, if not found return None"
    proj = skiboot.getproject(project)
    if proj is None:
        return
    textblocks = proj.textblocks
    if (textref,language) in textblocks:
        return textblocks[(textref,language)]
    
def set_text(text, textref, language, project):
    "Set text into textblock"
    proj = skiboot.getproject(project)
    if proj is None:
        return
    proj.textblocks_set_text(text, textref, language)


def del_text(textref, language, project):
    "Deletes one textblock:language"
    proj = skiboot.getproject(project)
    if proj is None:
        return
    proj.textblocks_del_text(textref, language)


def del_textblock(textref, project):
    "Deletes all textblocks with this language"
    proj = skiboot.getproject(project)
    if proj is None:
        return
    proj.textblocks_del_textblock(textref)


def copy_textblock(sourceref, destinationref, project):
    "Copies textblock from source to destination"
    proj = skiboot.getproject(project)
    if proj is None:
        return
    proj.textblocks_copy(sourceref, destinationref)
