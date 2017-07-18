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



from ....skilift import fromjson, off_piste
from ....ski.excepts import FailPage, ValidateError, ServerError, GoTo

from .. import css_styles



def retrieve_operations_data(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Retrieves field data for operations page"

    editedprojname = call_data['editedprojname']

    # project background color
    page_data['htmlbackcol','input_text'] = fromjson.get_defaults(editedprojname, key="backcol")



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



