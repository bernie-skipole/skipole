####### SKIPOLE WEB FRAMEWORK #######
#
# editresponder.py of skilift package  - functions for editing a responder
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


"""Functions for editing a responder"""

import inspect

from collections import namedtuple

from ..ski import skiboot, responders
from ..ski.page_class_definition import RespondPage
from ..ski.excepts import ServerError

from . import project_loaded, item_info, get_proj_page, del_location_in_page, insert_item_in_page

from .info_tuple import ResponderInfo



def _label_or_ident(ident):
    "Returns ident tuple or label"
    if isinstance(ident, skiboot.Ident):
        return ident.to_tuple()
    if ident is None:
        return ''
    return str(ident)


def list_responders():
    """Returns a list of lists, each inner list consisting of
       0) the responder class name
       1) the responder module name"""
    responderlist = []
    for name,responder in inspect.getmembers(responders, inspect.isclass):
        if issubclass(responder, responders.Respond):
            if name == 'Respond': continue
            responderlist.append([name, responder.module_name()])
    return responderlist


def responder_info(project, pagenumber, pchange):
    """Return a ResponderInfo named tuple"""
    proj, page = get_proj_page(project, pagenumber, pchange)
    if page.page_type != "RespondPage":
        raise ServerError(message = "Invalid page type")
    responder = page.responder

    if responder.widgfield_required and responder.widgfield:
        widgfield = responder.widgfield.to_str_tuple()
    else:
        widgfield = None

    if responder.alternate_ident_required and responder.alternate_ident:
        alternate_ident = responder.alternate_ident
    else:
        alternate_ident = None

    if responder.target_ident_required and responder.target_ident:
        target_ident = responder.target_ident
    else:
        target_ident = None

    if responder.allowed_callers_required and responder.allowed_callers:
        allowed_callers = [_label_or_ident(ident) for ident in responder.allowed_callers]
    else:
        allowed_callers = []

    if responder.validate_option_available:
        validate_option = responder.validate_option
    else:
        validate_option = False

    if responder.validate_option_available and responder.validate_fail_ident:
        validate_fail_ident = responder.validate_fail_ident
    else:
        validate_fail_ident = None

    # submit option

    if responder.submit_option_available:
        submit_option = responder.submit_option
    else:
        submit_option = False

    if responder.submit_required or submit_option:
        if responder.submit_list:
            submit_list = responder.submit_list[:]
        else:
            submit_list = []
        if responder.fail_ident:
            fail_ident = responder.fail_ident
        else:
            fail_ident = None
    else:
        submit_list = []
        fail_ident = None

    # fields

    field_options = responder.field_options.copy()
    field_values_list = []
    field_list = []
    single_field_value = []
    single_field = None

    if field_options['fields']:

        # field_values_list
        if field_options['field_values'] and ( not field_options['single_field'] ):
            field_vals = responder.fields
            for field, value in field_vals.items():
                if isinstance(field, skiboot.WidgField):
                    f = field.to_tuple()
                elif isinstance(field, skiboot.Ident):
                    f = str(field)
                else:
                    f = field
                if isinstance(value, skiboot.WidgField):
                    v = value.to_tuple()
                elif isinstance(value, skiboot.Ident):
                    v = str(value)
                else:
                    v = value
                field_values_list.append([f,v])

        # field_list
        if (not field_options['field_values']) and (not field_options['single_field']):
            field_vals = responder.fields
            for field in field_vals:
                if isinstance(field, skiboot.WidgField):
                    f = field.to_tuple()
                elif isinstance(field, skiboot.Ident):
                    f = str(field)
                else:
                    f = field
                field_list.append(f)

        if field_options['single_field']:

            # single_field_value - still to do
            # as there is currently no responder which takes a single field and value
            #????????????????????????????????????????????????????????

            # single_field
            if not field_options['field_values']:
                if not responder.responder_fields.keys():
                    single_field = ''
                else:
                    single_field = list(responder.responder_fields.keys())[0]

    return ResponderInfo(responder.__class__.__name__,
                         responder.module_name(),
                         responder.widgfield_required,
                         widgfield,
                         responder.alternate_ident_required,
                         _label_or_ident(alternate_ident),
                         responder.target_ident_required,
                         _label_or_ident(target_ident),
                         responder.allowed_callers_required,
                         allowed_callers,
                         responder.validate_option_available,
                         validate_option,
                         _label_or_ident(validate_fail_ident),
                         responder.submit_option_available,
                         submit_option,
                         responder.submit_required,
                         submit_list,
                         _label_or_ident(fail_ident),
                         field_options,
                         field_values_list,
                         field_list,
                         single_field_value,
                         single_field
                       )


def set_widgfield(project, pagenumber, pchange, widgfield):
    "sets responder widgfield, returns new pchange"
    proj, page = get_proj_page(project, pagenumber, pchange)
    if page.page_type != "RespondPage":
        raise ServerError(message = "Invalid page type")
    responder = page.responder
    if not responder.widgfield_required:
        raise ServerError(message="Invalid submission, this responder does not have a widgfield")
    responder.widgfield = skiboot.make_widgfield(widgfield)._replace(i='')
    # save the altered page, and return the page.change uuid
    return proj.save_page(page)


def set_alternate_ident(project, pagenumber, pchange, ident):
    "Sets the alternate page"
    proj, page = get_proj_page(project, pagenumber, pchange)
    if page.page_type != "RespondPage":
        raise ServerError(message = "Invalid page type")
    responder = page.responder
    if not responder.alternate_ident_required:
        raise ServerError(message="Invalid submission, this responder does not have an alternate page")
    a_i = skiboot.make_ident_or_label_or_url(ident, proj_ident=project)
    if a_i is None:
        raise ServerError(message="Invalid alternate ident")
    responder.alternate_ident = a_i
    # save the altered page, and return the page.change uuid
    return proj.save_page(page)



