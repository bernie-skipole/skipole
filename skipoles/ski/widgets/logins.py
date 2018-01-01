####### SKIPOLE WEB FRAMEWORK #######
#
# logins.py  - widgets displaying login forms
#
# This file is part of the Skipole web framework
#
# Date : 20161014
#
# Author : Bernard Czenkusz
# Email  : bernie@skipole.co.uk
#
#
#   Copyright 2016 Bernard Czenkusz
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


"""Contains widgets for logging in to a service"""


from .. import skiboot, tag, excepts
from . import Widget, ClosedWidget, FieldArg, FieldArgList, FieldArgTable, FieldArgDict


class Pin4(Widget):
    """Defines a form containing four single character input fields."""


    _container = ((0,1,0),)

    error_location = (0,0,0,0)

    # js_validators is a class attribute, True if javascript validation is enabled
    js_validators=True

    arg_descriptions = {
                        'hide':FieldArg("boolean", False, jsonset=True),
                        'action':FieldArg("url", ''),
                        'hidden_field1':FieldArg("text", '', valdt=True),
                        'hidden_field2':FieldArg("text", '', valdt=True),
                        'hidden_field3':FieldArg("text", '', valdt=True),
                        'hidden_field4':FieldArg("text", '', valdt=True),
                        'button_text':FieldArg("text", 'Submit'),
                        'pin1':FieldArg("boolean", True, valdt=True),
                        'pin2':FieldArg("boolean", True, valdt=True),
                        'pin3':FieldArg("boolean", True, valdt=True),
                        'pin4':FieldArg("boolean", True, valdt=True),
                        'inner_div_class':FieldArg("cssclass", ''),
                        'char_div_class':FieldArg("cssclass", ''),
                        'char_div_style':FieldArg("cssstyle", ''),
                        'butt_div_class':FieldArg("cssclass", ''),
                        'button_class':FieldArg("cssclass", ''),
                        'error_class':FieldArg("cssclass", ""),
                        'left_label':FieldArg("text", ''),
                        'left_class':FieldArg("cssclass", ''),
                        'right_label':FieldArg("text", ''),
                        'right_class':FieldArg("cssclass", ''),
                       }


    def __init__(self, name=None, brief='', **field_args):
        """
        action: The page ident this button links to
        hidden_field1: A hidden field value, leave blank if unused, name used as the get field name
        hidden_field2: A second hidden field value, leave blank if unused, name used as the get field name
        hidden_field3: A third hidden field value, leave blank if unused, name used as the get field name
        hidden_field4: A fourth hidden field value, leave blank if unused, name used as the get field name
        button_text: The text on the button
        """
        Widget.__init__(self, name=name, tag_name="div", brief=brief, **field_args)
        # inner div
        self[0] = tag.Part(tag_name="div")
        # error div
        self[0][0] = tag.Part(tag_name="div", attribs={"style":"display:none;"})
        self[0][0][0] = tag.Part(tag_name="p")
        self[0][0][0][0] = ''
        self[0][1] = tag.Part(tag_name="div")
        # container at 0,1,0
        self[0][1][0] = ""
        # form containing input text fields and button
        self[0][2] = tag.Part(tag_name="form", attribs={"role":"form", "method":"post"})
        # div containing text character fields
        self[0][2][0] = tag.Part(tag_name='div')
        # the first text input field
        self[0][2][0][0] = tag.ClosedPart(tag_name="input", attribs ={"type":"password",
                                                                      "size":"1",
                                                                      "maxlength":"1",
                                                                      "required":"required",
                                                                      "style":"width:2em;"})
        self[0][2][0][1] = "-"
        # the second text input field
        self[0][2][0][2] = tag.ClosedPart(tag_name="input", attribs ={"type":"password",
                                                                      "size":"1",
                                                                      "maxlength":"1",
                                                                      "required":"required",
                                                                      "style":"width:2em;"})
        self[0][2][0][3] = "-"
        # the third text input field
        self[0][2][0][4] = tag.ClosedPart(tag_name="input", attribs ={"type":"password",
                                                                      "size":"1",
                                                                      "maxlength":"1",
                                                                      "required":"required",
                                                                      "style":"width:2em;"})
        self[0][2][0][5] = "-"
        # the fourth text input field
        self[0][2][0][6] = tag.ClosedPart(tag_name="input", attribs ={"type":"password",
                                                                      "size":"1",
                                                                      "maxlength":"1",
                                                                      "required":"required",
                                                                      "style":"width:2em;"})
        # div containing submit button
        self[0][2][1] = tag.Part(tag_name='div')
        # the left label
        self[0][2][1][0] = tag.Part(tag_name="label", hide_if_empty=True)
        # the submit button
        self[0][2][1][1] = tag.ClosedPart(tag_name="input", attribs = {"type":"submit"})
        # the right label
        self[0][2][1][2] = tag.Part(tag_name="label", hide_if_empty=True)



    def _build(self, page, ident_list, environ, call_data, lang):
        "build the form"
        # Hides widget if no error and hide is True
        self.widget_hide(self.get_field_value("hide"))
        if not self.get_field_value("action"):
            # setting self._error replaces the entire tag
            self._error = "Warning: No form action"
            return
        actionurl = skiboot.get_url(self.get_field_value("action"),  proj_ident=page.proj_ident)
        if not actionurl:
            # setting self._error replaces the entire tag
            self._error = "Warning: broken link"
            return

        if self.get_field_value('inner_div_class'):
            self[0].update_attribs({"class":self.get_field_value('inner_div_class')})

        if self.get_field_value('error_class'):
            self[0][0].update_attribs({"class":self.get_field_value('error_class')})
        if self.error_status:
            self[0][0].del_one_attrib("style")

        # update the action of the form
        self[0][2].update_attribs({"action": actionurl})

        if self.get_field_value('char_div_class'):
            self[0][2][0].update_attribs({"class":self.get_field_value('char_div_class')})
        if self.get_field_value('char_div_style'):
            self[0][2][0].update_attribs({"style":self.get_field_value('char_div_style')})

        # set autofocus on first non-disabled input field
        autofocus = False

        # first input field
        self[0][2][0][0].update_attribs({"name":self.get_formname('pin1')})
        if self.get_field_value('pin1'):
            self[0][2][0][0].update_attribs({"autofocus":"autofocus"})
            autofocus = True
        else:
            self[0][2][0][0].update_attribs({"disabled":"disabled", "value":"X"})

        # second input field
        self[0][2][0][2].update_attribs({"name":self.get_formname('pin2')})
        if self.get_field_value('pin2'):
            if not autofocus:
                self[0][2][0][2].update_attribs({"autofocus":"autofocus"})
                autofocus = True
        else:
            self[0][2][0][2].update_attribs({"disabled":"disabled", "value":"X"})

        # third input field
        self[0][2][0][4].update_attribs({"name":self.get_formname('pin3')})
        if self.get_field_value('pin3'):
            if not autofocus:
                self[0][2][0][4].update_attribs({"autofocus":"autofocus"})
                autofocus = True
        else:
            self[0][2][0][4].update_attribs({"disabled":"disabled", "value":"X"})

        # fourth input field
        self[0][2][0][6].update_attribs({"name":self.get_formname('pin4')})
        if self.get_field_value('pin4'):
            if not autofocus:
                self[0][2][0][6].update_attribs({"autofocus":"autofocus"})
                autofocus = True
        else:
            self[0][2][0][6].update_attribs({"disabled":"disabled", "value":"X"})

        # div containing the button
        if self.get_field_value('butt_div_class'):
            self[0][2][1].update_attribs({"class":self.get_field_value('butt_div_class')})

        if self.get_field_value('left_label'):
            self[0][2][1][0][0] = self.get_field_value('left_label')
        if self.get_field_value('left_class'):
            self[0][2][1][0].attribs = {"class": self.get_field_value('left_class')}
 
        # the submit button
        if self.get_field_value('button_class'):
            self[0][2][1][1].update_attribs({"class":self.get_field_value('button_class'),
                                                                                   "value":self.get_field_value('button_text')})
        else:
            self[0][2][1][1].update_attribs({"value":self.get_field_value('button_text')})

        # set an id in the submit button for the 'label for' tag
        self[0][2][1][1].insert_id()

        if self.get_field_value('right_label'):
            self[0][2][1][2][0] = self.get_field_value('right_label')
        if self.get_field_value('right_class'):
            self[0][2][1][2].attribs = {"class": self.get_field_value('right_class')}

        # set the label 'for' attribute
        self[0][2][1][0].update_attribs({'for':self[0][2][1][1].get_id()})
        self[0][2][1][2].update_attribs({'for':self[0][2][1][1].get_id()})

        # add ident and four hidden fields
        self.add_hiddens(self[0][2], page)


    def __str__(self):
        """Returns a text string to illustrate the widget"""
        return """
<div>  <!-- with widget id and class widget_class -->
  <div>  <!-- with class attribute set to inner_div_class if a class is set -->
    <div> <!-- normally hidden div, with class error_class -->
      <p> <!-- Any error text appears here --> </p>
    </div>
    <div>
     <!- A container of further code goes here ->
    </div>
    <form method="post"> <!-- action attribute set to action field -->
      <div>  <!-- with class attribute set to char_div_class and style to char_div_style -->
       <!-- each input field has maxlength set to one character -->
        <input type=\"password\" />-<input type=\"password\" />-<input type=\"password\" />-<input type=\"password\" />
      </div>
      <div>  <!-- with class attribute set to butt_div_class if a class is set -->
        <label> <!-- with class set to left_class and content to left_label -->
        </label>
        <input type=\"submit\" /> <!-- button value set to button_text -->
                                       <!-- and class attribute set to button_class if a class is set -->
        <label> <!-- with class set to right_class and content to right_label -->
        </label>
      </div>
      <!-- hidden input fields -->    
    </form>
  </div>
</div>"""





