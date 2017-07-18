####### SKIPOLE WEB FRAMEWORK #######
#
# arrows.py  - defines SVG arrow images
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


class Arrow1(Widget):
    """An svg arrow shape
    """

    # This class does not display any error messages
    display_errors = False

    _points = ((49,1), (50,1), (98,30), (98,32), (60,32), (60,98), (39,98), (39,32), (1,32), (1,30))

    arg_descriptions = {'x':FieldArg("text", "0"),
                        'y':FieldArg("text", "0"),
                        'width':FieldArg("text", "100"),
                        'height':FieldArg("text", "100"),
                        'direction':FieldArg("text", "up"),
                        'fill':FieldArg("text", "none"),
                        'stroke':FieldArg("text", "black")
                       }

    def __init__(self, name=None, brief='', **field_args):
        """
        x: x coords, for example 0
        y: y coords, for example 0
        width: A width field, for example 100
        height: A height field, for example 100
        direction: One of left, right, up, down giving the direction of the arrows
        fill: The fill colour, use none for no fill
        stroke: The outline edge colour
        """
        Widget.__init__(self, name=name, tag_name="polygon", brief=brief, **field_args)
        self.hide_if_empty=False
        self.attribs = {"stroke-width":"2"}

    def _build(self, page, ident_list, environ, call_data, lang):
        # set points attrib
        self._scale()
        # set x,y translation
        self._transform()
        if self.get_field_value("fill"):
            self.update_attribs({"fill":self.get_field_value("fill")})
        if self.get_field_value("stroke"):
            self.update_attribs({"stroke":self.get_field_value("stroke")})


    def _scale(self):
        # remove px, em etc
        width = float(self.get_field_value("width"))
        height = float(self.get_field_value("height"))
        # normalise w, h to 100 == unity, to 3 decimal places
        x_scale = round(width/100.0, 3)
        y_scale = round(height/100.0, 3)
        if self.get_field_value("direction") == "up":
            points = [(x*x_scale, y*y_scale) for x,y in self._points]
        elif self.get_field_value("direction") == "left":
            points = [(y*x_scale, x*y_scale) for x,y in self._points]
        elif self.get_field_value("direction") == "right":
            points = [((99-y)*x_scale, x*y_scale) for x,y in self._points]
        elif self.get_field_value("direction") == "down":
            points = [(x*x_scale, (99-y)*y_scale) for x,y in self._points]
        else:
            points = [(x*x_scale, y*y_scale) for x,y in self._points]
        attrib_points = ""
        for p in points:
            point = "%s, %s " % p
            attrib_points += point
        self.update_attribs({"points":attrib_points})

    def _transform(self):
        t_x = self.get_field_value("x")
        t_y = self.get_field_value("y")
        if not t_x:
            t_x = 0
        if not t_y:
            t_y = 0
        if t_x or t_y:
            transform = "translate(%s, %s)" % (t_x, t_y)
            self.update_attribs({"transform":transform})


    def __str__(self):
        """Returns a text string to illustrate the widget"""
        return """
<polygon stroke-width="2"> <!-- creates outline of an arrow -->
</polygon>"""



class Arrow_U_R(Widget):
    """An svg arrow shape, pointing upwards and to the right
    """

    # This class does not display any error messages
    display_errors = False

    _points = ((40,2), (96,2), (98,4), (98,60), (96,60), (74.5,38.5), (15,98), (2,85), (61.5,25.5), (40,4))

    arg_descriptions = {'x':FieldArg("text", "0"),
                        'y':FieldArg("text", "0"),
                        'width':FieldArg("text", "100"),
                        'height':FieldArg("text", "100"),
                        'fill':FieldArg("text", "none"),
                        'stroke':FieldArg("text", "black")
                       }

    def __init__(self, name=None, brief='', **field_args):
        """
        x: x coords, for example 0
        y: y coords, for example 0
        width: A width field, for example 100
        height: A height field, for example 100
        fill: The fill colour, use none for no fill
        stroke: The outline edge colour
        """
        Widget.__init__(self, name=name, tag_name="polygon", brief=brief, **field_args)
        self.hide_if_empty=False
        self.attribs = {"stroke-width":"2"}

    def _build(self, page, ident_list, environ, call_data, lang):
        # set points attrib
        self._scale()
        # set x,y translation
        self._transform()
        if self.get_field_value("fill"):
            self.update_attribs({"fill":self.get_field_value("fill")})
        if self.get_field_value("stroke"):
            self.update_attribs({"stroke":self.get_field_value("stroke")})


    def _scale(self):
        # remove px, em etc
        width = float(self.get_field_value("width"))
        height = float(self.get_field_value("height"))
        # normalise w, h to 100 == unity, to 3 decimal places
        x_scale = round(width/100.0, 3)
        y_scale = round(height/100.0, 3)
        points = [(x*x_scale, y*y_scale) for x,y in self._points]
        attrib_points = ""
        for p in points:
            point = "%s, %s " % p
            attrib_points += point
        self.update_attribs({"points":attrib_points})

    def _transform(self):
        t_x = self.get_field_value("x")
        t_y = self.get_field_value("y")
        if not t_x:
            t_x = 0
        if not t_y:
            t_y = 0
        if t_x or t_y:
            transform = "translate(%s, %s)" % (t_x, t_y)
            self.update_attribs({"transform":transform})

    def __str__(self):
        """Returns a text string to illustrate the widget"""
        return """
<polygon stroke-width="2"> <!-- creates up-right outline of an arrow -->
</polygon>"""


class Arrow_D_R(Widget):
    """An svg arrow shape, pointing downwards and to the right
    """

    # This class does not display any error messages
    display_errors = False

    _points = ((15,2), (74.5,61.5), (96,40), (98,40), (98,96), (96,98), (40,98), (40,96), (61.5,74.5), (2,15))

    arg_descriptions = {'x':FieldArg("text", "0"),
                        'y':FieldArg("text", "0"),
                        'width':FieldArg("text", "100"),
                        'height':FieldArg("text", "100"),
                        'fill':FieldArg("text", "none"),
                        'stroke':FieldArg("text", "black")
                       }

    def __init__(self, name=None, brief='', **field_args):
        """
        x: x coords, for example 0
        y: y coords, for example 0
        width: A width field, for example 100
        height: A height field, for example 100
        fill: The fill colour, use none for no fill
        stroke: The outline edge colour
        """
        Widget.__init__(self, name=name, tag_name="polygon", brief=brief, **field_args)
        self.hide_if_empty=False
        self.attribs = {"stroke-width":"2"}

    def _build(self, page, ident_list, environ, call_data, lang):
        # set points attrib
        self._scale()
        # set x,y translation
        self._transform()
        if self.get_field_value("fill"):
            self.update_attribs({"fill":self.get_field_value("fill")})
        if self.get_field_value("stroke"):
            self.update_attribs({"stroke":self.get_field_value("stroke")})


    def _scale(self):
        # remove px, em etc
        width = float(self.get_field_value("width"))
        height = float(self.get_field_value("height"))
        # normalise w, h to 100 == unity, to 3 decimal places
        x_scale = round(width/100.0, 3)
        y_scale = round(height/100.0, 3)
        points = [(x*x_scale, y*y_scale) for x,y in self._points]
        attrib_points = ""
        for p in points:
            point = "%s, %s " % p
            attrib_points += point
        self.update_attribs({"points":attrib_points})

    def _transform(self):
        t_x = self.get_field_value("x")
        t_y = self.get_field_value("y")
        if not t_x:
            t_x = 0
        if not t_y:
            t_y = 0
        if t_x or t_y:
            transform = "translate(%s, %s)" % (t_x, t_y)
            self.update_attribs({"transform":transform})


    def __str__(self):
        """Returns a text string to illustrate the widget"""
        return """
<polygon stroke-width="2"> <!-- creates down-right outline of an arrow -->
</polygon>"""

