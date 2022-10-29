

"Functions implementing widget editing"

import re, html, json

from ... import skilift
from ....skilift import fromjson, editsection, editpage, editwidget, versions

from .. import utils
from ... import FailPage, ValidateError, ServerError, GoTo

from ....ski.project_class_definition import SectionData

# a search for anything none-alphanumeric and not an underscore
_AN = re.compile('[^\w]')


def _field_name(widget, field_argument):
    "Returns a field name"
    if "set_names" not in widget:
        return field_argument
    name_dict = widget["set_names"]
    if field_argument in name_dict:
        return name_dict[field_argument]
    return field_argument


def _field_value(widget, field_argument):
    "Returns value,string value"
    value = widget["fields"][field_argument]
    if value is None:
        field_value = ''
    elif isinstance(value, list):
        if value:
            field_value = ','.join(str(val) for val in value)
        else:
            field_value = ''
    else:
        field_value = str(value)
    return value, field_value


def _field_ref(widgetdescription, field_argument):
    "Returns a field textblock reference string"
    if field_argument == 'show':
        return 'widgets.show'
    elif field_argument == 'widget_class':
        return 'widgets.widget_class'
    elif field_argument == 'widget_style':
        return 'widgets.widget_style'
    elif field_argument == 'show_error':
        return 'widgets.show_error'
    elif field_argument == 'clear_error':
        return 'widgets.clear_error'
    else:
        return ".".join(("widgets", widgetdescription.modulename, widgetdescription.classname, field_argument))


def retrieve_widget(skicall):
    "Fills in the edit a widget page"

    call_data = skicall.call_data
    pd = call_data['pagedata']
    sd = SectionData("adminhead")

    # get the widget name
    if ("left_nav","navbuttons","nav_links") in call_data:
        # should be submitted as widgetname from left navigation links
        widget_name = call_data["left_nav","navbuttons","nav_links"]
    elif 'widget_name' in call_data:
        widget_name = call_data['widget_name']
    elif 'part_tuple' in call_data:
        # called from dom table, via responder that finds what is being edited
        # and has set it into part_tuple
        part_tuple = call_data['part_tuple']
        widget_name = part_tuple.name
    else:
        raise FailPage(message="Invalid widget")

    if not widget_name:
        raise FailPage(message="Invalid widget")

    # and this is the widget to be edited, it is now set into session data
    call_data['widget_name'] = widget_name

    # Fill in header
    sd["page_head","large_text"] = "Widget " + widget_name

    project = call_data['editedprojname']

    section_name = None
    pagenumber = None
    if 'section_name' in call_data:
        section_name = call_data['section_name']
    elif 'page_number' in call_data:
        pagenumber = call_data['page_number']
    else:
        raise FailPage(message="No section or page given")

    try:
        if section_name:
            widgetdescription = editwidget.section_widget_description(project, section_name, call_data['schange'], widget_name)
            widget =  editwidget.section_widget(project, section_name, call_data['schange'], widget_name)
        else:
            widgetdescription = editwidget.page_widget_description(project, pagenumber, call_data['pchange'], widget_name)
            widget = editwidget.page_widget(project, pagenumber, call_data['pchange'], widget_name)
    except ServerError as e:
        raise FailPage(e.message)

    # set map link to link to examples
    if skicall.proj_data['examples']:
        sd["map", "show"] = True
        sd["map", "button_text"] = "Example"
        sd["map", "force_ident"] = False
        sd["map", "link_ident"] = skicall.proj_data['examples'] + widgetdescription.modulename +"/" + widgetdescription.classname

    pd.update(sd)
    

    pd['widget_type','para_text'] = "This widget is of type %s.%s." % (widgetdescription.modulename, widgetdescription.classname)
    pd['widget_textblock','textblock_ref'] = ".".join(("widgets", widgetdescription.modulename, widgetdescription.classname))
    pd['widget_name','input_text'] = widget_name
    pd['widget_brief','input_text'] = widgetdescription.brief

    # widgetdescription.fields_single is a list of namedtuples, each inner namedtuple representing a field
    # with items ['field_arg', 'field_type', 'valdt', 'jsonset', 'cssclass', 'cssstyle']

    args = widgetdescription.fields_single
    arg_list = widgetdescription.fields_list
    arg_table = widgetdescription.fields_table 
    arg_dict = widgetdescription.fields_dictionary

    if arg_list or arg_table or arg_dict:
        pd['args_multi','show'] = True
    else:
        pd['args_multi','show'] = False


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
            name = _field_name(widget, arg.field_arg)
            ref = _field_ref(widgetdescription, arg.field_arg)
            if arg.valdt:   
                name = "* " + name
                args_valdt = True
            # field value
            value,field_value = _field_value(widget, arg.field_arg)
            if len(field_value) > 20:
                field_value = field_value[:18]
                field_value += '...'
            arg_row = [ name, arg.field_arg, '',field_value, ref, 'No description for %s' % (ref,), '']
            args_content.append(arg_row)
        pd['args','link_table'] = args_content
    else:
        pd['args','show'] = False
        pd['args_description','show'] = False


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
            name = _field_name(widget, arg.field_arg)
            ref = _field_ref(widgetdescription, arg.field_arg)
            if arg.valdt:
                name = "* " + name
                args_valdt = True
            arg_row = [ name, arg.field_arg, '', ref, 'No description for %s' % (ref,), '']
            arg_list_content.append(arg_row)
        pd['arg_list','link_table'] = arg_list_content
    else:
        pd['arg_list','show'] = False
        pd['arg_list_description','show'] = False

    arg_table_content = []
    if arg_table:
        for arg in arg_table:
            name = _field_name(widget, arg.field_arg)
            ref = _field_ref(widgetdescription, arg.field_arg)
            if arg.valdt:
                name = "* " + name
                args_valdt = True
            arg_row = [ name, arg.field_arg, '', ref, 'No description for %s' % (ref,), '']
            arg_table_content.append(arg_row)
        pd['arg_table','link_table'] = arg_table_content
    else:
        pd['arg_table','show'] = False
        pd['arg_table_description','show'] = False

    arg_dict_content = []
    if arg_dict:
        for arg in arg_dict:
            name = _field_name(widget, arg.field_arg)
            ref = _field_ref(widgetdescription, arg.field_arg)
            if arg.valdt:
                name = "* " + name
                args_valdt = True
            arg_row = [ name, arg.field_arg, '', ref, 'No description for %s' % (ref,), '']
            arg_dict_content.append(arg_row)
        pd['arg_dict','link_table'] = arg_dict_content
    else:
        pd['arg_dict','show'] = False
        pd['arg_dict_description','show'] = False

    pd['args_valdt','show'] = args_valdt

    # display the widget html
    pd['widget_code','pre_text'] = widgetdescription.illustration

    if widgetdescription.containers:
        pd['containerdesc','show'] = True

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


def set_widget_params(skicall):
    "Sets widget name and brief"

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

    new_name = None
    brief = None

    if 'new_widget_name' in call_data:
        new_name = call_data['new_widget_name']
    elif 'widget_brief' in call_data:
        brief = call_data['widget_brief']
    else:
        raise FailPage(message="No new name or brief given")
    
    try:
        if section_name:
            if new_name:
                call_data['schange'] = editwidget.rename_section_widget(project, section_name, call_data['schange'], widget_name, new_name)
                call_data['status'] = "Widget name changed"
                call_data['widget_name'] = new_name
            else:
                call_data['schange'] = editwidget.new_brief_in_section_widget(project, section_name, call_data['schange'], widget_name, brief)
                call_data['status'] = "Widget brief changed"
        else:
            if new_name:
                call_data['pchange'] = editwidget.rename_page_widget(project, pagenumber, call_data['pchange'], widget_name, new_name)
                call_data['status'] = "Widget name changed"
                call_data['widget_name'] = new_name
            else:
                call_data['pchange'] = editwidget.new_brief_in_page_widget(project, pagenumber, call_data['pchange'], widget_name, brief)
                call_data['status'] = "Widget brief changed"
    except ServerError as e:
        raise FailPage(e.message)


def retrieve_editfield(skicall):
    "Fills in the edit a widget field page"

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

    try:
        if section_name:
            widgetdescription = editwidget.section_widget_description(project, section_name, call_data['schange'], widget_name)
            widget =  editwidget.section_widget(project, section_name, call_data['schange'], widget_name)
        else:
            widgetdescription = editwidget.page_widget_description(project, pagenumber, call_data['pchange'], widget_name)
            widget = editwidget.page_widget(project, pagenumber, call_data['pchange'], widget_name)
    except ServerError as e:
        raise FailPage(e.message)

    pd['widget_type','para_text'] = "Widget type : %s.%s" % (widgetdescription.modulename, widgetdescription.classname)
    pd['widget_name','para_text'] = "Widget name : %s" % (widget_name,)
    pd['field_type','para_text'] = "Field type : %s" % (field_arg,)

    # widgetdescription.fields_single is a list of namedtuples, each inner namedtuple representing a field
    # with items ['field_arg', 'field_type', 'valdt', 'jsonset', 'cssclass', 'cssstyle']

    # create dictionaries of {field_arg : namedtuples }
    fields_single = { arg.field_arg:arg for arg in widgetdescription.fields_single }
    fields_list = { arg.field_arg:arg for arg in widgetdescription.fields_list }
    fields_table = { arg.field_arg:arg for arg in widgetdescription.fields_table }
    fields_dictionary = { arg.field_arg:arg for arg in widgetdescription.fields_dictionary }

    if field_arg in fields_single:
        field_datalist = fields_single[field_arg]
    elif field_arg in fields_list:
        field_datalist = fields_list[field_arg]
    elif field_arg in fields_table:
        field_datalist = fields_table[field_arg]
    elif field_arg in fields_dictionary:
        field_datalist = fields_dictionary[field_arg]
    else:
        raise FailPage("Field not identified")

    if field_datalist.jsonset:
        pd['json_enabled','para_text'] = "JSON Enabled : Yes"
    else:
        pd['json_enabled','para_text'] = "JSON Enabled : No"

    if field_arg in fields_single:
        if field_datalist.cssclass or field_datalist.cssstyle:
            default_value = skilift.fromjson.get_widget_default_field_value(project, widgetdescription.modulename, widgetdescription.classname, field_arg)
            if default_value:
                pd['field_default','para_text'] = "Default value : " + default_value
                pd['field_default','show'] = True

    field_name = _field_name(widget, field_arg)
    sd["page_head","large_text"] = "(\'%s\',\'%s\')" % (widget_name, field_name)
    pd.update(sd)
    pd['show_field_name','para_text'] = "Field name : %s" % (field_name,)

    value, field_value = _field_value(widget, field_arg)

    # show the textblock description with .full, or if it doesnt exist, without the .full
    ref = _field_ref(widgetdescription, field_arg)

    full_textref = ref + '.full'   # the field reference string
    adminaccesstextblocks = skilift.get_accesstextblocks(skicall.project)

    if adminaccesstextblocks.textref_exists(full_textref):
        pd['widget_field_textblock','textblock_ref'] = full_textref
    else:
        pd['widget_field_textblock','textblock_ref'] = ref
    pd['field_name','input_text'] = field_name

    replace_strings = [widget_name+'\",\"'+field_name]

    if field_arg in fields_single:
        if field_datalist.field_type == 'boolean':
            pd["field_submit",'show'] = True
            pd["boolean_field_value", "radio_checked"] = value
        else:
            pd["field_value",'show'] = True
            pd["field_value",'input_text'] = field_value
        if field_datalist.cssclass or field_datalist.cssstyle:
            # add button to set given css class or style to defaults.json
            pd["css_default_desc",'show'] = True
            pd["set_field_default",'show'] = True
        else:
            pd["css_default_desc",'show'] = False
            pd["set_field_default",'show'] = False

        pd["show_field_value",'show'] = True
        pd["show_field_value",'para_text'] = "Field value : %s" % (field_value,)
        pd["widget_args_desc",'show'] = True
        pd["widget_args_desc",'replace_strings'] = replace_strings
    elif field_arg in fields_list:
        pd["widget_arg_list_desc",'show'] = True
        pd["widget_arg_list_desc",'replace_strings'] = replace_strings
        pd["css_default_desc",'show'] = False
        pd["set_field_default",'show'] = False
    elif field_arg in fields_table:
        pd["widget_arg_table_desc",'show'] = True
        pd["widget_arg_table_desc",'replace_strings'] = replace_strings
        pd["css_default_desc",'show'] = False
        pd["set_field_default",'show'] = False
    elif field_arg in fields_dictionary:
        pd["widget_arg_dict_desc",'show'] = True
        pd["widget_arg_dict_desc",'replace_strings'] = replace_strings
        pd["css_default_desc",'show'] = False
        pd["set_field_default",'show'] = False

    # Show validators
    if field_datalist.valdt:
        pd["validators_desc",'show'] = True
        pd["validators_desc2",'show'] = True
        pd["add_validator",'show'] = True
        # create the contents for the validator_table
        contents = []
        if ("validators" in widget) and (field_arg in widget["validators"]):
            val_list = widget["validators"][field_arg]
            pd["validator_table","show"] = True
            max_validator_index = len(val_list) - 1
            for index,validator in enumerate(val_list):
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
                contents.append([validator['class'], table_pos, table_pos, table_pos, table_pos, True, up, down, True])
            pd["validator_table","contents"] = contents

    # set field_arg into session call_data
    call_data['field_arg'] = field_arg

    if 'validx' in call_data:
        del call_data['validx']


def set_field_name(skicall):
    "Sets a widget field name"

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

    if 'field_name' in call_data:
        field_name = call_data['field_name']
    else:
        raise FailPage("New field name not identified")

    try:
        if section_name:
            call_data['schange'] = editwidget.set_widget_field_name_in_section(project, section_name, call_data['schange'], widget_name, field_arg, field_name)
        else:
            call_data['pchange'] = editwidget.set_widget_field_name_in_page(project, pagenumber, call_data['pchange'], widget_name, field_arg, field_name)
    except ServerError as e:
        raise FailPage(e.message)

    call_data['status'] = "Field name changed"


def set_field_value(skicall):
    "Sets a widget field value"

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

    if 'field_value' in call_data:
        field_value = call_data['field_value']
    else:
        raise FailPage("New field value not identified")

    try:
        if section_name:
            call_data['schange'] = editwidget.set_widget_field_value_in_section(project, section_name, call_data['schange'], widget_name, field_arg, field_value)
        else:
            call_data['pchange'] = editwidget.set_widget_field_value_in_page(project, pagenumber, call_data['pchange'], widget_name, field_arg, field_value)
    except ServerError as e:
        raise FailPage(e.message)

    call_data['status'] = "Field value changed"


def set_field_default(skicall):
    "Sets a widget field default value"

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

    try:
        if section_name:
            widgetdescription = editwidget.section_widget_description(project, section_name, call_data['schange'], widget_name)
            widget =  editwidget.section_widget(project, section_name, call_data['schange'], widget_name)
        else:
            widgetdescription = editwidget.page_widget_description(project, pagenumber, call_data['pchange'], widget_name)
            widget = editwidget.page_widget(project, pagenumber, call_data['pchange'], widget_name)
    except ServerError as e:
        raise FailPage(e.message)

    fields_single = { arg.field_arg:arg for arg in widgetdescription.fields_single }
    if field_arg not in fields_single:
        raise FailPage("Cannot set a default value on this field")
    field_info = fields_single[field_arg]

    value, str_value = _field_value(widget, field_arg)

    if field_info.cssclass or field_info.cssstyle:
        # set the default value
        result = fromjson.save_widget_default_field_value(project,
                                                          widgetdescription.modulename,
                                                          widgetdescription.classname,
                                                          field_arg,
                                                          str_value)
        if result:
            if str_value:
                call_data['status'] = "Field default value set to %s" % (str_value,)
            else:
                call_data['status'] = "Field default value removed"
            return

    raise FailPage("Unable to set default")



def retrieve_container(skicall):
    "Edits a widget container"

    call_data = skicall.call_data
    pd = call_data['pagedata']
    sd_adminhead = SectionData("adminhead")
    sd_widgetinserts = SectionData("widgetinserts")

    # remove any unwanted fields from session call_data
    if 'location' in call_data:
        del call_data['location']
    if 'part' in call_data:
        del call_data['part']

    # get data
    if ("left_nav","navbuttons","nav_links") in call_data:
        # should be submitted as widgetname-containernumber
        widget_container = call_data["left_nav","navbuttons","nav_links"].split("-")
        if len(widget_container) != 2:
            raise FailPage(message="Invalid container")
        widget_name = widget_container[0]
        try:
            container = int(widget_container[1])
        except Exception:
            raise FailPage(message="Invalid container")
    elif ('widget_name' in call_data) and ('container' in call_data):
        widget_name = call_data['widget_name']
        container = call_data['container']
    else:
        raise FailPage(message="Invalid container")

    # and this is the container to be edited, it is now set into session data
    call_data['widget_name'] = widget_name
    call_data['container'] = container

    project = call_data['editedprojname']

    section_name = None
    pagenumber = None
    if 'section_name' in call_data:
        section_name = call_data['section_name']
    elif 'page_number' in call_data:
        pagenumber = call_data['page_number']
    else:
        raise FailPage(message="No section or page given")

    try:
        if section_name:
            widgetdescription = editwidget.section_widget_description(project, section_name, call_data['schange'], widget_name)
            containerinfo = editwidget.container_in_section(project, section_name, call_data['schange'], widget_name, container)
            # going into a section, so cannot add sections
            sd_widgetinserts["insert_section", "show"] = False
        else:
            widgetdescription = editwidget.page_widget_description(project, pagenumber, call_data['pchange'], widget_name)
            containerinfo = editwidget.container_in_page(project, pagenumber, call_data['pchange'], widget_name, container)
            sd_widgetinserts["insert_section", "show"] = True
    except ServerError as e:
        raise FailPage(e.message)
    pd.update(sd_widgetinserts)

    # containerinfo is a namedtuple ('container', 'empty')

    call_data['widgetdescription'] = widgetdescription

    if containerinfo.empty:
        # empty container
        # set location, where item is to be inserted
        call_data['location'] = (widget_name, container, ())
        # go to page showing empty contaier
        raise GoTo(target = 54600, clear_submitted=True)

    # Fill in header
    sd_adminhead["page_head","large_text"] = "Widget " + widget_name + " container: " + str(container)
    pd.update(sd_adminhead)

    # so header text and navigation done, now continue with the page contents
    pd['container_description','textblock_ref'] = ".".join(("widgets",widgetdescription.modulename, widgetdescription.classname, "container" + str(container)))

    pd['further_description','para_text'] = "Choose an item to edit."
    # fill in the table
    call_data['location_string'] = widget_name
    retrieve_container_dom(skicall)

    # and do show the download button
    pd['download_description', 'show'] = True
    pd['containerdownload', 'show'] = True


def empty_container(skicall):
    "Fills in empty_container page"
    call_data = skicall.call_data
    pd = call_data['pagedata']
    sd = SectionData("adminhead")

    # location is (widget_name, container, ())
    location = call_data['location']
    widgetdescription = call_data['widgetdescription']
    sd["page_head","large_text"] = "Widget " + location[0] + " container: " + str(location[1])
    pd.update(sd)

    pd['container_description','textblock_ref'] = ".".join(("widgets",widgetdescription.modulename, widgetdescription.classname, "container" + str(location[1])))


def retrieve_container_dom(skicall):
    "this call fills in the container dom table"

    call_data = skicall.call_data
    pd = call_data['pagedata']
    sd = SectionData("editdom")

    project = call_data['editedprojname']

    pagenumber = None
    section_name = None

    if "page_number" in call_data:
        pagenumber = call_data["page_number"]
    elif "section_name" in call_data:
        section_name = call_data["section_name"]
    else:
        raise FailPage(message = "No page or section given")

    # location_string is the widget name

    if 'location_string' in call_data:
        location_string = call_data['location_string']
    elif 'widget_name' in call_data:
        location_string = call_data['widget_name']
    else:
        raise FailPage(message = "widget_name not in call_data")

    if 'container' not in call_data:
        raise FailPage(message = "container not in call_data")
    container = call_data["container"]

    try:
        domcontents, dragrows, droprows = _container_domcontents(project, pagenumber, section_name, location_string, container)
    except ServerError as e:
        raise FailPage(message=e.message)

    # widget editdom,domtable is populated with fields

    #    dragrows: A two element list for every row in the table, could be empty if no drag operation
    #              0 - True if draggable, False if not
    #              1 - If 0 is True, this is data sent with the call wnen a row is dropped
    #    droprows: A two element list for every row in the table, could be empty if no drop operation
    #              0 - True if droppable, False if not
    #              1 - text to send with the call when a row is dropped here
    #    dropident: ident or label of target, called when a drop occurs which returns a JSON page

    #    cols: A three element list for every column in the table, must be given with empty values if no links
    #              0 - target HTML page link ident of buttons in each column, if col1 not present or no javascript
    #              1 - target JSON page link ident of buttons in each column,
    #              2 - session storage key 'ski_part'

    #    contents: A list for every element in the table, should be row*col lists
    #               0 - text string, either text to display or button text
    #               1 - A 'style' string set on the td cell, if empty string, no style applied
    #               2 - Is button? If False only text will be shown, not a button, button class will not be applied
    #                       If True a link to link_ident/json_ident will be set with button_class applied to it
    #               3 - The get field value of the button link, empty string if no get field

    # create the table

    sd['domtable', 'contents']  = domcontents
    sd['domtable', 'dragrows']  = dragrows
    sd['domtable', 'droprows']  = droprows

    # for each column: html link, JSON link, storage key
    sd['domtable', 'cols']  =  [  ['','',''],                                                 # tag name, no link
                                  ['','',''],                                                 # brief, no link
                                  ['no_javascript','move_up_in_container_dom',''],            # up arrow
                                  ['no_javascript','move_up_right_in_container_dom',''],      # up right
                                  ['no_javascript','move_down_in_container_dom',''],          # down
                                  ['no_javascript','move_down_right_in_container_dom',''],    # down right
                                  ['edit_container_dom','',''],                               # edit, html only
                                  ['no_javascript',44205,''],                                 # insert/append
                                  ['no_javascript',44580,''],                                 # copy
                                  ['no_javascript',44590,'ski_part'],                         # paste
                                  ['no_javascript','cut_container_dom',''],                   # cut
                                  ['no_javascript','delete_container_dom','']                 # delete
                               ]

    sd['domtable', 'dropident'] = 'move_in_container_dom'
    pd.update(sd)



def _container_domcontents(project, pagenumber, section_name, location_string, container):
    "Return the info for domtable contents"

    parttext, partdict = fromjson.container_outline(project, pagenumber, section_name, location_string, container)

    # create first row of the table

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
                   ['', '', False, '' ],
                   ['', '', False, '' ],
                   ['', '', False, '' ],
                   ['', '', False, '' ]
                ]
    # add further items to domcontents
    part_string_list = []

    # containers flags those widgets with containers, each item is a list of tuples, each tuple being (rownumber, number of containers)
    containers = []

    part_loc = location_string + '-' + str(container)

    if 'parts' not in partdict:
        rows = 1
        containers = []
        container_rows = []
    else:
        rows, containers = _domtree(partdict, part_loc, domcontents, part_string_list)
        container_rows = list(zip(*containers))
        # gives list of two elements [rowlist, container number list]

    # insert containers into the table
    _insert_containers(domcontents, containers)


    # for every row in the table
    dragrows = [[ False, '']]
    droprows = [[ True, part_loc]]

    # for each row
    if rows>1:
        for row in range(0, rows-1):
            dragrows.append( [ True, part_string_list[row]] )
            droprows.append( [ True, part_string_list[row]] )
            if container_rows:
                row2 = row+2
                if row2 in container_rows[0]:
                    number_of_containers = container_rows[1][container_rows[0].index(row2)]
                    for c in range(number_of_containers):
                        dragrows.append( [ False, ''] )
                        droprows.append( [ False, ''] )
    
    return domcontents, dragrows, droprows


def copy_container(skicall):
    "Gets container part and return it in page_data['localStorage'] with key ski_part for browser session storage"
    call_data = skicall.call_data
    pd = call_data['pagedata']
    project = call_data['editedprojname']
    pagenumber = None
    section_name = None

    if "page_number" in call_data:
        pagenumber = call_data["page_number"]
    elif "section_name" in call_data:
        section_name = call_data["section_name"]
    else:
        raise FailPage(message = "No page or section given")
    if ('editdom', 'domtable', 'contents') not in call_data:
        raise FailPage(message = "item missing")

    part = call_data['editdom', 'domtable', 'contents']

    # so part is widget_name, container with location string of integers

    # create location which is a tuple or list consisting of three items:
    # a string of widget name
    # a container integer
    # a tuple or list of location integers
    location_list = part.split('-')
    # first item should be a string, rest integers
    if len(location_list) < 3:
        raise FailPage("Item has not been recognised")

    try:
        widget_name = location_list[0]
        container = int(location_list[1])
        location_integers = [ int(i) for i in location_list[2:]]
    except Exception:
        raise FailPage("Item has not been recognised")

    # location is a tuple of widget_name, container, tuple of location integers
    location = (widget_name, container, location_integers)

    # get a json string dump of the item outline, however change any Sections to Parts
    itempart, itemdict = fromjson.item_outline(project, pagenumber, section_name, location)
    if itempart == 'Section':
        jsonstring = json.dumps(['Part',itemdict], indent=0, separators=(',', ':'))
    else:
        jsonstring = json.dumps([itempart,itemdict], indent=0, separators=(',', ':'))
    pd.localStorage = {'ski_part':jsonstring}
    call_data['status'] = 'Item copied, and can now be pasted.'


def paste_container(skicall):
    "Gets submitted json string and inserts it"
    call_data = skicall.call_data
    pd = call_data['pagedata']
    sd = SectionData("editdom")

    project = call_data['editedprojname']
    pagenumber = None
    section_name = None

    if "page_number" in call_data:
        pagenumber = call_data["page_number"]
    elif "section_name" in call_data:
        section_name = call_data["section_name"]
    else:
        raise FailPage(message = "No page or section given")
    if ('editdom', 'domtable', 'contents') not in call_data:
        raise FailPage(message = "item missing")
    part = call_data['editdom', 'domtable', 'contents']
    if ('editdom', 'domtable', 'cols') not in call_data:
        raise FailPage(message = "item to paste missing")
    json_string = call_data['editdom', 'domtable', 'cols']

    # so part is widget_name, container with location string of integers

    # create location which is a tuple or list consisting of three items:
    # a string of widget name
    # a container integer
    # a tuple or list of location integers
    location_list = part.split('-')
    # first item should be a string, rest integers
    if len(location_list) < 3:
        raise FailPage("Item has not been recognised")

    try:
        widget_name = location_list[0]
        container = int(location_list[1])
        location_integers = [ int(i) for i in location_list[2:]]
    except Exception:
        raise FailPage("Item has not been recognised")

    # location is a tuple of widget_name, container, tuple of location integers
    location = (widget_name, container, location_integers)

    if section_name:
        call_data['schange'] = editsection.create_item_in_section(project, section_name, call_data['schange'], location, json_string)
    else:
        call_data['pchange'] = editpage.create_item_in_page(project, pagenumber, call_data['pchange'], location, json_string)

    domcontents, dragrows, droprows = _container_domcontents(project, pagenumber, section_name, widget_name, container)
    sd['domtable', 'dragrows']  = dragrows
    sd['domtable', 'droprows']  = droprows
    sd['domtable', 'contents']  = domcontents
    pd.update(sd)



def downloadcontainer(skicall):
    "Gets container, and returns a json dictionary, this will be sent as an octet file to be downloaded"

    call_data = skicall.call_data
    pd = call_data['pagedata']
    project = call_data['editedprojname']

    pagenumber = None
    section_name = None

    if "page_number" in call_data:
        pagenumber = call_data["page_number"]
    elif "section_name" in call_data:
        section_name = call_data["section_name"]
    else:
        raise FailPage(message = "No page or section given")

    if 'widget_name' in call_data:
        widget_name = call_data['widget_name']
    else:
        raise FailPage(message = "widget_name not in call_data")

    if 'container' not in call_data:
        raise FailPage(message = "container not in call_data")
    container = call_data["container"]

    parttext, part_dict = fromjson.container_outline(project, pagenumber, section_name, widget_name, container)
    # set contents into a div
    part_dict["hide_if_empty"] = False
    part_dict.move_to_end("hide_if_empty", last=False)
    part_dict["show"] = True
    part_dict.move_to_end("show", last=False)
    part_dict["brief"] = "From widget %s container %s" % (widget_name, container)
    part_dict.move_to_end("brief", last=False)
    part_dict["tag_name"] = "div"
    part_dict.move_to_end("tag_name", last=False)
    # set version and skipole as the first two items in the dictionary
    versions_tuple = versions(project)
    part_dict["skipole"] = versions_tuple.skipole
    part_dict.move_to_end('skipole', last=False)
    part_dict["version"] = versions_tuple.project
    part_dict.move_to_end('version', last=False)
    jsonstring = json.dumps(part_dict, indent=4, separators=(',', ':'))
    line_list = []
    n = 0
    for line in jsonstring.splitlines(True):
        binline = line.encode('utf-8')
        n += len(binline)
        line_list.append(binline)
    pd.mimetype = 'application/octet-stream'
    pd.content_length = str(n)
    return line_list


def back_to_parent_container(skicall):
    "Sets call_data['widget_name'] to parent_widget and call_data['container'] to parent_container"

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

    try:
        if section_name:
            widgetdescription = editwidget.section_widget_description(project, section_name, call_data['schange'], widget_name)
        else:
            widgetdescription = editwidget.page_widget_description(project, pagenumber, call_data['pchange'], widget_name)
    except ServerError as e:
        raise FailPage(e.message)

    utils.clear_call_data(call_data)

    if section_name:
        call_data['section_name'] = section_name
    else:
        call_data['page_number'] = pagenumber

    call_data['widget_name'] = widgetdescription.parent_widget
    call_data['container'] = widgetdescription.parent_container



def edit_container_dom(skicall):
    "Called by domtable to edit an item in a container"

    call_data = skicall.call_data

    project = call_data['editedprojname']
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

    if '--' in part:
        # part is widgetname--containernumber
        splitpart = part.split('--')
        call_data['widget_name'] = splitpart[0]    # the widget name
        call_data['container'] = int(splitpart[1]) # the container number
        raise GoTo(target = 54710, clear_submitted=True)

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
    except Exception:
        raise FailPage("Item to edit has not been recognised")


    part_tuple = skilift.part_info(project, pagenumber, section_name, [widget_name, container, location_integers])
    if part_tuple is None:
        raise FailPage("Item to edit has not been recognised")

    if part_tuple.name:
        # item to edit is a widget
        call_data['part_tuple'] = part_tuple
        raise GoTo(target = 54006, clear_submitted=True)
    if part_tuple.part_type == "Part":
        # edit the html part
        call_data['part_tuple'] = part_tuple
        raise GoTo(target = 53007, clear_submitted=True)
    if part_tuple.part_type == "ClosedPart":
        # edit the html closed part
        call_data['part_tuple'] = part_tuple
        raise GoTo(target = 53007, clear_submitted=True)
    if part_tuple.part_type == "HTMLSymbol":
        # edit the symbol
        call_data['part_tuple'] = part_tuple
        raise GoTo(target = 51107, clear_submitted=True)
    if part_tuple.part_type == "str":
        # edit the text
        call_data['part_tuple'] = part_tuple
        raise GoTo(target = 51017, clear_submitted=True)
    if part_tuple.part_type == "TextBlock":
        # edit the TextBlock
        call_data['part_tuple'] = part_tuple
        raise GoTo(target = 52017, clear_submitted=True)
    if part_tuple.part_type == "Comment":
        # edit the Comment
        call_data['part_tuple'] = part_tuple
        raise GoTo(target = 51207, clear_submitted=True)
    if (not section_name) and (part_tuple.part_type == "SectionPlaceHolder"):
        # edit the SectionPlaceHolder
        call_data['part_tuple'] = part_tuple
        raise GoTo(target = 55007, clear_submitted=True)

    raise FailPage("Item to edit has not been recognised")


def cut_container_dom(skicall):
    "Called by domtable to cut an item in a container"

    call_data = skicall.call_data
    pd = call_data['pagedata']
    sd = SectionData("editdom")

    project = call_data['editedprojname']
    pagenumber = None
    section_name = None

    if "page_number" in call_data:
        pagenumber = call_data["page_number"]
    elif "section_name" in call_data:
        section_name = call_data["section_name"]
    else:
        raise FailPage(message = "No page or section given")
    if ('editdom', 'domtable', 'contents') not in call_data:
        raise FailPage(message = "item to remove missing")

    part = call_data['editdom', 'domtable', 'contents']

    # so part is widget_name, container with location string of integers

    # create location which is a tuple or list consisting of three items:
    # a string of widget name
    # a container integer
    # a tuple or list of location integers
    location_list = part.split('-')
    # first item should be a string, rest integers
    if len(location_list) < 3:
        raise FailPage("Item to remove has not been recognised")

    try:
        widget_name = location_list[0]
        container = int(location_list[1])
        location_integers = [ int(i) for i in location_list[2:]]
    except Exception:
        raise FailPage("Item to remove has not been recognised")

    # location is a tuple of widget_name, container, tuple of location integers
    location = (widget_name, container, location_integers)

    part_tuple = skilift.part_info(project, pagenumber, section_name, location)
    if part_tuple is None:
        raise FailPage("Item to remove has not been recognised")

    # prior to deleting, take a copy
    # get a json string dump of the item outline, however change any Sections to Parts
    itempart, itemdict = fromjson.item_outline(project, pagenumber, section_name, location)
    if itempart == 'Section':
        jsonstring = json.dumps(['Part',itemdict], indent=0, separators=(',', ':'))
    else:
        jsonstring = json.dumps([itempart,itemdict], indent=0, separators=(',', ':'))
    pd.localStorage = {'ski_part':jsonstring}

    # remove the item using functions from skilift.editsection and skilift.editpage
    if pagenumber is None:
        # remove the item from a section
        try:
            call_data['schange'] = editsection.del_location(project, section_name, call_data['schange'], location)
            containerinfo = editwidget.container_in_section(project, section_name, call_data['schange'], widget_name, container)
        except ServerError as e:
            raise FailPage(message = e.message)
    else:
        # remove the item from a page
        try:
            call_data['pchange'] = editpage.del_location(project, pagenumber, call_data['pchange'], location)
            containerinfo = editwidget.container_in_page(project, pagenumber, call_data['pchange'], widget_name, container)
        except ServerError as e:
            raise FailPage(message = e.message)

    # containerinfo is a namedtuple ('container', 'empty')

    # once item is deleted, no info on the item should be
    # left in call_data - this may not be required in future
    if 'location' in call_data:
        del call_data['location']
    if 'part' in call_data:
        del call_data['part']
    if 'part_loc' in call_data:
        del call_data['part_loc']

    call_data['container'] = container
    call_data['widget_name'] = widget_name

    # If deleting item has left container empty, return a full retrieve of the container page
    if containerinfo.empty:
        raise GoTo("back_to_container")

    # and get info to re-draw the table
    domcontents, dragrows, droprows = _container_domcontents(project, pagenumber, section_name, widget_name, container)

    # otherwise just redraw the table
    sd['domtable', 'dragrows']  = dragrows
    sd['domtable', 'droprows']  = droprows
    sd['domtable', 'contents']  = domcontents
    pd.update(sd)
    call_data['status'] = 'Item copied and then deleted. Use paste to recover or move it.'


def delete_container_dom(skicall):
    "Called by domtable to delete an item in a container"

    call_data = skicall.call_data
    pd = call_data['pagedata']
    sd = SectionData("editdom")

    project = call_data['editedprojname']
    pagenumber = None
    section_name = None

    if "page_number" in call_data:
        pagenumber = call_data["page_number"]
    elif "section_name" in call_data:
        section_name = call_data["section_name"]
    else:
        raise FailPage(message = "No page or section given")
    if ('editdom', 'domtable', 'contents') not in call_data:
        raise FailPage(message = "item to remove missing")

    part = call_data['editdom', 'domtable', 'contents']

    # so part is widget_name, container with location string of integers

    # create location which is a tuple or list consisting of three items:
    # a string of widget name
    # a container integer
    # a tuple or list of location integers
    location_list = part.split('-')
    # first item should be a string, rest integers
    if len(location_list) < 3:
        raise FailPage("Item to remove has not been recognised")

    try:
        widget_name = location_list[0]
        container = int(location_list[1])
        location_integers = [ int(i) for i in location_list[2:]]
    except Exception:
        raise FailPage("Item to remove has not been recognised")

    # location is a tuple of widget_name, container, tuple of location integers
    location = (widget_name, container, location_integers)

    part_tuple = skilift.part_info(project, pagenumber, section_name, location)
    if part_tuple is None:
        raise FailPage("Item to remove has not been recognised")

    # remove the item using functions from skilift.editsection and skilift.editpage
    if pagenumber is None:
        # remove the item from a section
        try:
            call_data['schange'] = editsection.del_location(project, section_name, call_data['schange'], location)
            containerinfo = editwidget.container_in_section(project, section_name, call_data['schange'], widget_name, container)
        except ServerError as e:
            raise FailPage(message = e.message)
    else:
        # remove the item from a page
        try:
            call_data['pchange'] = editpage.del_location(project, pagenumber, call_data['pchange'], location)
            containerinfo = editwidget.container_in_page(project, pagenumber, call_data['pchange'], widget_name, container)
        except ServerError as e:
            raise FailPage(message = e.message)

    # containerinfo is a namedtuple ('container', 'empty')

    # once item is deleted, no info on the item should be
    # left in call_data - this may not be required in future
    if 'location' in call_data:
        del call_data['location']
    if 'part' in call_data:
        del call_data['part']
    if 'part_loc' in call_data:
        del call_data['part_loc']

    call_data['container'] = container
    call_data['widget_name'] = widget_name

    # If deleting item has left container empty, return a full retrieve of the container page
    if containerinfo.empty:
        raise GoTo("back_to_container")

    # and get info to re-draw the table
    domcontents, dragrows, droprows = _container_domcontents(project, pagenumber, section_name, widget_name, container)

    # otherwise just redraw the table
    sd['domtable', 'dragrows']  = dragrows
    sd['domtable', 'droprows']  = droprows
    sd['domtable', 'contents']  = domcontents
    pd.update(sd)
    call_data['status'] = 'Item deleted.'


def _item_to_move(call_data):
    "Gets the item to be moved"
    project = call_data['editedprojname']
    pagenumber = None
    section_name = None

    if "page_number" in call_data:
        pagenumber = call_data["page_number"]
    elif "section_name" in call_data:
        section_name = call_data["section_name"]
    else:
        raise FailPage(message = "No page or section given")
    if ('editdom', 'domtable', 'contents') not in call_data:
        raise FailPage(message = "item to move missing")

    part = call_data['editdom', 'domtable', 'contents']

    # so part is widget_name, container with location string of integers

    # create location which is a tuple or list consisting of three items:
    # a string of widget name
    # a container integer
    # a tuple or list of location integers
    location_list = part.split('-')
    # first item should be a string, rest integers
    if len(location_list) < 3:
        raise FailPage("Item to move has not been recognised")

    try:
        widget_name = location_list[0]
        container = int(location_list[1])
        location_integers = [ int(i) for i in location_list[2:]]
    except Exception:
        raise FailPage("Item to move has not been recognised")

    # location is a tuple of widget_name, container, tuple of location integers
    location = (widget_name, container, location_integers)
    call_data['container'] = container
    call_data['widget_name'] = widget_name
    try:
        part_tuple = skilift.part_info(project, pagenumber, section_name, location)
    except ServerError as e:
        raise FailPage(message = e.message)

    if part_tuple is None:
        raise FailPage("Item to move has not been recognised")
    return part_tuple


def move_up_in_container_dom(skicall):
    "Called by domtable to move an item in a container up"

    call_data = skicall.call_data
    pd = call_data['pagedata']
    sd = SectionData("editdom")

    try:
        part_tuple = _item_to_move(call_data)
        location = part_tuple.location
        widget_name = location[0]
        container = int(location[1])
        location_integers = location[2]

        if (len(location_integers) == 1) and (location_integers[0] == 0):
            # at top, cannot be moved
            raise FailPage("Cannot be moved up")

        if location_integers[-1] == 0:
            # move up to next level
            new_location_integers = location_integers[:-1]
        else:
            # swap parts on same level
            new_location_integers = list(location_integers[:-1])
            new_location_integers.append(location_integers[-1] - 1)

        # after a move, location is wrong, so remove from call_data
        if 'location' in call_data:
            del call_data['location']
        if 'part' in call_data:
            del call_data['part']
        if 'part_top' in call_data:
            del call_data['part_top']
        if 'part_loc' in call_data:
            del call_data['part_loc']

        # move the item

        if part_tuple.section_name:
            # move the part in a section, using skilift.editsection.move_location(project, section_name, schange, from_location, to_location)
            call_data['schange'] = editsection.move_location(part_tuple.project, part_tuple.section_name, call_data['schange'], location, (widget_name, container, new_location_integers))
            domcontents, dragrows, droprows = _container_domcontents(part_tuple.project, None, part_tuple.section_name, widget_name, container)
        else:
            # move the part in a page, using skilift.editpage.move_location(project, pagenumber, pchange, from_location, to_location)
            call_data['pchange'] = editpage.move_location(part_tuple.project, part_tuple.pagenumber, call_data['pchange'], location, (widget_name, container, new_location_integers))
            domcontents, dragrows, droprows = _container_domcontents(part_tuple.project, part_tuple.pagenumber, None, widget_name, container)
    except ServerError as e:
        raise FailPage(message = e.message)

    # redraw the table
    sd['domtable', 'dragrows']  = dragrows
    sd['domtable', 'droprows']  = droprows
    sd['domtable', 'contents']  = domcontents
    pd.update(sd)


def move_up_right_in_container_dom(skicall):
    "Called by domtable to move an item in a container up and to the right"

    call_data = skicall.call_data
    pd = call_data['pagedata']
    sd = SectionData("editdom")

    try:
        part_tuple = _item_to_move(call_data)
        location = part_tuple.location
        widget_name = location[0]
        container = int(location[1])
        location_integers = location[2]

        if location_integers[-1] == 0:
            # at top of a part, cannot be moved
            raise FailPage("Cannot be moved up")
        new_parent_integers = list(location_integers[:-1])
        new_parent_integers.append(location_integers[-1] - 1)
        new_parent_location = (location[0], location[1], new_parent_integers)

        new_parent_tuple = skilift.part_info(part_tuple.project, part_tuple.pagenumber, part_tuple.section_name, new_parent_location)

        if new_parent_tuple is None:
            raise FailPage("Cannot be moved up")
        if new_parent_tuple.part_type != "Part":
            raise FailPage("Cannot be moved up")

        items_in_new_parent = len(skilift.part_contents(part_tuple.project, part_tuple.pagenumber, part_tuple.section_name, new_parent_location))

        new_location_integers =  tuple(new_parent_integers + [items_in_new_parent])

        # after a move, location is wrong, so remove from call_data
        if 'location' in call_data:
            del call_data['location']
        if 'part' in call_data:
            del call_data['part']
        if 'part_top' in call_data:
            del call_data['part_top']
        if 'part_loc' in call_data:
            del call_data['part_loc']

        # move the item

        if part_tuple.section_name:
            # move the part in a section, using skilift.editsection.move_location(project, section_name, schange, from_location, to_location)
            call_data['schange'] = editsection.move_location(part_tuple.project, part_tuple.section_name, call_data['schange'], location, (widget_name, container, new_location_integers))
            domcontents, dragrows, droprows = _container_domcontents(part_tuple.project, None, part_tuple.section_name, widget_name, container)
        else:
            # move the part in a page, using skilift.editpage.move_location(project, pagenumber, pchange, from_location, to_location)
            call_data['pchange'] = editpage.move_location(part_tuple.project, part_tuple.pagenumber, call_data['pchange'], location, (widget_name, container, new_location_integers))
            domcontents, dragrows, droprows = _container_domcontents(part_tuple.project, part_tuple.pagenumber, None, widget_name, container)
    except ServerError as e:
        raise FailPage(message = e.message)

    # redraw the table
    sd['domtable', 'dragrows']  = dragrows
    sd['domtable', 'droprows']  = droprows
    sd['domtable', 'contents']  = domcontents
    pd.update(sd)


def move_down_in_container_dom(skicall):
    "Called by domtable to move an item in a container down"

    call_data = skicall.call_data
    pd = call_data['pagedata']
    sd = SectionData("editdom")

    try:
        part_tuple = _item_to_move(call_data)
        location = part_tuple.location
        widget_name = location[0]
        container = int(location[1])
        location_integers = location[2]

        if len(location_integers) == 1:
            # Just at immediate level below top
            parent_location = (widget_name, container, ())
            items_in_parent = len(skilift.part_contents(part_tuple.project, part_tuple.pagenumber, part_tuple.section_name, parent_location))
            if location_integers[0] == (items_in_parent-1):
                # At end, cannot be moved
                raise FailPage("Cannot be moved down")
            new_location_integers = (location_integers[0]+2,)
        else:
            parent_integers = tuple(location_integers[:-1])
            parent_location = (widget_name, container, parent_integers)
            items_in_parent = len(skilift.part_contents(part_tuple.project, part_tuple.pagenumber, part_tuple.section_name, parent_location))
            if location_integers[-1] == (items_in_parent-1):
                # At end of a part, so move up a level
                new_location_integers = list(parent_integers[:-1])
                new_location_integers.append(parent_integers[-1] + 1)
            else:
                # just insert into current level
                new_location_integers = list(parent_integers)
                new_location_integers.append(location_integers[-1] + 2)

        # after a move, location is wrong, so remove from call_data
        if 'location' in call_data:
            del call_data['location']
        if 'part' in call_data:
            del call_data['part']
        if 'part_top' in call_data:
            del call_data['part_top']
        if 'part_loc' in call_data:
            del call_data['part_loc']

        # move the item

        if part_tuple.section_name:
            # move the part in a section, using skilift.editsection.move_location(project, section_name, schange, from_location, to_location)
            call_data['schange'] = editsection.move_location(part_tuple.project, part_tuple.section_name, call_data['schange'], location, (widget_name, container, new_location_integers))
            domcontents, dragrows, droprows = _container_domcontents(part_tuple.project, None, part_tuple.section_name, widget_name, container)
        else:
            # move the part in a page, using skilift.editpage.move_location(project, pagenumber, pchange, from_location, to_location)
            call_data['pchange'] = editpage.move_location(part_tuple.project, part_tuple.pagenumber, call_data['pchange'], location, (widget_name, container, new_location_integers))
            domcontents, dragrows, droprows = _container_domcontents(part_tuple.project, part_tuple.pagenumber, None, widget_name, container)
    except ServerError as e:
        raise FailPage(message = e.message)

    # redraw the table
    sd['domtable', 'dragrows']  = dragrows
    sd['domtable', 'droprows']  = droprows
    sd['domtable', 'contents']  = domcontents
    pd.update(sd)


def move_down_right_in_container_dom(skicall):
    "Called by domtable to move an item in a container down and to the right"

    call_data = skicall.call_data
    pd = call_data['pagedata']
    sd = SectionData("editdom")

    try:
        part_tuple = _item_to_move(call_data)
        location = part_tuple.location
        widget_name = location[0]
        container = int(location[1])
        location_integers = location[2]

        if len(location_integers) == 1:
            parent_location = (widget_name, container, ())
        else:
            parent_integers = list(location_integers[:-1])
            parent_location = (widget_name, container, parent_integers)
        p_contents = skilift.part_contents(part_tuple.project, part_tuple.pagenumber, part_tuple.section_name, parent_location)
        items_in_parent = len(p_contents)
        if location_integers[-1] == (items_in_parent-1):
            # At end of a block, cannot be moved
            raise FailPage("Cannot be moved down")
        new_parent_integers = list(location_integers[:-1])
        new_parent_integers.append(location_integers[-1] + 1)
        new_parent_location = (location[0], location[1], new_parent_integers)
        new_parent_tuple = skilift.part_info(part_tuple.project, part_tuple.pagenumber, part_tuple.section_name, new_parent_location)

        if new_parent_tuple is None:
            raise FailPage("Cannot be moved down")
        if not (new_parent_tuple.part_type == 'Part' or new_parent_tuple.part_type == 'Section'):
            raise FailPage("Cannot be moved down")

        new_location_integers = tuple(new_parent_integers+[0])

        # after a move, location is wrong, so remove from call_data
        if 'location' in call_data:
            del call_data['location']
        if 'part' in call_data:
            del call_data['part']
        if 'part_top' in call_data:
            del call_data['part_top']
        if 'part_loc' in call_data:
            del call_data['part_loc']

        # move the item

        if part_tuple.section_name:
            # move the part in a section, using skilift.editsection.move_location(project, section_name, schange, from_location, to_location)
            call_data['schange'] = editsection.move_location(part_tuple.project, part_tuple.section_name, call_data['schange'], location, (widget_name, container, new_location_integers))
            domcontents, dragrows, droprows = _container_domcontents(part_tuple.project, None, part_tuple.section_name, widget_name, container)
        else:
            # move the part in a page, using skilift.editpage.move_location(project, pagenumber, pchange, from_location, to_location)
            call_data['pchange'] = editpage.move_location(part_tuple.project, part_tuple.pagenumber, call_data['pchange'], location, (widget_name, container, new_location_integers))
            domcontents, dragrows, droprows = _container_domcontents(part_tuple.project, part_tuple.pagenumber, None, widget_name, container)
    except ServerError as e:
        raise FailPage(message = e.message)

    # redraw the table
    sd['domtable', 'dragrows']  = dragrows
    sd['domtable', 'droprows']  = droprows
    sd['domtable', 'contents']  = domcontents
    pd.update(sd)


def move_in_container_dom(skicall):
    "Called by domtable to move an item in a container after a drag and drop"

    call_data = skicall.call_data
    pd = call_data['pagedata']
    sd = SectionData("editdom")

    if ('editdom', 'domtable', 'dragrows') not in call_data:
        raise FailPage(message = "item to drop missing")
    editedprojname = call_data['editedprojname']
    pagenumber = None
    section_name = None

    if "page_number" in call_data:
        pagenumber = call_data["page_number"]
    elif "section_name" in call_data:
        section_name = call_data["section_name"]
    else:
        raise FailPage(message = "No page or section given")

    part_to_move = call_data['editdom', 'domtable', 'dragrows']

    # so part_to_move is widget name with container and location string of integers
    # create location which is a tuple or list consisting of three items:
    # a string of widget name
    # a container integer
    # a tuple or list of location integers
    location_list = part_to_move.split('-')
    # first item should be a string, rest integers
    if len(location_list) < 3:
        raise FailPage("Item to move has not been recognised")

    try:
        widget_name = location_list[0]
        container = int(location_list[1])
        location_to_move_integers = [ int(i) for i in location_list[2:]]
    except Exception:
        raise FailPage("Item to move has not been recognised")

    # location is a tuple of widget_name, container, tuple of location integers
    location_to_move = (widget_name, container, location_to_move_integers)
    call_data['container'] = container
    call_data['widget_name'] = widget_name


    # new target location

    target_part = call_data['editdom', 'domtable', 'droprows']

    # so target_part is widget name with location string of integers

    # create location which is a tuple or list consisting of three items:
    # a string of widget name
    # a container integer
    # a tuple or list of location integers

    location_list = target_part.split('-')
    # first item should be a string, rest integers
    if len(location_list) < 2:
        raise FailPage("target of move has not been recognised")
 
    if widget_name != location_list[0]:
        raise FailPage("Invalid move, widget name differs")

    if container != int(location_list[1]):
        raise FailPage("Invalid move, container number differs")

    if len(location_list) == 2:
            # At the container top row
            new_location_integers = [0]
    else:
        try:
            target_location_integers = [ int(i) for i in location_list[2:]]
        except Exception:
            raise FailPage("Invalid move, location not accepted")

        # location is a tuple of widget_name, container, tuple of location integers
        target_location = (widget_name, container, target_location_integers)

        # get target part_tuple from project, pagenumber, section_name, target_location
        target_part_tuple = skilift.part_info(editedprojname, pagenumber, section_name, target_location)
        if target_part_tuple is None:
            raise FailPage("Target has not been recognised")

        if (target_part_tuple.part_type == "Part") or (target_part_tuple.part_type == "Section"):
            # insert
            if target_location_integers:
                new_location_integers = list(target_location_integers)
                new_location_integers.append(0)
            else:
                new_location_integers = [0]
        else:
            # append
            new_location_integers = list(target_location_integers)
            new_location_integers[-1] = new_location_integers[-1] + 1

    # after a move, location is wrong, so remove from call_data
    if 'location' in call_data:
        del call_data['location']
    if 'part' in call_data:
        del call_data['part']
    if 'part_top' in call_data:
        del call_data['part_top']
    if 'part_loc' in call_data:
        del call_data['part_loc']

    # move the item
    try:
        if section_name:
            # move the part in a section, using skilift.editsection.move_location(project, section_name, schange, from_location, to_location)
            call_data['schange'] = editsection.move_location(editedprojname, section_name, call_data['schange'], location_to_move, (widget_name, container, new_location_integers))
            domcontents, dragrows, droprows = _container_domcontents(editedprojname, None, section_name, widget_name, container)
        else:
            # move the part in a page, using skilift.editpage.move_location(project, pagenumber, pchange, from_location, to_location)
            call_data['pchange']= editpage.move_location(editedprojname, pagenumber, call_data['pchange'], location_to_move, (widget_name, container, new_location_integers))
            domcontents, dragrows, droprows = _container_domcontents(editedprojname, pagenumber, None, widget_name, container)
    except ServerError as e:
        raise FailPage(message = e.message)

    # redraw the table
    sd['domtable', 'dragrows']  = dragrows
    sd['domtable', 'droprows']  = droprows
    sd['domtable', 'contents']  = domcontents
    pd.update(sd)



def _domtree(partdict, part_loc, contents, part_string_list, rows=1, indent=1):
    "Creates the contents of the domtable"

    # note: if in a container
    # part_loc = widget_name + '-' + container_number
    # otherwise part_loc = body, head, svg, section_name


    indent += 1
    padding = "padding-left : %sem;" % (indent,)
    u_r_flag = False
    last_row_at_this_level = 0

    parts = partdict['parts']

    # parts is a list of items
    last_index = len(parts)-1

    # list widgets with containers, each item is a list of tuples, each tuple being (rownumber, number of containers, indent, widget name)
    containers = []

    #Text   #characters..      #up  #up_right  #down  #down_right   #edit   #insert  #copy  #paste  #cut #delete

    for index, part in enumerate(parts):
        part_location_string = part_loc + '-' + str(index)
        part_string_list.append(part_location_string)
        rows += 1
        container_count = 0
        part_type, part_dict = part
        # the row text
        if part_type == 'Widget' or part_type == 'ClosedWidget':
            part_name = 'Widget ' + part_dict['name']
            if len(part_name)>40:
                part_name = part_name[:35] + '...'
            contents.append([part_name, padding, False, ''])
            part_brief = html.escape(part_dict.get('brief',''))
            if len(part_brief)>40:
                part_brief = part_brief[:35] + '...'
            if not part_brief:
                part_brief = '-'
            contents.append([part_brief, '', False, ''])
            if 'container_0' in part_dict:
                for n in range(20):   # assume maximum of 20 containers in a widget
                    containerstring = f"container_{n}"
                    if containerstring in part_dict:
                        container_count += 1
                    else:
                        # no further containers
                        containers.append((rows, container_count, indent, part_dict['name']))
                        break
        elif part_type == 'TextBlock':
            contents.append(['TextBlock', padding, False, ''])
            part_ref = part_dict['textref']
            if len(part_ref)>40:
                part_ref = part_ref[:35] + '...'
            if not part_ref:
                part_ref = '-'
            contents.append([part_ref, '', False, ''])
        elif part_type == 'SectionPlaceHolder':
            section_name = part_dict['placename']
            if section_name:
                section_name = "Section " + section_name
            else:
                section_name = "Section -None-"
            if len(section_name)>40:
                section_name = section_name[:35] + '...'
            contents.append([section_name, padding, False, ''])
            part_brief = html.escape(part_dict.get('brief',''))
            if len(part_brief)>40:
                part_brief = part_brief[:35] + '...'
            if not part_brief:
                part_brief = '-'
            contents.append([part_brief, '', False, ''])
        elif part_type == 'Text':
            contents.append(['Text', padding, False, ''])
            # in this case part_dict is the text string rather than a dictionary
            if len(part_dict)<40:
                part_str = html.escape(part_dict)
            else:
                part_str = html.escape(part_dict[:35] + '...')
            if not part_str:
                part_str = '-'
            contents.append([part_str, '', False, ''])
        elif part_type == 'HTMLSymbol':
            contents.append(['Symbol', padding, False, ''])
            part_text = part_dict['text']
            if len(part_text)<40:
                part_str = html.escape(part_text)
            else:
                part_str = html.escape(part_text[:35] + '...')
            if not part_str:
                part_str = '-'
            contents.append([part_str, '', False, ''])
        elif part_type == 'Comment':
            contents.append(['Comment', padding, False, ''])
            part_text = part_dict['text']
            if len(part_text)<33:
                part_str =  "&lt;!--" + part_text + '--&gt;'
            else:
                part_str = "&lt;!--" + part_text[:31] + '...'
            if not part_str:
                part_str = '&lt;!----&gt;'
            contents.append([part_str, '', False, ''])
        elif part_type == 'ClosedPart':
            if 'attribs' in part_dict:
                tag_name = "&lt;%s ... /&gt;" % part_dict['tag_name']
            else:
                tag_name = "&lt;%s /&gt;" % part_dict['tag_name']
            contents.append([tag_name, padding, False, ''])
            part_brief = html.escape(part_dict.get('brief',''))
            if len(part_brief)>40:
                part_brief = part_brief[:35] + '...'
            if not part_brief:
                part_brief = '-'
            contents.append([part_brief, '', False, ''])
        elif part_type == 'Part':
            if 'attribs' in part_dict:
                tag_name = "&lt;%s ... &gt;" % part_dict['tag_name']
            else:
                tag_name = "&lt;%s&gt;" % part_dict['tag_name']
            contents.append([tag_name, padding, False, ''])
            part_brief = html.escape(part_dict.get('brief',''))
            if len(part_brief)>40:
                part_brief = part_brief[:35] + '...'
            if not part_brief:
                part_brief = '-'
            contents.append([part_brief, '', False, ''])
        else:
            contents.append(['UNKNOWN', padding, False, ''])
            contents.append(['ERROR', '', False, ''])

        # UP ARROW
        if rows == 2:
            # second line in table cannot move upwards
            contents.append(['', '', False, '' ])
        else:
            contents.append(['&uarr;', 'width : 1%;', True, part_location_string])

        # UP RIGHT ARROW
        if u_r_flag:
            contents.append(['&nearr;', 'width : 1%;', True, part_location_string])
        else:
            contents.append(['', '', False, '' ])

        # DOWN ARROW
        if (indent == 2) and (index == last_index):
            # the last line at this top indent has been added, no down arrow
            contents.append(['', '', False, '' ])
        else:
            contents.append(['&darr;', 'width : 1%;', True, part_location_string])

        # DOWN RIGHT ARROW
        # set to empty, when next line is created if down-right not applicable
        contents.append(['', '', False, '' ])

        # EDIT
        contents.append(['Edit', 'width : 1%;', True, part_location_string])

        # INSERT or APPEND
        if part_type == 'Part':
            contents.append(['Insert', 'width : 1%;text-align: center;', True, part_location_string])
        else:
            contents.append(['Append', 'width : 1%;text-align: center;', True, part_location_string])

        # COPY
        contents.append(['Copy', 'width : 1%;', True, part_location_string])

        # PASTE
        contents.append(['Paste', 'width : 1%;', True, part_location_string])

        # CUT
        contents.append(['Cut', 'width : 1%;', True, part_location_string])

        # DELETE
        contents.append(['Delete', 'width : 1%;', True, part_location_string])

        u_r_flag = False
        if part_type == 'Part':
            if last_row_at_this_level and (part_dict['tag_name'] != 'script') and (part_dict['tag_name'] != 'pre'):
                # add down right arrow in previous row at this level, get loc_string from adjacent edit cell
                editcell = contents[last_row_at_this_level *12-6]
                loc_string = editcell[3]
                contents[last_row_at_this_level *12-7] = ['&searr;', 'width : 1%;', True, loc_string]
            last_row_at_this_level = rows
            rows, more_containers = _domtree(part_dict, part_location_string, contents, part_string_list, rows, indent)
            if more_containers:
                containers.extend(more_containers)
            # set u_r_flag for next item below this one
            if  (part_dict['tag_name'] != 'script') and (part_dict['tag_name'] != 'pre'):
                u_r_flag = True
        else:
            last_row_at_this_level =rows

    return rows, containers


def _insert_containers(contents, containers):
    "Inserts container lines into the dom table"
    if not containers:
        return

    # so some widgets have containers
    # containers is a list, each item is a list of tuples, each tuple being (rownumber, number of containers, indent, widget name)

    extrarows = 0
    
    for row, containercount, indent, name in containers:
        for c in range(containercount):
            cellnumber = (row + extrarows)*12
            # add row of contents cells for each container
            contents.insert(cellnumber, [f'{name} {c}', f"padding-left : {indent+1}em;", False, '' ])
            contents.insert(cellnumber+1, [f'Container {c} of {name}', '', False, '' ])
            contents.insert(cellnumber+2, ['', '', False, '' ])                                              # no up arrow
            contents.insert(cellnumber+3, ['', '', False, '' ])                                              # no up_right arrow
            contents.insert(cellnumber+4, ['', '', False, '' ])                                              # no down arrow
            contents.insert(cellnumber+5, ['', '', False, '' ])                                              # no down_right arrow
            contents.insert(cellnumber+6, ['Edit',  'width : 1%;', True, f'{name}--{c}'])                    # edit, with name_containernumber
            contents.insert(cellnumber+7, ['', '', False, '' ])                                              # no insert
            contents.insert(cellnumber+8, ['', '', False, '' ])                                              # no copy
            contents.insert(cellnumber+9, ['', '', False, '' ])                                              # no paste
            contents.insert(cellnumber+10, ['', '', False, '' ])                                             # no cut
            contents.insert(cellnumber+11, ['', '', False, '' ])                                             # no delete
            # As an extra row has been added
            extrarows += 1



