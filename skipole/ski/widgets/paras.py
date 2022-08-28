
"""Contains commonly used paragraphs"""


from .. import tag
from . import Widget, ClosedWidget, AnchorClickEventMixin, FieldArg, FieldArgList, FieldArgTable, FieldArgDict


class TagBlock(Widget):

    # This class does not display any error messages
    display_errors = False

    arg_descriptions = {'tag':FieldArg("text", 'div'),
                        'hide':FieldArg("boolean", False, jsonset=True),
                        'drag':FieldArg("text", '', valdt=True, jsonset=True),
                        'drop':FieldArg("text", '', valdt=True, jsonset=True),
                        'dropident':FieldArg("url", "")}

    _container = ((),)

    def __init__(self, name=None, brief='', **field_args):
        """Acts as a widget, containing other widgets, so show, class and hide can be set
           drag - if given this is text data sent with a JSON call when this item is dropped
                  if nothing set here, this item will not be set as draggable.
           drop - if given this is text data sent with a JSON call when another item is dropped here
                  if nothing set here, this item will not be set as droppable.
           dropident - ident or label of target which returns a JSON page, called when a drop occurs here

        """
        Widget.__init__(self, name=name, brief=brief, **field_args)
        self.tag_name = "div"
        # container is the widget itself
        self[0] =  ""

    def _build(self, page, ident_list, environ, call_data, lang):
        self.tag_name = self.wf.tag
        # Hides widget if no error and hide is True
        self.widget_hide(self.wf.hide)

        # any label:value added to self.jlabels will be set in a javascript fieldvalues attribute for the widget
        dropurl = self.get_url(self.wf.dropident)
        if dropurl:
            self.jlabels['dropurl'] = dropurl

        # drag
        drag = self.wf.drag
        if drag:
            self.attribs.update(
{"draggable":"true",
"ondragstart":f"SKIPOLE.widgets['{self.get_id()}'].dragstartfunc(event, '{drag}')"})
        # drop
        drop = self.wf.drop
        if drop:
            self.attribs.update(
{"ondrop":f"SKIPOLE.widgets['{self.get_id()}'].dropfunc(event, '{drop}')",
"ondragover":f"SKIPOLE.widgets['{self.get_id()}'].allowdropfunc(event)"})


    @classmethod
    def description(cls):
        """Returns a text string to illustrate the widget"""
        return """
<div>  <!-- with widget id and class widget_class, and with div tag, or any other specified -->
       <!-- attribute style=display:none if hide is True, with drag and drop events if enabled -->
  <!-- further html and widgets can be contained here -->
</div>"""


class DivStyleDiv(Widget):

    # This class does not display any error messages
    display_errors = False

    arg_descriptions = {
                        'inner_tag':FieldArg("text", 'div'),
                        'style':FieldArg("cssstyle", ''),
                        'set_html':FieldArg("text", "", jsonset=True)}

    def __init__(self, name=None, brief='', **field_args):
        """A div, containing a div which can have a style set, containing unescaped html
            inner_tag - the tag of the inside element
           style - the style of the inside element"""
        Widget.__init__(self, name=name, brief=brief, **field_args)
        self.tag_name = "div"
        self[0] = tag.Part(tag_name='div')
        self[0].htmlescaped = False
        self[0].linebreaks=False
        self[0][0] =  ""  # where html is to be set

    def _build(self, page, ident_list, environ, call_data, lang):
        self[0].tag_name = self.wf.inner_tag
        if self.wf.style:
            self[0].attribs["style"] = self.wf.style
        self[0][0] = self.wf.set_html

    @classmethod
    def description(cls):
        """Returns a text string to illustrate the widget"""
        return """
<div>  <!-- with widget id and class widget_class -->
  <div>  <!-- with div tag, or any other specified and the set style -->
    <!-- set with unescaped html -->
  </div>
</div>"""


class DivHTML(Widget):

    # This class does not display any error messages
    display_errors = False

    arg_descriptions = {'set_html':FieldArg("text", "", jsonset=True),
                        'hide':FieldArg("boolean", False, jsonset=True),
                        'drag':FieldArg("text", '', valdt=True, jsonset=True),
                        'drop':FieldArg("text", '', valdt=True, jsonset=True),
                        'dropident':FieldArg("url", "")}

    def __init__(self, name=None, brief='', **field_args):
        """A div, containing a string, which will be set as html, without escaping
           drag - if given this is text data sent with a JSON call when this item is dropped
                  if nothing set here, this item will not be set as draggable.
           drop - if given this is text data sent with a JSON call when another item is dropped here
                  if nothing set here, this item will not be set as droppable.
           dropident - ident or label of target which returns a JSON page, called when a drop occurs here"""

        Widget.__init__(self, name=name, brief=brief, **field_args)
        self.tag_name = "div"
        self[0] = ""  # where the html string is to be set
        self.htmlescaped = False
        self.linebreaks=False

    def _build(self, page, ident_list, environ, call_data, lang):
        self[0] = self.wf.set_html
        # Hides widget if no error and hide is True
        self.widget_hide(self.wf.hide)
        # dropurl
        # any label:value added to self.jlabels will be set in a javascript fieldvalues attribute for the widget
        dropurl = self.get_url(self.wf.dropident)
        if dropurl:
            self.jlabels['dropurl'] = dropurl

        # drag
        drag = self.wf.drag
        if drag:
            self.attribs.update(
{"draggable":"true",
"ondragstart":f"SKIPOLE.widgets['{self.get_id()}'].dragstartfunc(event, '{drag}')"})
        # drop
        drop = self.wf.drop
        if drop:
            self.attribs.update(
{"ondrop":f"SKIPOLE.widgets['{self.get_id()}'].dropfunc(event, '{drop}')",
"ondragover":f"SKIPOLE.widgets['{self.get_id()}'].allowdropfunc(event)"})

    @classmethod
    def description(cls):
        """Returns a text string to illustrate the widget"""
        return """
<div>  <!-- with widget id and class widget_class -->
       <!-- attribute style=display:none if hide is True, with drag and drop events if enabled -->
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
        Widget.__init__(self, name=name, brief=brief, **field_args)
        self.tag_name = "pre"
        self[0] = ''

    def _build(self, page, ident_list, environ, call_data, lang):
        self[0] = self.wf.pre_text

    @classmethod
    def description(cls):
        """Returns a text string to illustrate the widget"""
        return """
<pre>  <!-- with widget id and class widget_class -->
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
        Widget.__init__(self, name=name, brief=brief, **field_args)
        self.tag_name = "span"
        self[0] = ''

    def _build(self, page, ident_list, environ, call_data, lang):
        self[0] = self.wf.span_text

    @classmethod
    def description(cls):
        """Returns a text string to illustrate the widget"""
        return """
<span>  <!-- with widget id and class widget_class -->
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
        Widget.__init__(self, name=name, brief=brief, **field_args)
        self.tag_name = "div"
        self[0] = ''

    def _build(self, page, ident_list, environ, call_data, lang):
        self.tag_name = self.wf.tag
        # Hides widget if no error and hide is True
        self.widget_hide(self.wf.hide)
        self[0] = self.wf.tag_text

    @classmethod
    def description(cls):
        """Returns a text string to illustrate the widget"""
        return """
<div>  <!-- with widget id and class widget_class and with div tag, or any other specified -->
               <!-- and attribute style=display:none if hide is True -->
    <!-- set with text -->
</div>"""


class TagUnEscaped(Widget):
    """A tag, which can be specified, containing unescaped content"""

     # This class does not display any error messages
    display_errors = False

    arg_descriptions = {'tag':FieldArg("text", 'div'),
                        'content':FieldArg("text", "", jsonset=True)}

    def __init__(self, name=None, brief='', **field_args):
        """
        content: The content appearing in the tag
        """
        # pass fields to Widget
        Widget.__init__(self, name=name, brief=brief, **field_args)
        self.tag_name = "div"
        self[0] = ''
        self.htmlescaped = False
        self.linebreaks=False

    def _build(self, page, ident_list, environ, call_data, lang):
        self.tag_name = self.wf.tag
        self[0] = self.wf.content

    @classmethod
    def description(cls):
        """Returns a text string to illustrate the widget"""
        return """
<div>  <!-- with widget id and class widget_class and with div tag, or any other specified -->
    <!-- set with content -->
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
        Widget.__init__(self, name=name, brief=brief, **field_args)
        self.tag_name = "p"
        self[0] = ''

    def _build(self, page, ident_list, environ, call_data, lang):
        self[0] = self.wf.para_text

    @classmethod
    def description(cls):
        """Returns a text string to illustrate the widget"""
        return """
<p>  <!-- with widget id and class widget_class -->
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
        Widget.__init__(self, name=name, brief=brief, **field_args)
        self.tag_name = "div"
        self[0] = tag.Part(tag_name='p')
        # do not insert <br /> - leave that to pre_line
        self[0].linebreaks=False
        self[0][0] = ''

    def _build(self, page, ident_list, environ, call_data, lang):
        if self.wf.pre_line:
            self[0].attribs["style"] = "white-space: pre-line;"
        if self.wf.para_class:
            self[0].attribs["class"] = self.wf.para_class
        # self[0][0] could be set by an error message
        if not self.error_status:
            self[0][0] = self.wf.para_text
        if self.error_status and self.wf.error_class:
            self[0].attribs["class"] = self.wf.error_class

        # any label:value added to self.jlabels will be set in a javascript fieldvalues attribute for the widget
        self.jlabels['para_class'] = self.wf.para_class
        self.jlabels['error_class'] = self.wf.error_class


    @classmethod
    def description(cls):
        """Returns a text string to illustrate the widget"""
        return """
<div>  <!-- with widget id and class widget_class -->
    <p style = "white-space: pre-line;">
    <!-- with class para_class, and style set if pre_line is True -->
    <!-- and class changed to error_class on error -->
        <!-- set with para_text, replaced by error message on error -->
    </p>
</div>"""


class JSONTextLink(AnchorClickEventMixin, Widget):
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
        Widget.__init__(self, name=name, brief=brief, **field_args)
        self.tag_name = "div"
        self[0] = tag.Part(tag_name='a', attribs={'role':'button', 'href':'#'})
        self[0][0] = ""  # where button text is to be set
        self[1] = tag.Part(tag_name="p")
        # do not insert <br /> - leave that to pre_line
        self[1].linebreaks=False
        self[1][0] =  ""  # where para_text is to be set


    def _build(self, page, ident_list, environ, call_data, lang):
        if self.wf.button_class:
             self[0].attribs["class"] = self.wf.button_class
        if not self.wf.link_ident:
            # setting self._error replaces the entire tag
            self._error = "Warning: No link ident"
            return
        url = self.get_url(self.wf.link_ident)
        if url:
            get_fields = {self.get_formname("get_field"):self.wf.get_field}
            self[0].attribs["href"] = self.make_get_url(page, url, get_fields, force_ident=True)
        else:
            self._error = "Warning: Invalid link ident"
            return
 
        if self.wf.para_class:
            self[1].attribs["class"] = self.wf.para_class

        if self.wf.hide and (not self.error_status):
            self[0][0] = self.wf.button_show_text
            if self.wf.pre_line:
                self[1].attribs["style"] = "display:none;white-space: pre-line;"
            else:
                self[1].attribs["style"] = "display:none;"
        else:
            self[0][0] = self.wf.button_hide_text
            if self.wf.pre_line:
                self[1].attribs["style"] = "white-space: pre-line;"

        if not self.error_status:
            # only set para_text if an error is not already there
            self[1][0] = self.wf.para_text
        if not self.self.wf.json_ident:
            # setting self._error replaces the entire tag
            self._error = "Warning: No link ident to JSON"
            return

        # any label:value added to self.jlabels will be set in a javascript fieldvalues attribute for the widget
        self.jlabels['button_show_text'] = self.wf.button_show_text
        self.jlabels['button_hide_text'] = self.wf.button_hide_text

        jsonurl = self.get_url(self.wf.json_ident)
        if not jsonurl:
            # setting self._error replaces the entire tag
            self._error = "Warning: broken link"
            return
        self.jlabels['url'] = jsonurl


    @classmethod
    def description(cls):
        """Returns a text string to illustrate the widget"""
        return """
<div>  <!-- with widget id and class widget_class -->
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
                        'button_style':FieldArg("cssstyle", ""),
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
        Widget.__init__(self, name=name, brief=brief, **field_args)
        self.tag_name = "div"
        self[0] = tag.Part(tag_name='a', attribs={'role':'button', 'href':'#'})
        self[0][0] = ""  # where button text is to be set
        self[1] = tag.Part(tag_name='div')
        self[1][0] =  ""  # where div_content is to be set

    def _build(self, page, ident_list, environ, call_data, lang):
        if self.wf.button_class:
             self[0].attribs["class"] = self.wf.button_class
        if self.wf.button_style:
             self[0].attribs["style"] = self.wf.button_style
        if self.wf.link_ident:
            url = self.get_url(self.wf.link_ident)
            if url:
                get_fields = {self.get_formname("get_field"):self.wf.get_field}
                self[0].attribs["href"] = self.make_get_url(page, url, get_fields, force_ident=True)

        if self.wf.hide and (not self.error_status):
            self[1].attribs["style"] = "display:none;"
            self[0][0] = self.wf.button_show_text
        else:
            self[0][0] = self.wf.button_hide_text
        if self.wf.div_class:
            self[1].attribs["class"] = self.wf.div_class
        if not self.error_status:
            # only set div_content if an error is not already there
            self[1][0] = self.wf.div_content
        if not self.wf.htmlescaped:
            # set the div to not escape its contents
            self[1].htmlescaped = False
        # set an id in the button and div
        # any label:value added to self.jlabels will be set in a javascript fieldvalues attribute for the widget
        self.jlabels['buttonident'] = self[0].insert_id()
        self.jlabels['divident'] = self[1].insert_id()

        self.jlabels['button_show_text'] = self.wf.button_show_text
        self.jlabels['button_hide_text'] = self.wf.button_hide_text
        self.jlabels['get_field'] = self.wf.get_field

        self.jlabels['htmlescaped'] = "text" if self.wf.htmlescaped else "html"

        if not self.wf.json_ident:
            # setting self._error replaces the entire tag
            self._error = "Warning: No link ident to JSON"
            return
        jsonurl = self.get_url(self.wf.json_ident)
        if not jsonurl:
            # setting self._error replaces the entire tag
            self._error = "Warning: broken link"
            return
        self.jlabels['url'] = jsonurl


    def _build_js(self, page, ident_list, environ, call_data, lang):
        """Sets a click event handler on the button"""
        ident = self.get_id()
        buttonident = self[0].get_id() # ident of the button
        return f"""  $("#{buttonident}").click(function (e) {{
    SKIPOLE.widgets['{ident}'].eventfunc(e);
    }});
"""


    @classmethod
    def description(cls):
        """Returns a text string to illustrate the widget"""
        return """
<div>  <!-- with widget id and class widget_class -->
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
                        'textblock_project':FieldArg("text", ""),
                        'text_refnotfound':FieldArg("text", ""),
                        'text_replaceblock':FieldArg("text", "" ,jsonset=True),
                        'replace_strings':FieldArgList("text"),
                        'linebreaks':FieldArg("boolean", True),
                        'error_class':FieldArg("cssclass", "")
                       }

    def __init__(self, name=None, brief='', **field_args):
        """
        textblock_ref: The reference of the TextBlock appearing in the paragraph
        textblock_project: Set with a project name if the TextBlock is defined in a sub project
        text_refnotfound: text to appear if the textblock is not found
        text_replaceblock: text set here will replace the textblock
        replace_strings: A list of strings, if given, will be used with python % operator on the textblock text (not on text_replaceblock)
        linebreaks: Set True if linebreaks in the text are to be shown as html breaks
        error_class: The class of the error text - which provides the appearance via CSS
                     replaces widget_class on error.
        """
        # pass fields to Widget
        Widget.__init__(self, name=name, brief=brief, **field_args)
        self.tag_name = "p"
        self[0] = ''

    def _build(self, page, ident_list, environ, call_data, lang):
        if not self.error_status:
            linebreaks = bool(self.wf.linebreaks)
            if self.wf.text_replaceblock:
                # no textblock, just the replacement text
                self[0] = self.wf.text_replaceblock
                if not linebreaks:
                    self.linebreaks = False             
            else:
                # define the textblock
                tblock = self.wf.textblock_ref
                tblock.project = self.wf.textblock_project
                tblock.failmessage = self.wf.text_refnotfound
                tblock.linebreaks = linebreaks
                if self.wf.replace_strings:
                    tblock.replace_strings = self.wf.replace_strings
                # place it at location 0
                self[0] = tblock
        if self.error_status and self.wf.error_class:
            self.attribs["class"] = self.wf.error_class

        # any label:value added to self.jlabels will be set in a javascript fieldvalues attribute for the widget
        self.jlabels['widget_class'] = self.wf.widget_class
        self.jlabels['error_class'] = self.wf.error_class
        self.jlabels['linebreaks'] = self.wf.linebreaks


    @classmethod
    def description(cls):
        """Returns a text string to illustrate the widget"""
        return """
<p>  <!-- with widget id, and class widget_class replaced by error_class on failure -->
   <!-- set with either text_replaceblock or textblock content, replaced by error message on error -->
</p>"""



class TextBlockDiv(Widget):
    """A div, containing a TextBlock. The TextBlock is not escaped, so may contain
       html which is set directly into the div"""

    # This class does not display any error messages
    display_errors = False


    arg_descriptions = {'textblock_ref':FieldArg("textblock_ref", ""),
                        'textblock_project':FieldArg("text", ""),
                        'content_refnotfound':FieldArg("text", ""),
                        'content_replaceblock':FieldArg("text", "" ,jsonset=True)
                       }

    def __init__(self, name=None, brief='', **field_args):
        """
        textblock_ref: The reference of the TextBlock appearing in the div
        textblock_project: Set with a project name if the TextBlock is defined in a sub project
        content_refnotfound: content to appear if the textblock is not found
        content_replaceblock: content set here will replace the textblock
        """
        # pass fields to Widget
        Widget.__init__(self, name=name, brief=brief, **field_args)
        self.tag_name = "div"
        self[0] = ''
        self.htmlescaped = False
        self.linebreaks = False

    def _build(self, page, ident_list, environ, call_data, lang):
        # define the textblock
        tblock = self.wf.textblock_ref
        tblock.project = self.wf.textblock_project
        tblock.failmessage = self.wf.content_refnotfound
        tblock.escape = False
        tblock.linebreaks = False
        # place it at location 0
        if self.wf.content_replaceblock:
            self[0] = self.wf.content_replaceblock
        else:
            self[0] = tblock

    @classmethod
    def description(cls):
        """Returns a text string to illustrate the widget"""
        return """
<div>  <!-- with widget id, and class widget_class -->
   <!-- set with either content_replaceblock or textblock content as unescaped html -->
</div>"""


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
        Widget.__init__(self, name=name, brief=brief, **field_args)
        self.tag_name = "div"
        # The para_text
        self[0] = tag.Part(tag_name="p")
        # do not insert <br /> - leave that to pre_line
        self[0].linebreaks=False
        self[1] = tag.Part(tag_name="div", attribs={"style":"display:none;"})
        self[1][0] = tag.Part(tag_name="p")
        self[1][0][0] = ''

    def _build(self, page, ident_list, environ, call_data, lang):

        if self.wf.para_class:
            self[0].attribs["class"] = self.wf.para_class

        if self.wf.show_para:
            if self.wf.pre_line:
                self[0].attribs["style"] = "white-space: pre-line;"
        else:
            if self.wf.pre_line:
                self[0].attribs["style"] = "display:none;white-space: pre-line;"
            else:
                self[0].attribs["style"] = "display:none;"

        self[0][0] = self.wf.para_text
        if self.error_status:
            del self[1].attribs["style"]
        if self.wf.error_class:
            self[1].attribs["class"] = self.wf.error_class

    @classmethod
    def description(cls):
        """Returns a text string to illustrate the widget"""
        return """
<div> <!-- with widget id and class widget_class -->
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
        Widget.__init__(self, name=name, brief=brief, **field_args)
        self.tag_name = "div"
        self[0] = tag.Part(tag_name='div', attribs={"onclick":"this.parentElement.style.display='none'"})
        self[0][0] = tag.HTMLSymbol("&times;")
        self[1] = tag.Part(tag_name='div')
        self[1][0] = tag.Part(tag_name='p')
        # do not insert <br /> - leave that to pre_line
        self[1][0].linebreaks=False
        self[1][0][0] = ''

    def _build(self, page, ident_list, environ, call_data, lang):
        # Hides widget if no error and hide is True
        self.widget_hide(self.wf.hide)
        # define the text paragraph
        self[1][0][0] = self.wf.para_text
        if self.wf.inner_class:
            self[1].attribs["class"] = self.wf.inner_class
        if self.wf.close_class:
            self[0].attribs["class"] = self.wf.close_class
        if self.wf.close_style:
            self[0].attribs["style"] = self.wf.close_style
        if self.wf.pre_line:
            self[1][0].attribs["style"] = "white-space: pre-line;"

    @classmethod
    def description(cls):
        """Returns a text string to illustrate the widget"""
        return """
<div>  <!-- with widget id and class widget_class -->
  <div onclick="this.parentElement.style.display='none'"> <!-- with class close_class and style close_style -->
    &times;
  </div>
  <div> <!-- with class inner_class -->
    <p style = "white-space: pre-line;"> <!-- style set if pre_line is True -->
      <!-- para_text -->
    </p>
  </div>
</div>"""



