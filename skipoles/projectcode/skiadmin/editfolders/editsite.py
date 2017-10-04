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



import os, shutil, copy, pickle, tarfile, tempfile, random

from .... import skilift
from ....skilift import off_piste, fromjson, editpage

from .. import utils, css_styles
from ....ski import skiboot
from ....ski.excepts import FailPage, ValidateError, ServerError, GoTo

from ....projectcode import code_reload


def retrieve_index_data(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Retrieves all field data for admin index page"
    editedproj = call_data['editedproj']
    adminproj = call_data['adminproj']

    proj_ident = editedproj.proj_ident

    page_data["projversion", "input_text"] = editedproj.version
    page_data["brief:input_text"] = editedproj.brief
    page_data["brief:bottomtext"] = "Current value: " + editedproj.brief
    page_data["deflang:input_text"] = editedproj.default_language
    page_data["deflang:bottomtext"] = "Current value: " + editedproj.default_language

    page_data["download","link_ident"] = adminproj.url + editedproj.proj_ident + ".tar.gz"

    if "root_path" in call_data:
        # "root_path" is set in call_data, so return it
        page_data["rtpath:input_text"] = call_data["root_path"]
    else:
        # "root_path" not in call_data, so return the current root_path
        page_data["rtpath:input_text"] = editedproj.url

    if skiboot.get_debug():
        page_data["debugstatus", "para_text"] = "Debug mode is ON"
        page_data["debugtoggle", "button_text"] = "Set Debug OFF"
    else:
        page_data["debugstatus", "para_text"] = "Debug mode is OFF"
        page_data["debugtoggle", "button_text"] = "Set Debug ON"

    ctable = []
    for proj, suburl in editedproj.subproject_paths.items():
        ctable.append([proj, suburl, skiboot.getproject(proj).brief, proj, '', proj, '', True, True])
    # append the final row showing this edited project
    ctable.append([editedproj.proj_ident, editedproj.url, editedproj.brief, '', '', '', '', False, False])
    page_data["projtable:contents"] = ctable

    # list directories under projects_dir()
    page_data['sdd1:option_list'] = []
    dirs = os.listdir(skiboot.projectfiles())
    if not dirs:
        page_data['sdd1:show_add_project'] = False
    else:
        # get loaded projects
        loaded_projects = editedproj.subproject_paths
        # get projects which have json files
        for directory in dirs:
            if directory == editedproj.proj_ident or (directory in loaded_projects):
                # do not include the current edited project or already loaded projects
                continue
            proj_jsonfile = skiboot.project_json(directory)
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
    page_data['l2','content'] = "about %s.tar.gz can be found here." % editedproj.proj_ident


def _clear_index_input_accepted(page_data):
    "Used by JSON to remove set_input_accepted flags from input fields"
    page_data['deflang','set_input_accepted'] = False
    page_data['projversion','set_input_accepted'] = False
    page_data['rtpath','set_input_accepted'] = False
    page_data['brief','set_input_accepted'] = False


def retrieve_help(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Uses skilift.get_textblock_text to get text help for the admin pages"
    page_data.clear()
    adminproj = call_data['adminproj']
    caller_ident = call_data['caller_ident']
    if not caller_ident:
        return
    textref = 'page.' + str(caller_ident[1])
    # text = skilift.get_textblock_text(textref, lang, project=adminproj.proj_ident).replace('\n', '\n<br />')
    text = skilift.get_textblock_text(textref, lang, project=adminproj.proj_ident)
    if not text:
        text = "No help text for page %s has been found" % caller_ident[1]
    page_data[("adminhead","show_help","para_text")] = "\n" + text
    page_data[("adminhead","show_help","hide")] = False


def about_export(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Retrieves text for about export page"
    editedproj = call_data['editedproj']
    adminproj = call_data['adminproj']

    proj_ident = editedproj.proj_ident

    # fill in header information
    page_data[("adminhead","page_head","large_text")] = "Project: %s" % (proj_ident,)
    page_data[("adminhead","page_head","small_text")] = editedproj.brief

    page_data["l2","link_ident"] = adminproj.url + editedproj.proj_ident + ".tar.gz"

    # set the directory structure
    page_data[('tar_contents','pre_text')] = _tar_contents(proj_ident)


def retrieve_colour_data(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Retrieves all field data for admin colour page"

    adminproj = call_data['adminproj']

    # get default admin background color from project data
    adminbackcol = skilift.get_proj_data(adminproj.proj_ident, 'adminbackcol')
    # get individual admin colors from project data
    colours = skilift.get_proj_data(adminproj.proj_ident, 'colours')

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


def goto_edit_item(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Goes to the edit page, folder etc depending on the item submitted"

    edited_item = call_data["edited_item"]
    editedprojname = call_data["editedprojname"]

    # clear call data
    utils.no_ident_data(call_data)

    if '/' in edited_item:
        # a url has been given
        ident = skiboot.ident_from_path(edited_item, proj_ident=editedprojname)
    else:
        # an ident or label has been given
        ident = skiboot.find_ident(edited_item, proj_ident=editedprojname)
    if ident is None:
        raise FailPage(message="Page not found")
    item = skiboot.from_ident(ident, proj_ident=editedprojname, import_sections=False)
    if item is None:
        raise FailPage(message="Page not found")
    if item.page_type == "TemplatePage":
        call_data['edit_page'] = item.ident
        raise GoTo(target=23207, clear_submitted=True)
    elif item.page_type == "RespondPage":
        call_data['edit_page'] = item.ident
        raise GoTo(target=26007, clear_submitted=True)
    elif item.page_type == "FilePage":
        call_data['edit_page'] = item.ident
        raise GoTo(target=29007, clear_submitted=True)
    elif item.page_type == "CSS":
        call_data['edit_page'] = item.ident
        raise GoTo(target=28007, clear_submitted=True)
    elif item.page_type == "JSON":
        call_data['edit_page'] = item.ident
        raise GoTo(target=20407, clear_submitted=True)
    elif item.page_type == "SVG":
        call_data['edit_page'] = item.ident
        raise GoTo(target=23407, clear_submitted=True)
    elif item.page_type == "Folder":
        call_data['edit_folder'] = str(item.ident) ####### moving away from ident objects
        raise GoTo(target=22008, clear_submitted=True)
    raise FailPage(message="Item not found")
    

def retrieve_download(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Set page_data['filepath'] to the path to edited project tar.gz file"
    editedproj = call_data['editedproj']
    # filepath is path beneath static
    filepath = os.path.join(editedproj.proj_ident, editedproj.proj_ident + '.tar.gz')
    if os.path.isfile(skiboot.tar_path(editedproj.proj_ident)):
        page_data["filepath"] = filepath
    else:
        raise FailPage(message="File %s not yet created" % (filepath,))


def submit_rootpath(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    if "root_path" not in call_data:
        raise ValidateError(message='Invalid call')
    editedproj = call_data['editedproj']
    if not editedproj.rootproject:
        # cannot set a rootpath if this is not the rootproject
        raise FailPage(message='Invalid: Not the root project', widget = "rtpath")
    try:
        editedproj.url = call_data["root_path"]
    except (ValidateError, ServerError) as e:
        raise FailPage(message = e.message, widget = "rtpath")
    call_data['editedprojurl'] = editedproj.url
    page_data['rtpath','set_input_accepted'] = True
    call_data['status'] = 'Root path set'


def submit_language(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    if "default_language" not in call_data:
        raise FailPage(message = 'Invalid call')
    editedproj = call_data['editedproj']
    try:
        editedproj.default_language = call_data["default_language"]
    except (ValidateError, ServerError) as e:
        raise FailPage(message = e.message)
    _clear_index_input_accepted(page_data)
    page_data['deflang','set_input_accepted'] = True
    call_data['status'] = 'Language set'


def submit_brief(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    if ('brief','input_text') not in call_data:
        raise ValidateError(message='Invalid call')
    editedproj = call_data['editedproj']
    try:
        editedproj.brief = call_data['brief','input_text']
    except ServerError as e:
        raise FailPage(message = e.message)
    call_data['editedprojbrief'] = editedproj.brief
    page_data['brief','set_input_accepted'] = True
    call_data['status'] = 'Project brief set'


def set_version(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    if ('projversion','input_text') not in call_data:
        raise ValidateError(message='Invalid call')
    editedproj = call_data['editedproj']
    try:
        editedproj.version = call_data['projversion','input_text']
    except ServerError as e:
        raise FailPage(message = e.message)
    _clear_index_input_accepted(page_data)
    call_data['editedprojversion'] = editedproj.version
    page_data['projversion','set_input_accepted'] = True
    page_data["adminhead","page_head","large_text"] = "Project: %s version: %s" % (editedproj.proj_ident,editedproj.version)
    call_data['status'] = 'Project version set'


def debugtoggle(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    if skiboot.get_debug():
        skiboot.set_debug(False)
        page_data["debugtoggle", "button_text"] = "Set Debug ON"
        call_data['status'] = 'Debug mode set OFF'
    else:
        skiboot.set_debug(True)
        page_data["debugtoggle", "button_text"] = "Set Debug OFF"
        call_data['status'] = 'Debug mode set ON'


def filter_from_tar(editedproj):
    "Returns a function which excludes unwanted files"
    def filter_out(tarinfo):
        "When creating the tar file, leave some things out of the skipole code directory"
        nonlocal editedproj
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
            if paths[3] == editedproj.proj_ident:
                return tarinfo
            if paths[3] == skiboot.admin_project():
                return None
            if paths[3] == "__init__.py":
                return tarinfo
            projects = editedproj.subprojects
            if paths[3] not in projects:
                return None
        return tarinfo
    return filter_out


def _submit_saveproject(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "save the project to tarfile projectfiles\project_name\project_name.tar"

    editedproj = call_data['editedproj']
    proj_ident = editedproj.proj_ident

    export =proj_ident
    export_tar = proj_ident + ".tar.gz"
    tar = None
    try:
        # Create textblock json files
        editedproj.textblocks.save()
        # create project.json
        fromjson.project_to_json(proj_ident)
        # open export_tar for writing - first deleting any old version
        tar_dst = os.path.join(skiboot.projectpath(proj_ident), export_tar)
        if os.path.isfile(tar_dst):
            os.remove(tar_dst)
        tar = tarfile.open(tar_dst, "w:gz")
        tar.dereference = True
        # generate a myapp.py file in a temporary file to insert into the tar file
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as tempmyapp:
            tempmyapp.write(skipole_myapp(editedproj))
        # add temporary file to the archive
        tar.add(tempmyapp.name, arcname=os.path.join(export,  "myapp.py"))
        # and delete the temporary file
        os.unlink(tempmyapp.name)
        # create export\__main__.py
        main_file = skiboot.project_main(proj_ident=proj_ident)
        if os.path.isfile(main_file):
            tar.add(main_file, arcname=os.path.join(export,  "__main__.py"))
        else:
            # generate a __main__.py file in a temporary file to insert into the tar file
            with tempfile.NamedTemporaryFile(mode='w', delete=False) as tempfp:
                tempfp.write(skipole_run(editedproj))
            # add temporary file to the archive
            tar.add(tempfp.name, arcname=os.path.join(export,  "__main__.py"))
            # and delete the temporary file
            os.unlink(tempfp.name)
        # skipoles -> export\skipoles
        tar_skipoles = os.path.join(export,'skipoles')
        from .... import __file__ as skipoles_file
        skipoles_dir = os.path.dirname(os.path.realpath(skipoles_file))
        tar.add(skipoles_dir, arcname=tar_skipoles, filter=filter_from_tar(editedproj))

        # projectfiles\proj_ident\static -> export\projectfiles\proj_ident\static
        static_dir = skiboot.projectstatic(proj_ident)
        if not os.path.isdir(static_dir):
            # make static dir
            os.mkdir(static_dir)
        tar_static_dir = os.path.join(export, 'projectfiles', proj_ident, 'static')
        tar.add(static_dir, arcname=tar_static_dir)

        # projectfiles\proj_ident\data -> export\projectfiles\proj_ident\data
        data_dir = skiboot.projectdata(proj_ident)
        if not os.path.isdir(data_dir):
            # make data dir
            os.mkdir(data_dir)
        tar_data_dir = os.path.join(export, 'projectfiles', proj_ident, 'data')
        tar.add(data_dir, arcname=tar_data_dir)

        projects = editedproj.subprojects
        for subproj_ident in projects:
            if subproj_ident == skiboot.admin_project():
                continue
            # projectfiles\subproj_ident\static -> export\projectfiles\subproj_ident\static
            static_dir = skiboot.projectstatic(subproj_ident)
            tar_static_dir = os.path.join(export, 'projectfiles', subproj_ident, 'static')
            tar.add(static_dir, arcname=tar_static_dir)
            # projectfiles\subproj_ident\data -> export\projectfiles\subproj_ident\data
            data_dir = skiboot.projectdata(subproj_ident)
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


def json_submit_saveproject(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "save the project to tarfile projectfiles\project_name\project_name.tar"
    tar_dst = _submit_saveproject(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang)
    page_data[("saveresult","para_text")] = "Project saved in file %s" % tar_dst
    page_data[("saveresult","show_para")] = True
    call_data['status'] = "Project saved"


def html_submit_saveproject(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "save the project to tarfile projectfiles\project_name\export.tar"
    tar_dst = _submit_saveproject(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang)
    call_data['status'] = "Project saved in file %s" % tar_dst


def submit_hex_color(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "set palette background color - from hex"
    adminproj = call_data['adminproj']
    palette = css_styles.hex_int(call_data['hexcol'].lower())
    adminbackcol = css_styles.int_hex(*palette)
    # generate colours
    colours = css_styles.get_colours(*palette)
    # set test colours in proj_data
    skilift.set_proj_data(adminproj.proj_ident, 'adminbackcol', adminbackcol)
    skilift.set_proj_data(adminproj.proj_ident, 'colours', colours)
    # set test colours in defaults.json
    fromjson.set_defaults(adminproj.proj_ident, key="backcol", value=adminbackcol)
    fromjson.set_defaults(adminproj.proj_ident, key="colours", value=colours)
    # change name of 220 to avoid css cache
    newname = "w3-theme-ski-" + str(random.randint(10000, 99999)) + ".css"
    editpage.rename_page(adminproj.proj_ident, 220, newname)


def set_colour(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "sets individual colour string"
    adminproj = call_data['adminproj']
    # get colors from project data
    colours = skilift.get_proj_data(adminproj.proj_ident, 'colours')
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
    skilift.set_proj_data(adminproj.proj_ident, 'colours', colours)
    # set test colours in defaults.json
    fromjson.set_defaults(adminproj.proj_ident, key="colours", value=colours)
    # change name of 220 to avoid css cache
    newname = "w3-theme-ski-" + str(random.randint(10000, 99999)) + ".css"
    editpage.rename_page(adminproj.proj_ident, 220, newname)


def ski_theme(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "set colours into the w3-theme-ski.css page"
    adminproject = skilift.admin_project()
    colours = skilift.get_proj_data(adminproject, 'colours')
    if not colours:
        return {}
    return colours


def set_widgets_css(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "sets default css classes into widgets"
    editedproj = call_data['editedproj']
    off_piste.set_widget_css_to_default(editedproj.proj_ident)
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

       __init__.py             - Package initialisation containing function load_project()

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


def reload_project_code(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Reloads the edited project user code"
    editedproj = call_data['editedproj']
    code_reload(editedproj.proj_ident)
    call_data['status'] = "Project %s code reloaded" % (editedproj.proj_ident,)


def skipole_myapp(editedproj):
    "Create myapp.py file for the tar"
    runfile = """

# this may need to be edited and uncommented so that the skipoles package
# can be found and imported

# import sys
# sys.path.append('/path/to/skipoles')

# for example if the skipoles package (together with projectfiles and myapp.py)
# were in the directory /home/myname/myproject
# then alter the above to:
# sys.path.append('/home/myname/myproject')

# alternatively, the web server may be able to change to this directory
# (see the chdir option of uwsgi)
# or may be able to set a value into pythonpath, so it does not have to be
# done here


import skipoles

_site = skipoles.load_project("%s", {})

def application(environ, start_response):
    "Defines the wsgi application"
    # uses the '_site' object created previously
    status, headers, data = _site.respond(environ)
    start_response(status, headers)
    return data

""" % (editedproj.proj_ident,)
    return runfile



def skipole_run(editedproj):

    proj_ident = editedproj.proj_ident
    proj_brief = editedproj.brief
    proj_version = editedproj.version

    runfile = """#!/usr/bin/env python3

# sys is used for the sys.exit function and to check python version
import sys, argparse

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

site = skipoles.load_project(project, options)

if site is None:
    print("Project not found")
    sys.exit(1)

# This 'site' object can now be used in a wsgi app function
# by calling its 'respond' method, with the environ as argument.
# The method returns status, headers and the page data

def application(environ, start_response):
    "Defines the wsgi application"
    # uses the 'site' object created previously
    status, headers, data = site.respond(environ)
    start_response(status, headers)
    return data

# serve the site

print("Serving on port " + str(port) + "...")
print("Press ctrl-c to stop")

if args.waitress:
    serve(application, host='0.0.0.0', port=port)
else:
    # using the python wsgi web server
    httpd = make_server("", port, application)
    httpd.serve_forever()
""" % (proj_ident, proj_brief, proj_version)
    return runfile

