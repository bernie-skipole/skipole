

import os, random, collections

from ... import skilift
from ....skilift import off_piste, fromjson, editpage

from .. import utils, css_styles
from ....ski.excepts import FailPage, ValidateError, ServerError, GoTo, SkiStop, SkiRestart

from ....ski.project_class_definition import SectionData


def stopserver(skicall):
    "Called from admin page to stop the web server"
    call_data = skicall.call_data
    starttime = call_data['starttime']
    rxstarttime = call_data.get('rxstarttime')
    if rxstarttime != starttime:
        raise GoTo('admin_home')    
    raise SkiStop

def restartserver(skicall):
    "Called from admin page to restart the web server"
    call_data = skicall.call_data
    starttime = call_data['starttime']
    rxstarttime = call_data.get('rxstarttime')
    if rxstarttime != starttime:
        raise GoTo('admin_home')    
    raise SkiRestart


def retrieve_index_data(skicall):
    "Retrieves all field data for admin index page"

    call_data = skicall.call_data
    pd = call_data['pagedata']

    # clears any session data
    utils.clear_call_data(call_data)

    # send starttime
    call_data['rxstarttime'] = call_data['starttime']

    project = call_data['editedprojname']

    projectinfo = skilift.project_info(project)

    pd["projversion", "input_text"] = projectinfo.version
    pd["brief","input_text"] = projectinfo.brief
    pd["brief","bottomtext"] = "Current value: " + projectinfo.brief
    pd["deflang","input_text"] = projectinfo.default_language
    pd["deflang","bottomtext"] = "Current value: " + projectinfo.default_language

    if "root_path" in call_data:
        # "root_path" is set in call_data, so return it
        pd["rtpath","input_text"] = call_data["root_path"]
    else:
        # "root_path" not in call_data, so return the current root_path
        pd["rtpath","input_text"] = projectinfo.path

    if skilift.get_debug():
        pd["debugstatus", "para_text"] = "Debug mode is ON"
        pd["debugtoggle", "button_text"] = "Set Debug OFF"
    else:
        pd["debugstatus", "para_text"] = "Debug mode is OFF"
        pd["debugtoggle", "button_text"] = "Set Debug ON"

    # create table of projects
    subprojects = projectinfo.subprojects
    col1 = []
    col2 = []
    col3 = []
    for proj, suburl in subprojects.items():
        projinfo = skilift.project_info(proj)
        col1.append(proj)
        col2.append(suburl)
        col3.append(projinfo.brief)
    # append the final row showing this edited project
    col1.append(project)
    col2.append(projectinfo.path)
    col3.append(projectinfo.brief)
    pd['subs','col1'] = col1
    pd['subs','col2'] = col2
    pd['subs','col3'] = col3


    ctable = []
    for proj, suburl in subprojects.items():
        projinfo = skilift.project_info(proj)
        ctable.append([proj, suburl, projinfo.brief, proj, '', proj, '', True, True])
    # append the final row showing this edited project
    ctable.append([project, projectinfo.path, projectinfo.brief, '', '', '', '', False, False])
    pd["projtable","contents"] = ctable

    # list directories under projects_dir()
    pd['sdd1','option_list'] = []

    # sdd1 must be deleted
    pd['sdd1','show_add_project'] = False
    pd['sdd1','selectvalue'] = ''


def _clear_index_input_accepted(pd):
    "Used by JSON to remove set_input_accepted flags from input fields"
    pd['deflang','set_input_accepted'] = False
    pd['projversion','set_input_accepted'] = False
    pd['rtpath','set_input_accepted'] = False
    pd['brief','set_input_accepted'] = False


def retrieve_help(skicall):
    "Uses skicall.textblock_text to get text help for the admin pages"

    call_data = skicall.call_data
    pd = call_data['pagedata']

    # clears any session data
    utils.clear_call_data(call_data)
    pd.clear()
    caller_ident = call_data['caller_ident']
    if not caller_ident:
        return
    textref = 'page.' + str(caller_ident[1])
    text = skicall.textblock(textref)
    if not text:
        text = "No help text for page %s has been found" % caller_ident[1]

    sd_adminhead = SectionData("adminhead")
    sd_adminhead["show_help","para_text"] = "\n" + text
    sd_adminhead["show_help","hide"] = False
    pd.update(sd_adminhead)


def get_text(skicall):
    """Finds any widget submitting 'get_field' with value of a textblock ref, sets
       pd with key widget with field 'div_content' and value the textblock text.
       Introduces <br /> at newlines"""

    pd = skicall.call_data['pagedata']

    if 'received' not in skicall.submit_dict:
        return
    received_widgfields = skicall.submit_dict['received']
    for key, val in received_widgfields.items():
        if isinstance(key, tuple) and (key[-1] == 'get_field'):
            text = skicall.textblock(val)
            if text is None:
                continue
            text = text.replace('\n', '\n<br />')
            if len(key) == 3:
                sd = SectionData(key[0])
                sd[key[1],'div_content'] = text
                sd[key[1],'hide'] = False
                pd.update(sd)
            elif len(key) == 2:
                pd[key[0],'div_content'] = text
                pd[key[0],'hide'] = False


def get_html(skicall):
    """Finds any widget submitting 'get_field' with value of a textblock ref, sets
       pd with key widget with field 'div_content' and value the textblock text
       but does not introduce <br /> for new lines"""

    pd = skicall.call_data['pagedata']

    if 'received' not in skicall.submit_dict:
        return
    received_widgfields = skicall.submit_dict['received']
    for key, val in received_widgfields.items():
        if isinstance(key, tuple) and (key[-1] == 'get_field'):
            text = skicall.textblock(val)
            if text is None:
                continue
            if len(key) == 3:
                sd = SectionData(key[0])
                sd[key[1],'div_content'] = text
                sd[key[1],'hide'] = False
                pd.update(sd)
            elif len(key) == 2:
                pd[key[0],'div_content'] = text
                pd[key[0],'hide'] = False



def retrieve_colour_data(skicall):
    "Retrieves all field data for admin colour page"

    call_data = skicall.call_data
    pd = call_data['pagedata']

    # get default admin background color from project data
    adminbackcol = skicall.proj_data['adminbackcol']
    # get individual admin colors from project data
    colours = skicall.proj_data['colours']

    pd["colhextest", "input_text"] = adminbackcol
#    admincol = css_styles.hex_int(adminbackcol)
#    pd["red","input_text"] = str(admincol[0])
#    pd["green","input_text"] = str(admincol[1])
#    pd["blue","input_text"] = str(admincol[2])
#    admin_h,admin_s,admin_l = css_styles.rgb_hsl(*admincol)
#    pd["hue","input_text"] = str(int(admin_h*360))
#    pd["saturation","input_text"] = str(int(admin_s*100))
#    pd["lightness","input_text"] = str(int(admin_l*100))

    l5_color = colours['w3_theme_l5_color']
    l5_background_color = colours['w3_theme_l5_background_color']
    l4_color = colours['w3_theme_l4_color']
    l4_background_color = colours['w3_theme_l4_background_color']
    l3_color = colours['w3_theme_l3_color']
    l3_background_color = colours['w3_theme_l3_background_color']
    l2_color = colours['w3_theme_l2_color']
    l2_background_color = colours['w3_theme_l2_background_color']
    l1_color = colours['w3_theme_l1_color']
    l1_background_color = colours['w3_theme_l1_background_color']
    d1_color = colours['w3_theme_d1_color']
    d1_background_color = colours['w3_theme_d1_background_color']
    d2_color = colours['w3_theme_d2_color']
    d2_background_color = colours['w3_theme_d2_background_color']
    d3_color = colours['w3_theme_d3_color']
    d3_background_color = colours['w3_theme_d3_background_color']
    d4_color = colours['w3_theme_d4_color']
    d4_background_color = colours['w3_theme_d4_background_color']
    d5_color = colours['w3_theme_d5_color']
    d5_background_color = colours['w3_theme_d5_background_color']
    light_color = colours['w3_theme_light_color']
    light_background_color = colours['w3_theme_light_background_color']
    dark_color = colours['w3_theme_dark_color']
    dark_background_color = colours['w3_theme_dark_background_color']
    action_color = colours['w3_theme_action_color']
    action_background_color = colours['w3_theme_action_background_color']
    theme_color = colours['w3_theme_color']
    theme_background_color = colours['w3_theme_background_color']
    text_color = colours['w3_text_theme_color']
    border_color = colours['w3_border_theme_color']
    hover_color = colours['w3_hover_theme_hover_color']
    hover_background_color = colours['w3_hover_theme_hover_background_color']
    hover_text_color = colours['w3_hover_text_theme_color']
    hover_border_color = colours['w3_hover_border_theme_hover_color']

    # l5_color
    _sectioncolor(pd, "l5_color", "w3-theme-l5 color:", l5_color, l5_background_color)

    # l5_background_color
    _sectioncolor(pd, "l5_background_color", "w3-theme-l5 background color:", l5_background_color, l5_color)

    # l4_color
    _sectioncolor(pd, "l4_color", "w3-theme-l4 color:", l4_color, l4_background_color)

    # l4_background_color
    _sectioncolor(pd, "l4_background_color", "w3-theme-l4 background color:", l4_background_color, l4_color)

    # l3_color
    _sectioncolor(pd, "l3_color", "w3-theme-l3 color:", l3_color, l3_background_color)

    # l3_background_color
    _sectioncolor(pd, "l3_background_color", "w3-theme-l3 background color:", l3_background_color, l3_color)

    # l2_color
    _sectioncolor(pd, "l2_color", "w3-theme-l2 color:", l2_color, l2_background_color)

    # l2_background_color
    _sectioncolor(pd, "l2_background_color", "w3-theme-l2 background color:", l2_background_color, l2_color)

    # l1_color
    _sectioncolor(pd, "l1_color", "w3-theme-l1 color:", l1_color, l1_background_color)

    # l1_background_color
    _sectioncolor(pd, "l1_background_color", "w3-theme-l1 background color:", l1_background_color, l1_color)

    # d1_color
    _sectioncolor(pd, "d1_color", "w3-theme-d1 color:", d1_color, d1_background_color)

    # d1_background_color
    _sectioncolor(pd, "d1_background_color", "w3-theme-d1 background color:", d1_background_color, d1_color)

    # d2_color
    _sectioncolor(pd, "d2_color", "w3-theme-d2 color:", d2_color, d2_background_color)

    # d2_background_color
    _sectioncolor(pd, "d2_background_color", "w3-theme-d2 background color:", d2_background_color, d2_color)

    # d3_color
    _sectioncolor(pd, "d3_color", "w3-theme-d3 color:", d3_color, d3_background_color)

    # d3_background_color
    _sectioncolor(pd, "d3_background_color", "w3-theme-d3 background color:", d3_background_color, d3_color)

    # d4_color
    _sectioncolor(pd, "d4_color", "w3-theme-d4 color:", d4_color, d4_background_color)

    # d4_background_color
    _sectioncolor(pd, "d4_background_color", "w3-theme-d4 background color:", d4_background_color, d4_color)

    # d5_color
    _sectioncolor(pd, "d5_color", "w3-theme-d5 color:", d5_color, d5_background_color)

    # d5_background_color
    _sectioncolor(pd, "d5_background_color", "w3-theme-d5 background color:", d5_background_color, d5_color)

    # light_color
    _sectioncolor(pd, "light_color", "w3-theme-light color:", light_color, light_background_color)

    # light_background_color
    _sectioncolor(pd, "light_background_color", "w3-theme-light background color:", light_background_color, light_color)

    # dark_color
    _sectioncolor(pd, "dark_color", "w3-theme-dark color:", dark_color, dark_background_color)

    # dark_background_color
    _sectioncolor(pd, "dark_background_color", "w3-theme-dark background color:", dark_background_color, dark_color)

    # action_color
    _sectioncolor(pd, "action_color", "w3-theme-action color:", action_color, action_background_color)

    # action_background_color
    _sectioncolor(pd, "action_background_color", "w3-theme-action background color:", action_background_color, action_color)

    # theme_color
    _sectioncolor(pd, "theme_color", "w3-theme color:", theme_color, theme_background_color)

    # theme_background_color
    _sectioncolor(pd, "theme_background_color", "w3-theme background color:", theme_background_color, theme_color)

    # text_color
    _sectioncolor(pd, "text_color", "w3-text-theme color:", text_color, theme_background_color)

    # border_color
    _sectioncolor(pd, "border_color", "w3-border-theme color:", border_color, theme_background_color)

    # hover_color
    _sectioncolor(pd, "hover_color", "w3-hover-theme:hover color:", hover_color, hover_background_color)

    # hover_background_color
    _sectioncolor(pd, "hover_background_color", "w3-hover-theme:hover background color:", hover_background_color, hover_color)

    # hover_text_color
    _sectioncolor(pd, "hover_text_color", "w3-hover-text-theme:hover color:", hover_text_color, hover_background_color)

    # hover_border_color
    _sectioncolor(pd, "hover_border_color", "w3-hover-border-theme:hover color:", hover_border_color, hover_background_color)


def _sectioncolor(pd, sectionalias, label, input_text, backcolor):
    "Called by above function to set section data"
    sd = SectionData(sectionalias)
    sd["inputcol","label"] = label
    sd["inputcol","input_text"] = input_text
    sd["boxcol", "style"] = f"width: 10em; background-color: {input_text}; color: {backcolor}; border: solid white 2px; padding: 5px;"
    sd["boxcol","set_html"] = input_text
    pd.update(sd)


def goto_edit_item(skicall):
    "Goes to the edit page, folder etc depending on the item submitted"

    call_data = skicall.call_data

    edited_item = call_data["edited_item"]
    project = call_data['editedprojname']

    # clear call data
    utils.clear_call_data(call_data)

    itemnumber = skilift.get_itemnumber(project, edited_item)
    if itemnumber is None:
        raise FailPage(message="Item not found")

    item = skilift.item_info(project, itemnumber)
    if item is None:
        raise FailPage(message="Item not found")

    if item.item_type == "Folder":
        call_data['folder_number'] = itemnumber
        call_data['fchange'] = item.change
        raise GoTo(target=22008, clear_submitted=True)

    call_data['page_number'] = itemnumber
    call_data['pchange'] = item.change

    if item.item_type == "TemplatePage":
        raise GoTo(target=23207, clear_submitted=True)
    elif item.item_type == "RespondPage":
        raise GoTo(target=26007, clear_submitted=True)
    elif item.item_type == "FilePage":
        raise GoTo(target=29007, clear_submitted=True)
    elif item.item_type == "CSS":
        raise GoTo(target=28007, clear_submitted=True)
    elif item.item_type == "JSON":
        raise GoTo(target=20407, clear_submitted=True)
    elif item.item_type == "SVG":
        raise GoTo(target=23407, clear_submitted=True)

    del call_data['page_number']
    del call_data['pchange']
    raise FailPage(message="Item not found")
    

def submit_language(skicall):
    "Sets the default language of the edited project"

    call_data = skicall.call_data
    pd = call_data['pagedata']

    project = call_data['editedprojname']
    if "default_language" not in call_data:
        raise FailPage(message = 'Invalid call')
    try:
        skilift.set_proj_default_language(project, call_data["default_language"])
    except ServerError as e:
        raise FailPage(message = e.message)
    _clear_index_input_accepted(pd)
    pd['deflang','set_input_accepted'] = True
    call_data['status'] = 'Language set'


def submit_brief(skicall):
    "Sets the brief description of the edited project"

    call_data = skicall.call_data
    pd = call_data['pagedata']

    project = call_data['editedprojname']
    if ('brief','input_text') not in call_data:
        raise FailPage(message='Invalid call')
    try:
        skilift.set_proj_brief(project, call_data['brief','input_text'])
    except ServerError as e:
        raise FailPage(message = e.message)
    call_data['editedprojbrief'] = call_data['brief','input_text']
    pd['brief','set_input_accepted'] = True
    call_data['status'] = 'Project brief set'


def set_version(skicall):
    "Sets the version of the edited project"

    call_data = skicall.call_data
    pd = call_data['pagedata']

    project = call_data['editedprojname']
    if ('projversion','input_text') not in call_data:
        raise FailPage(message='Invalid call')
    try:
        skilift.set_proj_version(project, call_data['projversion','input_text'])
    except ServerError as e:
        raise FailPage(message = e.message)
    _clear_index_input_accepted(pd)
    call_data['editedprojversion'] = call_data['projversion','input_text']
    pd['projversion','set_input_accepted'] = True

    sd = SectionData("adminhead")
    sd["page_head","large_text"] = "Project: %s version: %s" % (project,call_data['projversion','input_text'])
    pd.update(sd)
    call_data['status'] = 'Project version set'


def debugtoggle(skicall):

    call_data = skicall.call_data
    pd = call_data['pagedata']

    if skilift.get_debug():
        skilift.set_debug(False)
        pd["debugtoggle", "button_text"] = "Set Debug ON"
        call_data['status'] = 'Debug mode set OFF'
    else:
        skilift.set_debug(True)
        pd["debugtoggle", "button_text"] = "Set Debug OFF"
        call_data['status'] = 'Debug mode set ON'


def submit_saveproject(skicall):
    "save the project textblock and project.json files"
    call_data = skicall.call_data
    project = call_data['editedprojname']
    projinfo = skilift.project_info(project)
    # Create textblock json files
    accesstextblocks = skilift.get_accesstextblocks(project)
    accesstextblocks.save()
    # create project.json
    fromjson.project_to_json(project)
    # clears any session data
    utils.clear_call_data(call_data)
    call_data['status'] = "Project data saved to JSON files"



def submit_hex_color(skicall):
    "set palette background color - from hex"

    call_data = skicall.call_data

    adminproj = call_data['adminproj']
    palette = css_styles.hex_int(call_data['hexcol'].lower())
    adminbackcol = css_styles.int_hex(*palette)
    # generate colours
    colours = css_styles.get_colours(*palette)
    # set test colours in proj_data
    skilift.set_proj_data(adminproj, 'adminbackcol', adminbackcol)
    skilift.set_proj_data(adminproj, 'colours', colours)
    # set test colours in defaults.json
    fromjson.set_defaults(adminproj, key="backcol", value=adminbackcol)
    ordered_colours = collections.OrderedDict(sorted(colours.items(), key=lambda t: t[0]))
    fromjson.set_defaults(adminproj, key="colours", value=ordered_colours)
    # change name of 220 to avoid css cache
    pchange = editpage.pagechange(adminproj, 220)
    if pchange is None:
        raise ServerError(message="Admin page 220, label w3-theme-ski has not been found")
    newname = "w3-theme-ski-" + str(random.randint(10000, 99999)) + ".css"
    editpage.rename_page(adminproj, 220, pchange, newname)


def set_colour(skicall):
    "sets individual colour string"

    call_data = skicall.call_data

    adminproj = call_data['adminproj']
    # get colors from project data
    colours = skilift.get_proj_data(adminproj, 'colours')
    if call_data["l5_color","inputcol","input_text"]:
        colours['w3_theme_l5_color'] = call_data["l5_color","inputcol","input_text"]
        call_data['status'] = 'w3-theme-l5 color set'
    elif call_data["l5_background_color","inputcol","input_text"]:
        colours['w3_theme_l5_background_color'] = call_data["l5_background_color","inputcol","input_text"]
        call_data['status'] = 'w3-theme-l5 background color set'
    elif call_data["l4_color","inputcol","input_text"]:
        colours['w3_theme_l4_color'] = call_data["l4_color","inputcol","input_text"]
        call_data['status'] = 'w3-theme-l4 color set'
    elif call_data["l4_background_color","inputcol","input_text"]:
        colours['w3_theme_l4_background_color'] = call_data["l4_background_color","inputcol","input_text"]
        call_data['status'] = 'w3-theme-l4 background color set'
    elif call_data["l3_color","inputcol","input_text"]:
        colours['w3_theme_l3_color'] = call_data["l3_color","inputcol","input_text"]
        call_data['status'] = 'w3-theme-l3 color set'
    elif call_data["l3_background_color","inputcol","input_text"]:
        colours['w3_theme_l3_background_color'] = call_data["l3_background_color","inputcol","input_text"]
        call_data['status'] = 'w3-theme-l3 background color set'
    elif call_data["l2_color","inputcol","input_text"]:
        colours['w3_theme_l2_color'] = call_data["l2_color","inputcol","input_text"]
        call_data['status'] = 'w3-theme-l2 color set'
    elif call_data["l2_background_color","inputcol","input_text"]:
        colours['w3_theme_l2_background_color'] = call_data["l2_background_color","inputcol","input_text"]
        call_data['status'] = 'w3-theme-l2 background color set'
    elif call_data["l1_color","inputcol","input_text"]:
        colours['w3_theme_l1_color'] = call_data["l1_color","inputcol","input_text"]
        call_data['status'] = 'w3-theme-l1 color set'
    elif call_data["l1_background_color","inputcol","input_text"]:
        colours['w3_theme_l1_background_color'] = call_data["l1_background_color","inputcol","input_text"]
        call_data['status'] = 'w3-theme-l1 background color set'
    elif call_data["d5_color","inputcol","input_text"]:
        colours['w3_theme_d5_color'] = call_data["d5_color","inputcol","input_text"]
        call_data['status'] = 'w3-theme-d5 color set'
    elif call_data["d5_background_color","inputcol","input_text"]:
        colours['w3_theme_d5_background_color'] = call_data["d5_background_color","inputcol","input_text"]
        call_data['status'] = 'w3-theme-d5 background color set'
    elif call_data["d4_color","inputcol","input_text"]:
        colours['w3_theme_d4_color'] = call_data["d4_color","inputcol","input_text"]
        call_data['status'] = 'w3-theme-d4 color set'
    elif call_data["d4_background_color","inputcol","input_text"]:
        colours['w3_theme_d4_background_color'] = call_data["d4_background_color","inputcol","input_text"]
        call_data['status'] = 'w3-theme-d4 background color set'
    elif call_data["d3_color","inputcol","input_text"]:
        colours['w3_theme_d3_color'] = call_data["d3_color","inputcol","input_text"]
        call_data['status'] = 'w3-theme-d3 color set'
    elif call_data["d3_background_color","inputcol","input_text"]:
        colours['w3_theme_d3_background_color'] = call_data["d3_background_color","inputcol","input_text"]
        call_data['status'] = 'w3-theme-d3 background color set'
    elif call_data["d2_color","inputcol","input_text"]:
        colours['w3_theme_d2_color'] = call_data["d2_color","inputcol","input_text"]
        call_data['status'] = 'w3-theme-d2 color set'
    elif call_data["d2_background_color","inputcol","input_text"]:
        colours['w3_theme_d2_background_color'] = call_data["d2_background_color","inputcol","input_text"]
        call_data['status'] = 'w3-theme-d2 background color set'
    elif call_data["d1_color","inputcol","input_text"]:
        colours['w3_theme_d1_color'] = call_data["d1_color","inputcol","input_text"]
        call_data['status'] = 'w3-theme-d1 color set'
    elif call_data["d1_background_color","inputcol","input_text"]:
        colours['w3_theme_d1_background_color'] = call_data["d1_background_color","inputcol","input_text"]
        call_data['status'] = 'w3-theme-d1 background color set'
    elif call_data["light_color","inputcol","input_text"]:
        colours['w3_theme_light_color'] = call_data["light_color","inputcol","input_text"]
        call_data['status'] = 'w3-theme-light color set'
    elif call_data["light_background_color","inputcol","input_text"]:
        colours['w3_theme_light_background_color'] = call_data["light_background_color","inputcol","input_text"]
        call_data['status'] = 'w3-theme-light background color set'
    elif call_data["dark_color","inputcol","input_text"]:
        colours['w3_theme_dark_color'] = call_data["dark_color","inputcol","input_text"]
        call_data['status'] = 'w3-theme-dark color set'
    elif call_data["dark_background_color","inputcol","input_text"]:
        colours['w3_theme_dark_background_color'] = call_data["dark_background_color","inputcol","input_text"]
        call_data['status'] = 'w3-theme-dark background color set'
    elif call_data["action_color","inputcol","input_text"]:
        colours['w3_theme_action_color'] = call_data["action_color","inputcol","input_text"]
        call_data['status'] = 'w3-theme-action color set'
    elif call_data["action_background_color","inputcol","input_text"]:
        colours['w3_theme_action_background_color'] = call_data["action_background_color","inputcol","input_text"]
        call_data['status'] = 'w3-theme-action background color set'
    elif call_data["theme_color","inputcol","input_text"]:
        colours['w3_theme_color'] = call_data["theme_color","inputcol","input_text"]
        call_data['status'] = 'w3-theme color set'
    elif call_data["theme_background_color","inputcol","input_text"]:
        colours['w3_theme_background_color'] = call_data["theme_background_color","inputcol","input_text"]
        call_data['status'] = 'w3-theme background color set'
    elif call_data["text_color","inputcol","input_text"]:
        colours['w3_text_theme_color'] = call_data["text_color","inputcol","input_text"]
        call_data['status'] = 'w3-text-theme color set'
    elif call_data["border_color","inputcol","input_text"]:
        colours['w3_border_theme_color'] = call_data["boder_color","inputcol","input_text"]
        call_data['status'] = 'w3-border-theme color set'
    elif call_data["hover_color","inputcol","input_text"]:
        colours['w3_hover_theme_hover_color'] = call_data["hover_color","inputcol","input_text"]
        call_data['status'] = 'w3-hover-theme:hover color set'
    elif call_data["hover_background_color","inputcol","input_text"]:
        colours['w3_hover_theme_hover_background_color'] = call_data["hover_background_color","inputcol","input_text"]
        call_data['status'] = 'w3-hover-theme:hover background color set'
    elif call_data["hover_text_color","inputcol","input_text"]:
        colours['w3_hover_text_theme_color'] = call_data["hover_text_color","inputcol","input_text"]
        call_data['status'] = 'w3-hover-text-theme:hover color set'
    elif call_data["hover_border_color","inputcol","input_text"]:
        colours['w3_hover_border_theme_hover_color'] = call_data["hover_border_color","inputcol","input_text"]
        call_data['status'] = 'w3-hover-border-theme:hover color set'
    else:
        # no colour recognised
        return
    # etc for each colour
    # Then set colours into project data
    skilift.set_proj_data(adminproj, 'colours', colours)
    # set test colours in defaults.json
    fromjson.set_defaults(adminproj, key="colours", value=colours)
    # change name of 220 to avoid css cache
    pchange = editpage.pagechange(adminproj, 220)
    if pchange is None:
        raise ServerError(message="Admin page 220, label w3-theme-ski has not been found")
    newname = "w3-theme-ski-" + str(random.randint(10000, 99999)) + ".css"
    editpage.rename_page(adminproj, 220, pchange, newname)


def ski_theme(skicall):
    "set colours into the w3-theme-ski.css page"

    call_data = skicall.call_data

    adminproject = call_data['adminproj']
    colours = skilift.get_proj_data(adminproject, 'colours')
    if not colours:
        return {}
    return colours


def set_widgets_css(skicall):
    "sets default css classes into widgets"

    call_data = skicall.call_data

    project = call_data["editedprojname"]
    off_piste.set_widget_css_to_default(project)
    call_data['status'] = 'Widget CSS classes set'



