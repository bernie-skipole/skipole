

from ... import FailPage, ValidateError, GoTo, ServerError, skilift

from ....skilift import editpage, editsection


def show_empty_modal_insert(skicall):
    "Fills in empty modal insert"
    call_data = skicall.call_data
    page_data = skicall.page_data
    page_data["widgetinserts", "insertitem", "hide"] = False
    location = call_data['location']
    widget_name = location[0]
    container = location[1]
    # This should be for an empty container
    if location[2]:
        raise FailPage("Invalid location")

    insert_location = widget_name + "-" + str(container)

    # for each of the links, set get_field1 to be the insert_location
    page_data[("widgetinserts","insert_text","get_field1")] = insert_location
    page_data[("widgetinserts","insert_textblock","get_field1")] = insert_location
    page_data[("widgetinserts","insert_symbol","get_field1")] = insert_location
    page_data[("widgetinserts","insert_comment","get_field1")] = insert_location
    page_data[("widgetinserts","insert_element","get_field1")] = insert_location
    page_data[("widgetinserts","insert_widget","get_field1")] = insert_location
    page_data[("widgetinserts","insert_section","get_field1")] = insert_location

    # set the hidden field
    page_data[("widgetinserts","uploadpart","hidden_field1")] = insert_location



def insert_in_widget(skicall):
    """Called by domtable to either insert or append an item in a widget container
       sets page_data to populate the insert or append modal panel"""
    call_data = skicall.call_data
    page_data = skicall.page_data

    pagenumber = None
    section_name = None

    if "page_number" in call_data:
        pagenumber = call_data["page_number"]
    elif "section_name" in call_data:
        section_name = call_data["section_name"]
    else:
        raise FailPage(message = "No page or section given")

    if ('editdom', 'domtable', 'contents') not in call_data:
        raise FailPage(message = "item to edit missing")
    editedprojname = call_data['editedprojname']
    part = call_data['editdom', 'domtable', 'contents']

    # so part is location_string with string of integers
    # where first string is the widget name,
    # and first digit is the container number
    # create location which is a tuple or list consisting of three items:
    # widget name
    # a container integer
    # a tuple or list of location integers
    location_list = part.split('-')
    # first item should be a string, rest integers
    # first item should be a string, rest integers
    if len(location_list) < 3:
        raise FailPage("Item to append to has not been recognised")
    try:
        widget_name = location_list[0]
        container = int(location_list[1])
        location_integers = tuple( int(i) for i in location_list[2:] )
    except:
        raise FailPage("Item to append to has not been recognised")

    location = (widget_name, container, location_integers)
    # get part_tuple from project, pagenumber, section_name, location
    part_tuple = skilift.part_info(editedprojname, pagenumber, section_name, location)
    if part_tuple is None:
        raise FailPage("Item to append to has not been recognised")

    insert_location = widget_name + '-' + str(container) + '-' + '-'.join(str(i) for i in location_integers)

    # display the modal panel
    page_data[("widgetinserts","insertitem","hide")] = False

    if (part_tuple.part_type == "Part") or (part_tuple.part_type == "Section"):
        # insert
        page_data[("widgetinserts","insertpara","para_text")] = "Choose an item to insert"
        page_data[("widgetinserts","insertupload","para_text")] = "Or insert a new block by uploading a block definition file:"
    else:
        # append
        page_data[("widgetinserts","insertpara","para_text")] = "Choose an item to append"
        page_data[("widgetinserts","insertupload","para_text")] = "Or append a new block by uploading a block definition file:"

    # for each of the links, set get_field1 to be the insert_location
    page_data[("widgetinserts","insert_text","get_field1")] = insert_location
    page_data[("widgetinserts","insert_textblock","get_field1")] = insert_location
    page_data[("widgetinserts","insert_symbol","get_field1")] = insert_location
    page_data[("widgetinserts","insert_comment","get_field1")] = insert_location
    page_data[("widgetinserts","insert_element","get_field1")] = insert_location
    page_data[("widgetinserts","insert_widget","get_field1")] = insert_location
    if pagenumber:
        page_data[("widgetinserts","insert_section","get_field1")] = insert_location

    # set the hidden field
    page_data[("widgetinserts","uploadpart","hidden_field1")] = insert_location


def insert_text(skicall):
    "Inserts text into a page"
    call_data = skicall.call_data
    page_data = skicall.page_data

    pagenumber = None
    section_name = None
    editedprojname = call_data['editedprojname']

    if "page_number" in call_data:
        pagenumber = call_data["page_number"]
        page_info = skilift.item_info(editedprojname, pagenumber)
        if page_info is None:
            raise FailPage("Page to edit not identified")
        if (page_info.item_type != "TemplatePage") and (page_info.item_type != "SVG"):
            raise FailPage("Page not identified")
    elif "section_name" in call_data:
        section_name = call_data["section_name"]
    else:
        raise FailPage(message = "No page or section given")

    if ("widgetinserts","insert_text","get_field1") not in call_data:
        raise FailPage(message = "item to edit missing")

    part = call_data["widgetinserts","insert_text","get_field1"]
    location_list = part.split('-')
    # first item should be a string, rest integers
    try:
        widget_name = location_list[0]
        container = int(location_list[1])
        if len(location_list) < 3:
            location_integers = ()
        else:
            location_integers = tuple( int(i) for i in location_list[2:] )
    except:
        raise FailPage("Item to append to has not been recognised")

    location = (widget_name, container, location_integers)
    # get part_tuple from project, pagenumber, section_name, location
    part_tuple = skilift.part_info(editedprojname, pagenumber, section_name, location)
    if part_tuple is None:
        raise FailPage("Item to append to has not been recognised")

    new_text = 'Set text here'
    if pagenumber:
        call_data['pchange'], new_location = skilift.insert_item_in_page(editedprojname, pagenumber, call_data['pchange'], location, new_text)
        page_data[("adminhead","page_head","large_text")] = "Edit Text in Page: %s Widget: %s" % (pagenumber,widget_name)
    else:
        call_data['schange'], new_location = skilift.insert_item_in_section(editedprojname, section_name, call_data['schange'], location, new_text)
        page_data[("adminhead","page_head","large_text")] = "Edit Text in Section : %s Widget %s" % (section_name,widget_name)
    call_data['location'] = new_location
    
    # go to edit text page, set the text in the text area
    page_data[("text_input","input_text")] = new_text


def insert_textblock(skicall):
    "Fills the template page for creating a textblock reference which will be inserted in the edited page"
    call_data = skicall.call_data
    page_data = skicall.page_data

    pagenumber = None
    section_name = None
    editedprojname = call_data['editedprojname']

    if "page_number" in call_data:
        pagenumber = call_data["page_number"]
        page_info = skilift.item_info(editedprojname, pagenumber)
        if page_info is None:
            raise FailPage("Page to edit not identified")
        if (page_info.item_type != "TemplatePage") and (page_info.item_type != "SVG"):
            raise FailPage("Page not identified")
    elif "section_name" in call_data:
        section_name = call_data["section_name"]
    else:
        raise FailPage(message = "No page or section given")

    if ("widgetinserts","insert_textblock","get_field1") not in call_data:
        raise FailPage(message = "item to edit missing")

    part = call_data["widgetinserts","insert_textblock","get_field1"]
    location_list = part.split('-')
    # first item should be a string, rest integers
    try:
        widget_name = location_list[0]
        container = int(location_list[1])
        if len(location_list) < 3:
            location_integers = ()
        else:
            location_integers = tuple( int(i) for i in location_list[2:] )
    except:
        raise FailPage("Item to append to has not been recognised")

    location = (widget_name, container, location_integers)
    # get part_tuple from project, pagenumber, section_name, location
    part_tuple = skilift.part_info(editedprojname, pagenumber, section_name, location)
    if part_tuple is None:
        raise FailPage("Item to append to has not been recognised")
    call_data['location'] = location

    # and set page data for the template page which inserts an textblock reference
    if pagenumber:
        page_data[("adminhead","page_head","large_text")] = "Insert TextBlock in Page: %s Widget: %s" % (pagenumber, widget_name)
    else:
        page_data[("adminhead","page_head","large_text")] = "Insert TextBlock in Section: %s Widget: %s" % (section_name, widget_name)

    page_data[("linebreaks","radio_values")]=['ON', 'OFF']
    page_data[("linebreaks","radio_text")]=['On', 'Off']
    page_data[("linebreaks","radio_checked")] = 'ON'

    page_data[("setescape","radio_values")]=['ON', 'OFF']
    page_data[("setescape","radio_text")]=['On', 'Off']
    page_data[("setescape","radio_checked")] = 'ON'


def insert_symbol(skicall):
    "Inserts html symbol into a page"
    call_data = skicall.call_data
    page_data = skicall.page_data

    pagenumber = None
    section_name = None
    editedprojname = call_data['editedprojname']

    if "page_number" in call_data:
        pagenumber = call_data["page_number"]
        page_info = skilift.item_info(editedprojname, pagenumber)
        if page_info is None:
            raise FailPage("Page to edit not identified")
        if (page_info.item_type != "TemplatePage") and (page_info.item_type != "SVG"):
            raise FailPage("Page not identified")
    elif "section_name" in call_data:
        section_name = call_data["section_name"]
    else:
        raise FailPage(message = "No page or section given")

    if ("widgetinserts","insert_symbol","get_field1") not in call_data:
        raise FailPage(message = "item to edit missing")

    part = call_data["widgetinserts","insert_symbol","get_field1"]
    location_list = part.split('-')
    # first item should be a string, rest integers
    try:
        widget_name = location_list[0]
        container = int(location_list[1])
        if len(location_list) < 3:
            location_integers = ()
        else:
            location_integers = tuple( int(i) for i in location_list[2:] )
    except:
        raise FailPage("Item to append to has not been recognised")

    location = (widget_name, container, location_integers)
    # get part_tuple from project, pagenumber, section_name, location
    part_tuple = skilift.part_info(editedprojname, pagenumber, section_name, location)
    if part_tuple is None:
        raise FailPage("Item to append to has not been recognised")

    # then passed to edit symbol page

    if pagenumber:
        call_data['pchange'], new_location = editpage.create_html_symbol_in_page(editedprojname, pagenumber, call_data['pchange'], location)
        sym = editpage.get_symbol(editedprojname, pagenumber, call_data['pchange'], new_location)
        page_data[("adminhead","page_head","large_text")] = "Edit Symbol in Page: %s Widget: %s" % (pagenumber, widget_name)
    else:
        call_data['schange'], new_location = editsection.create_html_symbol_in_section(editedprojname, section_name, call_data['schange'], location)
        sym = editsection.get_symbol(editedprojname, section_name, call_data['schange'], new_location)
        page_data[("adminhead","page_head","large_text")] = "Edit Symbol in Section: %s Widget: %s" % (section_name, widget_name)

    call_data['location'] = new_location
    page_data["symbol_input","input_text"] = sym


def insert_comment(skicall):
    "Inserts a comment into a page"
    call_data = skicall.call_data
    page_data = skicall.page_data

    pagenumber = None
    section_name = None
    editedprojname = call_data['editedprojname']

    if "page_number" in call_data:
        pagenumber = call_data["page_number"]
        page_info = skilift.item_info(editedprojname, pagenumber)
        if page_info is None:
            raise FailPage("Page to edit not identified")
        if (page_info.item_type != "TemplatePage") and (page_info.item_type != "SVG"):
            raise FailPage("Page not identified")
    elif "section_name" in call_data:
        section_name = call_data["section_name"]
    else:
        raise FailPage(message = "No page or section given")

    if ("widgetinserts","insert_comment","get_field1") not in call_data:
        raise FailPage(message = "item to edit missing")


    part = call_data["widgetinserts","insert_comment","get_field1"]
    location_list = part.split('-')
    # first item should be a string, rest integers
    try:
        widget_name = location_list[0]
        container = int(location_list[1])
        if len(location_list) < 3:
            location_integers = ()
        else:
            location_integers = tuple( int(i) for i in location_list[2:] )
    except:
        raise FailPage("Item to append to has not been recognised")

    location = (widget_name, container, location_integers)
    # get part_tuple from project, pagenumber, section_name, location
    part_tuple = skilift.part_info(editedprojname, pagenumber, section_name, location)
    if part_tuple is None:
        raise FailPage("Item to append to has not been recognised")

    # then passed to edit symbol page

    if pagenumber:
        call_data['pchange'], new_location = editpage.create_html_comment_in_page(editedprojname, pagenumber, call_data['pchange'], location)
        com = editpage.get_comment(editedprojname, pagenumber, call_data['pchange'], new_location)
        page_data[("adminhead","page_head","large_text")] = "Edit Comment in Page: %s Widget: %s" % (pagenumber, widget_name)
    else:
        call_data['schange'], new_location = editsection.create_html_comment_in_section(editedprojname, section_name, call_data['schange'], location)
        com = editsection.get_comment(editedprojname, section_name, call_data['schange'], new_location)
        page_data[("adminhead","page_head","large_text")] = "Edit Comment in Section: %s Widget: %s" % (section_name, widget_name)

    call_data['location'] = new_location
    page_data[("comment_input","input_text")] = com


def insert_element(skicall):
    "Fills the template page for creating an html element which will be inserted in the edited page"
    call_data = skicall.call_data
    page_data = skicall.page_data

    pagenumber = None
    section_name = None
    editedprojname = call_data['editedprojname']

    if "page_number" in call_data:
        pagenumber = call_data["page_number"]
        page_info = skilift.item_info(editedprojname, pagenumber)
        if page_info is None:
            raise FailPage("Page to edit not identified")
        if (page_info.item_type != "TemplatePage") and (page_info.item_type != "SVG"):
            raise FailPage("Page not identified")
    elif "section_name" in call_data:
        section_name = call_data["section_name"]
    else:
        raise FailPage(message = "No page or section given")

    if ("widgetinserts","insert_element","get_field1") not in call_data:
        raise FailPage(message = "item to edit missing")

    part = call_data["widgetinserts","insert_element","get_field1"]
    location_list = part.split('-')
    # first item should be a string, rest integers
    try:
        widget_name = location_list[0]
        container = int(location_list[1])
        if len(location_list) < 3:
            location_integers = ()
        else:
            location_integers = tuple( int(i) for i in location_list[2:] )
    except:
        raise FailPage("Item to append to has not been recognised")

    location = (widget_name, container, location_integers)
    # get part_tuple from project, pagenumber, section_name, location
    part_tuple = skilift.part_info(editedprojname, pagenumber, section_name, location)
    if part_tuple is None:
        raise FailPage("Item to append to has not been recognised")
    call_data['location'] = location

    # and set page data for the template page which inserts an HTML element
    if pagenumber:
        page_data[("adminhead","page_head","large_text")] = "Insert  an HTML element into Page: %s Widget: %s" % (pagenumber, widget_name)
    else:
        page_data[("adminhead","page_head","large_text")] = "Insert  an HTML element into Section: %s Widget: %s" % (section_name, widget_name)


def insert_widget(skicall):
    "Gets page number and location, used for creating a widget which will be inserted in the page"
    call_data = skicall.call_data
    page_data = skicall.page_data

    pagenumber = None
    section_name = None
    editedprojname = call_data['editedprojname']

    if "page_number" in call_data:
        pagenumber = call_data["page_number"]
        page_info = skilift.item_info(editedprojname, pagenumber)
        if page_info is None:
            raise FailPage("Page to edit not identified")
        if (page_info.item_type != "TemplatePage") and (page_info.item_type != "SVG"):
            raise FailPage("Page not identified")
    elif "section_name" in call_data:
        section_name = call_data["section_name"]
    else:
        raise FailPage(message = "No page or section given")

    if ("widgetinserts","insert_widget","get_field1") not in call_data:
        raise FailPage(message = "item to edit missing")


    part = call_data["widgetinserts","insert_widget","get_field1"]
    location_list = part.split('-')
    # first item should be a string, rest integers
    try:
        widget_name = location_list[0]
        container = int(location_list[1])
        if len(location_list) < 3:
            location_integers = ()
        else:
            location_integers = tuple( int(i) for i in location_list[2:] )
    except:
        raise FailPage("Item to append to has not been recognised")

    location = (widget_name, container, location_integers)
    # get part_tuple from project, pagenumber, section_name, location
    part_tuple = skilift.part_info(editedprojname, pagenumber, section_name, location)
    if part_tuple is None:
        raise FailPage("Item to append to has not been recognised")
    call_data['location'] = location

    # at this point, the call is passed to 54507 which is a responder which lists widget modules
    # and displays them on a template


def insert_section(skicall):
    "Gets page number and location, used for creating a section reference which will be inserted in the page"
    call_data = skicall.call_data
    page_data = skicall.page_data

    pagenumber = None
    section_name = None
    editedprojname = call_data['editedprojname']

    if "page_number" in call_data:
        pagenumber = call_data["page_number"]
    else:
        raise FailPage(message = "No page given")

    if ("widgetinserts","insert_section","get_field1") not in call_data:
        raise FailPage(message = "item to edit missing")

    page_info = skilift.item_info(editedprojname, pagenumber)
    if page_info is None:
        raise FailPage("Page to edit not identified")
    if (page_info.item_type != "TemplatePage") and (page_info.item_type != "SVG"):
        raise FailPage("Page not identified")

    part = call_data["widgetinserts","insert_section","get_field1"]
    location_list = part.split('-')
    # first item should be a string, rest integers
    try:
        widget_name = location_list[0]
        container = int(location_list[1])
        if len(location_list) < 3:
            location_integers = ()
        else:
            location_integers = tuple( int(i) for i in location_list[2:] )
    except:
        raise FailPage("Item to append to has not been recognised")

    location = (widget_name, container, location_integers)
    # get part_tuple from project, pagenumber, section_name, location
    part_tuple = skilift.part_info(editedprojname, pagenumber, None, location)
    if part_tuple is None:
        raise FailPage("Item to append to has not been recognised")
    call_data['location'] = location

    # Fill in header
    page_data[("adminhead","page_head","large_text")] = "Insert Section place holder"

    # get current sections
    section_list = editsection.list_section_names(editedprojname)
    if not section_list:
        page_data[("nosection", "show")] = True
        page_data[("descript", "show")] = False
        page_data[("placename","show")] = False
        return

    page_data[('sectionname','option_list')] = section_list[:]
    page_data[('sectionname','selectvalue')] = section_list[0]



def insert_upload(skicall):
    "Gets page number and location, used for creating a widget which will be inserted in the page"
    call_data = skicall.call_data
    page_data = skicall.page_data

    pagenumber = None
    section_name = None
    editedprojname = call_data['editedprojname']

    if "page_number" in call_data:
        pagenumber = call_data["page_number"]
        page_info = skilift.item_info(editedprojname, pagenumber)
        if page_info is None:
            raise FailPage("Page to edit not identified")
        if (page_info.item_type != "TemplatePage") and (page_info.item_type != "SVG"):
            raise FailPage("Page not identified")
    elif "section_name" in call_data:
        section_name = call_data["section_name"]
    else:
        raise FailPage(message = "No page or section given")

    if ("widgetinserts","uploadpart","hidden_field1") not in call_data:
        raise FailPage(message = "item to edit missing")

    part = call_data["widgetinserts","uploadpart","hidden_field1"]
    location_list = part.split('-')
    # first item should be a string, rest integers
    try:
        widget_name = location_list[0]
        container = int(location_list[1])
        if len(location_list) < 3:
            location_integers = ()
        else:
            location_integers = tuple( int(i) for i in location_list[2:] )
    except:
        raise FailPage("Item to append to has not been recognised")

    location = (widget_name, container, location_integers)
    # get part_tuple from project, pagenumber, section_name, location
    part_tuple = skilift.part_info(editedprojname, pagenumber, section_name, location)
    if part_tuple is None:
        raise FailPage("Item to append to has not been recognised")
    # get file contents
    file_contents = call_data["widgetinserts","uploadpart", "action"]
    json_string = file_contents.decode(encoding='utf-8')
    try:
        if pagenumber:
            call_data['pchange'] = editpage.create_part_in_page(editedprojname, pagenumber, call_data['pchange'], location, json_string)
        else:
            call_data['schange'] = editsection.create_part_in_section(editedprojname, section_name, call_data['schange'], location, json_string)
    except ServerError as e:
        if e.message:
            raise FailPage(e.message)
        else:
            raise FailPage("An error has occurred in creating the item")
    call_data['widget_name'] = widget_name
    call_data['container'] = container
    call_data['status'] = 'New block created'


