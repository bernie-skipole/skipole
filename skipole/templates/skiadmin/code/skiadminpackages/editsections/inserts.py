

from skipole import FailPage, ValidateError, GoTo, ServerError, skilift

from skipole.skilift import editsection


def insert_in_section(skicall):
    """Called by domtable to either insert or append an item in a section
       sets page_data to populate the insert or append modal panel"""
    call_data = skicall.call_data
    page_data = skicall.page_data
    if ('editdom', 'domtable', 'contents') not in call_data:
        raise FailPage(message = "item to edit missing")
    editedprojname = call_data['editedprojname']
    part = call_data['editdom', 'domtable', 'contents']
    location_list = part.split('-')
    # first item should be a string, rest integers
    try:
        if len(location_list) == 1:
            # no location integers, so location_list[0] is the section name
            location_integers = ()
        else:
            location_integers = tuple( int(i) for i in location_list[1:] )
        section_name = location_list[0]
    except:
        raise FailPage("Item to append to has not been recognised")

    # location is a tuple of section_name, None for no container, tuple of location integers
    location = (section_name, None, location_integers)
    # get part_tuple from project, pagenumber, section_name, location
    part_tuple = skilift.part_info(editedprojname, None, section_name, location)
    if part_tuple is None:
        raise FailPage("Item to append to has not been recognised")

    if location_integers:
        insert_location = section_name + '-' + '-'.join(str(i) for i in location_integers)
    else:
        insert_location = section_name

    # display the modal panel
    page_data[("sectioninserts","insertitem","hide")] = False

    if (part_tuple.part_type == "Part") or (part_tuple.part_type == "Section"):
        # insert
        page_data[("sectioninserts","insertpara","para_text")] = "Choose an item to insert"
        page_data[("sectioninserts","insertupload","para_text")] = "Or insert a new block by uploading a block definition file:"
    else:
        # append
        page_data[("sectioninserts","insertpara","para_text")] = "Choose an item to append"
        page_data[("sectioninserts","insertupload","para_text")] = "Or append a new block by uploading a block definition file:"

    # for each of the links, set get_field1 to be the insert_location
    page_data[("sectioninserts","insert_text","get_field1")] = insert_location
    page_data[("sectioninserts","insert_textblock","get_field1")] = insert_location
    page_data[("sectioninserts","insert_symbol","get_field1")] = insert_location
    page_data[("sectioninserts","insert_comment","get_field1")] = insert_location
    page_data[("sectioninserts","insert_element","get_field1")] = insert_location
    page_data[("sectioninserts","insert_widget","get_field1")] = insert_location

    # set the hidden field
    page_data[("sectioninserts","uploadpart","hidden_field1")] = insert_location



def insert_text(skicall):
    "Inserts text into a section"
    call_data = skicall.call_data
    page_data = skicall.page_data

    if ("sectioninserts","insert_text","get_field1") not in call_data:
        raise FailPage(message = "item to edit missing")
    editedprojname = call_data['editedprojname']
    part = call_data["sectioninserts","insert_text","get_field1"]
    location_list = part.split('-')
    # first item should be a string, rest integers
    try:
        if len(location_list) == 1:
            # no location integers, so location_list[0] is the section name
            location_integers = ()
        else:
            location_integers = tuple( int(i) for i in location_list[1:] )
        section_name = location_list[0]
    except:
        raise FailPage("Item to append to has not been recognised")

    # location is a tuple of section_name, None for no container, tuple of location integers
    location = (section_name, None, location_integers)
    # get part_tuple from project, pagenumber, section_name, location
    part_tuple = skilift.part_info(editedprojname, None, section_name, location)
    if part_tuple is None:
        raise FailPage("Item to append to has not been recognised")

    call_data['section_name'] = section_name

    new_text = 'Set text here'

    call_data['schange'], new_location = skilift.insert_item_in_section(editedprojname, section_name, call_data['schange'], location, new_text)
    call_data['location'] = new_location
    
    # go to edit text page
    page_data[("adminhead","page_head","large_text")] = "Edit Text in section : %s" % (section_name,)
    # Set the text in the text area
    page_data[("text_input","input_text")] = new_text


def insert_textblock(skicall):
    "Fills the template page for creating a textblock reference which will be inserted in the section"
    call_data = skicall.call_data
    page_data = skicall.page_data

    if ("sectioninserts","insert_textblock","get_field1") not in call_data:
        raise FailPage(message = "item to edit missing")
    editedprojname = call_data['editedprojname']
    part = call_data["sectioninserts","insert_textblock","get_field1"]
    location_list = part.split('-')
    # first item should be a string, rest integers
    try:
        if len(location_list) == 1:
            # no location integers, so location_list[0] is the section name
            location_integers = ()
        else:
            location_integers = tuple( int(i) for i in location_list[1:] )
        section_name = location_list[0]
    except:
        raise FailPage("Item to append to has not been recognised")

    # location is a tuple of section_name, None for no container, tuple of location integers
    location = (section_name, None, location_integers)
    # get part_tuple from project, pagenumber, section_name, location
    part_tuple = skilift.part_info(editedprojname, None, section_name, location)
    if part_tuple is None:
        raise FailPage("Item to append to has not been recognised")

    # section_name and location are set into call_data, so they will also be set into the ident data
    call_data['section_name'] = section_name
    call_data['location'] = location

    # and set page data for the template page which inserts an textblock reference

    page_data[("adminhead","page_head","large_text")] = "Insert TextBlock in section %s" % (section_name,)

    page_data[("linebreaks","radio_values")]=['ON', 'OFF']
    page_data[("linebreaks","radio_text")]=['On', 'Off']
    page_data[("linebreaks","radio_checked")] = 'ON'

    page_data[("setescape","radio_values")]=['ON', 'OFF']
    page_data[("setescape","radio_text")]=['On', 'Off']
    page_data[("setescape","radio_checked")] = 'ON'



def insert_symbol(skicall):
    "Inserts html symbol into a section"
    call_data = skicall.call_data
    page_data = skicall.page_data

    if ("sectioninserts","insert_symbol","get_field1") not in call_data:
        raise FailPage(message = "item to edit missing")
    editedprojname = call_data['editedprojname']
    part = call_data["sectioninserts","insert_symbol","get_field1"]
    location_list = part.split('-')
    # first item should be a string, rest integers
    try:
        if len(location_list) == 1:
            # no location integers, so location_list[0] is the section name
            location_integers = ()
        else:
            location_integers = tuple( int(i) for i in location_list[1:] )
        section_name = location_list[0]
    except:
        raise FailPage("Item to append to has not been recognised")

    # location is a tuple of section_name, None for no container, tuple of location integers
    location = (section_name, None, location_integers)
    # get part_tuple from project, pagenumber, section_name, location
    part_tuple = skilift.part_info(editedprojname, None, section_name, location)
    if part_tuple is None:
        raise FailPage("Item to append to has not been recognised")

    call_data['section_name'] = section_name
    call_data['schange'], new_location = editsection.create_html_symbol_in_section(editedprojname, section_name, call_data['schange'], location)
    call_data['location'] = new_location
    
    # go to edit symbol page
    sym = editsection.get_symbol(editedprojname, section_name, call_data['schange'], new_location)
    page_data[("adminhead","page_head","large_text")] = "Edit Symbol in section : %s" % (section_name,)
    page_data["symbol_input","input_text"] = sym


def insert_comment(skicall):
    "Inserts a comment into a section"
    call_data = skicall.call_data
    page_data = skicall.page_data

    if ("sectioninserts","insert_comment","get_field1") not in call_data:
        raise FailPage(message = "item to edit missing")
    editedprojname = call_data['editedprojname']
    part = call_data["sectioninserts","insert_comment","get_field1"]
    location_list = part.split('-')
    # first item should be a string, rest integers
    try:
        if len(location_list) == 1:
            # no location integers, so location_list[0] is the section name
            location_integers = ()
        else:
            location_integers = tuple( int(i) for i in location_list[1:] )
        section_name = location_list[0]
    except:
        raise FailPage("Item to append to has not been recognised")

    # location is a tuple of section_name, None for no container, tuple of location integers
    location = (section_name, None, location_integers)
    # get part_tuple from project, pagenumber, section_name, location
    part_tuple = skilift.part_info(editedprojname, None, section_name, location)
    if part_tuple is None:
        raise FailPage("Item to append to has not been recognised")

    call_data['section_name'] = section_name
    call_data['schange'], new_location = editsection.create_html_comment_in_section(editedprojname, section_name, call_data['schange'], location)
    call_data['location'] = new_location
    
    # go to edit comment page
    com = editsection.get_comment(editedprojname, section_name, call_data['schange'], new_location)
    page_data[("adminhead","page_head","large_text")] = "Edit Comment in section : %s" % (section_name,)
    page_data[("comment_input","input_text")] = com


def insert_element(skicall):
    "Fills the template page for creating an html element which will be inserted in the section"
    call_data = skicall.call_data
    page_data = skicall.page_data

    if ("sectioninserts","insert_element","get_field1") not in call_data:
        raise FailPage(message = "item to edit missing")
    editedprojname = call_data['editedprojname']
    part = call_data["sectioninserts","insert_element","get_field1"]
    location_list = part.split('-')
    # first item should be a string, rest integers
    try:
        if len(location_list) == 1:
            # no location integers, so location_list[0] is the section name
            location_integers = ()
        else:
            location_integers = tuple( int(i) for i in location_list[1:] )
        section_name = location_list[0]
    except:
        raise FailPage("Item to append to has not been recognised")

    # location is a tuple of section_name, None for no container, tuple of location integers
    location = (section_name, None, location_integers)
    # get part_tuple from project, pagenumber, section_name, location
    part_tuple = skilift.part_info(editedprojname, None, section_name, location)
    if part_tuple is None:
        raise FailPage("Item to append to has not been recognised")

    # section_name and location are set into call_data, so they will also be set into the ident data
    call_data['section_name'] = section_name
    call_data['location'] = location

    # and set page data for the template page which inserts an element
    page_data[("adminhead","page_head","large_text")] = "Insert an HTML element into section " + call_data['section_name']


def insert_widget(skicall):
    "Gets section_name and location, used for creating a widget which will be inserted in the section"
    call_data = skicall.call_data
    page_data = skicall.page_data

    if ("sectioninserts","insert_widget","get_field1") not in call_data:
        raise FailPage(message = "item to edit missing")
    editedprojname = call_data['editedprojname']
    part = call_data["sectioninserts","insert_widget","get_field1"]
    location_list = part.split('-')
    # first item should be a string, rest integers
    try:
        if len(location_list) == 1:
            # no location integers, so location_list[0] is the section name
            location_integers = ()
        else:
            location_integers = tuple( int(i) for i in location_list[1:] )
        section_name = location_list[0]
    except:
        raise FailPage("Item to append to has not been recognised")

    # location is a tuple of section_name, None for no container, tuple of location integers
    location = (section_name, None, location_integers)
    # get part_tuple from project, pagenumber, section_name, location
    part_tuple = skilift.part_info(editedprojname, None, section_name, location)
    if part_tuple is None:
        raise FailPage("Item to append to has not been recognised")

    # section_name and location are set into call_data, so they will also be set into the ident data
    call_data['section_name'] = section_name
    call_data['location'] = location

    # at this point, the call is passed to 54507 which is a responder which lists widget modules
    # and displays them on a template


def insert_upload(skicall):
    "Gets section_name and location, used for creating a widget which will be inserted in the section"
    call_data = skicall.call_data
    page_data = skicall.page_data

    if ("sectioninserts","uploadpart","hidden_field1") not in call_data:
        raise FailPage(message = "item to edit missing")
    editedprojname = call_data['editedprojname']
    part = call_data["sectioninserts","uploadpart","hidden_field1"]
    location_list = part.split('-')
    # first item should be a string, rest integers
    try:
        if len(location_list) == 1:
            # no location integers, so location_list[0] is the section name
            location_integers = ()
        else:
            location_integers = tuple( int(i) for i in location_list[1:] )
        section_name = location_list[0]
    except:
        raise FailPage("Item to append to has not been recognised")

    # location is a tuple of section_name, None for no container, tuple of location integers
    location = (section_name, None, location_integers)
    # get part_tuple from project, pagenumber, section_name, location
    part_tuple = skilift.part_info(editedprojname, None, section_name, location)
    if part_tuple is None:
        raise FailPage("Item to append to has not been recognised")

    # section_name and location are set into call_data, so they will also be set into the ident data
    call_data['section_name'] = section_name

    # get file contents
    file_contents = call_data["sectioninserts","uploadpart", "action"]
    json_string = file_contents.decode(encoding='utf-8')

    call_data['schange'] = editsection.create_part_in_section(editedprojname, section_name, call_data['schange'], location, json_string)

    call_data['status'] = 'New block created'


