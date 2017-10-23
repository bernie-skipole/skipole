####### SKIPOLE WEB FRAMEWORK #######
#
# headers.py  - page header widgets
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

"""Defines widgets of page headers,
typically with titles, logo images and navigational buttons."""

from .. import skiboot
from .. import tag
from . import Widget, FieldArg, FieldArgList, FieldArgTable, FieldArgDict


class NavButtons1(Widget):
    """Defines a div, with a normally hidden error paragraph followed by a list of navigation buttons."""

    error_location = (0,0,0)

    arg_descriptions = {
                        'nav_links':FieldArgTable(("url", "text", "boolean", "text"), valdt=True),    # target, text in box, force_ident, get data
                        'button_class':FieldArg("cssclass", ''),
                        'li_class':FieldArg("cssclass", ''),
                        'ul_class':FieldArg("cssclass", ''),
                        'error_class':FieldArg("cssclass", "")
                       }

    def __init__(self, name=None, brief='', **field_args):
        """
         nav_links: A list of lists, each inner list describing a link, the name of this field is used in the
               widgfield for any data returned in the get field
        For each navigation link, the table row is
          0 : The url, label or ident of the target page of the link
          1 : The displayed text of the link
          2 : If True, ident is appended to link even if there is no get field
          3 : The get field data to send with the link
        button_class: The class of the button links - which provides the appearance via CSS
        li_class: The class of the li tag
        ul_class: The class of the ul tag
        """
        Widget.__init__(self, name=name, tag_name="div", brief=brief, **field_args)
        self[0] = tag.Part(tag_name="div", attribs={"style":"display:none;"})
        self[0][0] = tag.Part(tag_name="p")
        self[0][0][0] = ''
        self[1] = tag.Part(tag_name="ul")


    def _build(self, page, ident_list, environ, call_data, lang):
        "Build the header"
        nav_links_name = self.get_name('nav_links')
        button_class = self.get_field_value('button_class')
        li_class = self.get_field_value('li_class')

        if self.get_field_value('error_class'):
            self[0].update_attribs({"class":self.get_field_value('error_class')})
        if self.error_status:
            self[0].del_one_attrib("style")
        if self.get_field_value('ul_class'):
            self[1].update_attribs({"class":self.get_field_value('ul_class')})

        # for each link in the nav_links table - create a link and add it
        # as a list item
        for row in self.get_field_value('nav_links'):
            linkurl, linktext, link_force_ident, link_getdata = row
            if not (linkurl or linktext):
                continue
            url = skiboot.get_url(linkurl, proj_ident=page.proj_ident)
            if not url:
                continue
            lnk = tag.Part(tag_name="a", text=linktext, attribs={"role":"button"})
            if self.get_field_value('button_class'):
                lnk.update_attribs({"class":self.get_field_value('button_class')})
            # create a url for the href
            get_field = {self.get_formname("nav_links"):link_getdata}
            url = self.make_get_url(page, url, get_field, link_force_ident)
            lnk.update_attribs({"href": url})
            if li_class:
                listtag = tag.Part(tag_name="li", attribs={'class':li_class})
            else:
                listtag = tag.Part(tag_name="li")
            listtag[0] = lnk
            self[1].append(listtag)

    def __str__(self):
        """Returns a text string to illustrate the widget"""
        return """
<div>  <!-- div has class set to widget_class -->
  <div>  <!-- normally hidden, class set to error_class -->
    <p> <!-- error message appears in this paragraph --> </p>
  </div>
  <ul>   <!-- class set to ul_class -->
    <li> <!-- class set to li_class -->
      <a role=\"button\" href=\"#\">  <!-- with class set to button_class -->
         <!-- The displayed text of the link -->
      </a>
    </li>
    <!-- further links -->
  </ul>
</div>"""




class NavButtons2(Widget):
    """Defines a div, containing navigation button links."""

    # This class does not display any error messages
    display_errors = False

    arg_descriptions = {
                        'nav_links':FieldArgTable(("url", "text", "boolean", "text"), valdt=True),    # target, text in box, force_ident, get data
                        'button_class':FieldArg("cssclass", ''),
                        'button_style':FieldArg("cssstyle", '')
                       }

    def __init__(self, name=None, brief='', **field_args):
        """
         nav_links: A list of lists, each inner list describing a link, the name of this field is used in the
               widgfield for any data returned in the get field
        For each navigation link, the table row is
          0 : The url, label or ident of the target page of the link
          1 : The displayed text of the link
          2 : If True, ident is appended to link even if there is no get field
          3 : The get field data to send with the link
        button_class: The class of the button links - which provides the appearance via CSS
        """
        Widget.__init__(self, name=name, tag_name="div", brief=brief, **field_args)
        # as this widget does not display errors, and is not json settable, hide if empty
        self.hide_if_empty=True


    def _build(self, page, ident_list, environ, call_data, lang):
        "Build the list of links"
        nav_links_name = self.get_name('nav_links')
        button_class = self.get_field_value('button_class')


        # for each link in the nav_links table - create a link and add it
        # as a list item
        for row in self.get_field_value('nav_links'):
            linkurl, linktext, link_force_ident, link_getdata = row
            if not (linkurl or linktext):
                continue
            url = skiboot.get_url(linkurl, proj_ident=page.proj_ident)
            if not url:
                continue
            lnk = tag.Part(tag_name="a", text=linktext, attribs={"role":"button"})
            if self.get_field_value('button_class'):
                lnk.update_attribs({"class":self.get_field_value('button_class')})
            if self.get_field_value('button_style'):
                lnk.update_attribs({"style":self.get_field_value('button_style')})
            # create a url for the href
            get_field = {self.get_formname("nav_links"):link_getdata}
            url = self.make_get_url(page, url, get_field, link_force_ident)
            lnk.update_attribs({"href": url})
            self.append(lnk)

    def __str__(self):
        """Returns a text string to illustrate the widget"""
        return """
<div>  <!-- div has class set to widget_class -->
  <a role=\"button\" href=\"#\">  <!-- with class set to button_class -->
    <!-- The displayed text of the link -->
  </a>
  <!-- further links -->
</div>"""




class HeaderErrorPara(Widget):
    """A paragraph containing error text - normally hidden, displayed on error"""

    error_location = 0

    arg_descriptions = {
                        'hide':FieldArg("boolean", True, jsonset=True)
                       }

    def __init__(self, name=None, brief='', **field_args):
        """
        hide: If True, sets display: none; on the widget, can be set/unset via JSON file
                    on error the value is overridden and the widget is shown
        """
        Widget.__init__(self, name=name, tag_name="p", brief=brief, **field_args)
        self[0] = self.error_message

    def _build(self, page, ident_list, environ, call_data, lang):
        # Hides widget if no error and hide is True
        self.widget_hide(self.get_field_value("hide"))


    def __str__(self):
        """Returns a text string to illustrate the widget"""
        return """
<p>  <!-- paragraph normally hidden, shown when an error is displayed.
          With class set to widget_class -->
  <!-- error message appears in this paragraph -->
</p>
"""


class HeadText(Widget):
    """A tag, normally a h1 tag, which can be specified, containing text"""

     # This class does not display any error messages
    display_errors = False

    arg_descriptions = {'tag':FieldArg("text", 'h1'),
                        'large_text':FieldArg("text", "", jsonset=True)}

    def __init__(self, name=None, brief='', **field_args):
        """
        large_text: The text appearing in the tag
        """
        # pass fields to Widget
        Widget.__init__(self, name=name, tag_name="h1", brief=brief, **field_args)
        self[0] = ''

    def _build(self, page, ident_list, environ, call_data, lang):
        self.tag_name = self.get_field_value('tag')
        self[0] = self.get_field_value("large_text")

    def __str__(self):
        """Returns a text string to illustrate the widget"""
        return """
<h1>  <!-- default h1, tag can be specified and class widget_class -->
    <!-- set with large_text -->
</h1>"""


class HeaderText1(Widget):
    """Defines a div with large text (h1) and small text (p)."""

    error_location = (2,0,0)

    arg_descriptions = {
                        'large_text':FieldArg("text", '', jsonset=True),
                        'small_text':FieldArg("text", '', jsonset=True),
                        'show_error':FieldArg("text", default="", valdt=False, jsonset=True),
                        'error_class':FieldArg("cssclass", "")
                       }

    def __init__(self, name=None, brief='', **field_args):
        """
        large_text: The large text at the top of the page
        small_text:  The smaller text, at the top of the page, but beneath the large text
        error_class: The class applied to the paragraph containing the error message on error.
        """
        Widget.__init__(self, name=name, tag_name="div", brief=brief, **field_args)
        self[0] = tag.Part(tag_name="h1")
        self[1] = tag.Part(tag_name="p")
        # error div at 2
        self[2] = tag.Part(tag_name="div", attribs={"style":"display:none;"})
        self[2][0] = tag.Part(tag_name="p")
        self[2][0][0] = ''

    def _build(self, page, ident_list, environ, call_data, lang):
        "Build the header"
        self[0].text=self.get_field_value("large_text")
        self[1].text=self.get_field_value("small_text")
        if self.get_field_value('error_class'):
            self[2].update_attribs({"class":self.get_field_value('error_class')})
        if self.error_status:
            self[2].del_one_attrib("style")



    def __str__(self):
        """Returns a text string to illustrate the widget"""
        return """
<div> <!--  class to widget_class -->
  <h1> <!-- content set to large_text --> </h1>
  <p> <!-- content set to small_text --> </p>
  <div style="display:none;"> <!-- class set to error_class -->
    <p> <!-- content set to show_error --> </p>
  </div>
</div>"""


class HeaderText2(Widget):
    """Defines a div with large text (h2) and small text (p)."""

    error_location = (2,0,0)

    arg_descriptions = {
                        'large_text':FieldArg("text", '', jsonset=True),
                        'small_text':FieldArg("text", '', jsonset=True),
                        'show_error':FieldArg("text", default="", valdt=False, jsonset=True),
                        'error_class':FieldArg("cssclass", "")
                       }

    def __init__(self, name=None, brief='', **field_args):
        """
        large_text: The large text at the top of the page
        small_text:  The smaller text, at the top of the page, but beneath the large text
        error_class: The class applied to the paragraph containing the error message on error.
        """
        Widget.__init__(self, name=name, tag_name="div", brief=brief, **field_args)
        self[0] = tag.Part(tag_name="h2")
        self[1] = tag.Part(tag_name="p")
        # error div at 2
        self[2] = tag.Part(tag_name="div", attribs={"style":"display:none;"})
        self[2][0] = tag.Part(tag_name="p")
        self[2][0][0] = ''


    def _build(self, page, ident_list, environ, call_data, lang):
        "Build the header"
        self[0].text=self.get_field_value("large_text")
        self[1].text=self.get_field_value("small_text")
        if self.get_field_value('error_class'):
            self[2].update_attribs({"class":self.get_field_value('error_class')})
        if self.error_status:
            self[2].del_one_attrib("style")



    def __str__(self):
        """Returns a text string to illustrate the widget"""
        return """
<div> <!--  class to widget_class -->
  <h2> <!-- content set to large_text --> </h2>
  <p> <!-- content set to small_text --> </p>
  <div style="display:none;"> <!-- class set to error_class -->
    <p> <!-- content set to show_error --> </p>
  </div>
</div>"""


class HeaderText3(Widget):
    """Defines a div with large text (h3) and small text (p)."""

    error_location = (2,0,0)

    arg_descriptions = {
                        'large_text':FieldArg("text", '', jsonset=True),
                        'small_text':FieldArg("text", '', jsonset=True),
                        'show_error':FieldArg("text", default="", valdt=False, jsonset=True),
                        'error_class':FieldArg("cssclass", "")
                       }

    def __init__(self, name=None, brief='', **field_args):
        """
        large_text: The large text at the top of the page
        small_text:  The smaller text, at the top of the page, but beneath the large text
        error_class: The class applied to the paragraph containing the error message on error.
        """
        Widget.__init__(self, name=name, tag_name="div", brief=brief, **field_args)
        self[0] = tag.Part(tag_name="h3")
        self[1] = tag.Part(tag_name="p")
        # error div at 2
        self[2] = tag.Part(tag_name="div", attribs={"style":"display:none;"})
        self[2][0] = tag.Part(tag_name="p")
        self[2][0][0] = ''


    def _build(self, page, ident_list, environ, call_data, lang):
        "Build the header"
        self[0].text=self.get_field_value("large_text")
        self[1].text=self.get_field_value("small_text")
        if self.get_field_value('error_class'):
            self[2].update_attribs({"class":self.get_field_value('error_class')})
        if self.error_status:
            self[2].del_one_attrib("style")



    def __str__(self):
        """Returns a text string to illustrate the widget"""
        return """
<div> <!--  class to widget_class -->
  <h3> <!-- content set to large_text --> </h3>
  <p> <!-- content set to small_text --> </p>
  <div style="display:none;"> <!-- class set to error_class -->
    <p> <!-- content set to show_error --> </p>
  </div>
</div>"""


class HeaderText4(Widget):
    """Defines a div with large text (h4) and small text (p)."""

    error_location = (2,0,0)

    arg_descriptions = {
                        'large_text':FieldArg("text", '', jsonset=True),
                        'small_text':FieldArg("text", '', jsonset=True),
                        'show_error':FieldArg("text", default="", valdt=False, jsonset=True),
                        'error_class':FieldArg("cssclass", "")
                       }

    def __init__(self, name=None, brief='', **field_args):
        """
        large_text: The large text at the top of the page
        small_text:  The smaller text, at the top of the page, but beneath the large text
        error_class: The class applied to the paragraph containing the error message on error.
        """
        Widget.__init__(self, name=name, tag_name="div", brief=brief, **field_args)
        self[0] = tag.Part(tag_name="h4")
        self[1] = tag.Part(tag_name="p")
        # error div at 2
        self[2] = tag.Part(tag_name="div", attribs={"style":"display:none;"})
        self[2][0] = tag.Part(tag_name="p")
        self[2][0][0] = ''


    def _build(self, page, ident_list, environ, call_data, lang):
        "Build the header"
        self[0].text=self.get_field_value("large_text")
        self[1].text=self.get_field_value("small_text")
        if self.get_field_value('error_class'):
            self[2].update_attribs({"class":self.get_field_value('error_class')})
        if self.error_status:
            self[2].del_one_attrib("style")



    def __str__(self):
        """Returns a text string to illustrate the widget"""
        return """
<div> <!--  class to widget_class -->
  <h4> <!-- content set to large_text --> </h4>
  <p> <!-- content set to small_text --> </p>
  <div style="display:none;"> <!-- class set to error_class -->
    <p> <!-- content set to show_error --> </p>
  </div>
</div>"""


class HeaderText5(Widget):
    """Defines a div with large text (h5) and small text (p)."""

    error_location = (2,0,0)

    arg_descriptions = {
                        'large_text':FieldArg("text", '', jsonset=True),
                        'small_text':FieldArg("text", '', jsonset=True),
                        'show_error':FieldArg("text", default="", valdt=False, jsonset=True),
                        'error_class':FieldArg("cssclass", "")
                       }

    def __init__(self, name=None, brief='', **field_args):
        """
        large_text: The large text at the top of the page
        small_text:  The smaller text, at the top of the page, but beneath the large text
        error_class: The class applied to the paragraph containing the error message on error.
        """
        Widget.__init__(self, name=name, tag_name="div", brief=brief, **field_args)
        self[0] = tag.Part(tag_name="h5")
        self[1] = tag.Part(tag_name="p")
        # error div at 2
        self[2] = tag.Part(tag_name="div", attribs={"style":"display:none;"})
        self[2][0] = tag.Part(tag_name="p")
        self[2][0][0] = ''


    def _build(self, page, ident_list, environ, call_data, lang):
        "Build the header"
        self[0].text=self.get_field_value("large_text")
        self[1].text=self.get_field_value("small_text")
        if self.get_field_value('error_class'):
            self[2].update_attribs({"class":self.get_field_value('error_class')})
        if self.error_status:
            self[2].del_one_attrib("style")



    def __str__(self):
        """Returns a text string to illustrate the widget"""
        return """
<div> <!--  class to widget_class -->
  <h5> <!-- content set to large_text --> </h5>
  <p> <!-- content set to small_text --> </p>
  <div style="display:none;"> <!-- class set to error_class -->
    <p> <!-- content set to show_error --> </p>
  </div>
</div>"""


class HeaderText6(Widget):
    """Defines a div with large text (h6) and small text (p)."""

    error_location = (2,0,0)

    arg_descriptions = {
                        'large_text':FieldArg("text", '', jsonset=True),
                        'small_text':FieldArg("text", '', jsonset=True),
                        'show_error':FieldArg("text", default="", valdt=False, jsonset=True),
                        'error_class':FieldArg("cssclass", "")
                       }

    def __init__(self, name=None, brief='', **field_args):
        """
        large_text: The large text at the top of the page
        small_text:  The smaller text, at the top of the page, but beneath the large text
        error_class: The class applied to the paragraph containing the error message on error.
        """
        Widget.__init__(self, name=name, tag_name="div", brief=brief, **field_args)
        self[0] = tag.Part(tag_name="h6")
        self[1] = tag.Part(tag_name="p")
        # error div at 2
        self[2] = tag.Part(tag_name="div", attribs={"style":"display:none;"})
        self[2][0] = tag.Part(tag_name="p")
        self[2][0][0] = ''


    def _build(self, page, ident_list, environ, call_data, lang):
        "Build the header"
        self[0].text=self.get_field_value("large_text")
        self[1].text=self.get_field_value("small_text")
        if self.get_field_value('error_class'):
            self[2].update_attribs({"class":self.get_field_value('error_class')})
        if self.error_status:
            self[2].del_one_attrib("style")



    def __str__(self):
        """Returns a text string to illustrate the widget"""
        return """
<div> <!--  class to widget_class -->
  <h6> <!-- content set to large_text --> </h6>
  <p> <!-- content set to small_text --> </p>
  <div style="display:none;"> <!-- class set to error_class -->
    <p> <!-- content set to show_error --> </p>
  </div>
</div>"""



