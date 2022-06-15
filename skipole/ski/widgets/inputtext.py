

"""Contains widgets for inputting text"""

from .. import tag
from . import Widget, ClosedWidget, FieldArg, FieldArgList, FieldArgTable, FieldArgDict


class TextInput1(ClosedWidget):
    """Defines an input field only (no form, label or submit button)
       does not display errors"""

    # This class does not display any error messages
    display_errors = False

    # js_validators is a class attribute, True if javascript validation is enabled
    js_validators=True

    arg_descriptions = {
                        'input_accepted_class':FieldArg("cssclass", ''),
                        'input_errored_class':FieldArg("cssclass", ''),
                        'set_input_accepted':FieldArg("boolean", False, jsonset=True),
                        'set_input_errored':FieldArg("boolean", False, jsonset=True),
                        'input_text':FieldArg("text", '', valdt=True, jsonset=True),
                        'size':FieldArg("text", ''),
                        'maxlength':FieldArg("text", ''),
                        'disabled':FieldArg("boolean", False),
                        'required':FieldArg("boolean", False),
                        'type':FieldArg("text", 'text'),
                        'pattern':FieldArg("text", ''),
                        'title':FieldArg("text", '')
                       }
    def __init__(self, name=None, brief='', **field_args):
        """
        input_accepted_class: A class which can be set on the input field
        input_errored_class: A class which can be set on the input field
        set_input_accepted: If True, input_accepted_class will be set on the input field
        set_errored_accepted: If True, input_errored_class will be set on the input field
        input_text: The default text in the text input field, field name used as name attribute
        size: The number of characters appearing in the text input field
        maxlength: The maximum number of characters accepted in the text input field
        disabled: Set True if the field is to be disabled
        required: Set True to put the 'required' attribute into the input field
        type: the type set on the input field, such as text or email
        pattern: regular expression pattern
        title: helps describe the pattern
        """
        ClosedWidget.__init__(self, name=name, brief=brief, **field_args)
        self.tag_name = "input"
        self.attribs["type"] = "text"


    def _build(self, page, ident_list, environ, call_data, lang):
        "build the input field"
        self.attribs["name"] = self.get_formname('input_text')
        self.attribs["value"] = self.wf.input_text

        if self.wf.set_input_accepted and self.wf.input_accepted_class:
            if self.wf.widget_class:
                self.attribs["class"] = self.wf.widget_class + " " + self.wf.input_accepted_class
            else:
                self.attribs["class"] = self.wf.input_accepted_class
        if self.wf.set_input_errored and self.wf.input_errored_class:
            if self.wf.widget_class:
                self.attribs["class"] = self.wf.widget_class + " " + self.wf.input_errored_class
            else:
                self.attribs["class"] = self.wf.input_errored_class

        # any label:value added to self.jlabels will be set in a javascript fieldvalues attribute for the widget
        self.jlabels['input_accepted_class'] = self.wf.input_accepted_class
        self.jlabels['input_errored_class'] = self.wf.input_errored_class

        if self.wf.size:
            self.attribs["size"] = self.wf.size
        if self.wf.maxlength:
            self.attribs["maxlength"] = self.wf.maxlength
        if self.wf.disabled:
            self.attribs["disabled"] = "disabled"
        if self.wf.required:
            self.attribs["required"] = "required"
        if self.wf.type:
            self.attribs["type"] = self.wf.type
        if self.wf.pattern:
            self.attribs["pattern"] = self.wf.pattern
        if self.wf.title:
            self.attribs["title"] = self.wf.title

 
    @classmethod
    def description(cls):
        """Returns a text string to illustrate the widget"""
        return """
  <input type='text' />
  <!-- with widget id and class widget_class and input_accepted_class added if
       set_input_accepted is set to True, and input_errored_class added if
       set_input_errored is set to True, (which will remove input_accepted_class) -->
"""


class Password1(ClosedWidget):
    """Defines a password input field only (no form, label or submit button)
       does not display errors"""

    # This class does not display any error messages
    display_errors = False

    # js_validators is a class attribute, True if javascript validation is enabled
    js_validators=True

    arg_descriptions = {
                        'input_accepted_class':FieldArg("cssclass", ''),
                        'input_errored_class':FieldArg("cssclass", ''),
                        'set_input_accepted':FieldArg("boolean", False, jsonset=True),
                        'set_input_errored':FieldArg("boolean", False, jsonset=True),
                        'input_text':FieldArg("text", '', valdt=True, jsonset=True),
                        'size':FieldArg("text", ''),
                        'maxlength':FieldArg("text", ''),
                        'disabled':FieldArg("boolean", False),
                        'required':FieldArg("boolean", False)
                       }
    def __init__(self, name=None, brief='', **field_args):
        """
        input_accepted_class: A class which can be set on the input field
        input_errored_class: A class which can be set on the input field
        set_input_accepted: If True, input_accepted_class will be set on the input field
        set_errored_accepted: If True, input_errored_class will be set on the input field
        input_text: The default text in the text input field, field name used as name attribute
        size: The number of characters appearing in the text input field
        maxlength: The maximum number of characters accepted in the text input field
        disabled: Set True if the field is to be disabled
        required: Set True to put the 'required' attribute into the input field
        """
        ClosedWidget.__init__(self, name=name, brief=brief, **field_args)
        self.tag_name = "input"
        self.attribs["type"] = "password"


    def _build(self, page, ident_list, environ, call_data, lang):
        "build the input field"
        self.attribs["name"] = self.get_formname('input_text')
        self.attribs["value"] = self.wf.input_text

        if self.wf.set_input_accepted and self.wf.input_accepted_class:
            if self.wf.widget_class:
                self.attribs["class"] = self.wf.widget_class + " " + self.wf.input_accepted_class
            else:
                self.attribs["class"] = self.wf.input_accepted_class
        if self.wf.set_input_errored and self.wf.input_errored_class:
            if self.wf.widget_class:
                self.attribs["class"] = self.wf.widget_class + " " + self.wf.input_errored_class
            else:
                self.attribs["class"] = self.wf.input_errored_class

        # any label:value added to self.jlabels will be set in a javascript fieldvalues attribute for the widget
        self.jlabels['input_accepted_class'] = self.wf.input_accepted_class
        self.jlabels['input_errored_class'] = self.wf.input_errored_class

        if self.wf.size:
            self.attribs["size"] = self.wf.size
        if self.wf.maxlength:
            self.attribs["maxlength"] = self.wf.maxlength
        if self.wf.disabled:
            self.attribs["disabled"] = "disabled"
        if self.wf.required:
            self.attribs["required"] = "required"

 
    @classmethod
    def description(cls):
        """Returns a text string to illustrate the widget"""
        return """
  <input type='password' />
  <!-- with widget id and class widget_class and input_accepted_class added if
       set_input_accepted is set to True, and input_errored_class added if
       set_input_errored is set to True, (which will remove input_accepted_class) -->
"""


class TextInput2(Widget):
    """Defines a div containing a hidden error paragraph
       with a text input field (no form or submit button)
       A label to the left of the text can have a class and text set"""

    # js_validators is a class attribute, True if javascript validation is enabled
    js_validators=True

    error_location = (0,0,0)

    arg_descriptions = {
                        'input_accepted_class':FieldArg("cssclass", ''),
                        'input_errored_class':FieldArg("cssclass", ''),
                        'inputdiv_class':FieldArg("cssclass", ''),
                        'set_input_accepted':FieldArg("boolean", False, jsonset=True),
                        'set_input_errored':FieldArg("boolean", False, jsonset=True),
                        'label':FieldArg("text", 'Your Input:'),
                        'label_class':FieldArg("cssclass", ''),
                        'label_style':FieldArg("cssstyle", ''),
                        'error_class':FieldArg("cssclass", ''),
                        'input_text':FieldArg("text", '', valdt=True, jsonset=True),
                        'input_class':FieldArg("cssclass", ''),
                        'input_disabled_class':FieldArg("cssclass", ''),
                        'size':FieldArg("text", ''),
                        'maxlength':FieldArg("text", ''),
                        'redstar':FieldArg("boolean", False),
                        'redstar_class':FieldArg("cssclass", ''),
                        'redstar_style':FieldArg("cssstyle", ''),
                        'disabled':FieldArg("boolean", False, jsonset=True),
                        'required':FieldArg("boolean", False),
                        'type':FieldArg("text", 'text'),
                        'pattern':FieldArg("text", ''),
                        'title':FieldArg("text", '')
                       }
    def __init__(self, name=None, brief='', **field_args):
        """
        input_accepted_class: A class which can be set on the input field
        input_errored_class: A class which can be set on the input field
        set_input_accepted: If True, input_accepted_class will be set on the input field
        set_errored_accepted: If True, input_errored_class will be set on the input field
        label: The text appearing in a label tag to the left of the input field
        label_class: The css class of the label to the left of the input field
        error_class: The class applied to the hidden paragraph on error.
        inputdiv_class: The css class of the div containing the label and input field
        input_text: The default text in the text input field, field name used as name attribute
        input_class: The css class of the input field
        input_disabled_class: css class of the input field which replaces input_class if disabled is True
        size: The number of characters appearing in the text input area
        maxlength: The maximum number of characters accepted in the text area
        redstar: If True a red asterix is shown by the side of the input field
        disabled: Set True if the field is to be disabled
        required: Set True to put the 'required' flag into the input field
        type: the type set on the input field, such as text or email
        pattern: regular expression pattern
        title: helps describe the pattern
        """
        Widget.__init__(self, name=name, brief=brief, **field_args)
        self.tag_name = "div"
        # error div at 0
        self[0] = tag.Part(tag_name="div", attribs={"style":"display:none;"})
        self[0][0] = tag.Part(tag_name="p")
        self[0][0][0] = ''
        # inputdiv
        self[1] = tag.Part(tag_name="div")
        # the label
        self[1][0] = tag.Part(tag_name="label", hide_if_empty=True)
        # the text input field
        self[1][1] = tag.ClosedPart(tag_name="input", attribs ={"type":"text"})


    def _build(self, page, ident_list, environ, call_data, lang):
        "build the input field"

        self[0].set_class_style(self.wf.error_class)
        if self.error_status:
            self[0].del_one_attrib("style")

        self[1].set_class_style(self.wf.inputdiv_class)

        self[1][0].set_class_style(self.wf.label_class, self.wf.label_style)
        if self.wf.label:
            self[1][0][0] = self.wf.label

        # set an id in the input field for the 'label for' tag
        # any label:value added to self.jlabels will be set in a javascript fieldvalues attribute for the widget
        self.jlabels['input_id'] = self[1][1].insert_id()
        self[1][0].attribs['for'] = self.jlabels['input_id']

        if self.wf.input_accepted_class:
            self.jlabels['input_accepted_class'] = self.wf.input_accepted_class
        if self.wf.input_errored_class:
            self.jlabels['input_errored_class'] = self.wf.input_errored_class
        if self.wf.input_class:
            self.jlabels['input_class'] = self.wf.input_class
        if self.wf.input_disabled_class:
            self.jlabels['input_disabled_class'] = self.wf.input_disabled_class

        self[1][1].attribs.update({"name":self.get_formname('input_text'), "value":self.wf.input_text})

        if self.wf.size:
            self[1][1].attribs["size"] = self.wf.size
        if self.wf.maxlength:
            self[1][1].attribs["maxlength"] = self.wf.maxlength
        if self.wf.required:
            self[1][1].attribs["required"] = "required"
        if self.wf.type:
            self[1][1].attribs["type"] = self.wf.type
        if self.wf.pattern:
            self[1][1].attribs["pattern"] = self.wf.pattern
        if self.wf.title:
            self[1][1].attribs["title"] = self.wf.title

        if self.wf.input_class:
            input_class = self.wf.input_class
        else:
            input_class = ''

        if self.wf.disabled:
            self[1][1].attribs["disabled"] = "disabled"
            if self.wf.input_disabled_class:
                input_class = self.wf.input_disabled_class
        if self.error_status and self.wf.input_errored_class:
            if input_class:
                input_class = input_class + ' ' + self.wf.input_errored_class
            else:
                input_class = self.wf.input_errored_class
        elif self.wf.set_input_errored and self.wf.input_errored_class:
            if input_class:
                input_class = input_class + ' ' + self.wf.input_errored_class
            else:
                input_class = self.wf.input_errored_class
        elif self.wf.set_input_accepted and self.wf.input_accepted_class:
            if input_class:
                input_class = input_class + ' ' + self.wf.input_accepted_class
            else:
                input_class = self.wf.input_accepted_class
        if input_class:
            self[1][1].attribs["class"] = input_class
        # redstar
        if self.wf.redstar:
            self[1][2] = tag.Part(tag_name="span")
            self[1][2].set_class_style(self.wf.redstar_class, self.wf.redstar_style)
            self[1][2][0] = '*'

    @classmethod
    def description(cls):
        """Returns a text string to illustrate the widget"""
        return """
<div>  <!-- with widget id and class widget_class -->
  <div> <!-- normally hidden div, with class error_class -->
    <p> <!-- Any error text appears here --> </p>
  </div>
  <div>  <!-- class attribute set to inputdiv_class -->
    <label> <!-- with class set to label_class -->
            <!-- content set to label -->
    </label>
    <input type='text' /> <!-- with attributes set appropriately -->
    <span>*</span> <!-- shown if redstar is True -->
  </div>
</div>"""


class Password2(Widget):
    """Defines a div containing a hidden error paragraph
       with a password input field (no form or submit button)
       A label to the left of the text can have a class and text set"""

    # js_validators is a class attribute, True if javascript validation is enabled
    js_validators=True

    error_location = (0,0,0)

    arg_descriptions = {
                        'input_accepted_class':FieldArg("cssclass", ''),
                        'input_errored_class':FieldArg("cssclass", ''),
                        'input_disabled_class':FieldArg("cssclass", ''),
                        'inputdiv_class':FieldArg("cssclass", ''),
                        'set_input_accepted':FieldArg("boolean", False, jsonset=True),
                        'set_input_errored':FieldArg("boolean", False, jsonset=True),
                        'label':FieldArg("text", 'Password:'),
                        'label_class':FieldArg("cssclass", ''),
                        'label_style':FieldArg("cssstyle", ''),
                        'error_class':FieldArg("cssclass", ''),
                        'input_text':FieldArg("text", '', valdt=True, jsonset=True),
                        'input_class':FieldArg("cssclass", ''),
                        'input_style':FieldArg("cssstyle", ''),
                        'size':FieldArg("text", ''),
                        'maxlength':FieldArg("text", ''),
                        'disabled':FieldArg("boolean", False, jsonset=True),
                        'redstar':FieldArg("boolean", False),
                        'redstar_class':FieldArg("cssclass", ''),
                        'redstar_style':FieldArg("cssstyle", ''),
                        'required':FieldArg("boolean", False)
                       }
    def __init__(self, name=None, brief='', **field_args):
        """
        input_accepted_class: A class which can be set on the input field
        input_errored_class: A class which can be set on the input field
        input_disabled_class: css class of the input field which replaces input_class if disabled is True
        inputdiv_class: The css class of the div containing the label and input field
        set_input_accepted: If True, input_accepted_class will be set on the input field
        set_errored_accepted: If True, input_errored_class will be set on the input field
        label: The text appearing in a label tag to the left of the input field
        label_class: The css class of the label to the left of the input field
        error_class: The class applied to the hidden paragraph on error.
        input_text: The default text in the text input field, field name used as name attribute
        input_class: The css class of the input field
        size: The number of characters appearing in the text input area
        maxlength: The maximum number of characters accepted in the text area
        disabled: Set True if the field is to be disabled
        redstar: If True a red asterix is shown by the side of the input field
        required: Set True to put the 'required' flag into the input field
        """
        Widget.__init__(self, name=name, brief=brief, **field_args)
        self.tag_name = "div"
        # error div at 0
        self[0] = tag.Part(tag_name="div", attribs={"style":"display:none;"})
        self[0][0] = tag.Part(tag_name="p")
        self[0][0][0] = ''
        # inputdiv
        self[1] = tag.Part(tag_name="div")
        # the label
        self[1][0] = tag.Part(tag_name="label", hide_if_empty=True)
        # the text input field
        self[1][1] = tag.ClosedPart(tag_name="input", attribs ={"type":"password"})


    def _build(self, page, ident_list, environ, call_data, lang):
        "build the input field"

        self[0].set_class_style(self.wf.error_class)
        if self.error_status:
            self[0].del_one_attrib("style")

        self[1].set_class_style(self.wf.inputdiv_class)

        self[1][0].set_class_style(self.wf.label_class, self.wf.label_style)
        if self.wf.label:
            self[1][0][0] = self.wf.label

        # set an id in the input field for the 'label for' tag
        self[1][0].attribs['for'] = self[1][1].insert_id()

        # any label:value added to self.jlabels will be set in a javascript fieldvalues attribute for the widget
        if self.wf.input_accepted_class:
            self.jlabels['input_accepted_class'] = self.wf.input_accepted_class
        if self.wf.input_errored_class:
            self.jlabels['input_errored_class'] = self.wf.input_errored_class
        if self.wf.input_class:
            self.jlabels['input_class'] = self.wf.input_class
        if self.wf.input_disabled_class:
            self.jlabels['input_disabled_class'] = self.wf.input_disabled_class

        self[1][1].attribs.update({"name":self.get_formname('input_text'), "value":self.wf.input_text})

        if self.wf.size:
            self[1][1].attribs["size"] = self.wf.size
        if self.wf.maxlength:
            self[1][1].attribs["maxlength"] = self.wf.maxlength
        if self.wf.required:
            self[1][1].attribs["required"] = "required"
        if self.wf.input_style:
            self[1][1].attribs["style"] = self.wf.input_style

        if self.wf.input_class:
            input_class = self.wf.input_class
        else:
            input_class = ''
        if self.wf.disabled:
            self[1][1].attribs["disabled"] = "disabled"
            if self.wf.input_disabled_class:
                input_class = self.wf.input_disabled_class
        if self.error_status and self.wf.input_errored_class:
            if input_class:
                input_class = input_class + ' ' + self.wf.input_errored_class
            else:
                input_class = self.wf.input_errored_class
        elif self.wf.set_input_errored and self.wf.input_errored_class:
            if input_class:
                input_class = input_class + ' ' + self.wf.input_errored_class
            else:
                input_class = self.wf.input_errored_class
        elif self.wf.set_input_accepted and self.wf.input_accepted_class:
            if input_class:
                input_class = input_class + ' ' + self.wf.input_accepted_class
            else:
                input_class = self.wf.input_accepted_class
        if input_class:
            self[1][1].attribs["class"] = input_class
        # redstar
        if self.wf.redstar:
            self[1][2] = tag.Part(tag_name="span")
            self[1][2].set_class_style(self.wf.redstar_class, self.wf.redstar_style)
            self[1][2][0] = '*'


    @classmethod
    def description(cls):
        """Returns a text string to illustrate the widget"""
        return """
<div>  <!-- with widget id and class widget_class -->
  <div> <!-- normally hidden paragraph, with class error_class -->
    <p> <!-- Any error text appears here --> </p>
  </div>
  <div>  <!-- class attribute set to inputdiv_class -->
    <label> <!-- with class set to label_class -->
            <!-- content set to label -->
    </label>
    <input type='password' /> <!-- with attributes set appropriately -->
    <span>*</span> <!-- shown if redstar is True -->
  </div>
</div>"""


class TextInput3(Widget):
    """Defines a div containing a text input field (no form or submit button)
       with a left and right label, does not display errors"""

    # This class does not display any error messages
    display_errors = False

    # js_validators is a class attribute, True if javascript validation is enabled
    js_validators=True

    arg_descriptions = {
                        'input_class':FieldArg("cssclass", ''),
                        'input_style':FieldArg("cssstyle", ''),
                        'input_accepted_class':FieldArg("cssclass", ''),
                        'input_errored_class':FieldArg("cssclass", ''),
                        'set_input_accepted':FieldArg("boolean", False, jsonset=True),
                        'set_input_errored':FieldArg("boolean", False, jsonset=True),
                        'left_label':FieldArg("text", 'Your Input:'),
                        'left_class':FieldArg("cssclass", ''),
                        'left_style':FieldArg("cssstyle", ''),
                        'right_label':FieldArg("text", ''),
                        'right_class':FieldArg("cssclass", ''),
                        'right_style':FieldArg("cssstyle", ''),
                        'input_text':FieldArg("text", '', valdt=True, jsonset=True),
                        'size':FieldArg("text", ''),
                        'maxlength':FieldArg("text", ''),
                        'disabled':FieldArg("boolean", False),
                        'required':FieldArg("boolean", False),
                        'type':FieldArg("text", 'text'),
                        'pattern':FieldArg("text", ''),
                        'title':FieldArg("text", '')
                       }
    def __init__(self, name=None, brief='', **field_args):
        """
        input_class: The css class of the input field
        input_style: The css style of the input field
        input_accepted_class: A class which can be set on the input field
        input_errored_class: A class which can be set on the input field
        set_input_accepted: If True, input_accepted_class will be set on the input field
        set_errored_accepted: If True, input_errored_class will be set on the input field
        left_label: The text displayed to the left of the input field
        left_class: The css class of the label to the left of the input field
        right_label: The text displayed to the right of the input field
        right_class: The css class of the label to the right of the input field
        input_text: The default text in the text input field, field name used as name attribute
        size: The number of characters appearing in the text input field
        maxlength: The maximum number of characters accepted in the text input field
        disabled: Set True if the field is to be disabled
        required: Set True to put the 'required' attribute into the input field
        type: the type set on the input field, such as text or email
        pattern: regular expression pattern
        title: helps describe the pattern
        """
        Widget.__init__(self, name=name, brief=brief, **field_args)
        self.tag_name = "div"
        self[0] = tag.Part(tag_name="label", hide_if_empty=True)
        self[1] = tag.ClosedPart(tag_name="input", attribs = {"type":"text"})
        self[2] = tag.Part(tag_name="label", hide_if_empty=True)


    def _build(self, page, ident_list, environ, call_data, lang):
        "build the input field"
        if self.wf.left_label:
            self[0][0] = self.wf.left_label

        self[0].set_class_style(self.wf.left_class, self.wf.left_style)

        self[1].attribs.update({"name":self.get_formname('input_text'), "value":self.wf.input_text})

        if self.wf.input_class:
            input_class = self.wf.input_class
        else:
            input_class = ''

        if self.wf.set_input_errored and self.wf.input_errored_class:
            if input_class:
                input_class = input_class + ' ' + self.wf.input_errored_class
            else:
                input_class = self.wf.input_errored_class
        elif self.wf.set_input_accepted and self.wf.input_accepted_class:
            if input_class:
                input_class = input_class + ' ' + self.wf.input_accepted_class
            else:
                input_class = self.wf.input_accepted_class

        self[1].set_class_style(input_class, self.wf.input_style)

        if self.wf.size:
            self[1].attribs["size"] = self.wf.size
        if self.wf.maxlength:
            self[1].attribs["maxlength"] = self.wf.maxlength
        if self.wf.disabled:
            self[1].attribs["disabled"] = "disabled"
        if self.wf.required:
            self[1].attribs["required"] = "required"
        if self.wf.type:
            self[1].attribs["type"] = self.wf.type
        if self.wf.pattern:
            self[1].attribs["pattern"] = self.wf.pattern
        if self.wf.title:
            self[1].attribs["title"] = self.wf.title

        if self.wf.right_label:
            self[2][0] = self.wf.right_label

        self[2].set_class_style(self.wf.right_class, self.wf.right_style)

        # set an id in the text input field for the 'label for' tag
        # any label:value added to self.jlabels will be set in a javascript fieldvalues attribute for the widget
        self.jlabels['input_id'] = self[1].insert_id()
        self[0].attribs['for'] = self.jlabels['input_id']
        self[2].attribs['for'] = self.jlabels['input_id']

        if self.wf.input_accepted_class:
            self.jlabels['input_accepted_class'] = self.wf.input_accepted_class
        if self.wf.input_errored_class:
            self.jlabels['input_errored_class'] = self.wf.input_errored_class
 
    @classmethod
    def description(cls):
        """Returns a text string to illustrate the widget"""
        return """
<div>  <!-- with widget id and class widget_class -->
  <label> <!-- with class set to left_class and content to left_label -->
  </label>
  <input type='text' /> <!-- with attributes set appropriately -->
  <label> <!-- with class set to right_class and content to right_label -->
  </label>
</div>"""


class TextInput4(Widget):
    """Defines a div containing a div with label
       and a div with a text input field (no form or submit button)
       All divs, label and input field can have class set
       No error display"""

    # This class does not display any error messages
    display_errors = False

    # js_validators is a class attribute, True if javascript validation is enabled
    js_validators=True   

    arg_descriptions = {
                        'input_accepted_class':FieldArg("cssclass", ''),
                        'input_errored_class':FieldArg("cssclass", ''),
                        'set_input_accepted':FieldArg("boolean", False, jsonset=True),
                        'set_input_errored':FieldArg("boolean", False, jsonset=True),
                        'labeldiv_class':FieldArg("cssclass", ''),
                        'labeldiv_style':FieldArg("cssstyle", ''),
                        'label':FieldArg("text", 'Your input:'),
                        'label_class':FieldArg("cssclass", ''),
                        'label_style':FieldArg("cssstyle", ''),
                        'inputdiv_class':FieldArg("cssclass", ''),
                        'inputdiv_style':FieldArg("cssstyle", ''),
                        'input_text':FieldArg("text", '', valdt=True, jsonset=True),
                        'input_class':FieldArg("cssclass", ''),
                        'input_style':FieldArg("cssstyle", ''),
                        'input_disabled_class':FieldArg("cssclass", ''),
                        'size':FieldArg("text", ''),
                        'maxlength':FieldArg("text", ''),
                        'redstar':FieldArg("boolean", False),
                        'redstar_class':FieldArg("cssclass", ''),
                        'redstar_style':FieldArg("cssstyle", ''),
                        'disabled':FieldArg("boolean", False, jsonset=True),
                        'required':FieldArg("boolean", False),
                        'type':FieldArg("text", 'text'),
                        'pattern':FieldArg("text", ''),
                        'title':FieldArg("text", '')
                       }
    def __init__(self, name=None, brief='', **field_args):
        """
        input_accepted_class: A class which can be set on the input field
        input_errored_class: A class which can be set on the input field
        set_input_accepted: If True, input_accepted_class will be set on the input field
        set_errored_accepted: If True, input_errored_class will be set on the input field
        labeldiv_class: The css class of the div containing the label
        label: The text appearing in a label tag to the left of the input field
        label_class: The css class of the label to the left of the input field
        inputdiv_class: The css class of the div containing the input field
        input_text: The default text in the text input field, field name used as name attribute
        input_class: The css class of the input field
        input_disabled_class: css class of the input field which replaces input_class if disabled is True
        size: The number of characters appearing in the text input area
        maxlength: The maximum number of characters accepted in the text area
        redstar: If True a red asterix is shown by the side of the input field
        disabled: Set True if the field is to be disabled
        required: Set True to put the 'required' flag into the input field
        type: the type set on the input field, such as text or email
        pattern: regular expression pattern
        title: helps describe the pattern
        """
        Widget.__init__(self, name=name, brief=brief, **field_args)
        self.tag_name = "div"
        # label div at 0
        self[0] = tag.Part(tag_name="div")
        # the label
        self[0][0] = tag.Part(tag_name="label", hide_if_empty=True)
        # input div at 1
        self[1] = tag.Part(tag_name="div")
        # the text input field
        self[1][0] = tag.ClosedPart(tag_name="input", attribs ={"type":"text"})


    def _build(self, page, ident_list, environ, call_data, lang):
        "build the input field"
        # label
        self[0].set_class_style(self.wf.labeldiv_class, self.wf.labeldiv_style)
        self[0][0].set_class_style(self.wf.label_class, self.wf.label_style)

        if self.wf.label:
            self[0][0][0] = self.wf.label
        # input div
        self[1].set_class_style(self.wf.inputdiv_class, self.wf.inputdiv_style)

        # set an id in the input field for the 'label for' tag
        # any label:value added to self.jlabels will be set in a javascript fieldvalues attribute for the widget
        self.jlabels['input_id'] = self[1][0].insert_id()
        self[0][0].attribs['for'] = self.jlabels['input_id']

        if self.wf.input_accepted_class:
            self.jlabels['input_accepted_class'] = self.wf.input_accepted_class
        if self.wf.input_errored_class:
            self.jlabels['input_errored_class'] = self.wf.input_errored_class
        if self.wf.input_class:
            self.jlabels['input_class'] = self.wf.input_class
        if self.wf.input_disabled_class:
            self.jlabels['input_disabled_class'] = self.wf.input_disabled_class

        # input field
        self[1][0].attribs.update({"name":self.get_formname('input_text'), "value":self.wf.input_text})

        if self.wf.size:
            self[1][0].attribs["size"] = self.wf.size
        if self.wf.maxlength:
            self[1][0].attribs["maxlength"] = self.wf.maxlength
        if self.wf.required:
            self[1][0].attribs["required"] = "required"
        if self.wf.type:
            self[1][0].attribs["type"] = self.wf.type
        if self.wf.pattern:
            self[1][0].attribs["pattern"] = self.wf.pattern
        if self.wf.title:
            self[1][0].attribs["title"] = self.wf.title

        if self.wf.input_class:
            input_class = self.wf.input_class
        else:
            input_class = ''
        if self.wf.disabled:
            self[1][0].attribs["disabled"] = "disabled"
            if self.wf.input_disabled_class:
                input_class = self.wf.input_disabled_class
        if self.wf.set_input_errored and self.wf.input_errored_class:
            if input_class:
                input_class = input_class + ' ' + self.wf.input_errored_class
            else:
                input_class = self.wf.input_errored_class
        elif self.wf.set_input_accepted and self.wf.input_accepted_class:
            if input_class:
                input_class = input_class + ' ' + self.wf.input_accepted_class
            else:
                input_class = self.wf.input_accepted_class

        self[1][0].set_class_style(input_class, self.wf.input_style)

        # redstar
        if self.wf.redstar:
            self[1][1] = tag.Part(tag_name="span")
            self[1][1].set_class_style(self.wf.redstar_class, self.wf.redstar_style)
            self[1][1][0] = '*'


    @classmethod
    def description(cls):
        """Returns a text string to illustrate the widget"""
        return """
<div>  <!-- with widget id and class widget_class -->
  <div> <!-- with class set to labeldiv_class -->
    <label> <!-- with class set to label_class -->
            <!-- content set to label -->
    </label>
  </div>
  <div> <!-- with class set to inputdiv_class -->
    <input type='text' /> <!-- with attributes set appropriately -->
    <span>*</span> <!-- shown if redstar is True -->
  </div>
</div>"""



class SubmitTextInput1(Widget):
    """Defines a form with a text input field, and four hidden fields"""

    # js_validators is a class attribute, True if javascript validation is enabled
    js_validators=True

    error_location = (0,0,0)

    arg_descriptions = {'label':FieldArg("text", 'Your input:'),
                        'label_class':FieldArg("cssclass", ''),
                        'label_style':FieldArg("cssstyle", ''),
                        'action_json':FieldArg("url", ''),
                        'action':FieldArg("url", ''),
                        'hidden_field1':FieldArg("text", '', valdt=True, jsonset=True),
                        'hidden_field2':FieldArg("text", '', valdt=True, jsonset=True),
                        'hidden_field3':FieldArg("text", '', valdt=True, jsonset=True),
                        'hidden_field4':FieldArg("text", '', valdt=True, jsonset=True),
                        'target':FieldArg("text",''),
                        'button_text':FieldArg("text",'Submit'),
                        'button_class':FieldArg("cssclass", ''),
                        'inputdiv_class':FieldArg("cssclass", ''),
                        'inputandbutton_class':FieldArg("cssclass", ''),
                        'inputandbutton_style':FieldArg("cssstyle", ''),
                        'error_class':FieldArg("cssclass", ''),
                        'input_text':FieldArg("text", '', valdt=True, jsonset=True),
                        'size':FieldArg("text", ''),
                        'maxlength':FieldArg("text", ''),
                        'required':FieldArg("boolean", False),
                        'type':FieldArg("text", 'text'),
                        'pattern':FieldArg("text", ''),
                        'title':FieldArg("text", ''),
                        'input_accepted_class':FieldArg("cssclass", ''),
                        'input_errored_class':FieldArg("cssclass", ''),
                        'input_class':FieldArg("cssclass", ''),
                        'set_input_accepted':FieldArg("boolean", False, jsonset=True),
                        'set_input_errored':FieldArg("boolean", False, jsonset=True),
                        'hide':FieldArg("boolean", False, jsonset=True)
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
        target: if given, the target attribute will be set
        button_text: The text on the button
        button_class: The class given to the button tag
        inputdiv_class: the class attribute of the div which contains the label, input text and button
        inputandbutton_class: the class attribute of the span which contains the input text and button
        error_class: The class applied to the paragraph containing the error message on error.
        input_text: The default text in the text input field, field name used as the name attribute
        size: The number of characters appearing in the text input area
        maxlength: The maximum number of characters accepted in the text area
        required: Set True to put the 'required' flag into the input field
        type: the type set on the input field, such as text or email
        pattern: regular expression pattern
        title: helps describe the pattern
        input_accepted_class: A class which can be set on the input field
        input_errored_class: A class which can be set on the input field
        input_class: Class set on the input field
        set_input_accepted: If True, input_accepted_class will be set on the input field
        set_errored_accepted: If True, input_errored_class will be set on the input field
        hide: If True, widget is hidden
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
        # the text input field
        self[1][0][1][0] = tag.ClosedPart(tag_name="input", attribs ={"type":"text"})
        # the submit button
        self[1][0][1][1] = tag.Part(tag_name="button", attribs ={"type":"submit"})
        self[1][0][1][1][0] = "Submit"


    def _build(self, page, ident_list, environ, call_data, lang):
        "build the form"
        if self.wf.target:
            self[1].attribs["target"] = self.wf.target
        # Hides widget if no error and hide is True
        self.widget_hide(self.wf.hide)

        # any label:value added to self.jlabels will be set in a javascript fieldvalues attribute for the widget
        jsonurl = self.get_url(self.wf.action_json)
        if jsonurl:
            self.jlabels['url'] = jsonurl

        if self.wf.error_class:
            self[0].attribs["class"] = self.wf.error_class
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
        self[1].attribs["action"] = actionurl
        # the div holding label, input text and button
        if self.wf.inputdiv_class:
            self[1][0].attribs["class"] = self.wf.inputdiv_class

        self[1][0][0].set_class_style(self.wf.label_class, self.wf.label_style)
        if self.wf.label:
            self[1][0][0][0] = self.wf.label

        # the span holding input text and button
        self[1][0][1].set_class_style(self.wf.inputandbutton_class, self.wf.inputandbutton_style)

        # set an id in the input field for the 'label for' tag
        self.jlabels['input_id'] = self[1][0][1][0].insert_id()

        self[1][0][1][0].attribs.update({"name":self.get_formname('input_text'), "value":self.wf.input_text})

        if self.wf.size:
            self[1][0][1][0].attribs["size"] = self.wf.size
        if self.wf.maxlength:
            self[1][0][1][0].attribs["maxlength"] = self.wf.maxlength
        if self.wf.required:
            self[1][0][1][0].attribs["required"] = "required"
        if self.wf.type:
            self[1][0][1][0].attribs["type"] = self.wf.type
        if self.wf.pattern:
            self[1][0][1][0].attribs["pattern"] = self.wf.pattern
        if self.wf.title:
            self[1][0][1][0].attribs["title"] = self.wf.title

        if self.wf.input_accepted_class:
            self.jlabels['input_accepted_class'] = self.wf.input_accepted_class
        if self.wf.input_errored_class:
            self.jlabels['input_errored_class'] = self.wf.input_errored_class

        if self.wf.input_class:
            input_class = self.wf.input_class
        else:
            input_class = ''

        if self.error_status and self.wf.input_errored_class:
            if input_class:
                input_class = input_class + ' ' + self.wf.input_errored_class
            else:
                input_class = self.wf.input_errored_class
        elif self.wf.set_input_errored and self.wf.input_errored_class:
            if input_class:
                input_class = input_class + ' ' + self.wf.input_errored_class
            else:
                input_class = self.wf.input_errored_class
        elif self.wf.set_input_accepted and self.wf.input_accepted_class:
            if input_class:
                input_class = input_class + ' ' + self.wf.input_accepted_class
            else:
                input_class = self.wf.input_accepted_class

        if input_class:
            self[1][0][1][0].attribs["class"] = input_class

        # set the label 'for' attribute
        self[1][0][0].attribs['for'] = self.jlabels['input_id']

        # submit button
        if self.wf.button_class:
            self[1][0][1][1].attribs["class"] = self.wf.button_class
        if self.wf.button_text:
            self[1][0][1][1][0] = self.wf.button_text

        # add ident and four hidden fields to the form at self[1]
        self.add_hiddens(self[1], page)


    def _build_js(self, page, ident_list, environ, call_data, lang):
        """Sets a submit event handler"""
        ident=self.get_id()
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
      <label> <!-- with class set to label_class and content to label, for set to input text id -->
      </label>
      <span>  <!-- class attribute set to inputandbutton_class -->
          <input type="text" />  <!-- class set to input_class -->
            <!-- input text value set to input_text -->
          <button type="submit"> <!-- with class set to button_class -->
            <!-- button_text -->
          </button>
      </span>
    </div>
    <!-- hidden input fields -->                              
  </form>
</div>"""



class SubmitTextInput3(Widget):
    """Defines paragraphs followed by a form with a text input field"""

    # js_validators is a class attribute, True if javascript validation is enabled
    js_validators=True

    error_location = (0,0,0)

    arg_descriptions = {
                        'show_para1':FieldArg("boolean", True, jsonset=True),
                        'para_text':FieldArg("text", '', jsonset=True),
                        'show_para2':FieldArg("boolean", True, jsonset=True),
                        'textblock_ref':FieldArg("textblock_ref", ""),
                        'label':FieldArg("text", 'Your input:'),
                        'label_class':FieldArg("cssclass", ''),
                        'label_style':FieldArg("cssstyle", ''),
                        'button_label':FieldArg("text", 'Please submit:'),
                        'button_label_class':FieldArg("cssclass", ''),
                        'button_label_style':FieldArg("cssstyle", ''),
                        'action':FieldArg("url", ''),
                        'action_json':FieldArg("url", ''),
                        'hidden_field1':FieldArg("text", '', valdt=True, jsonset=True),
                        'hidden_field2':FieldArg("text", '', valdt=True, jsonset=True),
                        'hidden_field3':FieldArg("text", '', valdt=True, jsonset=True),
                        'hidden_field4':FieldArg("text", '', valdt=True, jsonset=True),
                        'target':FieldArg("text",''),
                        'button_text':FieldArg("text",'Submit'),
                        'button_class':FieldArg("cssclass", ''),
                        'buttondiv_class':FieldArg("cssclass", ''),
                        'outer_class':FieldArg("cssclass", ''),
                        'inputdiv_class':FieldArg("cssclass", ''),
                        'error_class':FieldArg("cssclass", ""),
                        'input_text':FieldArg("text", '', valdt=True, jsonset=True),
                        'size':FieldArg("text", ''),
                        'maxlength':FieldArg("text", ''),
                        'required':FieldArg("boolean", False),
                        'type':FieldArg("text", 'text'),
                        'pattern':FieldArg("text", ''),
                        'title':FieldArg("text", ''),
                        'input_accepted_class':FieldArg("cssclass", ''),
                        'input_errored_class':FieldArg("cssclass", ''),
                        'input_class':FieldArg("cssclass", ''),
                        'set_input_accepted':FieldArg("boolean", False, jsonset=True),
                        'set_input_errored':FieldArg("boolean", False, jsonset=True),
                        'hide':FieldArg("boolean", False, jsonset=True)
                       }

    def __init__(self, name=None, brief='', **field_args):
        """
        show_para1: True if the paragraph is to be visible, False if not
        para_text: The text appearing in the paragraph
        show_para2: True if the paragraph is to be visible, False if not
        textblock_ref: The reference of the TextBlock appearing in the second paragraph
        label: The text displayed to the left of the text input field
        label_class: The css class of the label
        button_label: The text displayed to the left of the button
        button_label_class: The css class of the label to the left of the button
        action_json:  if a value set, and client has jscript enabled, this is the page ident, label, url this button links to, expects a json page back
        action: The page ident, label, url this button links to
        hidden_field1: A hidden field value, leave blank if unused, name used as the get field name
        hidden_field2: A second hidden field value, leave blank if unused, name used as the get field name
        hidden_field3: A third hidden field value, leave blank if unused, name used as the get field name
        hidden_field4: A fourth hidden field value, leave blank if unused, name used as the get field name
        target: if given, the target attribute will be set
        button_text: The text on the button
        buttondiv_class: the class attribute of the div which contains the button
        button_class: the class attribute of the button
        outer_class: the class attribute of the outside div
        inputdiv_class: the class attribute of the tag which contains the label and input text
        error_class: The class applied to the paragraph containing the error message on error.
        input_text: The default text in the text input field, field name used as the name attribute
        size: The number of characters appearing in the text input area
        maxlength: The maximum number of characters accepted in the text area
        required: Set True to put the 'required' flag into the input field
        type: the type set on the input field, such as text or email
        pattern: regular expression pattern
        title: helps describe the pattern
        input_accepted_class: A class which can be set on the input field
        input_errored_class: A class which can be set on the input field
        input_class: Class set on the input field
        set_input_accepted: If True, input_accepted_class will be set on the input field
        set_errored_accepted: If True, input_errored_class will be set on the input field
        hide: If True, widget is hidden
        """
        Widget.__init__(self, name=name, brief=brief, **field_args)
        self.tag_name = "div"
        # error div at 0
        self[0] = tag.Part(tag_name="div", attribs={"style":"display:none;"})
        self[0][0] = tag.Part(tag_name="p")
        self[0][0][0] = ''
        # div containing paragraphs
        self[1] = tag.Part(tag_name='div')
        # paragraph one and two
        self[1][0] = tag.Part(tag_name='p')
        self[1][0][0] =''
        self[1][1] = tag.Part(tag_name='p')
        self[1][1][0] = ''

        # The form
        self[2] = tag.Part(tag_name='form', attribs={"role":"form", "method":"post"})

        # div containing label and input text
        self[2][0] = tag.Part(tag_name='div')
        # the label
        self[2][0][0] = tag.Part(tag_name="label", hide_if_empty=True)
        # the text input field
        self[2][0][1] = tag.ClosedPart(tag_name="input", attribs ={"type":"text"})

        # div containing button
        self[2][1] = tag.Part(tag_name='div')
        # the label on the left of the button
        self[2][1][0] = tag.Part(tag_name="label", hide_if_empty=True)
        # the submit button
        self[2][1][1] = tag.ClosedPart(tag_name="input", attribs={"type":"submit"})


    def _build(self, page, ident_list, environ, call_data, lang):
        "build the form"

        if self.wf.target:
            self[2].attribs["target"] = self.wf.target
        # Hides widget if no error and hide is True
        self.widget_hide(self.wf.hide)

        # any label:value added to self.jlabels will be set in a javascript fieldvalues attribute for the widget
        jsonurl = self.get_url(self.wf.action_json)
        if jsonurl:
            self.jlabels['url'] = jsonurl

        if self.wf.error_class:
            self[0].attribs["class"] = self.wf.error_class
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
        self[2].attribs["action"] = actionurl

        # the class of the outer div
        self[1].set_class_style(self.wf.outer_class)


        # set paragraphs
        if not self.wf.show_para1:
            self[1][0].attribs["style"] = "display:none;"
        self[1][0][0] = self.wf.para_text
        if not self.wf.show_para2:
            self[1][1].attribs["style"] = "display:none;"
        # define the textblock
        tblock = self.wf.textblock_ref
        if tblock:
            tblock.proj_ident = page.proj_ident
            self[1][1][0] = tblock

        # the div holding label and input text
        self[2][0].set_class_style(self.wf.inputdiv_class)

        if self.wf.label:
            self[2][0][0][0] = self.wf.label

        self[2][0][0].set_class_style(self.wf.label_class, self.wf.label_style)

        # set an id in the input field for the 'label for' tag
        self.jlabels['input_id'] = self[2][0][1].insert_id()

        self[2][0][1].attribs.update({"name":self.get_formname('input_text'), "value":self.wf.input_text})

        if self.wf.size:
            self[2][0][1].attribs["size"] = self.wf.size
        if self.wf.maxlength:
            self[2][0][1].attribs["maxlength"] = self.wf.maxlength
        if self.wf.required:
            self[2][0][1].attribs["required"] = "required"
        if self.wf.type:
            self[2][0][1].attribs["type"] = self.wf.type
        if self.wf.pattern:
            self[2][0][1].attribs["pattern"] = self.wf.pattern
        if self.wf.title:
            self[2][0][1].attribs["title"] = self.wf.title

        if self.wf.input_accepted_class:
            self.jlabels['input_accepted_class'] = self.wf.input_accepted_class
        if self.wf.input_errored_class:
            self.jlabels['input_errored_class'] = self.wf.input_errored_class

        if self.wf.input_class:
            input_class = self.wf.input_class
        else:
            input_class = ''

        if self.error_status and self.wf.input_errored_class:
            if input_class:
                input_class = input_class + ' ' + self.wf.input_errored_class
            else:
                input_class = self.wf.input_errored_class
        elif self.wf.set_input_errored and self.wf.input_errored_class:
            if input_class:
                input_class = input_class + ' ' + self.wf.input_errored_class
            else:
                input_class = self.wf.input_errored_class
        elif self.wf.set_input_accepted and self.wf.input_accepted_class:
            if input_class:
                input_class = input_class + ' ' + self.wf.input_accepted_class
            else:
                input_class = self.wf.input_accepted_class

        if input_class:
            self[2][0][1].attribs["class"] = input_class

        # set the label 'for' attribute
        self[2][0][0].attribs['for'] = self.jlabels['input_id']

        # the div holding button
        if self.wf.buttondiv_class:
            self[2][1].attribs["class"] = self.wf.buttondiv_class

        if self.wf.button_label:
            self[2][1][0][0] = self.wf.button_label

        self[2][1][0].set_class_style(self.wf.button_label_class, self.wf.button_label_style)

        # submit button
        self[2][1][1].attribs["value"] = self.wf.button_text
        # set an id in the submit button for the 'label for' tag
        submit_id = self[2][1][1].insert_id()
        # the button class
        if self.wf.button_class:
            self[2][1][1].attribs["class"] = self.wf.button_class

        # set the label 'for' attribute
        self[2][1][0].attribs['for'] = submit_id

        # add ident and four hidden fields
        self.add_hiddens(self[2], page)


    def _build_js(self, page, ident_list, environ, call_data, lang):
        """Sets a submit event handler"""
        ident=self.get_id()
        return f"""  $("#{ident} form").on("submit input", function(e) {{
    SKIPOLE.widgets["{ident}"].eventfunc(e);
    }});
"""

    @classmethod
    def description(cls):
        """Returns a text string to illustrate the widget"""
        return """
<div> <!-- with widget id and class widget_class -->
  <div> <!-- normally hidden div, with class error_class -->
    <p> <!-- Any error text appears here --> </p>
  </div>
  <div> <!-- class attribute set to outer_class -->
    <p><!-- Paragraph 1, hidden if show_para1 is False -->
      <!-- Containing para_text -->
    </p>
    <p><!-- Paragraph 2, hidden if show_para2 is False -->
      <!-- Contains TextBlock -->
    </p>
  <div>
  <form method="post"> <!-- action attribute set to action field -->
    <div> <!-- class attribute set to inputdiv_class -->
      <label> <!-- with class set to label_class and content to label -->
      </label>
      <input type=\"text\" /> <!-- input text value set to input_text -->
    </div>
    <div> <!-- class attribute set to buttondiv_class -->
      <label> <!-- with class set to button_label_class and content to button_label -->
      </label>
      <input type=\"submit\" /> <!-- button value set to button_text and class to button_class -->
    </div>
    <!-- hidden input fields -->
  </form>    
</div>"""


class TwoInputsSubmit1(Widget):
    """Defines a form containing two text input fields."""

    error_location = (0,0,0)

    # js_validators is a class attribute, True if javascript validation is enabled
    js_validators=True

    arg_descriptions = {'action':FieldArg("url", ''),
                        'action_json':FieldArg("url", ''),
                        'error_class':FieldArg("cssclass", ""),
                        'inputdiv_class':FieldArg("cssclass", ''),
                        'label':FieldArg("text", 'Your input:'),
                        'label_class':FieldArg("cssclass", ''),
                        'label_style':FieldArg("cssstyle", ''),
                        'hidden_field1':FieldArg("text", '', valdt=True, jsonset=True),
                        'hidden_field2':FieldArg("text", '', valdt=True, jsonset=True),
                        'hidden_field3':FieldArg("text", '', valdt=True, jsonset=True),
                        'hidden_field4':FieldArg("text", '', valdt=True, jsonset=True),
                        'button_text':FieldArg("text", 'Submit'),
                        'button_class':FieldArg("cssclass", ''),
                        'input_text1':FieldArg("text", '', valdt=True, jsonset=True),
                        'size1':FieldArg("text", ''),
                        'maxlength1':FieldArg("text", ''),
                        'disabled1':FieldArg("boolean", False),
                        'required1':FieldArg("boolean", False),
                        'type1':FieldArg("text", 'text'),
                        'pattern1':FieldArg("text", ''),
                        'title1':FieldArg("text", ''),
                        'set_input_accepted1':FieldArg("boolean", False, jsonset=True),
                        'set_input_errored1':FieldArg("boolean", False, jsonset=True),
                        'input_text2':FieldArg("text", '', valdt=True, jsonset=True),
                        'size2':FieldArg("text", ''),
                        'maxlength2':FieldArg("text", ''),
                        'disabled2':FieldArg("boolean", False),
                        'required2':FieldArg("boolean", False),
                        'type2':FieldArg("text", 'text'),
                        'pattern2':FieldArg("text", ''),
                        'title2':FieldArg("text", ''),
                        'set_input_accepted2':FieldArg("boolean", False, jsonset=True),
                        'set_input_errored2':FieldArg("boolean", False, jsonset=True),
                        'input_class1':FieldArg("cssclass", ''),
                        'input_class2':FieldArg("cssclass", ''),
                        'input_accepted_class':FieldArg("cssclass", ''),
                        'input_errored_class':FieldArg("cssclass", '')
                       }


    def __init__(self, name=None, brief='', **field_args):
        """
        action: The page ident this button links to
        action_json:  if a value set, and client has jscript enabled, this is the page ident, label, url this button links to, expects a json page back
        error_class: The class applied to the paragraph containing the error message on error.
        inputdiv_class: the class attribute of the tag which contains the label and inputs
        label: The text displayed to the left of the text input field
        label_class: The css class of the label
        hidden_field1: A hidden field value, leave blank if unused, name used as the get field name
        hidden_field2: A second hidden field value, leave blank if unused, name used as the get field name
        hidden_field3: A third hidden field value, leave blank if unused, name used as the get field name
        hidden_field4: A fourth hidden field value, leave blank if unused, name used as the get field name
        button_text: The text on the button
        button_class: the class attribute of the button
        input_accepted_class: A class which can be set on each input field
        input_errored_class: A class which can be set on each input field
        input_text1: The default text in the first text input field, field name used as the name attribute
        input_class1: Class set on the first input field
        size1: The number of characters appearing in the first text input area
        maxlength1: The maximum number of characters accepted in the first text area
        disabled1: Set True if the first input field is to be disabled
        required1: Set True to put the 'required' flag into the first input field
        type1: the type set on the first input field, such as text or email
        pattern1: regular expression pattern for first input field
        title1: helps describe the pattern of the first input field
        input_text2: The default text in the second text input field, field name used as the name attribute
        input_class2: Class set on the second input field
        size2: The number of characters appearing in the second text input area
        maxlength2: The maximum number of characters accepted in the second text area
        disabled2: Set True if the second field is to be disabled
        required2: Set True to put the 'required' flag into the second input field
        type2: the type set on the second input field, such as text or email
        pattern2: regular expression pattern for the second input field
        title2: helps describe the pattern of the second input field
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
        # the first text input field
        self[1][0][1] = tag.ClosedPart(tag_name="input", attribs ={"type":"text"})
        # the second text input field
        self[1][0][2] = tag.ClosedPart(tag_name="input", attribs ={"type":"text"})
        # the submit button
        self[1][0][3] = tag.ClosedPart(tag_name="input", attribs={"type":"submit"})


    def _build(self, page, ident_list, environ, call_data, lang):
        "build the form"

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
        self[1].attribs["action"] = actionurl

        # any label:value added to self.jlabels will be set in a javascript fieldvalues attribute for the widget
        jsonurl = self.get_url(self.wf.action_json)
        if jsonurl:
            self.jlabels['url'] = jsonurl

        if self.wf.error_class:
            self[0].attribs["class"] = self.wf.error_class
        if self.error_status:
            self[0].del_one_attrib("style")


        # the div holding label, input text and button
        if self.wf.inputdiv_class:
            self[1][0].attribs["class"] = self.wf.inputdiv_class

        # set up label
        if self.wf.label:
            self[1][0][0][0] = self.wf.label
        self[1][0][0].set_class_style(self.wf.label_class, self.wf.label_style)

        # first input field
        self[1][0][1].attribs.update({"name":self.get_formname('input_text1'), "value":self.wf.input_text1})

        if self.wf.size1:
            self[1][0][1].attribs["size"] = self.wf.size1
        if self.wf.maxlength1:
            self[1][0][1].attribs["maxlength"] = self.wf.maxlength1
        if self.wf.disabled1:
            self[1][0][1].attribs["disabled"] = "disabled"
        if self.wf.required1:
            self[1][0][1].attribs["required"] = "required"
        if self.wf.type1:
            self[1][0][1].attribs["type"] = self.wf.type1
        if self.wf.pattern1:
            self[1][0][1].attribs["pattern"] = self.wf.pattern1
        if self.wf.title1:
            self[1][0][1].attribs["title"] = self.wf.title1

        if self.wf.input_class1:
            input_class1 = self.wf.input_class1
        else:
            input_class1 = ''

        if self.error_status and self.wf.input_errored_class:
            if input_class1:
                input_class1 = input_class1 + ' ' + self.wf.input_errored_class
            else:
                input_class1 = self.wf.input_errored_class
        elif self.wf.set_input_errored1 and self.wf.input_errored_class:
            if input_class1:
                input_class1 = input_class1 + ' ' + self.wf.input_errored_class
            else:
                input_class1 = self.wf.input_errored_class
        elif self.wf.set_input_accepted1 and self.wf.input_accepted_class:
            if input_class1:
                input_class1 = input_class1 + ' ' + self.wf.input_accepted_class
            else:
                input_class1 = self.wf.input_accepted_class

        if input_class1:
            self[1][0][1].attribs["class"] = input_class1


        # second input field
        self[1][0][2].attribs.update({"name":self.get_formname('input_text2'), "value":self.wf.input_text2})

        if self.wf.size2:
            self[1][0][2].attribs["size"] = self.wf.size2
        if self.wf.maxlength2:
            self[1][0][2].attribs["maxlength"] = self.wf.maxlength2
        if self.wf.disabled2:
            self[1][0][2].attribs["disabled"] = "disabled"
        if self.wf.required2:
            self[1][0][2].attribs["required"] = "required"
        if self.wf.type2:
            self[1][0][2].attribs["type"] = self.wf.type2
        if self.wf.pattern2:
            self[1][0][2].attribs["pattern"] = self.wf.pattern2
        if self.wf.title2:
            self[1][0][2].attribs["title"] = self.wf.title2

        if self.wf.input_class2:
            input_class2 = self.wf.input_class2
        else:
            input_class2 = ''

        if self.error_status and self.wf.input_errored_class:
            if input_class2:
                input_class2 = input_class2 + ' ' + self.wf.input_errored_class
            else:
                input_class2 = self.wf.input_errored_class
        elif self.wf.set_input_errored2 and self.wf.input_errored_class:
            if input_class2:
                input_class2 = input_class2 + ' ' + self.wf.input_errored_class
            else:
                input_class2 = self.wf.input_errored_class
        elif self.wf.set_input_accepted2 and self.wf.input_accepted_class:
            if input_class2:
                input_class2 = input_class2 + ' ' + self.wf.input_accepted_class
            else:
                input_class2 = self.wf.input_accepted_class

        if input_class2:
            self[1][0][2].attribs["class"] = input_class2

        if self.wf.input_accepted_class:
            self.jlabels['input_accepted_class'] = self.wf.input_accepted_class
        if self.wf.input_errored_class:
            self.jlabels['input_errored_class'] = self.wf.input_errored_class


        # submit button
        self[1][0][3].attribs["value"] = self.wf.button_text
        # the button class
        if self.wf.button_class:
            self[1][0][3].attribs["class"] = self.wf.button_class

        # set an id in the first input field for the 'label for' tag
        submit_id = self[1][0][1].insert_id()
        # set the label 'for' attribute
        self[1][0][0].attribs['for'] = submit_id

        # add ident and four hidden fields
        self.add_hiddens(self[1], page)


    def _build_js(self, page, ident_list, environ, call_data, lang):
        """Sets a submit event handler"""
        ident=self.get_id()
        return f"""  $("#{ident} form").on("submit input", function(e) {{
    SKIPOLE.widgets["{ident}"].eventfunc(e);
    }});
"""


    @classmethod
    def description(cls):
        """Returns a text string to illustrate the widget"""
        return """
<div> <!-- with widget id and class widget_class -->
  <div> <!-- normally hidden div, with class error_class -->
    <p> <!-- Any error text appears here --> </p>
  </div>
  <form method="post"> <!-- action attribute set to action field -->
    <div> <!-- class attribute set to inputdiv_class -->
      <label> <!-- with class set to label_class and content to label -->
      </label>
      <input type=\"text\" /> <!-- input text value set to input_text1, class to input_class1 -->
      <input type=\"text\" /> <!-- input text value set to input_text2, class to input_class2 -->
      <input type=\"submit\" /> <!-- button value set to button_text and class to button_class -->
    </div>
    <!-- hidden input fields -->    
  </form>
</div>"""


class SubmitDict1(Widget):
    """Defines a form with a list of input fields followed by a single submit button
       to allow a client to input a dictionary"""

    display_errors = False

    arg_descriptions = {'action':FieldArg("url", ''),
                        'button_text':FieldArg("text", "Submit"),
                        'button_class':FieldArg("cssclass", ''),
                        'input_dict':FieldArgDict('text', valdt=False, senddict=True),
                        'input_class':FieldArg("cssclass", ''),
                        'inputdiv_class':FieldArg("cssclass", ''),
                        'inputdiv_style':FieldArg("cssstyle", ''),
                        'ul_class':FieldArg("cssclass", ""),
                        'ul_style':FieldArg("cssstyle", ""),
                        'li_class':FieldArg("cssclass", ""),
                        'li_style':FieldArg("cssstyle", ""),
                        'hidden_field1':FieldArg("text", '', valdt=True, jsonset=True),
                        'hidden_field2':FieldArg("text", '', valdt=True, jsonset=True),
                        'hidden_field3':FieldArg("text", '', valdt=True, jsonset=True),
                        'hidden_field4':FieldArg("text", '', valdt=True, jsonset=True)
                       }

    def __init__(self, name=None, brief='', **field_args):
        """
        action: The label or ident of the action page
        button_text: text appearing on the button
        button_class: The css class of the button
        input_dict: an ordered dictionary, keys used in the field name, values are the text input
        input_class: Class set on each input field
        ul_class: Unordered list class
        ul_style: Style applied to ul element
        li_class: list element class
        li_style: Style applied to li element
        hidden_field1: A hidden field value, leave blank if unused, name used as the get field name
        hidden_field2: A second hidden field value, leave blank if unused, name used as the get field name
        hidden_field3: A third hidden field value, leave blank if unused, name used as the get field name
        hidden_field4: A fourth hidden field value, leave blank if unused, name used as the get field name
        """
        Widget.__init__(self, name=name, brief=brief, **field_args)
        self.tag_name = "div"
        # The form
        self[0] = tag.Part(tag_name='form', attribs={"method":"post"})
        self[0][0] = tag.Part(tag_name='ul')
        # the submit button in a div
        self[0][1] = tag.Part(tag_name="div")
        self[0][1][0] = tag.ClosedPart(tag_name="input")

    def _build(self, page, ident_list, environ, call_data, lang):
        "Build the form and list"

        input_dict = self.wf.input_dict
        if not input_dict:
            self.show = False
            return

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
        self[0].attribs["action"] = actionurl

        self[0][0].set_class_style(self.wf.ul_class, self.wf.ul_style)

        li_class =  self.wf.li_class

        input_name = self.get_formname("input_dict") + '-'

        if self.wf.input_class:
            input_class = self.wf.input_class
        else:
            input_class = ''

        linumber = -1
        for key, value in input_dict.items():
            keyed_name = input_name + key
            if input_class:
                li_input = tag.ClosedPart(tag_name="input",
                                          attribs ={"name":keyed_name,
                                                    "value":value,
                                                    "type":"text",
                                                    "class":input_class})
            else:
                li_input = tag.ClosedPart(tag_name="input",
                                          attribs ={"name":keyed_name,
                                                    "value":value,
                                                    "type":"text"})
            linumber += 1
            if li_class:
                self[0][0][linumber] = tag.Part(tag_name="li", attribs ={"class":li_class})
            else:
                self[0][0][linumber] = tag.Part(tag_name="li")
            if self.wf.li_style:
                self[0][0][linumber].attribs["style"] = self.wf.li_style

            self[0][0][linumber][0] = li_input

        # list done, now for submit button

        # the div holding button
        self[0][1].set_class_style(self.wf.inputdiv_class, self.wf.inputdiv_style)

        if self.wf.button_class:
            self[0][1][0].attribs = {"value":self.wf.button_text, "type":"submit", "class":self.wf.button_class}
        else:
            self[0][1][0].attribs = {"value":self.wf.button_text, "type":"submit"}

        # add ident and four hidden fields
        self.add_hiddens(self[0], page)


    @classmethod
    def description(cls):
        """Returns a text string to illustrate the widget"""
        return """
<div> <!-- with widget id and class widget_class -->
  <form method=\"post\"> <!-- action attribute set to action field -->
    <ul> <!-- with class set to ul_class and style to ul_style -->
      <!-- a li is created for each value in the input_dict dictionary -->
      <li>  <!-- with class set to li_class and style to li_style -->
        <input type="text" /> <!-- with CSS class input_class -->
             <!-- and with input name 'widgetname:input_dict-keyname' -->
      </li>
    </ul>
    <div> <!-- class attribute set to inputdiv_class, style to inputdiv_style -->
      <input type="submit" /> <!-- with value button_text, and CSS class button_class -->
    </div>
    <!-- hidden fields -->
  </form>
</div>"""



class SubmitTextInput2(Widget):
    """Defines a form with a text input field, and four hidden fields
       Can send session or local storage values."""

    # js_validators is a class attribute, True if javascript validation is enabled
    js_validators=True

    error_location = (0,0,0)

    arg_descriptions = {'label':FieldArg("text", 'Your input:'),
                        'label_class':FieldArg("cssclass", ''),
                        'label_style':FieldArg("cssstyle", ''),
                        'action_json':FieldArg("url", ''),
                        'action':FieldArg("url", ''),
                        'hidden_field1':FieldArg("text", '', valdt=True, jsonset=True),
                        'hidden_field2':FieldArg("text", '', valdt=True, jsonset=True),
                        'hidden_field3':FieldArg("text", '', valdt=True, jsonset=True),
                        'hidden_field4':FieldArg("text", '', valdt=True, jsonset=True),
                        'session_storage':FieldArg("text", "", valdt=True, jsonset=True),
                        'local_storage':FieldArg("text","", valdt=True, jsonset=True),
                        'target':FieldArg("text",''),
                        'button_text':FieldArg("text",'Submit'),
                        'button_class':FieldArg("cssclass", ''),
                        'inputdiv_class':FieldArg("cssclass", ''),
                        'inputandbutton_class':FieldArg("cssclass", ''),
                        'inputandbutton_style':FieldArg("cssstyle", ''),
                        'error_class':FieldArg("cssclass", ''),
                        'input_text':FieldArg("text", '', valdt=True, jsonset=True),
                        'size':FieldArg("text", ''),
                        'maxlength':FieldArg("text", ''),
                        'required':FieldArg("boolean", False),
                        'type':FieldArg("text", 'text'),
                        'pattern':FieldArg("text", ''),
                        'title':FieldArg("text", ''),
                        'input_accepted_class':FieldArg("cssclass", ''),
                        'input_errored_class':FieldArg("cssclass", ''),
                        'input_class':FieldArg("cssclass", ''),
                        'set_input_accepted':FieldArg("boolean", False, jsonset=True),
                        'set_input_errored':FieldArg("boolean", False, jsonset=True),
                        'hide':FieldArg("boolean", False, jsonset=True)
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
        session_storage: A session storage key, this widgfield returns the stored value if anything
        local_storage: A local storage key, this widgfield returns the stored value if anything
        target: if given, the target attribute will be set
        button_text: The text on the button
        button_class: The class given to the button tag
        inputdiv_class: the class attribute of the div which contains the label, input text and button
        inputandbutton_class: the class attribute of the span which contains the input text and button
        error_class: The class applied to the paragraph containing the error message on error.
        input_text: The default text in the text input field, field name used as the name attribute
        size: The number of characters appearing in the text input area
        maxlength: The maximum number of characters accepted in the text area
        required: Set True to put the 'required' flag into the input field
        type: the type set on the input field, such as text or email
        pattern: regular expression pattern
        title: helps describe the pattern
        input_accepted_class: A class which can be set on the input field
        input_errored_class: A class which can be set on the input field
        input_class: Class set on the input field
        set_input_accepted: If True, input_accepted_class will be set on the input field
        set_errored_accepted: If True, input_errored_class will be set on the input field
        hide: If True, widget is hidden
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
        # the text input field
        self[1][0][1][0] = tag.ClosedPart(tag_name="input", attribs ={"type":"text"})
        # the submit button
        self[1][0][1][1] = tag.Part(tag_name="button", attribs ={"type":"submit"})
        self[1][0][1][1][0] = "Submit"


    def _build(self, page, ident_list, environ, call_data, lang):
        "build the form"
        if self.wf.target:
            self[1].attribs["target"] = self.wf.target
        # Hides widget if no error and hide is True
        self.widget_hide(self.wf.hide)

        if self.wf.error_class:
            self[0].attribs["class"] = self.wf.error_class
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

        jsonurl = self.get_url(self.wf.action_json)
        # any label:value added to self.jlabels will be set in a javascript fieldvalues attribute for the widget
        if jsonurl:
            self.jlabels['url'] = jsonurl
        if self.wf.input_accepted_class:
           self.jlabels['input_accepted_class'] = self.wf.input_accepted_class
        if self.wf.input_errored_class:
           self.jlabels['input_errored_class'] = self.wf.input_errored_class
        if self.wf.session_storage:
           self.jlabels['session_storage'] = self.wf.session_storage
        if self.wf.local_storage:
           self.jlabels['local_storage'] = self.wf.local_storage

        # update the action of the form
        self[1].attribs["action"] = actionurl
        # the div holding label, input text and button
        if self.wf.inputdiv_class:
            self[1][0].attribs["class"] = self.wf.inputdiv_class

        self[1][0][0].set_class_style(self.wf.label_class, self.wf.label_style)
        if self.get_field_value('label'):
            self[1][0][0][0] = self.wf.label

        # the span holding input text and button
        self[1][0][1].set_class_style(self.wf.inputandbutton_class, self.wf.inputandbutton_style)

        # set an id in the input field for the 'label for' tag
        self.jlabels['input_id'] = self[1][0][1][0].insert_id()
        # set the label 'for' attribute
        self[1][0][0].attribs['for'] = self.jlabels['input_id']

        self[1][0][1][0].attribs["name"] = self.get_formname('input_text')
        self[1][0][1][0].attribs["value"] = self.wf.input_text

        if self.wf.size:
            self[1][0][1][0].attribs["size"] = self.wf.size
        if self.wf.maxlength:
            self[1][0][1][0].attribs["maxlength"] = self.wf.maxlength
        if self.wf.required:
            self[1][0][1][0].attribs["required"] = "required"
        if self.wf.type:
            self[1][0][1][0].attribs["type"] = self.wf.type
        if self.wf.pattern:
            self[1][0][1][0].attribs["pattern"] = self.wf.pattern
        if self.wf.title:
            self[1][0][1][0].attribs["title"] = self.wf.title


        if self.wf.input_class:
            input_class = self.wf.input_class
        else:
            input_class = ''

        if self.error_status and self.wf.input_errored_class:
            if input_class:
                input_class = input_class + ' ' + self.wf.input_errored_class
            else:
                input_class = self.wf.input_errored_class
        elif self.wf.set_input_errored and self.wf.input_errored_class:
            if input_class:
                input_class = input_class + ' ' + self.wf.input_errored_class
            else:
                input_class =self.wf.input_errored_class
        elif self.wf.set_input_accepted and self.wf.input_accepted_class:
            if input_class:
                input_class = input_class + ' ' + self.wf.input_accepted_class
            else:
                input_class = self.wf.input_accepted_class

        if input_class:
            self[1][0][1][0].attribs["class"] = input_class

        # submit button
        if self.wf.button_class:
            self[1][0][1][1].attribs["class"] = self.wf.button_class
        if self.wf.button_text:
            self[1][0][1][1][0] = self.wf.button_text

        # add ident and four hidden fields
        self.add_hiddens(self[1], page)



    def _build_js(self, page, ident_list, environ, call_data, lang):
        """Sets a submit event handler"""
        ident=self.get_id()
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
      <label> <!-- with class set to label_class and content to label, for set to input text id -->
      </label>
      <span>  <!-- class attribute set to inputandbutton_class -->
          <input type="text" />  <!-- class set to input_class -->
            <!-- input text value set to input_text -->
          <button type="submit"> <!-- with class set to button_class -->
            <!-- button_text -->
          </button>
      </span>
    </div>
    <!-- hidden input fields -->                              
  </form>
</div>"""



class SubmitTextInput4(Widget):
    """Defines a form with a text input field, and four hidden fields"""

    # js_validators is a class attribute, True if javascript validation is enabled
    js_validators=True

    error_location = (0,0,0)

    arg_descriptions = {'left_text':FieldArg("text", 'Your input:'),
                        'left_class':FieldArg("cssclass", ''),
                        'left_style':FieldArg("cssstyle", ''),
                        'leftdiv_class':FieldArg("cssclass", ''),
                        'leftdiv_style':FieldArg("cssstyle", ''),
                        'action_json':FieldArg("url", ''),
                        'action':FieldArg("url", ''),
                        'error_class':FieldArg("cssclass", ''),
                        'hidden_field1':FieldArg("text", '', valdt=True, jsonset=True),
                        'hidden_field2':FieldArg("text", '', valdt=True, jsonset=True),
                        'hidden_field3':FieldArg("text", '', valdt=True, jsonset=True),
                        'hidden_field4':FieldArg("text", '', valdt=True, jsonset=True),
                        'target':FieldArg("text",''),
                        'button_text':FieldArg("text",'Submit'),
                        'button_class':FieldArg("cssclass", ''),
                        'formdiv_class':FieldArg("cssclass", ''),
                        'formdiv_style':FieldArg("cssstyle", ''),
                        'inputdiv_class':FieldArg("cssclass", ''),
                        'inputdiv_style':FieldArg("cssstyle", ''),
                        'buttondiv_class':FieldArg("cssclass", ''),
                        'buttondiv_style':FieldArg("cssstyle", ''),
                        'input_text':FieldArg("text", '', valdt=True, jsonset=True),
                        'size':FieldArg("text", ''),
                        'maxlength':FieldArg("text", ''),
                        'required':FieldArg("boolean", False),
                        'type':FieldArg("text", 'text'),
                        'pattern':FieldArg("text", ''),
                        'title':FieldArg("text", ''),
                        'input_accepted_class':FieldArg("cssclass", ''),
                        'input_errored_class':FieldArg("cssclass", ''),
                        'input_class':FieldArg("cssclass", ''),
                        'input_style':FieldArg("cssstyle", ''),
                        'set_input_accepted':FieldArg("boolean", False, jsonset=True),
                        'set_input_errored':FieldArg("boolean", False, jsonset=True),
                        'hide':FieldArg("boolean", False, jsonset=True)
                       }

    def __init__(self, name=None, brief='', **field_args):
        """
        left_text: The text displayed to the left of the text input field
        leftdiv_class: The css class of the div containing the left paragraph
        leftdiv_style: The css style of the div containing the left paragraph
        left_class: The css class of the p tag containing left_text
        left_style: The css style of the p tag containing left_text
        action_json:  if a value set, and client has jscript enabled, this is the page ident, label, url this button links to, expects a json page back
        action: The page ident, label, url this button links to, overridden if action_json is set.
        error_class: The class applied to the paragraph containing the error message on error.
        hidden_field1: A hidden field value, leave blank if unused, name used as the get field name
        hidden_field2: A second hidden field value, leave blank if unused, name used as the get field name
        hidden_field3: A third hidden field value, leave blank if unused, name used as the get field name
        hidden_field4: A fourth hidden field value, leave blank if unused, name used as the get field name
        target: if given, the target attribute will be set
        button_text: The text on the button
        button_class: The class given to the button tag
        formdiv_class: the class attribute of the div which contains the left text, input field and button
        formdiv_style: the style attribute of the div which contains the left text, input field and button
        inputdiv_class: the class attribute of the div which contains the input field
        inputdiv_style: the style attribute of the div which contains the input field
        buttondiv_class: the class attribute of the div which contains the submit button
        buttondiv_style: the style attribute of the div which contains the submit button
        input_text: The default text in the text input field, field name used as the name attribute
        size: The number of characters appearing in the text input area
        maxlength: The maximum number of characters accepted in the text area
        required: Set True to put the 'required' flag into the input field
        type: the type set on the input field, such as text or email
        pattern: regular expression pattern
        title: helps describe the pattern
        input_accepted_class: A class which can be set on the input field
        input_errored_class: A class which can be set on the input field
        input_class: Class set on the input field
        input_style: Style set on the input field
        set_input_accepted: If True, input_accepted_class will be set on the input field
        set_errored_accepted: If True, input_errored_class will be set on the input field
        hide: If True, widget is hidden
        """
        Widget.__init__(self, name=name, brief=brief, **field_args)
        self.tag_name = "div"
        # error div at 0
        self[0] = tag.Part(tag_name="div", attribs={"style":"display:none;"})
        self[0][0] = tag.Part(tag_name="p")
        self[0][0][0] = ''

        # The form
        self[1] = tag.Part(tag_name='form', attribs={"role":"form", "method":"post"})

        # div containing left text, input text and button
        self[1][0] = tag.Part(tag_name='div')
        # the left div
        self[1][0][0] = tag.Part(tag_name="div", hide_if_empty=True)
        # the left paragraph
        self[1][0][0][0] = tag.Part(tag_name="p", hide_if_empty=True)
        # div containing input field
        self[1][0][1] = tag.Part(tag_name='div')
        # the text input field
        self[1][0][1][0] = tag.ClosedPart(tag_name="input", attribs ={"type":"text"})
        # div containing the submit button
        self[1][0][2] = tag.Part(tag_name='div')
        # the submit button
        self[1][0][2][0] = tag.Part(tag_name="button", attribs ={"type":"submit"})
        self[1][0][2][0][0] = "Submit"


    def _build(self, page, ident_list, environ, call_data, lang):
        "build the form"
        if self.wf.target:
            self[1].attribs["target"] = self.wf.target
        # Hides widget if no error and hide is True
        self.widget_hide(self.wf.hide)

        if self.wf.error_class:
            self[0].attribs["class"] = self.wf.error_class
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

        jsonurl = self.get_url(self.wf.action_json)
        # any label:value added to self.jlabels will be set in a javascript fieldvalues attribute for the widget
        if jsonurl:
            self.jlabels['url'] = jsonurl
        if self.wf.input_accepted_class:
           self.jlabels['input_accepted_class'] = self.wf.input_accepted_class
        if self.wf.input_errored_class:
           self.jlabels['input_errored_class'] = self.wf.input_errored_class


        # update the action of the form
        self[1].attribs["action"] = actionurl
        # the div holding label, input text and button
        self[1][0].set_class_style(self.wf.formdiv_class, self.wf.formdiv_style)

        self[1][0][0].set_class_style(self.wf.leftdiv_class, self.wf.leftdiv_style)

        self[1][0][0][0].set_class_style(self.wf.left_class, self.wf.left_style)
        if self.wf.left_text:
            self[1][0][0][0][0] = self.wf.left_text

        # the div holding the input field
        self[1][0][1].set_class_style(self.wf.inputdiv_class, self.wf.inputdiv_style)

        # set an id in the input field
        self.jlabels['input_id'] = self[1][0][1][0].insert_id()

        self[1][0][1][0].attribs["name"] = self.get_formname('input_text')
        self[1][0][1][0].attribs["value"] = self.wf.input_text

        if self.wf.size:
            self[1][0][1][0].attribs["size"] = self.wf.size
        if self.wf.maxlength:
            self[1][0][1][0].attribs["maxlength"] = self.wf.maxlength
        if self.wf.required:
            self[1][0][1][0].attribs["required"] = "required"
        if self.wf.type:
            self[1][0][1][0].attribs["type"] = self.wf.type
        if self.wf.pattern:
            self[1][0][1][0].attribs["pattern"] = self.wf.pattern
        if self.wf.title:
            self[1][0][1][0].attribs["title"] = self.wf.title
        if self.wf.input_style:
            self[1][0][1][0].attribs["style"] = self.wf.input_style


        if self.wf.input_class:
            input_class = self.wf.input_class
        else:
            input_class = ''

        if self.error_status and self.wf.input_errored_class:
            if input_class:
                input_class = input_class + ' ' + self.wf.input_errored_class
            else:
                input_class = self.wf.input_errored_class
        elif self.wf.set_input_errored and self.wf.input_errored_class:
            if input_class:
                input_class = input_class + ' ' + self.wf.input_errored_class
            else:
                input_class =self.wf.input_errored_class
        elif self.wf.set_input_accepted and self.wf.input_accepted_class:
            if input_class:
                input_class = input_class + ' ' + self.wf.input_accepted_class
            else:
                input_class = self.wf.input_accepted_class

        if input_class:
            self[1][0][1][0].attribs["class"] = input_class

        # the div holding the button
        self[1][0][2].set_class_style(self.wf.buttondiv_class, self.wf.buttondiv_style)
        # submit button
        if self.wf.button_class:
            self[1][0][2][0].attribs["class"] = self.wf.button_class
        if self.wf.button_text:
            self[1][0][2][0][0] = self.wf.button_text
        # add ident and four hidden fields
        self.add_hiddens(self[1], page)


    def _build_js(self, page, ident_list, environ, call_data, lang):
        """Sets a submit event handler"""
        ident=self.get_id()
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
    <div> <!-- class attribute set to formdiv_class -->
      <div> <!-- class set to leftdiv_class -->
          <p>  <!-- class set to left_class -->
              <!-- content set to left_text -->
          </p>
      </div>
      <div>  <!-- class attribute set to inputdiv_class -->
          <input type="text" />  <!-- class set to input_class -->
            <!-- input text value set to input_text -->
      </div>
      <div>  <!-- class attribute set to buttondiv_class -->
          <button type="submit"> <!-- with class set to button_class -->
            <!-- button_text -->
          </button>
      </div>
    </div>
    <!-- hidden input fields -->                              
  </form>
</div>"""



