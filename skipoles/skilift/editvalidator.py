####### SKIPOLE WEB FRAMEWORK #######
#
# editvalidator.py of skilift package  - functions for editing a validator
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


"""Functions for editing a validator"""

import pkgutil, importlib, inspect


from ..ski import skiboot, widgets, validators
from ..ski.excepts import ServerError

from . import get_proj_page, get_proj_section

from .info_tuple import ValidatorInfo



def validator_modules():
    "Returns a tuple of validator modules"
    return tuple(name for (module_loader, name, ispkg) in pkgutil.iter_modules(validators.__path__))


def validators_in_module(module_name):
    "Returns a tuple of validator names in a module"
    module = importlib.import_module("skipoles.ski.validators." + module_name)
    return tuple(name for name,obj in inspect.getmembers(module, lambda member: inspect.isclass(member) and (member.__module__ == module.__name__)))


def get_section_field_validator_list(project, section_name, schange, widget_name, field_arg):
    "Returns list of validators attached to this widget field, each item in the list being a tuple of validator class name, module name)"
    proj, section = get_proj_section(project, section_name, schange)
    widget = section.widgets.get(widget_name)
    if (not isinstance(widget, widgets.Widget)) and (not isinstance(widget, widgets.ClosedWidget)):
        raise ServerError("Widget not found")
    return tuple( (v.__class__.__name__, v.module_name()) for v in widget.field_arg_val_list(field_arg) )


def get_page_field_validator_list(project, pagenumber, pchange, widget_name, field_arg):
    "Returns list of validators attached to this widget field, each item in the list being a tuple of validator class name, module name)"
    proj, page = get_proj_page(project, pagenumber, pchange)
    widget = page.widgets.get(widget_name)
    if (not isinstance(widget, widgets.Widget)) and (not isinstance(widget, widgets.ClosedWidget)):
        raise ServerError("Widget not found")
    return tuple( (v.__class__.__name__, v.module_name()) for v in widget.field_arg_val_list(field_arg) )


def page_field_validator_info(project, pagenumber, pchange, widget_name, field_arg, validx):
    "Returns a named tuple of info about a validator, validx is the index number of the validator within the validator list attached to the field"
    proj, page = get_proj_page(project, pagenumber, pchange)
    widget = page.widgets.get(widget_name)
    if (not isinstance(widget, widgets.Widget)) and (not isinstance(widget, widgets.ClosedWidget)):
        raise ServerError("Widget not found")
    if field_arg not in widget.fields:
        raise ServerError("Field not found")
    field = widget.fields[field_arg]
    if not field.valdt:
        raise ServerError("Field does not take validators")
    val_list = field.val_list
    # get validator
    if val_list and (validx >= 0) and (validx < len(val_list)):
        validator = val_list[validx]
    else:
        raise ServerError("Unknown validator")
    return ValidatorInfo(validator.__class__.__name__,
                         validator.module_name(),
                         validator.message,
                         validator.message_ref,
                         validator.displaywidget.to_str_tuple(),
                         validator.allowed_values,
                         validator.val_args
                        )


def section_field_validator_info(project, section_name, schange, widget_name, field_arg, validx):
    "Returns a named tuple of info about a validator, validx is the index number of the validator within the validator list attached to the field"
    proj, section = get_proj_section(project, section_name, schange)
    widget = section.widgets.get(widget_name)
    if (not isinstance(widget, widgets.Widget)) and (not isinstance(widget, widgets.ClosedWidget)):
        raise ServerError("Widget not found")
    if field_arg not in widget.fields:
        raise ServerError("Field not found")
    field = widget.fields[field_arg]
    if not field.valdt:
        raise ServerError("Field does not take validators")
    val_list = field.val_list
    # get validator
    if val_list and (validx >= 0) and (validx < len(val_list)):
        validator = val_list[validx]
    else:
        raise ServerError("Unknown validator")
    return ValidatorInfo(validator.__class__.__name__,
                         validator.module_name(),
                         validator.message,
                         validator.message_ref,
                         validator.displaywidget.to_str_tuple(),
                         validator.allowed_values,
                         validator.val_args
                        )
   

def create_section_field_validator(project, section_name, schange, widget_name, field_arg, validator_module, validator_name):
    "Add a validator to the field, return the new section change"
    proj, section = get_proj_section(project, section_name, schange)
    widget = section.widgets.get(widget_name)
    if (not isinstance(widget, widgets.Widget)) and (not isinstance(widget, widgets.ClosedWidget)):
        raise ServerError("Widget not found")
    if field_arg not in widget.fields:
        raise ServerError("Field not found")
    field = widget.fields[field_arg]
    if not field.valdt:
        raise ServerError("Field does not take validators")

    val_modules = validator_modules()
    if validator_module not in val_modules:
        raise ServerError("Validator module not found")
    module = importlib.import_module("skipoles.ski.validators." + validator_module)

    validator_dict = {name:cls for (name,cls) in inspect.getmembers(module, lambda member: inspect.isclass(member) and (member.__module__ == module.__name__))}

    if validator_name not in validator_dict:
        raise ServerError("Validator not identified")

    validator_cls = validator_dict[validator_name]
    validator_instance = validator_cls()
    field.add_validator(validator_instance)

    # save the altered section, and return the section.change uuid
    return proj.add_section(section_name, section)


def create_page_field_validator(project, pagenumber, pchange, widget_name, field_arg, validator_module, validator_name):
    "Add a validator to the field, return the new page change"
    proj, page = get_proj_page(project, pagenumber, pchange)
    widget = page.widgets.get(widget_name)
    if (not isinstance(widget, widgets.Widget)) and (not isinstance(widget, widgets.ClosedWidget)):
        raise ServerError("Widget not found")
    if field_arg not in widget.fields:
        raise ServerError("Field not found")
    field = widget.fields[field_arg]
    if not field.valdt:
        raise ServerError("Field does not take validators")

    val_modules = validator_modules()
    if validator_module not in val_modules:
        raise ServerError("Validator module not found")
    module = importlib.import_module("skipoles.ski.validators." + validator_module)

    validator_dict = {name:cls for (name,cls) in inspect.getmembers(module, lambda member: inspect.isclass(member) and (member.__module__ == module.__name__))}

    if validator_name not in validator_dict:
        raise ServerError("Validator not identified")

    validator_cls = validator_dict[validator_name]
    validator_instance = validator_cls()
    field.add_validator(validator_instance)

    # save the altered page, and return the page.change uuid
    return proj.save_page(page)


def remove_page_field_validator(project, pagenumber, pchange, widget_name, field_arg, validx):
    "Removes a validator, validx is the index number of the validator within the validator list attached to the field, return the new page change"
    proj, page = get_proj_page(project, pagenumber, pchange)
    widget = page.widgets.get(widget_name)
    if (not isinstance(widget, widgets.Widget)) and (not isinstance(widget, widgets.ClosedWidget)):
        raise ServerError("Widget not found")
    if field_arg not in widget.fields:
        raise ServerError("Field not found")
    field = widget.fields[field_arg]
    if not field.valdt:
        raise ServerError("Field does not take validators")
    val_list = field.val_list
    # get validator
    if val_list and (validx >= 0) and (validx < len(val_list)):
        del val_list[validx]
    else:
        raise ServerError("Unknown validator")
    # save the altered page, and return the page.change uuid
    return proj.save_page(page)


def remove_section_field_validator(project, section_name, schange, widget_name, field_arg, validx):
    "Removes a validator, validx is the index number of the validator within the validator list attached to the field, return the new section change"
    proj, section = get_proj_section(project, section_name, schange)
    widget = section.widgets.get(widget_name)
    if (not isinstance(widget, widgets.Widget)) and (not isinstance(widget, widgets.ClosedWidget)):
        raise ServerError("Widget not found")
    if field_arg not in widget.fields:
        raise ServerError("Field not found")
    field = widget.fields[field_arg]
    if not field.valdt:
        raise ServerError("Field does not take validators")
    val_list = field.val_list
    # get validator
    if val_list and (validx >= 0) and (validx < len(val_list)):
        del val_list[validx]
    else:
        raise ServerError("Unknown validator")
    # save the altered section, and return the section.change uuid
    return proj.add_section(section_name, section)


def swap_page_field_validators(project, pagenumber, pchange, widget_name, field_arg, validx1, validx2):
    "swaps validators at index positions validx1, validx2, which are positions within the validator list attached to the field, return the new page change"
    proj, page = get_proj_page(project, pagenumber, pchange)
    widget = page.widgets.get(widget_name)
    if (not isinstance(widget, widgets.Widget)) and (not isinstance(widget, widgets.ClosedWidget)):
        raise ServerError("Widget not found")
    if field_arg not in widget.fields:
        raise ServerError("Field not found")
    field = widget.fields[field_arg]
    if not field.valdt:
        raise ServerError("Field does not take validators")
    val_list = field.val_list
    # swap validators
    try:
        val_list[validx1], val_list[validx2] = val_list[validx2], val_list[validx1]
    except:
        raise ServerError("Invalid operation")
    # save the altered page, and return the page.change uuid
    return proj.save_page(page)


def swap_section_field_validators(project, section_name, schange, widget_name, field_arg, validx1, validx2):
    "swaps validators at index positions validx1, validx2, which are positions within the validator list attached to the field, return the new section change"
    proj, section = get_proj_section(project, section_name, schange)
    widget = section.widgets.get(widget_name)
    if (not isinstance(widget, widgets.Widget)) and (not isinstance(widget, widgets.ClosedWidget)):
        raise ServerError("Widget not found")
    if field_arg not in widget.fields:
        raise ServerError("Field not found")
    field = widget.fields[field_arg]
    if not field.valdt:
        raise ServerError("Field does not take validators")
    val_list = field.val_list
    # swap validators
    try:
        val_list[validx1], val_list[validx2] = val_list[validx2], val_list[validx1]
    except:
        raise ServerError("Invalid operation")
    # save the altered page, and return the page.change uuid
    return proj.save_page(page)





