####### SKIPOLE WEB FRAMEWORK #######
#
# managesections.py  - managing and editing sections
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


import pkgutil, re, html

from .. import utils
from ....ski.excepts import FailPage, ValidateError, GoTo, ServerError
from ....ski import tag
from ....ski import widgets
from ....skilift import fromjson

# a search for anything none-alphanumeric and not an underscore
_AN = re.compile('[^\w]')

def retrieve_managepage(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    # this call is for the manage sections page

    editedproj = call_data['editedproj']

    page_data[("adminhead","page_head","large_text")] = "Manage Sections"

    if 'status' in call_data:
        page_data[("adminhead","page_head","small_text")] = call_data['status']
    else:
        page_data[("adminhead","page_head","small_text")] = "Set or edit sections"

    # get current sections
    section_list = editedproj.list_section_names()
    if not section_list:
        page_data[("tabledescription", "show")] = False
        page_data[("sectiontable", "show")] = False
        return

    # fill in the sections table

    #       contents: col 0 is the text to place in the first column,
    #                  col 1, 2, 3, 4 are the get field contents of links 1,2,3 and 4
    #                  col 5 - True if the first button and link is to be shown, False if not
    #                  col 6 - True if the second button and link is to be shown, False if not
    #                  col 7 - True if the third button and link is to be shown, False if not
    #                  col 8 - True if the fourth button and link is to be shown, False if not

    contents = []
    for section_name in section_list:
        contents.append([ section_name, section_name, section_name, '', '', True, True, False, False ])

    page_data[("sectiontable", "contents")] = contents

    # clear call_data, as no session info needed from this page
    utils.no_ident_data(call_data)


def retrieve_section_contents(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "this call is for the edit section contents page"

    editedproj = call_data['editedproj']

    if "section_name" in call_data:
        section_name = call_data["section_name"]
    else:
        raise FailPage(message = "Section name missing")

    if not section_name:
        raise FailPage(message = "Section name missing")

    section_list = editedproj.list_section_names()
    if section_name not in section_list:
        raise FailPage(message = "Section name invalid", widget="table_error")

    section = editedproj.section(section_name)

    page_data[("adminhead","page_head","large_text")] = "Edit Section %s" % (section_name,)

    if 'status' in call_data:
        page_data[("adminhead","page_head","small_text")] = call_data['status']
    else:
        page_data[("adminhead","page_head","small_text")] = "Set section contents"


    #        contents: A list for every element in the table, should be row*col lists
    #              col 0 - text string (This will be either text to display, button text, or Textblock reference)
    #               col 1 - True if this is a TextBlock, False if not
    #               col 2 - A 'style' string set on the td cell, if empty string, no style applied
    #               col 3 - Link ident, if empty, only text will be shown, not a button
    #                             if given, a link will be set with button_class applied to it
    #              col 4 - The get field value of the button link, empty string if no get field, ignored if no link ident given

    page_data['editparts', 'parts', 'cols']  = 9
    rows = 1

    if section.attribs:
        tag_name = '<' + section.tag_name + ' ... >'
    else:
        tag_name = '<' + section.tag_name + '>'

    section_brief = html.escape(section.brief)

    if len( section_brief)>40:
        section_brief =  section_brief[:35] + '...'
    if not section_brief:
         section_brief = '-'

    no_link = [False, '', '']
    empty = ['', False, '', '']

    contents = [
                   [tag_name] + no_link,              # col 0 the <div> text (or whatever section tag is used)
                   [section_brief] + no_link,
                   empty,                                       # no up arrow for top line
                   empty,                                       # no up_right arrow for top line
                   empty,                                       # no down arrow for top line
                   empty,                                       # no down_right arrow for top line
                   ['Edit', False, 'width : 1%;', 'get_part_edit', section_name],                 # edit - link to part_edit = 43101
                   ['Insert', False, 'width : 1%;text-align: center;', 'new_insert', section_name],             # insert - link to page 43102
                   empty                                       # no remove image for top line
                ]

    rows = utils.extendparts(rows, section, section_name, contents, no_link, empty)

    page_data['editparts', 'parts', 'contents']  = contents
    page_data['editparts', 'parts', 'rows']  = rows

    ####################################################
    # new editdom,domtable


    #    cols: A two element list for every column in the table, must be given with empty values if no links
    #              0 - target HTML page link ident of buttons in each column, if col1 not present or no javascript
    #              1 - target JSON page link ident of buttons in each column,

    #    contents: A list for every element in the table, should be row*col lists
    #               0 - text string, either text to display or button text
    #               1 - A 'style' string set on the td cell, if empty string, no style applied
    #               2 - Is button? If False only text will be shown, not a button, button class will not be applied
    #                       If True a link to link_ident/json_ident will be set with button_class applied to it
    #               3 - The get field value of the button link, empty string if no get field

    # create first row of the table

    if section.attribs:
        section_tag = '&lt;' + section.tag_name + ' ... &gt;'
    else:
        section_tag = '&lt;' + section.tag_name + '&gt;'

    domcontents = [
                   [section_tag, '', False, '' ],
                   [section_brief, '', False, '' ],
                   ['', '', False, '' ],                                             # no up arrow for top line
                   ['', '', False, '' ],                                             # no up_right arrow for top line
                   ['', '', False, '' ],                                             # no down arrow for top line
                   ['', '', False, '' ],                                             # no down_right arrow for top line
                   ['Edit',  'width : 1%;', True, section_name],                     # edit - link to part_edit = 43101
                   ['Insert','width : 1%;text-align: center;', True, section_name],  # insert - link to page 43102
                   ['', '', False, '' ],                                             # no remove image for top line
                ]

    # add further items to domcontents
    rows = utils.domcontents(section, section_name, domcontents)


    page_data['editdom', 'domtable', 'contents']  = domcontents
    page_data['editdom', 'domtable', 'cols']  =  [    ['',''],                    # tag name
                                                      ['',''],                    # brief
                                                      ['admin_home',''],          # up arrow
                                                      ['admin_home',''],          # up right
                                                      ['admin_home',''],          # down
                                                      ['admin_home',''],          # down right
                                                      ['edit_section_dom',''],    # edit
                                                      ['admin_home',''],          # insert/append
                                                      ['remove_section_dom','']   # remove
                                                   ]

    ###############################################################


    # remove any unwanted fields from session call_data
    if 'location' in call_data:
        del call_data['location']
    if 'field_arg' in call_data:
        del call_data['field_arg']
    if 'validx' in call_data:
        del call_data['validx']
    if 'module' in call_data:
        del call_data['module']
    if 'widget_name' in call_data:
        del call_data['widget_name']
    if 'container' in call_data:
        del call_data['container']
    if 'widgetclass' in call_data:
        del call_data['widgetclass']

    # set the section into call_data
    call_data['section'] = section


def submit_new_section(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Create new section"

    editedproj = call_data['editedproj']

    # get new section name

    if ("newsection", "section_name") not in call_data:
        raise FailPage(message = "Section name missing from call_data")
    section_name = call_data["newsection", "section_name"]
    if not section_name:
        raise FailPage(message = "Section name missing")
    section_lower_name = section_name.lower()
    if (section_lower_name == 'body') or (section_lower_name == 'head') or (section_lower_name == 'svg'):
        raise FailPage(message="Unable to create the section, the name given is reserved")
    if _AN.search(section_name):
        raise FailPage(message="Invalid section name, alphanumeric and underscore only")
    if section_name[0] == '_':
        raise FailPage(message="Invalid section name, must not start with an underscore")
    if section_name.isdigit():
        raise FailPage(message="Unable to create the section, the name must include some letters")
    section_list = editedproj.list_section_names()
    if section_name in section_list:
        raise FailPage(message = "Section name already exists", widget="new")

    tag_name = call_data['new_tag', 'input_text']
    tag_brief = call_data['description', 'input_text']

    # adds a section consisting of a div
    section_part = tag.Section(tag_name=tag_name, brief=tag_brief)
    try:
        editedproj.add_section(section_name, section_part)
    except (ValidateError, ServerError) as e:
        raise FailPage(message = e.message)

    # new section created
    utils.no_ident_data(call_data)
    call_data['status'] = 'Section %s created' % (section_name,)


def delete_section(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Deletes a section"

    editedproj = call_data['editedproj']

    if "delete_section" not in call_data:
        raise FailPage(message = "Section name missing from call_data", widget="table_error")
    section_name = call_data["delete_section"]
    if not section_name:
        raise FailPage(message = "Section name missing", widget="table_error")

    section_list = editedproj.list_section_names()
    if section_name not in section_list:
        raise FailPage(message = "Section name does not exists", widget="table_error")
    # deletes the section
    try:
        editedproj.delete_section(section_name)
    except (ValidateError, ServerError) as e:
        raise FailPage(message = e.message, widget = "table_error")
    call_data['status'] = 'Section %s deleted' % (section_name,)


def downloadsection(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Gets section, and returns a json dictionary, this will be sent as an octet file to be downloaded"
    if 'section_name' not in call_data:
        raise FailPage(message = "section missing")
    section_name = call_data["section_name"]
    project = call_data['editedproj']
    jsonstring =  fromjson.section_to_json(project.proj_ident, section_name, indent=4)
    line_list = []
    n = 0
    for line in jsonstring.splitlines(True):
        binline = line.encode('utf-8')
        n += len(binline)
        line_list.append(binline)
    page_data['headers'] = [('content-type', 'application/octet-stream'), ('content-length', str(n))]
    return line_list


def newsectionpage(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):

    editedproj = call_data['editedproj']

    if 'section_name' not in call_data:
        raise FailPage(message = "new section name missing")
    section_name = call_data["section_name"]
    if not section_name:
        raise FailPage(message = "Section name missing")
    section_lower_name = section_name.lower()
    if (section_lower_name == 'body') or (section_lower_name == 'head') or (section_lower_name == 'svg'):
        raise FailPage(message="Unable to create the section, the name given is reserved")
    if _AN.search(section_name):
        raise FailPage(message="Invalid section name, alphanumeric and underscore only")
    if section_name[0] == '_':
        raise FailPage(message="Invalid section name, must not start with an underscore")
    if section_name.isdigit():
        raise FailPage(message="Unable to create the section, the name must include some letters")
    section_list = editedproj.list_section_names()
    if section_name in section_list:
        raise FailPage(message = "Section name already exists", widget="new")

    page_data[("adminhead","page_head","large_text")] = "New Section"

    if 'status' in call_data:
        page_data[("adminhead","page_head","small_text")] = call_data['status']
    else:
        page_data[("adminhead","page_head","small_text")] = "Create new section %s" % (section_name,)

    page_data["description", "input_text"] = "New section %s" % (section_name,)

    # set hidden fields on the two forms with the submitted section name
    page_data["newsection", "section_name"] = section_name
    page_data["uploadsection","section_name"] = section_name


def file_new_section(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Create new section from uploaded file"

    editedproj = call_data['editedproj']

    # get new section name

    if ("uploadsection", "section_name") not in call_data:
        raise FailPage(message = "Section name missing from call_data")
    section_name = call_data["uploadsection", "section_name"]
    if not section_name:
        raise FailPage(message = "Section name missing")
    section_lower_name = section_name.lower()
    if (section_lower_name == 'body') or (section_lower_name == 'head') or (section_lower_name == 'svg'):
        raise FailPage(message="Unable to create the section, the name given is reserved")
    if _AN.search(section_name):
        raise FailPage(message="Invalid section name, alphanumeric and underscore only")
    if section_name[0] == '_':
        raise FailPage(message="Invalid section name, must not start with an underscore")
    if section_name.isdigit():
        raise FailPage(message="Unable to create the section, the name must include some letters")
    section_list = editedproj.list_section_names()
    if section_name in section_list:
        raise FailPage(message = "Section name already exists", widget="new")

    # get file contents
    file_contents = call_data["uploadsection", "action"]
    json_string = file_contents.decode(encoding='utf-8')
    # create the section
    try:
        fromjson.create_section(editedproj.proj_ident, section_name, json_string)
    except ServerError as e:
        raise FailPage(message = e.message)

    # new section created
    utils.no_ident_data(call_data)
    call_data['status'] = 'Section %s created' % (section_name,)

