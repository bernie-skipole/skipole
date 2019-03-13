####### SKIPOLE WEB FRAMEWORK #######
#
# Th skiadmin application
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

import os, sys, re, collections, uuid, random

# This project needs to import the skipole package, which
# should normally be immediately available if skipole
# has been installed on your system. However if it has not
# then skipole must be added to your path with the following
# lines - and with the skipole_package_location set to the
# directory containing the skipole package

skipole_package_location = "/home/bernie/myprojects"
if skipole_package_location not in sys.path:
    sys.path.append(skipole_package_location)



from skipole import WSGIApplication, FailPage, GoTo, ValidateError, ServerError, use_submit_list, set_debug

from skipole import skilift
from skipole.skilift.fromjson import get_defaults_from_file

import skiadminpackages

PROJECT = 'skiadmin'

# a search for anything none-alphanumeric and not an underscore
_AN = re.compile('[^\w]')

# dictionary of session numbers as keys
# and values being a dictionary of items to carry over as session data
# 'page' or 'folder' as a tuple of its ident
# 'pchange', 'fchange', 'schange' as the page, folder, section integer change number
_SESSION_DATA = collections.OrderedDict()
_IDENT_DATA = 0



def start_call(called_ident, skicall):
    "Checks initial incoming call parameters, and using ident_data, retrieves session data and populates call_data"

    # initially populate call_data with some project info
    editedprojname = skilift.get_root()

    projinfo = skilift.project_info(editedprojname)

    skicall.call_data = {'editedprojname':editedprojname,
                         'editedprojurl':projinfo.path,
                         'editedprojversion':projinfo.version,
                         'editedprojbrief':projinfo.brief,
                         'adminproj':skicall.project,
                         'extend_nav_buttons':[],
                         'caller_ident':skicall.caller_ident}

    # The tar.gz file, being dynamically created, does not have a called_ident, so if called_ident is None,
    # check the path is a request for the tar.gz file, and route the call to the responder which sets the file
    # to be returned in a file page

    if called_ident is None:
        tarfile = editedprojname + ".tar.gz"
        if skicall.path.endswith(tarfile):
            # request is for the edited project tar.gz
            return 90
        # else the call is to a url not found
        return

    # If caller_ident is not given there should be no further session data
    if not skicall.caller_ident:
        return called_ident

    # if ident_data is given, then session data can be found in _SESSION_DATA[ident_data]
    # so this is added to call_data

    ident_data = skicall.ident_data

    if (ident_data) and (ident_data in _SESSION_DATA):
        # update call_data with session_data
        skicall.call_data.update(_SESSION_DATA[ident_data])

    return called_ident


# submit_list defines packages, module, function to call
@use_submit_list
def submit_data(skicall):
    "The decorator calls the appropriate submit_data function, if submit_list is invalid, then this function raises ServerError"
    raise ServerError("submit_list invalid for responder %s,%s" % skicall.ident_list[-1])


def end_call(page_ident, page_type, skicall):
    """Sets navigation menus, and stores session data under a random generated key in _SESSION_DATA and send the key as ident_data
       Also limits the length of _SESSION_DATA by popping the oldest member"""

    global _SESSION_DATA, _IDENT_DATA

    # do not include session data or navigation for these types of pages
    if page_type in ('FilePage', 'CSS'):
        return

    call_data = skicall.call_data
    page_data = skicall.page_data

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


    # store any required session data which has been set into call_data

    sent_session_data = {}

    # this is a list of items to store in session data if they are available in call_data
    session_keys = ['location', 'field_arg', 'validx', 'module', 'widgetclass', 'widget_name', 'container', 'add_to_foldernumber', 
                    'section_name', 'schange', 'page_number', 'pchange', 'folder_number', 'fchange']

    for key, val in call_data.items():
        if key in session_keys:
            sent_session_data[key] = val

    if not sent_session_data:
        return

    # store as a key:value in _SESSION_DATA, and send the key as ident_data
    # this key will be saved in the returned page, and then sent back in the next call to the server
    # on being received by the start_call function, the key will be used to read the session values
    # from _SESSION_DATA

    # generate a key, being a combination of incrementing _IDENT_DATA and a random number
    _IDENT_DATA += 1
    ident_data_key = str(_IDENT_DATA) + "a" + str(random.randrange(1000, 9999))
    _SESSION_DATA[ident_data_key] = sent_session_data
    # if length of _SESSION_DATA is longer than 50, remove old values,
    # this expires old sessions
    if len(_SESSION_DATA)>50:
        _SESSION_DATA.popitem(last=False)
    page_data['ident_data'] = ident_data_key


def makeapp(projectfiles, proj_data={}):
    """This particular sub project does not know where its projectfiles are, so this function
       is called to provide that info, and returns the application
       skiadmin makes use of some color values, so these are set here and passed to the project
       as proj_data"""

    # get pallet of colours from defaults.json and place in proj_data
    # these will be used to populate w3-theme-ski.css and the Colours page

    adminbackcol = get_defaults_from_file(projectfiles, PROJECT, key="backcol")
    if not adminbackcol:
        adminbackcol = "#bfb786"
    colours = get_defaults_from_file(projectfiles, PROJECT, key="colours")
    if not colours:
        adminbackcol_rgb = skiadminpackages.css_styles.hex_int(adminbackcol)
        colours = skiadminpackages.css_styles.get_colours(*adminbackcol_rgb)


    return WSGIApplication(project=PROJECT,
                           projectfiles=projectfiles,
                           proj_data={"colours":colours, "adminbackcol":adminbackcol},
                           start_call=start_call,
                           submit_data=submit_data,
                           end_call=end_call,
                           url="/" + PROJECT)


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
    elif (identnum == 510) or (identnum == 20500) or (identnum == 70105):
        # about_lib page, about tar page, about skilift
        page_data["left_nav","navbuttons","nav_links"] = [  [call_data['editedprojurl'], "Project", False, ''],
                                                            ['admin_home', "Admin", False, ''],
                                                            [3, "Root Folder", False, ''],
                                                            ["manage_specialpages", "Page Labels", False, ''],
                                                            ["manage_textblocks", "TextBlocks", False, ''],
                                                            ["manage_sections", "Sections", False, ''],
                                                            [300, "Colours", False, ''],
                                                            ['operations', "Operations", False, ''],
                                                            ["about_code", "Python Code", False, '']
                                                           ]
    elif identnum == 85001:
        # operations index page
        page_data["left_nav","navbuttons","nav_links"] = [  [call_data['editedprojurl'], "Project", False, ''],
                                                            ['admin_home', "Admin", False, ''],
                                                            [3, "Root Folder", False, ''],
                                                            ["manage_specialpages", "Page Labels", False, ''],
                                                            ["manage_textblocks", "TextBlocks", False, ''],
                                                            ["manage_sections", "Sections", False, ''],
                                                            [300, "Colours", False, ''],
                                                            ["about_code", "Python Code", False, '']
                                                           ]
    elif identnum == 20300:
        # colours index page
        page_data["left_nav","navbuttons","nav_links"] = [  [call_data['editedprojurl'], "Project", False, ''],
                                                            ['admin_home', "Admin", False, ''],
                                                            [3, "Root Folder", False, ''],
                                                            ["manage_specialpages", "Page Labels", False, ''],
                                                            ["manage_textblocks", "TextBlocks", False, ''],
                                                            ["manage_sections", "Sections", False, ''],
                                                            ['operations', "Operations", False, ''],
                                                            ["about_code", "Python Code", False, '']
                                                           ]

    elif identnum == 70101:
        # about code page
        page_data["left_nav","navbuttons","nav_links"] = [  [call_data['editedprojurl'], "Project", False, ''],
                                                            ['admin_home', "Admin", False, ''],
                                                            [3, "Root Folder", False, ''],
                                                            ["manage_specialpages", "Page Labels", False, ''],
                                                            ["manage_textblocks", "TextBlocks", False, ''],
                                                            ["manage_sections", "Sections", False, ''],
                                                            [300, "Colours", False, ''],
                                                            ['operations', "Operations", False, '']
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
                if item_info.item_type == 'TemplatePage':
                    page_data["left_nav","navbuttons","nav_links"].append(['back_to_page', item_info.name, True, ''])
                    page_data["left_nav","navbuttons","nav_links"].append(['page_head', item_info.name + ' - Head', True, ''])
                    page_data["left_nav","navbuttons","nav_links"].append(['page_body', item_info.name + ' - Body', True, ''])
                if item_info.item_type == 'SVG':
                    page_data["left_nav","navbuttons","nav_links"].append(['back_to_svgpage', item_info.name, True, ''])
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




# In normal use, the skiadmin project is only imported, so the following is never run.
# However if you want to use skiadmin to modify itself, then it could be run like any other
# project, however it's something of a risky business!

if __name__ == "__main__":

    PROJECTFILES = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

    set_debug(True)

    application = makeapp(PROJECTFILES)

    skis_code = os.path.join(PROJECTFILES, 'skis', 'code')
    if skis_code not in sys.path:
        sys.path.append(skis_code)
    import skis
    skis_application = skis.makeapp(PROJECTFILES)
    application.add_project(skis_application, url='/'+ PROJECT + '/skis')


    from wsgiref.simple_server import make_server

    # serve the application
    host = "127.0.0.1"
    port = 8000

    httpd = make_server(host, port, application)
    print("Serving %s on port %s , go to url /%s to edit." % (PROJECT, port, PROJECT))
    httpd.serve_forever()


