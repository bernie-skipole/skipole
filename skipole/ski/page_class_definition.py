


"""
This module defines the page objects
"""


import os, mimetypes, copy, collections, json, re, uuid, pprint
from string import Template
from urllib.parse import quote
from base64 import urlsafe_b64encode

from . import skiboot
from .tag import Part, ClosedPart, TextBlock, Section
from .widgets import links
from .excepts import ValidateError, ServerError, SkiError

# a search for anything none-alphanumeric and not an underscore
_AN = re.compile('[^\w]')


class ParentPage(object):

    def __init__(self, name="", brief = "New Page"):
        """Initiates a ParentPage instance

        name: a url friendly page name
        """
        # self._parentfolder_ident is set when a page is added to a folder.
        self._parentfolder_ident = None
        if name:
            self._name = name.lower()
        else:
            self._name = ""
        self.ident = None
        self.status = '200 OK'
        self.brief = brief
        # the change is a uuid which alters whenever the page changes
        self.change = uuid.uuid4().hex
        self.ident_data = ''
        # Set by end_call
        self.session_cookie = ()
        self.language_cookie = ()
        # page settings, provided by users page_data
        self.page_settings = {}
        # values to create a page header
        self.headers = []
        self.header_content_length = None
        self.header_content_type = None
        self.header_cache_control = None
        self.header_Pragma = None
        self.header_Expires = None


    def _set_enable_cache(self, enable_cache):
        "Sets enable cache in header"
        if enable_cache:
            self.header_cache_control = 'max-age=3600'
            self.header_Pragma = None
            self.header_Expires = None
        else:
            self.header_cache_control = 'no-cache, no-store, must-revalidate'
            self.header_Pragma = 'no-cache'
            self.header_Expires = '0'

    def _get_enable_cache(self):
        if self.header_cache_control == 'max-age=3600':
            return True
        return False

    enable_cache = property(_get_enable_cache, _set_enable_cache)



    def _create_header(self):
        if self.headers:
            # headers have been set by the user, only set cookies
            if self.session_cookie:
                self.headers.append(self.session_cookie)
            if self.language_cookie:
                self.headers.append(self.language_cookie)
            return
        if self.header_content_length:
            self.headers.append(("content-length", self.header_content_length))
        if self.header_content_type:
            self.headers.append(("content-type", self.header_content_type))
        if self.header_cache_control:
            self.headers.append(("cache-control", self.header_cache_control))
        if self.header_Pragma:
            self.headers.append(("Pragma", self.header_Pragma))
        if self.header_Expires:
            self.headers.append(("Expires", self.header_Expires))
        if self.session_cookie:
            self.headers.append(self.session_cookie)
        if self.language_cookie:
            self.headers.append(self.language_cookie)


    def get_name(self):
        "The page name"
        return self._name

    def set_name(self, name):
        "Ensure name is lower case"
        self._name = name.lower()

    name = property(get_name, set_name)


    def _get_mimetype(self):
        if self.header_content_type: return self.header_content_type
        # mimetype not set, so guess it
        if hasattr(self, 'filepath'):
            if self.filepath:
                name = os.path.basename(self.filepath)
            else:
                name=self._name
        else:
            name = self._name
        mimetypes.init()
        t, e = mimetypes.guess_type(name, strict=False)
        if t:
            return t
        else:
            return "application/octet-stream"


    def _set_mimetype(self, mimetype):
        self.header_content_type = mimetype


    mimetype = property(_get_mimetype, _set_mimetype)


    @property
    def page_type(self):
        return self.__class__.__name__

    @property
    def ident_data_string(self):
        "Encode ident_data as a base64 string"
        if not self.ident:
            return
        if self.ident_data:
            # encode the ident data as base64, and append it as a string to the page ident
            b64binarydata = urlsafe_b64encode(self.ident_data.encode('utf-8')).rstrip(b"=")  # removes final '=' padding
            return str(self.ident) + '_' + b64binarydata.decode('ascii')
        else:
            return str(self.ident)        

    @property
    def proj_ident(self):
        return self.ident.proj

    @property
    def project(self):
        if self.ident:
            return skiboot.getproject(proj_ident=self.ident.proj) 

    def copy(self, name, brief):
        "Returns a deepcopy of this page, with new name and brief, parentfolder and ident are None"
        copy_page = copy.deepcopy(self.project.get_item(self.ident))
        copy_page._parentfolder_ident = None
        copy_page.ident = None
        copy_page.name = name
        copy_page.brief = brief
        copy_page.change = uuid.uuid4().hex
        return copy_page

    def root(self):
        "Returns the page root folder"
        if self.ident():
            proj = self.project()
            if proj is None:
                return
            return proj.root

    def get_parentfolder(self):
        "Uncopied parent folder"
        if self._parentfolder_ident is None:
            return None
        return skiboot.get_item(self._parentfolder_ident)

    def set_parentfolder(self, parentfolder):
        "Warning, this does not set this page into the parents pages dictionary, it just sets this parentfolder attribute"
        if parentfolder is None:
            self._parentfolder_ident = None
        else:
            self._parentfolder_ident = parentfolder.ident

    parentfolder = property(get_parentfolder, set_parentfolder)

    def get_folder(self):
        "folder is an alias of parentfolder"
        return self.get_parentfolder()

    def set_folder(self, parentfolder):
        "folder is an alias of parentfolder"
        self.set_parentfolder(parentfolder)

    folder = property(get_folder, set_folder)

    @property
    def parentfolder_ident(self):
        "Returns the parentfolder ident"
        return self._parentfolder_ident

    @property
    def url(self):
        if self._parentfolder_ident is None:
            return ""
        return self._parentfolder_ident.url() + self.name


    def parent_list(self):
        "returns a list of (name, identnumber) starting at root"
        p_list = self.parentfolder.parent_list()
        p_list.append((self.name, self.ident.num))
        return p_list


    @property
    def restricted(self):
        "returns restricted status of parentfolder"
        parentfolder = self.parentfolder
        if parentfolder is None:
            return True
        return parentfolder.restricted


    def show_error(self, error_messages=None):
        """override"""
        pass

    def set_values(self, page_data):
        """Checks for special page values"""
        page_setting_list = skiboot.PAGE_VARIABLES
        # set all page settings into self.page_settings
        # and remove them from page_data
        for item in page_setting_list:
            if item in page_data:
                self.page_settings[item] = page_data.pop(item)

        # deal with these particular settings
        if ('status' in self.page_settings) and self.page_settings['status']:
            self.status = self.page_settings['status']
        if ('headers' in self.page_settings) and self.page_settings['headers']:
            self.headers = self.page_settings['headers']
        if ('mimetype' in self.page_settings) and self.page_settings['mimetype']:
            self.header_content_type = self.page_settings['mimetype']
        if ('content_length' in self.page_settings) and self.page_settings['content_length']:
            self.header_content_length = str(self.page_settings['content_length'])
        if 'enable_cache' in self.page_settings:
            self._set_enable_cache(bool(self.page_settings['enable_cache']))
        if 'ident_data' in self.page_settings:
            # set ident_data in page
            self.ident_data = str(self.page_settings['ident_data'])


    def update(self, environ, call_data, lang, ident_list=[]):
        """Normally overriden to add specific page attributes"""
        # create the http header
        self._create_header()


    def import_sections(self, page_data=None):
        "Only used by Template and SVG, everything else just returns"
        return


    def get_status(self):
        "Returns (status, headers)"
        return self.status, self.headers

    def __eq__(self, other):
        return self.ident == other.ident

    def __ne__(self, other):
        return self.ident != other.ident

    def __bool__(self):
        return True


class TemplatePageAndSVG(ParentPage):
    "Acts as parent to template pages and svg pages"


    def __init__(self, name="", brief = "New Page"):
        """Initiates a TemplatePageAndSVG instance
        """
        ParentPage.__init__(self, name=name, brief=brief)
        # self.widgets is a widget name -> widget dictionary
        self.widgets = {}
        # self.section_places is a section alias -> SectionPlaceHolder dictionary
        self.section_places = {}
        # dictionary of sections, section alias -> section
        # this is filled in when the sections are imported
        self.sections = {}
        # a list of section aliases, filled in when sections are imported
        self.section_aliases = []


    def set_values(self, page_data):
        """Sets the widget fields to the given values.
           page_data is either a dictionary of
           {(pagesectionname,widgetname,fieldname):value, ..}
           or a dictionary of
           {'pagesectionname-widgetname:fieldname':value, ..}
           or a dictionary of
          {WidgField_object:value, ..}
           or a dictionary of
          {pagesectionname:value, ..}

           NOTE : currently untested, but this should work with index as well
           so if the widgfield is of format (pagesectionname,widgetname,fieldname,index)
           or 'pagesectionname-widgetname:fieldname-index' then the single indexed field value
           should be updated
           """
        ParentPage.set_values(self, page_data)
        # the above has removed page settings from page_data
        for widgfield, value in page_data.items():
            self._widget_set_value(widgfield, value)


    def _widget_set_value(self, widgfield, value):
        "Given a widgfield, checks its value"

        # does this widgfield specify a section, and field rather than widget
        widglist = []
        if isinstance(widgfield, str) and (':' in widgfield):
            widglist = widgfield.split(':')
        elif isinstance(widgfield, list) or isinstance(widgfield, tuple):
            widglist = widgfield

        if len(widglist) == 2:
            sectionname, field = widglist
            if sectionname in self.section_aliases:
                # Its a section
                if sectionname not in self.sections:
                    # This sectionname is a valid section alias, but is not in self sections, as it has not been imported
                    # due to its show value being set to False
                    return
                if field == 'section_class':
                    self.sections[sectionname].set_class(value)
                if field == 'hide':
                    self.sections[sectionname].set_hide(value)
                return
        # so its not a section
        widget, fieldname = self.widget_from_field(widgfield)
        if (widget is not None) and fieldname:
            widget.set_value(fieldname, value)



    def widget_from_field(self, widgfield):
        """Return the (widget, fieldname) given a widgfield, which is either a string of
         pagesectionname-widgetname:fieldname or a list/tuple or cfg.WidgField object, if widget not found in the page,
         (None, fieldname) will be returned.
        If widget is found, but the fieldname is not in the widget, return (widget, None)
        The widget returned is the actual widget instance in the page, and fieldname is the widgets field name
        Please note - if the given widgfield has an index, fieldname will be 'fieldname-index'"""
        if not widgfield:
            raise ValidateError(message = "Invalid field given to page.widget_from_field method")
        widg_field = skiboot.make_widgfield(widgfield)
        # widg_field is now a WidgField object with s, w, f and i attributes
        if (not widg_field.w) or (not widg_field.f):
            raise ValidateError(message = "Field %s not recognised" % (widgfield,))
        widget = self.widget_from_name(widg_field.s, widg_field.w)
        if widg_field.f == 'show_error':
            return widget, 'show_error'
        # check is the fieldname in the widget
        if widget is not None:
            if not widget.is_fieldname_in_widget(widg_field.f):
                return widget, None
        if widg_field.i:
            fieldname = widg_field.f + '-' + widg_field.i
        else:
            fieldname = widg_field.f
        return widget, fieldname

    def widget_from_name(self, section_name, widgetname):
        """Return the widget given a widgetname, if widget not found in the page, None will be returned
           This should only be called after sections have been imported and returns the actual widget in the page"""
        if not section_name:
            # widget is not in a section, should be local to this page
            return self.widgets.get(widgetname)
        if section_name not in self.sections:
            return None
        sectionpart = self.sections[section_name]
        return sectionpart.widgets.get(widgetname)


    def copy_widget_from_name(self, section_name, widgetname):
        """Return the widget given a widgetname, if widget not found in the page or section, None will be returned
           This can be called before or after sections have been imported and returns a copy of the widget"""
        if not section_name:
            # widget is not in a section, should be local to this page
            widget = self.widgets.get(widgetname)
        elif section_name in self.sections:
            section = self.sections[section_name]
            widget = section.widgets.get(widgetname)
        elif section_name in self.section_places:
            # self.section_places is a section alias -> SectionPlaceHolder dictionary
            sectionplaceholder = self.section_places.get(section_name)
            if not sectionplaceholder:
                return
            section = sectionplaceholder.get_section()
            widget = section.widgets.get(widgetname)
        elif "_" in section_name:
            result = self.widget_from_multiplier(section_name, widgetname)
            if result:
                sectionplaceholder,widget = result
            else:
                widget = None
        else:
            return
        if widget is None:
            return
        return copy.deepcopy(widget)


    def widget_from_multiplier(self, section_name, widgetname):
        """Return (sectionplaceholder, widget) if section_name is a multiplied section, such as name_3, return None on failure"""
        if "_" not in section_name:
            return
        sname, snumber = section_name.rsplit('_', 1)
        try:
            snumber = int(snumber)
        except Exception:
            return
        sectionplaceholder = self.section_places.get(sname)
        if not sectionplaceholder:
            return
        section = sectionplaceholder.get_section()
        return sectionplaceholder, section.widgets.get(widgetname)


    def append_scriptlink(self, label):
        """Used to append a scriptlink to head, overridden in class Page"""
        pass

    def import_sections(self, page_data=None):
        "Imports the project sections into the page"
        self.sections = {}
        self.section_aliases = []
        for placename, placeholder in self.section_places.items():
            # get top part of placeholder location
            pagepart = placeholder.pagepart
            if pagepart == 'head':
                toppart = self.head
            elif pagepart == 'body':
                toppart = self.body
            elif pagepart == 'svg':
                toppart = self.svg
            else:
                raise ServerError(message = 'Invalid section placeholder in page %s' % (self.ident,))
            if page_data and (placename,'multiplier') in page_data:
                try:
                    multiplier = int(page_data[placename,'multiplier'])
                except Exception:
                    placeholder.multiplier = 0
                else:
                    placeholder.multiplier = multiplier
            ########
            # set all section aliases, including multiplied aliases into self.section_aliases list
            self.section_aliases.append(placename)
            if placeholder.multiplier > 0:
                for m in range(placeholder.multiplier):
                    self.section_aliases.append(placename + "_" + str(m))

            # if this section has show False, then do not import it
            showsection = placeholder.show
            if page_data and (placename,'show') in page_data:
                showsection = page_data[placename,'show']

            if not showsection:
                continue
            #########

            if placeholder.multiplier > 0:
                for m in range(placeholder.multiplier):
                    self._import_multiplied_section(m, placeholder, toppart, page_data)
                continue
            section_name = placeholder.section_name
            sectionpart = self.project.section(section_name)
            # sectionpart is a tag.Section
            if not isinstance(sectionpart, Section):
                continue
            # gives sectionpart and subparts an ident of page_ident_name_locationnumbers
            # and sets sectionpart into self.sections
            sectionpart.widgets = {}
            sectionpart.section_places = {}
            sectionpart.set_idents(str(self.ident) + '_' + placename, sectionpart.widgets, sectionpart.section_places, embedded=(section_name,'',None))
            # If no id placed in the top tag, inserts the section placename
            if not sectionpart.has_attrib('id'):
                sectionpart.insert_id(id_string=placename)
            self.sections[placename] = sectionpart
            # Set section widgets field displaynames
            for widget in sectionpart.widgets.values():
                # Note - this is called on named widgets only
                widget.set_placename(section_name, placename)
            # insert sectionpart at the point where the placeholder is
            toppart.set_location_value(placeholder.ident_list, sectionpart)
            # add section scriptlinks
            if self.page_type == 'TemplatePage':
                if sectionpart.validator_scriptlinks:
                    for link_label in sectionpart.validator_scriptlinks:
                        self.append_scriptlink(link_label)
                for widget in sectionpart.widgets.values():
                    # get 'ski_modulename'
                    link_label = "ski_" + widget.__class__.__module__.split(".")[-1]
                    # add a link in the page head to the widget module javascript file
                    self.append_scriptlink(link_label)


    def _import_multiplied_section(self, m, placeholder, toppart, page_data):
        "If a placeholder has a multiplier, import its section multiple times inside a div"
        placename = placeholder.placename + "_" + str(m)
        section_name = placeholder.section_name
        sectionpart = self.project.section(section_name)
        # sectionpart is a tag.Section
        if not isinstance(sectionpart, Section):
            return
        if (placename,'show') in page_data:
            sectionpart.show = bool(page_data[placename,'show'])
        # gives sectionpart and subparts an ident of page_ident_name_locationnumbers
        # and sets sectionpart into self.sections
        sectionpart.widgets = {}
        sectionpart.section_places = {}
        sectionpart.set_idents(str(self.ident) + '_' + placename, sectionpart.widgets, sectionpart.section_places, embedded=(section_name,'',None))
        # If no id placed in the top tag, inserts the section placename
        if not sectionpart.has_attrib('id'):
            sectionpart.insert_id(id_string=placename)
        self.sections[placename] = sectionpart
        # Set section widgets field displaynames
        for widget in sectionpart.widgets.values():
            # Note - this is called on named widgets only
            widget.set_placename(section_name, placename)
        # now the sectionpart has to be set within a div which is set at the placeholder location
        if m == 0:
            topdiv = Part(tag_name=placeholder.mtag)
            if page_data:
                if (placeholder.placename,'section_class') in page_data:
                    topdiv.set_class(page_data[placeholder.placename,'section_class'])
                if (placeholder.placename,'multiplier_tag') in page_data:
                    topdiv.tag_name = page_data[placeholder.placename,'multiplier_tag']
                if self.page_type == 'TemplatePage':
                    # hide not relevant to svg
                    if (placeholder.placename,'hide') in page_data:
                        topdiv.set_hide(bool(page_data[placeholder.placename,'hide']))
            topdiv.insert_id(id_string=placeholder.placename)
            topdiv[0] = sectionpart
            toppart.set_location_value(placeholder.ident_list, topdiv)
        else:
            location = placeholder.ident_list[:]
            location.append(m)
            toppart.insert_location_value(location, sectionpart)
        # add section scriptlinks
        if self.page_type == 'TemplatePage':
            if sectionpart.validator_scriptlinks:
                for link_label in sectionpart.validator_scriptlinks:
                    self.append_scriptlink(link_label)
            for widget in sectionpart.widgets.values():
                # get 'ski_modulename'
                link_label = "ski_" + widget.__class__.__module__.split(".")[-1]
                # add a link in the page head to the widget module javascript file
                self.append_scriptlink(link_label)


class TemplatePage(TemplatePageAndSVG):
    """A template page object
    """

    def __init__(self, name="",
                       brief = "New Page",
                       show_backcol=False,
                       backcol="#FFFFFF",
                       last_scroll=True,
                       default_error_widget=None,
                       lang=None,
                       interval = 0,
                       interval_target=None,
                       catch_to_html=None):
        """Initiates a Page instance

        name: a url friendly page name
        brief: description of the page
        show_backcol: True if colour can be placed in the html tag
        backcol: The colour to place in the html tag
        last_scroll: True if the page is to remember its last scroll position
        default_error_widget: widget name to display errors, if no other widget specified in the error call
        lang: language string to place in the html tag
        interval: Time interval in integer seconds for repeated call for JSON update, 0 if not used.
        interval_target: ident or label (not URL) to call for the JSON update
        catch_to_html: ident or label (not URL) to call when a javascript error is thrown
        """

        TemplatePageAndSVG.__init__(self, name=name, brief=brief)

        self.header_content_type = 'text/html'

        # set up page head
        self.head = Part(tag_name="head")
        self.head.brief = "The head section of the page"
        # Set up the page body
        self.body = Part(tag_name="body")
        self.body.brief = "The body section of the page"

        # html lang setting
        if lang is None:
            self.lang = skiboot.default_language()
        else:
            self.lang = lang

        # ERROR MESSAGES
        # This widget is the default widget where errors are displayed, if no other error location is specified
        if default_error_widget is None:
            self._default_error_widget = skiboot.WidgField(s='', w="top_error", f='', i='')
        else:
            self.default_error_widget = default_error_widget
        # flag if any error present
        self.page_in_error = False
        # store errors as they arrive
        # self.stored_errors will be a dictionary with key widgetname (of the widget to show the error)
        # and value being the message to be displayed by the widget
        self.stored_errors = {}

        self.show_backcol = show_backcol
        self.backcol = backcol
        self.catch_to_html = catch_to_html

        # A list of appended script links in head
        self._headlinks = []

        # Used to hold javascript created at run time
        self._js = ''

        # A javscript string for each widgfield
        self._scriptcontents = ''

        # last scroll is True if the page is to be restored to the last scrolled position
        self.last_scroll = last_scroll

        # if requesting a json target to be called at regular intervals,
        # self.interval is the time in seconds, and self.interval_target
        # is the target url
         
        self.interval = interval
        if interval_target:
            self.interval_target = interval_target
        else:
            self.interval_target = None

        # self.validator_scriptlinks is a list of validator module ski_name's
        # calculated when the page is saved, and used 
        # to add links to the validator js modules in the page head
        self._validator_scriptlinks = []

        # These will be added to the page javascript within the jquery $(function() { ... })
        # handler which ensures these are run after the dom is loaded
        self._add_storage = ''
        self._add_jscript = ''

        # holds cookies to send
        self._sendcookies = None

    @property
    def validator_scriptlinks(self):
        return self._validator_scriptlinks

    def load_validator_scriptlinks(self):
        "Called when page saved to database"
        self._validator_scriptlinks = []
        val_modules = []
        for widget in self.widgets.values():
            for field in widget.fields.values():
                val_list = field.val_list
                for val in val_list:
                    mod_name = val.__class__.__module__.split(".")[-1]
                    if mod_name not in val_modules:
                        val_modules.append(mod_name)
        for mod_name in val_modules:
            link_label = 'ski_' + mod_name
            if link_label not in self._validator_scriptlinks:
                self._validator_scriptlinks.append(link_label)

    def import_sections(self, page_data=None):
        "Imports javascript modules used by widgets and validators, and then imports sections"
        if self._validator_scriptlinks:
            for link_label in self._validator_scriptlinks:
                        self.append_scriptlink(link_label)
        for widget in self.widgets.values():
            # get 'ski_modulename'
            link_label = "ski_" + widget.__class__.__module__.split(".")[-1]
            # add a link in the page head to the widget module javascript file
            self.append_scriptlink(link_label)
        # import sections using parent method
        TemplatePageAndSVG.import_sections(self, page_data)

    def location_item(self, location):
        "Returns the part or widget at location"
        location_string, container_number, location_list = location
        if not location_string:
            return
        if container_number is None:
            # Not in a widget
            if location_string == 'body':
                if not location_list:
                    return self.body
                return self.body.get_location_value(location_list)
            elif location_string == 'head':
                if not location_list:
                    return self.head
                return self.head.get_location_value(location_list)
            # not found
            return
        # location string must be a widget name
        # so part is within a widget container within the page
        if location_string not in self.widgets:
            return
        widget = self.widgets.get(location_string)
        if widget is None:
            return
        if widget.can_contain():
            if not location_list:
                # return the container
                return widget.container_part(container_number)
            else:
                return widget.get_from_container(container_number, location_list)
        # part not found
        return

    def set_default_error_widget(self, errorwidget):
        "Widget only, no field information"
        self._default_error_widget = skiboot.make_widgfield(errorwidget, widgetonly=True)

    def get_default_error_widget(self):
        return self._default_error_widget

    default_error_widget = property(get_default_error_widget, set_default_error_widget)

    def append_scriptlink(self, label):
        """Used to append a scriptlink to head"""
        if label not in self._headlinks:
            self._headlinks.append(label)
            # create a scriptlink
            scriptlink = Part(tag_name = "script", attribs={"src":"{" + label + "}"}, brief='script link to %s' % (label,))
            self.head.append(scriptlink)

    def add_javascript(self, contents):
        "Adds contents to self._scriptcontents"
        self._scriptcontents += contents


    def make_js(self, ident_list, environ, call_data, lang):
        "Auto generates the javascript for this page, sets into self._js, called after head and body updates"
        # for each part in the page body, get its associated javascript, and add to scriptcontents
        # send self, plus call arguments so part.make_js has all data necessary
        self.body.make_js(self, ident_list, environ, call_data, lang)
        # The start of the script is created in the .data function
        scriptmiddle = """
// Widget functions
$(function(){
"""
        if self._add_storage:
            scriptmiddle += self._add_storage
        if self._add_jscript:
            scriptmiddle += self._add_jscript

        # and create the script end
        scriptend = """
  if(SKIPOLE.interval && SKIPOLE.IntervalTarget) {
    SKIPOLE.interval_id = setInterval(SKIPOLE.refreshjson, SKIPOLE.interval*1000, SKIPOLE.IntervalTarget);
    }
"""
        # SKIPOLE.interval_id is needed so clearInterval(SKIPOLE.interval_id) can be called
        # if the interval changes
        if self.last_scroll:
            # restore to last store position
            scriptend += """
  SKIPOLE.restorepagepos();
"""
        # and set an event to store window position on unload
        scriptend += """
  if(typeof(Storage) !== "undefined") {
    $(window).on('unload', function(){
      // on unloading, store the x and y position of the window
      sessionStorage.setItem('%s_y', $(window).scrollTop().toString());
      sessionStorage.setItem('%s_x', $(window).scrollLeft().toString());
      });
   }
});
""" % (self.ident, self.ident)
        self._js = scriptmiddle + self._scriptcontents + scriptend


    def update(self, environ, call_data, lang, ident_list=[]):
        "Updates page and body parts, lang is a tuple of (language, default_language)"
        # show all errors on the page
        self._show_errors_on_update()
        self.body.update(self, ident_list, environ, call_data, lang, str(self.ident)+"_body")
        # update page head parts (done last as previous updates may change css)
        self.head.update(self, ident_list, environ, call_data, lang, str(self.ident)+"_head")
        # create javascript for widgets, this is set into self._js and appended
        # to self.head in the data function
        self.make_js(ident_list, environ, call_data, lang)
        # create the http header
        self._create_header()
        # add cookies
        if self._sendcookies:
            for morsel in self._sendcookies.values():
                self.headers.append(("Set-Cookie", morsel.OutputString()))


    def set_idents(self):
        """Each widget adds its ident, to itself, and to the self.widgets dictionary
           Each sectionplaceholder adds its ident, to itself, and to the self.section_places dictionary
           This is called when the page is created and added to a folder, it is also
           called when an existing page is edited, and the page saved"""
        self.widgets = {}
        self.section_places = {}
        self.body.set_idents(str(self.ident)+"_body", self.widgets, self.section_places)
        self.head.set_idents(str(self.ident)+"_head", self.widgets, self.section_places)


    def validate(self, widgfield, value, environ, lang, form_data, call_data, page_data):
        """Given a widgfield, its value and other parameters, call its widget validate function
           which returns (value, error_list)"""
        if not widgfield:
            raise ValidateError(message = "Invalid widget-field, unable to validate")
        widg_field = skiboot.make_widgfield(widgfield)

        # widg_field is now a WidgField object with s, w, f and i attributes
        if (not widg_field.w) or (not widg_field.f):
            raise ValidateError(message = "Field %s not recognised" % (widgfield,))

        # Find the widget in this page, to call its validate function
        widget = None

        if widg_field.s:
            # self.section_places is a page section name -> SectionPlaceHolder dictionary
            sectionplaceholder = self.section_places.get(widg_field.s)
            if sectionplaceholder:
                sectionpart = sectionplaceholder.get_section()
                widget = sectionpart.widgets.get(widg_field.w)
            elif "_" in widg_field.s:
                result = self.widget_from_multiplier(widg_field.s, widg_field.w)
                if result:
                    sectionplaceholder, widget = result                
        else:
            # widget is not in a section, should be local to this page
            widget = self.widgets.get(widg_field.w)

        if widget is None:
            raise ValidateError(message = "Widget %s not found in page %s" % (widg_field.w, self.ident))

        # check is the fieldname in the widget
        if not widget.is_fieldname_in_widget(widg_field.f):
            raise ValidateError(message = "Field %s not found in widget %s, page %s" % (widg_field.f, widg_field.w, self.ident))

        # validate
        newvalue, error_list = widget.validate(widg_field, value, environ, lang, form_data, call_data, self.ident)

        # errors in same section as the errored widget need s value changing
        if widg_field.s:
            for error in error_list:
                if error.section == sectionplaceholder.section_name:
                    error.section = widg_field.s

        return newvalue, error_list


    def show_error(self, error_messages=[]):
        """Stores the errors to display on the page in dictionary self.stored_errors.
           These are subsequently set on the widgets during the page update by _show_errors_on_update().
           Any fields which are just to be flagged as errored, via the widgets mark_field_in_error are set here.
           error_messages is a list of ErrorMessage instances (class defined in excepts)"""
        # an ErrorMessage has attributes message,
        #                                section,
        #                                widget,
        self.page_in_error = True
        for e in error_messages:
            # e is an instance of ErrorMessage
            if e.widget:
                displaywidget = skiboot.WidgField(s=e.section, w=e.widget, f='', i='')
            else:
                # use page default error location 
                displaywidget = self.default_error_widget
            if not displaywidget:
                # nowhere to display an error
                continue
            if displaywidget not in self.stored_errors:
                self.stored_errors[displaywidget] = e.message
            else:
                # displaywidget is already in self.stored_errors
                # existing messages have priority
                # unless existing message is an empty string
                if not self.stored_errors[displaywidget]:
                    self.stored_errors[displaywidget] = e.message

                
    def _show_errors_on_update(self):
        """Called on page update to show all stored errors"""
        if not self.page_in_error:
            # show_error never called - so no error condition
            return
        # if no error widget or message given, show the page default error widget
        if not self.stored_errors:
            widget = self.widget_from_name(self.default_error_widget.s, self.default_error_widget.w)
            if widget is None:
                return
            widget.show_error(message='')
            return
        # There are stored messages, so call the errored widgets
        for displaywidget, message in self.stored_errors.items():
            if not displaywidget:
                continue
            widget = self.widget_from_name(displaywidget.s, displaywidget.w)
            if widget is None:
                continue
            widget.show_error(message)

    def set_values(self, page_data):
        """Passes on to parent set_values to set the widgets, then checks for special page template settings"""
        TemplatePageAndSVG.set_values(self, page_data)
        try:
            if 'set_cookie' in self.page_settings:
                # sets the cookies in the page headers
                self._sendcookies = self.page_settings['set_cookie']
            if 'CatchToHTML' in self.page_settings:
                self.catch_to_html = self.page_settings['CatchToHTML']
            if 'interval' in self.page_settings:
                interval = 0
                try:
                    interval = int(self.page_settings['interval'])
                except:
                    raise ServerError("Invalid interval")
                else:
                    self.interval=interval
            if 'IntervalTarget' in self.page_settings:
                self.interval_target = self.page_settings['IntervalTarget']
            if 'last_scroll' in self.page_settings:
                self.last_scroll = bool(self.page_settings['last_scroll'])
            if 'lang' in self.page_settings:
                if isinstance(self.page_settings['lang'], tuple) or isinstance(self.page_settings['lang'], list):
                    self.lang = self.page_settings['lang'][0]
                else:
                    self.lang = self.page_settings['lang']
            if 'show_backcol' in self.page_settings:
                self.show_backcol = bool(self.page_settings['show_backcol'])
            if 'backcol' in self.page_settings:
                self.backcol = self.page_settings['backcol']
            if 'body_class' in self.page_settings:
                self.body.update_attribs({'class':self.page_settings['body_class']})
            if 'show_error' in self.page_settings:
                self._widget_set_value(self._default_error_widget.set_field(f='show_error'), self.page_settings['show_error'])
            if 'add_jscript' in self.page_settings:
                self._add_jscript = self.page_settings['add_jscript']
            if ('localStorage' in self.page_settings) or ('sessionStorage' in self.page_settings):
                self._add_storage += """  if (typeof(Storage) !== "undefined") {
"""
                if 'localStorage' in self.page_settings:
                    if not isinstance(self.page_settings['localStorage'], dict):
                        raise ServerError("localStorage must be a dictionary")
                    for key,val in self.page_settings['localStorage'].items():
                        escapedval = json.dumps(val)
                        self._add_storage += """    localStorage.setItem("%s", %s);
""" % (key,escapedval)
                if 'sessionStorage' in self.page_settings:
                    if not isinstance(self.page_settings['sessionStorage'], dict):
                        raise ServerError("sessionStorage must be a dictionary")
                    for key,val in self.page_settings['sessionStorage'].items():
                        escapedval = json.dumps(val)
                        self._add_storage += """    sessionStorage.setItem("%s", %s);
""" % (key,escapedval)
                self._add_storage += """    }
"""
        except ServerError:
            raise
        except Exception as e:
            raise ServerError("Error while setting values into Template page") from e


    def data(self):
        "Returns the page as a list of binary strings"
        # set data into the page
        page_javascript = """// javascript for skipole project %s page ident %s
//<![CDATA[
SKIPOLE.identdata = '%s';
SKIPOLE.default_error_widget = '%s';
SKIPOLE.widget_register = {};
SKIPOLE.interval = %s;
"""  % (self.ident.proj, self.ident.num, self.ident_data_string, self.default_error_widget, self.interval)
        if self.interval_target:
            intervalurl = skiboot.get_url(self.interval_target, self.proj_ident)
            if intervalurl:
                page_javascript += "SKIPOLE.IntervalTarget = \'" + quote(intervalurl, safe='/:?&=') + "\';\n"
        if self.catch_to_html:
            catchurl = skiboot.get_url(self.catch_to_html, self.proj_ident)
            if catchurl:
                page_javascript += "SKIPOLE.CatchToHTML = \'" + quote(catchurl, safe='/:?&=') + "\';\n"

        # set a list of section alias names, to include section alias, and multiplied section alias
        section_alias_list = list(self.sections.keys())
        for alias in self.section_places.keys():
            if alias not in section_alias_list:
                section_alias_list.append(alias)

        page_javascript += "SKIPOLE.sections =  " + str(section_alias_list) + ";\n"

        # append javascript to page head
        self.head.append(Part(tag_name="script", text=page_javascript + self._js + "//]]>\n"))

        topstring = "<!DOCTYPE HTML>\n<html"
        if self.show_backcol:
            back = " style=\"background-color: %s;\"" % self.backcol
            topstring += back
        if self.lang:
            topstring += " lang=\"%s\"" % self.lang
        topstring += ">\n"
        topbytes = topstring.encode('ascii', 'xmlcharrefreplace')

        docbytes = [topbytes]
        docbytes.extend(d.encode('ascii', 'xmlcharrefreplace') for d in self.head.data())
        docbytes.extend(d.encode('ascii', 'xmlcharrefreplace') for d in self.body.data())
        docbytes.append("\n</html>".encode('ascii', 'xmlcharrefreplace'))
        return docbytes

    def __str__(self):
        "Returns the page as a string"
        topstring = "<!DOCTYPE HTML>\n<html"
        if self.show_backcol:
            back = " style=\"background-color: %s;\"" % self.backcol
            topstring += back
        if self.lang:
            topstring += " lang=\"%s\"" % self.lang
        topstring += ">"
        return topstring + str(self.head) + str(self.body) + "\n</html>"

    def __repr__(self):
        if self.ident:
            return "Template Page ident %s" % (self.ident,)
        else:
            return "Template Page name %s" % (self.name,)


class RespondPage(ParentPage):


    def __init__(self, name, brief = "New RespondPage", responder=None):
        ParentPage.__init__(self, name=name, brief=brief)
        # A responder is an instance of the Respond class
        # - or more usually, an instance of a child of the Respond class
        self.responder = responder

    def call_responder(self, skicall, form_data, caller_ident, ident_list, rawformdata):
        """Checks for circulating calls, then updates ident_list with this pages ident,
           then calls the respond objects call method, note rawformdata is a cgi.FieldStorage object"""
        if self.responder is None:
            raise ServerError(message = "No responder has been assigned to this page")
        if self.ident in ident_list:
            raise ServerError(message="Circulating call to Respond page: ident %s" % (self.ident,))
        ident_list.append(self.ident)
        proj = self.ident.proj

        # create submit_dict
        skicall.submit_dict["responder_brief"] = self.brief
        skicall.submit_dict["number"] = self.ident.num

        page = self.responder(skicall, form_data, caller_ident, ident_list, proj, rawformdata)
        return page

    def set_values(self, page_data):
        return

    def __repr__(self):
        if self.ident:
            return "Respond Page ident %s" % (self.ident,)
        else:
            return "Respond Page name %s" % (self.name,)



class SVG(TemplatePageAndSVG):
    """An SVG image
    """

    def __init__(self, name="", brief = "New SVG Page", width="100", height="100", css_list=[], enable_cache=False):
        """Initiates a Page instance

        name: a url friendly page name
        """
        TemplatePageAndSVG.__init__(self, name=name, brief=brief)

        self.header_content_type = 'image/svg+xml'

        self.css_list = [skiboot.make_ident(ident) for ident in css_list]
        self.svg = Part(tag_name="svg", attribs = {"xmlns":"http://www.w3.org/2000/svg",
                                                   "baseProfile":"full",
                                                   "version":"1.1",
                                                   "width":width,
                                                   "height":height})
        self.svg.brief = "The svg section of the page"
        self._set_enable_cache(enable_cache)



    def location_item(self, location):
        "Returns the part or widget at location"
        location_string, container_number, location_list = location
        if not location_string:
            return
        if container_number is None:
            # Not in a widget
            if location_string == 'svg':
                if not location_list:
                    return self.svg
                return self.svg.get_location_value(location_list)
            # not found
            return
        # location string must be a widget name
        # so part is within a widget container within the page
        if location_string not in self.widgets:
            return
        widget = self.widgets.get(location_string)
        if widget is None:
            return
        if widget.can_contain():
            if not location_list:
                # return the container
                return widget.container_part(container_number)
            else:
                return widget.get_from_container(container_number, location_list)
        # part not found
        return



    def get_width(self):
        return self.svg.get_attrib_value("width")

    def set_width(self, width):
        self.svg.update_attribs({"width":width})

    width = property(get_width, set_width)

    def get_height(self):
        return self.svg.get_attrib_value("height")

    def set_height(self, height):
        self.svg.update_attribs({"height":height})

    height = property(get_height, set_height)

    def update(self, environ, call_data, lang, ident_list=[]):
        "Updates svg parts"
        ident_string = str(self.ident)+"_svg"
        self.svg.update(self, ident_list, environ, call_data, lang, ident_string)
        # create the http header
        self._create_header()

    def add_javascript(self, contents):
        "Currently not used"
        pass

    def set_idents(self):
        """Each widget adds its ident, to itself, and to the self.widgets dictionary
           Each sectionplaceholder adds its ident, to itself, and to the self.section_places dictionary
           This is called when the page is created and added to a folder, it is also
           called when an existing page is edited"""
        self.widgets = {}
        self.section_places = {}
        self.svg.set_idents(str(self.ident)+"_svg", self.widgets, self.section_places)

    def show_error(self, error_messages=None):
        """Currently not used"""
        return


    def set_values(self, page_data):
        """Passes on to parent set_values to set the widgets, checks for special svg page template values"""
        TemplatePageAndSVG.set_values(self, page_data)
        try:
            if 'width' in self.page_settings:
                self.width = self.page_settings['width']
            if 'height' in self.page_settings:
                self.height = self.page_settings['height']
        except ServerError:
            raise
        except Exception as e:
            raise ServerError("Error while setting values into SVG page") from e


    def data(self):
        "Returns the page as a list of binary strings"

        # note xmls initial dtd statements and stuff left out as per
        # https://developer.mozilla.org/en-US/docs/Web/SVG/Tutorial/Getting_Started

        svg_list = self.svg.data()
        return [d.encode('ascii', 'xmlcharrefreplace') for d in svg_list]


    def __str__(self):
        return str(self.svg)

    def __repr__(self):
        if self.ident:
            return "SVG Page ident %s" % (self.ident,)
        else:
            return "SVG Page name %s" % (self.name,)


class FilePage(ParentPage):
    """A page representing a file to be downloaded to the user.
    """

    def __init__(self, name="", brief="", filepath="", mimetype=None, enable_cache=False):
        "If no filepath given, assumes a file of the same name under the project static folder"
        if not brief:
            brief = "Link to %s" % filepath
        ParentPage.__init__(self, name=name, brief=brief)

        if mimetype:
            self.header_content_type = mimetype

        self.filepath = filepath
        self._absolute_filepath = None
        self._set_enable_cache(enable_cache)
        # environ, set by the update method
        self._environ = None


    def get_filepath(self):
        # self._filepath is a list of path parts
        if (not self._filepath):
            self._filepath = [self.proj_ident, "static"]
            self._filepath.append(self.name)
        return os.sep.join(self._filepath)

    def set_filepath(self, path):
        if path:
            if ('/' in path) and ('\\' in path):
                raise ValidateError("Invalid path")
            if '/' in path:
                self._filepath = path.strip('/').split('/')
            elif '\\' in path:
                self._filepath = path.strip('\\').split('\\')
            else:
                self._filepath = [path]
        else:
            self._filepath = []
        for item in self._filepath:
            if (not item) or (item == '.') or (item == '..'):
                self._filepath = []
                raise ValidateError("Invalid path")

    filepath = property(get_filepath, set_filepath)


    def set_values(self, page_data):
        "Set filepath"
        ParentPage.set_values(self, page_data)
        try:
            if 'filepath' in self.page_settings:
                self.filepath = self.page_settings['filepath']
        except ServerError:
            raise
        except Exception as e:
            raise ServerError("Error while setting values into File page") from e


    def update(self, environ, call_data, lang, ident_list=[]):
        """"If filepath set, then this is the file returned, if not, then projectfiles/project/static/name is returned"""
        self._environ = environ
        if not self.filepath:
            raise ServerError(message="Filepath not set")
        self._absolute_filepath = os.path.join(skiboot.projectfiles(self.proj_ident), self.filepath)
        if not os.path.isfile(self._absolute_filepath):
            # no need to do anything further
            return
        # get length of file
        if not self.header_content_length:
            self.header_content_length = str(os.path.getsize(self._absolute_filepath))
        # if mimetype not given, guess it
        if not self.header_content_type:
            self.header_content_type = self.mimetype
        # create the http header
        self._create_header()


    def _readfile(self, size=32768):
        "Return a generator reading the file"
        with open(self._absolute_filepath, "rb") as f:
            data = f.read(size)
            while data:
                yield data
                data = f.read(size)


    def data(self):
        "returns an iterator reading the file"
        if not os.path.isfile(self._absolute_filepath):
            # no need to do anything further
            return
        try:
            size = 32768
            if 'wsgi.file_wrapper' in self._environ:
                f = open(self._absolute_filepath, "rb")
                return self._environ['wsgi.file_wrapper'](f, size)
            else:
                return self._readfile(size)
        except IOError:            
            return ["<!DOCTYPE HTML>\n<html>ERROR:UNABLE TO OPEN FILE\n</html>".encode('ascii', 'xmlcharrefreplace')]


    def __str__(self):
        return self.filepath

    def __repr__(self):
        if self.ident:
            return "File Page ident %s" % (self.ident,)
        else:
            return "File Page name %s" % (self.name,)


class CSS(ParentPage):
    """A CSS object represents a css file
    """


    def __init__(self, name="", brief="New CSS Page", style=collections.OrderedDict(), enable_cache=False):
        "style held as ordered dictionary each value being a list of lists"
        ParentPage.__init__(self, name=name, brief=brief)

        self.header_content_type = "text/css"

        # self.style is a dictionary with keys being css selectors
        # and values being a list of two element lists
        # acting as css declaration blocks.

        self.style = style
        self.colour_substitution = {}

        # imports
        self.imports = []

        self._set_enable_cache(enable_cache)


    def set_values(self, page_data):
        """cssimport, ident_data"""
        ParentPage.set_values(self, page_data)
        try:
            if 'colour_substitution' in self.page_settings:
                self.colour_substitution = self.page_settings['colour_substitution']
            if 'cssimport' in self.page_settings:
                if isinstance(self.page_settings['cssimport'], list):
                    self.imports = self.page_settings['cssimport']
                elif isinstance(self.page_settings['cssimport'], str):
                    self.imports = [self.page_settings['cssimport']]
        except ServerError:
            raise
        except Exception as e:
            raise ServerError("Error while setting values into File page") from e


    def selector_list(self):
        return list(self._style.keys())

    def selector_properties(self, selector):
        "Returns the property strings of the selector"
        style_text = ""
        if selector not in self._style:
            return ""
        value = self._style[selector]
        if value:
            # value is a list of two element lists
            # created value_list, which is value, sorted by the first element in each sub list
            value_list = sorted(value, key=lambda val : val[0])
            for a,b in value_list:
                style_text += "{a} : {b};\n".format(a=a, b=b)
        return style_text

    # property style is a dictionary of lists
    def get_style(self):
        return self._style

    def set_style(self, style):
        if isinstance(style, collections.OrderedDict):
            self._style = style
        elif isinstance(style, dict):
            self._style = collections.OrderedDict([(selector,value) for selector,value in style.items()])
        else:
            self._style = collections.OrderedDict()

    style = property(get_style, set_style)

    def write(self, filepath):
        "Writes a css file to the given filepath"
        if not self._style:
            return
        with open(filepath, "w") as f:
            f.write(self.__str__())

    def data(self):
        "Returns the page as a list of binary strings"
        if not self._style:
            return []
        style_binary = ["@charset \"UTF-8\";\n".encode('UTF-8')]
        if self.imports:
            for imp in self.imports:
                style_binary.append("@import : {imp};\n".format(imp=imp.strip(';')).encode('UTF-8'))
        for selector,value in self._style.items():
            if value:
                style_binary.append("\n{selector} {{".format(selector=selector).encode('UTF-8'))
                # value is a list of two element lists
                # created value_list, which is value, sorted by the first element in each sub list
                value_list = sorted(value, key=lambda val : val[0])
                for a,b in value_list:
                    if self.colour_substitution and ('$' in b):
                        c = Template(b)
                        b= c.safe_substitute(self.colour_substitution)
                    style_binary.append("\n{a} : {b};".format(a=a, b=b).encode('UTF-8'))
                style_binary.append("}\n".encode('UTF-8'))
        return style_binary

    def __str__(self):
        "Returns the css page as a string"
        if not self._style:
            return ""
        style_text = ""
        if self.imports:
            for imp in self.imports:
                style_text += "@import : {imp};\n".format(imp=imp.strip(';'))
        for selector, value in self._style.items():
            if value:
                style_text += """
{selector} {{""".format(selector=selector)
                # value is a list of two element lists
                # created value_list, which is value, sorted by the first element in each sub list
                value_list = sorted(value, key=lambda val : val[0])
                for a,b in value_list:
                    style_text += "\n{a} : {b};".format(a=a, b=b)
                style_text += "}\n"
        return style_text

    def __repr__(self):
        if self.ident:
            return "CSS Page ident %s" % (self.ident,)
        else:
            return "CSS Page name %s" % (self.name,)


class JSON(ParentPage):
    """A JSON object represents dynamically created json data
    """

    def __init__(self, name="", brief="New JSON Page", content=None, enable_cache=False):
        "content held as ordered dictionary"
        ParentPage.__init__(self, name=name, brief=brief)
        self.header_content_type = "application/json"
        if content:
            self.content = content
        else:
            self.content = collections.OrderedDict()
        self._set_enable_cache(enable_cache)
        # setting jsondict overrides self.content
        self.jsondict = None

    def add_widgfield(self, widgfield, value):
        "Add widgfield and value to self.content"
        # ensure widgfield is a skiboot.WidgField object
        fld = skiboot.make_widgfield(widgfield)
        if not fld:
            return
        self.content[str(fld)] = value

    def del_widgfield(self, widgfield):
        "Removes widgfield from self.content"
        # ensure widgfield is a skiboot.WidgField object
        fld = skiboot.make_widgfield(widgfield)
        if not fld:
            return
        strfld = str(fld)
        if strfld in self.content:
            del self.content[strfld]

    def set_values(self, page_data):
        """Sets json content"""
        if not page_data:
            return
        ParentPage.set_values(self, page_data)
        if 'ClearAllErrors' in self.page_settings:
            self.content["ClearAllErrors"] = bool(self.page_settings['ClearAllErrors'])

        if 'localStorage' in self.page_settings:
            if not isinstance(self.page_settings['localStorage'], dict):
                raise ServerError("localStorage must be a dictionary")
            self.content["localStorage"] = self.page_settings['localStorage']
 
        if 'sessionStorage' in self.page_settings:
            if not isinstance(self.page_settings['sessionStorage'], dict):
                raise ServerError("sessionStorage must be a dictionary")
            self.content["sessionStorage"] = self.page_settings['sessionStorage']

        if 'throw' in self.page_settings:
            self.content["throw"] = self.page_settings['throw']

        if "IntervalTarget" in self.page_settings:
            url = skiboot.get_url(self.page_settings["IntervalTarget"], proj_ident=self.proj_ident)
            if url:
                self.content["IntervalTarget"] = url

        if 'interval' in self.page_settings:
            interval=0
            try:
                interval = int(self.page_settings['interval'])
            except:
                raise ServerError("Invalid interval")
            else:
                self.content["interval"]=interval
        if "CatchToHTML" in self.page_settings:
            url = skiboot.get_url(self.page_settings["CatchToHTML"], proj_ident=self.proj_ident)
            if url:
                self.content["CatchToHTML"] = url

        if "JSONtoHTML" in self.page_settings:
            url = skiboot.get_url(self.page_settings["JSONtoHTML"], proj_ident=self.proj_ident)
            if url:
                self.content["JSONtoHTML"] = url
                return

        if 'lang' in self.page_settings:
            item = self.page_settings['lang']
            if isinstance(item, 'tuple') or isinstance(item, 'list'):
                self.content['lang'] = item[0]
            else:
                self.content['lang'] = item

        for field, item in page_data.items():
            if isinstance(field, str):
                self.content[field] = item
            else:
                widgfield = str(skiboot.make_widgfield(field))
                self.content[widgfield] = item

    def update(self, environ, call_data, lang, ident_list=[]):
        "Adds session_cookie, and also ident_list if debug mode is on"
        if skiboot.get_debug():
            # include environ, call_data and ident_list in json file
            self.content['environ'] = pprint.pformat(environ)
            if call_data:
                self.content['call_data'] = pprint.pformat(call_data)
            if ident_list:
                idents = []
                for ident in ident_list:
                    item = skiboot.from_ident(ident)
                    idents.append([ident.to_comma_str(), item.responder.__class__.__name__, item.brief])
                idents.append([self.ident.to_comma_str(), 'This page', self.brief])
                self.content['ident_list'] = idents
            else:
                self.content['ident_list'] = [[self.ident.to_comma_str(), 'This page', self.brief]]
        self._create_header()

    def show_error(self, error_messages=None):
        """Sets show error in page data"""
        if not error_messages:
            # send a default page error
            self.content["show_error"] = ""
            return
        for e in error_messages:
            # e is an instance of ErrorMessage
            if e.widget:
                displaywidget = str(skiboot.WidgField(s=e.section, w=e.widget, f='show_error', i=''))
            else:
                displaywidget = "show_error"
            self.content[displaywidget] = e.message

    def data(self):
        "Returns the page as a list of binary strings"
        if self.jsondict is not None:
            return [json.dumps(self.jsondict).encode('UTF-8')]
        if self.ident_data:
            # encode the ident data as base64
            b64binarydata = urlsafe_b64encode(self.ident_data.encode('utf-8')).rstrip(b"=")  # removes final '=' padding
            self.content['ident_data'] = b64binarydata.decode('ascii')
        elif 'ident_data' in self.content:
            del self.content['ident_data']
        return [json.dumps(self.content).encode('UTF-8')]

    def __str__(self):
        "Returns the json page as a string"
        if self.jsondict is not None:
            return json.dumps(self.jsondict)
        if self.ident_data:
            # encode the ident data as base64
            b64binarydata = urlsafe_b64encode(self.ident_data.encode('utf-8')).rstrip(b"=")  # removes final '=' padding
            self.content['ident_data'] = b64binarydata.decode('ascii')
        elif 'ident_data' in self.content:
            del self.content['ident_data']
        return json.dumps(self.content)

    def __repr__(self):
        if self.ident:
            return "JSON Page ident %s" % (self.ident,)
        else:
            return "JSON Page name %s" % (self.name,)

