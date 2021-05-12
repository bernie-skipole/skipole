

"Functions implementing admin page editing"

import html, json

from ... import ValidateError, FailPage, ServerError, GoTo

from ... import skilift
from ....skilift import fromjson, part_contents, editpage

from ....ski.project_class_definition import SectionData

from .. import utils


def retrieve_page_edit(skicall):
    "Retrieves data for the edit page"

    call_data = skicall.call_data
    pd = call_data['pagedata']

    # clears any session data, keeping page_number, pchange and any status message
    utils.clear_call_data(call_data, keep=["page_number", "pchange", "status"])

    if 'page_number' in call_data:
        pagenumber = call_data['page_number']
        str_pagenumber = str(pagenumber)
    else:
        raise FailPage(message = "page missing")

    try:
        project = call_data['editedprojname']
        pageinfo = skilift.page_info(project, pagenumber)

        if pageinfo.item_type != 'TemplatePage':
            raise FailPage(message = "Invalid page")

        call_data['pchange'] = pageinfo.change

        sd_adminhead = SectionData("adminhead")
        sd_page_edit = SectionData("page_edit")

        # fills in the data for editing page name, brief, parent, etc., 
        sd_adminhead["page_head","large_text"] = pageinfo.name
        sd_page_edit['p_ident','page_ident'] = (project,str_pagenumber)
        sd_page_edit['p_name','page_ident'] = (project,str_pagenumber)
        sd_page_edit['p_description','page_ident'] = (project,str_pagenumber)
        sd_page_edit['p_rename','input_text'] = pageinfo.name
        sd_page_edit['p_parent','input_text'] = "%s,%s" % (project, pageinfo.parentfolder_number)
        sd_page_edit['p_brief','input_text'] = pageinfo.brief

        pd.update(sd_adminhead)
        pd.update(sd_page_edit)

        pageOD = fromjson.page_to_OD(project, pagenumber)
    except ServerError as e:
        raise FailPage(message=e.message)

    if "TemplatePage" in pageOD:
        pagedict = pageOD["TemplatePage"]
    else:
        raise FailPage(message="This page not recognised as a Template page.")

    # page language
    pd["setlang","input_text"] = pagedict["lang"]

    # default error widget
    dew = pagedict["default_error_widget"]
    if dew[0]:
        pd["default_e_widg","input_text"] = dew[0] + ',' + dew[1] ############
        pd["d_e_section","input_text"] = dew[0]
        pd["d_e_widget","input_text"] = dew[1]

    elif dew[1]:
        pd["default_e_widg","input_text"] = dew[1]                #############
        pd["d_e_widget","input_text"] = dew[1]

    # sets last_scroll flag
    pd["lastscroll","checked"] = pagedict["last_scroll"]

    # fills in the backcolor checkbox and value
    if pagedict["show_backcol"]:
        pd["enablebackcolor","checked"] = True
        pd['setbackcolor', 'hide'] = False
    else:
        pd["enablebackcolor","checked"] = False
        pd['setbackcolor', 'hide'] = True

    pd['setbackcolor', 'input_text'] = pagedict["backcol"]

    # Sets CatchToHTML
    if pagedict["catch_to_html"] is None:
        pd["set_catch_to_html", "input_text"] = ''
    else:
        pd["set_catch_to_html", "input_text"] = str(pagedict["catch_to_html"])

    # fills in the JSON refresh checkbox
    if pagedict["interval"] and pagedict["interval_target"]:
        if pagedict["interval_target"] is None:
            interval_target = ''
        else:
            interval_target = str(pagedict["interval_target"])
        pd["refreshcheck","checked"] = True
        pd['interval', 'disabled'] = False
        pd['interval_target', 'disabled'] = False
        pd['interval', 'input_text'] = str(pagedict["interval"])
        pd['interval_target', 'input_text'] = interval_target
    else:
        pd["refreshcheck","checked"] = False
        pd['interval', 'disabled'] = True
        pd['interval_target', 'disabled'] = True
        pd['interval', 'input_text'] = '0'
        pd['interval_target', 'input_text'] = ''


def retrieve_page_head(skicall):
    "Gets data for the page head"

    call_data = skicall.call_data
    pd = call_data['pagedata']

    project = call_data['editedprojname']

    if "page_number" in call_data:
        pagenumber = call_data["page_number"]
    else:
        raise FailPage(message = "Page number missing")

    if pagenumber is None:
        raise FailPage(message = "Page number missing")

    try:
        pageinfo = skilift.page_info(project, pagenumber)
    except ServerError as e:
        raise FailPage(message=e.message)

    if pageinfo.item_type != 'TemplatePage':
        raise FailPage(message = "Invalid page")

    sd_adminhead = SectionData("adminhead")
    sd_adminhead["page_head","large_text"] = pageinfo.name + ' head'
    pd.update(sd_adminhead)

    pd["pageid", "para_text"] = "Page Ident: " + str(pagenumber)

    # fill in the table
    call_data['location_string'] = 'head'
    retrieve_page_dom(skicall)


def retrieve_page_dom(skicall):
    "this call fills in the page dom table"

    call_data = skicall.call_data
    pd = call_data['pagedata']

    project = call_data['editedprojname']

    if "page_number" in call_data:
        pagenumber = call_data["page_number"]
    else:
        raise FailPage(message = "Page number missing")

    if pagenumber is None:
        raise FailPage(message = "Page number missing")

    location_string = call_data['location_string']

    try:
        domcontents, dragrows, droprows = _page_domcontents(project, pagenumber, location_string)
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

    sd_editdom = SectionData("editdom")
    sd_editdom['domtable', 'contents']  = domcontents
    sd_editdom['domtable', 'dragrows']  = dragrows
    sd_editdom['domtable', 'droprows']  = droprows

    # for each column: html link, JSON link, storage key
    sd_editdom['domtable', 'cols']  =  [  ['','',''],                                          # tag name, no link
                                          ['','',''],                                          # brief, no link
                                          ['no_javascript','move_up_in_page_dom',''],          # up arrow
                                          ['no_javascript','move_up_right_in_page_dom',''],    # up right
                                          ['no_javascript','move_down_in_page_dom',''],        # down
                                          ['no_javascript','move_down_right_in_page_dom',''],  # down right
                                          ['edit_page_dom','',''],                             # edit, html only
                                          ['no_javascript','insert_in_page',''],               # insert/append
                                          ['no_javascript',3680,''],                           # copy
                                          ['no_javascript',3690,'ski_part'],                   # paste
                                          ['no_javascript','cut_page_dom',''],                 # cut
                                          ['no_javascript','delete_page_dom','']               # delete
                                       ]

    sd_editdom['domtable', 'dropident']  = 'move_in_page_dom'

    pd.update(sd_editdom)

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


def retrieve_page_body(skicall):
    "Gets data for the page body"

    call_data = skicall.call_data
    pd = call_data['pagedata']

    project = call_data['editedprojname']

    if "page_number" in call_data:
        pagenumber = call_data["page_number"]
    else:
        raise FailPage(message = "Page number missing")

    if pagenumber is None:
        raise FailPage(message = "Page number missing")

    try:
        pageinfo = skilift.page_info(project, pagenumber)
    except ServerError as e:
        raise FailPage(message=e.message)

    if pageinfo.item_type != 'TemplatePage':
        raise FailPage(message = "Invalid page")

    sd_adminhead = SectionData("adminhead")
    sd_adminhead["page_head","large_text"] = pageinfo.name + ' body'
    pd.update(sd_adminhead)

    pd["pageid", "para_text"] = "Page Ident: " + str(pagenumber)

    # fill in the table
    call_data['location_string'] = 'body'
    retrieve_page_dom(skicall)



def copy_page(skicall):
    "Gets page part and set PageData().localStorage with key ski_part for browser session storage"
    call_data = skicall.call_data
    pd = call_data['pagedata']

    if "page_number" in call_data:
        pagenumber = call_data["page_number"]
    else:
        raise FailPage(message = "Page number missing")

    if pagenumber is None:
        raise FailPage(message = "Page number missing")

    if ('editdom', 'domtable', 'contents') not in call_data:
        raise FailPage(message = "item to copy missing")
    editedprojname = call_data['editedprojname']
    part = call_data['editdom', 'domtable', 'contents']

    # so part is location_string with string of integers

    # create location which is a tuple or list consisting of three items:
    # a location_string
    # a container integer, in this case always None
    # a tuple or list of location integers
    location_list = part.split('-')
    # first item should be a string, rest integers
    if len(location_list) == 1:
        location_integers = ()
    else:
        location_integers = tuple( int(i) for i in location_list[1:] )
    location_string = location_list[0]

    # location is a tuple of location_string, None for no container, tuple of location integers
    location = (location_string, None, location_integers)

    # get a json string dump of the item outline, however change any Sections to Parts
    itempart, itemdict = fromjson.item_outline(editedprojname, pagenumber, None, location)
    if itempart == 'Section':
        jsonstring = json.dumps(['Part',itemdict], indent=0, separators=(',', ':'))
    else:
        jsonstring = json.dumps([itempart,itemdict], indent=0, separators=(',', ':'))
    pd.localStorage = {'ski_part':jsonstring}
    call_data['status'] = 'Item copied, and can now be pasted.'


def paste_page(skicall):
    "Gets submitted json string and inserts it"
    call_data = skicall.call_data
    pd = call_data['pagedata']

    if "page_number" in call_data:
        pagenumber = call_data["page_number"]
    else:
        raise FailPage(message = "Page number missing")
    if pagenumber is None:
        raise FailPage(message = "Page number missing")
    if ('editdom', 'domtable', 'contents') not in call_data:
        raise FailPage(message = "position to paste missing")
    if ('editdom', 'domtable', 'cols') not in call_data:
        raise FailPage(message = "item to paste missing")
    json_string = call_data['editdom', 'domtable', 'cols']

    editedprojname = call_data['editedprojname']
    part = call_data['editdom', 'domtable', 'contents']

    # so part is location_string with string of integers

    # create location which is a tuple or list consisting of three items:
    # a location_string
    # a container integer, in this case always None
    # a tuple or list of location integers
    location_list = part.split('-')
    # first item should be a string, rest integers
    if len(location_list) == 1:
        # no location integers
        location_integers = ()
    else:
        location_integers = tuple( int(i) for i in location_list[1:] )
    location_string = location_list[0]

    # location is a tuple of location_string, None for no container, tuple of location integers
    location = (location_string, None, location_integers)

    call_data['pchange'] = editpage.create_item_in_page(editedprojname, pagenumber, call_data['pchange'], location, json_string)

    domcontents, dragrows, droprows = _page_domcontents(editedprojname, pagenumber, location_string)

    sd_editdom = SectionData("editdom")
    sd_editdom['domtable', 'dragrows']  = dragrows
    sd_editdom['domtable', 'droprows']  = droprows
    sd_editdom['domtable', 'contents']  = domcontents
    pd.update(sd_editdom)



def retrieve_svgpage_edit(skicall):
    "Retrieves widget data for the svg edit page"

    call_data = skicall.call_data
    pd = call_data['pagedata']

    # clears any session data, keeping page_number, pchange and any status message
    utils.clear_call_data(call_data, keep=["page_number", "pchange", "status"])

    if 'page_number' in call_data:
        pagenumber = call_data['page_number']
        str_pagenumber = str(pagenumber)
    else:
        raise FailPage(message = "page missing")

    try:
        project = call_data['editedprojname']
        pageinfo = skilift.page_info(project, pagenumber)

        if pageinfo.item_type != 'SVG':
            raise FailPage(message = "Invalid page")

        call_data['pchange'] = pageinfo.change

        # fills in the data for editing page name, brief, parent, etc.,

        sd_adminhead = SectionData("adminhead")
        sd_adminhead["page_head","large_text"] = pageinfo.name
        pd.update(sd_adminhead)

        sd_page_edit = SectionData("page_edit")
        sd_page_edit['p_ident','page_ident'] = (project,str_pagenumber)
        sd_page_edit['p_name','page_ident'] = (project,str_pagenumber)
        sd_page_edit['p_description','page_ident'] = (project,str_pagenumber)
        sd_page_edit['p_rename','input_text'] = pageinfo.name
        sd_page_edit['p_parent','input_text'] = "%s,%s" % (project, pageinfo.parentfolder_number)
        sd_page_edit['p_brief','input_text'] = pageinfo.brief
        pd.update(sd_page_edit)

        pd['enable_cache','radio_checked'] = pageinfo.enable_cache

    except ServerError as e:
        raise FailPage(message=e.message)


def retrieve_page_svg(skicall):
    "Gets data for the page svg part"

    call_data = skicall.call_data
    pd = call_data['pagedata']

    project = call_data['editedprojname']

    if "page_number" in call_data:
        pagenumber = call_data["page_number"]
    else:
        raise FailPage(message = "Page number missing")
    if pagenumber is None:
        raise FailPage(message = "Page number missing")
    try:
        pageinfo = skilift.page_info(project, pagenumber)
    except ServerError as e:
        raise FailPage(message = e.message)
    if pageinfo.item_type != 'SVG':
        raise FailPage(message = "Invalid page")

    sd_adminhead = SectionData("adminhead")
    sd_adminhead["page_head","large_text"] = pageinfo.name + ' svg'
    pd.update(sd_adminhead)

    pd["pageid", "para_text"] = "Page Ident: " + str(pagenumber)
    # fill in the table
    call_data['location_string'] = 'svg'
    retrieve_page_dom(skicall)


def set_html_lang(skicall):
    "Sets language in the page html tag"

    call_data = skicall.call_data

    project = call_data['editedprojname']
    pagenumber = call_data['page_number']
    pchange = call_data['pchange']
    if not 'setlang' in call_data:
        raise FailPage(message="No language given", widget="setlang")
    new_lang = call_data['setlang']
    # call skilift.editpage.page_language which returns a new pchange
    try:
        call_data['pchange'] = editpage.page_language(project, pagenumber, pchange, new_lang)
    except ServerError as e:
        raise FailPage(e.message)
    if not new_lang:
        call_data['status'] = "No language set"
    else:
        call_data['status'] = "Page language set to %s" % new_lang


def enable_backcolour(skicall):
    """Enables background colour in HTML tag"""

    call_data = skicall.call_data

    project = call_data['editedprojname']
    pagenumber = call_data['page_number']
    pchange = call_data['pchange']

    try:
        show_backcol, backcol = editpage.get_page_backcol(project, pagenumber, pchange)

        if (("enablebackcolor","checkbox") in call_data) and call_data["enablebackcolor","checkbox"]:
            show_backcol = True
            result = "Background colour %s set in HTML tag" % backcol
        else:
            show_backcol = False
            result = "Background colour removed from HTML tag"

        call_data['pchange'] = editpage.page_backcol(project, pagenumber, pchange, show_backcol, backcol)
    except ServerError as e:
        raise FailPage(message=e.message)
    call_data['status'] = result


def set_backcolour(skicall):
    """Sets the background colour in the HTML tag"""

    call_data = skicall.call_data

    project = call_data['editedprojname']
    pagenumber = call_data['page_number']
    pchange = call_data['pchange']

    try:
        show_backcol, backcol = editpage.get_page_backcol(project, pagenumber, pchange)

        if show_backcol == False:
            raise FailPage(message = "Backgound colour in HTML tag has not been enabled")

        if (('setbackcolor','input_text') in call_data) and call_data['setbackcolor','input_text']:
            backcol = call_data['setbackcolor','input_text']
        else:
            raise FailPage(message = "Background colour to set is missing")

        call_data['pchange'] = editpage.page_backcol(project, pagenumber, pchange, show_backcol, backcol)

    except ServerError as e:
        raise FailPage(message=e.message)
    call_data['status'] = 'HTML tag background color set to %s' % backcol



def set_last_scroll(skicall):
    "Sets page last_scroll flag"

    call_data = skicall.call_data

    project = call_data['editedprojname']
    pagenumber = call_data['page_number']
    pchange = call_data['pchange']
    try:
        if (('lastscroll','checkbox') in call_data) and (call_data['lastscroll','checkbox'] == 'checked'):
            # enable the last_scroll flag
            call_data['pchange'] = editpage.page_last_scroll(project, pagenumber, pchange, True)
            text = 'Page will be displayed at the last scroll position'
        else:
            # disable the last_scroll flag
            call_data['pchange'] = editpage.page_last_scroll(project, pagenumber, pchange, False)
            text = 'Page will not display at previous scroll position'
    except ServerError as e:
        raise FailPage(message=e.message)
    call_data['status'] = text



def set_catch_to_html(skicall):
    """Sets the CatchToHTML target"""

    call_data = skicall.call_data

    project = call_data['editedprojname']
    pagenumber = call_data['page_number']
    pchange = call_data['pchange']

    try:
        if ('set_catch_to_html', 'input_text') not in call_data:
            catch_to_html = None
        else:
            catch_to_html = call_data['set_catch_to_html', 'input_text']

        call_data['pchange'] = editpage.catch_to_html(project, pagenumber, pchange, catch_to_html)

    except ServerError as e:
        raise FailPage(message=e.message)
    call_data['status'] = 'CatchToHTML target set'



def submit_refresh(skicall):
    "Sets JSON refresh facility"

    call_data = skicall.call_data

    project = call_data['editedprojname']
    pagenumber = call_data['page_number']
    pchange = call_data['pchange']

    interval = 0
    interval_target = None

    try:
        if ('refreshcheck', 'checkbox') not in call_data:
            interval = 0
        elif call_data['refreshcheck', 'checkbox'] != 'enable_refresh':
            interval = 0
        elif ('interval', 'input_text') not in call_data:
            interval = 0
        elif call_data['interval', 'input_text'] == '0':
            interval = 0
        elif ('interval_target', 'input_text') not in call_data:
            interval = 0
        elif not call_data['interval_target', 'input_text']:
            interval = 0
        else:
            interval = int(call_data['interval', 'input_text'])
            interval_target = call_data['interval_target', 'input_text']
    except Exception:
        raise FailPage(message="Error setting JSON refresh")

    try:
        # set page attributes
        if (interval == 0) or (not interval_target):
            text = 'JSON refresh facility disabled'
            call_data['pchange'] = editpage.page_interval(project, pagenumber, pchange, 0, None)
        else:
            text = 'JSON refresh facility enabled'
            call_data['pchange'] = editpage.page_interval(project, pagenumber, pchange, interval, interval_target)
    except ServerError as e:
        raise FailPage(message=e.message)
    call_data['status'] = text



def set_default_error_widget(skicall):
    "Sets page default_error_widget"

    call_data = skicall.call_data

    project = call_data['editedprojname']
    pagenumber = call_data['page_number']
    pchange = call_data['pchange']

    if (("d_e_widget","input_text") not in call_data) or (not call_data["d_e_widget","input_text"]):
        raise FailPage(message="Error setting default error widget")

    if (("d_e_section","input_text") in call_data) and call_data["d_e_section","input_text"]:
        default_widget = call_data["d_e_section","input_text"] + ',' + call_data["d_e_widget","input_text"]
    else:
        default_widget = call_data["d_e_widget","input_text"]
    try:
        call_data['pchange'] = editpage.page_default_error_widget(project, pagenumber, pchange, default_widget)
    except ServerError as e:
        raise FailPage(message=e.message)
    call_data['status'] = "default error widget set"



def submit_cache(skicall):
    "Sets cache true or false"

    call_data = skicall.call_data

    project = call_data['editedprojname']
    pagenumber = call_data['page_number']
    pchange = call_data['pchange']
    if 'cache' not in call_data:
        raise FailPage(message="No cache instruction given")
    try:
        # Set the page cache
        if call_data['cache'] == 'True':
            enable_cache = True
            message = "Cache Enabled"
        else:
            enable_cache = False
            message = "Cache Disabled"
        call_data['pchange'] = editpage.page_enable_cache(project, pagenumber, pchange, enable_cache)
    except ServerError as e:
        raise FailPage(message=e.message)
    call_data['status'] = message


################## JSON PAGE #############################


def retrieve_edit_jsonpage(skicall):
    "Retrieves widget data for the edit json page"

    call_data = skicall.call_data
    pd = call_data['pagedata']

    # clears any session data, keeping page_number, pchange and any status message
    utils.clear_call_data(call_data, keep=["page_number", "pchange", "status"])

    project = call_data['editedprojname']
    
    if 'page_number' in call_data:
        pagenumber = call_data['page_number']
        str_pagenumber = str(pagenumber)
    else:
        raise FailPage(message = "page missing")

    if not pagenumber:
        raise FailPage(message = "Invalid page")

    try:
        pageinfo = skilift.page_info(project, pagenumber)
        if pageinfo.item_type != 'JSON':
            raise FailPage(message = "Invalid page")

        call_data['pchange'] = pageinfo.change

    except ServerError as e:
        raise FailPage(message = e.message)

    # fills in the data for editing page name, brief, parent, etc.,

    sd_adminhead = SectionData("adminhead")
    sd_adminhead["page_head","large_text"] = pageinfo.name
    pd.update(sd_adminhead)

    sd_page_edit = SectionData("page_edit")
    sd_page_edit['p_ident','page_ident'] = (project,str_pagenumber)
    sd_page_edit['p_name','page_ident'] = (project,str_pagenumber)
    sd_page_edit['p_description','page_ident'] = (project,str_pagenumber)
    sd_page_edit['p_rename','input_text'] = pageinfo.name
    sd_page_edit['p_parent','input_text'] = "%s,%s" % (project, pageinfo.parentfolder_number)
    sd_page_edit['p_brief','input_text'] = pageinfo.brief
    pd.update(sd_page_edit)

    json_content = editpage.json_contents(project, pagenumber)

    if json_content:
        # If json page has contents, show the table of widgfields, values
        contents = []
        for widgfieldinfo,value in json_content.items():
            wfcomma = widgfieldinfo.str_comma_widgfield
            wfstr = widgfieldinfo.str_widgfield
            if value is True:
                contents.append([wfcomma,'True',wfstr])
            elif value is False:
                contents.append([wfcomma,'False',wfstr])
            else:
                contents.append([wfcomma,value,wfstr])
        if contents:
            pd['field_values_list','show'] = True
            pd['field_values_list','contents'] = contents
        else:
            pd['field_values_list','show'] = False
    else:
        pd['field_values_list','show'] = False

    pd['enable_cache','radio_checked'] = pageinfo.enable_cache


def set_json_cache(skicall):
    "Sets cache true or false"

    call_data = skicall.call_data

    project = call_data['editedprojname']
    pagenumber = call_data['page_number']
    pchange = call_data['pchange']
    if ('enable_cache', 'radio_checked') not in call_data:
        raise FailPage(message="No cache instruction given")
    try:
        # Set the page cache
        if call_data['enable_cache', 'radio_checked'] == 'True':
            enable_cache = True
            message = "Cache Enabled"
        else:
            enable_cache = False
            message = "Cache Disabled"
        call_data['pchange'] = editpage.page_enable_cache(project, pagenumber, pchange, enable_cache)
    except ServerError as e:
        raise FailPage(message=e.message)
    call_data['status'] = message


def remove_json_widgfield(skicall):
    "Removes widgfield from JSON page"

    call_data = skicall.call_data

    project = call_data['editedprojname']
    pagenumber = call_data['page_number']
    pchange = call_data['pchange']
    if ('field_values_list','contents') not in call_data:
        raise FailPage(message="No widgfield given")
    try:
        str_widgfield = call_data['field_values_list','contents']
        call_data['pchange'] = editpage.remove_json_widgfield(project, pagenumber, pchange, str_widgfield)
    except ServerError as e:
        raise FailPage(message=e.message)
    call_data['status'] = "Widgfield removed"


def add_json_widgfield(skicall):
    "Adds a widgfield to JSON page"

    call_data = skicall.call_data

    project = call_data['editedprojname']
    pagenumber = call_data['page_number']
    pchange = call_data['pchange']

    str_widgfield = ""

    if (('jsonsection', 'input_text') in call_data) and call_data['jsonsection', 'input_text']:
        str_widgfield = str_widgfield + ',' + call_data['jsonsection', 'input_text']
    jsonwidget = call_data.get(('jsonwidget', 'input_text'))
    if not jsonwidget:
        raise FailPage(message="No widget given")
    str_widgfield = str_widgfield + ',' + jsonwidget
    jsonfield = call_data.get(('jsonfield', 'input_text'))
    if not jsonfield:
        raise FailPage(message="No widget field given")
    str_widgfield = str_widgfield + ',' + jsonfield

    if call_data['jsontrue', 'button_text'] == 'True':
        value = True
    elif call_data['jsonfalse', 'button_text'] == 'False':
        value = False
    elif call_data['jsontext', 'input_text']:
        value = call_data['jsontext', 'input_text']
    else:
        value = ''
    try:
        call_data['pchange'] = editpage.add_json_widgfield(project, pagenumber, pchange, str_widgfield, value)
    except ServerError as e:
        raise FailPage(message=e.message)
    call_data['status'] = "Widget field value added"


def downloadpage(skicall):
    "Gets template or SVG page, and returns a json dictionary, this will be sent as an octet file to be downloaded"

    call_data = skicall.call_data
    pd = call_data['pagedata']

    if 'page_number' in call_data:
        pagenumber = call_data['page_number']
    else:
        raise FailPage(message = "page missing")

    try:
        project = call_data['editedprojname']
        pageinfo = skilift.page_info(project, pagenumber)

        if (pageinfo.item_type != 'TemplatePage') and (pageinfo.item_type != 'SVG'):
            raise FailPage(message = "Invalid page")

        jsonstring = fromjson.page_to_json(project, pagenumber, indent=4)
    except ServerError as e:
        raise FailPage(message=e.message)

    line_list = []
    n = 0
    for line in jsonstring.splitlines(True):
        binline = line.encode('utf-8')
        n += len(binline)
        line_list.append(binline)
    pd.mimetype = 'application/octet-stream'
    pd.content_length = str(n)
    return line_list


def move_up_in_page_dom(skicall):
    "Called by domtable to move an item in a page up"

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

    # create location which is a tuple or list consisting of three items:
    # a location_string
    # a container integer, in this case always None
    # a tuple or list of location integers
    location_list = part.split('-')
    # first item should be a string, rest integers
    if len(location_list) == 1:
        # no location integers
        return
    else:
        location_integers = tuple( int(i) for i in location_list[1:] )
    location_string = location_list[0]

    # location is a tuple of location_string, None for no container, tuple of location integers
    location = (location_string, None, location_integers)
    # get part_tuple from project, pagenumber, section_name, location
    part_tuple = skilift.part_info(editedprojname, pagenumber, None, location)
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

    call_data['location_string'] = location_string

    # move the item
    try:
        call_data['pchange'] = editpage.move_location(editedprojname, pagenumber, call_data['pchange'], location, (location_string, None, new_location_integers))
    except ServerError as e:
        raise FailPage(message = e.message)

    # and re-draw the table
    domcontents, dragrows, droprows = _page_domcontents(editedprojname, pagenumber, location_string)

    sd_editdom = SectionData("editdom")
    sd_editdom['domtable', 'dragrows']  = dragrows
    sd_editdom['domtable', 'droprows']  = droprows
    sd_editdom['domtable', 'contents']  = domcontents
    pd.update(sd_editdom)



def move_up_right_in_page_dom(skicall):
    "Called by domtable to move an item in a page up and to the right"

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

    # create location which is a tuple or list consisting of three items:
    # a location_string
    # a container integer, in this case always None
    # a tuple or list of location integers
    location_list = part.split('-')
    # first item should be a string, rest integers
    if len(location_list) == 1:
        # no location integers, so location_list[0] is the location_string
        return
    else:
        location_integers = tuple( int(i) for i in location_list[1:] )
    location_string = location_list[0]

    # location is a tuple of location_string, None for no container, tuple of location integers
    location = (location_string, None, location_integers)
    # get part_tuple from project, pagenumber, section_name, location
    part_tuple = skilift.part_info(editedprojname, pagenumber, None, location)
    if part_tuple is None:
        raise FailPage("Item to move has not been recognised")

    if location_integers[-1] == 0:
        # at top of a part, cannot be moved
        raise FailPage("Cannot be moved up")
    new_parent_integers = list(location_integers[:-1])
    new_parent_integers.append(location_integers[-1] - 1)
    new_parent_location = (location_string, None, new_parent_integers)

    new_parent_tuple = skilift.part_info(editedprojname, pagenumber, None, new_parent_location)

    if new_parent_tuple is None:
        raise FailPage("Cannot be moved up")
    if new_parent_tuple.part_type != "Part":
        raise FailPage("Cannot be moved up")

    items_in_new_parent = len(part_contents(editedprojname, pagenumber, None, new_parent_location))

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

    call_data['location_string'] = location_string

    # move the item
    try:
        call_data['pchange'] = editpage.move_location(editedprojname, pagenumber, call_data['pchange'], location, (location_string, None, new_location_integers))
    except ServerError as e:
        raise FailPage(message = e.message)

    # and re-draw the table
    domcontents, dragrows, droprows = _page_domcontents(editedprojname, pagenumber, location_string)

    sd_editdom = SectionData("editdom")
    sd_editdom['domtable', 'dragrows']  = dragrows
    sd_editdom['domtable', 'droprows']  = droprows
    sd_editdom['domtable', 'contents']  = domcontents
    pd.update(sd_editdom)




def move_down_in_page_dom(skicall):
    "Called by domtable to move an item in a page down"

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

    # create location which is a tuple or list consisting of three items:
    # a location_string
    # a container integer, in this case always None
    # a tuple or list of location integers
    location_list = part.split('-')
    # first item should be a string, rest integers
    if len(location_list) == 1:
        # no location integers, the location_string top cannot be moved
        return
    else:
        location_integers = tuple( int(i) for i in location_list[1:] )
    location_string = location_list[0]

    # location is a tuple of location_string, None for no container, tuple of location integers
    location = (location_string, None, location_integers)
    # get part_tuple from project, pagenumber, section_name, location
    part_tuple = skilift.part_info(editedprojname, pagenumber, None, location)
    if part_tuple is None:
        raise FailPage("Item to move has not been recognised")

    if len(location_integers) == 1:
        # Just at immediate level below top
        parent_location = (location_string, None, ())
        items_in_parent = len(part_contents(editedprojname, pagenumber, None, parent_location))
        if location_integers[0] == (items_in_parent-1):
            # At end, cannot be moved
            raise FailPage("Cannot be moved down")
        new_location_integers = (location_integers[0]+2,)
    else:
        parent_integers = tuple(location_integers[:-1])
        parent_location = (location_string, None, parent_integers)
        items_in_parent = len(part_contents(editedprojname, pagenumber, None, parent_location))
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

    call_data['location_string'] = location_string

    # move the item
    try:
        call_data['pchange'] = editpage.move_location(editedprojname, pagenumber, call_data['pchange'], location, (location_string, None, new_location_integers))
    except ServerError as e:
        raise FailPage(message = e.message)

    # and re-draw the table
    domcontents, dragrows, droprows = _page_domcontents(editedprojname, pagenumber, location_string)

    sd_editdom = SectionData("editdom")
    sd_editdom['domtable', 'dragrows']  = dragrows
    sd_editdom['domtable', 'droprows']  = droprows
    sd_editdom['domtable', 'contents']  = domcontents
    pd.update(sd_editdom)



def move_down_right_in_page_dom(skicall):
    "Called by domtable to move an item in a page down and to the right"

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

    # create location which is a tuple or list consisting of three items:
    # a location_string
    # a container integer, in this case always None
    # a tuple or list of location integers
    location_list = part.split('-')
    # first item should be a string, rest integers
    if len(location_list) == 1:
        # no location integers, the location_string top cannot be moved
        return
    else:
        location_integers = tuple( int(i) for i in location_list[1:] )
    location_string = location_list[0]

    # location is a tuple of location_string, None for no container, tuple of location integers
    location = (location_string, None, location_integers)
    # get part_tuple from project, pagenumber, section_name, location
    part_tuple = skilift.part_info(editedprojname, pagenumber, None, location)
    if part_tuple is None:
        raise FailPage("Item to move has not been recognised")

    if len(location_integers) == 1:
        parent_location = (location_string, None, ())
    else:
        parent_integers = list(location_integers[:-1])
        parent_location = (location_string, None, parent_integers)
    items_in_parent = len(part_contents(editedprojname, pagenumber, None, parent_location))
    if location_integers[-1] == (items_in_parent-1):
        # At end of a block, cannot be moved
        raise FailPage("Cannot be moved down")
    new_parent_integers = list(location_integers[:-1])
    new_parent_integers.append(location_integers[-1] + 1)
    new_parent_location = (location_string, None, new_parent_integers)
    new_parent_tuple = skilift.part_info(editedprojname, pagenumber, None, new_parent_location)

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

    call_data['location_string'] = location_string

    # move the item
    try:
        call_data['pchange'] = editpage.move_location(editedprojname, pagenumber, call_data['pchange'], location, (location_string, None, new_location_integers))
    except ServerError as e:
        raise FailPage(message = e.message)

    # and re-draw the table
    domcontents, dragrows, droprows = _page_domcontents(editedprojname, pagenumber, location_string)

    sd_editdom = SectionData("editdom")
    sd_editdom['domtable', 'dragrows']  = dragrows
    sd_editdom['domtable', 'droprows']  = droprows
    sd_editdom['domtable', 'contents']  = domcontents
    pd.update(sd_editdom)



def after_dom_edit(skicall):
    "Called after a dom edit to refresh the correct page"

    call_data = skicall.call_data

    if 'location_string' in call_data:
        if call_data['location_string'] == 'head':
            del call_data['location_string']
            raise GoTo(target = 23321, clear_submitted=True)
        elif call_data['location_string'] == 'body':
            del call_data['location_string']
            raise GoTo(target = 23341, clear_submitted=True)
        elif call_data['location_string'] == 'svg':
            del call_data['location_string']
            raise GoTo(target = 23421, clear_submitted=True)
    elif 'location' in call_data:
        location_string = call_data['location'][0]
        if location_string == 'head':
            raise GoTo(target = 23321, clear_submitted=True)
        elif location_string == 'body':
            raise GoTo(target = 23341, clear_submitted=True)
        elif call_data['location_string'] == 'svg':
            raise GoTo(target = 23421, clear_submitted=True)
    # if nothing matches
    raise FailPage(message = "Cannot return to correct page")


def move_in_page_dom(skicall):
    "Called by domtable to move an item in a page after a drag and drop"

    call_data = skicall.call_data
    pd = call_data['pagedata']

    if "page_number" in call_data:
        pagenumber = call_data["page_number"]
    else:
        raise FailPage(message = "Page number missing")

    if pagenumber is None:
        raise FailPage(message = "Page number missing")

    if ('editdom', 'domtable', 'dragrows') not in call_data:
        raise FailPage(message = "item to drop missing")
    editedprojname = call_data['editedprojname']

    projpartsplit = call_data['editdom', 'domtable', 'dragrows'].split('_', 2)
    if len(projpartsplit) != 3:
        raise FailPage(message = "Invalid move")

    if projpartsplit[0] != editedprojname:
        raise FailPage(message = "Invalid move")

    if projpartsplit[1] != str(pagenumber):
        raise FailPage(message = "Invalid move")

    part_to_move = projpartsplit[2]

    # so part is location_string with string of integers

    # create location which is a tuple or list consisting of three items:
    # a location_string
    # a container integer, in this case always None
    # a tuple or list of location integers
    location_to_move_list = part_to_move.split('-')
    # first item should be a string, rest integers
    if len(location_to_move_list) == 1:
        # no location integers, the location_string top cannot be moved
        return
    else:
        location_to_move_integers = tuple( int(i) for i in location_to_move_list[1:] )
    location_string = location_to_move_list[0]

    # location is a tuple of location_string, None for no container, tuple of location integers
    location_to_move = (location_string, None, location_to_move_integers)
    # get part_tuple from project, pagenumber, section_name, location
    part_to_move_tuple = skilift.part_info(editedprojname, pagenumber, None, location_to_move)
    if part_to_move_tuple is None:
        raise FailPage("Item to move has not been recognised")

    # new location

    target_part = call_data['editdom', 'domtable', 'droprows']

    # so target_part is location_string with string of integers

    # create location which is a tuple or list consisting of three items:
    # a string of location_string
    # a container integer, in this case always None
    # a tuple or list of location integers
    target_location_list = target_part.split('-')
    # first item should be a string, rest integers
    if len(target_location_list) == 1:
        # no location integers
        target_location_integers = ()
    else:
        target_location_integers = tuple( int(i) for i in target_location_list[1:] )

    if location_string != target_location_list[0]:
        raise FailPage("Target location has not been recognised")

    # location is a tuple of location_string, None for no container, tuple of location integers
    target_location = (location_string, None, target_location_integers)
    # get part_tuple from project, pagenumber, section_name, location
    target_part_tuple = skilift.part_info(editedprojname, pagenumber, None, target_location)
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

    call_data['location_string'] = location_string

    # move the item
    try:
        call_data['pchange'] = editpage.move_location(editedprojname, pagenumber, call_data['pchange'], location_to_move, (location_string, None, new_location_integers))
    except ServerError as e:
        raise FailPage(message = e.message)

    # and re-draw the table
    domcontents, dragrows, droprows = _page_domcontents(editedprojname, pagenumber, location_string)

    sd_editdom = SectionData("editdom")
    sd_editdom['domtable', 'dragrows']  = dragrows
    sd_editdom['domtable', 'droprows']  = droprows
    sd_editdom['domtable', 'contents']  = domcontents
    pd.update(sd_editdom)



def edit_page_dom(skicall):
    "Called by domtable to edit an item in a page"

    call_data = skicall.call_data

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

    # create location which is a tuple or list consisting of three items:
    # a location_string
    # a container integer, in this case always None
    # a tuple or list of location integers
    location_list = part.split('-')
    # first item should be a string, rest integers
    if len(location_list) == 1:
        # no location integers, so location_list[0] is the location_string
        # edit the top location_string html part
        call_data['part_tuple'] = skilift.part_info(editedprojname, pagenumber, None, [location_list[0], None, ()])
        raise GoTo(target = 53007, clear_submitted=True)

    location_string = location_list[0]

    location_integers = [ int(i) for i in location_list[1:]]
    part_tuple = skilift.part_info(editedprojname, pagenumber, None, [location_string, None, location_integers])
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
    if part_tuple.part_type == "SectionPlaceHolder":
        # edit the SectionPlaceHolder
        call_data['part_tuple'] = part_tuple
        raise GoTo(target = 55007, clear_submitted=True)

    # note : a sectionplaceholder cannot appear in a section
    raise FailPage("Item to edit has not been recognised")


def cut_page_dom(skicall):
    "Called by domtable to remove an item in a page"

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

    # create location which is a tuple or list consisting of three items:
    # a location_string
    # a container integer, in this case always None
    # a tuple or list of location integers
    location_list = part.split('-')
    # first item should be a string, rest integers
    if len(location_list) == 1:
        # no location integers
        raise FailPage("Item to remove has not been recognised")

    location_integers = tuple( int(i) for i in location_list[1:] )
    location_string = location_list[0]

    # location is a tuple of location_string, None for no container, tuple of location integers
    location = (location_string, None, location_integers)
    # get part_tuple from project, pagenumber, section_name, location
    part_tuple = skilift.part_info(editedprojname, pagenumber, None, location)
    if part_tuple is None:
        raise FailPage("Item to remove has not been recognised")

    # prior to deleting, take a copy
    # get a json string dump of the item outline, however change any Sections to Parts
    itempart, itemdict = fromjson.item_outline(editedprojname, pagenumber, None, location)
    if itempart == 'Section':
        jsonstring = json.dumps(['Part',itemdict], indent=0, separators=(',', ':'))
    else:
        jsonstring = json.dumps([itempart,itemdict], indent=0, separators=(',', ':'))
    pd.localStorage = {'ski_part':jsonstring}

    # remove the item
    try:
        call_data['pchange'] = editpage.del_location(editedprojname, pagenumber, call_data['pchange'], location)
    except ServerError as e:
        raise FailPage(message = e.message)

    # and re-draw the table
    domcontents, dragrows, droprows = _page_domcontents(editedprojname, pagenumber, location_string)

    sd_editdom = SectionData("editdom")
    sd_editdom['domtable', 'dragrows']  = dragrows
    sd_editdom['domtable', 'droprows']  = droprows
    sd_editdom['domtable', 'contents']  = domcontents
    pd.update(sd_editdom)

    # once item is deleted, no info on the item should be
    # left in call_data - this may not be required in future
    if 'location' in call_data:
        del call_data['location']
    if 'part' in call_data:
        del call_data['part']
    if 'part_loc' in call_data:
        del call_data['part_loc']

    call_data['location_string'] = location_string

    call_data['status'] = 'Item copied and then deleted. Use paste to recover or move it.'



def delete_page_dom(skicall):
    "Called by domtable to delete an item in a page"

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

    # create location which is a tuple or list consisting of three items:
    # a location_string
    # a container integer, in this case always None
    # a tuple or list of location integers
    location_list = part.split('-')
    # first item should be a string, rest integers
    if len(location_list) == 1:
        # no location integers
        raise FailPage("Item to delete has not been recognised")

    location_integers = tuple( int(i) for i in location_list[1:] )
    location_string = location_list[0]

    # location is a tuple of location_string, None for no container, tuple of location integers
    location = (location_string, None, location_integers)
    # get part_tuple from project, pagenumber, section_name, location
    part_tuple = skilift.part_info(editedprojname, pagenumber, None, location)
    if part_tuple is None:
        raise FailPage("Item to delete has not been recognised")

    # delete the item
    try:
        call_data['pchange'] = editpage.del_location(editedprojname, pagenumber, call_data['pchange'], location)
    except ServerError as e:
        raise FailPage(message = e.message)

    # and re-draw the table
    domcontents, dragrows, droprows = _page_domcontents(editedprojname, pagenumber, location_string)

    sd_editdom = SectionData("editdom")
    sd_editdom['domtable', 'dragrows']  = dragrows
    sd_editdom['domtable', 'droprows']  = droprows
    sd_editdom['domtable', 'contents']  = domcontents
    pd.update(sd_editdom)

    # once item is deleted, no info on the item should be
    # left in call_data - this may not be required in future
    if 'location' in call_data:
        del call_data['location']
    if 'part' in call_data:
        del call_data['part']
    if 'part_loc' in call_data:
        del call_data['part_loc']

    call_data['location_string'] = location_string

    call_data['status'] = 'Item deleted.'


def _page_domcontents(project, pagenumber, location_string):
    "Return the info for domtable contents, location_string is head', body or svg"

    page_location = (location_string, None, ())
    parttext,partdict = fromjson.item_outline(project, pagenumber, None, page_location)

    # create first row of the table
    if "attribs" in partdict:
        part_tag = '&lt;' + partdict['tag_name'] + ' ... &gt;'
    else:
        part_tag = '&lt;' + partdict['tag_name'] + '&gt;'

    part_brief = html.escape(partdict['brief'])

    if len(part_brief)>40:
        part_brief =  part_brief[:35] + '...'
    if not part_brief:
         part_brief = '-'

    domcontents = [
                   [part_tag, '', False, '' ],
                   [part_brief, '', False, '' ],
                   ['', '', False, '' ],                                                # no up arrow for top line
                   ['', '', False, '' ],                                                # no up_right arrow for top line
                   ['', '', False, '' ],                                                # no down arrow for top line
                   ['', '', False, '' ],                                                # no down_right arrow for top line
                   ['Edit',  'width : 1%;', True, location_string],                     # edit
                   ['Insert','width : 1%;text-align: center;', True, location_string],  # insert
                   ['Copy','width : 1%;text-align: center;', True, location_string],    # copy image for top line
                   ['Paste','width : 1%;text-align: center;', True, location_string],   # paste image for top line
                   ['', '', False, '' ],                                                # no cut image for top line
                   ['', '', False, '' ]                                                 # no delete image for top line
                ]

    # add further items to domcontents
    part_string_list = []

    if 'parts' not in partdict:
        rows = 1
    else:
        rows = _domtree(partdict, location_string, domcontents, part_string_list)
    
    # for every row in the table
    dragrows = [ [ False, '']]
    droprows = [ [ True, location_string ]]

    # send project and page number with dragrow info to avoid items being dragged across web screens showing different pages
    proj_page = project+"_"+str(pagenumber)+"_"

    # for each row (minus 1 as the first row is done)
    for row in range(0, rows-1):
        row_string = proj_page + part_string_list[row]
        dragrows.append( [ True, row_string] )
        droprows.append( [ True, part_string_list[row]] )
    
    return domcontents, dragrows, droprows


def _domtree(partdict, part_loc, contents, part_string_list, rows=1, indent=1):
    "Creates the contents of the domtable"

    # note part_loc = body, head or svg

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



