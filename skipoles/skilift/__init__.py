####### SKIPOLE WEB FRAMEWORK #######
#
# __init__.py of skilift package  - Defines interface to ski functions
#
# This file is part of the Skipole web framework
#
# Date : 20160509
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


"""Functions that access the ski framework"""

import os
from collections import namedtuple

from ..ski.excepts import FailPage, GoTo, ValidateError, ServerError

from ..ski import skiboot


ItemInfo = namedtuple('ItemInfo', ['project', 'project_version', 'itemnumber', 'item_type', 'name', 'brief', 'path', 'label_list', 'change', 'parentfolder_number', 'restricted'])

PartInfo = namedtuple('PartInfo', ['project', 'pagenumber', 'page_part', 'section_name', 'widget_name', 'container_number', 'location_list', 'part_type'])

PageInfo = namedtuple('PageInfo', ['name', 'number', 'restricted', 'brief', 'item_type', 'responder'])

FolderInfo = namedtuple('FolderInfo', ['name', 'number', 'restricted', 'brief', 'contains_pages', 'contains_folders'])


def project_loaded(project, error_if_not=True):
    "Returns True if the project is loaded, False if not, or raise ServerError"
    if isinstance(project, str) and skiboot.is_project(project):
        return True
    if error_if_not:
        raise ServerError(message="The project has not been loaded")
    return False


def get_root():
    "Returns the root project name"
    return skiboot.project_ident()

def admin_project():
    "Returns the ski admin project name"
    return skiboot.admin_project()

def get_proj_data(project, key):
    "Returns the value from the proj_data dictionary, or None if not found"
    # raise error if invalid project
    project_loaded(project)
    proj = skiboot.getproject(project)
    if proj is None:
        return
    return proj.proj_data.get(key)

def set_proj_data(project, key, value):
    "Sets the key, value in the proj_data dictionary"
    # raise error if invalid project
    project_loaded(project)
    proj = skiboot.getproject(project)
    if proj is None:
        return
    proj.proj_data[key] = value

def get_projectfiles_dir(project=None):
    """If project not given, returns the projectfiles directory path
       If project is given, returns the projectfiles/project directory path"""
    if project:
        return os.path.join(skiboot.projectfiles(), project)
    else:
        return skiboot.projectfiles()


def get_textblock_text(textref, lang, project=None):
    """Gets the textblock text, given a textref, if text for a given lang is not found, makes an
       effort to still get text, if project not given assumes
       the root project, project must exist as either the root, or a sub project of the root
       returns None if nothing found"""
    if project is None:
        project = skiboot.project_ident()
    # raise error if invalid project
    project_loaded(project)
    proj = skiboot.getproject(project)
    if proj is None:
        return ''
    return proj.textblocks_get_text(textref, lang)


def item_info(project, itemnumber):
    """Returns None if page or folder not found, otherwise returns a namedtuple with contents
       project, project_version, itemnumber, item_type, name, brief, path, label_list, change, parentfolder_number, restricted
    """
    # raise error if invalid project
    project_loaded(project)
    if not isinstance(itemnumber, int):
         raise ServerError(message="Given itemnumber is not an integer")
    ident = skiboot.Ident.to_ident((project, itemnumber))
    if ident is None:
        return
    info = skiboot.item_info(ident)
    if not info:
        return
    if info.parentfolder_ident:
        parentfolder_number = info.parentfolder_ident.num
    else:
        parentfolder_number = None

    return ItemInfo(
                   project,
                   info.project_version,
                   itemnumber,
                   info.item_type,
                   info.name,
                   info.brief,
                   info.path,
                   info.label_list,
                   info.change,
                   parentfolder_number,
                   info.restricted
                   )


def part_info(project, pagenumber, section_name, location):
    """location is a tuple or list consisting of three items:
       a string (such as head or section name or widget name)
       a container integer, such as 0 for widget container 0, or None if not in container
       a tuple or list of location integers
       returns None if part not found, otherwise returns a namedtuple with items
       project, pagenumber, page_part, section_name, widget_name, container_number, location_list, part_type
    """
    # raise error if invalid project
    project_loaded(project)

    location_string, container_number, location_list = location

    ident = None
    page_part = None
    widget_name = None
    part_type = None

    # get page or section - an error if both are present
    if pagenumber is not None:
        if section_name:
            # page and section should not both be given
            return
        ident = skiboot.find_ident(pagenumber, project)
        if not ident:
            return
        page = skiboot.get_item(ident)
        if not page:
            return
        if (page.page_type != "TemplatePage") and (page.page_type != "SVG"):
            return
        if (location_string == 'head') or (location_string == 'body') or (location_string == 'svg'):
            # part not in a widget
            page_part = location_string
        else:
            widget_name = location_string
            # find page_part containing widget
            widget = page.widgets[widget_name]
            if widget is not None:
               ident_top = widget.ident_string.split("-", 1)
               # ident_top[0] will be of the form proj_pagenum_head
               page_part = ident_top[0].split("_")[2]
    elif section_name:
        # location_string is either a section_name or a widget
        if location_string != section_name:
            widget_name = location_string
    else:
        # return None
        return

    part = skiboot.get_part(project, ident, page_part, section_name, widget_name, container_number, location_list)
    if part is None:
        return

    if hasattr(part, '__class__'):
        part_type = part.__class__.__name__

    return PartInfo(project, pagenumber, page_part, section_name, widget_name, container_number, location_list, part_type)


def ident_exists(project, itemnumber):
    "Return True if ident exists, False otherwise"
    return skiboot.ident_exists((project, itemnumber))


def ident_numbers(project=None):
    "Returns a list of the project ident numbers"
    num_list = [0]
    if project is None:
        project = skiboot.project_ident()
    # raise error if invalid project
    project_loaded(project)
    proj = skiboot.getproject(project)
    if proj is None:
        return []
    return proj.ident_numbers


def labels(project=None):
    "return dictionary of labels to page, folder tuple idents or urls"
    if project is None:
        project = skiboot.project_ident()
    # raise error if invalid project
    project_loaded(project)
    proj = skiboot.getproject(project)
    if proj is None:
        return {}
    return proj.labels()


def projectURLpaths():
    "Returns a dictionary of project name : project path"
    rootproject = skiboot.getproject()
    paths = {ident:path for ident,path in rootproject.subproject_urls.items()}
    paths[rootproject.proj_ident] = rootproject.url
    return paths



def pages(project, foldernumber):
    """Returns generator of PageInfo named tuples, one for each page in the folder"""
    # raise error if invalid project
    project_loaded(project)
    proj = skiboot.getproject(project)
    folder_ident = skiboot.Ident(project, foldernumber)
    folder = proj.get_item(folder_ident)
    if folder is None:
        raise ServerError("Folder not recognised")
    for page_ident in folder.page_idents():
        page = proj.get_item(page_ident)
        if page.page_type == 'RespondPage':
            responder = page.responder.__class__.__name__
        else:
            responder = ''
        yield PageInfo(page.name, page.ident.num, page.restricted, page.brief, page.page_type, responder)


def page_info(project, pagenumber):
    """Returns PageInfo named tuple for page"""
    # raise error if invalid project
    project_loaded(project)
    proj = skiboot.getproject(project)
    page_ident = skiboot.Ident(project, pagenumber)
    page = proj.get_item(page_ident)
    if page is None:
        raise ServerError("Page not recognised")
    if page.page_type == 'RespondPage':
        responder = page.responder.__class__.__name__
    else:
        responder = ''
    return PageInfo(page.name, page.ident.num, page.restricted, page.brief, page.page_type, responder)


def folders(project, foldernumber):
    """Returns generator of FolderInfo named tuples, one for each sub folders in the folder"""
    # raise error if invalid project
    project_loaded(project)
    proj = skiboot.getproject(project)
    folder_ident = skiboot.Ident(project, foldernumber)
    folder = proj.get_item(folder_ident)
    if folder is None:
        raise ServerError("Folder not recognised")
    for subfolder_ident in folder.folder_idents():
        subfolder = proj.get_item(subfolder_ident)
        yield FolderInfo(subfolder.name, subfolder.ident.num, subfolder.restricted, subfolder.brief, bool(subfolder.pages), bool(subfolder.folders))


def folder_info(project, foldernumber):
    """Returns FolderInfo named tuple for folder"""
    # raise error if invalid project
    project_loaded(project)
    proj = skiboot.getproject(project)
    folder_ident = skiboot.Ident(project, foldernumber)
    folder = proj.get_item(folder_ident)
    if folder is None:
        raise ServerError("Folder not recognised")
    return FolderInfo(folder.name, folder.ident.num, folder.restricted, folder.brief, bool(folder.pages), bool(folder.folders))


def folder_page_names(project, foldernumber):
    """Returns tuple of (default_page_name, [page names,....]) where default_page_name is None if no default page has been set
       and the page names list is empty if no pages are present. The page names list is sorted."""
    # raise error if invalid project
    project_loaded(project)
    proj = skiboot.getproject(project)
    folder_ident = skiboot.Ident(project, foldernumber)
    folder = proj.get_item(folder_ident)
    if folder is None:
        raise ServerError("Folder not recognised")
    # folder.pages is a dictionary of page.name:page.ident
    if not folder.pages:
        return None, []
    page_names = list(folder.pages.keys())
    page_names.sort()
    if folder.default_page_name:
        return folder.default_page_name, page_names
    return None, page_names


def parent_list(project, itemnumber):
    """Returns list of [(name,number),...] of parents, starting with ('root',0) ending with name and number of item"""
    # raise error if invalid project
    project_loaded(project)
    proj = skiboot.getproject(project)
    item_ident = skiboot.Ident(project, itemnumber)
    item = proj.get_item(item_ident)
    if item is None:
        raise ServerError("Item not recognised")
    return item.parent_list()



