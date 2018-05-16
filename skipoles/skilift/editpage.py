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

from ..ski import skiboot
from ..ski.excepts import ServerError

from . import project_loaded, item_info, get_proj_page, del_location_in_page


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


def rename_page(project, pagenumber, pchange, newname):
    "rename this page, return the page change uuid on success, raises ServerError on failure"
    if not newname:
        raise ServerError(message="No new page name given")
    # get a copy of the page, which can have a new name set
    # and can then be saved to the project
    proj, page = get_proj_page(project, pagenumber, pchange)
    # Rename the page
    page.name = newname
    # save the altered page, and return the page.change uuid
    return proj.save_page(page)


def page_description(project, pagenumber, pchange, brief):
    "Set a page brief description"
    if not brief:
        return "No new page name given"
    # get a copy of the page, which can have a new brief set
    # and can then be saved to the project
    proj, page = get_proj_page(project, pagenumber, pchange)
    # Set the page brief
    page.brief = brief
    # save the altered page, and return the page.change uuid
    return proj.save_page(page)


def new_parent(project, pagenumber, pchange, new_parent_number):
    "Gives a page a new parent folder"

    # get a copy of the page, which is to have a new parent folder set
    # and can then be saved to the project
    proj, page = get_proj_page(project, pagenumber, pchange)
    if not isinstance(new_parent_number, int):
        raise ServerError(message="Given new_parent_number is not an integer")
    ident = skiboot.Ident.to_ident((project, new_parent_number))
    if ident is None:
        raise ServerError(message="Invalid project, new_parent_number")
    folder = skiboot.from_ident(ident, project)
    if folder is None:
        raise ServerError(message="Invalid Folder")
    if folder.page_type != 'Folder':
        raise ServerError(message="Item is not a page")
    old_parent = page.parentfolder
    if old_parent == folder:
        raise ServerError(message="Parent folder unchanged?")
    if page.name in folder:
        raise ServerError(message="The folder already contains an item with this name")
    return proj.save_page(page, folder.ident)


def delete_page(project, pagenumber):
    "delete this page, return None on success, error message on failure"
    try:
        proj, page = get_proj_page(project, pagenumber)
        # delete the page from the project
        proj.delete_item(page.ident)
    except ServerError as e:
        return e.message



def del_location(project, pagenumber, pchange, location):
    "Deletes the item at the given location in the page, returns new pchange"
    return del_location_in_page(project, pagenumber, pchange, location)


def move_location(project, pagenumber, from_location, to_location):
    """Move an item in the given page from one spot to another, defined by its location"""
    proj, page = get_proj_page(project, pagenumber)
    if to_location == from_location:
        # no movement
        return

    from_location_string, from_container, from_location_integers = from_location
    to_location_string, to_container, to_location_integers = to_location

    if (from_location_string != to_location_string) or (from_container != to_container):
        raise ServerError(message="Unable to move")

    location_string = from_location_string

    if from_container is None:
        # item to move is not in a widget
        if (location_string != 'head') and (location_string != 'body') and (location_string != 'svg'):
            raise ServerError(message="Unable to move item")
        # location integers are integers within the page, move it 
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
        proj.save_page(page)
        return

    # so item is in a widget, location_string is the widget name
    widget = page.widgets[location_string]
    ident_string = widget.ident_string

    # ident_string is of the form; project_pageidentnumber_body-x-y

    splitstring = ident_string.split("_")
    splitloc = splitstring[2].split("-")
    loc_top = splitloc[0]
    widg_ints = [ int(i) for i in splitloc[1:] ]

    widg_container_ints = list(widget.get_container_loc(from_container))

    from_location_ints = widg_ints + widg_container_ints + list(from_location_integers)
    to_location_ints = widg_ints + widg_container_ints + list(to_location_integers)

    # and move this item by calling this function again
    move_location(project, pagenumber, (loc_top, None, from_location_ints), (loc_top, None, to_location_ints))


def css_style(project, pagenumber):
    "Return CSS style of a page, as an ordered Dictionary"
    proj, page = get_proj_page(project, pagenumber)
    if page.page_type != "CSS":
        raise ServerError(message = "Invalid page type")
    return page.style


def file_parameters(project, pagenumber):
    "Return filepath,mimetype of a page"
    proj, page = get_proj_page(project, pagenumber)
    if page.page_type != "FilePage":
        raise ServerError(message = "Invalid page type")
    return (page.filepath, page.mimetype)


def json_contents(project, pagenumber):
    "Return contents dictionary of a JSON page, where keys are WidgField objects (convert to strings for the JSON dictionary string keys)"
    proj, page = get_proj_page(project, pagenumber)
    if page.page_type != "JSON":
        raise ServerError(message = "Invalid page type")
    contents = {}
    if page.content:
        for widgfield,value in page.content.items():
            wf = skiboot.make_widgfield(widgfield)
            if not wf:
                continue
            contents[wf] = value
    return contents

