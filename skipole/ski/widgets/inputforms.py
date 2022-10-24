

"""Contains form widgets, these have 'container' functionality - they can contain further html and widgets, typically
      further input fields.  The module also has an Hidden Field and Submit Button widgets, which can be inserted into
     a form. """

from .. import tag
from . import Widget, ClosedWidget, FieldArg, FieldArgList, FieldArgTable, FieldArgDict


class HiddenField(ClosedWidget):
    """An input field of type hidden, for use as an insert into form widgets"""

    # This class does not display any error messages
    display_errors = False

    arg_descriptions = {'hidden_field':FieldArg("text", '', valdt=True, jsonset=True)}

    def __init__(self, name=None, brief='', **field_args):
        "hidden_field: A hidden input field"
        ClosedWidget.__init__(self, name=name, brief=brief, **field_args)
        self.tag_name = "input"

    def _build(self, page, ident_list, environ, call_data, lang):
        "Sets the attributes"
        if not self.wf.hidden_field:
            self.show = False
            return
        self.attribs.update({"name":self.get_formname('hidden_field'),
                             "value":self.wf.hidden_field,
                             "type":"hidden"})

    @classmethod
    def description(cls):
        """Returns a text string to illustrate the widget"""
        return """
<input type="hidden" /> <!-- with widget id and class widget_class -->
  <!-- with value of the "hidden_field" value, and name being the widgfield -->"""


class HiddenSessionStorage(ClosedWidget):
    """An input field of type hidden, for use as an insert into form widgets"""

    # This class does not display any error messages
    display_errors = False

    arg_descriptions = {'session_key':FieldArg("text", '', valdt=True, jsonset=True)}

    def __init__(self, name=None, brief='', **field_args):
        "hidden_field: A hidden input field with value from session storage"
        ClosedWidget.__init__(self, name=name, brief=brief, **field_args)
        self.tag_name = "input"

    def _build(self, page, ident_list, environ, call_data, lang):
        "Sets the attributes"
        if not self.wf.session_key:
            self.show = False
            return
        self.attribs.update({"name":self.get_formname('session_key'),
                             "value":"",
                             "type":"hidden"})
        # any label:value added to self.jlabels will be set in a javascript fieldvalues attribute for the widget
        self.jlabels['session_key'] = self.wf.session_key

    def _build_js(self, page, ident_list, environ, call_data, lang):
        """Sets key value into the value attribute by calling the widget updatefunc"""
        if not self.wf.session_key:
            return
        ident = self.get_id()
        return f"""
  SKIPOLE.widgets["{ident}"].updatefunc();
"""

    @classmethod
    def description(cls):
        """Returns a text string to illustrate the widget"""
        return """
<input type="hidden" /> <!-- with widget id and class widget_class -->
  <!-- with value taken from the session storage with key "session_key", and name being the session_key widgfield -->"""



class HiddenLocalStorage(ClosedWidget):
    """An input field of type hidden, for use as an insert into form widgets"""

    # This class does not display any error messages
    display_errors = False

    arg_descriptions = {'local_key':FieldArg("text", '', valdt=True, jsonset=True)}

    def __init__(self, name=None, brief='', **field_args):
        "hidden_field: A hidden input field with value from local storage"
        ClosedWidget.__init__(self, name=name, brief=brief, **field_args)
        self.tag_name = "input"

    def _build(self, page, ident_list, environ, call_data, lang):
        "Sets the attributes"
        if not self.wf.local_key:
            self.show = False
            return
        self.attribs.update({"name":self.get_formname('local_key'),
                             "value":"",
                             "type":"hidden"})
        # any label:value added to self.jlabels will be set in a javascript fieldvalues attribute for the widget
        self.jlabels['local_key'] = self.wf.local_key

    def _build_js(self, page, ident_list, environ, call_data, lang):
        """Sets key value into the value attribute by calling the widget updatefunc"""
        if not self.wf.local_key:
            return
        ident = self.get_id()
        return f"""
  SKIPOLE.widgets["{ident}"].updatefunc();
"""

    @classmethod
    def description(cls):
        """Returns a text string to illustrate the widget"""
        return """
<input type="hidden" /> <!-- with widget id and class widget_class -->
  <!-- with value taken from the local storage with key "local_key", and name being the local_key widgfield -->"""



class SubmitButton1(ClosedWidget):
    """An input field of type submit, for use as an insert into form widgets"""

    # This class does not display any error messages
    display_errors = False

    arg_descriptions = {'button_text':FieldArg("text", 'Submit', valdt=True, jsonset=True)}

    def __init__(self, name=None, brief='', **field_args):
        "Create input type submit button widget"
        ClosedWidget.__init__(self, name=name, brief=brief, **field_args)
        self.tag_name = "input"

    def _build(self, page, ident_list, environ, call_data, lang):
        "Sets the attributes"
        button_text = self.wf.button_text
        if not button_text:
            button_text = "Submit"
        self.attribs.update({"name":self.get_formname('button_text'),
                             "value":button_text,
                             "type":"submit"})

    @classmethod
    def description(cls):
        """Returns a text string to illustrate the widget"""
        return """
<input type="button_text" /> <!-- with widget id and class widget_class -->
  <!-- with value of the "button_text" value, and name being the 'button_text widgfield -->"""


class SubmitButton2(ClosedWidget):
    """An input field of type submit, for use as an insert into form widgets"""

    # This class does not display any error messages
    display_errors = False

    arg_descriptions = {'button_text':FieldArg("text", 'Submit', jsonset=True)}

    def __init__(self, name=None, brief='', **field_args):
        "Create input type submit button widget"
        ClosedWidget.__init__(self, name=name, brief=brief, **field_args)
        self.tag_name = "input"

    def _build(self, page, ident_list, environ, call_data, lang):
        "Sets the attributes"
        button_text = self.wf.button_text
        if not button_text:
            button_text = "Submit"
        self.attribs.update({"value":button_text, "type":"submit"})

    @classmethod
    def description(cls):
        """Returns a text string to illustrate the widget"""
        return """
<input type="button_text" /> <!-- with widget id and class widget_class -->
  <!-- with value of the "button_text" value, but no name, so does not submit a widgfield -->"""


class Form1(Widget):
    """A form with a container and four hidden fields. Used with further input fields set within it.
       On error - the error message is displayed before any of the contents
       Does not include a submit button, therefore requires one to be inserted with the contents"""

    _container =  ((1,0),)   ### ((1,0),(2,)) #########

    error_location = (0,0,0)

    arg_descriptions = {'action':FieldArg("url", ''),
                        'enctype':FieldArg("text", ''),
                        'hidden_field1':FieldArg("text", '', valdt=True, jsonset=True),
                        'hidden_field2':FieldArg("text", '', valdt=True, jsonset=True),
                        'hidden_field3':FieldArg("text", '', valdt=True, jsonset=True),
                        'hidden_field4':FieldArg("text", '', valdt=True, jsonset=True),
                        'container_class':FieldArg("cssclass", ''),
                        'error_class':FieldArg("cssclass", '')
                       }

    def __init__(self, name=None, brief='', **field_args):
        """
        action: The page ident, label, url this form links to
        enctype: Sets the enctype attribute if given
        hidden_field1: A hidden field value, leave blank if unused
        hidden_field2: A second hidden field value, leave blank if unused
        hidden_field3: A third hidden field value, leave blank if unused
        hidden_field4: A fourth hidden field value, leave blank if unused
        container_class: the class attribute of the div holding the container
        error_class: The class applied to the paragraph containing the error message on error."""
        Widget.__init__(self, name=name, brief=brief, **field_args)
        self.tag_name = "div"
        self.attribs.update({"role":"form", "method":"post"})
        # error div at 0
        self[0] = tag.Part(tag_name="div", attribs={"style":"display:none;"})
        self[0][0] = tag.Part(tag_name="p")
        self[0][0][0] = ''
        # The form
        self[1] = tag.Part(tag_name='form', attribs={"role":"form", "method":"post"})
        # The location 1,0 is available as a container
        self[1][0] = tag.Part(tag_name="div")
        self[1][0][0] = ''
        ######################################
        #self[2] = tag.Part(tag_name="div")
        #self[2][0] = ''



    def _build(self, page, ident_list, environ, call_data, lang):
        "build the form"
        self[0].set_class_style(self.wf.error_class)
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
        if self.wf.enctype:
            self[1].attribs["enctype"] = self.wf.enctype

        # the div holding the container
        self[1][0].set_class_style(self.wf.container_class)

        # add ident and four hidden fields
        self.add_hiddens(self[1], page)


    def _build_js(self, page, ident_list, environ, call_data, lang):
        """Sets a submit event handler"""
        # this ensures any input text widgets added to the container, get local validation
        # when the form is submitted
        ident=self.get_id()
        return f"""  $('#{ident} form').on("submit", function(e) {{
    SKIPOLE.widgets['{ident}'].eventfunc(e);
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
  <form method=\"post\"> <!-- action attribute set to action field -->
    <div> <!-- this div has the class attribute set to container_class -->
      <!-- container 0 for further html -->
    </div>
    <!-- hidden input fields -->                              
  </form>
</div>"""


class SubmitForm1(Widget):
    """A form taking contents with submit button, left or right labels and four hidden fields.
       Used with further input fields set within it. On error - the error message is displayed
       below the form tag, before any of the contents"""

    _container = ((1,0),)

    error_location = (0,0,0)

    arg_descriptions = {'left_label':FieldArg("text", 'Please Submit:'),
                        'left_class':FieldArg("cssclass", ''),
                        'left_style':FieldArg("cssstyle", ''),
                        'right_label':FieldArg("text", ''),
                        'right_class':FieldArg("cssclass", ''),
                        'right_style':FieldArg("cssstyle", ''),
                        'action_json':FieldArg("url", ''),
                        'action':FieldArg("url", ''),
                        'enctype':FieldArg("text", ''),
                        'hidden_field1':FieldArg("text", '', valdt=True, jsonset=True),
                        'hidden_field2':FieldArg("text", '', valdt=True, jsonset=True),
                        'hidden_field3':FieldArg("text", '', valdt=True, jsonset=True),
                        'hidden_field4':FieldArg("text", '', valdt=True, jsonset=True),
                        'button_text':FieldArg("text",'Submit'),
                        'button_wait_text':FieldArg("text", ''),
                        'button_class':FieldArg("cssclass", ''),
                        'div_class':FieldArg("cssclass", ''),
                        'container_class':FieldArg("cssclass", ''),
                        'error_class':FieldArg("cssclass", ''),
                       }

    def __init__(self, name=None, brief='', **field_args):
        """
        left_label: The text displayed to the left of the button
        left_class: The css class of the label to the left of the button
        right_label: The text displayed to the right of the button
        right_class: The css class of the label to the right of the button
        action_json:  if a value set, and client has jscript enabled, this is the page ident, label, url this button links to, expects a json page back
        action: The page ident, label, url this button links to
        enctype: Sets the enctype attribute if given
        hidden_field1: A hidden field value, leave blank if unused, name used as the get field name
        hidden_field2: A second hidden field value, leave blank if unused, name used as the get field name
        hidden_field3: A third hidden field value, leave blank if unused, name used as the get field name
        hidden_field4: A fourth hidden field value, leave blank if unused, name used as the get field name
        button_text: The text on the button
        button_wait_text: A 'please wait' message shown on the button
        button_class: The css class of the button
        div_class: the class attribute of the div tag which contains the label and button
        container_class: the class attribute of the div holding the container
        error_class: The class applied to the paragraph containing the error message on error.
        """
        Widget.__init__(self, name=name, brief=brief, **field_args)
        self.tag_name = "div"
        # error div at 0
        self[0] = tag.Part(tag_name="div", attribs={"style":"display:none;"})
        self[0][0] = tag.Part(tag_name="p")
        self[0][0][0] = ''
        # The form
        self[1] = tag.Part(tag_name='form', attribs={"role":"form", "method":"post"})
        # The location 1,0 is available as a container
        self[1][0] = tag.Part(tag_name='div')
        self[1][0][0] = ''
        # tag containing label and button
        self[1][1] = tag.Part(tag_name='div')
        # the left label
        self[1][1][0] = tag.Part(tag_name="label", hide_if_empty=True)
        # the submit button
        self[1][1][1] = tag.ClosedPart(tag_name="input", attribs={"type":"submit"})
        # the right label
        self[1][1][2] = tag.Part(tag_name="label", hide_if_empty=True)

    def _build(self, page, ident_list, environ, call_data, lang):
        "build the form"
        jsonurl = self.get_url(self.wf.action_json)
        # any label:value added to self.jlabels will be set in a javascript fieldvalues attribute for the widget
        if jsonurl:
            self.jlabels['url'] = jsonurl
        if self.wf.button_wait_text:
           self.jlabels['button_wait_text'] = self.wf.button_wait_text

        self[0].set_class_style(self.wf.error_class)
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
        if self.wf.enctype:
            self[1].attribs["enctype"] = self.wf.enctype

        # the div holding the container
        self[1][0].set_class_style(self.wf.container_class)

        # the div holding label and button
        self[1][1].set_class_style(self.wf.div_class)

        self[1][1][0].set_class_style(self.wf.left_class, self.wf.left_style)
        if self.wf.left_label:
            self[1][1][0][0] = self.wf.left_label

        # submit button
        self[1][1][1].set_class_style(self.wf.button_class)
        self[1][1][1].attribs["value"] = self.wf.button_text

        # set an id in the submit button for the 'label for' tag
        for_id = self[1][1][1].insert_id()

        self[1][1][2].set_class_style(self.wf.right_class, self.wf.right_style)
        if self.wf.right_label:
            self[1][1][2][0] = self.wf.right_label

        # set the label 'for' attribute
        self[1][1][0].attribs['for'] = for_id
        self[1][1][2].attribs['for'] = for_id

        # any label:value added to self.jlabels will be set in a javascript fieldvalues attribute for the widget
        self.jlabels['buttonident'] = for_id

        # add ident and four hidden fields
        self.add_hiddens(self[1], page)


    def _build_js(self, page, ident_list, environ, call_data, lang):
        """Sets a submit event handler"""
        ident=self.get_id()
        return f"""$('#{ident} form').on("submit", function(e) {{
    SKIPOLE.widgets['{ident}'].eventfunc(e);
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
    <div>  <!-- this div has the class attribute set to container_class -->
      <!-- container 0 for further html -->
    </div>
    <div>  <!-- this div has the class attribute set to div_class -->
      <label> <!-- with class set to left_class and content to left_label -->
      </label>
      <input type=\"submit\" /> <!-- button value set to button_text -->
      <label> <!-- with class set to right_class and content to right_label -->
      </label>
    </div>
    <!-- hidden input fields -->                              
  </form>
</div>"""



class SubmitForm2(Widget):
    """A form taking contents with submit button, left or right labels and four hidden fields.
       Used with further input fields set within it. On error - the error message is displayed
       below the form tag, before any of the contents
       Can send session or local storage values."""

    _container = ((1,0),)

    error_location = (0,0,0)

    arg_descriptions = {'left_label':FieldArg("text", 'Please Submit:'),
                        'left_class':FieldArg("cssclass", ''),
                        'left_style':FieldArg("cssstyle", ''),
                        'right_label':FieldArg("text", ''),
                        'right_class':FieldArg("cssclass", ''),
                        'right_style':FieldArg("cssstyle", ''),
                        'action_json':FieldArg("url", ''),
                        'action':FieldArg("url", ''),
                        'enctype':FieldArg("text", ''),
                        'hidden_field1':FieldArg("text", '', valdt=True, jsonset=True),
                        'hidden_field2':FieldArg("text", '', valdt=True, jsonset=True),
                        'hidden_field3':FieldArg("text", '', valdt=True, jsonset=True),
                        'hidden_field4':FieldArg("text", '', valdt=True, jsonset=True),
                        'session_storage':FieldArg("text", "", valdt=True, jsonset=True),
                        'local_storage':FieldArg("text","", valdt=True, jsonset=True),
                        'button_text':FieldArg("text",'Submit'),
                        'button_wait_text':FieldArg("text", ''),
                        'button_class':FieldArg("cssclass", ''),
                        'div_class':FieldArg("cssclass", ''),
                        'container_class':FieldArg("cssclass", ''),
                        'error_class':FieldArg("cssclass", ''),
                       }

    def __init__(self, name=None, brief='', **field_args):
        """
        left_label: The text displayed to the left of the button
        left_class: The css class of the label to the left of the button
        right_label: The text displayed to the right of the button
        right_class: The css class of the label to the right of the button
        action_json:  if a value set, and client has jscript enabled, this is the page ident, label, url this button links to, expects a json page back
        action: The page ident, label, url this button links to
        enctype: Sets the enctype attribute if given
        hidden_field1: A hidden field value, leave blank if unused, name used as the get field name
        hidden_field2: A second hidden field value, leave blank if unused, name used as the get field name
        hidden_field3: A third hidden field value, leave blank if unused, name used as the get field name
        hidden_field4: A fourth hidden field value, leave blank if unused, name used as the get field name
        session_storage: A session storage key, this widgfield returns the stored value if anything
        local_storage: A local storage key, this widgfield returns the stored value if anything
        button_text: The text on the button
        button_wait_text: A 'please wait' message shown on the button
        button_class: The css class of the button
        div_class: the class attribute of the div tag which contains the label and button
        container_class: the class attribute of the div holding the container
        error_class: The class applied to the paragraph containing the error message on error.
        """
        Widget.__init__(self, name=name, brief=brief, **field_args)
        self.tag_name = "div"
        # error div at 0
        self[0] = tag.Part(tag_name="div", attribs={"style":"display:none;"})
        self[0][0] = tag.Part(tag_name="p")
        self[0][0][0] = ''
        # The form
        self[1] = tag.Part(tag_name='form', attribs={"role":"form", "method":"post"})
        # The location 1,0 is available as a container
        self[1][0] = tag.Part(tag_name='div')
        self[1][0][0] = ''
        # tag containing label and button
        self[1][1] = tag.Part(tag_name='div')
        # the left label
        self[1][1][0] = tag.Part(tag_name="label", hide_if_empty=True)
        # the submit button
        self[1][1][1] = tag.ClosedPart(tag_name="input", attribs={"type":"submit"})
        # the right label
        self[1][1][2] = tag.Part(tag_name="label", hide_if_empty=True)


    def _build(self, page, ident_list, environ, call_data, lang):
        "build the form"
        jsonurl = self.get_url(self.wf.action_json)
        # any label:value added to self.jlabels will be set in a javascript fieldvalues attribute for the widget
        if jsonurl:
            self.jlabels['url'] = jsonurl
        if self.wf.button_wait_text:
           self.jlabels['button_wait_text'] = self.wf.button_wait_text
        if self.wf.session_storage:
           self.jlabels['session_storage'] = self.wf.session_storage
        if self.wf.local_storage:
           self.jlabels['local_storage'] = self.wf.local_storage

        self[0].set_class_style(self.wf.error_class)
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
        if self.wf.enctype:
            self[1].attribs["enctype"] = self.wf.enctype

        # the div holding the container
        self[1][0].set_class_style(self.wf.container_class)

        # the div holding label and button
        self[1][1].set_class_style(self.wf.div_class)

        self[1][1][0].set_class_style(self.wf.left_class, self.wf.left_style)
        if self.wf.left_label:
            self[1][1][0][0] = self.wf.left_label

        # submit button
        self[1][1][1].set_class_style(self.wf.button_class)
        self[1][1][1].attribs["value"] = self.wf.button_text

        # set an id in the submit button for the 'label for' tag
        for_id = self[1][1][1].insert_id()

        self[1][1][2].set_class_style(self.wf.right_class, self.wf.right_style)
        if self.wf.right_label:
            self[1][1][2][0] = self.wf.right_label

        # set the label 'for' attribute
        self[1][1][0].attribs['for'] = for_id
        self[1][1][2].attribs['for'] = for_id

        # any label:value added to self.jlabels will be set in a javascript fieldvalues attribute for the widget
        self.jlabels['buttonident'] = for_id

        # add ident and four hidden fields
        self.add_hiddens(self[1], page)


    def _build_js(self, page, ident_list, environ, call_data, lang):
        """Sets a submit event handler"""
        ident=self.get_id()
        return f"""$('#{ident} form').on("submit", function(e) {{
    SKIPOLE.widgets['{ident}'].eventfunc(e);
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
    <div>  <!-- this div has the class attribute set to container_class -->
      <!-- container 0 for further html -->
    </div>
    <div>  <!-- this div has the class attribute set to div_class -->
      <label> <!-- with class set to left_class and content to left_label -->
      </label>
      <input type=\"submit\" /> <!-- button value set to button_text -->
      <label> <!-- with class set to right_class and content to right_label -->
      </label>
    </div>
    <!-- hidden input fields -->                              
  </form>
</div>"""


class SubmitFromScript(Widget):
    """Defines a form with four hidden fields, values set by javascript"""

    # This class does not display any error messages
    display_errors = False

    arg_descriptions = {
                        'action_json':FieldArg("url", ''),
                        'action':FieldArg("url", ''),
                        'hidden_field1':FieldArg("text", '', valdt=True),
                        'hidden_field2':FieldArg("text", '', valdt=True),
                        'hidden_field3':FieldArg("text", '', valdt=True),
                        'hidden_field4':FieldArg("text", '', valdt=True),
                        'target':FieldArg("text",''),
                        'button_text':FieldArg("text",'Submit'),
                        'button_class':FieldArg("cssclass", ''),
                        'buttondiv_class':FieldArg("cssclass", ''),
                        'buttondiv_style':FieldArg("cssstyle", ''),
                        'hide':FieldArg("boolean", False, jsonset=True)
                       }

    def __init__(self, name=None, brief='', **field_args):
        """
        action_json:  if a value set, and client has jscript enabled, this is the page ident, label, url this button links to, expects a json page back
        action: The page ident, label, url this button links to, overridden if action_json is set.
        hidden_field1: Body of a javascript function returning a value, leave blank if unused
        hidden_field2: Body of a javascript function returning a value, leave blank if unused
        hidden_field3: Body of a javascript function returning a value, leave blank if unused
        hidden_field4: Body of a javascript function returning a value, leave blank if unused
        target: if given, the target attribute will be set
        button_text: The text on the button
        button_class: The class given to the button tag
        buttondiv_class: the class attribute of the div which contains the submit button
        buttondiv_style: the style attribute of the div which contains the submit button
        hide: If True, widget is hidden
        """
        Widget.__init__(self, name=name, brief=brief, **field_args)
        self.tag_name = "div"
        # The form
        self[0] = tag.Part(tag_name='form', attribs={"role":"form", "method":"post"})
        # div containing the submit button
        self[0][0] = tag.Part(tag_name='div')
        # the submit button
        self[0][0][0] = tag.Part(tag_name="button", attribs ={"type":"submit"})
        self[0][0][0][0] = "Submit"


    def _build(self, page, ident_list, environ, call_data, lang):
        "build the form"
        if self.wf.target:
            self[0].attribs["target"] = self.wf.target
        # Hides widget if no error and hide is True
        self.widget_hide(self.wf.hide)

        jsonurl = self.get_url(self.wf.action_json)
        # any label:value added to self.jlabels will be set in a javascript fieldvalues attribute for the widget
        if jsonurl:
            self.jlabels['url'] = jsonurl
        if self.wf.hidden_field1:
           self.jlabels['hidden_field1'] = self.wf.hidden_field1
        if self.wf.hidden_field2:
           self.jlabels['hidden_field2'] = self.wf.hidden_field2
        if self.wf.local_storage:
           self.jlabels['hidden_field3'] = self.wf.hidden_field3
        if self.wf.local_storage:
           self.jlabels['hidden_field4'] = self.wf.hidden_field4

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

        # the div holding the submit button
        self[0][0].set_class_style(self.wf.buttondiv_class, self.wf.buttondiv_style)

        # submit button
        self[0][0][0].set_class_style(self.wf.button_class)
        if self.wf.button_text:
            self[0][0][0][0] = self.wf.button_text

        # add ident and four hidden fields
        if page is not None:
            self[0].append(tag.ClosedPart(tag_name="input",
                                   attribs ={"name":'ident',
                                             "value":page.ident_data_string,
                                             "type":"hidden"}))
        # hidden field on the form
        if self.wf.hidden_field1:
            self[0].append(tag.ClosedPart(tag_name="input",
                                       attribs ={"name":self.get_formname('hidden_field1'),
                                                 "type":"hidden"}))

        # Second hidden field on the form
        if self.wf.hidden_field2:
            self[0].append(tag.ClosedPart(tag_name="input",
                                       attribs ={"name":self.get_formname('hidden_field2'),
                                                 "type":"hidden"}))

        # third hidden field on the form
        if self.wf.hidden_field3:
            self[0].append(tag.ClosedPart(tag_name="input",
                                       attribs ={"name":self.get_formname('hidden_field3'),
                                                 "type":"hidden"}))

        # fourth hidden field on the form
        if self.wf.hidden_field4:
            self[0].append(tag.ClosedPart(tag_name="input",
                                       attribs ={"name":self.get_formname('hidden_field4'),
                                                 "type":"hidden"}))


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
  <form role="form" method="post"> <!-- action attribute set to action field -->
    <div>  <!-- class attribute set to buttondiv_class -->
      <button type="submit"> <!-- with class set to button_class -->
        <!-- button_text -->
      </button>
    </div>
    <!-- hidden input fields each submitting a value as returned by the corresponding javascript functions -->                              
  </form>
</div>"""



