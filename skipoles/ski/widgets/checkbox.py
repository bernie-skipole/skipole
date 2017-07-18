####### SKIPOLE WEB FRAMEWORK #######
#
# checkbox.py  - widgets displaying checkboxes
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


"""Contains widgets displaying checkboxes"""

from .. import skiboot, tag, excepts
from . import Widget, ClosedWidget, FieldArg, FieldArgList, FieldArgTable, FieldArgDict


class CheckBox1(Widget):
    """A div holding a checkbox. Without a form or submit button, typically included within a form"""

    error_location = (0,0,0)

    arg_descriptions = {
                       'checkbox':FieldArg("text", '', valdt=True),
                       'checkbox_class':FieldArg("cssclass", ''),
                       'left_label':FieldArg("text", ''),
                       'left_class':FieldArg("cssclass", ''),
                       'error_class':FieldArg("cssclass", ""),
                       'div_class':FieldArg("cssclass", ""),
                       'right_label':FieldArg("text", ''),
                       'right_class':FieldArg("cssclass", ''),
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
        Widget.__init__(self, name=name, tag_name="div", brief=brief, **field_args)
        self[0] = tag.Part(tag_name="div", attribs={"style":"display:none;"})
        self[0][0] = tag.Part(tag_name="p")
        self[0][0][0] = ''
        self[1] = tag.Part(tag_name="div")
        self[1][0] = tag.Part(tag_name="label", hide_if_empty=True)
        self[1][1] = tag.ClosedPart(tag_name="input", attribs = {"type":"checkbox"})
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
        if self.get_field_value('checked'):
            self[1][1].update_attribs({"name":self.get_formname('checkbox'), "value":self.get_field_value('checkbox'), "checked":"checked"})
        else:
            self[1][1].update_attribs({"name":self.get_formname('checkbox'), "value":self.get_field_value('checkbox')})
        if self.get_field_value('checkbox_class'):
            self[1][1].update_attribs({"class": self.get_field_value('checkbox_class')})
        if self.get_field_value('right_label'):
            self[1][2][0] = self.get_field_value('right_label')
        if self.get_field_value('right_class'):
            self[1][2].attribs = {"class": self.get_field_value('right_class')}
        # set an id in the checkbox for the 'label for' tag
        self[1][1].insert_id()
        # set the label 'for' attribute
        self[1][0].update_attribs({'for':self[1][1].get_id()})
        self[1][2].update_attribs({'for':self[1][1].get_id()})

    def __str__(self):
        """Returns a text string to illustrate the widget"""
        return """<div>  <!-- with class attribute set to widget_class if a class is set -->
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
                       'left_label':FieldArg("text", ''),
                       'left_class':FieldArg("cssclass", ''),
                       'right_label':FieldArg("text", ''),
                       'right_class':FieldArg("cssclass", ''),
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
        Widget.__init__(self, name=name, tag_name="span", brief=brief, **field_args)
        self[0] = tag.Part(tag_name="label", hide_if_empty=True)
        self[1] = tag.ClosedPart(tag_name="input", attribs = {"type":"checkbox"})
        self[2] = tag.Part(tag_name="label", hide_if_empty=True)


    def _build(self, page, ident_list, environ, call_data, lang):
        "build the checkbox"
        if self.get_field_value('left_label'):
            self[0][0] = self.get_field_value('left_label')
        if self.get_field_value('left_class'):
            self[0].attribs = {"class": self.get_field_value('left_class')}
        if self.get_field_value('checked'):
            self[1].update_attribs({"name":self.get_formname('checkbox'), "value":self.get_field_value('checkbox'), "checked":"checked"})
        else:
            self[1].update_attribs({"name":self.get_formname('checkbox'), "value":self.get_field_value('checkbox')})
        if self.get_field_value('checkbox_class'):
            self[1].update_attribs({"class": self.get_field_value('checkbox_class')})
        if self.get_field_value('right_label'):
            self[2][0] = self.get_field_value('right_label')
        if self.get_field_value('right_class'):
            self[2].attribs = {"class": self.get_field_value('right_class')}
        # set an id in the checkbox for the 'label for' tag
        self[1].insert_id()
        # set the label 'for' attribute
        self[0].update_attribs({'for':self[1].get_id()})
        self[2].update_attribs({'for':self[1].get_id()})

    def __str__(self):
        """Returns a text string to illustrate the widget"""
        return """<span>  <!-- with class attribute set to widget_class if a class is set -->
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
                        'error_class':FieldArg("cssclass", ""),
                        'input_text':FieldArg("text", '', valdt=True),
                        'input_class':FieldArg("cssclass", ''),
                        'inputdiv_class':FieldArg("cssclass", ''),
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
        Widget.__init__(self, name=name, tag_name="div", brief=brief, **field_args)
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
        if self.get_field_value('error_class'):
            self[0].update_attribs({"class":self.get_field_value('error_class')})
        if self.error_status:
            self[0].del_one_attrib("style")

        # the div holding label, input fields
        if self.get_field_value('inputdiv_class'):
            self[1].attribs = {"class": self.get_field_value('inputdiv_class')}


        if self.get_field_value('label_text'):
            self[1][0][0] = self.get_field_value('label_text')
        if self.get_field_value('label_class'):
            self[1][0].attribs = {"class": self.get_field_value('label_class')}
        if self.get_field_value('checked'):
            self[1][1].update_attribs({"name":self.get_formname('checkbox'), "checked":"checked"})
        else:
            self[1][1].update_attribs({"name":self.get_formname('checkbox')})
            self[1][2].update_attribs({"disabled":"disabled"})
        if self.get_field_value('checkbox'):
            self[1][1].update_attribs({"value":self.get_field_value('checkbox')})
        if self.get_field_value('checkbox_class'):
            self[1][1].update_attribs({"class": self.get_field_value('checkbox_class')})
        self[1][2].update_attribs({"name":self.get_formname('input_text'), "value":self.get_field_value('input_text')})
        if self.get_field_value('size'):
            self[1][2].update_attribs({"size":self.get_field_value('size')})
        if self.get_field_value('maxlength'):
            self[1][2].update_attribs({"maxlength":self.get_field_value('maxlength')})
        if self.get_field_value('input_class'):
            self[1][2].update_attribs({"class":self.get_field_value('input_class')})

        # set an id in the checkbox for the 'label for' tag
        self[1][1].insert_id()
        # set the label 'for' attribute
        self[1][0].update_attribs({'for':self[1][1].get_id()})

    def _build_js(self, page, ident_list, environ, call_data, lang):
        """jscript to enable the textbox"""
        jscript = """  $('#{checkident}').change(function() {{
    $('#{ident} input').last().prop('disabled',!this.checked);
    }});
""".format(checkident=self[1][1].get_id(), ident=self.get_id())
        return jscript

    def __str__(self):
        """Returns a text string to illustrate the widget"""
        return """<div>  <!-- with class attribute set to widget_class if a class is set -->
  <div> <!-- normally hidden div, with class error_class -->
    <p> <!-- Any error text appears here --> </p>
  </div>
  <div> <!-- class attribute set to inputdiv_class -->
    <label> <!-- with class set to label_class and content to label_text -->
    </label>
    <input type='checkbox' /> <!-- checked if checked field is True, and value to the checkbox value -->
                              <!-- and class set to checkbox_class -->
    <input type=\"text\" /> <!-- input text value set to input_text -->
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
                        'label_class':FieldArg("text", ''),
                        'error_class':FieldArg("cssclass", ""),
                        'checked':FieldArg("boolean", False, jsonset=True)
                       }
    def __init__(self, name=None, brief='', **field_args):
        """
        div_class: The class attribute of the div
        checkbox: The name of the checkbox, with the value returned, value normally empty, as the checkbox purpose is only
                  to enable the contained fields, however if a value is given, it is returned if checked
        checkbox_class: The css class of the checkbox input field
        label_text: The text displayed to the left of the checkbox
        label_class: The css class of the label to the left of the checkbox
        checked: True if checkbox ticked, False otherwise
        error_class: css class applied to the normally hidden error paragraph
        """
        Widget.__init__(self, name=name, tag_name="div", brief=brief, **field_args)
        self[0] = tag.Part(tag_name="div", attribs={"style":"display:none;"})
        self[0][0] = tag.Part(tag_name="p")
        self[0][0][0] = ''
        self[1] = tag.Part(tag_name="div")
        self[1][0] = tag.Part(tag_name="label", hide_if_empty=True)
        self[1][1] = tag.ClosedPart(tag_name="input", attribs = {"type":"checkbox"})
        self[1][2] = ""  # where items can be contained

    def _build(self, page, ident_list, environ, call_data, lang):
        "build the checkbox"
        if self.get_field_value('error_class'):
            self[0].update_attribs({"class":self.get_field_value('error_class')})
        if self.error_status:
            self[0].del_one_attrib("style")
        if self.get_field_value('div_class'):
            self[1].attribs = {"class": self.get_field_value('div_class')}
        if self.get_field_value('label_text'):
            self[1][0][0] = self.get_field_value('label_text')
        if self.get_field_value('label_class'):
            self[1][0].attribs = {"class": self.get_field_value('label_class')}
        # Create the checkbox
        if self.get_field_value('checked'):
            self[1][1].update_attribs({"name":self.get_formname('checkbox'), "checked":"checked"})
        else:
            self[1][1].update_attribs({"name":self.get_formname('checkbox')})
        if self.get_field_value('checkbox'):
            self[1][1].update_attribs({"value":self.get_field_value('checkbox')})
        if self.get_field_value('checkbox_class'):
            self[1][1].update_attribs({"class": self.get_field_value('checkbox_class')})
        # set an id in the checkbox for the 'label for' tag
        self[1][1].insert_id()
        # set the label 'for' attribute
        self[1][0].update_attribs({'for':self[1][1].get_id()})


    def _build_js(self, page, ident_list, environ, call_data, lang):
        """jscript to enable the contained input text fields"""
        jscript = """  $("#{ident} input").first().change(function() {{
    $('#{ident} input[type="text"]').prop('disabled',!this.checked);
    }});
""".format(ident=self.get_id())
        return jscript

    def __str__(self):
        """Returns a text string to illustrate the widget"""
        return """<div>  <!-- with class attribute set to widget_class if a class is set -->
  <div> <!-- normally hidden div, with class error_class -->
    <p> <!-- Any error text appears here --> </p>
  </div>
  <div>
    <label> <!-- with class set to label_class and content to label_text -->
    </label>
    <input type='checkbox' /> <!-- checked if checked field is True, and value to the checkbox value -->
                              <!-- and class set to checkbox_class -->
    <!-- container can hold input fields -->
  </div>
</div>"""

