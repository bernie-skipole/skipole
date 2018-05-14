####### SKIPOLE WEB FRAMEWORK #######
#
# editwidget.py of skilift package  - functions for editing a widget
#
# This file is part of the Skipole web framework
#
# Date : 20180403
#
# Author : Bernard Czenkusz
# Email  : bernie@skipole.co.uk
#
#
#   Copyright 2018 Bernard Czenkusz
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


"""Functions for editing a widget"""

import pkgutil, importlib, inspect

from collections import namedtuple


from ..ski import skiboot, tag, widgets
from ..ski.excepts import ServerError

from . import project_loaded, widget_info, fromjson, insert_item_in_page, insert_item_in_section

WidgetDescription = namedtuple('Widget', ['classname', 'reference', 'fields', 'containers', 'illustration'])

# 'fields' is a list of lists: [ field arg, field ref]
# 'containers' is the number of containers in the widget, 0 for none

def widget_modules():
    "Return a tuple of widget module names"
    return tuple(name for (module_loader, name, ispkg) in pkgutil.iter_modules(widgets.__path__))


def widgets_in_module(module_name):
    "Returns a list of WidgetDescription's present in the module"
    module = importlib.import_module("skipoles.ski.widgets." + module_name)
    widget_list = []
    for classname,obj in inspect.getmembers(module, lambda member: inspect.isclass(member) and (member.__module__ == module.__name__)):
        widget_list.append( WidgetDescription( classname,
                                               obj.description_ref(),
                                               obj.arg_references(),
                                               obj.len_containers(),
                                               obj.description()
                                               ) )
    return widget_list


def _get_proj_page_section(project, pagenumber=None, pchange=None, section_name=None, schange=None):
    "Returns (project_object, page_object, section_object) - one page, section being None" 

    project_loaded(project)
    proj = skiboot.getproject(project)

    page = None
    section = None

    if section_name:
        # get a copy of the section
        if pagenumber is not None:
            raise ServerError(message="Either pagenumber or section_name must be given, not both")
        if not isinstance(section_name, str):
            raise ServerError(message="Given section_name is invalid")
        section = proj.section(section_name, makecopy=True)
        if section is None:
            raise ServerError(message="Given section_name is invalid")
        if section.change != schange:
            raise ServerError(message="The section has been changed prior to this submission, someone else may be editing this project")
    else:
        # get a copy of the page
        if not isinstance(pagenumber, int):
            raise ServerError(message="Given pagenumber is not an integer")
        ident = skiboot.Ident.to_ident((project, pagenumber))
        if ident is None:
            raise ServerError(message="Invalid project, pagenumber")
        page = skiboot.from_ident(ident, project)
        if page is None:
            raise ServerError(message="Invalid Page")
        if (page.page_type != 'TemplatePage') and (page.page_type != 'SVG'):
            raise ServerError(message="Item must be a Template or SVG page")
        if page.change != pchange:
            raise ServerError(message="The page has been changed prior to this submission, someone else may be editing this project")
    return proj, page, section


def create_new_widget_in_page(project, pagenumber, pchange, location, module_name, widget_classname, name, brief):
    "Creates a new widget in the given page, returns the new pchange"
    modules_tuple = widget_modules()
    if module_name not in modules_tuple:
        raise FailPage("Module not identified")
    module = importlib.import_module("skipoles.ski.widgets." + module_name)

    widget_dict = {name:cls for (name,cls) in inspect.getmembers(module, lambda member: inspect.isclass(member) and (member.__module__ == module.__name__))}

    if widget_classname not in widget_dict:
        raise ServerError(message="Widget not identified")

    widget_cls = widget_dict[widget_classname]
    widget_instance = widget_cls(name=name, brief=brief)
    # set widget css class defaults, taken from defaults.json
    widget_fields = widget_instance.fields
    try:
        for fieldarg, field in widget_fields.items():
            if field.cssclass or field.cssstyle:
                # get default
                default_value = fromjson.get_widget_default_field_value(project, module_name, widget_classname, fieldarg)
                widget_instance.set_field_value(fieldarg, default_value)
    except e:
        raise ServerError("Unable to obtain defaults from defaults.json")
    # call skilift.insert_item_in_page to insert the item, save the page and return pchange
    return insert_item_in_page(project, pagenumber, pchange, location, widget_instance)


def create_new_widget_in_section(project, section_name, schange, location, module_name, widget_classname, name, brief):
    "Creates a new widget in the given section, returns the new schange"
    modules_tuple = widget_modules()
    if module_name not in modules_tuple:
        raise FailPage("Module not identified")
    module = importlib.import_module("skipoles.ski.widgets." + module_name)

    widget_dict = {name:cls for (name,cls) in inspect.getmembers(module, lambda member: inspect.isclass(member) and (member.__module__ == module.__name__))}

    if widget_classname not in widget_dict:
        raise ServerError(message="Widget not identified")

    widget_cls = widget_dict[widget_classname]
    widget_instance = widget_cls(name=name, brief=brief)
    # set widget css class defaults, taken from defaults.json
    widget_fields = widget_instance.fields
    try:
        for fieldarg, field in widget_fields.items():
            if field.cssclass or field.cssstyle:
                # get default
                default_value = fromjson.get_widget_default_field_value(project, module_name, widget_classname, fieldarg)
                widget_instance.set_field_value(fieldarg, default_value)
    except e:
        raise ServerError("Unable to obtain defaults from defaults.json")
    # call skilift.insert_item_in_page to insert the item, save the page and return pchange
    return insert_item_in_section(project, section_name, schange, location, widget_instance)




def create_new_widget(project, module_name, widget_classname, location, name, brief, pagenumber=None, pchange=None, section_name=None, schange=None):
    "Creates a new widget in the given page or section (one must be None), at location with name and brief description"

    proj, page, section = _get_proj_page_section(project, pagenumber, pchange, section_name, schange)
    location_string, container, location_integers = location

    # location string is either a widget name, or body, head, or svg
    # if a widget_name, container must be given

    modules_tuple = widget_modules()

    if module_name not in modules_tuple:
        raise FailPage("Module not identified")

    module = importlib.import_module("skipoles.ski.widgets." + module_name)

    widget_dict = {name:cls for (name,cls) in inspect.getmembers(module, lambda member: inspect.isclass(member) and (member.__module__ == module.__name__))}

    if widget_classname not in widget_dict:
        raise ServerError(message="Widget not identified")

    if page is not None:
        if name in page.widgets:
            raise ServerError(message="Duplicate widget name in the page")
        if name in page.section_places:
            raise ServerError(message="This name clashes with a section alias within this page")
    else:
        if name in section.widgets:
            raise ServerError(message="Duplicate widget name in the section")
        if name == section.name:
            raise ServerError(message="Cannot use the same name as the containing section")

    widget_cls = widget_dict[widget_classname]
    widget_instance = widget_cls(name=name, brief=brief)
    # set widget css class defaults, taken from defaults.json
    widget_fields = widget_instance.fields
    try:
        for fieldarg, field in widget_fields.items():
            if field.cssclass or field.cssstyle:
                # get default
                default_value = fromjson.get_widget_default_field_value(project, module_name, widget_classname, fieldarg)
                widget_instance.set_field_value(fieldarg, default_value)
    except e:
        raise ServerError("Unable to obtain defaults from defaults.json")

    location_integers = [int(i) for i in location[2]]

    if container is None:
        # not in a widget
        parent_widget = None
    else:
        # so item is in a widget, location_string is the widget name
        if page is not None:
            parent_widget = page.widgets[location_string]
        else:
            parent_widget = section.widgets[location_string]

    # get the part at the current location
    part = None
    if page is not None:
        # part is in a page
        if parent_widget is None:
            # part not in a widget
            part = page.get_part(location_string, location_integers)
        else:
            part = parent_widget.get_from_container(container, location_integers)
    else:
        # part is in a section
        if parent_widget is None:
            # part not in a widget
            if location_string == section_name:
                if location_integers:
                    part = section.get_location_value(location_integers)
                else:
                    part = section
        else:
            part = parent_widget.get_from_container(container, location_integers)



    # If this widget_instance is to be placed inside a parent widget container
    if (parent_widget is not None) and (parent_widget.is_container_empty(container)):
        # widget_instance is to be set as the first item in a widget container
        parent_widget.set_in_container(container, (0,), widget_instance)
    elif isinstance(part, tag.Part) and (not hasattr(part, "arg_descriptions")): # not Closed Part and not a widget
        # insert at position 0 inside the part
        part.insert(0,widget_instance)
    elif (parent_widget is not None) and (len(location_integers) == 1):
        # part is inside a container with parent being the containing div
        # so append after the part by inserting at the right place in the container
        position = location_integers[0] + 1
        parent_widget.insert_into_container(container, position, widget_instance)

    else:
        # do an append, rather than an insert
        # get parent part
        loc_integers = location_integers[:-1]
        if page is not None:
            if (location_string == 'head') or (location_string == 'body') or (location_string == 'svg'):
                parent_part = page.get_part(location_string, loc_integers)
            else:
                # parent_widget is the containing widget 
                parent_part = parent_widget.get_from_container(container, loc_integers)
        else:
            # part is in a section
            if parent_widget is None:
                # part not in a widget
                if location_string == section_name:
                    if loc_integers:
                        parent_part = section.get_location_value(loc_integers)
                    else:
                        parent_part = section
            else:
                parent_part = parent_widget.get_from_container(container, loc_integers)

        # find location digit
        loc = location_integers[-1] + 1
        # insert placeholder at loc in parent_part
        parent_part.insert(loc,widget_instance)

    # save the altered page or section, and return the change uuid
    if page is not None:
        return proj.save_page(page)
    else:
        return proj.add_section(section_name, section)






        



