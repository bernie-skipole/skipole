

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
    pd = call_data['pagedata']

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


        # Fill in header
        sd_adminhead = SectionData("adminhead")
        sd_adminhead["page_head","large_text"] = pageinfo.name
        sd_adminhead["map","show"] = True
        pd.update(sd_adminhead)

        # fills in the data for editing page name, brief, parent, etc.,

        sd_page_edit = SectionData("page_edit")
        sd_page_edit['p_ident','page_ident'] = (project,str_pagenumber)
        sd_page_edit['p_name','page_ident'] = (project,str_pagenumber)
        sd_page_edit['p_description','page_ident'] = (project,str_pagenumber)
        sd_page_edit['p_rename','input_text'] = pageinfo.name
        sd_page_edit['p_parent','input_text'] = "%s,%s" % (project, pageinfo.parentfolder_number)
        sd_page_edit['p_brief','input_text'] = pageinfo.brief
        pd.update(sd_page_edit)

        # get a ResponderInfo named tuple with information about the responder
        r_info = editresponder.responder_info(project, pagenumber, call_data['pchange'])
    except ServerError as e:
        raise FailPage(message=e.message)

    pd['respondertype','para_text'] = "This page is a responder of type: %s." % (r_info.responder,)
    pd['responderdescription','textblock_ref'] = ".".join(["responders",r_info.module_name, r_info.responder])


    sd_setwidgfield = SectionData("setwidgfield")
    sd_setwidgfield['widgfieldform', 'action'] = "responder_widgfield"

    if r_info.widgfield_required:
        if r_info.widgfield:
            pd['widgfield','input_text'] = r_info.widgfield
            if not r_info.widgfield:
                sd_setwidgfield['respondersection','input_text'] = ''
                sd_setwidgfield['responderwidget','input_text'] = ''
                sd_setwidgfield['responderfield','input_text'] = ''
            else:
                widg = r_info.widgfield.split(',')
                if len(widg) == 3:
                    sd_setwidgfield['respondersection','input_text'] = widg[0]
                    sd_setwidgfield['responderwidget','input_text'] = widg[1]
                    sd_setwidgfield['responderfield','input_text'] = widg[2]
                elif len(widg) == 2:
                    sd_setwidgfield['respondersection','input_text'] = ''
                    sd_setwidgfield['responderwidget','input_text'] = widg[0]
                    sd_setwidgfield['responderfield','input_text'] = widg[1]
                else:
                    sd_setwidgfield['respondersection','input_text'] = ''
                    sd_setwidgfield['responderwidget','input_text'] = ''
                    sd_setwidgfield['responderfield','input_text'] = ''
    else:
        pd['widgfield','show'] = False
        sd_setwidgfield.show = False

    pd.update(sd_setwidgfield)

    # alternate ident
    if r_info.alternate_ident_required:
        sd_alternate = utils.formtextinput( "alternate_ident",                         # section alias
                                            _t_ref(r_info, 'alternate_ident'),         # textblock
                                            "Set an alternate ident:",                 # field label
                                            _ident_to_str(r_info.alternate_ident),     # input text
                                            action = "alternate_ident",
                                            action_json = "alternate_ident_json",
                                            left_label = "Submit the ident : ")
    else:
        sd_alternate = SectionData("alternate_ident")
        sd_alternate.show = False
    pd.update(sd_alternate)

    # target ident
    if r_info.target_ident_required:
        sd_target = utils.formtextinput("target_ident",                         # section alias
                                        _t_ref(r_info, 'target_ident'),         # textblock
                                        "Set the target ident:",                 # field label
                                        _ident_to_str(r_info.target_ident),     # input text
                                        action = "set_target_ident",
                                        action_json = "set_target_ident_json",
                                        left_label = "Submit the ident : ")
    else:
        sd_target = SectionData("target_ident")
        sd_target.show = False
    pd.update(sd_target)

    # allowed callers
    if r_info.allowed_callers_required:
        pd['allowed_callers_description','textblock_ref'] = _t_ref(r_info, 'allowed_callers_list')
        if r_info.allowed_callers:
            contents = []
            for ident in r_info.allowed_callers:
                ident_row = [_ident_to_str(ident), _ident_to_str(ident).replace(",","_")]
                contents.append(ident_row)
            pd['allowed_callers_list','contents'] = contents
        else:
            pd['allowed_callers_list','show'] = False

        sd_allowed_caller = utils.formtextinput("allowed_caller",                         # section alias
                                                _t_ref(r_info, 'allowed_callers'),        # textblock
                                                "Add an allowed caller ident or label:",  # field label
                                                "",                                       # input text
                                                action = "add_allowed_caller",
                                                left_label = "Add the allowed caller : ")
    else:
        pd['allowed_callers_description','show'] = False
        pd['allowed_callers_list','show'] = False
        sd_allowed_caller = SectionData("allowed_caller")
        sd_allowed_caller.show = False

    pd.update(sd_allowed_caller)

    # validate option
    if r_info.validate_option_available:
        pd['val_option_desc', 'textblock_ref'] =  _t_ref(r_info, 'validate_option')
        if r_info.validate_option:
            pd['set_val_option','button_text'] = "Disable Validation"
            pd['val_status','para_text'] = "Validate received field values : Enabled"
            pd['validate_fail', 'input_text'] = _ident_to_str(r_info.validate_fail_ident)
            pd['validate_fail', 'hide'] = False
        else:
            pd['set_val_option','button_text'] = "Enable Validation"
            pd['val_status','para_text'] = "Validate received field values : Disabled"
            pd['validate_fail', 'hide'] = True
    else:
        pd['val_option_desc','show'] = False
        pd['set_val_option','show'] = False
        pd['val_status','show'] = False
        pd['validate_fail', 'show'] = False

    
    # submit option

    if r_info.submit_option_available:
        pd['submit_option_desc','textblock_ref'] = _t_ref(r_info, 'submit_option')
        if r_info.submit_option:
            pd['set_submit_option','button_text'] = 'Disable submit_data'
            pd['submit_status','para_text'] = "Call submit_data : Enabled"
        else:
            pd['set_submit_option','button_text'] = 'Enable submit_data'
            pd['submit_status','para_text'] = "Call submit_data : Disabled"
    else:
        pd['submit_option_desc','show'] = False
        pd['set_submit_option','show'] = False
        pd['submit_status','show'] = False

    if r_info.submit_required or r_info.submit_option:
        pd['submit_list_description','textblock_ref'] = 'responders.about_submit_list'

        if r_info.submit_list:
            contents = []
            for index, s in enumerate(r_info.submit_list):
                s_row = [s, str(index)]
                contents.append(s_row)
            pd['submit_list','contents'] = contents
        else:
            pd['submit_list','show'] = False
        pd['submit_string','input_text'] = ''
        # fail page
        sd_failpage = utils.formtextinput(  "failpage",                        # section alias
                                            'responders.shortfailpage',        # textblock
                                            "Fail page ident or label:",       # field label
                                            _ident_to_str(r_info.fail_ident),  # input text
                                            action = "set_fail_ident",
                                            left_label = "Set the fail page : ")
    else:
        pd['submit_list_description','show'] = False
        pd['submit_list','show'] = False
        pd['submit_string','show'] = False
        pd['submit_info','show'] = False
        sd_failpage = SectionData('failpage')
        sd_failpage.show = False

    pd.update(sd_failpage)


    # final paragraph
    pd['final_paragraph','textblock_ref'] = _t_ref(r_info, 'final_paragraph')

    # field options
    f_options = r_info.field_options
    if not f_options['fields']:
        # no fields so no further data to input, ensure the following sections are not shown

        sd_singlefield = SectionData('singlefield')
        sd_singlefield.show = False
        pd.update(sd_singlefield)

        sd_widgfieldval = SectionData('widgfieldval')
        sd_widgfieldval.show = False
        pd.update(sd_widgfieldval)

        sd_addfieldval = SectionData('addfieldval')
        sd_addfieldval.show = False
        pd.update(sd_addfieldval)

        return

    # the fields option is enabled

    # show the fields description  ========      this to be removed and replaced
    pd['fields_description','show'] = True
    pd['fields_description','textblock_ref'] = _t_ref(r_info, 'fields')
    ###########################################################################

    if f_options['single_field']:
        # single field, no value
        if not f_options['field_values']:
            if r_info.single_field:
                fieldname = r_info.single_field
            else:
                fieldname = ''
            sd_singlefield = utils.formtextinput(   "singlefield",                   # section alias
                                                    _t_ref(r_info, 'fields'),        # textblock
                                                    "Set the field name:",           # field label
                                                    fieldname,                       # input text
                                                    action = "set_field",
                                                    left_label = "Submit the field : ")
            pd.update(sd_singlefield)
        # currently there is no responder which takes a single field and value
        #########################################################################
        # if singlefield is enabled, no others are
        sd_widgfieldval = SectionData('widgfieldval')
        sd_widgfieldval.show = False
        pd.update(sd_widgfieldval)

        sd_addfieldval = SectionData('addfieldval')
        sd_addfieldval.show = False
        pd.update(sd_addfieldval)

        return
    else:
        sd_singlefield = SectionData('singlefield')
        sd_singlefield.show = False
        pd.update(sd_singlefield)


    # to get here single_field is not enabled


    if f_options['field_values']:
        pd['field_values_list','show'] = True
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
            pd['field_values_list','contents'] = contents
        else:
            pd['field_values_list','show'] = False
        # populate the widgfieldval section
        if f_options['widgfields']:
            # addfieldval is not shown
            sd_addfieldval = SectionData('addfieldval')
            sd_addfieldval.show = False
 
            if f_options['field_keys']:
                sd_widgfieldval = utils.widgfieldval('widgfieldval',
                                                     _t_ref(r_info, 'fields'),
                                                     "key to be used in call_data:",
                                                     action='add_widgfield_value',
                                                     left_label='Add the key :')
            else:
                sd_widgfieldval = utils.widgfieldval('widgfieldval',
                                                     _t_ref(r_info, 'fields'),
                                                     "Widget/field value:",
                                                     action='add_widgfield_value',
                                                     left_label='submit value :')
        else:
            ### f_options['field_values'] is True, but not f_options['widgfields']
            sd_addfieldval = utils.addfieldval('addfieldval',
                                               _t_ref(r_info, 'fields'),        # textblock
                                               'Set the value to be tested :',
                                               'Set the ident or label to go to :',
                                               action='admin_home')
            sd_widgfieldval = SectionData('widgfieldval')
            sd_widgfieldval.show = False
        pd.update(sd_widgfieldval)
        pd.update(sd_addfieldval)
    else:
        # not field:values, so do not show widgfieldval or addfieldval sections
        sd_widgfieldval = SectionData('widgfieldval')
        sd_widgfieldval.show = False
        pd.update(sd_widgfieldval)

        sd_addfieldval = SectionData('addfieldval')
        sd_addfieldval.show = False
        pd.update(sd_addfieldval)

        pd['field_list','show'] = True
        pd['add_field','show'] = True
        # populate field_list
        contents = []
        field_vals = r_info.field_list
        for field in field_vals:
            f1,f2 = _field_to_string(field)
            row = [f1, f2]
            contents.append(row)
        if contents:
            contents.sort()
            pd['field_list','contents'] = contents
        else:
            pd['field_list','show'] = False
        # populate add_field
        if f_options['widgfields']:
             pd['add_field','label'] = "Add a widgfield:"
        else:
            pd['add_field,','label'] = "Add a string:"



def submit_widgfield(skicall):
    "Sets widgfield"

    call_data = skicall.call_data

    project = call_data['editedprojname']
    pagenumber = call_data['page_number']
    pchange = call_data['pchange']

    if ('setwidgfield','responderwidget','input_text') not in call_data:
        raise FailPage(message="No widget name given")
    if not call_data['setwidgfield','responderwidget','input_text']:
        raise FailPage(message="No widget name given")
    widgfield = call_data['setwidgfield','responderwidget','input_text']

    if ('setwidgfield','responderfield','input_text') not in call_data:
        raise FailPage(message="No widget field given")
    if not call_data['setwidgfield','responderfield','input_text']:
        raise FailPage(message="No widget field given")
    widgfield = widgfield + "," + call_data['setwidgfield','responderfield','input_text']

    if ('setwidgfield','respondersection','input_text') in call_data:
        if call_data['setwidgfield','respondersection','input_text']:
            widgfield = call_data['setwidgfield','respondersection','input_text'] + ',' + widgfield
    try:
        call_data['pchange'] = editresponder.set_widgfield(project, pagenumber, pchange, widgfield)
    except ServerError as e:
        raise FailPage(e.message)
    call_data['status'] = 'WidgField set'


def submit_alternate_ident(skicall):
    "Sets the alternate page"

    call_data = skicall.call_data
    pd = call_data['pagedata']

    project = call_data['editedprojname']
    pagenumber = call_data['page_number']
    pchange = call_data['pchange']
    if not 'alternate_ident' in call_data:
        raise FailPage(message="No alternate page label given")
    if not call_data['alternate_ident']:
        raise FailPage(message="No alternate page label given")
    # Set the page alternate_ident
    try:
        call_data['pchange'] = editresponder.set_alternate_ident(project, pagenumber, pchange, call_data['alternate_ident'])
    except ServerError as e:
        raise FailPage(e.message)
    sd_alternate = SectionData("alternate_ident")
    sd_alternate['textinput', 'set_input_accepted'] = True
    pd.update(sd_alternate)
    call_data['status'] = 'Page set'


def submit_target_ident(skicall):
    "Sets the target ident"

    call_data = skicall.call_data
    pd = call_data['pagedata']

    project = call_data['editedprojname']
    pagenumber = call_data['page_number']
    pchange = call_data['pchange']
    if not 'target_ident' in call_data:
        raise FailPage(message="No target ident given")
    if not call_data['target_ident']:
        raise FailPage(message="No target ident given")
    # Set the page target_ident
    try:
        call_data['pchange'] = editresponder.set_target_ident(project, pagenumber, pchange, call_data['target_ident'])
    except ServerError as e:
        raise FailPage(e.message)
    sd_target = SectionData("target_ident")
    sd_target['textinput', 'set_input_accepted'] = True
    pd.update(sd_target)
    call_data['status'] = 'Target Ident set'


def submit_validate_fail_ident(skicall):
    "Sets the validate fail ident"

    call_data = skicall.call_data
    pd = call_data['pagedata']

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
    pd['validate_fail','set_input_accepted'] = True
    call_data['status'] = 'Validate Fail Ident set'


def submit_fail_ident(skicall):
    "Sets the fail ident"

    call_data = skicall.call_data

    project = call_data['editedprojname']
    pagenumber = call_data['page_number']
    pchange = call_data['pchange']
    if not 'fail_ident' in call_data:
        raise FailPage(message="No fail ident given")
    # Set the page fail_ident
    try:
        call_data['pchange'] = editresponder.set_fail_ident(project, pagenumber, pchange, call_data['fail_ident'])
    except ServerError as e:
        raise FailPage(e.message)
    call_data['status'] = 'Fail Ident set'


def add_allowed_caller(skicall):
    "Adds a new allowed caller"

    call_data = skicall.call_data

    project = call_data['editedprojname']
    pagenumber = call_data['page_number']
    pchange = call_data['pchange']
    if not 'allowed_caller' in call_data:
        raise FailPage(message="No allowed caller given")
    # Set the page allowed caller
    try:
        call_data['pchange'] = editresponder.add_allowed_caller(project, pagenumber, pchange, call_data['allowed_caller'])
    except ServerError as e:
        raise FailPage(e.message)


def delete_allowed_caller(skicall):
    "Deletes an allowed caller"

    call_data = skicall.call_data

    project = call_data['editedprojname']
    pagenumber = call_data['page_number']
    pchange = call_data['pchange']
    if not 'delete_allowed_caller' in call_data:
        raise FailPage(message="No allowed caller given")
    # Delete the page allowed caller
    try:
        call_data['pchange'] = editresponder.delete_allowed_caller(project, pagenumber, pchange, call_data['delete_allowed_caller'])
    except ServerError as e:
        raise FailPage(e.message)


def remove_field(skicall):
    "Deletes a field"

    call_data = skicall.call_data

    project = call_data['editedprojname']
    pagenumber = call_data['page_number']
    pchange = call_data['pchange']
    if not 'remove_field' in call_data:
        raise FailPage(message="No field to remove given")
    # Delete the page field
    try:
        call_data['pchange'] = editresponder.remove_field(project, pagenumber, pchange, call_data['remove_field'])
    except ServerError as e:
        raise FailPage(e.message)


def add_widgfield_value(skicall):
    "Adds a widgfield and value"

    call_data = skicall.call_data
    pd = call_data['pagedata']

    project = call_data['editedprojname']
    pagenumber = call_data['page_number']
    pchange = call_data['pchange']

    try:
        s = call_data['widgfieldval','respondersection','input_text']
        w = call_data['widgfieldval','responderwidget','input_text']
        f = call_data['widgfieldval','responderfield','input_text']
        v = call_data['widgfieldval','responderval','input_text']
    except:
        raise FailPage(message="Invalid data given")

    if (not w) or (not f):
        raise FailPage(message="A widget and field is required")

    if s:
        field = s + ',' + w + ',' + f
    else:
        field = w + ',' + f

    # if value is empty ensure empty values allowed
    if not v:
        # get a ResponderInfo named tuple with information about the responder
        try:
            r_info = editresponder.responder_info(project, pagenumber, pchange)
        except ServerError as e:
            raise FailPage(message=e.message)
        # field options
        f_options = r_info.field_options
        if not f_options['fields']:
            raise FailPage(message="Invalid submission, this responder does not have fields")
        if not f_options['empty_values_allowed']:
            ############  add field values to avoid re-inputting them
            sd_widgfieldval = SectionData('widgfieldval')
            sd_widgfieldval['respondersection','input_text'] = s
            sd_widgfieldval['responderwidget','input_text'] = w
            sd_widgfieldval['responderfield','input_text'] = f
            pd.update(sd_widgfieldval)
            raise FailPage(message="Invalid submission, empty field values are not allowed")
    # Add the field and value
    try:
        call_data['pchange'] = editresponder.add_field_value(project, pagenumber, pchange, field, v)
    except ServerError as e:
        raise FailPage(e.message)


######## will need another add_field_value for non-widgfield fields


def add_field(skicall):
    "Adds a field"

    call_data = skicall.call_data

    project = call_data['editedprojname']
    pagenumber = call_data['page_number']
    pchange = call_data['pchange']
    if not 'field' in call_data:
        raise FailPage(message="No field given")
    if not call_data['field']:
        raise FailPage(message="No field given")
    # Add the field
    try:
        call_data['pchange'] = editresponder.add_field(project, pagenumber, pchange, call_data['field'])
    except ServerError as e:
        raise FailPage(e.message)


def set_single_field(skicall):
    "Sets the field in a responder, which require s single field only"

    call_data = skicall.call_data

    project = call_data['editedprojname']
    pagenumber = call_data['page_number']
    pchange = call_data['pchange']
    if not ('singlefield', 'textinput', 'input_text') in call_data:
        raise FailPage(message="No field given")
    field = call_data['singlefield', 'textinput', 'input_text']
    if not field:
        raise FailPage(message="No field given")
    # Add the field
    try:
        call_data['pchange'] = editresponder.set_single_field(project, pagenumber, pchange, field)
    except ServerError as e:
        raise FailPage(e.message)
    call_data['status'] = 'Fields set'



def delete_submit_list_string(skicall):
    "deletes an indexed string from the submit_list"

    call_data = skicall.call_data

    project = call_data['editedprojname']
    pagenumber = call_data['page_number']
    pchange = call_data['pchange']
    if not 'delete_submit_list_string_index' in call_data:
        raise FailPage(message="No submit_list string given")
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

    project = call_data['editedprojname']
    pagenumber = call_data['page_number']
    pchange = call_data['pchange']
    if not 'submit_list_string' in call_data:
        raise FailPage(message="No submit_list string given")
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
    pd = call_data['pagedata']

    project = call_data['editedprojname']
    pagenumber = call_data['page_number']
    pchange = call_data['pchange']
    try:
        call_data['pchange'], validate_option = editresponder.toggle_validate_option(project, pagenumber, pchange)
    except ServerError as e:
        raise FailPage(e.message)        
    if validate_option:
        pd['set_val_option','button_text'] = "Disable Validation"
        pd['val_status','para_text'] = "Validate received field values : Enabled"
        pd['validate_fail', 'hide'] = False
    else:
        pd['set_val_option','button_text'] = "Enable Validation"
        pd['val_status','para_text'] = "Validate received field values : Disabled"
        pd['validate_fail', 'hide'] = True
    call_data['status'] = 'Validator changed'


def set_submit_option(skicall):
    "Enable or disable the submit option"

    call_data = skicall.call_data

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
    pd = skicall.call_data['pagedata']

    map_height = 1600

    # get information about the responder
    pageinfo = skilift.page_info(project, pagenumber)
    r_info = editresponder.responder_info(project, pagenumber)
    i_info = skilift.item_info(project, pagenumber)
    label_list = i_info.label_list


    sd_responder = SectionData('responder')
    sd_responder['responderid', 'text'] = "Ident: " + str(pagenumber)

    # insert font text style
    pd['textstyle', 'text'] = """
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

    # fill in the box regarding this responder
    if pageinfo.restricted:
        sd_responder['responderaccess', 'text'] = "Restricted access"
    else:
        sd_responder['responderaccess', 'text'] = "Open access"
    if label_list:
        sd_responder['responderlabels', 'text'] = "Label: " + ','.join(label_list)
    else:
        sd_responder['responderlabels', 'show'] = False
    sd_responder['respondertype', 'text'] = "Responder: " + r_info.responder
    sd_responder['responderbrief', 'text'] = pageinfo.brief
    pd.update(sd_responder)


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

    sd_callers = SectionData('callers')
    sd_callers2 = SectionData('callers2')

    if n == 40:
        sd_callers.show = False
        sd_callers2.show = False
    elif not callers2:
        sd_callers['callers', 'lines'] = callers
        sd_callers2.show = False
    else:
        sd_callers['callers', 'lines'] = callers
        sd_callers2['callers', 'lines'] = callers2

    pd.update(sd_callers)
    pd.update(sd_callers2)


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

    sd_fails = SectionData('fails')
    if count:
        fails.append([0, 320, "Plus %s more responders." % (count,)]) 
    if n == 40:
        sd_fails.show = False
    else:
        sd_fails['callers', 'lines'] = fails

    pd.update(sd_fails)


    # Find allowed callers to this responder

    sd_allowed = SectionData('allowed')

    allowed_list = r_info.allowed_callers
    if allowed_list:
        sd_allowed.show = True
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

        sd_allowed['callers', 'lines'] = allowed
    else:
        sd_allowed.show = False

    pd.update(sd_allowed)


    # If the responder has a target, draw a target line on the page

    sd_targetline = SectionData('targetline')

    if r_info.target_ident or r_info.target_ident_required:
        sd_targetline.show = True
    else:
        sd_targetline.show = False

    # normally no output ellipse is shown
    sd_output = SectionData('output')
    sd_output.show = False

    # submit_data information
    sd_submitdata = SectionData('submitdata')

    sd_submitdata_failpage = SectionData('submitdata_failpage')

    if r_info.submit_option or r_info.submit_required:
        sd_submitdata.show = True
        if r_info.submit_list:
            s_list = []
            s = 0
            for item in r_info.submit_list:
                s_list.append([0,s,item])
                s += 20
            sd_submitdata['submitlist','lines'] = s_list
        # show the return value
        if r_info.responder == "ColourSubstitute":
            sd_submitdata['submitdatareturn','text'] = "Returns a dictionary of strings: colour strings"
        elif r_info.responder == "SetCookies":
            sd_submitdata['submitdatareturn','text'] = "Returns an instance of http.cookies.BaseCookie"
        elif r_info.responder == "GetDictionaryDefaults":
            sd_submitdata['submitdatareturn','text'] = "Returns a dictionary with default values"
        elif r_info.responder == "SubmitJSON":
            sd_submitdata['submitdatareturn','text'] = "Returns a dictionary"
            # no target, but include a target line
            sd_targetline.show = True
            # change 'Target Page' to 'Output'
            sd_submitdata['output', 'text'] = "Output"
            # show an output ellipse
            sd_output.show = True
            sd_output['textout', 'text'] = "Send JSON data"
            sd_output['textout', 'x'] = 320
        elif r_info.responder == "SubmitPlainText":
            sd_submitdata['submitdatareturn','text'] = "Returns a string"
            # no target, but include a target line
            sd_targetline.show = True
            # change 'Target Page' to 'Output'
            sd_submitdata['output', 'text'] = "Output"
            # show an output ellipse
            sd_output.show = True
            sd_output['textout', 'text'] = "Send plain text"
            sd_output['textout', 'x'] = 320
        elif r_info.responder == "SubmitCSS":
            sd_submitdata['submitdatareturn','text'] = "Returns a style"
            # no target, but include a target line
            sd_targetline.show = True
            # change 'Target Page' to 'Output'
            sd_submitdata['output', 'text'] = "Output"
            # show an output ellipse
            sd_output.show = True
            sd_output['textout', 'text'] = "Send CSS data"
            sd_output['textout', 'x'] = 320
        elif r_info.responder == "MediaQuery":
            sd_submitdata['submitdatareturn','text'] = "Returns a dictionary of media queries : CSS targets"
            # no target, but include a target line
            sd_targetline.show = True
            # change 'Target Page' to 'Output'
            sd_submitdata['output', 'text'] = "Output"
            # show an output ellipse
            sd_output.show = True
            sd_output['textout', 'text'] = "Update query:target items"
            sd_output['textout', 'x'] = 320
        elif r_info.responder == "SubmitIterator":
            sd_submitdata['submitdatareturn','text'] = "Returns a binary file iterator"
            # no target, but include a target line
            sd_targetline.show = True
            # change 'Target Page' to 'Output'
            sd_submitdata['output', 'text'] = "Output"
            # show an output ellipse
            sd_output.show = True
            sd_output['textout', 'text'] = "Send Binary data"
            sd_output['textout', 'x'] = 320

        # show the fail page
        _show_submit_data_failpage(project, sd_submitdata_failpage, r_info)
    else:
        sd_submitdata.show = False
        sd_submitdata_failpage.show = False


    # The target page
    sd_target = SectionData('target')
    _show_target(project, sd_target, r_info)

    # validation option
    sd_validate = SectionData('validate')
    _show_validate_fail(project, sd_validate, r_info)

    # The alternate option
    sd_alternatebox = SectionData('alternatebox')
    _show_alternate(project, sd_alternatebox, r_info)

    if r_info.responder == 'CaseSwitch':
        _show_caseswitch(project, pd, r_info)
    elif r_info.responder == 'EmptyCallDataGoto':
        _show_emptycalldatagoto(project, pd, r_info)
    elif r_info.responder == 'EmptyGoto':
        _show_emptygoto(project, pd, r_info)
    elif r_info.responder == "MediaQuery":
        _show_mediaquery(project, pd, r_info)

    pd.update(sd_targetline)
    pd.update(sd_output)
    pd.update(sd_submitdata)
    pd.update(sd_submitdata_failpage)
    pd.update(sd_target)
    pd.update(sd_validate)
    pd.update(sd_alternatebox)




def _show_target(project, sd_target, r_info):
    "The responder passes the call to this target"
    if r_info.target_ident or r_info.target_ident_required:
        sd_target.show = True
        if r_info.target_ident:
            targetident = r_info.target_ident
            if isinstance(targetident, str):
                targetident = skilift.ident_from_label(project, targetident)
            if targetident is None:
                sd_target.show = False
            elif isinstance(targetident, str):
                sd_target['responderid', 'text'] = targetident
            elif isinstance(targetident, tuple) and (len(targetident) == 2):
                try:
                    targetinfo = skilift.page_info(*targetident)
                except ServerError:
                    sd_target['responderid', 'text'] = "Unknown Ident: " + targetident[0] + ", " + str(targetident[1])
                else:
                    if targetident[0] == project:
                        sd_target['responderid', 'text'] = "Ident: " + str(targetident[1])
                    else:
                        sd_target['responderid', 'text'] = "Ident: " + targetident[0] + ", " + str(targetident[1])
                    if targetinfo.restricted:
                        sd_target['responderaccess', 'text'] = "Restricted access"
                    else:
                        sd_target['responderaccess', 'text'] = "Open access"
                    if isinstance(r_info.target_ident, str):
                        sd_target['responderlabels', 'text'] = "Targeted from responder as: " + r_info.target_ident
                    else:
                        sd_target['responderlabels', 'text'] = "Targeted from responder as: " + r_info.target_ident[0] + ", " + str(r_info.target_ident[1])
                    sd_target['responderbrief', 'text'] = targetinfo.brief
                    if targetinfo.item_type == "RespondPage":
                        sd_target['respondertype', 'text'] = "Responder: " + targetinfo.responder
                    else:
                        sd_target['respondertype', 'text'] = targetinfo.item_type
    else:
        sd_target.show = False


def _show_submit_data_failpage(project, sd_submitdata_failpage, r_info):
    "The responder calls submit data, which, if it raises a FailPage, calls this"
    sd_submitdata_failpage.show = True
    if r_info.fail_ident:
        failident = r_info.fail_ident
        if isinstance(failident, str):
            failident = skilift.ident_from_label(project, failident)
        if failident is None:
            sd_submitdata_failpage['responderid', 'text'] = "Ident not recognised"
        elif isinstance(failident, str):
            sd_submitdata_failpage['responderid', 'text'] = failident
        elif isinstance(failident, tuple) and (len(failident) == 2):
            try:
                failinfo = skilift.page_info(*failident)
            except ServerError:
                sd_submitdata_failpage['responderid', 'text'] = "Unknown Ident: " + failident[0] + ", " + str(failident[1])
            else:
                if failident[0] == project:
                    sd_submitdata_failpage['responderid', 'text'] = "Ident: " + str(failident[1])
                else:
                    sd_submitdata_failpage['responderid', 'text'] = "Ident: " + failident[0] + ", " + str(failident[1])
                if failinfo.restricted:
                    sd_submitdata_failpage['responderaccess', 'text'] = "Restricted access"
                else:
                    sd_submitdata_failpage['responderaccess', 'text'] = "Open access"
                if isinstance(r_info.fail_ident, str):
                    sd_submitdata_failpage['responderlabels', 'text'] = "Set in responder as: " + r_info.fail_ident
                else:
                    sd_submitdata_failpage['responderlabels', 'text'] = "Set in responder as: " + r_info.fail_ident[0] + ", " + str(r_info.fail_ident[1])
                sd_submitdata_failpage['responderbrief', 'text'] = failinfo.brief
                if failinfo.item_type == "RespondPage":
                    sd_submitdata_failpage['respondertype', 'text'] = "Responder: " + failinfo.responder
                else:
                    sd_submitdata_failpage['respondertype', 'text'] = failinfo.item_type
    else:
        sd_submitdata_failpage['responderid', 'text'] = "Ident not set"


def _show_validate_fail(project, sd_validate, r_info):
    "The responder validates received data, on failure calls this"

    if r_info.validate_option:
        sd_validate.show = True
    else:
        sd_validate.show = False
        return

    if r_info.validate_fail_ident:
        failident = r_info.validate_fail_ident
        if isinstance(failident, str):
            failident = skilift.ident_from_label(project, failident)
        if isinstance(failident, str):
            sd_validate['responderid', 'text'] = failident
        elif isinstance(failident, tuple) and (len(failident) == 2):
            try:
                failinfo = skilift.page_info(*failident)
            except ServerError:
                sd_validate['responderid', 'text'] = "Unknown Ident: " + failident[0] + ", " + str(failident[1])
            else:
                if failident[0] == project:
                    sd_validate['responderid', 'text'] = "Ident: " + str(failident[1])
                else:
                    sd_validate['responderid', 'text'] = "Ident: " + failident[0] + ", " + str(failident[1])
                if failinfo.restricted:
                    sd_validate['responderaccess', 'text'] = "Restricted access"
                else:
                    sd_validate['responderaccess', 'text'] = "Open access"
                if isinstance(r_info.fail_ident, str):
                    sd_validate['responderlabels', 'text'] = "Set in responder as: " + r_info.fail_ident
                else:
                    sd_validate['responderlabels', 'text'] = "Set in responder as: " + r_info.fail_ident[0] + ", " + str(r_info.fail_ident[1])
                sd_validate['responderbrief', 'text'] = failinfo.brief
                if failinfo.item_type == "RespondPage":
                    sd_validate['respondertype', 'text'] = "Responder: " + failinfo.responder
                else:
                    sd_validate['respondertype', 'text'] = failinfo.item_type


def _show_alternate(project, sd_alternatebox, r_info):
    "The alternate page"

    if r_info.alternate_ident:
        sd_alternatebox.show = True
    else:
        sd_alternatebox.show = False
        return

    if r_info.alternate_ident:
        altident = r_info.alternate_ident
        if isinstance(altident, str):
            altident = skilift.ident_from_label(project, altident)
        if isinstance(altident, str):
            sd_alternatebox['responderid', 'text'] = altident
        elif isinstance(altident, tuple) and (len(altident) == 2):
            try:
                altinfo = skilift.page_info(*altident)
            except ServerError:
                sd_alternatebox['responderid', 'text'] = "Unknown Ident: " + altident[0] + ", " + str(altident[1])
            else:
                if altident[0] == project:
                    sd_alternatebox['responderid', 'text'] = "Ident: " + str(altident[1])
                else:
                    sd_alternatebox['responderid', 'text'] = "Ident: " + altident[0] + ", " + str(altident[1])
                if altinfo.restricted:
                    sd_alternatebox['responderaccess', 'text'] = "Restricted access"
                else:
                    sd_alternatebox['responderaccess', 'text'] = "Open access"
                if isinstance(r_info.alternate_ident, str):
                    sd_alternatebox['responderlabels', 'text'] = "Set in responder as: " + r_info.alternate_ident
                else:
                    sd_alternatebox['responderlabels', 'text'] = "Set in responder as: " + r_info.alternate_ident[0] + ", " + str(r_info.alternate_ident[1])
                sd_alternatebox['responderbrief', 'text'] = altinfo.brief
                if altinfo.item_type == "RespondPage":
                    sd_alternatebox['respondertype', 'text'] = "Responder: " + altinfo.responder
                else:
                    sd_alternatebox['respondertype', 'text'] = altinfo.item_type

    if r_info.responder == 'CaseSwitch':
        sd_alternatebox['alttext', 'text'] = "Called if no match found"
    elif r_info.responder == 'EmptyCallDataGoto':
        sd_alternatebox['alttext', 'text'] = "Called if skicall.call_data has key with value"
    elif r_info.responder == 'EmptyGoto':
        sd_alternatebox['alttext', 'text'] = "Called if widgfield is present with a value"


def _show_caseswitch(project, pd, r_info):

    pd['textgroup', 'transform'] = 'translate(500,600)'

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
    pd['textgroup', 'text'] = text_title + table_element


def _caseswitchtable(index, field_values_list):
    y = 100 + 60*index
    return """
<rect height="60" style="fill:white;stroke-width:3;stroke:black" width="600" x="0" y="%s" />
<line x1="180" y1="%s" x2="180" y2="%s" style="stroke-width:3;stroke:black" />
<text x="20" y="%s">%s</text>
<text x="200" y="%s">%s</text>
""" % (y, y, y+60, y+30, field_values_list[index][0],y+30, field_values_list[index][1])


def _show_emptycalldatagoto(project, pd, r_info):
    value = 'UNKNOWN'
    if r_info.single_field:
        value = r_info.single_field
    pd['textgroup', 'transform'] = 'translate(750,700)'
    pd['textgroup', 'text'] = """
<text x="0" y="0">Test skicall.call_data["%s"]</text>
<text x="0" y="60">Called if key not present, or has empty value.</text>
""" % (value,)


def _show_emptygoto(project, pd, r_info):
    value = 'UNKNOWN'
    if r_info.widgfield:
        value = r_info.widgfield
    pd['textgroup', 'transform'] = 'translate(750,700)'
    pd['textgroup', 'text'] = """
<text x="0" y="0">Test widgfield %s</text>
<text x="0" y="60">Called if widgfield not present, or has empty value.</text>
""" % (value,)



def _show_mediaquery(project, pd, r_info):
    pd['textgroup', 'transform'] = 'translate(50,550)'

    if r_info.field_values_list:
        text_title = """<line x1="450" y1="70" x2="450" y2="100" style="stroke-width:3;stroke:black" />
<text x="0" y="90">Query:target</text>"""
    else:
        return
    table_element = ''
    for index, item in enumerate(r_info.field_values_list):
        table_element += _mediaquerytable(index, r_info.field_values_list)
    pd['textgroup', 'text'] = text_title + table_element


def _mediaquerytable(index, field_values_list):
    y = 100 + 60*index
    return """
<rect height="60" style="fill:white;stroke-width:3;stroke:black" width="600" x="0" y="%s" />
<line x1="280" y1="%s" x2="280" y2="%s" style="stroke-width:3;stroke:black" />
<text x="20" y="%s">%s</text>
<text x="300" y="%s">%s</text>
""" % (y, y, y+60, y+30, field_values_list[index][0],y+30, field_values_list[index][1])



