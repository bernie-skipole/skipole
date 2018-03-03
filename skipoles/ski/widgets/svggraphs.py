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

import math, datetime

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

    @classmethod
    def description(cls):
        """Returns a text string to illustrate the widget"""
        return """
<g>  <!-- with widget id and class widget_class, and transform attribute if given -->
  <rect /> <!-- the chart rectangle -->
  <!-- lines and text which draw the chart -->
  <polyline /> <!-- Draws the values on the chart -->
</g>"""




class Graph48Hr(Widget):

    # This class does not display any error messages
    display_errors = False


    arg_descriptions = {
                        'transform':FieldArg("text", "", jsonset=True),
                        'values':FieldArgTable(('text', 'datetime')),
                        'fill':FieldArg("text", "white"),
                        'fill_opacity':FieldArg("text", "1"),
                        'plotcol':FieldArg("text", "black"),
                        'font_family':FieldArg("text", "arial"),
                        'axiscol':FieldArg("text", "green"),
                        'minvalue':FieldArg("text", "0"),
                        'maxvalue':FieldArg("text", "100"),
                       }


    def __init__(self, name=None, brief='', **field_args):
        """A g element which holds a graph, held in a 1200 high x 1200 wide space
           values: a list of datetime objects within the last 48 hr
           These will be plotted on the chart from 48hr ago to now
        """
        Widget.__init__(self, name=name, tag_name="g", brief=brief, **field_args)
        self._hr = datetime.timedelta(hours=1)
        self._axiscol = "green"
        self._plotcol = "black"
        self._font_family = "arial"


    def _build(self, page, ident_list, environ, call_data, lang):
        if self.get_field_value("transform"):
            self.update_attribs({"transform":self.get_field_value("transform")})

        fill = self.get_field_value("fill")
        if not fill:
            fill = "white"

        fill_opacity = self.get_field_value("fill_opacity")
        if not fill_opacity:
            fill_opacity = "0"

        self._font_family = self.get_field_value("font_family")
        if not self._font_family:
            self._font_family = "arial"

        self._axiscol = self.get_field_value("axiscol")
        if not self._axiscol:
            self._axiscol = "green"

        self._plotcol = self.get_field_value("plotcol")
        if not self._plotcol:
            self._plotcol = "black"

        self[0] = tag.ClosedPart(tag_name='rect', attribs={"x":"240",
                                                           "y":"20",
                                                           "width":"960",
                                                           "height":"720",
                                                           "fill":fill,
                                                           "fill-opacity":fill_opacity,
                                                           "stroke":self._axiscol,
                                                           "stroke-width":"1"})

        values = self.get_field_value("values")
        if not values:
            return

        # create time axis

        maxt = values[0][1]
        for valpair in values:
            val, t = valpair
            # t is a datetime object
            if t > maxt:
                maxt = t

        # maxt is latest time
        maxt = maxt.replace(minute=0, second=0, microsecond=0) + self._hr
        mint = maxt - datetime.timedelta(days=2)

        axist = mint
        for h in range(0,49):
            x = str(240 + h*20)
            if (axist.hour == 6) or (axist.hour == 18):
                if (h>0) and (h<48):
                    self.append(tag.ClosedPart(tag_name='line', attribs={"x1":x,
                                                                         "y1":"740",
                                                                         "x2":x,
                                                                         "y2":"720",
                                                                         "stroke":self._axiscol,
                                                                         "stroke-width":"1"}))
            elif axist.hour == 12:
                if (h>0) and (h<48):
                    self.append(tag.ClosedPart(tag_name='line', attribs={"x1":x,
                                                                         "y1":"740",
                                                                         "x2":x,
                                                                         "y2":"715",
                                                                         "stroke":self._axiscol,
                                                                         "stroke-width":"1"}))
                self.append(tag.Part(tag_name='text', text="12:00", attribs={
                                                            'x':str(215 + h*20),
                                                            'y': "770",
                                                            'font-size': '20',
                                                            'font-family': self._font_family,
                                                            'fill':self._axiscol,
                                                            'stroke-width':"0"  }))
            elif axist.hour == 0:
                if (h>0) and (h<48):
                    self.append(tag.ClosedPart(tag_name='line', attribs={"x1":x,
                                                                         "y1":"740",
                                                                         "x2":x,
                                                                         "y2":"710",
                                                                         "stroke":self._axiscol,
                                                                         "stroke-width":"2"}))
                self.append(tag.Part(tag_name='text', text=axist.strftime("%d %b"), attribs={
                                                            'x':str(215 + h*20),
                                                            'y': "770",
                                                            'font-size': '20',
                                                            'font-family': self._font_family,
                                                            'fill':self._axiscol,
                                                            'stroke-width':"0"  }))
                self.append(tag.Part(tag_name='text', text="00:00", attribs={
                                                            'x':str(215 + h*20),
                                                            'y': "790",
                                                            'font-size': '20',
                                                            'font-family': self._font_family,
                                                            'fill':self._axiscol,
                                                            'stroke-width':"0"  }))

            elif (h>0) and (h<48):
                self.append(tag.ClosedPart(tag_name='line', attribs={"x1":x,
                                                                     "y1":"740",
                                                                     "x2":x,
                                                                     "y2":"730",
                                                                     "stroke":self._axiscol,
                                                                     "stroke-width":"1"}))

            axist = axist + self._hr

        # create Y axis
        minv = self.get_field_value("minvalue")
        maxv = self.get_field_value("maxvalue")

        isint = True
        try: 
            int_minv = int(minv)
        except ValueError:
            isint = False
        if isint:
            try: 
                int_maxv = int(maxv)
            except ValueError:
                isint = False

        if isint and (int_maxv > int_minv+4):
            # create a Y axis of integer values
            int_maxv, str_minv, str_maxv = self._integer_axis(int_maxv, int_minv)
        else:
            int_maxv, str_minv, str_maxv = self._float_axis(float(maxv), float(minv))


        ymin = Decimal(str_minv)
        ymax = Decimal(str_maxv)

        # y = m*val + c
        # m = 720 / (ymax-ymin)
        # c = -m*ymin

        m = Decimal("720") / (ymax-ymin)
        c = -ymin*m

        # for each point, plot a + on the graph
        for valpair in values:
            val, t = valpair
            if t < mint:
                # early point outside plottable range
                continue
            val = Decimal(val)
            if val < ymin:
                # low point outside plottable range
                continue
            if val > ymax:
                # high point outside plottable range
                continue
            tdelta = t-mint
            seconds = tdelta.total_seconds()
            x = int(960 * seconds / 172800)
            y = int(m*val + c)
            self._plot_cross(x, y)


    def _plot_cross(self, x, y):
        "plot a + on the graph at x, y"
        # Vertical line
        self.append(tag.ClosedPart(tag_name='line', attribs={"x1":str(240+x),
                                                             "y1":str(735-y),
                                                             "x2":str(240+x),
                                                             "y2":str(745-y),
                                                             "stroke":self._plotcol,
                                                             "stroke-width":"1"}))
        # Horizontal line
        self.append(tag.ClosedPart(tag_name='line', attribs={"x1":str(235+x),
                                                             "y1":str(740-y),
                                                             "x2":str(245+x),
                                                             "y2":str(740-y),
                                                             "stroke":self._plotcol,
                                                             "stroke-width":"1"}))

    def _float_axis(self, maxv, minv):
        "create a Y axis of float values, return new int_maxv, str_minv, str_maxv"
        if minv == 0.0:
            # convert 0.0045 to 45
            # convert 4500.0 to 45
            tens = math.floor(math.log10(abs(maxv)))-1
            maxy = math.ceil(maxv/10**tens)
            return self._integer_axis(maxy, 0, tens)
        else:
            diff = maxv - minv
            tens = math.floor(math.log10(abs(diff)))-1
            maxy = math.ceil(maxv/10**tens)
            miny = math.floor(minv/10**tens)
            return self._integer_axis(maxy, miny, tens)



    def _integer_axis(self, int_maxv, int_minv, tens=0):
        "create a Y axis of integer values, if necessary increase int_maxv, return new int_maxv, str_minv, str_maxv"
        # diff is the difference between minimum and maximum, divide it into intervals
        # the number of intervals should also divide 720 pixels nicely, i.e. 16, 15, 12, 10, 9, 8, 6, 5
        diff = int_maxv - int_minv

        # order of prefferred interval spacing
        prefferred = (5, 10, 2, 15, 4, 25, 20)

        difftens = math.floor(math.log10(diff))

        if difftens>2:
            prefferred = ( item * 10**(difftens-1) for item in prefferred)

        number_of_intervals = 0
        for i in prefferred:
            if (diff % i == 0) and (diff//i in (16, 15, 12, 10, 9, 8, 6, 5)):
                # intervals with spacing of i is given priority
                number_of_intervals = diff//i
                break

        if not number_of_intervals:
            if diff % 16 == 0:
                # divide axis by sixteen
                number_of_intervals = 16
            elif diff % 15 == 0:
                # divide axis by fifteen
                number_of_intervals = 15
            elif diff % 12 == 0:
                # divide axis by twelve
                number_of_intervals = 12
            elif diff % 10 == 0:
                # divide axis by ten
                number_of_intervals = 10
            elif diff % 9 == 0:
                # divide axis by nine
                number_of_intervals = 9
            elif diff % 8 == 0:
                # divide axis by eight
                number_of_intervals = 8
            elif diff % 6 == 0:
                # divide axis by six
                number_of_intervals = 6
            elif diff % 5 == 0:
                # divide axis by five
                number_of_intervals = 5
            else:
                # None of the above go nicely into diff, so add 1 to int_maxv and try again
                return self._integer_axis(int_maxv+1, int_minv, tens)

        if tens:
            mult = Decimal("1e" + str(tens))
            if abs(tens)>3:
                fstring = "0.4g"
            elif tens<0:
                fstring = "0." + str(abs(tens)) + "f"
            else:
                fstring = "0.2f"
        else:
            mult = 1
            fstring = ''

        # put the maximum value at the top of the axis
        str_maxv = format(int_maxv*mult, fstring)
        self.append(tag.Part(tag_name='text', text=str_maxv, attribs={
                                                                    'x':str(220),
                                                                    'y': "25",
                                                                    'text-anchor':'end',
                                                                    'font-size': '20',
                                                                    'font-family': self._font_family,
                                                                    'fill':self._axiscol,
                                                                    'stroke-width':"0"  }))

        # put the minimum value at the bottom of the axis
        if int_minv:
            str_minv = format(int_minv*mult, fstring)
        else:
            str_minv = "0"
        self.append(tag.Part(tag_name='text', text=str_minv, attribs={
                                                                'x':str(220),
                                                                'y': "745",
                                                                'text-anchor':'end',
                                                                'font-size': '20',
                                                                'font-family': self._font_family,
                                                                'fill':self._axiscol,
                                                                'stroke-width':"0"  }))


        # yval is the axis value at the intervals, so starting from the top
        yval = int_maxv
        y_interval = diff//number_of_intervals
        # pixel_interval is the number of pixels in the interval
        pixel_interval = 720//number_of_intervals
        # with range limits so no line at top and bottem - so rectangle not overdrawn
        for y in range(pixel_interval+20, 740, pixel_interval):
            yval -= y_interval
            self.append(tag.ClosedPart(tag_name='line', attribs={"x1":"240",
                                                                 "y1":str(y),
                                                                 "x2":"260",
                                                                 "y2":str(y),
                                                                 "stroke":self._axiscol,
                                                                 "stroke-width":"1"}))
            self.append(tag.Part(tag_name='text', text=format(yval*mult, fstring), attribs={
                                                                        'x':str(220),
                                                                        'y': str(y+5),
                                                                        'text-anchor':'end',
                                                                        'font-size': '20',
                                                                        'font-family': self._font_family,
                                                                        'fill':self._axiscol,
                                                                        'stroke-width':"0"  }))
        return int_maxv, str_minv, str_maxv



    @classmethod
    def description(cls):
        """Returns a text string to illustrate the widget"""
        return """
<g>  <!-- with widget id and class widget_class, and transform attribute if given -->
  <rect x="240" y="20" height="720" width="960" /> <!-- the axis rectangle -->
  <!-- lines and text which draw the graph -->
</g>"""

