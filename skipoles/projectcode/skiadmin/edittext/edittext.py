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


from .... import skilift
from ....skilift import editpage, editsection
from ....ski.excepts import FailPage, ValidateError, GoTo, ServerError



def retrieve_edittextpage(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Fills in the edit text page"

    # a skilift.part_tuple is (project, pagenumber, page_part, section_name, name, location, part_type, brief)

    pagenumber = None
    section_name = None

    if 'part_tuple' in call_data:
        part_tuple = call_data['part_tuple']
        project = part_tuple.project
        location = part_tuple.location
        pagenumber = part_tuple.pagenumber
        section_name = part_tuple.section_name
    else:
        project = call_data['editedprojname']
        location = call_data['location']
        if 'page_number' in call_data:
            pagenumber = call_data['page_number']
        else:
            section_name = call_data['section_name']

    if (pagenumber is None) and (section_name is None):
        raise ValidateError("Page/section not identified")

    call_data['location'] = location

    try:

        if pagenumber:
            call_data['page_number'] = pagenumber
            text = editpage.get_text(project, pagenumber, call_data['pchange'], location)
            page_data[("adminhead","page_head","large_text")] = "Edit Text in page : %s" % (pagenumber,)
        elif section_name:
            call_data['section_name'] = section_name
            text = editsection.get_text(project, section_name, call_data['schange'], location)
            page_data[("adminhead","page_head","large_text")] = "Edit Text in section : %s" % (section_name,)
        else:
            raise FailPage("Either a page or section must be specified")

    except ServerError as e:
        raise FailPage(e.message)

    # Set the text in the text area
    page_data[("text_input","input_text")] = text



def edit_text(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Submits new text"

    project = call_data['editedprojname']
    location = call_data['location']

    text = call_data['text']

    try:
        if 'page_number' in call_data:
            pagenumber = call_data['page_number']
            call_data['pchange'] = skilift.set_item_in_page(project, pagenumber, call_data['pchange'], location, text)
        elif 'section_name' in call_data:
            section_name = call_data['section_name']
            call_data['schange'] = skilift.set_item_in_section(project, section_name, call_data['schange'], location, text)
        else:
            raise ValidateError("Page/section not identified")
    except ServerError as e:
        raise FailPage(e.message)
    call_data['status'] = "Text changed"


def create_insert(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Creates new text"

    project = call_data['editedprojname']

    try:

        if 'page_number' in call_data:
            pagenumber = call_data['page_number']
            page_info = skilift.item_info(project, pagenumber)
            if page_info is None:
                raise FailPage("Page to edit not identified")
            if (page_info.item_type != "TemplatePage") and (page_info.item_type != "SVG"):
                raise FailPage("Page not identified")

            call_data['pchange'], new_location = skilift.insert_item_in_page(project, pagenumber, call_data['pchange'], call_data['location'], 'Set text here')

        elif 'section_name' in call_data:
            section_name = call_data['section_name']
            call_data['schange'], new_location = skilift.insert_item_in_section(project, section_name, call_data['schange'], call_data['location'], 'Set text here')

        else:
            raise FailPage("Either a page or section must be specified")

    except ServerError as e:
        raise FailPage(e.message)
    call_data['location'] = new_location


def create_insert_symbol(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Creates new html symbol"

    project = call_data['editedprojname']

    try:

        if 'page_number' in call_data:
            pagenumber = call_data['page_number']
            page_info = skilift.item_info(project, pagenumber)
            if page_info is None:
                raise FailPage("Page to edit not identified")
            if (page_info.item_type != "TemplatePage") and (page_info.item_type != "SVG"):
                raise FailPage("Page not identified")

            call_data['pchange'], new_location = editpage.create_html_symbol_in_page(project, pagenumber, call_data['pchange'], call_data['location'])

        elif 'section_name' in call_data:
            section_name = call_data['section_name']
            call_data['schange'], new_location = editsection.create_html_symbol_in_section(project, section_name, call_data['schange'], call_data['location'])

        else:
            raise FailPage("Either a page or section must be specified")

    except ServerError as e:
        raise FailPage(e.message)
    call_data['location'] = new_location


def retrieve_edit_symbol(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Fills in the edit html symbol page"

    # a skilift.part_tuple is (project, pagenumber, page_part, section_name, name, location, part_type, brief)

    pagenumber = None
    section_name = None

    if 'part_tuple' in call_data:
        part_tuple = call_data['part_tuple']
        project = part_tuple.project
        location = part_tuple.location
        pagenumber = part_tuple.pagenumber
        section_name = part_tuple.section_name
    else:
        project = call_data['editedprojname']
        location = call_data['location']
        if 'page_number' in call_data:
            pagenumber = call_data['page_number']
        else:
            section_name = call_data['section_name']

    if (pagenumber is None) and (section_name is None):
        raise ValidateError("Page/section not identified")

    call_data['location'] = location

    try:

        if pagenumber:
            call_data['page_number'] = pagenumber
            sym = editpage.get_symbol(project, pagenumber, call_data['pchange'], location)
            page_data[("adminhead","page_head","large_text")] = "Edit Symbol in page : %s" % (pagenumber,)
        elif section_name:
            call_data['section_name'] = section_name
            sym = editsection.get_symbol(project, section_name, call_data['schange'], location)
            page_data[("adminhead","page_head","large_text")] = "Edit Symbol in section : %s" % (section_name,)
        else:
            raise FailPage("Either a page or section must be specified")

    except ServerError as e:
        raise FailPage(e.message)

    # Set the symbol in the text area
    page_data["symbol_input","input_text"] = sym


def set_edit_symbol(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Submits new symbol after editing"

    project = call_data['editedprojname']
    location = call_data['location']

    if 'symbol' not in call_data:
        raise FailPage(message = "Invalid symbol")

    symbol = call_data['symbol']

    try:
        if 'page_number' in call_data:
            pagenumber = call_data['page_number']
            call_data['pchange'] = editpage.edit_page_symbol(project, pagenumber, call_data['pchange'], location, symbol)
        elif 'section_name' in call_data:
            section_name = call_data['section_name']
            call_data['schange'] = editsection.edit_section_symbol(project, section_name, call_data['schange'], location, symbol)
        else:
            raise ValidateError("Page/section not identified")
    except ServerError as e:
        raise FailPage(e.message)
    call_data['status'] = "Symbol changed"


def retrieve_edit_comment(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Fills in the edit html comment page"

    # a skilift.part_tuple is (project, pagenumber, page_part, section_name, name, location, part_type, brief)

    pagenumber = None
    section_name = None

    if 'part_tuple' in call_data:
        part_tuple = call_data['part_tuple']
        project = part_tuple.project
        location = part_tuple.location
        pagenumber = part_tuple.pagenumber
        section_name = part_tuple.section_name
    else:
        project = call_data['editedprojname']
        location = call_data['location']
        if 'page_number' in call_data:
            pagenumber = call_data['page_number']
        else:
            section_name = call_data['section_name']

    if (pagenumber is None) and (section_name is None):
        raise ValidateError("Page/section not identified")

    call_data['location'] = location

    try:

        if pagenumber:
            call_data['page_number'] = pagenumber
            com = editpage.get_comment(project, pagenumber, call_data['pchange'], location)
            page_data[("adminhead","page_head","large_text")] = "Edit Comment in page : %s" % (pagenumber,)
        elif section_name:
            call_data['section_name'] = section_name
            com = editsection.get_comment(project, section_name, call_data['schange'], location)
            page_data[("adminhead","page_head","large_text")] = "Edit Comment in section : %s" % (section_name,)
        else:
            raise FailPage("Either a page or section must be specified")

    except ServerError as e:
        raise FailPage(e.message)

    # Set the text in the input field
    page_data[("comment_input","input_text")] = com



def set_edit_comment(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Submits new comment after editing"

    project = call_data['editedprojname']
    location = call_data['location']

    if 'comment' not in call_data:
        raise FailPage(message = "Invalid symbol")

    comment = call_data['comment']

    try:
        if 'page_number' in call_data:
            pagenumber = call_data['page_number']
            call_data['pchange'] = editpage.edit_page_comment(project, pagenumber, call_data['pchange'], location, comment)
        elif 'section_name' in call_data:
            section_name = call_data['section_name']
            call_data['schange'] = editsection.edit_section_comment(project, section_name, call_data['schange'], location, comment)
        else:
            raise ValidateError("Page/section not identified")
    except ServerError as e:
        raise FailPage(e.message)
    call_data['status'] = "Comment changed"



def create_insert_comment(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Creates new html comment"

    project = call_data['editedprojname']

    try:

        if 'page_number' in call_data:
            pagenumber = call_data['page_number']
            page_info = skilift.item_info(project, pagenumber)
            if page_info is None:
                raise FailPage("Page to edit not identified")
            if (page_info.item_type != "TemplatePage") and (page_info.item_type != "SVG"):
                raise FailPage("Page not identified")

            call_data['pchange'], new_location = editpage.create_html_comment_in_page(project, pagenumber, call_data['pchange'], call_data['location'])

        elif 'section_name' in call_data:
            section_name = call_data['section_name']
            call_data['schange'], new_location = editsection.create_html_comment_in_section(project, section_name, call_data['schange'], call_data['location'])

        else:
            raise FailPage("Either a page or section must be specified")

    except ServerError as e:
        raise FailPage(e.message)
    call_data['location'] = new_location

