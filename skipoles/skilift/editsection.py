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

    if container is None:
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

    widg_container_ints = list(widget.get_container_loc(container))

    from_location_ints = widg_ints + widg_container_ints + list(from_location_integers)
    to_location_ints = widg_ints + widg_container_ints + list(to_location_integers)

    # and move this item by calling this function again
    move_location(project, section_name, (section_name, None, from_location_ints), (section_name, None, to_location_ints))



def move_item(project, section_name, from_location_integers, to_location_integers):
    """Move an item in the given section from one spot to another, defined by its location integers"""
    # raise error if invalid project
    project_loaded(project)
    proj = skiboot.getproject(project)
    if not section_name:
         raise ServerError(message="Given section_name is invalid")
    section = proj.section(section_name, makecopy=True)
    if section is None:
        raise ServerError(message="Given Section not found")
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


