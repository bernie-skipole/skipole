####### SKIPOLE WEB FRAMEWORK #######
#
# __init__.py  - skiadmin functions
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

import pkgutil, re, collections, uuid, os, random

from . import editfolders, editresponders, editpages, editcss, editfiles, editparts, css_styles, editspecialpages, editwidgets, editsections, editsectionplaces, edittextblocks, edittext, editvalidators

from .. import FailPage, GoTo, ValidateError, ServerError
from ...ski import skiboot

from ... import skilift
from ...skilift.fromjson import get_defaults
from ...skilift.editsection import sectionchange
from ...skilift.editpage import pagechange
from ...skilift.editfolder import folderchange
from ...skilift.editwidget import widget_modules

# a search for anything none-alphanumeric and not an underscore
_AN = re.compile('[^\w]')

# dictionary of session numbers as keys
# and values being a dictionary of items to carry over as session data
# 'page' or 'folder' as a tuple of its ident
# 'pchange', 'fchange', 'schange' as the page, folder, section integer change number
_SESSION_DATA = collections.OrderedDict()
_IDENT_DATA = 0



def start_project(project, projectfiles, path, option):
    """On a project being loaded, and before the wsgi service is started, this is called once,
       Note: it may be called multiple times if your web server starts multiple processes.
       This function should return a dictionary (typically an empty dictionary if this value is not used).
       Can be used to set any initial parameters, and the dictionary returned will be passed as
       'proj_data' to subsequent start_call functions."""

    # get pallet of colours from defaults.json and place in proj_data
    # these will be used to populate w3-theme-ski.css and the Colours page

    adminbackcol = get_defaults(project, key="backcol")
    if not adminbackcol:
        adminbackcol = "#bfb786"
    colours = get_defaults(project, key="colours")
    if not colours:
        adminbackcol_rgb = css_styles.hex_int(adminbackcol)
        colours = css_styles.get_colours(*adminbackcol_rgb)
    return {"colours":colours, "adminbackcol":adminbackcol}



def start_call(environ, path, project, called_ident, caller_ident, received_cookies, ident_data, lang, option, proj_data):
    "Checks initial incoming call parameters, and using ident_data, retrieves session data and populates call_data"

    # initially populate call_data with some project info
    editedprojname = skilift.get_root()

    projinfo = skilift.project_info(editedprojname)

    call_data = {'editedprojname':editedprojname,
                 'editedprojurl':projinfo.path,
                 'editedprojversion':projinfo.version,
                 'editedprojbrief':projinfo.brief,
                 'adminproj':project,
                 'extend_nav_buttons':[],
                 'caller_ident':caller_ident}

    page_data = {}

    # The tar.gz file, being dynamically created, does not have a called_ident, so if called_ident is None,
    # check the path is a request for the tar.gz file, and route the call to the responder which sets the file
    # to be returned in a file page

    if called_ident is None:
        tarfile = editedprojname + ".tar.gz"
        if path.endswith(tarfile):
            # request is for the edited project tar.gz
            return 90, call_data, page_data, lang
        # else the call is to a url not found
        return None, {}, {}, lang

    # If caller_ident is not given there should be no further session data
    if not caller_ident:
        return called_ident, call_data, page_data, lang

    # get the called_ident page number
    projname, identnum = called_ident

    # If the called page does not use session data, do not bother getting any
    if identnum in (
                       1,         # index page
                      90,         # tar file
                    4001,         # manage textblocks
                    4010,         # edit textblock
                    5001,         # manage special pages
                    7001,         # manage sections
                   80001          # operations
                    ):
        return called_ident, call_data, page_data, lang

    # get session data from received ident_data
    if ident_data in _SESSION_DATA:
        session_data = _SESSION_DATA[ident_data]
    else:
        session_data = {}

    if identnum == 7030:
        if 'section_name' in session_data:
            call_data['section_name'] = session_data['section_name']
            call_data['schange'] = session_data['schange']
        return called_ident, call_data, page_data, lang

    if identnum == 2003:
        if 'folder_number' in session_data:
            call_data['folder_number'] = session_data['folder_number']
            call_data['fchange'] = session_data['fchange']
            return called_ident, call_data, page_data, lang
        else:
            return "admin_home", call_data, page_data, lang

    # set the received session data into the call_data dictionary

    if 'location' in session_data:
        # Set a list of leading string, container integer (or None) and location tuple in call_data
        call_data['location'] = session_data['location']
        if 'field_arg' in session_data:
            if not _AN.search(session_data['field_arg']):
                call_data['field_arg'] = session_data['field_arg']

    # When creating a new widget, a widget class is chosen
    if 'widgetclass' in session_data:
        call_data['widgetclass'] = session_data['widgetclass']

    if 'field_arg' in session_data:
        call_data['field_arg'] = session_data['field_arg']

    if 'validx' in session_data:
        try:
            validx = int(session_data['validx'])
        except:
            # validx is rejected
            pass
        else:
            call_data['validx'] = session_data['validx']


    if 'module' in session_data:
        # module should be a widget module
        # If ok, set module string into call_data
        if session_data['module'] in widget_modules():
            call_data['module'] = session_data['module']

    # either a section is being edited, or a folder/page - not both
    if ('section_name' in session_data) and ('page_number' in session_data):
        return "admin_home", call_data, page_data, lang

    if 'section_name' in session_data:
        call_data['section_name'] = session_data['section_name']
        call_data['schange'] = session_data['schange']
    elif 'page_number' in session_data:
        call_data['page_number'] = session_data['page_number']
        call_data['pchange'] = session_data['pchange']


    if 'widget_name' in session_data:
        call_data['widget_name'] = session_data['widget_name']

    if 'container' in session_data:
        call_data['container'] = session_data['container']

    if 'folder_number' in session_data:
        call_data['folder_number'] = session_data['folder_number']
        call_data['fchange'] = session_data['fchange']

    if 'add_to_foldernumber' in session_data:
        call_data['add_to_foldernumber'] = session_data['add_to_foldernumber']

    return called_ident, call_data, page_data, lang


def submit_data(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Call the appropriate submit_data function"

    # routes to appropriate function depending on submit_list
    if submit_list and (len(submit_list) > 2):
        if submit_list[0] == 'editfolders':
            return editfolders.submit_data(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang)
        elif submit_list[0] == 'editresponders':
            return editresponders.submit_data(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang)
        elif submit_list[0] == 'editpages':
            return editpages.submit_data(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang)
        elif submit_list[0] == 'editcss':
            return editcss.submit_data(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang)
        elif submit_list[0] == 'editfiles':
            return editfiles.submit_data(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang)
        elif submit_list[0] == 'editparts':
            return editparts.submit_data(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang)
        elif submit_list[0] == 'editspecialpages':
            return editspecialpages.submit_data(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang)
        elif submit_list[0] == 'editwidgets':
            return editwidgets.submit_data(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang)
        elif submit_list[0] == 'editsections':
            return editsections.submit_data(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang)
        elif submit_list[0] == 'editsectionplaces':
            return editsectionplaces.submit_data(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang)
        elif submit_list[0] == 'edittextblocks':
            return edittextblocks.submit_data(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang)
        elif submit_list[0] == 'edittext':
            return edittext.submit_data(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang)
        elif submit_list[0] == 'editvalidators':
            return editvalidators.submit_data(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang)

    raise ServerError("submit_data function not found for responder %s,%s" % ident_list[-1])


def end_call(page_ident, page_type, call_data, page_data, proj_data, lang):
    """Stores session data under a random generated key in _SESSION_DATA and send the key as ident_data
       Also limits the length of _SESSION_DATA by popping the oldest member"""

    global _SESSION_DATA, _IDENT_DATA

    # do not include session data for these types of pages
    if page_type in ('FilePage', 'CSS'):
        return

    editedprojname = call_data['editedprojname']

    projname, identnum = page_ident

    # do not include session data if target page is in another project
    if projname != skilift.admin_project():
        return

    if page_type == "TemplatePage":
        # header information
        if ("adminhead","page_head","large_text") not in page_data:
            page_data["adminhead","page_head","large_text"] = "Project: %s version: %s" % (editedprojname, call_data['editedprojversion'])
        # fill in navigation information
        set_navigation(identnum, call_data, page_data)

    # Show the status message
    if 'status' in call_data:
        page_data['foot', 'foot_status','footer_text'] = call_data['status']
        page_data[("adminhead","show_status","para_text")] = call_data['status']
        page_data[("adminhead","show_status","hide")] = False


    # do not send any session data for the following pages
 
    if identnum in (
                    4,               # help json file
                    20001,           # index_template
                    20041,           # project saved json file
                    24001,           # textblock_management
                    24019,           # edit textblock
                    25001,           # special page management
                    27001,           # manage sections
                    70150,           # json of textblock contents
                    80001):          # operations template
        return

    # for all other pages, store the data from call_data

    sent_session_data = {}

    if 'location' in call_data:
        sent_session_data['location'] = call_data['location']

    if 'field_arg' in call_data:
        sent_session_data['field_arg'] = call_data['field_arg']

    if 'validx' in call_data:
        sent_session_data['validx'] = call_data['validx']

    if 'module' in call_data:
        sent_session_data['module'] = call_data['module']

    if 'widgetclass' in call_data:
        sent_session_data['widgetclass'] = call_data['widgetclass']

    if 'widget_name' in call_data:
        sent_session_data['widget_name'] = call_data['widget_name']

    if 'container' in call_data:
        sent_session_data['container'] = call_data['container']

    if 'add_to_foldernumber' in call_data:
        sent_session_data['add_to_foldernumber'] = call_data['add_to_foldernumber']


    # either a section is being edited, or a folder/page - not both
    if ('section_name' in call_data) and ('schange' in call_data):
        sent_session_data['section_name'] = call_data['section_name']
        sent_session_data['schange'] = call_data['schange']
    else:
        # send page or folder as a tuple of its ident
        if ('page_number' in call_data) and ('pchange' in call_data):
            sent_session_data['page_number'] = call_data['page_number']
            sent_session_data['pchange'] = call_data['pchange']

        if ('folder_number' in call_data) and ('fchange' in call_data):
            sent_session_data['folder_number'] = call_data['folder_number']
            sent_session_data['fchange'] = call_data['fchange']

    if sent_session_data:
        # store in _SESSION_DATA, and send the key as ident_data
        # generate a key
        _IDENT_DATA += 1
        if "ident_data" in call_data:
            ident_data = str(_IDENT_DATA) + "a" + str(random.randrange(1000, 9999)) + "b" + str(call_data["ident_data"])
        else:
            ident_data = str(_IDENT_DATA) + "a" + str(random.randrange(1000, 9999)) + "b0"
        _SESSION_DATA[ident_data] = sent_session_data
        # if length of _SESSION_DATA is longer than 50, remove old values
        if len(_SESSION_DATA)>50:
            _SESSION_DATA.popitem(last=False)
        page_data['ident_data'] = ident_data
    return


def set_navigation(identnum, call_data, page_data):
    "Sets the navigation buttons"

    # top navigation

    page_data["adminhead","top_nav","nav_links"] = [ [3, "Root Folder", False, ''] ]

    editedprojname = call_data['editedprojname']

    item_number = None

    if 'page_number' in call_data:
        item_number = call_data['page_number']
    elif 'folder_number' in call_data:
        item_number = call_data['folder_number']

    if item_number:
        # get list of [(name,number),...] of parents
        parents = skilift.parent_list(editedprojname, item_number)
        for item in parents:
            # for each item apart from root
            if item[1]:
                edited_folder = editedprojname + '_' + str(item[1])
                page_data["adminhead","top_nav","nav_links"].append(['edit_from_top_nav', item[0], False, edited_folder])
    # Top navigation lists in reverse order as the float right keeps making the next link the rightmost
    page_data["adminhead","top_nav","nav_links"].reverse()


    # Left navigation

    # uses a headers.NavButtons1 widget, each inner list consists of

    # 0 : The url, label or ident of the target page of the link
    # 1 : The displayed text of the link
    # 2 : If True, ident_data is sent with the link even if there is no get field data
    # 3 : The get field data to send with the link 

    if identnum == 20001:
        # main site index page
        page_data["left_nav","navbuttons","nav_links"] = [  [call_data['editedprojurl'], "Project", False, ''],
                                                            [3, "Root Folder", False, ''],
                                                            ["manage_specialpages", "Page Labels", False, ''],
                                                            ["manage_textblocks", "TextBlocks", False, ''],
                                                            ["manage_sections", "Sections", False, ''],
                                                            [300, "Colours", False, ''],
                                                            ['operations', "Operations", False, ''],
                                                            ["about_code", "Python Code", False, '']
                                                           ]
    elif identnum == 80001:
        # operations index page
        page_data["left_nav","navbuttons","nav_links"] = [  [call_data['editedprojurl'], "Project", False, ''],
                                                            ['admin_home', "Admin", False, ''],
                                                            [3, "Root Folder", False, ''],
                                                            ["manage_specialpages", "Page Labels", False, ''],
                                                            ["manage_textblocks", "TextBlocks", False, ''],
                                                            ["manage_sections", "Sections", False, '']
                                                           ]
    elif identnum == 20300:
        # colours index page
        page_data["left_nav","navbuttons","nav_links"] = [  [call_data['editedprojurl'], "Project", False, ''],
                                                            ['admin_home', "Admin", False, ''],
                                                            [3, "Root Folder", False, ''],
                                                            ["manage_specialpages", "Page Labels", False, ''],
                                                            ["manage_textblocks", "TextBlocks", False, ''],
                                                            ["manage_sections", "Sections", False, ''],
                                                            ['operations', "Operations", False, '']
                                                           ]

    elif identnum == 70101:
        # about code page
        page_data["left_nav","navbuttons","nav_links"] = [  [call_data['editedprojurl'], "Project", False, ''],
                                                            ['admin_home', "Admin", False, ''],
                                                            [3, "Root Folder", False, ''],
                                                            ["manage_specialpages", "Page Labels", False, ''],
                                                            ["manage_textblocks", "TextBlocks", False, ''],
                                                            ["manage_sections", "Sections", False, '']
                                                           ]

    elif identnum == 25001:
        # page labels
        page_data["left_nav","navbuttons","nav_links"] = [  [call_data['editedprojurl'], "Project", False, ''],
                                                            ['admin_home', "Admin", False, ''],
                                                            [3, "Root Folder", False, ''],
                                                            ["manage_textblocks", "TextBlocks", False, ''],
                                                            ["manage_sections", "Sections", False, ''],
                                                            ['operations', "Operations", False, '']
                                                           ]


    elif ("left_nav","navbuttons","nav_links") not in page_data:
        # all other page have full suite of navigation buttons
        page_data["left_nav","navbuttons","nav_links"] = [  [call_data['editedprojurl'], "Project", False, ''],
                                                            ['admin_home', "Admin", False, ''],
                                                            [3, "Root Folder", False, ''],
                                                            ["manage_specialpages", "Page Labels", False, ''],
                                                            ["manage_textblocks", "TextBlocks", False, ''],
                                                            ["manage_sections", "Sections", False, '']
                                                           ]

    widget_info = None

    if item_number:
        item_info = skilift.item_info(editedprojname, item_number)
        if item_info:
            if (item_info.item_type == 'TemplatePage') or (item_info.item_type == 'SVG'):
                # add page name to navbuttons
                page_data["left_nav","navbuttons","nav_links"].append(['back_to_page', item_info.name, True, ''])
                if item_info.item_type == 'TemplatePage':
                    page_data["left_nav","navbuttons","nav_links"].append(['page_head', item_info.name + ' - Head', True, ''])
                    page_data["left_nav","navbuttons","nav_links"].append(['page_body', item_info.name + ' - Body', True, ''])
                if item_info.item_type == 'SVG':
                    page_data["left_nav","navbuttons","nav_links"].append(['page_svg', 'SVG', True, ''])
                if ('widget_name' in call_data) and ((item_info.item_type == 'TemplatePage') or (item_info.item_type == 'SVG')):
                    widget_info = skilift.widget_info(editedprojname, item_number, None, call_data['widget_name'])

    elif 'section_name' in call_data:
        page_data["left_nav","navbuttons","nav_links"].append(['back_to_section', call_data['section_name'], True, ''])
        if 'widget_name' in call_data:
            widget_info = skilift.widget_info(editedprojname, None, call_data['section_name'], call_data['widget_name'])

    if widget_info:
        # if widget has parent, dsiplay parent links
        display_parent(widget_info, page_data)
        page_data["left_nav","navbuttons","nav_links"].append(['retrieve_widget', widget_info.name, True, widget_info.name])
        # if widget has containers, display links to them
        if widget_info.containers:
            for cont in range(widget_info.containers):
                str_cont = str(cont)
                page_data["left_nav","navbuttons","nav_links"].append(['retrieve_container', widget_info.name + " " + str_cont, True, widget_info.name + "-" + str_cont])

    # add further buttons which may be set in call_data['extend_nav_buttons']
    if 'extend_nav_buttons' in call_data:
        if call_data['extend_nav_buttons']:
            page_data["left_nav","navbuttons","nav_links"].extend(call_data['extend_nav_buttons'])


def display_parent(widget_info, page_data):
    "Appends link to parent widget in navigation buttons"
    location = widget_info.location
    # location is (parent, container, location integers) where parent is section_name, head/body or parent widget name
    # if container is None then there is no parent widget
    if location[1] is None:
        return
    # widget is in a container
    # does the parent have parents?
    parent_name = location[0]
    parent_info = skilift.widget_info(widget_info.project, widget_info.pagenumber, widget_info.section_name, parent_name)
    # recursively display grandparents
    display_parent(parent_info, page_data)
    # display links to the parent widget
    page_data["left_nav","navbuttons","nav_links"].append(['retrieve_widget', parent_name, True, parent_name])
    page_data["left_nav","navbuttons","nav_links"].append(['retrieve_container', parent_name + " " + str(location[1]), True, parent_name + "-" + str(location[1])])






