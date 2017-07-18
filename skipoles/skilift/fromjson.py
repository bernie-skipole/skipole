####### SKIPOLE WEB FRAMEWORK #######
#
# fromjson.py of skilift package  - functions reading a json string
#
# This file is part of the Skipole web framework
#
# Date : 20160509
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


"""Functions that read a json string to create sections, pages and folders"""

import os, sys, traceback, json, collections

from ..ski import skiboot, read_json, dump_project
from ..ski.excepts import ServerError

from . import project_loaded, item_info, ident_exists

def _raise_server_error(message=''):
    "Raises a ServerError, and if debug mode on, adds taceback to message"
    if skiboot.get_debug():
        # append traceback to message
        if message:
            message += "\n"
        else:
            message = ''
        exc_type, exc_value, exc_traceback = sys.exc_info()
        str_list = traceback.format_exception(exc_type, exc_value, exc_traceback)
        for item in str_list:
            message += item
    raise ServerError(message)


def create_part(project, pagenumber, page_part, section_name, widget_name, container_number, location_list, part_type, json_data):
    """Builds the part from the given json string or ordered dictionary, and adds it to project either inserted into the html element
       currently at the given part location, or if not an element that can accept contents, inserted after the element."""
    # raise error if invalid project
    project_loaded(project)
    if section_name:
        ident = None
    else:
        ident = skiboot.make_ident(pagenumber, proj_ident=project)

    if location_list == 0:
        location_list = [0]

    if widget_name and (not location_list):
        # Specifies a container part, if a Part, then an insert can be done
        # however if not, then the container part must be replaced
        if part_type != 'Part':
            # The container part cannot have stuff inserted, therefore it must be replaced
            # get the widget
            widget = skiboot.get_part(project, ident, page_part, section_name, widget_name, None, [])
            # insert json data into widget at the container
            try:
                read_json.create_part_in_widget(project, ident, section_name, widget, container_number, json_data)
            except:
                _raise_server_error("Unable to create part")
            return

    if (part_type == 'Part') or (part_type == 'Section'):
        # insert in the part at the given location
        part = skiboot.get_part(project, ident, page_part, section_name, widget_name, container_number, location_list)
        # insert at position 0
        loc = 0
    else:
        # append after the part given, by inserting in the parent
        parent_location_list = location_list[:-1]
        part = skiboot.get_part(project, ident, page_part, section_name, widget_name, container_number, parent_location_list)
        # append after part
        loc = location_list[-1] + 1
    try:
        read_json.create_part(project, ident, section_name, part, loc, json_data)
    except:
        _raise_server_error("Unable to create part")


def part_to_OD(project, pagenumber, page_part, section_name, widget_name, container_number, location_list, part_type):
    """Builds an Ordered Dictionary from the part, ServerError if not found"""
    # raise error if invalid project
    project_loaded(project)
    if (part_type != 'Part') and (part_type != 'Section'):
        raise ServerError("Invalid part type")
    # part is either in a page or a section
    if pagenumber is None:
        if not section_name:
            raise ServerError("Page and section both missing")
        part = skiboot.get_part(project, None, None, section_name, widget_name, container_number, location_list)
    else:
        if section_name:
            raise ServerError("Part cannot be in both a page and a section")
        ident = skiboot.make_ident(pagenumber, project)
        if ident is None:
            raise ServerError("Part not recognised")
        part = skiboot.get_part(project, ident, page_part, None, widget_name, container_number, location_list)
    if part is None:
        raise ServerError("Part not recognised")
    return dump_project.part_to_OD(project, part)


def part_to_json(project, pagenumber, page_part, section_name, widget_name, container_number, location_list, part_type, indent=0):
    """Builds a json string from the part, ServerError if not found"""
    part_dict = part_to_OD(project, pagenumber, page_part, section_name, widget_name, container_number, location_list, part_type)
    return json.dumps(part_dict, indent=indent, separators=(',', ':'))


def create_section(project, section_name, json_data):
    """Builds the section from the given json string or ordered dictionary, and adds it to project"""
    # raise error if invalid project
    project_loaded(project)
    try:
        read_json.create_section(project, section_name, json_data)
    except:
        _raise_server_error("Unable to create section")


def section_to_OD(project, section_name):
    """Builds an Ordered Dictionary from the section, ServerError if not found"""
    # raise error if invalid project
    project_loaded(project)
    proj = skiboot.getproject(project)
    section = proj.section(section_name, makecopy=False)
    if section is None:
        raise ServerError(message="Section not found")
    return dump_project.section_to_OD(project, section_name, section)


def section_to_json(project, section_name, indent=0):
    """Builds a json string from the section, ServerError if not found"""
    section_dict = section_to_OD(project, section_name)
    return json.dumps(section_dict, indent=indent, separators=(',', ':'))


def create_page(project, parentnumber, pagenumber, page_name, page_brief, json_data):
    """Builds a page from the given json string / ordered dictionary, and adds it to project"""
    # raise error if invalid project
    project_loaded(project)
    if not isinstance(pagenumber, int):
        raise ServerError(message="pagenumber is not an integer")
    if not isinstance(parentnumber, int):
        raise ServerError(message="parentnumber is not an integer")
    if ident_exists(project, pagenumber):
        raise ServerError(message = "An item with this ident number already exists")
    parentinfo = item_info(project, parentnumber)
    if not parentinfo:
        raise ServerError(message = "The parent folder with this ident number has not been found")
    if parentinfo.item_type != "Folder":
        raise ServerError(message = "The parent with this ident number is not a folder")
    if isinstance(json_data, str):
        page_dict = json.loads(json_data, object_pairs_hook=collections.OrderedDict)
    else:
        page_dict = json_data
    # create the page
    try:
        if "SVG" in page_dict:
            read_json.create_svgpage(project, parentnumber, pagenumber, page_name, page_brief, page_dict)
            return
        elif "TemplatePage" in page_dict:
            read_json.create_templatepage(project, parentnumber, pagenumber, page_name, page_brief, page_dict)
            return
    except ServerError as e:
        _raise_server_error(e.message)
    raise ServerError(message = "Invalid JSON file")



def page_to_OD(project, pagenumber):
    """Returns an Ordered Dictionary from the given page, ServerError if not found"""
    # raise error if invalid project
    project_loaded(project)
    if not isinstance(pagenumber, int):
        raise ServerError(message="pagenumber is not an integer")
    page = skiboot.from_ident(pagenumber, project, import_sections=False)
    if page is None:
        raise ServerError(message="Page not found")
    if page.page_type == 'SVG':
        page_dict = dump_project.svg_to_OD(project, page)
    elif page.page_type == 'TemplatePage':
        page_dict = dump_project.templatepage_to_OD(project, page)
    else:
        raise ServerError(message="The given pagenumber is not that of an svg or template page")
    return page_dict


def page_to_json(project, pagenumber, indent=0):
    """Builds a json string from the given page, ServerError if not found"""
    page_dict = page_to_OD(project, pagenumber)
    return json.dumps(page_dict, indent=indent, separators=(',', ':'))



def create_folder(project, parentnumber, addition_number, folder_name, restricted, json_data):
    """Builds a folder and contents from the given json string / ordered dictionary, and adds it to project"""
    # raise error if invalid project
    project_loaded(project)
    if not isinstance(addition_number, int):
        raise ServerError(message="addition number is not an integer")
    if not isinstance(parentnumber, int):
        raise ServerError(message="parentnumber is not an integer")
    parentinfo = item_info(project, parentnumber)
    if not parentinfo:
        raise ServerError(message = "The parent folder with this ident number has not been found")
    if parentinfo.item_type != "Folder":
        raise ServerError(message = "The parent with this ident number is not a folder")
    # create the folder
    try:
        read_json.create_folder(project, parentnumber, addition_number, folder_name, restricted, json_data)
    except ServerError as e:
        _raise_server_error(e.message)


def folder_to_OD(project, foldernumber):
    """Returns an Ordered Dictionary from the given folder, ServerError if not found"""
    # raise error if invalid project
    project_loaded(project)
    if not isinstance(foldernumber, int):
        raise ServerError(message="foldernumber is not an integer")
    folder = skiboot.from_ident(foldernumber, project, import_sections=False)
    if folder is None:
        raise ServerError(message="Folder not found")
    if folder.page_type != 'Folder':
        raise ServerError(message="The given foldernumber is not that of a Folder")
    return dump_project.folder_to_OD(project, folder)


def folder_to_json(project, foldernumber, indent=0):
    """Builds a json string from the given folder, ServerError if not found"""
    folder_dict = folder_to_OD(project, foldernumber)
    return json.dumps(folder_dict, indent=indent, separators=(',', ':'))


def project_to_OD(project):
    """Returns an Ordered Dictionary of the project, ServerError if not found"""
    # raise error if invalid project
    project_loaded(project)
    return dump_project.project_to_OD(project)


def project_to_json(project, save_to_file=True, indent=0):
    """If save_to_file is True:
         creates the file project.json under the projectfiles/project/data directory
         and then returns None
       If save_to_file is False, returns a json string of the project"""

    project_dict = project_to_OD(project)

    if save_to_file:
        # write out the project dictionary to a json file
        filepath = skiboot.project_json(project)
        with open(filepath, 'w') as fp:
            json.dump(project_dict, fp, indent=indent)
        return

    return json.dumps(project_dict, indent=indent, separators=(',', ':'))


def get_defaults(project, key=None):
    """If key not given, returns the defaults dictionary,
       if key given returns the value,
       if key given, but not present, returns None"""
    defaults = {}
    defaultsfile = skiboot.project_defaults(proj_ident=project)
    if os.path.isfile(defaultsfile):
        # load defaultsfile into defaults
        with open(defaultsfile, 'r') as fp:
            defaults = json.load(fp, object_pairs_hook=collections.OrderedDict)
    else:
        return
    if not defaults:
        return
    if not key:
        return defaults
    if key in defaults:
        return defaults[key]


def get_widget_default_field_value(project, widg_module, widg_class, widg_field):
    "Returns the default value to set into a widget field argument, returns '' if not found"
    if not (widg_module and widg_class and widg_field):
        return ''
    widg_defaults_dict = get_defaults(project, key='widgets')
    if widg_defaults_dict is None:
        return ''
    # widg_defaults_dict is a dictionary of keys being module names, values being another dictionary
    if widg_module in widg_defaults_dict:
        widg_module_dict = widg_defaults_dict[widg_module]
    else:
        return ''
    # widg_module_dict is a dictionary of keys being widget class names in the module, values being another dictionary
    if widg_class in widg_module_dict:
        widg_class_dict = widg_module_dict[widg_class]
    else:
        return ''
    # widg_class_dict is a dictionary of keys being widget field arg names in the module, values being the default field values
    if widg_field in widg_class_dict:
        default_field_value = widg_class_dict[widg_field]
    else:
        return ''
    if default_field_value:
        return default_field_value
    return ''


def set_defaults(project, key, value):
    "Sets a key, value into defaults"
    defaults = get_defaults(project)
    if not defaults:
        defaults = {}
    defaults[key] = value
    save_defaults(project, defaults)


def save_defaults(project, defaults):
    "Saves defaults.json"
    # create defaults.json
    defaults_json_filename = skiboot.project_defaults(project)
    # write out the project defaults dictionary to a json file
    with open(defaults_json_filename, 'w') as fp:
        json.dump(defaults, fp, indent=0)


def save_widget_default_field_value(project, widg_module, widg_class, widg_field, value):
    "Saves the default value to set into a widget field argument, returns True if ok, False if not"
    if not (widg_module and widg_class and widg_field):
        return False
    widg_defaults_dict = get_defaults(project, key='widgets')
    if widg_defaults_dict is None:
        widg_defaults_dict = collections.OrderedDict()
    # widg_defaults_dict is a dictionary of keys being module names, values being another dictionary
    if widg_module in widg_defaults_dict:
        widg_module_dict = widg_defaults_dict[widg_module]
    else:
        widg_module_dict = collections.OrderedDict()
        widg_defaults_dict[widg_module] = widg_module_dict
    # widg_module_dict is a dictionary of keys being widget class names in the module, values being another dictionary
    if widg_class in widg_module_dict:
        widg_class_dict = widg_module_dict[widg_class]
    else:
        widg_class_dict = collections.OrderedDict()
        widg_module_dict[widg_class] = widg_class_dict
    # widg_class_dict is a dictionary of keys being widget field arg names in the module, values being the default field value
    widg_class_dict[widg_field] = value
    try:
        set_defaults(project, key='widgets', value=widg_defaults_dict)
    except e:
        return False
    return True


