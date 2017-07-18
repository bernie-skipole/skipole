####### SKIPOLE WEB FRAMEWORK #######
#
# info.py  - widgets displaying page info
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



"""This module defines various widgets which provide information"""
import time

from string import Template

from .. import skiboot
from .. import tag
from . import Widget, ClosedWidget, FieldArg, FieldArgList, FieldArgTable, FieldArgDict


class ServerTimeStamp(Widget):
    """A widget containing the current server time. consists of a span with time stamp, if an error is raised, the span class
         becomes the error_class and the span text changes to the error message"""

    error_location = 0

    arg_descriptions = {
                        'timestamp':FieldArg("text", '', jsonset=True),
                        'error_class':FieldArg("cssclass", ''),
                        'utc':FieldArg("boolean", True)
                       }

    def __init__(self, name=None, brief='', **field_args):
        """
        timestamp: normally empty and timestamp will automatically be displayed, or other text can be set here.
        error_class: The class of the widget set on error - which provides the appearance via CSS
        utc: If True, time is utc, if False it is local time
        """
        Widget.__init__(self, name=name, tag_name="span", brief=brief, **field_args)
        self[0] = ""

    def _build(self, page, ident_list, environ, call_data, lang):
        "Build the element"
        if self.error_status:
            self.update_attribs({"class":self.get_field_value('error_class')})
        else:
            # set timer or string
            if self.get_field_value("timestamp"):
                self[0] = self.get_field_value("timestamp")
            elif self.get_field_value("utc"):
                self[0] = time.strftime("%c", time.gmtime())
            else:
                self[0] = time.strftime("%c", time.localtime())


    def _build_js(self, page, ident_list, environ, call_data, lang):
        """Sets error_class into fieldvalues"""
        if not self.get_field_value('error_class'):
            return ''
        return self._make_fieldvalues('error_class')

    def __str__(self):
        """Returns a text string to illustrate the widget"""
        return """
<span>  <!--  class set to widget_class, changes to error_class on error -->
  <!-- Normally timestamp, replaced by error message on error -->
</span>
"""


class PageIdent(Widget):
    """A widget containing the given ident which is set within the text
         If no page ident is given, shows ident of the current page"""

    error_location = 0

    arg_descriptions = {'page_ident':FieldArg("ident", ''),
                        'error_class':FieldArg("cssclass", '')
                       }

    def __init__(self, name=None, brief='', **field_args):
        """
        page_ident: The ident of a page or folder, converted to string
        error_class: The class of the widget set on error - which provides the appearance via CSS
        """
        Widget.__init__(self, name=name, tag_name="span", brief=brief, **field_args)
        self[0] = ""

    def _build(self, page, ident_list, environ, call_data, lang):
        "Build the element"
        if not self[0]:
            if self.get_field_value("page_ident"):
                self[0] = self.get_field_value("page_ident").to_comma_str()
            else:
                self[0] = page.ident.to_comma_str()
        if self.error_status:
            self.update_attribs({"class":self.get_field_value('error_class')})

    def _build_js(self, page, ident_list, environ, call_data, lang):
        """Sets error_class into fieldvalues"""
        if not self.get_field_value('error_class'):
            return ''
        return self._make_fieldvalues('error_class')

    def __str__(self):
        """Returns a text string to illustrate the widget"""
        return """
<span>  <!--  class set to widget_class, changes to error_class on error -->
  <!-- string value of the page_ident, replaced by error message on error -->
</span>
"""


class Version(Widget):
    """A span showing the project version of the page it is in"""

    # This class does not display any error messages
    display_errors = False

    arg_descriptions = {}

    def __init__(self, name=None, brief='', **field_args):
        """
        Shows project version
        """
        Widget.__init__(self, name=name, tag_name="span", brief=brief, **field_args)
        self[0] = ""

    def _build(self, page, ident_list, environ, call_data, lang):
        "Build the element"        
        self[0] = page.project.version

    def __str__(self):
        """Returns a text string to illustrate the widget"""
        return """
<span>  <!--  class set to widget_class -->
  <!-- string of the project version -->
</span>
"""


class SkipoleVersion(Widget):
    """A span showing this version of the skipole framework"""

    # This class does not display any error messages
    display_errors = False

    arg_descriptions = {}

    def __init__(self, name=None, brief='', **field_args):
        """
        Shows skipole version
        """
        Widget.__init__(self, name=name, tag_name="span", brief=brief, **field_args)
        self[0] = ""

    def _build(self, page, ident_list, environ, call_data, lang):
        "Build the element"        
        self[0] = skiboot.version()

    def __str__(self):
        """Returns a text string to illustrate the widget"""
        return """
<span>  <!--  class set to widget_class -->
  <!-- string of the skipole framework version -->
</span>
"""


class Redirector(Widget):
    """A widget containing javascript which redirects the page to the url
       Once the page is loaded, the redirection occurs, so normally
       this is the only widget on the page
       A textblock is displayed with the link to the url if the client has javascript disabled"""

    # This class does not display any error messages
    display_errors = False

    arg_descriptions = {'url':FieldArg("text", ''),
                        'textblock_ref':FieldArg("textblock_ref", ""),
                        'text_refnotfound':FieldArg("text", ""),
                        'text_replaceblock':FieldArg("text", "If this page does not redirect automatically, follow this link:")
                       }

    def __init__(self, name=None, brief='', **field_args):
        """
        url: the url to redirect to
        textblock_ref: The reference of the TextBlock appearing in the paragraph
        text_refnotfound: text to appear if the textblock is not found
        text_replaceblock: text set here will replace the textblock
        """
        Widget.__init__(self, name=name, tag_name="div", brief=brief, **field_args)

        self[0] = tag.Part(tag_name='script', attribs={"type":"text/javascript"})
        self[1] = tag.Part(tag_name='p')


    def _build(self, page, ident_list, environ, call_data, lang):
        "Build the widget"
        url = self.get_field_value("url")
        if not url:
            self.show = False
            return
        self[0][0] = "window.location.replace(\"%s\");" % (url,)

        # define the textblock
        tblock = self.get_field_value("textblock_ref")
        tblock.text = self.get_field_value('text_replaceblock')
        tblock.failmessage = self.get_field_value('text_refnotfound')
        tblock.proj_ident = page.proj_ident

        self[1][0] = tblock
        self[1][1] = tag.Part(tag_name='a', attribs={"href":url}, text=url)


    def __str__(self):
        """Returns a text string to illustrate the widget"""
        return """
<div>  <!--  class set to widget_class -->
  <script type="text/javascript">
     <!-- window.location.replace("url"); -->
  </script>
  <p>
    <!-- text_replaceblock or the textblock text here -->
    <a href="url"> 
        <!-- url --> 
    </a>
  </p>
</div>
"""

