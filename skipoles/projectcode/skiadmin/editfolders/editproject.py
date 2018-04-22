####### SKIPOLE WEB FRAMEWORK #######
#
# editproject.py  - get and put functions for the edit project page
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


import os, shutil

from .... import skilift
from ....ski import skiboot
from ....ski.excepts import FailPage, ValidateError, ServerError


def retrieve_edit_project(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Fill in the page to edit the sub project url"

    # project is the edited project name
    project = call_data['editedprojname']

    #  get the sub project to be edited
    if 'project' in call_data:
        sub_project = call_data['project']
    else:
        raise FailPage(message="Project not found")
    if not sub_project:
        raise FailPage(message = 'invalid project')
    if sub_project == project:
        raise FailPage(message = 'invalid project')

    projectpaths = skilift.projectURLpaths()
    if sub_project not in projectpaths:
        raise FailPage(message = 'invalid project')

    url = projectpaths[sub_project]
    page_data['subprojurl:hidden_field1'] = sub_project
    page_data['subprojurl:input_text'] = url
    page_data[("adminhead","page_head","large_text")] = "Sub-project : " + sub_project


def submit_addproject(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "add a project"

    # project is the edited project name
    project = call_data['editedprojname']

    if "add_project" not in call_data:
        raise FailPage(message='Invalid call')

    proj_id = call_data["add_project"]
    if proj_id == skilift.admin_project():
        raise FailPage(message = "Cannot add skiadmin project")
    if proj_id == project:
        raise FailPage(message = "Cannot add a project to itself")
    try:
        skilift.add_sub_project(proj_id)
    except (ValidateError, ServerError) as e:
        raise FailPage(message = e.message)


def submit_removeproject(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "remove a project"

    if "remove_project" not in call_data:
        raise FailPage(message='Invalid call')

    proj_id = call_data["remove_project"]
    if proj_id == skilift.admin_project():
        # Cannot remove skiadmin
        raise FailPage(message = "Cannot remove the current admin project")
    # remove a project
    try:
        # remove the sub project
        skilift.remove_sub_project(proj_id)
    except (ValidateError, ServerError) as e:
        raise FailPage(message = e.message)


def submit_suburl(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "sets the url of a sub project"

    # project is the edited project name
    project = call_data['editedprojname']

    if "project_url" not in call_data:
        raise FailPage(message='New sub project path has not been given')
    if "project" not in call_data:
        raise FailPage(message='The sub project to edit has not been given')
    #  get the sub project to be edited
    proj_id = call_data['project']
    if (not proj_id) or (proj_id == project):
        raise FailPage(message = 'invalid project')
    projectpaths = skilift.projectURLpaths()
    if proj_id not in projectpaths:
        raise FailPage(message = 'invalid project')
    current_url = projectpaths[proj_id]
    if current_url == call_data["project_url"]:
        return {("adminhead","page_head","small_text"):"No change to the current URL?"}
    try:
        skilift.set_sub_project_path(proj_id, call_data["project_url"])
    except (ValidateError, ServerError) as e:
        raise FailPage(message = e.message)
    call_data['status'] = "Sub project URL set."


def retrieve_about_code(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "About your code page"
    # project is the edited project name
    project = call_data['editedprojname']
    page_data[("adminhead","page_head","large_text")] = "Your Code"
    page_data[("codelocation","para_text")] = skilift.get_projectcode_dir(project)
    page_data[('codedir', 'proj_ident')] = project
    page_data[("filelocation","para_text")] = os.path.join(skilift.get_projectfiles_dir(project), "static")


def retrieve_about_skilift(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "About skilift page"
    page_data[("adminhead","page_head","large_text")] = "skilift"


def retrieve_about_fromjson(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "About fromjson module"
    page_data[("adminhead","page_head","large_text")] = "fromjson"
    call_data['extend_nav_buttons'] = [[70005, "skilift", False, '']]


def retrieve_about_editfolder(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "About editfolder module"
    page_data[("adminhead","page_head","large_text")] = "editfolder"
    call_data['extend_nav_buttons'] = [[70005, "skilift", False, '']]


def retrieve_about_editpage(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "About editpage module"
    page_data[("adminhead","page_head","large_text")] = "editpage"
    call_data['extend_nav_buttons'] = [[70005, "skilift", False, '']]


def retrieve_about_editsection(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "About editsection module"
    page_data[("adminhead","page_head","large_text")] = "editsection"
    call_data['extend_nav_buttons'] = [[70005, "skilift", False, '']]


def retrieve_about_off_piste(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "About off_piste module"
    page_data[("adminhead","page_head","large_text")] = "off_piste"
    call_data['extend_nav_buttons'] = [[70005, "skilift", False, '']]


def get_text(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    """Finds any widget submitting 'get_field' with value of a textblock ref, returns
       page_data with key widget with field 'div_content' and value the textblock text"""
    # adminproj is the admin project name, normally skiadmin
    adminproj = skilift.admin_project()
    if 'received' not in submit_dict:
        return
    received_widgfields = submit_dict['received']
    for key, val in received_widgfields.items():
        if isinstance(key, tuple) and (key[-1] == 'get_field'):
            text = skilift.get_textblock_text(val, lang, project=adminproj).replace('\n', '\n<br />')
            if text is None:
                continue
            if len(key) == 3:
                page_data[(key[0], key[1],'div_content')] = text
                page_data[(key[0], key[1],'hide')] = False
            elif len(key) == 2:
                page_data[(key[0],'div_content')] = text
                page_data[(key[0],'hide')] = False

