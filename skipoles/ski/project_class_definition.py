####### SKIPOLE WEB FRAMEWORK #######
#
# project_class_definition.py  - Contains project class
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
This module defines the Project class
"""


import copy, os, cgi, collections, html, pprint, json, shutil, uuid, sys, traceback

from http import cookies

from . import skiboot, read_json
from .excepts import ValidateError, ServerError, ErrorMessage, GoTo, PageError
from .. import projectcode


class Project(object):
    """Represents the project"""


    def __init__(self, proj_ident, url="/", options={}, rootproject=False, projectfiles=None):
        """Initiates a Project instance"""

        if projectfiles:
            skiboot.set_projectfiles(projectfiles)

        # get project location
        project_dir = skiboot.projectpath(proj_ident)
        if not os.path.isdir(project_dir):
            raise ServerError("Project %s not found" % (proj_ident,))

        self._proj_ident = str(proj_ident)

        # This parameter is sent to the user start_call function
        self.options = options
        self.option = None
        if options:
            if self._proj_ident in options:
                self.option = options[self._proj_ident]


        self.brief = "Project %s" % proj_ident
        self.version = "0.0.0"
        # The url of the root folder
        self._url = url
        # The root Folder
        self.root = None
        # dictionary of special pages, key = label: value = page ident
        self.special_pages = {}
        # dictionary of sections, key = name: value = section
        self.sections = {}

        # an ordered dictionary of {proj_ident: url,...}, ordered by length of url
        self._subproject_paths = collections.OrderedDict()
        # A dictionary of subproject dicts {proj_ident: {'path':path,...}}
        # this dictionary being loaded from the project.json file
        self.subproject_dicts = {}
        # self.subprojects is a dictionary of sub projects {proj_ident: Project instance,.....}
        self.subprojects = {}

        # dictionary of idents: to folder or page, apart from root
        # note keys are full Ident instances, values are  folder or page instances
        self.identitems = {}

        # This is set to True if the project is the top root project
        # otherwise it is False - which means this is a subproject
        self.rootproject = rootproject

        # This dictionary is available to the user
        self.proj_data = {}

        # Create an instance of the AccessTextBlocks class for this project
        self.textblocks = projectcode.make_AccessTextBlocks(self._proj_ident, 
                                                            skiboot.projectfiles(),
                                                            skiboot.default_language())

        # maintain a cach dictionary of paths against idents {path:ident}
        self._paths = {}

        # load project from json files
        self.load_from_json(rootproject)

        # set this project as the main site project
        if rootproject:
            skiboot.set_site_root(self)

        if rootproject:
            # Call the start_project function for this project and any sub_projects
            self.start_project()



    def __call__(self, environ, start_response):
        "Defines this projects callable as the wsgi application"
        status, headers, data = self.respond(environ)
        start_response(status, headers)
        return data


    def set_default_language(self, language):
        "Sets the project default language"
        self.textblocks.default_language = language

    def get_default_language(self):
        "Returns the project default language"
        return self.textblocks.default_language

    default_language = property(get_default_language, set_default_language)

    def clear_cache(self):
        "clear the cache of paths"
        self._paths = {}


    def load_from_json(self, rootproject = False):
        "Loads project with data saved in project.json file, set rootproject True if this is a rootproject "
        self.rootproject = rootproject
        projectdict = read_json.create_project(self._proj_ident)
        self.url = projectdict['url']
        self.subproject_dicts = projectdict["subprojects"]
        if self.subproject_dicts and rootproject:
            # pull out a dictionary of sub project ident:path
            sub_paths = {sub_ident:sub_dict['path'] for sub_ident,sub_dict in self.subproject_dicts.items()}
            # make this an ordered dictionary, ordered by length of path elements
            self._subproject_paths = collections.OrderedDict(sorted(sub_paths.items(), key=lambda t: len(t[1].strip("/").split("/")), reverse=True))
            for subproj_ident in self._subproject_paths:
                subproject = Project(subproj_ident, options=self.options)
                # and add it to this site
                self.subprojects[subproj_ident] = subproject
        else:
            self._subproject_paths = collections.OrderedDict()
            self.subprojects = {}
        self.default_language = projectdict['default_language']
        self.brief = projectdict['brief']
        self.version = projectdict['version']
        self.special_pages = projectdict['specialpages']
        self.sections = projectdict['sections']
        self.root = projectdict['siteroot']
        itemlist = projectdict['itemlist']
        self.identitems = {}
        if itemlist:
            for item in itemlist:
                self.identitems[item.ident] = item

    def start_project(self, path=None):
        "Called from  load_project to call the user start_project function"
        if not self.rootproject:
            self.proj_data = projectcode.start_project(self._proj_ident, path, self.option)
            return
        # root project
        self.proj_data = projectcode.start_project(self._proj_ident, self.url, self.option)
       # and call start_project for each subproject
        for subproj_ident, proj in self.subprojects.items():
            proj.start_project(path=self._subproject_paths[subproj_ident])


    @property
    def max_ident_num(self):
        "Returns the maximum identnumber currently in use"
        maxnum = 0
        for ident in self.identitems:
            if ident.num > maxnum:
                    maxnum = ident.num
        return maxnum

    def list_section_names(self):
        "Returns a list of section names, alphabetacily ordered"
        if not self.sections:
            return []
        s = [ name for name in self.sections ]
        s.sort()
        return s

    def widget_from_section(self, section_name, widget_name):
        "Returns the widget from the project section"
        # get the section part with the given name
        section = self._get_section(section_name)
        if section is None:
            return None
        # find widget in the section with the given name
        if widget_name in section.widgets:
            return section.widgets[widget_name]

    def section(self, section_name, makecopy=True):
        "Returns a section, or a deep copy of a section, or None if the section name is not found"
        if section_name not in self.sections:
            return
        section = self.sections[section_name]
        if not makecopy:
            return section
        if section is None:
            return None
        return copy.deepcopy(section)
 

    def add_section(self, name, section):
        "Adds a section to the project, returns section.change uuid"
        # and save the section
        section.widgets = {}
        section.section_places = {}  # currently unused
        embedded = (name, '', None)
        section.set_idents(name, section.widgets, section.section_places, embedded)
        # set validators in section
        section.load_validator_scriptlinks()
        # set the section change number
        section.change = uuid.uuid4().hex
        self.sections[name] = section
        return section.change


    def delete_section(self, name):
        "Deletes a section"
        if name in self.sections:
            del self.sections[name]

    @property
    def ident_numbers(self):
        "return a list of ident numbers"
        num_list = [ ident.num for ident in self.identitems ]
        # insert the root
        num_list.insert(0,0)
        num_list.sort()
        return num_list

    def __getitem__(self, ident):
        """given an Ident, or a string version of ident, return page or folder. 
              If folder or respond page return the item, any other page, return a deep copy
              of the item. If item not found, return None"""
        ident = skiboot.Ident.to_ident(ident, proj_ident=self._proj_ident)
        if ident is None:
            return
        if ident.proj != self._proj_ident:
            return
        if ident.num == 0:
            return self.root
        if ident not in self.identitems:
            return
        item = self.identitems[ident]
        if item is None:
            return
        if item.page_type == 'Folder':
            return item
        if item.page_type == 'RespondPage':
            return item
        return copy.deepcopy(item)

    def add_item(self, parent_ident, item, ident=None):
        """Adds a new page or folder to the project, returns the item ident"""

        # check ident
        if ident is None:
            ident = skiboot.Ident(self._proj_ident, self.max_ident_num+1)
        else:
            ident = skiboot.make_ident(ident, self._proj_ident)
            if ident is None:
                raise ServerError(message="Sorry. Invalid ident")
            if ident.num == 0:
                # cannot add the root folder
                raise ServerError(message="Sorry. Unable to add a new root")
            if ident.proj != self._proj_ident:
                # must be in this project
                raise ServerError(message="Sorry. Invalid ident")
            if ident in self.identitems:
                # ident must not exist
                raise ServerError(message="Sorry. The given ident already exists")

        # check parent folder
        if parent_ident.proj != self._proj_ident:
            raise ServerError(message="Invalid parent ident")
        parent = self.get_item(parent_ident)
        if parent is None:
            raise ServerError(message="Parent folder not found: Error in add_item method of Project class.")
        if parent.page_type != 'Folder':
            raise ServerError(message="Parent not a folder")

        if item.name in parent.pages:
            raise ServerError(message="Sorry, a page with that name already exists in the parent folder")
        if item.name in parent.folders:
            raise ServerError(message="Sorry, a folder with that name already exists in the parent folder")

        # set the item ident
        item.ident = ident

        # set this item name into the parent
        if item.page_type == 'Folder':
            if parent.restricted:
                item.set_restricted()
            parent.folders[item.name] = item.ident
        # if the page is a template or svg page, then set its idents
        # and store its widgets in the page's widgets dictionary and sectionplaceholders
        # in the page's sections directory
        elif (item.page_type == 'TemplatePage') or (item.page_type == 'SVG'):
            item.set_idents()
            parent.pages[item.name] = item.ident
            # now set validator modules in page
            if item.page_type == 'TemplatePage':
                item.load_validator_scriptlinks()
        else:
            parent.pages[item.name] = item.ident

        # set the parent change value
        parent.change = uuid.uuid4().hex
        item.parentfolder = parent

        # and finally, add the item
        self.identitems[item.ident] = item
        self.clear_cache()
        return item.ident


    def delete_item(self, itemident):
        """Deletes the page or folder with the given ident from the database."""
        #############  TO DO - if folder has contents, recursivly delete contents ########
        if itemident.num == 0:
            # cannot delete the root folder
            raise ServerError(message="Cannot delete the root folder")
        if itemident.proj != self._proj_ident:
            # Must belong to this project
            raise ServerError(message="Cannot delete this item (does not belong to this project)")
        if itemident not in self.identitems:
            raise ServerError(message="Item not found")
        # get the item
        item = self.identitems[itemident]
        # get the items parent folder
        parentfolder = item.parentfolder
        if item.name in parentfolder.pages:
            del parentfolder.pages[item.name]
        if item.name in parentfolder.folders:
            del parentfolder.folders[item.name]
        parentfolder.change = uuid.uuid4().hex
        # del the item
        del self.identitems[itemident]
        self.clear_cache()


    def save_item(self, item, new_parent_ident=None):
        """Saves the page or folder - used to save an altered item, not to add a new one
           If new_parent_ident is not None, indicates the item has moved to a different folder"""
        if item.page_type == 'Folder':
            self.save_folder(item, new_parent_ident)
        else:
            self.save_page(item, new_parent_ident)


    def save_page(self, item, new_parent_ident=None):
        """Saves the page - used to save an altered page, not to add a new one
           If new_parent_ident is not None, indicates the page has moved to a different folder
           Returns the new page.change uuid"""
        if item.page_type == 'Folder':
            raise ServerError(message="Invalid item, not a page.")
        item_ident = item.ident
        if item_ident is None:
            raise ServerError(message="Unable to save page - no ident set")
        if self._proj_ident != item_ident.proj:
            raise ServerError(message="Unable to save page - invalid ident")
        if item_ident not in self.identitems:
            raise ServerError(message="This page ident does not exist")
        old_parent = self.identitems[item_ident].parentfolder
        old_name = self.identitems[item_ident].name
        if new_parent_ident is not None:
            # So its a parent folder change
            if new_parent_ident.num is 0:
                # new parent is root
                new_parent = self.root
            else:
                new_parent = self.identitems[new_parent_ident]
            if new_parent == old_parent:
                new_parent_ident = None
        if (item.page_type == 'TemplatePage') or (item.page_type == 'SVG'):
            item.set_idents()
        # now set validator modules in page
        if item.page_type == 'TemplatePage':
            item.load_validator_scriptlinks()
        item.change = uuid.uuid4().hex
        if (old_name == item.name) and (new_parent_ident is None):
            # no folder change
            self.identitems[item_ident] = item
            self.clear_cache()
            return item.change
        if new_parent_ident is None:
            # so just a name change
            if item.name in old_parent.pages:
                raise ServerError(message="Sorry, a page with that name already exists")
            if item.name in old_parent.folders:
                raise ServerError(message="Sorry, a folder with that name already exists")
            if old_name in old_parent.pages:
                del old_parent.pages[old_name]
            old_parent.pages[item.name] = item_ident
            old_parent.change = uuid.uuid4().hex
            self.identitems[item_ident] = item
            self.clear_cache()
            return item.change
        # change of folder
        if item.name in new_parent.pages:
            raise ServerError(message="Sorry, a page with that name already exists")
        if item.name in new_parent.folders:
            raise ServerError(message="Sorry, a folder with that name already exists")
        if old_name in old_parent.pages:
            del old_parent.pages[old_name]
            old_parent.change = uuid.uuid4().hex
        new_parent.pages[item.name] = item_ident
        new_parent.change = uuid.uuid4().hex
        item.parentfolder = new_parent
        self.identitems[item_ident] = item
        self.clear_cache()
        return item.change


    def save_folder(self, item, new_parent_ident=None):
        """Saves the folder - used to save an altered folder, not to add a new one
           If new_parent_ident is not None, indicates the folder has moved to a different parent folder
           Returns the new folder.change uuid"""
        if item.page_type != 'Folder':
            raise ServerError(message="Invalid item, not a folder.")
        item_ident = item.ident
        if item_ident is None:
            raise ServerError(message="Unable to save folder - no ident set")
        if self._proj_ident != item_ident.proj:
            raise ServerError(message="Unable to save folder - invalid ident")
        if item_ident.num == 0:
            if new_parent_ident:
                raise ServerError(message="Root folder cannot have new parent")
            item.change = uuid.uuid4().hex
            self.root = item
            self.clear_cache()
            return item.change
        if item_ident not in self.identitems:
            raise ServerError(message="This folder ident does not exist")
        old_parent = self.identitems[item_ident].parentfolder
        old_name = self.identitems[item_ident].name
        if new_parent_ident is not None:
            # So its a parent folder change
            if new_parent_ident.num is 0:
                # new parent is root
                new_parent = self.root
            else:
                new_parent = self.identitems[new_parent_ident]
            if new_parent == old_parent:
                new_parent_ident = None
        item.change = uuid.uuid4().hex
        if (old_name == item.name) and (new_parent_ident is None):
            # no parent folder change
            self.identitems[item_ident] = item
            self.clear_cache()
            return item.change
        if new_parent_ident is None:
            # so just a name change
            if item.name in old_parent.pages:
                raise ServerError(message="Sorry, a page with that name already exists")
            if item.name in old_parent.folders:
                raise ServerError(message="Sorry, a folder with that name already exists")
            if old_name in old_parent.folders:
                del old_parent.folders[old_name]
            old_parent.folders[item.name] = item_ident
            old_parent.change = uuid.uuid4().hex
            self.identitems[item_ident] = item
            self.clear_cache()
            return item.change
        # change of folder
        # A folder cannot be moved into a sub folder of itself

        folder_list = new_parent.parent_list()
        # folder list is a list of (name, identnumber) starting at root
        folder_ident_numbers = [ identnumber for name,identnumber in folder_list ]
        if item.ident.num in folder_ident_numbers:
            # item is a parent of new_parent
            raise ServerError(message="Sorry, a folder cannot be moved into a subfolder of itself.")
        if item.name in new_parent.pages:
            raise ServerError(message="Sorry, a page with that name already exists")
        if item.name in new_parent.folders:
            raise ServerError(message="Sorry, a folder with that name already exists")
        if old_name in old_parent.folders:
            del old_parent.folders[old_name]
            old_parent.change = uuid.uuid4().hex
        new_parent.folders[item.name] = item_ident
        new_parent.change = uuid.uuid4().hex
        item.parentfolder = new_parent
        self.identitems[item_ident] = item
        self.clear_cache()
        return item.change



    def get_item(self, ident):
        """given an ident (Ident object or integer), return a
           folder or page from the database, if not found, return None.
           Note: the item is returned without copying and without sections imported"""
        if isinstance(ident, int):
            ident = skiboot.Ident(self._proj_ident, ident)
        elif ident.proj != self._proj_ident:
            return None
        if ident.num == 0:
            return self.root
        if ident not in self.identitems:
            return None
        return self.identitems[ident]


    def __iter__(self):
        "This iterator does not return the root folder"
        for ident in self.identitems:
            yield ident

    def __contains__(self, item):
        "Checks if this project contains folder, page or ident"
        if hasattr(item, 'ident'):
            ident = item.ident
        else:
            ident = skiboot.Ident.to_ident(item, self._proj_ident)
        if ident in self.identitems:
            return True
        if (ident.proj == self._proj_ident) and (ident.num is 0):
            return True
        return False

    def __len__(self):
        "This length does not include the root"
        return len(self.identitems)

    def __bool__(self):
        return True


    def get_url(self):
        "Return self._url if this is the rootproject, or the subproject url if not"
        if self.rootproject:
            if self._url:
                return self._url
            return "/"
        # Not root, so get root project
        rp = skiboot.getproject()
        # may be a subproject instance created before a root project has been defined
        # or not yet added to a root project
        if (rp is not None) and  (self._proj_ident in rp.subproject_paths):
            return rp.subproject_paths[self._proj_ident]
        if self._url:
            return self._url
        return "/"
        

    def set_url(self, url):
        url=url.strip("/")
        if url:
            url = "/" + url + "/"
        else:
            url = "/"
        if self.rootproject:
            current_url = self._url
            # set the url of all sub projects
            sub_paths = collections.OrderedDict()
            if self._subproject_paths:
                for proj_ident, proj_url in self._subproject_paths.items():
                    sub_paths[proj_ident] = proj_url.replace(current_url, url, 1)
                    self.subproject_dicts[proj_ident]["path"] = sub_paths[proj_ident]
                self._subproject_paths = sub_paths
        self._url = url

    url = property(get_url, set_url)


    def set_special_page(self, label, target):
        "Sets a special page"
        if not label:
            raise ValidateError(message="Sorry, a special page label must be given")
        if not target:
            raise ValidateError(message="Sorry, a label target must be given")
        if isinstance(target, str) and ( '/' in target ):
                # item is a url
                item = target
        elif isinstance(target, str) and ( ',' in target ) and not (target.split(',')[1].isdigit()):
            if len(target.split(',')) == 2:
                # item points to a subproject label
                item = target
        else:
            item = skiboot.make_ident(target, self._proj_ident)
            if not item:
                raise ValidateError(message="Sorry, the page target is not recognised")
        self.special_pages[label] = item


    def delete_special_page(self, label):
        "Deletes a special page"
        if label in self.special_pages:
            del self.special_pages[label]

    def _system_page(self, label):
        """Returns the system page with the given label, if not found, returns None"""
        # label must be one of the system pages
        if label not in skiboot.sys_list():
            return
        if label not in self.special_pages:
            return
        target = self.special_pages[label]
        ident = skiboot.find_ident(target, proj_ident=self._proj_ident)
        if ident is None:
            return
        return ident.item()


    def labels(self):
        "Returns the special pages dictionary as a dictionary of labels with url's and tuples"
        labels_dict = {}
        for key, val in self.special_pages.items():
            if isinstance(val, str):
                labels_dict[key] = val
            else:
                labels_dict[key] = val.to_tuple()
        return labels_dict


    def _redirect_to_url(self, url, environ, call_data, page_data, lang):
        "Return status, headers, page.data() of the redirector page, with fields set to url"
        if '/' not in url:
            raise ServerError(message="Invalid target url, must contain at least one /")
        page = self._system_page('redirector')
        if (not page) or (page.page_type != "TemplatePage"):
            page_text = "<!DOCTYPE HTML>\n<html>\n<p>Page Redirect request. Please try: <a href=%s>%s</a></p>\n</html>" % (url, url)
            return '200 OK', [('content-type', 'text/html')], [page_text.encode('ascii', 'xmlcharrefreplace')]
        # create an ErrorMessage with the url as the message
        err = ErrorMessage(message=html.escape(url))
        # import any sections
        page.import_sections()
        page.show_error(error_messages=[err])
        # update head and body parts
        if page_data:
            page.set_values(page_data)
        page.update(environ, call_data, lang)
        status, headers = page.get_status()
        return status, headers, page.data()



    def read_form_data(self, rawformdata, caller_page):
        """Reads raw form data from the environ and returns a dictionary with keys as skiboot.WidgField objects and values as
           the form values.  Where input fields have indexed names, the skiboot.WidgField object still
           has i set to empty string, but the value is given as a dictionary with indexes as keys"""
        # rawformdata is the data obtained from environ
        # form_data is a dictionary of data returned, without the caller ident
        # and after a set of checks
        if not rawformdata:
            return {}
        if not caller_page:
            return {}
        form_data = {}
        for field in rawformdata.keys():
            # get fields and values from the rawformdata and store them in form_data
            # with keys as skiboot.WidgField objects, and values as field values
            # in the case of indexed fields, the values are dictionaries
            if field == 'ident':
                continue
            if ':' not in field:
                # All widgfields have a : in them to separate widget name from field name
                raise ValidateError(message="Form data not accepted, (invalid field %s)" % (field,))
            widgfield = skiboot.make_widgfield(field)
            # get fields and values from the rawformdata and store them in form_data
            widget = caller_page.copy_widget_from_name(widgfield.s, widgfield.w)
            if widget is None:
                raise ValidateError(message="Form data not accepted, (unexpected field %s)" % (field,))
            if isinstance(rawformdata[field], list):
                # fieldvalue is a list of items
                fieldvalue = [ item.value.strip() for item in rawformdata[field] ]
            else:
                fieldvalue = rawformdata[field].value.strip()
            if widget.is_senddict(widgfield.f):
                # field sends a dictionary, must have an index appended to the name
                # this part removes the index from the field name, and creates a form value of a dictionary with the index as keys
                fieldindex = widgfield.i
                if not fieldindex:
                    raise ValidateError(message="Form data not accepted, (invalid dictionary field %s)" % (field,))
                widgfieldnoindex = widgfield._replace(i='')
                if widgfieldnoindex in form_data:
                    form_data[widgfieldnoindex][fieldindex] = fieldvalue
                else:
                    form_data[widgfieldnoindex] = {fieldindex:fieldvalue}
            else:
                if widgfield.i:
                    raise ValidateError(message="Form data not accepted, (unexpected dictionary field %s)" % (field,))
                form_data[widgfield] = fieldvalue
        return form_data


    def respond(self, environ):
        "called from the project top script"
        # get cookies
        try:
            cookiemorsals = cookies.SimpleCookie(environ["HTTP_COOKIE"])
        except Exception:
            cookiemorsals = None
        if cookiemorsals:
            received_cookies = {item:m.value for item,m in cookiemorsals.items()}
        else:
            received_cookies = {}
        if 'language' in received_cookies:
            language = received_cookies["language"]
        else:
            if "HTTP_ACCEPT_LANGUAGE" in environ:
                language_list = environ["HTTP_ACCEPT_LANGUAGE"].split(',')
                language = language_list[0]
            else:
                language = self.default_language
        lang = (language, self.default_language)
        if 'PATH_INFO' in environ:
            path = environ['PATH_INFO'].lower()
        else:
            path = ''

        try:
            # This is the root project, check if the call is for a page in any sub project
            for proj, projurl in self._subproject_paths.items():
                if (path.find(projurl) == 0) or (path + "/" == projurl):
                    # this url is within a sub project
                    subproj = self.subprojects[proj]
                    return subproj.proj_respond(environ, path, lang, received_cookies)

            # the call is for a page in this root project
            return self.proj_respond(environ, path, lang, received_cookies)
        except ServerError as e:
            page = self._system_page("server_error")
            if (not page) or (page.page_type != "TemplatePage"):
                # make a temp page
                text_start = "<!DOCTYPE HTML>\n<html>\n<p>SERVER ERROR</p>\n<p>Error code : %s</p>\n" % (e.code,)
                if e.message:
                    page_text = text_start + "<p>%s</p>\n</html>" % (html.escape(e.message),)
                else:
                    page_text = text_start + "</html>"
                return '500 Internal Server Error', [('content-type', 'text/html')], [page_text.encode('ascii', 'xmlcharrefreplace')]
            # import any sections
            page.import_sections()
            # show message passed by the exception
            page.show_error([e.errormessage])
            # if ServerError code, set it into the widget
            if e.code:
                if e.section:
                    page_data = {(e.section, e.widget, 'code'):str(e.code)}
                elif e.widget:
                    page_data = {(e.widget, 'code'):str(e.code)}
                elif page.default_error_widget.s:
                    page_data = {(page.default_error_widget.s, page.default_error_widget.w, 'code'):str(e.code)}
                elif page.default_error_widget.w:
                    page_data = {(page.default_error_widget.w, 'code'):str(e.code)}
                else:
                    page_data = None
                if page_data:
                    page.set_values(page_data)
            # update head and body parts
            page.update(environ, {}, lang, e.ident_list)
            status, headers = page.get_status()
            # return page data
            return e.status, headers, page.data()


    def proj_respond(self, environ, path, lang, received_cookies):
        "Calls start call, and depending on the returned page, calls the project status_headers_data method"

        # get the initial called page from the path
        page = self.page_from_path(path)
        # note; page could be None if not found from a path

        caller_page = None
        call_ident = None

        try:
            # get caller page and call_ident from any form data submitted
            # rawformdata, caller_page, call_ident = self.parse_ident(environ)

            # Note: caller_page could belong to another project, sog get it using ident.item() method
            # which will query the right project

            rawformdata = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ)
            if rawformdata:
                # form data has been submitted - so get the caller page
                if 'ident' not in rawformdata:
                    # external page without ident calling with data
                    caller_page = None
                    call_ident = None
                elif not hasattr(rawformdata['ident'], 'value'):
                    raise ValidateError(message="Form data not accepted, caller page ident not recognised")
                else:
                    # rawformdata has 'ident' with attribute 'value'
                    # get the caller page ident, and the call_ident received from the 'ident' field
                    c_list = rawformdata['ident'].value.split('_', 2)
                    ident_items = len(c_list)
                    try:
                        if ident_items == 2:
                            caller_page = skiboot.Ident(c_list[0], int(c_list[1])).item()
                            call_ident = None
                        elif ident_items == 3:
                            caller_page = skiboot.Ident(c_list[0], int(c_list[1])).item()
                            call_ident = c_list[2]
                    except Exception:
                        caller_page = None
                    if caller_page is None:
                       raise ValidateError(message="Form data not accepted, (received ident is not valid)")
                    if caller_page.page_type != 'TemplatePage':
                        raise ValidateError(message="Form data not accepted, (caller page ident is not a template page)")
        except ValidateError as e:
            page = self._system_page("validate_error")
            if (not page) or (page.page_type != "TemplatePage"):
                # make a temp page
                if e.message:
                    page_text = "<!DOCTYPE HTML>\n<html>\n<p>VALIDATION ERROR</p>\n<p>%s</p>\n</html>" % (html.escape(e.message),)
                else:
                    page_text = "<!DOCTYPE HTML>\n<html>\n<p>VALIDATION ERROR</p>\n</html>"
                return '400 Bad Request', [('content-type', 'text/html')], [page_text.encode('ascii', 'xmlcharrefreplace')]
            # import any sections
            page.import_sections()
            # show message passed by the exception
            page.show_error([e.errormessage])
            # update head and body parts
            page.update(environ, {}, lang, e.ident_list)
            status, headers = page.get_status()
            # return page data
            return e.status, headers, page.data()

        # so caller_page could be either given, or could be None

        # now call the project start_call function

        if page is None:
            ident = None
        else:
            ident = page.ident  # this is the called page ident

        # call the project start_call
        try:
            if caller_page:
                caller_page_ident = caller_page.ident
            else:
                caller_page_ident = None
            # start_call could return a different page ident, or None
            # call_data will be the dictionary of values passed between responders
            # page_data will be the dictionary of widgfields and values to set in the page
            pident, call_data, page_data, lang = projectcode.start_call(environ,
                                                                       path,
                                                                       self._proj_ident,
                                                                       ident,
                                                                       caller_page_ident,
                                                                       received_cookies,
                                                                       call_ident,
                                                                       lang,
                                                                       self.option,
                                                                       self.proj_data)
        except Exception:
            message = "Invalid exception in start_call function."
            if skiboot.get_debug():
                message += "\n"
                exc_type, exc_value, exc_traceback = sys.exc_info()
                str_list = traceback.format_exception(exc_type, exc_value, exc_traceback)
                for item in str_list:
                    message += item
            raise ServerError(message)
 
        if pident is None:
            # URL NOT FOUND and start_call does not divert
            page = self._system_page("url_not_found")
            if (not page) or (page.page_type != "TemplatePage"):
                page_text = "<!DOCTYPE HTML>\n<html>\nERROR:UNKNOWN URL\n</html>"
                return '404 Not Found', [('content-type', 'text/html')], [page_text.encode('ascii', 'xmlcharrefreplace')]
            # create an ErrorMessage with the path as the message
            err = ErrorMessage(message=html.escape(path))
            # import any sections
            page.import_sections()
            page.show_error(error_messages=[err])
            # update head and body parts
            page.update(environ, call_data, lang)
            status, headers = page.get_status()
            return '404 Not Found', headers, page.data()

        # pident is the ident of the diverted page or a label or url string

        # get the page from pident
        if isinstance(pident, str):
            # either a label, or url
            if '/' in pident:
                # get redirector page
                return self._redirect_to_url(pident, environ, call_data, page_data, lang)
            else:
                # no '/' in pident so must be a label
                pident = skiboot.find_ident_or_url(pident, self._proj_ident)
                if not pident:
                    raise ServerError(message="Returned page ident from start_call not recognised")
                if isinstance(pident, str):
                    # must be a url, get redirector page
                    return self._redirect_to_url(pident, environ, call_data, page_data, lang)

        # so pident must be an ident
        if not isinstance(pident, skiboot.Ident):
            raise ServerError(message="Invalid ident returned from start_call")

        # ident is the ident originally called, pident is the ident returned from start_call
        if pident != ident:
            # a new page is requested
            page = pident.item()
            if page is None:
                raise ServerError(message="Invalid ident returned from start_call")
            if page.page_type == 'Folder':
                page = page.default_page
                if not page:
                    raise ServerError(message="Invalid ident returned from start_call")

        # read any submitted data from rawformdata, and place in form_data
        try:
            form_data = {}
            if rawformdata and (caller_page is not None) and (page.page_type == "RespondPage"):
                form_data = self.read_form_data(rawformdata, caller_page)

            # so form_data only available if
                # rawformdata has been submitted
                # and caller_page is known, so widgets can be extracted
                # and the destination is a RespondPage

                # otherwise form_data is empty (though rawformdata is retained)
        

            # dependent on wether the requested page is in this project or a sub project,
            # call status_headers_data() to find the final page to return to the client

            # ident_list retains list of idents called during a call to ensure no circulating calls
            ident_list = []
            # initially no errors, e_list is a list of errors to be shown
            e_list = []

            if page.ident.proj != self._proj_ident:
                # page returned from start_call is in another project
                subproj = self.subprojects.get(page.ident.proj)
                return subproj.status_headers_data(environ, lang, received_cookies, rawformdata, caller_page, page, call_data, page_data, ident_list, e_list, form_data)
                
            # call status_headers_data to return status, headers and data to the top script
            return self.status_headers_data(environ, lang, received_cookies, rawformdata, caller_page, page, call_data, page_data, ident_list, e_list, form_data)

        except ValidateError as e:
            page = self._system_page("validate_error")
            if (not page) or (page.page_type != "TemplatePage"):
                # make a temp page
                if e.message:
                    page_text = "<!DOCTYPE HTML>\n<html>\n<p>VALIDATION ERROR</p>\n<p>%s</p>\n</html>" % (html.escape(e.message),)
                else:
                    page_text = "<!DOCTYPE HTML>\n<html>\n<p>VALIDATION ERROR</p>\n</html>"
                return '400 Bad Request', [('content-type', 'text/html')], [page_text.encode('ascii', 'xmlcharrefreplace')]
            # import any sections
            page.import_sections()
            # show message passed by the exception
            page.show_error([e.errormessage])
            # update head and body parts
            page.update(environ, call_data, lang, e.ident_list)
            status, headers = page.get_status()
            # return page data
            return e.status, headers, page.data()


    def status_headers_data(self, environ, lang, received_cookies, rawformdata, caller_page, page, call_data, page_data, ident_list, e_list, form_data):
        """calls responders until it can return status, headers, page.data()"""

        try:
            while page.page_type == 'RespondPage':
                ident = page.ident
                if page.responder is None:
                    raise ServerError(message="Respond page %s does not have any responder set" % page.url)
                try: 
                    page = page.call_responder(environ, lang, form_data, caller_page, ident_list, call_data, page_data, rawformdata)
                    if isinstance(page, str):
                        # must be a url
                        call_data.clear()
                        page_data.clear()
                        # get redirector page
                        return self._redirect_to_url(page, environ, call_data, page_data, lang)
                except PageError as ex:
                    # a jump to a page has occurred, with a list of errors
                    page = ex.page
                    if isinstance(page, str):
                        # must be a url
                        call_data.clear()
                        page_data.clear()
                        # get redirector page
                        return self._redirect_to_url(page, environ, call_data, page_data, lang)
                    if page.ident in ident_list:
                        raise ServerError(message="Invalid Failure page: can cause circulating call")
                    # show the list of errors on the page
                    e_list = ex.e_list
                except GoTo as ex:
                    if ex.clear_submitted:
                        form_data.clear()
                    if ex.clear_page_data:
                        page_data.clear()
                    target = skiboot.find_ident_or_url(ex.target, ex.proj_ident)
                    # target is either an Ident, a URL or None
                    if not target:
                        raise ServerError(message="GoTo exception target not recognised")
                    if isinstance(target, skiboot.Ident):
                        if target == ident:
                            raise ServerError(message="GoTo exception page ident %s invalid, can cause circulating call" % (target,))
                        if target in ident_list:
                            raise ServerError(message="GoTo exception page ident %s invalid, can cause circulating call" % (target,))
                        page = target.item()
                        if not page:
                            raise ServerError(message="GoTo exception page ident %s not recognised" % (target,))
                        if page.page_type == 'Folder':
                            raise ServerError(message="GoTo exception page ident %s is a Folder, must be a page." % (target,))
                    else:
                        # target is a URL
                        call_data.clear()
                        return self._redirect_to_url(target, environ, call_data, page_data, lang)

                # it is possible that a jump to a page in another project has been made
                if page.ident.proj != self._proj_ident:
                    subproj = skiboot.getproject(proj_ident=page.ident.proj)
                    return subproj.status_headers_data(environ, lang, received_cookies, rawformdata, caller_page, page, call_data, page_data, ident_list, e_list, form_data)
                
        except (ServerError, ValidateError) as e:
            e.ident_list = ident_list
            raise e

        # the page to be returned to the client is now 'page'
        # and 'e_list' is a list of errors to be shown on it

        # call the user function end_call
        try:
            projectcode.end_call(self._proj_ident, page, call_data, page_data, self.proj_data, lang)
        except Exception:
            message = "Invalid exception in end_call function."
            if skiboot.get_debug():
                message += "\n"
                exc_type, exc_value, exc_traceback = sys.exc_info()
                str_list = traceback.format_exception(exc_type, exc_value, exc_traceback)
                for item in str_list:
                    message += item
            raise ServerError(message)

        # import any sections
        page.import_sections(page_data)
        if e_list:
            # show the list of errors on the page
            page.show_error(e_list)
        # now set the widget fields
        if page_data:
            page.set_values(page_data)
        page.update(environ, call_data, lang, ident_list)
        status, headers = page.get_status()
        return status, headers, page.data()



    def page_from_path(self, path):
        """Tests cache, if item exists, return it, if not, call self.root.page_from_path(path)
           and cach the result, then return the page"""
        if path in self._paths:
            ident = self._paths[path]
            if ident is None:
                return
            return self[ident]
        page = self.root.page_from_path(path)
        if page is not None:
            self._paths[path] = page.ident
        return page


    @property
    def proj_ident(self):
        return self._proj_ident

    @property
    def subproject_paths(self):
        "property getter to return an ordered dictionary of sub project {ident:path,...}"
        if not self.rootproject:
            # sub project do not themselves contain further sub projects
            return collections.OrderedDict()
        return self._subproject_paths.copy()


    def list_of_subproject_idents(self):
        "Returns a list of subproject idents"
        return [i for i in self.subproject_paths]

    def add_project(self, proj, url=None):
        """Add a project to self, returns the url
           proj can be the sub project itself, sub project rootfolder, or the sub project ident string.
           This adds a reference to the project to the subproject_paths, returns the sub project path"""
        if not self.rootproject:
           raise ValidateError(message="Cannot add to a sub project")
        if hasattr(proj, 'proj_ident'):
            proj_id = proj.proj_ident
        else:
            proj_id = proj
        if not proj_id:
            raise ValidateError(message="Sorry, invalid project id")
        if not proj_id.isalnum():
            raise ValidateError(message="Sorry, invalid project id")
        # get a copy of the {proj_id:url} subproject_paths dictionary, and this projects url
        sub_paths = self._subproject_paths.copy()
        this_url = self.url
        if proj_id in sub_paths:
            # sub project already exists, overwrite current one with new one, in case of changes
            if isinstance(proj, Project):
                proj.rootproject = False
                self.subprojects[proj_id] = proj
            return sub_paths[proj_id]
        if url is None:
            url = this_url + proj_id
        url=url.strip("/")
        url = "/" + url + "/"
        # Ensure url starts with this project url
        if not url.startswith(this_url):
            url = url.lstrip("/")
            url = this_url + url
        # add this ident and url to subproject_paths
        sub_paths[proj_id] = url
        # save new subproject_paths dictionary
        self._subproject_paths = collections.OrderedDict(sorted(sub_paths.items(), key=lambda t: len(t[1].strip("/").split("/")), reverse=True))
        # add the subproject to this project
        if isinstance(proj, Project):
            proj.rootproject = False
            self.subprojects[proj_id] = proj
        else:
            subproj = Project(proj_id, options=self.options)
            self.subprojects[proj_id] = subproj
        # add the subproject to the self.subproject_dicts
        self.subproject_dicts[proj_id] = {}
        self.subproject_dicts[proj_id]["path"] = url
        # call the subproject start_project function
        self.subprojects[proj_id].start_project(url)
        return url

    def set_project_url(self, proj, url=None):
        """Sets the url of the given sub project, the project must have been added
           returns the url"""
        if hasattr(proj, 'proj_ident'):
            proj_id = proj.proj_ident
        else:
            proj_id = proj
        if not proj_id:
            raise ValidateError(message="Sorry, invalid project id")
        if not proj_id.isalnum():
            raise ValidateError(message="Sorry, invalid project id")
        # get a copy of this projects url
        this_url = self.url
        if url is None:
            url = this_url + proj_id
        url=url.strip("/")
        if url:
            url = "/" + url + "/"
        else:
            url = "/"
        if proj_id == self._proj_ident:
            # setting the url of this project
            self.url = url
            return url
        sub_paths = self._subproject_paths.copy()
        if proj_id not in sub_paths:
            raise ValidateError(message="Sorry, this sub project does not exist")
        if url == "/":
            raise ValidateError(message="Sorry, a sub project cannot have a url of '/'")
        if this_url == url:
            raise ValidateError(message="Sorry, a url identical to the parent project is not allowed")
        # Ensure url starts with this project url
        if not url.startswith(this_url):
            url = url.lstrip("/")
            url = this_url + url
        if url in sub_paths.values():
            raise ValidateError(message="Sorry, a sub project with this url already exists")
        # add this ident and url to sub_paths
        sub_paths[proj_id] = url
        # save new subproject_paths dictionary
        self._subproject_paths = collections.OrderedDict(sorted(sub_paths.items(), key=lambda t: len(t[1].strip("/").split("/")), reverse=True))
        self.subproject_dicts[proj_id]["path"] = url
        return url

    def remove_project(self, proj):
        "Remove a project from self"
        if hasattr(proj, 'proj_ident'):
            proj_id = proj.proj_ident
        else:
            proj_id = proj
        if not proj_id:
            raise ValidateError(message="Sorry, invalid project id")
        if not proj_id.isalnum():
            raise ValidateError(message="Sorry, invalid project id")
        if proj_id not in self.subproject_paths:
            return
        del self._subproject_paths[proj_id]
        # remove from subprojects
        if proj_id in self.subprojects:
            del self.subprojects[proj_id]
        # remove from subproject_dicts
        if proj_id in self.subproject_dicts:
            del self.subproject_dicts[proj_id]

    @property
    def root_ident(self):
        'provides a root_ident attribute'
        return skiboot.Ident(self._proj_ident, 0)

    def next_ident(self):
        "Returns next Ident available by incrementing the maximum existing ident number"
        return skiboot.Ident(self._proj_ident, self.max_ident_num+1)

    def __repr__(self):
        return "Project(\'%s\', \'%s\')" % (self.proj_ident, self.url)


