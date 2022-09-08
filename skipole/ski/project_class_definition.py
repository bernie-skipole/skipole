

"""
This module defines the SkipoleProject, SkiCall, PageData, SectionData classes

SkipoleProject being the core of the project which loads
the project from JSON files and responds to incoming calls by calling the user functions

SkiCall is the class of the skicall object which is created for each incoming
call and is passed as an argument to the user functions 
"""


import copy, os, cgi, collections, html, pprint, json, shutil, uuid, sys, traceback, re, pathlib, mimetypes

from base64 import urlsafe_b64decode

from collections.abc import MutableMapping

from http import cookies

# a search for anything none-alphanumeric and not an underscore
_AN = re.compile('[^\w]')

# a search for anything none-alphanumeric, not an underscore, not -
# to allow any character in base64.urlsafe_b64encode/base64.urlsafe_b64decode
# note the = sign is not allowed, though in b64encode it is used for padding
# This is because padding is removed on sending, and added here on receiving

_AN64 = re.compile('[^\w\-]')

from . import skiboot, read_json
from .excepts import ValidateError, ServerError, FailPage, ErrorMessage, GoTo, PageError, ServeFile
from .. import textblocks

# ServerError raised in this module use codes 9000 to 9100


# These three are 'default' functions, used if the
# user functions are not given 

def _start_call(called_ident, skicall):
    "Default start_call function"
    return called_ident

def _submit_data(skicall):
    "Default submit_data function"
    return

def _end_call(page_ident, page_type, skicall):
    "Default end_call function"
    return



class SkipoleProject(object):
    """The SkipoleProject - an instance being a callable WSGI application"""

    def __init__(self, project, projectfiles, proj_data={}, start_call=None, submit_data=None, end_call=None, url="/"):
        """Loads the project from JSON files and records the user functions"""
        if _AN.search(project):
            raise ServerError(message="Error: Invalid project name, alphanumeric only")
        if '_' in project:
            raise ServerError(message="Error: Invalid project name, alphanumeric only (no underscore).")
        self._proj_ident = project
        self.projectfiles = projectfiles
        self.proj_data = proj_data
        if start_call is None:
            self.start_call = _start_call
        else:
            self.start_call = start_call
        if submit_data is None:
            self.submit_data = _submit_data
        else:
            self.submit_data = submit_data
        if end_call is None:
            self.end_call = _end_call
        else:
            self.end_call = end_call

        # initially, assume this is the root projet, and sub projects can be added
        self.rootproject = True

        # A check cookies function can be set in this project if it is added as a sub-project
        # initially it is None
        self.check_cookies = None

        # initial values, will be set from the json file
        self.brief = "Project %s" % project
        self.version = "0.0.0"
        # The url of the root folder
        url=url.strip("/").lower()
        if url:
            self.url = "/" + url + "/"
        else:
            self.url = "/"
        # The root Folder
        self.root = None
        # dictionary of special pages, key = label: value = page ident
        self.special_pages = {}
        # dictionary of sections, key = name: value = section
        self.sections = {}

        # an ordered dictionary of {proj_ident: url,...}, ordered by length of url
        self._subproject_paths = collections.OrderedDict()
        # self.subprojects is a dictionary of sub projects {proj_ident: Project instance,.....}
        self.subprojects = {}

        # dictionary of idents: to folder or page, apart from root
        # note keys are full Ident instances, values are  folder or page instances
        self.identitems = {}

        # Create an instance of the AccessTextBlocks class for this project
        self.textblocks = textblocks.AccessTextBlocks(self._proj_ident, projectfiles, skiboot.default_language())

        # maintain a cach dictionary of paths against idents {path:ident}
        self._paths = {}

        # load project from json files
        self.load_from_json()

        # and add this project to the project register
        skiboot.add_to_project_register(self)


    def set_default_language(self, language):
        "Sets the project default language"
        self.textblocks.default_language = language

    def get_default_language(self):
        "Returns the project default language"
        return self.textblocks.default_language

    default_language = property(get_default_language, set_default_language)


    # The __call__ method makes the instance callable, as required by a wsgi application

    # This method first gets cookies from method self.get_cookies()
    # it then gets status, headers and data from method self.respond()

    # self.respond() parses the requested path, and calls self.proj_respond() if the page
    # requested is part of this project, or it calls subproj.proj_respond() if the page
    # requested is part of a sub project.
    # It returns a page not found if the path does not match any page.
    # It checks for a ServerError, and returns the server error page if one is raised.

    # self.proj_respond(), parses caller ident and called ident and calls
    # self.proj_start_call() which creates the skicall object and calls the users start_call function
    # self.proj_respond() checks the ident returned from self.proj_start_call(), it then calls
    # self.read_form_data() to read any any form data submitted in the raw data, and finally calls
    # self.status_headers_data() or subproj.status_headers_data() if the page returned from start_call
    # is a page of a subproject. It checks for a ValidateError, and returns the validate error page if one is raised.

    # self.status_headers_data() calls responders, and finally calls end_call, returning the wanted status, headers and data



    def __call__(self, environ, start_response):
        "Defines this projects callable as the wsgi application"
        # get received cookies, and lang which is a tuple of (preferred language, default language)
        lang, received_cookies = self.get_cookies(environ)
        status, headers, data = self.respond(environ, lang, received_cookies)
        start_response(status, headers)
        return data


    def get_cookies(self, environ):
        """Gets cookies from environ. and places them in 'received_cookies' dictionary.
           Checks presence of language in received cookie, or environ and creates a 'lang' tuple
           consisting of (preferred language, default language)
           returns lang, received_cookies"""
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
        return lang, received_cookies


    def respond(self, environ, lang, received_cookies):
        """After cookies obtained, this is called by __call__, and returns status, headers, data
           Finds the path called, and passes the path to self.proj_respond()
           or to subproj.proj_respond() if the path indicates the call is to a sub project.
           Detects if a ServerError occurs, and if so returns status, headers, data
           for the system server_error page."""
        # The tuple s_h_data is the tuple to return, start with it as None
        s_h_data = None
        try:
            if 'PATH_INFO' in environ:
                path = environ['PATH_INFO']
            else:
                raise ServerError(message="Invalid path")

            # the path must start with this root project url
            if (path.find(self.url) != 0) and (path + "/" != self.url):
                # path does not start with the root, so send URL NOT FOUND
                return self._url_not_found(environ, path, lang)

            # This is the root project, check if the call is for a page in any sub project
            for proj, projurl in self._subproject_paths.items():
                if (path.find(projurl) == 0) or (path + "/" == projurl):
                    # this url is within a sub project
                    subproj = self.subprojects[proj]
                    if subproj.check_cookies is None:
                        # there is no check_cookies function, so no divertedcall. Call proj_respond of the sub project
                        s_h_data = subproj.proj_respond(environ, projurl, path, lang, received_cookies)
                        break
                    # the subproj has a check_cookies function, call it. Call proj_respond of the sub project
                    divertedcall = subproj.check_cookies(received_cookies, self.proj_data)
                    if divertedcall is None:
                        # check_cookies returns None, so no diversion
                        s_h_data = subproj.proj_respond(environ, projurl, path, lang, received_cookies)
                        break
                    # a divertedcall has been returned, it can be integer/tuple/label. Convert to ident
                    divertedcall = skiboot.find_ident(divertedcall, proj_ident=self._proj_ident)
                    if divertedcall is None:
                        # no ident found, so this is a ulr_not_found, leave s_h_data as None
                        break
                    # a divertedcall ident is given, but it could be to a page in this root project or any sub project
                    if divertedcall[0] == self._proj_ident:
                        # the diversion is to an ident of this root project
                        s_h_data = self.proj_respond(environ, self.url, path, lang, received_cookies, divertedcall)
                        break
                    elif divertedcall[0] in self.subprojects:
                        # the diversion is to an ident of a sub project, identify the sub project
                        subproj = self.subprojects[divertedcall[0]]
                        s_h_data = subproj.proj_respond(environ, self._subproject_paths[divertedcall[0]], path, lang, received_cookies, divertedcall)
                        break
                    else:
                        # should never occur, but if it does, leave s_h_data as None
                        break
            else:
                # the call is for a page in this root project
                s_h_data = self.proj_respond(environ, self.url, path, lang, received_cookies)

            if s_h_data is None:
                # No page to return has been found, 
                return self._url_not_found(environ, path, lang)

            if s_h_data[2] is None:
                # No page data has been given
                return self._url_not_found(environ, path, lang)

        except ServerError as e:
            # if debug is enabled, expand the exception message to include the exception trace
            if skiboot.get_debug():
                e.message += "\n"
                exc_type, exc_value, exc_traceback = sys.exc_info()
                str_list = traceback.format_exception(exc_type, exc_value, exc_traceback)
                for item in str_list:
                    e.message += item
            # ServerError has occurred, return the server error page
            page = self._system_page("server_error")
            if (not page) or (page.page_type != "TemplatePage"):
                # return the default server error page
                return self.default_server_error_page(e.message, e.code)
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
            data = page.data()
            if not data:
                return self.default_server_error_page(e.message, e.code)
            # return page data
            s_h_data = e.status, headers, data

        return s_h_data



    def proj_respond(self, environ, projurl, path, lang, received_cookies, divertedcall=None):
        """Gets any received form data, and parses the ident field if present to find the caller page and ident_data
           Calls start call, and depending on the returned page, calls the project status_headers_data method"""

        caller_page = None
        ident_data = None

        rawformdata = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ)

        # if ident present in the rawformdata it should consist of project_pagenumber_identdata
        # and so the caller page can be found from the project_pagenumber
        # identdata may not exist

        try:
            # get the caller_page, from the ident field of submitted data
            # which could be None if no ident received

            if rawformdata and ('ident' in rawformdata):
                if not hasattr(rawformdata['ident'], 'value'):
                    raise ValidateError(message="Form data not accepted, caller page ident not recognised")
                else:
                    # rawformdata has 'ident' with attribute 'value'
                    # get the caller page ident, and the ident_data received from the 'ident' field
                    # which will be project_pagenumber_b64encodeddata

                    # Note: caller_page could belong to another project, so get it using ident.item() method
                    # which will query the right project

                    # project name, number and b64 encoded data should all be ascii characters passing this test
                    if _AN64.search(rawformdata['ident'].value):
                        raise ValidateError(message="Form data not accepted, caller page ident not recognised")

                    ident_parts = rawformdata['ident'].value.split('_', 2)
                    ident_items = len(ident_parts)
                    try:
                        if ident_items == 2:
                            caller_page = skiboot.Ident(ident_parts[0], int(ident_parts[1])).item()
                        elif ident_items == 3:
                            caller_page = skiboot.Ident(ident_parts[0], int(ident_parts[1])).item()
                            b64binarydata = ident_parts[2].encode('ascii') # get the submitted data and convert to binary
                            # add padding
                            b64binarydata = b64binarydata + b"=" * (4-len(b64binarydata)%4)
                            ident_data = urlsafe_b64decode(b64binarydata).decode('utf-8') # b64 decode, and convert to string
                    except Exception:
                        caller_page = None
                    if caller_page is None:
                        raise ValidateError(message="Form data not accepted, (received ident is not valid)")
                    if caller_page.page_type != 'TemplatePage':
                        raise ValidateError(message="Form data not accepted, (caller page ident is not a template page)")

        except ValidateError as e:
            page = self._system_page("validate_error")
            if (not page) or (page.page_type != "TemplatePage"):
                return self.default_validate_error_page(e.message)
            # import any sections
            page.import_sections()
            # show message passed by the exception
            page.show_error([e.errormessage])
            # update head and body parts
            page.update(environ, {}, lang, e.ident_list)
            status, headers = page.get_status()
            data = page.data()
            if not data:
                return self.default_validate_error_page(e.message)
            # return page data
            return e.status, headers, data


        # so caller_page could be either given, or could be None

        # get the called ident, could be None
        if divertedcall is None:
            ident = self.page_ident_from_path(projurl, path)
        else:
            ident = divertedcall

        if caller_page:
            caller_page_ident = caller_page.ident
        else:
            caller_page_ident = None

        # now call the proj_start_call function which creates a skicall object and
        # calls the users start_call function, which could return a different page ident, or None

        try:

            pident, skicall = self.proj_start_call(environ,
                                                   path,
                                                   ident,
                                                   caller_page_ident,
                                                   received_cookies,
                                                   ident_data,
                                                   lang)

        except ServeFile as e:
            server_file = e.server_file
            if server_file is None:
                # URL NOT FOUND
                return
            # server_file is a path to a file on the server, so serve that file by returning status, headers, data
            try:
                data = _read_server_file(environ, server_file)
            except Exception as e:
                raise ServerError(message=f"Failed to read file {server_file}") from e
            return e.status, e.headers, data

        # pident is the ident of the diverted page or a label or url string
        if pident is None:
            return

        # get the page from pident
        if isinstance(pident, str):
            # either a label, or url
            if '/' in pident:
                # get redirector page
                return self._redirect_to_url(pident, environ, skicall.call_data, skicall.page_data, skicall.lang)
            else:
                # no '/' in pident so must be a label
                pident = skiboot.find_ident_or_url(pident, self._proj_ident)
                if not pident:
                    raise ServerError(message="Returned page ident from start_call not recognised")
                if isinstance(pident, str):
                    # must be a url, get redirector page
                    return self._redirect_to_url(pident, environ, skicall.call_data, skicall.page_data, skicall.lang)

        # so pident must be an ident
        if not isinstance(pident, skiboot.Ident):
            raise ServerError(message="Invalid ident returned from start_call")

        # pident is the ident returned from start_call, may be in a different project
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
                return subproj.status_headers_data(skicall, environ, received_cookies, rawformdata, caller_page, page, ident_list, e_list, form_data)
                
            # call status_headers_data to return status, headers and data to the top script
            return self.status_headers_data(skicall, environ, received_cookies, rawformdata, caller_page, page, ident_list, e_list, form_data)

        except ValidateError as e:
            page = self._system_page("validate_error")
            if (not page) or (page.page_type != "TemplatePage"):
                return self.default_validate_error_page(e.message)
            # import any sections
            page.import_sections()
            # show message passed by the exception
            page.show_error([e.errormessage])
            # update head and body parts
            page.update(environ, skicall.call_data, skicall.lang, e.ident_list)
            status, headers = page.get_status()
            data = page.data()
            if not data:
                return self.default_validate_error_page(e.message)
            # return page data
            return e.status, headers, page.data()



    def proj_start_call(self, environ, path, ident, caller_ident, received_cookies, ident_data, lang):
        """Creates a skicall object and calls the users start_call function
           ident is the ident of the page being called, could be None if not recognised
           Returns new called_ident, and the skicall object"""

        if not caller_ident:
            tuple_caller_ident = ()
        else:
            tuple_caller_ident = caller_ident.to_tuple()

        if ident is None:
            called_ident = None
        else:
            called_ident = ident.to_tuple()

        try:
            # create the SkiCall object
            skicall = SkiCall(environ = environ,
                              path = path,
                              project = self._proj_ident,
                              rootproject = self.rootproject,
                              caller_ident = tuple_caller_ident,
                              received_cookies = received_cookies,
                              ident_data = ident_data,
                              lang = lang,
                              proj_data = self.proj_data)

            # the skicall object is changed in place, with call_data and page_data
            # being set by the users own start_call function
            new_called_ident = self.start_call(called_ident, skicall)

            # convert returned tuple to an Ident object
            if isinstance(new_called_ident, int):
                new_called_ident = (self._proj_ident, new_called_ident)
            if isinstance(new_called_ident, tuple):
                new_called_ident = skiboot.make_ident(new_called_ident, self._proj_ident)
            # could be a label or URL
        except ServerError as e:
            raise e
        except ServeFile as e:
            raise e
##########################################
        except AssertionError as e:
            raise e
###########################################
        except Exception as e:
            raise ServerError(message = "Invalid exception in start_call function.") from e
        return new_called_ident, skicall


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



    def status_headers_data(self, skicall, environ, received_cookies, rawformdata, caller_page, page, ident_list, e_list, form_data):
        """calls responders until it can return status, headers, page.data()"""

        try:
            while page.page_type == 'RespondPage':
                ident = page.ident
                if page.responder is None:
                    raise ServerError(message="Respond page %s does not have any responder set" % (page.url,))
                try:
                    page = page.call_responder(skicall, form_data, caller_page, ident_list, rawformdata)
                    if isinstance(page, str):
                        # must be a url
                        skicall.call_data.clear()
                        skicall.page_data.clear()
                        # get redirector page
                        return self._redirect_to_url(page, environ, skicall.call_data, skicall.page_data, skicall.lang)
                except ServeFile as e:
                    server_file = e.server_file
                    if server_file is None:
                        # URL NOT FOUND
                        return
                    # server_file is a path to a file on the server, so serve that file by returning status, headers, data
                    try:
                        data = _read_server_file(environ, server_file)
                    except Exception as e:
                        raise ServerError(message=f"Failed to read file {server_file}") from e
                    return e.status, e.headers, data
                except PageError as ex:
                    # a jump to a page has occurred, with a list of errors
                    page = ex.page
                    if isinstance(page, str):
                        # must be a url
                        skicall.call_data.clear()
                        skicall.page_data.clear()
                        # get redirector page
                        return self._redirect_to_url(page, environ, skicall.call_data, skicall.page_data, skicall.lang)
                    if page.ident == ident:
                        raise ServerError(message="Invalid Failure page: can cause circulating call")
                    if page.ident in ident_list:
                        raise ServerError(message="Invalid Failure page: can cause circulating call")
                    # show the list of errors on the page
                    e_list = ex.e_list
                except GoTo as ex:
                    if ex.clear_submitted:
                        form_data.clear()
                    if ex.clear_page_data:
                        skicall.page_data.clear()
                    if ex.clear_errors:
                        ex.e_list = []
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
                        skicall.call_data.clear()
                        return self._redirect_to_url(target, environ, skicall.call_data, skicall.page_data, skicall.lang)
                    
                    # A divert to a fail page may lead to a GoTo exception which can therefore
                    # have an e_list
                    # show the list of errors on the page
                    e_list = ex.e_list

                # it is possible that a jump to a page in another project has been made
                if page.ident.proj != self._proj_ident:
                    subproj = skiboot.getproject(proj_ident=page.ident.proj)
                    return subproj.status_headers_data(skicall, environ, received_cookies, rawformdata, caller_page, page, ident_list, e_list, form_data)
                
        except (ServerError, ValidateError) as e:
            e.ident_list = ident_list
            raise e

        # the page to be returned to the client is now 'page'
        # and 'e_list' is a list of errors to be shown on it

        # call the user function end_call
        try:
            skicall.project = self._proj_ident
            skicall.proj_data = self.proj_data
            skicall.rootproject = self.rootproject
            try:
                session_string = self.end_call(page.ident.to_tuple(), page.page_type, skicall)
                if session_string:
                    # set cookie in target_page
                    page.session_cookie = "Set-Cookie", "%s=%s; Path=%s" % (skicall.project, session_string, skiboot.root_project().url)
            except FailPage as e:
                page.show_error([e.errormessage])
            finally:
                if skicall._lang_cookie:
                    page.language_cookie = skicall._lang_cookie
        except ServeFile as e:
            server_file = e.server_file
            if server_file is None:
                # URL NOT FOUND
                return
            # server_file is a path to a file on the server, so serve that file by returning status, headers, data
            try:
                data = _read_server_file(environ, server_file)
            except Exception as e:
                raise ServerError(message=f"Failed to read file {server_file}") from e
            return e.status, e.headers, data
        except GoTo as e:
            raise ServerError("Invalid GoTo exception in end_call") from e
        except Exception as e:
            raise ServerError("Invalid exception in end_call function.") from e

         # import any sections
        page.import_sections(skicall.page_data)
        if e_list:
            # show the list of errors on the page
            page.show_error(e_list)
        try:
            # now set the widget fields
            if skicall.page_data:
                page.set_values(skicall.page_data)
            page.update(environ, skicall.call_data, skicall.lang, ident_list)
        except ServerError as e:
            raise e
        except Exception as e:
            raise ServerError(message = "Exception setting page values.") from e
        status, headers = page.get_status()
        return status, headers, page.data()



    def clear_cache(self):
        "clear the cache of paths"
        self._paths = {}


    def load_from_json(self):
        "Loads project with data saved in project.json file"
        projectdict = read_json.create_project(self._proj_ident, self.projectfiles)
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

    def delete_folder_recursively(self, itemident):
        """Deletes the folder and contents with the given ident from the database.
           returns parentfolder number and change when done, raises ServerError on failure"""
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
            raise ServerError(message="The item is not a Folder")
        if item.name not in parentfolder.folders:
            raise ServerError(message="The item to delete has not been found")
        # recursive delete this item and all contents
        self._do_delete_folder_recursively(itemident)
        # create change uuid for parentfolder
        change = uuid.uuid4().hex
        num = parentfolder.ident.num
        parentfolder.change = change
        self.clear_cache()
        return num, change


    def _do_delete_folder_recursively(self, folderident):
        "Used by delete_folder_recursively to rcursively delete"
        # get the folder
        folder = self.identitems[folderident]
        page_idents = folder.page_idents()
        folder_idents = folder.folder_idents()

        # get the parent folder
        parentfolder = folder.parentfolder

        # delete all subfolders
        for folder_ident in folder_idents:
            self._do_delete_folder_recursively(folder_ident)

        # delete all pages in the folder
        for page_ident in page_idents:
            page = self.identitems[page_ident]
            del folder.pages[page.name]
            del self.identitems[page_ident]

        # and finally delete itself
        del parentfolder.folders[folder.name]
        # del this item from identitems
        del self.identitems[folderident]


    def save_item(self, item, new_parent_ident=None):
        """Saves the page or folder - used to save an altered item, not to add a new one
           If new_parent_ident is not None, indicates the item has moved to a different folder
           returns the items new change uuid"""
        if item.page_type == 'Folder':
            return self.save_folder(item, new_parent_ident)
        else:
            return self.save_page(item, new_parent_ident)


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
            if new_parent_ident.num == 0:
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
            if new_parent_ident.num == 0:
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
        if (ident.proj == self._proj_ident) and (ident.num == 0):
            return True
        return False

    def __len__(self):
        "This length does not include the root"
        return len(self.identitems)

    def __bool__(self):
        return True

    def set_special_page(self, label, target):
        "Sets a special page"
        if not label:
            raise ServerError(message="Sorry, a special page label must be given")
        if not target:
            raise ServerError(message="Sorry, a label target must be given")
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
                raise ServerError(message="Sorry, the page target is not recognised")
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


    def label_value(self, key):
        "Returns the url or tuple associated with the label"
        val = self.special_pages.get(key)
        if val is None:
            return
        labels_dict = {}
        if isinstance(val, str):
            return val
        else:
            return val.to_tuple()


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


    def _url_not_found(self, environ, path, lang):
        "Used to return the url not found page"
        page = self._system_page("url_not_found")
        page_content = "<!DOCTYPE HTML>\n<html>\nERROR:UNKNOWN URL\n</html>".encode('ascii', 'xmlcharrefreplace')
        if not page:
            return '404 Not Found', [('content-type', 'text/html')], [page_content]
        if page.page_type == "TemplatePage":
            # create an ErrorMessage with the path as the message
            err = ErrorMessage(message=html.escape(path))
            # import any sections
            page.import_sections()
            page.show_error(error_messages=[err])
        if (page.page_type == "TemplatePage") or (page.page_type == "FilePage"):
            # update head and body parts
            page.update(environ, {}, lang)
            status, headers = page.get_status()
            page_data = page.data()
            if page_data:
                return '404 Not Found', headers, page_data
        # if any other type of page, or no page content, then return this
        return '404 Not Found', [('content-type', 'text/html')], [page_content]


    def default_server_error_page(self, message='', code=0):
        "Given a ServerError exception, return a default status,headers,data"
        text_start = "<!DOCTYPE HTML>\n<html>\n<p>SERVER ERROR</p>\n<p>Error code : %s</p>\n" % (code,)
        if message:
            page_text = text_start + "<pre>%s</pre>\n</html>" % (html.escape(message),)
        else:
            page_text = text_start + "</html>"
        return '500 Internal Server Error', [('content-type', 'text/html')], [page_text.encode('ascii', 'xmlcharrefreplace')]


    def default_validate_error_page(self, message):
        "Given a ValidateError exception, return a default status,headers,data"
        if message:
            page_text = "<!DOCTYPE HTML>\n<html>\n<p>VALIDATION ERROR</p>\n<p>%s</p>\n</html>" % (html.escape(message),)
        else:
            page_text = "<!DOCTYPE HTML>\n<html>\n<p>VALIDATION ERROR</p>\n</html>"
        return '400 Bad Request', [('content-type', 'text/html')], [page_text.encode('ascii', 'xmlcharrefreplace')]


    def page_ident_from_path(self, projurl, path):
        """Tests if ident exists in the cache, return it, if not, call self.root.page_ident_from_path
           and cach the result, then return the ident. If no ident found, or if ident within a restricted folder, return None."""
        if path in self._paths:
            return self._paths[path]
        ident = None
        strip_path = path.strip("/")
        if not strip_path:
            pathlist = []
        else:
            pathlist = strip_path.split("/")
        strip_projurl = projurl.strip("/")
        # The projurl must be removed from the pathlist before the call to self.root.page_ident_from_path()
        if (not strip_projurl):
            # no projurl to remove
            ident = self.root.page_ident_from_path(self.identitems, pathlist)
        else:
            # strip_projurl may be something like "lib", remove the projurl from the pathlist
            projurl_list = strip_projurl.split("/")
            for item in projurl_list:
                if not pathlist:
                    # invalid call, the pathlist must start with the projurl
                    return
                if item == pathlist[0]:
                    pathlist.pop(0)
                else:
                    # invalid call, the pathlist must start with the projurl
                    return
            ident = self.root.page_ident_from_path(self.identitems, pathlist)
        if ident is not None:
            self._paths[path] = ident
        return ident


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

    def add_project(self, proj, url=None, check_cookies=None):
        """Add a project to self, returns the url
           proj is the sub project application.
           This adds a reference to the project to the subproject_paths, returns the sub project path"""
        if not self.rootproject:
           raise ValidateError(message="Cannot add to a sub project")

        if check_cookies is not None:
            if not callable(check_cookies):
                raise ValidateError(message="If given check_cookies must be callable as check_cookies(received_cookies, proj_data)")
        proj_id = proj.proj_ident

        # get a copy of the {proj_id:url} subproject_paths dictionary, and this projects url
        sub_paths = self._subproject_paths.copy()

        if (proj_id == self._proj_ident) or (proj_id in sub_paths):
            raise ValidateError(message="Project already exits")

        this_url = self.url

        if url is None:
            url = proj.url.strip("/").lower()
            if not url:
                url = proj_id.lower()
        else:
            url=url.strip("/").lower()
            if not url:
                raise ValidateError(message="Invalid URL passed to add_project, it must be a path longer than the root application path")
        url = "/" + url + "/"
        # Ensure url starts with this project url
        if not url.startswith(this_url):
            raise ValidateError(message="Invalid URL passed to add_project, it must be a path longer than the root application path")
        # add this ident and url to subproject_paths
        sub_paths[proj_id] = url
        # save new subproject_paths dictionary
        self._subproject_paths = collections.OrderedDict(sorted(sub_paths.items(), key=lambda t: len(t[1].strip("/").split("/")), reverse=True))
        # add the subproject to this project
        proj.rootproject = False
        proj.url = url
        proj._subproject_paths = collections.OrderedDict()
        proj.subprojects = {}
        self.subprojects[proj_id] = proj
        # set check_cookies function into the sub project
        proj.check_cookies = check_cookies
        # clear non root projects from the project register
        skiboot.del_from_project_register()
        return url

    @property
    def root_ident(self):
        'provides a root_ident attribute'
        return skiboot.Ident(self._proj_ident, 0)

    def next_ident(self):
        "Returns next Ident available by incrementing the maximum existing ident number"
        return skiboot.Ident(self._proj_ident, self.max_ident_num+1)


class SkiCall(object):
    """SkiCall is the class of the skicall object which is created for each incoming
       call and is passed as an argument to the user functions"""

    def __init__(self, environ, path, project, rootproject, caller_ident, received_cookies, ident_data, lang, proj_data):

        self.environ = environ
        self.path = path
        self.project = project
        self.rootproject = rootproject
        self.caller_ident = caller_ident
        self.received_cookies = received_cookies
        self.ident_data = ident_data
        self._lang = lang
        self._lang_cookie = None
        self.proj_data = proj_data

        self._projectfiles = skiboot.projectfiles(project)

        self.ident_list = []
        self.submit_list = []
        self.submit_dict = {'error_dict':{}}
        self.call_data = {}
        self.page_data = {}

    def update(self, itemdata):
        "Updates page_data from a PageData, SectionData or Dictionary"
        if isinstance(itemdata, PageData):
            self.page_data.update(itemdata._page_data)
        elif isinstance(itemdata, SectionData):
            # create a PageData object and update it with the section
            pd = PageData()
            pd.update(itemdata)
            self.page_data.update(pd._page_data)
        elif isinstance(itemdata, dict):
            # create a PageData object from the dictionary
            pd = PageData.from_dict(itemdict)
            # and update from that
            self.page_data.update(pd._page_data)
        else:
            raise ServerError(message="Error: invalid item used to update skicall")

        # backwards compatable stuff
        if ('content_length' not in self.page_data) and ('content-length' in self.page_data):
            val = self.page_data['content-length']
            del self.page_data['content-length']
            self.page_data['content_length'] = val
        if ('cssimport' not in self.page_data) and ('@import' in self.page_data):
            val = self.page_data['@import']
            del self.page_data['@import']
            self.page_data['cssimport'] = val

    def get_pagedata(self):
        """Returns a PageData object of the current data in skicall, note this is a copy,
          if changed it will not change the data in skicall, unless skicall.update is called with
          the new PageData object """
        return PageData.from_dict(self.page_data.copy())


    def clear_page_data(self):
        self.page_data = {}

    def clear_pagedata(self):
        self.page_data = {}

    @property
    def projectfiles(self):
        "Returns the projectfiles string"
        return self._projectfiles

    @property
    def lang(self):
        "Returns the lang tuple"
        return self._lang

    def get_language(self):
        "Returns the language string"
        return self._lang[0]

    def set_language(self, language):
        "Sets the language string and creates a language cookie with a persistance of 30 days"
        if language:
            self._lang = (language, self._lang[1])
            self._lang_cookie = "Set-Cookie", "language=%s; Path=%s; Max-Age=2592000" % (language_string, skiboot.root_project().url)

    language = property(get_language, set_language)

    @property
    def accesstextblocks(self):
        "Returns the project instance of the AccessTextBlocks class"
        this_project = skiboot.getproject(proj_ident=self.project)
        return this_project.textblocks

    def textblock(self, textref, project=None):
        """This method returns the textblock text, given a textblock reference string,
           If project is not given assumes this project, if given, project must exist as either the root,
           or a sub project of the root.
           If no textblock is found, returns None."""
        if project is None:
            project = self.project
        proj = skiboot.getproject(project)
        if proj is None:
            return
        return proj.textblocks.get_text(textref, self.lang)


    def ident_from_path(self, path, project=None):
        "Returns tuple of projectname, ident number, of the page or folder given by the path, or None if not found"
        if project is None:
            project = self.project
        proj = skiboot.getproject(project)
        if proj is None:
            return
        ident = proj.root.ident_from_path(path)
        if ident:
            return ident.to_tuple()


    def label_value(self, label, project=None):
        """Given a label, returns the associated ident or URL
           If project is not given assumes this project, if given, project must exist as either the root,
           or a sub project of the root.
           If no label is found, returns None."""
        if project is None:
            project = self.project
        proj = skiboot.getproject(project)
        if proj is None:
            return
        return proj.label_value(label)


    def projectpaths(self):
        """Returns a dictionary of project name : project path

           This method returns a dictionary of project names as keys with the project paths as values."""
        return skiboot.projectpaths()

    def makepath(self, *foldernames):
        "Returns a url path string starting with the projects path, with the given foldernames joined"
        projectpath = self.projectpaths()[self.project]
        if not foldernames:
            return projectpath
        folderpath =  "/".join(foldernames)
        if projectpath.endswith("/"):
            fullpath = projectpath + folderpath
        else:
            fullpath = projectpath + "/" + folderpath
        return fullpath


    def map_url_to_server(self, urlfolder, serverfolder):
        """Generally called in the start_call function. Maps a url folder such as
           "special/css" to a server folder such as "/home/user/thisproject/css"
           If a call is made to, say "/projectpath/special/css/myfile.css" this function will return a 
           pathlib.Path object to the file "/home/user/thisproject/css/myfile.css" if such a file
           exists. If not then None is returned.
           If the given urlfolder starts with "/" then it is an absolute path and projectpath is not prepended.
           If start_call uses this to raise a ServeFile exception, then the framework will serve the file.
           An example of usage is:
            def start_call(called_ident, skicall):
                servedfile = skicall.map_url_to_server("special/css", "/home/user/thisproject/css")
                if servedfile:
                    raise ServeFile(servedfile)
                return called_ident
        """
        server_folder = pathlib.Path(serverfolder).expanduser().resolve()
        if not server_folder.is_dir():
            return
        if not urlfolder.startswith("/"):
            # relative path, pre-pend the project url
            projectpath = self.projectpaths()[self.project]
            if projectpath.endswith("/"):
                urlfolder = projectpath + urlfolder
            else:
                urlfolder = projectpath + "/" + urlfolder
        if self.path.startswith(urlfolder):
            url_folder = pathlib.Path(urlfolder)
            # the path requested
            path = pathlib.Path(self.path)
            # path must have more elements than url_folder, as it should have at least the filename
            if len(path.parts) <= len(url_folder.parts):
                return
            servedfileparts = server_folder.parts + path.parts[len(url_folder.parts):]
            servedfile = pathlib.Path(*servedfileparts)
            if servedfile.is_file():
                return servedfile
        return

def _readfile(filepath, size):
    "Return a generator reading the file"
    with filepath.open("rb") as f:
        data = f.read(size)
        while data:
            yield data
            data = f.read(size)

def _read_server_file(environ, filepath, size=32768):
    "Returns an iterator of the file"   
    if 'wsgi.file_wrapper' in environ:
        f = filepath.open("rb")
        return environ['wsgi.file_wrapper'](f, size)
    else:
        return _readfile(filepath, size)


# An instance of this PageData is set into a skicall object to provide data for page widgets

class PageData(MutableMapping):

    page_variables = skiboot.PAGE_VARIABLES

    @classmethod
    def from_dict(cls, pagedict):
        "Returns an instance of this class given a dictionary as produced by the to_dict method"
        pd = cls()
        for key,val in pagedict.items():
            if "/" in key:
                # sectionalias/attribute
                sectionalias,att = key.split("/")
                pd.sections.add(sectionalias)
                pd._page_data[sectionalias, att] = val
            elif ":" in key:
                section_widg,fld = key.split(":")
                if "-" in section_widg:
                    # sectionalias-widget:field
                    sectionalias, widg = section_widg.split("-")
                    pd.sections.add(sectionalias)
                    pd._page_data[sectionalias, widg, fld] = val
                else:
                    # widget:field
                    pd._page_data[section_widg, fld] = val
            else:
                # a single string without / or : must be a page attribute
                pd._page_data[key] = val
        return pd


    def __init__(self):
        "_page_data will become the skicall.page_data when this object is set into skicall"
        self._page_data = {}
        self.sections = set()

    def clear(self):
        self._page_data.clear()
        self.sections.clear()

    def to_dict(self):
        """Returns a dictionary containing the data held in this object, with keys as strings
           possibly useful for storage or caching if this data is to be re-used"""
        # introduce field delimiters / : - 
        pagedict = {}
        for key, val in self._page_data.items():
            if isinstance(key,str):
                # keys are strings - page attributes, leave as strings
                pagedict[key] = val
            elif isinstance(key, tuple):
                if len(key) == 2:
                    if key[0] in self.sections:
                        # keys are (sectionalias, attribute) set as "sectionalias/attribute"
                        pagedict[key[0]+'/'+key[1]] = val
                    else:
                        # or keys are (widgetname, fieldname) set as "widgetname:fieldname"
                        pagedict[key[0]+':'+key[1]] = val
                elif len(key) == 3:
                    # keys will be of the form sectionalias-widgetname:fieldname
                    pagedict[key[0]+'-'+key[1]+':'+key[2]] = val
        return pagedict


    def get_value(self, sectionalias, widgetname, fieldname):
        """Returns the value set in this field, if item not found, return None.
           Set sectionalias to None if this widget is not in a section"""
        if sectionalias is None:
            key = (widgetname, fieldname)
            if not self._valid_widgfield(key):
                return
            if key in self._page_data:
                return self._page_data[key]
            else:
                return
        if sectionalias not in self.sections:
            # it does not exist
            return None
        key = (sectionalias, widgetname, fieldname)
        if key in self._page_data:
            return self._page_data[key]


    def get_section(self, sectionalias):
        "Retrieve a section, if it has not been added to the page, return None"
        if sectionalias not in self.sections:
            # it does not exist
            return None
        s = SectionData(sectionalias)
        for key, val in self._page_data.items():
            if not isinstance(key, tuple):
                continue
            if key[0] == sectionalias:
                if len(key) == 2:
                    s._section_data[key[1]] = val
                else:
                    s._section_data[key[1], key[2]] = val
        return s


    def delete_section(self, sectionalias):
        "Deletes a section"
        if sectionalias not in self.sections:
            return
        self.sections.remove(sectionalias)
        newdict = {}
        for key, val in self._page_data.items():
            if isinstance(key, tuple) and (len(key) >= 2) and (key[0] == sectionalias):
                continue
            newdict[key] = val
        self._page_data = newdict


    def update(self, item):
        "Update with a PageData, SectionData or a dictionary"
        if isinstance(item, SectionData):
            # update from SectionData
            sectionalias = item.sectionalias
            if sectionalias not in self.sections:
                # test no widget clash
                for key in self:
                    # iterates through every widget, with key being (widg,fld)
                    if sectionalias == key[0]:
                        # sectionalias clashes with a widget
                        raise KeyError
            self._add_section(item)
        elif isinstance(item, PageData):
            # update this PageData with another PageData object
            # test the sections in the item object do not clash with widgets in this object
            for key in self:
                # iterates through every widget in self, with key being (widg,fld)
                if key[0] in item.sections:
                    # widget in self has the same name as a section in item
                    raise KeyError
            self._page_data.update(item._page_data)
            self.sections.update(item.sections)
        elif isinstance(item, dict):
            # create a PageData object from the dictionary, and update with that
            pd = PageData.from_dict(item)
            for key in self:
                # iterates through every widget in self, with key being (widg,fld)
                if key[0] in pd.sections:
                    # widget in self has the same name as a section in pd
                    raise KeyError
            self._page_data.update(pd._page_data)
            self.sections.update(pd.sections)
        else:
            raise KeyError


    def _add_section(self, section):
        "Add section data"
        sectionalias = section.sectionalias
        self.sections.add(sectionalias)
        for at, val in section._section_data.items():
            if isinstance(at, str):
                # A section attribute
                if val is None:
                    continue
                self._page_data[sectionalias, at] = val
        # add items from section
        for key,val in section.items():
            self._page_data[sectionalias, key[0], key[1]] = val
                

    def __getattr__(self, name):
        "Get a page attribute from the _page_data dictionary"
        if name not in self.page_variables:
            raise AttributeError
        if name in self._page_data:
            return self._page_data[name]


    def __setattr__(self, name, value):
        "Sets a page attribute"
        if name in self.page_variables:
            if value is None:
                if name in self._page_data:
                    del self._page_data[name]
            else:
                self._page_data[name] = value
            return
        # for all other values
        super().__setattr__(name, value)


    def _valid_widgfield(self, key):
        if not isinstance(key, tuple):
            return False
        if len(key) != 2:
            # All widgfields have a two element tuple as key
            return False
        if key[0] in self.sections:
            # this key name is used as a section alias
            return False
        return True


    def __setitem__(self, key, value):
        if self._valid_widgfield(key):
            if (value is None) and (key in self._page_data):
                del self._page_data[key]
            else:
                self._page_data[key] = value
        else:
            raise KeyError


    def __delitem__(self, key):
        if self._valid_widgfield(key):
            if key in self._page_data:
                del self._page_data[key]
        else:
            raise KeyError


    def __getitem__(self, key):
        if self._valid_widgfield(key):
            return self._page_data[key]
        else:
            raise KeyError


    def __iter__(self):
        page_data = self._page_data
        for key in page_data.keys():
            if self._valid_widgfield(key):
                yield key


    def __len__(self):
        "Returns the number of widgfields associated with the page"
        page_data = self._page_data
        length = 0
        for key in page_data.keys():
            if self._valid_widgfield(key):
                length += 1
        return length


# instances of this SectionData is used with the update method of a PageData object to provide data for sections

class SectionData(MutableMapping):

    section_variables = skiboot.SECTION_VARIABLES

    @classmethod
    def from_dict(cls, sectiondict, sectionalias):
        "Returns an instance of this class given a dictionary as produced by the to_dict method"
        sd = cls(sectionalias)
        newdict = {}
        for key,val in sectiondict.items():
            if not isinstance(key, str):
                raise KeyError
            if "/" in key:
                alias, att = key.split("/")
                # discard alias, as it is to be replaced by sectionalias
                if att not in cls.section_variables:
                    raise KeyError
                newdict[att] = val
            elif ":" in key:
                section_widg, fld = key.split(":")
                if "-" in section_widg:
                    alias,widg = section_widg.split("-")
                    newdict[widg,fld] = val
                else:
                    raise KeyError
            else:
                # not an attribute or widget
                raise KeyError
        # assign newdict to the new class
        sd._section_data = newdict
        return sd


    def __init__(self, sectionalias):
        """sectionalias is the name of this section as set in the page"""
        self._section_data = {}
        self._sectionalias = sectionalias

    def clear(self):
        self._section_data = {}

    def to_dict(self):
        """Returns a dictionary containing the data held in this object, with keys as strings
           possibly useful for storage or caching if this data is to be re-used"""
        # introduce field delimiter :  
        sectiondict = {}
        for key, val in self._section_data.items():
            if isinstance(key,str):
                # keys are strings - section attributes, introduce sectionalias/attribute
                if val is None:
                    continue
                sectiondict[self._sectionalias + "/" + key] = val
            elif isinstance(key, tuple):
                if len(key) == 2:
                    # keys are (widgetname, fieldname) set as "sectionalias-widgetname:fieldname"
                    sectiondict[self._sectionalias + "-" + key[0]+':'+key[1]] = val
        return sectiondict


    def copy(self, newalias):
        "Return a copy of this section with a new sectionalias"
        s = self.__class__(newalias)
        s._section_data = self._section_data.copy()
        return s


    def multiply(self, number):
        """Sets the multiplier to number and returns the given number of SectionData objects
           each with sectionalias of sectionalias_0, sectionalias_1,.. etc"""
        if number <= 1:
            return []
        sectionlist = []
        for n in range(number):
            newalias = self.sectionalias+ "_" + str(n)
            newsection = self.copy(newalias)
            newsection.multiplier = 0
            sectionlist.append(newsection)
        self.multiplier = number
        return sectionlist


    def __getattr__(self, name):
        "Get a section attribute from the _section_data dictionary"
        if name == "sectionalias":
            return self._sectionalias
        if name not in self.section_variables:
            raise AttributeError
        return self._section_data[name]


    def __setattr__(self, name, value):
        "Sets a section attribute"
        if name == '_section_data':
            # this is required to insert values into self._section_data
            super().__setattr__(name, value)
            return
        if name == '_sectionalias':
            # this is required to insert the section name into self._sectionalias
            super().__setattr__(name, value)
            return
        if name not in self.section_variables:
            raise AttributeError
        self._section_data[name] = value


    def _valid_widgfield(self, key):
        if not isinstance(key, tuple):
            return False
        if len(key) != 2:
            # All widgfields have a two element tuple as key
            return False
        return True

    def __setitem__(self, key, value):
        if self._valid_widgfield(key):
            self._section_data[key] = value
        else:
            raise KeyError

    def __delitem__(self, key):
        if self._valid_widgfield(key):
            del self._section_data[key]
        else:
            raise KeyError

    def __getitem__(self, key):
        if self._valid_widgfield(key):
            return self._section_data[key]
        else:
            raise KeyError

    def __iter__(self):
        for key in self._section_data.keys():
            if self._valid_widgfield(key):
                yield key

    def __len__(self):
        "Returns the number of widgfields associated with the section"
        length = 0
        for key in self._section_data.keys():
            if self._valid_widgfield(key):
                length += 1
        return length




