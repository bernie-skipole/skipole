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

import math

from decimal import Decimal

from .. import tag

from . import Widget, ClosedWidget, FieldArg, FieldArgList, FieldArgTable, FieldArgDict


class Arrow1(ClosedWidget):
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
        ClosedWidget.__init__(self, name=name, tag_name="polygon", brief=brief, **field_args)

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
<polygon /> <!-- arrow shape with widget id, class widget_class and the given attributes -->"""



class Arrow2(ClosedWidget):
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
        ClosedWidget.__init__(self, name=name, tag_name="polygon", brief=brief, **field_args)

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
<polygon /> <!-- arrow shape with widget id, class widget_class and the given attributes -->"""


class Vertical1(Widget):

    # This class does not display any error messages
    display_errors = False

    _points = ((110,49), (110,50), (81,98), (79,98), (79,60), (13,60), (13,39), (79,39), (79,1), (81,1))

    arg_descriptions = {
                        'transform':FieldArg("text", "", jsonset=True),
                        'arrow_fill':FieldArg("text", "blue", jsonset=True),
                        'minimum':FieldArg("text", "0"),
                        'maximum':FieldArg("text", "100"),
                        'smallintervals':FieldArg("text", "10"),
                        'largeintervals':FieldArg("text", "20"),
                        'measurement':FieldArg("text", "50", jsonset=True),
                       }


    def _make_scale(self, minimum, maximum, smallintervals, largeintervals):
        "Returns two lists of Decimal values"

        minvalue = Decimal(minimum)
        maxvalue = Decimal(maximum)
        smallint = Decimal(smallintervals)
        largeint = Decimal(largeintervals)
       
        # start at the bottom of the scale with minvalue
        minscale = [minvalue]
        maxscale = [minvalue]
        mns = minvalue
        mxs = minvalue

        while mxs < maxvalue:
            mxs += largeint
            maxscale.append(mxs)

        while True:
            mns += smallint
            if mns > maxscale[-1]:
                break
            minscale.append(mns)
        return minscale, maxscale

    def __init__(self, name=None, brief='', **field_args):
        """A g element which holds a vertical scale and arrow, held in a 700 high x 250 wide space"""
        Widget.__init__(self, name=name, tag_name="g", brief=brief, **field_args)
        self[0] = tag.ClosedPart(tag_name='rect', attribs={"x":"100",
                                                           "y":"1",
                                                           "rx":"2",
                                                           "ry":"2",
                                                           "width":"149",
                                                           "height":"698",
                                                           "fill":"white",
                                                           "stroke":"black",
                                                           "stroke-width":"1"})
        arrow_points = ""
        for p in self._points:
            point = "%s, %s " % p
            arrow_points += point
        self[1] = tag.ClosedPart(tag_name='polygon', attribs={
                                                           "fill":"white",
                                                           "stroke":"black",
                                                           "stroke-width":"2",
                                                           "points":arrow_points })
        self[2] = tag.ClosedPart(tag_name='line', attribs={
                                                            'x1':'120',
                                                            'y1':'50',
                                                            'x2':'120',
                                                            'y2':'650',
                                                            'stroke':"black",
                                                            'stroke-width':"2"  })


    def _build(self, page, ident_list, environ, call_data, lang):
        if self.get_field_value("transform"):
            self.update_attribs({"transform":self.get_field_value("transform")})
        if self.get_field_value("arrow_fill"):
            self[1].update_attribs({"fill":self.get_field_value("arrow_fill")})
        # make the scale
        minscale, maxscale = self._make_scale(self.get_field_value("minimum"),
                                              self.get_field_value("maximum"),
                                              self.get_field_value("smallintervals"),
                                              self.get_field_value("largeintervals"))

        # small lines
        minitems = len(minscale)
        scalemins = Decimal('600.0') / (minitems-1)
        n = 3
        for index, item in enumerate(minscale):
            vert = Decimal(650) - index*scalemins
            self[n] = tag.ClosedPart(tag_name='line', attribs={
                                                            'x1':'120',
                                                            'y1': str(vert),
                                                            'x2':'150',
                                                            'y2':str(vert),
                                                            'stroke':"black",
                                                            'stroke-width':"1"  })
            n += 1

        # large lines
        maxitems = len(maxscale)
        scalemaxs = Decimal('600.0') / (maxitems-1)
        for index, item in enumerate(maxscale):
            vert = Decimal('650') - index*scalemaxs
            self[n] = tag.ClosedPart(tag_name='line', attribs={
                                                            'x1':'119',
                                                            'y1': str(vert),
                                                            'x2':'210',
                                                            'y2':str(vert),
                                                            'stroke':"black",
                                                            'stroke-width':"3"  })

            n += 1
            self[n] = tag.Part(tag_name='text', text=str(item), attribs={
                                                            'x':'160',
                                                            'y': str(vert-10),
                                                            'font-size': '20',
                                                            'font-family': 'arial',
                                                            'stroke':"black",
                                                            'stroke-width':"1"  })

            n += 1

        # now place arrow at the measurement point
        measurement = Decimal(self.get_field_value("measurement"))
        self._minvalue = maxscale[0]
        self._maxvalue = maxscale[-1]
        if measurement >= self._maxvalue:
            return
        if measurement <= self._minvalue:
            self[1].update_attribs({"transform" : "translate(0, 600)"})
            return
        m = Decimal('600.0') - (measurement - self._minvalue)*600/(self._maxvalue-self._minvalue)
        self[1].update_attribs({"transform" : "translate(0, %s)" % (m,)})

    def _build_js(self, page, ident_list, environ, call_data, lang):
        """Sends scaling factor for mapping measurement to scale"""
        return self._make_fieldvalues(maxvalue=str(self._maxvalue), minvalue=str(self._minvalue))


    def __str__(self):
        """Returns a text string to illustrate the widget"""
        return """
<g>  <!-- with widget id and class widget_class, and transform attribute if given -->
  <rect /> <!-- the scale rectangle -->
  <!-- lines and text dependent on the input scale values -->
  <polygon /> <!-- the arrow, with translate linked to the input value -->
</g>"""



class Traditional1(Widget):

    # This class does not display any error messages
    display_errors = False

    _points = ((24,1), (25,1), (49,50), (49,52), (30,52), (30,198), (19,198), (19,52), (1,52), (1,50))

    arg_descriptions = {
                        'transform':FieldArg("text", "translate(10,10)", jsonset=True),
                        'minimum':FieldArg("text", "0"),
                        'maximum':FieldArg("text", "100"),
                        'smallintervals':FieldArg("text", "10"),
                        'largeintervals':FieldArg("text", "20"),
                        'arrow_stroke':FieldArg("text", "red", jsonset=True),
                        'measurement':FieldArg("text", "50", jsonset=True),
                       }


    def _make_scale(self, minimum, maximum, smallintervals, largeintervals):
        "Returns two lists of Decimal values"

        minvalue = Decimal(minimum)
        maxvalue = Decimal(maximum)
        smallint = Decimal(smallintervals)
        largeint = Decimal(largeintervals)
       
        # start at the bottom of the scale with minvalue
        minscale = [minvalue]
        maxscale = [minvalue]
        mns = minvalue
        mxs = minvalue

        while mxs < maxvalue:
            mxs += largeint
            maxscale.append(mxs)

        while True:
            mns += smallint
            if mns > maxscale[-1]:
                break
            minscale.append(mns)
        return minscale, maxscale

    def __init__(self, name=None, brief='', **field_args):
        """A g element which holds the scale and arrow, held in a 400 high x 700 wide space"""
        Widget.__init__(self, name=name, tag_name="g", brief=brief, **field_args)

        # A path which holds the curved shape which will contain the meter

        # the angle of the white backing to the scale, 140 degrees
        white_angle = 140

        # the angle to the horizontal, 20 degrees, get it in radians
        white_out_angle = math.radians((180-white_angle)/2.0)

        # radius of the outside of the white backing
        outer_r = 320
        centre_x = outer_r * math.cos(white_out_angle)
        outer_x = 2 * centre_x
        outer_y = outer_r - outer_r * math.sin(white_out_angle)

        # radius of the inside of the white backing
        inner_r = 200
        inner_right_x = centre_x + inner_r * math.cos(white_out_angle)
        inner_right_y = outer_r - inner_r * math.sin(white_out_angle)
        inner_left_x = centre_x - inner_r * math.cos(white_out_angle)

        # The scale

        # the angle of the scale, 120 degrees
        scale_angle = 120

        # the angle to the horizontal, 30 degrees, get it in radians
        scale_out_angle = math.radians((180-scale_angle)/2.0)

        # scale curved line radius
        scale_r = inner_r + 30
        # still centred on centre_x, outer_r
        scale_left_x = centre_x - scale_r * math.cos(scale_out_angle)
        scale_left_y = outer_r - scale_r * math.sin(scale_out_angle)
        scale_right_x = centre_x + scale_r * math.cos(scale_out_angle)

        path_data = """
M 0 %s
A %s %s 0 0 1 %s %s
L %s %s
A %s %s 0 0 0 %s %s
Z""" % (outer_y,
       outer_r, outer_r, outer_x, outer_y,
       inner_right_x, inner_right_y,
       inner_r, inner_r, inner_left_x, inner_right_y)

        self[0] = tag.ClosedPart(tag_name='path', attribs={
                                                            "fill":"white",
                                                            "stroke":"black",
                                                            "stroke-width":"1",
                                                            "d":path_data
                                                           })
        # The arrow points
        arrow_points = ""
        # move all points to the right and down,
        # note 24.5 is x distance to arrow point
        x_move = centre_x - 24.5
        # moves arrow down to just touch the scale
        y_move = outer_r - scale_r
        for p in self._points:
            point = "%s, %s " % (p[0] + x_move, p[1] + y_move)
            arrow_points += point
        self[1] = tag.ClosedPart(tag_name='polygon', attribs={
                                                           "fill":"black",
                                                           "stroke":"red",
                                                           "stroke-width":"2",
                                                           "points":arrow_points })

        # insert a circle at arrow hub
        self[2] = tag.ClosedPart(tag_name='circle', attribs={
                                                           "cx": str(centre_x),
                                                           "cy": str(outer_r),
                                                           "r": "50",
                                                           "fill":"black",
                                                           "stroke":"red",
                                                           "stroke-width":"2" })

        # Draw the scale curve
        scale_data = """
M %s %s
A %s %s 0 0 1 %s %s
""" % (scale_left_x, scale_left_y,
       scale_r, scale_r, scale_right_x, scale_left_y,)

        self[3] = tag.ClosedPart(tag_name='path', attribs={ "fill":"none",
                                                            "stroke":"black",
                                                            "stroke-width":"2",
                                                            "d":scale_data
                                                           })

        # store these values for use in build
        self._centre_x = centre_x
        self._centre_y = outer_r
        self._scale_r = scale_r
        self._scale_angle = Decimal(scale_angle)


    def _build(self, page, ident_list, environ, call_data, lang):
        if self.get_field_value("transform"):
            self.update_attribs({"transform":self.get_field_value("transform")})
        if self.get_field_value("arrow_stroke"):
            self[1].update_attribs({"stroke":self.get_field_value("arrow_stroke")})
            self[2].update_attribs({"stroke":self.get_field_value("arrow_stroke")})
        # make the scale
        minscale, maxscale = self._make_scale(self.get_field_value("minimum"),
                                              self.get_field_value("maximum"),
                                              self.get_field_value("smallintervals"),
                                              self.get_field_value("largeintervals"))

        # start angle is 180 - 120 / 2 normally 30
        start_angle = (Decimal('180') - self._scale_angle)/Decimal('2')

        # small lines, each of length 20
        minitems = len(minscale)
        scalemindegs = self._scale_angle / (minitems-1)
        line_r = self._scale_r + 20
        n = 4
        for index, item in enumerate(minscale):
            angle = start_angle + index*scalemindegs
            rads = math.radians(float(angle))

            x1 = self._centre_x - self._scale_r * math.cos(rads)
            y1 = self._centre_y - self._scale_r * math.sin(rads)
            x2 = self._centre_x - line_r * math.cos(rads)
            y2 = self._centre_y - line_r * math.sin(rads)

            self[n] = tag.ClosedPart(tag_name='line', attribs={
                                                            'x1':str(x1),
                                                            'y1':str(y1),
                                                            'x2':str(x2),
                                                            'y2':str(y2),
                                                            'stroke':"black",
                                                            'stroke-width':"1"  })
            n += 1

        # large lines, each of length 40
        maxitems = len(maxscale)
        scalemaxdegs = self._scale_angle / (maxitems-1)
        line_r = self._scale_r + 40
        # slightly shorter r as the curved line has stroke width of 2
        reduced_r = self._scale_r - 1
        for index, item in enumerate(maxscale):
            angle = start_angle + index*scalemaxdegs
            rads = math.radians(float(angle))

            x1 = self._centre_x - reduced_r * math.cos(rads)
            y1 = self._centre_y - reduced_r * math.sin(rads)
            x2 = self._centre_x - line_r * math.cos(rads)
            y2 = self._centre_y - line_r * math.sin(rads)

            self[n] = tag.ClosedPart(tag_name='line', attribs={
                                                            'x1':str(x1),
                                                            'y1':str(y1),
                                                            'x2':str(x2),
                                                            'y2':str(y2),
                                                            'stroke':"black",
                                                            'stroke-width':"3"  })
            n += 1
            self[n] = tag.Part(tag_name='text', text=str(item), attribs={
                                                            'x':str(x2-10),
                                                            'y': str(y2-5),
                                                            'font-size': '20',
                                                            'font-family': 'arial',
                                                            'stroke':"black",
                                                            'stroke-width':"1"  })

            n += 1

        # now place arrow at the measurement point
        measurement = Decimal(self.get_field_value("measurement"))
        self._minvalue = maxscale[0]
        self._maxvalue = maxscale[-1]
        centre_string = " " + str(self._centre_x) + " " + str(self._centre_y) + ")"
        if measurement >= self._maxvalue:
            self[1].update_attribs({"transform" : "rotate(" + str(self._scale_angle/2) + centre_string})
            return
        if measurement <= self._minvalue:
            self[1].update_attribs({"transform" : "rotate(-" + str(self._scale_angle/2) + centre_string})
            return

        measurement_angle = (measurement - self._minvalue)*self._scale_angle/(self._maxvalue-self._minvalue) - self._scale_angle/2

        rotate_string = "rotate(" + str(measurement_angle) + centre_string
        self[1].update_attribs({"transform" : rotate_string})





