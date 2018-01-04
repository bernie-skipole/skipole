####### SKIPOLE WEB FRAMEWORK #######
#
# insertpart.py  - functions to insert an html tag
#
# This file is part of the Skipole web framework
#
# Date : 20150326
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

"Functions to insert an html tage"


from ....ski import skiboot, tag, widgets
from .. import utils
from ....ski.excepts import FailPage, ValidateError, GoTo, ServerError

from .... import skilift
from ....skilift import fromjson


def retrieve_insert(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Fills in the insert an html tag page"

    editedproj = call_data['editedproj']

    # get data
    bits = utils.get_bits(call_data)

    page = bits.page
    section = bits.section
    widget = bits.widget
    part = bits.part

    if (page is None) and (section is None):
        raise FailPage("Page/section not identified")

    # Fill in header

    # navigator boxes
    utils.nav_boxes(call_data, page, section, bits.page_top, bits.parent_container, widget, bits.container)

    page_data[("adminhead","page_head","large_text")] = "Insert an HTML tag"

    if 'status' in call_data:
        page_data[("adminhead","page_head","small_text")] = call_data['status']
    else:
        page_data[("adminhead","page_head","small_text")] = "Set values."

    # header done, now page contents

    if part is None:
        raise FailPage("Part not identified")


def create_insert(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Creates the html tag"

    editedproj = call_data['editedproj']

    # get data
    bits = utils.get_bits(call_data)

    page = bits.page
    section = bits.section
    widget = bits.widget
    location = bits.location
    part = bits.part

    # location is a tuple consisting of the leading string (such as head or section name or widget name)
    # container integer, such as 0 for container 0, or None if no container
    # and tuple of location integers


    if (page is None) and (section is None):
        raise FailPage("Page/section not identified")

    if part is None:
        raise FailPage("Part not identified")

    # label used in GoTo jump to return to the point where item is inserted
    label = None

    if page is not None:
        if (page.page_type != 'TemplatePage') and (page.page_type != 'SVG'):
            raise FailPage(message = "Invalid page")
        # page to go back to
        if bits.part_top == 'head':
            label = "page_head"   # label to 3320
        elif bits.part_top == 'body':
            label = "page_body"   # label to 3340
        elif bits.part_top == 'svg':
            label = "page_svg"   # label to 3420

    if section is not None:
        if bits.part_top == bits.section_name:
            label = "back_to_section"   # label to 7040

    # could be a widget container
    if label is None:
        if (widget is not None) and bits.part_top == widget.name: 
            label = "back_to_container"   # label to 44704
        else:
            raise FailPage("Invalid location")

    location_integers = [int(i) for i in location[2]]

    # create the item
    if call_data['newopenclosed'] == 'open':
        newpart = tag.Part(tag_name=call_data['newpartname'], brief=call_data['newbrief'])
    else:
        newpart = tag.ClosedPart(tag_name=call_data['newpartname'], brief=call_data['newbrief'])

    if (location[1] is not None) and (widget.is_container_empty(location[1])):
        # newpart is to be set as the first item in a container
        new_location = (location[0], location[1], (0,))
        utils.set_part(newpart, 
                       new_location,
                       page=page,
                       section=section,
                       section_name=bits.section_name,
                       widget=widget,
                       failmessage='Part to have element inserted not identified')
    elif isinstance(part, tag.Part) and (not isinstance(part, widgets.Widget)):
        # insert at position 0 inside the part
        part.insert(0,newpart)
        new_location = (location[0], location[1], tuple(location_integers + [0]))
    elif (location[1] is not None) and (len(location_integers) == 1):
        # part is inside a container with parent being the containing div
        # so append newpart after the part by inserting at the right place in the container
        position = location_integers[0] + 1
        widget.insert_into_container(location[1], position, newpart)
        new_location = (location[0], location[1], (position,))
    else:
        # do an append, rather than an insert
        # get parent part
        parent_part = utils.part_from_location(page,
                                               section,
                                               bits.section_name,
                                               location_string=location[0],
                                               container=location[1],
                                               location_integers=location_integers[:-1])
        # find location digit
        loc = location_integers[-1] + 1
        # insert newpart at loc in parent_part
        parent_part.insert(loc,newpart)
        new_location = (location[0], location[1], tuple(location_integers[:-1] + [loc]))

    utils.save(call_data, page=page, section_name=bits.section_name, section=section)

    call_data['status'] = 'New tag inserted'
    raise GoTo(target = label, clear_submitted=True)



def file_new_part(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Create new part from uploaded file"

    editedprojname = call_data['editedprojname']

    if 'page' in call_data:
        page = call_data['page']
        if (page.page_type != 'TemplatePage') and (page.page_type != 'SVG'):
            raise FailPage(message = "Invalid page")
        pagenumber = page.ident.num
    else:
        pagenumber = None

    if 'section_name' in call_data:
        section_name = call_data['section_name']
    else:
        section_name = None

    if (pagenumber is None) and (section_name is None):
        raise FailPage(message = "Invalid location")


    part_info = skilift.part_info(editedprojname, pagenumber, section_name, call_data['location'])
    if not part_info:
        raise FailPage("Part to locate block not identified")

    label = "admin_home"
    # is item contained in a widget
    container = part_info.location[1]
    if container is not None:
        parent_widget = part_info.location[0]
    else:
        parent_widget = None

    if parent_widget is None:
        if section_name:
            label = "back_to_section"   # label to 7040
        else:
            # page to go back to
            if part_info.page_part == 'head':
                label = "page_head"   # label to 3320
            elif part_info.page_part == 'body':
                label = "page_body"   # label to 3340
            elif part_info.page_part == 'svg':
                label = "page_svg"   # label to 3420
    else:
        # it's in a widget container
        label = "back_to_container"   # label to 44704
       

    # get file contents
    file_contents = call_data["uploadpart", "action"]
    json_string = file_contents.decode(encoding='utf-8')
    # create the part
    try:
        fromjson.create_part(*part_info, json_data=json_string)
    except ServerError as e:
        raise FailPage(message = e.message)

    # refresh page, section, widget in call_data
    if section_name:
        call_data['section'] = call_data['editedproj'].section(section_name)
    else:
        call_data['page'] = skiboot.from_ident(page.ident, import_sections=False)

    if parent_widget:
        call_data['widget_name'] = parent_widget

    # new part created
    call_data['status'] = 'New block created'
    raise GoTo(target = label, clear_submitted=True)

