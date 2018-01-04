####### SKIPOLE WEB FRAMEWORK #######
#
# edittext.py  - creating and editing text
#
# This file is part of the Skipole web framework
#
# Date : 20130205
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

from ....ski import skiboot, tag, widgets
from .. import utils
from ....ski.excepts import FailPage, ValidateError, GoTo

def retrieve_edittextpage(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Fills in the edit text page"

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

    page_data[("adminhead","page_head","large_text")] = "Edit : " + bits.part_string
    page_data[("adminhead","page_head","small_text")] = "Edit the text string."

    # so header text and navigation done, now continue with the page contents

    if not isinstance(part, str):
        raise FailPage("Part not identified as a text string")

    # Set the text in the text area
    page_data[("text_input","input_text")] = part


def edit_text(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Submits new text"

    editedproj = call_data['editedproj']

    # get data
    bits = utils.get_bits(call_data)

    page = bits.page
    section = bits.section
    widget = bits.widget
    location = bits.location
    part = bits.part

    if 'text' not in call_data:
        raise FailPage(message = "Invalid text")

    text = call_data['text']

    utils.set_part(text, 
                   location,
                   page=page,
                   section=section,
                   section_name=bits.section_name,
                   widget=widget,
                   failmessage='Part to have text inserted not identified')

    utils.save(call_data, page=page, section_name=bits.section_name, section=section)
    call_data['status'] = "Text changed"


def create_insert(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Creates new text"

    editedproj = call_data['editedproj']

    # get data
    bits = utils.get_bits(call_data)

    page = bits.page
    section = bits.section
    widget = bits.widget
    location = bits.location
    part = bits.part

    if (page is None) and (section is None):
        raise FailPage("Page/section not identified")

    # get part to have text inserted
    if part is None:
        raise FailPage("Part not identified")

    location_integers = [int(i) for i in location[2]]

    if (location[1] is not None) and (widget.is_container_empty(location[1])):
        # text is to be set as the first item in a container
        new_location = (location[0], location[1], (0,))
        utils.set_part('Set text here', 
                           new_location,
                           page=page,
                           section=section,
                           section_name=bits.section_name,
                           widget=widget,
                           failmessage='Part to have text inserted not identified')
    elif isinstance(part, tag.Part) and (not isinstance(part, widgets.Widget)):
        # insert at position 0 inside the part
        part.insert(0,'Set text here')
        new_location = (location[0], location[1], tuple(location_integers + [0]))
    elif (location[1] is not None) and (len(location_integers) == 1):
        # part is inside a container with parent being the containing div
        # so insert after the part
        position = location_integers[0] + 1
        widget.insert_into_container(location[1], position, 'Set text here')
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
        # insert text at loc in parent_part
        parent_part.insert(loc,'Set text here')
        new_location = (location[0], location[1], tuple(location_integers[:-1] + [loc]))

    utils.save(call_data, page=page, section_name=bits.section_name, section=section)
    # goes to edit text, with location set to the new location
    call_data['location'] = new_location


def create_insert_symbol(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Creates new html symbol"

    editedproj = call_data['editedproj']

    # get data
    bits = utils.get_bits(call_data)

    page = bits.page
    section = bits.section
    widget = bits.widget
    location = bits.location
    part = bits.part

    if (page is None) and (section is None):
        raise FailPage("Page/section not identified")

    # get part to have symbol inserted
    if part is None:
        raise FailPage("Part not identified")

    sym = tag.HTMLSymbol(text="&nbsp;")

    location_integers = [int(i) for i in location[2]]

    if (location[1] is not None) and (widget.is_container_empty(location[1])):
        # text is to be set as the first item in a container
        new_location = (location[0], location[1], (0,))
        utils.set_part(sym, 
                       new_location,
                       page=page,
                       section=section,
                       section_name=bits.section_name,
                       widget=widget,
                       failmessage='Part to have symbol inserted not identified')
    elif isinstance(part, tag.Part) and (not isinstance(part, widgets.Widget)):
        # insert at position 0 inside the part
        part.insert(0,sym)
        new_location = (location[0], location[1], tuple(location_integers + [0]))
    elif (location[1] is not None) and (len(location_integers) == 1):
        # part is inside a container with parent being the containing div
        # so insert after the part
        position = location_integers[0] + 1
        widget.insert_into_container(location[1], position, sym)
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
        # insert symbol at loc in parent_part
        parent_part.insert(loc,sym)
        new_location = (location[0], location[1], tuple(location_integers[:-1] + [loc]))

    utils.save(call_data, page=page, section_name=bits.section_name, section=section)
    # goes to edit symbol, with location set to the new location
    call_data['location'] = new_location


def retrieve_edit_symbol(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Fills in the edit html symbol page"

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

    page_data[("adminhead","page_head","large_text")] = "Edit : " + bits.part_string

    if 'status' in call_data:
        page_data[("adminhead","page_head","small_text")] = call_data['status']
    else:
        page_data[("adminhead","page_head","small_text")] = "Edit the symbol."

    # so header text and navigation done, now continue with the page contents

    if not isinstance(part, tag.HTMLSymbol):
        raise FailPage("Part not identified as an HTML Symbol")

    # Set the text in the input field
    page_data[("symbol_input","input_text")] = part.text


def set_edit_symbol(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Submits new symbol after editing"

    editedproj = call_data['editedproj']

    # get data
    bits = utils.get_bits(call_data)

    page = bits.page
    section = bits.section
    widget = bits.widget
    location = bits.location
    part = bits.part

    if 'symbol' not in call_data:
        raise FailPage(message = "Invalid symbol")

    symbol = call_data['symbol']

    sym = tag.HTMLSymbol(text=symbol)

    utils.set_part(sym, 
                   location,
                   page=page,
                   section=section,
                   section_name=bits.section_name,
                   widget=widget,
                   failmessage='Location to have symbol set not identified')

    utils.save(call_data, page=page, section_name=bits.section_name, section=section)
    call_data['status'] = "Symbol changed"


def retrieve_edit_comment(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Fills in the edit html comment page"

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

    page_data[("adminhead","page_head","large_text")] = "Edit : " + bits.part_string

    if 'status' in call_data:
        page_data[("adminhead","page_head","small_text")] = call_data['status']
    else:
        page_data[("adminhead","page_head","small_text")] = "Edit the comment."

    # so header text and navigation done, now continue with the page contents

    if not isinstance(part, tag.Comment):
        raise FailPage("Part not identified as an HTML comment")

    # Set the text in the input field
    page_data[("comment_input","input_text")] = part.text



def set_edit_comment(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Submits new comment after editing"

    editedproj = call_data['editedproj']

    # get data
    bits = utils.get_bits(call_data)

    page = bits.page
    section = bits.section
    widget = bits.widget
    location = bits.location
    part = bits.part

    if 'comment' not in call_data:
        raise FailPage(message = "Invalid comment")

    comment = call_data['comment']

    com = tag.Comment(text=comment)

    utils.set_part(com, 
                   location,
                   page=page,
                   section=section,
                   section_name=bits.section_name,
                   widget=widget,
                   failmessage='Location to have comment set not identified')

    utils.save(call_data, page=page, section_name=bits.section_name, section=section)
    call_data['status'] = "Comment changed"


def create_insert_comment(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Creates new html comment"

    editedproj = call_data['editedproj']

    # get data
    bits = utils.get_bits(call_data)

    page = bits.page
    section = bits.section
    widget = bits.widget
    location = bits.location
    part = bits.part

    if (page is None) and (section is None):
        raise FailPage("Page/section not identified")

    # get part to have symbol inserted
    if part is None:
        raise FailPage("Part not identified")

    com = tag.Comment(text="comment here")

    location_integers = [int(i) for i in location[2]]

    if (location[1] is not None) and (widget.is_container_empty(location[1])):
        # text is to be set as the first item in a container
        new_location = (location[0], location[1], (0,))
        utils.set_part(com, 
                       new_location,
                       page=page,
                       section=section,
                       section_name=bits.section_name,
                       widget=widget,
                       failmessage='Part to have comment inserted not identified')
    elif isinstance(part, tag.Part) and (not isinstance(part, widgets.Widget)):
        # insert at position 0 inside the part
        part.insert(0,com)
        new_location = (location[0], location[1], tuple(location_integers + [0]))
    elif (location[1] is not None) and (len(location_integers) == 1):
        # part is inside a container with parent being the containing div
        # so insert after the part
        position = location_integers[0] + 1
        widget.insert_into_container(location[1], position, com)
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
        # insert comment at loc in parent_part
        parent_part.insert(loc,com)
        new_location = (location[0], location[1], tuple(location_integers[:-1] + [loc]))


    utils.save(call_data, page=page, section_name=bits.section_name, section=section)
    # goes to edit comment, with location set to the new location
    call_data['location'] = new_location


