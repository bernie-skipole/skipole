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
        """A g element which holds a chart, held in a 210 high x 510 wide space
           The vertical scale is +100 to -100
           values: a list of integers, each integer should be between -100 and +100
           with a maximum of fifty integers.
           These will be plotted on the chart at 10point intervals, with the
           last point on the right of the chart
        """
        Widget.__init__(self, name=name, tag_name="g", brief=brief, **field_args)
        self[0] = tag.ClosedPart(tag_name='rect', attribs={"x":"5",
                                                           "y":"5",
                                                           "width":"500",
                                                           "height":"200",
                                                           "fill":"white",
                                                           "stroke":"green",
                                                           "stroke-width":"1"})
        # centre line
        self[1] = tag.ClosedPart(tag_name='line', attribs={"x1":"5",
                                                           "y1":"105",
                                                           "x2":"505",
                                                           "y2":"105",
                                                           "stroke":"green",
                                                           "stroke-width":"3"})

        # 50 lines - horizontal
        self[2] = tag.ClosedPart(tag_name='line', attribs={"x1":"5",
                                                           "y1":"55",
                                                           "x2":"505",
                                                           "y2":"55",
                                                           "stroke":"green",
                                                           "stroke-width":"1"})
        self[3] = tag.ClosedPart(tag_name='line', attribs={"x1":"5",
                                                           "y1":"155",
                                                           "x2":"505",
                                                           "y2":"155",
                                                           "stroke":"green",
                                                           "stroke-width":"1"})
        # 50 lines - vertical
        for n in range(55, 505, 50):
            self.append(tag.ClosedPart(tag_name='line', attribs={"x1":str(n),
                                                                 "y1":"5",
                                                                 "x2":str(n),
                                                                 "y2":"205",
                                                                 "stroke":"green",
                                                                 "stroke-width":"1"}))


    def _build(self, page, ident_list, environ, call_data, lang):
        if self.get_field_value("transform"):
            self.update_attribs({"transform":self.get_field_value("transform")})

        if self.get_field_value("plus50legend"):
            charnumbers = len(self.get_field_value("plus50legend"))
            textlength = 5*charnumbers
            self.append(tag.ClosedPart(tag_name='rect', attribs={"x":"8",
                                                           "y":"45",
                                                           "width":str(textlength+10),
                                                           "height":"20",
                                                           "fill":"white",
                                                           "stroke-width":"0"}))
            self.append( tag.Part(tag_name='text',
                                  text=self.get_field_value("plus50legend"),
                                  attribs={
                                            'x':"10",
                                            'y':"58",
                                            'font-size': '10',
                                            'font-family': 'arial',
                                            'lengthAdjust':"spacingAndGlyphs",
                                            'textLength':str(textlength),
                                            'fill':"green",
                                            'stroke-width':"0"  }))

        if self.get_field_value("minus50legend"):
            charnumbers = len(self.get_field_value("minus50legend"))
            textlength = 5*charnumbers
            self.append(tag.ClosedPart(tag_name='rect', attribs={"x":"8",
                                                           "y":"145",
                                                           "width":str(textlength+10),
                                                           "height":"20",
                                                           "fill":"white",
                                                           "stroke-width":"0"}))
            self.append( tag.Part(tag_name='text',
                                  text=self.get_field_value("minus50legend"),
                                  attribs={
                                            'x':"10",
                                            'y':"158",
                                            'font-size': '10',
                                            'font-family': 'arial',
                                            'lengthAdjust':"spacingAndGlyphs",
                                            'textLength':str(textlength),
                                            'fill':"green",
                                            'stroke-width':"0"  }))


        if self.get_field_value("zerolegend"):
            charnumbers = len(self.get_field_value("zerolegend"))
            textlength = 5*charnumbers
            self.append(tag.ClosedPart(tag_name='rect', attribs={"x":"8",
                                                           "y":"95",
                                                           "width":str(textlength+10),
                                                           "height":"20",
                                                           "fill":"white",
                                                           "stroke-width":"0"}))
            self.append( tag.Part(tag_name='text',
                                  text=self.get_field_value("zerolegend"),
                                  attribs={
                                            'x':"10",
                                            'y':"108",
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
            self.append(tag.ClosedPart(tag_name='polyline', attribs={"points":"5,105, 505,105",
                                                                     "fill":"none",
                                                                     "stroke":stroke,
                                                                     "stroke-width":stroke_width}))

            return

        vals = list(reversed(values))

        xpoint = 515
        points = ""
        for ypoint in vals:
            xpoint = xpoint-10
            if xpoint < 5:
                break
            if ypoint > 100:
                y = "5"
            elif ypoint < -100:
                y = "205"
            else:
                y = str(105-ypoint)
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


