


"""Contains widgets displaying confirm/cancel messages and buttons"""


from .. import skiboot, tag, excepts
from . import Widget, ClosedWidget, FieldArg, FieldArgList, FieldArgTable, FieldArgDict



class ConfirmBox1(Widget):
    """A div with a paragraph of text and two buttons, each with three optional get fields."""

    # This class does not display any error messages
    display_errors = False

    arg_descriptions = {'hide':FieldArg("boolean", False, jsonset=True),
                        'boxdiv_class':FieldArg("cssclass", ""),
                        'boxdiv_style':FieldArg("cssstyle", ""),
                        'paradiv_class':FieldArg("cssclass", ""),
                        'para_class':FieldArg("cssclass", ""),
                        'buttondiv_class':FieldArg("cssclass", ""),
                        'buttondiv_style':FieldArg("cssstyle", ""),
                        'para_text':FieldArg("text", "", jsonset=True),

                        'button1_class':FieldArg("cssclass", ""),
                        'button1_style':FieldArg("cssstyle", ""),
                        'link_ident1':FieldArg("url", ''),
                        'json_ident1':FieldArg("url", ''),
                        'get_field1_1':FieldArg("text", "", valdt=True, jsonset=True),
                        'get_field1_2':FieldArg("text","", valdt=True, jsonset=True),
                        'get_field1_3':FieldArg("text","", valdt=True, jsonset=True),
                        'button_text1':FieldArg("text", "Cancel"),

                        'button2_class':FieldArg("cssclass", ""),
                        'button2_style':FieldArg("cssstyle", ""),
                        'link_ident2':FieldArg("url", ''),
                        'json_ident2':FieldArg("url", ''),
                        'get_field2_1':FieldArg("text", "", valdt=True, jsonset=True),
                        'get_field2_2':FieldArg("text","", valdt=True, jsonset=True),
                        'get_field2_3':FieldArg("text","", valdt=True, jsonset=True),
                        'button_text2':FieldArg("text", "Confirm")
            }


    def __init__(self, name=None, brief='', **field_args):
        """
        hide: If True, sets display: none; on the widget, can be set/unset via JSON file
              If False, or error sets display:block
        boxdiv_class: class of the box holding paragraph and buttons
        paradiv_class: The class of the div containing the paragraph
        para_class: The class of the paragraph
        buttondiv_class: The class of the div holding the buttons
        json_ident1: The url, ident or label to link by button1, expecting a json file to be returned
        json_ident2: The url, ident or label to link by button2, expecting a json file to be returned
        """
        Widget.__init__(self, name=name, brief=brief, **field_args)
        self.tag_name = "div"
        self[0] = tag.Part(tag_name="div")
        # The location 0,0 is the div containing the paragraph
        self[0][0] = tag.Part(tag_name="div")
        self[0][0][0] = tag.Part(tag_name="p")
        self[0][0][0][0] = ''
        # div holding buttons
        self[0][1] = tag.Part(tag_name="div")
        self[0][1][0] = tag.Part(tag_name="a", attribs={"role":"button"})
        self[0][1][1] = tag.Part(tag_name="a", attribs={"role":"button"})


    def _build(self, page, ident_list, environ, call_data, lang):
        "build the box"
        # Hides widget if no error and hide is True
        self.widget_hide(self.wf.hide)
        if self.wf.boxdiv_class:
            self[0].update_attribs({"class":self.wf.boxdiv_class})
        if self.wf.boxdiv_style:
            self[0].update_attribs({"style":self.wf.boxdiv_style})
        if self.wf.buttondiv_class:
            self[0][1].update_attribs({"class":self.wf.buttondiv_class})
        if self.wf.buttondiv_style:
            self[0][1].update_attribs({'style':self.wf.buttondiv_style})
        if self.wf.paradiv_class:
            self[0][0].update_attribs({"class":self.wf.paradiv_class})
        if self.wf.para_class:
            self[0][0][0].update_attribs({"class":self.wf.para_class})
        if self.wf.para_text:
            self[0][0][0][0] = self.wf.para_text
        # button1
        if self.wf.button1_class:
            self[0][1][0].update_attribs({"class":self.wf.button1_class})
        if self.wf.button1_style:
            self[0][1][0].update_attribs({"style":self.wf.button1_style})

        # any label:value added to self.jlabels will be set in a javascript fieldvalues attribute for the widget
        if self.wf.json_ident1:
            self.jlabels['url1'] = skiboot.get_url(self.wf.json_ident1, proj_ident=page.proj_ident)

        if not self.wf.link_ident1:
            self[0][1][0][0] = "Warning: broken link"
        else:
            url = skiboot.get_url(self.wf.link_ident1, proj_ident=page.proj_ident)
            if not url:
                self[0][1][0][0] = "Warning: broken link"
            else:
                if self.wf.button_text1:
                    self[0][1][0][0] = self.wf.button_text1
                else:
                    self[0][1][0][0] = url
                # create a url for the href
                get_fields = {self.get_formname("get_field1_1"):self.wf.get_field1_1,
                              self.get_formname("get_field1_2"):self.wf.get_field1_2,
                              self.get_formname("get_field1_3"):self.wf.get_field1_3}
                url = self.make_get_url(page, url, get_fields, True)
                self[0][1][0].update_attribs({"href": url})
        # button2
        if self.wf.button2_class:
            self[0][1][1].update_attribs({"class":self.wf.button2_class})
        if self.wf.button2_style:
            self[0][1][1].update_attribs({"style":self.wf.button2_style})

        # any label:value added to self.jlabels will be set in a javascript fieldvalues attribute for the widget
        if self.wf.json_ident2:
            self.jlabels['url2'] = skiboot.get_url(self.wf.json_ident2, proj_ident=page.proj_ident)

        if not self.wf.link_ident2:
            self[0][1][1][0] = "Warning: broken link"
        else:
            url = skiboot.get_url(self.wf.link_ident2, proj_ident=page.proj_ident)
            if not url:
                self[0][1][1][0] = "Warning: broken link"
            else:
                if self.wf.button_text2:
                    self[0][1][1][0] = self.wf.button_text2
                else:
                    self[0][1][1][0] = url
                # create a url for the href
                get_fields = {self.get_formname("get_field2_1"):self.wf.get_field2_1,
                              self.get_formname("get_field2_2"):self.wf.get_field2_2,
                              self.get_formname("get_field2_3"):self.wf.get_field2_3}
                url = self.make_get_url(page, url, get_fields, True)
                self[0][1][1].update_attribs({"href": url})


    def _build_js(self, page, ident_list, environ, call_data, lang):
        """Sets a click event handler"""
        if not (self.jlabels['url1'] or self.jlabels['url2']):
            return
        ident = self.get_id()
        return f"""  $("#{ident} a").click(function (e) {{
    SKIPOLE.widgets['{ident}'].eventfunc(e);
    }});
"""

    @classmethod
    def description(cls):
        """Returns a text string to illustrate the widget"""
        return """
<div> <!-- with widget id and class widget_class -->
  <div> <!-- With boxdiv_class -->
    <div> <!-- With paradiv_class -->
      <p> <!-- With class set by para_class -->
          <!-- para_text shown here -->
      </p>
    </div>
    <div>    <!-- with class set by buttondiv_class and style by buttondiv_style -->
      <a role="button" href="#">
        <!-- With class set by button1_class, and the href link will be the url of the link_ident1 with the three get_fields -->
        <!-- the button will show the button_text1 -->
      </a>
      <a role="button" href="#">
        <!-- With class set by button2_class, and the href link will be the url of the link_ident2 with the three get_fields -->
        <!-- the button will show the button_text2 -->
      </a>
    </div>
  </div>
</div>"""


class ConfirmBox2(Widget):
    """A div - normally used for modal background containing a  div with a paragraph
         of text and two buttons, each with three optional get fields.
         The 'cancel' button1 hides the widget without making a call if javascript is available
         if not, then the link is called."""

    # This class does not display any error messages
    display_errors = False

    arg_descriptions = {'hide':FieldArg("boolean", False, jsonset=True),
                        'boxdiv_class':FieldArg("cssclass", ""),
                        'boxdiv_style':FieldArg("cssstyle", ""),
                        'paradiv_class':FieldArg("cssclass", ""),
                        'para_class':FieldArg("cssclass", ""),
                        'buttondiv_class':FieldArg("cssclass", ""),
                        'buttondiv_style':FieldArg("cssstyle", ""),
                        'para_text':FieldArg("text", "", jsonset=True),

                        'button1_class':FieldArg("cssclass", ""),
                        'button1_style':FieldArg("cssstyle", ""),
                        'link_ident1':FieldArg("url", ''),
                        'get_field1_1':FieldArg("text", "", valdt=True, jsonset=True),
                        'get_field1_2':FieldArg("text","", valdt=True, jsonset=True),
                        'get_field1_3':FieldArg("text","", valdt=True, jsonset=True),
                        'button_text1':FieldArg("text", "Cancel"),

                        'button2_class':FieldArg("cssclass", ""),
                        'button2_style':FieldArg("cssstyle", ""),
                        'link_ident2':FieldArg("url", ''),
                        'get_field2_1':FieldArg("text", "", valdt=True, jsonset=True),
                        'get_field2_2':FieldArg("text","", valdt=True, jsonset=True),
                        'get_field2_3':FieldArg("text","", valdt=True, jsonset=True),
                        'button_text2':FieldArg("text", "Confirm")
            }


    def __init__(self, name=None, brief='', **field_args):
        """
        hide: If True, sets display: none; on the widget, can be set/unset via JSON file
              If False, or error sets display:block
        boxdiv_class: class of the box holding paragraph and buttons
        paradiv_class: The class of the div containing the paragraph
        para_class: The class of the text paragraph
        buttondiv_class: The class of the div holding the buttons
        """
        Widget.__init__(self, name=name, brief=brief, **field_args)
        self.tag_name = "div"
        self[0] = tag.Part(tag_name="div")
        # The location 0,0 is the div containing the paragraph
        self[0][0] = tag.Part(tag_name="div")
        self[0][0][0] = tag.Part(tag_name="p")
        self[0][0][0][0] = ''
        # div holding buttons
        self[0][1] = tag.Part(tag_name="div")
        self[0][1][0] = tag.Part(tag_name="a", attribs={"role":"button"})
        self[0][1][1] = tag.Part(tag_name="a", attribs={"role":"button"})

    def _build(self, page, ident_list, environ, call_data, lang):
        "build the box"
        # Hides widget if no error and hide is True
        self.widget_hide(self.wf.hide)
        if self.wf.boxdiv_class:
            self[0].update_attribs({"class":self.wf.boxdiv_class})
        if self.wf.boxdiv_style:
            self[0].update_attribs({"style":self.wf.boxdiv_style})
        if self.wf.buttondiv_class:
            self[0][1].update_attribs({"class":self.wf.buttondiv_class})
        if self.wf.buttondiv_style:
            self[0][1].update_attribs({'style':self.wf.buttondiv_style})
        if self.wf.paradiv_class:
            self[0][0].update_attribs({"class":self.wf.paradiv_class})
        if self.wf.para_class:
            self[0][0][0].update_attribs({"class":self.wf.para_class})
        if self.wf.para_text:
            self[0][0][0][0] = self.wf.para_text
        # button1
        if self.wf.button1_class:
            self[0][1][0].update_attribs({"class":self.wf.button1_class})
        if self.wf.button1_style:
            self[0][1][0].update_attribs({"style":self.wf.button1_style})
        if not self.wf.link_ident1:
            self[0][1][0][0] = "Warning: broken link"
        else:
            url = skiboot.get_url(self.wf.link_ident1, proj_ident=page.proj_ident)
            if not url:
                self[0][1][0][0] = "Warning: broken link"
            else:
                if self.wf.button_text1:
                    self[0][1][0][0] = self.wf.button_text1
                else:
                    self[0][1][0][0] = url
                # create a url for the href
                get_fields = {self.get_formname("get_field1_1"):self.wf.get_field1_1,
                              self.get_formname("get_field1_2"):self.wf.get_field1_2,
                              self.get_formname("get_field1_3"):self.wf.get_field1_3}
                url = self.make_get_url(page, url, get_fields, True)
                self[0][1][0].update_attribs({"href": url})
        # button2
        if self.wf.button2_class:
            self[0][1][1].update_attribs({"class":self.wf.button2_class})
        if self.wf.button2_style:
            self[0][1][1].update_attribs({"style":self.wf.button2_style})
        if not self.wf.link_ident2:
            self[0][1][1][0] = "Warning: broken link"
        else:
            url = skiboot.get_url(self.wf.link_ident2, proj_ident=page.proj_ident)
            if not url:
                self[0][1][1][0] = "Warning: broken link"
            else:
                if self.wf.button_text2:
                    self[0][1][1][0] = self.wf.button_text2
                else:
                    self[0][1][1][0] = url
                # create a url for the href
                get_fields = {self.get_formname("get_field2_1"):self.wf.get_field2_1,
                              self.get_formname("get_field2_2"):self.wf.get_field2_2,
                              self.get_formname("get_field2_3"):self.wf.get_field2_3}
                url = self.make_get_url(page, url, get_fields, True)
                self[0][1][1].update_attribs({"href": url})


    def _build_js(self, page, ident_list, environ, call_data, lang):
        """Sets a click event handler on the a buttons"""
        ident = self.get_id()
        return f"""  $("#{ident} a").click(function (e) {{
    SKIPOLE.widgets['{ident}'].eventfunc(e);
    }});
"""

    @classmethod
    def description(cls):
        """Returns a text string to illustrate the widget"""
        return """
<div> <!-- with widget id and class widget_class -->
  <div> <!-- With boxdiv_class -->
    <div> <!-- With paradiv_class -->
      <p> <!-- With class set by para_class -->
        <!-- para_text shown here -->
      </p>
    </div>
    <div>    <!-- with class set by buttondiv_class and style by buttondiv_style -->
      <a role="button" href="#">
        <!-- With class set by button1_class, and the href link will be the url of the link_ident1 with the three get_fields -->
        <!-- the button will show the button_text1 -->
      </a>
      <a role="button" href="#">
        <!-- With class set by button2_class, and the href link will be the url of the link_ident2 with the three get_fields -->
        <!-- the button will show the button_text2 -->
      </a>
    </div>
  </div>
</div>"""


class AlertClear1(Widget):
    """A div - normally used for modal background containing a div with a paragraph
         of text or error message and an X button with three optional get fields.
         The 'clear' button hides the widget without making a call if javascript is available
         if not, then the link is called."""

    error_location = (0,1,0,0)

    arg_descriptions = {'hide':FieldArg("boolean", True, jsonset=True),
                        'para_text':FieldArg("text", "", jsonset=True),
                        'pre_line':FieldArg("boolean", True),
                        'boxdiv_class':FieldArg("cssclass", ""),
                        'boxdiv_style':FieldArg("cssstyle", ""),
                        'error_class':FieldArg("cssclass", ""),
                        'inner_class':FieldArg("cssclass", ""),
                        'inner_style':FieldArg("cssstyle", ""),
                        'buttondiv_class':FieldArg("cssclass", ""),
                        'buttondiv_style':FieldArg("cssstyle", ""),
                        'button_class':FieldArg("cssclass", ""),
                        'link_ident':FieldArg("url", ''),
                        'get_field1':FieldArg("text", "", valdt=True, jsonset=True),
                        'get_field2':FieldArg("text","", valdt=True, jsonset=True),
                        'get_field3':FieldArg("text","", valdt=True, jsonset=True)
            }


    def __init__(self, name=None, brief='', **field_args):
        """
        hide: If True, sets display: none; on the widget, can be set/unset via JSON file
              If False, or error sets display:block
        para_text: The text appearing in the paragraph, replaced on error by error message
        pre_line: If True, sets style="white-space: pre-line;" into the paragraph which preserves
                  new line breaks
        boxdiv_class: class of the box holding paragraph and button
        inner_class: The CSS class of the div holding the paragraph, replaced by error_class on error
        error_class: The CSS class of the div holding the paragraph when error raised
        buttondiv_class: The class of the div holding the button
        """
        Widget.__init__(self, name=name, brief=brief, **field_args)
        self.tag_name = "div"
        self[0] = tag.Part(tag_name="div")
        # div holding X button
        self[0][0] = tag.Part(tag_name="div")
        self[0][0][0] = tag.Part(tag_name="a", attribs={"role":"button"})
        self[0][0][0][0] = tag.HTMLSymbol("&times;")
        # The location 0,1 is the div holding the text paragraph
        self[0][1] = tag.Part(tag_name="div")
        self[0][1][0] = tag.Part(tag_name="p")
        # do not set any linebreaks, leave that to pre-line
        self[0][1][0].linebreaks = False
        self[0][1][0][0] = ''


    def _build(self, page, ident_list, environ, call_data, lang):
        "build the box"
        # Hides widget if no error and hide is True
        self.widget_hide(self.wf.hide)
        if self.wf.boxdiv_class:
            self[0].update_attribs({"class":self.wf.boxdiv_class})
        if self.wf.boxdiv_style:
            self[0].update_attribs({"style":self.wf.boxdiv_style})
        # buttondiv
        if self.wf.buttondiv_class:
            self[0][0].update_attribs({"class":self.wf.buttondiv_class})
        if self.wf.buttondiv_style:
            self[0][0].update_attribs({'style':self.wf.buttondiv_style})
        # inner div
        if self.error_status and self.wf.error_class:
            self[0][1].update_attribs({"class":self.wf.error_class})
        elif self.wf.inner_class:
            self[0][1].update_attribs({"class":self.wf.inner_class})
        if self.wf.inner_style:
            self[0][1].update_attribs({'style':self.wf.inner_style})

        # insert an id for setting the error class
        # any label:value added to self.jlabels will be set in a javascript fieldvalues attribute for the widget
        self.jlabels['inner_id'] = self[0][1].insert_id()
        self.jlabels['inner_class'] = self.wf.inner_class
        self.jlabels['error_class'] = self.wf.error_class

        # paragraph
        if self.wf.pre_line:
            self[0][1][0].attribs={"style":"white-space: pre-line;"}
        if not self.error_status:
            self[0][1][0][0] = self.wf.para_text
        # button
        if self.wf.button_class:
            self[0][0][0].update_attribs({"class":self.wf.button_class})
        if not self.wf.link_ident:
            self[0][1][0][0] = "Warning: broken link"
        else:
            url = skiboot.get_url(self.wf.link_ident, proj_ident=page.proj_ident)
            if url:
                # create a url for the href
                get_fields = {self.get_formname("get_field1"):self.wf.get_field1,
                              self.get_formname("get_field2"):self.wf.get_field2,
                              self.get_formname("get_field3"):self.wf.get_field3}
                url = self.make_get_url(page, url, get_fields, True)
                self[0][0][0].update_attribs({"href": url})
            else:
                self[0][1][0][0] = "Warning: broken link"


    def _build_js(self, page, ident_list, environ, call_data, lang):
        """Sets a click event handler on the a button"""
        ident = self.get_id()
        return f"""  $("#{ident} a").click(function (e) {{
    SKIPOLE.widgets['{ident}'].eventfunc(e);
    }});
"""

    @classmethod
    def description(cls):
        """Returns a text string to illustrate the widget"""
        return """
<div> <!-- with widget id and class widget_class -->
  <div> <!-- With boxdiv_class -->
    <div>    <!-- with class set by buttondiv_class and style by buttondiv_style -->
      <a role="button" href="#">
        <!-- With class set by button_class, and the href link will be the url of the link_ident with the three get_fields -->
        <!-- the button will show the &times; symbol -->
      </a>
    </div>
    <div> <!-- With class set by inner_class, replaced by error_class on error-->
      <p style = "white-space: pre-line;"> <!-- style set if pre_line is True -->
        <!-- para_text or error message appears in this paragraph -->
      </p>
    </div>
  </div>
</div>"""


class AlertClear2(Widget):
    """A div - normally used for modal background containing a div with a paragraph
         of text or error message and an X button with three optional get fields.
         The 'clear' button hides the widget and makes a call requesting a JSON page,
         if a JSON link is not set, then the html link is called."""

    error_location = (0,1,0,0)

    arg_descriptions = {'hide':FieldArg("boolean", True, jsonset=True),
                        'para_text':FieldArg("text", "", jsonset=True),
                        'pre_line':FieldArg("boolean", True),
                        'boxdiv_class':FieldArg("cssclass", ""),
                        'boxdiv_style':FieldArg("cssstyle", ""),
                        'error_class':FieldArg("cssclass", ""),
                        'inner_class':FieldArg("cssclass", ""),
                        'inner_style':FieldArg("cssstyle", ""),
                        'buttondiv_class':FieldArg("cssclass", ""),
                        'buttondiv_style':FieldArg("cssstyle", ""),
                        'button_class':FieldArg("cssclass", ""),
                        'link_ident':FieldArg("url", ''),
                        'json_ident':FieldArg("url", ''),
                        'get_field1':FieldArg("text", "", valdt=True, jsonset=True),
                        'get_field2':FieldArg("text","", valdt=True, jsonset=True),
                        'get_field3':FieldArg("text","", valdt=True, jsonset=True)
            }


    def __init__(self, name=None, brief='', **field_args):
        """
        hide: If True, sets display: none; on the widget, can be set/unset via JSON file
              If False, or error sets display:block
        para_text: The text appearing in the paragraph, replaced on error by error message
        pre_line: If True, sets style="white-space: pre-line;" into the paragraph which preserves
                  new line breaks
        boxdiv_class: class of the box holding paragraph and button
        inner_class: The CSS class of the div holding the paragraph, replaced by error_class on error
        error_class: The CSS class of the div holding the paragraph when error raised
        buttondiv_class: The class of the div holding the button
        json_ident: The url, ident or label to link by the X button, expecting a json file to be returned
        """
        Widget.__init__(self, name=name, brief=brief, **field_args)
        self.tag_name = "div"
        self[0] = tag.Part(tag_name="div")
        # div holding X button
        self[0][0] = tag.Part(tag_name="div")
        self[0][0][0] = tag.Part(tag_name="a", attribs={"role":"button"})
        self[0][0][0][0] = tag.HTMLSymbol("&times;")
        # The location 0,1 is the div holding the text paragraph
        self[0][1] = tag.Part(tag_name="div")
        self[0][1][0] = tag.Part(tag_name="p")
        # do not set any linebreaks, leave that to pre-line
        self[0][1][0].linebreaks = False
        self[0][1][0][0] = ''


    def _build(self, page, ident_list, environ, call_data, lang):
        "build the box"
        # Hides widget if no error and hide is True
        self.widget_hide(self.wf.hide)
        if self.wf.boxdiv_class:
            self[0].update_attribs({"class":self.wf.boxdiv_class})
        if self.wf.boxdiv_style:
            self[0].update_attribs({"style":self.wf.boxdiv_style})
        # buttondiv
        if self.wf.buttondiv_class:
            self[0][0].update_attribs({"class":self.wf.buttondiv_class})
        if self.wf.buttondiv_style:
            self[0][0].update_attribs({'style':self.wf.buttondiv_style})
        # inner div
        if self.error_status and self.wf.error_class:
            self[0][1].update_attribs({"class":self.wf.error_class})
        elif self.wf.inner_class:
            self[0][1].update_attribs({"class":self.wf.inner_class})
        if self.wf.inner_style:
            self[0][1].update_attribs({'style':self.wf.inner_style})
        # insert an id for setting the error class
        self[0][1].insert_id()

        # insert an id for setting the error class
        # any label:value added to self.jlabels will be set in a javascript fieldvalues attribute for the widget
        self.jlabels['inner_id'] = self[0][1].insert_id()
        self.jlabels['inner_class'] = self.wf.inner_class
        self.jlabels['error_class'] = self.wf.error_class

        # paragraph
        if self.wf.pre_line:
            self[0][1][0].attribs={"style":"white-space: pre-line;"}
        if not self.error_status:
            self[0][1][0][0] = self.wf.para_text
        # button
        if self.wf.button_class:
            self[0][0][0].update_attribs({"class":self.wf.button_class})

        if self.wf.json_ident:
            self.jlabels['url'] = skiboot.get_url(self.wf.json_ident, proj_ident=page.proj_ident)

        if not self.wf.link_ident:
            self[0][1][0][0] = "Warning: broken link"
        else:
            url = skiboot.get_url(self.wf.link_ident, proj_ident=page.proj_ident)
            if url:
                # create a url for the href
                get_fields = {self.get_formname("get_field1"):self.wf.get_field1,
                              self.get_formname("get_field2"):self.wf.get_field2,
                              self.get_formname("get_field3"):self.wf.get_field3}
                url = self.make_get_url(page, url, get_fields, True)
                self[0][0][0].update_attribs({"href": url})
            else:
                self[0][1][0][0] = "Warning: broken link"


    def _build_js(self, page, ident_list, environ, call_data, lang):
        """Sets a click event handler on the a button"""
        ident = self.get_id()
        return f"""  $("#{ident} a").click(function (e) {{
    SKIPOLE.widgets['{ident}'].eventfunc(e);
    }});
"""

    @classmethod
    def description(cls):
        """Returns a text string to illustrate the widget"""
        return """
<div> <!-- with widget id and class widget_class -->
  <div> <!-- With boxdiv_class -->
    <div>    <!-- with class set by buttondiv_class and style by buttondiv_style -->
      <a role="button" href="#">
        <!-- With class set by button_class, and the href link will be the url of the link_ident with the three get_fields -->
        <!-- If json_ident is set, then the call will be made to this ident instead, and a JSON file is expected -->
        <!-- the button will show the &times; symbol -->
      </a>
    </div>
    <div> <!-- With class set by inner_class, replaced by error_class on error-->
      <p style = "white-space: pre-line;"> <!-- style set if pre_line is True -->
        <!-- para_text or error message appears in this paragraph -->
      </p>
    </div>
  </div>
</div>"""


