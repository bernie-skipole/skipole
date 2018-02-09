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
            if button_class:
                lnk.update_attribs({"class":button_class})
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

    @classmethod
    def description(cls):
        """Returns a text string to illustrate the widget"""
        return """
<div>  <!-- with widget id and class widget_class -->
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
        button_class = self.get_field_value('button_class')
        button_style = self.get_field_value('button_style')

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
            if button_class:
                lnk.update_attribs({"class":button_class})
            if button_style:
                lnk.update_attribs({"style":button_style})
            # create a url for the href
            get_field = {self.get_formname("nav_links"):link_getdata}
            url = self.make_get_url(page, url, get_field, link_force_ident)
            lnk.update_attribs({"href": url})
            self.append(lnk)

    @classmethod
    def description(cls):
        """Returns a text string to illustrate the widget"""
        return """
<div>  <!-- with widget id and class widget_class -->
  <a role=\"button\" href=\"#\">  <!-- with class set to button_class -->
    <!-- The displayed text of the link -->
  </a>
  <!-- further links -->
</div>"""




class TabButtons1(Widget):
    """Defines a div, containing tab buttons which can hide/display portions of the page.
       Hides and part of the page with a given class, then displays a portion of the
       page with a given id"""

    # This class does not display any error messages
    display_errors = False

    arg_descriptions = {
                        'tabs':FieldArgTable(("text", "text")), # text on button, id to display
                        'hide_class':FieldArg("cssclass", ''),
                        'button_class':FieldArg("cssclass", ''),
                        'button_style':FieldArg("cssstyle", ''),
                        'onclick_addclass':FieldArg("cssstyle", ''),
                        'onclick_removeclass':FieldArg("cssstyle", '')
                       }

    def __init__(self, name=None, brief='', **field_args):
        """
        tabs: A list of lists, each inner list describing a button
          0 : The text to appear on the button
          1 : The id of the portion of the page to make visible
        button_class: The CSS class of the buttons
        button_style: The button style
        onclick_addclass: CSS class to add to a button when it is clicked
        onclick_removeclass: CSS class to remove from a button when it is clicked
        """
        Widget.__init__(self, name=name, tag_name="div", brief=brief, **field_args)
        # as this widget does not display errors, and is not json settable, hide if empty
        self.hide_if_empty=True
        self._display_id_list = []
        self._hide_class = ''
        self._onclick_addclass = ''
        self._onclick_removeclass = ''


    def _build(self, page, ident_list, environ, call_data, lang):
        "Build the list of buttons"

        # get parameters to send to javascript
        self._hide_class = self.get_field_value('hide_class')
        self._onclick_addclass = self.get_field_value('onclick_addclass')
        self._onclick_removeclass = self.get_field_value('onclick_removeclass')

        button_class = self.get_field_value('button_class')
        button_style = self.get_field_value('button_style')
        # for each button in the tabs table - create a button and add it

        for buttontext, displayid in self.get_field_value('tabs'):
            if not (buttontext or displayid):
                continue
            btn = tag.Part(tag_name="button", text=buttontext)
            # give each button button_class and self._onclick_removeclass which will be removed when the button is clicked
            if button_class and self._onclick_removeclass:
                if button_class == self._onclick_removeclass:
                    btn.update_attribs({"class":button_class})
                else:
                    btn.update_attribs({"class":button_class + " " + self._onclick_removeclass})
            elif button_class:
                btn.update_attribs({"class":button_class})
            elif self._onclick_removeclass:
                btn.update_attribs({"class":self._onclick_removeclass})
            if button_style:
                btn.update_attribs({"style":button_style})
            self.append(btn)
            self._display_id_list.append(displayid)


    def _build_js(self, page, ident_list, environ, call_data, lang):
        """Sets a click event handler"""
        jscript = """  $("#{ident} button").click(function (e) {{
    SKIPOLE.widgets['{ident}'].eventfunc(e);
    }});
""".format(ident = self.get_id())
        other_parameters = {}
        if self._display_id_list:
            other_parameters['display_id_list'] = self._display_id_list
        if self._hide_class:
            other_parameters['hide_class'] = self._hide_class
        if self._onclick_addclass:
            other_parameters['onclick_addclass'] = self._onclick_addclass
        if self._onclick_removeclass:
            other_parameters['onclick_removeclass'] = self._onclick_removeclass
        if other_parameters:
            return jscript + self._make_fieldvalues(**other_parameters)
        else:
            return jscript


    @classmethod
    def description(cls):
        """Returns a text string to illustrate the widget"""
        return """
<div>  <!-- with widget id and class widget_class -->
  <button>  <!-- with class set to button_class -->
    <!-- The displayed text of the button -->
  </button>
  <!-- further buttons -->
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


    @classmethod
    def description(cls):
        """Returns a text string to illustrate the widget"""
        return """
<p>  <!-- with widget id and class widget_class, normally hidden,
          shown when an error is displayed. -->
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

    @classmethod
    def description(cls):
        """Returns a text string to illustrate the widget"""
        return """
<h1>  <!-- default h1, tag can be specified and with widget id and class widget_class -->
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



    @classmethod
    def description(cls):
        """Returns a text string to illustrate the widget"""
        return """
<div> <!--  with widget id and class widget_class -->
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



    @classmethod
    def description(cls):
        """Returns a text string to illustrate the widget"""
        return """
<div> <!--  with widget id and class widget_class -->
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



    @classmethod
    def description(cls):
        """Returns a text string to illustrate the widget"""
        return """
<div> <!-- with widget id and class widget_class -->
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



    @classmethod
    def description(cls):
        """Returns a text string to illustrate the widget"""
        return """
<div> <!-- with widget id and class widget_class -->
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



    @classmethod
    def description(cls):
        """Returns a text string to illustrate the widget"""
        return """
<div> <!-- with widget id and class widget_class -->
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



    @classmethod
    def description(cls):
        """Returns a text string to illustrate the widget"""
        return """
<div> <!-- with widget id and class widget_class -->
  <h6> <!-- content set to large_text --> </h6>
  <p> <!-- content set to small_text --> </p>
  <div style="display:none;"> <!-- class set to error_class -->
    <p> <!-- content set to show_error --> </p>
  </div>
</div>"""



