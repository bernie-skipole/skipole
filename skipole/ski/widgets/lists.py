

"""Contains widgets for lists"""

from .. import tag
from . import Widget, ClosedWidget, FieldArg, FieldArgList, FieldArgTable, FieldArgDict, AnchorClickEventMixin


class UList1(Widget):
    """An unordered list widget."""

    # This class does not display any error messages
    display_errors = False

    arg_descriptions = {
                       'highlight_class':FieldArg("cssclass", ''),
                       'set_highlight':FieldArg("boolean", False, jsonset=True),
                       'contents': FieldArgList('text', jsonset=True),
                       'even_class':FieldArg("cssclass", ""),
                       'odd_class':FieldArg("cssclass", "")
                       }

    def __init__(self, name=None, brief='', **field_args):
        """
        highlight_class: CSS class will replace widget_class if set_highlight is True
        set_highlight: Set to True to force highlight_class to replace widget_class
                       Set to False to remove highlight_class and return to widget_class
        contents: List of text strings to be shown, gives the number of list items
        even_class: class of even li elements, if empty string, then no class will be applied
        odd_class: class of odd li elements, if empty string, then no class will be applied
        """
        Widget.__init__(self, name=name, brief=brief, **field_args)
        self.tag_name = "ul"


    def _build(self, page, ident_list, environ, call_data, lang):
        "Build the list"
        contents = self.wf.contents

        # any label:value added to self.jlabels will be set in a javascript fieldvalues attribute for the widget
        if self.wf.highlight_class:
            self.jlabels['highlight_class'] = self.wf.highlight_class
            if self.wf.set_highlight:
                self.attribs["class"] = self.wf.highlight_class

        # set even li class
        if self.wf.even_class:
            _even = self.wf.even_class
            self.jlabels['even_class'] = _even
        else:
            _even = ''
        # set odd li class
        if self.wf.odd_class:
            _odd = self.wf.odd_class
            self.jlabels['odd_class'] = _odd
        else:
            _odd = ''
        for index, item in enumerate(contents):
            if _even and (index % 2):
                self[index] = tag.Part(tag_name="li", attribs={"class":_even}, text=item)
            elif _odd and not (index % 2):
                self[index] = tag.Part(tag_name='li', attribs={"class":_odd}, text=item)
            else:
                self[index] = tag.Part(tag_name='li', text=item)


    @classmethod
    def description(cls):
        """Returns a text string to illustrate the widget"""
        return """<ul>  <!-- with widget id and class widget_class -->
  <li> <!-- with style from odd_class or even_class -->
      <!-- with text from each contents element -->
  </li>
  <!-- with appropriate number of list elements -->
</ul>
"""


class UList2(Widget):
    """An unordered list widget containing html"""

    # This class does not display any error messages
    display_errors = False

    arg_descriptions = {
                       'highlight_class':FieldArg("cssclass", ''),
                       'set_highlight':FieldArg("boolean", False, jsonset=True),
                       'set_html': FieldArgList('text', jsonset=True),
                       'even_class':FieldArg("cssclass", ""),
                       'odd_class':FieldArg("cssclass", "")
                       }

    def __init__(self, name=None, brief='', **field_args):
        """
        highlight_class: CSS class will replace widget_class if set_highlight is True
        set_highlight: Set to True to force highlight_class to replace widget_class
                       Set to False to remove highlight_class and return to widget_class
        set_html: List of html strings to be shown, html will be shown unescaped
        even_class: class of even li elements, if empty string, then no class will be applied
        odd_class: class of odd li elements, if empty string, then no class will be applied
        """
        Widget.__init__(self, name=name, brief=brief, **field_args)
        self.tag_name = "ul"

    def _build(self, page, ident_list, environ, call_data, lang):
        "Build the list"
        contents = self.wf.set_html

        # any label:value added to self.jlabels will be set in a javascript fieldvalues attribute for the widget

        if self.wf.highlight_class:
            self.jlabels['highlight_class'] = self.wf.highlight_class
            if self.wf.set_highlight:
                self.attribs["class"] = self.wf.highlight_class

        # set even li class
        if self.wf.even_class:
            _even = self.wf.even_class
            self.jlabels['even_class'] = _even
        else:
            _even = ''
        # set odd li class
        if self.wf.odd_class:
            _odd = self.wf.odd_class
            self.jlabels['odd_class'] = _odd
        else:
            _odd = ''

        for index, item in enumerate(contents):
            if _even and (index % 2):
                self[index] = tag.Part(tag_name="li", attribs={"class":_even}, text=item)
            elif _odd and not (index % 2):
                self[index] = tag.Part(tag_name='li', attribs={"class":_odd}, text=item)
            else:
                self[index] = tag.Part(tag_name='li', text=item)
            self[index].htmlescaped = False
            self[index].linebreaks=False


    @classmethod
    def description(cls):
        """Returns a text string to illustrate the widget"""
        return """<ul>  <!-- with widget id and class widget_class -->
  <li> <!-- with style from odd_class or even_class -->
      <!-- with html from each set_html element -->
  </li>
  <!-- with appropriate number of list elements -->
</ul>
"""


class TableList(AnchorClickEventMixin, Widget):
    """A table of a single text column, followed by Up, Down and Remove button link columns
       Each link having an individual get field set
       Typically used to display and order a Python list"""


    # This class does not display any error messages
    display_errors = False

    arg_descriptions = {
                        'highlight_class':FieldArg("cssclass", ''),
                        'set_highlight':FieldArg("boolean", False, jsonset=True),
                        'even_class':FieldArg("cssclass", ""),
                        'odd_class':FieldArg("cssclass", ""),
                        'maximize_text_col':FieldArg('boolean',True),
                        'hide':FieldArg("boolean", False, jsonset=True),
                        'button_class':FieldArg("cssclass", ""),
                        'remove_button_text':FieldArg('text', 'Remove'),
                        'up_link_ident':FieldArg("url", 'no_javascript'),
                        'up_json_ident':FieldArg("url", ''),
                        'down_link_ident':FieldArg("url", 'no_javascript'),
                        'down_json_ident':FieldArg("url", ''),
                        'remove_link_ident':FieldArg("url", 'no_javascript'),
                        'remove_json_ident':FieldArg("url", ''),
                        'contents':FieldArgTable(['text', 'text', 'text', 'text'], valdt=True, jsonset=True)
                        }

    def __init__(self, name=None, brief='', **field_args):
        """
        highlight_class: CSS class will replace widget_class if set_highlight is True
        set_highlight: Set to True to force highlight_class to replace widget_class
                       Set to False to remove highlight_class and return to widget_class
        even_class: class of even rows, if empty string, then no class will be applied
        odd_class: class of odd rows, if empty string, then no class will be applied
        maximize_text_col: If True the text column is made large, with the button columns reduced to the size of the buttons
        hide: if True, table will be hidden
        button_class: The CSS class to apply to the buttons
        remove_button_text: Text on the Remove button
        up_link_ident: For the up arrow button: the target page link ident, label or url, if javascript not available
        up_json_ident: For the up arrow button: the url, ident or label to link, expecting a json file to be returned
        down_link_ident: For the down arrow button: the target page link ident, label or url, if javascript not available
        down_json_ident: For the down arrow button: the url, ident or label to link, expecting a json file to be returned
        remove_link_ident: For the Remove button: the target page link ident, label or url, if javascript not available
        remove_json_ident: For the Remove button: the url, ident or label to link, expecting a json file to be returned
        contents: col 0 is the text string to place in the first column,
                  col 1 is the get field contents of the up button link
                  col 2 is the get field contents of the down button link
                  col 3 is the get field contents of the remove button link
                  This fieldname used as the widgfield
        """
        Widget.__init__(self, name=name, brief=brief, **field_args)
        self.tag_name = "table"


    def _build(self, page, ident_list, environ, call_data, lang):
        "Build the table"
        # Hides widget if no error and hide is True
        self.widget_hide(self.wf.hide)
        fieldtable = self.wf.contents

        # any label:value added to self.jlabels will be set in a javascript fieldvalues attribute for the widget

        if self.wf.highlight_class:
            self.jlabels['highlight_class'] = self.wf.highlight_class
            if self.wf.set_highlight:
                self.attribs["class"] = self.wf.highlight_class
        self.jlabels['button_class'] = self.wf.button_class
        self.jlabels['remove_button_text'] = self.wf.remove_button_text

        # set even row colour
        if self.wf.even_class:
            even = self.wf.even_class
        else:
            even = ''
        self.jlabels['even_class'] = even

        # set odd row colour
        if self.wf.odd_class:
            odd = self.wf.odd_class
        else:
            odd = ''
        self.jlabels['odd_class'] = odd

        if self.wf.up_json_ident:
            self.jlabels['up_json_url'] = self.get_url(self.wf.up_json_ident)
        if self.wf.down_json_ident:
            self.jlabels['down_json_url'] = self.get_url(self.wf.down_json_ident)
        if self.wf.remove_json_ident:
            self.jlabels['remove_json_url'] = self.get_url(self.wf.remove_json_ident)

        if self.wf.up_link_ident:
            up_url = self.get_url(self.wf.up_link_ident)
            self.jlabels['up_link_url'] = up_url
        else:
            up_url = ''

        if self.wf.down_link_ident:
            down_url = self.get_url(self.wf.down_link_ident)
            self.jlabels['down_link_url'] = down_url
        else:
            down_url = ''

        if self.wf.remove_link_ident:
            remove_url = self.get_url(self.wf.remove_link_ident)
            self.jlabels['remove_link_url'] = remove_url
        else:
            remove_url = ''

        if self.wf.maximize_text_col:
           self.jlabels['maximize_text_col'] = True

        if not fieldtable:
            return
        len_fieldtable = len(fieldtable)
        lastrow = len_fieldtable - 1

        # create rows
        for rownumber, row in enumerate(fieldtable):
            if even and (rownumber % 2) :
                self[rownumber] = tag.Part(tag_name="tr", attribs={"class":even})
            elif odd and not (rownumber % 2):
                self[rownumber] = tag.Part(tag_name='tr', attribs={"class":odd})
            else:
                self[rownumber] = tag.Part(tag_name='tr')

            # first column is text
            if self.wf.maximize_text_col:
                self[rownumber][0] = tag.Part(tag_name='td', text = row[0], attribs={"style":"width : 100%;"})
            else:
                self[rownumber][0] = tag.Part(tag_name='td', text = row[0])

            # Next column is up button link
            self[rownumber][1] = tag.Part(tag_name='td')
            if not rownumber:
                # rownumber 0 has no up button
                self[rownumber][1][0] = tag.HTMLSymbol("&nbsp;")
            else:
                if self.wf.button_class:
                    self[rownumber][1][0] = tag.Part(tag_name='a', attribs = {"role":"button", "class":self.wf.button_class})
                else:
                    self[rownumber][1][0] = tag.Part(tag_name='a', attribs = {"role":"button"})
                self[rownumber][1][0].htmlescaped=False
                if up_url:
                    self[rownumber][1][0][0] = tag.HTMLSymbol("&uarr;")
                    # create a url for the href
                    get_fields = {self.get_formname("contents"):row[1]}
                    self[rownumber][1][0].attribs["href"] = self.make_get_url(page, up_url, get_fields, True)
                else:
                    self[rownumber][1][0] = "Warning: broken link"

            # Next column is down button link
            self[rownumber][2] = tag.Part(tag_name='td')
            if rownumber == lastrow:
                # last row has no down button
                self[rownumber][2][0] = tag.HTMLSymbol("&nbsp;")
            else:
                if self.wf.button_class:
                    self[rownumber][2][0] = tag.Part(tag_name='a', attribs = {"role":"button", "class":self.wf.button_class})
                else:
                    self[rownumber][2][0] = tag.Part(tag_name='a', attribs = {"role":"button"})
                self[rownumber][2][0].htmlescaped=False
                if down_url:
                    self[rownumber][2][0][0] = tag.HTMLSymbol("&darr;")
                    # create a url for the href
                    get_fields = {self.get_formname("contents"):row[2]}
                    self[rownumber][2][0].attribs["href"] = self.make_get_url(page, down_url, get_fields, True)
                else:
                    self[rownumber][2][0] = "Warning: broken link"

            # Next column is Remove button link
            self[rownumber][3] = tag.Part(tag_name='td')
            if self.wf.button_class:
                self[rownumber][3][0] = tag.Part(tag_name='a', attribs = {"role":"button", "class":self.wf.button_class})
            else:
                self[rownumber][3][0] = tag.Part(tag_name='a', attribs = {"role":"button"})
            self[rownumber][3][0].htmlescaped=False
            if remove_url:
                if self.wf.remove_button_text:
                    self[rownumber][3][0][0] = self.wf.remove_button_text
                else:
                    self[rownumber][3][0][0] = "Remove"
                # create a url for the href
                get_fields = {self.get_formname("contents"):row[3]}
                self[rownumber][3][0].attribs["href"] = self.make_get_url(page, remove_url, get_fields, True)
            else:
                self[rownumber][3][0] = "Warning: broken link"



    @classmethod
    def description(cls):
        """Returns a text string to illustrate the widget"""
        return """
<table>  <!-- with widget id and class widget_class -->
                   <!-- and attribute style=display:none if hide is True -->
  <tr> <!-- with class from even or odd classes -->
    <td> <!-- text string --> </td>
    <td>
      <a role="button" href="#">
      <!-- With class set by button_class, and the href link will be the url of the up_link_ident with get field -->
        &uarr;
      </a>
    </td>
    <td>
      <a role="button" href="#">
      <!-- With class set by button_class, and the href link will be the url of the down_link_ident with get field -->
        &darr;
      </a>
    </td>
    <td>
      <a role="button" href="#">
      <!-- With class set by button_class, and the href link will be the url of the remove_link_ident with get field -->
        Remove
      </a>
    </td>
  </tr>
  <!-- rows repeated -->
</table>"""

