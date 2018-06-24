####### SKIPOLE WEB FRAMEWORK #######
#
# editfile.py  - download file editing functions
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

"Functions implementing download file page editing"


from ....ski.excepts import ValidateError, FailPage, ServerError

from .... import skilift
from ....skilift import editpage

from .. import utils


def retrieve_edit_filepage(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Retrieves widget data for the edit file page"
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
        if pageinfo.item_type != 'FilePage':
            raise FailPage(message = "Invalid page")
        filepath, mimetype = editpage.file_parameters(project, pagenumber)
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
    page_data['p_file:input_text'] = filepath
    page_data['p_mime:input_text'] = mimetype
    page_data['enable_cache:radio_checked'] = pageinfo.enable_cache


def submit_new_filepath(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Sets new page filepath"
    project = call_data['editedprojname']
    pagenumber = call_data['page_number']
    pchange = call_data['pchange']
    if not 'filepath' in call_data:
        raise FailPage(message="No filepath given")
    new_filepath = call_data['filepath']
    if not new_filepath:
        raise FailPage(message="No filepath given")
    try:
        call_data['pchange'] = editpage.page_filepath(project, pagenumber, pchange, new_filepath)
    except ServerError as e:
        raise FailPage(message=e.message)
    call_data['status'] = 'Page filepath set: %s' % (new_filepath,)


def submit_mimetype(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Sets mimetype"
    # the page to have a new mimetype should be given by session data
    if 'page' not in call_data:
        raise FailPage(message = "page missing")
    page = call_data['page']
    if page.page_type != "FilePage":
        raise ValidateError("Invalid page type")
    if not 'mime_type' in call_data:
        raise FailPage(message="No mimetype given", widget="p_mime")
    # Set the page mimetype
    page.mimetype = call_data['mime_type']
    # save the altered page in the database
    utils.save(call_data, page=page, widget_name="p_mime")
    call_data['status'] = 'Mimetype set'


def submit_cache(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Sets cache true or false"
    if 'page' not in call_data:
        raise FailPage(message = "page missing")
    page = call_data['page']
    if page.page_type != "FilePage":
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
    utils.save(call_data, page=page, widget_name="cache_submit")
    call_data['status'] = message

