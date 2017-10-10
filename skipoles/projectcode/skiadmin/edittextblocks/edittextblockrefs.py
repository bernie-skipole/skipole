####### SKIPOLE WEB FRAMEWORK #######
#
# edittextblockrefs.py  - edits a pages reference to a textblock
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


import re

# a search for anything none-alphanumeric and not an underscore or a dot
_TB = re.compile('[^\w\.]')

from ....ski import tag, skiboot, widgets
from .. import utils
from ....ski.excepts import FailPage, ValidateError, GoTo, ServerError


def retrieve_textblockref(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Fills in the edit textblockref page"

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

    page_data[("adminhead","page_head","large_text")] = "TextBlock"

    if 'status' in call_data:
        page_data[("adminhead","page_head","small_text")] = call_data['status']
    else:
        page_data[("adminhead","page_head","small_text")] = "Edit the TextBlock."

    # header done, now page contents

    if part is None:
        raise FailPage("Part not identified")

    if not isinstance(part, tag.TextBlock):
        raise FailPage("Part to be edited is not a TextBlock")

    page_data[("textblock_ref","input_text")]=part.textref
    page_data[("textblock_failed","input_text")]=part.failmessage

    page_data[("linebreaks","radio_values")]=['ON', 'OFF']
    page_data[("linebreaks","radio_text")]=['On', 'Off']
    if part.linebreaks and not part.decode:
        page_data[("linebreaks","radio_checked")] = 'ON'
    else:
        page_data[("linebreaks","radio_checked")] = 'OFF'

    page_data[("setescape","radio_values")]=['ON', 'OFF']
    page_data[("setescape","radio_text")]=['On', 'Off']
    if part.escape and not part.decode:
        page_data[("setescape","radio_checked")] = 'ON'
    else:
        page_data[("setescape","radio_checked")] = 'OFF'

    page_data[("setdecode","radio_values")]=['ON', 'OFF']
    page_data[("setdecode","radio_text")]=['On', 'Off']
    if part.decode:
        page_data[("setdecode","radio_checked")] = 'ON'
    else:
        page_data[("setdecode","radio_checked")] = 'OFF'



def set_textblock(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Sets the textblock reference, fail message, linebreaks or escape"

    editedproj = call_data['editedproj']

    # get data
    bits = utils.get_bits(call_data)

    page = bits.page
    section = bits.section
    widget = bits.widget
    part = bits.part

    if (page is None) and (section is None):
        raise FailPage("Page/section not identified")

    if part is None:
        raise FailPage("Part not identified")

    if not isinstance(part, tag.TextBlock):
        raise FailPage("Part to be edited is not a TextBlock")

    if 'textblock_ref' in call_data:
        if _TB.search(call_data["textblock_ref"]):
            raise FailPage(message="Invalid reference")
        part.textref = call_data["textblock_ref"]
        message = 'New reference string set'
        widget_name="textblock_ref"
    elif 'textblock_failed' in call_data:
        part.failmessage = call_data["textblock_failed"]
        message = 'New fail message set'
        widget_name="textblock_failed"
    elif 'linebreaks' in call_data:
        if call_data['linebreaks'] == 'ON':
            part.linebreaks = True
            if part.decode:
                message = "Decode is on; linbreaks setting is overridden"
            else:
                message = 'Linebreaks set on'
        else:
            part.linebreaks = False
            message = 'Linebreaks set off'
        widget_name='linebreaks'
    elif 'setescape' in call_data:
        if call_data['setescape'] == 'ON':
            part.escape = True
            if part.decode:
                message = "Decode is on; escape setting is overridden"
            else:
                message = 'HTML escape set on'
        else:
            part.escape = False
            message = 'HTML escape set off'
        widget_name='setescape'
    elif 'setdecode' in call_data:
        if call_data['setdecode'] == 'ON':
            part.decode = True
            message = 'Text Decode set on'
        else:
            part.decode = False
            message = 'Text Decode off'
        widget_name='setdecode'
    else:
        raise FailPage("A TextBlock value to edit has not been found")

    utils.save(call_data, page=page, section_name=bits.section_name, section=section, widget_name=widget_name)
    call_data['status'] = message


def retrieve_insert(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Fills in the insert a textblock ref page"

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

    page_data[("adminhead","page_head","large_text")] = "Insert TextBlock"
    if isinstance(part, str):
        page_data[("adminhead","page_head","small_text")] = "At location " + bits.part_string
    else:
        page_data[("adminhead","page_head","small_text")] = "At location " + bits.part_string + "_0"

    # so header text and navigation done, now continue with the page contents

    page_data[("linebreaks","radio_values")]=['ON', 'OFF']
    page_data[("linebreaks","radio_text")]=['On', 'Off']
    page_data[("linebreaks","radio_checked")] = 'ON'

    page_data[("setescape","radio_values")]=['ON', 'OFF']
    page_data[("setescape","radio_text")]=['On', 'Off']
    page_data[("setescape","radio_checked")] = 'ON'

    page_data[("decode","radio_values")]=['ON', 'OFF']
    page_data[("decode","radio_text")]=['On', 'Off']
    page_data[("decode","radio_checked")] = 'OFF'


def create_insert(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Creates the textblock ref"

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

    # create the textblock
    if 'textblock_ref' not in call_data:
        raise FailPage(message="Invalid reference")
    if _TB.search(call_data["textblock_ref"]):
        raise FailPage(message="Invalid reference")

    textblock = tag.TextBlock(textref=call_data["textblock_ref"])

    if 'textblock_failed' in call_data:
        textblock.failmessage = call_data["textblock_failed"]

    if 'linebreaks' in call_data:
        if call_data['linebreaks'] == 'ON':
            textblock.linebreaks = True
        else:
            textblock.linebreaks = False

    if 'setescape' in call_data:
        if call_data['setescape'] == 'ON':
            textblock.escape = True
        else:
            textblock.escape = False

    if 'decode' in call_data:
        if call_data['decode'] == 'ON':
            textblock.decode = True
        else:
            textblock.decode = False

    if (location[1] is not None) and (not location[2])  and (not isinstance(part, tag.Part)):
        # part is the top part of a container
        utils.set_part(textblock, 
                       location,
                       page=page,
                       section=section,
                       section_name=bits.section_name,
                       widget=widget,
                       failmessage='Part to have textblock inserted not identified')
    elif isinstance(part, tag.Part) and (not isinstance(part, widgets.Widget)):
        # insert at position 0 inside the part
        part.insert(0,textblock)
    else:
        # do an append, rather than an insert
        # get parent part
        parent_part = utils.part_from_location(page,
                                               section,
                                               bits.section_name,
                                               location_string=location[0],
                                               container=location[1],
                                               location_integers=location[2][:-1])
        # find location digit
        loc = location[2][-1] + 1
        # insert textblock at loc in parent_part
        parent_part.insert(loc,textblock)

    utils.save(call_data, page=page, section_name=bits.section_name, section=section, widget_name='')
    call_data['status'] = "TextBlock inserted"
    raise GoTo(target = label, clear_submitted=True)
