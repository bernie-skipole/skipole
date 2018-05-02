####### SKIPOLE WEB FRAMEWORK #######
#
# off_piste.py  - Specialist functions
#
# This file is part of the Skipole web framework
#
# Date : 20160114
#
# Author : Bernard Czenkusz
# Email  : bernie@skipole.co.uk
#
#
#   Copyright 2016 Bernard Czenkusz
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

"""
Somewhat risky functions, hence 'off_piste'.

"""

import copy, os, json, collections

from ..ski import skiboot, tag, widgets
from ..ski.excepts import ServerError

from . import project_loaded


def _get_proj(project):
    "Returns the Project with name project"
    project_loaded(project)
    return skiboot.getproject(project)


def _get_project_template_pages(project):
    "yields all template pages in the project"
    proj = _get_proj(project)
    identitems = proj.identitems
    for ident, item  in identitems.items():
        # item is taken direct from the project without copying or importing sections
        if item.page_type == 'TemplatePage':
            yield item


def set_widget_field_value(project, widget_name, widget_field_name, new_value, new_brief=None):
    """For each template page, with a given widget name and field name, set the field value, and widget brief.
       The field can only be a single value field - as can be edited on the admin pages, not dictionary, table
       or list fields which are dynamically set.
       If no brief is given, or an empty string is given, then the brief is not changed"""
    field_value = str(new_value)
    proj = _get_proj(project)
    for page in _get_project_template_pages(project):
        if widget_name in page.widgets:
            widget = page.widgets[widget_name]
            field_arg = widget.get_field_arg(widget_field_name)
            if field_arg is None:
                continue
            field_info = widget.field_arg_info(field_arg)
            # (field name, field description ref, fieldvalue, str_fieldvalue, fieldarg class string, field type, field.valdt, field.jsonset, field.cssclass, field.csstyle)
            if field_info[4] != 'args':
                raise ServerError(message="Invalid field type in widget in page %s " % (page.ident,))
            if (field_info[5] == "ident" or field_info[5] == "url") and field_value.isdigit():
                # A digit is being input as a page ident
                field_value = project + '_' + field_value
            widget.set_field_value(field_arg, field_value)
            if new_brief:
                widget.brief = new_brief
            proj.save_page(page)


def insert_div_in_body(project, css_class, brief):
    """Inserts a div with the given css class attribute as the containing div in each template page body
       unless a div with this class already exists at this point.
       Sets the body div brief with the brief given here"""
    proj = _get_proj(project)
    for page in _get_project_template_pages(project):
        body = page.body
        if (len(body) == 1) and hasattr(body[0], 'attribs') and body[0].get_attrib_value('class'):
            # body has one item with a class attribute
            if body[0].get_attrib_value('class') == css_class:
                # container div already exists
                if body[0].brief != brief:
                    body[0].brief = brief
                    itemlist.append(page)
                continue
        # so insert a div
        contents = copy.deepcopy(body.parts)
        newdiv = tag.Part(tag_name='div', attribs={'class':css_class}, brief=brief)
        newdiv.parts = contents
        body.parts = [newdiv]
        proj.save_page(page)


def set_backcol_in_pages(project, backcol):
    "Sets a background colour in the <html> tags of template pages"
    proj = _get_proj(project)
    for page in _get_project_template_pages(project):
        page.backcol = backcol
        proj.save_page(page)


def set_bodyclass_in_pages(project, bodyclass):
    "Sets the CSS class into the <body> tags of template pages"
    proj = _get_proj(project)
    for page in _get_project_template_pages(project):
        page.body.set_class(bodyclass)
        proj.save_page(page)


def append_scriptlink_in_pages(project, label):
    "Appends a script link to the head of each page"
    proj = _get_proj(project)
    if "/" in label:
        scriptlink = tag.Part(tag_name = "script", attribs={"src":label}, brief='script link to %s' % (label,))
    else:
        scriptlink = tag.Part(tag_name = "script", attribs={"src":"{" + label + "}"}, brief='script link to %s' % (label,))
    for page in _get_project_template_pages(project):
        page.head.append(scriptlink)
        proj.save_page(page)


def set_widget_css_to_default(project):
    """For each template page, set all widget css class fields to their default values, if a default has been set
          Note: does not change widgets in sections or svg pages"""
    proj = _get_proj(project)
    defaults = {}
    defaultsfile = skiboot.project_defaults(proj_ident=project)
    if os.path.isfile(defaultsfile):
        # load defaultsfile into defaults
        with open(defaultsfile, 'r') as fp:
            defaults = json.load(fp, object_pairs_hook=collections.OrderedDict)
    else:
        return
    if not defaults:
        return
    if 'widgets' not in defaults:
        return
    widget_defaults = defaults['widgets']
    # widget_defaults is a dictionary with keys of widget modules, and values which are themselves dictionaries
    # the value dictionaries have keys of the widget class, and values which are dictionaries of field:css class
    for page in _get_project_template_pages(project):
        change_flag = False
        for widget in page.widgets.values():
            widget_module = widget.__class__.__module__.split('.')[-1]
            widget_class = widget.__class__.__name__
            field_css = {}
            if (widget_module in widget_defaults) and (widget_class in widget_defaults[widget_module]):
                field_css = widget_defaults[widget_module][widget_class]
            else:
                continue
            if not field_css:
                continue                
            # for each css field in the widget, if it has a default in field_css, set it
            args, arg_list, arg_table, arg_dict = widget.classargs()
            for field in args:
                field_arg = field[0]
                field_type = field[2]
                if field_type != 'cssclass':
                    continue
                if (field_arg in field_css) and (field_css[field_arg]):
                    widget.set_field_value(field_arg, field_css[field_arg])
                    change_flag = True
        if change_flag:
            proj.save_page(page)


def insert_css_link(project, label, brief):
    """For each template page, insert a css link to the given label, in the page head, before the element with the given brief"""
    if "/" in label:
        csslink = tag.ClosedPart(tag_name = "link",
                       attribs={"href":label,
                                "rel":"stylesheet",
                                "type":"text/css"},
                       brief='css link to %s' % (label,))
    else:
        csslink = tag.ClosedPart(tag_name = "link",
                       attribs={"href":"{" + label + "}",
                                "rel":"stylesheet",
                                "type":"text/css"},
                       brief='css link to %s' % (label,))
    proj = _get_proj(project)
    for page in _get_project_template_pages(project):
        head = page.head
        index = 0
        for part in head:
            if hasattr(part, 'brief') and (part.brief == brief):
                break
            index += 1
        else:
            continue
        head.insert(index, csslink)
        proj.save_page(page)


def set_css_class(project, brief, cssclass):
    """For each element within a template page body, if it has a given brief, set its class attribute
       return number of changes"""
    count = 0
    proj = _get_proj(project)
    for page in _get_project_template_pages(project):
        body = page.body
        for part in body:
            count = _set_class_part(part, brief, cssclass, count)
        proj.save_page(page)
    return count


def _set_class_part(part, brief, cssclass, count):
    "Used by set_css_class"
    if hasattr(part, 'brief') and (part.brief == brief):
        part.set_class(cssclass)
        count += 1
    if isinstance(part, tag.Part):
        for subpart in part:
            count = _set_class_part(subpart, brief, cssclass, count)
    return count




