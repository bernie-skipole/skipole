####### SKIPOLE WEB FRAMEWORK #######
#
# links.py  - Contains link widgets
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

"Contains link widgets"

from urllib.parse import quote, quote_plus
from string import Template
import json

from .. import skiboot, tag
from . import Widget, ClosedWidget, FieldArg, FieldArgList, FieldArgTable, FieldArgDict


class Link(Widget):
    """A link to the page with the given ident, label or url, with a text string as the
       visible content and two optional get fields.
       On error replace the link by the error message"""

    # This class does not display any error messages
    display_errors = False

    arg_descriptions = {'link_ident':FieldArg("url", ''),
                        'get_field1':FieldArg("text", "", valdt=True),
                        'get_field2':FieldArg("text","", valdt=True),
                        'content':FieldArg("text", "", jsonset=True),
                        'new_window':FieldArg("boolean", False),
                        'force_ident':FieldArg("boolean", False)
                       }

    def __init__(self, name=None, brief='', **field_args):
        """
        link_ident: The url, ident or label to link with
        get_field1: Optional 'get' string set in the target url
        get_field2: Optional second 'get' string set in the target url
        content: The text to be placed within the link, if none given, the page url will be used
        new_window: if True, the target='_blank' attribute will be set, to open the target in a new window
        force_ident: If True then the page ident will be included, even if no get fields set
                     If False, the page ident will only be included if a get field is set
        """
        Widget.__init__(self, name=name, tag_name="a", brief=brief, **field_args)
        # where content can be placed
        self[0] = ''

    def _build(self, page, ident_list, environ, call_data, lang):
        "Build the link"
        # self[0] is initially set as the empty string ''
        if self.get_field_value("content"):
            self[0] = self.get_field_value("content")
        if not self.get_field_value("link_ident"):
            self._error = "Warning: broken link"
            return
        url = skiboot.get_url(self.get_field_value("link_ident"), proj_ident=page.proj_ident)
        if not url:
            self._error = "Warning: broken link"
            return
        if not self[0]:
            # if no content, place the page url as content
            self[0] = url
        # create a url for the href
        get_fields = {self.get_formname("get_field1"):self.get_field_value("get_field1"),
                      self.get_formname("get_field2"):self.get_field_value("get_field2")}
        # add get fields and page ident_data to the url (defined in tag.ParentPart)
        url = self.make_get_url(page, url, get_fields, self.get_field_value("force_ident"))
        self.update_attribs({"href": url})
        if self.get_field_value("new_window"):
            self.update_attribs({"target":"_blank"})

    def __str__(self):
        """Returns a text string to illustrate the widget"""
        return """
<a href="#">  <!-- with class widget_class and href the url -->
  <!-- content or url if no content given -->
</a>"""


class ImageOrTextLink(Widget):
    """A link to the page with the given ident, with four optional get fields.
       The displayed contents of the link is either an image page given by img_link
       or the text given by link_text
       If no link_ident is given, this is not an error - the img or text will simply
       be displayed in a span without a link.
       If no link or image or text is displayed, no widget will be shown
       On error replace the link by the error message"""

    # This class does not display any error messages
    display_errors = False

    arg_descriptions = {'link_ident':FieldArg("url",''),
                        'img_link':FieldArg("url",''),
                        'width':FieldArg("text", "100"),
                        'height':FieldArg("text", "100"),
                        'link_text':FieldArg("text", ""),
                        'get_field1':FieldArg("text", "", valdt=True),
                        'get_field2':FieldArg("text", "", valdt=True),
                        'get_field3':FieldArg("text", "", valdt=True),
                        'get_field4':FieldArg("text", "", valdt=True),
                        'new_window':FieldArg("boolean", False),
                        'force_ident':FieldArg("boolean", False)
                       }

    def __init__(self, name=None, brief='', **field_args):
        """
        link_ident: The target page link ident
        img_link: The ident of the image page
        width: The width of the image, ignored if text is to be displayed
        height: The height of the image, ignored if text is to be displayed
        link_text: If given, this text will be used instead of an image
        get_field1: Optional 'get' string set in the target url
        get_field2: Optional second 'get' string set in the target url
        get_field3: Optional third 'get' string set in the target url
        get_field4: Optional fourth 'get' string set in the target url
        new_window: if True, the target='_blank' attribute will be set, to open the target in a new window
        force_ident: If True then the page ident will be included, even if no get fields set
                     If False, the page ident will only be included if a get field is set
        """
        Widget.__init__(self, name=name, tag_name="a", brief=brief, **field_args)


    def _build(self, page, ident_list, environ, call_data, lang):
        "Build the link"

        if self.get_field_value("link_ident"):
            url = skiboot.get_url(self.get_field_value("link_ident"), proj_ident=page.proj_ident)
            justurl = url
            if url:
                # create a url for the href
                get_fields = {self.get_formname("get_field1"):self.get_field_value("get_field1"),
                              self.get_formname("get_field2"):self.get_field_value("get_field2"),
                              self.get_formname("get_field3"):self.get_field_value("get_field3"),
                              self.get_formname("get_field4"):self.get_field_value("get_field4")}
                url = self.make_get_url(page, url, get_fields, self.get_field_value("force_ident"))
                self.update_attribs({"href": url})
                if self.get_field_value("new_window"):
                    self.update_attribs({"target":"_blank"})
            else:
                self.tag_name="span"
        else:
            justurl = ''
            self.tag_name="span"

        if self.get_field_value("link_text"):
            self[0] = self.get_field_value("link_text")
        elif self.get_field_value("img_link"):
            imageurl = skiboot.get_url(self.get_field_value("img_link"), proj_ident=page.proj_ident)
            if imageurl:
                if self.get_field_value('width') and self.get_field_value('height'):
                    self[0] = tag.ClosedPart(tag_name="img", attribs={"src": quote(imageurl, safe='/:'),
                                                                      'width':self.get_field_value('width'),
                                                                      'height':self.get_field_value('height')})
                elif self.get_field_value('width'):
                    self[0] = tag.ClosedPart(tag_name="img", attribs={"src": quote(imageurl, safe='/:'),
                                                                      'width':self.get_field_value('width')})
                elif self.get_field_value('height'):
                    self[0] = tag.ClosedPart(tag_name="img", attribs={"src": quote(imageurl, safe='/:'),
                                                                      'height':self.get_field_value('height')})
                else:
                    self[0] = tag.ClosedPart(tag_name="img", attribs={"src": quote(imageurl, safe='/:')})
            else:
                # No image url, so show the text
                self[0] = self.get_field_value("img_link")
        elif justurl:
            # if no image ident or text, place the link page url as content, without the get fields
            self[0] = justurl
        else:
            # no text or link - nothing to show
            self[0] = ''
            self.show = False

    def __str__(self):
        """Returns a text string to illustrate the widget"""
        return """
<a href="#">  <!-- with class widget_class and href the url -->
  <!-- The link_text, if any. If no text given, then the following image -->
  <img src="#" />   <!-- with src set to url of img_ident -->
</a>"""


class CloseButton(Widget):
    """A link button that closes a given section/widget, or if javascript is disabled, calls a link"""

    # This class does not display any error messages
    display_errors = False

    arg_descriptions = {'link_ident':FieldArg("url", ''),
                        'get_field1':FieldArg("text", "", valdt=True),
                        'get_field2':FieldArg("text","", valdt=True),
                        'target_section':FieldArg("text", ""),
                        'target_widget':FieldArg("text", ""),
                       }

    def __init__(self, name=None, brief='', **field_args):
        """
        link_ident: The link to an html page taken if the client does not have javascript
        get_field1: Optional 'get' string set in the target url
        get_field2: Optional second 'get' string set in the target url
        """
        Widget.__init__(self, name=name, tag_name="a", brief=brief, **field_args)
        self.update_attribs({"role":"button"})
        self[0] = tag.HTMLSymbol("&times;")

    def _build(self, page, ident_list, environ, call_data, lang):
        "Build the link"
        if self.get_field_value("link_ident"):
            url = skiboot.get_url(self.get_field_value("link_ident"), proj_ident=page.proj_ident)
            if url:
                # create a url for the href
                get_fields = {self.get_formname("get_field1"):self.get_field_value("get_field1"),
                              self.get_formname("get_field2"):self.get_field_value("get_field2")}
                url = self.make_get_url(page, url, get_fields, True)
                self.update_attribs({"href": url})


    def _build_js(self, page, ident_list, environ, call_data, lang):
        """Sets a click event handler"""
        jscript = """  $("#{ident}").click(function (e) {{
    SKIPOLE.widgets['{ident}'].eventfunc(e);
    }});
""".format(ident = self.get_id())
        return jscript + self._make_fieldvalues('target_section', 'target_widget')


    def __str__(self):
        """Returns a text string to illustrate the widget"""
        return """
<a role="button" href="#"> <!-- With class set by widget_class, and the href link will be the url of the link_ident -->
      <!-- However if javascipt enabled the link will not be called, but the target widget will be hidden -->
      <!-- Content is the &times; symbol -->
</a>"""


class OpenButton(Widget):
    """A link button that opens a given section/widget, or if javascript is disabled, calls a link"""

    # This class does not display any error messages
    display_errors = False

    arg_descriptions = {'link_ident':FieldArg("url", ''),
                        'get_field1':FieldArg("text", "", valdt=True),
                        'get_field2':FieldArg("text","", valdt=True),
                        'target_section':FieldArg("text", ""),
                        'target_widget':FieldArg("text", ""),
                       }

    def __init__(self, name=None, brief='', **field_args):
        """
        link_ident: The link to an html page taken if the client does not have javascript
        get_field1: Optional 'get' string set in the target url
        get_field2: Optional second 'get' string set in the target url
        """
        Widget.__init__(self, name=name, tag_name="a", brief=brief, **field_args)
        self.update_attribs({"role":"button"})
        self[0] = tag.HTMLSymbol("&#9776;")

    def _build(self, page, ident_list, environ, call_data, lang):
        "Build the link"
        if self.get_field_value("link_ident"):
            url = skiboot.get_url(self.get_field_value("link_ident"), proj_ident=page.proj_ident)
            if url:
                # create a url for the href
                get_fields = {self.get_formname("get_field1"):self.get_field_value("get_field1"),
                              self.get_formname("get_field2"):self.get_field_value("get_field2")}
                url = self.make_get_url(page, url, get_fields, True)
                self.update_attribs({"href": url})


    def _build_js(self, page, ident_list, environ, call_data, lang):
        """Sets a click event handler"""
        jscript = """  $("#{ident}").click(function (e) {{
    SKIPOLE.widgets['{ident}'].eventfunc(e);
    }});
""".format(ident = self.get_id())
        return jscript + self._make_fieldvalues('target_section', 'target_widget')


    def __str__(self):
        """Returns a text string to illustrate the widget"""
        return """
<a role="button" href="#"> <!-- With class set by widget_class, and the href link will be the url of the link_ident -->
      <!-- However if javascipt enabled the link will not be called, but the target widget will be displayed -->
      <!-- Content is the &#9776; hamburger symbol -->
</a>"""


class JSONButtonLink(Widget):
    """A button link to the JSON page with the given ident, label or url.
       On error replace the button text
       by the error message, and set widget class to error_class. You will
       need to provide a css button"""

    error_location = 0

    arg_descriptions = {'json_ident':FieldArg("url", ''),
                        'link_ident':FieldArg("url", 'no_javascript'),
                        'hide':FieldArg("boolean", False, jsonset=True),
                        'button_text':FieldArg("text", "", jsonset=True),
                        'button_wait_text':FieldArg("text", "Please wait..."),
                        'get_field1':FieldArg("text", "", valdt=True, jsonset=True),
                        'get_field2':FieldArg("text","", valdt=True, jsonset=True),
                        'error_class':FieldArg("cssclass", "")
                       }

    def __init__(self, name=None, brief='', **field_args):
        """
        json_ident: The url, ident or label to link, expecting a json file to be returned
        link_ident: The link to an html page taken if the client does not have javascript
        hide: if True, and no error, button will be hidden
        button_text: The text to be placed within the link, if none given, the page url will be used
        button_wait_text: A 'please wait' message shown on the button while the call is made
        get_field1: Optional 'get' string set in the target url
        get_field2: Optional second 'get' string set in the target url
        widget_class: The class applied to the widget, should describe a button
        error_class: class which replaces widget_class on error
        """
        Widget.__init__(self, name=name, tag_name="a", brief=brief, **field_args)
        self.update_attribs({"role":"button"})
        self._jsonurl = ''
        # on error, button text is replaced by error message
        self[0] = ''


    def _build(self, page, ident_list, environ, call_data, lang):
        "Build the link"
        if self.error_status and self.get_field_value('error_class'):
            self.update_attribs({'class':self.get_field_value('error_class')})
        # Hides widget if no error and hide is True
        self.widget_hide(self.get_field_value("hide"))
        if self.get_field_value("json_ident"):
            self._jsonurl = skiboot.get_url(self.get_field_value("json_ident"), proj_ident=page.proj_ident)
        url = skiboot.get_url(self.get_field_value("link_ident"), proj_ident=page.proj_ident)
        if not url:
            if self.get_field_value('error_class'):
                self.update_attribs({'class':self.get_field_value('error_class')})
            self[0] = "Warning: broken link"
            return
        if self.get_field_value("button_text"):
            self[0] = self.get_field_value("button_text")
        else:
            self[0] = url
        # create a url for the href
        get_fields = {self.get_formname("get_field1"):self.get_field_value("get_field1"),
                      self.get_formname("get_field2"):self.get_field_value("get_field2")}
        url = self.make_get_url(page, url, get_fields, True)
        self.update_attribs({"href": url})

    def _build_js(self, page, ident_list, environ, call_data, lang):
        """Sets a click event handler"""
        jscript = """  $("#{ident}").click(function (e) {{
    SKIPOLE.widgets['{ident}'].eventfunc(e);
    }});
""".format(ident = self.get_id())
        if self._jsonurl:
            return jscript + self._make_fieldvalues('button_wait_text', 'error_class', 'widget_class', url=self._jsonurl)
        else:
            return jscript + self._make_fieldvalues('button_wait_text', 'error_class', 'widget_class')

    def __str__(self):
        """Returns a text string to illustrate the widget"""
        return """
<a role="button" href="#">
      <!-- With class set by widget_class, and the href link will be the url of the link_ident -->
      <!-- However if javascipt enabled the json_ident link will be called on button click -->
      <!-- the button will show the button_text, and button_wait_text while pressed (if the
           client browser has javascript enabled). -->
</a>"""


class ButtonLink1(Widget):
    """A button link to the page with the given ident, label or url,
       and two optional get fields.  On error replace the button text
       by the error message, and set widget class to error_class. You will
       need to provide a css button"""

    error_location = 0

    arg_descriptions = {'link_ident':FieldArg("url", ''),
                        'hide':FieldArg("boolean", False, jsonset=True),
                        'get_field1':FieldArg("text", "", valdt=True),
                        'get_field2':FieldArg("text","", valdt=True),
                        'button_text':FieldArg("text", "", jsonset=True),
                        'error_class':FieldArg("cssclass", ""),
                        'new_window':FieldArg("boolean", False),
                        'force_ident':FieldArg("boolean", False)
                       }

    def __init__(self, name=None, brief='', **field_args):
        """
        link_ident: The url, ident or label to link with
        hide: if True, and no error, button will be hidden
        get_field1: Optional 'get' string set in the target url
        get_field2: Optional second 'get' string set in the target url
        button_text: The text to be displayed within the button. If none given, the page url will be used.
        widget_class: The class applied to the widget, should describe a button
        error_class: class which replaces widget_class on error
        new_window: if True, the target='_blank' attribute will be set, to open the target in a new window
        force_ident: If True then the page ident will be included, even if no get fields set
                     If False, the page ident will only be included if a get field is set
        """
        Widget.__init__(self, name=name, tag_name="a", brief=brief, **field_args)
        self.update_attribs({"role":"button"})
        # on error, button text is replaced by error message
        self[0] = ''

    def _build(self, page, ident_list, environ, call_data, lang):
        "Build the link"
        if self.error_status and self.get_field_value('error_class'):
            self.update_attribs({'class':self.get_field_value('error_class')})
        # Hides widget if no error and hide is True
        self.widget_hide(self.get_field_value("hide"))
        if not self.get_field_value("link_ident"):
            if self.get_field_value('error_class'):
                self.update_attribs({'class':self.get_field_value('error_class')})
            self[0] = "Warning: broken link"
            return
        url = skiboot.get_url(self.get_field_value("link_ident"), proj_ident=page.proj_ident)
        if not url:
            if self.get_field_value('error_class'):
                self.update_attribs({'class':self.get_field_value('error_class')})
            self[0] = "Warning: broken link"
            return
        if self.get_field_value("button_text"):
            self[0] = self.get_field_value("button_text")
        else:
            self[0] = url
        # create a url for the href
        get_fields = {self.get_formname("get_field1"):self.get_field_value("get_field1"),
                      self.get_formname("get_field2"):self.get_field_value("get_field2")}
        url = self.make_get_url(page, url, get_fields, self.get_field_value("force_ident"))
        self.update_attribs({"href": url})
        if self.get_field_value("new_window"):
            self.update_attribs({"target":"_blank"})

    def _build_js(self, page, ident_list, environ, call_data, lang):
        """Sets field values"""
        return self._make_fieldvalues('error_class', 'widget_class')

    def __str__(self):
        """Returns a text string to illustrate the widget"""
        return """
<a role="button" href="#">
 <!-- With class set by widget_class, and the href link will be the url of the link_ident with the two get_fields -->
 <!-- the button will show the button_text, on error this will be replaced by the error message -->
</a>"""


class ButtonLink2(Widget):
    """A div holding a button link to the page with the given ident, label or url,
       and two optional get fields."""

    error_location = (0,0,0)

    arg_descriptions = {'json_ident':FieldArg("url", ''),
                        'link_ident':FieldArg("url", 'no_javascript'),
                        'hide':FieldArg("boolean", False, jsonset=True),
                        'button_text':FieldArg("text", "", jsonset=True),
                        'button_wait_text':FieldArg("text", "Please wait..."),
                        'button_class':FieldArg("cssclass", ""),
                        'get_field1':FieldArg("text", "", valdt=True),
                        'get_field2':FieldArg("text","", valdt=True),
                        'error_class':FieldArg("cssclass", ""),
                        'buttondiv_class':FieldArg("cssclass", ""),
                        'buttondiv_style':FieldArg("cssstyle", "")
                       }

    def __init__(self, name=None, brief='', **field_args):
        """
        json_ident: The url, ident or label to link, expecting a json file to be returned
        link_ident: The link to an html page taken if the client does not have javascript
        hide: if True, and no error, button will be hidden
        button_text: The text to be placed within the link, if none given, the page url will be used
        button_wait_text: A 'please wait' message shown on the button if a JSON call is made
        button_class: A CSS class applied to the button
        buttondiv_class: A CSS class applied to the div containing the button
        buttondiv_style: A CSS style applied to the div containing the button
        get_field1: Optional 'get' string set in the target url
        get_field2: Optional second 'get' string set in the target url
        widget_class: The class applied to the widget
        error_class: class given to normally hidden error div
        """

        Widget.__init__(self, name=name, tag_name="div", brief=brief, **field_args)
        # error div at 0
        self[0] = tag.Part(tag_name="div", attribs={"style":"display:none;"})
        self[0][0] = tag.Part(tag_name="p")
        self[0][0][0] = ''
        # buttondiv
        self[1] = tag.Part(tag_name="div")
        self[1][0] = tag.Part(tag_name="a", attribs={"role":"button"})
        self._jsonurl = ''


    def _build(self, page, ident_list, environ, call_data, lang):
        "Build the link"
        # Hides widget if no error and hide is True
        self.widget_hide(self.get_field_value("hide"))
        if self.get_field_value('error_class'):
            self[0].update_attribs({"class":self.get_field_value('error_class')})
        if self.error_status:
            self[0].del_one_attrib("style")
        if self.get_field_value("json_ident"):
            self._jsonurl = skiboot.get_url(self.get_field_value("json_ident"), proj_ident=page.proj_ident)
        if not self.get_field_value("link_ident"):
            # setting self._error replaces the entire tag
            self._error = "Warning: No link ident"
            return
        # set buttondiv
        if self.get_field_value('buttondiv_class'):
            self[1].attribs = {"class":self.get_field_value('buttondiv_class')}
        if self.get_field_value('buttondiv_style'):
            self[1].update_attribs({"style":self.get_field_value('buttondiv_style')})
        # set button class
        if self.get_field_value('button_class'):
            self[1][0].update_attribs({"class":self.get_field_value('button_class')})
        # get url and button text
        url = skiboot.get_url(self.get_field_value("link_ident"), proj_ident=page.proj_ident)
        if self.get_field_value("button_text"):
            self[1][0][0] = self.get_field_value("button_text")
        else:
            self[1][0][0] = url
        # create a url for the href
        get_fields = {self.get_formname("get_field1"):self.get_field_value("get_field1"),
                      self.get_formname("get_field2"):self.get_field_value("get_field2")}
        url = self.make_get_url(page, url, get_fields, True)
        self[1][0].update_attribs({"href": url})


    def _build_js(self, page, ident_list, environ, call_data, lang):
        """Sets a click event handler"""
        jscript = """  $("#{ident}").click(function (e) {{
    SKIPOLE.widgets['{ident}'].eventfunc(e);
    }});
""".format(ident = self.get_id())
        if self._jsonurl:
            return jscript + self._make_fieldvalues('button_wait_text', url=self._jsonurl)
        else:
            return jscript + self._make_fieldvalues('button_wait_text')


    def __str__(self):
        """Returns a text string to illustrate the widget"""
        return """
<div> <!-- with class attribute set to widget_class if a class is set -->
  <div> <!-- normally hidden div, with class error_class -->
    <p> <!-- Any error text appears here --> </p>
  </div>
  <div> <!-- class attribute set to buttondiv_class, style to buttondiv_style -->
    <a role="button" href="#">
      <!-- With class set by button_class, and the href link will be the url of the link_ident -->
      <!-- However if javascipt enabled the json_ident link will be called on button click -->
      <!-- the button will show the button_text. -->
    </a>
  </div>
</div>"""




class ImageLink1(Widget):
    """A link to the page with the given ident, with three optional get fields.
       The displayed contents of the link is an image page given by img_ident"""

    # This class does not display any error messages
    display_errors = False

    arg_descriptions = {'link_ident':FieldArg("url", ''),
                        'img_ident':FieldArg("url", ''),
                        'width':FieldArg("text","100"),
                        'height':FieldArg("text","100"),
                        'align':FieldArg("text",""),
                        'get_field1':FieldArg("text","", valdt=True),
                        'get_field2':FieldArg("text","", valdt=True),
                        'get_field3':FieldArg("text","", valdt=True),
                        'force_ident':FieldArg("boolean",False)
                       }

    def __init__(self, name=None, brief='', **field_args):
        """
        link_ident: The target page link ident, label or url
        img_ident: The ident of the image page
        width: The width of the image
        height: The height of the image
        get_field1: Optional 'get' string set in the target url
        get_field2: Optional second 'get' string set in the target url
        get_field3: Optional third 'get' string set in the target url
        force_ident: If True then the page ident will be included, even if no get fields set
                     If False, the page ident will only be included if a get field is set
        """
        Widget.__init__(self, name=name, tag_name="a", brief=brief, **field_args)
        self[0] = tag.ClosedPart(tag_name="img")

    def _build(self, page, ident_list, environ, call_data, lang):
        "Build the link"
        if self.get_field_value('width') and self.get_field_value('height'):
            self[0].set_attribs({'width':self.get_field_value('width'), 'height':self.get_field_value('height')})
        elif self.get_field_value('width'):
            self[0].set_attribs({'width':self.get_field_value('width')})
        elif self.get_field_value('height'):
            self[0].set_attribs({'height':self.get_field_value('height')})
        if self.get_field_value('align'):
            self[0].update_attribs({'align':self.get_field_value('align')})
        if not self.get_field_value("link_ident"):
            self._error = "Warning: broken link"
            return
        url = skiboot.get_url(self.get_field_value("link_ident"), proj_ident=page.proj_ident)
        if not url:
            self._error = "Warning: broken link"
            return
        justurl = url
        # create a url for the href
        get_fields = {self.get_formname("get_field1"):self.get_field_value("get_field1"),
                      self.get_formname("get_field2"):self.get_field_value("get_field2"),
                      self.get_formname("get_field3"):self.get_field_value("get_field3")}
        url = self.make_get_url(page, url, get_fields, self.get_field_value("force_ident"))
        self.update_attribs({"href": url})
        if not self.get_field_value("img_ident"):
            # if no image ident, place the link page url as content, without the get fields
            self[0] = justurl
            return
        imageurl = skiboot.get_url(self.get_field_value("img_ident"), proj_ident=page.proj_ident)
        if not imageurl:
            self[0] = justurl
        else:
            self[0].update_attribs({"src": quote(imageurl, safe='/:')})

    def __str__(self):
        """Returns a text string to illustrate the widget"""
        return """
<a href="#">  <!-- with class widget_class and href the url -->
  <img src="#" />   <!-- with src set to url of img_ident -->
</a>"""


class CSSLink(ClosedWidget):
    "Defines a link to a stylesheet"

    # This class does not display any error messages
    display_errors = False

    arg_descriptions = {'css_ident':FieldArg("url", ''),
                        'media':FieldArg("text", '')}

    def __init__(self, name=None, brief='', **field_args):
        """
        css_ident: A CSS url, label or page ident
        media: a media string
        """
        ClosedWidget.__init__(self, name=name, tag_name="link", brief=brief, **field_args)
        self.update_attribs({"rel":"stylesheet", "type":"text/css"})

    def _build(self, page, ident_list, environ, call_data, lang):
        "Build the link url"
        if not self.get_field_value("css_ident"):
            self._error = "Warning: broken link"
            return
        url = skiboot.get_url(self.get_field_value("css_ident"), proj_ident=page.proj_ident)
        if not url:
            self._error = "Warning: broken link"
            return
        self.update_attribs({"href": quote(url, safe='/:')})
        if self.get_field_value("media"):
            self.update_attribs({"media": self.get_field_value("media")})

    def __str__(self):
        """Returns a text string to illustrate the widget"""
        return """
<link rel="stylesheet" type="text/css" />  <!-- with href and media set as per fields -->"""


class FaviconLink(ClosedWidget):
    "Defines a link to a png favicon"

    # This class does not display any error messages
    display_errors = False

    arg_descriptions = {'favicon_ident':FieldArg("url", '')}

    def __init__(self, name=None, brief='', **field_args):
        """
        favicon_ident: A favicon url, label or page ident
        """
        ClosedWidget.__init__(self, name=name, tag_name="link", brief=brief, **field_args)
        self.update_attribs({"rel":"icon", "type":"image/png"})

    def _build(self, page, ident_list, environ, call_data, lang):
        "Build the link url"
        if not self.get_field_value("favicon_ident"):
            self._error = "Warning: broken link"
            return
        url = skiboot.get_url(self.get_field_value("favicon_ident"), proj_ident=page.proj_ident)
        if not url:
            self._error = "Warning: broken link"
            return    
        self.update_attribs({"href": quote(url, safe='/:')})

    def __str__(self):
        """Returns a text string to illustrate the widget"""
        return """
<link rel="icon" type="image/png" />  <!-- with href given by favicon_ident -->"""


class ScriptLink(Widget):
    "Defines a link to a js filepage given by a page ident"

    # This class does not display any error messages
    display_errors = False

    arg_descriptions = {'script_ident':FieldArg("url", "")}

    def __init__(self, name=None, brief='', **field_args):
        """
        script_ident: A filepage ident
        """
        Widget.__init__(self, name=name, tag_name="script", brief=brief, **field_args)

    def _build(self, page, ident_list, environ, call_data, lang):
        "Build the link url"
        if not self.get_field_value("script_ident"):
            self._error = "Warning: broken link"
            return
        url = skiboot.get_url(self.get_field_value("script_ident"), proj_ident=page.proj_ident)
        if not url:
            self._error = "Warning: broken link"
            return
        self.update_attribs({"src": quote(url, safe='/:')})

    def __str__(self):
        """Returns a text string to illustrate the widget"""
        return """
<script>  <!-- with src given by script_ident -->
</script>"""


class LinkTextBlockTable1(Widget):
    "A table of links to a page, with link text, two get fields and a TextBlock"

    # This class does not display any error messages
    display_errors = False

    arg_descriptions = {'link_ident':FieldArg("url", ""),
                        'header_class':FieldArg("cssclass",""),
                        'even_class':FieldArg("cssclass", ""),
                        'odd_class':FieldArg("cssclass", ""),
                        'col1_link_title':FieldArg('text', ''),
                        'col2_text_title':FieldArg('text', ''),
                        'show_get_field1':FieldArg("boolean", True, valdt=True),
                        'show_get_field2':FieldArg("boolean", True, valdt=True),
                        'link_table':FieldArgTable(['text', 'text', 'text', 'textblock_ref', 'text', 'text']),               # coltypes
                        'force_ident':FieldArg("boolean", False)
                        }

    def __init__(self, name=None, brief='', **field_args):
        """
        link_ident: The target page link ident, url or label
        header_class: class of the header row, if empty string, then no class will be applied
        even_class: class of even rows, if empty string, then no class will be applied
        odd_class: class of odd rows, if empty string, then no class will be applied
        col1_link_title: The title of the first column, above the links
        col2_text_title: The title of the second colum, above the textblock
        show_get_field1: If True, enables the get field, the name of this variable is used as the field name
        show_get_field2: If True, enables the second get field, the name of this variable is used as the field name
        link_table: col 0 is the visible text to place in the link,
                    col 1 is the get field of the link
                    col 2 is the get field of the link
                    col 3 is the reference string of a textblock to appear in the column adjacent to the link
                    col 4 is text to appear if the reference cannot be found in the database
                    col 5 normally empty string, if set to text it will replace the textblock
        force_ident: If True then the page ident will be included, even if no get fields set
                     If False, the page ident will only be included if a get field is set
        """
        Widget.__init__(self, name=name, tag_name="table", brief=brief, **field_args)


    def _build(self, page, ident_list, environ, call_data, lang):
        "Build the table"
        table = self.get_field_value("link_table")
        title1 = self.get_field_value("col1_link_title")
        title2 = self.get_field_value("col2_text_title")

        # set even row colour
        if self.get_field_value('even_class'):
            evenclass = self.get_field_value('even_class')
        else:
            evenclass = ''
        # set odd row colour
        if self.get_field_value('odd_class'):
            oddclass = self.get_field_value('odd_class')
        else:
            oddclass = ''
        # set header row colour
        if self.get_field_value('header_class'):
            headerclass = self.get_field_value('header_class')
        else:
            headerclass = ''

        for num, row in enumerate(table):
            if title1 or title2:
                rownumber = num+1
            else:
                rownumber = num
            if (not num) and (title1 or title2):
                if headerclass:
                    self[0]  = tag.Part(tag_name="tr", attribs={"class":headerclass})
                else:
                    self[0]  = tag.Part(tag_name="tr")
                if title1:
                    self[0][0] = tag.Part(tag_name="th", text=title1)
                else:
                    self[0][0] = tag.Part(tag_name="th")
                if title2:
                    self[0][1] = tag.Part(tag_name="th", text=title2)
                else:
                    self[0][1] = tag.Part(tag_name="th")
            if evenclass and (rownumber % 2):
                self[rownumber]  = tag.Part(tag_name="tr", attribs={"class":evenclass})
            elif oddclass and not (rownumber % 2):
                self[rownumber]  = tag.Part(tag_name="tr", attribs={"class":oddclass})
            else:
                self[rownumber]  = tag.Part(tag_name="tr")
            # each row has parameters 0 to 5
            self[rownumber][0] = tag.Part(tag_name="td")
            if row[0]:
                content = row[0]
            else:
                content = "?"
            self[rownumber][0][0]= Link(link_ident=self.get_field_value("link_ident"),
                                        get_field1=row[1],
                                        get_field2=row[2],
                                        content=content,
                                        force_ident=self.get_field_value("force_ident"))
            self[rownumber][0][0].set_name('get_field1', self.get_name("show_get_field1"))
            self[rownumber][0][0].set_name('get_field2', self.get_name("show_get_field2"))
            if not self.get_field_value("show_get_field1"):
                self[rownumber][0][0].set_field_value('get_field1','')
            if not self.get_field_value("show_get_field2"):
                self[rownumber][0][0].set_field_value('get_field2','')
            # second column
            self[rownumber][1] = tag.Part(tag_name="td")
            # Set the text column, row[3] is a textblock
            if row[5]:
                # override the textblock
                self[rownumber][1][0] = row[5]
                continue
            if (not row[3]) and row[4]:
                self[rownumber][1][0] = row[4]
                continue
            if row[3]:
                if row[4]:
                    row[3].failmessage = row[4]
                self[rownumber][1][0] = row[3]
            else: 
                self[rownumber][1][0] = ''

    def __str__(self):
        """Returns a text string to illustrate the widget"""
        return """
<table>  <!-- with CSS class given by widget_class -->
  <tr> <!-- with class header_class -->
    <th> <!-- col1_link_title --> </th>   <th> <!-- col2_text_title --> </th>
  </tr>
  <tr> <!-- with class  odd_class -->
    <td> <!-- link and link text--> </td>   <td> <!-- textblock --> </td>
  </tr>
  <!-- rows repeated for each link, with odd and even row classes -->
</table>"""



class LinkTextBlockTable2(Widget):
    "A 3 column table of links to a page, with link text, two get fields, a text string and a TextBlock"

    # This class does not display any error messages
    display_errors = False

    arg_descriptions = {'link_ident':FieldArg("url", ""),
                        'header_class':FieldArg("cssclass",""),
                        'even_class':FieldArg("cssclass", ""),
                        'odd_class':FieldArg("cssclass", ""),
                        'col_link_title':FieldArg('text', ''),
                        'col_text_title':FieldArg('text', ''),
                        'col_textblock_title':FieldArg('text', ''),
                        'show_get_field1':FieldArg("boolean", True, valdt=True),
                        'show_get_field2':FieldArg("boolean", True, valdt=True),
                        'link_table':FieldArgTable(['text', 'text', 'text', 'text', 'textblock_ref', 'text', 'text']),
                        'force_ident':FieldArg("boolean", False)
                        }


    def __init__(self, name=None, brief='', **field_args):
        """
        link_ident: The target page link ident, url or label
        header_class: class of the header row, if empty string, then no class will be applied
        even_class: class of even rows, if empty string, then no class will be applied
        odd_class: class of odd rows, if empty string, then no class will be applied
        col_link_title: The title of the first column, above the links
        col_text_title: The title of the second colum, above the text
        col_textblock_title: The title of the second colum, above the textblock
        show_get_field1: If True, enables the get field, the name of this variable is used as the field name
        show_get_field2: If True, enables the second get field, the name of this variable is used as the field name
        link_table: col 0 is the visible text to place in the link,
                    col 1 is the get field of the link
                    col 2 is the get field of the link
                    col 3 is the text to appear in the second table column
                    col 4 is the reference string of a textblock to appear in the third table column
                    col 5 is text to appear if the reference cannot be found in the database
                    col 6 normally empty string, if set to text it will replace the textblock
        force_ident: If True then the page ident will be included, even if no get fields set
                     If False, the page ident will only be included if a get field is set
        """
        Widget.__init__(self, name=name, tag_name="table", brief=brief, **field_args)
        self.update_attribs({"style":"border-spacing:0;border-collapse:collapse;"})


    def _build(self, page, ident_list, environ, call_data, lang):
        "Build the table"
        table = self.get_field_value("link_table")
        title1 = self.get_field_value("col_link_title")
        title2 = self.get_field_value("col_text_title")
        title3 = self.get_field_value("col_textblock_title")

        # set even row colour
        if self.get_field_value('even_class'):
            evenclass = self.get_field_value('even_class')
        else:
            evenclass = ''
        # set odd row colour
        if self.get_field_value('odd_class'):
            oddclass = self.get_field_value('odd_class')
        else:
            oddclass = ''
        # set header row colour
        if self.get_field_value('header_class'):
            headerclass = self.get_field_value('header_class')
        else:
            headerclass = ''

        for num, row in enumerate(table):
            if title1 or title2 or title3:
                rownumber = num+1
            else:
                rownumber = num
            if (not num) and (title1 or title2):
                if headerclass:
                    self[0]  = tag.Part(tag_name="tr", attribs={"class":headerclass})
                else:
                    self[0]  = tag.Part(tag_name="tr")
                if title1:
                    self[0][0] = tag.Part(tag_name="th", text=title1)
                else:
                    self[0][0] = tag.Part(tag_name="th")
                if title2:
                    self[0][1] = tag.Part(tag_name="th", text=title2)
                else:
                    self[0][1] = tag.Part(tag_name="th")
                if title3:
                    self[0][2] = tag.Part(tag_name="th", text=title3)
                else:
                    self[0][2] = tag.Part(tag_name="th")
            if evenclass and (rownumber % 2):
                self[rownumber]  = tag.Part(tag_name="tr", attribs={"class":evenclass})
            elif oddclass and not (rownumber % 2):
                self[rownumber]  = tag.Part(tag_name="tr", attribs={"class":oddclass})
            else:
                self[rownumber]  = tag.Part(tag_name="tr")
            # each row has parameters 0 to 6

            # first column, the link column
            self[rownumber][0] = tag.Part(tag_name="td")
            if row[0]:
                content = row[0]
            else:
                content = "?"
            self[rownumber][0][0]= Link(link_ident=self.get_field_value("link_ident"),
                                        get_field1=row[1],
                                        get_field2=row[2],
                                        content=content,
                                        force_ident=self.get_field_value("force_ident"))
            self[rownumber][0][0].set_name('get_field1', self.get_name("show_get_field1"))
            self[rownumber][0][0].set_name('get_field2', self.get_name("show_get_field2"))
            if not self.get_field_value("show_get_field1"):
                self[rownumber][0][0].set_field_value('get_field1','')
            if not self.get_field_value("show_get_field2"):
                self[rownumber][0][0].set_field_value('get_field2','')

            # second column, the text string column
            self[rownumber][1] = tag.Part(tag_name="td")
            self[rownumber][1][0] = row[3]

            # third column, the TextBlock column
            self[rownumber][2] = tag.Part(tag_name="td")
            # Set the text column, row[4] is a textblock
            if row[6]:
                # override the textblock
                self[rownumber][2][0] = row[6]
                continue
            if (not row[4]) and row[5]:
                self[rownumber][2][0] = row[5]
                continue
            if row[4]:
                if row[5]:
                    row[4].failmessage = row[5]
                self[rownumber][2][0] = row[4]
            else: 
                self[rownumber][2][0] = ''

    def __str__(self):
        """Returns a text string to illustrate the widget"""
        return """
<table>  <!-- with CSS class given by widget_class -->
  <tr> <!-- with class header_class -->
    <th> <!-- col_link_title --> </th>   <th> <!-- col_text_title --> </th>   <th> <!-- col_textblock_title --> </th>
  </tr>
  <tr> <!-- with class  odd_class -->
    <td> <!-- link and link text--> </td>   <td> <!-- text string --> </td>  <td> <!-- textblock --> </td>
  </tr>
  <!-- rows repeated for each link, with odd and even row classes -->
</table>"""


class ListLinks(Widget):
    """A list of links, each with one get field"""

    # This class does not display any error messages
    display_errors = False

    arg_descriptions = {
                        'li_class':FieldArg("cssclass", ""),
                        'link_class':FieldArg("cssclass", ""),
                        'new_window':FieldArg("boolean", False),
                        'force_ident':FieldArg("boolean", False),
                        'links':FieldArgTable(['text', 'url', 'text'], valdt=True)
                        }

    def __init__(self, name=None, brief='', **field_args):
        """
        li_class: class to set in each li element
        link_class: class to set in each a element
        new_window: if True, the target='_blank' attribute will be set on each link, to open the target in a new window
        force_ident: If True then the page ident will be included, even if no get field set
                     If False, the page ident will only be included if a get field is set
        links: col 0 is the text to place in link,
                     col 1 is the link ident, label or url
                     col 2 is the get field contents of the link, empty if not used
                     the name of this field is used as the widgfield of the get data returned
        """
        Widget.__init__(self, name=name, tag_name="ul", brief=brief, **field_args)


    def _build(self, page, ident_list, environ, call_data, lang):
        "Build the list"
        fieldlist = self.get_field_value('links')
        li_class = self.get_field_value('li_class')
        link_class = self.get_field_value('link_class')
        new_window = self.get_field_value('new_window')
        force_ident = self.get_field_value('force_ident')
        # create rows
        for rownumber, row in enumerate(fieldlist):
            if li_class:
                self[rownumber] = tag.Part(tag_name="l")
            else:
                self[rownumber] = tag.Part(tag_name="li")
            self[rownumber][0] = Link(widget_class = link_class,
                                       link_ident = row[1],
                                       get_field1 = row[2],
                                       content = row[0],
                                       new_window = new_window,
                                       force_ident = force_ident   )
            self[rownumber][0].set_name('get_field1',  self.get_name('links'))


    def __str__(self):
        """Returns a text string to illustrate the widget"""
        return """
<ul>  <!-- with CSS class given by widget_class -->
  <li> <!-- with class  given by li_class -->
    <a href="#">  <!-- with class link_class and href the url -->
    <!-- content or url if no content given -->
    </a>
  <li>
  <!-- rows repeated -->
</ul>"""


class Table1_Button(Widget):
    """A table of a single text column, followed by a button link column
       There is a header and title over the text column,
       the button link can have one get field"""

    # This class does not display any error messages
    display_errors = False

    arg_descriptions = {
                        'header_class':FieldArg("cssclass",""),
                        'even_class':FieldArg("cssclass", ""),
                        'odd_class':FieldArg("cssclass", ""),
                        'maximize_text_col':FieldArg('boolean',True),
                        'hide':FieldArg("boolean", False, jsonset=True),
                        'title1':FieldArg('text', ''),
                        'button_class':FieldArg("cssclass", ""),
                        'button_text':FieldArg('text', ''),
                        'link_ident':FieldArg("url", 'no_javascript'),
                        'json_ident':FieldArg("url", ''),
                        'contents':FieldArgTable(['text', 'text'], valdt=True)
                        }

    def __init__(self, name=None, brief='', **field_args):
        """
        header_class: class of the header row
        even_class: class of even rows, if empty string, then no class will be applied
        odd_class: class of odd rows, if empty string, then no class will be applied
        maximize_text_col: If True the text column is made large, with the button columns reduced to the size of the buttons
        hide: if True, table will be hidden
        title1: The header title over the text column
        button_class: The CSS class to apply to the buttons
        button_text: Text on the link button
        link_ident: The target page link ident, label or url, if javascript not available
        json_ident: The url, ident or label to link, expecting a json file to be returned
        contents: col 0 is the text string to place in the first column,
                  col 1 is the get field contents of the button link
                  This fieldname used as the widgfield
        """
        Widget.__init__(self, name=name, tag_name="table", brief=brief, **field_args)
        self._jsonurl =''

    def _build(self, page, ident_list, environ, call_data, lang):
        "Build the table"
        # Hides widget if no error and hide is True
        self.widget_hide(self.get_field_value("hide"))
        fieldtable = self.get_field_value("contents")
        header = 0
        if self.get_field_value('title1'):
            header = 1
            if self.get_field_value('header_class'):
                self[0] = tag.Part(tag_name='tr', attribs={"class":self.get_field_value('header_class')})
            else:
                self[0] = tag.Part(tag_name='tr')
            if self.get_field_value('maximize_text_col'):
                self[0][0] = tag.Part(tag_name='th', text = self.get_field_value('title1'), attribs={"style":"width : 100%;"})
            else:
                self[0][0] = tag.Part(tag_name='th', text = self.get_field_value('title1'))
            self[0][1] = tag.Part(tag_name='th')
        # set even row colour
        if self.get_field_value('even_class'):
            even = self.get_field_value('even_class')
        else:
            even = ''
        # set odd row colour
        if self.get_field_value('odd_class'):
            odd = self.get_field_value('odd_class')
        else:
            odd = ''
        if self.get_field_value("json_ident"):
            self._jsonurl = skiboot.get_url(self.get_field_value("json_ident"), proj_ident=page.proj_ident)
        # create rows
        for index, row in enumerate(fieldtable):
            rownumber = index+header
            if even and (rownumber % 2) :
                self[rownumber] = tag.Part(tag_name="tr", attribs={"class":even})
            elif odd and not (rownumber % 2):
                self[rownumber] = tag.Part(tag_name='tr', attribs={"class":odd})
            else:
                self[rownumber] = tag.Part(tag_name='tr')
            # first column is text
            if self.get_field_value('maximize_text_col'):
                self[rownumber][0] = tag.Part(tag_name='td', text = row[0], attribs={"style":"width : 100%;"})
            else:
                self[rownumber][0] = tag.Part(tag_name='td', text = row[0])
            # Next column is a button link
            self[rownumber][1] = tag.Part(tag_name='td')
            if self.get_field_value('button_class'):
                self[rownumber][1][0] = tag.Part(tag_name='a', attribs = {"role":"button", "class":self.get_field_value('button_class')})
            else:
                self[rownumber][1][0] = tag.Part(tag_name='a', attribs = {"role":"button"})
            self[rownumber][1][0].htmlescaped=False
            if self.get_field_value("link_ident"):
                url = skiboot.get_url(self.get_field_value("link_ident"), proj_ident=page.proj_ident)
                if url:
                    if self.get_field_value("button_text"):
                        self[rownumber][1][0][0] = self.get_field_value("button_text")
                    else:
                        self[rownumber][1][0][0] = url
                    # create a url for the href
                    get_fields = {self.get_formname("contents"):row[1]}
                    url = self.make_get_url(page, url, get_fields, True)
                    self[rownumber][1][0].update_attribs({"href": url})
                else:
                   self[rownumber][1][0] = "Warning: broken link"
            else:
                self[rownumber][1][0] = "Warning: broken link"


    def _build_js(self, page, ident_list, environ, call_data, lang):
        """Sets a click event handler"""
        if not self._jsonurl:
            return
        jscript = """  $("#{ident} a").click(function (e) {{
    SKIPOLE.widgets['{ident}'].eventfunc(e);
    }});
""".format(ident = self.get_id())
        return jscript + self._make_fieldvalues( url=self._jsonurl)

    def __str__(self):
        """Returns a text string to illustrate the widget"""
        return """
<table>  <!-- with CSS class given by widget_class -->
                   <!-- and attribute style=display:none if hide is True -->
  <tr> <!-- with header class -->
    <th> <!-- title1 --> </th>
    <th></th>
  </tr>
  <tr> <!-- with class from even or odd classes -->
    <td> <!-- text string --> </td>
    <td>
      <a role="button" href="#">
      <!-- With class set by button_class, and the href link will be the url of the link_ident with get field -->
      <!-- the button will show the button_text  (not html escaped) -->
      </a>
    </td>
  </tr>
  <!-- rows repeated -->
</table>"""


class Table2_Button(Widget):
    """A table of a two text columns, followed by a button link
       There is a header and titles over the two text columns,
       the button link can have one get field"""

    # This class does not display any error messages
    display_errors = False

    arg_descriptions = {
                        'header_class':FieldArg("cssclass",""),
                        'even_class':FieldArg("cssclass", ""),
                        'odd_class':FieldArg("cssclass", ""),
                        'hide':FieldArg("boolean", False, jsonset=True),
                        'title1':FieldArg('text', ''),
                        'title2':FieldArg('text', ''),
                        'button_class':FieldArg("cssclass", ""),
                        'button_text':FieldArg('text', ''),
                        'link_ident':FieldArg("url", 'no_javascript'),
                        'json_ident':FieldArg("url", ''),
                        'contents':FieldArgTable(['text', 'text', 'text'], valdt=True)
                        }

    def __init__(self, name=None, brief='', **field_args):
        """
        header_class: class of the header row
        even_class: class of even rows, if empty string, then no class will be applied
        odd_class: class of odd rows, if empty string, then no class will be applied
        hide: if True, table will be hidden
        title1: The header title over the first text column
        title2: The header title over the second text column
        button_class: The CSS class to apply to the buttons
        button_text: Text on the link button
        link_ident: The target page link ident, label or url, if javascript not available
        json_ident: The url, ident or label to link, expecting a json file to be returned
        contents: col 0 and 1 are the text strings to place in the first two columns,
                  col 2 is the get field contents of the button link
                  This fieldname used as the widgfield
        """
        Widget.__init__(self, name=name, tag_name="table", brief=brief, **field_args)
        self._jsonurl =''


    def _build(self, page, ident_list, environ, call_data, lang):
        "Build the table"
        # Hides widget if no error and hide is True
        self.widget_hide(self.get_field_value("hide"))
        fieldtable = self.get_field_value("contents")
        header = 0
        if self.get_field_value('title1') or self.get_field_value('title2'):
            header = 1
            if self.get_field_value('header_class'):
                self[0] = tag.Part(tag_name='tr', attribs={"class":self.get_field_value('header_class')})
            else:
                self[0] = tag.Part(tag_name='tr')
            self[0][0] = tag.Part(tag_name='th', text = self.get_field_value('title1'))
            self[0][1] = tag.Part(tag_name='th', text = self.get_field_value('title2'))
            self[0][2] = tag.Part(tag_name='th')
        # set even row colour
        if self.get_field_value('even_class'):
            even = self.get_field_value('even_class')
        else:
            even = ''
        # set odd row colour
        if self.get_field_value('odd_class'):
            odd = self.get_field_value('odd_class')
        else:
            odd = ''
        if self.get_field_value("json_ident"):
            self._jsonurl = skiboot.get_url(self.get_field_value("json_ident"), proj_ident=page.proj_ident)
        # create rows
        for index, row in enumerate(fieldtable):
            rownumber = index+header
            if even and (rownumber % 2) :
                self[rownumber] = tag.Part(tag_name="tr", attribs={"class":even})
            elif odd and not (rownumber % 2):
                self[rownumber] = tag.Part(tag_name='tr', attribs={"class":odd})
            else:
                self[rownumber] = tag.Part(tag_name='tr')
            # first two columns are text
            self[rownumber][0] = tag.Part(tag_name='td', text = row[0])
            self[rownumber][1] = tag.Part(tag_name='td', text = row[1])
            # Next column is a button link
            self[rownumber][2] = tag.Part(tag_name='td', attribs={"style":"width : 1%;"})
            if self.get_field_value('button_class'):
                self[rownumber][2][0] = tag.Part(tag_name='a', attribs = {"role":"button", "class":self.get_field_value('button_class')})
            else:
                self[rownumber][2][0] = tag.Part(tag_name='a', attribs = {"role":"button"})
            self[rownumber][2][0].htmlescaped=False
            if self.get_field_value("link_ident"):
                url = skiboot.get_url(self.get_field_value("link_ident"), proj_ident=page.proj_ident)
                if url:
                    if self.get_field_value("button_text"):
                        self[rownumber][2][0][0] = self.get_field_value("button_text")
                    else:
                        self[rownumber][2][0][0] = url
                    # create a url for the href
                    get_fields = {self.get_formname("contents"):row[2]}
                    url = self.make_get_url(page, url, get_fields, True)
                    self[rownumber][2][0].update_attribs({"href": url})
                else:
                   self[rownumber][2][0] = "Warning: broken link"
            else:
                self[rownumber][2][0] = "Warning: broken link"

    def _build_js(self, page, ident_list, environ, call_data, lang):
        """Sets a click event handler"""
        if not self._jsonurl:
            return
        jscript = """  $("#{ident} a").click(function (e) {{
    SKIPOLE.widgets['{ident}'].eventfunc(e);
    }});
""".format(ident = self.get_id())
        return jscript + self._make_fieldvalues( url=self._jsonurl)


    def __str__(self):
        """Returns a text string to illustrate the widget"""
        return """
<table>  <!-- with CSS class given by widget_class -->
                   <!-- and attribute style=display:none if hide is True -->
  <tr> <!-- with header class -->
    <th> <!-- title 1 --> </th>
    <th> <!-- title 2 --> </th>
    <th></th>
  </tr>
  <tr> <!-- with class  from even or odd classes -->
    <td> <!-- text string --> </td>
    <td> <!-- text string --> </td>
    <td>
      <a role="button" href="#">
      <!-- With class set by button_class, and the href link will be the url of the link_ident with get field -->
      <!-- the button will show the button_text  (not html escaped) -->
      </a>
    </td>
  </tr>
  <!-- rows repeated -->
</table>"""



class Table3_Buttons2(Widget):
    """A table of three text columns, followed by two button link columns
       The first row is three headers - over the three text columns"""

    # This class does not display any error messages
    display_errors = False

    arg_descriptions = {'header_class':FieldArg("cssclass",""),
                        'even_class':FieldArg("cssclass", ""),
                        'odd_class':FieldArg("cssclass", ""),
                        'title1':FieldArg('text', ''),
                        'title2':FieldArg('text', ''),
                        'title3':FieldArg('text', ''),
                        'button_class':FieldArg("cssclass", ""),
                        'link_ident1':FieldArg("url",''),
                        'json_ident1':FieldArg("url", ''),
                        'button_text1':FieldArg('text', ''),
                        'get_field1_1':FieldArg('boolean',True, valdt=True),
                        'get_field1_2':FieldArg('boolean',True, valdt=True),
                        'link_ident2':FieldArg("url",''),
                        'json_ident2':FieldArg("url", ''),
                        'button_text2':FieldArg('text', ''),
                        'get_field2_1':FieldArg("boolean", True, valdt=True),
                        'get_field2_2':FieldArg("boolean",True, valdt=True),
                        'contents':FieldArgTable(['text', 'text', 'text', 'text', 'text', 'text', 'text', "boolean", "boolean"])
                        }

    def __init__(self, name=None, brief='', **field_args):
        """
        header_class: class of the header row, if empty string, then no class will be applied
        even_class: class of even rows, if empty string, then no class will be applied
        odd_class: class of odd rows, if empty string, then no class will be applied
        title1: The header title over the first text column
        title2: The header title over the second text column
        title3: The header title over the third text column
        button_class: The CSS class to apply to the buttons
        link_ident1: The target page link ident of the first link, if json_ident1 not present or no javascript
        json_ident1: The target JSON page link ident of the first link
        button_text1: Text on the first link button
        link_ident2: The target page link ident of the second link, if json_ident2 not present or no javascript
        json_ident2: The target JSON page link ident of the second link
        button_text2: Text on the second link button
        get_field1_1: The field name is the name (not value) of the get field 1 of the first link, value is bool: True, if get field exists, False if not 
        get_field1_2: The field name is the name (not value) of the get field 2 of the first link, value is bool: True, if get field exists, False if not
        get_field2_1: The field name is the name (not value) of the get field 1 of the second link, value is bool: True, if get field exists, False if not
        get_field2_2: The field name is the name (not value) of the get field 2 of the second link, value is bool: True, if get field exists, False if not
        contents: col 0, 1 and 2 is the text to place in the first three columns,
                    col 3, 4 is the two get field contents of the first link
                    col 5, 6 is the two get field contents of the second link
                    col 7 - True if the first button and link is to be shown, False if not
                    col 8 - True if the second button and link is to be shown, False if not
        """
        Widget.__init__(self, name=name, tag_name="table", brief=brief, **field_args)
        self._url1 = ''
        self._jsonurl1 = ''
        self._url2 = ''
        self._jsonurl2 = ''


    def _build(self, page, ident_list, environ, call_data, lang):
        "Build the table"
        if self.get_field_value("json_ident1"):
            self._jsonurl1 = skiboot.get_url(self.get_field_value("json_ident1"), proj_ident=page.proj_ident)
        if self.get_field_value("json_ident2"):
            self._jsonurl2 = skiboot.get_url(self.get_field_value("json_ident2"), proj_ident=page.proj_ident)
        if self.get_field_value("link_ident1"):
            self._url1 = skiboot.get_url(self.get_field_value("link_ident1"), proj_ident=page.proj_ident)
        if self.get_field_value("link_ident2"):
            self._url2 = skiboot.get_url(self.get_field_value("link_ident2"), proj_ident=page.proj_ident)
        fieldtable = self.get_field_value("contents")
        header = 0
        if self.get_field_value('title1') or self.get_field_value('title2') or self.get_field_value('title3'):
            header = 1
            if self.get_field_value('header_class'):
                self[0] = tag.Part(tag_name='tr', attribs={"class":self.get_field_value('header_class')})
            else:
                self[0] = tag.Part(tag_name='tr')
            self[0][0] = tag.Part(tag_name='th', text = self.get_field_value('title1'))
            self[0][1] = tag.Part(tag_name='th', text = self.get_field_value('title2'))
            self[0][2] = tag.Part(tag_name='th', text = self.get_field_value('title3'))
            self[0][3] = tag.Part(tag_name='th')
            self[0][4] = tag.Part(tag_name='th')
        # set even row colour
        if self.get_field_value('even_class'):
            even = self.get_field_value('even_class')
        else:
            even = ''
        # set odd row colour
        if self.get_field_value('odd_class'):
            odd = self.get_field_value('odd_class')
        else:
            odd = ''
        # create rows
        for index, row in enumerate(fieldtable):
            rownumber = index+header
            if even and (rownumber % 2) :
                self[rownumber] = tag.Part(tag_name="tr", attribs={"class":even})
            elif odd and not (rownumber % 2):
                self[rownumber] = tag.Part(tag_name='tr', attribs={"class":odd})
            else:
                self[rownumber] = tag.Part(tag_name='tr')
            # first three columns are text
            self[rownumber][0] = tag.Part(tag_name='td', text = row[0])
            self[rownumber][1] = tag.Part(tag_name='td', text = row[1])
            self[rownumber][2] = tag.Part(tag_name='td', text = row[2])

            # Next two columns are button links

            self[rownumber][3] = tag.Part(tag_name='td')
            if row[7]:
                # reduce button column to minimum size
                self[rownumber][3].attribs={"style":"width : 1%;"}
                g1 = row[3] if self.get_field_value('get_field1_1') else ''
                g2 = row[4] if self.get_field_value('get_field1_2') else ''
                if self.get_field_value('button_class'):
                    self[rownumber][3][0] = tag.Part(tag_name='a', attribs = {"role":"button", "class":self.get_field_value('button_class')})
                else:
                    self[rownumber][3][0] = tag.Part(tag_name='a', attribs = {"role":"button"})
                self[rownumber][3][0].htmlescaped=False
                if self._url1:
                    if self.get_field_value("button_text1"):
                        self[rownumber][3][0][0] = self.get_field_value("button_text1")
                    else:
                        self[rownumber][3][0][0] = self._url1
                    # create a url for the href
                    get_fields = {self.get_formname("get_field1_1"):g1,
                                                 self.get_formname("get_field1_2"):g2}
                    url = self.make_get_url(page, self._url1, get_fields, True)
                    self[rownumber][3][0].update_attribs({"href": url})
                else:
                    self[rownumber][3][0] = "Warning: broken link"

            self[rownumber][4] = tag.Part(tag_name='td')
            if row[8]:
                # reduce button column to minimum size
                self[rownumber][4].attribs={"style":"width : 1%;"}
                g3 = row[5] if self.get_field_value('get_field2_1') else ''
                g4 = row[6] if self.get_field_value('get_field2_2') else ''
                if self.get_field_value('button_class'):
                    self[rownumber][4][0] = tag.Part(tag_name='a', attribs = {"role":"button", "class":self.get_field_value('button_class')})
                else:
                    self[rownumber][4][0] = tag.Part(tag_name='a', attribs = {"role":"button"})
                self[rownumber][4][0].htmlescaped=False
                if self._url2:
                    if self.get_field_value("button_text2"):
                        self[rownumber][4][0][0] = self.get_field_value("button_text2")
                    else:
                        self[rownumber][4][0][0] = self._url2
                    # create a url for the href
                    get_fields = {self.get_formname("get_field2_1"):g3,
                                                 self.get_formname("get_field2_2"):g4}
                    url = self.make_get_url(page, self._url2, get_fields, True)
                    self[rownumber][4][0].update_attribs({"href": url})
                else:
                    self[rownumber][4][0] = "Warning: broken link"

    def _build_js(self, page, ident_list, environ, call_data, lang):
        """Sets a click event handler"""
        #if not (self._jsonurl1 or self._jsonurl2):
         #   return
        jscript = """  $("#{ident} a").click(function (e) {{
    SKIPOLE.widgets['{ident}'].eventfunc(e);
    }});
""".format(ident = self.get_id())
        return jscript + self._make_fieldvalues( url1=self._jsonurl1, url2=self._jsonurl2)


    def __str__(self):
        """Returns a text string to illustrate the widget"""
        return """
<table>  <!-- with CSS class given by widget_class -->
  <tr> <!-- with header class -->
    <th> <!-- title 1 --> </th>
    <th> <!-- title 2 --> </th>
    <th> <!-- title 3 --> </th>
    <th></th>
    <th></th>
  </tr>
  <tr> <!-- with class  from even or odd classes -->
    <td> <!-- text string --> </td>
    <td> <!-- text string --> </td>
    <td> <!-- text string --> </td>
    <td>
      <a role="button" href="#">
      <!-- With class set by button_class, and the href link will be the url of the link_ident1 with the two get_fields -->
      <!-- the button will show the button_text1  (not html escaped) -->
      </a>
    </td>
    <td>
      <a role="button" href="#">
      <!-- With class set by button_class, and the href link will be the url of the link_ident2 with the two get_fields -->
      <!-- the button will show the button_text2  (not html escaped) -->
      </a>
    </td>
  </tr>
  <!-- rows repeated -->
</table>"""


class Table1_Buttons4(Widget):
    """A table of a single text column, followed by four button links
       There is no header row or column titles, each button link can have one get field"""

    # This class does not display any error messages
    display_errors = False

    arg_descriptions = {'even_class':FieldArg("cssclass", ""),
                        'odd_class':FieldArg("cssclass", ""),
                        'maximize_text_col':FieldArg('boolean',True),
                        'button_class':FieldArg("cssclass", ""),
                        'button_text1':FieldArg('text', ''),
                        'link_ident1':FieldArg("url", ''),
                        'btn_col1':FieldArg("boolean", True, valdt=True),
                        'button_text2':FieldArg('text', ''),
                        'link_ident2':FieldArg("url", ''),
                        'btn_col2':FieldArg("boolean", True, valdt=True),
                        'button_text3':FieldArg('text', ''),
                        'link_ident3':FieldArg("url", ''),
                        'btn_col3':FieldArg("boolean", True, valdt=True),
                        'button_text4':FieldArg('text', ''),
                        'link_ident4':FieldArg("url", ''),
                        'btn_col4':FieldArg("boolean", True, valdt=True),
                        'contents':FieldArgTable(['text', 'text', 'text', 'text', 'text', 'boolean', 'boolean', "boolean", "boolean"]),
                        'col0_classes':FieldArgList('cssclass')
                        }

    def __init__(self, name=None, brief='', **field_args):
        """
        even_class: class of even rows, if empty string, then no class will be applied
        odd_class: class of odd rows, if empty string, then no class will be applied
        maximize_text_col: If True the text column is made large, with the button columns reduced to the size of the buttons
        button_class: The CSS class to apply to the buttons
        button_text1: Text on the first link button
        button_text2: Text on the second link button
        button_text3: Text on the third link button
        button_text4: Text on the fourth link button
        link_ident1: The target page link ident of the first link
        link_ident2: The target page link ident of the second link
        link_ident3: The target page link ident of the third link
        link_ident4: The target page link ident of the fourth link
        btn_col1: The field name is the name (not value) of the get field of the first link, value is bool: True, if column exists, False if not 
        btn_col2: The field name is the name (not value) of the get field of the second link, value is bool: True, if column exists, False if not
        btn_col3: The field name is the name (not value) of the get field of the third link, value is bool: True, if column exists, False if not
        btn_col4: The field name is the name (not value) of the get field of the fourth link, value is bool: True, if column exists, False if not
        contents: col 0 is the text to place in the first column,
                    col 1, 2, 3, 4 are the get field contents of links 1,2,3 and 4
                    col 5 - True if the first button and link is to be shown, False if not
                    col 6 - True if the second button and link is to be shown, False if not
                    col 7 - True if the third button and link is to be shown, False if not
                    col 8 - True if the fourth button and link is to be shown, False if not
        col0_classes: if given is a list of CSS classes to apply to each td of the text column
        """
        Widget.__init__(self, name=name, tag_name="table", brief=brief, **field_args)


    def _build(self, page, ident_list, environ, call_data, lang):
        "Build the table"
        fieldtable = self.get_field_value("contents")
        col0_classes = self.get_field_value("col0_classes")
        # set even row colour
        if self.get_field_value('even_class'):
            even = self.get_field_value('even_class')
        else:
            even = ''
        # set odd row colour
        if self.get_field_value('odd_class'):
            odd = self.get_field_value('odd_class')
        else:
            odd = ''
        # create rows
        for rownumber, row in enumerate(fieldtable):
            if even and (rownumber % 2) :
                self[rownumber] = tag.Part(tag_name="tr", attribs={"class":even})
            elif odd and not (rownumber % 2):
                self[rownumber] = tag.Part(tag_name='tr', attribs={"class":odd})
            else:
                self[rownumber] = tag.Part(tag_name='tr')
            # first column is text, set css class and style
            try:
                css_class = col0_classes[rownumber]
            except IndexError:
                css_class = ''
            if css_class:
                if self.get_field_value('maximize_text_col'):
                    self[rownumber][0] = tag.Part(tag_name='td', text = row[0], attribs={"class":css_class, "style":"width : 100%;"})
                else:
                    self[rownumber][0] = tag.Part(tag_name='td', text = row[0], attribs={"class":css_class})
            else:
                if self.get_field_value('maximize_text_col'):
                    self[rownumber][0] = tag.Part(tag_name='td', text = row[0], attribs={"style":"width : 100%;"})
                else:
                    self[rownumber][0] = tag.Part(tag_name='td', text = row[0])
            # Next four columns are button links
            if self.get_field_value('btn_col1'):
                btn_col1 = tag.Part(tag_name='td')
                if row[5]:
                    g1 = row[1] if row[1] else ''
                    if self.get_field_value('button_class'):
                        btn_col1[0] = tag.Part(tag_name='a', attribs = {"role":"button", "class":self.get_field_value('button_class')})
                    else:
                        btn_col1[0] = tag.Part(tag_name='a', attribs = {"role":"button"})
                    btn_col1[0].htmlescaped=False
                    if self.get_field_value("link_ident1"):
                        url = skiboot.get_url(self.get_field_value("link_ident1"), proj_ident=page.proj_ident)
                        if url:
                            if self.get_field_value("button_text1"):
                                btn_col1[0][0] = self.get_field_value("button_text1")
                            else:
                                btn_col1[0][0] = url
                            # create a url for the href
                            url = self.make_get_url(page, url, {self.get_formname("btn_col1"):g1}, True)
                            btn_col1[0].update_attribs({"href": url})
                        else:
                           btn_col1[0] = "Warning: broken link"
                    else:
                        btn_col1[0] = "Warning: broken link"
                self[rownumber].append(btn_col1)
            if self.get_field_value('btn_col2'):
                btn_col2 = tag.Part(tag_name='td')
                if row[6]:
                    g2 = row[2] if row[2] else ''
                    if self.get_field_value('button_class'):
                        btn_col2[0] = tag.Part(tag_name='a', attribs = {"role":"button", "class":self.get_field_value('button_class')})
                    else:
                        btn_col2[0] = tag.Part(tag_name='a', attribs = {"role":"button"})
                    btn_col2[0].htmlescaped=False
                    if self.get_field_value("link_ident2"):
                        url = skiboot.get_url(self.get_field_value("link_ident2"), proj_ident=page.proj_ident)
                        if url:
                            if self.get_field_value("button_text2"):
                                btn_col2[0][0] = self.get_field_value("button_text2")
                            else:
                                btn_col2[0][0] = url
                            # create a url for the href
                            url = self.make_get_url(page, url, {self.get_formname("btn_col2"):g2}, True)
                            btn_col2[0].update_attribs({"href": url})
                        else:
                            btn_col2[0] = "Warning: broken link"
                    else:
                        btn_col2[0] = "Warning: broken link"
                self[rownumber].append(btn_col2)
            if self.get_field_value('btn_col3'):
                btn_col3 = tag.Part(tag_name='td')
                if row[7]:
                    g3 = row[3] if row[3] else ''
                    if self.get_field_value('button_class'):
                        btn_col3[0] = tag.Part(tag_name='a', attribs = {"role":"button", "class":self.get_field_value('button_class')})
                    else:
                        btn_col3[0] = tag.Part(tag_name='a', attribs = {"role":"button"})
                    btn_col3[0].htmlescaped=False
                    if self.get_field_value("link_ident3"):
                        url = skiboot.get_url(self.get_field_value("link_ident3"), proj_ident=page.proj_ident)
                        if url:
                            if self.get_field_value("button_text3"):
                                btn_col3[0][0] = self.get_field_value("button_text3")
                            else:
                                btn_col3[0][0] = url
                            # create a url for the href
                            url = self.make_get_url(page, url, {self.get_formname("btn_col3"):g3}, True)
                            btn_col3[0].update_attribs({"href": url})
                        else:
                           btn_col3[0] = "Warning: broken link"
                    else:
                        btn_col3[0] = "Warning: broken link"
                self[rownumber].append(btn_col3)
            if self.get_field_value('btn_col4'):
                btn_col4 = tag.Part(tag_name='td')
                if row[8]:
                    g4 = row[4] if row[4] else ''
                    if self.get_field_value('button_class'):
                        btn_col4[0] = tag.Part(tag_name='a', attribs = {"role":"button", "class":self.get_field_value('button_class')})
                    else:
                        btn_col4[0] = tag.Part(tag_name='a', attribs = {"role":"button"})
                    btn_col4[0].htmlescaped=False
                    if self.get_field_value("link_ident4"):
                        url = skiboot.get_url(self.get_field_value("link_ident4"), proj_ident=page.proj_ident)
                        if url:
                            if self.get_field_value("button_text4"):
                                btn_col4[0][0] = self.get_field_value("button_text4")
                            else:
                                btn_col4[0][0] = url
                            # create a url for the href
                            url = self.make_get_url(page, url, {self.get_formname("btn_col4"):g4}, True)
                            btn_col4[0].update_attribs({"href": url})
                        else:
                           btn_col4[0] = "Warning: broken link"
                    else:
                        btn_col4[0] = "Warning: broken link"
                self[rownumber].append(btn_col4)


    def __str__(self):
        """Returns a text string to illustrate the widget"""
        return """
<table>  <!-- with CSS class given by widget_class -->
  <tr> <!-- with class  from even or odd classes -->
    <td> <!-- with style = width : 100% if maximize_text_col is True -->
         <!-- and with a class from col0_classes list if a list is given -->
      <!-- text string -->
    </td>
    <td>  <!-- Exists if btn_col1 is True -->
      <a role="button" href="#">
      <!-- With class set by button_class, and the href link will be the url of the link_ident1 with get field -->
      <!-- the button will show the button_text1 (not html escaped) -->
      </a>
    </td>
    <td>  <!-- Exists if btn_col2 is True -->
      <a role="button" href="#">
      <!-- With class set by button_class, and the href link will be the url of the link_ident2 with get field -->
      <!-- the button will show the button_text2 (not html escaped) -->
      </a>
    </td>
    <td>  <!-- Exists if btn_col3 is True -->
      <a role="button" href="#">
      <!-- With class set by button_class, and the href link will be the url of the link_ident3 with get field -->
      <!-- the button will show the button_text3 (not html escaped) -->
      </a>
    </td>
    <td>  <!-- Exists if btn_col4 is True -->
      <a role="button" href="#">
      <!-- With class set by button_class, and the href link will be the url of the link_ident4 with get field -->
      <!-- the button will show the button_text4 (not html escaped) -->
      </a>
    </td>
  </tr>
  <!-- rows repeated -->
</table>"""


class GeneralButtonTable1(Widget):
    """A table of buttons, text, TextBlocks."""

    # This class does not display any error messages
    display_errors = False

    arg_descriptions = {
                        'rows':FieldArg("integer", ""),
                        'cols':FieldArg("integer", ""),
                        'even_class':FieldArg("cssclass", ""),
                        'odd_class':FieldArg("cssclass", ""),
                        'hide':FieldArg("boolean", False, jsonset=True),
                        'button_class':FieldArg("cssclass", ""),
                        'new_window':FieldArg("boolean", False),
                        'force_ident':FieldArg("boolean", False),
                        'contents':FieldArgTable(['textblock_ref', 'boolean', 'url', 'text', 'text'], valdt=True)
                        }

    def __init__(self, name=None, brief='', **field_args):
        """
        rows: number of rows in the table
        cols: number of columns in the table
        even_class: class of even rows, if empty string, then no class will be applied
        odd_class: class of odd rows, if empty string, then no class will be applied
        hide: if True, table will be hidden
        button_class: The CSS class to apply to the buttons
        new_window: if True, the target='_blank' attribute will be set on each link, to open the target in a new window
        force_ident: If True then the page ident will be included, even if no get field set
                     If False, the page ident will only be included if a get field is set
        contents: A list for every element in the table, should be row*col lists
                   col 0 - text string (This will be either text to display, button text, or Textblock reference)
                   col 1 - True if this is a TextBlock, False if not
                   col 2 - A 'style' string set on the td cell, if empty string, no style applied
                   col 3 - Link ident, if empty, only text will be shown, not a button
                                 if given, a link will be set with button_class applied to it
                   col 4 - The get field value of the button link, empty string if no get field, ignored if no link ident given
 
                  This fieldname used as the widgfield for the get data
        """
        Widget.__init__(self, name=name, tag_name="table", brief=brief, **field_args)


    def _build(self, page, ident_list, environ, call_data, lang):
        "Build the table"
        # Hides widget if no error and hide is True
        self.widget_hide(self.get_field_value("hide"))
        fieldtable = self.get_field_value("contents")
        new_window = self.get_field_value('new_window')
        force_ident = self.get_field_value('force_ident')
        button_class = self.get_field_value('button_class')
        get_field_name = self.get_formname("contents")
        elements = len(fieldtable)
        rows = self.get_field_value("rows")
        cols = self.get_field_value("cols")
        if (not rows) or (not cols):
            self.show = False
            return
        if elements != rows*cols:
            self._error = "Invalid table size : rows (%s) by cols (%s) not equal to given number of table elements (%s)" % (rows, cols, elements)
            return
        # set even row colour
        if self.get_field_value('even_class'):
            even = self.get_field_value('even_class')
        else:
            even = ''
        # set odd row colour
        if self.get_field_value('odd_class'):
            odd = self.get_field_value('odd_class')
        else:
            odd = ''
        # cell  increments for every table cell
        cell = -1
        # create rows
        for rownumber  in range(rows):
            if even and (rownumber % 2) :
                self[rownumber] = tag.Part(tag_name="tr", attribs={"class":even})
            elif odd and not (rownumber % 2):
                self[rownumber] = tag.Part(tag_name='tr', attribs={"class":odd})
            else:
                self[rownumber] = tag.Part(tag_name='tr')
            for colnumber in range(cols):
                cell += 1
                element = fieldtable[cell]
                if element[2]:
                    self[rownumber][colnumber] = tag.Part(tag_name='td', attribs={"style":element[2]})
                else:
                    self[rownumber][colnumber] = tag.Part(tag_name='td')
                if element[0]:
                    if element[1]:
                        # text is a TextBlock
                        textblk = element[0]
                    else:
                        # text is a string
                        textblk = element[0]
                        textblk.text = textblk.textref
                else:
                    textblk = ''
                if element[3]:
                    # its a link
                    # set button text not to be escaped
                    if textblk:
                        textblk.escape = False
                        textblk.linebreaks = False
                    if button_class:
                        self[rownumber][colnumber][0] = tag.Part(tag_name='a', attribs = {"role":"button", "class":button_class})
                    else:
                        self[rownumber][colnumber][0] = tag.Part(tag_name='a', attribs = {"role":"button"})
                    url = skiboot.get_url(element[3], proj_ident=page.proj_ident)
                    if url:
                        if textblk:
                            self[rownumber][colnumber][0][0] = textblk
                        else:
                            self[rownumber][colnumber][0][0] = url
                        # create a url for the href
                        url = self.make_get_url(page, url, {get_field_name:element[4]}, force_ident)
                        if new_window:
                            self[rownumber][colnumber][0].update_attribs({"href": url, "target":"_blank"})
                        else:
                            self[rownumber][colnumber][0].update_attribs({"href": url})
                    else:
                        self[rownumber][colnumber][0] = "Warning: broken link"
                else:
                    # not a link
                    self[rownumber][colnumber][0] = textblk


class GeneralButtonTable2(Widget):
    """A table of buttons and text."""

    # This class does not display any error messages
    display_errors = False

    arg_descriptions = {
                        'rows':FieldArg("integer", ""),
                        'cols':FieldArgTable(['url', 'url']),
                        'even_class':FieldArg("cssclass", ""),
                        'odd_class':FieldArg("cssclass", ""),
                        'hide':FieldArg("boolean", False, jsonset=True),
                        'button_class':FieldArg("cssclass", ""),
                        'contents':FieldArgTable(['text', 'text', 'boolean', 'text'], valdt=True)
                        }

    def __init__(self, name=None, brief='', **field_args):
        """
        rows: number of rows in the table
        cols: A two element list for every column in the table
                  col 0 - target HTML page link ident of buttons in each column, if col1 not present or no javascript
                  col 1 - target JSON page link ident of buttons in each column, 
              col0, col1 values should be emty strings if no url applied to column
        even_class: class of even rows, if empty string, then no class will be applied
        odd_class: class of odd rows, if empty string, then no class will be applied
        hide: if True, table will be hidden
        button_class: The CSS class to apply to the buttons
        contents: A list for every element in the table, should be row*col lists
                   col 0 - text string, either text to display or button text
                   col 1 - A 'style' string set on the td cell, if empty string, no style applied
                   col 2 - Is button? If False only text will be shown, not a button, button class will not be applied
                           If True a link to link_ident/json_ident will be set with button_class applied to it
                   col 3 - The get field value of the button link, empty string if no get field
 
                  This fieldname used as the widgfield for the get data
        """
        Widget.__init__(self, name=name, tag_name="table", brief=brief, **field_args)
        self._jsonurl_list = []


    def _build(self, page, ident_list, environ, call_data, lang):
        "Build the table"
        # Hides widget if no error and hide is True
        self.widget_hide(self.get_field_value("hide"))
        fieldtable = self.get_field_value("contents")
        button_class = self.get_field_value('button_class')
        get_field_name = self.get_formname("contents")
        elements = len(fieldtable)
        rows = self.get_field_value("rows")
        colidents = self.get_field_value("cols")
        cols = len(colidents)
        if (not rows) or (not cols):
            self.show = False
            return
        if elements != rows*cols:
            self._error = "Invalid table size : rows (%s) by cols (%s) not equal to given number of table elements (%s)" % (rows, cols, elements)
            return
        # list of json url's
        self._jsonurl_list = [ skiboot.get_url(item[1], proj_ident=page.proj_ident) for item in colidents ]
        # list of html url's
        url_list = []
        for item in colidents:
            url = ''
            if item[0]:
                url = skiboot.get_url(item[0], proj_ident=page.proj_ident)
            if not url:
                url = skiboot.get_url('no_javascript', proj_ident=page.proj_ident)
            if not url:
                url = ''
            url_list.append(url)
        # set even row class
        if self.get_field_value('even_class'):
            even = self.get_field_value('even_class')
        else:
            even = ''
        # set odd row class
        if self.get_field_value('odd_class'):
            odd = self.get_field_value('odd_class')
        else:
            odd = ''
        # cell  increments for every table cell
        cell = -1
        # create rows
        for rownumber  in range(rows):
            if even and (rownumber % 2) :
                self[rownumber] = tag.Part(tag_name="tr", attribs={"class":even})
            elif odd and not (rownumber % 2):
                self[rownumber] = tag.Part(tag_name='tr', attribs={"class":odd})
            else:
                self[rownumber] = tag.Part(tag_name='tr')
            for colnumber in range(cols):
                cell += 1
                element = fieldtable[cell]
                # cell text
                if element[0]:
                    celltext = element[0]
                else:
                    celltext = ''
                # cell class
                if element[1]:
                    self[rownumber][colnumber] = tag.Part(tag_name='td', attribs={"style":element[1]})
                else:
                    self[rownumber][colnumber] = tag.Part(tag_name='td')
                # get html url for this column
                url = url_list[colnumber]
                # is it a button link
                if url and element[2]:
                    # its a link, apply button class
                    if button_class:
                        self[rownumber][colnumber][0] = tag.Part(tag_name='a', attribs = {"role":"button", "class":button_class})
                    else:
                        self[rownumber][colnumber][0] = tag.Part(tag_name='a', attribs = {"role":"button"})
                     # apply button text
                    if celltext:
                        self[rownumber][colnumber][0][0] = celltext
                    else:
                        self[rownumber][colnumber][0][0] = url
                    # create a url for the href
                    cellurl = self.make_get_url(page, url, {get_field_name:element[3]}, True)
                    # apply url and href
                    self[rownumber][colnumber][0].update_attribs({"href": cellurl})
                else:
                    # not a link
                    self[rownumber][colnumber][0] = celltext

    def _build_js(self, page, ident_list, environ, call_data, lang):
        """Sets a click event handler"""
        jscript = """  $("#{ident} a").click(function (e) {{
    SKIPOLE.widgets['{ident}'].eventfunc(e);
    }});
""".format(ident = self.get_id())
        if self._jsonurl_list:
            return jscript + self._make_fieldvalues(url=self._jsonurl_list)
        return jscript


