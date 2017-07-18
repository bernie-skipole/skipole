####### SKIPOLE WEB FRAMEWORK #######
#
# editfolder.py of skilift package  - functions for editing a folder
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


"""Functions for editing a folder"""

import sys, traceback

from ..ski import skiboot
from ..ski.excepts import ServerError

from . import project_loaded, item_info

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


def _get_folder(project, foldernumber):
    """On success return (deep copy of folder, empty string)
       on failure return (None, failure string)"""
    if not project_loaded(project, error_if_not=False):
        return None, "Given project is not loaded"
    if not isinstance(foldernumber, int):
        return None, "Given foldernumber is not an integer"
    ident = skiboot.Ident.to_ident((project, foldernumber))
    if ident is None:
        return None, "Invalid project, foldernumber"
    folder = skiboot.from_ident(ident, project, import_sections=False)
    if folder is None:
        return None, "Invalid Folder"
    if folder.page_type != 'Folder':
        return None, "Item is not a Folder"
    return folder, ""


def folderchange(project, foldernumber):
    "Returns None if foldernumber is not found (or is a page), otherwise returns the integer folder change number"
    # raise error if invalid project
    project_loaded(project)
    info = item_info(project, foldernumber)
    if not info:
        return
    if info.item_type != "Folder":
        return
    return info.change


def rename_folder(project, foldernumber, newname):
    "rename this folder, return None on success, error message on failure"
    if not newname:
        return "No new folder name given"
    # get a copy of the folder, which can have a new name set
    # and can then be saved to the project
    folder, error_message = _get_folder(project, foldernumber)
    if folder is None:
        return error_message
    if folder.ident.num == 0:
        return "Cannot rename the root folder"
    editedproj = skiboot.getproject(project)
    if editedproj is None:
        return "Project not loaded"
    # Rename the folder
    folder.name = newname
    # And save this folder copy to the project
    try:
        editedproj.save_folder(folder)
    except ServerError as e:
        return e.message



def delete_folder(project, foldernumber):
    "delete this folder, return None on success, error message on failure"
    folder, error_message = _get_folder(project, foldernumber)
    if folder is None:
        return error_message
    editedproj = skiboot.getproject(project)
    if editedproj is None:
        return "Project not loaded"
    if folder.page_type != "Folder":
        return "Invalid folder"
    if folder.ident.num == 0:
        return "Cannot delete the root folder"
    if len(folder):
        return "Cannot delete a folder with contents"
    try:
        # delete the folder from the project
        editedproj.delete_item(folder.ident)
    except ServerError as e:
        return e.message


def set_folder_brief(project, foldernumber, newbrief):
    "set new brief on this folder, return None on success, error message on failure"
    if not newbrief:
        return "No new folder description given"
    # get a copy of the folder, which can have a new brief set
    # and can then be saved to the project
    folder, error_message = _get_folder(project, foldernumber)
    if folder is None:
        return error_message
    editedproj = skiboot.getproject(project)
    if editedproj is None:
        return "Project not loaded"
    # set new folder brief
    folder.brief = newbrief
    # And save this folder copy to the project
    try:
        editedproj.save_folder(folder)
    except ServerError as e:
        return e.message


def set_default_page(project, foldernumber, default_page_name):
    "set new default page on this folder, return None on success, error message on failure"
    # get a copy of the folder
    # which can then be saved to the project
    folder, error_message = _get_folder(project, foldernumber)
    if folder is None:
        return error_message
    editedproj = skiboot.getproject(project)
    if editedproj is None:
        return "Project not loaded"
    if not default_page_name:
        default_page_name = ''
    elif default_page_name not in folder.pages:
        return "The page to set as default has not been found in this folder"
    folder.default_page_name = default_page_name
    # And save this folder copy to the project
    try:
        editedproj.save_folder(folder)
    except ServerError as e:
        return e.message


