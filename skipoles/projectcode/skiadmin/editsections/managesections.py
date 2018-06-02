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
from ....skilift import fromjson, part_info, part_contents, editsection

# a search for anything none-alphanumeric and not an underscore
_AN = re.compile('[^\w]')

def retrieve_managepage(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    # this call is for the manage sections page

    project = call_data['editedprojname']

    page_data[("adminhead","page_head","large_text")] = "Manage Sections"

    # get current sections
    section_list = editsection.list_section_names(project)
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


def retrieve_section_dom(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "this call fills in the section dom table"

    project = call_data['editedprojname']

    if "section_name" in call_data:
        section_name = call_data["section_name"]
    else:
        raise FailPage(message = "Section name missing")

    if not section_name:
        raise FailPage(message = "Section name missing")

    section_list = editsection.list_section_names(project)
    if section_name not in section_list:
        raise FailPage(message = "Section name invalid")

    # fill in the section dom table

    # section location is a tuple of section_name, None for no container, () tuple of location integers
    section_location = (section_name, None, ())
    # get section_tuple from project, pagenumber, section_name, section_location
    section_tuple = part_info(project, None, section_name, section_location)

    # section_tuple is None if part not found, otherwise a namedtuple with items
    #  project, pagenumber, page_part, section_name, name, location, part_type, brief

    if section_tuple is None:
        raise FailPage("The section has not been recognised")

    try:
        partdict = fromjson.part_to_OD(project, None, section_name, section_location)
    except:
       raise FailPage(message = "call to fromjson.part_to_OD failed")

    # widget editdom,domtable is populated with fields

    #    dragrows: A two element list for every row in the table, could be empty if no drag operation
    #              0 - True if draggable, False if not
    #              1 - If 0 is True, this is data sent with the call wnen a row is dropped
    #    droprows: A two element list for every row in the table, could be empty if no drop operation
    #              0 - True if droppable, False if not
    #              1 - text to send with the call when a row is dropped here
    #    dropident: ident or label of target, called when a drop occurs which returns a JSON page

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

    if "attribs" in partdict:
        section_tag = '&lt;' + partdict['tag_name'] + ' ... &gt;'
    else:
        section_tag = '&lt;' + partdict['tag_name'] + '&gt;'

    section_brief = html.escape(partdict['brief'])

    if len( section_brief)>40:
        section_brief =  section_brief[:35] + '...'
    if not section_brief:
         section_brief = '-'

    domcontents = [
                   [section_tag, '', False, '' ],
                   [section_brief, '', False, '' ],
                   ['', '', False, '' ],                                             # no up arrow for top line
                   ['', '', False, '' ],                                             # no up_right arrow for top line
                   ['', '', False, '' ],                                             # no down arrow for top line
                   ['', '', False, '' ],                                             # no down_right arrow for top line
                   ['Edit',  'width : 1%;', True, section_name],                     # edit
                   ['Insert','width : 1%;text-align: center;', True, section_name],  # insert
                   ['', '', False, '' ],                                             # no remove image for top line
                ]

    # add further items to domcontents
    part_string_list = []

    if 'parts' not in partdict:
        rows = 1
    else:
        rows = utils.domtree(partdict, section_name, domcontents, part_string_list)
    
    page_data['editdom', 'domtable', 'contents']  = domcontents

    # for each column: html link, JSON link
    page_data['editdom', 'domtable', 'cols']  =  [    ['',''],                                  # tag name, no link
                                                      ['',''],                                  # brief, no link
                                                      ['move_up_in_section_dom',7540],          # up arrow
                                                      ['move_up_right_in_section_dom',7550],    # up right
                                                      ['move_down_in_section_dom',7560],        # down
                                                      ['move_down_right_in_section_dom',7570],  # down right
                                                      ['edit_section_dom',''],                  # edit, html only
                                                      ['add_to_section_dom',''],                # insert/append, html only
                                                      ['remove_section_dom',7520]               # remove
                                                   ]
    # for every row in the table
    dragrows = [ [ False, '']]
    droprows = [ [ True, section_name ]]

    # for each row (minus 1 as the first row is done)
    if rows > 1:
        for row in range(0, rows-1):
            dragrows.append( [ True, part_string_list[row]] )
            droprows.append( [ True, part_string_list[row]] )

    page_data['editdom', 'domtable', 'dragrows']  = dragrows
    page_data['editdom', 'domtable', 'droprows']  = droprows

    page_data['editdom', 'domtable', 'dropident']  = 'move_in_section_dom'


def retrieve_section_contents(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "this call is for the edit section contents page"

    # fill in section dom table
    retrieve_section_dom(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang)

    page_data[("adminhead","page_head","large_text")] = "Edit Section %s" % (call_data["section_name"],)

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
    project = call_data['editedprojname']
    if "delete_section" not in call_data:
        raise FailPage(message = "Section name missing from call_data", widget="table_error")
    section_name = call_data["delete_section"]
    if not section_name:
        raise FailPage(message = "Section name missing", widget="table_error")
    section_list = editsection.list_section_names(project)
    if section_name not in section_list:
        raise FailPage(message = "Section name does not exists", widget="table_error")
    # deletes the section
    try:
        editsection.delete_section(project, section_name)
    except ServerError as e:
        raise FailPage(message = e.message, widget = "table_error")
    call_data['status'] = 'Section %s deleted' % (section_name,)


def downloadsection(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Gets section, and returns a json dictionary, this will be sent as an octet file to be downloaded"
    if 'section_name' not in call_data:
        raise FailPage(message = "section missing")
    section_name = call_data["section_name"]
    project = call_data['editedprojname']
    jsonstring =  fromjson.section_to_json(project, section_name, indent=4)
    line_list = []
    n = 0
    for line in jsonstring.splitlines(True):
        binline = line.encode('utf-8')
        n += len(binline)
        line_list.append(binline)
    page_data['headers'] = [('content-type', 'application/octet-stream'), ('content-length', str(n))]
    return line_list


def newsectionpage(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Populate the page which creates a new section"
    project = call_data['editedprojname']
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
    section_list = editsection.list_section_names(project)
    if section_name in section_list:
        raise FailPage(message = "Section name already exists")
    page_data[("adminhead","page_head","large_text")] = "New Section"
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


def edit_section_dom(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Called by domtable to edit an item in a section"
    if ('editdom', 'domtable', 'contents') not in call_data:
        raise FailPage(message = "item to edit missing")
    editedprojname = call_data['editedprojname']
    part = call_data['editdom', 'domtable', 'contents']

    # so part is section name with location string of integers

    # create location which is a tuple or list consisting of three items:
    # a string of section name
    # a container integer, in this case always None
    # a tuple or list of location integers
    location_list = part.split('-')
    # first item should be a string, rest integers
    if len(location_list) == 1:
        # no location integers, so location_list[0] is the section name
        # edit the top section html part
        call_data['part'] = part
        raise GoTo(target = 53007, clear_submitted=True)

    section_name = location_list[0]

    location_integers = [ int(i) for i in location_list[1:]]
    part_tuple = part_info(editedprojname, None, section_name, [section_name, None, location_integers])
    if part_tuple is None:
        raise FailPage("Item to edit has not been recognised")

    if part_tuple.name:
        # item to edit is a widget
        call_data['part_tuple'] = part_tuple
        raise GoTo(target = 54006, clear_submitted=True)
    if part_tuple.part_type == "Part":
        # edit the html part
        call_data['part_tuple'] = part_tuple
        raise GoTo(target = 53007, clear_submitted=True)
    if part_tuple.part_type == "ClosedPart":
        # edit the html closed part
        call_data['part_tuple'] = part_tuple
        raise GoTo(target = 53007, clear_submitted=True)
    if part_tuple.part_type == "HTMLSymbol":
        # edit the symbol
        call_data['part_tuple'] = part_tuple
        raise GoTo(target = 51107, clear_submitted=True)
    if part_tuple.part_type == "str":
        # edit the text
        call_data['part_tuple'] = part_tuple
        raise GoTo(target = 51017, clear_submitted=True)
    if part_tuple.part_type == "TextBlock":
        # edit the TextBlock
        call_data['part_tuple'] = part_tuple
        raise GoTo(target = 52017, clear_submitted=True)
    if part_tuple.part_type == "Comment":
        # edit the Comment
        call_data['part_tuple'] = part_tuple
        raise GoTo(target = 51207, clear_submitted=True)

    # note : a sectionplaceholder cannot appear in a section
    raise FailPage("Item to edit has not been recognised")


def add_to_section_dom(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    """Called by domtable to either insert or append an item in a section
       sets page_data to populate the insert or append page and then go to appropriate template page"""

    if ('editdom', 'domtable', 'contents') not in call_data:
        raise FailPage(message = "item to edit missing")
    editedprojname = call_data['editedprojname']
    part = call_data['editdom', 'domtable', 'contents']
    location_list = part.split('-')
    # first item should be a string, rest integers
    if len(location_list) == 1:
        # no location integers, so location_list[0] is the section name
        location_integers = ()
    else:
        location_integers = tuple( int(i) for i in location_list[1:] )
    section_name = location_list[0]

    # location is a tuple of section_name, None for no container, tuple of location integers
    location = (section_name, None, location_integers)
    # get part_tuple from project, pagenumber, section_name, location
    part_tuple = part_info(editedprojname, None, section_name, location)
    if part_tuple is None:
        raise FailPage("Item to append to has not been recognised")
    # goto either the install or append page

    call_data['part'] = part                 ################ note, in future pass part_tuple rather than part
    call_data['location'] = location         ########## also part_tuple should replace location

    # Fill in menu of items, Part items have insert, others have append
    # as this is to be input into a section, a further section is not present in this list


    if (part_tuple.part_type == "Part") or (part_tuple.part_type == "Section"):
        # insert
        page_data[("adminhead","page_head","large_text")] = "Choose an item to insert"
        page_data[("insertlist","links")] = [
                                                ["Insert text", "inserttext", ""],
                                                ["Insert a TextBlock", "insert_textblockref", ""],
                                                ["Insert html symbol", "insertsymbol", ""],
                                                ["Insert comment", "insertcomment", ""],
                                                ["Insert an html element", "part_insert", ""],
                                                ["Insert a Widget", "list_widget_modules", ""]
                                            ]
        raise GoTo(target = '23609', clear_submitted=True)
    else:
        # append
        page_data[("adminhead","page_head","large_text")] = "Choose an item to append"
        page_data[("appendlist","links")] = [
                                                ["Append text", "inserttext", ""],
                                                ["Append a TextBlock", "insert_textblockref", ""],
                                                ["Append html symbol", "insertsymbol", ""],
                                                ["Append comment", "insertcomment", ""],
                                                ["Append an html element", "part_insert", ""],
                                                ["Append a Widget", "list_widget_modules", ""]
                                            ]
        raise GoTo(target = '23509', clear_submitted=True)


def remove_section_dom(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Called by domtable to remove an item in a section"

    if ('editdom', 'domtable', 'contents') not in call_data:
        raise FailPage(message = "item to edit missing")
    editedprojname = call_data['editedprojname']
    part = call_data['editdom', 'domtable', 'contents']

    # so part is section name with location string of integers

    # create location which is a tuple or list consisting of three items:
    # a string of section name
    # a container integer, in this case always None
    # a tuple or list of location integers
    location_list = part.split('-')
    # first item should be a string, rest integers
    if len(location_list) == 1:
        # no location integers
        raise FailPage("Item to remove has not been recognised")

    location_integers = tuple( int(i) for i in location_list[1:] )
    section_name = location_list[0]

    # location is a tuple of section_name, None for no container, tuple of location integers
    location = (section_name, None, location_integers)
    # get part_tuple from project, pagenumber, section_name, location
    part_tuple = part_info(editedprojname, None, section_name, location)
    if part_tuple is None:
        raise FailPage("Item to remove has not been recognised")

    # once item is deleted, no info on the item should be
    # left in call_data - this may not be required in future
    if 'location' in call_data:
        del call_data['location']
    if 'part' in call_data:
        del call_data['part']
    if 'part_loc' in call_data:
        del call_data['part_loc']

    # remove the item
    try:
        call_data['schange'] = editsection.del_location(editedprojname, section_name, call_data['schange'], location)
    except ServerError as e:
        raise FailPage(message = e.message)

    call_data['status'] = 'Item deleted'


def move_up_in_section_dom(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Called by domtable to move an item in a section up"

    if ('editdom', 'domtable', 'contents') not in call_data:
        raise FailPage(message = "item to edit missing")
    editedprojname = call_data['editedprojname']
    part = call_data['editdom', 'domtable', 'contents']

    # so part is section name with location string of integers

    # create location which is a tuple or list consisting of three items:
    # a string of section name
    # a container integer, in this case always None
    # a tuple or list of location integers
    location_list = part.split('-')
    # first item should be a string, rest integers
    if len(location_list) == 1:
        # no location integers
        return
    else:
        location_integers = tuple( int(i) for i in location_list[1:] )
    section_name = location_list[0]

    # location is a tuple of section_name, None for no container, tuple of location integers
    location = (section_name, None, location_integers)
    # get part_tuple from project, pagenumber, section_name, location
    part_tuple = part_info(editedprojname, None, section_name, location)
    if part_tuple is None:
        raise FailPage("Item to move has not been recognised")

    if (len(location_integers) == 1) and (location_integers[0] == 0):
        # at top, cannot be moved
        raise FailPage("Cannot be moved up")

    if location_integers[-1] == 0:
        # move up to next level
        new_location_integers = location_integers[:-1]
    else:
        # swap parts on same level
        new_location_integers = list(location_integers[:-1])
        new_location_integers.append(location_integers[-1] - 1)

    # after a move, location is wrong, so remove from call_data
    if 'location' in call_data:
        del call_data['location']
    if 'part' in call_data:
        del call_data['part']
    if 'part_top' in call_data:
        del call_data['part_top']
    if 'part_loc' in call_data:
        del call_data['part_loc']

    # move the item
    try:
        editsection.move_location(editedprojname, section_name, location, (section_name, None, new_location_integers))
    except ServerError as e:
        raise FailPage(message = e.message)


def move_up_right_in_section_dom(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Called by domtable to move an item in a section up and to the right"

    if ('editdom', 'domtable', 'contents') not in call_data:
        raise FailPage(message = "item to edit missing")
    editedprojname = call_data['editedprojname']
    part = call_data['editdom', 'domtable', 'contents']

    # so part is section name with location string of integers

    # create location which is a tuple or list consisting of three items:
    # a string of section name
    # a container integer, in this case always None
    # a tuple or list of location integers
    location_list = part.split('-')
    # first item should be a string, rest integers
    if len(location_list) == 1:
        # no location integers, so location_list[0] is the section name
        return
    else:
        location_integers = tuple( int(i) for i in location_list[1:] )
    section_name = location_list[0]

    # location is a tuple of section_name, None for no container, tuple of location integers
    location = (section_name, None, location_integers)
    # get part_tuple from project, pagenumber, section_name, location
    part_tuple = part_info(editedprojname, None, section_name, location)
    if part_tuple is None:
        raise FailPage("Item to move has not been recognised")

    if location_integers[-1] == 0:
        # at top of a part, cannot be moved
        raise FailPage("Cannot be moved up")
    new_parent_integers = list(location_integers[:-1])
    new_parent_integers.append(location_integers[-1] - 1)
    new_parent_location = (section_name, None, new_parent_integers)

    new_parent_tuple = part_info(editedprojname, None, section_name, new_parent_location)

    if new_parent_tuple is None:
        raise FailPage("Cannot be moved up")
    if new_parent_tuple.part_type != "Part":
        raise FailPage("Cannot be moved up")

    items_in_new_parent = len(part_contents(editedprojname, None, section_name, new_parent_location))

    new_location_integers =  tuple(new_parent_integers + [items_in_new_parent])

    # after a move, location is wrong, so remove from call_data
    if 'location' in call_data:
        del call_data['location']
    if 'part' in call_data:
        del call_data['part']
    if 'part_top' in call_data:
        del call_data['part_top']
    if 'part_loc' in call_data:
        del call_data['part_loc']

    # move the item
    try:
        editsection.move_location(editedprojname, section_name, location, (section_name, None, new_location_integers))
    except ServerError as e:
        raise FailPage(message = e.message)


def move_down_in_section_dom(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Called by domtable to move an item in a section down"

    if ('editdom', 'domtable', 'contents') not in call_data:
        raise FailPage(message = "item to edit missing")
    editedprojname = call_data['editedprojname']
    part = call_data['editdom', 'domtable', 'contents']

    # so part is section name with location string of integers

    # create location which is a tuple or list consisting of three items:
    # a string of section name
    # a container integer, in this case always None
    # a tuple or list of location integers
    location_list = part.split('-')
    # first item should be a string, rest integers
    if len(location_list) == 1:
        # no location integers, the section top cannot be moved
        return
    else:
        location_integers = tuple( int(i) for i in location_list[1:] )
    section_name = location_list[0]

    # location is a tuple of section_name, None for no container, tuple of location integers
    location = (section_name, None, location_integers)
    # get part_tuple from project, pagenumber, section_name, location
    part_tuple = part_info(editedprojname, None, section_name, location)
    if part_tuple is None:
        raise FailPage("Item to move has not been recognised")

    if len(location_integers) == 1:
        # Just at immediate level below top
        parent_location = (section_name, None, ())
        items_in_parent = len(part_contents(editedprojname, None, section_name, parent_location))
        if location_integers[0] == (items_in_parent-1):
            # At end, cannot be moved
            raise FailPage("Cannot be moved down")
        new_location_integers = (location_integers[0]+2,)
    else:
        parent_integers = tuple(location_integers[:-1])
        parent_location = (section_name, None, parent_integers)
        items_in_parent = len(part_contents(editedprojname, None, section_name, parent_location))
        if location_integers[-1] == (items_in_parent-1):
            # At end of a part, so move up a level
            new_location_integers = list(parent_integers[:-1])
            new_location_integers.append(parent_integers[-1] + 1)
        else:
            # just insert into current level
            new_location_integers = list(parent_integers)
            new_location_integers.append(location_integers[-1] + 2)

    # after a move, location is wrong, so remove from call_data
    if 'location' in call_data:
        del call_data['location']
    if 'part' in call_data:
        del call_data['part']
    if 'part_top' in call_data:
        del call_data['part_top']
    if 'part_loc' in call_data:
        del call_data['part_loc']

    # move the item
    try:
        editsection.move_location(editedprojname, section_name, location, (section_name, None, new_location_integers))
    except ServerError as e:
        raise FailPage(message = e.message)


def move_down_right_in_section_dom(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Called by domtable to move an item in a section down and to the right"

    if ('editdom', 'domtable', 'contents') not in call_data:
        raise FailPage(message = "item to edit missing")
    editedprojname = call_data['editedprojname']
    part = call_data['editdom', 'domtable', 'contents']

    # so part is section name with location string of integers

    # create location which is a tuple or list consisting of three items:
    # a string of section name
    # a container integer, in this case always None
    # a tuple or list of location integers
    location_list = part.split('-')
    # first item should be a string, rest integers
    if len(location_list) == 1:
        # no location integers, the section top cannot be moved
        return
    else:
        location_integers = tuple( int(i) for i in location_list[1:] )
    section_name = location_list[0]

    # location is a tuple of section_name, None for no container, tuple of location integers
    location = (section_name, None, location_integers)
    # get part_tuple from project, pagenumber, section_name, location
    part_tuple = part_info(editedprojname, None, section_name, location)
    if part_tuple is None:
        raise FailPage("Item to move has not been recognised")

    if len(location_integers) == 1:
        parent_location = (section_name, None, ())
    else:
        parent_integers = list(location_integers[:-1])
        parent_location = (section_name, None, parent_integers)
    items_in_parent = len(part_contents(editedprojname, None, section_name, parent_location))
    if location_integers[-1] == (items_in_parent-1):
        # At end of a block, cannot be moved
        raise FailPage("Cannot be moved down")
    new_parent_integers = list(location_integers[:-1])
    new_parent_integers.append(location_integers[-1] + 1)
    new_parent_location = (section_name, None, new_parent_integers)
    new_parent_tuple = part_info(editedprojname, None, section_name, new_parent_location)

    if new_parent_tuple is None:
        raise FailPage("Cannot be moved down")
    if not (new_parent_tuple.part_type == 'Part' or new_parent_tuple.part_type == 'Section'):
        raise FailPage("Cannot be moved down")

    new_location_integers = tuple(new_parent_integers+[0])

    # after a move, location is wrong, so remove from call_data
    if 'location' in call_data:
        del call_data['location']
    if 'part' in call_data:
        del call_data['part']
    if 'part_top' in call_data:
        del call_data['part_top']
    if 'part_loc' in call_data:
        del call_data['part_loc']

    # move the item
    try:
        editsection.move_location(editedprojname, section_name, location, (section_name, None, new_location_integers))
    except ServerError as e:
        raise FailPage(message = e.message)



def move_in_section_dom(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Called by domtable to move an item in a section after a drag and drop"

    if ('editdom', 'domtable', 'dragrows') not in call_data:
        raise FailPage(message = "item to drop missing")
    editedprojname = call_data['editedprojname']
    part_to_move = call_data['editdom', 'domtable', 'dragrows']

    # so part_to_move is section name with location string of integers

    # create location which is a tuple or list consisting of three items:
    # a string of section name
    # a container integer, in this case always None
    # a tuple or list of location integers
    location_to_move_list = part_to_move.split('-')
    # first item should be a string, rest integers
    if len(location_to_move_list) == 1:
        # no location integers, the section top cannot be moved
        return
    else:
        location_to_move_integers = tuple( int(i) for i in location_to_move_list[1:] )
    section_name = location_to_move_list[0]

    # location is a tuple of section_name, None for no container, tuple of location integers
    location_to_move = (section_name, None, location_to_move_integers)
    # get part_tuple from project, pagenumber, section_name, location
    part_to_move_tuple = part_info(editedprojname, None, section_name, location_to_move)
    if part_to_move_tuple is None:
        raise FailPage("Item to move has not been recognised")


    # new location

    target_part = call_data['editdom', 'domtable', 'droprows']

    # so target_part is section name with location string of integers

    # create location which is a tuple or list consisting of three items:
    # a string of section name
    # a container integer, in this case always None
    # a tuple or list of location integers
    target_location_list = target_part.split('-')
    # first item should be a string, rest integers
    if len(target_location_list) == 1:
        # no location integers
        target_location_integers = ()
    else:
        target_location_integers = tuple( int(i) for i in target_location_list[1:] )

    if section_name != target_location_list[0]:
        raise FailPage("Target location has not been recognised")

    # location is a tuple of section_name, None for no container, tuple of location integers
    target_location = (section_name, None, target_location_integers)
    # get part_tuple from project, pagenumber, section_name, location
    target_part_tuple = part_info(editedprojname, None, section_name, target_location)
    if target_part_tuple is None:
        raise FailPage("Target has not been recognised")

    if (target_part_tuple.part_type == "Part") or (target_part_tuple.part_type == "Section"):
        # insert
        if target_location_integers:
            new_location_integers = list(target_location_integers)
            new_location_integers.append(0)
        else:
            new_location_integers = [0]
    else:
        # append
        new_location_integers = list(target_location_integers)
        new_location_integers[-1] = new_location_integers[-1] + 1

    # after a move, location is wrong, so remove from call_data
    if 'location' in call_data:
        del call_data['location']
    if 'part' in call_data:
        del call_data['part']
    if 'part_top' in call_data:
        del call_data['part_top']
    if 'part_loc' in call_data:
        del call_data['part_loc']

    # move the item
    try:
        editsection.move_location(editedprojname, section_name, location_to_move, (section_name, None, new_location_integers))
    except ServerError as e:
        raise FailPage(message = e.message)




