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
from ....skilift import fromjson

from ....ski import skiboot, tag, widgets
from .. import utils
from ....ski.excepts import FailPage, ValidateError, GoTo

# a search for anything none-alphanumeric and not an underscore
_AN = re.compile('[^\w]')


def retrieve_editwidget(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Fills in the edit a widget page"

    editedproj = call_data['editedproj']

    # get data
    bits = utils.get_bits(call_data)

    page = bits.page
    section = bits.section
    widget = bits.widget

    if widget is None:
        # widget not derived from session data, must be from submitted data
        widget = bits.part

    if (widget is None) and ('widget_name' in call_data):
        widget_name = call_data['widget_name']
        if section:
            widget = section.widgets.get(widget_name)
        if page:
            widget = page.widgets.get(widget_name)

    if not (isinstance(widget, widgets.Widget) or isinstance(widget, widgets.ClosedWidget)):
        raise FailPage("Widget to edit not identified")

    # and this is the widget to be edited, it is now set into session data
    call_data['widget_name'] = widget.name
    if section:
        call_data['section'] = section
    if page:
        call_data['page'] = page

    if page is not None:
        parent_widget, parent_container = widget.get_parent_widget(page)
    else:
        parent_widget, parent_container = widget.get_parent_widget(section)

    # Fill in header

    # navigator boxes
    utils.nav_boxes(call_data, page, section, bits.page_top, parent_container)

    page_data[("adminhead","page_head","large_text")] = widget.name

    if 'status' in call_data:
        page_data[("adminhead","page_head","small_text")] = call_data['status']
    else:
        page_data[("adminhead","page_head","small_text")] = "Edit the widget"

    page_data[('widget_type','para_text')] = "This widget is of type %s.%s." % (widget.__class__.__module__.split('.')[-1], widget.__class__.__name__)
    page_data[('widget_textblock','textblock_ref')] = widget.description_ref()
    page_data[('widget_name','input_text')] = widget.name
    page_data[('widget_brief','input_text')] = widget.brief

    args, arg_list, arg_table, arg_dict = widget.classargs()
    # lists of [ field arg, field ref, field type]

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
            # get string value
            field_info = widget.field_arg_info(arg[0])
            # (field name, field description ref, fieldvalue, str_fieldvalue, fieldarg class string, field type, field.valdt, field.jsonset, field.cssclass, field.csstyle)
            if not field_info:
                raise FailPage(message = "Error in widget")
            name = field_info[0]
            if field_info[6]:
                name = "* " + name
                args_valdt = True
            # if value is an Ident of this project, just put ident number
            if isinstance(field_info[2], skiboot.Ident) and (field_info[2].proj == editedproj.proj_ident):
                field_value = str(field_info[2].num)
            else:
                field_value = field_info[3]
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
            name = widget.get_name(arg[0])
            if widget.get_field_valdt(name):
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
            name = widget.get_name(arg[0])
            if widget.get_field_valdt(name):
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
            name = widget.get_name(arg[0])
            if widget.get_field_valdt(name):
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
    page_data[('widget_code','pre_text')] = str(widget)

    #          append further nav links for containers
    #          0 : The url, label or ident of the target page of the link
    #          1 : The displayed text of the link
    #          2 : If True, ident is appended to link even if there is no get field
    #          3 : The get field data to send with the link

    if widget.can_contain():
        page_data[('containerdesc','show')] = True
        if widget.len_containers() == 1:
            call_data['extend_nav_buttons'].append(['edit_container', 'Container', True, '0'])
        else:
            # multiple containers
            for n in range(widget.len_containers()):
                # set up a link for each container
                link_text = "Container %s" % n
                call_data['extend_nav_buttons'].append(['edit_container', link_text, True, str(n)])

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

    editedproj = call_data['editedproj']

    bits = utils.get_bits(call_data)

    page = bits.page
    section = bits.section
    widget = bits.widget

    if (page is None) and (section is None):
        raise FailPage("Page/section not identified")

    if page:
        call_data['page_number'] = page.ident.num
    if bits.section_name:
        call_data['section_name'] = bits.section_name


    if widget is None:
        raise FailPage("Widget not identified")

    if 'new_widget_name' in call_data:
        new_name = call_data['new_widget_name']
        if not new_name:
            raise FailPage("Invalid name")
        new_lower_name = new_name.lower()
        if (new_lower_name == 'body') or (new_lower_name == 'head') or (new_lower_name == 'svg')  or (new_lower_name == 'show_error'):
            raise FailPage(message="Unable to rename the widget, the name given is reserved")
        if _AN.search(new_name):
            raise FailPage(message="Invalid name, alphanumeric and underscore only")
        if new_name[0] == '_':
            raise FailPage(message="Invalid name, must not start with an underscore")
        if new_name.isdigit():
            raise FailPage(message="Unable to rename the widget, the name must include some letters")
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

        widget.name = new_name
        utils.save(call_data, page=page, section_name=bits.section_name, section=section)
        call_data['status'] = "Widget name changed"
    elif 'widget_brief' in call_data:
        widget.brief = call_data['widget_brief']
        utils.save(call_data, page=page, section_name=bits.section_name, section=section)
        call_data['status'] = "Widget description changed"
    else:
        raise FailPage("Invalid entry")
    call_data['widget_name'] = widget.name


def retrieve_editfield(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Fills in the edit a widget field page"

    editedproj = call_data['editedproj']

    bits = utils.get_bits(call_data)

    page = bits.page
    section = bits.section
    widget = bits.widget

    if (page is None) and (section is None):
        raise FailPage("Page/section not identified")

    if 'status' in call_data:
        page_data[("adminhead","page_head","small_text")] = call_data['status']
    else:
        page_data[("adminhead","page_head","small_text")] = "Edit the widget field"

    # Fill in header

    # navigator boxes
    utils.nav_boxes(call_data, page, section, bits.page_top, bits.parent_container, widget)


    if 'field' in call_data:
        field_arg = call_data['field']
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



def edit_container(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Edits a widget container"

    # remove any unwanted fields from session call_data
    if 'location' in call_data:
        del call_data['location']
    if 'part' in call_data:
        del call_data['part']

    # get data
    bits = utils.get_bits(call_data)

    page = bits.page
    section = bits.section
    widget = bits.widget

    # container is either from submitted container_part, or from container

    if bits.container_part is None:
        # container_part not submitted, therefore must be derived from session data
        container = bits.container
    else:
        # container from submitted container_part
        container = bits.container_part

    if container is None:
        raise FailPage(message="Invalid container")

    # and this is the container to be edited, it is now set into session data
    call_data['container'] = container

    # Fill in header

    # navigator boxes
    utils.nav_boxes(call_data, page, section, bits.page_top, bits.parent_container, widget)

    page_data[("adminhead","page_head","large_text")] = "Edit Widget Container"

    if 'status' in call_data:
        page_data[("adminhead","page_head","small_text")] = call_data['status']
    else:
        page_data[("adminhead","page_head","small_text")] = widget.name + " container: " + str(container)

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
    location_string = call_data['location_string']
    container = call_data["container"]

    contdict = fromjson.container_to_OD(editedprojname, pagenumber, section_name, location_string, container)

    partdict = {'parts': contdict['container']}

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
    page_data['editdom', 'domtable', 'cols']  =  [    ['',''],                                    # tag name, no link
                                                      ['',''],                                    # brief, no link
                                                      ['move_up_in_container_dom',''],            # up arrow
                                                      ['move_up_right_in_container_dom',''],      # up right
                                                      ['move_down_in_container_dom',''],          # down
                                                      ['move_down_right_in_container_dom',''],    # down right
                                                      ['edit_container_dom',''],                  # edit, html only
                                                      ['add_to_container_dom',''],                # insert/append, html only
                                                      ['remove_container_dom','']                 # remove
                                                   ]
    # for every row in the table
    dragrows = []
    droprows = []

    # for each row
    for row in range(0, rows-1):
        dragrows.append( [ False, ''] )
        droprows.append( [ False, ''] )

    page_data['editdom', 'domtable', 'dragrows']  = []
    page_data['editdom', 'domtable', 'droprows']  = []
    page_data['editdom', 'domtable', 'dropident']  = ''




def empty_container(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Sets call_data['part'] to container"

    editedproj = call_data['editedproj']

    # get data
    bits = utils.get_bits(call_data)

    widget = bits.widget
    container = bits.container

    if (widget is None) or (container is None):
        raise FailPage(message="Invalid container")

    if 'location' in call_data:
        del call_data['location']

    widget.set_container_part(container, '')

    utils.save(call_data, page=bits.page, section_name=bits.section_name, section=bits.section)

    call_data['status'] = "Item deleted"


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
        call_data['part'] = part                 ################ note, in future pass part_tuple rather than part
        raise GoTo(target = 54006, clear_submitted=True)
    if part_tuple.part_type == "Part":
        # edit the html part
        call_data['part'] = part                 ################ note, in future pass part_tuple rather than part
        raise GoTo(target = 53007, clear_submitted=True)
    if part_tuple.part_type == "ClosedPart":
        # edit the html closed part
        call_data['part'] = part                 ################ note, in future pass part_tuple rather than part
        raise GoTo(target = 53007, clear_submitted=True)
    if part_tuple.part_type == "HTMLSymbol":
        # edit the symbol
        call_data['part'] = part                 ################ note, in future pass part_tuple rather than part
        raise GoTo(target = 51107, clear_submitted=True)
    if part_tuple.part_type == "str":
        # edit the text
        call_data['part'] = part                 ################ note, in future pass part_tuple rather than part
        raise GoTo(target = 51017, clear_submitted=True)
    if part_tuple.part_type == "TextBlock":
        # edit the TextBlock
        call_data['part'] = part                 ################ note, in future pass part_tuple rather than part
        raise GoTo(target = 52017, clear_submitted=True)
    if part_tuple.part_type == "Comment":
        # edit the Comment
        call_data['part'] = part                 ################ note, in future pass part_tuple rather than part
        raise GoTo(target = 51207, clear_submitted=True)

    # note : a sectionplaceholder cannot appear in a container
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

    page_data[("adminhead","page_head","small_text")] = "Pick an item type"

    # navigator boxes
    boxes = [['back_to_container', "Container", True, '']]
    if 'extend_nav_buttons' in call_data:
        call_data['extend_nav_buttons'].extend(boxes)
    else:
        call_data['extend_nav_buttons'] = boxes

    # Fill in menu of items, Part items have insert, others have append
    # as this is to be input into a section, a further section is not present in this list


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
        raise GoTo(target = '23509', clear_submitted=True)



