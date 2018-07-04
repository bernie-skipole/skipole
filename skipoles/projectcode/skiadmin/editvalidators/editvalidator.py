####### SKIPOLE WEB FRAMEWORK #######
#
# editvalidator.py  - validator editing functions
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

"Functions implementing validator editing"

from ....ski import skiboot, tag, widgets, validators
from .. import utils
from ....ski.excepts import ServerError, FailPage, ValidateError, GoTo

from .... import skilift
from ....skilift import editwidget, editvalidator


def _field_name(widget, field_argument):
    "Returns a field name"
    if "set_names" not in widget:
        return field_argument
    name_dict = widget["set_names"]
    if field_argument in name_dict:
        return name_dict[field_argument]
    return field_argument


def retrieve_editvalidator(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Fills in the edit a validator page"
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

    if 'field_arg' in call_data:
        field_arg = call_data['field_arg']
    else:
        raise FailPage("Field not identified")

    if section_name:
        page_data[("validator_displaywidget_textblock","replace_strings")] = ['If the widget is in this section, the name should be of the form %s,widget_name.' % (section_name,)]
    else:
        page_data[("validator_displaywidget_textblock","replace_strings")] = ['If the widget is in a section, the name should be of the form section_alias,widget_name.']

    # get validator
    try:
        validx = int(call_data['validx'])
    except:
        raise FailPage("Unknown validator to edit")

    # get validator and widget info
    try:
        if section_name:
            widgetdescription = editwidget.section_widget_description(project, section_name, call_data['schange'], widget_name)
            widget =  editwidget.section_widget(project, section_name, call_data['schange'], widget_name)
            vinfo = editvalidator.section_field_validator_info(project, section_name, call_data['schange'], widget_name, field_arg, validx)
        else:
            widgetdescription = editwidget.page_widget_description(project, pagenumber, call_data['pchange'], widget_name)
            widget = editwidget.page_widget(project, pagenumber, call_data['pchange'], widget_name)
            vinfo = editvalidator.page_field_validator_info(project, pagenumber, call_data['pchange'], widget_name, field_arg, validx)
    except ServerError as e:
        raise FailPage(e.message)

    field_name = _field_name(widget, field_arg)

    call_data['extend_nav_buttons'].append(["back_to_field_edit", "Back to field", True, ''])

    page_data[("adminhead","page_head","large_text")] = "Edit : %s on field %s" % (vinfo.validator, field_name)

    page_data[('widget_type','para_text')] = "Widget type : %s.%s" % (widgetdescription.modulename, widgetdescription.classname)
    page_data[('widget_name','para_text')] = "Widget name : %s" % (widget_name,)
    page_data[('field_type','para_text')] = "Field type : %s" % (field_arg,)
    page_data[('field_name','para_text')] = "Field name : %s" % (field_name,)
    page_data[('validator_type','para_text')] = "Validator type : %s.%s" % (vinfo.module_name,vinfo.validator)

    page_data[('validator_textblock','textblock_ref')] = ".".join(("validators",vinfo.module_name,vinfo.validator))

    page_data[('e_message','input_text')] = vinfo.message
    page_data[('e_message_ref','input_text')] = vinfo.message_ref

    page_data[('displaywidget','input_text')] = vinfo.displaywidget

    # list of allowed values
    contents = []
    allowed_vals = vinfo.allowed_values
    for idx, val in enumerate(allowed_vals):
        row = [val, str(idx)]
        contents.append(row)
    if contents:
        page_data[('allowed_values','contents')] = contents
        page_data[('allowed_values','show')] = True
    else:
        page_data[('allowed_values','show')] = False

    # Validator arguments
    arg_contents = []
    val_args = vinfo.val_args
    for name, value in val_args.items():
        row = [name, str(value), name]
        arg_contents.append(row)
    if arg_contents:
        arg_contents.sort(key=lambda x: x[0])
        page_data[('validator_args','contents')] = arg_contents
        page_data[('validator_args','show')] = True
        page_data[('description5','show')] = True
    else:
        page_data[('validator_args','show')] = False
        page_data[('description5','show')] = False


def set_e_message(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Sets a validator error message"
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

    if 'field_arg' in call_data:
        field_arg = call_data['field_arg']
    else:
        raise FailPage("Field not identified")

    if 'e_message' not in call_data:
        raise FailPage("Error message not given")

    if call_data['e_message']:
        e_message = call_data['e_message']
    else:
        e_message = ''

    # get validator index
    try:
        validx = int(call_data['validx'])
    except:
        raise FailPage("Invalid validator")

    # set message
    try:
        if section_name:
            call_data['schange'] = editvalidator.set_section_field_validator_error_message(project, section_name, call_data['schange'], widget_name, field_arg, validx, e_message)
        else:
            call_data['pchange'] = editvalidator.set_page_field_validator_error_message(project, pagenumber, call_data['pchange'], widget_name, field_arg, validx, e_message)
    except ServerError as e:
        raise FailPage(e.message)
    call_data['status'] = "Validator error message changed"


def set_e_message_ref(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Sets a validator error message reference"
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

    if 'field_arg' in call_data:
        field_arg = call_data['field_arg']
    else:
        raise FailPage("Field not identified")

    if 'e_message_ref' not in call_data:
        raise FailPage("Error message reference not given")

    if call_data['e_message_ref']:
        e_message_ref = call_data['e_message_ref']
    else:
        e_message_ref = ''

    # get validator index
    try:
        validx = int(call_data['validx'])
    except:
        raise FailPage("Invalid validator")

    # set message reference
    try:
        if section_name:
            call_data['schange'] = editvalidator.set_section_field_validator_error_message_reference(project, section_name, call_data['schange'], widget_name, field_arg, validx, e_message_ref)
        else:
            call_data['pchange'] = editvalidator.set_page_field_validator_error_message_reference(project, pagenumber, call_data['pchange'], widget_name, field_arg, validx, e_message_ref)
    except ServerError as e:
        raise FailPage(e.message)
    call_data['status'] = "Validator error message reference changed"


def set_displaywidget(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Sets a validator displaywidget"
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

    if 'field_arg' in call_data:
        field_arg = call_data['field_arg']
    else:
        raise FailPage("Field not identified")

    if 'displaywidget' not in call_data:
        raise FailPage("Display widget not given")

    if call_data['displaywidget']:
        displaywidget = call_data['displaywidget']
    else:
        displaywidget = ''

    # get validator index
    try:
        validx = int(call_data['validx'])
    except:
        raise FailPage("Invalid validator")

    # set displaywidge
    try:
        if section_name:
            call_data['schange'] = editvalidator.set_section_field_validator_displaywidget(project, section_name, call_data['schange'], widget_name, field_arg, validx, displaywidget)
        else:
            call_data['pchange'] = editvalidator.set_page_field_validator_displaywidget(project, pagenumber, call_data['pchange'], widget_name, field_arg, validx, displaywidget)
    except ServerError as e:
        raise FailPage(e.message)
    call_data['status'] = "Validator display widget changed"


def set_allowed_value(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Adds a validator allowed value"
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

    if 'field_arg' in call_data:
        field_arg = call_data['field_arg']
    else:
        raise FailPage("Field not identified")

    # get validator index
    try:
        validx = int(call_data['validx'])
    except:
        raise FailPage("Invalid validator")

    if 'add_allowed' not in call_data:
        raise FailPage("Allowed value to be added not given")

    if call_data['add_allowed']:
        allowed_value = call_data['add_allowed']
    else:
        raise FailPage("A none-empty string is required")

    # add allowed_value
    try:
        if section_name:
            call_data['schange'] = editvalidator.add_section_field_validator_allowed_value(project, section_name, call_data['schange'], widget_name, field_arg, validx, allowed_value)
        else:
            call_data['pchange'] = editvalidator.add_page_field_validator_allowed_value(project, pagenumber, call_data['pchange'], widget_name, field_arg, validx, allowed_value)
    except ServerError as e:
        raise FailPage(e.message)
    call_data['status'] = "Validator allowed values changed"


def remove_allowed_value(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Removes a validator allowed value"
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

    if 'field_arg' in call_data:
        field_arg = call_data['field_arg']
    else:
        raise FailPage("Field not identified")

    # get validator index
    try:
        validx = int(call_data['validx'])
    except:
        raise FailPage("Invalid validator")

    if 'remove_allowed' not in call_data:
        raise FailPage("Allowed value to be removed not given")

    try:
        idx = int(call_data['remove_allowed'])
    except:
        raise FailPage("Invalid allowed value")

    # remove allowed_value
    try:
        if section_name:
            call_data['schange'] = editvalidator.remove_section_field_validator_allowed_value(project, section_name, call_data['schange'], widget_name, field_arg, validx, idx)
        else:
            call_data['pchange'] = editvalidator.remove_page_field_validator_allowed_value(project, pagenumber, call_data['pchange'], widget_name, field_arg, validx, idx)
    except ServerError as e:
        raise FailPage(e.message)
    call_data['status'] = "Validator allowed values changed"


def retrieve_arg(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Fills in the edit a validator argument page"

    editedproj = call_data['editedproj']

    bits = utils.get_bits(call_data)

    page = bits.page
    section = bits.section
    widget = bits.widget
    field_arg = bits.field_arg
    field = bits.field
    validator = bits.validator

    if (page is None) and (section is None):
        raise FailPage("Page/section not identified")

    if section is not None:
        page_data[("validator_displaywidget_textblock","replace_strings")] = ['If the widget is in this section, the name should be of the form %s,widget_name.' % (bits.section_name,)]
    else:
        page_data[("validator_displaywidget_textblock","replace_strings")] = ['If the widget is in a section, the name should be of the form section_alias,widget_name.']

    if widget is None:
        raise FailPage("Widget not identified")

    if field_arg is None:
        raise FailPage("Field not identified")

    if field is None:
        raise FailPage("Field not identified")

    if validator is None:
        raise FailPage("Validator not identified")

    call_data['extend_nav_buttons'].extend([["back_to_field_edit", "Back to field", True, ''],["back_to_validator", "Back to validator", True, '']])

    if 'arg_name' not in call_data:
        raise FailPage("Validator argument not identified")
    if call_data['arg_name'] not in validator.val_args:
        raise FailPage("Validator argument not identified")
    arg_name = call_data['arg_name']

    # navigator text
    page_data[("adminhead","page_head","large_text")] = arg_name

    page_data[('widget_type','para_text')] = "Widget type : %s.%s" % (widget.__class__.__module__.split('.')[-1], widget.__class__.__name__)
    page_data[('widget_name','para_text')] = "Widget name : %s" % (widget.name,)
    page_data[('field_type','para_text')] = "Field type : %s" % (field_arg,)
    page_data[('field_name','para_text')] = "Field name : %s" % (field.name,)
    page_data[('validator_type','para_text')] = "Validator type : %s" % (validator,)

    page_data[('validator_arg_textblock','textblock_ref')] = validator.description_ref(arg_name)

    page_data[('arg_val','input_text')] = validator[arg_name]
    page_data[('arg_val','hidden_field1')] = arg_name


def set_arg_value(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Sets a validator argument value"

    editedproj = call_data['editedproj']

    bits = utils.get_bits(call_data)

    page = bits.page
    section = bits.section
    validator = bits.validator

    if (page is None) and (section is None):
        raise FailPage("Page/section not identified")

    if validator is None:
        raise FailPage("Validator not identified")

    if 'arg_name' not in call_data:
        raise FailPage("argument name not given")
    if 'arg_value' not in call_data:
        raise FailPage("argument value not given")

    if call_data['arg_name'] not in validator.val_args:
        raise FailPage("Validator argument not identified")
    arg_name = call_data['arg_name']

    try:
        validator[arg_name] = call_data['arg_value']
    except ValidateError as e:
        raise FailPage(message = e.message, message_ref = e.message_ref)

    utils.save(call_data, page=page, section_name=bits.section_name, section=section)
    call_data['status'] = "Validator argument changed"


def move_up(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Moves a validator up in a field validator list"
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

    if 'field_arg' in call_data:
        field_arg = call_data['field_arg']
    else:
        raise FailPage("Field not identified")

    # get validator
    try:
        validx = int(call_data['validx'])
    except:
        raise FailPage("Invalid value to move")

    if validx == 0:
        raise FailPage("Invalid value to move")

    # move validator
    try:
        if section_name:
            call_data['schange'] = editvalidator.swap_section_field_validators(project, section_name, call_data['schange'], widget_name, field_arg, validx, validx-1)
        else:
            call_data['pchange'] = editvalidator.swap_page_field_validators(project, pagenumber, call_data['pchange'], widget_name, field_arg, validx, validx-1)
    except ServerError as e:
        raise FailPage(e.message)
    del call_data['validx']


def move_down(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Moves a validator down in a field validator list"
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

    if 'field_arg' in call_data:
        field_arg = call_data['field_arg']
    else:
        raise FailPage("Field not identified")

    # get validator
    try:
        validx = int(call_data['validx'])
    except:
        raise FailPage("Invalid value to move")

    # move validator
    try:
        if section_name:
            call_data['schange'] = editvalidator.swap_section_field_validators(project, section_name, call_data['schange'], widget_name, field_arg, validx, validx+1)
        else:
            call_data['pchange'] = editvalidator.swap_page_field_validators(project, pagenumber, call_data['pchange'], widget_name, field_arg, validx, validx+1)
    except ServerError as e:
        raise FailPage(e.message)
    del call_data['validx']


def remove_validator(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Removes a validator"
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

    if 'field_arg' in call_data:
        field_arg = call_data['field_arg']
    else:
        raise FailPage("Field not identified")

    # get validator
    try:
        validx = int(call_data['validx'])
    except:
        raise FailPage("Invalid value to remove")

    # remove validator
    try:
        if section_name:
            call_data['schange'] = editvalidator.remove_section_field_validator(project, section_name, call_data['schange'], widget_name, field_arg, validx)
        else:
            call_data['pchange'] = editvalidator.remove_page_field_validator(project, pagenumber, call_data['pchange'], widget_name, field_arg, validx)
    except ServerError as e:
        raise FailPage(e.message)

    del call_data['validx']
    call_data['status'] = "Validator removed"


def retrieve_validator_modules(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Creates a list of validator modules"
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

    if 'field_arg' in call_data:
        field_arg = call_data['field_arg']
    else:
        raise FailPage("Field not identified")

    # get a WidgetDescription named tuple, and a widget dictionary

    try:
        if section_name:
            widgetdescription = editwidget.section_widget_description(project, section_name, call_data['schange'], widget_name)
            widget =  editwidget.section_widget(project, section_name, call_data['schange'], widget_name)
        else:
            widgetdescription = editwidget.page_widget_description(project, pagenumber, call_data['pchange'], widget_name)
            widget = editwidget.page_widget(project, pagenumber, call_data['pchange'], widget_name)
    except ServerError as e:
        raise FailPage(e.message)

    field_name = _field_name(widget, field_arg)

    page_data[("adminhead","page_head","large_text")] = "Add validator to (\"%s\",\"%s\")" % (widget_name, field_name)

    page_data[('widget_type','para_text')] = "Widget type : %s.%s" % (widgetdescription.modulename, widgetdescription.classname)
    page_data[('widget_name','para_text')] = "Widget name : %s" % (widget_name,)
    page_data[('field_type','para_text')] = "Field type : %s" % (field_arg,)
    page_data[('field_name','para_text')] = "Field name : %s" % (field_name,)

    call_data['extend_nav_buttons'].append(["back_to_field_edit", "Back to field", True, ''])

    # table of validator modules

    # col 0 is the visible text to place in the link,
    # col 1 is the get field of the link
    # col 2 is the get field of the link
    # col 3 is the reference string of a textblock to appear in the column adjacent to the link
    # col 4 is text to appear if the reference cannot be found in the database
    # col 5 normally empty string, if set to text it will replace the textblock

    validator_modules = editvalidator.validator_modules()

    page_data[("modulestable","link_table")] = [ [name, name, '', ".".join(('validators', name, 'module')), 'Description not found', ''] for name in validator_modules ]


def retrieve_validator_list(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Creates a list of validators"
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

    if 'field_arg' in call_data:
        field_arg = call_data['field_arg']
    else:
        raise FailPage("Field not identified")

    # get a WidgetDescription named tuple, and a widget dictionary

    try:
        if section_name:
            widgetdescription = editwidget.section_widget_description(project, section_name, call_data['schange'], widget_name)
            widget =  editwidget.section_widget(project, section_name, call_data['schange'], widget_name)
        else:
            widgetdescription = editwidget.page_widget_description(project, pagenumber, call_data['pchange'], widget_name)
            widget = editwidget.page_widget(project, pagenumber, call_data['pchange'], widget_name)
    except ServerError as e:
        raise FailPage(e.message)

    field_name = _field_name(widget, field_arg)

    page_data[("adminhead","page_head","large_text")] = "Add validator to (\"%s\",\"%s\")" % (widget_name, field_name)

    page_data[('widget_type','para_text')] = "Widget type : %s.%s" % (widgetdescription.modulename, widgetdescription.classname)
    page_data[('widget_name','para_text')] = "Widget name : %s" % (widget_name,)
    page_data[('field_type','para_text')] = "Field type : %s" % (field_arg,)
    page_data[('field_name','para_text')] = "Field name : %s" % (field_name,)

    call_data['extend_nav_buttons'].extend([["back_to_field_edit", "Back to field", True, ''],["validator_modules", "Modules", True, '']])

    if 'valmodule' in call_data:
        module_name = call_data['valmodule']
    else:
        raise FailPage("Module not identified")

    validator_modules = editvalidator.validator_modules()

    if module_name not in validator_modules:
        raise FailPage("Module not identified")

    page_data[('moduledesc','textblock_ref')] = 'validators.' + module_name + '.module'

    # table of validators

    # col 0 is the visible text to place in the link,
    # col 1 is the get field of the link
    # col 2 is the get field of the link
    # col 3 is the reference string of a textblock to appear in the column adjacent to the link
    # col 4 is text to appear if the reference cannot be found in the database
    # col 5 normally empty string, if set to text it will replace the textblock

    # tuple of validators in the module
    validators = editvalidator.validators_in_module(module_name)
    page_data[("validators","link_table")] = [ [name, name, module_name, ".".join(("validators",module_name,name)), 'Description not found', ''] for name in validators ]


def create_validator(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Creates a validator and adds it to the field"
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

    if 'field_arg' in call_data:
        field_arg = call_data['field_arg']
    else:
        raise FailPage("Field not identified")
    if 'validator' not in call_data:
        raise FailPage("Validator not given")
    validator_name = call_data['validator']
    if not validator_name:
        raise FailPage("Validator not given")

    if 'valmodule' not in call_data:
        raise FailPage("Validator module not given")

    module_name = call_data['valmodule']

    try:
        if section_name:
            call_data['schange'] =  editvalidator.create_section_field_validator(project, section_name, call_data['schange'], widget_name, field_arg, module_name, validator_name)
            # get new list of validators attached to the field
            val_list = editvalidator.get_section_field_validator_list(project, section_name, call_data['schange'], widget_name, field_arg)
        else:
            call_data['pchange'] =  editvalidator.create_page_field_validator(project, pagenumber, call_data['pchange'], widget_name, field_arg, module_name, validator_name)
            val_list = editvalidator.get_page_field_validator_list(project, pagenumber, call_data['pchange'], widget_name, field_arg)
    except ServerError as e:
        raise FailPage(e.message)
 
    call_data['validx'] = str(len(val_list)-1)
    del call_data['validator']
    del call_data['valmodule']

    call_data['status'] = "Validator added"

