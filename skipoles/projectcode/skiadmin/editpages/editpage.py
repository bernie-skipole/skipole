####### SKIPOLE WEB FRAMEWORK #######
#
# editpage.py  - page editing functions
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

"Functions implementing admin page editing"

import html

from ....ski.excepts import ValidateError, FailPage, ServerError, GoTo

from .... import skilift
from ....skilift import fromjson, part_contents, editpage

from .. import utils


def retrieve_page_edit(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Retrieves data for the edit page"

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

        # fills in the data for editing page name, brief, parent, etc., 
        page_data[("adminhead","page_head","large_text")] = pageinfo.name
        page_data[('page_edit','p_ident','page_ident')] = (project,str_pagenumber)
        page_data[('page_edit','p_name','page_ident')] = (project,str_pagenumber)
        page_data[('page_edit','p_description','page_ident')] = (project,str_pagenumber)
        page_data[('page_edit','p_rename','input_text')] = pageinfo.name
        page_data[('page_edit','p_parent','input_text')] = "%s,%s" % (project, pageinfo.parentfolder_number)
        page_data[('page_edit','p_brief','input_text')] = pageinfo.brief

        pageOD = fromjson.page_to_OD(project, pagenumber)
    except ServerError as e:
        raise FailPage(message=e.message)

    if "TemplatePage" in pageOD:
        pagedict = pageOD["TemplatePage"]
    else:
        raise FailPage(message="This page not recognised as a Template page.")

    # page language
    page_data[("setlang","input_text")] = pagedict["lang"]

    # default error widget
    dew = pagedict["default_error_widget"]
    if dew[0]:
        page_data[("default_e_widg","input_text")] = dew[0] + ',' + dew[1]
    elif dew[1]:
        page_data[("default_e_widg","input_text")] = dew[1]

    # sets last_scroll flag
    page_data[("lastscroll","checked")] = pagedict["last_scroll"]

    # fills in the backcolor checkbox and value
    if pagedict["show_backcol"]:
        page_data[("enablebackcolor","checked")] = True
        page_data[('setbackcolor', 'hide')] = False
    else:
        page_data[("enablebackcolor","checked")] = False
        page_data[('setbackcolor', 'hide')] = True
    page_data[('setbackcolor', 'input_text')] = pagedict["backcol"]


    # fills in the JSON refresh checkbox
    if pagedict["interval"] and pagedict["interval_target"]:
        if pagedict["interval_target"] is None:
            interval_target = ''
        else:
            interval_target = str(pagedict["interval_target"])
        page_data[("refreshcheck","checked")] = True
        page_data[('interval', 'disabled')] = False
        page_data[('interval_target', 'disabled')] = False
        page_data[('interval', 'input_text')] = str(pagedict["interval"])
        page_data[('interval_target', 'input_text')] = interval_target
    else:
        page_data[("refreshcheck","checked")] = False
        page_data[('interval', 'disabled')] = True
        page_data[('interval_target', 'disabled')] = True
        page_data[('interval', 'input_text')] = '0'
        page_data[('interval_target', 'input_text')] = ''

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



def retrieve_page_head(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Gets data for the page head"

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

    page_data[("adminhead","page_head","large_text")] = pageinfo.name + ' head'

    # fill in the table
    call_data['location_string'] = 'head'
    retrieve_page_dom(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang)


def retrieve_page_dom(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "this call fills in the page dom table"

    project = call_data['editedprojname']

    if "page_number" in call_data:
        pagenumber = call_data["page_number"]
    else:
        raise FailPage(message = "Page number missing")

    if pagenumber is None:
        raise FailPage(message = "Page number missing")

    location_string = call_data['location_string']

    # page location is a tuple of either 'body' 'head' or 'svg', None for no container, () tuple of location integers
    page_location = (location_string, None, ())
    # get page_tuple from project, pagenumber, section_name, page_location
    try:
        page_tuple = skilift.part_info(project, pagenumber, None, page_location)
        partdict = fromjson.part_to_OD(project, pagenumber, None, page_location)
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
                   ['', '', False, '' ],                                                # no remove image for top line
                ]

    # add further items to domcontents
    part_string_list = []

    if 'parts' not in partdict:
        rows = 1
    else:
        rows = utils.domtree(partdict, location_string, domcontents, part_string_list)
    
    page_data['editdom', 'domtable', 'contents']  = domcontents

    # for each column: html link, JSON link
    page_data['editdom', 'domtable', 'cols']  =  [    ['',''],                               # tag name, no link
                                                      ['',''],                               # brief, no link
                                                      ['move_up_in_page_dom',3640],          # up arrow
                                                      ['move_up_right_in_page_dom',3650],    # up right
                                                      ['move_down_in_page_dom',3660],        # down
                                                      ['move_down_right_in_page_dom',3670],  # down right
                                                      ['edit_page_dom',''],                  # edit, html only
                                                      ['add_to_page_dom',''],                # insert/append, html only
                                                      ['remove_page_dom',3620]               # remove
                                                   ]
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

    page_data['editdom', 'domtable', 'dragrows']  = dragrows
    page_data['editdom', 'domtable', 'droprows']  = droprows

    page_data['editdom', 'domtable', 'dropident']  = 'move_in_page_dom'

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



def retrieve_page_body(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Gets data for the page body"

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

    page_data[("adminhead","page_head","large_text")] = pageinfo.name + ' body'

    # fill in the table
    call_data['location_string'] = 'body'
    retrieve_page_dom(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang)


def retrieve_svgpage_edit(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Retrieves widget data for the svg edit page"

    if 'page_number' in call_data:
        pagenumber = call_data['page_number']
        str_pagenumber = str(pagenumber)
    else:
        raise FailPage(message = "page missing")

    project = call_data['editedprojname']

    try:
        pageinfo = skilift.page_info(project, pagenumber)
    except ServerError as e:
        raise FailPage(message=e.message)

    if pageinfo.item_type != 'SVG':
        raise FailPage(message = "Invalid page")

    # fills in the data for editing page name, brief, parent, etc., 
    page_data[("adminhead","page_head","large_text")] = pageinfo.name
    page_data[('page_edit','p_ident','page_ident')] = (project,str_pagenumber)
    page_data[('page_edit','p_name','page_ident')] = (project,str_pagenumber)
    page_data[('page_edit','p_description','page_ident')] = (project,str_pagenumber)
    page_data[('page_edit','p_rename','input_text')] = pageinfo.name
    page_data[('page_edit','p_parent','input_text')] = "%s,%s" % (project, pageinfo.parentfolder_number)
    page_data[('page_edit','p_brief','input_text')] = pageinfo.brief
    page_data['enable_cache:radio_checked'] = pageinfo.enable_cache


def retrieve_page_svg(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Gets data for the page svg part"

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
    page_data[("adminhead","page_head","large_text")] = pageinfo.name + ' svg'
    # fill in the table
    call_data['location_string'] = 'svg'
    retrieve_page_dom(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang)


def set_html_lang(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Sets language in the page html tag"
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


def enable_backcolour(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    """Enables background colour in HTML tag"""
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


def set_backcolour(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    """Sets the background colour in the HTML tag"""

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



def set_last_scroll(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Sets page last_scroll flag"

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


def submit_refresh(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Sets JSON refresh facility"

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
    except:
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


def submit_default_error_widget(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Sets page default_error_widget"
    project = call_data['editedprojname']
    pagenumber = call_data['page_number']
    pchange = call_data['pchange']
    if ('e_widg' not in call_data) or (not call_data['e_widg']):
        raise FailPage(message="Error setting default error widget")
    try:
        call_data['pchange'] = editpage.page_default_error_widget(project, pagenumber, pchange, call_data['e_widg'])
    except ServerError as e:
        raise FailPage(message=e.message)
    call_data['status'] = "default error widget set"


def submit_cache(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Sets cache true or false"
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


def retrieve_edit_jsonpage(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Retrieves widget data for the edit json page"

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
    except ServerError as e:
        raise FailPage(message = e.message)

   # fills in the data for editing page name, brief, parent, etc., 
    page_data[("adminhead","page_head","large_text")] = pageinfo.name
    page_data[('page_edit','p_ident','page_ident')] = (project,str_pagenumber)
    page_data[('page_edit','p_name','page_ident')] = (project,str_pagenumber)
    page_data[('page_edit','p_description','page_ident')] = (project,str_pagenumber)
    page_data[('page_edit','p_rename','input_text')] = pageinfo.name
    page_data[('page_edit','p_parent','input_text')] = "%s,%s" % (project, pageinfo.parentfolder_number)
    page_data[('page_edit','p_brief','input_text')] = pageinfo.brief

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
            page_data['field_values_list','show'] = True
            page_data['field_values_list','contents'] = contents
        else:
            page_data['field_values_list','show'] = False
    else:
        page_data['field_values_list','show'] = False

    page_data['enable_cache:radio_checked'] = pageinfo.enable_cache


def set_json_cache(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Sets cache true or false"
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


def remove_json_widgfield(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Removes widgfield from JSON page"
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



def add_json_widgfield(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Adds a widgfield to JSON page"
    project = call_data['editedprojname']
    pagenumber = call_data['page_number']
    pchange = call_data['pchange']
    if not ('jsonwidgfield', 'input_text') in call_data:
        raise FailPage(message="No widgfield given")
    str_widgfield = call_data[ 'jsonwidgfield', 'input_text']
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
    call_data['status'] = "Widgfield added"


def downloadpage(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Gets template or SVG page, and returns a json dictionary, this will be sent as an octet file to be downloaded"

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
    page_data['headers'] = [('content-type', 'application/octet-stream'), ('content-length', str(n))]
    return line_list


def move_up_in_page_dom(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Called by domtable to move an item in a page up"

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


def move_up_right_in_page_dom(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Called by domtable to move an item in a page up and to the right"

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


def move_down_in_page_dom(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Called by domtable to move an item in a page down"

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


def move_down_right_in_page_dom(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Called by domtable to move an item in a page down and to the right"

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



def after_dom_edit(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Called after a dom edit to refresh the correct page"

    if 'location_string' not in call_data:
        raise FailPage("Cannot return to item")
    if call_data['location_string'] == 'head':
        del call_data['location_string']
        raise GoTo(target = 23321, clear_submitted=True)
    if call_data['location_string'] == 'body':
        del call_data['location_string']
        raise GoTo(target = 23341, clear_submitted=True)
    if call_data['location_string'] == 'svg':
        del call_data['location_string']
        raise GoTo(target = 23421, clear_submitted=True)



def move_in_page_dom(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Called by domtable to move an item in a page after a drag and drop"

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



def edit_page_dom(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Called by domtable to edit an item in a page"

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


def add_to_page_dom(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    """Called by domtable to either insert or append an item in a page
       sets page_data to populate the insert or append page and then go to appropriate template page"""

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
    location_list = part.split('-')
    # first item should be a string, rest integers
    if len(location_list) == 1:
        # no location integers, so location_list[0] is the location_string
        location_integers = ()
    else:
        location_integers = tuple( int(i) for i in location_list[1:] )
    location_string = location_list[0]

    # location is a tuple of location_string, None for no container, tuple of location integers
    location = (location_string, None, location_integers)
    # get part_tuple from project, pagenumber, section_name, location
    part_tuple = skilift.part_info(editedprojname, pagenumber, None, location)
    if part_tuple is None:
        raise FailPage("Item to append to has not been recognised")

    # goto either the install or append page, to add an item at this location
    call_data['location'] = location

    # Fill in menu of items, Part items have insert, others have append
    # as this is to be input into a section, a further section is not present in this list


    if part_tuple.part_type == "Part":
        # insert
        page_data[("adminhead","page_head","large_text")] = "Choose an item to insert"
        page_data[("insertlist","links")] = [
                                                ["Insert text", "inserttext", ""],
                                                ["Insert a TextBlock", "insert_textblockref", ""],
                                                ["Insert html symbol", "insertsymbol", ""],
                                                ["Insert comment", "insertcomment", ""],
                                                ["Insert an html element", "part_insert", ""],
                                                ["Insert a Widget", "list_widget_modules", ""],
                                                ["Insert a Section", "placeholder_insert", ""]
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
                                                ["Append a Widget", "list_widget_modules", ""],
                                                ["Append a Section", "placeholder_insert", ""]
                                            ]
        raise GoTo(target = '23509', clear_submitted=True)


def remove_page_dom(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Called by domtable to remove an item in a page"

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

    # once item is deleted, no info on the item should be
    # left in call_data - this may not be required in future
    if 'location' in call_data:
        del call_data['location']
    if 'part' in call_data:
        del call_data['part']
    if 'part_loc' in call_data:
        del call_data['part_loc']

    call_data['location_string'] = location_string

    # remove the item
    try:
        call_data['pchange'] = editpage.del_location(editedprojname, pagenumber, call_data['pchange'], location)
    except ServerError as e:
        raise FailPage(message = e.message)






