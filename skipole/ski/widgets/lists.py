

"""Contains widgets for lists"""

from .. import tag
from . import Widget, ClosedWidget, FieldArg, FieldArgList, FieldArgTable, FieldArgDict


class UList1(Widget):
    """An unordered list widget."""

    # This class does not display any error messages
    display_errors = False

    arg_descriptions = {
                       'contents': FieldArgList('text', jsonset=True),
                       'even_class':FieldArg("cssclass", ""),
                       'odd_class':FieldArg("cssclass", "")
                       }

    def __init__(self, name=None, brief='', **field_args):
        """
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
                       'set_html': FieldArgList('text', jsonset=True),
                       'even_class':FieldArg("cssclass", ""),
                       'odd_class':FieldArg("cssclass", "")
                       }

    def __init__(self, name=None, brief='', **field_args):
        """
        set_html: List of html strings to be shown, html will be shown unescaped
        even_class: class of even li elements, if empty string, then no class will be applied
        odd_class: class of odd li elements, if empty string, then no class will be applied
        """
        Widget.__init__(self, name=name, brief=brief, **field_args)
        self.tag_name = "ul"
        self._even = ''
        self._odd = ''

    def _build(self, page, ident_list, environ, call_data, lang):
        "Build the list"
        contents = self.wf.set_html

        # any label:value added to self.jlabels will be set in a javascript fieldvalues attribute for the widget

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



