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

from collections import namedtuple

from ..ski import skiboot
from ..ski.excepts import ServerError

from . import project_loaded


PlaceHolderInfo = namedtuple('PlaceHolderInfo', ['project', 'pagenumber', 'section_name', 'alias', 'brief', 'multiplier'])


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


def list_section_names(project=None):
    """Returns a list of section names in the project"""
    if project is None:
        project = skiboot.project_ident()
    # raise error if invalid project
    project_loaded(project)
    proj = skiboot.getproject(project)
    if proj is None:
        return ()
    return proj.list_section_names()


def placeholder__info(project, pagenumber, location):
    """location is a tuple or list consisting of three items:
       a string (such as head or widget name)
       a container integer, such as 0 for widget container 0, or None if not in container
       a tuple or list of location integers
       returns None if placeholder not found, otherwise returns a namedtuple with items
       project, pagenumber, section_name, alias, brief, multiplier
    """
    # raise error if invalid project
    if project is None:
        project = skiboot.project_ident()
    # raise error if invalid project
    project_loaded(project)
    proj = skiboot.getproject(project)
    if proj is None:
        return

    location_string, container_number, location_list = location

    ident = None
    page_part = None
    widget_name = None
    part_type = None

    if pagenumber is None:
        return

    ident = skiboot.find_ident(pagenumber, project)
    if not ident:
        return
    page = skiboot.get_item(ident)
    if not page:
        return
    if (page.page_type != "TemplatePage") and (page.page_type != "SVG"):
        return
    if (location_string == 'head') or (location_string == 'body') or (location_string == 'svg'):
        # part not in a widget
        page_part = location_string
    else:
        widget_name = location_string
        # find page_part containing widget
        widget = page.widgets[widget_name]
        if widget is not None:
           ident_top = widget.ident_string.split("-", 1)
           # ident_top[0] will be of the form proj_pagenum_head
           page_part = ident_top[0].split("_")[2]

    part = skiboot.get_part(project, ident, page_part, None, widget_name, container_number, location_list)
    if part is None:
        return

    if part.__class__.__name__ != "SectionPlaceHolder":
        return

    if hasattr(part, 'brief'):
        brief = part.brief
    else:
        brief = None

    if hasattr(part, 'section_name'):
        section_name = part.section_name
    else:
        section_name = None

    if hasattr(part, 'placename'):
        alias = part.placename
    else:
        alias = None

    if hasattr(part, 'multiplier'):
        multiplier = part.multiplier
    else:
        multiplier = None

    return PlaceHolderInfo(project, pagenumber, section_name, alias, brief, multiplier)



def edit_placeholder(project, pagenumber, location, section_name, alias, brief, multiplier):
    """Given a placeholder at project, pagenumber, location
       sets the values section_name, alias, brief, multiplier"""
    # raise error if invalid project
    if project is None:
        project = skiboot.project_ident()
    # raise error if invalid project
    project_loaded(project)
    proj = skiboot.getproject(project)
    if proj is None:
        return

    location_string, container_number, location_list = location

    part = None

    if pagenumber is None:
        return

    ident = skiboot.find_ident(pagenumber, project)
    if not ident:
        return
    page = skiboot.get_item(ident)
    if not page:
        return
    if (page.page_type != "TemplatePage") and (page.page_type != "SVG"):
        return
    if (location_string == 'head') or (location_string == 'body') or (location_string == 'svg'):
        # part not in a widget
        part = page.get_part(location_string, location_list)
    else:
        # the location_string is the widget name
        widget = page.widgets[location_string]
        if widget is not None:
            # widget is the containing widget 
            if widget.can_contain() and not (container_number is None):
                part = widget.get_from_container(container_number, location_list)

    if part is None:
        return

    if part.__class__.__name__ != "SectionPlaceHolder":
        return

    part.section_name = section_name
    part.placename = alias
    part.brief = brief
    part.multiplier = multiplier

    # save the altered page
    proj.save_page(page)



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


def del_location(project, section_name, location):
    "Deletes the item at the given location"
    # raise error if invalid project
    project_loaded(project)
    proj = skiboot.getproject(project)
    if not section_name:
         raise ServerError(message="Given section_name is invalid")
    section = proj.section(section_name, makecopy=True)
    if section is None:
        raise ServerError(message="Given Section not found")

    location_string, container, location_integers = location

    if container is None:
        if location_string != section_name:
            raise ServerError(message="Unable to delete item")
        # remove the item
        try:
            section.del_location_value(location_integers)
        except:
            raise ServerError(message="Unable to delete item")
        # And save this section copy to the project
        proj.add_section(section_name, section)
        return

    # so item is in a widget, location_string is the widget name
    widget = section.widgets[location_string]
    ident_string = widget.ident_string

    # ident_string is sectionname-x-y

    splitstring = ident_string.split("-")
    widg_ints = [ int(i) for i in splitstring[1:] ]

    widg_container_ints = list(widget.get_container_loc(container))

    item_location_ints = widg_ints + widg_container_ints + list(location_integers)

    # remove the item
    try:
        section.del_location_value(item_location_ints)
    except:
        raise ServerError(message="Unable to delete item")
    # And save this section copy to the project
    proj.add_section(section_name, section)


def move_location(project, section_name, from_location, to_location):
    """Move an item in the given section from one spot to another, defined by its location"""
    # raise error if invalid project
    project_loaded(project)
    proj = skiboot.getproject(project)
    if not section_name:
         raise ServerError(message="Given section_name is invalid")
    section = proj.section(section_name, makecopy=True)
    if section is None:
        raise ServerError(message="Given Section not found")

    if to_location == from_location:
        # no movement
        return

    from_location_string, from_container, from_location_integers = from_location
    to_location_string, to_container, to_location_integers = to_location

    if (from_location_string != to_location_string) or (from_container != to_container):
        raise ServerError(message="Unable to move")

    if from_container is None:
        if from_location_string != section_name:
            raise ServerError(message="Unable to move item")
        # location integers are integers within the section, move it 
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
                # get the part at from_location_integers
                part = section.get_location_value(from_location_integers)
                # delete part from current location
                section.del_location_value(from_location_integers)
                # and insert it in the new location
                section.insert_location_value(to_location_integers, part)
            except:
                raise ServerError(message="Unable to move item")
        else:
            # move in the downwards direction
            #    insert it into new location
            #    delete it from original location
            try:
                # get the part at from_location_integers
                part = section.get_location_value(from_location_integers)
                # and insert it in the new location
                section.insert_location_value(to_location_integers, part)
                # delete part from current location
                section.del_location_value(from_location_integers)
            except:
                raise ServerError(message="Unable to move item")
        # And save this section copy to the project
        proj.add_section(section_name, section)
        return

    # part is within a widget, so get its location relative to the section
    widget = section.widgets[from_location_string]
    ident_string = widget.ident_string

    # ident_string is sectionname-x-y

    splitstring = ident_string.split("-")
    widg_ints = [ int(i) for i in splitstring[1:] ]

    widg_container_ints = list(widget.get_container_loc(from_container))

    from_location_ints = widg_ints + widg_container_ints + list(from_location_integers)
    to_location_ints = widg_ints + widg_container_ints + list(to_location_integers)

    # and move this item by calling this function again
    move_location(project, section_name, (section_name, None, from_location_ints), (section_name, None, to_location_ints))



