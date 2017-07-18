####### SKIPOLE WEB FRAMEWORK #######
#
# insert.py  - insert page elements
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

"Functions implementing item insertion into a page"


from .. import utils
from ....ski import skiboot
from ....ski.excepts import FailPage, ValidateError


def retrieve_insert(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "this call is for the choose an item to insert page"

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

    # navigator boxes
    utils.nav_boxes(call_data, page, section, bits.page_top, widget, bits.container)

    page_data[("adminhead","page_head","large_text")] = "Choose an item to insert"
    page_data[("adminhead","page_head","small_text")] = "Pick an item type"

    if page is not None:
        # table contents includes 'insert a section'
        page_data[("insertlist","links")] = [
                ["Insert text", "inserttext", ""],
                ["Insert a TextBlock", "insert_textblockref", ""],
                ["Insert html symbol", "insertsymbol", ""],
                ["Insert comment", "insertcomment", ""],
                ["Insert an html element", "part_insert", ""],
                ["Insert a Widget", "list_widget_modules", ""],
                ["Insert a Section", "placeholder_insert", ""]
               ]
    if section is not None:
        page_data[("insertlist","links")] = [
                ["Insert text", "inserttext", ""],
                ["Insert a TextBlock", "insert_textblockref", ""],
                ["Insert html symbol", "insertsymbol", ""],
                ["Insert comment", "insertcomment", ""],
                ["Insert an html element", "part_insert", ""],
                ["Insert a Widget", "list_widget_modules", ""]
               ]



def retrieve_append(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "this call is for the choose an item to append into a page"

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

    # navigator boxes
    utils.nav_boxes(call_data, page, section, bits.page_top, widget, bits.container)

    page_data[("adminhead","page_head","large_text")] = "Choose an item to append"
    page_data[("adminhead","page_head","small_text")] = "Pick an item type"

    if page is not None:
        # table contents includes 'insert a section'
        page_data[("appendlist","links")] = [
                ["Append text", "inserttext", ""],
                ["Append a TextBlock", "insert_textblockref", ""],
                ["Append html symbol", "insertsymbol", ""],
                ["Append comment", "insertcomment", ""],
                ["Append an html element", "part_insert", ""],
                ["Append a Widget", "list_widget_modules", ""],
                ["Append a Section", "placeholder_insert", ""]
               ]
    if section is not None:
        page_data[("appendlist","links")] = [
                ["Append text", "inserttext", ""],
                ["Append a TextBlock", "insert_textblockref", ""],
                ["Append html symbol", "insertsymbol", ""],
                ["Append comment", "insertcomment", ""],
                ["Append an html element", "part_insert", ""],
                ["Append a Widget", "list_widget_modules", ""]
               ]

