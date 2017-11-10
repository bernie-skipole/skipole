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

import pkgutil, re, collections, uuid, os

from . import editfolders, editresponders, editpages, editcss, editfiles, editparts, css_styles, editspecialpages, editwidgets

from .editfolders import editproject, addpage
from .editpages import common, editpage, insert
from .editresponders import editrespondpage
from .editfiles import editfile
from .edittextblocks import managetextblocks, edittextblockrefs
from .editspecialpages import managespecialpages
from .editsections import managesections
from .editsectionplaces import editplaceholder
from .edittext import edittext
from .editparts import editpart, insertpart
from .editwidgets import editwidget, listwidgets
from .editvalidators import editvalidator


from .. import FailPage, GoTo, ValidateError, ServerError
from ...ski import skiboot, widgets
from ... import skilift
from ...skilift import fromjson

# a search for anything none-alphanumeric and not an underscore
_AN = re.compile('[^\w]')

# List of widget modules
_MODULES_TUPLE = tuple(name for (module_loader, name, ispkg) in pkgutil.iter_modules(widgets.__path__))

# dictionary of session numbers as keys
# and values being a dictionary of items to carry over as session data
# 'page' or 'folder' as a tuple of its ident
# 'pchange', 'fchange', 'schange' as the page, folder, section integer change number
_SESSION_DATA = collections.OrderedDict()


# This dictionary maps responder ident numbers to the submit_data functions
# this method to eventually be replaced by responders with submit lists

_CALL_SUBMIT_DATA = {
                        2460: addpage.submit_copy_page,                 # copies an existing page to create a new one
                        2470: addpage.submit_upload_page,           # copies an uploaded page definition file to create a new one
                        3230: editpage.set_html_lang,                   # sets page html lang tag
                        3260: editpage.downloadpage,                      # downloads json file of given page ident
                        3510: editpage.move_up,                         # moves part upwards
                        3520: editpage.move_up_right,                   # moves part upwards and rightwards
                        3530: editpage.move_down,                       # moves part downwards
                        3540: editpage.move_down_right,                 # moves part downwards and rightwards
                        3710: editpage.set_json_cache,                  # sets json page cache setting
                        3720: editpage.remove_json_widgfield,                # remove widgfield and value from a json page
                        3730: editpage.add_json_widgfield,                # add widgfield and value to a json page
                        4001: managetextblocks.retrieve_link_table,     # fill manage text blocks page link table
                        4005: managetextblocks.retrieve_more,           # fill more text blocks link tables
                        4006: managetextblocks.retrieve_more,           # fill more text blocks link tables
                        6250: editrespondpage.set_validate_option,      # enables or disables validate option
                        6260: editrespondpage.set_submit_option,        # enables or disables submit option
                        6320: editrespondpage.set_single_field,         # sets the field, number = 1 option
                        7010: managesections.submit_new_section,        # creates a new section
                        7011: managesections.file_new_section,          # creates a new section from uploaded file
                        7050: managesections.downloadsection,           # downloads section as json file
                        7060: managesections.newsectionpage,            # populates the new section page
                       20101: editproject.submit_addproject,            # adds a project
                       20111: editproject.submit_removeproject,         # remove the project
                       20121: editproject.retrieve_edit_project,        # gets field data for edit project page
                       20139: editproject.submit_suburl,                # sets the url of a sub project
                       22307: addpage.retrieve_add_page,                # gets field data for add page
                       22410: addpage.submit_new_template,              # add a new template page
                       22420: addpage.retrieve_new_responder,           # gets data for creating a new responder
                       22425: addpage.submit_new_responder,             # add a new responder
                       22430: addpage.retrieve_new_svg,                 # gets data for creating a new svg image page
                       22439: addpage.submit_new_svg,                   # add a new svg
                       22440: addpage.submit_new_css,                   # add a new css page
                       22450: addpage.retrieve_new_file,                # gets data for creating a new filepage
                       22455: addpage.submit_new_file,                  # add a new file page
                       22460: addpage.retrieve_new_copypage,            # gets data for creating a page copy
                       22470: addpage.submit_new_json,                  # add a new json page
                       23039: common.submit_new_parent,                 # page given a new parent folder
                       23049: common.submit_page_brief,                 # page given a new brief
                       23229: editpage.submit_last_scroll,              # sets last scroll flag
                       23259: editpage.submit_default_error_widget,     # sets default error widget
                       23309: editpage.submit_backcol,                  # sets page background colour
                       23321: editpage.retrieve_page_head,              # gets data for page head
                       23341: editpage.retrieve_page_body,              # gets data for page body
                       23419: editpage.submit_cache,                    # sets cache header
                       23421: editpage.retrieve_page_svg,               # gets data for page svg
                       24003: managetextblocks.submit_new_textblock,    # adds a textblock from manage textblock page
                       24017: managetextblocks.retrieve_textblock,      # fill edit textblock page
                       24042: managetextblocks.submit_delete_language,  # deletes a textblock language
                       24051: managetextblocks.submit_delete_textblock, # deletes a textblock
                       24062: managetextblocks.submit_copy_textblock,   # copies a textblock
                       24103: managetextblocks.submit_text,             # inputs new text for a textblock
                       25109: managespecialpages.submit_special_page,   # edits a special system page
                       25209: managespecialpages.submit_special_page,   # edits a special jq page
                       25309: managespecialpages.submit_user_page,      # edits or deletes a special user page
                       26039: editrespondpage.submit_widgfield,         # sets widgfield
                       26079: editrespondpage.submit_fail_ident,        # sets the fail ident
                       26089: editrespondpage.add_allowed_caller,       # adds a new allowed caller
                       26099: editrespondpage.delete_allowed_caller,    # deletes an allowed caller
                       26109: editrespondpage.remove_field,             # removes responder field
                       26209: editrespondpage.add_field_value,          # adds a field and value
                       26219: editrespondpage.add_field,                # adds a field
                       26409: editrespondpage.delete_submit_list_string,# deletes an indexed string from the submit_list
                       26419: editrespondpage.add_submit_list_string,   # adds a string to the submit_list
                       27003: managesections.retrieve_managepage,       # fill sections management page
                       27022: managesections.delete_section,            # deletes a section
                       27047: managesections.retrieve_section_contents, # retrieves data for section contents page
                       29109: editfile.submit_new_filepath,             # sets new file path on a filepage
                       29209: editfile.submit_mimetype,                 # sets new mimetype on a filepage
                       29309: editfile.submit_cache,                    # sets cache header
                       41050: edittext.create_insert,                   # creates and inserts new text
                       41100: edittext.create_insert_symbol,            # creates new html symbol
                       41120: edittext.set_edit_symbol,                 # changes an html symbol
                       41200: edittext.create_insert_comment,           # creates new html comment
                       41220: edittext.set_edit_comment,                # changes an html comment
                       43050: editpart.remove_tag_attribute,            # removes the part attribute
                       43102: insert.retrieve_insert,                   # sets data into insert a part page
                       43103: insert.retrieve_append,                   # sets data into append a part page
                       43104: editpage.remove_part,                     # Removes an item from a page
                       44701: editwidget.empty_container,               # empty the container
                       51022: edittext.edit_text,                       # sets the new text
                       51017: edittext.retrieve_edittextpage,           # gets data for edit text page
                       51107: edittext.retrieve_edit_symbol,            # edits an html symbol
                       51207: edittext.retrieve_edit_comment,           # edits an html comment
                       52017: edittextblockrefs.retrieve_textblockref,  # gets data to edit a textblock ref
                       52060: edittextblockrefs.set_textblock,          # sets edited textblock value in a page
                       52507: edittextblockrefs.retrieve_insert,        # gets data for inserting a textblock reference
                       52607: edittextblockrefs.create_insert,          # inserts a textblock reference
                       53007: editpart.retrieve_editpart,               # gets data for edit a part page
                       53050: editpart.set_tag,                         # sets the part tag_name or brief
                       53507: insertpart.retrieve_insert,               # get data for insert a html tag page
                       53607: insertpart.create_insert,                 # create an html tag
                       54007: editwidget.retrieve_editwidget,           # gets data for edit a widget
                       54020: editwidget.retrieve_editfield,            # gets data for edit a widget field
                       54024: editwidget.set_field_name,                # sets the widget field name
                       54027: editwidget.set_field_value,               # sets the widget field value
                       54032: editwidget.set_widget_params,             # sets the widget name
                       54042: editwidget.set_widget_params,             # sets the widget brief
                       54507: listwidgets.retrieve_module_list,         # gets data for widget modules list page
                       54517: listwidgets.retrieve_widgets_list,        # gets data for widgets list page
                       54527: listwidgets.retrieve_new_widget,          # gets data for new widget page
                       54537: listwidgets.create_new_widget,            # creates the new widget
                       54706: editwidget.edit_container,                # edit a container
                       54721: editwidget.back_to_parent_container,      # get container
                       55007: editplaceholder.retrieve_editplaceholder, # gets data for editing a placeholder
                       55050: editplaceholder.set_placeholder,          # sets the placeholder section name, brief or alias
                       55507: editplaceholder.retrieve_insert,          # gets data for inserting a placeholder
                       55607: editplaceholder.create_insert,            # create a section placeholder
                       56007: editvalidator.retrieve_editvalidator,     # gets data for edit a validator page
                       56013: editvalidator.set_e_message,              # sets error message for a validator
                       56023: editvalidator.set_e_message_ref,          # sets error message reference for a validator
                       56033: editvalidator.set_displaywidget,          # sets error message reference for a validator
                       56043: editvalidator.set_allowed_value,          # adds an allowed value to a validator
                       56053: editvalidator.remove_allowed_value,       # removes an allowed value
                       56107: editvalidator.retrieve_arg,               # gets data for edit an argument page
                       56114: editvalidator.set_arg_value,              # sets the arg value
                       56203: editvalidator.move_up,                    # moves a validator upwards
                       56213: editvalidator.move_down,                  # moves a validator downwards
                       56223: editvalidator.remove_validator,           # removes a validator
                       56307: editvalidator.retrieve_validator_modules, # gets data for listing validator modules
                       56317: editvalidator.retrieve_validator_list,    # gets data for listing validators
                       56353: editvalidator.create_validator,           # creates new validator
                       70001: editproject.retrieve_about_code,          # retrieve content for about user code
                       70005: editproject.retrieve_about_skilift,       # retrieve content for about skilift
                       70010: editproject.retrieve_about_fromjson,      # retrieve content for about fromjson
                       70015: editproject.retrieve_about_editfolder,    # retrieve content for about editfolder
                       70020: editproject.retrieve_about_editpage,      # retrieve content for about editpage
                       70025: editproject.retrieve_about_editsection,   # retrieve content for about editsection
                       70050: editproject.get_text,                     # gets textblock text
                       70090: editproject.retrieve_about_off_piste      # retrieve content for about off_piste
                   }



def start_project(project, projectfiles, path, option):
    """On a project being loaded, and before the wsgi service is started, this is called once,
       Note: it may be called multiple times if your web server starts multiple processes.
       This function should return a dictionary (typically an empty dictionary if this value is not used).
       Can be used to set any initial parameters, and the dictionary returned will be passed as
       'proj_data' to subsequent start_call functions."""

    # get pallet of colours from defaults.json and place in proj_data
    # these will be used to populate w3-theme-ski.css and the Colours page

    adminbackcol = fromjson.get_defaults(project, key="backcol")
    if not adminbackcol:
        adminbackcol = "#bfb786"
    colours = fromjson.get_defaults(project, key="colours")
    if not colours:
        adminbackcol_rgb = css_styles.hex_int(adminbackcol)
        colours = css_styles.get_colours(*adminbackcol_rgb)
    return {"colours":colours, "adminbackcol":adminbackcol}



def start_call(environ, path, project, called_ident, caller_ident, received_cookies, ident_data, lang, option, proj_data):
    "Checks initial incoming call parameters, and using ident_data, retrieves session data and populates call_data"

    # get the root project - which is the project being edited, and set it into call_data
    editedproj = skiboot.getproject()

    # Note, eventual aim is to use functions from skilift rather than directly altering
    # objects, so editedprojname should in future replace editedproj
    editedprojname = skilift.get_root()

    # also set this admin project into call_data
    adminproj = skiboot.getproject(project)

    call_data = {'editedprojname':editedprojname,
                 'editedprojurl':editedproj.url,
                 'editedprojversion':editedproj.version,
                 'editedprojbrief':editedproj.brief,
                 'editedproj':editedproj,
                 'adminproj':adminproj,
                 'extend_nav_buttons':[],
                 'caller_ident':caller_ident}

    page_data = {}

    # The tar.gz file, being dynamically created, does not have a called_ident, so if called_ident is None,
    # check the path is a request for the tar.gz file, and route the call to the responder which sets the file
    # to be returned in a file page

    if called_ident is None:
        tarfile = editedproj.proj_ident + ".tar.gz"
        if path.endswith(tarfile):
            # request is for the edited project tar.gz
            return 90, call_data, page_data, lang
        # else the call is to a url not found
        return None, {}, {}, lang

    # get the called_ident page number
    projname, identnum = called_ident

    # If caller_ident is not given there should be no further session data
    if not caller_ident:
        return called_ident, call_data, page_data, lang


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
        call_data['section_name'] = session_data.get('section_name', '')
        return called_ident, call_data, page_data, lang

    if identnum == 2003:
        if 'folder' in session_data:
            # call to go back to edit a folder, ignore anything else in session data
            folder_ident = session_data['folder']
            # folder_ident is tuple (project, folder_number)
            if folder_ident[0] != editedprojname:
                return "admin_home", call_data, page_data, lang
            # check this folder exists
            folder_info = skilift.item_info(*folder_ident)
            # folder_info is a named tuple with contents
            # project, project_version, itemnumber, item_type, name, brief, path, label_list, change, parentfolder_number, restricted
            if (folder_info is None) or (folder_info.item_type != 'Folder'):
                return "admin_home", call_data, page_data, lang
            call_data['folder_number'] = folder_ident[1]
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
        if session_data['module'] in _MODULES_TUPLE:
            call_data['module'] = session_data['module']
        

    # either a section is being edited, or a folder/page - not both
    if ('section_name' in session_data) and ('page' in session_data):
        return "admin_home", call_data, page_data, lang


    if 'section_name' in session_data:
        section_name = session_data['section_name']
        if not section_name:
            return "admin_home", call_data, page_data, lang
        # check this edited section exists
        section = editedproj.section(section_name)
        if section is None:
            return "admin_home", call_data, page_data, lang

        # if section provided, so must schange
        if 'schange' not in session_data:
            return "admin_home", call_data, page_data, lang
        if section.change != session_data['schange']:
            call_data['status'] = "Someone else is editing this site, please try again later."
            return "admin_home", call_data, page_data, lang
        call_data['section_name'] = section_name
        call_data['section'] = section

    if 'page' in session_data:
        page_ident = session_data['page']
        # check this page exists
        page = skiboot.from_ident(page_ident, import_sections=False)
        if (page is None) or (page.page_type == 'Folder'):
            return "admin_home", call_data, page_data, lang
        if not page in editedproj:
            return "admin_home", call_data, page_data, lang
        # if page provided, so must pchange
        if 'pchange' not in session_data:
            return "admin_home", call_data, page_data, lang
        if page.change != session_data['pchange']:
            call_data['status'] = "Someone else is editing this site, please try again later. page (%s, %s)" % (page.change, session_data['pchange'])
            return "admin_home", call_data, page_data, lang
        call_data['page'] = page
        call_data['page_number'] = page.ident.num

    if 'widget_name' in session_data:
        call_data['widget_name'] = session_data['widget_name']

    if 'container' in session_data:
        call_data['container'] = session_data['container']

    if 'folder' in session_data:
        folder_ident = session_data['folder']
        # folder_ident is tuple (project, folder_number)
        if folder_ident[0] != editedprojname:
            return "admin_home", call_data, page_data, lang
        # check this folder exists
        folder_info = skilift.item_info(*folder_ident)
        # folder_info is a named tuple with contents
        # project, project_version, itemnumber, item_type, name, brief, path, label_list, change, parentfolder_number, restricted
        if (folder_info is None) or (folder_info.item_type != 'Folder'):
            return "admin_home", call_data, page_data, lang
        # if folder provided, so must fchange
        if 'fchange' not in session_data:
            return "admin_home", call_data, page_data, lang
        if folder_info.change != session_data['fchange']:
            call_data['status'] = "Someone else is editing this site, please try again later. folder (%s, %s)" % (folder_info.change, session_data['fchange'])
            return "admin_home", call_data, page_data, lang
        call_data['folder_number'] = folder_ident[1]

    if 'add_to_foldernumber' in session_data:
        call_data['add_to_foldernumber'] = session_data['add_to_foldernumber']

    return called_ident, call_data, page_data, lang


def submit_data(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Call the appropriate submit_data function"

    # Trying this new way of routing
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


    # the routing method below is being replaced by above method
    calling_responder = ident_list[-1]
    identnum = calling_responder[1]
    if identnum in _CALL_SUBMIT_DATA:
        return _CALL_SUBMIT_DATA[identnum](caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang)

    raise FailPage("submit_data function not found for responder %s,%s" % calling_responder)


def end_call(page_ident, page_type, call_data, page_data, proj_data, lang):
    """Stores session data under a random generated key in _SESSION_DATA and send the key as ident_data
       Also limits the length of _SESSION_DATA by popping the oldest member"""

    global _SESSION_DATA

    # do not include session data for these types of pages
    if page_type in ('FilePage', 'CSS'):
        return

    projname, identnum = page_ident

    # do not include session data if target page is in another project
    if projname != skilift.admin_project():
        return

    # header information
    if ("adminhead","page_head","large_text") not in page_data:
        page_data["adminhead","page_head","large_text"] = "Project: %s version: %s" % (call_data['editedprojname'], call_data['editedprojversion'])

    if page_type == "TemplatePage":
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
    section_name = call_data.get('section_name', '')
    if section_name:
        section = call_data.get('section', None)
        if section is not None:
            sent_session_data['section_name'] = section_name
            sent_session_data['schange'] = section.change
    else:
        # send page or folder as a tuple of its ident
        if 'page_number' in call_data:
            info = skilift.item_info(call_data['editedprojname'], call_data['page_number'])
            sent_session_data['page'] = (info.project, info.itemnumber)
            sent_session_data['pchange'] = info.change
        elif 'page' in call_data:
            page_ident = skiboot.make_ident(call_data['page'])
            sent_session_data['page'] = page_ident.to_tuple()
            info = skilift.item_info(*sent_session_data['page'])
            sent_session_data['pchange'] = info.change
        if 'folder_number' in call_data:
            info = skilift.item_info(call_data['editedprojname'], call_data['folder_number'])
            sent_session_data['folder'] = (info.project, info.itemnumber)
            sent_session_data['fchange'] = info.change

    if sent_session_data:
        # store in _SESSION_DATA, and send the key as ident_data
        # generate a key
        ident_data = uuid.uuid4().hex
        while ident_data in _SESSION_DATA:
            ident_data = uuid.uuid4().hex
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

    item_number = None

    if 'page_number' in call_data:
        item_number = call_data['page_number']
    elif 'page' in call_data:
        page_ident = skiboot.make_ident(call_data['page'])
        item_number = page_ident.num
    elif 'folder_number' in call_data:
        item_number = call_data['folder_number']

    if item_number:
        parents = skilift.parent_list(call_data['editedprojname'], item_number)
        for item in parents:
            # for each item apart from root
            if item[1]:
                edited_folder = call_data['editedprojname'] + '_' + str(item[1])
                page_data["adminhead","top_nav","nav_links"].append(['edit_from_top_nav', item[0], False, edited_folder])
    # Top navigation lists in reverse order as the float right keeps making the next link the rightmost
    page_data["adminhead","top_nav","nav_links"].reverse()


    # Left navigation

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

    # add further buttons which may be set in call_data['extend_nav_buttons']
    if 'extend_nav_buttons' in call_data:
        page_data["left_nav","navbuttons","nav_links"].extend(call_data['extend_nav_buttons'])




