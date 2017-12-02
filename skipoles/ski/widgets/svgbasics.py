####### SKIPOLE WEB FRAMEWORK #######
#
# basics.py  - defines basic building blocks for SVG images
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

from .. import tag
from . import Widget, ClosedWidget, FieldArg, FieldArgList, FieldArgTable, FieldArgDict



class SVGContainer(Widget):

    # This class does not display any error messages
    display_errors = False

    arg_descriptions = {
                        'width':FieldArg("text", "100", jsonset=True),
                        'height':FieldArg("text", "100", jsonset=True)
                       }

    _container = (0,)

    def __init__(self, name=None, brief='', **field_args):
        """Acts as an SVG widget, containing other widgets, so show, class and dimensions can be set"""
        Widget.__init__(self, name=name, tag_name="svg", brief=brief, **field_args)
        self[0] =  ""  # where items can be contained

    def _build(self, page, ident_list, environ, call_data, lang):
        if self.get_field_value("width"):
            self.update_attribs({"width":self.get_field_value("width")})
        if self.get_field_value("height"):
            self.update_attribs({"height":self.get_field_value("height")})        

    def __str__(self):
        """Returns a text string to illustrate the widget"""
        return """
<svg>  <!-- with widget id and class widget_class, and the given attributes -->
  <!-- further svg elements and widgets can be contained here -->
</svg>"""


class Group(Widget):

    # This class does not display any error messages
    display_errors = False

    arg_descriptions = {
                        'transform':FieldArg("text", "", jsonset=True)
                       }

    _container = (0,)

    def __init__(self, name=None, brief='', **field_args):
        """Acts as an g widget, containing other widgets, so group class, style, transform can be set"""
        Widget.__init__(self, name=name, tag_name="g", brief=brief, **field_args)
        self[0] =  ""  # where items can be contained

    def _build(self, page, ident_list, environ, call_data, lang):
        if self.get_field_value("transform"):
            self.update_attribs({"transform":self.get_field_value("transform")})

    def __str__(self):
        """Returns a text string to illustrate the widget"""
        return """
<g>  <!-- with widget id and class widget_class, and transform attribute if given -->
  <!-- further svg elements and widgets can be contained here -->
</g>"""


class Rect(ClosedWidget):
    """An svg rect tag
    """

    # This class does not display any error messages
    display_errors = False

    arg_descriptions = {'x':FieldArg("text", "0", jsonset=True),
                        'y':FieldArg("text", "0", jsonset=True),
                        'rx':FieldArg("text", "0", jsonset=True),
                        'ry':FieldArg("text", "0", jsonset=True),
                        'width':FieldArg("text", "100", jsonset=True),
                        'height':FieldArg("text", "100", jsonset=True),
                        'fill':FieldArg("text", "none", jsonset=True),
                        'stroke':FieldArg("text", "black", jsonset=True),
                        'stroke_width':FieldArg("text", "1", jsonset=True)
                       }

    def __init__(self, name=None, brief='', **field_args):
        """
        x: x coords, for example 0
        y: y coords, for example 0
        rx: x radius, for example 0
        ry: y radius, for example 0
        width: A width field, for example 100
        height: A height field, for example 100
        fill: The fill colour, use none for no fill
        stroke: The outline edge colour
        stroke_width: The outline edge width
        """
        # pass fields to Widget
        ClosedWidget.__init__(self, name=name, tag_name="rect", brief=brief, **field_args)
        self.hide_if_empty=False

    def _build(self, page, ident_list, environ, call_data, lang):
        "Set the attributes"
        # Note - all arg_descriptions are attributes, apart from stroke_width which is actually
        # attribute stroke-width. So update the tag with each item from arg_descriptions
        for att in self.arg_descriptions.keys():
            if self.get_field_value(att):
                if att == "stroke_width":
                    self.update_attribs({"stroke-width":self.get_field_value(att)})
                else:
                    self.update_attribs({att:self.get_field_value(att)})   

    def __str__(self):
        """Returns a text string to illustrate the widget"""
        return """
<rect /> <!-- creates rectangle with widget id, class widget_class and the given attributes -->"""



class SimpleText(Widget):
    """An svg text tag
    """

    # This class does not display any error messages
    display_errors = False

    arg_descriptions = {'x':FieldArg("text", "0", jsonset=True),
                        'y':FieldArg("text", "0", jsonset=True),
                        'dx':FieldArg("text", "0", jsonset=True),
                        'dy':FieldArg("text", "0", jsonset=True),
                        'font_family':FieldArg("text", "Arial", jsonset=True),
                        'font_size':FieldArg("text", "20", jsonset=True),
                        'fill':FieldArg("text", "white", jsonset=True),
                        'stroke':FieldArg("text", "", jsonset=True),
                        'stroke_width':FieldArg("text", "", jsonset=True),
                        'text':FieldArg("text", "", jsonset=True)
                       }

    def __init__(self, name=None, brief='', **field_args):
        """
        x: x coords, for example 0
        y: y coords, for example 0
        dx: x displacement from absolute value, for example 0
        dy: y displacement from absolute value, for example 0
        font_family: font-family css  attribute, such as Arial
        font_size: font-size css  attribute, such as 20
        fill: The fill colour, use none for no fill
        stroke: The outline edge colour
        stroke_width: The outline edge width
        text: The text to display
        """
        # pass fields to Widget
        Widget.__init__(self, name=name, tag_name="text", brief=brief, **field_args)
        self.hide_if_empty=False


    def _build(self, page, ident_list, environ, call_data, lang):
        "Set the attributes"
        if self.get_field_value("x"):
            self.update_attribs({"x":self.get_field_value("x")})
        if self.get_field_value("y"):
            self.update_attribs({"y":self.get_field_value("y")})
        if self.get_field_value("dx"):
            self.update_attribs({"dx":self.get_field_value("dx")})
        if self.get_field_value("dy"):
            self.update_attribs({"dy":self.get_field_value("dy")})
        if self.get_field_value("font_family"):
            self.update_attribs({"font-family":self.get_field_value("font_family")})
        if self.get_field_value("font_size"):
            self.update_attribs({"font-size":self.get_field_value("font_size")})
        if self.get_field_value("fill"):
            self.update_attribs({"fill":self.get_field_value("fill")})
        if self.get_field_value("stroke"):
            self.update_attribs({"stroke":self.get_field_value("stroke")})
        if self.get_field_value("stroke_width"):
            self.update_attribs({"stroke-width":self.get_field_value("stroke_width")})
        self[0] = self.get_field_value("text")


    def __str__(self):
        """Returns a text string to illustrate the widget"""
        return """
<text> <!-- with widget id, class widget_class and the given attributes -->
  <!-- contains given text -->
</text>"""


class Circle(ClosedWidget):
    """An svg circle tag
    """

    # This class does not display any error messages
    display_errors = False

    arg_descriptions = {'cx':FieldArg("text", "50", jsonset=True),
                        'cy':FieldArg("text", "50", jsonset=True),
                        'r':FieldArg("text", "40", jsonset=True),
                        'fill':FieldArg("text", "none", jsonset=True),
                        'stroke':FieldArg("text", "black", jsonset=True),
                        'stroke_width':FieldArg("text", "1", jsonset=True)
                       }

    def __init__(self, name=None, brief='', **field_args):
        """
        cx: centre x coords, for example 0
        cy: centre y coords, for example 0
        r: radius, for example 0
        fill: The fill colour, use none for no fill
        stroke: The outline edge colour
        stroke_width: The outline edge width
        """
        # pass fields to Widget
        ClosedWidget.__init__(self, name=name, tag_name="circle", brief=brief, **field_args)
        self.hide_if_empty=False

    def _build(self, page, ident_list, environ, call_data, lang):
        "Set the attributes"
        # Note - all arg_descriptions are attributes, apart from stroke_width which is actually
        # attribute stroke-width. So update the tag with each item from arg_descriptions
        for att in self.arg_descriptions.keys():
            if self.get_field_value(att):
                if att == "stroke_width":
                    self.update_attribs({"stroke-width":self.get_field_value(att)})
                else:
                    self.update_attribs({att:self.get_field_value(att)})   

    def __str__(self):
        """Returns a text string to illustrate the widget"""
        return """
<circle /> <!-- creates circle with widget id, class widget_class and the given attributes -->"""


class Line(ClosedWidget):
    """An svg line tag
    """

    # This class does not display any error messages
    display_errors = False

    arg_descriptions = {'x1':FieldArg("text", "0", jsonset=True),
                        'y1':FieldArg("text", "0", jsonset=True),
                        'x2':FieldArg("text", "100", jsonset=True),
                        'y2':FieldArg("text", "100", jsonset=True),
                        'stroke':FieldArg("text", "black", jsonset=True),
                        'stroke_width':FieldArg("text", "1", jsonset=True)
                       }

    def __init__(self, name=None, brief='', **field_args):
        """
        x1,y1: coordinates of line start
        x2,y2: coordinates of line end
        stroke: The line colour
        stroke_width: The outline edge width
        """
        # pass fields to Widget
        ClosedWidget.__init__(self, name=name, tag_name="line", brief=brief, **field_args)
        self.hide_if_empty=False

    def _build(self, page, ident_list, environ, call_data, lang):
        "Set the attributes"
        # Note - all arg_descriptions are attributes, apart from stroke_width which is actually
        # attribute stroke-width. So update the tag with each item from arg_descriptions
        for att in self.arg_descriptions.keys():
            if self.get_field_value(att):
                if att == "stroke_width":
                    self.update_attribs({"stroke-width":self.get_field_value(att)})
                else:
                    self.update_attribs({att:self.get_field_value(att)})   

    def __str__(self):
        """Returns a text string to illustrate the widget"""
        return """
<line /> <!-- creates line with widget id, class widget_class and the given attributes -->"""


