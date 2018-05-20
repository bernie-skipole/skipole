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
from ....skilift import item_info, fromjson, editpage, editsection


def retrieve_insert(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Fills in the insert an html element page header"
    project = call_data['editedprojname']
    if 'page_number' in call_data:
        pageinfo = skilift.item_info(project, call_data['page_number'])
        if (pageinfo.item_type != "TemplatePage") and (pageinfo.item_type != "SVG"):
            raise FailPage("Invalid page")
        # Fill in header
        page_data[("adminhead","page_head","large_text")] = "Insert an HTML element into %s,%s" % (project, call_data['page_number'])
    elif 'section_name' in call_data:
        page_data[("adminhead","page_head","large_text")] = "Insert an HTML element into section " + call_data['section_name']
    else:
        raise FailPage("Insertion page/section for html element is missing")


def create_insert(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Creates the html element"
    project = call_data['editedprojname']
    part_top, container, location_integers = call_data['location']

    if call_data['newopenclosed'] == 'open':
        opentag = True
    else:
        opentag = False

    if 'page_number' in call_data:
        pagenumber = call_data['page_number']
        page_info = item_info(project, pagenumber)
        if page_info is None:
            raise FailPage("Page to edit not identified")

        if (page_info.item_type != "TemplatePage") and (page_info.item_type != "SVG"):
            raise FailPage("Page not identified")

        # page to go back to
        target = None
        if part_top == 'head':
            target = "page_head"
        elif part_top == 'body':
            target = "page_body"
        elif part_top == 'svg':
            target = "page_svg"

        if container is not None:
            target = "back_to_container"

        if target is None:
            raise FailPage("Invalid location")

        try:
            call_data['pchange'] = editpage.create_html_element_in_page(project,
                                                                        pagenumber,
                                                                        call_data['pchange'],
                                                                        call_data['location'],
                                                                        call_data['newpartname'],
                                                                        call_data['newbrief'],
                                                                        opentag)
        except ServerError as e:
            raise FailPage(e.message)
        call_data['status'] = 'New tag inserted'
        raise GoTo(target = target, clear_submitted=True)


    if 'section_name' in call_data:
        section_name = call_data['section_name']

        if container is not None:
            target = "back_to_container"
        else:
            target = "back_to_section"

        try:
            call_data['schange'] = editsection.create_html_element_in_section(project,
                                                                              section_name,
                                                                              call_data['schange'],
                                                                              call_data['location'],
                                                                              call_data['newpartname'],
                                                                              call_data['newbrief'],
                                                                              opentag)
        except ServerError as e:
            raise FailPage(e.message)
        call_data['status'] = 'New tag inserted'
        raise GoTo(target = target, clear_submitted=True)

    raise FailPage("Either a page or section must be specified")


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
        call_data['page'] = skiboot.from_ident(page.ident)

    if parent_widget:
        call_data['widget_name'] = parent_widget

    # new part created
    call_data['status'] = 'New block created'
    raise GoTo(target = label, clear_submitted=True)

