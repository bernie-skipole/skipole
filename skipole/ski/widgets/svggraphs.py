

import math, datetime

from decimal import Decimal, ROUND_UP
from collections import namedtuple

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
                        'font_family':FieldArg("text", "arial")
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

        font_family = self.get_field_value("font_family")
        if not font_family:
            font_family = "arial"

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
                                            'font-family': font_family,
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
                                            'font-family': font_family,
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
                                            'font-family': font_family,
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
                        'last_day':FieldArg("date", "")
                       }


    def __init__(self, name=None, brief='', **field_args):
        """A g element which holds a graph, held in a 1200 high x 1400 wide space
           values: a list of datetime objects covering a 48 hr period
           These will be plotted on the chart to the latest date in the values
           If last_day given, rightmost axis will be midnight of that day 
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
        last_day = self.get_field_value("last_day")

        if (not values) and (not last_day):
            # do not know when to plot
            return

        # get maxt the last datetime to plot
        if last_day:
            # set maxt at midnight of last_day
            maxt = datetime.datetime(last_day.year, last_day.month, last_day.day) + datetime.timedelta(days=1)
        else:
            # set maxt as the start of the hour after the last plotted value
            maxt = values[0][1]
            for valpair in values:
                val, t = valpair
                # t is a datetime object
                if t > maxt:
                    maxt = t
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
            if t > maxt:
                # late point outside plottable range
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



class StarChart(Widget):

    # This class does not display any error messages
    display_errors = False


    arg_descriptions = {
                        'transform':FieldArg("text", "", jsonset=True),
                        'fill':FieldArg("text", "white"),
                        'stroke_width':FieldArg("integer", 1),
                        'stroke':FieldArg("text", "black"),
                        'stars':FieldArgTable(('text', 'text', 'text')),   # star diameter, ra, dec
                        'lines':FieldArgTable(('text', 'text', 'text', 'text')),   # line start ra, dec to line end ra, dec
                        'ra':FieldArg("text", "0"),      # right ascension 0 to 360
                        'dec':FieldArg("text", "90"),    # declination 90 to -90
                        'view':FieldArg("text", "180"),  # the field of view
                        'cross':FieldArg("boolean", False),
                        'square':FieldArg("boolean", False)
                       }


    def __init__(self, name=None, brief='', **field_args):
        """A g element which holds a circular star chart, held in a 500 high x 500 wide space
        """
        Widget.__init__(self, name=name, tag_name="g", brief=brief, **field_args)
        self[0] = tag.ClosedPart(tag_name='circle', attribs={"cx":"250",
                                                             "cy":"250",
                                                             "r":"250",
                                                             "fill":"white",
                                                             "stroke":"black",
                                                             "stroke-width":"1"})


    def _build(self, page, ident_list, environ, call_data, lang):
        if self.get_field_value("transform"):
            self.update_attribs({"transform":self.get_field_value("transform")})
        stroke_width = self.get_field_value("stroke_width")
        if stroke_width:
            self[0].update_attribs({"stroke-width":str(stroke_width)})
        # stroke will be the star colour
        stroke = self.get_field_value("stroke")
        if stroke:
            self[0].update_attribs({"stroke":stroke})
        fill = self.get_field_value("fill")
        if fill:
            self[0].update_attribs({"fill":fill})
        if not self.get_field_value("stars"):
            return

        # limit centre of the chart
        ra0_deg = float(self.get_field_value("ra"))
        if (ra0_deg < 0.0) or (ra0_deg > 360.0):
            ra0_deg = 0.0
        ra0 = math.radians(ra0_deg)

        dec0_deg = float(self.get_field_value("dec"))
        if dec0_deg > 90.0:
            dec0_deg = 90.0
        if dec0_deg < -90.0:
            dec0_deg = -90.0
        dec0 = math.radians(dec0_deg)

        view_deg = float(self.get_field_value("view"))

        # avoid division by zero
        if view_deg < 0.000001:
            view_deg = 0.00001

        # avoid extra wide angle
        if view_deg > 270.0:
            view_deg = 270.0

        max_dec = dec0_deg + view_deg / 2.0
        if max_dec > 90.0:
            max_dec = 90.0

        min_dec = dec0_deg - view_deg / 2.0
        if min_dec < -90.0:
            min_dec = -90.0

        scale = 500 / math.radians(view_deg)

        cosdec0 = math.cos(dec0)
        sindec0 = math.sin(dec0)

        # stereographic algorithm
        # taken from www.projectpluto.com/project.htm


        for star in self.get_field_value("stars"):

            ra_deg = float(star[1])
            dec_deg = float(star[2])

            if (ra_deg < 0.0) or (ra_deg > 360.0):
                # something wrong, do not plot this star
                continue

            # don't calculate star position if its declination is outside required view
            # unfortunately ra is more complicated
            if dec_deg > max_dec:
                continue
            if dec_deg < min_dec:
                continue

            # get the radius of a star circle to plot
            if star[0]:
                radius = float(star[0])/2.0
            else:
                radius = 0.5
            if radius < 0.1:
                radius = 0.1

            ra = math.radians(ra_deg)
            dec = math.radians(dec_deg)
            delta_ra = ra - ra0
            sindec = math.sin(dec)
            cosdec = math.cos(dec)
            cosdelta_ra = math.cos(delta_ra)

            x1 = cosdec * math.sin(delta_ra);
            y1 = sindec * cosdec0 - cosdec * cosdelta_ra * sindec0
            z1 = sindec * sindec0 + cosdec * cosdec0 * cosdelta_ra
            if z1 < -0.9:
               d = 20.0 * math.sqrt(( 1.0 - 0.81) / ( 1.00001 - z1 * z1))
            else:
               d = 2.0 / (z1 + 1.0)
            x = x1 * d * scale
            y = y1 * d * scale

            if x*x + y*y > 62500:
                # star position is outside the circle
                continue

            # move origin to circle centre (250,250)
            cx = 250 - x
            cy = 250 - y
            self.append(tag.ClosedPart(tag_name='circle', attribs={"cx":str(cx),
                                                                   "cy":str(cy),
                                                                   "r":str(radius),
                                                                   "fill":stroke,
                                                                   "stroke":stroke}))


        if self.get_field_value("square"):
            # plot a square on the chart centre
            self.append(tag.ClosedPart(tag_name='rect', attribs={"x":"240",
                                                                 "y":"240",
                                                                 "width":"20",
                                                                 "height":"20",
                                                                 "style":"stroke:%s;stroke-width:1;fill-opacity:0;" % (stroke,)}))

        if self.get_field_value("cross"):
            # plot a + on the chart centre
            self.append(tag.ClosedPart(tag_name='line', attribs={"x1":"240",
                                                                 "y1":"250",
                                                                 "x2":"260",
                                                                 "y2":"250",
                                                                 "stroke":stroke,
                                                                 "stroke-width":"1"}))
            self.append(tag.ClosedPart(tag_name='line', attribs={"x1":"250",
                                                                 "y1":"240",
                                                                 "x2":"250",
                                                                 "y2":"260",
                                                                 "stroke":stroke,
                                                                 "stroke-width":"1"}))

        for line in self.get_field_value("lines"):

            start_ra_deg = float(line[0])
            start_dec_deg = float(line[1])
            end_ra_deg = float(line[2])
            end_dec_deg = float(line[3])

            if (start_ra_deg < 0.0) or (start_ra_deg > 360.0) or (end_ra_deg < 0.0) or (end_ra_deg > 360.0):
                # something wrong, do not plot this line
                continue

            # don't draw line if either start or end declination is outside required view
            # unfortunately ra is more complicated
            if start_dec_deg > max_dec:
                continue
            if start_dec_deg < min_dec:
                continue
            if end_dec_deg > max_dec:
                continue
            if end_dec_deg < min_dec:
                continue

            # start of line
            ra = math.radians(start_ra_deg)
            dec = math.radians(start_dec_deg)
            delta_ra = ra - ra0
            sindec = math.sin(dec)
            cosdec = math.cos(dec)
            cosdelta_ra = math.cos(delta_ra)

            x1 = cosdec * math.sin(delta_ra);
            y1 = sindec * cosdec0 - cosdec * cosdelta_ra * sindec0
            z1 = sindec * sindec0 + cosdec * cosdec0 * cosdelta_ra
            if z1 < -0.9:
               d = 20.0 * math.sqrt(( 1.0 - 0.81) / ( 1.00001 - z1 * z1))
            else:
               d = 2.0 / (z1 + 1.0)
            x = x1 * d * scale
            y = y1 * d * scale

            if x*x + y*y > 62500:
                # line start position is outside the circle
                continue

            # move origin to circle centre (250,250)
            startx = 250 - x
            starty = 250 - y

            # end of line
            ra = math.radians(end_ra_deg)
            dec = math.radians(end_dec_deg)
            delta_ra = ra - ra0
            sindec = math.sin(dec)
            cosdec = math.cos(dec)
            cosdelta_ra = math.cos(delta_ra)

            x1 = cosdec * math.sin(delta_ra);
            y1 = sindec * cosdec0 - cosdec * cosdelta_ra * sindec0
            z1 = sindec * sindec0 + cosdec * cosdec0 * cosdelta_ra
            if z1 < -0.9:
               d = 20.0 * math.sqrt(( 1.0 - 0.81) / ( 1.00001 - z1 * z1))
            else:
               d = 2.0 / (z1 + 1.0)
            x = x1 * d * scale
            y = y1 * d * scale

            if x*x + y*y > 62500:
                # line end position is outside the circle
                continue

            # move origin to circle centre (250,250)
            endx = 250 - x
            endy = 250 - y

            self.append(tag.ClosedPart(tag_name='line', attribs={"x1":str(startx),
                                                                 "y1":str(starty),
                                                                 "x2":str(endx),
                                                                 "y2":str(endy),
                                                                 "stroke":stroke,
                                                                 "stroke-width":"1"}))

 
    @classmethod
    def description(cls):
        """Returns a text string to illustrate the widget"""
        return """
<g>  <!-- with widget id and class widget_class, and transform attribute if given -->
  <circle /> <!-- A circle with fill, stroke and stroke width, and diameter 500 -->
  <!-- with multiple 'star' spots, positioned according to the given ra and dec values -->
  <!-- and each with a drawn diameter given per star -->
  <!-- centre cross drawn if cross is True -->
</g>"""



class StarChartXY(Widget):

    # This class does not display any error messages
    display_errors = False


    arg_descriptions = {
                        'transform':FieldArg("text", "", jsonset=True),
                        'fill':FieldArg("text", "white"),
                        'stroke_width':FieldArg("integer", 1),
                        'stroke':FieldArg("text", "black"),
                        'stars':FieldArgTable(('text', 'text', 'text'), jsonset=True),   # star diameter, x, y positions on the chart
                        'lines':FieldArgTable(('text', 'text', 'text', 'text'), jsonset=True),   # line start x, y to line end x, y
                        'cross':FieldArg("boolean", False),
                        'square':FieldArg("boolean", False)
                       }


    def __init__(self, name=None, brief='', **field_args):
        """A g element which holds a circular star chart, held in a 500 high x 500 wide space
        """
        Widget.__init__(self, name=name, tag_name="g", brief=brief, **field_args)
        self[0] = tag.ClosedPart(tag_name='circle', attribs={"cx":"250",
                                                             "cy":"250",
                                                             "r":"250",
                                                             "fill":"white",
                                                             "stroke":"black",
                                                             "stroke-width":"1"})



    def _build(self, page, ident_list, environ, call_data, lang):
        if self.get_field_value("transform"):
            self.update_attribs({"transform":self.get_field_value("transform")})
        stroke_width = self.get_field_value("stroke_width")
        if stroke_width:
            self[0].update_attribs({"stroke-width":str(stroke_width)})
        # stroke will be the star colour
        stroke = self.get_field_value("stroke")
        if stroke:
            self[0].update_attribs({"stroke":stroke})
        fill = self.get_field_value("fill")
        if fill:
            self[0].update_attribs({"fill":fill})
        if not self.get_field_value("stars"):
            return

        for star in self.get_field_value("stars"):

            # get the radius of a star circle to plot
            if star[0]:
                radius = float(star[0])/2.0
            else:
                radius = 0.5
            if radius < 0.1:
                radius = 0.1

            # get the position x, y with origin (0,0) in the centre of the chart

            x = float(star[1])
            y = float(star[2])

            # move origin to circle centre (250,250)
            cx = 250 - x
            cy = 250 - y
            self.append(tag.ClosedPart(tag_name='circle', attribs={"cx":str(cx),
                                                                   "cy":str(cy),
                                                                   "r":str(radius),
                                                                   "fill":stroke,
                                                                   "stroke":stroke}))


        if self.get_field_value("square"):
            # plot a square on the chart centre
            self.append(tag.ClosedPart(tag_name='rect', attribs={"x":"240",
                                                                 "y":"240",
                                                                 "width":"20",
                                                                 "height":"20",
                                                                 "style":"stroke:%s;stroke-width:1;fill-opacity:0;" % (stroke,)}))

        if self.get_field_value("cross"):
            # plot a + on the chart centre
            self.append(tag.ClosedPart(tag_name='line', attribs={"x1":"240",
                                                                 "y1":"250",
                                                                 "x2":"260",
                                                                 "y2":"250",
                                                                 "stroke":stroke,
                                                                 "stroke-width":"1"}))
            self.append(tag.ClosedPart(tag_name='line', attribs={"x1":"250",
                                                                 "y1":"240",
                                                                 "x2":"250",
                                                                 "y2":"260",
                                                                 "stroke":stroke,
                                                                 "stroke-width":"1"}))

        for line in self.get_field_value("lines"):

            # move origin to circle centre (250,250)
            startx = 250 - float(line[0])
            starty = 250 - float(line[1])

            endx = 250 - float(line[2])
            endy = 250 - float(line[3])

            self.append(tag.ClosedPart(tag_name='line', attribs={"x1":str(startx),
                                                                 "y1":str(starty),
                                                                 "x2":str(endx),
                                                                 "y2":str(endy),
                                                                 "stroke":stroke,
                                                                 "stroke-width":"1"}))


    def _build_js(self, page, ident_list, environ, call_data, lang):
        """Sets scale values"""
        return self._make_fieldvalues('stroke', 'stroke_width', 'fill', 'cross', 'square')
 
    @classmethod
    def description(cls):
        """Returns a text string to illustrate the widget"""
        return """
<g>  <!-- with widget id and class widget_class, and transform attribute if given -->
  <circle /> <!-- A circle with fill, stroke and stroke width, and diameter 500 -->
  <!-- with multiple 'star' spots, positioned according to the given x,y values -->
  <!-- as pixel distances with x,y origin on the chart centre --> 
  <!-- and each with a drawn diameter given per star -->
  <!-- centre cross drawn if cross is True -->
</g>"""



class Axis1(Widget):

    # This class does not display any error messages
    display_errors = False

    _container = ((1,),)


    arg_descriptions = {
                        'transform':FieldArg("text", "", jsonset=True),
                        'fill':FieldArg("text", "white"),
                        'fill_opacity':FieldArg("text", "1"),
                        'font_family':FieldArg("text", "arial"),
                        'axiscol':FieldArg("text", "green"),
                        'minxvalue':FieldArg("text", "0"),
                        'maxxvalue':FieldArg("text", "100"),
                        'minyvalue':FieldArg("text", "0"),
                        'maxyvalue':FieldArg("text", "100")
                       }


    def __init__(self, name=None, brief='', **field_args):
        """A g element which holds a graph axis, held in a 1200 high x 1200 wide space
        """
        Widget.__init__(self, name=name, tag_name="g", brief=brief, **field_args)
        self._axiscol = "green"
        self._font_family = "arial"
        self[0] = tag.Part(tag_name="g")
        # The location 1 is available as a container
        self[1] = tag.Part(tag_name='g')
        self[1][0] = ''
        self._leftspace = 240
        self._topspace = 20



    def _build(self, page, ident_list, environ, call_data, lang):
        if self.get_field_value("transform"):
            self.update_attribs({"transform":self.get_field_value("transform")})

        fill = self.get_field_value("fill")
        if not fill:
            fill = "white"

        fill_opacity = self.get_field_value("fill_opacity")
        if not fill_opacity:
            fill_opacity = "1"

        self._font_family = self.get_field_value("font_family")
        if not self._font_family:
            self._font_family = "arial"

        self._axiscol = self.get_field_value("axiscol")
        if not self._axiscol:
            self._axiscol = "green"

        self[0][0] = tag.ClosedPart(tag_name='rect', attribs={"x":str(self._leftspace),
                                                           "y":str(self._topspace),
                                                           "width":"960",
                                                           "height":"720",
                                                           "fill":fill,
                                                           "fill-opacity":fill_opacity,
                                                           "stroke":self._axiscol,
                                                           "stroke-width":"1"})

        # create Y axis
        minv = self.get_field_value("minyvalue")
        maxv = self.get_field_value("maxyvalue")

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
           miny,maxy = self._integer_axis(int_maxv, int_minv)
        else:
           miny,maxy = self._float_axis(float(maxv), float(minv))


        # create X axis
        minv = self.get_field_value("minxvalue")
        maxv = self.get_field_value("maxxvalue")

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
            # create a X axis of integer values
            minx,maxx = self._integer_axis(int_maxv, int_minv, 0, True)
        else:
            minx,maxx = self._float_axis(float(maxv), float(minv), True)

        # get line gradients and constants, note y starts from top and goes down the page
        # x = m*val + c
        # m = 960 / (xmax-xmin)
        # c = leftspace - m*xmin

        # y = m*val + c
        # m = 960 / (ymin - ymax)   - note min-max to give negative gradient
        # c = topspace - m*ymax

        my = Decimal("720") / (miny-maxy)
        cy = self._topspace - maxy*my

        mx = Decimal("960") / (maxx-minx)
        cx = self._leftspace - minx*mx 

        # ensure all contained parts have these values
        AxisLimits = namedtuple('AxisLimits', ['miny','maxy','minx','maxx', 'my', 'cy', 'mx', 'cx'])

        self.set_contained_values(AxisLimits(miny,maxy,minx,maxx,my,cy,mx,cx))



    def _float_axis(self, maxv, minv, x=False):
        "create an axis of float values"
        if minv == 0.0:
            # convert 0.0045 to 45
            # convert 4500.0 to 45
            tens = math.floor(math.log10(abs(maxv)))-1
            int_maxv = math.ceil(maxv/10**tens)
            return self._integer_axis(int_maxv, 0, tens, x)
        else:
            diff = maxv - minv
            tens = math.floor(math.log10(abs(diff)))-1
            int_maxv = math.ceil(maxv/10**tens)
            int_minv = math.floor(minv/10**tens)
            return self._integer_axis(int_maxv, int_minv, tens, x)



    def _integer_axis(self, int_maxv, int_minv, tens=0, x=False):
        "create an axis of integer values"
        # diff is the difference between minimum and maximum, divide it into intervals
        # the number of intervals should also divide 720 pixels nicely, i.e. 16, 15, 12, 10, 9, 8, 6, 5
        # or into 960 pixels, 20, 16, 15, 12, 10, 8, 6, 5
        if x:
            divlist = (20, 16, 15, 12, 10, 8, 6, 5)
        else:
            divlist = (16, 15, 12, 10, 9, 8, 6, 5)

        diff = int_maxv - int_minv

        # order of prefferred interval spacing
        prefferred = (5, 10, 2, 15, 4, 25, 20)

        difftens = math.floor(math.log10(diff))

        if difftens>2:
            prefferred = ( item * 10**(difftens-1) for item in prefferred)

        number_of_intervals = 0
        for i in prefferred:
            if (diff % i == 0) and (diff//i in divlist):
                # intervals with spacing of i is given priority
                number_of_intervals = diff//i
                break

        if not number_of_intervals:
            for divd in divlist:
                if diff % divd == 0:
                    number_of_intervals = divd
                    break
            else:
                # None of the items in divlist go nicely into diff, so add 1 to int_maxv and try again
                return self._integer_axis(int_maxv+1, int_minv, tens, x)

        if x:
            return self._x_axis(int_maxv, int_minv, tens, number_of_intervals)
        else:
            return self._y_axis(int_maxv, int_minv, tens, number_of_intervals)



    def _y_axis(self, int_maxv, int_minv, tens, number_of_intervals):
        "Draw a y axis, return decimal values of ymin,ymax"

        diff = int_maxv - int_minv

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
        self[0].append(tag.Part(tag_name='text', text=str_maxv, attribs={
                                                                    'x':str(self._leftspace-20),
                                                                    'y': str(self._topspace+5),
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
        self[0].append(tag.Part(tag_name='text', text=str_minv, attribs={
                                                                'x':str(self._leftspace-20),
                                                                'y': str(720+self._topspace+5),
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
        y = self._topspace
        for n in range(int(number_of_intervals)-1):
            y += pixel_interval
            yval -= y_interval
            self[0].append(tag.ClosedPart(tag_name='line', attribs={"x1":str(self._leftspace-5),
                                                                 "y1":str(y),
                                                                 "x2":str(self._leftspace+20),
                                                                 "y2":str(y),
                                                                 "stroke":self._axiscol,
                                                                 "stroke-width":"1"}))
            self[0].append(tag.Part(tag_name='text', text=format(yval*mult, fstring), attribs={
                                                                        'x':str(self._leftspace-20),
                                                                        'y': str(y+5),
                                                                        'text-anchor':'end',
                                                                        'font-size': '20',
                                                                        'font-family': self._font_family,
                                                                        'fill':self._axiscol,
                                                                        'stroke-width':"0"  }))
        return Decimal(str_minv), Decimal(str_maxv)



    def _x_axis(self, int_maxv, int_minv, tens, number_of_intervals):
        "Draw a x axis, return decimal values of xmin,xmax"

        diff = int_maxv - int_minv

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

        # put the maximum value at the right of the axis
        str_maxv = format(int_maxv*mult, fstring)
        self[0].append(tag.Part(tag_name='text', text=str_maxv, attribs={
                                                                    'x':str(self._leftspace+960+5),
                                                                    'y': str(720+self._topspace+40),
                                                                    'text-anchor':'end',
                                                                    'font-size': '20',
                                                                    'font-family': self._font_family,
                                                                    'fill':self._axiscol,
                                                                    'stroke-width':"0"  }))

        # put the minimum value at the left of the axis
        if int_minv:
            str_minv = format(int_minv*mult, fstring)
        else:
            str_minv = "0"
        self[0].append(tag.Part(tag_name='text', text=str_minv, attribs={
                                                                'x':str(self._leftspace+5),
                                                                'y': str(720+self._topspace+40),
                                                                'text-anchor':'end',
                                                                'font-size': '20',
                                                                'font-family': self._font_family,
                                                                'fill':self._axiscol,
                                                                'stroke-width':"0"  }))


        # xval is the axis value at the intervals, so starting from the left
        xval = int_minv
        x_interval = diff//number_of_intervals
        # pixel_interval is the number of pixels in the interval
        pixel_interval = 960//number_of_intervals
        # with range limits so no line at right and left - so rectangle not overdrawn
        x = self._leftspace
        for n in range(int(number_of_intervals)-1):
            x += pixel_interval
            xval += x_interval
            self[0].append(tag.ClosedPart(tag_name='line', attribs={"x1":str(x),
                                                                 "y1":str(720+self._topspace+5),
                                                                 "x2":str(x),
                                                                 "y2":str(720+self._topspace-20),
                                                                 "stroke":self._axiscol,
                                                                 "stroke-width":"1"}))
            self[0].append(tag.Part(tag_name='text', text=format(xval*mult, fstring), attribs={
                                                                        'x':str(x+5),
                                                                        'y': str(720+self._topspace+40),
                                                                        'text-anchor':'end',
                                                                        'font-size': '20',
                                                                        'font-family': self._font_family,
                                                                        'fill':self._axiscol,
                                                                        'stroke-width':"0"  }))
        return Decimal(str_minv), Decimal(str_maxv)


    @classmethod
    def description(cls):
        """Returns a text string to illustrate the widget"""
        return """
<g>  <!-- with widget id and class widget_class, and transform attribute if given -->
  <g>
    <rect x="240" y="20" height="720" width="960" /> <!-- the axis rectangle -->
    <!-- lines and text which draw the axis -->
  </g>
  <g>
    <!-- Container 0 with further items, typically a widget displaying values -->
  </g>
</g>"""


class Points(Widget):

    # This class does not display any error messages
    display_errors = False


    arg_descriptions = {
                        'transform':FieldArg("text", "", jsonset=True),
                        'values':FieldArgTable(('text', 'text'), jsonset=True),
                        'pointcol':FieldArg("text", "black")
                       }


    def __init__(self, name=None, brief='', **field_args):
        """A g element which holds a table of points, intended to be included in the container 0
           of an Axis widget. 
        """
        Widget.__init__(self, name=name, tag_name="g", brief=brief, **field_args)
        self._minx = 0
        self._maxx = 960
        self._miny = 0
        self._maxy = 720

        self._my = -1
        self._cy = 720
        self._mx = 1
        self._cx = 0


    def set_contained_values(self, values):
        "These values set by the containing widget"
        if values.__class__.__name__ != "AxisLimits":
            return
        self._minx = values.minx
        self._maxx = values.maxx
        self._miny = values.miny
        self._maxy = values.maxy
        self._my = values.my
        self._cy = values.cy
        self._mx = values.mx
        self._cx = values.cx



    def _build(self, page, ident_list, environ, call_data, lang):
        if self.get_field_value("transform"):
            self.update_attribs({"transform":self.get_field_value("transform")})

        values = self.get_field_value("values")
        if not values:
            return

        self._pointcol = self.get_field_value("pointcol")
        if not self._pointcol:
            self._pointcol = "black"


        # for each point, plot a + on the graph
        for valpair in values:
            valx, valy = valpair
            valx = Decimal(valx)
            valy = Decimal(valy)
            if valy < self._miny:
                # low point outside plottable range
                continue
            if valy > self._maxy:
                # high point outside plottable range
                continue
            if valx < self._minx:
                # low point outside plottable range
                continue
            if valx > self._maxx:
                # high point outside plottable range
                continue
            x = int(self._mx*valx + self._cx)
            y = int(self._my*valy + self._cy)
            self._plot_cross(x, y)


    def _plot_cross(self, x, y):
        "plot a + on the graph at x, y"
        # Vertical line
        self.append(tag.ClosedPart(tag_name='line', attribs={"x1":str(x),
                                                             "y1":str(y-5),
                                                             "x2":str(x),
                                                             "y2":str(y+5),
                                                             "stroke":self._pointcol,
                                                             "stroke-width":"1"}))
        # Horizontal line
        self.append(tag.ClosedPart(tag_name='line', attribs={"x1":str(x-5),
                                                             "y1":str(y),
                                                             "x2":str(x+5),
                                                             "y2":str(y),
                                                             "stroke":self._pointcol,
                                                             "stroke-width":"1"}))


    def _build_js(self, page, ident_list, environ, call_data, lang):
        """Sets scale values"""
        return self._make_fieldvalues('pointcol',
                                      minx = float(self._minx),
                                      maxx = float(self._maxx),
                                      miny = float(self._miny),
                                      maxy = float(self._maxy),
                                      my = float(self._my),
                                      cy = float(self._cy),
                                      mx = float(self._mx),
                                      cx = float(self._cx))


    @classmethod
    def description(cls):
        """Returns a text string to illustrate the widget"""
        return """
<g>  <!-- with widget id and class widget_class, and transform attribute if given -->
    <!-- lines forming a cross at each point, positioned on the axis of the containing Axis widget -->
</g>"""



class Axis2(Widget):

    # This class does not display any error messages
    display_errors = False

    _container = ((1,),)


    arg_descriptions = {
                        'transform':FieldArg("text", "", jsonset=True),
                        'fill':FieldArg("text", "white"),
                        'fill_opacity':FieldArg("text", "1"),
                        'font_family':FieldArg("text", "arial"),
                        'axiscol':FieldArg("text", "green"),
                        'minxvalue':FieldArg("text", "0"),
                        'maxxvalue':FieldArg("text", "100"),
                        'xinterval':FieldArg("text", "20"),
                        'minyvalue':FieldArg("text", "0"),
                        'maxyvalue':FieldArg("text", "100"),
                        'yinterval':FieldArg("text", "20"),
                        'leftspace':FieldArg("text", "240"),
                        'topspace':FieldArg("text", "20"),
                        'axiswidth':FieldArg("text", "960"),
                        'axisheight':FieldArg("text", "720"),
                        'xoffset':FieldArg("boolean", False),
                        'yoffset':FieldArg("boolean", False)
                       }


    def __init__(self, name=None, brief='', **field_args):
        """A g element which holds a graph axis
        """
        Widget.__init__(self, name=name, tag_name="g", brief=brief, **field_args)
        self._axiscol = "green"
        self._font_family = "arial"
        self[0] = tag.Part(tag_name="g")
        # The location 1 is available as a container
        self[1] = tag.Part(tag_name='g')
        self[1][0] = ''
        self._leftspace = 240
        self._topspace = 20
        self._axiswidth = 960
        self._axisheight = 720


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

        self._leftspace = int(self.get_field_value("leftspace"))
        self._topspace = int(self.get_field_value("topspace"))
        self._axiswidth = int(self.get_field_value("axiswidth"))
        self._axisheight = int(self.get_field_value("axisheight"))


        self[0][0] = tag.ClosedPart(tag_name='rect', attribs={"x":str(self._leftspace),
                                                           "y":str(self._topspace),
                                                           "width":str(self._axiswidth),
                                                           "height":str(self._axisheight),
                                                           "fill":fill,
                                                           "fill-opacity":fill_opacity,
                                                           "stroke":self._axiscol,
                                                           "stroke-width":"1"})

        # create Y axis
        minv = Decimal(self.get_field_value("minyvalue"))
        maxv = Decimal(self.get_field_value("maxyvalue"))
        interval = Decimal(self.get_field_value("yinterval"))
        if (maxv <= minv):
            return
        if (maxv-minv)<interval:
            return
 
        miny,maxy = self._y_axis(maxv, minv, interval)


        # create X axis
        minv = Decimal(self.get_field_value("minxvalue"))
        maxv = Decimal(self.get_field_value("maxxvalue"))
        interval = Decimal(self.get_field_value("xinterval"))
        if (maxv <= minv):
            return
        if (maxv-minv)<interval:
            return

        minx,maxx = self._x_axis(maxv, minv, interval)

        # get line gradients and constants, note y starts from top and goes down the page
        # x = m*val + c
        # m = 960 / (xmax-xmin)
        # c = leftspace - m*xmin

        # y = m*val + c
        # m = 960 / (ymin - ymax)   - note min-max to give negative gradient
        # c = topspace - m*ymax

        my = Decimal(str(self._axisheight)) / (miny-maxy)
        cy = self._topspace - maxy*my

        mx = Decimal(str(self._axiswidth)) / (maxx-minx)
        cx = self._leftspace - minx*mx

        # ensure all contained parts have these values
        AxisLimits = namedtuple('AxisLimits', ['miny','maxy','minx','maxx', 'my', 'cy', 'mx', 'cx'])

        self.set_contained_values(AxisLimits(miny,maxy,minx,maxx,my,cy,mx,cx))




    def _y_axis(self, maxv, minv, interval):
        "Draw a y axis, return decimal values of ymin,ymax"

        fraction_number_of_intervals = (maxv-minv)/interval
        number_of_intervals = fraction_number_of_intervals.to_integral_value(rounding=ROUND_UP)
        maxv = minv + number_of_intervals*interval


        yoffset = self.get_field_value("yoffset")
        if yoffset:
            maxv += interval/Decimal("2.0")
            minv -= interval/Decimal("2.0")
            # pixel_interval is the number of pixels in the interval - but in this case there is an extra interval
            pixel_interval = int(self._axisheight//(number_of_intervals+1))
        else:
            # pixel_interval is the number of pixels in the interval
            pixel_interval = int(self._axisheight//number_of_intervals)


        # yval is the axis value at the intervals, so starting from the top
        # y is the pixel value to be plotted
        if yoffset:
            y = self._topspace - pixel_interval//2
            yval = maxv + interval/Decimal("2.0")
            for n in range(int(number_of_intervals)+1):
                y += pixel_interval
                yval -= interval
                self[0].append(tag.ClosedPart(tag_name='line', attribs={"x1":str(self._leftspace-5),
                                                                     "y1":str(y),
                                                                     "x2":str(self._leftspace+20),
                                                                     "y2":str(y),
                                                                     "stroke":self._axiscol,
                                                                     "stroke-width":"1"}))
                self[0].append(tag.Part(tag_name='text', text=str(yval), attribs={
                                                                            'x':str(self._leftspace-20),
                                                                            'y': str(y+5),
                                                                            'text-anchor':'end',
                                                                            'font-size': '20',
                                                                            'font-family': self._font_family,
                                                                            'fill':self._axiscol,
                                                                            'stroke-width':"0"  }))
        else:
            y = self._topspace
            yval = maxv
            for n in range(int(number_of_intervals)-1):
                y += pixel_interval
                yval -= interval
                self[0].append(tag.ClosedPart(tag_name='line', attribs={"x1":str(self._leftspace-5),
                                                                     "y1":str(y),
                                                                     "x2":str(self._leftspace+20),
                                                                     "y2":str(y),
                                                                     "stroke":self._axiscol,
                                                                     "stroke-width":"1"}))
                self[0].append(tag.Part(tag_name='text', text=str(yval), attribs={
                                                                            'x':str(self._leftspace-20),
                                                                            'y': str(y+5),
                                                                            'text-anchor':'end',
                                                                            'font-size': '20',
                                                                            'font-family': self._font_family,
                                                                            'fill':self._axiscol,
                                                                            'stroke-width':"0"  }))

            # put the maximum value at the top of the axis
            self[0].append(tag.Part(tag_name='text', text=str(maxv), attribs={
                                                                        'x':str(self._leftspace-20),
                                                                        'y': str(self._topspace+5),
                                                                        'text-anchor':'end',
                                                                        'font-size': '20',
                                                                        'font-family': self._font_family,
                                                                        'fill':self._axiscol,
                                                                        'stroke-width':"0"  }))

            # put the minimum value at the bottom of the axis
            self[0].append(tag.Part(tag_name='text', text=str(minv), attribs={
                                                                    'x':str(self._leftspace-20),
                                                                    'y': str(self._axisheight+self._topspace+5),
                                                                    'text-anchor':'end',
                                                                    'font-size': '20',
                                                                    'font-family': self._font_family,
                                                                    'fill':self._axiscol,
                                                                    'stroke-width':"0"  }))

        return minv,maxv



    def _x_axis(self, maxv, minv, interval):
        "Draw a x axis, return decimal values of xmin,xmax"

        fraction_number_of_intervals = (maxv-minv)/interval
        number_of_intervals = fraction_number_of_intervals.to_integral_value(rounding=ROUND_UP)
        maxv = minv + number_of_intervals*interval


        xoffset = self.get_field_value("xoffset")
        if xoffset:
            maxv += interval/Decimal("2.0")
            minv -= interval/Decimal("2.0")
            # pixel_interval is the number of pixels in the interval - but in this case there is an extra interval
            pixel_interval = int(self._axiswidth//(number_of_intervals+1))
        else:
            # pixel_interval is the number of pixels in the interval
            pixel_interval = int(self._axiswidth//number_of_intervals)

        # xval is the axis value at the intervals, so starting from the left
        # x is the pixel value to be plotted
        if xoffset:
            x = self._leftspace - pixel_interval//2
            xval = minv - interval/Decimal("2.0")
            for n in range(int(number_of_intervals)+1):
                x += pixel_interval
                xval += interval
                self[0].append(tag.ClosedPart(tag_name='line', attribs={"x1":str(x),
                                                                     "y1":str(self._axisheight+self._topspace+5),
                                                                     "x2":str(x),
                                                                     "y2":str(self._axisheight+self._topspace-20),
                                                                     "stroke":self._axiscol,
                                                                     "stroke-width":"1"}))
                self[0].append(tag.Part(tag_name='text', text=str(xval), attribs={
                                                                            'x':str(x+5),
                                                                            'y': str(self._axisheight+self._topspace+40),
                                                                            'text-anchor':'end',
                                                                            'font-size': '20',
                                                                            'font-family': self._font_family,
                                                                            'fill':self._axiscol,
                                                                            'stroke-width':"0"  }))
        else:
            x = self._leftspace
            xval = minv
            for n in range(int(number_of_intervals)-1):
                x += pixel_interval
                xval += interval
                self[0].append(tag.ClosedPart(tag_name='line', attribs={"x1":str(x),
                                                                     "y1":str(self._axisheight+self._topspace+5),
                                                                     "x2":str(x),
                                                                     "y2":str(self._axisheight+self._topspace-20),
                                                                     "stroke":self._axiscol,
                                                                     "stroke-width":"1"}))
                self[0].append(tag.Part(tag_name='text', text=str(xval), attribs={
                                                                            'x':str(x+5),
                                                                            'y': str(self._axisheight+self._topspace+40),
                                                                            'text-anchor':'end',
                                                                            'font-size': '20',
                                                                            'font-family': self._font_family,
                                                                            'fill':self._axiscol,
                                                                            'stroke-width':"0"  }))
      
            # put the maximum value at the right of the axis
            self[0].append(tag.Part(tag_name='text', text=str(maxv), attribs={
                                                                        'x':str(self._leftspace+self._axiswidth+5),
                                                                        'y': str(self._axisheight+self._topspace+40),
                                                                        'text-anchor':'end',
                                                                        'font-size': '20',
                                                                        'font-family': self._font_family,
                                                                        'fill':self._axiscol,
                                                                        'stroke-width':"0"  }))

            # put the minimum value at the left of the axis
            self[0].append(tag.Part(tag_name='text', text=str(minv), attribs={
                                                                    'x':str(self._leftspace+5),
                                                                    'y': str(self._axisheight+self._topspace+40),
                                                                    'text-anchor':'end',
                                                                    'font-size': '20',
                                                                    'font-family': self._font_family,
                                                                    'fill':self._axiscol,
                                                                    'stroke-width':"0"  }))

        return minv, maxv


    @classmethod
    def description(cls):
        """Returns a text string to illustrate the widget"""
        return """
<g>  <!-- with widget id and class widget_class, and transform attribute if given -->
  <g>
    <!-- rectangle with given position, height and width -->
    <!-- lines and text which draw the axis -->
  </g>
  <g>
    <!-- Container 0 with further items, typically a widget displaying values -->
  </g>
</g>"""



class Lines(Widget):

    # This class does not display any error messages
    display_errors = False


    arg_descriptions = {
                        'transform':FieldArg("text", "", jsonset=True),
                        'values':FieldArgTable(('text', 'text'), jsonset=True),
                        'linecol':FieldArg("text", "black"),
                        'linewidth':FieldArg("text", "2"),
                        'pointradius':FieldArg("text", "1")
                       }


    def __init__(self, name=None, brief='', **field_args):
        """A g element which holds a table of points joined by lines, intended to be included in the container 0
           of an Axis widget. 
        """
        Widget.__init__(self, name=name, tag_name="g", brief=brief, **field_args)
        self._minx = 0
        self._maxx = 960
        self._miny = 0
        self._maxy = 720

        self._my = -1
        self._cy = 720
        self._mx = 1
        self._cx = 0


    def set_contained_values(self, values):
        "These values set by the containing widget"
        if values.__class__.__name__ != "AxisLimits":
            return
        self._minx = values.minx
        self._maxx = values.maxx
        self._miny = values.miny
        self._maxy = values.maxy
        self._my = values.my
        self._cy = values.cy
        self._mx = values.mx
        self._cx = values.cx


    def _build(self, page, ident_list, environ, call_data, lang):
        if self.get_field_value("transform"):
            self.update_attribs({"transform":self.get_field_value("transform")})

        values = self.get_field_value("values")
        if not values:
            return

        self._linecol = self.get_field_value("linecol")
        if not self._linecol:
            self._linecol = "black"

        self._linewidth = self.get_field_value("linewidth")

        self._pointradius = self.get_field_value("pointradius")
        if not self._pointradius:
            self._pointradius = "2"

        old_x = ''
        old_y = ''
        # for each point, plot a circle on the graph
        for valpair in values:
            valx, valy = valpair
            valx = Decimal(valx)
            valy = Decimal(valy)
            if valy < self._miny:
                # low point outside plottable range
                continue
            if valy > self._maxy:
                # high point outside plottable range
                continue
            if valx < self._minx:
                # low point outside plottable range
                continue
            if valx > self._maxx:
                # high point outside plottable range
                continue
            x = int(self._mx*valx + self._cx)
            y = int(self._my*valy + self._cy)
            # plot a circle at point
            self.append(tag.ClosedPart(tag_name='circle', attribs={"cx":str(x),
                                                                   "cy":str(y),
                                                                   "r":str(self._pointradius),
                                                                   "fill":self._linecol,
                                                                   "stroke":self._linecol}))
            # plot a line from previous point
            if old_x and self._linewidth:
                self.append(tag.ClosedPart(tag_name='line', attribs={"x1":old_x,
                                                                     "y1":old_y,
                                                                     "x2":str(x),
                                                                     "y2":str(y),
                                                                     "stroke":self._linecol,
                                                                     "stroke-width":self._linewidth}))
            old_x = str(x)
            old_y = str(y)


    def _build_js(self, page, ident_list, environ, call_data, lang):
        """Sets scale values"""
        return self._make_fieldvalues('linecol',
                                      'linewidth',
                                      'pointradius',
                                      minx = float(self._minx),
                                      maxx = float(self._maxx),
                                      miny = float(self._miny),
                                      maxy = float(self._maxy),
                                      my = float(self._my),
                                      cy = float(self._cy),
                                      mx = float(self._mx),
                                      cx = float(self._cx))


    @classmethod
    def description(cls):
        """Returns a text string to illustrate the widget"""
        return """
<g>  <!-- with widget id and class widget_class, and transform attribute if given -->
    <!-- lines linking value points, positioned on the axis of the containing Axis widget -->
</g>"""



class XBars(Widget):

    # This class does not display any error messages
    display_errors = False


    arg_descriptions = {
                        'transform':FieldArg("text", "", jsonset=True),
                        'values':FieldArgTable(('text', 'text'), jsonset=True),
                        'bar_width':FieldArg("text", "10"),
                        'fill':FieldArg("text", "green"),
                        'fill_opacity':FieldArg("text", "1"),
                        'stroke':FieldArg("text", "black"),
                        'stroke_width':FieldArg("text", "1")
                       }


    def __init__(self, name=None, brief='', **field_args):
        """A g element which holds a series of vertical bars, intended to be included in the container 0
           of an Axis widget. 
        """
        Widget.__init__(self, name=name, tag_name="g", brief=brief, **field_args)
        self._minx = 0
        self._maxx = 960
        self._miny = 0
        self._maxy = 720
        self._my = -1
        self._cy = 720
        self._mx = 1
        self._cx = 0
        self._barwidth = 10
        self._yaxis = 720


    def set_contained_values(self, values):
        "These values set by the containing widget"
        if values.__class__.__name__ != "AxisLimits":
            return
        self._minx = values.minx
        self._maxx = values.maxx
        self._miny = values.miny
        self._maxy = values.maxy
        self._my = values.my
        self._cy = values.cy
        self._mx = values.mx
        self._cx = values.cx



    def _build(self, page, ident_list, environ, call_data, lang):
        if self.get_field_value("transform"):
            self.update_attribs({"transform":self.get_field_value("transform")})

        values = self.get_field_value("values")
        if not values:
            return

        bar_width = self.get_field_value("bar_width")
        if not bar_width:
            return

        # get bar in pixels
        self._barwidth = int(self._mx*Decimal(bar_width))
        if not self._barwidth:
            return

        self._halfbar = self._barwidth//2
        self._yaxis = int(self._my*self._miny + self._cy)

        self._fill = self.get_field_value("fill")
        self._fill_opacity = self.get_field_value("fill_opacity")
        self._stroke = self.get_field_value("stroke")
        self._stroke_width = self.get_field_value("stroke_width")

        # for each point, plot a bar on the graph
        for valpair in values:
            valx, valy = valpair
            valx = Decimal(valx)
            valy = Decimal(valy)
            if valy < self._miny:
                # low point outside plottable range
                continue
            if valy > self._maxy:
                # high point outside plottable range
                continue
            if valx < self._minx:
                # low point outside plottable range
                continue
            if valx > self._maxx:
                # high point outside plottable range
                continue
            x = int(self._mx*valx + self._cx)
            y = int(self._my*valy + self._cy)
            self._plot_bar(x, y)


    def _plot_bar(self, x, y):
        "plot a bar on the graph at x, y"
        self.append(tag.ClosedPart(tag_name='rect', attribs={"x":str(x-self._halfbar),
                                                            "y":str(y),
                                                            "width":str(self._barwidth),
                                                            "height":str(self._yaxis-y),
                                                            "fill":self._fill,
                                                            "fill-opacity":self._fill_opacity,
                                                            "stroke":self._stroke,
                                                            "stroke-width":self._stroke_width}))



    def _build_js(self, page, ident_list, environ, call_data, lang):
        """Sets scale values"""
        return self._make_fieldvalues(
                                     'fill',
                                     'fill_opacity',
                                     'stroke',
                                     'stroke_width',
                                      barwidth = self._barwidth,
                                      yaxis = self._yaxis,
                                      minx = float(self._minx),
                                      maxx = float(self._maxx),
                                      miny = float(self._miny),
                                      maxy = float(self._maxy),
                                      my = float(self._my),
                                      cy = float(self._cy),
                                      mx = float(self._mx),
                                      cx = float(self._cx))


    @classmethod
    def description(cls):
        """Returns a text string to illustrate the widget"""
        return """
<g>  <!-- with widget id and class widget_class, and transform attribute if given -->
    <!-- vertical rectangle bars at each X point, positioned on the axis of the containing Axis widget -->
</g>"""


class YBars(Widget):

    # This class does not display any error messages
    display_errors = False


    arg_descriptions = {
                        'transform':FieldArg("text", "", jsonset=True),
                        'values':FieldArgTable(('text', 'text'), jsonset=True),
                        'bar_width':FieldArg("text", "10"),
                        'fill':FieldArg("text", "green"),
                        'fill_opacity':FieldArg("text", "1"),
                        'stroke':FieldArg("text", "black"),
                        'stroke_width':FieldArg("text", "1")
                       }


    def __init__(self, name=None, brief='', **field_args):
        """A g element which holds a series of horizontal bars, intended to be included in the container 0
           of an Axis widget. 
        """
        Widget.__init__(self, name=name, tag_name="g", brief=brief, **field_args)
        self._minx = 0
        self._maxx = 960
        self._miny = 0
        self._maxy = 720
        self._my = -1
        self._cy = 720
        self._mx = 1
        self._cx = 0
        self._barwidth = 10
        self._xaxis = 960


    def set_contained_values(self, values):
        "These values set by the containing widget"
        if values.__class__.__name__ != "AxisLimits":
            return
        self._minx = values.minx
        self._maxx = values.maxx
        self._miny = values.miny
        self._maxy = values.maxy
        self._my = values.my
        self._cy = values.cy
        self._mx = values.mx
        self._cx = values.cx



    def _build(self, page, ident_list, environ, call_data, lang):
        if self.get_field_value("transform"):
            self.update_attribs({"transform":self.get_field_value("transform")})

        values = self.get_field_value("values")
        if not values:
            return

        bar_width = self.get_field_value("bar_width")
        if not bar_width:
            return

        # get bar in pixels, -1 multiplier as my is negative
        self._barwidth = int(-1*self._my*Decimal(bar_width))
        if not self._barwidth:
            return

        self._halfbar = self._barwidth//2
        self._xaxis = int(self._mx*self._minx + self._cx)

        self._fill = self.get_field_value("fill")
        self._fill_opacity = self.get_field_value("fill_opacity")
        self._stroke = self.get_field_value("stroke")
        self._stroke_width = self.get_field_value("stroke_width")

        # for each point, plot a bar on the graph
        for valpair in values:
            valx, valy = valpair
            valx = Decimal(valx)
            valy = Decimal(valy)
            if valy < self._miny:
                # low point outside plottable range
                continue
            if valy > self._maxy:
                # high point outside plottable range
                continue
            if valx < self._minx:
                # low point outside plottable range
                continue
            if valx > self._maxx:
                # high point outside plottable range
                continue
            x = int(self._mx*valx + self._cx)
            y = int(self._my*valy + self._cy)
            self._plot_bar(x, y)


    def _plot_bar(self, x, y):
        "plot a bar on the graph at x, y"
        self.append(tag.ClosedPart(tag_name='rect', attribs={"x":str(self._xaxis),
                                                            "y":str(y-self._halfbar),
                                                            "width":str(x-self._xaxis),
                                                            "height":str(self._barwidth),
                                                            "fill":self._fill,
                                                            "fill-opacity":self._fill_opacity,
                                                            "stroke":self._stroke,
                                                            "stroke-width":self._stroke_width}))


    def _build_js(self, page, ident_list, environ, call_data, lang):
        """Sets scale values"""
        return self._make_fieldvalues(
                                     'fill',
                                     'fill_opacity',
                                     'stroke',
                                     'stroke_width',
                                      barwidth = self._barwidth,
                                      xaxis = self._xaxis,
                                      minx = float(self._minx),
                                      maxx = float(self._maxx),
                                      miny = float(self._miny),
                                      maxy = float(self._maxy),
                                      my = float(self._my),
                                      cy = float(self._cy),
                                      mx = float(self._mx),
                                      cx = float(self._cx))


    @classmethod
    def description(cls):
        """Returns a text string to illustrate the widget"""
        return """
<g>  <!-- with widget id and class widget_class, and transform attribute if given -->
    <!-- horizontal rectangle bars at each Y point, positioned on the axis of the containing Axis widget -->
</g>"""


class Axis3(Widget):

    # This class does not display any error messages
    display_errors = False

    _container = ((1,),)


    arg_descriptions = {
                        'transform':FieldArg("text", "", jsonset=True),
                        'fill':FieldArg("text", "white"),
                        'fill_opacity':FieldArg("text", "1"),
                        'font_family':FieldArg("text", "arial"),
                        'axiscol':FieldArg("text", "green"),
                        'minxvalue':FieldArg("text", "0"),
                        'maxxvalue':FieldArg("text", "100"),
                        'xlabels':FieldArgList('text'),
                        'ylabels':FieldArgList('text'),
                        'minyvalue':FieldArg("text", "0"),
                        'maxyvalue':FieldArg("text", "100"),
                        'leftspace':FieldArg("text", "240"),
                        'topspace':FieldArg("text", "20"),
                        'axiswidth':FieldArg("text", "960"),
                        'axisheight':FieldArg("text", "720"),
                        'xoffset':FieldArg("boolean", False),
                        'yoffset':FieldArg("boolean", False)
                       }


    def __init__(self, name=None, brief='', **field_args):
        """A g element which holds a graph axis
        """
        Widget.__init__(self, name=name, tag_name="g", brief=brief, **field_args)
        self._axiscol = "green"
        self._font_family = "arial"
        self[0] = tag.Part(tag_name="g")
        # The location 1 is available as a container
        self[1] = tag.Part(tag_name='g')
        self[1][0] = ''
        self._leftspace = 240
        self._topspace = 20
        self._axiswidth = 960
        self._axisheight = 720


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

        self._leftspace = int(self.get_field_value("leftspace"))
        self._topspace = int(self.get_field_value("topspace"))
        self._axiswidth = int(self.get_field_value("axiswidth"))
        self._axisheight = int(self.get_field_value("axisheight"))


        self[0][0] = tag.ClosedPart(tag_name='rect', attribs={"x":str(self._leftspace),
                                                           "y":str(self._topspace),
                                                           "width":str(self._axiswidth),
                                                           "height":str(self._axisheight),
                                                           "fill":fill,
                                                           "fill-opacity":fill_opacity,
                                                           "stroke":self._axiscol,
                                                           "stroke-width":"1"})

        xlabels = self.get_field_value('xlabels')
        ylabels = self.get_field_value('ylabels')


        # create Y axis
        minv = Decimal(self.get_field_value("minyvalue"))
        maxv = Decimal(self.get_field_value("maxyvalue"))
        if (maxv <= minv):
            return
        if ylabels and (len(ylabels) > 1): 
            interval = (maxv-minv)/(len(ylabels)-1)
        else:
            interval = (maxv-minv)/10
 
        miny,maxy = self._y_axis(maxv, minv, interval, ylabels)


        # create X axis
        minv = Decimal(self.get_field_value("minxvalue"))
        maxv = Decimal(self.get_field_value("maxxvalue"))
        if (maxv <= minv):
            return
        if xlabels and (len(xlabels) > 1): 
            interval = (maxv-minv)/(len(xlabels)-1)
        else:
            interval = (maxv-minv)/10

        minx,maxx = self._x_axis(maxv, minv, interval, xlabels)

        # get line gradients and constants, note y starts from top and goes down the page
        # x = m*val + c
        # m = 960 / (xmax-xmin)
        # c = leftspace - m*xmin

        # y = m*val + c
        # m = 960 / (ymin - ymax)   - note min-max to give negative gradient
        # c = topspace - m*ymax

        my = Decimal(str(self._axisheight)) / (miny-maxy)
        cy = self._topspace - maxy*my

        mx = Decimal(str(self._axiswidth)) / (maxx-minx)
        cx = self._leftspace - minx*mx

        # ensure all contained parts have these values
        AxisLimits = namedtuple('AxisLimits', ['miny','maxy','minx','maxx', 'my', 'cy', 'mx', 'cx'])

        self.set_contained_values(AxisLimits(miny,maxy,minx,maxx,my,cy,mx,cx))




    def _y_axis(self, maxv, minv, interval, labels):
        "Draw a y axis, return decimal values of ymin,ymax"

        fraction_number_of_intervals = (maxv-minv)/interval
        number_of_intervals = fraction_number_of_intervals.to_integral_value(rounding=ROUND_UP)
        maxv = minv + number_of_intervals*interval


        yoffset = self.get_field_value("yoffset")
        if yoffset:
            maxv += interval/Decimal("2.0")
            minv -= interval/Decimal("2.0")
            # pixel_interval is the number of pixels in the interval - but in this case there is an extra interval
            pixel_interval = int(self._axisheight//(number_of_intervals+1))
        else:
            # pixel_interval is the number of pixels in the interval
            pixel_interval = int(self._axisheight//number_of_intervals)


        # yval is the axis value at the intervals, so starting from the top
        # y is the pixel value to be plotted
        if yoffset:
            y = self._topspace - pixel_interval//2
            yval = maxv + interval/Decimal("2.0")
            lbl = int(number_of_intervals)
            for n in range(int(number_of_intervals)+1):
                y += pixel_interval
                yval -= interval
                self[0].append(tag.ClosedPart(tag_name='line', attribs={"x1":str(self._leftspace-5),
                                                                     "y1":str(y),
                                                                     "x2":str(self._leftspace+20),
                                                                     "y2":str(y),
                                                                     "stroke":self._axiscol,
                                                                     "stroke-width":"1"}))
                if labels:
                    try:
                        ylabel = labels[lbl]
                    except IndexError as e:
                        ylabel = str(yval)
                    lbl -= 1
                else:
                    ylabel = str(yval)

                self[0].append(tag.Part(tag_name='text', text=ylabel, attribs={
                                                                            'x':str(self._leftspace-20),
                                                                            'y': str(y+5),
                                                                            'text-anchor':'end',
                                                                            'font-size': '20',
                                                                            'font-family': self._font_family,
                                                                            'fill':self._axiscol,
                                                                            'stroke-width':"0"  }))
        else:
            y = self._topspace
            yval = maxv
            lbl = int(number_of_intervals)-1
            for n in range(int(number_of_intervals)-1):
                y += pixel_interval
                yval -= interval
                self[0].append(tag.ClosedPart(tag_name='line', attribs={"x1":str(self._leftspace-5),
                                                                     "y1":str(y),
                                                                     "x2":str(self._leftspace+20),
                                                                     "y2":str(y),
                                                                     "stroke":self._axiscol,
                                                                     "stroke-width":"1"}))
                if labels:
                    try:
                        ylabel = labels[lbl]
                    except IndexError as e:
                        ylabel = str(yval)
                    lbl -= 1
                else:
                    ylabel = str(yval)
                self[0].append(tag.Part(tag_name='text', text=ylabel, attribs={
                                                                            'x':str(self._leftspace-20),
                                                                            'y': str(y+5),
                                                                            'text-anchor':'end',
                                                                            'font-size': '20',
                                                                            'font-family': self._font_family,
                                                                            'fill':self._axiscol,
                                                                            'stroke-width':"0"  }))

            # put the maximum value at the top of the axis
            if labels:
                try:
                    ylabel = labels[int(number_of_intervals)]
                except IndexError as e:
                    ylabel = str(maxv)
            else:
                ylabel = str(maxv)
            self[0].append(tag.Part(tag_name='text', text=ylabel, attribs={
                                                                        'x':str(self._leftspace-20),
                                                                        'y': str(self._topspace+5),
                                                                        'text-anchor':'end',
                                                                        'font-size': '20',
                                                                        'font-family': self._font_family,
                                                                        'fill':self._axiscol,
                                                                        'stroke-width':"0"  }))

            # put the minimum value at the bottom of the axis
            if labels:
                try:
                    ylabel = labels[0]
                except IndexError as e:
                    ylabel = str(minv)
            else:
                ylabel = str(minv)
            self[0].append(tag.Part(tag_name='text', text=ylabel, attribs={
                                                                    'x':str(self._leftspace-20),
                                                                    'y': str(self._axisheight+self._topspace+5),
                                                                    'text-anchor':'end',
                                                                    'font-size': '20',
                                                                    'font-family': self._font_family,
                                                                    'fill':self._axiscol,
                                                                    'stroke-width':"0"  }))

        return minv,maxv



    def _x_axis(self, maxv, minv, interval, labels):
        "Draw a x axis, return decimal values of xmin,xmax"

        fraction_number_of_intervals = (maxv-minv)/interval
        number_of_intervals = fraction_number_of_intervals.to_integral_value(rounding=ROUND_UP)
        maxv = minv + number_of_intervals*interval


        xoffset = self.get_field_value("xoffset")
        if xoffset:
            maxv += interval/Decimal("2.0")
            minv -= interval/Decimal("2.0")
            # pixel_interval is the number of pixels in the interval - but in this case there is an extra interval
            pixel_interval = int(self._axiswidth//(number_of_intervals+1))
        else:
            # pixel_interval is the number of pixels in the interval
            pixel_interval = int(self._axiswidth//number_of_intervals)

        # xval is the axis value at the intervals, so starting from the left
        # x is the pixel value to be plotted
        if xoffset:
            x = self._leftspace - pixel_interval//2
            xval = minv - interval/Decimal("2.0")
            lbl = 0
            for n in range(int(number_of_intervals)+1):
                x += pixel_interval
                xval += interval
                self[0].append(tag.ClosedPart(tag_name='line', attribs={"x1":str(x),
                                                                     "y1":str(self._axisheight+self._topspace+5),
                                                                     "x2":str(x),
                                                                     "y2":str(self._axisheight+self._topspace-20),
                                                                     "stroke":self._axiscol,
                                                                     "stroke-width":"1"}))
                if labels:
                    try:
                        xlabel = labels[lbl]
                    except IndexError as e:
                        xlabel = str(xval)
                    lbl += 1
                else:
                    xlabel = str(xval)

                self[0].append(tag.Part(tag_name='text', text=xlabel, attribs={
                                                                            'x':str(x+5),
                                                                            'y': str(self._axisheight+self._topspace+40),
                                                                            'text-anchor':'end',
                                                                            'font-size': '20',
                                                                            'font-family': self._font_family,
                                                                            'fill':self._axiscol,
                                                                            'stroke-width':"0"  }))
        else:
            x = self._leftspace
            xval = minv
            lbl = 1
            for n in range(int(number_of_intervals)-1):
                x += pixel_interval
                xval += interval
                self[0].append(tag.ClosedPart(tag_name='line', attribs={"x1":str(x),
                                                                     "y1":str(self._axisheight+self._topspace+5),
                                                                     "x2":str(x),
                                                                     "y2":str(self._axisheight+self._topspace-20),
                                                                     "stroke":self._axiscol,
                                                                     "stroke-width":"1"}))
                if labels:
                    try:
                        xlabel = labels[lbl]
                    except IndexError as e:
                        xlabel = str(xval)
                    lbl += 1
                else:
                    xlabel = str(xval)
                self[0].append(tag.Part(tag_name='text', text=xlabel, attribs={
                                                                            'x':str(x+5),
                                                                            'y': str(self._axisheight+self._topspace+40),
                                                                            'text-anchor':'end',
                                                                            'font-size': '20',
                                                                            'font-family': self._font_family,
                                                                            'fill':self._axiscol,
                                                                            'stroke-width':"0"  }))
      
            # put the maximum value at the right of the axis
            if labels:
                try:
                    xlabel = labels[lbl]
                except IndexError as e:
                    xlabel = str(maxv)
            else:
                xlabel = str(maxv)
            self[0].append(tag.Part(tag_name='text', text=xlabel, attribs={
                                                                        'x':str(self._leftspace+self._axiswidth+5),
                                                                        'y': str(self._axisheight+self._topspace+40),
                                                                        'text-anchor':'end',
                                                                        'font-size': '20',
                                                                        'font-family': self._font_family,
                                                                        'fill':self._axiscol,
                                                                        'stroke-width':"0"  }))

            # put the minimum value at the left of the axis
            if labels:
                try:
                    xlabel = labels[0]
                except IndexError as e:
                    xlabel = str(minv)
            else:
                xlabel = str(minv)
            self[0].append(tag.Part(tag_name='text', text=xlabel, attribs={
                                                                    'x':str(self._leftspace+5),
                                                                    'y': str(self._axisheight+self._topspace+40),
                                                                    'text-anchor':'end',
                                                                    'font-size': '20',
                                                                    'font-family': self._font_family,
                                                                    'fill':self._axiscol,
                                                                    'stroke-width':"0"  }))

        return minv, maxv


    @classmethod
    def description(cls):
        """Returns a text string to illustrate the widget"""
        return """
<g>  <!-- with widget id and class widget_class, and transform attribute if given -->
  <g>
    <!-- rectangle with given position, height and width -->
    <!-- lines and labels which draw the axis -->
  </g>
  <g>
    <!-- Container 0 with further items, typically a widget displaying values -->
  </g>
</g>"""



