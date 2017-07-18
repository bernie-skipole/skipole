####### SKIPOLE WEB FRAMEWORK #######
#
# paras.py  - Contains commonly used paragraph widgets
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

"""Contains commonly used paragraphs"""

from string import Template
import json

from .. import skiboot
from .. import tag
from . import Widget, ClosedWidget, FieldArg, FieldArgList, FieldArgTable, FieldArgDict


class TagBlock(Widget):

    # This class does not display any error messages
    display_errors = False

    arg_descriptions = {'tag':FieldArg("text", 'div'),
                        'hide':FieldArg("boolean", False, jsonset=True)}

    _container = (0,)

    def __init__(self, name=None, brief='', **field_args):
        """Acts as a widget, containing other widgets, so show, class and hide can be set"""
        Widget.__init__(self, name=name, tag_name="div", brief=brief, **field_args)
        self[0] =  ""  # where items can be contained

    def _build(self, page, ident_list, environ, call_data, lang):
        self.tag_name = self.get_field_value('tag')
        # Hides widget if no error and hide is True
        self.widget_hide(self.get_field_value("hide"))

    def __str__(self):
        """Returns a text string to illustrate the widget"""
        return """
<div>  <!-- with div tag, or any other specified and class widget_class -->
               <!-- and attribute style=display:none if hide is True -->
  <!-- further html and widgets can be contained here -->
</div>"""


class DivStyleDiv(Widget):

    # This class does not display any error messages
    display_errors = False

    arg_descriptions = {
                        'inner_tag':FieldArg("text", 'div'),
                        'style':FieldArg("cssstyle", ''),
                        'set_text':FieldArg("text", "")}

    def __init__(self, name=None, brief='', **field_args):
        """A div, containing a div which can have a style set, containing text
            inner_tag - the tag of the inside element
           style - the style of the inside element"""
        Widget.__init__(self, name=name, tag_name="div", brief=brief, **field_args)
        self[0] = tag.Part(tag_name='div')
        self[0][0] =  ""  # where text is to be set

    def _build(self, page, ident_list, environ, call_data, lang):
        self[0].tag_name = self.get_field_value('inner_tag')
        if self.get_field_value('style'):
            self[0].update_attribs({"style":self.get_field_value('style')})
        self[0][0] = self.get_field_value("set_text")

    def __str__(self):
        """Returns a text string to illustrate the widget"""
        return """
<div>  <!-- with class widget_class -->
  <div>  <!-- with div tag, or any other specified and the set style -->
    <!-- set with text -->
  </div>
</div>"""


class DivHTML(Widget):

    # This class does not display any error messages
    display_errors = False

    arg_descriptions = {'set_html':FieldArg("text", "", jsonset=True)}

    def __init__(self, name=None, brief='', **field_args):
        """A div, containing a string, which will be set as html, without escaping"""
        Widget.__init__(self, name=name, tag_name="div", brief=brief, **field_args)
        self[0] = ""  # where the html string is to be set
        self.htmlescaped = False

    def _build(self, page, ident_list, environ, call_data, lang):
        self[0] = self.get_field_value("set_html")

    def __str__(self):
        """Returns a text string to illustrate the widget"""
        return """
<div>  <!-- with class widget_class -->
    <!-- set with the set_html string -->
</div>"""


class PreText(Widget):
    """A pre tag, containing text, if an error is raised, then the text is changed
       for the error_message"""

    error_location = 0

    arg_descriptions = {'pre_text':FieldArg("text", "", jsonset=True)}

    def __init__(self, name=None, brief='', **field_args):
        """
        pre_text: The text appearing in the pre tag
        """
        # pass fields to Widget
        Widget.__init__(self, name=name, tag_name="pre", brief=brief, **field_args)
        self[0] = ''

    def _build(self, page, ident_list, environ, call_data, lang):
        self[0] = self.get_field_value("pre_text")

    def __str__(self):
        """Returns a text string to illustrate the widget"""
        return """
<pre>  <!-- with class widget_class -->
    <!-- set with text, replaced by error message on error -->
</pre>"""


class SpanText(Widget):
    """A span tag, containing text"""

     # This class does not display any error messages
    display_errors = False

    arg_descriptions = {'span_text':FieldArg("text", "", jsonset=True)}

    def __init__(self, name=None, brief='', **field_args):
        """
        span_text: The text appearing in the span tag
        """
        # pass fields to Widget
        Widget.__init__(self, name=name, tag_name="span", brief=brief, **field_args)
        self[0] = ''

    def _build(self, page, ident_list, environ, call_data, lang):
        self[0] = self.get_field_value("span_text")

    def __str__(self):
        """Returns a text string to illustrate the widget"""
        return """
<span>  <!-- with class widget_class -->
    <!-- set with text -->
</span>"""


class TagText(Widget):
    """A tag, which can be specified, containing text"""

     # This class does not display any error messages
    display_errors = False

    arg_descriptions = {'tag':FieldArg("text", 'div'),
                        'hide':FieldArg("boolean", False, jsonset=True),
                        'tag_text':FieldArg("text", "", jsonset=True)}

    def __init__(self, name=None, brief='', **field_args):
        """
        tag_text: The text appearing in the tag
        """
        # pass fields to Widget
        Widget.__init__(self, name=name, tag_name="div", brief=brief, **field_args)
        self[0] = ''

    def _build(self, page, ident_list, environ, call_data, lang):
        self.tag_name = self.get_field_value('tag')
        # Hides widget if no error and hide is True
        self.widget_hide(self.get_field_value("hide"))
        self[0] = self.get_field_value("tag_text")

    def __str__(self):
        """Returns a text string to illustrate the widget"""
        return """
<div>  <!-- with div tag, or any other specified and class widget_class -->
               <!-- and attribute style=display:none if hide is True -->
    <!-- set with text -->
</div>"""


class ParaText(Widget):
    """A p tag, containing text"""

     # This class does not display any error messages
    display_errors = False

    arg_descriptions = {'para_text':FieldArg("text", "", jsonset=True)}

    def __init__(self, name=None, brief='', **field_args):
        """
        para_text: The text appearing in the p tag
        """
        # pass fields to Widget
        Widget.__init__(self, name=name, tag_name="p", brief=brief, **field_args)
        self[0] = ''

    def _build(self, page, ident_list, environ, call_data, lang):
        self[0] = self.get_field_value("para_text")

    def __str__(self):
        """Returns a text string to illustrate the widget"""
        return """
<p>  <!-- with class widget_class -->
    <!-- set with text -->
</p>"""


class DivPara(Widget):
    """A div containing a paragraph, containing text, if an error is raised, then the text is changed
       for the error_message and the error_class given to the paragraph"""

    error_location = (0,0)

    arg_descriptions = {'para_text':FieldArg("text", "", jsonset=True),
                        'para_class':FieldArg("cssclass", ""),
                        'error_class':FieldArg("cssclass", ""),
                        'pre_line':FieldArg("boolean", True)
                       }

    def __init__(self, name=None, brief='', **field_args):
        """
        para_text: The text appearing in the paragraph
        para_class: The class of the paragraph
        error_class: The class of the error text - which provides the appearance via CSS
                     replaces para_class on error.
        pre_line: If True, sets style="white-space: pre-line;" into the paragraph which preserves
                  new line breaks
        """
        # pass fields to Widget
        Widget.__init__(self, name=name, tag_name="div", brief=brief, **field_args)
        self[0] = tag.Part(tag_name='p')
        # do not insert <br /> - leave that to pre_line
        self[0].linebreaks=False
        self[0][0] = ''

    def _build(self, page, ident_list, environ, call_data, lang):
        if self.get_field_value("pre_line"):
            self[0].attribs={"style":"white-space: pre-line;"}
        if self.get_field_value('para_class'):
            self[0].update_attribs({"class":self.get_field_value('para_class')})
        # self[0][0] could be set by an error message
        if not self.error_status:
            self[0][0] = self.get_field_value("para_text")
        if self.error_status and self.get_field_value('error_class'):
            self[0].update_attribs({"class":self.get_field_value('error_class')})

            
    def _build_js(self, page, ident_list, environ, call_data, lang):
        """Sets fieldvalues"""
        return self._make_fieldvalues('para_class', 'error_class')


    def __str__(self):
        """Returns a text string to illustrate the widget"""
        return """
<div>  <!-- with class widget_class -->
    <p style = "white-space: pre-line;">
    <!-- with class para_class, and style set if pre_line is True -->
    <!-- and class changed to error_class on error -->
        <!-- set with para_text, replaced by error message on error -->
    </p>
</div>"""


class JSONTextLink(Widget):
    """A div, containing an anchor link (used as a button) followed by a paragraph containing text
       If the button is pressed, and the text is visible - the text is hidden, and button text set to 'button_show_text'.
       If the button is pressed, and the text is hidden - a call to a json file is made which should return the
       {(widgname,'para_text'):'new text to place in paragraph', (widgname,'hide'):False} to display the text and
       to set the button to 'button_hide_text'."""

    error_location = (1,0) # set error in para_text

    arg_descriptions = {'para_text':FieldArg("text", "",jsonset=True),
                        'para_class':FieldArg("cssclass", ""),
                        'button_show_text':FieldArg("text", "Show"),
                        'button_hide_text':FieldArg("text", "Hide"),
                        'button_class':FieldArg("cssclass", ""),
                        'json_ident':FieldArg("url", ''),
                        'link_ident':FieldArg("url", 'no_javascript'),
                        'get_field':FieldArg("text", "", valdt=True),
                        'hide':FieldArg("boolean", True, jsonset=True),
                        'pre_line':FieldArg("boolean", True)
                       }

    def __init__(self, name=None, brief='', **field_args):
        """
        para_text: The text appearing in the paragraph
        pre_line: If True, sets style="white-space: pre-line;" into the paragraph which preserves
                  new line breaks
        """
        # pass fields to Widget
        Widget.__init__(self, name=name, tag_name="div", brief=brief, **field_args)
        self[0] = tag.Part(tag_name='a', attribs={'role':'button'})
        self[0][0] = ""  # where button text is to be set
        self[1] = tag.Part(tag_name="p")
        # do not insert <br /> - leave that to pre_line
        self[1].linebreaks=False
        self[1][0] =  ""  # where para_text is to be set
        self._jsonurl = ''


    def _build(self, page, ident_list, environ, call_data, lang):
        if self.get_field_value('button_class'):
             self[0].update_attribs({"class":self.get_field_value('button_class')})
        self[0].update_attribs({"href":"#"})
        if not self.get_field_value("link_ident"):
            # setting self._error replaces the entire tag
            self._error = "Warning: No link ident"
            return
        url = skiboot.get_url(self.get_field_value("link_ident"), proj_ident=page.proj_ident)
        if url:
            get_fields = {self.get_formname("get_field"):self.get_field_value("get_field")}
            url = self.make_get_url(page, url, get_fields, force_ident=True)
            self[0].update_attribs({"href": url})
        else:
            self._error = "Warning: Invalid link ident"
            return

        para_style = {}

        if self.get_field_value("para_class"):
            para_style["class"] = self.get_field_value("para_class")

        if self.get_field_value("hide") and (not self.error_status):
            self[0][0] = self.get_field_value("button_show_text")
            if self.get_field_value("pre_line"):
                para_style["style"] = "display:none;white-space: pre-line;"
            else:
                para_style["style"] = "display:none;"
        else:
            self[0][0] = self.get_field_value("button_hide_text")
            if self.get_field_value("pre_line"):
                para_style["style"] = "white-space: pre-line;"

        if para_style:
            self[1].attribs=para_style

        if not self.error_status:
            # only set para_text if an error is not already there
            self[1][0] = self.get_field_value("para_text")
        if not self.get_field_value("json_ident"):
            # setting self._error replaces the entire tag
            self._error = "Warning: No link ident to JSON"
            return
        self._jsonurl = skiboot.get_url(self.get_field_value("json_ident"),  proj_ident=page.proj_ident)
        if not self._jsonurl:
            # setting self._error replaces the entire tag
            self._error = "Warning: broken link"
            return


    def _build_js(self, page, ident_list, environ, call_data, lang):
        """Sets a click event handler"""
        if not self._jsonurl:
            return
        jscript = """  $("#{ident} a").click(function (e) {{
    SKIPOLE.widgets['{ident}'].eventfunc(e);
    }});
""".format(ident = self.get_id())
        return jscript + self._make_fieldvalues( 'button_show_text', 'button_hide_text', url=self._jsonurl)

    def __str__(self):
        """Returns a text string to illustrate the widget"""
        return """
<div>  <!-- with class widget_class -->
  <a href="#" role="button">  <!-- with class button_class -->
    <!-- set with button_show_text or button_hide_text -->
  </a>
  <p style = "white-space: pre-line;">  <!-- Either hidden or not, depending on hide -->
    <!-- with class para_class, and style set if pre_line is True -->
    <!-- para_text or error message -->
  </p>
</div>"""



class JSONDivLink(Widget):
    """A div, containing an anchor link (used as a button) followed by a div containing text or html content
       If the button is pressed, and the content is visible - the content is hidden, and button text set to 'button_show_text'.
       If the button is pressed, and the content is hidden - a call to a json file is made which should return the
       {(widgname,'div_content'):'new content to place in div', (widgname,'hide'):False} to display the content and
       to set the button to 'button_hide_text'."""

    error_location = (1,0) # set error in div_content

    arg_descriptions = {'div_content':FieldArg("text", "",jsonset=True),
                        'div_class':FieldArg("cssclass", ""),
                        'button_show_text':FieldArg("text", "Show"),
                        'button_hide_text':FieldArg("text", "Hide"),
                        'button_class':FieldArg("cssclass", ""),
                        'json_ident':FieldArg("url", ''),
                        'link_ident':FieldArg("url", 'no_javascript'),
                        'get_field':FieldArg("text", "", valdt=True),
                        'hide':FieldArg("boolean", True, jsonset=True),
                        'htmlescaped':FieldArg("boolean", True)
                       }

    def __init__(self, name=None, brief='', **field_args):
        """
        div_content: The content appearing in the div
        """
        # pass fields to Widget
        Widget.__init__(self, name=name, tag_name="div", brief=brief, **field_args)
        self[0] = tag.Part(tag_name='a', attribs={'role':'button'})
        self[0][0] = ""  # where button text is to be set
        self[1] = tag.Part(tag_name='div')
        self[1][0] =  ""  # where div_content is to be set
        self._jsonurl = ''


    def _build(self, page, ident_list, environ, call_data, lang):
        if self.get_field_value('button_class'):
             self[0].update_attribs({"class":self.get_field_value('button_class')})
        self[0].update_attribs({"href":"#"})
        if self.get_field_value("link_ident"):
            url = skiboot.get_url(self.get_field_value("link_ident"), proj_ident=page.proj_ident)
            if url:
                get_fields = {self.get_formname("get_field"):self.get_field_value("get_field")}
                url = self.make_get_url(page, url, get_fields, force_ident=True)
                self[0].update_attribs({"href": url})

        if self.get_field_value("hide") and (not self.error_status):
            self[1].attribs={"style":"display:none;"}
            self[0][0] = self.get_field_value("button_show_text")
        else:
            self[1].attribs={}
            self[0][0] = self.get_field_value("button_hide_text")
        if self.get_field_value('div_class'):
            self[1].update_attribs({"class":self.get_field_value('div_class')})
        if not self.error_status:
            # only set div_content if an error is not already there
            self[1][0] = self.get_field_value("div_content")
        if not self.get_field_value("htmlescaped"):
            # set the div to not escape its contents
            self[1].htmlescaped = False
        # set an id in the button and div
        self[0].insert_id()
        self[1].insert_id()
        if not self.get_field_value("json_ident"):
            # setting self._error replaces the entire tag
            self._error = "Warning: No link ident to JSON"
            return
        self._jsonurl = skiboot.get_url(self.get_field_value("json_ident"),  proj_ident=page.proj_ident)
        if not self._jsonurl:
            # setting self._error replaces the entire tag
            self._error = "Warning: broken link"
            return


    def _build_js(self, page, ident_list, environ, call_data, lang):
        """Sets a click event handler"""
        jscript = """  $("#{buttonident}").click(function (e) {{
    SKIPOLE.widgets['{ident}'].eventfunc(e);
    }});
""".format(
        ident = self.get_id(),
        buttonident = self[0].get_id(), # ident of the button
        )
        return jscript + self._make_fieldvalues("button_hide_text", "button_show_text", "get_field",
                                                htmlescaped = "text" if self.get_field_value("htmlescaped") else "html",
                                                divident = self[1].get_id(),
                                                buttonident = self[0].get_id(),
                                                url = self._jsonurl
                                                )

    def __str__(self):
        """Returns a text string to illustrate the widget"""
        return """
<div>  <!-- with class widget_class -->
  <a href="#" role="button">  <!-- with class button_class -->
    <!-- set with button_show_text or button_hide_text -->
  </a>
  <div>  <!-- with class div_class, and either hidden or not, depending on hide -->
    <!-- div_content shown as either text or html -->
  </div>
</div>"""


class TextBlockPara(Widget):
    """A paragraph, containing a TextBlock, if a error is raised, then the text is changed
       for the error_message and the error_class given to the paragraph"""

    error_location = 0

    arg_descriptions = {'textblock_ref':FieldArg("textblock_ref", ""),
                        'text_refnotfound':FieldArg("text", ""),
                        'text_replaceblock':FieldArg("text", "" ,jsonset=True),
                        'replace_strings':FieldArgList("text"),
                        'project_ident':FieldArg("text", ""),
                        'linebreaks':FieldArg("boolean", True),
                        'error_class':FieldArg("cssclass", "")
                       }

    def __init__(self, name=None, brief='', **field_args):
        """
        textblock_ref: The reference of the TextBlock appearing in the paragraph
        text_refnotfound: text to appear if the textblock is not found
        text_replaceblock: text set here will replace the textblock
        replace_strings: A list of strings, if given, will be used with python % operator on the text
        project_ident: If empty, the current project database will be used, otherwise a subproject database can be checked
        linebreaks: Set True if linebreaks in the text are to be shown as html breaks
        error_class: The class of the error text - which provides the appearance via CSS
                     replaces widget_class on error.
        """
        # pass fields to Widget
        Widget.__init__(self, name=name, tag_name="p", brief=brief, **field_args)
        self[0] = ''

    def _build(self, page, ident_list, environ, call_data, lang):
        if not self.error_status:
            # define the textblock
            tblock = self.get_field_value("textblock_ref")
            tblock.text = self.get_field_value('text_replaceblock')
            tblock.failmessage = self.get_field_value('text_refnotfound')
            if self.get_field_value('project_ident'):
                tblock.proj_ident = self.get_field_value('project_ident')
            else:
                tblock.proj_ident = page.proj_ident
            tblock.linebreaks = bool(self.get_field_value('linebreaks'))
            if self.get_field_value('replace_strings'):
                tblock.replace_strings = self.get_field_value('replace_strings')
            # place it at location 0
            self[0] = tblock
        if self.error_status and self.get_field_value('error_class'):
            self.update_attribs({"class":self.get_field_value('error_class')})

    def _build_js(self, page, ident_list, environ, call_data, lang):
        """Sets fieldvalues"""
        return self._make_fieldvalues('widget_class','error_class','linebreaks')

    def __str__(self):
        """Returns a text string to illustrate the widget"""
        return """
<p>  <!-- with class widget_class replaced by error_class on failure -->
   <!-- set with either text_replaceblock or textblock content, replaced by error message on error -->
</p>"""


class ShowPara1(Widget):
    """A div, containing a paragraph of text followed by an error div and paragraph.
    The text paragraph is normally visible (depending on the show_para field)
    The error div is invisible, and becomes visible on error."""

    error_location = (1,0,0)

    arg_descriptions = {'para_text':FieldArg("text", default="", valdt=False, jsonset=True),
                        'show_para':FieldArg("boolean", default=True, valdt=False, jsonset=True),
                        'para_class':FieldArg("cssclass", ""),
                        'error_class':FieldArg("cssclass", ""),
                        'pre_line':FieldArg("boolean", True)
                       }

    def __init__(self, name=None, brief='', **field_args):
        """
        para_text: The text appearing in the paragraph
        show_para: True if the paragraph is to be visible, False if not
        para_class: The class of the paragraph - which provides the appearance via CSS
        error_class: The class of the error text - which provides the appearance via CSS
        pre_line: If True, sets style="white-space: pre-line;" into the paragraph which preserves
                  new line breaks
        """
        Widget.__init__(self, name=name, tag_name="div", brief=brief, **field_args)
        # The para_text
        self[0] = tag.Part(tag_name="p")
        # do not insert <br /> - leave that to pre_line
        self[0].linebreaks=False
        self[1] = tag.Part(tag_name="div", attribs={"style":"display:none;"})
        self[1][0] = tag.Part(tag_name="p")
        self[1][0][0] = ''

    def _build(self, page, ident_list, environ, call_data, lang):
        para_style = {}

        if self.get_field_value("para_class"):
            para_style["class"] = self.get_field_value("para_class")

        if self.get_field_value("show_para"):
            if self.get_field_value("pre_line"):
                para_style["style"] = "white-space: pre-line;"
        else:
            if self.get_field_value("pre_line"):
                para_style["style"] = "display:none;white-space: pre-line;"
            else:
                para_style["style"] = "display:none;"

        if para_style:
            self[0].attribs=para_style

        self[0][0] = self.get_field_value("para_text")
        if self.error_status:
            self[1].del_one_attrib("style")
        if self.get_field_value('error_class'):
            self[1].update_attribs({"class":self.get_field_value('error_class')})

    def __str__(self):
        """Returns a text string to illustrate the widget"""
        return """
<div> <!-- with class widget_class -->
  <p style = "white-space: pre-line;">
    <!-- with class para_class, and style set if pre_line is True -->
    <!-- hidden if show_para is False -->
    <!-- set with para_text -->
  </p>
  <div>  <!-- with class error_class, normally hidden, shown on error -->
    <p> <!-- set with error message --> </p>
  </div>
</div>"""


class ShowPara2(Widget):
    """A div, containing an x button which on pressed will hide it, and after the button, another div holding text."""

     # This class does not display any error messages
    display_errors = False

    arg_descriptions = {'para_text':FieldArg("text", default="", valdt=False, jsonset=True),
                        'hide':FieldArg("boolean", False, jsonset=True),
                        'inner_class':FieldArg("cssclass", ""),
                        'close_class':FieldArg("cssclass", ""),
                        'close_style':FieldArg("cssstyle", ""),
                        'pre_line':FieldArg("boolean", True)
                       }

    def __init__(self, name=None, brief='', **field_args):
        """
        pre_line: If True, sets style="white-space: pre-line;" into the paragraph which preserves
                  new line breaks
        """
        # pass fields to Widget
        Widget.__init__(self, name=name, tag_name="div", brief=brief, **field_args)
        self[0] = tag.Part(tag_name='div', attribs={"onclick":"this.parentElement.style.display='none'"})
        self[0][0] = tag.HTMLSymbol("&times;")
        self[1] = tag.Part(tag_name='div')
        self[1][0] = tag.Part(tag_name='p')
        # do not insert <br /> - leave that to pre_line
        self[1][0].linebreaks=False
        self[1][0][0] = ''

    def _build(self, page, ident_list, environ, call_data, lang):
        # Hides widget if no error and hide is True
        self.widget_hide(self.get_field_value("hide"))
        # define the text paragraph
        self[1][0][0] = self.get_field_value("para_text")
        if self.get_field_value("inner_class"):
            self[1].update_attribs({"class":self.get_field_value("inner_class")})
        if self.get_field_value("close_class"):
            self[0].update_attribs({"class":self.get_field_value("close_class")})
        if self.get_field_value("close_style"):
            self[0].update_attribs({"style":self.get_field_value("close_style")})
        if self.get_field_value("pre_line"):
            self[1][0].attribs = {"style":"white-space: pre-line;"}

    def __str__(self):
        """Returns a text string to illustrate the widget"""
        return """
<div>  <!-- with class widget_class -->
  <div onclick="this.parentElement.style.display='none'"> <!-- with class close_class and style close_style -->
    &times;
  </div>
  <div> <!-- with class inner_class -->
    <p style = "white-space: pre-line;"> <!-- style set if pre_line is True -->
      <!-- para_text -->
    </p>
  </div>
</div>"""



