####### SKIPOLE WEB FRAMEWORK #######
#
# editcss.py  - css editing functions
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

"Functions implementing css editing"


import collections

from ....ski.excepts import ValidateError, FailPage, ServerError

from .... import skilift
from ....skilift import editpage

from .. import utils


def retrieve_edit_csspage(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Retrieves widget data for the edit css page"

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
        if pageinfo.item_type != 'CSS':
            raise FailPage(message = "Invalid page")
        selectors = list(editpage.css_style(project, pagenumber).keys())
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
    # create the contents for the selectortable
    contents = []

    if selectors:
        max_selector_index = len(selectors) - 1
        for index,selector in enumerate(selectors):
            if index:
                up = True
            else:
                # first item (index zero) has no up button
                up = False
            if index < max_selector_index:
                down = True
            else:
                # last item has no down button
                down = False 
            contents.append([selector, selector, selector, selector, selector, True, up, down, True])
        page_data["selectortable:contents"] = contents
    else:
        page_data["selectortable:show"] = False

    page_data['enable_cache:radio_checked'] = pageinfo.enable_cache


def retrieve_edit_selector(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Retrieves widget data for the edit selector page"

    project = call_data['editedprojname']
    
    if 'page_number' in call_data:
        pagenumber = call_data['page_number']
        str_pagenumber = str(pagenumber)
    else:
        raise FailPage(message = "page missing")

    if not pagenumber:
        raise FailPage(message = "Invalid page")

    if 'edit_selector' not in call_data:
        raise FailPage(message="No selector given")

    try:
        pageinfo = skilift.page_info(project, pagenumber)
        if pageinfo.item_type != 'CSS':
            raise FailPage(message = "Invalid page")
        edit_selector = call_data['edit_selector']
        property_string = editpage.css_selector_properties(project, pagenumber, edit_selector)
    except ServerError as e:
        raise FailPage(message = e.message)

    call_data['extend_nav_buttons'] = [['back_to_css_page', 'CSS Page', True, '']]    # label to 8003

    if 'status' in call_data:
        status_text = call_data['status']
    else:
        status_text = 'Edit selector : %s' % (edit_selector,)

    page_data.update({("adminhead","page_head","large_text"):"Edit CSS page : %s" % (pageinfo.name,),
                      ("adminhead","page_head","small_text"):status_text,
                      ('selectorname','para_text'):"Selector : %s" % (edit_selector,),
                      ('p_ident','page_ident'):(project,str_pagenumber),
                      ('properties','hidden_field1'):edit_selector,
                      ('properties','input_text'):property_string })



def retrieve_print_csspage(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Retrieves widget data for the print css page"
    # the page to be printed should be given by session data
    if 'page' not in call_data:
        raise FailPage(message = "page missing")
    page = call_data['page']
    if page.page_type != "CSS":
        raise ValidateError("Invalid page type")
    page_data['page_details:para_text'] = "/**************************\n\nIdent:%s\nPath:%s\n%s" % (page.ident.to_comma_str(), page.url, page.brief)
    page_data['page_contents:para_text'] = str(page)


def submit_new_selector(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Sets new selector"
    # the page to have a selector added should be given by session data
    if 'page' not in call_data:
        raise FailPage(message = "page missing")
    page = call_data['page']
    if page.page_type != "CSS":
        raise ValidateError("Invalid page type")
    if not 'new_selector' in call_data:
        raise FailPage(message="No new selector given", widget="add")
    new_selector = call_data['new_selector']
    if not new_selector:
        raise FailPage(message="No selector given", widget="add")
    style = page.style
    if new_selector in style:
        raise FailPage(message="Selector already exists", widget="add")
    # Set the selector
    style[new_selector] = []
    page.style = style
    # save the altered page in the database
    utils.save(call_data, page=page, widget_name='add')
    page_data["adminhead","page_head","small_text"] = 'Page selector set'


def submit_delete_selector(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Deletes selector"
    # the page to have a selector deleted should be given by session data
    if 'page' not in call_data:
        raise FailPage(message = "page missing")
    page = call_data['page']
    if page.page_type != "CSS":
        raise ValidateError("Invalid page type")
    if not 'remove_selector' in call_data:
        raise FailPage(message="No selector to delete given", widget="selectortable")
    remove_selector = call_data['remove_selector']
    if not remove_selector:
        raise FailPage(message="No selector given", widget="selectortable")
    style = page.style
    if remove_selector not in style:
        raise FailPage(message="Selector to remove is not present", widget="selectortable")
    # Remove the selector
    del style[remove_selector]
    page.style = style
    # save the altered page in the database
    utils.save(call_data, page=page, widget_name='selectortable')
    page_data["adminhead","page_head","small_text"] = 'Selector deleted'


def submit_selector_properties(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Sets the selector properties"
    # the page to have a selector edited should be given by session data
    if 'page' not in call_data:
        raise FailPage(message = "page missing")
    page = call_data['page']
    if page.page_type != "CSS":
        raise ValidateError("Invalid page type")

    if not 'edit_selector' in call_data:
        raise FailPage(message="No selector to edit given")
    edit_selector = call_data['edit_selector']
    if not 'properties' in call_data:
        raise FailPage(message="No properties to set given")
    property_string = call_data['properties']

    property_list = property_string.split(';')

    properties = []
    for item in property_list:
        if not item:
            continue
        if ':' not in item:
            continue
        pair = item.split(':')
        if len(pair) != 2:
            raise FailPage(message="Invalid properties", widget='properties')
        a = pair[0].strip()
        b = pair[1].strip()
        #if (not a) or (not b):
        #   raise FailPage(message="Invalid properties", widget='properties')
        properties.append([a,b])
    if not properties:
        raise FailPage(message="Invalid properties", widget='properties')
    style = page.style
    style[edit_selector] = properties
    page.style = style
    # save the altered page in the database
    utils.save(call_data, page=page, widget_name='properties')
    call_data['status'] = 'Properties set'

        

def move_selector_up(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Moves selector upwards"
    # the page to have a selector moved should be given by session data
    if 'page' not in call_data:
        raise FailPage(message = "page missing")
    page = call_data['page']
    if page.page_type != "CSS":
        raise ValidateError("Invalid page type")
    if not 'up_selector' in call_data:
        raise FailPage(message="No selector to move up given", widget="selectortable")
    up_selector = call_data['up_selector']
    if not up_selector:
        raise FailPage(message="No selector given", widget="selectortable")
    style = page.style
    if up_selector not in style:
        raise FailPage(message="Selector to move up is not present", widget="selectortable")
    # Move the selector up
    selector_list = page.selector_list()
    idx = selector_list.index(up_selector)
    if not idx:
        # idx cannot be zero
        raise FailPage(message="Selector already at top", widget="selectortable")
    selector_list[idx-1], selector_list[idx] = selector_list[idx], selector_list[idx-1]
    new_style = collections.OrderedDict([(selector,style[selector]) for selector in selector_list])
    page.style = new_style
    # save the altered page in the database
    utils.save(call_data, page=page, widget_name='selectortable')
    page_data["adminhead","page_head","small_text"] = 'Selector moved'


def move_selector_down(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Moves selector downwardswards"
    # the page to have a selector moved should be given by session data
    if 'page' not in call_data:
        raise FailPage(message = "page missing")
    page = call_data['page']
    if page.page_type != "CSS":
        raise ValidateError("Invalid page type")
    if not 'down_selector' in call_data:
        raise FailPage(message="No selector to move down given", widget="selectortable")
    down_selector = call_data['down_selector']
    if not down_selector:
        raise FailPage(message="No selector given", widget="selectortable")
    style = page.style
    if down_selector not in style:
        raise FailPage(message="Selector to move down is not present", widget="selectortable")
    # Move the selector down
    selector_list = page.selector_list()
    idx = selector_list.index(down_selector)
    if idx == len(selector_list) -1:
        # idx cannot be last element
        raise FailPage(message="Selector already at end", widget="selectortable")
    selector_list[idx+1], selector_list[idx] = selector_list[idx], selector_list[idx+1]
    new_style = collections.OrderedDict([(selector,style[selector]) for selector in selector_list])
    page.style = new_style
    # save the altered page in the database
    utils.save(call_data, page=page, widget_name='selectortable')
    page_data["adminhead","page_head","small_text"] = 'Selector moved'


def submit_cache(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Sets cache true or false"
    if 'page' not in call_data:
        raise FailPage(message = "page missing")
    page = call_data['page']
    if page.page_type != "CSS":
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
