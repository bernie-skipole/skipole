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


ResponderInfo = namedtuple('ResponderInfo', ['responder',
                                             'description_ref',
                                             'widgfield_required',
                                             'widgfield',
                                             'alternate_ident_required',
                                             'alternate_ident',
                                             'alternate_ident_description_ref',
                                             'target_ident_required',
                                             'target_ident',
                                             'target_ident_description_ref',
                                             'allowed_callers_required',
                                             'allowed_callers',
                                             'allowed_callers_description_ref',
                                             'validate_option_available',
                                             'validate_fail_ident',
                                             'validate_option_description_ref',
                                             'validate_fail_ident_description_ref',
                                             'submit_option_available',
                                             'submit_option',
                                             'submit_required',
                                             'submit_list',
                                             'fail_ident',
                                             'submit_option_description_ref',
                                             'submit_list_description_ref',
                                             'fail_ident_description_ref',
                                             'final_paragraph_description_ref',
                                             'field_options,',
                                             'fields_description_ref',
                                             'field_values_list',

])



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
       1) the textblock reference describing the responder"""
    responderlist = []
    for name,item in inspect.getmembers(responders, inspect.isclass):
        if issubclass(item, responders.Respond):
            if name == 'Respond': continue
            responderlist.append([name, item.description_ref()])
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
    if responder.alternate_ident_required and responder.description_ref('alternate_ident'):
        alternate_ident_description_ref = responder.description_ref('alternate_ident')
    else:
        alternate_ident_description_ref = None
    if responder.target_ident_required and responder.target_ident:
        target_ident = responder.target_ident
    else:
        target_ident = None
    if responder.target_ident_required and responder.description_ref('target_ident'):
        target_ident_description_ref = responder.description_ref('target_ident')
    else:
        target_ident_description_ref = None
    if responder.allowed_callers_required and responder.allowed_callers:
        allowed_callers = [_label_or_ident(ident) for ident in responder.allowed_callers]
    else:
        allowed_callers = []
    if responder.allowed_callers_required and responder.description_ref('allowed_callers'):
        allowed_callers_description_ref = responder.description_ref('allowed_callers')
    else:
        allowed_callers_description_ref = None
    if responder.validate_option_available and responder.validate_fail_ident:
        validate_fail_ident = responder.validate_fail_ident
    else:
        validate_fail_ident = None
    if responder.validate_option_available and responder.description_ref('validate_option'):
        validate_option_description_ref = responder.description_ref('validate_option')
    else:
        validate_option_description_ref = None
    if responder.validate_option_available and responder.description_ref('validate_fail_ident'):
        validate_fail_ident_description_ref = responder.description_ref('validate_fail_ident')
    else:
        validate_fail_ident_description_ref = None

    # submit option

    if responder.submit_option_available:
        submit_option_description_ref = responder.description_ref('submit_option')
        submit_option = responder.submit_option:
    else:
        submit_option_description_ref = None
        submit_option = False

    if responder.submit_required or responder.submit_option_available:
        submit_list_description_ref = responder.description_ref('submit_list')
        fail_ident_description_ref = responder.description_ref('fail_ident')
    else:
        submit_list_description_ref = None
        fail_ident_description_ref = None
    if responder.submit_required or submit_option:
        if responder.submit_list:
            submit_list = responder.submit_list
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
    field_values_list = []

    field_options = responder.field_options
    if not field_options['fields']:
        # no fields so no further data to input
        fields_description_ref = None

    else:
        fields_description_ref = responder.fields_description_ref()

        # field_values_list
        if field_options['field_values'] and ( not field_options['single_field'] ):
            # populate field_values_list
            field_vals = responder.fields
            for field, value in field_vals.items():
                if isinstance(field, skiboot.WidgField):
                    f1 = field.to_str_tuple()
                    f2 = str(field)
                else:
                    f1 = field
                    f2 = field
                if isinstance(value, skiboot.WidgField):
                    v = value.to_str_tuple()
                else:
                    v = value
                if not v:
                    v = "' '"
                row = [f1, v, f2]
                contents.append(row)
            if contents:
                contents.sort()
                page_data['field_values_list:contents'] = contents
            else:
                page_data['field_values_list:show'] = False










    return ResponderInfo(responder.__class__.__name__,
                         responder.description_ref(),
                         responder.widgfield_required,
                         widgfield,
                         responder.alternate_ident_required,
                         _label_or_ident(alternate_ident),
                         alternate_ident_description_ref,
                         responder.target_ident_required,
                         _label_or_ident(target_ident),
                         target_ident_description_ref,
                         responder.allowed_callers_required,
                         allowed_callers,
                         allowed_callers_description_ref,
                         responder.validate_option_available,
                         _label_or_ident(validate_fail_ident),
                         validate_option_description_ref,
                         validate_fail_ident_description_ref,
                         responder.submit_option_available,
                         submit_option,
                         responder.submit_required,
                         submit_list,
                         _label_or_ident(fail_ident),
                         submit_option_description_ref,
                         submit_list_description_ref,
                         fail_ident_description_ref,
                         responder.description_ref('final_paragraph'),
                         field_options,
                         fields_description_ref,
                         field_values_list

)


