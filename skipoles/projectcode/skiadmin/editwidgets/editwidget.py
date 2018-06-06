####### SKIPOLE WEB FRAMEWORK #######
#
# editwidget.py  - widget editing functions
#
# This file is part of the Skipole web framework
#
# Date : 20150421
#
# Author : Bernard Czenkusz
# Email  : bernie@skipole.co.uk
#
#
#   Copyright 2015 Bernard Czenkusz
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

"Functions implementing widget editing"

import re, html

from .... import skilift
from ....skilift import fromjson, editsection, editpage, editwidget

from ....ski import skiboot, tag, widgets
from .. import utils
from ....ski.excepts import FailPage, ValidateError, ServerError, GoTo

# a search for anything none-alphanumeric and not an underscore
_AN = re.compile('[^\w]')


def _field_name(widget, field_argument):
    "Returns a field name"
    if "set_names" not in widget:
        return field_argument
    name_dict = widget["set_names"]
    if field_argument in name_dict:
        return name_dict[field_argument]
    return field_argument

def _field_value(widget, field_argument):
    "Returns value,string value"
    value = widget["fields"][field_argument]
    if value is None:
        field_value = ''
    elif isinstance(value, list):
        if value:
            field_value = ','.join(str(val) for val in value)
        else:
            field_value = ''
    else:
        field_value = str(value)
    return value, field_value


def retrieve_widget(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Fills in the edit a widget page"

    # get the widget name
    if ("left_nav","navbuttons","nav_links") in call_data:
        # should be submitted as widgetname from left navigation links
        widget_name = call_data["left_nav","navbuttons","nav_links"]
    elif 'widget_name' in call_data:
        widget_name = call_data['widget_name']
    elif 'part_tuple' in call_data:
        # called from dom table, via responder that finds what is being edited
        # and has set it into part_tuple
        part_tuple = call_data['part_tuple']
        widget_name = part_tuple.name
    else:
        raise FailPage(message="Invalid widget")

    if not widget_name:
        raise FailPage(message="Invalid widget")

    # and this is the widget to be edited, it is now set into session data
    call_data['widget_name'] = widget_name

    # Fill in header
    page_data[("adminhead","page_head","large_text")] = "Widget " + widget_name

    project = call_data['editedprojname']

    section_name = None
    pagenumber = None
    if 'section_name' in call_data:
        section_name = call_data['section_name']
    elif 'page_number' in call_data:
        pagenumber = call_data['page_number']
    else:
        raise FailPage(message="No section or page given")

    try:
        if section_name:
            widgetdescription = editwidget.section_widget_description(project, section_name, call_data['schange'], widget_name)
            widget =  editwidget.section_widget(project, section_name, call_data['schange'], widget_name)
        else:
            widgetdescription = editwidget.page_widget_description(project, pagenumber, call_data['pchange'], widget_name)
            widget = editwidget.page_widget(project, pagenumber, call_data['pchange'], widget_name)
    except ServerError as e:
        raise FailPage(e.message)
    

    page_data[('widget_type','para_text')] = "This widget is of type %s.%s." % (widgetdescription.modulename, widgetdescription.classname)
    page_data[('widget_textblock','textblock_ref')] = widgetdescription.reference
    page_data[('widget_name','input_text')] = widget_name
    page_data[('widget_brief','input_text')] = widgetdescription.brief


    args = widgetdescription.fields_single                 # lists of [ field arg, field ref, field type, valdt, jsonset, cssclass, cssstyle]
    arg_list = widgetdescription.fields_list               # [ field arg, field ref, field type, valdt, jsonset]
    arg_table = widgetdescription.fields_table             # [ field arg, field ref, field type, valdt, jsonset]
    arg_dict = widgetdescription.fields_dictionary         # [ field arg, field ref, field type, valdt, jsonset]

    if arg_list or arg_table or arg_dict:
        page_data[('args_multi','show')] = True
    else:
        page_data[('args_multi','show')] = False


    # args is shown on a LinkTextBlockTable2

    # contents row is
    # col 0 is the visible text to place in the link,
    # col 1 is the get field of the link
    # col 2 is the second get field of the link
    # col 3 is text appearing in the second table column
    # col 4 is the reference string of a textblock to appear the third table column
    # col 5 is text to appear if the reference cannot be found in the database
    # col 6 normally empty string, if set to text it will replace the textblock

    args_valdt = False

    args_content = []
    if args:
        for arg in args:
            name = _field_name(widget, arg[0])
            if arg[3]:   
                name = "* " + name
                args_valdt = True
            # field value
            value,field_value = _field_value(widget, arg[0])
            if len(field_value) > 20:
                field_value = field_value[:18]
                field_value += '...'
            arg_row = [ name, arg[0], '',field_value, arg[1], 'No description for %s' % (arg[1],), '']
            args_content.append(arg_row)
        page_data[('args','link_table')] = args_content
    else:
        page_data[('args','show')] = False
        page_data[('args_description','show')] = False


    # arg_list, arg_table and arg_dict are shown on LinkTextBlockTable widgets

    # contents row is
    # col 0 is the visible text to place in the link,
    # col 1 is the get field of the link
    # col 2 is the second get field of the link
    # col 3 is the reference string of a textblock to appear in the column adjacent to the link
    # col 4 is text to appear if the reference cannot be found in the database
    # col 5 normally empty string, if set to text it will replace the textblock


    arg_list_content = []
    if arg_list:
        for arg in arg_list:
            name = _field_name(widget, arg[0])
            if arg[3]:
                name = "* " + name
                args_valdt = True
            arg_row = [ name, arg[0], '', arg[1], 'No description for %s' % (arg[1],), '']
            arg_list_content.append(arg_row)
        page_data[('arg_list','link_table')] = arg_list_content
    else:
        page_data[('arg_list','show')] = False
        page_data[('arg_list_description','show')] = False

    arg_table_content = []
    if arg_table:
        for arg in arg_table:
            name = _field_name(widget, arg[0])
            if arg[3]:
                name = "* " + name
                args_valdt = True
            arg_row = [ name, arg[0], '', arg[1], 'No description for %s' % (arg[1],), '']
            arg_table_content.append(arg_row)
        page_data[('arg_table','link_table')] = arg_table_content
    else:
        page_data[('arg_table','show')] = False
        page_data[('arg_table_description','show')] = False

    arg_dict_content = []
    if arg_dict:
        for arg in arg_dict:
            name = _field_name(widget, arg[0])
            if arg[3]:
                name = "* " + name
                args_valdt = True
            arg_row = [ name, arg[0], '', arg[1], 'No description for %s' % (arg[1],), '']
            arg_dict_content.append(arg_row)
        page_data[('arg_dict','link_table')] = arg_dict_content
    else:
        page_data[('arg_dict','show')] = False
        page_data[('arg_dict_description','show')] = False

    page_data[('args_valdt','show')] = args_valdt

    # display the widget html
    page_data[('widget_code','pre_text')] = widgetdescription.illustration

    if widgetdescription.containers:
        page_data[('containerdesc','show')] = True

    # remove any unwanted fields from session call_data
    if 'container' in call_data:
        del call_data['container']
    if 'location' in call_data:
        del call_data['location']
    if 'part' in call_data:
        del call_data['part']
    if 'field_arg' in call_data:
        del call_data['field_arg']
    if 'validx' in call_data:
        del call_data['validx']


def set_widget_params(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Sets widget name and brief"

    project = call_data['editedprojname']

    section_name = None
    pagenumber = None
    if 'section_name' in call_data:
        section_name = call_data['section_name']
    elif 'page_number' in call_data:
        pagenumber = call_data['page_number']
    else:
        raise FailPage(message="No section or page given")

    if 'widget_name' in call_data:
        widget_name = call_data['widget_name']
    else:
        raise FailPage(message="Widget not identified")

    new_name = None
    brief = None

    if 'new_widget_name' in call_data:
        new_name = call_data['new_widget_name']
    elif 'widget_brief' in call_data:
        brief = call_data['widget_brief']
    else:
        raise FailPage(message="No new name or brief given")
    
    try:
        if section_name:
            if new_name:
                call_data['schange'] = editwidget.rename_section_widget(project, section_name, call_data['schange'], widget_name, new_name)
                call_data['status'] = "Widget name changed"
                call_data['widget_name'] = new_name
            else:
                call_data['schange'] = editwidget.new_brief_in_section_widget(project, section_name, call_data['schange'], widget_name, brief)
                call_data['status'] = "Widget brief changed"
        else:
            if new_name:
                call_data['pchange'] = editwidget.rename_page_widget(project, pagenumber, call_data['pchange'], widget_name, new_name)
                call_data['status'] = "Widget name changed"
                call_data['widget_name'] = new_name
            else:
                call_data['pchange'] = editwidget.new_brief_in_page_widget(project, pagenumber, call_data['pchange'], widget_name, brief)
                call_data['status'] = "Widget brief changed"
    except ServerError as e:
        raise FailPage(e.message)


def retrieve_editfield(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Fills in the edit a widget field page"

    project = call_data['editedprojname']

    section_name = None
    pagenumber = None
    if 'section_name' in call_data:
        section_name = call_data['section_name']
    elif 'page_number' in call_data:
        pagenumber = call_data['page_number']
    else:
        raise FailPage(message="No section or page given")

    if 'widget_name' in call_data:
        widget_name = call_data['widget_name']
    else:
        raise FailPage(message="Widget not identified")

    # Fill in header

    if 'field_arg' in call_data:
        field_arg = call_data['field_arg']
    else:
        raise FailPage("Field not identified")

    try:
        if section_name:
            widgetdescription = editwidget.section_widget_description(project, section_name, call_data['schange'], widget_name)
            widget =  editwidget.section_widget(project, section_name, call_data['schange'], widget_name)
        else:
            widgetdescription = editwidget.page_widget_description(project, pagenumber, call_data['pchange'], widget_name)
            widget = editwidget.page_widget(project, pagenumber, call_data['pchange'], widget_name)
    except ServerError as e:
        raise FailPage(e.message)

    page_data[('widget_type','para_text')] = "Widget type : %s.%s" % (widgetdescription.modulename, widgetdescription.classname)
    page_data[('widget_name','para_text')] = "Widget name : %s" % (widget_name,)
    page_data[('field_type','para_text')] = "Field type : %s" % (field_arg,)


    # create dictionaries of {field_arg : field_datalist }
    fields_single = { arg[0]:arg for arg in widgetdescription.fields_single } # [ field arg, field ref, field type, valdt, jsonset, cssclass, cssstyle]
    fields_list = { arg[0]:arg for arg in widgetdescription.fields_list }  # [ field arg, field ref, field type, valdt, jsonset]
    fields_table = { arg[0]:arg for arg in widgetdescription.fields_table } # [ field arg, field ref, field type, valdt, jsonset]
    fields_dictionary = { arg[0]:arg for arg in widgetdescription.fields_dictionary } # [ field arg, field ref, field type, valdt, jsonset]

    if field_arg in fields_single:
        field_datalist = fields_single[field_arg]
    elif field_arg in fields_list:
        field_datalist = fields_list[field_arg]
    elif field_arg in fields_table:
        field_datalist = fields_table[field_arg]
    elif field_arg in fields_dictionary:
        field_datalist = fields_dictionary[field_arg]
    else:
        raise FailPage("Field not identified")

    if field_datalist[4]:
        page_data[('json_enabled','para_text')] = "JSON Enabled : Yes"
    else:
        page_data[('json_enabled','para_text')] = "JSON Enabled : No"

    if field_arg in fields_single:
        if field_datalist[5] or field_datalist[6]:
            default_value = skilift.fromjson.get_widget_default_field_value(project, widgetdescription.modulename, widgetdescription.classname, field_arg)
            if default_value:
                page_data[('field_default','para_text')] = "Default value : " + default_value
                page_data[('field_default','show')] = True

    field_name = _field_name(widget, field_arg)
    page_data[("adminhead","page_head","large_text")] = "(\'%s\',\'%s\')" % (widget_name, field_name)
    page_data[('show_field_name','para_text')] = "Field name : %s" % (field_name,)

    value, field_value = _field_value(widget, field_arg)

    # show the textblock description with .full, or if it doesnt exist, without the .full
    full_textref = field_datalist[1] + '.full'   # the field reference string
    adminaccesstextblocks = skilift.get_accesstextblocks(skilift.admin_project())

    if adminaccesstextblocks.textref_exists(full_textref):
        page_data[('widget_field_textblock','textblock_ref')] = full_textref
    else:
        page_data[('widget_field_textblock','textblock_ref')] = field_datalist[1]
    page_data[('field_name','input_text')] = field_name

    replace_strings = [widget_name+'\",\"'+field_name]

    if field_arg in fields_single:
        if field_datalist[2] == 'boolean':
            page_data[("field_submit",'show')] = True
            page_data[("boolean_field_value", "radio_checked")] = value
        else:
            page_data[("field_value",'show')] = True
            page_data[("field_value",'input_text')] = field_value
        if field_datalist[5] or field_datalist[6]:
            # add button to set given css class or style to defaults.json
            page_data[("css_default_desc",'show')] = True
            page_data[("set_field_default",'show')] = True
        else:
            page_data[("css_default_desc",'show')] = False
            page_data[("set_field_default",'show')] = False

        page_data[("show_field_value",'show')] = True
        page_data[("show_field_value",'para_text')] = "Field value : %s" % (field_value,)
        page_data[("widget_args_desc",'show')] = True
        page_data[("widget_args_desc",'replace_strings')] = replace_strings
    elif field_arg in fields_list:
        page_data[("widget_arg_list_desc",'show')] = True
        page_data[("widget_arg_list_desc",'replace_strings')] = replace_strings
        page_data[("css_default_desc",'show')] = False
        page_data[("set_field_default",'show')] = False
    elif field_arg in fields_table:
        page_data[("widget_arg_table_desc",'show')] = True
        page_data[("widget_arg_table_desc",'replace_strings')] = replace_strings
        page_data[("css_default_desc",'show')] = False
        page_data[("set_field_default",'show')] = False
    elif field_arg in fields_dictionary:
        page_data[("widget_arg_dict_desc",'show')] = True
        page_data[("widget_arg_dict_desc",'replace_strings')] = replace_strings
        page_data[("css_default_desc",'show')] = False
        page_data[("set_field_default",'show')] = False

    # Show validators
    if field_datalist[3]:
        page_data[("validators_desc",'show')] = True
        page_data[("validators_desc2",'show')] = True
        page_data[("add_validator",'show')] = True
        # create the contents for the validator_table
        contents = []
        if ("validators" in widget) and (field_arg in widget["validators"]):
            val_list = widget["validators"][field_arg]
            page_data["validator_table:show"] = True
            max_validator_index = len(val_list) - 1
            for index,validator in enumerate(val_list):
                if index:
                    up = True
                else:
                    # first item (index zero) has no up button
                    up = False
                if index < max_validator_index:
                    down = True
                else:
                    # last item has no down button
                    down = False
                table_pos =  str(index)
                contents.append([validator['class'], table_pos, table_pos, table_pos, table_pos, True, up, down, True])
            page_data["validator_table:contents"] = contents


    # set field_arg into session call_data
    call_data['field_arg'] = field_arg

    if 'validx' in call_data:
        del call_data['validx']



def oldretrieve_editfield(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Fills in the edit a widget field page"

    editedproj = call_data['editedproj']

    bits = utils.get_bits(call_data)

    page = bits.page
    section = bits.section
    widget = bits.widget

    if (page is None) and (section is None):
        raise FailPage("Page/section not identified")

    # Fill in header

    if 'field_arg' in call_data:
        field_arg = call_data['field_arg']
        if not field_arg:
            raise FailPage("Field not identified")
    elif bits.field_arg is not None:
        field_arg = bits.field_arg
    else:
        raise FailPage("Field not identified")

    page_data[('widget_type','para_text')] = "Widget type : %s.%s" % (widget.__class__.__module__.split('.')[-1], widget.__class__.__name__)
    page_data[('widget_name','para_text')] = "Widget name : %s" % (widget.name,)
    page_data[('field_type','para_text')] = "Field type : %s" % (field_arg,)

    field_info = widget.field_arg_info(field_arg)
    # (field name, field description ref, fieldvalue, str_fieldvalue, fieldarg class string, field type, field.valdt, field.jsonset, field.cssclass, field.csstyle)

    if not field_info:
        raise FailPage("Field not identified")

    if field_info[7]:
        page_data[('json_enabled','para_text')] = "JSON Enabled : Yes"
    else:
        page_data[('json_enabled','para_text')] = "JSON Enabled : No"

    if field_info[8] or field_info[9]:
        default_value = skilift.fromjson.get_widget_default_field_value(editedproj.proj_ident, widget.__class__.__module__.split('.')[-1], widget.__class__.__name__, field_arg)
        if default_value:
            page_data[('field_default','para_text')] = "Default value : " + default_value
            page_data[('field_default','show')] = True


    page_data[("adminhead","page_head","large_text")] = "(\'%s\',\'%s\')" % (widget.name, field_info[0])

    page_data[('show_field_name','para_text')] = "Field name : %s" % (field_info[0],)

    # if value is an Ident, show as project,number
    if isinstance(field_info[2], skiboot.Ident):
        field_value = field_info[2].to_comma_str()
    else:
        field_value = field_info[3]

    # show the textblock description with .full, or if it doesnt exist, without the .full
    full_textref = field_info[1] + '.full'   # the field reference string
    adminaccesstextblocks = skilift.get_accesstextblocks(skilift.admin_project())

    if adminaccesstextblocks.textref_exists(full_textref):
        page_data[('widget_field_textblock','textblock_ref')] = full_textref
    else:
        page_data[('widget_field_textblock','textblock_ref')] = field_info[1]


    page_data[('field_name','input_text')] = field_info[0]   # the field name

    if field_info[4] == 'args':
        if field_info[5] == 'boolean':
            page_data[("field_submit",'show')] = True
            page_data[("boolean_field_value", "radio_checked")] = field_info[2]
        else:
            page_data[("field_value",'show')] = True
            page_data[("field_value",'input_text')] = field_value
        if widget.fields[field_arg].cssclass or widget.fields[field_arg].cssstyle:
            # add button to set given css class or style to defaults.json
            page_data[("css_default_desc",'show')] = True
            page_data[("set_field_default",'show')] = True
        else:
            page_data[("css_default_desc",'show')] = False
            page_data[("set_field_default",'show')] = False

        page_data[("show_field_value",'show')] = True
        page_data[("show_field_value",'para_text')] = "Field value : %s" % (field_value,)
        page_data[("widget_args_desc",'show')] = True
        page_data[("widget_args_desc",'replace_strings')] = [widget.name+'\",\"'+field_info[0]]
    elif field_info[4] == 'arg_list':
        page_data[("widget_arg_list_desc",'show')] = True
        page_data[("widget_arg_list_desc",'replace_strings')] = [widget.name+'\",\"'+field_info[0]]
        page_data[("css_default_desc",'show')] = False
        page_data[("set_field_default",'show')] = False
    elif field_info[4] == 'arg_table':
        page_data[("widget_arg_table_desc",'show')] = True
        page_data[("widget_arg_table_desc",'replace_strings')] = [widget.name+'\",\"'+field_info[0]]
        page_data[("css_default_desc",'show')] = False
        page_data[("set_field_default",'show')] = False
    elif field_info[4] == 'arg_dict':
        page_data[("widget_arg_dict_desc",'show')] = True
        page_data[("widget_arg_dict_desc",'replace_strings')] = [widget.name+'\",\"'+field_info[0]]
        page_data[("css_default_desc",'show')] = False
        page_data[("set_field_default",'show')] = False

    # Show validators
    if field_info[6]:
        page_data[("validators_desc",'show')] = True
        page_data[("validators_desc2",'show')] = True
        page_data[("add_validator",'show')] = True
        # create the contents for the validator_table
        contents = []
        validators = widget.field_arg_val_list(field_arg)
        if validators:
            page_data["validator_table:show"] = True
            max_validator_index = len(validators) - 1
            for index,validator in enumerate(validators):
                if index:
                    up = True
                else:
                    # first item (index zero) has no up button
                    up = False
                if index < max_validator_index:
                    down = True
                else:
                    # last item has no down button
                    down = False
                table_pos =  str(index)
                contents.append([str(validator), table_pos, table_pos, table_pos, table_pos, True, up, down, True])
            page_data["validator_table:contents"] = contents


    # set field_arg into session call_data
    call_data['field_arg'] = field_arg

    if 'validx' in call_data:
        del call_data['validx']


def set_field_name(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Sets a widget field name"

    editedproj = call_data['editedproj']

    bits = utils.get_bits(call_data)

    page = bits.page
    section = bits.section
    widget = bits.widget
    field_arg = bits.field_arg

    if (page is None) and (section is None):
        raise FailPage("Page/section not identified")

    if widget is None:
        raise FailPage("Widget not identified")

    if field_arg is None:
        raise FailPage("Field not identified")

    if 'field_name' not in call_data:
        raise FailPage("Invalid name")

    new_name = call_data['field_name']
    if not new_name:
        raise FailPage("Invalid name")
    if new_name.startswith('_'):
        raise FailPage(message="Invalid name - cannot start with an underscore.")
    if (new_name == "show_error") and (field_arg != "show_error"):
        raise FailPage(message="Invalid name - show_error is a reserved name.")
    try:
        widget.set_name(field_arg, new_name)
    except ValidateError as e:
        raise FailPage(message=e.message)
    utils.save(call_data, page=page, section_name=bits.section_name, section=section)
    call_data['status'] = "Field name changed"



def set_field_value(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Sets a widget field value"

    editedproj = call_data['editedproj']

    bits = utils.get_bits(call_data)

    page = bits.page
    section = bits.section
    widget = bits.widget
    field_arg = bits.field_arg

    if (page is None) and (section is None):
        raise FailPage("Page/section not identified")

    if widget is None:
        raise FailPage("Widget not identified")

    if field_arg is None:
        raise FailPage("Field not identified")

    # is this field of class args?
    field_info = widget.field_arg_info(field_arg)
    # (field name, field description ref, fieldvalue, str_fieldvalue, fieldarg class string, field type, field.valdt, field.jsonset, field.cssclass, field.csstyle)

    if not field_info:
        raise FailPage("Field not identified")

    if field_info[4] != 'args':
        raise FailPage("Cannot set a value on this field")

    if 'field_value' not in call_data:
        raise FailPage("Field value not found")

    field_value = call_data['field_value']

    if (field_info[5] == "ident" or field_info[5] == "url") and field_value.isdigit():
        # The user is inputting a digit as a page ident
        field_value = editedproj.proj_ident + '_' + field_value

    try:
        widget.set_field_value(field_arg, field_value)
    except ValidateError as e:
        raise FailPage(message=e.message)

    utils.save(call_data, page=page, section_name=bits.section_name, section=section)
    call_data['status'] = "Field value changed"


def set_field_default(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Sets a widget field default value"

    editedproj = call_data['editedproj']

    bits = utils.get_bits(call_data)

    page = bits.page
    section = bits.section
    widget = bits.widget
    field_arg = bits.field_arg

    if (page is None) and (section is None):
        raise FailPage("Page/section not identified")

    if widget is None:
        raise FailPage("Widget not identified")

    if field_arg is None:
        raise FailPage("Field not identified")

    # is this field of class args?
    field_info = widget.field_arg_info(field_arg)
    # (field name, field description ref, fieldvalue, str_fieldvalue, fieldarg class string, field type, field.valdt, field.jsonset, field.cssclass, field.csstyle)

    if not field_info:
        raise FailPage("Field not identified")

    if field_info[4] != 'args':
        raise FailPage("Cannot set a default value on this field")

    if field_info[8] or field_info[9]:
        # set the default value
        result = skilift.fromjson.save_widget_default_field_value(editedproj.proj_ident,
                                    widget.__module__.split(".")[-1],
                                    widget.__class__.__name__,
                                    field_arg,
                                    field_info[3])
        if result:
            if field_info[3]:
                call_data['status'] = "Field default value set to %s" % (field_info[3],)
            else:
                call_data['status'] = "Field default value removed"
            return

    raise FailPage("Unable to set default")



def retrieve_container(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Edits a widget container"

    # remove any unwanted fields from session call_data
    if 'location' in call_data:
        del call_data['location']
    if 'part' in call_data:
        del call_data['part']

    # get data
    if ("left_nav","navbuttons","nav_links") in call_data:
        # should be submitted as widgetname-containernumber
        widget_container = call_data["left_nav","navbuttons","nav_links"].split("-")
        if len(widget_container) != 2:
            raise FailPage(message="Invalid container")
        widget_name = widget_container[0]
        try:
            container = int(widget_container[1])
        except:
            raise FailPage(message="Invalid container")
    elif ('widget_name' in call_data) and ('container' in call_data):
        widget_name = call_data['widget_name']
        container = call_data['container']
    else:
        raise FailPage(message="Invalid container")

    # and this is the container to be edited, it is now set into session data
    call_data['widget_name'] = widget_name
    call_data['container'] = container

    # Fill in header
    page_data[("adminhead","page_head","large_text")] = "Widget " + widget_name + " container: " + str(container)

    ## these bits may eventually be replaced by skilift api

    editedprojname = call_data['editedprojname']
    editedproj = skiboot.getproject(editedprojname)
    section = None
    page = None
    if 'section_name' in call_data:
        section = editedproj.section(call_data['section_name'])
    elif 'page_number' in call_data:
        page = editedproj.get_item(call_data['page_number'])  # actual page, not a copy
    else:
        raise FailPage(message="No section or page given")
    if section:
        widget = section.widgets.get(widget_name)
    else:
        widget = page.widgets.get(widget_name)
    if widget is None:
        raise FailPage(message="Widget not found")

    # so header text and navigation done, now continue with the page contents
    page_data[('container_description','textblock_ref')] = widget.get_container_ref(container)

    if widget.is_container_empty(container):
        # empty container
        page_data[('further_description','para_text')] = "The container is empty. Please choose an item to insert."
        # do not show the container table
        page_data[('editdom', 'show')] = False
        # table contents do not include Insert a section
        page_data[("insertlist","links")] = [
                ["Insert text", "inserttext", ""],
                ["Insert a TextBlock", "insert_textblockref", ""],
                ["Insert html symbol", "insertsymbol", ""],
                ["Insert comment", "insertcomment", ""],
                ["Insert an html element", "part_insert", ""],
                ["Insert a Widget", "list_widget_modules", ""]
                ]
        if section is None:
            # going into a page, so a sectionplaceholder can be added
            page_data[("insertlist","links")].append(["Insert a Section", "placeholder_insert", ""])
        # set location, where item is to be inserted
        call_data['location'] = (widget.name, container, (0,))
        return

    # part has content, do not show insertlist or upload button
    page_data[('further_description','para_text')] = "Choose an item to edit."
    page_data[('insertlist', 'show')] = False
    page_data['upload_description', 'show'] = False
    page_data['uploadpart', 'show'] = False

    # fill in the table
    call_data['location_string'] = widget.name
    retrieve_container_dom(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang)




def retrieve_container_dom(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "this call fills in the container dom table"

    editedprojname = call_data['editedprojname']

    pagenumber = None
    section_name = None

    if "page_number" in call_data:
        pagenumber = call_data["page_number"]
    elif "section_name" in call_data:
        section_name = call_data["section_name"]
    else:
        raise FailPage(message = "No page or section given")

    # location_string is the widget name

    if 'location_string' in call_data:
        location_string = call_data['location_string']
    elif 'widget_name' in call_data:
        location_string = call_data['widget_name']
    else:
        raise FailPage(message = "widget_name not in call_data")


    if 'container' not in call_data:
        raise FailPage(message = "container not in call_data")
    container = call_data["container"]

    try:
        contdict = fromjson.container_to_OD(editedprojname, pagenumber, section_name, location_string, container)
        partdict = {'parts': contdict['container']}
    except:
       raise FailPage(message = "call to fromjson.container_to_OD failed")

    # widget editdom,domtable is populated with fields

    #    dragrows: A two element list for every row in the table, could be empty if no drag operation
    #              0 - True if draggable, False if not
    #              1 - If 0 is True, this is data sent with the call wnen a row is dropped
    #    droprows: A two element list for every row in the table, could be empty if no drop operation
    #              0 - True if droppable, False if not
    #              1 - text to send with the call when a row is dropped here
    #    dropident: ident or label of target, called when a drop occurs which returns a JSON page

    #    cols: A two element list for every column in the table, must be given with empty values if no links
    #              0 - target HTML page link ident of buttons in each column, if col1 not present or no javascript
    #              1 - target JSON page link ident of buttons in each column,

    #    contents: A list for every element in the table, should be row*col lists
    #               0 - text string, either text to display or button text
    #               1 - A 'style' string set on the td cell, if empty string, no style applied
    #               2 - Is button? If False only text will be shown, not a button, button class will not be applied
    #                       If True a link to link_ident/json_ident will be set with button_class applied to it
    #               3 - The get field value of the button link, empty string if no get field

    # create the table

    top_row_widget = "Widget %s" % location_string
    top_row_container = "Container %s" % container

    domcontents = [
                   [top_row_widget, '', False, '' ],
                   [top_row_container, '', False, '' ],
                   ['', '', False, '' ],
                   ['', '', False, '' ],
                   ['', '', False, '' ],
                   ['', '', False, '' ],
                   ['', '', False, '' ],
                   ['', '', False, '' ],
                   ['', '', False, '' ]
                ]


    # add further items to domcontents
    part_string_list = []

    part_loc = location_string + '-' + str(container)

    rows = utils.domtree(partdict, part_loc, domcontents, part_string_list)
    
    page_data['editdom', 'domtable', 'contents']  = domcontents

    # for each column: html link, JSON link
    page_data['editdom', 'domtable', 'cols']  =  [    ['',''],                                       # tag name, no link
                                                      ['',''],                                       # brief, no link
                                                      ['move_up_in_container_dom',44540],            # up arrow
                                                      ['move_up_right_in_container_dom',44550],      # up right
                                                      ['move_down_in_container_dom',44560],          # down
                                                      ['move_down_right_in_container_dom',44570],    # down right
                                                      ['edit_container_dom',''],                     # edit, html only
                                                      ['add_to_container_dom',''],                   # insert/append, html only
                                                      ['remove_container_dom','']                    # remove, html only
                                                   ]
    # for every row in the table
    dragrows = [[ False, '']]
    droprows = [[ True, part_loc]]

    # for each row
    if rows>1:
        for row in range(0, rows-1):
            dragrows.append( [ True, part_string_list[row]] )
            droprows.append( [ True, part_string_list[row]] )

    page_data['editdom', 'domtable', 'dragrows']  = dragrows
    page_data['editdom', 'domtable', 'droprows']  = droprows
    page_data['editdom', 'domtable', 'dropident'] = 'move_in_container_dom'



def back_to_parent_container(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Sets call_data['widget_name'] to parent_widget and call_data['container'] to parent_container"

    bits = utils.get_bits(call_data)

    if (bits.parent_widget is None) or (bits.parent_container is None):
        raise FailPage(message="Invalid container")

    utils.no_ident_data(call_data)

    if bits.page is not None:
        call_data['page'] = bits.page
    if bits.section_name is not None:
        call_data['section_name'] = bits.section_name

    call_data['widget_name'] = bits.parent_widget.name
    call_data['container'] = bits.parent_container



def edit_container_dom(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Called by domtable to edit an item in a container"

    editedprojname = call_data['editedprojname']
    pagenumber = None
    section_name = None

    if "page_number" in call_data:
        pagenumber = call_data["page_number"]
    elif "section_name" in call_data:
        section_name = call_data["section_name"]
    else:
        raise FailPage(message = "No page or section given")
    if ('editdom', 'domtable', 'contents') not in call_data:
        raise FailPage(message = "item to edit missing")

    part = call_data['editdom', 'domtable', 'contents']

    # so part is widget_name, container with location string of integers

    # create location which is a tuple or list consisting of three items:
    # a string of widget name
    # a container integer
    # a tuple or list of location integers
    location_list = part.split('-')
    # first item should be a string, rest integers
    if len(location_list) < 3:
        raise FailPage("Item to edit has not been recognised")

    try:
        widget_name = location_list[0]
        container = int(location_list[1])
        location_integers = [ int(i) for i in location_list[2:]]
    except:
        raise FailPage("Item to edit has not been recognised")


    part_tuple = skilift.part_info(editedprojname, pagenumber, section_name, [widget_name, container, location_integers])
    if part_tuple is None:
        raise FailPage("Item to edit has not been recognised")

    if part_tuple.name:
        # item to edit is a widget
        call_data['part_tuple'] = part_tuple
        raise GoTo(target = 54006, clear_submitted=True)
    if part_tuple.part_type == "Part":
        # edit the html part
        call_data['part_tuple'] = part_tuple
        raise GoTo(target = 53007, clear_submitted=True)
    if part_tuple.part_type == "ClosedPart":
        # edit the html closed part
        call_data['part_tuple'] = part_tuple
        raise GoTo(target = 53007, clear_submitted=True)
    if part_tuple.part_type == "HTMLSymbol":
        # edit the symbol
        call_data['part_tuple'] = part_tuple
        raise GoTo(target = 51107, clear_submitted=True)
    if part_tuple.part_type == "str":
        # edit the text
        call_data['part_tuple'] = part_tuple
        raise GoTo(target = 51017, clear_submitted=True)
    if part_tuple.part_type == "TextBlock":
        # edit the TextBlock
        call_data['part_tuple'] = part_tuple
        raise GoTo(target = 52017, clear_submitted=True)
    if part_tuple.part_type == "Comment":
        # edit the Comment
        call_data['part_tuple'] = part_tuple
        raise GoTo(target = 51207, clear_submitted=True)
    if (not section_name) and (part_tuple.part_type == "SectionPlaceHolder"):
        # edit the SectionPlaceHolder
        call_data['part_tuple'] = part_tuple
        raise GoTo(target = 55007, clear_submitted=True)

    raise FailPage("Item to edit has not been recognised")


def add_to_container_dom(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    """Called by domtable to either insert or append an item in a container
       sets page_data to populate the insert or append page and then go to appropriate template page"""

    editedprojname = call_data['editedprojname']
    pagenumber = None
    section_name = None

    if "page_number" in call_data:
        pagenumber = call_data["page_number"]
    elif "section_name" in call_data:
        section_name = call_data["section_name"]
    else:
        raise FailPage(message = "No page or section given")
    if ('editdom', 'domtable', 'contents') not in call_data:
        raise FailPage(message = "item to append to missing")

    part = call_data['editdom', 'domtable', 'contents']

    # so part is widget_name, container with location string of integers

    # create location which is a tuple or list consisting of three items:
    # a string of widget name
    # a container integer
    # a tuple or list of location integers
    location_list = part.split('-')
    # first item should be a string, rest integers
    if len(location_list) < 3:
        raise FailPage("Item to append to has not been recognised")

    try:
        widget_name = location_list[0]
        container = int(location_list[1])
        location_integers = [ int(i) for i in location_list[2:]]
    except:
        raise FailPage("Item to append to has not been recognised")

    # location is a tuple of widget_name, container, tuple of location integers
    location = (widget_name, container, location_integers)

    part_tuple = skilift.part_info(editedprojname, pagenumber, section_name, location)
    if part_tuple is None:
        raise FailPage("Item to append to has not been recognised")

    # goto either the install or append page

    call_data['part'] = part                 ################ note, in future pass part_tuple rather than part
    call_data['location'] = location         ########## also part_tuple should replace location

    # Fill in menu of items, Part items have insert, others have append


    if (part_tuple.part_type == "Part") or (part_tuple.part_type == "Section"):
        # insert
        page_data[("adminhead","page_head","large_text")] = "Choose an item to insert"
        page_data[("insertlist","links")] = [
                                                ["Insert text", "inserttext", ""],
                                                ["Insert a TextBlock", "insert_textblockref", ""],
                                                ["Insert html symbol", "insertsymbol", ""],
                                                ["Insert comment", "insertcomment", ""],
                                                ["Insert an html element", "part_insert", ""],
                                                ["Insert a Widget", "list_widget_modules", ""]
                                            ]
        if not section_name:
            # going into a page, so a sectionplaceholder can be added
            page_data[("insertlist","links")].append(["Insert a Section", "placeholder_insert", ""])
        raise GoTo(target = '23609', clear_submitted=True)
    else:
        # append
        page_data[("adminhead","page_head","large_text")] = "Choose an item to append"
        page_data[("appendlist","links")] = [
                                                ["Append text", "inserttext", ""],
                                                ["Append a TextBlock", "insert_textblockref", ""],
                                                ["Append html symbol", "insertsymbol", ""],
                                                ["Append comment", "insertcomment", ""],
                                                ["Append an html element", "part_insert", ""],
                                                ["Append a Widget", "list_widget_modules", ""]
                                            ]
        if not section_name:
            # going into a page, so a sectionplaceholder can be added
            page_data[("appendlist","links")].append(["Append a Section", "placeholder_insert", ""])
        raise GoTo(target = '23509', clear_submitted=True)


def remove_container_dom(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Called by domtable to remove an item in a container"

    editedprojname = call_data['editedprojname']
    pagenumber = None
    section_name = None

    if "page_number" in call_data:
        pagenumber = call_data["page_number"]
    elif "section_name" in call_data:
        section_name = call_data["section_name"]
    else:
        raise FailPage(message = "No page or section given")
    if ('editdom', 'domtable', 'contents') not in call_data:
        raise FailPage(message = "item to remove missing")

    part = call_data['editdom', 'domtable', 'contents']

    # so part is widget_name, container with location string of integers

    # create location which is a tuple or list consisting of three items:
    # a string of widget name
    # a container integer
    # a tuple or list of location integers
    location_list = part.split('-')
    # first item should be a string, rest integers
    if len(location_list) < 3:
        raise FailPage("Item to remove has not been recognised")

    try:
        widget_name = location_list[0]
        container = int(location_list[1])
        location_integers = [ int(i) for i in location_list[2:]]
    except:
        raise FailPage("Item to remove has not been recognised")

    # location is a tuple of widget_name, container, tuple of location integers
    location = (widget_name, container, location_integers)

    part_tuple = skilift.part_info(editedprojname, pagenumber, section_name, location)
    if part_tuple is None:
        raise FailPage("Item to remove has not been recognised")

    # once item is deleted, no info on the item should be
    # left in call_data - this may not be required in future
    if 'location' in call_data:
        del call_data['location']
    if 'part' in call_data:
        del call_data['part']
    if 'part_loc' in call_data:
        del call_data['part_loc']

    # remove the item using functions from skilift.editsection and skilift.editpage
    if pagenumber is None:
        # remove the item from a section
        try:
            call_data['schange'] = editsection.del_location(editedprojname, section_name, call_data['schange'], location)
        except ServerError as e:
            raise FailPage(message = e.message)
    else:
        # remove the item from a page
        try:
            call_data['pchange'] = editpage.del_location(editedprojname, pagenumber, call_data['pchange'], location)
        except ServerError as e:
            raise FailPage(message = e.message)
        # page has changed, hopefully, in due course, this line will not be needed
        call_data['page'] = skiboot.from_ident(pagenumber, proj_ident=editedprojname)

    call_data['container'] = container
    call_data['widget_name'] = widget_name


def _item_to_move(call_data):
    "Gets the item to be moved"
    editedprojname = call_data['editedprojname']
    pagenumber = None
    section_name = None

    if "page_number" in call_data:
        pagenumber = call_data["page_number"]
    elif "section_name" in call_data:
        section_name = call_data["section_name"]
    else:
        raise FailPage(message = "No page or section given")
    if ('editdom', 'domtable', 'contents') not in call_data:
        raise FailPage(message = "item to move missing")

    part = call_data['editdom', 'domtable', 'contents']

    # so part is widget_name, container with location string of integers

    # create location which is a tuple or list consisting of three items:
    # a string of widget name
    # a container integer
    # a tuple or list of location integers
    location_list = part.split('-')
    # first item should be a string, rest integers
    if len(location_list) < 3:
        raise FailPage("Item to move has not been recognised")

    try:
        widget_name = location_list[0]
        container = int(location_list[1])
        location_integers = [ int(i) for i in location_list[2:]]
    except:
        raise FailPage("Item to move has not been recognised")

    # location is a tuple of widget_name, container, tuple of location integers
    location = (widget_name, container, location_integers)
    call_data['container'] = container
    call_data['widget_name'] = widget_name

    part_tuple = skilift.part_info(editedprojname, pagenumber, section_name, location)
    if part_tuple is None:
        raise FailPage("Item to move has not been recognised")
    return part_tuple


def move_up_in_container_dom(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Called by domtable to move an item in a container up"

    part_tuple = _item_to_move(call_data)
    location = part_tuple.location
    location_integers = location[2]

    if (len(location_integers) == 1) and (location_integers[0] == 0):
        # at top, cannot be moved
        raise FailPage("Cannot be moved up")

    if location_integers[-1] == 0:
        # move up to next level
        new_location_integers = location_integers[:-1]
    else:
        # swap parts on same level
        new_location_integers = list(location_integers[:-1])
        new_location_integers.append(location_integers[-1] - 1)

    # after a move, location is wrong, so remove from call_data
    if 'location' in call_data:
        del call_data['location']
    if 'part' in call_data:
        del call_data['part']
    if 'part_top' in call_data:
        del call_data['part_top']
    if 'part_loc' in call_data:
        del call_data['part_loc']

    # move the item
    try:
        if part_tuple.section_name:
            # move the part in a section, using skilift.editsection.move_location(project, section_name, from_location, to_location)
            editsection.move_location(part_tuple.project, part_tuple.section_name, location, (location[0], location[1], new_location_integers))
        else:
            # move the part in a page, using skilift.editpage.move_location(project, pagenumber, from_location, to_location)
            editpage.move_location(part_tuple.project, part_tuple.pagenumber, location, (location[0], location[1], new_location_integers))
    except ServerError as e:
        raise FailPage(message = e.message)


def move_up_right_in_container_dom(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Called by domtable to move an item in a container up and to the right"

    part_tuple = _item_to_move(call_data)
    location = part_tuple.location
    location_integers = location[2]

    if location_integers[-1] == 0:
        # at top of a part, cannot be moved
        raise FailPage("Cannot be moved up")
    new_parent_integers = list(location_integers[:-1])
    new_parent_integers.append(location_integers[-1] - 1)
    new_parent_location = (location[0], location[1], new_parent_integers)

    new_parent_tuple = skilift.part_info(part_tuple.project, part_tuple.pagenumber, part_tuple.section_name, new_parent_location)

    if new_parent_tuple is None:
        raise FailPage("Cannot be moved up")
    if new_parent_tuple.part_type != "Part":
        raise FailPage("Cannot be moved up")

    items_in_new_parent = len(skilift.part_contents(part_tuple.project, part_tuple.pagenumber, part_tuple.section_name, new_parent_location))

    new_location_integers =  tuple(new_parent_integers + [items_in_new_parent])

    # after a move, location is wrong, so remove from call_data
    if 'location' in call_data:
        del call_data['location']
    if 'part' in call_data:
        del call_data['part']
    if 'part_top' in call_data:
        del call_data['part_top']
    if 'part_loc' in call_data:
        del call_data['part_loc']

    # move the item
    try:
        if part_tuple.section_name:
            # move the part in a section, using skilift.editsection.move_location(project, section_name, from_location, to_location)
            editsection.move_location(part_tuple.project, part_tuple.section_name, location, (location[0], location[1], new_location_integers))
        else:
            # move the part in a page, using skilift.editpage.move_location(project, pagenumber, from_location, to_location)
            editpage.move_location(part_tuple.project, part_tuple.pagenumber, location, (location[0], location[1], new_location_integers))
    except ServerError as e:
        raise FailPage(message = e.message)


def move_down_in_container_dom(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Called by domtable to move an item in a container down"

    part_tuple = _item_to_move(call_data)
    location = part_tuple.location
    location_integers = location[2]


    if len(location_integers) == 1:
        # Just at immediate level below top
        parent_location = (location[0], location[1], ())
        items_in_parent = len(skilift.part_contents(part_tuple.project, part_tuple.pagenumber, part_tuple.section_name, parent_location))
        if location_integers[0] == (items_in_parent-1):
            # At end, cannot be moved
            raise FailPage("Cannot be moved down")
        new_location_integers = (location_integers[0]+2,)
    else:
        parent_integers = tuple(location_integers[:-1])
        parent_location = (location[0], location[1], parent_integers)
        items_in_parent = len(skilift.part_contents(part_tuple.project, part_tuple.pagenumber, part_tuple.section_name, parent_location))
        if location_integers[-1] == (items_in_parent-1):
            # At end of a part, so move up a level
            new_location_integers = list(parent_integers[:-1])
            new_location_integers.append(parent_integers[-1] + 1)
        else:
            # just insert into current level
            new_location_integers = list(parent_integers)
            new_location_integers.append(location_integers[-1] + 2)

    # after a move, location is wrong, so remove from call_data
    if 'location' in call_data:
        del call_data['location']
    if 'part' in call_data:
        del call_data['part']
    if 'part_top' in call_data:
        del call_data['part_top']
    if 'part_loc' in call_data:
        del call_data['part_loc']

    # move the item
    try:
        if part_tuple.section_name:
            # move the part in a section, using skilift.editsection.move_location(project, section_name, from_location, to_location)
            editsection.move_location(part_tuple.project, part_tuple.section_name, location, (location[0], location[1], new_location_integers))
        else:
            # move the part in a page, using skilift.editpage.move_location(project, pagenumber, from_location, to_location)
            editpage.move_location(part_tuple.project, part_tuple.pagenumber, location, (location[0], location[1], new_location_integers))
    except ServerError as e:
        raise FailPage(message = e.message)


def move_down_right_in_container_dom(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Called by domtable to move an item in a container down and to the right"

    part_tuple = _item_to_move(call_data)
    location = part_tuple.location
    location_integers = location[2]

    if len(location_integers) == 1:
        parent_location = (location[0], location[1], ())
    else:
        parent_integers = list(location_integers[:-1])
        parent_location = (location[0], location[1], parent_integers)
    items_in_parent = len(skilift.part_contents(part_tuple.project, part_tuple.pagenumber, part_tuple.section_name, parent_location))
    if location_integers[-1] == (items_in_parent-1):
        # At end of a block, cannot be moved
        raise FailPage("Cannot be moved down")
    new_parent_integers = list(location_integers[:-1])
    new_parent_integers.append(location_integers[-1] + 1)
    new_parent_location = (location[0], location[1], new_parent_integers)
    new_parent_tuple = skilift.part_info(part_tuple.project, part_tuple.pagenumber, part_tuple.section_name, new_parent_location)

    if new_parent_tuple is None:
        raise FailPage("Cannot be moved down")
    if not (new_parent_tuple.part_type == 'Part' or new_parent_tuple.part_type == 'Section'):
        raise FailPage("Cannot be moved down")

    new_location_integers = tuple(new_parent_integers+[0])

    # after a move, location is wrong, so remove from call_data
    if 'location' in call_data:
        del call_data['location']
    if 'part' in call_data:
        del call_data['part']
    if 'part_top' in call_data:
        del call_data['part_top']
    if 'part_loc' in call_data:
        del call_data['part_loc']

    # move the item
    try:
        if part_tuple.section_name:
            # move the part in a section, using skilift.editsection.move_location(project, section_name, from_location, to_location)
            editsection.move_location(part_tuple.project, part_tuple.section_name, location, (location[0], location[1], new_location_integers))
        else:
            # move the part in a page, using skilift.editpage.move_location(project, pagenumber, from_location, to_location)
            editpage.move_location(part_tuple.project, part_tuple.pagenumber, location, (location[0], location[1], new_location_integers))
    except ServerError as e:
        raise FailPage(message = e.message)


def move_in_container_dom(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Called by domtable to move an item in a container after a drag and drop"

    if ('editdom', 'domtable', 'dragrows') not in call_data:
        raise FailPage(message = "item to drop missing")
    editedprojname = call_data['editedprojname']
    pagenumber = None
    section_name = None

    if "page_number" in call_data:
        pagenumber = call_data["page_number"]
    elif "section_name" in call_data:
        section_name = call_data["section_name"]
    else:
        raise FailPage(message = "No page or section given")

    part_to_move = call_data['editdom', 'domtable', 'dragrows']

    # so part_to_move is widget name with container and location string of integers
    # create location which is a tuple or list consisting of three items:
    # a string of widget name
    # a container integer
    # a tuple or list of location integers
    location_list = part_to_move.split('-')
    # first item should be a string, rest integers
    if len(location_list) < 3:
        raise FailPage("Item to move has not been recognised")

    try:
        widget_name = location_list[0]
        container = int(location_list[1])
        location_to_move_integers = [ int(i) for i in location_list[2:]]
    except:
        raise FailPage("Item to move has not been recognised")

    # location is a tuple of widget_name, container, tuple of location integers
    location_to_move = (widget_name, container, location_to_move_integers)
    call_data['container'] = container
    call_data['widget_name'] = widget_name


    # new target location

    target_part = call_data['editdom', 'domtable', 'droprows']

    # so target_part is widget name with location string of integers

    # create location which is a tuple or list consisting of three items:
    # a string of widget name
    # a container integer
    # a tuple or list of location integers

    location_list = target_part.split('-')
    # first item should be a string, rest integers
    if len(location_list) < 2:
        raise FailPage("target of move has not been recognised")
 
    if widget_name != location_list[0]:
        raise FailPage("Invalid move, widget name differs")

    if container != int(location_list[1]):
        raise FailPage("Invalid move, container number differs")

    if len(location_list) == 2:
            # At the container top row
            new_location_integers = [0]
    else:
        try:
            target_location_integers = [ int(i) for i in location_list[2:]]
        except:
            raise FailPage("Invalid move, location not accepted")

        # location is a tuple of widget_name, container, tuple of location integers
        target_location = (widget_name, container, target_location_integers)

        # get target part_tuple from project, pagenumber, section_name, target_location
        target_part_tuple = skilift.part_info(editedprojname, pagenumber, section_name, target_location)
        if target_part_tuple is None:
            raise FailPage("Target has not been recognised")

        if (target_part_tuple.part_type == "Part") or (target_part_tuple.part_type == "Section"):
            # insert
            if target_location_integers:
                new_location_integers = list(target_location_integers)
                new_location_integers.append(0)
            else:
                new_location_integers = [0]
        else:
            # append
            new_location_integers = list(target_location_integers)
            new_location_integers[-1] = new_location_integers[-1] + 1

    # after a move, location is wrong, so remove from call_data
    if 'location' in call_data:
        del call_data['location']
    if 'part' in call_data:
        del call_data['part']
    if 'part_top' in call_data:
        del call_data['part_top']
    if 'part_loc' in call_data:
        del call_data['part_loc']

    # move the item
    try:
        if section_name:
            # move the part in a section, using skilift.editsection.move_location(project, section_name, from_location, to_location)
            editsection.move_location(editedprojname, section_name, location_to_move, (widget_name, container, new_location_integers))
        else:
            # move the part in a page, using skilift.editpage.move_location(project, pagenumber, from_location, to_location)
            editpage.move_location(editedprojname, pagenumber, location_to_move, (widget_name, container, new_location_integers))
    except ServerError as e:
        raise FailPage(message = e.message)


