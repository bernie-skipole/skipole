####### SKIPOLE WEB FRAMEWORK #######
#
# listwidgets.py  - list widgets in a module
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

"Functions implementing admin page editing"


import pkgutil, importlib, inspect, re

from ....ski import skiboot, tag, widgets
from .... import skilift
from ....skilift import fromjson

from .. import utils
from ....ski.excepts import FailPage, ValidateError, GoTo

# a search for anything none-alphanumeric and not an underscore
_AN = re.compile('[^\w]')

_MODULES_TUPLE = tuple(name for (module_loader, name, ispkg) in pkgutil.iter_modules(widgets.__path__))


def retrieve_module_list(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "this call is to retrieve data for listing widget modules"

    editedproj = call_data['editedproj']

    # get data
    bits = utils.get_bits(call_data)

    page = bits.page
    section = bits.section
    widget = bits.widget
    part = bits.part

    if (page is None) and (section is None):
        raise FailPage("Page/section not identified")

    if part is None:
        raise FailPage("Part not identified")

    # Fill in header

    # navigator boxes
    utils.nav_boxes(call_data, page, section, bits.page_top, bits.parent_container, widget, bits.container)

    page_data[("adminhead","page_head","large_text")] = "Choose module"
    if isinstance(part, str):
        page_data[("adminhead","page_head","small_text")] = "For widget insert at location " + bits.part_string
    else:
        page_data[("adminhead","page_head","small_text")] = "For widget insert at location " + bits.part_string + "_0"

    # so header text and navigation done, now continue with the page contents

    # as this page chooses a module, clear any previous chosen module and widget class
    if 'module' in call_data:
        del call_data['module']
    if 'widgetclass' in call_data:
        del call_data['widgetclass']

    # table of widget modules

    # col 0 is the visible text to place in the link,
    # col 1 is the get field of the link
    # col 2 is the get field of the link
    # col 3 is the reference string of a textblock to appear in the column adjacent to the link
    # col 4 is text to appear if the reference cannot be found in the database
    # col 5 normally empty string, if set to text it will replace the textblock

    contents = []

    for name in _MODULES_TUPLE:
        ref = 'widgets.' + name + '.module'
        contents.append([name, name, '', ref, 'Description not found', ''])

    page_data[("modules","link_table")] = contents


def retrieve_widgets_list(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "this call is to retrieve data for listing widgets in a module"

    editedproj = call_data['editedproj']

    # get data
    bits = utils.get_bits(call_data)

    page = bits.page
    section = bits.section
    widget = bits.widget
    part = bits.part

    if (page is None) and (section is None):
        raise FailPage("Page/section not identified")

    if part is None:
        raise FailPage("Part not identified")

    # Fill in header

    utils.nav_boxes(call_data, page, section, bits.page_top, bits.parent_container, widget, bits.container)
    call_data['extend_nav_buttons'].append(["list_widget_modules", "Modules", True, ''])

    if isinstance(part, str):
        page_data[("adminhead","page_head","small_text")] = "For widget insert at location " + bits.part_string
    else:
        page_data[("adminhead","page_head","small_text")] = "For widget insert at location " + bits.part_string + "_0"

    if 'chosen_module' in call_data:
        module_name = call_data['chosen_module']
    elif 'module' in call_data:
        module_name = call_data['module']
    else:
        raise FailPage("Module not identified")

    if module_name not in _MODULES_TUPLE:
        raise FailPage("Module not identified")

    page_data[("adminhead","page_head","large_text")] = "Widgets in module %s" % (module_name,)
    page_data[('moduledesc','textblock_ref')] = 'widgets.' + module_name + '.module'

    if 'widgetclass' in call_data:
        # as this page chooses a widget, clear any previous chosen widget class
        del call_data['widgetclass']

    # table of widgets

    # col 0 is the visible text to place in the link,
    # col 1 is the get field of the link
    # col 2 is the get field of the link
    # col 3 is the reference string of a textblock to appear in the column adjacent to the link
    # col 4 is text to appear if the reference cannot be found in the database
    # col 5 normally empty string, if set to text it will replace the textblock

    module = importlib.import_module("skipoles.ski.widgets." + module_name)

    # set module into call_data
    call_data['module'] = module_name

    contents = []

    for name,obj in inspect.getmembers(module, lambda member: inspect.isclass(member) and (member.__module__ == module.__name__)):
        contents.append([name, name, '', obj.description_ref(), 'Description not found', ''])

    page_data[("widgets","link_table")] = contents


def retrieve_new_widget(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "this call is to retrieve data for displaying a new widget"

    editedproj = call_data['editedproj']

    # get data
    bits = utils.get_bits(call_data)

    page = bits.page
    section = bits.section
    widget = bits.widget
    part = bits.part

    if (page is None) and (section is None):
        raise FailPage("Page/section not identified")

    if part is None:
        raise FailPage("Part not identified")

    # Fill in header

    utils.nav_boxes(call_data, page, section, bits.page_top, bits.parent_container, widget, bits.container)
    call_data['extend_nav_buttons'].extend([["list_widget_modules", "Modules", True, ''], ["back_widget_list", "Widgets", True, '']])

    if isinstance(part, str):
        page_data[("adminhead","page_head","small_text")] = "For widget insert at location " + bits.part_string
    else:
        page_data[("adminhead","page_head","small_text")] = "For widget insert at location " + bits.part_string + "_0"

    if 'module' not in call_data:
        raise FailPage("Module not identified")

    module_name = call_data['module']

    if module_name not in _MODULES_TUPLE:
        raise FailPage("Module not identified")

    module = importlib.import_module("skipoles.ski.widgets." + module_name)

    if 'chosen_widget' in call_data:
        widget_class_name = call_data['chosen_widget']
    elif 'widgetclass' in call_data:
        widget_class_name = call_data['widgetclass']
    else:
        raise FailPage("Widget not identified")

    widget_dict = {name:cls for (name,cls) in inspect.getmembers(module, lambda member: inspect.isclass(member) and (member.__module__ == module.__name__))}

    if widget_class_name not in widget_dict:
        raise FailPage("Widget not identified")

    widget_cls = widget_dict[widget_class_name]

    page_data[("adminhead","page_head","large_text")] = "Create widget of type %s" % (widget_class_name,)
    page_data[('widgetdesc','textblock_ref')] = widget_cls.description_ref()

    page_data[('fieldtable','contents')] = widget_cls.arg_references()

    if widget_cls.can_contain():
        page_data[('containerdesc','show')] = True

    if bits.section_name:
        id_string = bits.section_name + ':name'
    else:
        id_string = 'name'

    # create a widget of this class to show as a string
    widget_instance = widget_cls(name='name')
    widget_instance.update_attribs({'id':id_string, 'class':'widget_class'})
    widget_instance.show=True

    # set widget class name into call_data
    call_data['widgetclass'] = widget_class_name

    # display the widget html
    page_data[('widget_code','pre_text')] = str(widget_instance)


def create_new_widget(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "this call is to create and insert a new widget, goes on to widget edit"

    editedproj = call_data['editedproj']

    # get data
    bits = utils.get_bits(call_data)

    page = bits.page
    section = bits.section
    widget = bits.widget
    location = bits.location
    part = bits.part

    if (page is None) and (section is None):
        raise FailPage("Page/section not identified")

    if part is None:
        raise FailPage("Part not identified")

    # Fill in header
    if 'module' not in call_data:
        raise FailPage("Module not identified")

    module_name = call_data['module']

    if module_name not in _MODULES_TUPLE:
        raise FailPage("Module not identified")

    module = importlib.import_module("skipoles.ski.widgets." + module_name)

    if 'widgetclass' not in call_data:
        raise FailPage("Widget not identified")

    widget_class_name = call_data['widgetclass']

    widget_dict = {name:cls for (name,cls) in inspect.getmembers(module, lambda member: inspect.isclass(member) and (member.__module__ == module.__name__))}

    if widget_class_name not in widget_dict:
        raise FailPage("Widget not identified")

    widget_cls = widget_dict[widget_class_name]

    if 'new_widget_name' not in call_data:
        raise FailPage("Widget name missing")
    new_name=call_data['new_widget_name']
    if not new_name:
        raise FailPage("Invalid name")
    new_lower_name = new_name.lower()
    if (new_lower_name == 'body') or (new_lower_name == 'head') or (new_lower_name == 'svg')  or (new_lower_name == 'show_error'):
        raise FailPage(message="Unable to create the widget, the name given is reserved")
    if _AN.search(new_name):
        raise FailPage(message="Invalid name, alphanumeric and underscore only")
    if new_name[0] == '_':
        raise FailPage(message="Invalid name, must not start with an underscore")
    if new_name.isdigit():
        raise FailPage(message="Unable to create the widget, the name must include some letters")
    section_list = editedproj.list_section_names()
    if page is not None:
        if new_name in page.widgets:
            raise FailPage("Duplicate widget name in the page")
        if new_name in page.section_places:
            raise FailPage("This name clashes with a section alias within this page")
    else:
        if new_name in section.widgets:
            raise FailPage("Duplicate widget name in the section")
        if new_name == bits.section_name:
            raise FailPage("Cannot use the same name as the containing section")


    if 'new_widget_brief' not in call_data:
        raise FailPage("Widget description missing")
    new_brief = call_data['new_widget_brief']



    widget_instance = widget_cls(name=new_name, brief=new_brief)
    # set widget css class defaults, taken from defaults.json
    widget_fields = widget_instance.fields
    editedproj_ident = editedproj.proj_ident
    try:
        for fieldarg, field in widget_fields.items():
            if field.cssclass or field.cssstyle:
                # get default
                default_value = fromjson.get_widget_default_field_value(editedproj_ident, module_name, widget_class_name, fieldarg)
                widget_instance.set_field_value(fieldarg, default_value)
    except e:
        raise FailPage("Unable to obtain defaults from defaults.json")


    location_integers = [int(i) for i in location[2]]

    # widget is the parent widget if this widget_instance is to be placed inside
    # a parent container
    if (location[1] is not None) and (widget.is_container_empty(location[1])):
        # widget_instance is to be set as the first item in a container
        new_location = (location[0], location[1], (0,))
        utils.set_part(widget_instance, 
                       new_location,
                       page=page,
                       section=section,
                       section_name=bits.section_name,
                       widget=widget,
                       failmessage='Part to have widget inserted not identified')
    elif isinstance(part, tag.Part) and (not isinstance(part, widgets.Widget)):
        # insert at position 0 inside the part
        part.insert(0,widget_instance)
        new_location = (location[0], location[1], tuple(location_integers + [0]))
    elif (location[1] is not None) and (len(location_integers) == 1):
        # part is inside a container with parent being the containing div
        # so append after the part by inserting at the right place in the container
        position = location_integers[0] + 1
        widget.insert_into_container(location[1], position, widget_instance)
        new_location = (location[0], location[1], (position,))
    else:
        # do an append, rather than an insert
        # get parent part
        parent_part = utils.part_from_location(page,
                                               section,
                                               bits.section_name,
                                               location_string=location[0],
                                               container=location[1],
                                               location_integers=location_integers[:-1])
        # find location digit
        loc = location_integers[-1] + 1
        # insert widget_instance at loc in parent_part
        parent_part.insert(loc,widget_instance)
        new_location = (location[0], location[1], tuple(location_integers[:-1] + [loc]))

    utils.save(call_data, page=page, section_name=bits.section_name, section=section)

    utils.no_ident_data(call_data)
    if page is not None:
        call_data['page'] = page
    if section is not None:
        call_data['section_name'] = bits.section_name
        call_data['section'] = section

    call_data['widget_name'] = widget_instance.name
    call_data['status'] = "Widget created"

