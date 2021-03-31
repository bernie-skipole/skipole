

from ... import FailPage, ValidateError, GoTo, ServerError, skilift

from ....skilift import editpage, editsection

from ....ski.project_class_definition import SectionData


def insert_in_page(skicall):
    """Called by domtable to either insert or append an item in a page
       sets page_data to populate the insert or append modal panel"""

    call_data = skicall.call_data
    pd = call_data['pagedata']

    if "page_number" in call_data:
        pagenumber = call_data["page_number"]
    else:
        raise FailPage(message = "Page number missing")
    if pagenumber is None:
        raise FailPage(message = "Page number missing")
    if ('editdom', 'domtable', 'contents') not in call_data:
        raise FailPage(message = "item to edit missing")
    editedprojname = call_data['editedprojname']
    part = call_data['editdom', 'domtable', 'contents']

    # so part is location_string with string of integers
    # where location_string is one of 'head', 'body', 'svg'

    # create location which is a tuple or list consisting of three items:
    # a location_string
    # a container integer, in this case always None
    # a tuple or list of location integers
    location_list = part.split('-')
    # first item should be a string, rest integers
    try:
        if len(location_list) == 1:
            # no location integers, so location_list[0] is the section name
            location_integers = ()
        else:
            location_integers = tuple( int(i) for i in location_list[1:] )
        location_string = location_list[0]
    except:
        raise FailPage("Item to append to has not been recognised")

    if location_string not in ('head', 'body', 'svg'):
        raise FailPage("Item to append to has not been recognised")

    # location is a tuple of location_string, None for no container, tuple of location integers
    location = (location_string, None, location_integers)
    # get part_tuple from project, pagenumber, section_name, location
    part_tuple = skilift.part_info(editedprojname, pagenumber, None, location)
    if part_tuple is None:
        raise FailPage("Item to append to has not been recognised")

    insert_location = location_string + '-' + '-'.join(str(i) for i in location_integers)

    if location_integers:
        insert_location = location_string + '-' + '-'.join(str(i) for i in location_integers)
    else:
        insert_location = location_string

    # display the modal panel

    sd = SectionData("pageinserts")

    sd["insertitem","hide"] = False

    if (part_tuple.part_type == "Part") or (part_tuple.part_type == "Section"):
        # insert
        sd["insertpara","para_text"] = "Choose an item to insert"
        sd["insertupload","para_text"] = "Or insert a new block by uploading a block definition file:"
    else:
        # append
        sd["insertpara","para_text"] = "Choose an item to append"
        sd["insertupload","para_text"] = "Or append a new block by uploading a block definition file:"

    # for each of the links, set get_field1 to be the insert_location
    sd["insert_text","get_field1"] = insert_location
    sd["insert_textblock","get_field1"] = insert_location
    sd["insert_symbol","get_field1"] = insert_location
    sd["insert_comment","get_field1"] = insert_location
    sd["insert_element","get_field1"] = insert_location
    sd["insert_widget","get_field1"] = insert_location
    sd["insert_section","get_field1"] = insert_location

    # set the hidden field
    sd["uploadpart","hidden_field1"] = insert_location

    # update the PageData object with this SectionData object
    pd.update(sd)


def insert_text(skicall):
    "Inserts text into a page"

    call_data = skicall.call_data
    pd = call_data['pagedata']

    if "page_number" in call_data:
        pagenumber = call_data["page_number"]
    else:
        raise FailPage(message = "Page number missing")
    if pagenumber is None:
        raise FailPage(message = "Page number missing")
    if ("pageinserts","insert_text","get_field1") not in call_data:
        raise FailPage(message = "item to edit missing")
    editedprojname = call_data['editedprojname']

    page_info = skilift.item_info(editedprojname, pagenumber)
    if page_info is None:
        raise FailPage("Page to edit not identified")
    if (page_info.item_type != "TemplatePage") and (page_info.item_type != "SVG"):
        raise FailPage("Page not identified")

    part = call_data["pageinserts","insert_text","get_field1"]
    location_list = part.split('-')
    # first item should be a string, rest integers
    try:
        if len(location_list) == 1:
            # no location integers, so location_list[0] is the section name
            location_integers = ()
        else:
            location_integers = tuple( int(i) for i in location_list[1:] )
        location_string = location_list[0]
    except:
        raise FailPage("Item to append to has not been recognised")

    if location_string not in ('head', 'body', 'svg'):
        raise FailPage("Item to append to has not been recognised")

    # location is a tuple of location_string, None for no container, tuple of location integers
    location = (location_string, None, location_integers)
    # get part_tuple from project, pagenumber, section_name, location
    part_tuple = skilift.part_info(editedprojname, pagenumber, None, location)
    if part_tuple is None:
        raise FailPage("Item to append to has not been recognised")

    new_text = 'Set text here'
    call_data['pchange'], new_location = skilift.insert_item_in_page(editedprojname, pagenumber, call_data['pchange'], location, new_text)
    call_data['location'] = new_location
    
    # go to edit text page
    sd_adminhead = SectionData("adminhead")
    sd_adminhead["page_head","large_text"] = "Edit Text in page : %s" % (pagenumber,)
    pd.update(sd_adminhead)

    # Set the text in the text area
    pd["text_input","input_text"] = new_text


def insert_textblock(skicall):
    "Fills the template page for creating a textblock reference which will be inserted in the edited page"

    call_data = skicall.call_data
    pd = call_data['pagedata']

    if "page_number" in call_data:
        pagenumber = call_data["page_number"]
    else:
        raise FailPage(message = "Page number missing")
    if pagenumber is None:
        raise FailPage(message = "Page number missing")
    if ("pageinserts","insert_textblock","get_field1") not in call_data:
        raise FailPage(message = "item to edit missing")
    editedprojname = call_data['editedprojname']

    page_info = skilift.item_info(editedprojname, pagenumber)
    if page_info is None:
        raise FailPage("Page to edit not identified")
    if (page_info.item_type != "TemplatePage") and (page_info.item_type != "SVG"):
        raise FailPage("Page not identified")

    part = call_data["pageinserts","insert_textblock","get_field1"]
    location_list = part.split('-')
    # first item should be a string, rest integers
    try:
        if len(location_list) == 1:
            # no location integers, so location_list[0] is the section name
            location_integers = ()
        else:
            location_integers = tuple( int(i) for i in location_list[1:] )
        location_string = location_list[0]
    except:
        raise FailPage("Item to append to has not been recognised")

    if location_string not in ('head', 'body', 'svg'):
        raise FailPage("Item to append to has not been recognised")

    # location is a tuple of location_string, None for no container, tuple of location integers
    location = (location_string, None, location_integers)
    # get part_tuple from project, pagenumber, section_name, location
    part_tuple = skilift.part_info(editedprojname, pagenumber, None, location)
    if part_tuple is None:
        raise FailPage("Item to append to has not been recognised")
    call_data['location'] = location

    # and set page data for the template page which inserts an textblock reference

    sd_adminhead = SectionData("adminhead")
    sd_adminhead["page_head","large_text"] = "Insert TextBlock in page %s" % (pagenumber,)
    pd.update(sd_adminhead)

    pd["linebreaks","radio_values"]=['ON', 'OFF']
    pd["linebreaks","radio_text"]=['On', 'Off']
    pd["linebreaks","radio_checked"] = 'ON'

    pd["setescape","radio_values"]=['ON', 'OFF']
    pd["setescape","radio_text"]=['On', 'Off']
    pd["setescape","radio_checked"] = 'ON'



def insert_symbol(skicall):
    "Inserts html symbol into a page"

    call_data = skicall.call_data
    pd = call_data['pagedata']

    if "page_number" in call_data:
        pagenumber = call_data["page_number"]
    else:
        raise FailPage(message = "Page number missing")
    if pagenumber is None:
        raise FailPage(message = "Page number missing")
    if ("pageinserts","insert_symbol","get_field1") not in call_data:
        raise FailPage(message = "item to edit missing")
    editedprojname = call_data['editedprojname']

    page_info = skilift.item_info(editedprojname, pagenumber)
    if page_info is None:
        raise FailPage("Page to edit not identified")
    if (page_info.item_type != "TemplatePage") and (page_info.item_type != "SVG"):
        raise FailPage("Page not identified")

    part = call_data["pageinserts","insert_symbol","get_field1"]
    location_list = part.split('-')
    # first item should be a string, rest integers
    try:
        if len(location_list) == 1:
            # no location integers, so location_list[0] is the section name
            location_integers = ()
        else:
            location_integers = tuple( int(i) for i in location_list[1:] )
        location_string = location_list[0]
    except:
        raise FailPage("Item to append to has not been recognised")

    if location_string not in ('head', 'body', 'svg'):
        raise FailPage("Item to append to has not been recognised")

    # location is a tuple of location_string, None for no container, tuple of location integers
    location = (location_string, None, location_integers)
    # get part_tuple from project, pagenumber, section_name, location
    part_tuple = skilift.part_info(editedprojname, pagenumber, None, location)
    if part_tuple is None:
        raise FailPage("Item to append to has not been recognised")
    call_data['pchange'], new_location = editpage.create_html_symbol_in_page(editedprojname, pagenumber, call_data['pchange'], location)
    call_data['location'] = new_location
    
    # go to edit symbol page
    sym = editpage.get_symbol(editedprojname, pagenumber, call_data['pchange'], new_location)

    sd_adminhead = SectionData("adminhead")
    sd_adminhead["page_head","large_text"] = "Edit Symbol in page : %s" % (pagenumber,)
    pd.update(sd_adminhead)

    pd["symbol_input","input_text"] = sym


def insert_comment(skicall):
    "Inserts a comment into a page"

    call_data = skicall.call_data
    pd = call_data['pagedata']

    if "page_number" in call_data:
        pagenumber = call_data["page_number"]
    else:
        raise FailPage(message = "Page number missing")
    if pagenumber is None:
        raise FailPage(message = "Page number missing")
    if ("pageinserts","insert_comment","get_field1") not in call_data:
        raise FailPage(message = "item to edit missing")
    editedprojname = call_data['editedprojname']

    page_info = skilift.item_info(editedprojname, pagenumber)
    if page_info is None:
        raise FailPage("Page to edit not identified")
    if (page_info.item_type != "TemplatePage") and (page_info.item_type != "SVG"):
        raise FailPage("Page not identified")

    part = call_data["pageinserts","insert_comment","get_field1"]
    location_list = part.split('-')
    # first item should be a string, rest integers
    try:
        if len(location_list) == 1:
            # no location integers, so location_list[0] is the section name
            location_integers = ()
        else:
            location_integers = tuple( int(i) for i in location_list[1:] )
        location_string = location_list[0]
    except:
        raise FailPage("Item to append to has not been recognised")

    if location_string not in ('head', 'body', 'svg'):
        raise FailPage("Item to append to has not been recognised")

    # location is a tuple of location_string, None for no container, tuple of location integers
    location = (location_string, None, location_integers)
    # get part_tuple from project, pagenumber, section_name, location
    part_tuple = skilift.part_info(editedprojname, pagenumber, None, location)
    if part_tuple is None:
        raise FailPage("Item to append to has not been recognised")
    call_data['pchange'], new_location = editpage.create_html_comment_in_page(editedprojname, pagenumber, call_data['pchange'], location)
    call_data['location'] = new_location
    
    # go to edit comment page
    com = editpage.get_comment(editedprojname, pagenumber, call_data['pchange'], new_location)

    sd_adminhead = SectionData("adminhead")
    sd_adminhead["page_head","large_text"] = "Edit Comment in page : %s" % (pagenumber,)
    pd.update(sd_adminhead)

    pd["comment_input","input_text"] = com


def insert_element(skicall):
    "Fills the template page for creating an html element which will be inserted in the edited page"

    call_data = skicall.call_data
    pd = call_data['pagedata']

    if "page_number" in call_data:
        pagenumber = call_data["page_number"]
    else:
        raise FailPage(message = "Page number missing")
    if pagenumber is None:
        raise FailPage(message = "Page number missing")
    if ("pageinserts","insert_element","get_field1") not in call_data:
        raise FailPage(message = "item to edit missing")
    editedprojname = call_data['editedprojname']

    page_info = skilift.item_info(editedprojname, pagenumber)
    if page_info is None:
        raise FailPage("Page to edit not identified")
    if (page_info.item_type != "TemplatePage") and (page_info.item_type != "SVG"):
        raise FailPage("Page not identified")

    part = call_data["pageinserts","insert_element","get_field1"]
    location_list = part.split('-')
    # first item should be a string, rest integers
    try:
        if len(location_list) == 1:
            # no location integers, so location_list[0] is the section name
            location_integers = ()
        else:
            location_integers = tuple( int(i) for i in location_list[1:] )
        location_string = location_list[0]
    except:
        raise FailPage("Item to append to has not been recognised")

    if location_string not in ('head', 'body', 'svg'):
        raise FailPage("Item to append to has not been recognised")

    # location is a tuple of location_string, None for no container, tuple of location integers
    location = (location_string, None, location_integers)
    # get part_tuple from project, pagenumber, section_name, location
    part_tuple = skilift.part_info(editedprojname, pagenumber, None, location)
    if part_tuple is None:
        raise FailPage("Item to append to has not been recognised")
    call_data['location'] = location

    # and set page data for the template page which inserts an element
    sd_adminhead = SectionData("adminhead")
    sd_adminhead["page_head","large_text"] = "Insert an HTML element into page %s" % (pagenumber,)
    pd.update(sd_adminhead)



def insert_widget(skicall):
    "Gets page number and location, used for creating a widget which will be inserted in the page"

    call_data = skicall.call_data

    if "page_number" in call_data:
        pagenumber = call_data["page_number"]
    else:
        raise FailPage(message = "Page number missing")
    if pagenumber is None:
        raise FailPage(message = "Page number missing")
    if ("pageinserts","insert_widget","get_field1") not in call_data:
        raise FailPage(message = "item to edit missing")
    editedprojname = call_data['editedprojname']

    page_info = skilift.item_info(editedprojname, pagenumber)
    if page_info is None:
        raise FailPage("Page to edit not identified")
    if (page_info.item_type != "TemplatePage") and (page_info.item_type != "SVG"):
        raise FailPage("Page not identified")

    part = call_data["pageinserts","insert_widget","get_field1"]
    location_list = part.split('-')
    # first item should be a string, rest integers
    try:
        if len(location_list) == 1:
            # no location integers, so location_list[0] is the section name
            location_integers = ()
        else:
            location_integers = tuple( int(i) for i in location_list[1:] )
        location_string = location_list[0]
    except:
        raise FailPage("Item to append to has not been recognised")

    if location_string not in ('head', 'body', 'svg'):
        raise FailPage("Item to append to has not been recognised")

    # location is a tuple of location_string, None for no container, tuple of location integers
    location = (location_string, None, location_integers)
    # get part_tuple from project, pagenumber, section_name, location
    part_tuple = skilift.part_info(editedprojname, pagenumber, None, location)
    if part_tuple is None:
        raise FailPage("Item to append to has not been recognised")
    call_data['location'] = location

    # at this point, the call is passed to 54507 which is a responder which lists widget modules
    # and displays them on a template


def insert_section(skicall):
    "Gets page number and location, used for creating a section reference which will be inserted in the page"

    call_data = skicall.call_data
    pd = call_data['pagedata']

    if "page_number" in call_data:
        pagenumber = call_data["page_number"]
    else:
        raise FailPage(message = "Page number missing")
    if pagenumber is None:
        raise FailPage(message = "Page number missing")
    if ("pageinserts","insert_section","get_field1") not in call_data:
        raise FailPage(message = "item to edit missing")
    editedprojname = call_data['editedprojname']

    page_info = skilift.item_info(editedprojname, pagenumber)
    if page_info is None:
        raise FailPage("Page to edit not identified")
    if (page_info.item_type != "TemplatePage") and (page_info.item_type != "SVG"):
        raise FailPage("Page not identified")

    part = call_data["pageinserts","insert_section","get_field1"]
    location_list = part.split('-')
    # first item should be a string, rest integers
    try:
        if len(location_list) == 1:
            # no location integers, so location_list[0] is the section name
            location_integers = ()
        else:
            location_integers = tuple( int(i) for i in location_list[1:] )
        location_string = location_list[0]
    except:
        raise FailPage("Item to append to has not been recognised")

    if location_string not in ('head', 'body', 'svg'):
        raise FailPage("Item to append to has not been recognised")

    # location is a tuple of location_string, None for no container, tuple of location integers
    location = (location_string, None, location_integers)
    # get part_tuple from project, pagenumber, section_name, location
    part_tuple = skilift.part_info(editedprojname, pagenumber, None, location)
    if part_tuple is None:
        raise FailPage("Item to append to has not been recognised")
    call_data['location'] = location

    # Fill in header
    sd_adminhead = SectionData("adminhead")
    sd_adminhead["page_head","large_text"] = "Insert Section place holder"
    pd.update(sd_adminhead)

    # get current sections
    section_list = editsection.list_section_names(editedprojname)
    if not section_list:
        pd["nosection", "show"] = True
        pd["descript", "show"] = False
        pd["placename","show"] = False
        return

    pd['sectionname','option_list'] = section_list[:]
    pd['sectionname','selectvalue'] = section_list[0]



def insert_upload(skicall):
    "Gets page number and location, used for creating a widget which will be inserted in the page"

    call_data = skicall.call_data

    if "page_number" in call_data:
        pagenumber = call_data["page_number"]
    else:
        raise FailPage(message = "Page number missing")
    if pagenumber is None:
        raise FailPage(message = "Page number missing")
    if ("pageinserts","uploadpart","hidden_field1") not in call_data:
        raise FailPage(message = "item to edit missing")
    editedprojname = call_data['editedprojname']

    page_info = skilift.item_info(editedprojname, pagenumber)
    if page_info is None:
        raise FailPage("Page to edit not identified")
    if (page_info.item_type != "TemplatePage") and (page_info.item_type != "SVG"):
        raise FailPage("Page not identified")

    part = call_data["pageinserts","uploadpart","hidden_field1"]
    location_list = part.split('-')
    # first item should be a string, rest integers
    try:
        if len(location_list) == 1:
            # no location integers, so location_list[0] is the section name
            location_integers = ()
        else:
            location_integers = tuple( int(i) for i in location_list[1:] )
        location_string = location_list[0]
    except:
        raise FailPage("Item to append to has not been recognised")

    if location_string not in ('head', 'body', 'svg'):
        raise FailPage("Item to append to has not been recognised")

    # location is a tuple of location_string, None for no container, tuple of location integers
    location = (location_string, None, location_integers)
    # get part_tuple from project, pagenumber, section_name, location
    part_tuple = skilift.part_info(editedprojname, pagenumber, None, location)
    if part_tuple is None:
        raise FailPage("Item to append to has not been recognised")
    # get file contents
    file_contents = call_data["pageinserts","uploadpart", "action"]
    json_string = file_contents.decode(encoding='utf-8')
    try:
        call_data['pchange'] = editpage.create_part_in_page(editedprojname, pagenumber, call_data['pchange'], location, json_string)
    except ServerError as e:
        if e.message:
            raise FailPage(e.message)
        else:
            raise FailPage("An error has occurred in creating the item")

    # this is necessary to go back to the right page
    call_data['location_string'] = location_string
    call_data['status'] = 'New block created'


