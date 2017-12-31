####### SKIPOLE WEB FRAMEWORK #######
#
# editpage.py of skilift package  - functions for editing a page
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


"""Functions for editing a page"""

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


def _get_page(project, pagenumber):
    """On success return (deep copy of page, empty string)
       on failure return (None, failure string)"""
    if not project_loaded(project, error_if_not=False):
        return None, "Given project is not loaded"
    if not isinstance(pagenumber, int):
        return None, "Given pagenumber is not an integer"
    ident = skiboot.Ident.to_ident((project, pagenumber))
    if ident is None:
        return None, "Invalid project, pagenumber"
    page = skiboot.from_ident(ident, project, import_sections=False)
    if page is None:
        return None, "Invalid Page"
    if page.page_type == 'Folder':
        return None, "Item is not a page"
    return page, ""


def pagechange(project, pagenumber):
    "Returns None if pagenumber is not found (or is a folder), otherwise returns the page change uuid"
    # raise error if invalid project
    project_loaded(project)
    info = item_info(project, pagenumber)
    if not info:
        return
    if info.item_type == "Folder":
        return
    return info.change


def rename_page(project, pagenumber, newname):
    "rename this page, return None on success, error message on failure"
    if not newname:
        return "No new page name given"
    # get a copy of the page, which can have a new name set
    # and can then be saved to the project
    page, error_message = _get_page(project, pagenumber)
    if page is None:
        return error_message
    editedproj = skiboot.getproject(project)
    if editedproj is None:
        return "Project not loaded"
    # Rename the page
    page.name = newname
    # And save this page copy to the project
    try:
        editedproj.save_page(page)
    except ServerError as e:
        return e.message


def delete_page(project, pagenumber):
    "delete this page, return None on success, error message on failure"
    page, error_message = _get_page(project, pagenumber)
    if page is None:
        return error_message
    editedproj = skiboot.getproject(project)
    if editedproj is None:
        return "Project not loaded"
    # Delete the page
    try:
        # delete the page from the project
        editedproj.delete_item(page.ident)
    except ServerError as e:
        return e.message


def del_item(project, pagenumber, location_string, location_integers):
    "Deletes the item"
    page, error_message = _get_page(project, pagenumber)
    if page is None:
        raise ServerError(message=error_message)
    if (page.page_type != 'TemplatePage') and (page.page_type != 'SVG'):
        raise ServerError(message = "Invalid page")
    editedproj = skiboot.getproject(project)
    if editedproj is None:
        raise ServerError(message = "Project not loaded")
    if location_string == 'body':
        top = page.body
    elif location_string == 'head':
        top = page.head
    elif location_string == 'svg':
        top = page.svg
    else:
        raise ServerError(message="Given location_string is invalid")
    # remove the item
    try:
        top.del_location_value(location_integers)
    except:
        raise ServerError(message="Unable to delete item")
    # And save this page copy to the project
    editedproj.save_page(page)


def move_item(project, pagenumber, location_string, from_location_integers, to_location_integers):
    """Move an item in the given page from one spot to another, defined by it
       location_string, being head, body or svg, and location integers"""
    page, error_message = _get_page(project, pagenumber)
    if page is None:
        raise ServerError(message=error_message)
    editedproj = skiboot.getproject(project)
    if editedproj is None:
        raise ServerError(message="Project not loaded")
    if to_location_integers == from_location_integers:
        # no movement
        return
    up = False
    i = 0
    while True:
        if to_location_integers[i] < from_location_integers[i]:
            up = True
            break
        if to_location_integers[i] > from_location_integers[i]:
            # up is False
            break
        # so this digit is the same
        i += 1
        if len(to_location_integers) == i:
            up = True
            break
    if up:
        # move in the upwards direction
        #    delete it from original location
        #    insert it into new location
        try:
            # get top part such as head, body, svg
            top_part = page.get_part(location_string, ())
            # get the part at from_location_integers
            part = top_part.get_location_value(from_location_integers)
            # delete part from top part location
            top_part.del_location_value(from_location_integers)
            # and insert it in the new location
            top_part.insert_location_value(to_location_integers, part)
        except:
            raise ServerError(message="Unable to move item")
    else:
        # move in the downwards direction
        #    insert it into new location
        #    delete it from original location
        try:
            # get top part such as head, body, svg
            top_part = page.get_part(location_string, ())
            # get the part at from_location_integers
            part = top_part.get_location_value(from_location_integers)
            # and insert it in the new location
            top_part.insert_location_value(to_location_integers, part)
            # delete part from current location
            top_part.del_location_value(from_location_integers)
        except:
            raise ServerError(message="Unable to move item")
    # And save this page copy to the project
    editedproj.save_page(page)



