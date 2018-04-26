####### SKIPOLE WEB FRAMEWORK #######
#
# operations.py  - site wide operations
#
# This file is part of the Skipole web framework
#
# Date : 20170617
#
# Author : Bernard Czenkusz
# Email  : bernie@skipole.co.uk
#
#
#   Copyright 2017 Bernard Czenkusz
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

import re
# a search for anything none-alphanumeric and not an underscore
_AN = re.compile('[^\w_]')

from ....skilift import fromjson, off_piste
from ....ski.excepts import FailPage, ValidateError, ServerError, GoTo

from .. import css_styles



def retrieve_operations_data(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Retrieves field data for operations page"

    editedprojname = call_data['editedprojname']

    # project background color
    backcol = fromjson.get_defaults(editedprojname, key="backcol")
    if backcol:
        page_data['htmlbackcol','input_text'] = backcol

    # project body class
    body_class = fromjson.get_defaults(editedprojname, key="body_class")
    if body_class:
        page_data['bodyclass','input_text'] = body_class

    # get default css links for widget css_defaults
    css_list = fromjson.get_defaults(editedprojname, key='css_links')

    if css_list:
        contents = []
        for label in css_list:
            row = [label,
                   label, label, label, '',
                   True,
                   True,
                   True,
                   False]
            contents.append(row)
        # remove up arrow in row 0
        contents[0][1] = ''
        contents[0][5] = False
        # remove down arrow in row -1
        contents[-1][2] = ''
        contents[-1][6] = False
        page_data[('css_links', 'contents')] = contents


  #      contents: col 0 is the text to place in the first column,
  #                  col 1, 2, 3, 4 are the get field contents of links 1,2,3 and 4
  #                  col 5 - True if the first button and link is to be shown, False if not
  #                  col 6 - True if the second button and link is to be shown, False if not
  #                  col 7 - True if the third button and link is to be shown, False if not
  #                  col 8 - True if the fourth button and link is to be shown, False if not


    # get default js links for widget js_defaults
    js_list = fromjson.get_defaults(editedprojname, key='js_links')

    if js_list:
        contents = []
        for label in js_list:
            row = [label,
                   label, label, label, '',
                   True,
                   True,
                   True,
                   False]
            contents.append(row)
        # remove up arrow in row 0
        contents[0][1] = ''
        contents[0][5] = False
        # remove down arrow in row -1
        contents[-1][2] = ''
        contents[-1][6] = False
        page_data[('js_links', 'contents')] = contents


def set_widgets_css(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "sets default css classes into widgets"
    editedprojname = call_data['editedprojname']
    off_piste.set_widget_css_to_default(editedprojname)
    call_data['status'] = 'Widget CSS classes set'


def submit_project_color(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "set project default background color"
    try:
        backcol = call_data['htmlbackcol','input_text']
    except:
        raise ValidateError(message='Invalid call')
    try:
        editedprojname = call_data['editedprojname']
        # set background color in existing pages
        off_piste.set_backcol_in_pages(editedprojname, backcol)
        # set the project colour for new pages
        fromjson.set_defaults(editedprojname, 'backcol', backcol)
    except (ValidateError, ServerError) as e:
        raise FailPage(message = e.message, widget = "htmlbackcol")
    call_data['status'] = 'Project background colour set'


def set_bodyclass_in_pages(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "sets css class into page body tags"
    try:
        bodyclass = call_data['bodyclass','input_text']
    except:
        raise ValidateError(message='Invalid call')
    # set body class in all project template pages
    editedprojname = call_data['editedprojname']
    off_piste.set_bodyclass_in_pages(editedprojname, bodyclass)
    # set the body class for new pages
    fromjson.set_defaults(editedprojname, 'body_class', bodyclass)
    if bodyclass:
        call_data['status'] = 'CSS class set in body tags'
    else:
        call_data['status'] = 'CSS class removed from body tags'



def insert_css_link(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "inserts css link into page head before element with given brief"
    try:
        brief = call_data['insert_css_link_brief','input_text']
        label = call_data['insert_css_link_label','input_text']
    except:
        raise ValidateError(message='Invalid call')
    if not brief:
        raise ValidateError(message='A brief must be given')
    if not label:
        raise ValidateError(message='A label must be given')
    # add CSS link in all project template pages
    editedprojname = call_data['editedprojname']
    off_piste.insert_css_link(editedprojname, label, brief)
    call_data['status'] = 'CSS links inserted'



def set_css_class(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "sets css class into elements with given brief"
    try:
        brief = call_data['set_css_class_brief','input_text']
        cssclass = call_data['set_css_class_string','input_text']
    except:
        raise ValidateError(message='Invalid call')
    if not brief:
        raise ValidateError(message='A brief must be given')
    editedprojname = call_data['editedprojname']
    count =  off_piste.set_css_class(editedprojname, brief, cssclass)
    if count:
        call_data['status'] = 'CSS class set, %d changes.' % count
    else:
        call_data['status'] = 'No changes, brief not found.'


def add_default_css(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Add a label to the default css list"

    editedprojname = call_data['editedprojname']

    # check label is valid
    if not "new_css_label" in call_data:
        raise FailPage(message = "label missing")

    label = call_data["new_css_label"]
    if not label:
        raise FailPage(message = "label missing")

    if _AN.search(label):
        raise FailPage(message = "The label can only contain A-Z, a-z, 0-9 and the underscore character.")

    if '_' in label:
        labelparts = label.split('_')
        if labelparts[0].isalnum() and labelparts[1].isdigit():
            raise FailPage(message = "Invalid label (Danger of confusion with a page ident).")

    if label.isdigit():
        raise FailPage(message = "Invalid label (Danger of confusion with a page ident).")

    css_list = fromjson.get_defaults(editedprojname, key='css_links')
    if label in css_list:
        raise FailPage(message = "This label is already in the list")
    css_list.append(label)
    try:
        fromjson.set_defaults(editedprojname, key='css_links', value=css_list)
    except e:
        raise FailPage(message = "Unable to save defaults.json")


def css_remove(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Removes css default label"
    editedprojname = call_data['editedprojname']
    if 'css_label' in call_data:
        label = call_data['css_label']
        d_list = fromjson.get_defaults(editedprojname, 'css_links')
        if not label in d_list:
            return
        index = d_list.index(label)
        # remove
        del d_list[index]
        # save d_list
        try:
            fromjson.set_defaults(editedprojname, key='css_links', value=d_list)
        except e:
            raise FailPage(message = "Unable to save defaults.json")


def css_up(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Moves css default label up"
    editedprojname = call_data['editedprojname']
    if 'css_label' in call_data:
        label = call_data['css_label']
        d_list = fromjson.get_defaults(editedprojname, 'css_links')
        if not label in d_list:
            return
        index = d_list.index(label)
        # move up
        if not index:
            return
        d_list.insert(index-1, d_list.pop(index))
        # save d_list
        try:
            fromjson.set_defaults(editedprojname, key='css_links', value=d_list)
        except e:
            raise FailPage(message = "Unable to save defaults.json")


def css_down(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Moves css default label down"
    editedprojname = call_data['editedprojname']
    if 'css_label' in call_data:
        label = call_data['css_label']
        d_list = fromjson.get_defaults(editedprojname, 'css_links')
        if not label in d_list:
            return
        index = d_list.index(label)
        # move down
        if index == len(d_list)-1:
            return
        d_list.insert(index+1, d_list.pop(index))
        # save d_list
        try:
            fromjson.set_defaults(editedprojname, key='css_links', value=d_list)
        except e:
            raise FailPage(message = "Unable to save defaults.json")


def add_default_js(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Add a label to the default javascript list"

    editedprojname = call_data['editedprojname']

    # check label is valid
    if not "new_js_label" in call_data:
        raise FailPage(message = "label missing")

    label = call_data["new_js_label"]
    if not label:
        raise FailPage(message = "label missing")

    if _AN.search(label):
        raise FailPage(message = "The label can only contain A-Z, a-z, 0-9 and the underscore character.")

    if '_' in label:
        labelparts = label.split('_')
        if labelparts[0].isalnum() and labelparts[1].isdigit():
            raise FailPage(message = "Invalid label (Danger of confusion with a page ident).")

    if label.isdigit():
        raise FailPage(message = "Invalid label (Danger of confusion with a page ident).")

    js_list = fromjson.get_defaults(editedprojname, key='js_links')
    if label in js_list:
        raise FailPage(message = "This label is already in the list")
    js_list. append(label)
    try:
        fromjson.set_defaults(editedprojname, key='js_links', value=js_list)
    except e:
        raise FailPage(message = "Unable to save defaults.json")


def js_remove(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Removes js default label"
    editedprojname = call_data['editedprojname']
    if 'js_label' in call_data:
        label = call_data['js_label']
        d_list = fromjson.get_defaults(editedprojname, 'js_links')
        if not label in d_list:
            return
        index = d_list.index(label)
        # remove
        del d_list[index]
        # save d_list
        try:
            fromjson.set_defaults(editedprojname, key='js_links', value=d_list)
        except e:
            raise FailPage(message = "Unable to save defaults.json")


def js_up(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Moves js default label up"
    editedprojname = call_data['editedprojname']
    if 'js_label' in call_data:
        label = call_data['js_label']
        d_list = fromjson.get_defaults(editedprojname, 'js_links')
        if not label in d_list:
            return
        index = d_list.index(label)
        # move up
        if not index:
            return
        d_list.insert(index-1, d_list.pop(index))
        # save d_list
        try:
            fromjson.set_defaults(editedprojname, key='js_links', value=d_list)
        except e:
            raise FailPage(message = "Unable to save defaults.json")

def js_down(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Moves js default label down"
    editedprojname = call_data['editedprojname']
    if 'js_label' in call_data:
        label = call_data['js_label']
        d_list = fromjson.get_defaults(editedprojname, 'js_links')
        if not label in d_list:
            return
        index = d_list.index(label)
        # move down
        if index == len(d_list)-1:
            return
        d_list.insert(index+1, d_list.pop(index))
        # save d_list
        try:
            fromjson.set_defaults(editedprojname, key='js_links', value=d_list)
        except e:
            raise FailPage(message = "Unable to save defaults.json")




