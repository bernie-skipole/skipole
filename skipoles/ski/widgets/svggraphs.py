####### SKIPOLE WEB FRAMEWORK #######
#
# svggraphs.py  - defines SVG graphs for displaying data
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

import math

from decimal import Decimal

from .. import tag

from . import Widget, ClosedWidget, FieldArg, FieldArgList, FieldArgTable, FieldArgDict


class Chart1(Widget):

    # This class does not display any error messages
    display_errors = False


    arg_descriptions = {
                        'transform':FieldArg("text", "", jsonset=True),
                        'values':FieldArgList('integer', jsonset=True),
                        'stroke_width':FieldArg("integer", 1),
                        'stroke':FieldArg("text", "black"),
                        'plus50legend':FieldArg("text", ""),
                        'minus50legend':FieldArg("text", ""),
                        'zerolegend':FieldArg("text", ""),
                       }


    def __init__(self, name=None, brief='', **field_args):
        """A g element which holds a chart, held in a 200 high x 500 wide space
           The vertical scale is +100 to -100
           values: a list of integers, each integer should be between -100 and +100
           with a maximum of fifty integers.
           These will be plotted on the chart at 10point intervals, with the
           last point on the right of the chart
        """
        Widget.__init__(self, name=name, tag_name="g", brief=brief, **field_args)
        self[0] = tag.ClosedPart(tag_name='rect', attribs={"x":"0",
                                                           "y":"0",
                                                           "width":"500",
                                                           "height":"200",
                                                           "fill":"white",
                                                           "stroke":"green",
                                                           "stroke-width":"1"})
        # centre line
        self[1] = tag.ClosedPart(tag_name='line', attribs={"x1":"0",
                                                           "y1":"100",
                                                           "x2":"500",
                                                           "y2":"100",
                                                           "stroke":"green",
                                                           "stroke-width":"3"})

        # 50 lines - horizontal
        self[2] = tag.ClosedPart(tag_name='line', attribs={"x1":"0",
                                                           "y1":"50",
                                                           "x2":"500",
                                                           "y2":"50",
                                                           "stroke":"green",
                                                           "stroke-width":"1"})
        self[3] = tag.ClosedPart(tag_name='line', attribs={"x1":"0",
                                                           "y1":"150",
                                                           "x2":"500",
                                                           "y2":"150",
                                                           "stroke":"green",
                                                           "stroke-width":"1"})
        # 50 lines - vertical
        for n in range(50, 500, 50):
            self.append(tag.ClosedPart(tag_name='line', attribs={"x1":str(n),
                                                                 "y1":"0",
                                                                 "x2":str(n),
                                                                 "y2":"200",
                                                                 "stroke":"green",
                                                                 "stroke-width":"1"}))


    def _build(self, page, ident_list, environ, call_data, lang):
        if self.get_field_value("transform"):
            self.update_attribs({"transform":self.get_field_value("transform")})

        if self.get_field_value("plus50legend"):
            charnumbers = len(self.get_field_value("plus50legend"))
            textlength = 5*charnumbers
            self.append(tag.ClosedPart(tag_name='rect', attribs={"x":"3",
                                                           "y":"40",
                                                           "width":str(textlength+10),
                                                           "height":"20",
                                                           "fill":"white",
                                                           "stroke-width":"0"}))
            self.append( tag.Part(tag_name='text',
                                  text=self.get_field_value("plus50legend"),
                                  attribs={
                                            'x':"5",
                                            'y':"53",
                                            'font-size': '10',
                                            'font-family': 'arial',
                                            'lengthAdjust':"spacingAndGlyphs",
                                            'textLength':str(textlength),
                                            'fill':"green",
                                            'stroke-width':"0"  }))

        if self.get_field_value("minus50legend"):
            charnumbers = len(self.get_field_value("minus50legend"))
            textlength = 5*charnumbers
            self.append(tag.ClosedPart(tag_name='rect', attribs={"x":"3",
                                                           "y":"140",
                                                           "width":str(textlength+10),
                                                           "height":"20",
                                                           "fill":"white",
                                                           "stroke-width":"0"}))
            self.append( tag.Part(tag_name='text',
                                  text=self.get_field_value("minus50legend"),
                                  attribs={
                                            'x':"5",
                                            'y':"153",
                                            'font-size': '10',
                                            'font-family': 'arial',
                                            'lengthAdjust':"spacingAndGlyphs",
                                            'textLength':str(textlength),
                                            'fill':"green",
                                            'stroke-width':"0"  }))


        if self.get_field_value("zerolegend"):
            charnumbers = len(self.get_field_value("zerolegend"))
            textlength = 5*charnumbers
            self.append(tag.ClosedPart(tag_name='rect', attribs={"x":"3",
                                                           "y":"90",
                                                           "width":str(textlength+10),
                                                           "height":"20",
                                                           "fill":"white",
                                                           "stroke-width":"0"}))
            self.append( tag.Part(tag_name='text',
                                  text=self.get_field_value("zerolegend"),
                                  attribs={
                                            'x':"5",
                                            'y':"103",
                                            'font-size': '10',
                                            'font-family': 'arial',
                                            'lengthAdjust':"spacingAndGlyphs",
                                            'textLength':str(textlength),
                                            'fill':"green",
                                            'stroke-width':"0"  }))

        stroke_width = self.get_field_value("stroke_width")
        if not stroke_width:
            stroke_width = "1"
        else:
            stroke_width = str(stroke_width)

        stroke = self.get_field_value("stroke")
        if not stroke:
            stroke = "black"

        values = self.get_field_value("values")
        if not values:
            # still include a polyline tag, for javascript to find
            self.append(tag.ClosedPart(tag_name='polyline', attribs={"points":"",
                                                                     "fill":"none",
                                                                     "stroke":stroke,
                                                                     "stroke-width":stroke_width}))

            return

        vals = list(reversed(values))

        xpoint = 510
        points = ""
        for ypoint in vals:
            xpoint = xpoint-10
            if xpoint < 0:
                break
            if ypoint > 100:
                y = "0"
            elif ypoint < -100:
                y = "200"
            else:
                y = str(100-ypoint)
            points = points + " " + str(xpoint) + "," + y

        self.append(tag.ClosedPart(tag_name='polyline', attribs={"points":points,
                                                                 "fill":"none",
                                                                 "stroke":stroke,
                                                                 "stroke-width":stroke_width}))

    def __str__(self):
        """Returns a text string to illustrate the widget"""
        return """
<g>  <!-- with widget id and class widget_class, and transform attribute if given -->
  <rect /> <!-- the chart rectangle -->
  <!-- lines and text which draw the chart -->
  <polyline /> <!-- Draws the values on the chart -->
</g>"""


