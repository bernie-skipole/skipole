####### SKIPOLE WEB FRAMEWORK #######
#
# managespecialpages.py  - get and put for managing and editing special pages
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


import re
# a search for anything none-alphanumeric and not an underscore
_AN = re.compile('[^\w_]')


from ....ski import skiboot
from .... import skilift
from ....skilift import fromjson

from .. import utils
from ....ski.excepts import FailPage, ValidateError, ServerError


def retrieve_managepage(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "this call is for the manage special pages page"

    editedproj = call_data['editedproj']
    editedproj_ident = editedproj.proj_ident
    specials = editedproj.special_pages

    page_data[("adminhead","page_head","large_text")] = "Manage page labels"
    page_data[("adminhead","page_head","small_text")] = "Set or edit page labels"

    system_list = skiboot.sys_list()
    page_data['system:col_label'] = system_list
    page_data['system:col_input'] = _make_list(editedproj_ident, system_list, specials)
    page_data['system:hidden_field1'] = system_list

    lib_list = skiboot.lib_list()
    page_data['jq:col_label'] = lib_list
    page_data['jq:col_input'] = _make_list(editedproj_ident, lib_list, specials)
    page_data['jq:hidden_field1'] = lib_list

    user_label_list = [item for item in specials if ( (item not in system_list) and (item not in lib_list) )]
    if user_label_list:
        user_label_list.sort()
        page_data['user:col_label'] = user_label_list
        page_data['user:col_input'] = _make_list(editedproj_ident, user_label_list, specials)
        page_data['user:hidden_field1'] = user_label_list
    else:
        page_data['user:show'] = False

    # get default css links for widget css_defaults
    css_list = fromjson.get_defaults(editedproj_ident, key='css_links')

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
    js_list = fromjson.get_defaults(editedproj_ident, key='js_links')

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


def _make_list(editedproj_ident, reflist, specials):
    "Creates a list of url's or string ident numbers of items in reflist"
    result = []
    for item in reflist:
        if item in specials:
            target = specials[item]
            if isinstance(target, str):
                # its a url
                result.append(target)
            else:
                # its an ident
                if target.proj == editedproj_ident:
                    result.append(str(target.num))
                else:
                    result.append(target.to_comma_str())
        else:
            result.append('')
    return result


def submit_special_page(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Sets special page"

    editedproj = call_data['editedproj']

    label = call_data["label"]
    ident_or_url = call_data["ident_or_url"]
    if (not label) or (not ident_or_url):
        raise FailPage(message = "label or ident missing")

    # check label is valid
    if _AN.search(label):
        raise FailPage(message = "The label can only contain A-Z, a-z, 0-9 and the underscore character.")

    if '_' in label:
        labelparts = label.split('_')
        for lpart in labelparts:
            if lpart.isdigit():
                raise FailPage(message = "Invalid label (Danger of confusion with a page ident, please avoid using digits without letters).")

    if label.isdigit():
        raise FailPage(message = "Invalid label (Danger of confusion with a page ident).")

    try:
        editedproj.set_special_page(label, ident_or_url)
    except (ValidateError, ServerError) as e:
        raise FailPage(message = e.message)

    if label in skiboot.sys_list():
        call_data['status'] = 'System special page %s set' % (label,)
        return
    if label in skiboot.lib_list():
        call_data['status'] = 'Library special page %s set' % (label,)
        return
    call_data['status'] = 'Label %s set' % (label,)


def add_user_page(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Sets user defined label and target"

    editedproj = call_data['editedproj']

    label = call_data["label"]
    ident_or_url = call_data["ident_or_url"]
    if (not label) or (not ident_or_url):
        raise FailPage(message = "label or ident missing", widget='addlabel')

    # check label is valid
    if _AN.search(label):
        raise FailPage(message = "The label can only contain A-Z, a-z, 0-9 and the underscore character.")

    if '_' in label:
        labelparts = label.split('_')
        for lpart in labelparts:
            if lpart.isdigit():
                raise FailPage(message = "Invalid label (Danger of confusion with a page ident, please avoid using digits without letters).")

    if label.isdigit():
        raise FailPage(message = "Invalid label (Danger of confusion with a page ident).")

    if label in skiboot.lib_list():
        raise FailPage(message = "Invalid label, reserved for system files.")
    if label in skiboot.sys_list():
        raise FailPage(message = "Invalid label, reserved for system pages.")

    try:
        editedproj.set_special_page(label, ident_or_url)
    except (ValidateError, ServerError) as e:
        raise FailPage(message = e.message)

    call_data['status'] = 'Label %s set' % (label,)


def submit_user_page(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Edits or deletes a special user page"

    editedproj = call_data['editedproj']

    if 'label' not in call_data:
        raise FailPage(message = "Invalid label.")
    label = call_data["label"]
    if label in skiboot.lib_list():
        raise FailPage(message = "Invalid label.")
    if label in skiboot.sys_list():
        raise FailPage(message = "Invalid label.")
    if ("edit" in call_data) and (call_data["edit"]):
        submit_special_page(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang)
        return
    if ("delete" not in call_data) or (not call_data["delete"]):
        raise FailPage(message = "Invalid submission.")
    try:
        editedproj.delete_special_page(label)
    except (ValidateError, ServerError) as e:
        raise FailPage(message = e.message)
    call_data['status'] = 'User label deleted'


def js_up(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Moves js default label up"
    editedproj = call_data['editedproj']
    if 'js_label' in call_data:
        label = call_data['js_label']
        d_list = fromjson.get_defaults(editedproj.proj_ident, 'js_links')
        if not label in d_list:
            return
        index = d_list.index(label)
        # move up
        if not index:
            return
        d_list.insert(index-1, d_list.pop(index))
        # save d_list
        try:
            fromjson.set_defaults(editedproj.proj_ident, key='js_links', value=d_list)
        except e:
            raise FailPage(message = "Unable to save defaults.json")

def js_down(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Moves js default label down"
    editedproj = call_data['editedproj']
    if 'js_label' in call_data:
        label = call_data['js_label']
        d_list = fromjson.get_defaults(editedproj.proj_ident, 'js_links')
        if not label in d_list:
            return
        index = d_list.index(label)
        # move down
        if index == len(d_list)-1:
            return
        d_list.insert(index+1, d_list.pop(index))
        # save d_list
        try:
            fromjson.set_defaults(editedproj.proj_ident, key='js_links', value=d_list)
        except e:
            raise FailPage(message = "Unable to save defaults.json")


def js_remove(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Removes js default label"
    editedproj = call_data['editedproj']
    if 'js_label' in call_data:
        label = call_data['js_label']
        d_list = fromjson.get_defaults(editedproj.proj_ident, 'js_links')
        if not label in d_list:
            return
        index = d_list.index(label)
        # remove
        del d_list[index]
        # save d_list
        try:
            fromjson.set_defaults(editedproj.proj_ident, key='js_links', value=d_list)
        except e:
            raise FailPage(message = "Unable to save defaults.json")



def css_up(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Moves css default label up"
    editedproj = call_data['editedproj']
    if 'css_label' in call_data:
        label = call_data['css_label']
        d_list = fromjson.get_defaults(editedproj.proj_ident, 'css_links')
        if not label in d_list:
            return
        index = d_list.index(label)
        # move up
        if not index:
            return
        d_list.insert(index-1, d_list.pop(index))
        # save d_list
        try:
            fromjson.set_defaults(editedproj.proj_ident, key='css_links', value=d_list)
        except e:
            raise FailPage(message = "Unable to save defaults.json")

def css_down(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Moves css default label down"
    editedproj = call_data['editedproj']
    if 'css_label' in call_data:
        label = call_data['css_label']
        d_list = fromjson.get_defaults(editedproj.proj_ident, 'css_links')
        if not label in d_list:
            return
        index = d_list.index(label)
        # move down
        if index == len(d_list)-1:
            return
        d_list.insert(index+1, d_list.pop(index))
        # save d_list
        try:
            fromjson.set_defaults(editedproj.proj_ident, key='css_links', value=d_list)
        except e:
            raise FailPage(message = "Unable to save defaults.json")


def css_remove(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Removes css default label"
    editedproj = call_data['editedproj']
    if 'css_label' in call_data:
        label = call_data['css_label']
        d_list = fromjson.get_defaults(editedproj.proj_ident, 'css_links')
        if not label in d_list:
            return
        index = d_list.index(label)
        # remove
        del d_list[index]
        # save d_list
        try:
            fromjson.set_defaults(editedproj.proj_ident, key='css_links', value=d_list)
        except e:
            raise FailPage(message = "Unable to save defaults.json")


def add_default_css(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Add a label to the default css list"

    editedproj = call_data['editedproj']

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

    css_list = fromjson.get_defaults(editedproj.proj_ident, key='css_links')
    if label in css_list:
        raise FailPage(message = "This label is already in the list")
    css_list. append(label)
    try:
        fromjson.set_defaults(editedproj.proj_ident, key='css_links', value=css_list)
    except e:
        raise FailPage(message = "Unable to save defaults.json")
    
    
def add_default_js(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Add a label to the default javascript list"

    editedproj = call_data['editedproj']

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

    js_list = fromjson.get_defaults(editedproj.proj_ident, key='js_links')
    if label in js_list:
        raise FailPage(message = "This label is already in the list")
    js_list. append(label)
    try:
        fromjson.set_defaults(editedproj.proj_ident, key='js_links', value=js_list)
    except e:
        raise FailPage(message = "Unable to save defaults.json")
