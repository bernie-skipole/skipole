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
from . import Widget, FieldArg, FieldArgList, FieldArgTable, FieldArgDict



class Rect(Widget):
    """An svg rect tag

    If the fill, stroke and stroke_width fields are set to empty,
    the svg image containing this rectangle should link to a css page
    with appropriate style settings for the rect tag.
    (Note stroke_width changes to stroke-width in a css context)

    For example:

    rect {fill:"red";stroke:"blue";stroke-width:3}
    """

    # This class does not display any error messages
    display_errors = False

    arg_descriptions = {'x':FieldArg("text", "0"),
                        'y':FieldArg("text", "0"),
                        'rx':FieldArg("text", "0"),
                        'ry':FieldArg("text", "0"),
                        'width':FieldArg("text", "100"),
                        'height':FieldArg("text", "100"),
                        'fill':FieldArg("text", "none"),
                        'stroke':FieldArg("text", "black"),
                        'stroke_width':FieldArg("text", "1")
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
        Widget.__init__(self, name=name, tag_name="rect", brief=brief, **field_args)
        self.hide_if_empty=False

    def _build(self, page, ident_list, environ, call_data, lang):
        self.attribs = {"x":self.get_field_value("x"),
                        "y":self.get_field_value("y"),
                        "rx":self.get_field_value("rx"),
                        "ry":self.get_field_value("ry"),
                        "width":self.get_field_value("width"),
                        "height":self.get_field_value("height")}
        if self.get_field_value("fill"):
            self.update_attribs({"fill":self.get_field_value("fill")})
        if self.get_field_value("stroke"):
            self.update_attribs({"stroke":self.get_field_value("stroke")})
        if self.get_field_value("stroke_width"):
            self.update_attribs({"stroke-width":self.get_field_value("stroke_width")})


    def __str__(self):
        """Returns a text string to illustrate the widget"""
        return """
<rect> <!-- creates rectangle -->
</rect>"""



class SimpleText(Widget):
    """An svg text tag

    If the fill, stroke, font_family and font_size fields are empty,
    the svg image containing this text should link to a css page
    with appropriate style settings for the text tag.
    (Note font_family etc., changes to font-family... in a css context)

    For example:

    text {fill:"red";stroke:"blue";font-family:"Arial"}
    """

    # This class does not display any error messages
    display_errors = False

    arg_descriptions = {'x':FieldArg("text", "0"),
                        'y':FieldArg("text", "0"),
                        'dx':FieldArg("text", "0"),
                        'dy':FieldArg("text", "0"),
                        'font_family':FieldArg("text", "Arial"),
                        'font_size':FieldArg("text", "20"),
                        'fill':FieldArg("text", "white"),
                        'stroke':FieldArg("text", ""),
                        'stroke_width':FieldArg("text", ""),
                        'text':FieldArg("text", "")
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
        self.attribs = {"x":self.get_field_value("x"),
                        "y":self.get_field_value("y"),
                        "dx":self.get_field_value("dx"),
                        "dy":self.get_field_value("dy")}

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
<text>
  <!-- contains given text -->
</text>"""


