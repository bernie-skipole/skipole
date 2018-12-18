####### SKIPOLE WEB FRAMEWORK #######
#
# editsite.py  - get and put functions for the admin site page
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



import os, shutil, copy, tarfile, tempfile, random, collections

from .... import skilift
from ....skilift import off_piste, fromjson, editpage

from .. import utils, css_styles
from ....ski.excepts import FailPage, ValidateError, ServerError, GoTo


def retrieve_index_data(skicall):
    "Retrieves all field data for admin index page"

    call_data = skicall.call_data
    page_data = skicall.page_data

    # clears any session data
    utils.clear_call_data(call_data)

    project = call_data['editedprojname']
    adminproj = skilift.admin_project()

    projectinfo = skilift.project_info(project)
    admininfo = skilift.project_info(adminproj)

    page_data["projversion", "input_text"] = projectinfo.version
    page_data["brief:input_text"] = projectinfo.brief
    page_data["brief:bottomtext"] = "Current value: " + projectinfo.brief
    page_data["deflang:input_text"] = projectinfo.default_language
    page_data["deflang:bottomtext"] = "Current value: " + projectinfo.default_language

    page_data["download","link_ident"] = admininfo.path + project + ".tar.gz"

    if "root_path" in call_data:
        # "root_path" is set in call_data, so return it
        page_data["rtpath:input_text"] = call_data["root_path"]
    else:
        # "root_path" not in call_data, so return the current root_path
        page_data["rtpath:input_text"] = projectinfo.path

    if skilift.get_debug():
        page_data["debugstatus", "para_text"] = "Debug mode is ON"
        page_data["debugtoggle", "button_text"] = "Set Debug OFF"
    else:
        page_data["debugstatus", "para_text"] = "Debug mode is OFF"
        page_data["debugtoggle", "button_text"] = "Set Debug ON"


    subprojects = projectinfo.subprojects

    ctable = []
    for proj, suburl in subprojects.items():
        projinfo = skilift.project_info(proj)
        ctable.append([proj, suburl, projinfo.brief, proj, '', proj, '', True, True])
    # append the final row showing this edited project
    ctable.append([project, projectinfo.path, projectinfo.brief, '', '', '', '', False, False])
    page_data["projtable:contents"] = ctable

    # list directories under projects_dir()
    page_data['sdd1:option_list'] = []
    dirs = os.listdir(skilift.get_projectfiles_dir())
    if not dirs:
        page_data['sdd1:show_add_project'] = False
    else:
        # get projects which have json files
        for directory in dirs:
            if directory == project or (directory in subprojects):
                # do not include the current edited project or already loaded projects
                continue
            proj_jsonfile = fromjson.project_json_file(directory)
            if os.path.isfile(proj_jsonfile):
                page_data['sdd1:option_list'].append(directory)
        if page_data['sdd1:option_list']:
             page_data['sdd1:show_add_project'] = True
        else:
             page_data['sdd1:show_add_project'] = False

    if page_data['sdd1:option_list']:
        page_data['sdd1:selectvalue'] = page_data['sdd1:option_list'][0]
    else:
        page_data['sdd1:selectvalue'] = ''
    page_data['l2','content'] = "about %s.tar.gz can be found here." % project


def _clear_index_input_accepted(page_data):
    "Used by JSON to remove set_input_accepted flags from input fields"
    page_data['deflang','set_input_accepted'] = False
    page_data['projversion','set_input_accepted'] = False
    page_data['rtpath','set_input_accepted'] = False
    page_data['brief','set_input_accepted'] = False


def retrieve_help(skicall):
    "Uses skilift.get_textblock_text to get text help for the admin pages"

    call_data = skicall.call_data
    page_data = skicall.page_data

    # clears any session data
    utils.clear_call_data(call_data)
    page_data.clear()
    adminproj = skilift.admin_project()
    caller_ident = call_data['caller_ident']
    if not caller_ident:
        return
    textref = 'page.' + str(caller_ident[1])
    text = skilift.get_textblock_text(textref, skicall.lang, project=adminproj)
    if not text:
        text = "No help text for page %s has been found" % caller_ident[1]
    page_data[("adminhead","show_help","para_text")] = "\n" + text
    page_data[("adminhead","show_help","hide")] = False


def about_export(skicall):
    "Retrieves text for about export page"

    call_data = skicall.call_data
    page_data = skicall.page_data

    project = call_data['editedprojname']
    adminproj = skilift.admin_project()
    admininfo = skilift.project_info(adminproj)

    # fill in header information
    page_data[("adminhead","page_head","large_text")] = "Project: %s" % (project,)

    page_data["l2","link_ident"] = admininfo.path + project + ".tar.gz"

    # set the directory structure
    page_data[('tar_contents','pre_text')] = _tar_contents(project)


def retrieve_colour_data(skicall):
    "Retrieves all field data for admin colour page"

    call_data = skicall.call_data
    page_data = skicall.page_data

    adminproj = skilift.admin_project()

    # get default admin background color from project data
    adminbackcol = skilift.get_proj_data(adminproj, 'adminbackcol')
    # get individual admin colors from project data
    colours = skilift.get_proj_data(adminproj, 'colours')

    page_data["colhextest", "input_text"] = adminbackcol
    admincol = css_styles.hex_int(adminbackcol)
    page_data["red","input_text"] = str(admincol[0])
    page_data["green","input_text"] = str(admincol[1])
    page_data["blue","input_text"] = str(admincol[2])
    admin_h,admin_s,admin_l = css_styles.rgb_hsl(*admincol)
    page_data["hue","input_text"] = str(int(admin_h*360))
    page_data["saturation","input_text"] = str(int(admin_s*100))
    page_data["lightness","input_text"] = str(int(admin_l*100))



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
    page_data["l5_color","inputcol","label"] = "w3-theme-l5 color:"
    page_data["l5_color","inputcol","input_text"] = l5_color
    page_data["l5_color", "boxcol", "style"] = "float: right; width: 20em; background-color: %s; color: %s; border: solid white 2px; padding: 5px;" % (l5_color,l5_background_color)
    page_data["l5_color", "boxcol","set_text"] = l5_color

    # l5_background_color
    page_data["l5_background_color","inputcol","label"] = "w3-theme-l5 background color:"
    page_data["l5_background_color","inputcol","input_text"] = l5_background_color
    page_data["l5_background_color", "boxcol", "style"] = "float: right; width: 20em; background-color: %s; color: %s; border: solid white 2px; padding: 5px;" % (l5_background_color, l5_color)
    page_data["l5_background_color", "boxcol","set_text"] = l5_background_color

    # l4_color
    page_data["l4_color","inputcol","label"] = "w3-theme-l4 color:"
    page_data["l4_color","inputcol","input_text"] = l4_color
    page_data["l4_color", "boxcol", "style"] = "float: right; width: 20em; background-color: %s; color: %s; border: solid white 2px; padding: 5px;" % (l4_color,l4_background_color)
    page_data["l4_color", "boxcol","set_text"] = l4_color

    # l4_background_color
    page_data["l4_background_color","inputcol","label"] = "w3-theme-l4 background color:"
    page_data["l4_background_color","inputcol","input_text"] = l4_background_color
    page_data["l4_background_color", "boxcol", "style"] = "float: right; width: 20em; background-color: %s; color: %s; border: solid white 2px; padding: 5px;" % (l4_background_color,l4_color)
    page_data["l4_background_color", "boxcol","set_text"] = l4_background_color

    # l3_color
    page_data["l3_color","inputcol","label"] = "w3-theme-l3 color:"
    page_data["l3_color","inputcol","input_text"] = l3_color
    page_data["l3_color", "boxcol", "style"] = "float: right; width: 20em; background-color: %s; color: %s; border: solid white 2px; padding: 5px;" % (l3_color,l3_background_color)
    page_data["l3_color", "boxcol","set_text"] = l3_color

    # l3_background_color
    page_data["l3_background_color","inputcol","label"] = "w3-theme-l3 background color:"
    page_data["l3_background_color","inputcol","input_text"] = l3_background_color
    page_data["l3_background_color", "boxcol", "style"] = "float: right; width: 20em; background-color: %s; color: %s; border: solid white 2px; padding: 5px;" % (l3_background_color,l3_color)
    page_data["l3_background_color", "boxcol","set_text"] = l3_background_color

    # l2_color
    page_data["l2_color","inputcol","label"] = "w3-theme-l2 color:"
    page_data["l2_color","inputcol","input_text"] = l2_color
    page_data["l2_color", "boxcol", "style"] = "float: right; width: 20em; background-color: %s; color: %s; border: solid white 2px; padding: 5px;" % (l2_color,l2_background_color)
    page_data["l2_color", "boxcol","set_text"] = l2_color

    # l2_background_color
    page_data["l2_background_color","inputcol","label"] = "w3-theme-l2 background color:"
    page_data["l2_background_color","inputcol","input_text"] = l2_background_color
    page_data["l2_background_color", "boxcol", "style"] = "float: right; width: 20em; background-color: %s; color: %s; border: solid white 2px; padding: 5px;" % (l2_background_color,l2_color)
    page_data["l2_background_color", "boxcol","set_text"] = l2_background_color

    # l1_color
    page_data["l1_color","inputcol","label"] = "w3-theme-l1 color:"
    page_data["l1_color","inputcol","input_text"] = l1_color
    page_data["l1_color", "boxcol", "style"] = "float: right; width: 20em; background-color: %s; color: %s; border: solid white 2px; padding: 5px;" % (l1_color,l1_background_color)
    page_data["l1_color", "boxcol","set_text"] = l1_color

    # l1_background_color
    page_data["l1_background_color","inputcol","label"] = "w3-theme-l1 background color:"
    page_data["l1_background_color","inputcol","input_text"] = l1_background_color
    page_data["l1_background_color", "boxcol", "style"] = "float: right; width: 20em; background-color: %s; color: %s; border: solid white 2px; padding: 5px;" % (l1_background_color,l1_color)
    page_data["l1_background_color", "boxcol","set_text"] = l1_background_color

    # d1_color
    page_data["d1_color","inputcol","label"] = "w3-theme-d1 color:"
    page_data["d1_color","inputcol","input_text"] = d1_color
    page_data["d1_color", "boxcol", "style"] = "float: right; width: 20em; background-color: %s; color: %s; border: solid white 2px; padding: 5px;" % (d1_color,d1_background_color)
    page_data["d1_color", "boxcol","set_text"] = d1_color

    # d1_background_color
    page_data["d1_background_color","inputcol","label"] = "w3-theme-d1 background color:"
    page_data["d1_background_color","inputcol","input_text"] = d1_background_color
    page_data["d1_background_color", "boxcol", "style"] = "float: right; width: 20em; background-color: %s; color: %s; border: solid white 2px; padding: 5px;" % (d1_background_color,d1_color)
    page_data["d1_background_color", "boxcol","set_text"] = d1_background_color

    # d2_color
    page_data["d2_color","inputcol","label"] = "w3-theme-d2 color:"
    page_data["d2_color","inputcol","input_text"] = d2_color
    page_data["d2_color", "boxcol", "style"] = "float: right; width: 20em; background-color: %s; color: %s; border: solid white 2px; padding: 5px;" % (d2_color,d2_background_color)
    page_data["d2_color", "boxcol","set_text"] = d2_color

    # d2_background_color
    page_data["d2_background_color","inputcol","label"] = "w3-theme-d2 background color:"
    page_data["d2_background_color","inputcol","input_text"] = d2_background_color
    page_data["d2_background_color", "boxcol", "style"] = "float: right; width: 20em; background-color: %s; color: %s; border: solid white 2px; padding: 5px;" % (d2_background_color,d2_color)
    page_data["d2_background_color", "boxcol","set_text"] = d2_background_color

    # d3_color
    page_data["d3_color","inputcol","label"] = "w3-theme-d3 color:"
    page_data["d3_color","inputcol","input_text"] = d3_color
    page_data["d3_color", "boxcol", "style"] = "float: right; width: 20em; background-color: %s; color: %s; border: solid white 2px; padding: 5px;" % (d3_color,d3_background_color)
    page_data["d3_color", "boxcol","set_text"] = d3_color

    # d3_background_color
    page_data["d3_background_color","inputcol","label"] = "w3-theme-d3 background color:"
    page_data["d3_background_color","inputcol","input_text"] = d3_background_color
    page_data["d3_background_color", "boxcol", "style"] = "float: right; width: 20em; background-color: %s; color: %s; border: solid white 2px; padding: 5px;" % (d3_background_color,d3_color)
    page_data["d3_background_color", "boxcol","set_text"] = d3_background_color

    # d4_color
    page_data["d4_color","inputcol","label"] = "w3-theme-d4 color:"
    page_data["d4_color","inputcol","input_text"] = d4_color
    page_data["d4_color", "boxcol", "style"] = "float: right; width: 20em; background-color: %s; color: %s; border: solid white 2px; padding: 5px;" % (d4_color,d4_background_color)
    page_data["d4_color", "boxcol","set_text"] = d4_color

    # d4_background_color
    page_data["d4_background_color","inputcol","label"] = "w3-theme-d4 background color:"
    page_data["d4_background_color","inputcol","input_text"] = d4_background_color
    page_data["d4_background_color", "boxcol", "style"] = "float: right; width: 20em; background-color: %s; color: %s; border: solid white 2px; padding: 5px;" % (d4_background_color,d4_color)
    page_data["d4_background_color", "boxcol","set_text"] = d4_background_color

    # d5_color
    page_data["d5_color","inputcol","label"] = "w3-theme-d5 color:"
    page_data["d5_color","inputcol","input_text"] = d5_color
    page_data["d5_color", "boxcol", "style"] = "float: right; width: 20em; background-color: %s; color: %s; border: solid white 2px; padding: 5px;" % (d5_color,d5_background_color)
    page_data["d5_color", "boxcol","set_text"] = d5_color

    # d5_background_color
    page_data["d5_background_color","inputcol","label"] = "w3-theme-d5 background color:"
    page_data["d5_background_color","inputcol","input_text"] = d5_background_color
    page_data["d5_background_color", "boxcol", "style"] = "float: right; width: 20em; background-color: %s; color: %s; border: solid white 2px; padding: 5px;" % (d5_background_color,d5_color)
    page_data["d5_background_color", "boxcol","set_text"] = d5_background_color


    # light_color
    page_data["light_color","inputcol","label"] = "w3-theme-light color:"
    page_data["light_color","inputcol","input_text"] = light_color
    page_data["light_color", "boxcol", "style"] = "float: right; width: 20em; background-color: %s; color: %s; border: solid white 2px; padding: 5px;" % (light_color,light_background_color)
    page_data["light_color", "boxcol","set_text"] = light_color

    # light_background_color
    page_data["light_background_color","inputcol","label"] = "w3-theme-light background color:"
    page_data["light_background_color","inputcol","input_text"] = light_background_color
    page_data["light_background_color", "boxcol", "style"] = "float: right; width: 20em; background-color: %s; color: %s; border: solid white 2px; padding: 5px;" % (light_background_color,light_color)
    page_data["light_background_color", "boxcol","set_text"] = light_background_color

    # dark_color
    page_data["dark_color","inputcol","label"] = "w3-theme-dark color:"
    page_data["dark_color","inputcol","input_text"] = dark_color
    page_data["dark_color", "boxcol", "style"] = "float: right; width: 20em; background-color: %s; color: %s; border: solid white 2px; padding: 5px;" % (dark_color,dark_background_color)
    page_data["dark_color", "boxcol","set_text"] = dark_color

    # dark_background_color
    page_data["dark_background_color","inputcol","label"] = "w3-theme-dark background color:"
    page_data["dark_background_color","inputcol","input_text"] = dark_background_color
    page_data["dark_background_color", "boxcol", "style"] = "float: right; width: 20em; background-color: %s; color: %s; border: solid white 2px; padding: 5px;" % (dark_background_color,dark_color)
    page_data["dark_background_color", "boxcol","set_text"] = dark_background_color

    # action_color
    page_data["action_color","inputcol","label"] = "w3-theme-action color:"
    page_data["action_color","inputcol","input_text"] = action_color
    page_data["action_color", "boxcol", "style"] = "float: right; width: 20em; background-color: %s; color: %s; border: solid white 2px; padding: 5px;" % (action_color,action_background_color)
    page_data["action_color", "boxcol","set_text"] = action_color

    # action_background_color
    page_data["action_background_color","inputcol","label"] = "w3-theme-action background color:"
    page_data["action_background_color","inputcol","input_text"] = action_background_color
    page_data["action_background_color", "boxcol", "style"] = "float: right; width: 20em; background-color: %s; color: %s; border: solid white 2px; padding: 5px;" % (action_background_color,action_color)
    page_data["action_background_color", "boxcol","set_text"] = action_background_color

    # theme_color
    page_data["theme_color","inputcol","label"] = "w3-theme color:"
    page_data["theme_color","inputcol","input_text"] = theme_color
    page_data["theme_color", "boxcol", "style"] = "float: right; width: 20em; background-color: %s; color: %s; border: solid white 2px; padding: 5px;" % (theme_color,theme_background_color)
    page_data["theme_color", "boxcol","set_text"] = theme_color

    # theme_background_color
    page_data["theme_background_color","inputcol","label"] = "w3-theme background color:"
    page_data["theme_background_color","inputcol","input_text"] = theme_background_color
    page_data["theme_background_color", "boxcol", "style"] = "float: right; width: 20em; background-color: %s; color: %s; border: solid white 2px; padding: 5px;" % (theme_background_color,theme_color)
    page_data["theme_background_color", "boxcol","set_text"] = theme_background_color

    # text_color
    page_data["text_color","inputcol","label"] = "w3-text-theme color:"
    page_data["text_color","inputcol","input_text"] = text_color
    page_data["text_color", "boxcol", "style"] = "float: right; width: 20em; background-color: %s; color: %s; border: solid white 2px; padding: 5px;" % (text_color,theme_background_color)
    page_data["text_color", "boxcol","set_text"] = text_color

    # border_color
    page_data["border_color","inputcol","label"] = "w3-border-theme color:"
    page_data["border_color","inputcol","input_text"] = border_color
    page_data["border_color", "boxcol", "style"] = "float: right; width: 20em; background-color: %s; color: %s; border: solid white 2px; padding: 5px;" % (border_color,theme_background_color)
    page_data["border_color", "boxcol","set_text"] = border_color

    # hover_color
    page_data["hover_color","inputcol","label"] = "w3-hover-theme:hover color:"
    page_data["hover_color","inputcol","input_text"] = hover_color
    page_data["hover_color", "boxcol", "style"] = "float: right; width: 20em; background-color: %s; color: %s; border: solid white 2px; padding: 5px;" % (hover_color,hover_background_color)
    page_data["hover_color", "boxcol","set_text"] = hover_color

    # hover_background_color
    page_data["hover_background_color","inputcol","label"] = "w3-hover-theme:hover background color:"
    page_data["hover_background_color","inputcol","input_text"] = hover_background_color
    page_data["hover_background_color", "boxcol", "style"] = "float: right; width: 20em; background-color: %s; color: %s; border: solid white 2px; padding: 5px;" % (hover_background_color,hover_color)
    page_data["hover_background_color", "boxcol","set_text"] = hover_background_color

    # hover_text_color
    page_data["hover_text_color","inputcol","label"] = "w3-hover-text-theme:hover color:"
    page_data["hover_text_color","inputcol","input_text"] = hover_text_color
    page_data["hover_text_color", "boxcol", "style"] = "float: right; width: 20em; background-color: %s; color: %s; border: solid white 2px; padding: 5px;" % (hover_text_color,hover_background_color)
    page_data["hover_text_color", "boxcol","set_text"] = hover_text_color

    # hover_border_color
    page_data["hover_border_color","inputcol","label"] = "w3-hover-border-theme:hover color:"
    page_data["hover_border_color","inputcol","input_text"] = hover_border_color
    page_data["hover_border_color", "boxcol", "style"] = "float: right; width: 20em; background-color: %s; color: %s; border: solid white 2px; padding: 5px;" % (hover_border_color,hover_background_color)
    page_data["hover_border_color", "boxcol","set_text"] = hover_border_color


def goto_edit_item(skicall):
    "Goes to the edit page, folder etc depending on the item submitted"

    call_data = skicall.call_data
    page_data = skicall.page_data

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
    

def retrieve_download(skicall):
    "Set page_data['filepath'] to the url of the edited project tar.gz file"

    call_data = skicall.call_data
    page_data = skicall.page_data

    # clears any session data
    utils.clear_call_data(call_data)
    # set filepath to tar file
    project = call_data["editedprojname"]
    projinfo = skilift.project_info(project)
    filepath = os.path.join(project, project + '.tar.gz')
    if os.path.isfile(projinfo.tar_path):
        page_data["filepath"] = filepath
    else:
        raise FailPage(message="File %s not yet created" % (filepath,))


def submit_rootpath(skicall):
    "Sets the path of the root project"

    call_data = skicall.call_data
    page_data = skicall.page_data

    project = call_data['editedprojname']
    if "root_path" not in call_data:
        raise FailPage(message='Invalid call')
    if project != skilift.get_root():
        # cannot set a rootpath if this is not the rootproject
        raise FailPage(message='Invalid: Not the root project', widget = "rtpath")
    try:
        path = skilift.set_root_project_path(call_data["root_path"])
    except ServerError as e:
        raise FailPage(message = e.message, widget = "rtpath")
    call_data['editedprojurl'] = path
    page_data['rtpath','set_input_accepted'] = True
    call_data['status'] = 'Root path set'


def submit_language(skicall):
    "Sets the default language of the edited project"

    call_data = skicall.call_data
    page_data = skicall.page_data

    project = call_data['editedprojname']
    if "default_language" not in call_data:
        raise FailPage(message = 'Invalid call')
    try:
        skilift.set_proj_default_language(project, call_data["default_language"])
    except ServerError as e:
        raise FailPage(message = e.message)
    _clear_index_input_accepted(page_data)
    page_data['deflang','set_input_accepted'] = True
    call_data['status'] = 'Language set'


def submit_brief(skicall):
    "Sets the brief description of the edited project"

    call_data = skicall.call_data
    page_data = skicall.page_data

    project = call_data['editedprojname']
    if ('brief','input_text') not in call_data:
        raise FailPage(message='Invalid call')
    try:
        skilift.set_proj_brief(project, call_data['brief','input_text'])
    except ServerError as e:
        raise FailPage(message = e.message)
    call_data['editedprojbrief'] = call_data['brief','input_text']
    page_data['brief','set_input_accepted'] = True
    call_data['status'] = 'Project brief set'


def set_version(skicall):
    "Sets the version of the edited project"

    call_data = skicall.call_data
    page_data = skicall.page_data

    project = call_data['editedprojname']
    if ('projversion','input_text') not in call_data:
        raise FailPage(message='Invalid call')
    try:
        skilift.set_proj_version(project, call_data['projversion','input_text'])
    except ServerError as e:
        raise FailPage(message = e.message)
    _clear_index_input_accepted(page_data)
    call_data['editedprojversion'] = call_data['projversion','input_text']
    page_data['projversion','set_input_accepted'] = True
    page_data["adminhead","page_head","large_text"] = "Project: %s version: %s" % (project,call_data['projversion','input_text'])
    call_data['status'] = 'Project version set'


def debugtoggle(skicall):

    call_data = skicall.call_data
    page_data = skicall.page_data

    if skilift.get_debug():
        skilift.set_debug(False)
        page_data["debugtoggle", "button_text"] = "Set Debug ON"
        call_data['status'] = 'Debug mode set OFF'
    else:
        skilift.set_debug(True)
        page_data["debugtoggle", "button_text"] = "Set Debug OFF"
        call_data['status'] = 'Debug mode set ON'


def filter_from_tar(projinfo):
    "Returns a function which excludes unwanted files"
    def filter_out(tarinfo):
        "When creating the tar file, leave some things out of the skipole code directory"
        nonlocal projinfo
        # return None if filename is to be excluded
        # or tarinfo if it is to be added
        filename = tarinfo.name
        if filename.endswith(('~','.pyc')):
            return None
        if os.path.basename(filename) == "__pycache__":
            return None
        paths = filename.split(os.path.sep)
        if len(paths) < 3:
            # must be export/skipoles
            return tarinfo
        if paths[2] == 'projectcode':
            if len(paths) < 4:
                # must be export/skipoles/projectcode
                return tarinfo
            if paths[3] == projinfo.project:
                return tarinfo
            if paths[3] == skilift.admin_project():
                return None
            if paths[3] == "__init__.py":
                return tarinfo
            if paths[3] not in projinfo.subprojects:
                return None
        return tarinfo
    return filter_out


def _submit_saveproject(skicall):
    "save the project to tarfile projectfiles\project_name\project_name.tar"

    call_data = skicall.call_data
    page_data = skicall.page_data

    project = call_data['editedprojname']
    export = project
    tar = None
    try:
        projinfo = skilift.project_info(project)
        # Create textblock json files
        accesstextblocks = skilift.get_accesstextblocks(project)
        accesstextblocks.save()
        # create project.json
        fromjson.project_to_json(project)
        # open "project.tar.gz" for writing - first deleting any old version
        tar_dst = projinfo.tar_path
        if os.path.isfile(tar_dst):
            os.remove(tar_dst)
        tar = tarfile.open(tar_dst, "w:gz")
        tar.dereference = True
        # generate a myapp.py file in a temporary file to insert into the tar file
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as tempmyapp:
            tempmyapp.write(skipole_myapp(project))
        # add temporary file to the archive
        tar.add(tempmyapp.name, arcname=os.path.join(export,  "myapp.py"))
        # and delete the temporary file
        os.unlink(tempmyapp.name)
        # create export\__main__.py
        main_file = projinfo.main_path
        if os.path.isfile(main_file):
            tar.add(main_file, arcname=os.path.join(export,  "__main__.py"))
        else:
            # generate a __main__.py file in a temporary file to insert into the tar file
            with tempfile.NamedTemporaryFile(mode='w', delete=False) as tempfp:
                tempfp.write(skipole_run(project))
            # add temporary file to the archive
            tar.add(tempfp.name, arcname=os.path.join(export,  "__main__.py"))
            # and delete the temporary file
            os.unlink(tempfp.name)
        # skipoles -> export\skipoles
        tar_skipoles = os.path.join(export,'skipoles')
        from .... import __file__ as skipoles_file
        skipoles_dir = os.path.dirname(os.path.realpath(skipoles_file))
        tar.add(skipoles_dir, arcname=tar_skipoles, filter=filter_from_tar(projinfo))

        # projectfiles\project\static -> export\projectfiles\project\static
        static_dir = projinfo.static_path
        if not os.path.isdir(static_dir):
            # make static dir
            os.mkdir(static_dir)
        tar_static_dir = os.path.join(export, 'projectfiles', project, 'static')
        tar.add(static_dir, arcname=tar_static_dir)

        # projectfiles\project\data -> export\projectfiles\project\data
        data_dir = projinfo.data_path
        if not os.path.isdir(data_dir):
            # make data dir
            os.mkdir(data_dir)
        tar_data_dir = os.path.join(export, 'projectfiles', project, 'data')
        tar.add(data_dir, arcname=tar_data_dir)

        projects = projinfo.subprojects
        for subproj_ident in projects:
            if subproj_ident == skilift.admin_project():
                continue
            subprojinfo = skilift.project_info(subproj_ident)
            # projectfiles\subproj_ident\static -> export\projectfiles\subproj_ident\static
            static_dir = subprojinfo.static_path
            tar_static_dir = os.path.join(export, 'projectfiles', subproj_ident, 'static')
            tar.add(static_dir, arcname=tar_static_dir)
            # projectfiles\subproj_ident\data -> export\projectfiles\subproj_ident\data
            data_dir = subprojinfo.data_path
            tar_data_dir = os.path.join(export, 'projectfiles', subproj_ident, 'data')
            tar.add(data_dir, arcname=tar_data_dir)
    except Exception as e:
        if hasattr(e, 'message'):
            raise FailPage(e.message)
        else:
            raise FailPage('Error: Unable to save the project')
    finally:
        if tar:
            tar.close()
    return tar_dst


def json_submit_saveproject(skicall):
    "save the project to tarfile projectfiles\project_name\project_name.tar"

    call_data = skicall.call_data
    page_data = skicall.page_data

    tar_dst = _submit_saveproject(skicall)
    page_data[("saveresult","para_text")] = "Project saved in file %s" % tar_dst
    page_data[("saveresult","show_para")] = True
    # clears any session data
    utils.clear_call_data(call_data)
    call_data['status'] = "Project saved"


def html_submit_saveproject(skicall):
    "save the project to tarfile projectfiles\project_name\export.tar"

    call_data = skicall.call_data
    page_data = skicall.page_data

    tar_dst = _submit_saveproject(skicall)
    # clears any session data
    utils.clear_call_data(call_data)
    call_data['status'] = "Project saved in file %s" % tar_dst


def submit_hex_color(skicall):
    "set palette background color - from hex"

    call_data = skicall.call_data
    page_data = skicall.page_data

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
    page_data = skicall.page_data

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
    page_data = skicall.page_data

    adminproject = call_data['adminproj']
    colours = skilift.get_proj_data(adminproject, 'colours')
    if not colours:
        return {}
    return colours


def set_widgets_css(skicall):
    "sets default css classes into widgets"

    call_data = skicall.call_data
    page_data = skicall.page_data

    project = call_data["editedprojname"]
    off_piste.set_widget_css_to_default(project)
    call_data['status'] = 'Widget CSS classes set'


def _tar_contents(proj_ident):
    "Returns the text of the tar directory structure"
    text = "\n\n"

    dirtext = proj_ident
    pos = 31-len(dirtext)
    if pos > 0:
        dirtext += ' '*pos
    dirtext += "- directory" 
    text += dirtext

    text += """

    myapp.py                   - Minimal python file holding the wsgi application, for use with other web servers

    __main__.py                - Runs a web server and serves your wsgi application

    projectfiles               - Directory of non-python data and static files

       lib                     - lib sub-project data and static files

"""

    projtext = "       " + proj_ident
    pos = 31-len(projtext)
    if pos > 0:
        projtext += ' '*pos
    projtext += "- One or more project folders, each containing:" 
    text += projtext

    text += """

          static               - A folder holding your static files

          data                 - A folder holding data files needed to build the project

             __main__.py       - Optional - copied to above __main__.py when project committed

             textblocks_json   - A folder holding json files of TextBlocks

             project.json      - A file of definitions used to build your pages

             defaults.json     - Used by the admin project when adding new pages and widgets

    skipoles                   - The python package directory holding the code

       __init__.py             - Package initialisation containing class WSGIApplication

       ski                     - Python package containing the framework page and widget classes

       skilift                 - Python package containing functions to edit the project

       projectcode             - Python package containing sub-packages of user project code

          __init__.py          - Package initialisation to route calls to the correct projects

          lib                  - Python lib sub-project package

          """

    projfoldertext = proj_ident
    pos = 21-len(projfoldertext)
    if pos > 0:
        projfoldertext += ' '*pos
    projfoldertext += "- One or more project packages, containing your code\n" 
    text += projfoldertext

    return text



def skipole_myapp(project):
    "Create myapp.py file for the tar"
    return """

# this may need to be edited and uncommented so that the skipoles package can be found

# import sys
# sys.path.append('/path/to/skipoles')

# alternatively, the web server may be able to change to this directory
# (see the chdir option of uwsgi)
# or may be able to set a value into pythonpath

import os
import skipoles

# the skipoles framework needs to know the directory where projectfiles are held
# The following line assumes projectfiles is in the same directory as this myapp.py file

projectfiles = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'projectfiles')

# create the wsgi application

application = skipoles.WSGIApplication("%s", {}, projectfiles)

""" % (project,)



def skipole_run(project):

    projectinfo = skilift.project_info(project)

    return """#!/usr/bin/env python3

# sys is used for the sys.exit function and to check python version
import sys, argparse, os

# Check the python version
if sys.version_info[0] != 3 or sys.version_info[1] < 2:
    print("Sorry, your python version is not compatable")
    print("This program requires python 3.2 or later")
    print("Program exiting")
    sys.exit(1)


import skipoles

project = "%s"

# Set up command line parser

parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
description='%s',
epilog='Stop the server with ctrl-c')

parser.add_argument("-p", "--port", type=int, dest="port", default=8000,
                  help="The port the web server will listen at, default 8000.")

parser.add_argument("-o", "--option", dest="option",
                  help="An optional value passed to your functions.")

parser.add_argument("-w", "--waitress", action='store_true', dest="waitress", default=False,
                  help="Serve project with the Waitress web server (python3-waitress is required).")

parser.add_argument('--version', action='version', version=project + ' ' + '%s')

args = parser.parse_args()

port = args.port

if args.waitress:
    # This requires python3 version of the waitress web server to be
    # installed on your server, package 'python3-waitress' with debian
    try:
        from waitress import serve
    except:
        print("Unable to import waitress")
        sys.exit(1)
else:
    # As default use the Python library web server
    from wsgiref.simple_server import make_server


# An 'option' value can be passed to the project, and futher options to subprojects
# with a dictionary of {project:option,..} where each key is the project or sub project name
# and each option is any value you care to add, and which will appear as an argument in
# your start_project and start_call functions. This allows you to pass a parameter from the
# command line, or from start up code set here, to your project code if required.
# If you do not wish to use this function, then pass an empty dictionary.

if args.option:
    options = {project : args.option}
else:
    options = {}

# the skipoles framework needs to know the directory where projectfiles are held
# The following line assumes projectfiles is in the same directory as this __main__.py file
projectfiles = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'projectfiles')


# create the wsgi application
application = skipoles.WSGIApplication(project, options, projectfiles)


# serve the application

print("Serving on port " + str(port) + "...")
print("Press ctrl-c to stop")

if args.waitress:
    serve(application, host='0.0.0.0', port=port)
else:
    # using wsgiref.simple_server
    httpd = make_server("", port, application)
    httpd.serve_forever()
""" % (project, projectinfo.brief, projectinfo.version)


