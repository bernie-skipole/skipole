


import pkgutil, re, html, json

from .. import utils
from ... import FailPage, ValidateError, GoTo, ServerError
from ....skilift import fromjson, part_info, part_contents, editsection, versions

# a search for anything none-alphanumeric and not an underscore
_AN = re.compile('[^\w]')

def retrieve_managepage(skicall):
    "this call is for the manage sections page"

    call_data = skicall.call_data
    page_data = skicall.page_data

    # clears any session data
    utils.clear_call_data(call_data)

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



def retrieve_section_dom(skicall):
    "this call fills in the section dom table"

    call_data = skicall.call_data
    page_data = skicall.page_data

    # clears any session data, keeping section_name and schange
    utils.clear_call_data(call_data, ["section_name", "schange"])

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

    call_data['schange'] = editsection.sectionchange(project, section_name)

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
        domcontents, dragrows, droprows = _section_domcontents(project, section_name)
    except ServerError as e:
        raise FailPage(message=e.message)


    # widget editdom,domtable is populated with fields

    #    dragrows: A two element list for every row in the table, could be empty if no drag operation
    #              0 - True if draggable, False if not
    #              1 - If 0 is True, this is data sent with the call wnen a row is dropped
    #    droprows: A two element list for every row in the table, could be empty if no drop operation
    #              0 - True if droppable, False if not
    #              1 - text to send with the call when a row is dropped here
    #    dropident: ident or label of target, called when a drop occurs which returns a JSON page

    #    cols: A three element list for every column in the table, must be given with empty values if no links
    #              0 - target HTML page link ident of buttons in each column, if col1 not present or no javascript
    #              1 - target JSON page link ident of buttons in each column,
    #              2 - session storage key 'ski_part'

    #    contents: A list for every element in the table, should be row*col lists
    #               0 - text string, either text to display or button text
    #               1 - A 'style' string set on the td cell, if empty string, no style applied
    #               2 - Is button? If False only text will be shown, not a button, button class will not be applied
    #                       If True a link to link_ident/json_ident will be set with button_class applied to it
    #               3 - The get field value of the button link, empty string if no get field

    page_data['editdom', 'domtable', 'contents']  = domcontents
    page_data['editdom', 'domtable', 'dragrows']  = dragrows
    page_data['editdom', 'domtable', 'droprows']  = droprows

    # for each column: html link, JSON link, storage key
    page_data['editdom', 'domtable', 'cols']  =  [    ['','',''],                                             # tag name, no link
                                                      ['','',''],                                             # brief, no link
                                                      ['no_javascript','move_up_in_section_dom',''],          # up arrow
                                                      ['no_javascript','move_up_right_in_section_dom',''],    # up right
                                                      ['no_javascript','move_down_in_section_dom',''],        # down
                                                      ['no_javascript','move_down_right_in_section_dom',''],  # down right
                                                      ['edit_section_dom','',''],                             # edit, html only
                                                      ['no_javascript','insert_in_section',''],               # insert/append
                                                      ['no_javascript',7580,''],                              # copy
                                                      ['no_javascript',7590,'ski_part'],                      # paste
                                                      ['no_javascript','cut_section_dom',''],                 # cut
                                                      ['no_javascript','delete_section_dom','']               # delete
                                                   ]

    page_data['editdom', 'domtable', 'dropident']  = 'move_in_section_dom'


def retrieve_section_contents(skicall):
    "this call is for the edit section contents page"
    # fill in section dom table
    retrieve_section_dom(skicall)
    # set page head text
    skicall.page_data[("adminhead","page_head","large_text")] = "Edit Section %s" % (skicall.call_data["section_name"],)


def submit_new_section(skicall):
    "Create new section"

    call_data = skicall.call_data
    page_data = skicall.page_data

    project = call_data['editedprojname']
    # get new section name
    if ("newsection", "section_name") not in call_data:
        raise FailPage(message = "Section name missing from call_data")
    section_name = call_data["newsection", "section_name"]
    if ('new_tag', 'input_text') in call_data:
        tag_name = call_data['new_tag', 'input_text']
    else:
        tag_name = 'div'
    if ('description', 'input_text') in call_data:
        brief = call_data['description', 'input_text']
    else:
        brief = "New Section"
    try:
        editsection.create_new_section(project, section_name, tag_name, brief)
    except (ValidateError, ServerError) as e:
        raise FailPage(message = e.message)
    utils.clear_call_data(call_data)
    call_data['status'] = 'Section %s created' % (section_name,)


def delete_section(skicall):
    "Deletes a section"

    call_data = skicall.call_data
    page_data = skicall.page_data

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


def downloadsection(skicall):
    "Gets section, and returns a json dictionary, this will be sent as an octet file to be downloaded"

    call_data = skicall.call_data
    page_data = skicall.page_data

    if 'section_name' not in call_data:
        raise FailPage(message = "section missing")
    section_name = call_data["section_name"]
    project = call_data['editedprojname']

    parttext, part_dict = fromjson.section_outline(project, section_name)
    # set version and skipole as the first two items in the dictionary
    versions_tuple = versions(project)
    part_dict["skipole"] = versions_tuple.skipole
    part_dict.move_to_end('skipole', last=False)
    part_dict["version"] = versions_tuple.project
    part_dict.move_to_end('version', last=False)
    jsonstring = json.dumps(part_dict, indent=4, separators=(',', ':'))
    line_list = []
    n = 0
    for line in jsonstring.splitlines(True):
        binline = line.encode('utf-8')
        n += len(binline)
        line_list.append(binline)
    page_data['headers'] = [('content-type', 'application/octet-stream'), ('content-length', str(n))]
    return line_list



def newsectionpage(skicall):
    "Populate the page which creates a new section"

    call_data = skicall.call_data
    page_data = skicall.page_data

    project = call_data['editedprojname']
    if 'new_section_name' not in call_data:
        raise FailPage(message = "new section name missing")
    section_name = call_data["new_section_name"]
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


def file_new_section(skicall):
    "Create new section from uploaded file"

    call_data = skicall.call_data
    page_data = skicall.page_data

    project = call_data['editedprojname']

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
    section_list = editsection.list_section_names(project)
    if section_name in section_list:
        raise FailPage(message = "Section name already exists", widget="new")

    # get file contents
    file_contents = call_data["uploadsection", "action"]
    json_string = file_contents.decode(encoding='utf-8')
    # create the section
    try:
        fromjson.create_section(project, section_name, json_string)
    except ServerError as e:
        raise FailPage(message = e.message)

    # new section created
    utils.clear_call_data(call_data)
    call_data['status'] = 'Section %s created' % (section_name,)


def edit_section_dom(skicall):
    "Called by domtable to edit an item in a section"

    call_data = skicall.call_data
    page_data = skicall.page_data

    if ('editdom', 'domtable', 'contents') not in call_data:
        raise FailPage(message = "item to edit missing")
    editedprojname = call_data['editedprojname']
    part = call_data['editdom', 'domtable', 'contents']

    # so part is section name with location string of integers
    # though string of integers may be missing if this is the section part itself

    # create location which is a tuple or list consisting of three items:
    # a string of section name
    # a container integer, in this case always None
    # a tuple or list of location integers
    location_list = part.split('-')
    # first item should be a string, rest integers
    if len(location_list) == 1:
        # no location integers, so location_list[0] is the section name, location_integers is ()
        # edit the top section html part
        call_data['part_tuple'] = part_info(editedprojname, None, location_list[0], [location_list[0], None, ()])
        raise GoTo(target = 53007, clear_submitted=True)

    section_name = location_list[0]
    call_data['section_name'] = section_name
    call_data['schange'] = editsection.sectionchange(editedprojname, section_name)

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



def copy_section(skicall):
    "Gets section part and return it in page_data['localStorage'] with key ski_part for browser session storage"
    call_data = skicall.call_data
    page_data = skicall.page_data

    if ('editdom', 'domtable', 'contents') not in call_data:
        raise FailPage(message = "item to copy missing")
    editedprojname = call_data['editedprojname']
    part = call_data['editdom', 'domtable', 'contents']

    # so part is section name with location string of integers
    # though string of integers may be missing if this is the section part itself

    # create location which is a tuple or list consisting of three items:
    # a string of section name
    # a container integer, in this case always None
    # a tuple or list of location integers
    location_list = part.split('-')
    section_name = location_list[0]
    # first item should be a string, rest integers
    if len(location_list) == 1:
        # no location integers, so location_list[0] is the section name, location_integers is ()
        location_integers = ()
    else:
        location_integers = tuple( int(i) for i in location_list[1:] )
    # location is a tuple of section_name, None for no container, tuple of location integers
    location = (section_name, None, location_integers)

    # get a json string dump of the item outline, however change any Sections to Parts
    itempart, itemdict = fromjson.item_outline(editedprojname, None, section_name, location)
    if itempart == 'Section':
        jsonstring = json.dumps(['Part',itemdict], indent=0, separators=(',', ':'))
    else:
        jsonstring = json.dumps([itempart,itemdict], indent=0, separators=(',', ':'))
    page_data['localStorage'] = {'ski_part':jsonstring}
    call_data['status'] = 'Item copied, and can now be pasted.'


def paste_section(skicall):
    "Gets submitted json string and inserts it"
    call_data = skicall.call_data
    page_data = skicall.page_data

    if ('editdom', 'domtable', 'contents') not in call_data:
        raise FailPage(message = "position to paste missing")
    if ('editdom', 'domtable', 'cols') not in call_data:
        raise FailPage(message = "item to paste missing")
    json_string = call_data['editdom', 'domtable', 'cols']

    editedprojname = call_data['editedprojname']
    part = call_data['editdom', 'domtable', 'contents']

    # so part is section name with location string of integers
    # though string of integers may be missing if this is the section part itself

    # create location which is a tuple or list consisting of three items:
    # a string of section name
    # a container integer, in this case always None
    # a tuple or list of location integers
    location_list = part.split('-')
    section_name = location_list[0]
    # first item should be a string, rest integers
    if len(location_list) == 1:
        # no location integers, so location_list[0] is the section name, location_integers is ()
        location_integers = ()
    else:
        location_integers = tuple( int(i) for i in location_list[1:] )
    # location is a tuple of section_name, None for no container, tuple of location integers
    location = (section_name, None, location_integers)
    call_data['schange'] = editsection.create_item_in_section(editedprojname, section_name, call_data['schange'], location, json_string)
    domcontents, dragrows, droprows = _section_domcontents(editedprojname, section_name)
    page_data['editdom', 'domtable', 'dragrows']  = dragrows
    page_data['editdom', 'domtable', 'droprows']  = droprows
    page_data['editdom', 'domtable', 'contents']  = domcontents


def cut_section_dom(skicall):
    "Called by domtable to cut an item in a section, and copy for later pasting"

    call_data = skicall.call_data
    page_data = skicall.page_data

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

    # prior to deleting, take a copy
    # get a json string dump of the item outline, however change any Sections to Parts
    itempart, itemdict = fromjson.item_outline(editedprojname, None, section_name, location)
    if itempart == 'Section':
        jsonstring = json.dumps(['Part',itemdict], indent=0, separators=(',', ':'))
    else:
        jsonstring = json.dumps([itempart,itemdict], indent=0, separators=(',', ':'))
    page_data['localStorage'] = {'ski_part':jsonstring}

    # remove the item
    try:
        call_data['schange'] = editsection.del_location(editedprojname, section_name, call_data['schange'], location)
    except ServerError as e:
        raise FailPage(message = e.message)

    # and re-draw the table
    domcontents, dragrows, droprows = _section_domcontents(editedprojname, section_name)
    page_data['editdom', 'domtable', 'dragrows']  = dragrows
    page_data['editdom', 'domtable', 'droprows']  = droprows
    page_data['editdom', 'domtable', 'contents']  = domcontents

    # once item is deleted, no info on the item should be
    # left in call_data - this may not be required in future
    if 'location' in call_data:
        del call_data['location']
    if 'part' in call_data:
        del call_data['part']
    if 'part_loc' in call_data:
        del call_data['part_loc']

    call_data['status'] = 'Item copied and then deleted. Use paste to recover or move it.'


def delete_section_dom(skicall):
    "Called by domtable to delete an item in a section"

    call_data = skicall.call_data
    page_data = skicall.page_data

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

    # remove the item
    try:
        call_data['schange'] = editsection.del_location(editedprojname, section_name, call_data['schange'], location)
    except ServerError as e:
        raise FailPage(message = e.message)

    # and re-draw the table
    domcontents, dragrows, droprows = _section_domcontents(editedprojname, section_name)
    page_data['editdom', 'domtable', 'dragrows']  = dragrows
    page_data['editdom', 'domtable', 'droprows']  = droprows
    page_data['editdom', 'domtable', 'contents']  = domcontents

    # once item is deleted, no info on the item should be
    # left in call_data - this may not be required in future
    if 'location' in call_data:
        del call_data['location']
    if 'part' in call_data:
        del call_data['part']
    if 'part_loc' in call_data:
        del call_data['part_loc']

    call_data['status'] = 'Item deleted.'



def move_up_in_section_dom(skicall):
    "Called by domtable to move an item in a section up"

    call_data = skicall.call_data
    page_data = skicall.page_data

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
        call_data['schange'] = editsection.move_location(editedprojname, section_name, call_data['schange'], location, (section_name, None, new_location_integers))
    except ServerError as e:
        raise FailPage(message = e.message)

    # and re-draw the table
    domcontents, dragrows, droprows = _section_domcontents(editedprojname, section_name)
    page_data['editdom', 'domtable', 'dragrows']  = dragrows
    page_data['editdom', 'domtable', 'droprows']  = droprows
    page_data['editdom', 'domtable', 'contents']  = domcontents


def move_up_right_in_section_dom(skicall):
    "Called by domtable to move an item in a section up and to the right"

    call_data = skicall.call_data
    page_data = skicall.page_data

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
        call_data['schange'] = editsection.move_location(editedprojname, section_name, call_data['schange'], location, (section_name, None, new_location_integers))
    except ServerError as e:
        raise FailPage(message = e.message)

    # and re-draw the table
    domcontents, dragrows, droprows = _section_domcontents(editedprojname, section_name)
    page_data['editdom', 'domtable', 'dragrows']  = dragrows
    page_data['editdom', 'domtable', 'droprows']  = droprows
    page_data['editdom', 'domtable', 'contents']  = domcontents


def move_down_in_section_dom(skicall):
    "Called by domtable to move an item in a section down"

    call_data = skicall.call_data
    page_data = skicall.page_data

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
        call_data['schange'] = editsection.move_location(editedprojname, section_name, call_data['schange'], location, (section_name, None, new_location_integers))
    except ServerError as e:
        raise FailPage(message = e.message)

    # and re-draw the table
    domcontents, dragrows, droprows = _section_domcontents(editedprojname, section_name)
    page_data['editdom', 'domtable', 'dragrows']  = dragrows
    page_data['editdom', 'domtable', 'droprows']  = droprows
    page_data['editdom', 'domtable', 'contents']  = domcontents


def move_down_right_in_section_dom(skicall):
    "Called by domtable to move an item in a section down and to the right"

    call_data = skicall.call_data
    page_data = skicall.page_data

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
        call_data['schange'] = editsection.move_location(editedprojname, section_name, call_data['schange'], location, (section_name, None, new_location_integers))
    except ServerError as e:
        raise FailPage(message = e.message)

    # and re-draw the table
    domcontents, dragrows, droprows = _section_domcontents(editedprojname, section_name)
    page_data['editdom', 'domtable', 'dragrows']  = dragrows
    page_data['editdom', 'domtable', 'droprows']  = droprows
    page_data['editdom', 'domtable', 'contents']  = domcontents



def move_in_section_dom(skicall):
    "Called by domtable to move an item in a section after a drag and drop"

    call_data = skicall.call_data
    page_data = skicall.page_data

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
        call_data['schange'] = editsection.move_location(editedprojname, section_name, call_data['schange'], location_to_move, (section_name, None, new_location_integers))
    except ServerError as e:
        raise FailPage(message = e.message)

    # and re-draw the table
    domcontents, dragrows, droprows = _section_domcontents(editedprojname, section_name)
    page_data['editdom', 'domtable', 'dragrows']  = dragrows
    page_data['editdom', 'domtable', 'droprows']  = droprows
    page_data['editdom', 'domtable', 'contents']  = domcontents


def _section_domcontents(project, section_name):
    "Return the info for domtable contents"
    section_location = (section_name, None, ())
    parttext,partdict = fromjson.item_outline(project, None, section_name, section_location)
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
                   ['Copy','width : 1%;text-align: center;', True, section_name],  # copy image for top line
                   ['Paste','width : 1%;text-align: center;', True, section_name],  # paste image for top line
                   ['', '', False, '' ],                                             # no cut image for top line
                   ['', '', False, '' ]                                              # no delete image for top line
                  ]
    # add further items to domcontents
    part_string_list = []

    if 'parts' not in partdict:
        rows = 1
    else:
        rows = _domtree(partdict, section_name, domcontents, part_string_list)
    # for every row in the table
    dragrows = [ [ False, '']]
    droprows = [ [ True, section_name ]]

    # for each row (minus 1 as the first row is done)
    if rows > 1:
        for row in range(0, rows-1):
            dragrows.append( [ True, part_string_list[row]] )
            droprows.append( [ True, part_string_list[row]] )
    
    return domcontents, dragrows, droprows



def _domtree(partdict, part_loc, contents, part_string_list, rows=1, indent=1):
    "Creates the contents of the domtable"

    # note: if in a container
    # part_loc = widget_name + '-' + container_number
    # otherwise part_loc = body, head, svg, section_name


    indent += 1
    padding = "padding-left : %sem;" % (indent,)
    u_r_flag = False
    last_row_at_this_level = 0

    parts = partdict['parts']

    # parts is a list of items
    last_index = len(parts)-1

    #Text   #characters..      #up  #up_right  #down  #down_right   #edit   #insert  #copy  #paste  #cut #delete

    for index, part in enumerate(parts):
        part_location_string = part_loc + '-' + str(index)
        part_string_list.append(part_location_string)
        rows += 1
        part_type, part_dict = part
        # the row text
        if part_type == 'Widget' or part_type == 'ClosedWidget':
            part_name = 'Widget ' + part_dict['name']
            if len(part_name)>40:
                part_name = part_name[:35] + '...'
            contents.append([part_name, padding, False, ''])
            part_brief = html.escape(part_dict.get('brief',''))
            if len(part_brief)>40:
                part_brief = part_brief[:35] + '...'
            if not part_brief:
                part_brief = '-'
            contents.append([part_brief, '', False, ''])
        elif part_type == 'TextBlock':
            contents.append(['TextBlock', padding, False, ''])
            part_ref = part_dict['textref']
            if len(part_ref)>40:
                part_ref = part_ref[:35] + '...'
            if not part_ref:
                part_ref = '-'
            contents.append([part_ref, '', False, ''])
        elif part_type == 'SectionPlaceHolder':
            section_name = part_dict['placename']
            if section_name:
                section_name = "Section " + section_name
            else:
                section_name = "Section -None-"
            if len(section_name)>40:
                section_name = section_name[:35] + '...'
            contents.append([section_name, padding, False, ''])
            part_brief = html.escape(part_dict.get('brief',''))
            if len(part_brief)>40:
                part_brief = part_brief[:35] + '...'
            if not part_brief:
                part_brief = '-'
            contents.append([part_brief, '', False, ''])
        elif part_type == 'Text':
            contents.append(['Text', padding, False, ''])
            # in this case part_dict is the text string rather than a dictionary
            if len(part_dict)<40:
                part_str = html.escape(part_dict)
            else:
                part_str = html.escape(part_dict[:35] + '...')
            if not part_str:
                part_str = '-'
            contents.append([part_str, '', False, ''])
        elif part_type == 'HTMLSymbol':
            contents.append(['Symbol', padding, False, ''])
            part_text = part_dict['text']
            if len(part_text)<40:
                part_str = html.escape(part_text)
            else:
                part_str = html.escape(part_text[:35] + '...')
            if not part_str:
                part_str = '-'
            contents.append([part_str, '', False, ''])
        elif part_type == 'Comment':
            contents.append(['Comment', padding, False, ''])
            part_text = part_dict['text']
            if len(part_text)<33:
                part_str =  "&lt;!--" + part_text + '--&gt;'
            else:
                part_str = "&lt;!--" + part_text[:31] + '...'
            if not part_str:
                part_str = '&lt;!----&gt;'
            contents.append([part_str, '', False, ''])
        elif part_type == 'ClosedPart':
            if 'attribs' in part_dict:
                tag_name = "&lt;%s ... /&gt;" % part_dict['tag_name']
            else:
                tag_name = "&lt;%s /&gt;" % part_dict['tag_name']
            contents.append([tag_name, padding, False, ''])
            part_brief = html.escape(part_dict.get('brief',''))
            if len(part_brief)>40:
                part_brief = part_brief[:35] + '...'
            if not part_brief:
                part_brief = '-'
            contents.append([part_brief, '', False, ''])
        elif part_type == 'Part':
            if 'attribs' in part_dict:
                tag_name = "&lt;%s ... &gt;" % part_dict['tag_name']
            else:
                tag_name = "&lt;%s&gt;" % part_dict['tag_name']
            contents.append([tag_name, padding, False, ''])
            part_brief = html.escape(part_dict.get('brief',''))
            if len(part_brief)>40:
                part_brief = part_brief[:35] + '...'
            if not part_brief:
                part_brief = '-'
            contents.append([part_brief, '', False, ''])
        else:
            contents.append(['UNKNOWN', padding, False, ''])
            contents.append(['ERROR', '', False, ''])

        # UP ARROW
        if rows == 2:
            # second line in table cannot move upwards
            contents.append(['', '', False, '' ])
        else:
            contents.append(['&uarr;', 'width : 1%;', True, part_location_string])

        # UP RIGHT ARROW
        if u_r_flag:
            contents.append(['&nearr;', 'width : 1%;', True, part_location_string])
        else:
            contents.append(['', '', False, '' ])

        # DOWN ARROW
        if (indent == 2) and (index == last_index):
            # the last line at this top indent has been added, no down arrow
            contents.append(['', '', False, '' ])
        else:
            contents.append(['&darr;', 'width : 1%;', True, part_location_string])

        # DOWN RIGHT ARROW
        # set to empty, when next line is created if down-right not applicable
        contents.append(['', '', False, '' ])

        # EDIT
        contents.append(['Edit', 'width : 1%;', True, part_location_string])

        # INSERT or APPEND
        if part_type == 'Part':
            contents.append(['Insert', 'width : 1%;text-align: center;', True, part_location_string])
        else:
            contents.append(['Append', 'width : 1%;text-align: center;', True, part_location_string])

        # COPY
        contents.append(['Copy', 'width : 1%;', True, part_location_string])

        # PASTE
        contents.append(['Paste', 'width : 1%;', True, part_location_string])

        # CUT
        contents.append(['Cut', 'width : 1%;', True, part_location_string])

        # DELETE
        contents.append(['Delete', 'width : 1%;', True, part_location_string])

        u_r_flag = False
        if part_type == 'Part':
            if last_row_at_this_level and (part_dict['tag_name'] != 'script') and (part_dict['tag_name'] != 'pre'):
                # add down right arrow in previous row at this level, get loc_string from adjacent edit cell
                editcell = contents[last_row_at_this_level *12-6]
                loc_string = editcell[3]
                contents[last_row_at_this_level *12-7] = ['&searr;', 'width : 1%;', True, loc_string]
            last_row_at_this_level = rows
            rows = _domtree(part_dict, part_location_string, contents, part_string_list, rows, indent)
            # set u_r_flag for next item below this one
            if  (part_dict['tag_name'] != 'script') and (part_dict['tag_name'] != 'pre'):
                u_r_flag = True
        else:
            last_row_at_this_level =rows

    return rows



