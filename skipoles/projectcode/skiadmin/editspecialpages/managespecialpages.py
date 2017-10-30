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


