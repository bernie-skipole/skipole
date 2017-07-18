####### SKIPOLE WEB FRAMEWORK #######
#
# common.py  - functions used to edit pages
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


from ....ski import skiboot
from ....ski.excepts import ValidateError, FailPage, ServerError, GoTo

from ....skilift.editpage import rename_page

from .. import utils




def submit_rename_page(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "rename this page"
    if 'page_number' not in call_data:
        raise FailPage(message = "Page missing")
    if 'new_name' not in call_data:
        raise FailPage(message="No new page name has been given")
    # Rename the page
    error_message = rename_page(call_data['editedprojname'], call_data['page_number'], call_data['new_name'])
    if error_message:
        raise FailPage(message=error_message)
    page_data['page_edit','p_rename','set_input_accepted'] = True
    call_data['status'] = 'Page renamed'



def submit_new_parent(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Gives a page a new parent"

    editedproj = call_data['editedproj']

    # the page to have a new parent should be given by session data
    if 'page' not in call_data:
        raise FailPage(message = "page missing")
    page = call_data['page']
    page_ident = str(page.ident)

    if not 'parent_ident' in call_data:
        raise FailPage(message="No parent ident given", widget="p_parent")
    parent_ident = call_data['parent_ident']
    if not parent_ident:
        raise FailPage(message="No parent ident given", widget="p_parent")
    new_parent = skiboot.from_ident(parent_ident)
    if not new_parent:
        raise FailPage(message="No valid parent ident given", widget="p_parent")
    if new_parent.page_type != 'Folder':
        raise FailPage(message="Item is not a folder", widget="p_parent")
    if new_parent not in editedproj:
        raise FailPage(message="Invalid folder", widget="p_parent")
    old_parent = page.parentfolder
    if old_parent == new_parent:
       raise FailPage(message="Parent folder unchanged?", widget="p_parent")
    if old_parent.proj_ident != new_parent.proj_ident:
        raise FailPage("Invalid folder project", widget="p_parent")
    if page.name in new_parent:
        raise FailPage("The folder already contains an item with this name", widget="p_parent")
    try:
        editedproj.save_page(page, new_parent.ident)
    except ServerError as e:
        raise FailPage(message=e.message, widget="p_parent")
    call_data['status'] = 'Page moved'


def submit_page_brief(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Sets new page brief"
    # the page to have a new brief should be given by session data
    if 'page' not in call_data:
        raise FailPage(message = "page missing")
    page = call_data['page']
    page_ident = str(page.ident)

    if not 'page_brief' in call_data:
        raise FailPage(message="No page brief given", widget="p_brief")
    new_brief = call_data['page_brief']
    if not new_brief:
        raise FailPage(message="No page brief given", widget="p_brief")
    # Set the page brief
    page.brief = new_brief
    utils.save(call_data, page=page)
    call_data['status'] = 'Page brief set: %s' % (new_brief,)


def goto_edit(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    caller_num = caller_ident[1]
    if caller_num == 28009:
        raise GoTo(28007)         # css edit page
    elif caller_num == 20409:
        raise GoTo(20407)         # json edit page
    elif caller_num == 23209:
        raise GoTo(23207)          # retrieve template edit page contents
    elif caller_num == 23409:
        raise GoTo(23407)          # svg edit page
    elif caller_num == 26009:
        raise GoTo(26007)          # retrieve responder edit page contents
    elif caller_num == 29009:
        raise GoTo(29007)          # filepage edit page
    else:
        raise GoTo('admin_home', clear_page_data=True)
