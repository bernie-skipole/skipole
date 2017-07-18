####### SKIPOLE WEB FRAMEWORK #######
#
# foldertree.py  - produces content for foldertree table
#
# This file is part of the Skipole web framework
#
# Date : 20170512
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

import collections, json, os

from ....ski import skiboot
from ....ski.excepts import ServerError
from ....skilift import pages, folders, folder_info, item_info


def foldertree(projectname, foldernumber):
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


