####### SKIPOLE WEB FRAMEWORK #######
#
# svgmeters.py  - defines SVG meters for displaying data
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
    """An svg arrow shape, fitting in a 100x100 space
    """

    # This class does not display any error messages
    display_errors = False

    _points = ((49,1), (50,1), (98,30), (98,32), (60,32), (60,98), (39,98), (39,32), (1,32), (1,30))

    arg_descriptions = {'fill':FieldArg("text", "none", jsonset=True),
                        'stroke':FieldArg("text", "black", jsonset=True),
                        'transform':FieldArg("text", "", jsonset=True),
                        'stroke_width':FieldArg("text", "1", jsonset=True)
                       }

    def __init__(self, name=None, brief='', **field_args):
        """
        fill: The fill colour, use none for no fill
        stroke: The outline edge colour
        stroke_width: The outline edge thickness
        transform: The svg transform object, use it to scals and rotate
        """
        Widget.__init__(self, name=name, tag_name="polygon", brief=brief, **field_args)
        self.hide_if_empty=False

    def _build(self, page, ident_list, environ, call_data, lang):
        "create arrow"                  
        attrib_points = ""
        for p in self._points:
            point = "%s, %s " % p
            attrib_points += point
        self.update_attribs({"points":attrib_points})

        if self.get_field_value("fill"):
            self.update_attribs({"fill":self.get_field_value("fill")})
        if self.get_field_value("stroke"):
            self.update_attribs({"stroke":self.get_field_value("stroke")})
        if self.get_field_value("transform"):
            self.update_attribs({"transform":self.get_field_value("transform")})
        if self.get_field_value("stroke_width"):
            self.update_attribs({"stroke-width":self.get_field_value("stroke_width")})

    def __str__(self):
        """Returns a text string to illustrate the widget"""
        return """
<polygon> <!-- arrow shape with widget id, class widget_class and the given attributes -->
</polygon>"""



class Arrow2(Widget):
    """A slim svg arrow shape, fitting in a 50x200 space
    """

    # This class does not display any error messages
    display_errors = False

    _points = ((24,1), (25,1), (49,50), (49,52), (30,52), (30,198), (19,198), (19,52), (1,52), (1,50))

    arg_descriptions = {'fill':FieldArg("text", "none", jsonset=True),
                        'stroke':FieldArg("text", "black", jsonset=True),
                        'transform':FieldArg("text", "", jsonset=True),
                        'stroke_width':FieldArg("text", "1", jsonset=True)
                       }

    def __init__(self, name=None, brief='', **field_args):
        """
        fill: The fill colour, use none for no fill
        stroke: The outline edge colour
        stroke_width: The outline edge thickness
        transform: The svg transform object, use it to scals and rotate
        """
        Widget.__init__(self, name=name, tag_name="polygon", brief=brief, **field_args)
        self.hide_if_empty=False

    def _build(self, page, ident_list, environ, call_data, lang):
        "create arrow"                  
        attrib_points = ""
        for p in self._points:
            point = "%s, %s " % p
            attrib_points += point
        self.update_attribs({"points":attrib_points})

        if self.get_field_value("fill"):
            self.update_attribs({"fill":self.get_field_value("fill")})
        if self.get_field_value("stroke"):
            self.update_attribs({"stroke":self.get_field_value("stroke")})
        if self.get_field_value("transform"):
            self.update_attribs({"transform":self.get_field_value("transform")})
        if self.get_field_value("stroke_width"):
            self.update_attribs({"stroke-width":self.get_field_value("stroke_width")})

    def __str__(self):
        """Returns a text string to illustrate the widget"""
        return """
<polygon> <!-- arrow shape with widget id, class widget_class and the given attributes -->
</polygon>"""




