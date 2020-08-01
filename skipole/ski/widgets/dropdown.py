

"""Contains widgets for dropdown forms"""


from .. import skiboot, tag, excepts
from . import Widget, ClosedWidget, FieldArg, FieldArgList, FieldArgTable, FieldArgDict



class DropDown1(Widget):
    """A div holding a drop down input field. Without a form or submit button, typically included within a form"""

    error_location = (0,0,0)

    arg_descriptions = {
                       'selectvalue':FieldArg("text", '', valdt=True),
                       'left_label':FieldArg("text", 'Choose:'),
                       'left_class':FieldArg("cssclass", ''),
                       'left_style':FieldArg("cssstyle", ''),
                       'error_class':FieldArg("cssclass", ""),
                       'select_class':FieldArg("cssclass", ""),
                       'select_style':FieldArg("cssstyle", ""),
                       'div_class':FieldArg("cssclass", ""),
                       'right_label':FieldArg("text", ''),
                       'right_class':FieldArg("cssclass", ''),
                       'right_style':FieldArg("cssstyle", ''),
                       'option_list':FieldArgList("text")
                       }
    def __init__(self, name=None, brief='', **field_args):
        """
        selectvalue: The option selected, field name is used as the widgfield attribute
        left_label: The text displayed to the left of the dropdown
        left_class: The css class of the label to the left of the dropdown
        right_label: The text displayed to the right of the dropdown
        right_class: The css class of the label to the right of the dropdown
        select_class: The css class of the select tag
        option_list: A list of options
        error_class: css class applied to the normally hidden error paragraph
        div_class: css class applied to the div after the error paragraph
        """
        Widget.__init__(self, name=name, tag_name="div", brief=brief, **field_args)
        self[0] = tag.Part(tag_name="div", attribs={"style":"display:none;"})
        self[0][0] = tag.Part(tag_name="p")
        self[0][0][0] = ''
        self[1] = tag.Part(tag_name="div")
        self[1][0] = tag.Part(tag_name="label", hide_if_empty=True)
        # the drop down input form
        self[1][1] = tag.Part(tag_name="select")
        self[1][2] = tag.Part(tag_name="label", hide_if_empty=True)

    def _build(self, page, ident_list, environ, call_data, lang):
        "build the checkbox"
        if self.get_field_value('error_class'):
            self[0].update_attribs({"class":self.get_field_value('error_class')})
        if self.error_status:
            self[0].del_one_attrib("style")
        if self.get_field_value('div_class'):
            self[1].update_attribs({"class":self.get_field_value('div_class')})
        if self.get_field_value('left_label'):
            self[1][0][0] = self.get_field_value('left_label')
        if self.get_field_value('left_class'):
            self[1][0].attribs = {"class": self.get_field_value('left_class')}
        if self.get_field_value('left_style'):
            self[1][0].attribs = {"style": self.get_field_value('left_style')}
        if self.get_field_value('select_class'):
            self[1][1].attribs = {"class": self.get_field_value('select_class')}
        if self.get_field_value('select_style'):
            self[1][1].attribs = {"style": self.get_field_value('select_style')}
        self[1][1].update_attribs({"name":self.get_formname('selectvalue')})
        selected_option = self.get_field_value('selectvalue')
        for index, opt in enumerate(self.get_field_value('option_list')):
            if selected_option == opt:
                self[1][1][index] = tag.Part(tag_name="option", text=opt, attribs ={"selected":"selected"})
            else:
                self[1][1][index] = tag.Part(tag_name="option", text=opt)
        if self.get_field_value('right_label'):
            self[1][2][0] = self.get_field_value('right_label')
        if self.get_field_value('right_class'):
            self[1][2].attribs = {"class": self.get_field_value('right_class')}
        if self.get_field_value('right_style'):
            self[1][2].attribs = {"style": self.get_field_value('right_style')}
        # set an id in the select for the 'label for' tag
        self[1][1].insert_id()
        # set the label 'for' attribute
        self[1][0].update_attribs({'for':self[1][1].get_id()})
        self[1][2].update_attribs({'for':self[1][1].get_id()})

    @classmethod
    def description(cls):
        """Returns a text string to illustrate the widget"""
        return """
<div>  <!-- with widget id and class widget_class -->
  <div> <!-- normally hidden div, with class error_class -->
    <p> <!-- Any error text appears here --> </p>
  </div>
  <div>  <!-- with class attribute set to div_class if a class is set -->
    <label> <!-- with class set to left_class and content to left_label -->
    </label>
    <select> <!-- with class set to select_class -->
     <option> <!-- with multiple options -->
     </option>
    </select>
    <label> <!-- with class set to right_class and content to right_label -->
    </label>
  </div>
</div>"""


class SubmitDropDown1(Widget):
    """Defines a form with a drop down input field, and four hidden fields"""

    error_location = (0,0,0)

    arg_descriptions = {'label':FieldArg("text", 'Choose:'),
                        'label_class':FieldArg("cssclass", ''),
                        'label_style':FieldArg("cssstyle", ''),
                        'action_json':FieldArg("url", ''),
                        'action':FieldArg("url", ''),
                        'hidden_field1':FieldArg("text", '', valdt=True, jsonset=True),
                        'hidden_field2':FieldArg("text", '', valdt=True, jsonset=True),
                        'hidden_field3':FieldArg("text", '', valdt=True, jsonset=True),
                        'hidden_field4':FieldArg("text", '', valdt=True, jsonset=True),
                        'button_text':FieldArg("text",'Submit'),
                        'button_class':FieldArg("cssclass", ''),
                        'error_class':FieldArg("cssclass", ''),
                        'inputdiv_class':FieldArg("cssclass", ""),
                        'select_class':FieldArg("cssclass", ""),
                        'select_style':FieldArg("cssstyle", ""),
                        'selectvalue':FieldArg("text", '', valdt=True),
                        'option_list':FieldArgList("text"),
                        'hide':FieldArg("boolean", False, jsonset=True),
                       'disabled':FieldArg("boolean", False),
                       }

    def __init__(self, name=None, brief='', **field_args):
        """
        label: The text displayed to the left of the text input field
        label_class: The css class of the label
        action_json:  if a value set, and client has jscript enabled, this is the page ident, label, url this button links to, expects a json page back
        action: The page ident, label, url this button links to, overridden if action_json is set.
        hidden_field1: A hidden field value, leave blank if unused, name used as the get field name
        hidden_field2: A second hidden field value, leave blank if unused, name used as the get field name
        hidden_field3: A third hidden field value, leave blank if unused, name used as the get field name
        hidden_field4: A fourth hidden field value, leave blank if unused, name used as the get field name
        button_text: The text on the button
        button_class: The class given to the button tag
        inputdiv_class: class of the div holding label, dropdown and button
        select_class: The css class of the select tag
        selectvalue: The option selected, field name is used as the widgfield attribute
        option_list: A list of options
        error_class: The class applied to the paragraph containing the error message on error.
        hide: If True, widget is hidden
        disabled: Set True if the select field and submit button are to be disabled
        """
        Widget.__init__(self, name=name, tag_name="div", brief=brief, **field_args)
        # error para at 0
        self[0] = tag.Part(tag_name="div", attribs={"style":"display:none;"})
        self[0][0] = tag.Part(tag_name="p")
        self[0][0][0] = ''

        # The form
        self[1] = tag.Part(tag_name='form', attribs={"role":"form", "method":"post"})

        # div containing label, input text and button
        self[1][0] = tag.Part(tag_name='div')
        # the label
        self[1][0][0] = tag.Part(tag_name="label", hide_if_empty=True)
        # the drop down input field
        self[1][0][1] = tag.Part(tag_name="select")
        # the submit button
        self[1][0][2] = tag.Part(tag_name="button", attribs ={"type":"submit"})
        self[1][0][2][0] = "Submit"
        self._jsonurl = ''


    def _build(self, page, ident_list, environ, call_data, lang):
        "build the form"
        # Hides widget if no error and hide is True
        self.widget_hide(self.get_field_value("hide"))
        self._jsonurl = skiboot.get_url(self.get_field_value("action_json"), proj_ident=page.proj_ident)
        if self.get_field_value('error_class'):
            self[0].update_attribs({"class":self.get_field_value('error_class')})
        if self.error_status:
            self[0].del_one_attrib("style")
        if not self.get_field_value("action"):
            # setting self._error replaces the entire tag
            self._error = "Warning: No form action"
            return
        actionurl = skiboot.get_url(self.get_field_value("action"),  proj_ident=page.proj_ident)
        if not actionurl:
            # setting self._error replaces the entire tag
            self._error = "Warning: broken link"
            return
        # update the action of the form
        self[1].update_attribs({"action": actionurl})
        # the div holding label, dropdown and button
        if self.get_field_value('inputdiv_class'):
            self[1][0].attribs = {"class": self.get_field_value('inputdiv_class')}
        if self.get_field_value('label'):
            self[1][0][0][0] = self.get_field_value('label')
        if self.get_field_value('label_class'):
            self[1][0][0].attribs = {"class": self.get_field_value('label_class')}
        if self.get_field_value('label_style'):
            self[1][0][0].attribs = {"style": self.get_field_value('label_style')}
        if self.get_field_value('select_class'):
            self[1][0][1].attribs = {"class": self.get_field_value('select_class')}
        if self.get_field_value('select_style'):
            self[1][0][1].attribs = {"style": self.get_field_value('select_style')}
        self[1][0][1].update_attribs({"name":self.get_formname('selectvalue')})

        if self.get_field_value('disabled'):
            self[1][0][1].update_attribs({"disabled":"disabled"})

        # set an id in the input field for the 'label for' tag
        self[1][0][1].insert_id()

        selected_option = self.get_field_value('selectvalue')
        for index, opt in enumerate(self.get_field_value('option_list')):
            if selected_option == opt:
                self[1][0][1][index] = tag.Part(tag_name="option", text=opt, attribs ={"selected":"selected"})
            else:
                self[1][0][1][index] = tag.Part(tag_name="option", text=opt)

        # set the label 'for' attribute
        self[1][0][0].update_attribs({'for':self[1][0][1].get_id()})

        # submit button
        if self.get_field_value('button_text'):
            self[1][0][2][0] = self.get_field_value('button_text')
        if self.get_field_value('button_class'):
            self[1][0][2].update_attribs({"class": self.get_field_value('button_class')})
        if self.get_field_value('disabled'):
            self[1][0][2].update_attribs({"disabled":"disabled"})

        # add ident and four hidden fields
        self.add_hiddens(self[1], page)


    def _build_js(self, page, ident_list, environ, call_data, lang):
        """Sets a submit event handler"""
        jscript = """  $('#{ident}').on("submit", function(e) {{
    SKIPOLE.widgets['{ident}'].eventfunc(e);
    }});
""".format(ident=self.get_id())
        if self._jsonurl:
            return jscript + self._make_fieldvalues(url=self._jsonurl)
        return jscript


    @classmethod
    def description(cls):
        """Returns a text string to illustrate the widget"""
        return """
<div> <!-- with widget id and class widget_class -->
  <div>  <!-- div hidden when no error is displayed, with class set to error_class on error -->
    <p> <!-- error message appears in this paragraph --> </p>
  </div>
  <form role="form" method="post"> <!-- action attribute set to action field -->
    <div> <!-- class attribute set to inputdiv_class -->
      <label> <!-- with class set to label_class and content to label -->
      </label>
      <select> <!-- with class set to select_class -->
       <option> <!-- with multiple options -->
       </option>
      </select>
      <button type="submit"> <!-- with class set to button_class -->
        <!-- button_text -->
      </button>
    </div>
    <!-- hidden input fields -->                              
  </form>
</div>"""


class HiddenContainer(Widget):
    """A div - normally used for modal background containing a div with a container
       and an X button with three optional get fields.
       The 'clear' button hides the widget without making a call if javascript is available
       if not, then the link is called."""

    _container = ((0,1),)

    # This class does not display any error messages
    display_errors = False

    arg_descriptions = {'hide':FieldArg("boolean", True, jsonset=True),
                        'boxdiv_class':FieldArg("cssclass", ""),
                        'boxdiv_style':FieldArg("cssstyle", ""),
                        'inner_class':FieldArg("cssclass", ""),
                        'inner_style':FieldArg("cssstyle", ""),
                        'buttondiv_class':FieldArg("cssclass", ""),
                        'buttondiv_style':FieldArg("cssstyle", ""),
                        'button_class':FieldArg("cssclass", ""),
                        'link_ident':FieldArg("url", 'no_javascript'),
                        'get_field1':FieldArg("text", "", valdt=True, jsonset=True),
                        'get_field2':FieldArg("text","", valdt=True, jsonset=True),
                        'get_field3':FieldArg("text","", valdt=True, jsonset=True)
            }


    def __init__(self, name=None, brief='', **field_args):
        """
        hide: If True, sets display: none; on the widget, can be set/unset via JSON file
              If False, or error sets display:block
        boxdiv_class: class of the box holding container and button
        inner_class: The CSS class of the div holding the paragraph
        buttondiv_class: The class of the div holding the button
        """
        Widget.__init__(self, name=name, tag_name="div", brief=brief, **field_args)
        self[0] = tag.Part(tag_name="div")
        # div holding X button
        self[0][0] = tag.Part(tag_name="div")
        self[0][0][0] = tag.Part(tag_name="a", attribs={"role":"button"})
        self[0][0][0][0] = tag.HTMLSymbol("&times;")
        # The location 0,1 is the div holding the container
        self[0][1] = tag.Part(tag_name="div")
        self[0][1][0] = ''


    def _build(self, page, ident_list, environ, call_data, lang):
        "build the box"
        # Hides widget if no error and hide is True
        self.widget_hide(self.get_field_value("hide"))
        if self.get_field_value("boxdiv_class"):
            self[0].update_attribs({"class":self.get_field_value('boxdiv_class')})
        if self.get_field_value('boxdiv_style'):
            self[0].update_attribs({"style":self.get_field_value('boxdiv_style')})
        # buttondiv
        if self.get_field_value("buttondiv_class"):
            self[0][0].update_attribs({"class":self.get_field_value('buttondiv_class')})
        if self.get_field_value("buttondiv_style"):
            self[0][0].update_attribs({'style':self.get_field_value("buttondiv_style")})
        # inner div
        if self.get_field_value("inner_class"):
            self[0][1].update_attribs({"class":self.get_field_value('inner_class')})
        if self.get_field_value("inner_style"):
            self[0][1].update_attribs({'style':self.get_field_value("inner_style")})
        # button
        if self.get_field_value('button_class'):
            self[0][0][0].update_attribs({"class":self.get_field_value('button_class')})
        if not self.get_field_value("link_ident"):
            self[0][0][0][0] = "Warning: broken link"
        else:
            url = skiboot.get_url(self.get_field_value("link_ident"), proj_ident=page.proj_ident)
            if url:
                # create a url for the href
                get_fields = {self.get_formname("get_field1"):self.get_field_value("get_field1"),
                              self.get_formname("get_field2"):self.get_field_value("get_field2"),
                              self.get_formname("get_field3"):self.get_field_value("get_field3")}
                url = self.make_get_url(page, url, get_fields, True)
                self[0][0][0].update_attribs({"href": url})
            else:
                self[0][0][0][0] = "Warning: broken link"


    def _build_js(self, page, ident_list, environ, call_data, lang):
        """Sets a click event handler on the a button"""
        return """  $("#{ident} a").first().click(function (e) {{
    SKIPOLE.widgets['{ident}'].eventfunc(e);
    }});
""".format(ident = self.get_id())


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
    <div> <!-- With class set by inner_class-->
         <!-- container 0 for further elements -->
    </div>
  </div>
</div>"""


