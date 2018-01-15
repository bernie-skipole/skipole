####### SKIPOLE WEB FRAMEWORK #######
#
# editplaceholder.py  - functions to edit and insert a section placeholder
#
# This file is part of the Skipole web framework
#
# Date : 20150412
#
# Author : Bernard Czenkusz
# Email  : bernie@skipole.co.uk
#
#
#   Copyright 2015 Bernard Czenkusz
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

"Functions to edit and insert a section placeholder"

import re

# a search for anything none-alphanumeric and not an underscore
_AN = re.compile('[^\w_]')


from ....ski import skiboot, tag, widgets
from .. import utils
from ....ski.excepts import FailPage, ValidateError, GoTo, ServerError


def retrieve_editplaceholder(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Fills in the edit placeholder page"

    editedproj = call_data['editedproj']

    # get data
    bits = utils.get_bits(call_data)

    page = bits.page
    section = None        # placeholder cannot be in a section
    widget = bits.widget
    part = bits.part

    if page is None:
        raise FailPage("Page not identified")

    # Fill in header
    page_data[("adminhead","page_head","large_text")] = "Section"

    # header done, now page contents

    if not isinstance(part, tag.SectionPlaceHolder):
        raise FailPage("Part to be edited is not a Section Place Holder")

    # get current sections
    section_list = editedproj.list_section_names()
    if not section_list:
        page_data[('editsection','option_list')] = ['-None-']
        page_data[('editsection','selectvalue')] = '-None-'
        page_data[("nosection", "show")] = True
    elif part.section_name in section_list:
        page_data[('editsection','option_list')] = section_list[:]
        page_data[('editsection','selectvalue')] = part.section_name
    else:
        page_data[('editsection','option_list')] = ['-None-'] + section_list
        page_data[('editsection','selectvalue')] = '-None-'
        page_data[("nosection", "show")] = True

    page_data[("brief", "input_text")] = part.brief
    page_data[("placename", "input_text")] = part.placename


def set_placeholder(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Sets the placeholder section name, brief, or placename"

    editedproj = call_data['editedproj']

    # get data
    bits = utils.get_bits(call_data)

    page = bits.page
    part = bits.part

    if page is None:
        raise FailPage("Page not identified")

    if not isinstance(part, tag.SectionPlaceHolder):
        raise FailPage("Part to be edited is not a Section place holder")

    if 'new_section_name' in call_data:
        if call_data['new_section_name'] == '-None-':
            raise FailPage(message='Section name not set')
        # get current sections
        section_list = editedproj.list_section_names()
        if not section_list:
            raise FailPage(message='No sections found')
        if call_data['new_section_name'] not in section_list:
            raise FailPage(message='Section not found')
        part.section_name = call_data['new_section_name']
        message = 'New section name set'
        widget_name="editsection"
    elif 'placeholder_brief' in call_data:
        part.brief = call_data["placeholder_brief"]
        message = 'New description set'
        widget_name="brief"
    elif 'placename' in call_data:
        if call_data['placename'] == part.placename:
            call_data['status'] = 'Alias not changed'
            return
        if call_data['placename'] in page.section_places:
            raise FailPage("This alias already exists")
        if _AN.search(call_data['placename']):
            raise FailPage(message="Invalid alias")
        part.placename = call_data['placename']
        message = 'New alias set'
        widget_name='placename'
    else:
        raise FailPage("A new placeholder value to edit has not been found")
    utils.save(call_data, page=page, widget_name=widget_name)
    call_data['status'] = message


def retrieve_insert(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Fills in the insert a placeholder page"

    editedproj = call_data['editedproj']

    # get data
    bits = utils.get_bits(call_data)

    page = bits.page
    section = None          # placeholder cannot be in a section
    widget = bits.widget
    part = bits.part

    if page is None:
        raise FailPage("Page not identified")

    # Fill in header
    page_data[("adminhead","page_head","large_text")] = "Insert Section"

    # so header text and navigation done, now continue with the page contents

    # get current sections
    section_list = editedproj.list_section_names()
    if not section_list:
        page_data[("nosection", "show")] = True
        page_data[("descript", "show")] = False
        page_data[("placename","show")] = False
        return

    page_data[('sectionname','option_list')] = section_list[:]
    page_data[('sectionname','selectvalue')] = section_list[0]


def create_insert(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Creates the section placeholder"

    editedproj = call_data['editedproj']

    # get data
    bits = utils.get_bits(call_data)

    page = bits.page
    widget = bits.widget
    location = bits.location
    part = bits.part

    if page is None:
        raise FailPage("Page not identified")

    if part is None:
        raise FailPage("Part not identified")

    # label used in GoTo jump to return to the point where item is inserted
    label = None

    if (page.page_type != 'TemplatePage') and (page.page_type != 'SVG'):
        raise FailPage(message = "Invalid page")
    # page to go back to
    if bits.part_top == 'head':
        label = "page_head"   # label to 3320
    elif bits.part_top == 'body':
        label = "page_body"   # label to 3340
    elif bits.part_top == 'svg':
        label = "page_svg"   # label to 3420

    # could be a widget container
    if label is None:
        if (widget is not None) and bits.part_top == widget.name: 
            label = "back_to_container"   # label to 44704
        else:
            raise FailPage("Invalid location")

    # create the item

    if 'newsectionname' not in call_data:
        raise FailPage(message = "Missing section name")
    section_name=call_data['newsectionname']

    # get current sections
    section_list = editedproj.list_section_names()
    if section_name not in section_list:
        raise FailPage(message = "Unknown section name")

    if 'newplacename' not in call_data:
        raise FailPage(message = "Missing section alias")
    placename=call_data['newplacename']
    if placename in page.section_places:
        raise FailPage(message = "This section alias already exists")
    if _AN.search(placename):
        raise FailPage(message="Invalid alias")

    newplaceholder = tag.SectionPlaceHolder(section_name=section_name,
                                            placename=placename,
                                            brief=call_data['newbrief'])

    location_integers = [int(i) for i in location[2]]

    if (location[1] is not None) and (widget.is_container_empty(location[1])):
        # text is to be set as the first item in a container
        new_location = (location[0], location[1], (0,))
        utils.set_part(newplaceholder, 
                       new_location,
                       page=page,
                       section=None,
                       section_name='',
                       widget=widget,
                       failmessage='Part to have placeholder inserted not identified')
    elif isinstance(part, tag.Part) and (not isinstance(part, widgets.Widget)):
        # insert at position 0 inside the part
        part.insert(0,newplaceholder)
        new_location = (location[0], location[1], tuple(location_integers + [0]))
    elif (location[1] is not None) and (len(location_integers) == 1):
        # part is inside a container with parent being the containing div
        # so append after the part by inserting at the right place in the container
        position = location_integers[0] + 1
        widget.insert_into_container(location[1], position, newplaceholder)
        new_location = (location[0], location[1], (position,))
    else:
        # do an append, rather than an insert
        # get parent part
        parent_part = utils.part_from_location(page,
                                               None,
                                               '',
                                               location_string=location[0],
                                               container=location[1],
                                               location_integers=location_integers[:-1])
        # find location digit
        loc = location_integers[-1] + 1
        # insert placeholder at loc in parent_part
        parent_part.insert(loc,newplaceholder)
        new_location = (location[0], location[1], tuple(location_integers[:-1] + [loc]))

    utils.save(call_data, page=page)
    call_data['status'] = "Section placeholder inserted"
    raise GoTo(target = label, clear_submitted=True)

