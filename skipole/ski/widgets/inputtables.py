
"""Contains widgets for inputting data"""

from urllib.parse import quote

from .. import skiboot, tag, excepts
from . import Widget, ClosedWidget, FieldArg, FieldArgList, FieldArgTable, FieldArgDict




class InputTable1(Widget):
    """A table of three columns, two being text strings, the third a text input field
       The first row is three header titles. Typically inserted into a form
       does not display errors"""

    display_errors = False


    arg_descriptions = {'header_class':FieldArg("cssclass",""),
                        'size':FieldArg("text", ''),
                        'maxlength':FieldArg("text", ''),
                        'title1':FieldArg('text', ''),
                        'title2':FieldArg('text', ''),
                        'title3':FieldArg('text', ''),
                        'row_classes':FieldArgList('text', jsonset=True),
                        'col1':FieldArgList('text', jsonset=True),
                        'col2':FieldArgList('text', jsonset=True),
                        'inputdict':FieldArgDict('text', valdt=True, jsonset=True, senddict=True)                 # dictionary of keyname:value
                        }                                                                                         # the field submitted as a dictionary
                                                                                                                  # each key will have 'keyname'
                                                                                                                  # and value will be the values ticked

    def __init__(self, name=None, brief='', **field_args):
        """
        header_class: class of the header row, if empty string, then no class will be applied
        size: The number of characters appearing in each text input area
        maxlength: The maximum number of characters accepted in each text area
        title1: The header title over the first text column
        title2: The header title over the second text column
        title3: The header title over the third text column
        row_classes: A list of CSS classes to apply to each row (not including the header)
        col1: A list of text strings to place in the first column
        col2: A list of text strings to place in the second column
        inputdict: A dictionary of keyname:value, should be Ordered Dict unless python >= 3.6
                   the fields submitted will have name 'widgetname:inputdict-keyname'
                   and the user will receive a widgfield ('widgetname','inputdict') containing a dictionary of keyname:values
         """
        Widget.__init__(self, name=name, tag_name="table", brief=brief, **field_args)


    def _build(self, page, ident_list, environ, call_data, lang):
        "Build the table"
        inputdict = self.get_field_value("inputdict")
        rowc = self.get_field_value("row_classes")
        col1 = self.get_field_value("col1")
        col2 = self.get_field_value("col2")
        input_name = self.get_formname("inputdict") + '-'
        size = self.get_field_value('size')
        maxlength = self.get_field_value('maxlength')

        header = 0
        if self.get_field_value('title1') or self.get_field_value('title2') or self.get_field_value('title3'):
            header = 1
            if self.get_field_value('header_class'):
                self[0] = tag.Part(tag_name='tr', attribs={"class":self.get_field_value('header_class')})
            else:
                self[0] = tag.Part(tag_name='tr')
            self[0][0] = tag.Part(tag_name='th', text = self.get_field_value('title1'))
            self[0][1] = tag.Part(tag_name='th', text = self.get_field_value('title2'))
            self[0][2] = tag.Part(tag_name='th', text = self.get_field_value('title3'))

        # create rows
        rows = max( len(col1), len(col2), len(inputdict) )
        if not rowc:
            rowc = ['']*rows
        if rows > len(rowc):
            rowc.extend(['']*(rows - len(rowc)))
        if rows > len(col1):
            col1.extend(['']*(rows - len(col1)))
        if rows > len(col2):
            col2.extend(['']*(rows - len(col2)))

        keylist = list(inputdict.keys())
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
                self[rownumber][2][0] = tag.ClosedPart(tag_name="input", attribs={"name":keyed_name, "type":"text", "value":inputdict[key]})
                if size:
                    self[rownumber][2][0].update_attribs({"size":size})
                if maxlength:
                    self[rownumber][2][0].update_attribs({"maxlength":maxlength})



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
    <td><input type="text" />  <!-- with names and value derived from 'inputdict' -->
    </td>
  </tr>
  <!-- rows repeated -->
</table>"""





class InputTable5(Widget):
    """Defines a div of four columns, the first just being label text, the second being text input fields,
       the third and fourth being submit buttons.  Each row of the table is a form, the
       form action ident is the same for all forms.
       On error the paragraph TextBlock is changed to the error message."""

    # This class does not display any error messages
    display_errors = False

    # js_validators is a class attribute, True if javascript validation is enabled
    js_validators=True

    arg_descriptions = {
                        'div_class':FieldArg("cssclass", ''),
                        'size':FieldArg("text", ''),
                        'maxlength':FieldArg("text", ''),
                        'required':FieldArg("boolean", False),
                        'action':FieldArg("url",''),
                        'button_text1':FieldArg("text", "Submit", valdt=True),
                        'button_text2':FieldArg("text", "Submit", valdt=True),
                        'button1_class':FieldArg("cssclass", ""),
                        'button2_class':FieldArg("cssclass", ""),
                        'col_label':FieldArgList('text'),
                        'label_class':FieldArg("cssclass", ""),
                        'label_style':FieldArg("cssstyle", ""),
                        'col_input':FieldArgList('text', valdt=True),
                        'hidden_field1':FieldArgList("text", valdt=True),
                        'hidden_field2':FieldArgList("text", valdt=True),
                        'hidden_field3':FieldArgList("text", valdt=True),
                        'hidden_field4':FieldArgList("text", valdt=True),
                        'input_accepted_class':FieldArg("cssclass", ''),
                        'input_class':FieldArg("cssclass", ''),
                        'input_style':FieldArg("cssstyle", ''),
                        'input_errored_class':FieldArg("cssclass", ''),
                        'set_input_accepted':FieldArgDict("boolean", jsonset=True),
                        'set_input_errored':FieldArgDict("boolean", jsonset=True)
                       }

    def __init__(self, name=None, brief='', **field_args):
        """
        div_class: the class attribute of each form div
        size: The number of characters appearing in each text input area
        maxlength: The maximum number of characters accepted in each text area
        required: Set True to put the 'required' flag into each input field
        action: The label or ident of the action page
        button_text1: text appearing on the first buttons - if empty, no button 1 is shown
        button_text2: text appearing on the second buttons - if empty, no button 2 is shown
        button1_class: class set on button1
        button2_class: class set on button2
        col_label: a list of all the text strings appearing in the first column
        label_class: the class to apply to each label
        col_input: a list of all the text strings appearing in the input fields
        hidden_field1-4: four hidden fields, each being a list
        input_accepted_class: A class which can be added on each input field
        input_class: A class which can be set on each input field
        input_errored_class: A class which can be added on each input field
        The following two dictionaries should have keys equal to the integer row number (starting
         at zero) and value True or False
        set_input_accepted: Dictionary of col index keys that should be set with input_accepted_class
        set_input_errored: Dictionary of col index keys that should be set with input_errored_class
        """
        Widget.__init__(self, name=name, tag_name="div", brief=brief, **field_args)


    def _build(self, page, ident_list, environ, call_data, lang):
        "Build the table"

        # get the widget ident
        ident_value = page.ident_data_string

        # get the form action url
        action_url = skiboot.get_url(self.get_field_value("action"), proj_ident=page.proj_ident)
        if not action_url:
            # setting self._error replaces the entire tag by the self._error message
            self._error = "Warning: broken link"
            return


        len_label = len(self.fields["col_label"])
        len_input = len(self.fields["col_input"])
        len_hidden_field1 = len(self.fields["hidden_field1"])
        len_hidden_field2 = len(self.fields["hidden_field2"])
        len_hidden_field3 = len(self.fields["hidden_field3"])
        len_hidden_field4 = len(self.fields["hidden_field4"])

        rows = max(len_label, len_input)
        if not rows:
            rows=1

        input_name = self.get_formname("col_input")
        button_name1 = self.get_formname("button_text1")
        button_value1 = self.get_field_value('button_text1')
        button1_class = self.get_field_value('button1_class')
        button_name2 = self.get_formname("button_text2")
        button_value2 = self.get_field_value('button_text2')
        button2_class = self.get_field_value('button2_class')
        hidden_field1_name = self.get_formname("hidden_field1")
        hidden_field2_name = self.get_formname("hidden_field2")
        hidden_field3_name = self.get_formname("hidden_field3")
        hidden_field4_name = self.get_formname("hidden_field4")

        label_class = self.get_field_value('label_class')
        label_style = self.get_field_value('label_style')

        form_id = self.get_id() + '_'

        if self.get_field_value('input_accepted_class') and self.get_field_value("set_input_accepted"):
            set_input_accepted = self.get_field_value("set_input_accepted")
        else:
            set_input_accepted = {}

        if self.get_field_value('input_errored_class') and self.get_field_value("set_input_errored"):
            set_input_errored = self.get_field_value("set_input_errored")
        else:
            set_input_errored = {}

        input_class = self.get_field_value('input_class')
        input_style = self.get_field_value('input_style')


        for rownumber in range(rows):
            if rownumber<len_label:
                col_label = self.get_field_value("col_label")[rownumber]
            else:
                col_label = ''
            if rownumber<len_input:
                col_input = self.get_field_value("col_input")[rownumber]
            else:
                col_input = ''
            if rownumber<len_hidden_field1:
                col_hidden_field1 = self.get_field_value("hidden_field1")[rownumber]
            else:
                col_hidden_field1 = ''
            if rownumber<len_hidden_field2:
                col_hidden_field2 = self.get_field_value("hidden_field2")[rownumber]
            else:
                col_hidden_field2 = ''
            if rownumber<len_hidden_field3:
                col_hidden_field3 = self.get_field_value("hidden_field3")[rownumber]
            else:
                col_hidden_field3 = ''
            if rownumber<len_hidden_field4:
                col_hidden_field4 = self.get_field_value("hidden_field4")[rownumber]
            else:
                col_hidden_field4 = ''

            # for every table row, create a form
            formrow = tag.Part(tag_name="form", attribs ={"method":"post", "action": action_url})

            # 1st column is label text 
            if label_class:
                formrow[0] = tag.Part(tag_name="label", attribs={'class':label_class})
            else:
                formrow[0] = tag.Part(tag_name="label")
            if label_style:
                formrow[0].update_attribs({"style":label_style})
            formrow[0][0] = col_label

            # 2nd column is a text input field
            formrow[1] = tag.ClosedPart(tag_name="input",
                                    attribs ={"name":input_name,
                                    "value":col_input,
                                    "type":"text"})
            if self.get_field_value('size'):
                formrow[1].update_attribs({"size":self.get_field_value('size')})
            if self.get_field_value('maxlength'):
                formrow[1].update_attribs({"maxlength":self.get_field_value('maxlength')})
            if self.get_field_value('required'):
                formrow[1].update_attribs({"required":"required"})
            # set an id in the input field for the 'label for' tag
            this_id = form_id + str(rownumber) + '_0_1'
            formrow[1].insert_id(this_id)
            # set the label 'for' attribute
            formrow[0].update_attribs({'for':formrow[1].get_id()})
            if (rownumber in set_input_errored) and set_input_errored[rownumber]:
                if input_class:
                    formrow[1].update_attribs({"class":input_class + ' ' + self.get_field_value('input_errored_class')})
                else:
                    formrow[1].update_attribs({"class":self.get_field_value('input_errored_class')})
            elif (rownumber in set_input_accepted) and set_input_accepted[rownumber]:
                if input_class:
                    formrow[1].update_attribs({"class":input_class + ' ' + self.get_field_value('input_accepted_class')})
                else:
                    formrow[1].update_attribs({"class":self.get_field_value('input_accepted_class')})
            elif input_class:
                formrow[1].update_attribs({"class":input_class})

            if input_style:
                formrow[1].update_attribs({"style":input_style})

            # 3rd column is a submit button
            if button_value1:
                formrow.append(tag.ClosedPart(tag_name="input",
                                 attribs ={"name":button_name1,
                                           "value":button_value1,
                                           "class":button1_class,
                                           "type":"submit"}))
            # 4th column is a submit button
            if button_value2:
                formrow.append(tag.ClosedPart(tag_name="input",
                                 attribs ={"name":button_name2,
                                           "value":button_value2,
                                           "class":button2_class,
                                           "type":"submit"}))

            # all submissions always have an 'ident' hidden field to provide the ident of the calling page
            formrow.append(tag.ClosedPart(tag_name="input",
                                          attribs ={"name":'ident',
                                                 "value":ident_value,
                                                 "type":"hidden"}))

            # hidden field on the form
            if col_hidden_field1:
                formrow.append(tag.ClosedPart(tag_name = "input",
                                            attribs =  {"name":hidden_field1_name,
                                                        "value":col_hidden_field1,
                                                        "type":"hidden"}))

            # Second hidden field on the form
            if col_hidden_field2:
                formrow.append(tag.ClosedPart(tag_name = "input",
                                            attribs =  {"name":hidden_field2_name,
                                                        "value":col_hidden_field2,
                                                        "type":"hidden"}))
            # Third hidden field on the form
            if col_hidden_field3:
                formrow.append(tag.ClosedPart(tag_name = "input",
                                            attribs =  {"name":hidden_field3_name,
                                                        "value":col_hidden_field3,
                                                        "type":"hidden"}))
            # Fourth hidden field on the form
            if col_hidden_field4:
                formrow.append(tag.ClosedPart(tag_name = "input",
                                            attribs =  {"name":hidden_field4_name,
                                                        "value":col_hidden_field4,
                                                        "type":"hidden"}))

            # place form in a div
            self[rownumber] = tag.Part(tag_name="div")
            if self.get_field_value('div_class'):
                self[rownumber].attribs = {"class": self.get_field_value('div_class')}
            self[rownumber][0] = formrow


    def _build_js(self, page, ident_list, environ, call_data, lang):
        """Sets a submit event handler"""
        jscript = """  $('#{ident}').find( 'form').each(function() {{
    $(this).on("submit", function(e) {{
        SKIPOLE.widgets['{ident}'].eventfunc(e);
        }});
    }});
""".format(ident=self.get_id())
        return jscript + self._make_fieldvalues('input_accepted_class', 'input_errored_class')

    @classmethod
    def description(cls):
        """Returns a text string to illustrate the widget"""
        return """
<div>   <!-- with widget id and class widget_class -->
  <!-- Then a div containing a form, label, input field, buttons and hidden fields, repeated for each list  item -->
  <div> <!-- with CSS class attribute set to div_class if a class is set -->
    <form method=\"post\"> <!-- action attribute set to action field -->
      <label> <!-- with col_label text and CSS class label_class -->
      </label >
        <input type="text" /> <!-- all with same CSS input_class and size and maxlength, with values from col_input -->
        <input type="submit" /> <!-- with value button_text1, CSS class button1_class and name widgfield derived from button_text1 field name -->
        <input type="submit" /> <!-- with value button_text2, CSS class button2_class and name widgfield derived from button_text2 field name -->
        <!-- hidden input fields -->
    </form>                              
  </div>
  <!--  The above repeated for each item in col_input or col_label, whichever is greater -->
</div>"""




class InputTable4(Widget):
    """A table of four columns, three being text strings,
       the fourth being a cell with up and down arrow links and a hidden field
       On the links being chosen a request for a json update is made, which
       typically updates the text columns, and the values in the hidden field.
       Each arrow has two get fields which can be set.
       The first row is four header titles.
       Typically inserted into a form, does not display errors"""

    display_errors = False


    arg_descriptions = {'header_class':FieldArg("cssclass",""),
                        'col1_class':FieldArg("cssclass",""),          # class applied to every td in the first column
                        'col2_class':FieldArg("cssclass",""),          # class applied to every td in the second column
                        'col3_class':FieldArg("cssclass",""),          # class applied to every td in the third column
                        'col4_class':FieldArg("cssclass",""),          # class applied to every td in the fourth column
                        'col4_style':FieldArg("cssstyle", ""),
                        'row_classes':FieldArgList('text', jsonset=True),
                        'title1':FieldArg('text', ''),
                        'title2':FieldArg('text', ''),
                        'title3':FieldArg('text', ''),
                        'title4':FieldArg('text', ''),
                        'up_link_ident':FieldArg("url", 'no_javascript'),
                        'up_json_ident':FieldArg("url", ''),
                        'down_link_ident':FieldArg("url", 'no_javascript'),
                        'down_json_ident':FieldArg("url", ''),
                        'up_style':FieldArg("cssstyle", ""),
                        'down_style':FieldArg("cssstyle", ""),
                        'up_class':FieldArg("cssclass", ""),
                        'down_class':FieldArg("cssclass", ""),
                        'up_getfield1':FieldArgList('text', valdt=True, jsonset=True),
                        'up_getfield2':FieldArgList('text', valdt=True, jsonset=True),
                        'down_getfield1':FieldArgList('text', valdt=True, jsonset=True),
                        'down_getfield2':FieldArgList('text', valdt=True, jsonset=True),
                        'col1':FieldArgList('text', jsonset=True),
                        'col2':FieldArgList('text', jsonset=True),
                        'col3':FieldArgList('text', jsonset=True),
                        'inputdict':FieldArgDict('text', valdt=True, jsonset=True, senddict=True)                 # dictionary of keyname:value
                        }                                                                                         # the field submitted as a dictionary
                                                                                                                  # each key will have 'keyname'
                                                                                                                  # and value will be the hidden field values

## w3-button.w3-padding-small.w3-small.w3-theme-dark

#"header_class": "w3-theme-d3",
#"widget_class": "w3-table w3-theme-d1 w3-border w3-bordered"

    def __init__(self, name=None, brief='', **field_args):
        """
        header_class: class of the header row, if empty string, then no class will be applied
        col1_class: class applied to every td in the first column
        col2_class: class applied to every td in the second column
        col3_class: class applied to every td in the third column
        col4_class: class applied to every td in the fourth column
        col4_style: style applied to every td in the fourth column
        row_classes: A list of CSS classes to apply to each row (not including the header)
        title1: The header title over the first text column
        title2: The header title over the second text column
        title3: The header title over the third text column
        title4: The header title over the fourth text column
        up_link_ident: ident of the up arrow link if javascript disabled
        up_json_ident: ident of the up arrow link, expects a json file returned
        down_link_ident: ident of the down arrow link if javascript disabled
        down_json_ident: ident of the down arrow link, expects a json file returned
        up_style: CSS style applied to the up arrows
        down_style: CSS style applied to the down arrows
        up_class: CSS class applied to the up arrows
        down_class: CSS class applied to the down arrows
        up_getfield1: list of get fields, one for each up arrow link
        up_getfield2: list of second get fields, one for each up arrow link
        down_getfield1: list of get fields, one for each down arrow link
        down_getfield2: list of get fields, one for each down arrow link
        col1: A list of text strings to place in the first column
        col2: A list of text strings to place in the second column
        col3: A list of text strings to place in the third column
        inputdict: A dictionary of keyname:value, should be Ordered Dict unless python >= 3.6
                   the fields submitted will have name 'widgetname:inputdict-keyname'
                   and the user will receive a widgfield ('widgetname','inputdict') containing a dictionary of keyname:values
         """
        Widget.__init__(self, name=name, tag_name="table", brief=brief, **field_args)
        self._up_jsonurl = ''
        self._down_jsonurl = ''


    def _build(self, page, ident_list, environ, call_data, lang):
        "Build the table"
        inputdict = self.get_field_value("inputdict")
        rowc = self.get_field_value("row_classes")
        col1 = self.get_field_value("col1")
        col2 = self.get_field_value("col2")
        col3 = self.get_field_value("col3")
        input_name = self.get_formname("inputdict") + '-'

        col1_class = self.get_field_value("col1_class")
        col2_class = self.get_field_value("col2_class")
        col3_class = self.get_field_value("col3_class")
        col4_class = self.get_field_value("col4_class")
        col4_style = self.get_field_value("col4_style")

        up_link_ident = self.get_field_value("up_link_ident") # ident of the up arrow link if javascript disabled
        if not up_link_ident:
            up_link_ident = 'no_javascript'
        up_json_ident = self.get_field_value("up_json_ident") # ident of the up arrow link, expects a json file returned

        down_link_ident = self.get_field_value("down_link_ident") # ident of the down arrow link if javascript disabled
        if not down_link_ident:
            down_link_ident = 'no_javascript'
        down_json_ident = self.get_field_value("down_json_ident") # ident of the down arrow link, expects a json file returned

        up_style = self.get_field_value("up_style") # CSS style applied to the up arrows
        down_style = self.get_field_value("down_style") # CSS style applied to the down arrows
        up_class = self.get_field_value("up_class") # CSS class applied to the up arrows
        down_class = self.get_field_value("down_class") # CSS class applied to the down arrows

        up_getfield1 = self.get_field_value("up_getfield1") # list of get fields, one for each up arrow link
        up_getfield2 = self.get_field_value("up_getfield2") # list of second get fields, one for each up arrow link
        down_getfield1 = self.get_field_value("down_getfield1") # list of get fields, one for each down arrow link
        down_getfield2 = self.get_field_value("down_getfield2") # list of get fields, one for each down arrow link

        # up arrow link
        # get json url
        if up_json_ident:
            self._up_jsonurl = skiboot.get_url(up_json_ident, proj_ident=page.proj_ident)
        # get url
        up_url = skiboot.get_url(up_link_ident, proj_ident=page.proj_ident)

        # down arrow link
        # get json url
        if down_json_ident:
            self._down_jsonurl = skiboot.get_url(down_json_ident, proj_ident=page.proj_ident)
        # get url
        down_url = skiboot.get_url(down_link_ident, proj_ident=page.proj_ident)


        header = 0
        if self.get_field_value('title1') or self.get_field_value('title2') or self.get_field_value('title3') or self.get_field_value('title4'):
            header = 1
            if self.get_field_value('header_class'):
                self[0] = tag.Part(tag_name='tr', attribs={"class":self.get_field_value('header_class')})
            else:
                self[0] = tag.Part(tag_name='tr')
            self[0][0] = tag.Part(tag_name='th', text = self.get_field_value('title1'))
            self[0][1] = tag.Part(tag_name='th', text = self.get_field_value('title2'))
            self[0][2] = tag.Part(tag_name='th', text = self.get_field_value('title3'))
            self[0][3] = tag.Part(tag_name='th', text = self.get_field_value('title4'))

        # create rows
        rows = max( len(col1), len(col2), len(col3), len(inputdict) )

        if not rows:
            return

        if rows > len(col1):
            col1.extend(['']*(rows - len(col1)))
        if rows > len(col2):
            col2.extend(['']*(rows - len(col2)))
        if rows > len(col3):
            col3.extend(['']*(rows - len(col3)))

        keylist = list(inputdict.keys())
        if rows > len(keylist):
            keylist.extend([None]*(rows - len(keylist)))

        # keylist is a list of the dictionary keys, extended by None keys, if the dictionary is smaller than the number of rows of the table

        for index in range(rows):
            rownumber = index+header

            cssclass = rowc[index] if index < len(rowc) else ''
            if cssclass:
                self[rownumber] = tag.Part(tag_name='tr', attribs={"class":cssclass})
            else:
                self[rownumber] = tag.Part(tag_name='tr')

            if col1_class:
                self[rownumber][0] = tag.Part(tag_name='td', text = col1[index], attribs={"class":col1_class})
            else:
                self[rownumber][0] = tag.Part(tag_name='td', text = col1[index])

            if col2_class:
                self[rownumber][1] = tag.Part(tag_name='td', text = col2[index], attribs={"class":col2_class})
            else:
                self[rownumber][1] = tag.Part(tag_name='td', text = col2[index])

            if col3_class:
                self[rownumber][2] = tag.Part(tag_name='td', text = col3[index], attribs={"class":col3_class})
            else:
                self[rownumber][2] = tag.Part(tag_name='td', text = col3[index])

            if col4_class:
                self[rownumber][3] = tag.Part(tag_name='td', attribs={"class":col4_class})
            else:
                self[rownumber][3] = tag.Part(tag_name='td')

            if col4_style:
                self[rownumber][3].update_attribs({"style": col4_style})

            if up_style:
                self[rownumber][3][0] = tag.Part(tag_name="a", attribs={"role":"button", "style":up_style})
            else:
                self[rownumber][3][0] = tag.Part(tag_name="a", attribs={"role":"button"})

            if up_class:
                self[rownumber][3][0].update_attribs({"class": up_class})

            self[rownumber][3][0][0] = tag.HTMLSymbol("&uarr;")

            # create a url for the up arrow link
            upget1 = up_getfield1[index] if index < len(up_getfield1) else ''
            upget2 = up_getfield2[index] if index < len(up_getfield2) else ''
            get_fields = {self.get_formname("up_getfield1"):upget1,
                          self.get_formname("up_getfield2"):upget2}
            url = self.make_get_url(page, up_url, get_fields, True)
            self[rownumber][3][0].update_attribs({"href": url})

            if down_style:
                self[rownumber][3][1] = tag.Part(tag_name="a", attribs={"role":"button", "style":down_style})
            else:
                self[rownumber][3][1] = tag.Part(tag_name="a", attribs={"role":"button"})

            if down_class:
                self[rownumber][3][1].update_attribs({"class": down_class})

            self[rownumber][3][1][0] = tag.HTMLSymbol("&darr;")

            # create a url for the down arrow link
            downget1 = down_getfield1[index] if index < len(down_getfield1) else ''
            downget2 = down_getfield2[index] if index < len(down_getfield2) else ''
            get_fields = {self.get_formname("down_getfield1"):downget1,
                          self.get_formname("down_getfield2"):downget2}
            url = self.make_get_url(page, down_url, get_fields, True)
            self[rownumber][3][1].update_attribs({"href": url})

            key = keylist[index]
            if key:  # this is the dictionary key
                keyed_name = input_name + key
                self[rownumber][3][2] = tag.ClosedPart(tag_name="input", attribs={"name":keyed_name, "type":"hidden", "value":inputdict[key]})


    def _build_js(self, page, ident_list, environ, call_data, lang):
        """Sets a click event handler"""
        jscript = """  $("#{ident} a").click(function (e) {{
    SKIPOLE.widgets['{ident}'].eventfunc(e);
    }});
""".format(ident = self.get_id())
        if self._up_jsonurl or self._down_jsonurl:
            return jscript + self._make_fieldvalues(upurl=self._up_jsonurl, downurl=self._down_jsonurl)



    @classmethod
    def description(cls):
        """Returns a text string to illustrate the widget"""
        return """
<table>  <!-- with widget id and class widget_class -->
  <tr> <!-- with header class -->
    <th> <!-- title1 --> </th>
    <th> <!-- title2 --> </th>
    <th> <!-- title3 --> </th>
    <th> <!-- title4 --> </th>
  </tr>
  <tr>
    <td> <!-- with class col1_class and col1 text string --> </td>
    <td> <!-- with class col2_class and col2 text string --> </td>
    <td> <!-- with class col3_class and col3 text string --> </td>
    <td> <!-- with class col4_class -->
      <a role="button" href="#"> <!-- with style up_style -->
      <!-- The href link will be the url of the up ident with up get fields -->
      &uarr;
      </a>
      <a role="button" href="#"> <!-- with style down_style -->
      <!-- The href link will be the url of the down ident with down get fields -->
      &darr;
      </a>
      <input type="hidden" /> <!-- with name being 'widgetname:inputdict-keyname' and
                              <!-- value from inputdict values  -->
                              <!-- on form submission received data will be a widgfield -->
                              <!-- ('widgetname','inputdict') containing a dictionary of keyname:values -->
    </td>
  </tr>
  <!-- rows repeated -->
</table>"""



