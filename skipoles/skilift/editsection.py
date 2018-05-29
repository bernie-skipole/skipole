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

from collections import namedtuple, OrderedDict

from ..ski import skiboot, tag, read_json
from ..ski.excepts import ServerError

from . import project_loaded, get_proj_section, get_proj_page, insert_item_in_page, del_location_in_section, insert_item_in_section


PlaceHolderInfo = namedtuple('PlaceHolderInfo', ['project', 'pagenumber', 'section_name', 'alias', 'brief', 'multiplier', 'mtag'])

SectionElement = namedtuple('SectionElement', ['project', 'section_name', 'schange', 'location', 'part_type', 'tag_name', 'brief', 'show', 'hide_if_empty', 'attribs'])


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


def placeholder_info(project, pagenumber, location):
    """location is a tuple or list consisting of three items:
       a string (such as head or widget name)
       a container integer, such as 0 for widget container 0, or None if not in container
       a tuple or list of location integers
       returns None if placeholder not found, otherwise returns a namedtuple with items
       project, pagenumber, section_name, alias, brief, multiplier, mtag
    """
    proj, page = get_proj_page(project, pagenumber)
    part = page.location_item(location)
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

    if hasattr(part, 'mtag'):
        mtag = part.mtag
    else:
        mtag = None

    return PlaceHolderInfo(project, pagenumber, section_name, alias, brief, multiplier, mtag)


def edit_placeholder(project, pagenumber, pchange, location, section_name, alias, brief, multiplier, mtag):
    """Given a placeholder at project, pagenumber, location
       sets the values section_name, alias, brief, multiplier, mtag, returns page change uuid """
    # raise error if invalid project
    if project is None:
        project = skiboot.project_ident()
    # raise error if invalid project
    project_loaded(project)
    proj = skiboot.getproject(project)
    if proj is None:
        raise ServerError(message="The edited project is invalid")

    location_string, container_number, location_list = location

    part = None

    if pagenumber is None:
        raise ServerError(message="The page containing this section seems to be invalid")

    ident = skiboot.find_ident(pagenumber, project)
    if not ident:
        raise ServerError(message="The page containing this section seems to be invalid")
    page = skiboot.get_item(ident)
    if not page:
        raise ServerError(message="The page containing this section seems to be invalid")
    if (page.page_type != "TemplatePage") and (page.page_type != "SVG"):
        raise ServerError(message="The page type containing this section seems to be invalid")
    if page.change != pchange:
        raise ServerError(message="The page has been changed prior to this submission, someone else may be editing this project")
    part = page.location_item(location)
    if part is None:
        raise ServerError(message="Cannot find the section placeholder")

    if part.__class__.__name__ != "SectionPlaceHolder":
        raise ServerError(message="The edited location does not seem to be a section placeholder")

    # is placename unique
    if alias != part.placename:
        if alias in page.widgets:
            raise ServerError(message="Duplicate name in the page - a widget has this assigned")
        if alias in page.section_places:
            raise ServerError(message="This name clashes with a section alias already within this page")
    part.section_name = section_name
    part.placename = alias
    part.brief = brief
    part.multiplier = multiplier
    part.mtag = mtag

    # save the altered page, and return the page.change uuid
    return proj.save_page(page)



def new_placeholder(project, pagenumber, pchange, location, section_name, alias, brief):
    """Create a new placeholder at project, pagenumber, location
       with section_name, alias, brief returns page change uuid """
    # create new placeholder
    newplaceholder = tag.SectionPlaceHolder(section_name=section_name,
                                            placename=alias,
                                            brief=brief)
    # call skilift.insert_item_in_page to insert the item, save the page and return pchange
    new_pchange, new_location = insert_item_in_page(project, pagenumber, pchange, location, newplaceholder)
    return new_pchange


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


def del_location(project, section_name, schange, location):
    "Deletes the item at the given location in the section, returns new schange"
    return del_location_in_section(project, section_name, schange, location)


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


def delete_section(project, section_name):
    "delete this section, return None on success, raises a ServerError on failure"
    # raise error if invalid project
    project_loaded(project)
    proj = skiboot.getproject(project)
    if proj is None:
        raise ServerError(message="The edited project is invalid")
    section_list = proj.list_section_names()
    if section_name not in section_list:
        raise ServerError(message="Section name does not exists")
    proj.delete_section(section_name)


def create_html_element_in_section(project, section_name, schange, location, name, brief, opentag = True):
    "Creates a new html element in the given section, returns the new schange"
    if opentag:
        newpart = tag.Part(tag_name=name, brief=brief)
    else:
        newpart = tag.ClosedPart(tag_name=name, brief=brief)
    # call skilift.insert_item_in_section to insert the item, save the section and return schange
    new_schange, new_location = insert_item_in_section(project, section_name, schange, location, newpart)
    return new_schange


def create_part_in_section(project, section_name, schange, location, json_data):
    """Builds the part from the given json string or ordered dictionary, and adds it to project either inserted into the html element
       currently at the given part location, or if not an element that can accept contents, inserted after the element.
       Returns new schange value"""
    proj, section = get_proj_section(project, section_name, schange)
    try:
        newpart = read_json.make_part_for_section(section, json_data)
    except:
        raise ServerError("Unable to create part")
    # call skilift.insert_item_in_section to insert the item, save the section and return schange
    new_schange, new_location = insert_item_in_section(project, section_name, schange, location, newpart)
    return new_schange


def section_element(project, section_name, schange, location):
    """Return a element tuple for the html element at the given location"""

    proj, section = get_proj_section(project, section_name, schange)
    part = section.location_item(location)

    if part is None:
        raise ServerError("The item at the location has not been found")

    if hasattr(part, '__class__'):
        part_type = part.__class__.__name__
    else:
        raise ServerError("The item at the location must be an html element")

    if (part_type != "Part") and (part_type != "ClosedPart"):
        raise ServerError("The item at the location must be an html element")

    tag_name = part.tag_name
    brief = part.brief
    show = part.show
    hide_if_empty = part.hide_if_empty
    attribs = OrderedDict(sorted(part.attribs.items(), key=lambda t: t[0]))

    return SectionElement(project, section_name, schange, location, part_type, tag_name, brief, show, hide_if_empty, attribs)


def edit_section_element(project, section_name, schange, location, tag_name, brief, hide_if_empty, attribs):
    """Given an element at project, section_name, location
       sets the element values, returns section change uuid """
    proj, section = get_proj_section(project, section_name, schange)
    part = section.location_item(location)
    part.tag_name = tag_name
    part.brief = brief
    part.attribs = OrderedDict(sorted(attribs.items(), key=lambda t: t[0]))
    if part.__class__.__name__ == "Part":
        part.hide_if_empty = hide_if_empty
    # save the altered section, and return the section.change uuid
    return proj.add_section(section_name, section)

def del_attrib(project, section_name, schange, location, attribute):
    """Given an element at project, section_name, location
       deletes the given attribute, returns sceetion change uuid """
    proj, section = get_proj_section(project, section_name, schange)
    part = section.location_item(location)
    part.del_one_attrib(attribute)
    # save the altered section, and return the section.change uuid
    return proj.add_section(section_name, section)

def get_text(project, section_name, schange, location):
    """Return a text string from the page at the given location"""
    proj, section = get_proj_section(project, section_name, schange)
    text = section.location_item(location)
    if not isinstance(text, str):
        raise ServerError("Item at this location is not identified as a text string")
    return text
 


