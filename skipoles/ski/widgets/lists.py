####### SKIPOLE WEB FRAMEWORK #######
#
# lists.py  - widgets displaying lists
#
# This file is part of the Skipole web framework
#
# Date : 20180116
#
# Author : Bernard Czenkusz
# Email  : bernie@skipole.co.uk
#
#
#   Copyright 2018 Bernard Czenkusz
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


"""Contains widgets for lists"""


from .. import skiboot, tag, excepts
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
        Widget.__init__(self, name=name, tag_name="ul", brief=brief, **field_args)
        self._even = ''
        self._odd = ''


    def _build(self, page, ident_list, environ, call_data, lang):
        "Build the list"
        contents = self.get_field_value("contents")
        # set even li class
        if self.get_field_value('even_class'):
            self._even = self.get_field_value('even_class')
        # set odd li class
        if self.get_field_value('odd_class'):
            self._odd = self.get_field_value('odd_class')

        for index, item in enumerate(contents):
            if self._even and (index % 2):
                self[index] = tag.Part(tag_name="li", attribs={"class":self._even}, text=item)
            elif self._odd and not (index % 2):
                self[index] = tag.Part(tag_name='li', attribs={"class":self._odd}, text=item)
            else:
                self[index] = tag.Part(tag_name='li', text=item)


    def _build_js(self, page, ident_list, environ, call_data, lang):
        """Sets list items"""
        return self._make_fieldvalues(even_class = self._even, odd_class = self._odd)


    def __str__(self):
        """Returns a text string to illustrate the widget"""
        return """<ul>  <!-- with widget id and class widget_class -->
  <li> <!-- with style from odd_class or even_class -->
      <!-- with text from each contents element -->
  </li>
  <!-- with appropriate number of list elements -->
</ul>
"""


