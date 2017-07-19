####### SKIPOLE WEB FRAMEWORK #######
#
# editfolder.py  - get and put functions for the edit folder page
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


from collections import OrderedDict

from ....ski import skiboot
from ....ski.excepts import ValidateError, FailPage, ServerError, GoTo
from .... import skilift
from ....skilift import editpage, editfolder, fromjson, pages, folders, folder_info, item_info


def edit_root(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Go to edit root folder, with no other call_data contents other than those set here"
    # called by responder 3, edit_root link from Root Folder nav button
    # this responder then targets responder 22008 to fill in root folder fields
    editedprojname = call_data['editedprojname']
    editedprojurl = call_data['editedprojurl']
    editedprojversion = call_data['editedprojversion']
    editedprojbrief = call_data['editedprojbrief']
    editedproj = call_data['editedproj']
    adminproj = call_data['adminproj']
    extend_nav_buttons = call_data['extend_nav_buttons']
    caller_ident = call_data['caller_ident']
    call_data.clear()
    call_data['editedprojname'] = editedprojname
    call_data['editedprojurl'] = editedprojurl
    call_data['editedprojversion'] = editedprojversion
    call_data['editedprojbrief'] = editedprojbrief
    call_data['editedproj'] = editedproj
    call_data['adminproj'] = adminproj
    call_data['caller_ident'] = caller_ident
    call_data['extend_nav_buttons'] = extend_nav_buttons
    call_data['folder_number'] = 0


def goto_edited_folder(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    """Called by responder 2001 with requests from various places to to edit a folder
       This responder passes the call to another responder which calls retrieve_edited_folder"""

    if 'received_data' not in submit_dict:
        raise FailPage(message = "Folder missing")

    # from the folder edit page
    widgfields = submit_dict['received_data']
    if ('ftree','edited_item') in widgfields:
        call_data['edit_folder'] = widgfields['ftree','edited_item']

    # also from the cancel button of the confirm page delete
    # uses session data, so does not need anything added here.




def retrieve_edited_folder(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):

    editedproj = call_data['editedproj']

    # 'edit_folder' is from a form, not from session data

    if 'edit_folder' in call_data:
        folder = skiboot.from_ident(call_data['edit_folder'])
        del call_data['edit_folder']
    elif 'folder_number' in call_data:
        folder = skiboot.from_ident((call_data['editedprojname'], call_data['folder_number']))
    elif 'folder' in call_data:
        folder = skiboot.from_ident(call_data['folder'])
    else:
        raise FailPage(message = "Folder missing")

    if (not folder) or (folder not in editedproj):
        raise FailPage(message = "Invalid folder")

    if folder.page_type != "Folder":
        raise FailPage(message = "Invalid folder")

    # set folder into call_data
    call_data['folder'] = folder
    call_data['folder_number'] = folder.ident.num

    folder_ident = str(folder.ident)

    contents, rows = _foldertree(editedproj.proj_ident, folder.ident.num)
    page_data['ftree', 'contents'] = contents
    page_data['ftree', 'rows'] = rows

    page_data['ftree', 'cols'] = [ ["edit_action", ""],
                                   ["edit_action", ""],
                                   ["edit_action", ""],
                                   ["edit_action", ""],
                                   ["edit_action", ""],
                                   ["edit_action", ""],
                                   ["edit_action", ""],
                                   ["no_javascript", "2004"]  ]

    if 'status' in call_data:
        page_data[("adminhead","page_head","small_text")] = call_data['status']
    else:
        page_data[("adminhead","page_head","small_text")] = folder.brief

    if folder.ident.num == 0:
        page_data[("adminhead","page_head","large_text")] = "Edit Root Folder : %s" % (folder.url,)
    else:
        page_data[("adminhead","page_head","large_text")] = "Edit Folder : %s" % (folder.url,)

    # set edited folder in the required dictionary
    page_data['ie1:page_ident'] = folder.ident
    if 'brief' in call_data:
        page_data['st2:folder_brief'] = call_data['brief']
    else:
        page_data['st2:folder_brief'] = folder.brief
    # check if this is rootfolder
    if folder.ident.num == 0:
        # hide certain items if this is the root folder
        page_data['rename_folder','show'] = False
        page_data['sp1:show_parent_restricted'] = False
        page_data['sb1:show_set_restricted'] = False
        page_data['sb2:show_set_unrestricted'] = False
    else:
        # The folder can be given a name
        if 'name' in call_data:
            page_data['rename_folder','input_text'] = call_data['name']
        else:
            page_data['rename_folder', 'input_text'] = folder.name
        if folder.parentfolder.restricted:
            page_data['sp1:show_parent_restricted'] = True
            page_data['sb1:show_set_restricted'] = False
            page_data['sb2:show_set_unrestricted'] = False
        else:
            # parent is not restricted
            page_data['sp1:show_parent_restricted'] = False
            if folder.restricted:
                # folder currently restricted
                page_data['sb1:show_set_restricted'] = False
                page_data['sb2:show_set_unrestricted'] = True
            else:
                # folder currently unrestricted
                page_data['sb1:show_set_restricted'] = True
                page_data['sb2:show_set_unrestricted'] = False
    if folder.default_page:
        page_data['sdd1:selectvalue'] = folder.default_page.name
    else:
        page_data['sdd1:selectvalue'] = "-None-"
    page_data['sdd1:option_list'] = [page_name for page_name in folder.pages]
    page_data['sdd1:option_list'].insert(0,"-None-")
    if folder.restricted:
        # do not give a choose default page option if the folder has restricted access
        page_data['sdd1:show'] = False
    else:
        page_data['sdd1:show'] = bool(folder.pages)


def choose_edit_action(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Choose which action to take when called from ftree"
    if ('ftree', 'contents') not in call_data:
        raise FailPage(message = "Requested action not recognised")
    action = call_data['ftree', 'contents']
    try:
        get_field_list = action.split('_')
        project = get_field_list[-2]
        itemnumber = int(get_field_list[-1])
    except:
        raise FailPage(message = "Requested action not recognised")
    if action.startswith('edit_folder_'):
        call_data['edit_folder'] = action[12:]
        raise GoTo(('skiadmin',22008), clear_submitted=True, clear_page_data=True)
    elif action.startswith('add_folder_'):
        call_data['parent'] = action[11:]
        raise GoTo(('skiadmin',22107), clear_submitted=True, clear_page_data=True)
    elif action.startswith('add_page_'):
        call_data['edited_folder'] = action[9:]
        raise GoTo(('skiadmin',22307), clear_submitted=True, clear_page_data=True)
    elif action.startswith('edit_page_'):
        # must find type of page to edit
        try:
            # pinfo is tuple 'name', 'number', 'restricted', 'brief', 'item_type', 'responder'
            pinfo = skilift.page_info(project, itemnumber)
        except:
            raise FailPage(message = "Requested page not recognised")
        call_data['page_number'] = pinfo.number
        if pinfo.item_type == 'CSS':
            raise GoTo(28007, clear_submitted=True, clear_page_data=True)         # css edit page
        elif pinfo.item_type == 'JSON':
            raise GoTo(20407, clear_submitted=True, clear_page_data=True)         # json edit page
        elif pinfo.item_type == 'TemplatePage':
            raise GoTo(23207, clear_submitted=True, clear_page_data=True)          # retrieve template edit page contents
        elif pinfo.item_type == 'SVG':
            raise GoTo(23407, clear_submitted=True, clear_page_data=True)          # svg edit page
        elif pinfo.item_type == 'RespondPage':
            raise GoTo(26007, clear_submitted=True, clear_page_data=True)          # retrieve responder edit page contents
        elif pinfo.item_type == 'FilePage':
            raise GoTo(29007, clear_submitted=True, clear_page_data=True)          # filepage edit page
    # no action recognised
    raise FailPage(message = "Requested action not recognised")



def choose_remove_action(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Choose to remove a page or folder, fills in confirm box"
    if ('ftree', 'contents') not in call_data:
        raise FailPage(message = "Requested action not recognised")
    action = call_data['ftree', 'contents']
    try:
        get_field_list = action.split('_')
        project = get_field_list[-2]
        itemnumber = int(get_field_list[-1])
        info = skilift.item_info(project, itemnumber)
    except:
        raise FailPage(message = "Item to remove not recognised")
    if not info:
        raise FailPage(message = "Item to remove not recognised")
    if itemnumber == 0:
        raise FailPage(message = "Cannot delete the root folder")
    # display the modal confirm box
    page_data['page_delete', 'hide'] = False
    page_data['page_delete', 'para_text'] = "Delete %s with ident %s and name %s" % (info.item_type, info.itemnumber, info.name)
    page_data['page_delete', 'get_field2_1'] = project + '_' + str(itemnumber)



def delete_item(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Deletes a folder or page"
    try:
        ident = call_data['page_delete','get_field2_1'].split('_')
        project = ident[0]
        itemnumber = int(ident[1])
        info = skilift.item_info(project, itemnumber)
    except:
        raise FailPage(message = "Item to remove not recognised")

    if not info:
        raise FailPage(message = "Item to remove not recognised")

    if itemnumber == 0:
        raise FailPage(message = "Cannot delete the root folder")

    if info.item_type == 'Folder':
        # call skilift.editfolder.delete_folder
        error = editfolder.delete_folder(project, itemnumber)
        if error:
            raise FailPage(message = "Unable to delete the folder")
        call_data['status'] = 'Folder deleted'
        return

    # If not a Folder, must be a page

    # call skilift.editpage.delete_page
    error = editpage.delete_page(project, itemnumber)
    if error:
        raise FailPage(message = "Unable to delete the page")

    # as page is deleted, this will affect any folder and page objects
    # stored in call_data, so clear them

    if 'page_number' in call_data:
        del call_data['page_number']
    if 'page' in call_data:
        del call_data['page']
    if 'folder' in call_data:
        del call_data['folder']

    call_data['status'] = 'Page deleted'
    


def submit_rename_folder(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "rename this folder"
    if 'folder_number' not in call_data:
        raise FailPage(message = "Folder missing")
    if 'name' not in call_data:
        raise FailPage(message="No new folder name has been given", widget="rename_folder")
    # Rename the folder
    error_message = editfolder.rename_folder(call_data['editedprojname'], call_data['folder_number'], call_data['name'])
    if error_message:
        raise FailPage(message=error_message, widget="rename_folder")
    call_data['status'] = 'Folder renamed'


def submit_folder_brief(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "set this folders brief"
    if 'folder_number' not in call_data:
        raise FailPage(message = "Folder missing")
    if 'brief' not in call_data:
        raise FailPage(message="No folder description available", widget="st2")
    # set folder brief
    error_message = editfolder.set_folder_brief(call_data['editedprojname'], call_data['folder_number'], call_data['brief'])
    if error_message:
        raise FailPage(message=error_message, widget="st2")
    call_data['status'] = 'Folder description set : %s' % (call_data['brief'],)


def submit_default_page(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Set this folder's default page"
    if 'folder_number' not in call_data:
        raise FailPage(message = "Folder missing")
    if 'selectvalue' not in call_data:
        raise FailPage(message="The page to set as default has not been found", widget="sdd1")
    if call_data['selectvalue'] == "-None-":
        default_page_name = ""
    else:
        default_page_name = call_data['selectvalue']
    error_message = editfolder.set_default_page(call_data['editedprojname'], call_data['folder_number'], default_page_name)
    if error_message:
        raise FailPage(message=error_message, widget="sdd1")
    call_data['status'] = 'Default page set'


def submit_restricted(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "set this folder as restricted"
    if 'folder_number' not in call_data:
        raise FailPage(message = "Folder missing")
    # restrict the folder
    error_message = editfolder.set_restricted_status(call_data['editedprojname'], call_data['folder_number'], True)
    if error_message:
        raise FailPage(message=error_message)
    call_data['status'] = 'Folder set to restricted access'


def submit_unrestricted(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "set this folder as unrestricted"
    if 'folder_number' not in call_data:
        raise FailPage(message = "Folder missing")
    # un-restrict the folder
    error_message = editfolder.set_restricted_status(call_data['editedprojname'], call_data['folder_number'], False)
    if error_message:
        raise FailPage(message=error_message)
    call_data['status'] = 'Folder set to unrestricted access'


def downloadfolder(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Gets folder, and returns a json dictionary, this will be sent as an octet file to be downloaded"
    if 'folder_number' not in call_data:
        raise FailPage(message = "Folder missing")
    jsonstring =  fromjson.folder_to_json(call_data['editedprojname'], call_data['folder_number'], indent=4)
    line_list = []
    n = 0
    for line in jsonstring.splitlines(True):
        binline = line.encode('utf-8')
        n += len(binline)
        line_list.append(binline)
    page_data['headers'] = [('content-type', 'application/octet-stream'), ('content-length', str(n))]
    return line_list



def _foldertree(projectname, foldernumber):
    """Returns contents list of lists with ftree table fields, with the given foldernumber of the folder at the top of
    the table"""

    finfo = folder_info(projectname, foldernumber)
    folder_path = item_info(projectname, foldernumber).path
    folder_ident = projectname + '_' + str(foldernumber)

    #   col 0 - text string, either text to display or button text
    #   col 1 - A 'style' string set on the td cell, if empty string, no style applied
    #   col 2 - Is button? If False only text will be shown, not a button, button class will not be applied
    #           If True a link to link_ident/json_ident will be set with button_class applied to it
    #   col 3 - The get field value of the button link, empty string if no get field

    # This creates a contents of cell's, each row of the table has eight columns
    contents = []

    # first cell is the folder URL, no style, Not a link, no get field
    contents.append( (folder_path, '', False, '') )
 
    # second cell is the folder ident number
    contents.append( (str(finfo.number), '', False, '') )

    # third cell is restricted or not
    if finfo.restricted:
        contents.append( ('R', 'width : 1%;text-align: center;color: black;background-color: red;', False, '') )
    else:
        contents.append( ('', '', False, '') )

    # fourth cell is the folder brief
    if len(finfo.brief)>40:
        contents.append( (finfo.brief[:35] + "...", '', False, '') )
    else:
        contents.append( (finfo.brief[:35], '', False, '') )

    # fifth cell is an Edit link
    # top folder does not have an edit link
    contents.append( ('', '', False, '') )

    # sixth cell is add folder
    contents.append( ('Add Folder', 'width : 1%;text-align: center;', True, 'add_folder_' + folder_ident)    )

    # seventh cell is add page
    contents.append( ('Add Page', 'width : 1%;text-align: center;', True, 'add_page_' + folder_ident) )

    # eighth cell is remove line - but no remove link for the top line
    contents.append( ('', '', False, '') )

    rownumber = 1

    # place all sub pages in rows beneath the folder
    if finfo.contains_pages:
        rownumber = _show_pages(contents, projectname, foldernumber, rownumber, 2)
    if finfo.contains_folders:
        rownumber = _show_folders(contents, projectname, foldernumber, rownumber, 2)
    return contents, rownumber


def _show_pages(contents, projectname, foldernumber, rownumber, indent):
    """Used to create pages  beneath the folder"""

    # pinfo attributes are 'name', 'number', 'restricted', 'brief', 'item_type', 'responder'

    ident = projectname + "_"
    padding = "padding-left : %sem;" % (indent,)

    for pinfo in pages(projectname, foldernumber):
        rownumber += 1
        page_ident = ident + str(pinfo.number)

        # first column is the page name, style includes padding, not a link, no get field
        contents.append( (pinfo.name, padding, False, '') )
 
        # second column is the page ident number, no style, not a link, no get field
        contents.append( (str(pinfo.number), '', False, '') )

        # third column is restricted or not
        if pinfo.restricted:
            contents.append( ('R', 'width : 1%;text-align: center;color: black;background-color: red;', False, '') )
        else:
            contents.append( ('', '', False, '') )

        # fourth cell is the page brief
        if len(pinfo.brief)>40:
            contents.append( (pinfo.brief[:35] + "...", '', False, '') )
        else:
            contents.append( (pinfo.brief[:35], '', False, '') )

        # fifth column is an Edit link
        contents.append( ('Edit', 'width: 1%;text-align: center;', True, 'edit_page_' + page_ident) )

        # sixth column is page type
        # seventh either empty or responder type

        if pinfo.item_type == 'TemplatePage':
            contents.append( ('TemplatePage', 'text-align: center;', False, '') )
            contents.append( ('', '', False, '') )
        elif pinfo.item_type == 'RespondPage':
            contents.append( ('RespondPage', 'text-align: center;', False, '') )
            contents.append( (pinfo.responder, 'text-align: center;', False, '') )
        elif pinfo.item_type == 'CSS':
            contents.append( ('CSS', 'text-align: center;', False, '') )
            contents.append( ('', '', False, '') )
        elif pinfo.item_type == 'JSON':
            contents.append( ('JSON', 'text-align: center;', False, '') )
            contents.append( ('', '', False, '') )
        elif pinfo.item_type == 'SVG':
            contents.append( ('SVG', 'text-align: center;', False, '') )
            contents.append( ('', '', False, '') )
        elif pinfo.item_type == 'FilePage':
            contents.append( ('FilePage', 'text-align: center;', False, '') )
            contents.append( ('', '', False, '') )
        else:
            raise ServerError(message="An unknown page type")

        # eighth column is remove page
        contents.append( ('Remove', 'width : 1%;text-align: center;', True, page_ident) )

    return rownumber


def _show_folders(contents, projectname, foldernumber, rownumber, indent):


    # finfo attributes are 'name', 'number', 'restricted', 'brief', 'contains_pages', 'contains_folders'

    ident = projectname + "_"
    padding = "padding-left : %sem;" % (indent,)

    for finfo in folders(projectname, foldernumber):
        rownumber += 1
        folder_ident = ident + str(finfo.number)

        # first column is the folder path from parent, with padding style, Not a link, no get field
        contents.append( (finfo.name+"/", padding, False, '') )

        # second column is the folder ident number, no style, not a link, no get field
        contents.append( (str(finfo.number), '', False, '') )

        # third column is restricted or not
        if finfo.restricted:
            contents.append( ('R', 'width : 1%;text-align: center;color: black;background-color: red;', False, '') )
        else:
            contents.append( ('', '', False, '') )

        # fourth cell is the folder brief
        if len(finfo.brief)>40:
            contents.append( (finfo.brief[:35] + "...", '', False, '') )
        else:
            contents.append( (finfo.brief[:35], '', False, '') )

        # fifth column is an Edit link
        contents.append( ('Edit', 'width: 1%;text-align: center;', True, 'edit_folder_' + folder_ident) )

        # sixth column is add folder
        contents.append( ('Add Folder', 'width : 1%;text-align: center;', True, 'add_folder_' + folder_ident) )

        # seventh column is add page
        contents.append( ('Add Page', 'width : 1%;text-align: center;', True, 'add_page_' + folder_ident) )

        # eighth column is remove line - but no remove if folder has contents
        if finfo.contains_pages or finfo.contains_folders:
            contents.append( ('', '', False, '') )
        else:
            contents.append( ('Remove', 'width : 1%;text-align: center;', True, folder_ident) )

        # place all sub pages in rows beneath the subfolder
        if finfo.contains_pages:
            rownumber = _show_pages(contents, projectname, finfo.number, rownumber, indent+1)

        if finfo.contains_folders:
            rownumber = _show_folders(contents, projectname, finfo.number, rownumber, indent+1)

    return rownumber



