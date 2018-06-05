####### SKIPOLE WEB FRAMEWORK #######
#
# dump_proj.py  - reads the project content and generates an OrderedDictionary
#
# This file is part of the Skipole web framework
#
# Date : 20150704
#
# Author : Bernard Czenkusz
# Email  : bernie@skipole.co.uk
#
#
#   Copyright 2015 Bernard Czenkusz
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


from collections import OrderedDict

from . import skiboot, excepts, tag, widgets


def part_to_OD(proj_ident, part):
    """Returns an OrderedDictionary of the part"""
    proj = skiboot.getproject(proj_ident)
    # Creates a list of ['Part', dictionary]
    parttext, part_dict = _create_part(part, proj_ident)
    # set version and skipole as the first two items in the dictionary
    part_dict["skipole"] = skiboot.version()
    part_dict.move_to_end('skipole', last=False)
    part_dict["version"] = proj.version
    part_dict.move_to_end('version', last=False)
    return part_dict


def closedpart_to_OD(proj_ident, part):
    """Returns an OrderedDictionary of the part"""
    proj = skiboot.getproject(proj_ident)
    # Creates a list of ['ClosedPart', dictionary]
    parttext, part_dict = _create_closedpart(part, proj_ident)
    # set version and skipole as the first two items in the dictionary
    part_dict["skipole"] = skiboot.version()
    part_dict.move_to_end('skipole', last=False)
    part_dict["version"] = proj.version
    part_dict.move_to_end('version', last=False)
    return part_dict


def widget_to_OD(proj_ident, widget):
    """Returns an OrderedDictionary of the widget"""
    proj = skiboot.getproject(proj_ident)
    # Creates a list of ['Widget', dictionary] or ['ClosedWidget', dictionary]
    parttext, part_dict = _create_widget(widget, proj_ident)
    # set version and skipole as the first two items in the dictionary
    part_dict["skipole"] = skiboot.version()
    part_dict.move_to_end('skipole', last=False)
    part_dict["version"] = proj.version
    part_dict.move_to_end('version', last=False)
    return part_dict


def container_to_OD(proj_ident, container, widget):
    """Returns an OrderedDictionary of the container"""
    proj = skiboot.getproject(proj_ident)
    container_dict = OrderedDict()
    container_dict["version"] = proj.version
    # stores the version of this skipole
    container_dict["skipole"] = skiboot.version()
    # get list of parts in the container
    parts = widget.get_container_parts(container)
    item_list = []
    for item in parts:
        if isinstance(item, widgets.Widget) or isinstance(item, widgets.ClosedWidget):
            item_list.append( _create_widget(item, proj_ident) )
        elif isinstance(item, tag.Part):
            item_list.append( _create_part(item, proj_ident) )
        elif isinstance(item, tag.ClosedPart):
            item_list.append( _create_closedpart(item, proj_ident) )
        elif isinstance(item, tag.TextBlock):
            item_list.append( _create_textblock(item, proj_ident) )
        elif isinstance(item, tag.SectionPlaceHolder):
            item_list.append(_create_sectionplaceholder(item, proj_ident) )
        elif isinstance(item, tag.HTMLSymbol):
            item_list.append( _create_htmlsymbol(item, proj_ident) )
        elif isinstance(item, tag.Comment):
            item_list.append( _create_comment(item, proj_ident) )
        else:
            item_list.append(  _create_text(item, proj_ident) )
    container_dict['container'] = item_list
    return container_dict


def section_to_OD(proj_ident, section_name, section):
    """Returns an OrderedDictionary of the section"""
    proj = skiboot.getproject(proj_ident)
    section_dict = OrderedDict()
    section_dict['name'] = section_name
    section_dict["version"] = proj.version
    # stores the version of this skipole
    section_dict["skipole"] = skiboot.version()
    sectiontext, section_dict = _create_section(section_dict, section, proj_ident)
    return section_dict


def templatepage_to_OD(proj_ident, page):
    """Returns an OrderedDictionary of the template page"""
    proj = skiboot.getproject(proj_ident)
    ident = page.ident
    page_dict = OrderedDict()
    page_dict["name"] = page.name
    page_dict["version"] = proj.version
    # stores the version of this skipole
    page_dict["skipole"] = skiboot.version()
    page_dict["ident"] = ident.num
    if page.brief:
        page_dict["brief"] = page.brief
    return _create_templatepage(page_dict, page, ident, proj_ident)


def svg_to_OD(proj_ident, page):
    """Returns an OrderedDictionary of the svg page"""
    proj = skiboot.getproject(proj_ident)
    ident = page.ident
    page_dict = OrderedDict()
    page_dict["name"] = page.name
    page_dict["version"] = proj.version
    # stores the version of this skipole
    page_dict["skipole"] = skiboot.version()
    page_dict["ident"] = ident.num
    if page.brief:
        page_dict["brief"] = page.brief
    return _create_svgpage(page_dict, page, ident, proj_ident)


def folder_to_OD(proj_ident, folder):
    """Returns an OrderedDictionary of the folder"""
    proj = skiboot.getproject(proj_ident)
    ident = folder.ident
    if ident.num:
        folder_dict = _create_folder(ident, proj_ident)
    else:
        folder_dict = _create_root_folder(proj_ident)
    # stores the version of this skipole
    folder_dict["skipole"] = skiboot.version()
    folder_dict.move_to_end("skipole", last=False)
    folder_dict["version"] = proj.version
    folder_dict.move_to_end("version", last=False)
    folder_dict["name"] = folder.name
    folder_dict.move_to_end("name", last=False)
    return folder_dict


def project_to_OD(proj_ident=None):
    """Returns an OrderedDictionary of the project"""
    if proj_ident is None:
        proj_ident = skiboot.project_ident()
    # proj is the actual Project instance to be dumped
    proj = skiboot.getproject(proj_ident)

    # create a big ordered dictionary
    project = OrderedDict()

    project["url"] = proj.url
    project["default_language"] = proj.default_language
    brief = proj.brief
    if not brief:
        project["brief"] = "Project : %s" % (proj_ident,)
    else:
        project["brief"] = brief
    project["version"] = proj.version

    # stores the version of this skipole
    project["skipole"] = skiboot.version()

    # proj.subproject_dicts is a dictionary of {proj_ident: {'path':path,...}}
    # currently only path is stored, but other project items could be stored
    subprojects = proj.subproject_dicts
    if skiboot.admin_project() in subprojects:
        del subprojects[skiboot.admin_project()]
    if subprojects:
        project["subprojects"] = OrderedDict(sorted(subprojects.items(), key=lambda t: t[0]))
    else:
        project["subprojects"] = OrderedDict()

    specialpages = {}
    specpages = proj.special_pages
    if specpages:
        for label, target in specpages.items():
            if isinstance(target, skiboot.Ident):
                if target.proj == proj_ident:
                    specialpages[label] = target.num
                else:
                    specialpages[label] = str(target)
            else:
                specialpages[label] = target
        project["specialpages"] = OrderedDict(sorted(specialpages.items(), key=lambda t: t[0]))
    else:
        project["specialpages"] = OrderedDict()

    sections = OrderedDict()
    projsections = proj.sections
    if projsections:
        for section_name, section in projsections.items():
            section_dict = OrderedDict()
            sections[section_name] = _create_section(section_dict, section, proj_ident)
        project["sections"] = OrderedDict(sorted(sections.items(), key=lambda t: t[0]))
    else:
        project["sections"] = OrderedDict()

    # add rootfolder to the project
    project["RootFolder"] = _create_root_folder(proj_ident)

    return project


def _create_root_folder(proj_ident):
    "Creates a dictionary for the root folder"
    if proj_ident is None:
        proj_ident = skiboot.project_ident()
    proj = skiboot.getproject(proj_ident)
    # rootfolder is the OrderedDict to return
    rootfolder = OrderedDict()
    root = proj.root
    brief = root.brief
    if not brief:
        rootfolder["brief"] = "Root folder"
    else:
        rootfolder["brief"] = brief
    default_page_name = root.default_page_name
    if default_page_name:
        rootfolder["default_page_name"] = default_page_name
    rootfolder["restricted"] = False
    # folders in root
    root_folders = OrderedDict()
    folders = root.folders
    if folders:
        for foldername, ident in folders.items():
            root_folders[foldername] = _create_folder(ident, proj_ident)
        rootfolder["folders"] = OrderedDict(sorted(root_folders.items(), key=lambda t: t[0]))
    else:
        rootfolder["folders"] = OrderedDict()
    # pages in root
    root_pages = {}
    pages = root.pages
    if pages:
        for pagename, ident in pages.items():
            root_pages[pagename] = _create_page(ident, proj_ident)
        rootfolder["pages"] = OrderedDict(sorted(root_pages.items(), key=lambda t: t[0]))
    else:
        rootfolder["pages"] = OrderedDict()
    return rootfolder


def _create_folder(ident, proj_ident):
    "Creates a dictionary for the folder"
    proj = skiboot.getproject(proj_ident)
    folder_dict = OrderedDict()
    folder = proj.identitems[ident]

    folder_dict["ident"] = ident.num
    if folder.brief:
        folder_dict["brief"] = folder.brief
    if folder.default_page_name:
        folder_dict["default_page_name"] = folder.default_page_name
    folder_dict["restricted"] = folder.restricted

    # folders in this folder
    sub_folders = {}
    folders = folder.folders
    if folders:
        for foldername, folderident in folders.items():
            sub_folders[foldername] = _create_folder(folderident, proj_ident)
        folder_dict["folders"] = OrderedDict(sorted(sub_folders.items(), key=lambda t: t[0]))
    else:
        folder_dict["folders"] = OrderedDict()

    # pages in this folder
    pages_dict = {}
    pages = folder.pages
    if pages:
        for pagename, pageident in pages.items():
            pages_dict[pagename] = _create_page(pageident, proj_ident)
        folder_dict["pages"] = OrderedDict(sorted(pages_dict.items(), key=lambda t: t[0]))
    else:
        folder_dict["pages"] = OrderedDict()

    return folder_dict


def _create_page(ident, proj_ident):
    "Creates a dictionary for the page"
    proj = skiboot.getproject(proj_ident)
    page_dict = OrderedDict()
    page = proj.identitems[ident]
    page_dict["ident"] = ident.num
    if page.brief:
        page_dict["brief"] = page.brief
    if page.page_type == 'FilePage':
        return _create_filepage(page_dict, page, ident, proj_ident)
    elif page.page_type == 'RespondPage':
        return _create_respondpage(page_dict, page, ident, proj_ident)
    elif page.page_type == 'CSS':
        return _create_csspage(page_dict, page, ident, proj_ident)
    elif page.page_type == 'JSON':
        return _create_jsonpage(page_dict, page, ident, proj_ident)
    elif page.page_type == 'SVG':
        return _create_svgpage(page_dict, page, ident, proj_ident)
    elif page.page_type == 'TemplatePage':
        return _create_templatepage(page_dict, page, ident, proj_ident)
    else:
        return OrderedDict()


def _make_dictionary(input_dict, proj_ident):
    """Used by other functions, takes input_dict and returns
       an ordered dict, with TextBlocks, idents converted for json compatability"""
    output_dict = OrderedDict()
    if not input_dict: return output_dict
    for key, val in input_dict.items():
        if val is None:
            output_dict[key] = None
        elif val is '':
            output_dict[key] = ""
        elif isinstance(val, list):
            output_dict[key] = _make_list(val, proj_ident)
        elif isinstance(val, dict):
            output_dict[key] = _make_dictionary(val, proj_ident)
        elif val is True:
            output_dict[key] = True
        elif val is False:
            output_dict[key] = False
        elif isinstance(val, tag.TextBlock):
            output_dict[key] = val.textref
        elif isinstance(val, skiboot.Ident):
            if val.proj == proj_ident:
                # ident is this project, put the number only
                output_dict[key] = val.num
            else:
                # ident is another project, put the full ident
                output_dict[key] = [val.proj, val.num]
        else:
            output_dict[key] = str(val)
    return output_dict


def _make_list(input_list, proj_ident):
    """Used by other functions, takes input_list and returns a list with items converted"""
    if not input_list: return []
    output_list = []
    for item in input_list:
        if item is None:
            output_list.append(None)
        elif item is '':
            output_list.append('')
        elif isinstance(item, list):
            output_list.append(_make_list(item, proj_ident))
        elif isinstance(item, dict):
            output_list.append(_make_dictionary(item, proj_ident))
        elif item is True:
            output_list.append(True)
        elif item is False:
            output_list.append(False)
        elif isinstance(item, skiboot.Ident):
            if item.proj == proj_ident:
                output_list.append(item.num)
            else:
                # ident is another project, put the full ident
                output_list.append([item.proj, item.num])
        else:
            output_list.append(str(item))
    return output_list


def _create_filepage(page_dict, page, ident, proj_ident):
    "Creates a dictionary for the filepage"
    page_args = OrderedDict()
    page_args["filepath"] = page.filepath
    page_args["enable_cache"] = page.enable_cache
    if page.mimetype:
        page_args["mimetype"] = page.mimetype

    page_dict["FilePage"] = page_args
    return page_dict


def _create_respondpage(page_dict, page, ident, proj_ident):
    "Creates a dictionary for the respondpage"
    page_args = OrderedDict()
    page_args["class"] = page.responder.__class__.__name__
    original_args = OrderedDict(sorted(page.responder.original_args().items(), key=lambda t: t[0]))
    page_args["original_args"] = _make_dictionary(original_args, proj_ident)
    original_fields = OrderedDict(sorted(page.responder.original_fields().items(), key=lambda t: t[0]))
    page_args["original_fields"] = _make_dictionary(original_fields, proj_ident)
    page_dict["RespondPage"] = page_args
    return page_dict


def _create_csspage(page_dict, page, ident, proj_ident):
    "Creates a dictionary for the page"
    page_args = OrderedDict()
    page_args["enable_cache"] = page.enable_cache
    page_args["style"] = _make_dictionary(page.style, proj_ident)
    page_dict["CSS"] = page_args
    return page_dict


def _create_jsonpage(page_dict, page, ident, proj_ident):
    "Creates a dictionary for the page"
    page_args = OrderedDict()
    page_args["enable_cache"] = page.enable_cache
    page_args["content"] = OrderedDict()
    if page.content:
        page_args["content"] = _make_dictionary(page.content, proj_ident)
    page_dict["JSON"] = page_args
    return page_dict


def _create_svgpage(page_dict, page, ident, proj_ident):
    "Creates a dictionary for the page"
    page_args = OrderedDict()
    page_args["enable_cache"] = page.enable_cache
    page_args["width"] = str(page.width)
    page_args["height"] = str(page.height)
    if page.css_list:
        page_args["css_list"] = _make_list(page.css_list, proj_ident)
    page_dict["SVG"] = page_args
    page_dict["svg"] = _create_part(page.svg, proj_ident)

    return page_dict


def _create_templatepage(page_dict, page, ident, proj_ident):
    "Creates a dictionary for the page"
    page_args = OrderedDict()

    page_args["show_backcol"] = page.show_backcol
    page_args["last_scroll"] = page.last_scroll
    page_args["interval"] = page.interval

    # convert page.interval_target to ident, label or None
    interval_target = skiboot.make_ident_or_label(page.interval_target, proj_ident)
    if isinstance(interval_target, skiboot.Ident):
        if interval_target.proj == proj_ident:
            page_args["interval_target"] = interval_target.num
        else:
            # ident is another project, put the full ident
            page_args["interval_target"] = interval_target.to_comma_str()
    else:
        # interval_target is label or None
        page_args["interval_target"] = interval_target

    page_args["lang"] = page.lang
    if page.backcol:
        page_args["backcol"] = page.backcol

    if page.default_error_widget:
        page_args["default_error_widget"] = page.default_error_widget.sw_tuple()

    page_dict["TemplatePage"] = page_args
    page_dict["head"] = _create_part(page.head, proj_ident)
    page_dict["body"] = _create_part(page.body, proj_ident)

    return page_dict


def _create_part(part, proj_ident):
    "Creates a list of ['Part', dictionary]"
    part_dict = OrderedDict()
    part_dict["tag_name"] = part.tag_name
    if part.brief:
        part_dict["brief"] = part.brief
    part_dict["show"] = part.show
    part_dict["hide_if_empty"] = part.hide_if_empty
    if part.attribs:
        part_attribs = OrderedDict(sorted(part.attribs.items(), key=lambda t: t[0]))
        part_dict["attribs"] = _make_dictionary(part_attribs, proj_ident)
    # now the Part contents in a list
    parts = []
    for item in part:
        if isinstance(item, widgets.Widget) or isinstance(item, widgets.ClosedWidget):
            parts.append(_create_widget(item, proj_ident))
        elif isinstance(item, tag.Part):
            parts.append(_create_part(item, proj_ident))
        elif isinstance(item, tag.ClosedPart):
            parts.append(_create_closedpart(item, proj_ident))
        elif isinstance(item, tag.TextBlock):
            parts.append(_create_textblock(item, proj_ident))
        elif isinstance(item, tag.SectionPlaceHolder):
            parts.append(_create_sectionplaceholder(item, proj_ident))
        elif isinstance(item, tag.HTMLSymbol):
            parts.append(_create_htmlsymbol(item, proj_ident))
        elif isinstance(item, tag.Comment):
            parts.append(_create_comment(item, proj_ident))
        else:
            parts.append(_create_text(item, proj_ident))
    part_dict["parts"] = parts
    return ['Part', part_dict]


def _create_closedpart(part, proj_ident):
    "Creates a list of ['ClosedPart', dictionary]"
    part_dict = OrderedDict()
    part_dict["tag_name"] = part.tag_name
    if part.brief:
        part_dict["brief"] = part.brief
    part_dict["show"] = part.show
    if part.attribs:
        part_attribs = OrderedDict(sorted(part.attribs.items(), key=lambda t: t[0]))
        part_dict["attribs"] = _make_dictionary(part_attribs, proj_ident)
    return ['ClosedPart', part_dict]


def _create_textblock(part, proj_ident):
    "Creates a list of ['TextBlock', dictionary]"
    part_dict = OrderedDict()
    part_dict["textref"] = part.textref
    if part.text:
        part_dict["text"] = part.text
    if part.failmessage:
        part_dict["failmessage"] = part.failmessage
    part_dict["show"] = part.show
    part_dict["escape"] = part.escape
    part_dict["linebreaks"] = part.linebreaks
    part_dict["decode"] = part.decode
    if part.replace_strings:
        part_dict["replace_strings"] = _make_list(part.replace_strings, proj_ident)
    return ['TextBlock', part_dict]


def _create_section(part_dict, part, proj_ident):
    "Creates a list of ['Section', dictionary]"
    part_dict["tag_name"] = part.tag_name
    if part.brief:
        part_dict["brief"] = part.brief
    part_dict["show"] = part.show
    part_dict["hide_if_empty"] = part.hide_if_empty
    if part.attribs:
        part_attribs = OrderedDict(sorted(part.attribs.items(), key=lambda t: t[0]))
        part_dict["attribs"] = _make_dictionary(part_attribs, proj_ident)
    # now the Part contents in a list
    parts = []
    for item in part:
        if isinstance(item, widgets.Widget) or isinstance(item, widgets.ClosedWidget):
            parts.append(_create_widget(item, proj_ident))
        elif isinstance(item, tag.Part):
            parts.append(_create_part(item, proj_ident))
        elif isinstance(item, tag.ClosedPart):
            parts.append(_create_closedpart(item, proj_ident))
        elif isinstance(item, tag.TextBlock):
            parts.append(_create_textblock(item, proj_ident))
        elif isinstance(item, tag.SectionPlaceHolder):
            parts.append(_create_sectionplaceholder(item, proj_ident))
        elif isinstance(item, tag.HTMLSymbol):
            parts.append(_create_htmlsymbol(item, proj_ident))
        elif isinstance(item, tag.Comment):
            parts.append(_create_comment(item, proj_ident))
        else:
            parts.append(_create_text(item, proj_ident))
    part_dict["parts"] = parts
    return ['Section', part_dict]



def _create_sectionplaceholder(part, proj_ident):
    "Creates a list of ['SectionPlaceHolder', dictionary]"
    part_dict = OrderedDict()
    if part.brief:
        part_dict["brief"] = part.brief
    if part.section_name:
        part_dict["section_name"] = part.section_name
    if part.placename:
        part_dict["placename"] = part.placename
    part_dict["multiplier"] = part.multiplier
    part_dict["mtag"] = part.mtag
    return ['SectionPlaceHolder', part_dict]


def _create_htmlsymbol(part, proj_ident):
    "Creates a list of ['HTMLSymbol', dictionary]"
    part_dict = OrderedDict()
    part_dict["text"] = part.text
    return ['HTMLSymbol', part_dict]


def _create_comment(part, proj_ident):
    "Creates a list of ['Comment', dictionary]"
    part_dict = OrderedDict()
    part_dict["text"] = part.text
    return ['Comment', part_dict]


def _create_text(part, proj_ident):
    "Creates a list of ['Text', text]"
    return ['Text', str(part)]

def _create_widget(widg, proj_ident):
    part_dict = OrderedDict()
    w_mod = widg.__module__.split(".")[-1]
    part_dict['class'] = "%s.%s" % (w_mod, widg.__class__.__name__)
    if widg.name:
        part_dict["name"] = widg.name
    if widg.brief:
        part_dict["brief"] = widg.brief
    fields_dict = {f_arg: f.value for f_arg, f in widg.fields.items()}
    if fields_dict:
        ordered_fields_dict = OrderedDict(sorted(fields_dict.items(), key=lambda t: t[0]))
        part_dict["fields"] = _make_dictionary(ordered_fields_dict, proj_ident)
    # set widget containers
    if widg.can_contain():
        for cont in range(widg.len_containers()):
            container_name = "container_%s" % (cont,)
            # get list of parts in the container
            parts = widg.get_container_parts(cont)
            item_list = []
            for item in parts:
                if isinstance(item, widgets.Widget) or isinstance(item, widgets.ClosedWidget):
                    item_list.append( _create_widget(item, proj_ident) )
                elif isinstance(item, tag.Part):
                    item_list.append( _create_part(item, proj_ident) )
                elif isinstance(item, tag.ClosedPart):
                    item_list.append( _create_closedpart(item, proj_ident) )
                elif isinstance(item, tag.TextBlock):
                    item_list.append( _create_textblock(item, proj_ident) )
                elif isinstance(item, tag.SectionPlaceHolder):
                    item_list.append(_create_sectionplaceholder(item, proj_ident))
                elif isinstance(item, tag.HTMLSymbol):
                    item_list.append( _create_htmlsymbol(item, proj_ident) )
                elif isinstance(item, tag.Comment):
                    item_list.append( _create_comment(item, proj_ident) )
                else:
                    item_list.append(  _create_text(item, proj_ident) )
            part_dict[container_name] = item_list
    # set widget field names
    if fields_dict:
        # check if any field name is not equal to f_arg
        fields_names = {f_arg:f.name for f_arg, f in widg.fields.items() if f_arg != f.name}
        if fields_names:
            ordered_fields_names = OrderedDict(sorted(fields_names.items(), key=lambda t: t[0]))
            part_dict["set_names"] = _make_dictionary(ordered_fields_names, proj_ident)
        # set widget validators
        field_validators = {f.name:f.val_list for f in widg.fields.values() if f.val_list}
        if field_validators:
            val_dict = {}
            for name, val_list in field_validators.items():
                val_dict[name] = _create_validator_list(val_list, proj_ident)
            part_dict["validators"] = OrderedDict(sorted(val_dict.items(), key=lambda t: t[0]))

    if isinstance(widg, widgets.Widget):
        return ['Widget', part_dict]
    elif isinstance(widg, widgets.ClosedWidget):
        return ['ClosedWidget', part_dict]
    else:
        return []


def _create_validator_list(val_list, proj_ident):
    v_list = []
    for validator in val_list:
        val_dict = OrderedDict()
        v_mod = validator.__module__.split(".")[-1]
        val_dict['class'] = "%s.%s" % (v_mod, validator.__class__.__name__)
        # now write the validator fields
        if validator.message:
            val_dict["message"] = validator.message
        if validator.message_ref:
            val_dict["message_ref"] = validator.message_ref
        if validator.displaywidget:
            val_dict["displaywidget"] = validator.displaywidget.to_tuple()
        allowed_values = validator.allowed_values
        if allowed_values:
            val_dict["allowed_values"] = _make_list(allowed_values, proj_ident)
        val_args = {}
        if validator.val_args:
            val_args = OrderedDict(sorted(validator.val_args.items(), key=lambda t: t[0]))
            val_dict["val_args"] = _make_dictionary(val_args, proj_ident)
        v_list.append(val_dict)
    return v_list

