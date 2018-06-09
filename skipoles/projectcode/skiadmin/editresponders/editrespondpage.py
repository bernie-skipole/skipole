####### SKIPOLE WEB FRAMEWORK #######
#
# editrespondpage.py  - respond page editing functions
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

"Functions implementing respond page editing"

import collections

from ....ski import skiboot
from ....ski.excepts import ValidateError, FailPage, ServerError, GoTo

from .. import utils


def _ident_to_str(ident):
    "Returns string ident or label"
    if isinstance(ident, skiboot.Ident):
        return ident.to_comma_str()
    if ident is None:
        return ''
    return str(ident)


def retrieve_edit_respondpage(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Retrieves widget data for the edit respond page"

    if 'page_number' in call_data:
        pagenumber = call_data['page_number']
        str_pagenumber = str(pagenumber)
    else:
        raise FailPage(message = "page missing")

    project = call_data['editedprojname']
    pageinfo = skilift.page_info(project, pagenumber)

    if pageinfo.item_type != 'RespondPage':
        raise FailPage(message = "Invalid page")

    # fills in the data for editing page name, brief, parent, etc., 
    page_data[("adminhead","page_head","large_text")] = pageinfo.name
    page_data[('page_edit','p_ident','page_ident')] = (project,str_pagenumber)
    page_data[('page_edit','p_name','page_ident')] = (project,str_pagenumber)
    page_data[('page_edit','p_description','page_ident')] = (project,str_pagenumber)
    page_data[('page_edit','p_rename','input_text')] = pageinfo.name
    page_data[('page_edit','p_parent','input_text')] = "%s,%s" % (project, pageinfo.parentfolder_number)
    page_data[('page_edit','p_brief','input_text')] = pageinfo.brief

    # get a copy of the page object
    proj, page = skilift.get_proj_page(project, pagenumber, call_data['pchange'])

    page_data['respondertype:para_text'] = "This page is a responder of type: %s." % (page.responder.__class__.__name__,)
    page_data['responderdescription:textblock_ref'] = page.responder.description_ref()

    if page.responder.widgfield_required:
        if page.responder.widgfield:
            page_data['widgfield:input_text'] = page.responder.widgfield.to_str_tuple()
    else:
        page_data['widgfield:show'] = False

    if page.responder.alternate_ident_required:
        page_data['alternate','input_text'] = _ident_to_str(page.responder.alternate_ident)
        page_data['alternate_ident_description','textblock_ref'] = page.responder.description_ref('alternate_ident')
    else:
        page_data['alternate','show'] = False
        page_data['alternate_ident_description','show'] = False

    if page.responder.target_ident_required:
        page_data['target:input_text'] = _ident_to_str(page.responder.target_ident)
        page_data['target_ident_description','textblock_ref'] = page.responder.description_ref('target_ident')
    else:
        page_data['target:show'] = False
        page_data['target_ident_description','show'] = False

    if page.responder.allowed_callers_required:
        page_data['allowed_callers_description:textblock_ref'] = page.responder.description_ref('allowed_callers')
        if page.responder.allowed_callers:
            contents = []
            for ident in page.responder.allowed_callers:
                ident_row = [_ident_to_str(ident), str(ident)]
                contents.append(ident_row)
            page_data['allowed_callers_list:contents'] = contents
        else:
            page_data['allowed_callers_list:show'] = False
        page_data['add_allowed_caller:input_text'] = ''
    else:
        page_data['allowed_callers_description:show'] = False
        page_data['allowed_callers_list:show'] = False
        page_data['add_allowed_caller:show'] = False

    # validate option
    if page.responder.validate_option_available:
        page_data[('val_option_desc', 'textblock_ref')] =  page.responder.description_ref('validate_option')
        if page.responder.validate_option:
            page_data['set_val_option','button_text'] = "Disable Validation"
            page_data['val_status','para_text'] = "Validate received field values : Enabled"
            page_data['validate_fail', 'input_text'] = _ident_to_str(page.responder.validate_fail_ident)
            page_data['validate_fail', 'hide'] = False
        else:
            page_data['set_val_option','button_text'] = "Enable Validation"
            page_data['val_status','para_text'] = "Validate received field values : Disabled"
            page_data['validate_fail', 'hide'] = True
    else:
        page_data['val_option_desc','show'] = False
        page_data['set_val_option','show'] = False
        page_data['val_status','show'] = False
        page_data['validate_fail', 'show'] = False

    
    # submit option

    if page.responder.submit_option_available:
        page_data['submit_option_desc','textblock_ref'] = page.responder.description_ref('submit_option')
        if page.responder.submit_option:
            page_data['set_submit_option','button_text'] = 'Disable submit_data'
            page_data['submit_status','para_text'] = "Call submit_data : Enabled"
        else:
            page_data['set_submit_option','button_text'] = 'Enable submit_data'
            page_data['submit_status','para_text'] = "Call submit_data : Disabled"
    else:
        page_data['submit_option_desc','show'] = False
        page_data['set_submit_option','show'] = False
        page_data['submit_status','show'] = False

    if page.responder.submit_required or page.responder.submit_option:
        page_data['submit_list_description:textblock_ref'] = page.responder.description_ref('submit_list')
        if page.responder.submit_list:
            contents = []
            for index, s in enumerate(page.responder.submit_list):
                s_row = [s, str(index)]
                contents.append(s_row)
            page_data['submit_list','contents'] = contents
        else:
            page_data['submit_list','show'] = False
        page_data['submit_string','input_text'] = ''
        page_data['fail_page_ident:input_text'] = _ident_to_str(page.responder.fail_ident)
    else:
        page_data['submit_list_description','show'] = False
        page_data['submit_list','show'] = False
        page_data['submit_string','show'] = False
        page_data['fail_page_ident','show'] = False

    # final paragraph
    page_data['final_paragraph:textblock_ref'] = page.responder.description_ref('final_paragraph')

    # field options
    f_options = page.responder.field_options
    if not f_options['fields']:
        # no fields so no further data to input
        return page_data

    # show the fields description
    page_data['fields_description:show'] = True
    page_data['fields_description:textblock_ref'] = page.responder.fields_description_ref()


    if f_options['field_values'] and ( not f_options['single_field'] ):
        page_data['field_values_list:show'] = True
        page_data['add_field_value:show'] = True
        page_data['add_field_value_para:show'] = True
        # populate field_values_list
        contents = []
        field_vals = page.responder.fields
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
        # populate add_field_value
        if f_options['widgfields']:
            if f_options['widgfield_values']:
                 page_data['add_field_value_para:para_text'] = "Add widgfields in both the field area and in the value area"
            else:
                page_data['add_field_value_para:para_text'] = "Add widgfield and value"
        else:
            page_data['add_field_value_para:para_text'] = "Add items"
            page_data['add_field_value','label'] = "Items:"
        if f_options['empty_values_allowed']:
           page_data['add_field_value_para:para_text'] += ", empty values are allowed:"
        else:
           page_data['add_field_value_para:para_text'] += ", empty values are not allowed:"
        return
       

    if (not f_options['field_values']) and (not f_options['single_field']):
        page_data['field_list','show'] = True
        page_data['add_field','show'] = True
        # populate field_list
        contents = []
        field_vals = page.responder.fields
        for field in field_vals:
            if isinstance(field, skiboot.WidgField):
                f1 = field.to_str_tuple()
                f2 = str(field)
            else:
                f1 = field
                f2 = field
            row = [f1, f2]
            contents.append(row)
        if contents:
            contents.sort()
            page_data['field_list','contents'] = contents
        else:
            page_data['field_list','show'] = False
        # populate add_field
        if f_options['widgfields']:
             page_data['add_field','label'] = "Add a widgfield:"
        else:
            page_data['add_field,','label'] = "Add a string:"

    if not f_options['single_field']:
        return

    # all remaining are if a single field is required

    if not f_options['field_values']:
        # a single value is a submit text input field
        page_data[('single_field','show')] = True
        if not page.responder.responder_fields.keys():
            page_data[('single_field','input_text')] = ''
        else:
            page_data[('single_field','input_text')] = list(page.responder.responder_fields.keys())[0]
        return


    # remaining is for a single field and value - still to do
    # as there is currently no responder which takes a single field and value
    #????????????????????????????????????????????????????????



def submit_widgfield(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Sets widgfield"
    if 'page' not in call_data:
        raise FailPage(message = "page missing")
    page = call_data['page']
    if page.page_type != 'RespondPage':
        raise ValidateError("Invalid page type")

    if not 'widget' in call_data:
        raise FailPage(message="No widgfield given", widget="widgfield_error")
    if not call_data['widget']:
        raise FailPage(message="No widgfield given", widget="widgfield_error")
    # Set the page widgfield
    responder = page.responder
    if not responder.widgfield_required:
        raise FailPage(message="Invalid submission, this responder does not have a widgfield")
    responder.widgfield = skiboot.make_widgfield(call_data['widget'])._replace(i='')
    utils.save(call_data, page=page, widget_name='widgfield_error')
    call_data['status'] = 'WidgField set'


def submit_alternate_ident(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Sets the alternate page"
    editedproj = call_data['editedproj']
    if 'page' not in call_data:
        raise FailPage(message = "page missing")
    page = call_data['page']
    if page.page_type != 'RespondPage':
        raise ValidateError("Invalid page type")

    if not 'alternate_ident' in call_data:
        raise FailPage(message="No alternate page label given", widget="alternate")
    # Set the page alternate_ident
    responder = page.responder
    if not responder.alternate_ident_required:
        raise FailPage(message="Invalid submission, this responder does not have a alternate page")
    a_i = skiboot.make_ident_or_label_or_url(call_data['alternate_ident'], proj_ident=editedproj.proj_ident)
    if a_i is None:
        raise FailPage(message="Invalid alternate ident", widget="alternate")
    responder.alternate_ident = a_i
    utils.save(call_data, page=page, widget_name='alternate')
    page_data['alternate','set_input_accepted'] = True
    call_data['status'] = 'Page set'



def submit_target_ident(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Sets the target ident"
    editedproj = call_data['editedproj']
    if 'page' not in call_data:
        raise FailPage(message = "page missing")
    page = call_data['page']
    if page.page_type != 'RespondPage':
        raise ValidateError("Invalid page type")

    if not 'target_ident' in call_data:
        raise FailPage(message="No target ident given", widget="target")
    # Set the page target_ident
    responder = page.responder
    if not responder.target_ident_required:
        raise FailPage(message="Invalid submission, this responder does not have a target ident")
    t_i = skiboot.make_ident_or_label_or_url(call_data['target_ident'], proj_ident=editedproj.proj_ident)
    if t_i is None:
        raise FailPage(message="Invalid target ident", widget="target")
    responder.target_ident = t_i
    utils.save(call_data, page=page, widget_name='target')
    page_data['target','set_input_accepted'] = True
    call_data['status'] = 'Target Ident set'


def submit_validate_fail_ident(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Sets the validate fail ident"
    editedproj = call_data['editedproj']
    if 'page' not in call_data:
        raise FailPage(message = "page missing")
    page = call_data['page']
    if page.page_type != 'RespondPage':
        raise ValidateError("Invalid page type")

    if not 'validate_fail_ident' in call_data:
        raise FailPage(message="No validate fail ident given", widget="validate_fail")
    # Set the page validate_fail_ident
    responder = page.responder
    if not responder.validate_option_available:
        raise FailPage(message="Invalid submission, this responder does not have a validate option")
    v_f_i = skiboot.make_ident_or_label_or_url(call_data['validate_fail_ident'], proj_ident=editedproj.proj_ident)
    if v_f_i is None:
        raise FailPage(message="Invalid validate fail ident", widget="validate_fail")
    responder.validate_fail_ident = v_f_i
    utils.save(call_data, page=page, widget_name='validate_fail')
    page_data['validate_fail','set_input_accepted'] = True
    call_data['status'] = 'Validate Fail Ident set'


def submit_fail_ident(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Sets the fail ident"
    editedproj = call_data['editedproj']
    if 'page' not in call_data:
        raise FailPage(message = "page missing")
    page = call_data['page']
    if page.page_type != 'RespondPage':
        raise ValidateError("Invalid page type")

    if not 'fail_ident' in call_data:
        raise FailPage(message="No fail ident given", widget="fail_ident_error")
    # Set the page fail_ident
    responder = page.responder
    if not (responder.submit_required or responder.submit_option_available):
        raise FailPage(message="Invalid submission, this responder does not have a fail ident")
    f_i = skiboot.make_ident_or_label_or_url(call_data['fail_ident'], proj_ident=editedproj.proj_ident)
    if f_i is None:
        raise FailPage(message="Invalid fail ident", widget="fail_ident_error")
    responder.fail_ident = f_i
    utils.save(call_data, page=page, widget_name='fail_ident_error')
    call_data['status'] = 'Fail Ident set'


def add_allowed_caller(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Adds a new allowed caller"
    editedproj = call_data['editedproj']
    if 'page' not in call_data:
        raise FailPage(message = "page missing")
    page = call_data['page']
    if page.page_type != 'RespondPage':
        raise ValidateError("Invalid page type")

    if not 'allowed_caller' in call_data:
        raise FailPage(message="No allowed caller given", widget="allowed_callers_error")
    # Set the page allowed caller
    responder = page.responder
    if not responder.allowed_callers_required:
        raise FailPage(message="Invalid submission, this responder does not have allowed callers")
    a_c = skiboot.make_ident_or_label(call_data['allowed_caller'], proj_ident=editedproj.proj_ident)
    if a_c is None:
        raise FailPage(message="Invalid allowed caller", widget="allowed_callers_error")
    # check not already in list
    allowed_callers = [str(ident) for ident in responder.allowed_callers ]
    s_a_c = str(a_c)
    if s_a_c in allowed_callers:
        return {("adminhead","page_head","small_text"):'This allowed caller already exists'}
    responder.allowed_callers.append(a_c)
    utils.save(call_data, page=page, widget_name='allowed_callers_error')


def delete_allowed_caller(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Deletes an allowed caller"
    editedproj = call_data['editedproj']
    if 'page' not in call_data:
        raise FailPage(message = "page missing")
    page = call_data['page']
    if page.page_type != 'RespondPage':
        raise ValidateError("Invalid page type")

    if not 'delete_allowed_caller' in call_data:
        raise FailPage(message="No allowed caller given", widget="allowed_callers_error")
    # Delete the page allowed caller
    responder = page.responder
    if not responder.allowed_callers_required:
        raise FailPage(message="Invalid submission, this responder does not have allowed callers")
    allowed_callers = [str(ident) for ident in responder.allowed_callers ]
    try:
        idx = allowed_callers.index(call_data['delete_allowed_caller'])
    except ValueError:
        return {("adminhead","page_head","small_text"):'This allowed caller does not exist'}
    del responder.allowed_callers[idx]
    utils.save(call_data, page=page, widget_name='allowed_callers_error')


def remove_field(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Deletes a field"
    if 'page' not in call_data:
        raise FailPage(message = "page missing")
    page = call_data['page']
    if page.page_type != 'RespondPage':
        raise ValidateError("Invalid page type")

    if not 'remove_field' in call_data:
        raise FailPage(message="No field to remove given", widget="fields_error")
    # Delete the page field
    responder = page.responder
    # field options
    f_options = responder.field_options
    if not f_options['fields']:
        raise FailPage(message="Invalid submission, this responder does not have fields")
    remove_field = call_data['remove_field']
    if f_options['widgfields']:
        # ensure the field to remove is a widgfield
        remove_field = skiboot.make_widgfield(remove_field)
    if remove_field in responder.fields:
        del responder.fields[remove_field]
    else:
        raise FailPage(message="Field not found", widget="fields_error")
    utils.save(call_data, page=page, widget_name='fields_error')


def add_field_value(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Adds a field and value"
    if 'page' not in call_data:
        raise FailPage(message = "page missing")
    page = call_data['page']
    if page.page_type != 'RespondPage':
        raise ValidateError("Invalid page type")

    if not 'field' in call_data:
        raise FailPage(message="No field given", widget="fields_error")
    if not call_data['field']:
        raise FailPage(message="No field given", widget="fields_error")
    if not 'value' in call_data:
        raise FailPage(message="No value given", widget="fields_error")
    responder = page.responder
    # field options
    f_options = responder.field_options
    if not f_options['fields']:
        raise FailPage(message="Invalid submission, this responder does not have fields", widget="fields_error")
    if not f_options['field_values']:
        raise FailPage(message="Invalid submission, this responder does not have values", widget="fields_error")
    if (not call_data['value']) and (not f_options['empty_values_allowed']):
        page_data['add_field_value', 'input_text1'] = call_data['field']
        page_data['add_field_value', 'set_input_accepted1'] = True
        page_data['add_field_value', 'set_input_errored2'] = True
        raise FailPage(message="Invalid submission, empty field values are not allowed", widget="fields_error")
    responder.set_field(call_data['field'], call_data['value'])
    utils.save(call_data, page=page, widget_name='fields_error')


def add_field(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Adds a field"
    if 'page' not in call_data:
        raise FailPage(message = "page missing")
    page = call_data['page']
    if page.page_type != 'RespondPage':
        raise ValidateError("Invalid page type")

    if not 'field' in call_data:
        raise FailPage(message="No field given", widget="fields_error")
    if not call_data['field']:
        raise FailPage(message="No field given", widget="fields_error")
    responder = page.responder
    # field options
    f_options = responder.field_options
    if not f_options['fields']:
        raise FailPage(message="Invalid submission, this responder does not have fields", widget="fields_error")
    if f_options['field_values']:
        raise FailPage(message="Invalid submission, this responder requires field values", widget="fields_error")
    responder.set_field(call_data['field'], '')
    utils.save(call_data, page=page, widget_name='fields_error')



def set_single_field(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Sets a field dictionary"
    if 'page' not in call_data:
        raise FailPage(message = "page missing")
    page = call_data['page']
    if page.page_type != 'RespondPage':
        raise ValidateError("Invalid page type")

    if not ('single_field', 'input_text') in call_data:
        raise FailPage(message="No field given", widget="fields_error")
    field = call_data[('single_field', 'input_text')]
    if not field:
        raise FailPage(message="No field given", widget="fields_error")
    responder = page.responder
    # field options
    f_options = responder.field_options
    if not f_options['fields']:
        raise FailPage(message="Invalid submission, this responder does not have fields", widget="fields_error")
    if f_options['field_values']:
        raise FailPage(message="Invalid submission, this responder requires field values", widget="fields_error")
    responder.set_fields({ field:'' })
    utils.save(call_data, page=page, widget_name='fields_error')
    call_data['status'] = 'Fields set'



def delete_submit_list_string(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "deletes an indexed string from the submit_list"
    if 'page' not in call_data:
        raise FailPage(message = "page missing")
    page = call_data['page']
    if page.page_type != 'RespondPage':
        raise ValidateError("Invalid page type")

    if not 'delete_submit_list_string_index' in call_data:
        raise FailPage(message="No string index given", widget="submit_list_error")
    # Delete the string
    responder = page.responder
    if not (responder.submit_required or responder.submit_option):
        raise FailPage(message="Invalid submission, this responder does not have a submit_list")
    try:
        idx = int(call_data['delete_submit_list_string_index'])
        del responder.submit_list[idx]
    except:
        raise FailPage(message="Failed to delete the string", widget="submit_list_error")
    utils.save(call_data, page=page, widget_name='submit_list_error')


def add_submit_list_string(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Adds a new submit_list string"
    if 'page' not in call_data:
        raise FailPage(message = "page missing")
    page = call_data['page']
    if page.page_type != 'RespondPage':
        raise ValidateError("Invalid page type")

    if not 'submit_list_string' in call_data:
        raise FailPage(message="No submit_list string given", widget="submit_list_error")
    # Set the page submit_list_string
    responder = page.responder
    if not (responder.submit_required or responder.submit_option):
        raise FailPage(message="Invalid submission, this responder does not have a submit list")
    responder.submit_list.append(call_data['submit_list_string'])
    utils.save(call_data, page=page, widget_name='submit_list_error')


def set_validate_option(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Enable or disable the validate option"
    if 'page' not in call_data:
        raise FailPage(message = "page missing")
    page = call_data['page']
    if page.page_type != 'RespondPage':
        raise ValidateError("Invalid page type")
    
    if not page.responder.validate_option_available:
        return
        
    if page.responder.validate_option:
        page.responder.validate_option = False
        page_data['set_val_option','button_text'] = "Enable Validation"
        page_data['val_status','para_text'] = "Validate received field values : Disabled"
        page_data['validate_fail', 'hide'] = True
    else:
        page.responder.validate_option = True
        page_data['set_val_option','button_text'] = "Disable Validation"
        page_data['val_status','para_text'] = "Validate received field values : Enabled"
        page_data['validate_fail', 'hide'] = False
        
    utils.save(call_data, page=page)
    call_data['status'] = 'Validator changed'


def set_submit_option(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Enable or disable the submit option"
    if 'page' not in call_data:
        raise FailPage(message = "page missing")
    page = call_data['page']
    if page.page_type != 'RespondPage':
        raise ValidateError("Invalid page type")
        
    if not page.responder.submit_option_available:
        return
        
    if page.responder.submit_option:
        page.responder.submit_option = False
        page.responder.submit_list = []
    else:
        page.responder.submit_option = True
        
    utils.save(call_data, page=page, widget_name='alternate')
    call_data['status'] = 'Submit option changed'

