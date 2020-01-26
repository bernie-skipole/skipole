


"""Contains widgets for uploading files"""


from .. import skiboot, tag, excepts
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
        Widget.__init__(self, name=name, tag_name="div", brief=brief, **field_args)
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
        # five divs, for the hidden ident field and four hidden fields
        self[1][2] = tag.Part(tag_name='div')
        self[1][3] = tag.Part(tag_name='div')
        self[1][4] = tag.Part(tag_name='div')
        self[1][5] = tag.Part(tag_name='div')
        self[1][6] = tag.Part(tag_name='div')


    def _build(self, page, ident_list, environ, call_data, lang):
        "build the form"
        # Hides widget if no error and hide is True
        self.widget_hide(self.get_field_value("hide"))
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

        # file button
        # the div holding file label and button
        if self.get_field_value('fileinputdiv_class'):
            self[1][0].attribs = {"class": self.get_field_value('fileinputdiv_class')}
        if self.get_field_value('filebutton_label'):
            self[1][0][0][0] = self.get_field_value('filebutton_label')
        if self.get_field_value('filebuttonlabel_class'):
            self[1][0][0].attribs = {"class": self.get_field_value('filebuttonlabel_class')}

        # set an id in the file button for the 'label for' tag
        self[1][0][1].insert_id()

        self[1][0][1].update_attribs({"name":self.get_formname('action')})

        if self.get_field_value('required'):
            self[1][0][1].update_attribs({"required":"required"})
        if self.get_field_value('filebutton_class'):
            self[1][0][1].update_attribs({"class": self.get_field_value('filebutton_class')})


        # set the label 'for' attribute
        self[1][0][0].update_attribs({'for':self[1][0][1].get_id()})

        # submit button
        # the div holding submit label and button
        if self.get_field_value('submitinputdiv_class'):
            self[1][1].attribs = {"class": self.get_field_value('submitinputdiv_class')}
        if self.get_field_value('submitbutton_label'):
            self[1][1][0][0] = self.get_field_value('submitbutton_label')
        if self.get_field_value('submitbuttonlabel_class'):
            self[1][1][0].attribs = {"class": self.get_field_value('submitbuttonlabel_class')}

        # submit button
        self[1][1][1].update_attribs({"value":self.get_field_value('submitbutton_text')})
        # set an id in the submit button for the 'label for' tag
        self[1][1][1].insert_id()

        if self.get_field_value('submitbutton_class'):
            self[1][1][1].update_attribs({"class": self.get_field_value('submitbutton_class')})

        # set the label 'for' attribute
        self[1][1][0].update_attribs({'for':self[1][1][1].get_id()})

        # add ident and four hidden fields
        #self.add_hiddens(self[1], page)

        self[1][2][0] = tag.ClosedPart(tag_name="input",
                                       attribs ={"name":'ident',
                                                 "value":page.ident_data_string,
                                                 "type":"hidden"})
        # hidden field on the form
        if self.get_field_value('hidden_field1'):
            self[1][3][0] = tag.ClosedPart(tag_name="input",
                                           attribs ={"name":self.get_formname('hidden_field1'),
                                                     "value":self.get_field_value('hidden_field1'),
                                                     "type":"hidden"})

        # Second hidden field on the form
        if self.get_field_value('hidden_field2'):
            self[1][4][0] = tag.ClosedPart(tag_name="input",
                                           attribs ={"name":self.get_formname('hidden_field2'),
                                                     "value":self.get_field_value('hidden_field2'),
                                                     "type":"hidden"})

        # third hidden field on the form
        if self.get_field_value('hidden_field3'):
            self[1][5][0] = tag.ClosedPart(tag_name="input",
                                           attribs ={"name":self.get_formname('hidden_field3'),
                                                     "value":self.get_field_value('hidden_field3'),
                                                     "type":"hidden"})
        # fourth hidden field on the form
        if self.get_field_value('hidden_field4'):
            self[1][6][0] = tag.ClosedPart(tag_name="input",
                                           attribs ={"name":self.get_formname('hidden_field4'),
                                                     "value":self.get_field_value('hidden_field4'),
                                                     "type":"hidden"})
        # insert id's into the four divs that contain each hidden field
        self[1][3].insert_id()
        self[1][4].insert_id()
        self[1][5].insert_id()
        self[1][6].insert_id()


    def _build_js(self, page, ident_list, environ, call_data, lang):
        """Gives the div id's of hidden fields, so they can be found via json"""
        return self._make_fieldvalues(ident1 = self[1][3].get_id(),
                                      ident2 = self[1][4].get_id(),
                                      ident3 = self[1][5].get_id(),
                                      ident4 = self[1][6].get_id() )



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
    <!-- four hidden input fields, each within a div -->
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
        Widget.__init__(self, name=name, tag_name="div", brief=brief, **field_args)
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
        if self.get_field_value('error_class'):
            self[0].update_attribs({"class":self.get_field_value('error_class')})
        if self.error_status:
            self[0].del_one_attrib("style")

        # file button
        # the div holding file label and button
        if self.get_field_value('inputdiv_class'):
            self[1].attribs = {"class": self.get_field_value('inputdiv_class')}
        if self.get_field_value('label'):
            self[1][0][0] = self.get_field_value('label')
        if self.get_field_value('label_class'):
            self[1][0].attribs = {"class": self.get_field_value('label_class')}
        if self.get_field_value('label_style'):
            self[1][0].attribs = {"style": self.get_field_value('label_style')}

        # set an id in the file button for the 'label for' tag
        self[1][1].insert_id()
        self[1][1].update_attribs({"name":self.get_formname('inputname')})
        if self.get_field_value('filebutton_class'):
            self[1][1].update_attribs({"class": self.get_field_value('filebutton_class')})
        # set the label 'for' attribute
        self[1][0].update_attribs({'for':self[1][1].get_id()})


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


