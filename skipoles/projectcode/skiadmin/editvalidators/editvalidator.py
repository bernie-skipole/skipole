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

import pkgutil, re, importlib, inspect

from ....ski import skiboot, tag, widgets, validators
from .. import utils
from ....ski.excepts import FailPage, ValidateError, GoTo

# a search for anything none-alphanumeric and not an underscore
_AN = re.compile('[^\w]')

_VALIDATORS_TUPLE = tuple(name for (module_loader, name, ispkg) in pkgutil.iter_modules(validators.__path__))


def retrieve_editvalidator(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Fills in the edit a validator page"

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

    if validator is None:
        raise FailPage("Validator not identified")

    # navigator boxes
    utils.nav_boxes(call_data, page, section, bits.page_top, bits.parent_container, widget)
    call_data['extend_nav_buttons'].append(["back_to_field_edit", "Back to field", True, ''])

    page_data[("adminhead","page_head","large_text")] = "Edit : %s on field %s" % (validator, field.name)
    if 'status' in call_data:
        page_data[("adminhead","page_head","small_text")] = call_data['status']
    else:
        page_data[("adminhead","page_head","small_text")] = "Edit the validator"

    page_data[('widget_type','para_text')] = "Widget type : %s.%s" % (widget.__class__.__module__.split('.')[-1], widget.__class__.__name__)
    page_data[('widget_name','para_text')] = "Widget name : %s" % (widget.name,)
    page_data[('field_type','para_text')] = "Field type : %s" % (field_arg,)
    page_data[('field_name','para_text')] = "Field name : %s" % (field.name,)
    page_data[('validator_type','para_text')] = "Validator type : %s" % (validator,)

    page_data[('validator_textblock','textblock_ref')] = validator.description_ref()

    page_data[('e_message','input_text')] = validator.message
    page_data[('e_message_ref','input_text')] = validator.message_ref

    page_data[('displaywidget','input_text')] = validator.displaywidget.to_str_tuple()

    # list of allowed values
    contents = []
    allowed_vals = validator.allowed_values
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
    val_args = validator.val_args
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

    editedproj = call_data['editedproj']

    bits = utils.get_bits(call_data)

    page = bits.page
    section = bits.section
    validator = bits.validator

    if (page is None) and (section is None):
        raise FailPage("Page/section not identified")

    if validator is None:
        raise FailPage("Validator not identified")

    if 'e_message' not in call_data:
        raise FailPage("Error message not given")

    if call_data['e_message']:
        validator.message = call_data['e_message']
    else:
        validator.message = ''

    utils.save(call_data, page=page, section_name=bits.section_name, section=section)
    call_data['status'] = "Validator error message changed"


def set_e_message_ref(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Sets a validator error message reference"

    editedproj = call_data['editedproj']

    bits = utils.get_bits(call_data)

    page = bits.page
    section = bits.section
    validator = bits.validator

    if (page is None) and (section is None):
        raise FailPage("Page/section not identified")

    if validator is None:
        raise FailPage("Validator not identified")

    if 'e_message_ref' not in call_data:
        raise FailPage("Error message reference not given")

    if call_data['e_message_ref']:
        validator.message_ref = call_data['e_message_ref']
    else:
        validator.message_ref = ''

    utils.save(call_data, page=page, section_name=bits.section_name, section=section)
    call_data['status'] = "Validator error message reference changed"


def set_displaywidget(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Sets a validator displaywidget"

    editedproj = call_data['editedproj']

    bits = utils.get_bits(call_data)

    page = bits.page
    section = bits.section
    validator = bits.validator

    if (page is None) and (section is None):
        raise FailPage("Page/section not identified")

    if validator is None:
        raise FailPage("Validator not identified")

    if 'displaywidget' not in call_data:
        raise FailPage("Display widget not given")

    if call_data['displaywidget']:
        validator.displaywidget = call_data['displaywidget']
    else:
        validator.displaywidget = ''

    utils.save(call_data, page=page, section_name=bits.section_name, section=section)
    call_data['status'] = "Validator display widget changed"


def set_allowed_value(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Adds a validator allowed value"

    editedproj = call_data['editedproj']

    bits = utils.get_bits(call_data)

    page = bits.page
    section = bits.section
    validator = bits.validator

    if (page is None) and (section is None):
        raise FailPage("Page/section not identified")

    if validator is None:
        raise FailPage("Validator not identified")

    if 'add_allowed' not in call_data:
        raise FailPage("Allowed value to be added not given")

    if call_data['add_allowed']:
        if call_data['add_allowed'] in validator.allowed_values:
            call_data['status'] = "Allowed value already exists"
            return
        # perhaps further checking needed here since allowed value strings appear in javascript
        lowval = call_data['add_allowed'].lower()
        if lowval == "</script>":
            raise FailPage("Invalid allowed value : strings of this form may confuse javascript")
        if "\"" in lowval:
            raise FailPage("Invalid allowed value : strings of this form may confuse javascript")
        validator.allowed_values.append(call_data['add_allowed'])
    else:
        call_data['status'] = "No value specified"
        return

    utils.save(call_data, page=page, section_name=bits.section_name, section=section)
    call_data['status'] = "Validator allowed values changed"


def remove_allowed_value(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Removes a validator allowed value"

    editedproj = call_data['editedproj']

    bits = utils.get_bits(call_data)

    page = bits.page
    section = bits.section
    validator = bits.validator

    if (page is None) and (section is None):
        raise FailPage("Page/section not identified")

    if validator is None:
        raise FailPage("Validator not identified")

    if 'remove_allowed' not in call_data:
        raise FailPage("Allowed value to be removed not given")

    try:
        idx = int(call_data['remove_allowed'])
    except:
        raise FailPage("Invalid allowed value")

    value_list = validator.allowed_values
    if not validator.allowed_values:
        raise FailPage("Allowed value list is empty")

    if (idx >= 0) and (idx < len(validator.allowed_values)):
        del validator.allowed_values[idx]
    else:
        raise FailPage("Invalid value to remove")

    utils.save(call_data, page=page, section_name=bits.section_name, section=section)
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

    # navigator boxes
    utils.nav_boxes(call_data, page, section, bits.page_top, bits.parent_container, widget)
    call_data['extend_nav_buttons'].extend([["back_to_field_edit", "Back to field", True, ''],["back_to_validator", "Back to validator", True, '']])

    if 'arg_name' not in call_data:
        raise FailPage("Validator argument not identified")
    if call_data['arg_name'] not in validator.val_args:
        raise FailPage("Validator argument not identified")
    arg_name = call_data['arg_name']

    # navigator text
    page_data[("adminhead","page_head","large_text")] = arg_name
    page_data[("adminhead","page_head","small_text")] = "Edit the validator argument"

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

    editedproj = call_data['editedproj']

    bits = utils.get_bits(call_data)

    page = bits.page
    section = bits.section
    field = bits.field
    validator = bits.validator

    if (page is None) and (section is None):
        raise FailPage("Page/section not identified")

    if field is None:
        raise FailPage("Field not identified")

    if validator is None:
        raise FailPage("Validator not identified")

    validx = int(call_data['validx'])
    del call_data['validx']

    val_list = field.val_list

    # Moving up
    if (validx >= 1) and (validx < len(val_list)):
        val_list.insert(validx-1, val_list.pop(validx))
    else:
        raise FailPage("Invalid value to move up")

    utils.save(call_data, page=page, section_name=bits.section_name, section=section)
    call_data['status'] = "Validator moved"


def move_down(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Moves a validator down in a field validator list"

    editedproj = call_data['editedproj']

    bits = utils.get_bits(call_data)

    page = bits.page
    section = bits.section
    field = bits.field
    validator = bits.validator

    if (page is None) and (section is None):
        raise FailPage("Page/section not identified")

    if field is None:
        raise FailPage("Field not identified")

    if validator is None:
        raise FailPage("Validator not identified")

    validx = int(call_data['validx'])
    del call_data['validx']

    val_list = field.val_list

    # Moving down
    if (validx >= 0) and (validx < len(val_list)-1):
        val_list.insert(validx+1, val_list.pop(validx))
    else:
        raise FailPage("Invalid value to move down")

    utils.save(call_data, page=page, section_name=bits.section_name, section=section)
    call_data['status'] = "Validator moved"


def remove_validator(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Removes a validator"

    editedproj = call_data['editedproj']

    bits = utils.get_bits(call_data)

    page = bits.page
    section = bits.section
    field = bits.field
    validator = bits.validator

    if (page is None) and (section is None):
        raise FailPage("Page/section not identified")

    if field is None:
        raise FailPage("Field not identified")

    if validator is None:
        raise FailPage("Validator not identified")

    validx = int(call_data['validx'])
    del call_data['validx']

    val_list = field.val_list

    # removing the validator
    if (validx >= 0) and (validx < len(val_list)):
        del val_list[validx]
    else:
        raise FailPage("Invalid value to remove")

    utils.save(call_data, page=page, section_name=bits.section_name, section=section)
    call_data['status'] = "Validator removed"


def retrieve_validator_modules(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Creates a list of validator modules"

    editedproj = call_data['editedproj']

    bits = utils.get_bits(call_data)

    page = bits.page
    section = bits.section
    widget = bits.widget
    field_arg = bits.field_arg
    field = bits.field

    if (page is None) and (section is None):
        raise FailPage("Page/section not identified")

    if widget is None:
        raise FailPage("Widget not identified")

    if field_arg is None:
        raise FailPage("Field not identified")

    # navigator boxes
    utils.nav_boxes(call_data, page, section, bits.page_top, bits.parent_container, bits.widget)
    call_data['extend_nav_buttons'].append(["back_to_field_edit", "Back to field", True, ''])

    page_data[("adminhead","page_head","large_text")] = "Add validator to (\"%s\",\"%s\")" % (widget.name, field.name)
    if 'status' in call_data:
        page_data[("adminhead","page_head","small_text")] = call_data['status']
    else:
        page_data[("adminhead","page_head","small_text")] = "Choose validator module"

    page_data[('widget_type','para_text')] = "Widget type : %s.%s" % (widget.__class__.__module__.split('.')[-1], widget.__class__.__name__)
    page_data[('widget_name','para_text')] = "Widget name : %s" % (widget.name,)
    page_data[('field_type','para_text')] = "Field type : %s" % (field_arg,)
    page_data[('field_name','para_text')] = "Field name : %s" % (field.name,)


    # table of validator modules

    # col 0 is the visible text to place in the link,
    # col 1 is the get field of the link
    # col 2 is the get field of the link
    # col 3 is the reference string of a textblock to appear in the column adjacent to the link
    # col 4 is text to appear if the reference cannot be found in the database
    # col 5 normally empty string, if set to text it will replace the textblock

    contents = []

    for name in _VALIDATORS_TUPLE:
        ref = 'validators.' + name + '.module'
        contents.append([name, name, '', ref, 'Description not found', ''])

    page_data[("modulestable","link_table")] = contents



def retrieve_validator_list(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Creates a list of validators"

    editedproj = call_data['editedproj']

    bits = utils.get_bits(call_data)

    page = bits.page
    section = bits.section
    widget = bits.widget
    field_arg = bits.field_arg
    field = bits.field

    if (page is None) and (section is None):
        raise FailPage("Page/section not identified")

    if widget is None:
        raise FailPage("Widget not identified")

    if field_arg is None:
        raise FailPage("Field not identified")

    # navigator boxes
    utils.nav_boxes(call_data, page, section, bits.page_top, bits.parent_container, bits.widget)
    call_data['extend_nav_buttons'].extend([["back_to_field_edit", "Back to field", True, ''],["validator_modules", "Modules", True, '']])

    page_data[("adminhead","page_head","large_text")] = "Add validator to (\"%s\",\"%s\")" % (widget.name, field.name)

    page_data[('widget_type','para_text')] = "Widget type : %s.%s" % (widget.__class__.__module__.split('.')[-1], widget.__class__.__name__)
    page_data[('widget_name','para_text')] = "Widget name : %s" % (widget.name,)
    page_data[('field_type','para_text')] = "Field type : %s" % (field_arg,)
    page_data[('field_name','para_text')] = "Field name : %s" % (field.name,)


    if 'valmodule' in call_data:
        module_name = call_data['valmodule']
    else:
        raise FailPage("Module not identified")

    if 'status' in call_data:
        page_data[("adminhead","page_head","small_text")] = call_data['status']
    else:
        page_data[("adminhead","page_head","small_text")] = "Validators in module %s" % (module_name,)


    if module_name not in _VALIDATORS_TUPLE:
        raise FailPage("Module not identified")

    page_data[('moduledesc','textblock_ref')] = 'validators.' + module_name + '.module'


    # table of validators

    # col 0 is the visible text to place in the link,
    # col 1 is the get field of the link
    # col 2 is the get field of the link
    # col 3 is the reference string of a textblock to appear in the column adjacent to the link
    # col 4 is text to appear if the reference cannot be found in the database
    # col 5 normally empty string, if set to text it will replace the textblock

    module = importlib.import_module("skipoles.ski.validators." + module_name)

    # set module into table
    # call_data['module'] = module_name

    contents = []

    for name,obj in inspect.getmembers(module, lambda member: inspect.isclass(member) and (member.__module__ == module.__name__)):
        contents.append([name, name, module_name, obj.description_ref(), 'Description not found', ''])

    page_data[("validators","link_table")] = contents


def create_validator(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Creates a validator and adds it to the field"

    editedproj = call_data['editedproj']

    bits = utils.get_bits(call_data)

    page = bits.page
    section = bits.section
    widget = bits.widget
    field = bits.field

    if (page is None) and (section is None):
        raise FailPage("Page/section not identified")

    if field is None:
        raise FailPage("Field not identified")
    if not field.valdt:
        raise FailPage("Field does not take validators")

    if 'validator' not in call_data:
        raise FailPage("Validator not given")
    validator_name = call_data['validator']
    if not validator_name:
        raise FailPage("Validator not given")

    if 'valmodule' not in call_data:
        raise FailPage("Validator module not given")

    module_name = call_data['valmodule']

    if module_name not in _VALIDATORS_TUPLE:
        raise FailPage("Validator module not recognised")

    module = importlib.import_module("skipoles.ski.validators." + module_name)

    validator_dict = {name:cls for (name,cls) in inspect.getmembers(module, lambda member: inspect.isclass(member) and (member.__module__ == module.__name__))}

    if validator_name not in validator_dict:
        raise FailPage("Validator not identified")

    validator_cls = validator_dict[validator_name]
    validator_instance = validator_cls()
    field.add_validator(validator_instance)

    utils.save(call_data, page=page, section_name=bits.section_name, section=section)

    call_data['validx'] = str(len(field.val_list)-1)
    del call_data['validator']
    del call_data['valmodule']

    call_data['status'] = "Validator added"

