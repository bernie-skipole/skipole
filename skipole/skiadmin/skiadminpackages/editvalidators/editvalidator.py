
"Functions implementing validator editing"

from ... import ServerError, FailPage, ValidateError, GoTo

from ... import skilift
from ....skilift import editwidget, editvalidator

from .. import utils

from ....ski.project_class_definition import SectionData


def _field_name(widget, field_argument):
    "Returns a field name"
    if "set_names" not in widget:
        return field_argument
    name_dict = widget["set_names"]
    if field_argument in name_dict:
        return name_dict[field_argument]
    return field_argument


def retrieve_editvalidator(skicall):
    "Fills in the edit a validator page"

    call_data = skicall.call_data
    pd = call_data['pagedata']
    sd = SectionData("adminhead")

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
    except Exception:
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

    sd["page_head","large_text"] = "Edit : %s on field %s" % (vinfo.validator, field_name)
    pd.update(sd)

    pd['widget_type','para_text'] = "Widget type : %s.%s" % (widgetdescription.modulename, widgetdescription.classname)
    pd['widget_name','para_text'] = "Widget name : %s" % (widget_name,)
    pd['field_type','para_text'] = "Field type : %s" % (field_arg,)
    pd['field_name','para_text'] = "Field name : %s" % (field_name,)
    pd['validator_type','para_text'] = "Validator type : %s.%s" % (vinfo.module_name,vinfo.validator)

    pd['validator_textblock','textblock_ref'] = ".".join(("validators",vinfo.module_name,vinfo.validator))

    # error message
    sd_error_message = utils.formtextinput( "error_message",                              # section alias
                                            "validators.about_error_message",             # textblock
                                            "The error message to be displayed:",         # field label
                                            vinfo.message,                                # input text
                                            action = "e_message",
                                            left_label = "Submit the error message : ")
    pd.update(sd_error_message)


    # error reference message
    sd_error_ref = utils.formtextinput( "error_ref",                                                   # section alias
                                        "validators.about_error_ref",                                  # textblock
                                        "A TextBlock reference string can provide the error message:", # field label
                                        vinfo.message_ref,                                             # input text
                                        action =  "e_message_ref",
                                        left_label = "Submit the reference string : ")
    pd.update(sd_error_ref)

    
    failsectionwidget = vinfo.displaywidget
    if "," in failsectionwidget:
        failsection,failwidget = failsectionwidget.split(",")
        pd['failsection','input_text'] = failsection
        pd['failwidget','input_text'] = failwidget
    else:
        pd['failsection','input_text'] = ""
        pd['failwidget','input_text'] = failsectionwidget

    # list of allowed values
    contents = []
    allowed_vals = vinfo.allowed_values
    for idx, val in enumerate(allowed_vals):
        row = [val, str(idx)]
        contents.append(row)
    if contents:
        pd['allowed_values','contents'] = contents
        pd['allowed_values','show'] = True
    else:
        pd['allowed_values','show'] = False


    # add an allowed value
    sd_add_allowed_value = utils.formtextinput( "add_allowed_value",                     # section alias
                                                "validators.add_allowed_value",          # textblock
                                                "Add an allowed value to list:",         # field label
                                                "",                                      # input text
                                                action = "add_allowed_value",
                                                left_label = "Submit a value : ")
    pd.update(sd_add_allowed_value)

    # Validator arguments
    arg_contents = []
    val_args = vinfo.val_args
    for name, value in val_args.items():
        row = [name, str(value), name]
        arg_contents.append(row)
    if arg_contents:
        arg_contents.sort(key=lambda x: x[0])
        pd['validator_args','contents'] = arg_contents
        pd['validator_args','show'] = True
        pd['description5','show'] = True
    else:
        pd['validator_args','show'] = False
        pd['description5','show'] = False


def set_e_message(skicall):
    "Sets a validator error message"

    call_data = skicall.call_data

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


    if ('error_message','textinput','input_text') not in call_data:
        raise FailPage("Error message not given")

    if call_data['error_message','textinput','input_text']:
        e_message = call_data['error_message','textinput','input_text']
    else:
        e_message = ''

    # get validator index
    try:
        validx = int(call_data['validx'])
    except Exception:
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


def set_e_message_ref(skicall):
    "Sets a validator error message reference"

    call_data = skicall.call_data

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

    if ('error_ref','textinput','input_text') not in call_data:
        raise FailPage("Error message reference not given")

    if call_data['error_ref','textinput','input_text']:
        e_message_ref = call_data['error_ref','textinput','input_text']
    else:
        e_message_ref = ''

    # get validator index
    try:
        validx = int(call_data['validx'])
    except Exception:
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


def set_displaywidget(skicall):
    "Sets a validator displaywidget"

    call_data = skicall.call_data

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

    if ('failwidget', 'input_text') not in call_data:
        raise FailPage("Display widget not given")

    if call_data['failwidget', 'input_text']:
        displaywidget = call_data['failwidget', 'input_text']
    else:
        displaywidget = ''

    if (('failsection', 'input_text') in call_data) and call_data['failsection', 'input_text'] and displaywidget:
        displaywidget = call_data['failsection', 'input_text'] + "," + displaywidget

    # get validator index
    try:
        validx = int(call_data['validx'])
    except Exception:
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


def set_allowed_value(skicall):
    "Adds a validator allowed value"

    call_data = skicall.call_data

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
    except Exception:
        raise FailPage("Invalid validator")

    if ('add_allowed_value','textinput','input_text') not in call_data:
        raise FailPage("Allowed value to be added not given")

    if call_data['add_allowed_value','textinput','input_text']:
        allowed_value = call_data['add_allowed_value','textinput','input_text']
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


def remove_allowed_value(skicall):
    "Removes a validator allowed value"

    call_data = skicall.call_data

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
    except Exception:
        raise FailPage("Invalid validator")

    if 'remove_allowed' not in call_data:
        raise FailPage("Allowed value to be removed not given")

    try:
        idx = int(call_data['remove_allowed'])
    except Exception:
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


def retrieve_arg(skicall):
    "Fills in the edit a validator argument page"

    call_data = skicall.call_data
    pd = call_data['pagedata']
    sd = SectionData("adminhead")

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
    except Exception:
        raise FailPage("Unknown validator to edit")

    if 'arg_name' not in call_data:
        raise FailPage("Validator argument not identified")
    arg_name = call_data['arg_name']

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

    if arg_name not in vinfo.val_args:
        raise FailPage("Validator argument not identified")

    field_name = _field_name(widget, field_arg)

    call_data['extend_nav_buttons'].extend([["back_to_field_edit", "Back to field", True, ''],["back_to_validator", "Back to validator", True, '']])

    # navigator text
    sd["page_head","large_text"] = arg_name
    pd.update(sd)

    pd['widget_type','para_text'] = "Widget type : %s.%s" % (widgetdescription.modulename, widgetdescription.classname)
    pd['widget_name','para_text'] = "Widget name : %s" % (widget_name,)
    pd['field_type','para_text'] = "Field type : %s" % (field_arg,)
    pd['field_name','para_text'] = "Field name : %s" % (field_name,)
    pd['validator_type','para_text'] = "Validator type : %s.%s" % (vinfo.module_name,vinfo.validator)

    # validator argument form
    tblockref = ".".join(("validators",vinfo.module_name,vinfo.validator,arg_name))
    sd_validator_argument = utils.formtextinput("validator_argument",                         # section alias
                                                tblockref,                                    # textblock
                                                "Set the validator parameter:",               # field label
                                                vinfo.val_args[arg_name],                     # input text
                                                action = "validator_parameter",
                                                hidden_field1 = arg_name,
                                                left_label = "Submit the value : ")
    pd.update(sd_validator_argument)



def set_arg_value(skicall):
    "Sets a validator argument value"

    call_data = skicall.call_data

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
    except Exception:
        raise FailPage("Unknown validator to edit")

    if 'arg_name' not in call_data:
        raise FailPage("argument name not given")
    if 'arg_value' not in call_data:
        raise FailPage("argument value not given")

    arg_name = call_data['arg_name']
    arg_value = call_data['arg_value']

    try:
        if section_name:
            call_data['schange'] = editvalidator.set_section_field_validator_argument(project, section_name, call_data['schange'], widget_name, field_arg, validx, arg_name, arg_value)
        else:
            call_data['pchange'] = editvalidator.set_page_field_validator_argument(project, pagenumber, call_data['pchange'], widget_name, field_arg, validx, arg_name, arg_value)
    except ServerError as e:
        raise FailPage(e.message)
    call_data['status'] = "Validator argument changed"


def move_up(skicall):
    "Moves a validator up in a field validator list"

    call_data = skicall.call_data

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
    except Exception:
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


def move_down(skicall):
    "Moves a validator down in a field validator list"

    call_data = skicall.call_data

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
    except Exception:
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


def remove_validator(skicall):
    "Removes a validator"

    call_data = skicall.call_data

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
    except Exception:
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


def retrieve_validator_modules(skicall):
    "Creates a list of validator modules"

    call_data = skicall.call_data
    pd = call_data['pagedata']
    sd = SectionData("adminhead")

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

    sd["page_head","large_text"] = "Add validator to (\"%s\",\"%s\")" % (widget_name, field_name)
    pd.update(sd)

    pd['widget_type','para_text'] = "Widget type : %s.%s" % (widgetdescription.modulename, widgetdescription.classname)
    pd['widget_name','para_text'] = "Widget name : %s" % (widget_name,)
    pd['field_type','para_text'] = "Field type : %s" % (field_arg,)
    pd['field_name','para_text'] = "Field name : %s" % (field_name,)

    call_data['extend_nav_buttons'].append(["back_to_field_edit", "Back to field", True, ''])

    # table of validator modules

    # col 0 is the visible text to place in the link,
    # col 1 is the get field of the link
    # col 2 is the get field of the link
    # col 3 is the reference string of a textblock to appear in the column adjacent to the link
    # col 4 is text to appear if the reference cannot be found in the database
    # col 5 normally empty string, if set to text it will replace the textblock

    validator_modules = editvalidator.validator_modules()

    pd["modulestable","link_table"] = [ [name, name, '', ".".join(('validators', name, 'module')), 'Description not found', ''] for name in validator_modules ]


def retrieve_validator_list(skicall):
    "Creates a list of validators"

    call_data = skicall.call_data
    pd = call_data['pagedata']
    sd = SectionData("adminhead")

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

    sd["page_head","large_text"] = "Add validator to (\"%s\",\"%s\")" % (widget_name, field_name)
    pd.update(sd)

    pd['widget_type','para_text'] = "Widget type : %s.%s" % (widgetdescription.modulename, widgetdescription.classname)
    pd['widget_name','para_text'] = "Widget name : %s" % (widget_name,)
    pd['field_type','para_text'] = "Field type : %s" % (field_arg,)
    pd['field_name','para_text'] = "Field name : %s" % (field_name,)

    call_data['extend_nav_buttons'].extend([["back_to_field_edit", "Back to field", True, ''],["validator_modules", "Modules", True, '']])

    if 'valmodule' in call_data:
        module_name = call_data['valmodule']
    else:
        raise FailPage("Module not identified")

    validator_modules = editvalidator.validator_modules()

    if module_name not in validator_modules:
        raise FailPage("Module not identified")

    pd['moduledesc','textblock_ref'] = 'validators.' + module_name + '.module'

    # table of validators

    # col 0 is the visible text to place in the link,
    # col 1 is the get field of the link
    # col 2 is the get field of the link
    # col 3 is the reference string of a textblock to appear in the column adjacent to the link
    # col 4 is text to appear if the reference cannot be found in the database
    # col 5 normally empty string, if set to text it will replace the textblock

    # tuple of validators in the module
    validators = editvalidator.validators_in_module(module_name)
    pd["validators","link_table"] = [ [name, name, module_name, ".".join(("validators",module_name,name)), 'Description not found', ''] for name in validators ]


def create_validator(skicall):
    "Creates a validator and adds it to the field"

    call_data = skicall.call_data

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

