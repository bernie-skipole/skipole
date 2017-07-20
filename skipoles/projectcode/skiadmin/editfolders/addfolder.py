####### SKIPOLE WEB FRAMEWORK #######
#
# addfolder.py  - get and put functions for the add folder page
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

import os

from ....ski import skiboot
from ....ski.excepts import ValidateError, FailPage, ServerError
from ....ski.folder_class_definition import Folder
from ....ski.page_class_definition import FilePage

from .. import utils

from .... import skilift
from ....skilift import editfolder, fromjson



def retrieve_add_folder(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):

    editedproj = call_data['editedproj']
    adminproj = call_data['adminproj']

    # parent is the folder a new folder is to be added to
    # the value in call_data is the string ident submitted by the ftree add_folder button
    # or by a value in session_data
    if 'parent' in call_data:
        parent_ident = skiboot.Ident.to_ident(call_data['parent'], editedproj.proj_ident)
        parent =  editedproj.get_item(parent_ident)
        if parent.page_type != "Folder":
            raise FailPage(message = "Invalid parent folder")

    elif 'add_to_foldernumber' in call_data:
        parent_ident = skiboot.Ident.to_ident(call_data['add_to_foldernumber'], editedproj.proj_ident)
        parent =  editedproj.get_item(parent_ident)
        if parent.page_type != "Folder":
            raise FailPage(message = "Invalid parent folder")
    else:
        raise FailPage(message = "Parent folder missing")
    parent_ident = str(parent.ident)

    page_data[("adminhead","page_head","large_text")] = "Add folder to : %s" % (parent.url,)
    page_data[("adminhead","page_head","small_text")] = "Choose options to add the folder:"

    page_data[('staticpath','input_text')] = os.path.join(editedproj.proj_ident, 'static')

    page_data[('newfolderform','parent')] = parent_ident
    call_data['add_to_foldernumber'] = parent.ident.num

    # st1: new folder name
    if 'new_folder' in call_data:
        page_data[('foldername','new_folder')] = call_data['new_folder']

    # cb1: restricted checkbox
    if ('checkbox' in call_data) and call_data['checkbox']:
        page_data[('cb1','checked')] = True
    else:
        page_data[('cb1','checked')] = False
    if parent.restricted:
        page_data[('cb1','show_restricted')] = False
    else:
        page_data[('cb1','show_restricted')] = True

    # it1: text input for folder brief
    if ('folder_brief' in call_data) and call_data['folder_brief']:
        page_data[('it1','folder_brief')] = call_data['folder_brief']

    # it2: folder ident number
    if 'folder_ident_number' in call_data:
        page_data[('it2','folder_ident_number')] = str(call_data['folder_ident_number'])
    else:
        page_data[('it2','folder_ident_number')] = str(editedproj.next_ident().num)


def submit_addfolder(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    """ Creates a folder by making a dictionary similar to:

    {
     "name":"folder_name",
     "ident":999,
     "brief":"brief description of the folder",
     "restricted":False
    }

    And then calling editfolder.make_new_folder.

    Also calls _make_static_folder if folderpath is in call data

"""

    folder_dict = {}

    if 'parent' not in call_data:
        raise FailPage(message = "Parent folder missing")
    # the parent value in call_data is the string ident submitted by the button
    try:
        project, parent_number = call_data['parent'].split('_')
        parent_number = int(parent_number)
    except:
        raise FailPage(message = "Invalid parent folder")
    if project != call_data['editedprojname']:
        raise FailPage(message = "Invalid parent folder")

    parentinfo = skilift.item_info(project, parent_number)
    if not parentinfo:
        raise FailPage(message = "Invalid parent folder")
    # parentinfo is a named tuple with members
    # 'project', 'project_version', 'itemnumber', 'item_type', 'name', 'brief', 'path', 'label_list', 'change', 'parentfolder_number', 'restricted'
    if parentinfo.item_type != "Folder":
        raise FailPage(message = "Invalid parent folder")

    if ('new_folder' not in call_data) or ('checkbox' not in call_data) or ('folder_brief' not in call_data) or ('folder_ident_number' not in call_data):
        raise FailPage("New folder information missing")

    try:
        folder_ident_number = int(call_data['folder_ident_number'])
    except:
        raise FailPage("The Folder Ident number must be an integer")
    if folder_ident_number<1:
        raise FailPage("The Folder Ident number must be a positive integer greater than zero")
    folder_dict["ident"] = folder_ident_number
    folder_dict["name"] = call_data['new_folder']
    folder_dict["brief"] = call_data['folder_brief']
    folder_dict["restricted"] = call_data['checkbox']


    if 'folderpath' in call_data and call_data['folderpath']:
        folderpath = call_data['folderpath']
        folderpath = folderpath.rstrip('/')
        folderpath = folderpath.rstrip('\\')
        if not folderpath:
            raise FailPage("Sorry, the given static folder is invalid.")
        fullpath = os.path.join(skiboot.projectfiles(), folderpath)
        if not os.path.isdir(fullpath):
            raise FailPage("Sorry, the given static folder location cannot be found.")
        if not call_data['folder_brief']:
            folder_dict["brief"] = "Link to %s" % folderpath
    else:
        folderpath = None
        fullpath = None

    try:
        # create the folder
        editfolder.make_new_folder(project, parent_number, folder_dict)
    except ServerError as e:
        raise FailPage(message = e.message)

    if fullpath:
        # add subfolders and file pages
        _make_static_folder(project, folder_dict, fullpath, folderpath)
        call_data['status'] = 'Static folder tree added'
        return

    call_data['status'] = 'New folder %s added.' % (parentinfo.path + folder_dict["name"] + '/',)


def _make_static_folder(project, folder_dict, fullpath, folderpath):
    """Creates containing sub folders and Filepages pointing to static files within a directory
       of the server"""
    ###### note, still uses parent 'Folder' object until FilePage is sorted
    try:
        editedproj = skiboot.getproject(project)
        # loads everything under folderpath as Folders and FilePages
        # ident_dict maps folderpath to newly created folder ident numbers
        ident_dict = {}
        ident_dict[folderpath] = folder_dict["ident"]
        ident = folder_dict["ident"]
        for root, dirs, files in os.walk(fullpath):
            # given root, find the folder, at first pass, equivalent to parent=folder
            fpath = root[len(skiboot.projectfiles())+1:]
            parent_ident = ident_dict[fpath]
            parent = editedproj.get_item(parent_ident)
            if files:
                # create files
                for filename in files:
                    new_file = FilePage(name=filename, filepath=os.path.join(fpath, filename))
                    if ident:
                        ident +=1
                        if ident in editedproj:
                            ident = None
                    parent.add_page(new_file, ident=ident)
            if dirs:
                # create folders
                for foldername in dirs:
                    new_folderpath=os.path.join(fpath, foldername)
                    new_folder_dict = {"name":foldername,
                                       "brief":"Link to %s" % (new_folderpath,),
                                       "restricted":False
                                      }
                    if ident:
                        ident +=1
                        if ident not in editedproj:
                            new_folder_dict["ident"] = ident
                    ident_dict[new_folderpath] = editfolder.make_new_folder(project, parent_ident, new_folder_dict)
    except ValidateError as e:
        raise FailPage(e.message)



def submit_upload_folder(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Copy a folder from uploaded file"

    editedproj = call_data['editedproj']
    adminproj = call_data['adminproj']

    # add_to_foldernumber is the folder a new folder is to be added to
    if 'add_to_foldernumber' in call_data:
        add_to_folderident = skiboot.Ident.to_ident(call_data['add_to_foldernumber'], editedproj.proj_ident)
        # add_to_folder is the folder from memory, not a copy
        add_to_folder =  editedproj.get_item(add_to_folderident)
        if add_to_folder.page_type != "Folder":
            raise FailPage(message = "Invalid parent folder")
    else:
        raise FailPage(message = "Parent folder missing")

    # get submitted data for new folder
    try:
        addident = int(call_data['addident'])
    except:
        raise FailPage(message = "Addition integer is invalid")
    importname = call_data['importname']
    uploadfile = call_data['uploadfile']
    json_string = uploadfile.decode(encoding='utf-8')
    # create the folder
    try:
        fromjson.create_folder(editedproj.proj_ident, add_to_folderident.num, addident, importname, add_to_folder.restricted, json_string)
    except ServerError as e:
        raise FailPage(message = e.message, widget='import_folder')
    del call_data['add_to_foldernumber']
    call_data['status'] = 'New folder and contents added'

