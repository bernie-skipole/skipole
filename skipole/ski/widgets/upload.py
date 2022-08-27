


"""Contains widgets for uploading files"""


from .. import tag
from . import Widget, ClosedWidget, FieldArg, FieldArgList, FieldArgTable, FieldArgDict


class SubmitUploadFile1(Widget):
    """Defines a form with a file input field"""

    error_location = (0,0,0)

    arg_descriptions = {'filebutton_label':FieldArg("text", ''),
                        'filebuttonlabel_class':FieldArg("cssclass", ''),
                        'filebutton_class':FieldArg("cssclass", ''),
                        'action':FieldArg("url", '', valdt=True),
                        'submitbutton_label':FieldArg("text", ''),
                        'submitbuttonlabel_class':FieldArg("cssclass", ''),
                        'submitbuttonlabel_style':FieldArg("cssstyle", ''),
                        'submitbutton_text':FieldArg("text",'Submit'),
                        'submitbutton_class':FieldArg("cssclass", ''),
                        'fileinputdiv_class':FieldArg("cssclass", ''),
                        'submitinputdiv_class':FieldArg("cssclass", ''),
                        'error_class':FieldArg("cssclass", ''),
                        'required':FieldArg("boolean", False),
                        'hide':FieldArg("boolean", False, jsonset=True),
                        'hidden_field1':FieldArg("text", '', valdt=True, jsonset=True),
                        'hidden_field2':FieldArg("text", '', valdt=True, jsonset=True),
                        'hidden_field3':FieldArg("text", '', valdt=True, jsonset=True),
                        'hidden_field4':FieldArg("text", '', valdt=True, jsonset=True)
                       }

    def __init__(self, name=None, brief='', **field_args):
        """
        filebutton_label: The text displayed to the left of the file button
        filebuttonlabel_class: The css class of the label
        filebutton_class: The css class of the file browse button
        action: The ident or label to send this file to, name of this field is used as widgfield fieldname
        submitbutton_text: The text on the button
        submitbutton_label: The text displayed to the left of the submit button
        submitbuttonlabel_class: The css class of the label
        submitbuttonlabel_style: The css style of the label
        submitbutton_class: The css class of the submit button
        fileinputdiv_class: the class attribute of the div which contains the file label and button
        submitinputdiv_class: the class attribute of the div which contains the submit label and button
        error_class: The class applied to the paragraph containing the error message on error.
        required: Set True to put the 'required' flag into the input field
        hide: If True, widget is hidden
        hidden_field1: A hidden field value, leave blank if unused, name used as the get field name
        hidden_field2: A second hidden field value, leave blank if unused, name used as the get field name
        hidden_field3: A third hidden field value, leave blank if unused, name used as the get field name
        hidden_field4: A fourth hidden field value, leave blank if unused, name used as the get field name
        """
        Widget.__init__(self, name=name, brief=brief, **field_args)
        self.tag_name = "div"
        # hidden error
        self[0] = tag.Part(tag_name="div", attribs={"style":"display:none;"})
        self[0][0] = tag.Part(tag_name="p")
        self[0][0][0] = ''
        # The form
        self[1] = tag.Part(tag_name='form', attribs={"role":"form", "method":"post", "enctype":"multipart/form-data"})
        # div containing file label and button
        self[1][0] = tag.Part(tag_name='div')
        # the label
        self[1][0][0] = tag.Part(tag_name="label", hide_if_empty=True)
        # the file button field
        self[1][0][1] = tag.ClosedPart(tag_name="input", attribs ={"type":"file"})
        # div containing submit label and button
        self[1][1] = tag.Part(tag_name='div')
        # the label
        self[1][1][0] = tag.Part(tag_name="label", hide_if_empty=True)
        # the submit button
        self[1][1][1] = tag.ClosedPart(tag_name="input", attribs ={"type":"submit"})


    def _build(self, page, ident_list, environ, call_data, lang):
        "build the form"
        # Hides widget if no error and hide is True
        self.widget_hide(self.wf.hide)
        if self.wf.error_class:
            self[0].attribs["class"] = self.wf.error_class
        if self.error_status:
            del self[0].attribs["style"]
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

        # file button
        # the div holding file label and button
        if self.wf.fileinputdiv_class:
            self[1][0].attribs["class"] = self.wf.fileinputdiv_class
        if self.wf.filebutton_label:
            self[1][0][0][0] = self.wf.filebutton_label
        if self.wf.filebuttonlabel_class:
            self[1][0][0].attribs["class"] = self.wf.filebuttonlabel_class

        # set an id in the file button for the 'label for' tag      
        # and set the label 'for' attribute
        self[1][0][0].attribs['for'] = self[1][0][1].insert_id()

        self[1][0][1].attribs["name"] = self.get_formname('action')

        if self.wf.required:
            self[1][0][1].attribs["required"] = "required"
        if self.wf.filebutton_class:
            self[1][0][1].attribs["class"] = self.wf.filebutton_class

        # submit button
        # the div holding submit label and button
        if self.wf.submitinputdiv_class:
            self[1][1].attribs["class"] = self.wf.submitinputdiv_class
        if self.wf.submitbutton_label:
            self[1][1][0][0] = self.wf.submitbutton_label

        self[1][1][0].set_class_style(self.wf.submitbuttonlabel_class, self.wf.submitbuttonlabel_style)

        # submit button
        self[1][1][1].attribs["value"] = self.wf.submitbutton_text
        # set an id in the submit button for the 'label for' tag
        # and set the label 'for' attribute
        self[1][1][0].attribs['for'] = self[1][1][1].insert_id()

        if self.wf.submitbutton_class:
            self[1][1][1].attribs["class"] = self.wf.submitbutton_class

        # add ident and four hidden fields
        self.add_hiddens(self[1], page)



    @classmethod
    def description(cls):
        """Returns a text string to illustrate the widget"""
        return """
<div> <!-- with widget id and class widget_class -->
  <div>  <!-- div hidden when no error is displayed, with class set to error_class on error -->
    <p> <!-- error message appears in this paragraph --> </p>
  </div>
  <form role="form" method="post" enctype="multipart/form-data"> <!-- action attribute set to action field -->
    <div> <!-- class attribute set to fileinputdiv_class -->
      <label> <!-- with class set to filebuttonlabel_class and content to filebutton_label -->
      </label>
      <input type="file" />  <!-- class attribute set to filebutton_class -->
    </div>
    <div> <!-- class attribute set to submitinputdiv_class -->
      <label> <!-- with class set to submitbuttonlabel_class and content to submitbutton_label -->
      </label>
      <input type="submit" /> <!-- button value set to submitbutton_text and class to submitbutton_class-->
    </div>
    <!-- hidden fields -->
  </form>
</div>"""


class UploadFile1(Widget):
    """Defines a file input field"""

    error_location = (0,0,0)

    arg_descriptions = {'label':FieldArg("text", 'Pick a file to upload:'),
                        'inputname':FieldArg("text", '', valdt=True),
                        'label_class':FieldArg("cssclass", ''),
                        'label_style':FieldArg("cssstyle", ''),
                        'filebutton_class':FieldArg("cssclass", ''),
                        'inputdiv_class':FieldArg("cssclass", ''),
                        'error_class':FieldArg("cssclass", '')
                       }

    def __init__(self, name=None, brief='', **field_args):
        """
        label: The text displayed to the left of the file button
        inputname: the field name of the widgfield which is submitted
        label_class: The css class of the label
        filebutton_class: The css class of the file browse button
        inputdiv_class: The css class of the div containing the label and input field
        error_class: The class applied to the paragraph containing the error message on error.
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
        # the file button field
        self[1][1] = tag.ClosedPart(tag_name="input", attribs ={"type":"file"})


    def _build(self, page, ident_list, environ, call_data, lang):
        "build the form"
        if self.wf.error_class:
            self[0].attribs["class"] = self.wf.error_class
        if self.error_status:
            del self[0].attribs["style"]

        # file button
        # the div holding file label and button
        if self.wf.inputdiv_class:
            self[1].attribs["class"] = self.wf.inputdiv_class
        if self.wf.label:
            self[1][0][0] = self.wf.label

        self[1][0].set_class_style(self.wf.label_class, self.wf.label_style)

        # set an id in the file button for the 'label for' tag
        # and set the label 'for' attribute
        self[1][0].attribs['for'] = self[1][1].insert_id()

        self[1][1].attribs["name"] = self.get_formname('inputname')
        if self.wf.filebutton_class:
            self[1][1].attribs["class"] = self.wf.filebutton_class


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
    <input type="file" />  <!-- class attribute set to filebutton_class -->
  </div>
</div>"""


class SubmitUploadFile2(Widget):
    """Defines a form with a file input field, which also submits the filename chosen"""

    _container = ((1,1),)

    error_location = (0,0,0)

    arg_descriptions = {'filebutton_label':FieldArg("text", ''),
                        'filebuttonlabel_class':FieldArg("cssclass", ''),
                        'filebutton_class':FieldArg("cssclass", ''),
                        'action':FieldArg("url", '', valdt=True),
                        'submitbutton_label':FieldArg("text", ''),
                        'submitbuttonlabel_class':FieldArg("cssclass", ''),
                        'submitbuttonlabel_style':FieldArg("cssstyle", ''),
                        'submitbutton':FieldArg("text",'Submit', valdt=True),
                        'submitbutton_class':FieldArg("cssclass", ''),
                        'fileinputdiv_class':FieldArg("cssclass", ''),
                        'submitinputdiv_class':FieldArg("cssclass", ''),
                        'container_class':FieldArg("cssclass", ''),
                        'error_class':FieldArg("cssclass", ''),
                        'required':FieldArg("boolean", False),
                        'hide':FieldArg("boolean", False, jsonset=True),
                        'hidden_field1':FieldArg("text", '', valdt=True, jsonset=True),
                        'hidden_field2':FieldArg("text", '', valdt=True, jsonset=True),
                        'hidden_field3':FieldArg("text", '', valdt=True, jsonset=True),
                        'hidden_field4':FieldArg("text", '', valdt=True, jsonset=True)
                       }

    def __init__(self, name=None, brief='', **field_args):
        """
        filebutton_label: The text displayed to the left of the file button
        filebuttonlabel_class: The css class of the label
        filebutton_class: The css class of the file browse button
        action: The ident or label to send this file to, name of this field is used as widgfield fieldname for file contents
        submitbutton: Sets the text on the button. The name of this field is used as the widgfield fieldname for the filename
        submitbutton_label: The text displayed to the left of the submit button
        submitbuttonlabel_class: The css class of the label
        submitbuttonlabel_style: The css style of the label
        submitbutton_class: The css class of the submit button
        fileinputdiv_class: the class attribute of the div which contains the file label and button
        submitinputdiv_class: the class attribute of the div which contains the submit label and button
        container_class: the class attribute of the div holding the container
        error_class: The class applied to the paragraph containing the error message on error.
        required: Set True to put the 'required' flag into the input field
        hide: If True, widget is hidden
        hidden_field1: A hidden field value, leave blank if unused, name used as the get field name
        hidden_field2: A second hidden field value, leave blank if unused, name used as the get field name
        hidden_field3: A third hidden field value, leave blank if unused, name used as the get field name
        hidden_field4: A fourth hidden field value, leave blank if unused, name used as the get field name
        """
        Widget.__init__(self, name=name, brief=brief, **field_args)
        self.tag_name = "div"
        # hidden error
        self[0] = tag.Part(tag_name="div", attribs={"style":"display:none;"})
        self[0][0] = tag.Part(tag_name="p")
        self[0][0][0] = ''
        # The form
        self[1] = tag.Part(tag_name='form', attribs={"role":"form", "method":"post", "enctype":"multipart/form-data"})
        # div containing file label and button
        self[1][0] = tag.Part(tag_name='div')
        # the label
        self[1][0][0] = tag.Part(tag_name="label", hide_if_empty=True)
        # the file button field
        self[1][0][1] = tag.ClosedPart(tag_name="input", attribs ={"type":"file"})

        # The location 1,1 is available as a container
        self[1][1] = tag.Part(tag_name="div")
        self[1][1][0] = ''

        # div containing submit label and button
        self[1][2] = tag.Part(tag_name='div')
        # the label
        self[1][2][0] = tag.Part(tag_name="label", hide_if_empty=True)
        # the submit button
        self[1][2][1] = tag.Part(tag_name="button", attribs ={"type":"submit"})


    def _build(self, page, ident_list, environ, call_data, lang):
        "build the form"
        # Hides widget if no error and hide is True
        self.widget_hide(self.wf.hide)
        if self.wf.error_class:
            self[0].attribs["class"] = self.wf.error_class
        if self.error_status:
            del self[0].attribs["style"]
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

        # file button
        # the div holding file label and button
        if self.wf.fileinputdiv_class:
            self[1][0].attribs["class"] = self.wf.fileinputdiv_class
        if self.wf.filebutton_label:
            self[1][0][0][0] = self.wf.filebutton_label
        if self.wf.filebuttonlabel_class:
            self[1][0][0].attribs["class"] = self.wf.filebuttonlabel_class

        # set an id in the file button for the 'label for' tag
        # and set the label 'for' attribute
        self[1][0][0].attribs['for'] = self[1][0][1].insert_id()

        self[1][0][1].attribs["name"] = self.get_formname('action')

        if self.wf.required:
            self[1][0][1].attribs["required"] = "required"
        if self.wf.filebutton_class:
            self[1][0][1].attribs["class"] = self.wf.filebutton_class

        # the div holding the container
        if self.wf.container_class:
            self[1][1].attribs["class"] = self.wf.container_class

        # submit button
        # the div holding submit label and button
        if self.wf.submitinputdiv_class:
            self[1][2].attribs["class"] = self.wf.submitinputdiv_class
        if self.wf.submitbutton_label:
            self[1][2][0][0] = self.wf.submitbutton_label

        self[1][2][0].set_class_style(self.wf.submitbuttonlabel_class, self.wf.submitbuttonlabel_style)

        # set an id in the submit button for the 'label for' tag
        # and set the label 'for' attribute
        submitid = self[1][2][1].insert_id()
        self[1][2][0].attribs['for'] = submitid

        if self.wf.submitbutton_class:
            self[1][2][1].attribs["class"] = self.wf.submitbutton_class

        # set the name of the submit button, so its value will be submitted with the form
        self[1][2][1].attribs["name"] = self.get_formname('submitbutton')

        # set the submitbutton contents
        self[1][2][1][0] = self.wf.submitbutton

        # set onchange string in 101  this sets the filename as the button value
        self[1][0][1].attribs["onchange"] = f'document.getElementById("{submitid}").value=this.value'

        # add ident and four hidden fields
        self.add_hiddens(self[1], page)


    def _build_js(self, page, ident_list, environ, call_data, lang):
        """Sets a submit event handler"""
        # this ensures any input text widgets added to the container, get local validation
        # when the form is submitted
        ident = self.get_id()
        return f"""  $('#{ident} form').on("submit", function(e) {{
    SKIPOLE.widgets['{ident}'].eventfunc(e);
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
  <form role="form" method="post" enctype="multipart/form-data"> <!-- action attribute set to action field -->
    <div> <!-- class attribute set to fileinputdiv_class -->
      <label> <!-- with class set to filebuttonlabel_class and content to filebutton_label -->
      </label>
      <input type="file" />  <!-- class attribute set to filebutton_class -->
    </div>
    <div> <!-- this div has the class attribute set to container_class -->
      <!-- container 0 for further html -->
    </div>
    <div> <!-- class attribute set to submitinputdiv_class -->
      <label> <!-- with class set to submitbuttonlabel_class and content to submitbutton_label -->
      </label>
      <button type="submit">  <!-- class to submitbutton_class-->
                              <!-- value set by javascript to the fiename being submitted-->
          <!-- Text on the button set to the value given in submitbutton-->
      </button>
    </div>
    <!-- hidden fields -->
  </form>
</div>"""

