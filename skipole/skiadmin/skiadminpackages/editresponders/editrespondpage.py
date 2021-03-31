

"Functions implementing respond page editing"

import collections


from ... import skilift
from ....skilift import editresponder

from ... import ValidateError, FailPage, ServerError, GoTo

from ....ski.project_class_definition import SectionData

from .. import utils

def _ident_to_str(ident):
    "Returns string ident or label"
    if ident is None:
        return ''
    if isinstance(ident, str):
        return ident
    # ident must be a list or tuple of (project,number)
    if len(ident) != 2:
        raise FailPage("Invalid ident")
    return ident[0] + "," + str(ident[1])


def _field_to_string(wfield):
    "Returns two forms of a widgfield, or if a string, then just the string twice"
    if isinstance(wfield, str):
        return wfield, wfield
    # a widgfield has four elements, reduce it to the non empty elements
    shortwfield = [ w for w in wfield if w ]
    if len(shortwfield) == 1:
        return shortwfield[0], shortwfield[0]
    wf1 = ",".join(shortwfield)
    if len(shortwfield) == 2:
        wf2 = shortwfield[0] + ":" + shortwfield[1]
    else:
        wf2 = shortwfield[0] + "-" + shortwfield[1] + ":" + shortwfield[2]
    return wf1, wf2


def _t_ref(r_info, item):
    "Returns a TextBlock ref for the given item"
    return ".".join(["responders", r_info.module_name, r_info.responder, item])


def skicall_help(skicall):
    "Retrieves help text for the skicall object"
    text = skicall.textblock("aboutcode.skicall")
    if not text:
        text = "No help text for aboutcode.skicall has been found"

    pd = skicall.call_data['pagedata']
    # Fill in header
    sd_adminhead = SectionData("adminhead")
    sd_adminhead["show_help","para_text"] = "\n" + text
    sd_adminhead["show_help","hide"] = False
    pd.update(sd_adminhead)


def use_submit_list_help(skicall):
    "Retrieves help text for the use_submit_list decorator"
    text = skicall.textblock("aboutcode.usesubmitlist")
    if not text:
        text = "No help text for aboutcode.use_submit_list has been found"

    pd = skicall.call_data['pagedata']
    # Fill in header
    sd_adminhead = SectionData("adminhead")
    sd_adminhead["show_help","para_text"] = "\n" + text
    sd_adminhead["show_help","hide"] = False
    pd.update(sd_adminhead)


def fail_page_help(skicall):
    "Retrieves help text for the fail page ident"
    text = skicall.textblock("responders.fail_page")
    if not text:
        text = "No help text for responders.fail_page has been found"

    pd = skicall.call_data['pagedata']
    # Fill in header
    sd_adminhead = SectionData("adminhead")
    sd_adminhead["show_help","para_text"] = "\n" + text
    sd_adminhead["show_help","hide"] = False
    pd.update(sd_adminhead)


def submit_data_help(skicall):
    "Retrieves help text for the submit_data function"
    call_data = skicall.call_data
    if 'page_number' in call_data:
        pagenumber = call_data['page_number']
    else:
        raise FailPage(message = "page missing")
    try:
        project = call_data['editedprojname']
        # get a ResponderInfo named tuple with information about the responder
        r_info = editresponder.responder_info(project, pagenumber, call_data['pchange'])
    except ServerError as e:
        raise FailPage(message=e.message)
    sdtextref = _t_ref(r_info, 'submit_data')
    text = skicall.textblock(sdtextref)
    if not text:
        text = "No help text for %s has been found" % sdtextref

    pd = call_data['pagedata']
    # Fill in header
    sd_adminhead = SectionData("adminhead")
    sd_adminhead["show_help","para_text"] = "\n" + text
    sd_adminhead["show_help","hide"] = False
    pd.update(sd_adminhead)


def submit_dict_help(skicall):
    "Retrieves help text for the responder submit_dict"
    call_data = skicall.call_data
    if 'page_number' in call_data:
        pagenumber = call_data['page_number']
    else:
        raise FailPage(message = "page missing")
    try:
        project = call_data['editedprojname']
        # get a ResponderInfo named tuple with information about the responder
        r_info = editresponder.responder_info(project, pagenumber, call_data['pchange'])
    except ServerError as e:
        raise FailPage(message=e.message)
    sdtextref = _t_ref(r_info, 'submit_dict')
    text = skicall.textblock(sdtextref)
    if not text:
        text = "No help text for %s has been found" % sdtextref

    pd = call_data['pagedata']
    # Fill in header
    sd_adminhead = SectionData("adminhead")
    sd_adminhead["show_help","para_text"] = "\n" + text
    sd_adminhead["show_help","hide"] = False
    pd.update(sd_adminhead)


def call_data_help(skicall):
    "Retrieves help text for the responder call_data"
    call_data = skicall.call_data
    if 'page_number' in call_data:
        pagenumber = call_data['page_number']
    else:
        raise FailPage(message = "page missing")
    try:
        project = call_data['editedprojname']
        # get a ResponderInfo named tuple with information about the responder
        r_info = editresponder.responder_info(project, pagenumber, call_data['pchange'])
    except ServerError as e:
        raise FailPage(message=e.message)
    cdtextref = _t_ref(r_info, 'call_data')
    text = skicall.textblock(cdtextref)
    if not text:
        text = "No help text for %s has been found" % cdtextref

    pd = call_data['pagedata']
    # Fill in header
    sd_adminhead = SectionData("adminhead")
    sd_adminhead["show_help","para_text"] = "\n" + text
    sd_adminhead["show_help","hide"] = False
    pd.update(sd_adminhead)


def retrieve_edit_respondpage(skicall):
    "Retrieves widget data for the edit respond page"

    call_data = skicall.call_data
    page_data = skicall.page_data

    # clears any session data, keeping page_number, pchange and any status message
    utils.clear_call_data(call_data, keep=["page_number", "pchange", "status"])

    if 'page_number' in call_data:
        pagenumber = call_data['page_number']
        str_pagenumber = str(pagenumber)
    else:
        raise FailPage(message = "page missing")

    try:
        project = call_data['editedprojname']
        pageinfo = skilift.page_info(project, pagenumber)

        if pageinfo.item_type != 'RespondPage':
            raise FailPage(message = "Invalid page")

        call_data['pchange'] = pageinfo.change

        # fills in the data for editing page name, brief, parent, etc., 
        page_data[("adminhead","page_head","large_text")] = pageinfo.name
        page_data[('page_edit','p_ident','page_ident')] = (project,str_pagenumber)
        page_data[('page_edit','p_name','page_ident')] = (project,str_pagenumber)
        page_data[('page_edit','p_description','page_ident')] = (project,str_pagenumber)
        page_data[('page_edit','p_rename','input_text')] = pageinfo.name
        page_data[('page_edit','p_parent','input_text')] = "%s,%s" % (project, pageinfo.parentfolder_number)
        page_data[('page_edit','p_brief','input_text')] = pageinfo.brief

        # get a ResponderInfo named tuple with information about the responder
        r_info = editresponder.responder_info(project, pagenumber, call_data['pchange'])
    except ServerError as e:
        raise FailPage(message=e.message)

    page_data['respondertype:para_text'] = "This page is a responder of type: %s." % (r_info.responder,)
    page_data['responderdescription:textblock_ref'] = ".".join(["responders",r_info.module_name, r_info.responder])

    if r_info.widgfield_required:
        if r_info.widgfield:
            page_data['widgfield:input_text'] = r_info.widgfield
    else:
        page_data['widgfield:show'] = False

    if r_info.alternate_ident_required:
        page_data['alternate','input_text'] = _ident_to_str(r_info.alternate_ident)
        page_data['alternate_ident_description','textblock_ref'] = _t_ref(r_info, 'alternate_ident')
    else:
        page_data['alternate','show'] = False
        page_data['alternate_ident_description','show'] = False

    if r_info.target_ident_required:
        page_data['target:input_text'] = _ident_to_str(r_info.target_ident)
        page_data['target_ident_description','textblock_ref'] = _t_ref(r_info, 'target_ident')
    else:
        page_data['target:show'] = False
        page_data['target_ident_description','show'] = False

    if r_info.allowed_callers_required:
        page_data['allowed_callers_description:textblock_ref'] = _t_ref(r_info, 'allowed_callers')
        if r_info.allowed_callers:
            contents = []
            for ident in r_info.allowed_callers:
                ident_row = [_ident_to_str(ident), _ident_to_str(ident).replace(",","_")]
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
    if r_info.validate_option_available:
        page_data[('val_option_desc', 'textblock_ref')] =  _t_ref(r_info, 'validate_option')
        if r_info.validate_option:
            page_data['set_val_option','button_text'] = "Disable Validation"
            page_data['val_status','para_text'] = "Validate received field values : Enabled"
            page_data['validate_fail', 'input_text'] = _ident_to_str(r_info.validate_fail_ident)
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

    if r_info.submit_option_available:
        page_data['submit_option_desc','textblock_ref'] = _t_ref(r_info, 'submit_option')
        if r_info.submit_option:
            page_data['set_submit_option','button_text'] = 'Disable submit_data'
            page_data['submit_status','para_text'] = "Call submit_data : Enabled"
        else:
            page_data['set_submit_option','button_text'] = 'Enable submit_data'
            page_data['submit_status','para_text'] = "Call submit_data : Disabled"
    else:
        page_data['submit_option_desc','show'] = False
        page_data['set_submit_option','show'] = False
        page_data['submit_status','show'] = False

    if r_info.submit_required or r_info.submit_option:
        page_data['submit_list_description','textblock_ref'] = 'responders.about_submit_list'

        if r_info.submit_list:
            contents = []
            for index, s in enumerate(r_info.submit_list):
                s_row = [s, str(index)]
                contents.append(s_row)
            page_data['submit_list','contents'] = contents
        else:
            page_data['submit_list','show'] = False
        page_data['submit_string','input_text'] = ''
        page_data['fail_page_ident:input_text'] = _ident_to_str(r_info.fail_ident)
    else:
        page_data['submit_list_description','show'] = False
        page_data['submit_list','show'] = False
        page_data['submit_string','show'] = False
        page_data['submit_info','show'] = False
        page_data['fail_page_ident','show'] = False

    # final paragraph
    page_data['final_paragraph:textblock_ref'] = _t_ref(r_info, 'final_paragraph')

    # field options
    f_options = r_info.field_options
    if not f_options['fields']:
        # no fields so no further data to input
        return page_data

    # show the fields description
    page_data['fields_description:show'] = True
    page_data['fields_description:textblock_ref'] = _t_ref(r_info, 'fields')


    if f_options['field_values'] and ( not f_options['single_field'] ):
        page_data['field_values_list:show'] = True
        page_data['add_field_value:show'] = True
        # populate field_values_list
        contents = []
        field_vals = r_info.field_values_list
        for field, value in field_vals:
            f1,f2 = _field_to_string(field)
            v1,v2 = _field_to_string(value)
            if not v1:
                v1 = "' '"
            row = [f1, v1, f2]
            contents.append(row)
        if contents:
            contents.sort()
            page_data['field_values_list:contents'] = contents
        else:
            page_data['field_values_list:show'] = False
        # set the add_field_value label to be descriptive
        if f_options['widgfields']:
            if f_options['field_keys']:
                page_data['add_field_value','label'] = "Widgfields and keys:"
            else:
                page_data['add_field_value','label'] = "Widgfields and values:"
        else:
            page_data['add_field_value','label'] = "Items:"

        return
       

    if (not f_options['field_values']) and (not f_options['single_field']):
        page_data['field_list','show'] = True
        page_data['add_field','show'] = True
        # populate field_list
        contents = []
        field_vals = r_info.field_list
        for field in field_vals:
            f1,f2 = _field_to_string(field)
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
        if not r_info.single_field:
            page_data[('single_field','input_text')] = ''
        else:
            page_data[('single_field','input_text')] = r_info.single_field
        return


    # remaining is for a single field and value - still to do
    # as there is currently no responder which takes a single field and value
    #????????????????????????????????????????????????????????


def submit_widgfield(skicall):
    "Sets widgfield"

    call_data = skicall.call_data
    page_data = skicall.page_data

    project = call_data['editedprojname']
    pagenumber = call_data['page_number']
    pchange = call_data['pchange']
    if not 'widget' in call_data:
        raise FailPage(message="No widgfield given", widget="widgfield_error")
    if not call_data['widget']:
        raise FailPage(message="No widgfield given", widget="widgfield_error")
    # Set the page widgfield
    try:
        call_data['pchange'] = editresponder.set_widgfield(project, pagenumber, pchange, call_data['widget'])
    except ServerError as e:
        raise FailPage(e.message)
    call_data['status'] = 'WidgField set'


def submit_alternate_ident(skicall):
    "Sets the alternate page"

    call_data = skicall.call_data
    page_data = skicall.page_data

    project = call_data['editedprojname']
    pagenumber = call_data['page_number']
    pchange = call_data['pchange']
    if not 'alternate_ident' in call_data:
        raise FailPage(message="No alternate page label given", widget="alternate")
    # Set the page alternate_ident
    try:
        call_data['pchange'] = editresponder.set_alternate_ident(project, pagenumber, pchange, call_data['alternate_ident'])
    except ServerError as e:
        raise FailPage(e.message)
    page_data['alternate','set_input_accepted'] = True
    call_data['status'] = 'Page set'



def submit_target_ident(skicall):
    "Sets the target ident"

    call_data = skicall.call_data
    page_data = skicall.page_data

    project = call_data['editedprojname']
    pagenumber = call_data['page_number']
    pchange = call_data['pchange']
    if not 'target_ident' in call_data:
        raise FailPage(message="No target ident given", widget="target")
    # Set the page target_ident
    try:
        call_data['pchange'] = editresponder.set_target_ident(project, pagenumber, pchange, call_data['target_ident'])
    except ServerError as e:
        raise FailPage(e.message)
    page_data['target','set_input_accepted'] = True
    call_data['status'] = 'Target Ident set'


def submit_validate_fail_ident(skicall):
    "Sets the validate fail ident"

    call_data = skicall.call_data
    page_data = skicall.page_data

    project = call_data['editedprojname']
    pagenumber = call_data['page_number']
    pchange = call_data['pchange']
    if not 'validate_fail_ident' in call_data:
        raise FailPage(message="No validate fail ident given", widget="validate_fail")
    # Set the page validate_fail_ident
    try:
        call_data['pchange'] = editresponder.set_validate_fail_ident(project, pagenumber, pchange, call_data['validate_fail_ident'])
    except ServerError as e:
        raise FailPage(e.message)
    page_data['validate_fail','set_input_accepted'] = True
    call_data['status'] = 'Validate Fail Ident set'


def submit_fail_ident(skicall):
    "Sets the fail ident"

    call_data = skicall.call_data
    page_data = skicall.page_data

    project = call_data['editedprojname']
    pagenumber = call_data['page_number']
    pchange = call_data['pchange']
    if not 'fail_ident' in call_data:
        raise FailPage(message="No fail ident given", widget="fail_ident_error")
    # Set the page fail_ident
    try:
        call_data['pchange'] = editresponder.set_fail_ident(project, pagenumber, pchange, call_data['fail_ident'])
    except ServerError as e:
        raise FailPage(e.message)
    call_data['status'] = 'Fail Ident set'


def add_allowed_caller(skicall):
    "Adds a new allowed caller"

    call_data = skicall.call_data
    page_data = skicall.page_data

    project = call_data['editedprojname']
    pagenumber = call_data['page_number']
    pchange = call_data['pchange']
    if not 'allowed_caller' in call_data:
        raise FailPage(message="No allowed caller given", widget="allowed_callers_error")
    # Set the page allowed caller
    try:
        call_data['pchange'] = editresponder.add_allowed_caller(project, pagenumber, pchange, call_data['allowed_caller'])
    except ServerError as e:
        raise FailPage(e.message)


def delete_allowed_caller(skicall):
    "Deletes an allowed caller"

    call_data = skicall.call_data
    page_data = skicall.page_data

    project = call_data['editedprojname']
    pagenumber = call_data['page_number']
    pchange = call_data['pchange']
    if not 'delete_allowed_caller' in call_data:
        raise FailPage(message="No allowed caller given", widget="allowed_callers_error")
    # Delete the page allowed caller
    try:
        call_data['pchange'] = editresponder.delete_allowed_caller(project, pagenumber, pchange, call_data['delete_allowed_caller'])
    except ServerError as e:
        raise FailPage(e.message)


def remove_field(skicall):
    "Deletes a field"

    call_data = skicall.call_data
    page_data = skicall.page_data

    project = call_data['editedprojname']
    pagenumber = call_data['page_number']
    pchange = call_data['pchange']
    if not 'remove_field' in call_data:
        raise FailPage(message="No field to remove given", widget="fields_error")
    # Delete the page field
    try:
        call_data['pchange'] = editresponder.remove_field(project, pagenumber, pchange, call_data['remove_field'])
    except ServerError as e:
        raise FailPage(e.message)


def add_field_value(skicall):
    "Adds a field and value"

    call_data = skicall.call_data
    page_data = skicall.page_data

    project = call_data['editedprojname']
    pagenumber = call_data['page_number']
    pchange = call_data['pchange']

    if not 'field' in call_data:
        raise FailPage(message="No field given", widget="fields_error")
    if not call_data['field']:
        raise FailPage(message="No field given", widget="fields_error")
    if not 'value' in call_data:
        raise FailPage(message="No value given", widget="fields_error")

    # if value is empty ensure empty values allowed
    if not call_data['value']:
        # get a ResponderInfo named tuple with information about the responder
        try:
            r_info = editresponder.responder_info(project, pagenumber, pchange)
        except ServerError as e:
            raise FailPage(message=e.message)
        # field options
        f_options = r_info.field_options
        if not f_options['fields']:
            raise FailPage(message="Invalid submission, this responder does not have fields", widget="fields_error")
        if not f_options['empty_values_allowed']:
            page_data['add_field_value', 'input_text1'] = call_data['field']
            page_data['add_field_value', 'set_input_accepted1'] = True
            page_data['add_field_value', 'set_input_errored2'] = True
            raise FailPage(message="Invalid submission, empty field values are not allowed", widget="fields_error")
    # Add the field and value
    try:
        call_data['pchange'] = editresponder.add_field_value(project, pagenumber, pchange, call_data['field'], call_data['value'])
    except ServerError as e:
        raise FailPage(e.message)


def add_field(skicall):
    "Adds a field"

    call_data = skicall.call_data
    page_data = skicall.page_data

    project = call_data['editedprojname']
    pagenumber = call_data['page_number']
    pchange = call_data['pchange']
    if not 'field' in call_data:
        raise FailPage(message="No field given", widget="fields_error")
    if not call_data['field']:
        raise FailPage(message="No field given", widget="fields_error")
    # Add the field
    try:
        call_data['pchange'] = editresponder.add_field(project, pagenumber, pchange, call_data['field'])
    except ServerError as e:
        raise FailPage(e.message)


def set_single_field(skicall):
    "Sets the field in a responder, which require s single field only"

    call_data = skicall.call_data
    page_data = skicall.page_data

    project = call_data['editedprojname']
    pagenumber = call_data['page_number']
    pchange = call_data['pchange']
    if not ('single_field', 'input_text') in call_data:
        raise FailPage(message="No field given", widget="fields_error")
    field = call_data[('single_field', 'input_text')]
    if not field:
        raise FailPage(message="No field given", widget="fields_error")
    # Add the field
    try:
        call_data['pchange'] = editresponder.set_single_field(project, pagenumber, pchange, field)
    except ServerError as e:
        raise FailPage(e.message)
    call_data['status'] = 'Fields set'



def delete_submit_list_string(skicall):
    "deletes an indexed string from the submit_list"

    call_data = skicall.call_data
    page_data = skicall.page_data

    project = call_data['editedprojname']
    pagenumber = call_data['page_number']
    pchange = call_data['pchange']
    if not 'delete_submit_list_string_index' in call_data:
        raise FailPage(message="No submit_list string given", widget="submit_list_error")
    try:
        # get the submit list
        submit_list = editresponder.get_submit_list(project, pagenumber, pchange)
        idx = int(call_data['delete_submit_list_string_index'])
        del submit_list[idx]
        call_data['pchange'] = editresponder.set_submit_list(project, pagenumber, pchange, submit_list)
    except ServerError as e:
        raise FailPage(e.message)


def add_submit_list_string(skicall):
    "Adds a new submit_list string"

    call_data = skicall.call_data
    page_data = skicall.page_data

    project = call_data['editedprojname']
    pagenumber = call_data['page_number']
    pchange = call_data['pchange']
    if not 'submit_list_string' in call_data:
        raise FailPage(message="No submit_list string given", widget="submit_list_error")
    try:
        # get the submit list
        submit_list = editresponder.get_submit_list(project, pagenumber, pchange)
        submit_list.append(call_data['submit_list_string'])
        call_data['pchange'] = editresponder.set_submit_list(project, pagenumber, pchange, submit_list)
    except ServerError as e:
        raise FailPage(e.message)


def set_validate_option(skicall):
    "Enable or disable the validate option"

    call_data = skicall.call_data
    page_data = skicall.page_data

    project = call_data['editedprojname']
    pagenumber = call_data['page_number']
    pchange = call_data['pchange']
    try:
        call_data['pchange'], validate_option = editresponder.toggle_validate_option(project, pagenumber, pchange)
    except ServerError as e:
        raise FailPage(e.message)        
    if validate_option:
        page_data['set_val_option','button_text'] = "Disable Validation"
        page_data['val_status','para_text'] = "Validate received field values : Enabled"
        page_data['validate_fail', 'hide'] = False
    else:
        page_data['set_val_option','button_text'] = "Enable Validation"
        page_data['val_status','para_text'] = "Validate received field values : Disabled"
        page_data['validate_fail', 'hide'] = True
    call_data['status'] = 'Validator changed'


def set_submit_option(skicall):
    "Enable or disable the submit option"

    call_data = skicall.call_data
    page_data = skicall.page_data

    project = call_data['editedprojname']
    pagenumber = call_data['page_number']
    pchange = call_data['pchange']
    try:
        call_data['pchange'], submit_option = editresponder.toggle_submit_option(project, pagenumber, pchange)
    except ServerError as e:
        raise FailPage(e.message)  
    call_data['status'] = 'Submit option changed'


def map(skicall):
    "Creates the responder map"
    pagenumber = skicall.call_data['page_number']
    project = skicall.call_data['editedprojname']
    page_data = skicall.page_data
    page_data['responder', 'responderid', 'text'] = "Ident: " + str(pagenumber)

    # insert font text style
    page_data['textstyle', 'text'] = """
  <style>
    /* <![CDATA[ */
    text {
      fill: black;
      font-family: Arial, Helvetica, sans-serif;
    }
    .bigtext {
      font-size: 20px;
    }
    /* ]]> */
  </style>
    """


    map_height = 1600

    # get information about the responder
    pageinfo = skilift.page_info(project, pagenumber)
    r_info = editresponder.responder_info(project, pagenumber)
    i_info = skilift.item_info(project, pagenumber)
    label_list = i_info.label_list

    # list of all responders
    responder_list = editresponder.all_responders(project)

    # Find all responders which call this responder

    callers = [[0,0, "Responders in this project with %s as Target:" % pagenumber]]
    callers2 = []
    n = 40
    for responder_id in responder_list:
        responder_info = editresponder.responder_info(project, responder_id)
        target = responder_info.target_ident
        if target:
            if isinstance(target, str) and (target in label_list):
                moreinfo = skilift.page_info(project, responder_id)
                if n<=300:
                    callers.append([0,n,str(responder_id) + " " + moreinfo.brief])
                else:
                    callers2.append([0,n-280,str(responder_id) + " " + moreinfo.brief])
                n += 20
            elif isinstance(target, tuple) and (len(target) == 2) and (project == target[0]) and (pagenumber == target[1]):
                moreinfo = skilift.page_info(project, responder_id)
                if n<=300:
                    callers.append([0,n,str(responder_id) + " " + moreinfo.brief])
                else:
                    callers2.append([0,n-280,str(responder_id) + " " + moreinfo.brief])
                n += 20
    if n == 40:
        page_data['callers','show'] = False
        page_data['callers2','show'] = False
    elif not callers2:
        page_data['callers', 'callers', 'lines'] = callers
        page_data['callers2','show'] = False
    else:
        page_data['callers', 'callers', 'lines'] = callers
        page_data['callers2', 'callers', 'lines'] = callers2


    # Find all responders which call this responder on failure

    fails = [[0,0, "Responders in this project with %s as Fail Page:" % pagenumber]]
    n = 40
    count = 0
    for responder_id in responder_list:
        responder_info = editresponder.responder_info(project, responder_id)
        failident = responder_info.fail_ident
        if failident:
            if n > 300:
                # do not display more than 14 responders, but continue to count remaining ones
                count += 1
                continue
            if isinstance(failident, str) and (failident in label_list):
                moreinfo = skilift.page_info(project, responder_id)
                fails.append([0,n,str(responder_id) + " " + moreinfo.brief])
                n += 20
            elif isinstance(failident, tuple) and (len(failident) == 2) and (project == failident[0]) and (pagenumber == failident[1]):
                moreinfo = skilift.page_info(project, responder_id)
                fails.append([0,n,str(responder_id) + " " + moreinfo.brief])
                n += 20
    if count:
        fails.append([0, 320, "Plus %s more responders." % (count,)]) 
    if n == 40:
        page_data['fails','show'] = False
    else:
        page_data['fails', 'callers', 'lines'] = fails


    # Find allowed callers to this responder

    allowed_list = r_info.allowed_callers
    if allowed_list:
        page_data['allowed','show'] = True
        allowed = [[0,0, "Allowed callers to %s:" % pagenumber], [0,20, "(Calling page must provide ident information)"]]
        n = 40
        for allowedid in allowed_list:
            allowedident = allowedid
            if isinstance(allowedident, str):
                allowedident = skilift.ident_from_label(project, allowedident)
            if allowedident is None:
                allowed.append([0,n,"UNKNOWN page: " + allowedid])
                n += 20
            elif isinstance(allowedident, str):
                allowed.append([0,n,"INVALID ident: " + allowedident])
                n += 20
            elif isinstance(allowedident, tuple) and (len(allowedident) == 2):
                try:
                    allowedinfo = skilift.page_info(*allowedident)
                except ServerError:
                    allowed.append([0,n,"UNKNOWN page: " + allowedident[0] + ", " + str(allowedident[1])])
                else:
                    if allowedident[0] == project:
                        allowed.append([0,n,str(allowedident[1]) + ": " + allowedinfo.brief])
                    else:
                        allowed.append([0,n,allowedident[0] + ", " + str(allowedident[1]) + ": " + allowedinfo.brief])
                n += 20

        page_data['allowed', 'callers', 'lines'] = allowed
    else:
        page_data['allowed','show'] = False



    # If the responder has a target, draw a target line on the page
    if r_info.target_ident or r_info.target_ident_required:
        page_data['targetline','show'] = True
    else:
        page_data['targetline','show'] = False

    # normally no output ellipse is shown
    page_data['output','show'] = False


    # fill in the box regarding this responder
    if pageinfo.restricted:
        page_data['responder', 'responderaccess', 'text'] = "Restricted access"
    else:
        page_data['responder', 'responderaccess', 'text'] = "Open access"
    if label_list:
        page_data['responder', 'responderlabels', 'text'] = "Label: " + ','.join(label_list)
    else:
        page_data['responder', 'responderlabels', 'show'] = False
    page_data['responder', 'respondertype', 'text'] = "Responder: " + r_info.responder
    page_data['responder', 'responderbrief', 'text'] = pageinfo.brief

    # submit_data information
    if r_info.submit_option or r_info.submit_required:
        page_data['submitdata','show'] = True
        if r_info.submit_list:
            s_list = []
            s = 0
            for item in r_info.submit_list:
                s_list.append([0,s,item])
                s += 20
            page_data['submitdata', 'submitlist','lines'] = s_list
        # show the return value
        if r_info.responder == "ColourSubstitute":
            page_data['submitdata','submitdatareturn','text'] = "Returns a dictionary of strings: colour strings"
        elif r_info.responder == "SetCookies":
            page_data['submitdata','submitdatareturn','text'] = "Returns an instance of http.cookies.BaseCookie"
        elif r_info.responder == "GetDictionaryDefaults":
            page_data['submitdata','submitdatareturn','text'] = "Returns a dictionary with default values"
        elif r_info.responder == "SubmitJSON":
            page_data['submitdata','submitdatareturn','text'] = "Returns a dictionary"
            # no target, but include a target line
            page_data['targetline','show'] = True
            # change 'Target Page' to 'Output'
            page_data['submitdata','output', 'text'] = "Output"
            # show an output ellipse
            page_data['output','show'] = True
            page_data['output','textout', 'text'] = "Send JSON data"
            page_data['output','textout', 'x'] = 320
        elif r_info.responder == "SubmitPlainText":
            page_data['submitdata','submitdatareturn','text'] = "Returns a string"
            # no target, but include a target line
            page_data['targetline','show'] = True
            # change 'Target Page' to 'Output'
            page_data['submitdata','output', 'text'] = "Output"
            # show an output ellipse
            page_data['output','show'] = True
            page_data['output','textout', 'text'] = "Send plain text"
            page_data['output','textout', 'x'] = 320
        elif r_info.responder == "SubmitCSS":
            page_data['submitdata','submitdatareturn','text'] = "Returns a style"
            # no target, but include a target line
            page_data['targetline','show'] = True
            # change 'Target Page' to 'Output'
            page_data['submitdata','output', 'text'] = "Output"
            # show an output ellipse
            page_data['output','show'] = True
            page_data['output','textout', 'text'] = "Send CSS data"
            page_data['output','textout', 'x'] = 320
        elif r_info.responder == "MediaQuery":
            page_data['submitdata','submitdatareturn','text'] = "Returns a dictionary of media queries : CSS targets"
            # no target, but include a target line
            page_data['targetline','show'] = True
            # change 'Target Page' to 'Output'
            page_data['submitdata','output', 'text'] = "Output"
            # show an output ellipse
            page_data['output','show'] = True
            page_data['output','textout', 'text'] = "Update query:target items"
            page_data['output','textout', 'x'] = 320
        elif r_info.responder == "SubmitIterator":
            page_data['submitdata','submitdatareturn','text'] = "Returns a binary file iterator"
            # no target, but include a target line
            page_data['targetline','show'] = True
            # change 'Target Page' to 'Output'
            page_data['submitdata','output', 'text'] = "Output"
            # show an output ellipse
            page_data['output','show'] = True
            page_data['output','textout', 'text'] = "Send Binary data"
            page_data['output','textout', 'x'] = 320

        # show the fail page
        _show_submit_data_failpage(project, page_data, r_info)
    else:
        page_data['submitdata','show'] = False
        page_data['submitdata_failpage','show'] = False

    # The target page
    _show_target(project, page_data, r_info)

    # validation option
    _show_validate_fail(project, page_data, r_info)

    # The alternate option
    _show_alternate(project, page_data, r_info)

    if r_info.responder == 'CaseSwitch':
        _show_caseswitch(project, page_data, r_info)
    elif r_info.responder == 'EmptyCallDataGoto':
        _show_emptycalldatagoto(project, page_data, r_info)
    elif r_info.responder == 'EmptyGoto':
        _show_emptygoto(project, page_data, r_info)
    elif r_info.responder == "MediaQuery":
        _show_mediaquery(project, page_data, r_info)


def _show_target(project, page_data, r_info):
    "The responder passes the call to this target"
    if r_info.target_ident or r_info.target_ident_required:
        page_data['target','show'] = True
        if r_info.target_ident:
            targetident = r_info.target_ident
            if isinstance(targetident, str):
                targetident = skilift.ident_from_label(project, targetident)
            if targetident is None:
                page_data['target','show'] = False
            elif isinstance(targetident, str):
                page_data['target', 'responderid', 'text'] = targetident
            elif isinstance(targetident, tuple) and (len(targetident) == 2):
                try:
                    targetinfo = skilift.page_info(*targetident)
                except ServerError:
                    page_data['target', 'responderid', 'text'] = "Unknown Ident: " + targetident[0] + ", " + str(targetident[1])
                else:
                    if targetident[0] == project:
                        page_data['target', 'responderid', 'text'] = "Ident: " + str(targetident[1])
                    else:
                        page_data['target', 'responderid', 'text'] = "Ident: " + targetident[0] + ", " + str(targetident[1])
                    if targetinfo.restricted:
                        page_data['target', 'responderaccess', 'text'] = "Restricted access"
                    else:
                        page_data['target', 'responderaccess', 'text'] = "Open access"
                    if isinstance(r_info.target_ident, str):
                        page_data['target', 'responderlabels', 'text'] = "Targeted from responder as: " + r_info.target_ident
                    else:
                        page_data['target', 'responderlabels', 'text'] = "Targeted from responder as: " + r_info.target_ident[0] + ", " + str(r_info.target_ident[1])
                    page_data['target', 'responderbrief', 'text'] = targetinfo.brief
                    if targetinfo.item_type == "RespondPage":
                        page_data['target', 'respondertype', 'text'] = "Responder: " + targetinfo.responder
                    else:
                        page_data['target', 'respondertype', 'text'] = targetinfo.item_type
    else:
        page_data['target','show'] = False


def _show_submit_data_failpage(project, page_data, r_info):
    "The responder calls submit data, which, if it raises a FailPage, calls this"
    page_data['submitdata_failpage','show'] = True
    if r_info.fail_ident:
        failident = r_info.fail_ident
        if isinstance(failident, str):
            failident = skilift.ident_from_label(project, failident)
        if failident is None:
            page_data['submitdata_failpage', 'responderid', 'text'] = "Ident not recognised"
        elif isinstance(failident, str):
            page_data['submitdata_failpage', 'responderid', 'text'] = failident
        elif isinstance(failident, tuple) and (len(failident) == 2):
            try:
                failinfo = skilift.page_info(*failident)
            except ServerError:
                page_data['submitdata_failpage', 'responderid', 'text'] = "Unknown Ident: " + failident[0] + ", " + str(failident[1])
            else:
                if failident[0] == project:
                    page_data['submitdata_failpage', 'responderid', 'text'] = "Ident: " + str(failident[1])
                else:
                    page_data['submitdata_failpage', 'responderid', 'text'] = "Ident: " + failident[0] + ", " + str(failident[1])
                if failinfo.restricted:
                    page_data['submitdata_failpage', 'responderaccess', 'text'] = "Restricted access"
                else:
                    page_data['submitdata_failpage', 'responderaccess', 'text'] = "Open access"
                if isinstance(r_info.fail_ident, str):
                    page_data['submitdata_failpage', 'responderlabels', 'text'] = "Set in responder as: " + r_info.fail_ident
                else:
                    page_data['submitdata_failpage', 'responderlabels', 'text'] = "Set in responder as: " + r_info.fail_ident[0] + ", " + str(r_info.fail_ident[1])
                page_data['submitdata_failpage', 'responderbrief', 'text'] = failinfo.brief
                if failinfo.item_type == "RespondPage":
                    page_data['submitdata_failpage', 'respondertype', 'text'] = "Responder: " + failinfo.responder
                else:
                    page_data['submitdata_failpage', 'respondertype', 'text'] = failinfo.item_type
    else:
        page_data['submitdata_failpage', 'responderid', 'text'] = "Ident not set"


def _show_validate_fail(project, page_data, r_info):
    "The responder validates received data, on failure calls this"

    if r_info.validate_option:
        page_data['validate','show'] = True
    else:
        page_data['validate','show'] = False
        return

    if r_info.validate_fail_ident:
        failident = r_info.validate_fail_ident
        if isinstance(failident, str):
            failident = skilift.ident_from_label(project, failident)
        if isinstance(failident, str):
            page_data['validate', 'responderid', 'text'] = failident
        elif isinstance(failident, tuple) and (len(failident) == 2):
            try:
                failinfo = skilift.page_info(*failident)
            except ServerError:
                page_data['validate', 'responderid', 'text'] = "Unknown Ident: " + failident[0] + ", " + str(failident[1])
            else:
                if failident[0] == project:
                    page_data['validate', 'responderid', 'text'] = "Ident: " + str(failident[1])
                else:
                    page_data['validate', 'responderid', 'text'] = "Ident: " + failident[0] + ", " + str(failident[1])
                if failinfo.restricted:
                    page_data['validate', 'responderaccess', 'text'] = "Restricted access"
                else:
                    page_data['validate', 'responderaccess', 'text'] = "Open access"
                if isinstance(r_info.fail_ident, str):
                    page_data['validate', 'responderlabels', 'text'] = "Set in responder as: " + r_info.fail_ident
                else:
                    page_data['validate', 'responderlabels', 'text'] = "Set in responder as: " + r_info.fail_ident[0] + ", " + str(r_info.fail_ident[1])
                page_data['validate', 'responderbrief', 'text'] = failinfo.brief
                if failinfo.item_type == "RespondPage":
                    page_data['validate', 'respondertype', 'text'] = "Responder: " + failinfo.responder
                else:
                    page_data['validate', 'respondertype', 'text'] = failinfo.item_type


def _show_alternate(project, page_data, r_info):
    "The alternate page"

    if r_info.alternate_ident:
        page_data['alternatebox','show'] = True
    else:
        page_data['alternatebox','show'] = False
        return

    if r_info.alternate_ident:
        altident = r_info.alternate_ident
        if isinstance(altident, str):
            altident = skilift.ident_from_label(project, altident)
        if isinstance(altident, str):
            page_data['alternatebox', 'responderid', 'text'] = altident
        elif isinstance(altident, tuple) and (len(altident) == 2):
            try:
                altinfo = skilift.page_info(*altident)
            except ServerError:
                page_data['alternatebox', 'responderid', 'text'] = "Unknown Ident: " + altident[0] + ", " + str(altident[1])
            else:
                if altident[0] == project:
                    page_data['alternatebox', 'responderid', 'text'] = "Ident: " + str(altident[1])
                else:
                    page_data['alternatebox', 'responderid', 'text'] = "Ident: " + altident[0] + ", " + str(altident[1])
                if altinfo.restricted:
                    page_data['alternatebox', 'responderaccess', 'text'] = "Restricted access"
                else:
                    page_data['alternatebox', 'responderaccess', 'text'] = "Open access"
                if isinstance(r_info.alternate_ident, str):
                    page_data['alternatebox', 'responderlabels', 'text'] = "Set in responder as: " + r_info.alternate_ident
                else:
                    page_data['alternatebox', 'responderlabels', 'text'] = "Set in responder as: " + r_info.alternate_ident[0] + ", " + str(r_info.alternate_ident[1])
                page_data['alternatebox', 'responderbrief', 'text'] = altinfo.brief
                if altinfo.item_type == "RespondPage":
                    page_data['alternatebox', 'respondertype', 'text'] = "Responder: " + altinfo.responder
                else:
                    page_data['alternatebox', 'respondertype', 'text'] = altinfo.item_type

    if r_info.responder == 'CaseSwitch':
        page_data['alternatebox', 'alttext', 'text'] = "Called if no match found"
    elif r_info.responder == 'EmptyCallDataGoto':
        page_data['alternatebox', 'alttext', 'text'] = "Called if skicall.call_data has key with value"
    elif r_info.responder == 'EmptyGoto':
        page_data['alternatebox', 'alttext', 'text'] = "Called if widgfield is present with a value"


def _show_caseswitch(project, page_data, r_info):

    page_data['textgroup', 'transform'] = 'translate(500,600)'

    if r_info.widgfield:
        text_title = """<text x="0" y="90">CaseSwitch on widgfield %s</text>""" % r_info.widgfield
    else:
        text_title = ''

    table_element = ''
    if r_info.field_values_list:
        for index, item in enumerate(r_info.field_values_list):
            table_element += _caseswitchtable(index, r_info.field_values_list)

    else:
        table_element = ''
    page_data['textgroup', 'text'] = text_title + table_element


def _caseswitchtable(index, field_values_list):
    y = 100 + 60*index
    return """
<rect height="60" style="fill:white;stroke-width:3;stroke:black" width="600" x="0" y="%s" />
<line x1="180" y1="%s" x2="180" y2="%s" style="stroke-width:3;stroke:black" />
<text x="20" y="%s">%s</text>
<text x="200" y="%s">%s</text>
""" % (y, y, y+60, y+30, field_values_list[index][0],y+30, field_values_list[index][1])


def _show_emptycalldatagoto(project, page_data, r_info):
    value = 'UNKNOWN'
    if r_info.single_field:
        value = r_info.single_field
    page_data['textgroup', 'transform'] = 'translate(750,700)'
    page_data['textgroup', 'text'] = """
<text x="0" y="0">Test skicall.call_data["%s"]</text>
<text x="0" y="60">Called if key not present, or has empty value.</text>
""" % (value,)


def _show_emptygoto(project, page_data, r_info):
    value = 'UNKNOWN'
    if r_info.widgfield:
        value = r_info.widgfield
    page_data['textgroup', 'transform'] = 'translate(750,700)'
    page_data['textgroup', 'text'] = """
<text x="0" y="0">Test widgfield %s</text>
<text x="0" y="60">Called if widgfield not present, or has empty value.</text>
""" % (value,)



def _show_mediaquery(project, page_data, r_info):
    page_data['textgroup', 'transform'] = 'translate(50,550)'

    if r_info.field_values_list:
        text_title = """<line x1="450" y1="70" x2="450" y2="100" style="stroke-width:3;stroke:black" />
<text x="0" y="90">Query:target</text>"""
    else:
        return
    table_element = ''
    for index, item in enumerate(r_info.field_values_list):
        table_element += _mediaquerytable(index, r_info.field_values_list)
    page_data['textgroup', 'text'] = text_title + table_element


def _mediaquerytable(index, field_values_list):
    y = 100 + 60*index
    return """
<rect height="60" style="fill:white;stroke-width:3;stroke:black" width="600" x="0" y="%s" />
<line x1="280" y1="%s" x2="280" y2="%s" style="stroke-width:3;stroke:black" />
<text x="20" y="%s">%s</text>
<text x="300" y="%s">%s</text>
""" % (y, y, y+60, y+30, field_values_list[index][0],y+30, field_values_list[index][1])



