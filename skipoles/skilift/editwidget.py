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

import pkgutil, importlib, inspect, re

from collections import namedtuple


from ..ski import widgets, dump_project
from ..ski.excepts import ServerError

from . import widget_info, fromjson, insert_item_in_page, insert_item_in_section, get_proj_page, get_proj_section


# a search for anything none-alphanumeric and not an underscore
_AN = re.compile('[^\w]')

WidgetDescription = namedtuple('WidgetDescription', ['modulename', 'classname', 'brief', 'reference', 'fields', 'containers', 'illustration',
                                                     'fields_single', 'fields_list', 'fields_table', 'fields_dictionary'])


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
        widget_list.append( WidgetDescription( module_name,
                                               classname,
                                               obj.brief,
                                               obj.description_ref(),
                                               obj.arg_references(),
                                               obj.len_containers(),
                                               obj.description(),
                                               obj.field_arguments_single(),
                                               obj.field_arguments_list(),
                                               obj.field_arguments_table(),
                                               obj.field_arguments_dictionary()
                                               ) )
    return widget_list


def _create_new_widget(project, module_name, widget_classname, name, brief):
    "Creates a new widget"
    if not name:
        raise ServerError("Invalid name")
    lower_name = name.lower()
    if (lower_name == 'body') or (lower_name == 'head') or (lower_name == 'svg')  or (lower_name == 'show_error'):
        raise ServerError(message="Unable to create the widget, the name given is reserved")
    if _AN.search(name):
        raise ServerError(message="Invalid name, alphanumeric and underscore only")
    if name[0] == '_':
        raise ServerError(message="Invalid name, must not start with an underscore")
    if name.isdigit():
        raise ServerError(message="Unable to create the widget, the name must include some letters")
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
    return widget_instance


def create_new_widget_in_page(project, pagenumber, pchange, location, module_name, widget_classname, name, brief):
    "Creates a new widget in the given page, returns the new pchange and new location"
    widget_instance = _create_new_widget(project, module_name, widget_classname, name, brief)
    # call skilift.insert_item_in_page to insert the item, save the page and return pchange and new location
    return insert_item_in_page(project, pagenumber, pchange, location, widget_instance)


def create_new_widget_in_section(project, section_name, schange, location, module_name, widget_classname, name, brief):
    "Creates a new widget in the given section, returns the new schange and new location"
    widget_instance = _create_new_widget(project, module_name, widget_classname, name, brief)
    # call skilift.insert_item_in_section to insert the item, save the section and return schange and new location
    return insert_item_in_section(project, section_name, schange, location, widget_instance)


def page_widget(project, pagenumber, pchange, name):
    """Return a widget dictionary from the page"""
    proj, page = get_proj_page(project, pagenumber, pchange)
    widget = page.widgets.get(name)
    if (not isinstance(widget, widgets.Widget)) and (not isinstance(widget, widgets.ClosedWidget)):
        raise ServerError("Widget not found")
    return dump_project.widget_to_OD(project, widget)


def section_widget(project, section_name, schange, name):
    """Return a widget dictionary from the section"""
    proj, section = get_proj_section(project, section_name, schange)
    widget = section.widgets.get(name)
    if (not isinstance(widget, widgets.Widget)) and (not isinstance(widget, widgets.ClosedWidget)):
        raise ServerError("Widget not found")
    return dump_project.widget_to_OD(project, widget)


def page_widget_description(project, pagenumber, pchange, name):
    """Return a WidgetDescription from the page"""
    proj, page = get_proj_page(project, pagenumber, pchange)
    widget = page.widgets.get(name)
    if (not isinstance(widget, widgets.Widget)) and (not isinstance(widget, widgets.ClosedWidget)):
        raise ServerError("Widget not found")
    return WidgetDescription( widget.__class__.__module__.split('.')[-1],
                              widget.__class__.__name__,
                              widget.brief,
                              widget.description_ref(),
                              widget.arg_references(),
                              widget.len_containers(),
                              widget.description(),
                              widget.field_arguments_single(),
                              widget.field_arguments_list(),
                              widget.field_arguments_table(),
                              widget.field_arguments_dictionary()
                               )


def section_widget_description(project, section_name, schange, name):
    """Return a widget WidgetDescription from the section"""
    proj, section = get_proj_section(project, section_name, schange)
    widget = section.widgets.get(name)
    if (not isinstance(widget, widgets.Widget)) and (not isinstance(widget, widgets.ClosedWidget)):
        raise ServerError("Widget not found")
    return WidgetDescription( widget.__class__.__module__.split('.')[-1],
                              widget.__class__.__name__,
                              widget.brief,
                              widget.description_ref(),
                              widget.arg_references(),
                              widget.len_containers(),
                              widget.description(),
                              widget.field_arguments_single(),
                              widget.field_arguments_list(),
                              widget.field_arguments_table(),
                              widget.field_arguments_dictionary()
                               )


def rename_page_widget(project, pagenumber, pchange, name, new_name):
    """Given a widget at project, pagenumber, with name 
       sets a new name, returns page change uuid """
    if not new_name:
        raise ServerError("Invalid name")
    proj, page = get_proj_page(project, pagenumber, pchange)
    widget = page.widgets.get(name)
    if (not isinstance(widget, widgets.Widget)) and (not isinstance(widget, widgets.ClosedWidget)):
        raise ServerError("Widget not found")
    if name == new_name:
        raise ServerError("Name unchanged")
    new_lower_name = new_name.lower()
    if (new_lower_name == 'body') or (new_lower_name == 'head') or (new_lower_name == 'svg')  or (new_lower_name == 'show_error'):
        raise ServerError(message="Unable to create the widget, the name given is reserved")
    if _AN.search(new_name):
        raise ServerError(message="Invalid name, alphanumeric and underscore only")
    if new_name[0] == '_':
        raise ServerError(message="Invalid name, must not start with an underscore")
    if new_name.isdigit():
        raise ServerError(message="Unable to create the widget, the name must include some letters")
    if new_name in page.widgets:
        raise ServerError("Duplicate widget name in the page")
    if new_name in page.section_places:
        raise ServerError("This name clashes with a section alias within this page")
    widget.name = new_name
    # save the altered page, and return the page.change uuid
    return proj.save_page(page)


def new_brief_in_page_widget(project, pagenumber, pchange, name, brief):
    """Given a widget at project, pagenumber, with name 
       sets a new brief, returns page change uuid """
    proj, page = get_proj_page(project, pagenumber, pchange)
    widget = page.widgets.get(name)
    if (not isinstance(widget, widgets.Widget)) and (not isinstance(widget, widgets.ClosedWidget)):
        raise ServerError("Widget not found")
    widget.brief = brief
    # save the altered page, and return the page.change uuid
    return proj.save_page(page)


def rename_section_widget(project, section_name, schange, name, new_name):
    """Given a widget at project, pagenumber, with name 
       sets a new name, returns page change uuid """
    if not new_name:
        raise ServerError("Invalid name")
    proj, section = get_proj_section(project, section_name, schange)
    widget = section.widgets.get(name)
    if (not isinstance(widget, widgets.Widget)) and (not isinstance(widget, widgets.ClosedWidget)):
        raise ServerError("Widget not found")
    if name == new_name:
        raise ServerError("Name unchanged")
    new_lower_name = new_name.lower()
    if (new_lower_name == 'body') or (new_lower_name == 'head') or (new_lower_name == 'svg')  or (new_lower_name == 'show_error'):
        raise ServerError(message="Unable to create the widget, the name given is reserved")
    if _AN.search(new_name):
        raise ServerError(message="Invalid name, alphanumeric and underscore only")
    if new_name[0] == '_':
        raise ServerError(message="Invalid name, must not start with an underscore")
    if new_name.isdigit():
        raise ServerError(message="Unable to create the widget, the name must include some letters")
    if new_name in section.widgets:
        raise ServerError("Duplicate widget name in the section")
    widget.name = new_name
    # save the altered section, and return the section.change uuid
    return proj.add_section(section_name, section)


def new_brief_in_section_widget(project, section_name, schange, name, brief):
    """Given a widget at project, section_name, with name 
       sets a new brief, returns section change uuid """
    proj, section = get_proj_section(project, section_name, schange)
    widget = section.widgets.get(name)
    if (not isinstance(widget, widgets.Widget)) and (not isinstance(widget, widgets.ClosedWidget)):
        raise ServerError("Widget not found")
    widget.brief = brief
    # save the altered section, and return the section.change uuid
    return proj.add_section(section_name, section)



        



