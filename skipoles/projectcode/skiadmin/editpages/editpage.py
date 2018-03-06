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
#   you may not use this file except in compliance with the License.from ....ski.skiboot import *
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

from ....ski import skiboot, tag, widgets
from ....ski.excepts import ValidateError, FailPage, ServerError, GoTo
from ....skilift import fromjson, part_info, item_info, part_contents, editpage

from .. import utils, css_styles


def _ident_to_str(ident):
    "Returns string ident or label"
    if isinstance(ident, skiboot.Ident):
        return ident.to_comma_str()
    if ident is None:
        return ''
    return str(ident)


def retrieve_page_edit(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Retrieves data for the edit page"

    editedproj = call_data['editedproj']

    # 'edit_page' is from a form, not from session data

    if 'edit_page' in call_data:
        page = skiboot.from_ident(call_data['edit_page'])
        del call_data['edit_page']
    elif 'page_number' in call_data:
        page = skiboot.from_ident((call_data['editedprojname'], call_data['page_number']))
    elif 'page' in call_data:
        page = skiboot.from_ident(call_data['page'])
    else:
        raise FailPage(message = "page missing")

    if (not page) or (page not in editedproj):
        raise FailPage(message = "Invalid page")

    if page.page_type != 'TemplatePage':
        raise FailPage(message = "Invalid page")

    # set page into call_data
    call_data['page'] = page
    call_data['page_number'] = page.ident.num

    # fills in the data for editing page name, brief, parent, etc., 
    utils.retrieve_edit_page(call_data, page_data)

    # page language
    page_data[("setlang","input_text")] = page.lang

    # default error widget
    page_data[("default_e_widg","input_text")] = page.default_error_widget.to_str_tuple()

    # sets last_scroll flag
    page_data[("lastscroll","checked")] = page.last_scroll

    # fills in the backcolor checkbox and value
    if page.show_backcol:
        page_data[("enablebackcolor","checked")] = True
        page_data[('setbackcolor', 'hide')] = False
    else:
        page_data[("enablebackcolor","checked")] = False
        page_data[('setbackcolor', 'hide')] = True
    page_data[('setbackcolor', 'input_text')] = page.backcol

    # fills in the JSON refresh checkbox
    if page.interval and page.interval_target:
        page_data[("refreshcheck","checked")] = True
        page_data[('interval', 'disabled')] = False
        page_data[('interval_target', 'disabled')] = False
        page_data[('interval', 'input_text')] = str(page.interval)
        page_data[('interval_target', 'input_text')] = _ident_to_str(page.interval_target)
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

    editedprojname = call_data['editedprojname']

    if "page_number" in call_data:
        pagenumber = call_data["page_number"]
    else:
        raise FailPage(message = "Page number missing")

    if pagenumber is None:
        raise FailPage(message = "Page number missing")

    page_info = item_info(editedprojname, pagenumber)
    if page_info is None:
        raise FailPage("The page has not been recognised")

    if page_info.item_type != 'TemplatePage':
        raise FailPage(message = "Invalid page")

    page_data[("adminhead","page_head","large_text")] = page_info.name + ' head'

    # fill in the table
    call_data['location_string'] = 'head'
    retrieve_page_dom(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang)


def retrieve_page_dom(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "this call fills in the page dom table"

    editedprojname = call_data['editedprojname']

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
    page_tuple = part_info(editedprojname, pagenumber, None, page_location)
    if page_tuple is None:
        raise FailPage("The page element has not been recognised")

    partdict = fromjson.part_to_OD(editedprojname, pagenumber, None, page_location)

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
    proj_page = editedprojname+"_"+str(pagenumber)+"_"

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

    editedprojname = call_data['editedprojname']

    if "page_number" in call_data:
        pagenumber = call_data["page_number"]
    else:
        raise FailPage(message = "Page number missing")

    if pagenumber is None:
        raise FailPage(message = "Page number missing")

    page_info = item_info(editedprojname, pagenumber)
    if page_info is None:
        raise FailPage("The page has not been recognised")

    if page_info.item_type != 'TemplatePage':
        raise FailPage(message = "Invalid page")

    page_data[("adminhead","page_head","large_text")] = page_info.name + ' body'

    # fill in the table
    call_data['location_string'] = 'body'
    retrieve_page_dom(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang)


def retrieve_svgpage_edit(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Retrieves widget data for the svg edit page"
    editedproj = call_data['editedproj']

    # 'edit_page' is from a form, not from session data

    if 'edit_page' in call_data:
        page = skiboot.from_ident(call_data['edit_page'])
        del call_data['edit_page']
    elif 'page_number' in call_data:
        page = skiboot.from_ident((call_data['editedprojname'], call_data['page_number']))
    elif 'page' in call_data:
        page = skiboot.from_ident(call_data['page'])
    else:
        raise FailPage(message = "page missing")

    if (not page) or (page not in editedproj):
        raise FailPage(message = "Invalid page")

    if page.page_type != 'SVG':
        raise FailPage(message = "Invalid page")

    # set page into call_data
    call_data['page'] = page
    call_data['page_number'] = page.ident.num

    # fills in the data for editing page name, brief, parent, etc., 
    utils.retrieve_edit_page(call_data, page_data)

    page_data['enable_cache:radio_checked'] = page.enable_cache

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


def retrieve_page_svg(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Gets data for the page svg part"

    editedprojname = call_data['editedprojname']

    if "page_number" in call_data:
        pagenumber = call_data["page_number"]
    else:
        raise FailPage(message = "Page number missing")

    if pagenumber is None:
        raise FailPage(message = "Page number missing")

    page_info = item_info(editedprojname, pagenumber)
    if page_info is None:
        raise FailPage("The page has not been recognised")

    if page_info.item_type != 'SVG':
        raise FailPage(message = "Invalid page")

    page_data[("adminhead","page_head","large_text")] = page_info.name + ' svg'

    # fill in the table
    call_data['location_string'] = 'svg'
    retrieve_page_dom(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang)


def set_html_lang(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Sets page background colour in the html tag"
    editedproj = call_data['editedproj']

    if 'page' in call_data:
        if call_data['page'].page_type == 'TemplatePage':
            # page given from session data
            page = call_data['page']
        else:
            raise FailPage(message = "Invalid page")
        if not page in editedproj:
            raise FailPage(message = "Invalid page")
    else:
        raise FailPage(message = "page missing")
    if 'setlang' not in call_data:
        raise FailPage(message = "Invalid language")
    page.lang = call_data['setlang']
    # save the page
    utils.save(call_data, page=page, widget_name="setlang")
    call_data['status'] = "Page lang set to %s" % call_data['setlang']


def enable_backcolour(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    """Enables background colour in HTML tag"""

    editedproj = call_data['editedproj']

    if 'page' in call_data:
        if call_data['page'].page_type == 'TemplatePage':
            # page given from session data
            page = call_data['page']
        else:
            raise FailPage(message = "Invalid page")
        if not page in editedproj:
            raise FailPage(message = "Invalid page")
    else:
        raise FailPage(message = "page missing")

    if (("enablebackcolor","checkbox") in call_data) and call_data["enablebackcolor","checkbox"]:
        page.show_backcol = True
        result = "Background colour %s set in HTML tag" % page.backcol
    else:
        page.show_backcol = False
        result = "Background colour removed from HTML tag"

    try:
        # save the altered page
        editedproj.save_page(page)
    except ServerError as e:
        raise FailPage(message=e.message)
    call_data['status'] = result


def set_backcolour(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    """Sets the background colour in the HTML tag"""

    editedproj = call_data['editedproj']

    if 'page' in call_data:
        if call_data['page'].page_type == 'TemplatePage':
            # page given from session data
            page = call_data['page']
        else:
            raise FailPage(message = "Invalid page")
        if not page in editedproj:
            raise FailPage(message = "Invalid page")
    else:
        raise FailPage(message = "page missing")

    if page.show_backcol == False:
        raise FailPage(message = "Backgound colour in HTML tag has not been enabled")

    if (('setbackcolor','input_text') in call_data) and call_data['setbackcolor','input_text']:
        page.backcol = call_data['setbackcolor','input_text']
    else:
        raise FailPage(message = "Background colour to set is missing")

    try:
        # save the altered page
        editedproj.save_page(page)
    except ServerError as e:
        raise FailPage(message=e.message)
    call_data['status'] = 'HTML tag background color set to %s' % page.backcol



def set_last_scroll(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Sets page last_scroll flag"

    editedproj = call_data['editedproj']

    if 'page' in call_data:
        if call_data['page'].page_type == 'TemplatePage':
            # page given from session data
            page = call_data['page']
        else:
            raise FailPage(message = "Invalid page")
        if not page in editedproj:
            raise FailPage(message = "Invalid page")
    else:
        raise FailPage(message = "page missing")

    if (('lastscroll','checkbox') in call_data) and (call_data['lastscroll','checkbox'] == 'checked'):
        # enable the last_scroll flag
        page.last_scroll = True
        text = 'Page will be displayed at the last scroll position'
    else:
        # disable the last_scroll flag
        page.last_scroll = False
        text = 'Page will not display at previous scroll position'

    try:
        # save the altered page
        editedproj.save_page(page)
    except ServerError as e:
        raise FailPage(message=e.message)
    call_data['status'] = text


def submit_refresh(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Sets JSON refresh facility"

    editedproj = call_data['editedproj']

    if 'page' in call_data:
        if call_data['page'].page_type == 'TemplatePage':
            # page given from session data
            page = call_data['page']
        else:
            raise FailPage(message = "Invalid page")
        if not page in editedproj:
            raise FailPage(message = "Invalid page")
    else:
        raise FailPage(message = "page missing")

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
            interval_target = skiboot.make_ident_or_label(call_data['interval_target', 'input_text'], proj_ident=editedproj.proj_ident)
    except:
        raise FailPage(message="Error setting JSON refresh")
    # set page attributes
    if (interval == 0) or (not interval_target):
        text = 'JSON refresh facility disabled'
        page.interval = 0
        page.interval_target = None
    else:
        text = 'JSON refresh facility enabled'
        page.interval = interval
        # if interval target is an ident of this project, only store an integer
        if isinstance(interval_target, skiboot.Ident):
            if interval_target.proj == editedproj.proj_ident:
                page.interval_target = interval_target.num
            else:
                # ident is another project, put the full ident
                page.interval_target = interval_target.to_comma_str()
        else:
            page.interval_target = interval_target

    # save the page
    utils.save(call_data, page=page)
    call_data['status'] = text


def submit_default_error_widget(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Sets page default_error_widget"

    editedproj = call_data['editedproj']

    if 'page' in call_data:
        if call_data['page'].page_type == 'TemplatePage':
            # page given from session data
            page = call_data['page']
        else:
            raise FailPage(message = "Invalid page")
        if not page in editedproj:
            raise FailPage(message = "Invalid page")
    else:
        raise FailPage(message = "page missing")

    if ('e_widg' not in call_data) or (not call_data['e_widg']):
        raise FailPage(message="Error setting default error widget")
    page.default_error_widget = call_data['e_widg']
    # save the page
    utils.save(call_data, page=page)
    call_data['status'] = "default error widget set"


def submit_cache(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Sets cache true or false"
    # the page to have a new mimetype should be given by session data
    if 'page' not in call_data:
        raise FailPage(message = "page missing")
    page = call_data['page']
    if page.page_type != 'SVG':
        raise ValidateError("Invalid page type")
    if not 'cache' in call_data:
        raise FailPage(message="No cache instruction given", widget="cache_submit")
    # Set the page cache
    if call_data['cache'] == 'True':
        page.enable_cache = True
        message = "Cache Enabled"
    else:
        page.enable_cache = False
        message = "Cache Disabled"
    # save the altered page in the database
    utils.save(call_data, page=page, widget_name='cache_submit')
    call_data['status'] = message


################## JSON PAGE #############################


def retrieve_edit_jsonpage(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Retrieves widget data for the edit json page"
    editedproj = call_data['editedproj']

    # 'edit_page' is from a form, not from session data

    if 'edit_page' in call_data:
        page = skiboot.from_ident(call_data['edit_page'])
        del call_data['edit_page']
    elif 'page_number' in call_data:
        page = skiboot.from_ident((call_data['editedprojname'], call_data['page_number']))
    elif 'page' in call_data:
        page = skiboot.from_ident(call_data['page'])
    else:
        raise FailPage(message = "page missing")

    if (not page) or (page not in editedproj):
        raise FailPage(message = "Invalid page")

    if page.page_type != 'JSON':
        raise FailPage(message = "Invalid page")

    # set page into call_data
    call_data['page'] = page
    call_data['page_number'] = page.ident.num

    # fills in the data for editing page name, brief, parent, etc., 
    utils.retrieve_edit_page(call_data, page_data)

    page_data['enable_cache:radio_checked'] = page.enable_cache

    if page.content:
        # If page has contents, show the table of widgfields, values
        contents = []
        for widgfield,value in page.content.items():
            wf = skiboot.make_widgfield(widgfield)
            if not wf:
                continue
            wfstrtuple = wf.to_str_tuple()
            if value is True:
                contents.append([wfstrtuple,'True',widgfield])
            elif value is False:
                contents.append([wfstrtuple,'False',widgfield])
            else:
                contents.append([wfstrtuple,value,widgfield])
        if contents:
            page_data['field_values_list','show'] = True
            page_data['field_values_list','contents'] = contents
        else:
            page_data['field_values_list','show'] = False
    else:
        page_data['field_values_list','show'] = False


def set_json_cache(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Sets cache true or false"
    if 'page' not in call_data:
        raise FailPage(message = "page missing")
    page = call_data['page']
    if page.page_type != 'JSON':
        raise FailPage("Invalid page type")
    if not ('enable_cache', 'radio_checked') in call_data:
        raise FailPage(message="No cache instruction given", widget="cache_submit")
    # Set the page cache
    if call_data[('enable_cache', 'radio_checked')] == 'True':
        page.enable_cache = True
        message = "Cache Enabled"
    else:
        page.enable_cache = False
        message = "Cache Disabled"
    # save the altered page in the database
    utils.save(call_data, page=page, widget_name='cache_submit')
    call_data['status'] = message


def remove_json_widgfield(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Removes widgfield from JSON page"
    if 'page' not in call_data:
        raise FailPage(message = "page missing")
    page = call_data['page']
    if page.page_type != 'JSON':
        raise FailPage("Invalid page type")
    if not ('field_values_list','contents') in call_data:
        raise FailPage(message="No widgfield given")
    widgfield = call_data['field_values_list','contents']
    if widgfield in page.content:
        page.del_widgfield(widgfield)
        # save the altered page in the database
        utils.save(call_data, page=page)
        call_data['status'] = "Widgfield removed"
    else:
        raise FailPage(message="Widgfield not recognised")

def add_json_widgfield(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Adds a widgfield to JSON page"
    if 'page' not in call_data:
        raise FailPage(message = "page missing")
    page = call_data['page']
    if page.page_type != 'JSON':
        raise FailPage("Invalid page type")
    if not ('jsonwidgfield', 'input_text') in call_data:
        raise FailPage(message="No widgfield given")
    widgfield = call_data[ 'jsonwidgfield', 'input_text']
    if call_data['jsontrue', 'button_text'] == 'True':
        value = True
    elif call_data['jsonfalse', 'button_text'] == 'False':
        value = False
    elif call_data['jsontext', 'input_text']:
        value = call_data['jsontext', 'input_text']
    else:
        value = ''
    page.add_widgfield(widgfield, value)
    # save the altered page in the database
    utils.save(call_data, page=page)
    call_data['status'] = "Widgfield added"



def downloadpage(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Gets template or SVG page, and returns a json dictionary, this will be sent as an octet file to be downloaded"
    if 'page' not in call_data:
        raise FailPage(message = "page missing")
    page = call_data['page']
    if (page.page_type != 'TemplatePage') and (page.page_type != 'SVG'):
        raise FailPage("Invalid page type")
    project = call_data['editedproj']
    jsonstring =  fromjson.page_to_json(project.proj_ident, page.ident.num, indent=4)
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
    part_tuple = part_info(editedprojname, pagenumber, None, location)
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
        editpage.move_location(editedprojname, pagenumber, location, (location_string, None, new_location_integers))
    except ServerError as e:
        raise FailPage(message = e.message)

    # page has changed, hopefully, in due course, this line will not be needed
    call_data['page'] = skiboot.from_ident(pagenumber, proj_ident=editedprojname)


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
    part_tuple = part_info(editedprojname, pagenumber, None, location)
    if part_tuple is None:
        raise FailPage("Item to move has not been recognised")

    if location_integers[-1] == 0:
        # at top of a part, cannot be moved
        raise FailPage("Cannot be moved up")
    new_parent_integers = list(location_integers[:-1])
    new_parent_integers.append(location_integers[-1] - 1)
    new_parent_location = (location_string, None, new_parent_integers)

    new_parent_tuple = part_info(editedprojname, pagenumber, None, new_parent_location)

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
        editpage.move_location(editedprojname, pagenumber, location, (location_string, None, new_location_integers))
    except ServerError as e:
        raise FailPage(message = e.message)

    # page has changed, hopefully, in due course, this line will not be needed
    call_data['page'] = skiboot.from_ident(pagenumber, proj_ident=editedprojname)


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
    part_tuple = part_info(editedprojname, pagenumber, None, location)
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
        editpage.move_location(editedprojname, pagenumber, location, (location_string, None, new_location_integers))
    except ServerError as e:
        raise FailPage(message = e.message)

    # page has changed, hopefully, in due course, this line will not be needed
    call_data['page'] = skiboot.from_ident(pagenumber, proj_ident=editedprojname)


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
    part_tuple = part_info(editedprojname, pagenumber, None, location)
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
    new_parent_tuple = part_info(editedprojname, pagenumber, None, new_parent_location)

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
        editpage.move_location(editedprojname, pagenumber, location, (location_string, None, new_location_integers))
    except ServerError as e:
        raise FailPage(message = e.message)

    # page has changed, hopefully, in due course, this line will not be needed
    call_data['page'] = skiboot.from_ident(pagenumber, proj_ident=editedprojname)



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
    part_to_move_tuple = part_info(editedprojname, pagenumber, None, location_to_move)
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
    target_part_tuple = part_info(editedprojname, pagenumber, None, target_location)
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
        editpage.move_location(editedprojname, pagenumber, location_to_move, (location_string, None, new_location_integers))
    except ServerError as e:
        raise FailPage(message = e.message)

    # page has changed, hopefully, in due course, this line will not be needed
    call_data['page'] = skiboot.from_ident(pagenumber, proj_ident=editedprojname)


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
        call_data['part'] = part
        raise GoTo(target = 53007, clear_submitted=True)

    location_string = location_list[0]

    location_integers = [ int(i) for i in location_list[1:]]
    part_tuple = part_info(editedprojname, pagenumber, None, [location_string, None, location_integers])
    if part_tuple is None:
        raise FailPage("Item to edit has not been recognised")

    if part_tuple.name:
        # item to edit is a widget
        call_data['part_tuple'] = part_tuple
        raise GoTo(target = 54006, clear_submitted=True)
    if part_tuple.part_type == "Part":
        # edit the html part
        call_data['part'] = part                 ################ note, in future pass part_tuple rather than part
        raise GoTo(target = 53007, clear_submitted=True)
    if part_tuple.part_type == "ClosedPart":
        # edit the html closed part
        call_data['part'] = part                 ################ note, in future pass part_tuple rather than part
        raise GoTo(target = 53007, clear_submitted=True)
    if part_tuple.part_type == "HTMLSymbol":
        # edit the symbol
        call_data['part'] = part                 ################ note, in future pass part_tuple rather than part
        raise GoTo(target = 51107, clear_submitted=True)
    if part_tuple.part_type == "str":
        # edit the text
        call_data['part'] = part                 ################ note, in future pass part_tuple rather than part
        raise GoTo(target = 51017, clear_submitted=True)
    if part_tuple.part_type == "TextBlock":
        # edit the TextBlock
        call_data['part'] = part                 ################ note, in future pass part_tuple rather than part
        raise GoTo(target = 52017, clear_submitted=True)
    if part_tuple.part_type == "Comment":
        # edit the Comment
        call_data['part'] = part                 ################ note, in future pass part_tuple rather than part
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
    part_tuple = part_info(editedprojname, pagenumber, None, location)
    if part_tuple is None:
        raise FailPage("Item to append to has not been recognised")
    # goto either the install or append page

    call_data['part'] = part                 ################ note, in future pass part_tuple rather than part
    call_data['location'] = location         ########## also part_tuple should replace location

    # navigator boxes
    if location_string == 'head':
        boxes = [['page_head', "Head", True, '']]    # label to 3320
    elif location_string == 'body':
        boxes = [['page_body', "Body", True, '']]    # label to 3340
    elif location_string == 'svg':
        boxes = [['page_svg', "SVG", True, '']]    # label to 3420
    else:
        raise FailPage("Item to add to has not been recognised")

    if 'extend_nav_buttons' in call_data:
        call_data['extend_nav_buttons'].extend(boxes)
    else:
        call_data['extend_nav_buttons'] = boxes

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
    part_tuple = part_info(editedprojname, pagenumber, None, location)
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
        editpage.del_location(editedprojname, pagenumber, location)
    except ServerError as e:
        raise FailPage(message = e.message)

    # page has changed, hopefully, in due course, this line will not be needed
    call_data['page'] = skiboot.from_ident(pagenumber, proj_ident=editedprojname)




