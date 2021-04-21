

import os, sys, re, json, pathlib


from .. import WSGIApplication, FailPage, GoTo, ValidateError, ServerError, use_submit_list, set_debug, skilift
from ..skilift.fromjson import get_defaults_from_file

from ..ski.project_class_definition import SectionData, PageData

from . import skiadminpackages

PROJECTFILES = os.path.dirname(os.path.realpath(__file__))
PROJECT = 'skiadmin'

# a search for anything none-alphanumeric and not an underscore
_AN = re.compile('[^\w]')



def start_call(called_ident, skicall):
    "Checks initial incoming call parameters, and using ident_data, retrieves session data and populates call_data"
     

    # initially populate call_data with some project info
    editedprojname = skicall.proj_data['editedprojname']

    projinfo = skilift.project_info(editedprojname)

    if (called_ident is not None) and (called_ident[1] == 80040):
        # does not call page 80040 (which is a nop which would return page not found)
        # instead it returns the server file defaults.json of the editedproject 
        defaults_json = pathlib.Path(projinfo.data_path, "defaults.json")
        pd = PageData()
        pd.mimetype = "application/octet-stream"
        skicall.update(pd)
        return defaults_json


    skicall.call_data = {'editedprojname':editedprojname,
                         'editedprojurl':projinfo.path,
                         'editedprojversion':projinfo.version,
                         'editedprojbrief':projinfo.brief,
                         'adminproj':skicall.project,
                         'extend_nav_buttons':[],
                         'caller_ident':skicall.caller_ident,
                         'pagedata': PageData()}

    if called_ident is None:
        # The call is to a url not found
        return

    # If caller_ident is not given there should be no further session data
    if not skicall.caller_ident:
        return called_ident

    # session data is received from the client as a json dictionary via ident_data
    if skicall.ident_data:
        session_data = json.loads(skicall.ident_data)
        # update call_data with session_data
        skicall.call_data.update(session_data)

    return called_ident


# skicall.submit_list defines packages, module, function to call
@use_submit_list
def submit_data(skicall):
    """The decorator calls the appropriate submit_data function, using skicall.submit_list
       if skicall.submit_list is invalid, then this function raises ServerError"""
    raise ServerError("skicall.submit_list invalid for responder %s,%s" % skicall.ident_list[-1])


def end_call(page_ident, page_type, skicall):
    """Sets navigation menus, and sends session data as ident_data."""

    # skicall.call_data['pagedata'] is a PageData object
    call_data = skicall.call_data
    pd = call_data['pagedata']

    skicall.update(pd)

    # do not include session data or navigation for these types of pages
    if page_type in ('FilePage', 'CSS'):
        return


    editedprojname = call_data['editedprojname']

    projname, identnum = page_ident

    # do not include session data if target page is in another project
    if projname != PROJECT:
        return

    # do not include session or navigation if this is the responder map page
    if identnum == 26010:
        return

    sd_adminhead = SectionData("adminhead")
    sd_foot = SectionData("foot")

    if page_type == "TemplatePage":
        # header information
        if not pd.get_value("adminhead","page_head","large_text"):
            sd_adminhead["page_head","large_text"] = "Project: %s version: %s" % (editedprojname, call_data['editedprojversion'])
        # fill in navigation information
        sd_left_nav = set_navigation(identnum, call_data, pd, sd_adminhead)
        skicall.update(sd_left_nav)
        sd_diagnostic = SectionData("diagnostic_footer")
        sd_diagnostic.show = True
        skicall.update(sd_diagnostic)
        

    # Show the status message
    if 'status' in call_data:
        sd_foot['foot_status','footer_text'] = call_data['status']
        sd_adminhead["show_status","para_text"] = call_data['status']
        sd_adminhead["show_status","hide"] = False

    skicall.update(sd_adminhead)
    skicall.update(sd_foot)


    # get any required session data which has been set into call_data
    # and pass it to the client as ident_data

    sent_session_data = {}

    # this is a list of items to store in session data if they are available in call_data
    session_keys = ['location', 'field_arg', 'validx', 'module', 'widgetclass', 'widget_name', 'container', 'add_to_foldernumber', 
                    'section_name', 'schange', 'page_number', 'pchange', 'folder_number', 'fchange']

    for key, val in call_data.items():
        if key in session_keys:
            sent_session_data[key] = val

    if not sent_session_data:
        return

    # and this dictionary is inserted into ident_data as a json string
    pd_ident = PageData()
    pd_ident.ident_data = json.dumps(sent_session_data)
    skicall.update(pd_ident)


# As this project is not intended to run as a stand-alone service, a function
# is provided rather than an application object being immediately created.


def makeapp(editedprojname):
    """This function returns the skiadmin application."""

    if not editedprojname:
        raise ServerError("The project name being edited is required")

    # get pallet of colours from defaults.json and place in proj_data
    # these will be used to populate w3-theme-ski.css and the Colours page

    adminbackcol = get_defaults_from_file(PROJECTFILES, PROJECT, key="backcol")
    if not adminbackcol:
        adminbackcol = "#bfb786"
    colours = get_defaults_from_file(PROJECTFILES, PROJECT, key="colours")
    if not colours:
        adminbackcol_rgb = skiadminpackages.css_styles.hex_int(adminbackcol)
        colours = skiadminpackages.css_styles.get_colours(*adminbackcol_rgb)


    proj_data = {"editedprojname":editedprojname, "colours":colours, "adminbackcol":adminbackcol}

    # The WSGIApplication created here is generally given a URL of "/skiadmin"
    # when added to the root project using application.add_project

    return WSGIApplication(project=PROJECT,
                           projectfiles=PROJECTFILES,
                           proj_data=proj_data,
                           start_call=start_call,
                           submit_data=submit_data,
                           end_call=end_call)


def set_navigation(identnum, call_data, pd, sd_adminhead):
    "Sets the navigation buttons, returns a left_nav SectionData object"

    sd = SectionData('left_nav')

    # top navigation

    sd_adminhead["top_nav","nav_links"] = [ [3, "Root", False, ''] ]

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
                sd_adminhead["top_nav","nav_links"].append(['edit_from_top_nav', item[0], False, edited_folder])
    # Top navigation lists in reverse order as the float right keeps making the next link the rightmost
    sd_adminhead["top_nav","nav_links"].reverse()


    # Left navigation

    # uses a headers.NavButtons1 widget, each inner list consists of

    # 0 : The url, label or ident of the target page of the link
    # 1 : The displayed text of the link
    # 2 : If True, ident_data is sent with the link even if there is no get field data
    # 3 : The get field data to send with the link 

    if identnum == 20001:
        # main site index page
        sd["navbuttons","nav_links"] = [    [call_data['editedprojurl'], "Project", False, ''],
                                            [3, "Root Folder", False, ''],
                                            ["manage_specialpages", "Page Labels", False, ''],
                                            ["manage_textblocks", "TextBlocks", False, ''],
                                            ["manage_sections", "Sections", False, ''],
                                            [300, "Colours", False, ''],
                                            ['defaults', "Defaults", False, ''],
                                            ["about_code", "Getting Started", False, '']
                                           ]
    elif identnum == 510:
        # about_skis page
        sd["navbuttons","nav_links"] = [    [call_data['editedprojurl'], "Project", False, ''],
                                            ['admin_home', "Admin", False, ''],
                                            [3, "Root Folder", False, ''],
                                            ["manage_specialpages", "Page Labels", False, ''],
                                            ["manage_textblocks", "TextBlocks", False, ''],
                                            ["manage_sections", "Sections", False, ''],
                                            [300, "Colours", False, ''],
                                            ['defaults', "Defaults", False, ''],
                                            ["about_code", "Getting Started", False, '']
                                           ]
    elif identnum == 85001:
        # operations index page
        sd["navbuttons","nav_links"] = [    [call_data['editedprojurl'], "Project", False, ''],
                                            ['admin_home', "Admin", False, ''],
                                            [3, "Root Folder", False, ''],
                                            ["manage_specialpages", "Page Labels", False, ''],
                                            ["manage_textblocks", "TextBlocks", False, ''],
                                            ["manage_sections", "Sections", False, ''],
                                            [300, "Colours", False, ''],
                                            ["about_code", "Getting Started", False, '']
                                           ]
    elif identnum == 20300:
        # colours index page
        sd["navbuttons","nav_links"] = [    [call_data['editedprojurl'], "Project", False, ''],
                                            ['admin_home', "Admin", False, ''],
                                            [3, "Root Folder", False, ''],
                                            ["manage_specialpages", "Page Labels", False, ''],
                                            ["manage_textblocks", "TextBlocks", False, ''],
                                            ["manage_sections", "Sections", False, ''],
                                            ['defaults', "Defaults", False, ''],
                                            ["about_code", "Getting Started", False, '']
                                           ]

    elif identnum == 70101:
        # about code page
        sd["navbuttons","nav_links"] = [    [call_data['editedprojurl'], "Project", False, ''],
                                            ['admin_home', "Admin", False, ''],
                                            [3, "Root Folder", False, ''],
                                            ["manage_specialpages", "Page Labels", False, ''],
                                            ["manage_textblocks", "TextBlocks", False, ''],
                                            ["manage_sections", "Sections", False, ''],
                                            [300, "Colours", False, ''],
                                            ['defaults', "Defaults", False, '']
                                           ]

    elif identnum == 25001:
        # page labels
        sd["navbuttons","nav_links"] = [    [call_data['editedprojurl'], "Project", False, ''],
                                            ['admin_home', "Admin", False, ''],
                                            [3, "Root Folder", False, ''],
                                            ["manage_textblocks", "TextBlocks", False, ''],
                                            ["manage_sections", "Sections", False, ''],
                                            ['defaults', "Defaults", False, '']
                                           ]


    elif not pd.get_value("left_nav","navbuttons","nav_links"):
        # all other page have full suite of navigation buttons
        sd["navbuttons","nav_links"] = [    [call_data['editedprojurl'], "Project", False, ''],
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
                    sd["navbuttons","nav_links"].append(['back_to_page', item_info.name, True, ''])
                    sd["navbuttons","nav_links"].append(['page_head', item_info.name + ' - Head', True, ''])
                    sd["navbuttons","nav_links"].append(['page_body', item_info.name + ' - Body', True, ''])
                if item_info.item_type == 'SVG':
                    sd["navbuttons","nav_links"].append(['back_to_svgpage', item_info.name, True, ''])
                    sd["navbuttons","nav_links"].append(['page_svg', 'SVG', True, ''])
                if ('widget_name' in call_data) and ((item_info.item_type == 'TemplatePage') or (item_info.item_type == 'SVG')):
                    widget_info = skilift.widget_info(editedprojname, item_number, None, call_data['widget_name'])

    elif 'section_name' in call_data:
        sd["navbuttons","nav_links"].append(['back_to_section', call_data['section_name'], True, ''])
        if 'widget_name' in call_data:
            widget_info = skilift.widget_info(editedprojname, None, call_data['section_name'], call_data['widget_name'])

    if widget_info:
        # if widget has parent, display parent links
        display_parent(widget_info, sd)
        sd["navbuttons","nav_links"].append(['retrieve_widget', widget_info.name, True, widget_info.name])
        # if widget has containers, display links to them
        if widget_info.containers:
            for cont in range(widget_info.containers):
                str_cont = str(cont)
                sd["navbuttons","nav_links"].append(['retrieve_container', widget_info.name + " " + str_cont, True, widget_info.name + "-" + str_cont])

    # add further buttons which may be set in call_data['extend_nav_buttons']
    if 'extend_nav_buttons' in call_data:
        if call_data['extend_nav_buttons']:
            sd["navbuttons","nav_links"].extend(call_data['extend_nav_buttons'])

    return sd


def display_parent(widget_info, sd):
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
    display_parent(parent_info, sd)
    # display links to the parent widget
    sd["navbuttons","nav_links"].append(['retrieve_widget', parent_name, True, parent_name])
    sd["navbuttons","nav_links"].append(['retrieve_container', parent_name + " " + str(location[1]), True, parent_name + "-" + str(location[1])])


