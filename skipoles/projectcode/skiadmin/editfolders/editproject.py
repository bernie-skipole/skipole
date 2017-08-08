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

from ... import get_projectcode_dir

from ....skilift import get_textblock_text, get_projectfiles_dir
from ....ski import skiboot, folder_class_definition
from ....ski.excepts import FailPage, ValidateError, ServerError


def retrieve_edit_project(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):

    editedproj = call_data['editedproj']
    adminproj = call_data['adminproj']

    #  get the sub project to be edited
    if 'project' in call_data:
        sub_project = call_data['project']
    else:
        raise FailPage(message="Project not found", widget = "projmap")
    if (not sub_project) or (not skiboot.is_project(sub_project)):
        raise FailPage(message = 'invalid project', widget = "projmap")
    url = editedproj.subproject_paths[sub_project]
    page_data['subprojurl:hidden_field1'] = sub_project
    page_data['subprojurl:bottomtext'] = "Current sub project URL is %s" % (url,)
    page_data['subprojurl:input_text'] = url

    page_data[("adminhead","page_head","large_text")] = "Sub-project : " + sub_project
    page_data[("adminhead","page_head","small_text")] = "(Editing here does not alter the sub project - only its location within this site)"


def submit_addproject(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "add a project"

    editedproj = call_data['editedproj']
    adminproj = call_data['adminproj']

    if not editedproj.rootproject:
        # cannot add a subproject if this is not the rootproject
        raise FailPage(message='Invalid: Not the root project', widget = "sdd1")

    if "add_project" not in call_data:
        raise ValidateError(message='Invalid call')

    proj_id = call_data["add_project"]
    if proj_id == adminproj.proj_ident:
        raise FailPage(message = "Cannot add skiadmin project",
                            widget = "sdd1")
    if proj_id == editedproj.proj_ident:
        raise FailPage(message = "Cannot add a project to itself",
                            widget = "sdd1")
    try:
        editedproj.add_project(proj_id)
    except (ValidateError, ServerError) as e:
        raise FailPage(message = e.message,
                    widget = "sdd1")


def submit_removeproject(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "remove a project"

    editedproj = call_data['editedproj']
    adminproj = call_data['adminproj']

    if not editedproj.rootproject:
        # cannot remove a subproject if this is not the rootproject
        raise FailPage(message='Invalid: Not the root project', widget = "projmap")

    if "remove_project" not in call_data:
        raise ValidateError(message='Invalid call')

    proj_id = call_data["remove_project"]
    if proj_id == editedproj.proj_ident:
        # Cannot remove the current project
        raise FailPage(message = "Cannot remove the current project",
                    widget = "projmap")
    if proj_id == adminproj.proj_ident:
        # Cannot remove skiadmin
        raise FailPage(message = "Cannot remove the current admin project",
                    widget = "projmap")
    if proj_id not in editedproj.subprojects:
        raise FailPage(message = 'Project not found',
                    widget = "projmap")
    # remove a project
    try:
        # remove reference
        editedproj.remove_project(proj_id)
    except (ValidateError, ServerError) as e:
        raise FailPage(message = e.message,
                    widget = "projmap")


def submit_suburl(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "sets the url of a sub project"

    editedproj = call_data['editedproj']

    if "project_url" not in call_data:
        raise ValidateError(message='Invalid call')
    if "project" not in call_data:
        raise ValidateError(message='Invalid call')
    #  get the project to be edited
    proj_id = call_data['project']

    if proj_id not in editedproj.subprojects:
        raise FailPage(message = "Invalid project")
    current_url = editedproj.subproject_paths[proj_id]
    if current_url == call_data["project_url"]:
        return {("adminhead","page_head","small_text"):"No change to the current URL?"}
    try:
        editedproj.set_project_url(proj_id, call_data["project_url"])
    except (ValidateError, ServerError) as e:
        raise FailPage(message = e.message)
    call_data['status'] = "Sub project URL set."


def submit_copy_project(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Copies the project"

    editedproj = call_data['editedproj']
    source_id = editedproj.proj_ident

    if "copy_project" not in call_data:
        raise ValidateError(message='Invalid call')
    #  get the project to be created
    proj_id = call_data['copy_project']
    if not proj_id:
        raise ValidateError(message="Error - a project name must be given")
    if not (proj_id.isalnum() and proj_id.islower()):
        raise FailPage(message="Error - the project name must be lower case alphanumeric only")
    if proj_id.isdigit():
        raise FailPage(message="Error - the project name must have some letters")
    if source_id == proj_id:
        raise FailPage(message="Error - cannot copy to itself")
    if proj_id == 'skiadmin':
        raise FailPage(message="Error - skiadmin is a reserved name")
    if proj_id == skiboot.admin_project():
        raise FailPage(message="Error - Sorry, this is a reserved name")
    if proj_id == skiboot.new_project():
        raise FailPage(message="Error - Sorry, this is a reserved name")
    proj_dir =  skiboot.projectpath(proj_ident=proj_id)
    if os.path.isdir(proj_dir):
        raise FailPage(message="Error - project directory already exists")
    try:
        # create directory structure
        os.mkdir(proj_dir)
        # copy data directory and contents
        newproject_data = skiboot.projectdata(proj_id)
        source_project_data = skiboot.projectdata(source_id)
        shutil.copytree(source_project_data, newproject_data)
        # copy static directory and contents
        newproject_static = skiboot.projectstatic(proj_id)
        source_project_static = skiboot.projectstatic(source_id)
        shutil.copytree(source_project_static, newproject_static)

        # get project.json and swap out
        # "filepath": "source_id
        # for
        # "filepath": "proj_id
        # where it occurs in the project.json file
        newproject_json = skiboot.project_json(proj_id)
        current_loc = "\"filepath\": \"%s" % source_id
        new_loc = "\"filepath\": \"%s" % proj_id
        with open(newproject_json, 'r') as f:
            read_data = f.read()
        new_data = read_data.replace(current_loc, new_loc)
        with open(newproject_json, 'w') as f:
            f.write(new_data)

        # copy code
        current_project_code = skiboot.projectcode(source_id)
        newproject_code = skiboot.projectcode(proj_id)
        shutil.copytree(current_project_code, newproject_code, ignore=shutil.ignore_patterns('*.pyc'))
    except:
        raise FailPage(message="Sorry an error occurred, partial files may have been created and may need cleaning up")
    call_data['status'] = "Project %s copied to project %s" % (source_id, proj_id)



def retrieve_about_code(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "About your code page"
    editedproj = call_data['editedproj']
    adminproj = call_data['adminproj']

    page_data[("adminhead","page_head","large_text")] = "Your Code"

    if 'status' in call_data:
        page_data[("adminhead","page_head","small_text")] = call_data['status']
    else:
        page_data[("adminhead","page_head","small_text")] = "About your Python code for this project"

    page_data[("codelocation","para_text")] = get_projectcode_dir(project=editedproj.proj_ident)
    page_data[('codedir', 'proj_ident')] = editedproj.proj_ident
    page_data[("filelocation","para_text")] = os.path.join(get_projectfiles_dir(project=editedproj.proj_ident), "static")


def retrieve_about_skilift(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "About skilift page"
    editedproj = call_data['editedproj']
    adminproj = call_data['adminproj']

    page_data[("adminhead","page_head","large_text")] = "skilift"

    if 'status' in call_data:
        page_data[("adminhead","page_head","small_text")] = call_data['status']
    else:
        page_data[("adminhead","page_head","small_text")] = "About the skilift package"


def retrieve_about_fromjson(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "About fromjson module"
    editedproj = call_data['editedproj']
    adminproj = call_data['adminproj']

    page_data[("adminhead","page_head","large_text")] = "fromjson"

    call_data['extend_nav_buttons'] = [[70005, "skilift", False, '']]

    if 'status' in call_data:
        page_data[("adminhead","page_head","small_text")] = call_data['status']
    else:
        page_data[("adminhead","page_head","small_text")] = "About the fromjson module"

def retrieve_about_editfolder(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "About editfolder module"
    editedproj = call_data['editedproj']
    adminproj = call_data['adminproj']

    page_data[("adminhead","page_head","large_text")] = "editfolder"

    call_data['extend_nav_buttons'] = [[70005, "skilift", False, '']]

    if 'status' in call_data:
        page_data[("adminhead","page_head","small_text")] = call_data['status']
    else:
        page_data[("adminhead","page_head","small_text")] = "About the editfolder module"


def retrieve_about_editpage(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "About editpage module"
    editedproj = call_data['editedproj']
    adminproj = call_data['adminproj']

    page_data[("adminhead","page_head","large_text")] = "editpage"

    call_data['extend_nav_buttons'] = [[70005, "skilift", False, '']]

    if 'status' in call_data:
        page_data[("adminhead","page_head","small_text")] = call_data['status']
    else:
        page_data[("adminhead","page_head","small_text")] = "About the editpage module"


def retrieve_about_editsection(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "About editsection module"
    editedproj = call_data['editedproj']
    adminproj = call_data['adminproj']

    page_data[("adminhead","page_head","large_text")] = "editsection"

    call_data['extend_nav_buttons'] = [[70005, "skilift", False, '']]

    if 'status' in call_data:
        page_data[("adminhead","page_head","small_text")] = call_data['status']
    else:
        page_data[("adminhead","page_head","small_text")] = "About the editsection module"


def retrieve_about_off_piste(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "About off_piste module"
    editedproj = call_data['editedproj']
    adminproj = call_data['adminproj']

    page_data[("adminhead","page_head","large_text")] = "off_piste"

    call_data['extend_nav_buttons'] = [[70005, "skilift", False, '']]

    if 'status' in call_data:
        page_data[("adminhead","page_head","small_text")] = call_data['status']
    else:
        page_data[("adminhead","page_head","small_text")] = "About the off_piste module"



def get_text(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    """Finds any widget submitting 'get_field' with value of a textblock ref, returns
       page_data with key widget with field 'div_content' and value the textblock text"""
    adminproj = call_data['adminproj']
    for key, val in submit_dict.items():
        if isinstance(key, tuple) and (key[-1] == 'get_field'):
            text = get_textblock_text(val, lang, project=adminproj.proj_ident).replace('\n', '\n<br />')
            if text is None:
                continue
            if len(key) == 3:
                page_data[(key[0], key[1],'div_content')] = text
                page_data[(key[0], key[1],'hide')] = False
            elif len(key) == 2:
                page_data[(key[0],'div_content')] = text
                page_data[(key[0],'hide')] = False

