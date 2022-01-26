


"""Contains widgets displaying checkboxes"""

from .. import tag, excepts
from . import Widget, ClosedWidget, FieldArg, FieldArgList, FieldArgTable, FieldArgDict


class CheckBox1(Widget):
    """A div holding a checkbox. Without a form or submit button, typically included within a form"""

    error_location = (0,0,0)

    arg_descriptions = {
                       'checkbox':FieldArg("text", '', valdt=True),
                       'checkbox_class':FieldArg("cssclass", ''),
                       'checkbox_style':FieldArg("cssstyle", ''),
                       'left_label':FieldArg("text", 'Left Label'),
                       'left_class':FieldArg("cssclass", ''),
                       'left_style':FieldArg("cssstyle", ''),
                       'error_class':FieldArg("cssclass", ""),
                       'div_class':FieldArg("cssclass", ""),
                       'div_style':FieldArg("cssstyle", ''),
                       'right_label':FieldArg("text", ''),
                       'right_class':FieldArg("cssclass", ''),
                       'right_style':FieldArg("cssstyle", ''),
                       'checked':FieldArg("boolean", False, jsonset=True)
                       }
    def __init__(self, name=None, brief='', **field_args):
        """
        checkbox: The name of the checkbox, with the value returned
        left_label: The text displayed to the left of the checkbox
        left_class: The css class of the label to the left of the checkbox
        checkbox_class: The css class of the checkbox input field
        right_label: The text displayed to the right of the checkbox
        right_class: The css class of the label to the right of the checkbox
        checked: True if checkbox ticked, False otherwise
        error_class: css class applied to the normally hidden error paragraph
        div_class: css class applied to the div after the error paragraph
        """
        Widget.__init__(self, name=name, brief=brief, **field_args)
        self.tag_name = "div"
        self[0] = tag.Part(tag_name="div", attribs={"style":"display:none;"})
        self[0][0] = tag.Part(tag_name="p")
        self[0][0][0] = ''
        self[1] = tag.Part(tag_name="div")
        self[1][0] = tag.Part(tag_name="label", hide_if_empty=True)
        self[1][1] = tag.ClosedPart(tag_name="input", attribs = {"type":"checkbox"})
        self[1][2] = tag.Part(tag_name="label", hide_if_empty=True)

    def _build(self, page, ident_list, environ, call_data, lang):
        "build the checkbox"
        self[0].set_class_style(self.wf.error_class)
        if self.error_status:
            self[0].del_one_attrib("style")
        self[1].set_class_style(self.wf.div_class, self.wf.div_style)
        if self.wf.left_label:
            self[1][0][0] = self.wf.left_label
        self[1][0].set_class_style(self.wf.left_class, self.wf.left_style)
        if self.wf.checked:
            self[1][1].update_attribs({"name":self.get_formname('checkbox'), "value":self.wf.checkbox, "checked":"checked"})
        else:
            self[1][1].update_attribs({"name":self.get_formname('checkbox'), "value":self.wf.checkbox})
        self[1][1].set_class_style(self.wf.checkbox_class, self.wf.checkbox_style)
        if self.wf.right_label:
            self[1][2][0] = self.wf.right_label
        self[1][2].set_class_style(self.wf.right_class, self.wf.right_style)
        # set an id in the checkbox for the 'label for' tag
        for_id = self[1][1].insert_id()
        # set the label 'for' attribute
        self[1][0].update_attribs({'for':for_id})
        self[1][2].update_attribs({'for':for_id})

    @classmethod
    def description(cls):
        """Returns a text string to illustrate the widget"""
        return """<div>  <!-- with widget id and class widget_class -->
  <div> <!-- normally hidden div, with class error_class -->
    <p> <!-- Any error text appears here --> </p>
  <div>
  <div>  <!-- with class attribute set to div_class if a class is set -->
    <label> <!-- with class set to left_class and content to left_label -->
    </label>
    <input type='checkbox' /> <!-- checked if checked field is True, and value to the checkbox value -->
                              <!-- and class set to checkbox_class -->
    <label> <!-- with class set to right_class and content to right_label -->
    </label>
  </div>
</div>"""



class CheckBox2(Widget):
    """A span holding a checkbox. Without a form or submit button, typically included within a form"""

    # This class does not display any error messages
    display_errors = False


    arg_descriptions = {
                       'checkbox':FieldArg("text", '', valdt=True),
                       'checkbox_class':FieldArg("cssclass", ''),
                       'checkbox_style':FieldArg("cssstyle", ''),
                       'left_label':FieldArg("text", ''),
                       'left_class':FieldArg("cssclass", ''),
                       'left_style':FieldArg("cssstyle", ''),
                       'right_label':FieldArg("text", ''),
                       'right_class':FieldArg("cssclass", ''),
                       'right_style':FieldArg("cssstyle", ''),
                       'checked':FieldArg("boolean", False, jsonset=True)
                       }
    def __init__(self, name=None, brief='', **field_args):
        """
        checkbox: The name of the checkbox, with the value returned
        checkbox_class: The css class of the checkbox input field
        left_label: The text displayed to the left of the checkbox
        left_class: The css class of the label to the left of the checkbox
        right_label: The text displayed to the right of the checkbox
        right_class: The css class of the label to the right of the checkbox
        checked: True if checkbox ticked, False otherwise
        """
        Widget.__init__(self, name=name, brief=brief, **field_args)
        self.tag_name = "span"
        self[0] = tag.Part(tag_name="label", hide_if_empty=True)
        self[1] = tag.ClosedPart(tag_name="input", attribs = {"type":"checkbox"})
        self[2] = tag.Part(tag_name="label", hide_if_empty=True)


    def _build(self, page, ident_list, environ, call_data, lang):
        "build the checkbox"
        if self.wf.left_label:
            self[0][0] = self.wf.left_label
        self[0].set_class_style(self.wf.left_class, self.wf.left_style) 
        if self.wf.checked:
            self[1].update_attribs({"name":self.get_formname('checkbox'), "value":self.wf.checkbox, "checked":"checked"})
        else:
            self[1].update_attribs({"name":self.get_formname('checkbox'), "value":self.wf.checkbox})
        self[1].set_class_style(self.wf.checkbox_class, self.wf.checkbox_style)
        if self.wf.right_label:
            self[2][0] = self.wf.right_label
        self[2].set_class_style(self.wf.right_class, self.wf.right_style)
        # set an id in the checkbox for the 'label for' tag
        for_id = self[1].insert_id()
        # set the label 'for' attribute
        self[0].update_attribs({'for':for_id})
        self[2].update_attribs({'for':for_id})

    @classmethod
    def description(cls):
        """Returns a text string to illustrate the widget"""
        return """<span>  <!-- with widget id and class widget_class -->
  <label> <!-- with class set to left_class and content to left_label -->
  </label>
  <input type='checkbox' /> <!-- checked if checked field is True, and value to the checkbox value -->
                            <!-- and class set to checkbox_class -->
  <label> <!-- with class set to right_class and content to right_label -->
  </label>
</span>"""


class CheckedText(Widget):
    """A div containing a checkbox and text input field. Without a form or submit button, typically included within a form
       The text input field is only enabled when the checkbox is checked
       uses javascript and jquery to enable/disable the text input field"""

    error_location = (0,0,0)

    arg_descriptions = {'checkbox':FieldArg("text", '', valdt=True),
                        'checkbox_class':FieldArg("cssclass", ''),
                        'checked':FieldArg("boolean", False, jsonset=True),
                        'label_text':FieldArg("text", ''),
                        'label_class':FieldArg("cssclass", ''),
                        'label_style':FieldArg("cssstyle", ''),
                        'error_class':FieldArg("cssclass", ""),
                        'input_text':FieldArg("text", '', valdt=True),
                        'input_class':FieldArg("cssclass", ''),
                        'inputdiv_class':FieldArg("cssclass", ''),
                        'inputdiv_style':FieldArg("cssstyle", ''),
                        'size':FieldArg("text", ''),
                        'maxlength':FieldArg("text", '')
                       }
    def __init__(self, name=None, brief='', **field_args):
        """
        checkbox: The name of the checkbox, with the value returned, value normally empty, as the checkbox purpose is only
                  to enable the input_text field, however if a value is given, it is returned if checked
        checkbox_class: The css class of the checkbox input field
        label_text: The text displayed to the left of the checkbox
        label_class: The css class of the label to the left of the checkbox
        checked: True if checkbox ticked, False otherwise
        error_class: css class applied to the normally hidden error paragraph
        input_text: The default text in the text input field, field name used as name attribute
        input_class: The css class of the input text field
        inputdiv_class: the class attribute of the tag which contains the label and inputs
        size: The number of characters appearing in the text input area
        maxlength: The maximum number of characters accepted in the text area
        """
        Widget.__init__(self, name=name, brief=brief, **field_args)
        self.tag_name = "div"
        self[0] = tag.Part(tag_name="div", attribs={"style":"display:none;"})
        self[0][0] = tag.Part(tag_name="p")
        self[0][0][0] = ''
        # div containing label and input fields
        self[1] = tag.Part(tag_name='div')
        self[1][0] = tag.Part(tag_name="label", hide_if_empty=True)
        self[1][1] = tag.ClosedPart(tag_name="input", attribs = {"type":"checkbox"})
        self[1][2] = tag.ClosedPart(tag_name="input", attribs ={"type":"text"})

    def _build(self, page, ident_list, environ, call_data, lang):
        "build the checkbox"
        self[0].set_class_style(self.wf.error_class)
        if self.error_status:
            self[0].del_one_attrib("style")

        # the div holding label, input fields
        self[1].set_class_style(self.wf.inputdiv_class, self.wf.inputdiv_style)

        # the label
        if self.wf.label_text:
            self[1][0][0] = self.wf.label_text
        self[1][0].set_class_style(self.wf.label_class, self.wf.label_style)

        if self.wf.checked:
            self[1][1].update_attribs({"name":self.get_formname('checkbox'), "checked":"checked"})
        else:
            self[1][1].update_attribs({"name":self.get_formname('checkbox')})
            self[1][2].update_attribs({"disabled":"disabled"})
        if self.wf.checkbox:
            self[1][1].update_attribs({"value":self.wf.checkbox})
        self[1][1].set_class_style(self.wf.checkbox_class)

        self[1][2].update_attribs({"name":self.get_formname('input_text'), "value":self.wf.input_text})
        if self.wf.size:
            self[1][2].update_attribs({"size":self.wf.size})
        if self.wf.maxlength:
            self[1][2].update_attribs({"maxlength":self.wf.maxlength})
        self[1][2].set_class_style(self.wf.input_class)

        # set an id in the checkbox for the 'label for' tag
        # and set the label 'for' attribute
        self[1][0].update_attribs({'for':self[1][1].insert_id()})

    def _build_js(self, page, ident_list, environ, call_data, lang):
        """jscript to enable the textbox"""
        return f"""  $('#{self[1][1].get_id()}').change(function() {{
    $('#{self.get_id()} input').last().prop('disabled',!this.checked);
    }});
"""

    @classmethod
    def description(cls):
        """Returns a text string to illustrate the widget"""
        return """<div>  <!-- with widget id and class widget_class -->
  <div> <!-- normally hidden div, with class error_class -->
    <p> <!-- Any error text appears here --> </p>
  </div>
  <div> <!-- class attribute set to inputdiv_class -->
    <label> <!-- with class set to label_class and content to label_text -->
    </label>
    <input type='checkbox' /> <!-- checked if checked field is True, and value to the checkbox value -->
                              <!-- and class set to checkbox_class -->
    <input type=\"text\" /> <!-- class set to input_class and text value set to input_text -->
  </div>
</div>"""


class CheckInputs(Widget):
    """A div holding a checkbox with a container meant to hold further input fields.
       Without a form or submit button, typically included within a form.
       The checkbox controls any text input fields (not other types of input)
       Contained input text fields must be initially set as enabled/disabled to match checkbox
       The contained input fields are only enabled when the checkbox is checked
       uses jquery"""

    _container = ((1,2),)

    error_location = (0,0,0)

    arg_descriptions = {'div_class':FieldArg("cssclass", ''),
                        'checkbox':FieldArg("text", '', valdt=True),
                        'checkbox_class':FieldArg("cssclass", ''),
                        'label_text':FieldArg("text", ''),
                        'label_class':FieldArg("cssclass", ''),
                        'label_style':FieldArg("cssstyle", ''),
                        'container_class':FieldArg("cssclass", ''),
                        'error_class':FieldArg("cssclass", ""),
                        'checked':FieldArg("boolean", False, jsonset=True)
                       }
    def __init__(self, name=None, brief='', **field_args):
        """
        div_class: The class attribute of the inner div holding input fields.
        checkbox: The name of the checkbox, with the value returned, value normally empty, as the checkbox purpose is only
                  to enable the contained fields, however if a value is given, it is returned if checked
        checkbox_class: The css class of the checkbox input field
        label_text: The text displayed to the left of the checkbox
        label_class: The css class of the label to the left of the checkbox
        container_class: the class attribute of the div holding the container
        checked: True if checkbox ticked, False otherwise
        error_class: css class applied to the normally hidden error paragraph
        """
        Widget.__init__(self, name=name, brief=brief, **field_args)
        self.tag_name = "div"
        self[0] = tag.Part(tag_name="div", attribs={"style":"display:none;"})
        self[0][0] = tag.Part(tag_name="p")
        self[0][0][0] = ''
        self[1] = tag.Part(tag_name="div")
        self[1][0] = tag.Part(tag_name="label", hide_if_empty=True)
        self[1][1] = tag.ClosedPart(tag_name="input", attribs = {"type":"checkbox"})
        # The location (1,2) is available as a container
        self[1][2] = tag.Part(tag_name="div")
        self[1][2][0] = ""

    def _build(self, page, ident_list, environ, call_data, lang):
        "build the checkbox"
        self[0].set_class_style(self.wf.error_class)
        if self.error_status:
            self[0].del_one_attrib("style")

        self[1].set_class_style(self.wf.div_class)
        if self.wf.label_text:
            self[1][0][0] = self.wf.label_text
        self[1][0].set_class_style(self.wf.label_class, self.wf.label_style)

        # Create the checkbox
        if self.wf.checked:
            self[1][1].update_attribs({"name":self.get_formname('checkbox'), "checked":"checked"})
        else:
            self[1][1].update_attribs({"name":self.get_formname('checkbox')})
        if self.wf.checkbox:
            self[1][1].update_attribs({"value":self.wf.checkbox})
        self[1][1].set_class_style(self.wf.checkbox_class)

        # the div holding the container
        self[1][2].set_class_style(self.wf.container_class)

        # set an id in the checkbox for the 'label for' tag
        # and set the label 'for' attribute
        self[1][0].update_attribs({'for':self[1][1].insert_id()})


    def _build_js(self, page, ident_list, environ, call_data, lang):
        """jscript to enable the contained input text fields"""
        ident = self.get_id()
        return f"""  $("#{ident} input").first().change(function() {{
    $('#{ident} input[type="text"]').prop('disabled',!this.checked);
    }});
"""

    @classmethod
    def description(cls):
        """Returns a text string to illustrate the widget"""
        return """<div>  <!-- with widget id and class widget_class -->
  <div> <!-- normally hidden div, with class error_class -->
    <p> <!-- Any error text appears here --> </p>
  </div>
  <div>  <!-- with class set to div_class -->
    <label> <!-- with class set to label_class and content to label_text -->
    </label>
    <input type='checkbox' /> <!-- checked if checked field is True, and value to the checkbox value -->
                              <!-- and class set to checkbox_class -->
    <div>
      <!-- container can hold input fields -->
    </div>
  </div>
</div>"""


class SubmitCheckBox1(Widget):
    """Defines a form with a checkbox input field, and four hidden fields"""

    # js_validators is a class attribute, True if javascript validation is enabled
    js_validators=True

    error_location = (0,0,0)

    arg_descriptions = {'label':FieldArg("text", 'Left Label'),
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
                        'inputdiv_class':FieldArg("cssclass", ''),
                        'inputandbutton_class':FieldArg("cssclass", ''),
                        'error_class':FieldArg("cssclass", ''),
                        'hide':FieldArg("boolean", False, jsonset=True),
                        'checkbox':FieldArg("text", '', valdt=True),
                        'checkbox_class':FieldArg("cssclass", ''),
                        'checked':FieldArg("boolean", False, jsonset=True)
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
        inputdiv_class: the class attribute of the div which contains the label, input text and button
        inputandbutton_class: the class attribute of the span which contains the input text and button
        error_class: The class applied to the paragraph containing the error message on error.
        hide: If True, widget is hidden
        checkbox: The name of the checkbox, with the value returned
        checkbox_class: The css class of the checkbox input field
        checked: True if checkbox ticked, False otherwise
        """
        Widget.__init__(self, name=name, brief=brief, **field_args)
        self.tag_name = "div"
        # error div at 0
        self[0] = tag.Part(tag_name="div", attribs={"style":"display:none;"})
        self[0][0] = tag.Part(tag_name="p")
        self[0][0][0] = ''
        # The form
        self[1] = tag.Part(tag_name='form', attribs={"role":"form", "method":"post"})

        # div containing label, input text and button
        self[1][0] = tag.Part(tag_name='div')
        # the label
        self[1][0][0] = tag.Part(tag_name="label", hide_if_empty=True)
        # span containing input text and button
        self[1][0][1] = tag.Part(tag_name='span')
        # the checkbox input field
        self[1][0][1][0] = tag.ClosedPart(tag_name="input", attribs = {"type":"checkbox"})
        # the submit button
        self[1][0][1][1] = tag.Part(tag_name="button", attribs ={"type":"submit"})
        self[1][0][1][1][0] = "Submit"


    def _build(self, page, ident_list, environ, call_data, lang):
        "build the form"
        # Hides widget if no error and hide is True
        self.widget_hide(self.wf.hide)

        # any label:value added to self.jlabels will be set in a javascript fieldvalues attribute for the widget
        if self.wf.action_json:
            self.jlabels['url'] = self.get_url(self.wf.action_json)

        self[0].set_class_style(self.wf.error_class)
        if self.error_status:
            self[0].del_one_attrib("style")
        if not self.wf.action:
            # setting self._error replaces the entire tag
            self._error = "Warning: No form action"
            return
        actionurl = self.get_url(self.wf.action)
        if not actionurl:
            # setting self._error replaces the entire tag
            self._error = "Warning: broken link"
            return
        # update the action of the form
        self[1].update_attribs({"action": actionurl})
        # the div holding label, checkbox and button
        self[1][0].set_class_style(self.wf.inputdiv_class)
        self[1][0][0].set_class_style(self.wf.label_class, self.wf.label_style)
        if self.wf.label:
            self[1][0][0][0] = self.wf.label

        # the span holding input checkbox and button
        self[1][0][1].set_class_style(self.wf.inputandbutton_class)

        # set an id in the input checkbox field for the 'label for' tag
        for_id = self[1][0][1][0].insert_id()

        if self.wf.checked:
            self[1][0][1][0].update_attribs({"name":self.get_formname('checkbox'), "value":self.wf.checkbox, "checked":"checked"})
        else:
            self[1][0][1][0].update_attribs({"name":self.get_formname('checkbox'), "value":self.wf.checkbox})
        self[1][0][1][0].set_class_style(self.wf.checkbox_class)

        # set the label 'for' attribute
        self[1][0][0].update_attribs({'for':for_id})

        # submit button
        self[1][0][1][1].set_class_style(self.wf.button_class)
        if self.wf.button_text:
            self[1][0][1][1][0] = self.wf.button_text

        # add ident and four hidden fields
        self.add_hiddens(self[1], page)


    def _build_js(self, page, ident_list, environ, call_data, lang):
        """Sets a submit event handler"""
        ident = self.get_id()
        return f"""  $("#{ident} form").on("submit input", function(e) {{
    SKIPOLE.widgets["{ident}"].eventfunc(e);
    }});
"""


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
      <label> <!-- with class set to label_class and content to label, for set to input checkbox id -->
      </label>
      <span>  <!-- class attribute set to inputandbutton_class -->
          <input type="checkbox" />  <!-- class set to checkbox_class -->
          <button type="submit"> <!-- with class set to button_class -->
            <!-- button_text -->
          </button>
      </span>
    </div>
    <!-- hidden input fields -->                              
  </form>
</div>"""




class CheckBoxTable1(Widget):
    """A table of three columns, two being text strings, the third checkboxes
       The first row is three header titles. Typically inserted into a form
       does not display errors"""

    display_errors = False


    arg_descriptions = {'header_class':FieldArg("cssclass",""),
                        'title1':FieldArg('text', ''),
                        'title2':FieldArg('text', ''),
                        'title3':FieldArg('text', ''),
                        'row_classes':FieldArgList('text', jsonset=True),
                        'col1':FieldArgList('text', jsonset=True),
                        'col2':FieldArgList('text', jsonset=True),
                        'checkbox_dict':FieldArgDict('text'),                                     # dictionary of keyname:value
                        'checked':FieldArgList("text", valdt=True, jsonset=True, senddict=True)  # the field submitted as a dictionary
                        }                                                                         # each key will have 'keyname'
                                                                                                  # and value will be the values ticked


    def __init__(self, name=None, brief='', **field_args):
        """
        header_class: class of the header row, if empty string, then no class will be applied
        title1: The header title over the first text column
        title2: The header title over the second text column
        title3: The header title over the second text column
        row_classes: A list of CSS classes to apply to each row (not including the header)
        col1: A list of text strings to place in the first column
        col2: A list of text strings to place in the second column
        checkbox_dict: A dictionary of keyname:value, should be Ordered Dict unless python >= 3.6
        checked: a list of keynames which will be checked,  the fields submitted will have name 'widgetname:checked-keyname'
                       and the user will receive a widgfield ('widgetname','checked') containing a dictionary of keyname:values ticked
         """
        Widget.__init__(self, name=name, brief=brief, **field_args)
        self.tag_name = "table"


    def _build(self, page, ident_list, environ, call_data, lang):
        "Build the table"
        checkbox_dict = self.wf.checkbox_dict
        rowc = self.wf.row_classes
        col1 = self.wf.col1
        col2 = self.wf.col2
        checked = self.wf.checked
        if not checked:
            checked = []
        input_name = self.get_formname("checked") + '-'

        header = 0
        if self.wf.title1 or self.wf.title2 or self.wf.title3:
            header = 1
            if self.wf.header_class:
                self[0] = tag.Part(tag_name='tr', attribs={"class":self.wf.header_class})
            else:
                self[0] = tag.Part(tag_name='tr')
            self[0][0] = tag.Part(tag_name='th', text = self.wf.title1)
            self[0][1] = tag.Part(tag_name='th', text = self.wf.title2)
            self[0][2] = tag.Part(tag_name='th', text = self.wf.title3)

        # create rows
        rows = max( len(col1), len(col2), len(checkbox_dict) )
        if not rowc:
            rowc = ['']*rows
        if rows > len(rowc):
            rowc.extend(['']*(rows - len(rowc)))
        if rows > len(col1):
            col1.extend(['']*(rows - len(col1)))
        if rows > len(col2):
            col2.extend(['']*(rows - len(col2)))

        keylist = list(checkbox_dict.keys())
        if rows > len(keylist):
            keylist.extend([None]*(rows - len(keylist)))

        # keylist is a list of the dictionary keys, extended by None keys, if the dictionary is smaller than the number of rows of the table
        
        for index in range(rows):
            rownumber = index+header
            if rowc[index]:
                self[rownumber] = tag.Part(tag_name='tr', attribs={"class":rowc[index]})
            else:
                self[rownumber] = tag.Part(tag_name='tr')
            self[rownumber][0] = tag.Part(tag_name='td', text = col1[index])
            self[rownumber][1] = tag.Part(tag_name='td', text = col2[index])
            self[rownumber][2] = tag.Part(tag_name='td')
            key = keylist[index]
            if key:  # this is the dictionary key
                keyed_name = input_name + key
                self[rownumber][2][0] = tag.ClosedPart(tag_name="input", attribs={"name":keyed_name, "type":"checkbox"})
                if key in checked:
                    self[rownumber][2][0].update_attribs({"value":checkbox_dict[key], "checked":"checked"})
                else:
                    self[rownumber][2][0].update_attribs({"value":checkbox_dict[key]})


    @classmethod
    def description(cls):
        """Returns a text string to illustrate the widget"""
        return """
<table>  <!-- with widget id and class widget_class -->
  <tr> <!-- with header class -->
    <th> <!-- title1 --> </th>
    <th> <!-- title2 --> </th>
    <th> <!-- title3 --> </th>
  </tr>
  <tr> <!-- with class from row_classes -->
    <td> <!-- col1 text string --> </td>
    <td> <!-- col2 text string --> </td>
    <td><input type="checkbox" />  <!-- with names and value derived from 'checkbox_dict' -->
    </td>
  </tr>
  <!-- rows repeated -->
</table>"""



