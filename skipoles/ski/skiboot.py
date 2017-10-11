####### SKIPOLE WEB FRAMEWORK #######
#
# skiboot.py  - Holds common functions and variables for skipole
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

"""
This module defines a number of functions and classes used throughout
the program.
"""

import os, copy, collections

# Configuration defaults

_CFG = {
"new_project"     : "newproj",           # copied to create a new project
"admin_project"   : "skiadmin",          # The skipole admin project
"lib_project"     : "lib",               # The skipole static library project
"version"         : "0.0.39",            # The skipole version
"default_language": 'en',                # The default language of the project
"debug"           : False                # The debug mode, True shows exceptions on server error
}

ROOTPROJECT = None
PROJECTFILES = None

_LIB_LABELS = ["skipole_js", "jquery_core",
               "ski_basic", "ski_paths", "ski_checkbox", "ski_confirm", "ski_debug_tools", "ski_error_messages",
               "ski_footers", "ski_headers", "ski_info", "ski_inputforms", "ski_inputtables",
               "ski_inputtext", "ski_links", "ski_logins", "ski_paras", "ski_radio", "ski_svgarrows", "ski_svgbasics",
               "ski_tables", "ski_textarea", "ski_dropdown", "ski_upload"]

_SYS_LABELS = ["url_not_found", "validate_error", "server_error", "redirector", "no_javascript", "general_json"]


Info = collections.namedtuple('Info', ['project', 'project_version', 'ident', 'item_type', 'name', 'brief', 'path', 'label_list', 'change', 'parentfolder_ident', 'restricted'])



def set_site_root(project):
    "Sets the given project as the root project of the site"
    global ROOTPROJECT
    project.rootproject = True
    ROOTPROJECT = project

def set_projectfiles(projectfiles):
    "Sets the directory where projectfiles can be found"
    global PROJECTFILES
    PROJECTFILES = projectfiles

def projectfiles():
    "Returns the directory where projectfiles can be found"
    return PROJECTFILES

def lib_list():
    "Returns list of library labels"
    return _LIB_LABELS

def sys_list():
    "Returns list of system page labels"
    return _SYS_LABELS

def is_project(proj_ident):
    "Returns True if this project is in the site, False otherwise"
    global ROOTPROJECT
    if proj_ident == ROOTPROJECT.proj_ident:
        return True
    if proj_ident in ROOTPROJECT.subprojects:
        return True
    return False


def admin_project():
    "Returns the ski admin project name"
    return _CFG["admin_project"]

def new_project():
    "Returns the new project name"
    return _CFG["new_project"]

def lib_project():
    "Returns the lib project name"
    return _CFG["lib_project"]

def get_debug():
    "Returns the debug mode"
    return _CFG["debug"]

def set_debug(mode):
    "Sets debug mode"
    global _CFG
    _CFG["debug"] = bool(mode)

def tar_path(proj_ident):
    "Returns the path to the tar file"
    export_tar = proj_ident + ".tar.gz"
    return os.path.join(projectpath(proj_ident), export_tar)

def admin_ident():
    "Returns the ident of the root folder of the admin project"
    return Ident(_CFG["admin_project"], 0)

def adminurl():
    "Returns the url of the admin folder"
    proj = getproject()
    return proj.url+_CFG["admin_project"]+"/"

def getproject(proj_ident=None):
    """If proj_ident is None, returns the site root project
       otherwise returns the project given by the proj_ident
       If proj_ident given, but project does not exist, return None"""
    global ROOTPROJECT
    if ROOTPROJECT is None:
        # root project not created yet
        return
    if (proj_ident is None) or (proj_ident == ROOTPROJECT.proj_ident):
        return ROOTPROJECT
    if proj_ident in ROOTPROJECT.subprojects:
        return ROOTPROJECT.subprojects[proj_ident]


def project_ident(proj_ident=None):
    "Returns the given project ident, if it is None, returns current site root project ident"
    global ROOTPROJECT
    if proj_ident is None:
        return ROOTPROJECT.proj_ident
    return proj_ident

def projectpath(proj_ident=None):
    return os.path.join(projectfiles(), project_ident(proj_ident))

def projectstatic(proj_ident=None):
    "Returns projectfiles/proj_ident/static"
    return os.path.join(projectpath(proj_ident), 'static')

def projectdata(proj_ident=None):
    "Returns projectfiles/proj_ident/data"
    return os.path.join(projectpath(proj_ident), 'data')

def projectcode(proj_ident=None):
    from ..projectcode import get_projectcode_dir
    return get_projectcode_dir(proj_ident)

def project_json(proj_ident=None):
    "Returns projectfiles/proj_ident/data/project.json"
    return os.path.join(projectdata(proj_ident), "project.json")

def project_defaults(proj_ident=None):
    "Returns projectfiles/proj_ident/data/defaults.json"
    return os.path.join(projectdata(proj_ident), "defaults.json")

def project_main(proj_ident=None):
    "Returns projectfiles/proj_ident/data/__main__.py"
    return os.path.join(projectdata(proj_ident), "__main__.py")

def textblocks_json_directory(proj_ident=None):
    "Returns the directory holding the textblocks json files"
    return os.path.join(projectdata(proj_ident), "textblocks_json")

def default_language():
    "Returns the default language"
    return _CFG["default_language"]

def version():
    "Returns the version string"
    return _CFG["version"]


def root(proj_ident = None):
    "Returns the root folder of the given project, if proj not given returns this projects rootfolder"
    global ROOTPROJECT
    if (proj_ident is None) or (proj_ident == ROOTPROJECT.proj_ident):
        return ROOTPROJECT.root
    if proj_ident not in ROOTPROJECT.subprojects:
        return None
    return ROOTPROJECT.subprojects[proj_ident].root
    

# These functions deal with page and folder 'idents'.  They are defined here
# as they are common functions used everywhere.

def from_ident(ident, proj_ident=None, import_sections=True):
    """given an Ident, or a string version of ident, or item with ident attribute, return deepcopy of page or folder.
       If a page with sections, and import_sections is True, the sections will be imported"""
    ident = Ident.to_ident(ident, proj_ident)
    if ident is None:
        return
    project = getproject(ident.proj)
    if project is None:
        return
    item = project.get_item(ident)
    item = copy.deepcopy(item)
    if import_sections and ((item.page_type == 'TemplatePage') or (item.page_type == 'SVG')):
        item.import_sections()
    return item


def item_info(ident):
    """Returns a namedtuple of item information
          None if not found, tuple has contents:
          project, project_version, ident, item_type, name, brief, path, label_list, change, parentfolder_ident, restricted
       note: project is the project name
             parentfolder_ident is the parent folder ident or None if this is root
             ident is this item ident"""

    project = getproject(ident.proj)
    if project is None:
        return
    item = project.get_item(ident)
    if item is None:
        return

    if item.name is None:
        name = ''
    else:
        name = item.name
    if item.parentfolder_ident is None:
        parentfolder_ident = None
    else:
        parentfolder_ident = item.parentfolder_ident
    special_pages = project.special_pages
    label_list = []
    for label, value in special_pages.items():
        if ident == value:
            label_list.append(label)
    return Info(ident.proj,
                project.version,
                ident,
                item.page_type,
                name,
                item.brief,
                item.url,
                label_list,
                item.change,
                parentfolder_ident,
                item.restricted
               )


def get_item(ident):
    """Gets uncopied page or folder, without importing sections and returns it
        Returns None if not found. Requires full ident object"""
    project = getproject(ident.proj)
    if project is None:
        return None
    return project.get_item(ident)


def get_url(label_url_ident, proj_ident=None):
    "Returns a url given a page ident, url or label, if not found, return None"
    if not label_url_ident:
        return
    result = find_ident_or_url(label_url_ident, proj_ident)
    if isinstance(result, Ident):
        return result.url()
    return result


def ident_from_path(path, proj_ident=None):
    project = getproject(proj_ident)
    if project is None:
        return
    return project.root.ident_from_path(path)


def get_part(proj_ident, ident, page_part, section_name, widget_name, container_number, location_list):
    """Given the above arguments for a html element such as a div, returns the actual part object if found,
       not a copy, otherwise None. page_part is a string such as head, body or svg, location_list is a
       list of integers, beneath the page part or widget container number that contains the part
       If widget_name is given but container_number is None, returns the widget"""
    project = getproject(proj_ident)
    if project is None:
        return

    if section_name:
        section = project.section(section_name, makecopy=False)
        if section is None:
            return
        if widget_name:
            # part is within a widget container within the section
            if widget_name not in section.widgets:
                return
            widget = section.widgets[widget_name]
            if widget is None:
                return
            if container_number is None:
                return widget
            if widget.can_contain():
                return widget.get_from_container(container_number, location_list)
            else:
                return
        # no widget name, so part is within the section
        if location_list:
            return section.get_location_value(location_list)
        else:
            return section

    # part not in a section, so must be in a page, template or svg.
    if ident is None:
        return

    page = get_item(ident)
    if page is None:
        return
    if (page.page_type != 'TemplatePage') and (page.page_type != 'SVG'):
        return

    if widget_name:
        # part is within a widget container within the page
        if widget_name not in page.widgets:
            return
        widget = page.widgets[widget_name]
        if widget is None:
            return
        if container_number is None:
            return widget
        if widget.can_contain() and not (container_number is None):
            return widget.get_from_container(container_number, location_list)
        else:
            return

    # no widget name, so part is within the page
    if not page_part:
        return
    if page.page_type == 'TemplatePage':
        if (page_part == 'head') or (page_part == 'body'):
            return page.get_part(page_part, location_list)
    if page.page_type == 'SVG':
        if page_part == 'svg':
            return page.get_part(page_part, location_list)

    # part not found
    return


def widget_from_part(part, widget_name):
    """Given a part and widget name, searches down through part contents and returns a
       widget with the given name - if none found returns None"""
    if hasattr(part, 'name'):
        if part.name == widget_name:
            return part
    if hasattr(part, 'parts'):
        for p in part.parts:
            w = widget_from_part(p, widget_name)
            if w:
                return w


def ident_exists(ident, proj_ident=None):
    "Return True if ident exists, False otherwise, ident can be a string form of ident"
    ident = Ident.to_ident(ident, proj_ident)
    if ident is None:
        return False
    project = getproject(ident.proj)
    if project is None:
        return False
    return ident.num in project.ident_numbers


def ident_exists_strict(ident):
    "Returns ident if it exists, None otherwise, ident must be an Ident object"
    if not isinstance(ident, Ident):
        return
    project = getproject(ident.proj)
    if project is None:
        return
    if ident.num in project.ident_numbers:
        return ident


# usefull functions

def page_from_referer(referer):
    "Returns page with the referer url, if it cannot be found, return None"
    referer = referer.lower()
    # create list
    ref_list = referer.split("//")
    if len(ref_list) != 2: return
    referer = ref_list[1]
    ref_list = referer.split("/")
    if len(ref_list)<2: return None
    path = '/' + '/'.join(ref_list[1:])
    return root().page_from_path(path)
    

def mergedict(dict1, dict2):
    "returns a dictionary, which is the update of two dictionaries"
    newdict = dict1.copy()
    newdict.update(dict2)
    return newdict

def mergedicttostyle(style_dict, key, add_dict):
    "Returns a new style_dict, with the dictionary of the key item updated with add_dict"
    if key in style_dict:
        new_sub_dict = mergedict(style_dict[key], add_dict)
    else:
        new_sub_dict = add_dict.copy()
    new_dict = style_dict.copy()
    new_dict[key] = new_sub_dict
    return new_dict


def make_ident_or_label_or_url(item, proj_ident=None):
    """Given an item, be it integer, string or Ident, return an Ident object
       If the item is an integer, the returned Ident object
       will have its proj set to the proj_ident if given, otherwise current project
       If item is a not convertable to an ident - then return the string,
       which should be a label or url"""
    if isinstance(item, str) and ('/' in item):
        # must be a url
        return item
    ident = Ident.to_ident(item, proj_ident)
    if ident is None:
        # not convertable to ident, must be a label
        return item
    return ident


def make_ident_or_label(item, proj_ident=None):
    """Given an item, be it integer, string or Ident, return an Ident object
       or label - not a url.
       If the item is an integer, the returned Ident object
       will have its proj set to the proj_ident if given, otherwise current project
       If item is a not convertable to an ident - then return the string,
       which should be a label, if string contains /, return None"""
    if isinstance(item, str) and ('/' in item):
        # a url - return None
        return
    ident = Ident.to_ident(item, proj_ident)
    if ident is None:
        # not convertable to ident, must be a label
        return item
    return ident



def make_ident(item, proj_ident=None):
    """Just calls Ident.to_ident"""
    return Ident.to_ident(item, proj_ident)


def find_ident(item, proj_ident=None):
    """Given any item makes an attempt to find an Ident
       existing in the project, item could have an ident attribute,
       or be an ident in string or integer or Ident form
       or label, or tuple of form (project,ident) or (project,label).
       If no existing ident or if a url found instead, returns None"""

    ident_or_url = find_ident_or_url(item, proj_ident)
    if isinstance(ident_or_url, Ident):
        return ident_or_url
    # ident_or_url may be a URL or None, in this case return None
    return



def find_ident_or_url(item, proj_ident=None):
    """Given any item makes an attempt to find an Ident or url
       existing in the project, item could have an ident attribute,
       or be an ident in string or integer or Ident form
       or label, or tuple of form (project,ident) or (project,label).
       If no existing ident or url found, returns None"""

    if not item:
        return

    if isinstance(item, Ident):
        return ident_exists_strict(item)

    if isinstance(item, str):
        item = item.strip()
        if not item:
            return
        if '/' in item:
            # its a url
            return item
        if item.isdigit():
            # string integer
            return ident_exists_strict(Ident.to_ident(item, proj_ident))
        # could be 'project,number' or 'project,label', 
        if ',' in item:
            item_parts = item.split(',')
            if len(item_parts) != 2:
                return
            if item_parts[1].isdigit():
                return ident_exists_strict(Ident.to_ident(item, proj_ident))
            # may be 'project,label' - so find [project,label]
            return find_ident_or_url(item_parts, proj_ident=proj_ident)
        # could be case of 'project_number'
        if '_' in item:
            item_parts = item.split('_')
            if (len(item_parts) == 2) and item_parts[1].isdigit():
                return ident_exists_strict(Ident.to_ident(item, proj_ident))

        # item is a label
        project = getproject(proj_ident)
        if project is None:
            return
        special_pages = project.special_pages
        if item not in special_pages:
            return
        target = special_pages[item]
        # target is either an Ident, url, or 'proj,label' string
        if isinstance(target, Ident):
            return ident_exists_strict(target)
        if '/' in target:
            # so item is a label pointing to this url
            return target
        if ',' in target:
            # so item is a label pointing to project,newitem
            target_parts = target.split(',')
            return find_ident_or_url(target_parts[1], proj_ident=target_parts[0])

    if not ( (isinstance(item, tuple)) or (isinstance(item, list)) ):
        # not a tuple or a list, so maybe integer - try to convert to ident
        return ident_exists_strict(Ident.to_ident(item, proj_ident))

    # test for [project, newitem]

    # item is a tuple or list
    if len(item) != 2:
        # invalid, return None
        return

    proj = item[0].strip()

    project = getproject(proj)
    if project is None:
        return

    return find_ident_or_url(item[1], proj_ident=proj)




# Each folder and page has an instance of Ident
class Ident(collections.namedtuple('Ident', ['proj','num'])):
    __slots__ = ()

    @classmethod
    def to_ident(cls, item, proj_ident=None):
        """Given an ident, be it tuple, integer, string or Ident, return an Ident object
           If the item is just an integer, the returned Ident object
           will have its proj set to the proj_ident if given, otherwise current project
           If an Ident object cannot be created, return None"""
        # Deal with cases where proj_ident is not needed
        if isinstance(item, cls):
            return item
        if isinstance(item, str):
            # first deal with case of a string ident myproj_num
            if '_' in item:
                item = item.split('_')
            elif ',' in item:
                item = item.split(',')
            else:
                # could be a string integer
                try:
                    item = int(item)
                except Exception:
                    # don't know what it is, return None
                    return
        if isinstance(item, tuple) or isinstance(item, list):
            if len(item) == 2:
                try:
                    num = int(item[1])
                except Exception:
                    # don't know what it is, return None
                    return
                if item[0] and isinstance(item[0], str):
                    return cls(item[0], num)
                else:
                    return
            else:
                # list, but not of length two, don't know what it is
                return
        if hasattr(item, 'ident') and (isinstance(item.ident, cls)):
            return item.ident
        if isinstance(item, int):
            # project not derived from item, therefore need to use proj_ident
            # proj_ident must be either an Ident instance, string or None
            if isinstance(proj_ident, cls):
                proj = proj_ident.proj
            elif proj_ident:
                proj = proj_ident
            else:
                proj = ROOTPROJECT.proj_ident
            return cls(proj, item)

    def item(self, import_sections=True):
        """Calls the from_ident function"""
        return from_ident(self, proj_ident=self.proj, import_sections=import_sections)

    def name(self):
        """Returns the name of the page or folder with this ident
           If item is root, or item not found, returns None"""
        if self.num is 0:
            return None
        item = get_item(self)
        if item is None:
            return
        return item.name

    def url(self):
        "Returns the url of the page or folder with this ident"
        item = get_item(self)
        if item is None:
            return
        return item.url

    def widg_ident(self, widgname):
        """Given a widget name, if this ident is the ident of a page, and the widget
           is in the page, return the widgets ident, if the ident is not that of a page
           or the widget name is not found in the page, return an empty string"""
        item = get_item(self)
        if ((item.page_type == 'TemplatePage') or (item.page_type == 'SVG')) and (widgname in item.widgets):
            return item.widgets[widgname]
        return ''

    def to_tuple(self):
        return (self.proj, self.num)

    def to_comma_str(self):
        return self.proj + "," + str(self.num)

    def __str__(self):
        return self.proj + "_" + str(self.num)

    def __add__(self, other):
        "An ident can be added to a integer or tuple to give a string"
        if isinstance(other, Ident):
            raise TypeError("An Ident cannot be added to another Ident")
        if isinstance(other, tuple) or isinstance(other, list):
            return self.__str__() + '_' + '_'.join(str(i) for i in other)
        return self.__str__() + '_' + str(other)

#
# Defines functions and class WidgField which is a named tuple with attributes s,w,f,i
# for section name, widget name, field name, index value
# section name could be empty if widget is not in a section
# index value is used for widgfield dictionaries, and can be empty if not applicable
# widgfield has string sectionname-widgetname:fieldname-index
#

def make_widgfield(field, widgetonly=False):
    """Given a string field, of the form sectionname-widgetname:fieldname-index, (set by widgets)
       or of the form sectionname-widgetname:fieldname.index, (set by browser, ie image x,y coordinates)
       or a list or tuple, of form (sectionname, widgetname, fieldname, index)
       Note: if index given, tuple must have four elements, if three given they will
       be assumed as (sectionname, widgetname, fieldname)
       returns a named tuple of the form WidgField(s=sectionname, w=widgetname, f=fieldname, i=index)
       If field is already a WidgField, just returns it"""
    if not field:
        return WidgField(s='', w='', f='', i='')
    if widgetonly:
        if isinstance(field, WidgField):
            return WidgField(s=field.s, w=field.w, f='', i='')
        if isinstance(field, str) and (',' in field):
            field = [ item.strip() for item in field.split(',') ]
        if isinstance(field, list) or isinstance(field, tuple):
            if len(field) == 1:
                return WidgField(s='', w=field[0], f='', i='')
            if len(field) >= 2:
                return WidgField(s=field[0], w=field[1], f='', i='')
        # so should be a string
        if ':' in field:
            field = field.split(':')[0]
        if not field:
            return WidgField(s='', w='', f='', i='')
        if '-' in field:
            sectionname, widgetname = field.split("-", 1)
            return WidgField(s=sectionname, w=widgetname, f='', i='')
        else:
            # widgetname only
            return WidgField(s='', w=field, f='', i='')
    # not just a widget, could be widget and field
    if isinstance(field, WidgField):
        return field
    if isinstance(field, str) and (',' in field):
        field = [ item.strip() for item in field.split(',') ]
    if isinstance(field, list) or isinstance(field, tuple):
        if len(field) == 1:
            return WidgField(s='', w=field[0], f='', i='')
        if len(field) == 2:
            return WidgField(s='', w=field[0], f=field[1], i='')
        if len(field) == 3:
            return WidgField(s=field[0], w=field[1], f=field[2], i='')
        return WidgField(s=field[0], w=field[1], f=field[2], i=field[3])
    # so should be a string
    if ':' not in field:
        if '-' in field:
            sectionname, widgetname = field.split("-", 1)
            return WidgField(s=sectionname, w=widgetname, f='', i='')
        else:
            # widgetname only, no section, field or index
            return WidgField(s='', w=field, f='', i='')
    sectionwidgetname, field_index = field.split(":", 1)
    if '-' in sectionwidgetname:
        sectionname, widgetname = sectionwidgetname.split("-", 1)
    else:
        sectionname = ''
        widgetname = sectionwidgetname
    # field index separated by - or by .
    if '-' in field_index:
        fieldname, index = field_index.split("-", 1)
    elif '.' in field_index:
        fieldname, index = field_index.split(".", 1)
    else:
        fieldname = field_index
        index=''
    return WidgField(s=sectionname, w=widgetname, f=fieldname, i=index)


def list_widgfield(widgfield, widgfield_dict):
    """Converts a widgfield (with no i value), and a dictionary to a list of
       of widgfield,value tuples, with each widgfield in the tuple having i set to the key
       and the list is sorted by key"""
    if widgfield.i:
        return [(widgfield, widgfield_dict)]
    return sorted([(widgfield._replace(i=key), val) for key, val in widgfield_dict.items()], key=lambda tup: tup[0].i)


class WidgField(collections.namedtuple('WidgField', 's w f i')):
    __slots__ = ()

    def set_field(self, f='', i=''):
        "Returns a copy of self, with new field and index set"
        return WidgField(s=self.s, w=self.w, f=f, i=i)

    def set_index(self, i=''):
        "Returns a copy of self, with new index set"
        return WidgField(s=self.s, w=self.w, f=self.f, i=i)

    def __bool__(self):
        if self.s or self.w or self.f or self.i:
            return True
        return False

    def __str__(self):
        "returns sectionname-widgetname:fieldname-index"
        if self.s:
            val = self.s + '-' + self.w
        else:
            val = self.w
        if self.f:
             val = val + ':' + self.f
        if self.i:
            val = val + '-' + self.i
        return val

    def to_tuple(self):
        "returns tuple of (self.s, self.w, self.f, self.i)"
        return (self.s, self.w, self.f, self.i)

    def to_tuple_no_i(self):
        "returns tuple of (self.s, self.w, self.f) if self.s or (self.w, self.f) if no self.s"
        if self.s:
            return (self.s, self.w, self.f)
        return (self.w, self.f)

    def sw_tuple(self):
        "returns tuple of (self.s, self.w)"
        if self.s:
            return (self.s, self.w)
        return ('',self.w)

    def to_str_tuple(self):
        "returns sectionname,widgetname,fieldname,index"
        if self.s:
            val = self.s + ',' + self.w
        else:
            val = self.w
        if self.f:
             val = val + ',' + self.f
        if self.i:
            val = val + ',' + self.i
        return val


