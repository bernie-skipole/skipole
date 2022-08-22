

from .. import tag
from . import Widget, ClosedWidget, FieldArg, FieldArgList, FieldArgTable, FieldArgDict



class SVGContainer(Widget):

    # This class does not display any error messages
    display_errors = False

    arg_descriptions = {
                        'width':FieldArg("text", "100", jsonset=True),
                        'height':FieldArg("text", "100", jsonset=True),
                        'viewBox':FieldArg("text", "", jsonset=True),
                        'preserveAspectRatio':FieldArg("text", "", jsonset=True)
                       }

    _container = ((),)

    def __init__(self, name=None, brief='', **field_args):
        """Acts as an SVG widget, containing other widgets, so show, class and dimensions can be set"""
        Widget.__init__(self, name=name, brief=brief, **field_args)
        self.tag_name = "svg"
        self.htmlescaped = False
        self.linebreaks = False
        # the widget is a container
        self[0] = ""

    def _build(self, page, ident_list, environ, call_data, lang):
        if self.wf.width:
            self.attribs["width"] = self.wf.width
        if self.wf.height:
            self.attribs["height"] = self.wf.height
        if self.wf.viewBox:
            self.attribs["viewBox"] = self.wf.viewBox
        if self.wf.preserveAspectRatio:
            self.attribs["preserveAspectRatio"] = self.wf.preserveAspectRatio

    @classmethod
    def description(cls):
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

    _container = ((),)

    def __init__(self, name=None, brief='', **field_args):
        """Acts as an g widget, containing other widgets, so group class, style, transform can be set"""
        Widget.__init__(self, name=name, brief=brief, **field_args)
        self.tag_name = "g"
        self.htmlescaped = False
        self.linebreaks = False
        # The widget is a container
        self[0] = ""

    def _build(self, page, ident_list, environ, call_data, lang):
        if self.wf.transform:
            self.attribs["transform"] = self.wf.transform

    @classmethod
    def description(cls):
        """Returns a text string to illustrate the widget"""
        return """
<g>  <!-- with widget id and class widget_class, and transform attribute if given -->
  <!-- further svg elements and widgets can be contained here -->
</g>"""


class TextBlockGroup(Widget):
    """A g tag, containing a TextBlock. The TextBlock is not escaped, so may contain
       svg commands which are set directly into the g"""

    # This class does not display any error messages
    display_errors = False


    arg_descriptions = {'textblock_ref':FieldArg("textblock_ref", ""),
                        'textblock_project':FieldArg("text", ""),
                        'content_refnotfound':FieldArg("text", ""),
                        'content_replaceblock':FieldArg("text", "" ,jsonset=True),
                        'transform':FieldArg("text", "", jsonset=True)
                       }

    def __init__(self, name=None, brief='', **field_args):
        """
        textblock_ref: The reference of the TextBlock appearing in the g
        textblock_project: Set with a project name if the TextBlock is defined in a sub project
        content_refnotfound: content to appear if the textblock is not found
        content_replaceblock: content set here will replace the textblock
        """
        # pass fields to Widget
        Widget.__init__(self, name=name, brief=brief, **field_args)
        self.tag_name = "g"
        self[0] = ''
        self.htmlescaped = False
        self.linebreaks = False

    def _build(self, page, ident_list, environ, call_data, lang):
        # define the textblock
        tblock = self.wf.textblock_ref
        tblock.project = self.wf.textblock_project
        tblock.failmessage = self.wf.content_refnotfound
        tblock.escape = False
        tblock.linebreaks = False
        # place it at location 0
        if self.wf.content_replaceblock:
            self[0] = self.wf.content_replaceblock
        else:
            self[0] = tblock
        if self.wf.transform:
            self.attribs["transform"] = self.wf.transform

    @classmethod
    def description(cls):
        """Returns a text string to illustrate the widget"""
        return """
<g>  <!-- with widget id and class widget_class, and transform attribute if given -->
   <!-- set with either content_replaceblock or textblock content as unescaped xtml -->
</g>"""



class TextGroup(Widget):
    """A g tag, containing a string. The string is not escaped, so may contain
       svg commands which are set directly into the g"""

    # This class does not display any error messages
    display_errors = False


    arg_descriptions = {
                        'text':FieldArg("text", "" ,jsonset=True),
                        'transform':FieldArg("text", "", jsonset=True)
                       }

    def __init__(self, name=None, brief='', **field_args):
        """
       text: the string set here will be set as content
        """
        # pass fields to Widget
        Widget.__init__(self, name=name, brief=brief, **field_args)
        self.tag_name = "g"
        self[0] = ''
        self.htmlescaped = False
        self.linebreaks = False

    def _build(self, page, ident_list, environ, call_data, lang):
        if self.wf.text:
            self[0] = self.wf.text
        if self.wf.transform:
            self.attribs["transform"] = self.wf.transform

    @classmethod
    def description(cls):
        """Returns a text string to illustrate the widget"""
        return """
<g>  <!-- with widget id and class widget_class, and transform attribute if given -->
   <!-- set with text content as unescaped xtml -->
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
        ClosedWidget.__init__(self, name=name, brief=brief, **field_args)
        self.tag_name = "rect"


    def _build(self, page, ident_list, environ, call_data, lang):
        "Set the attributes"
        # Note - all arg_descriptions are attributes, apart from stroke_width which is actually
        # attribute stroke-width. So update the tag with each item from arg_descriptions
        for att in self.arg_descriptions.keys():
            if getattr(self.wf, att, ''):
                if att == "stroke_width":
                    self.attribs["stroke-width"] = getattr(self.wf, att)
                else:
                    self.attribs[att] = getattr(self.wf, att)

    @classmethod
    def description(cls):
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
        Widget.__init__(self, name=name, brief=brief, **field_args)
        self.tag_name = "text"
        self.hide_if_empty=False


    def _build(self, page, ident_list, environ, call_data, lang):
        "Set the attributes"
        if self.wf.x:
            self.attribs["x"] = self.wf.x
        if self.wf.y:
            self.attribs["y"] = self.wf.y
        if self.wf.dx:
            self.attribs["dx"] = self.wf.dx
        if self.wf.dy:
            self.attribs["dy"] = self.wf.dy
        if self.wf.font_family:
            self.attribs["font-family"] = self.wf.font_family
        if self.wf.font_size:
            self.attribs["font-size"] = self.wf.font_size
        if self.wf.fill:
            self.attribs["fill"] = self.wf.fill
        if self.wf.stroke:
            self.attribs["stroke"] = self.wf.stroke
        if self.wf.stroke_width:
            self.attribs["stroke-width"] = self.wf.stroke_width
        self[0] = self.wf.text


    @classmethod
    def description(cls):
        """Returns a text string to illustrate the widget"""
        return """
<text> <!-- with widget id, class widget_class and the given attributes -->
  <!-- contains given text -->
</text>"""



class TextList(Widget):
    """An svg text tag with further tspan elements
    """

    # This class does not display any error messages
    display_errors = False

    arg_descriptions = {'font_family':FieldArg("text", "Arial", jsonset=True),
                        'font_size':FieldArg("text", "20", jsonset=True),
                        'fill':FieldArg("text", "white", jsonset=True),
                        'stroke':FieldArg("text", "", jsonset=True),
                        'stroke_width':FieldArg("text", "", jsonset=True),
                        'lines': FieldArgTable(['integer', 'integer', 'text'])
                       }

    def __init__(self, name=None, brief='', **field_args):
        """
        font_family: font-family css  attribute, such as Arial
        font_size: font-size css  attribute, such as 20
        fill: The fill colour, use none for no fill
        stroke: The outline edge colour
        stroke_width: The outline edge width
        lines: List of lists, of [x,y,text]
        """
        # pass fields to Widget
        Widget.__init__(self, name=name, brief=brief, **field_args)
        self.tag_name = "text"
        self.hide_if_empty=False


    def _build(self, page, ident_list, environ, call_data, lang):
        "Set the attributes"
        if self.wf.font_family:
            self.attribs["font-family"] = self.wf.font_family
        if self.wf.font_size:
            self.attribs["font-size"] = self.wf.font_size
        if self.wf.fill:
            self.attribs["fill"] = self.wf.fill
        if self.wf.stroke:
            self.attribs["stroke"] = self.wf.stroke
        if self.wf.stroke_width:
            self.attribs["stroke-width"] = self.wf.stroke_width
        lines = self.wf.lines
        if not lines:
            return
        line1 = lines[0]
        self.attribs["x"] = str(line1[0])
        self.attribs["y"] = str(line1[1])
        self[0] = line1[2]
        for line in lines[1:]:
            tspan = tag.Part(tag_name='tspan', text = line[2])
            tspan.attribs["x"] = str(line[0])
            tspan.attribs["y"] = str(line[1])
            self.append(tspan)

    @classmethod
    def description(cls):
        """Returns a text string to illustrate the widget"""
        return """
<text> <!-- with widget id, class widget_class and the given attributes -->
  <!-- contains given text, each line within tspan elements -->
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
        ClosedWidget.__init__(self, name=name, brief=brief, **field_args)
        self.tag_name = "circle"


    def _build(self, page, ident_list, environ, call_data, lang):
        "Set the attributes"
        # Note - all arg_descriptions are attributes, apart from stroke_width which is actually
        # attribute stroke-width. So update the tag with each item from arg_descriptions
        for att in self.arg_descriptions.keys():
            if getattr(self.wf, att, ''):
                if att == "stroke_width":
                    self.attribs["stroke-width"] = getattr(self.wf, att)
                else:
                    self.attribs[att] = getattr(self.wf, att)

    @classmethod
    def description(cls):
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
        ClosedWidget.__init__(self, name=name, brief=brief, **field_args)
        self.tag_name = "line"


    def _build(self, page, ident_list, environ, call_data, lang):
        "Set the attributes"
        # Note - all arg_descriptions are attributes, apart from stroke_width which is actually
        # attribute stroke-width. So update the tag with each item from arg_descriptions
        for att in self.arg_descriptions.keys():
            if getattr(self.wf, att, ''):
                if att == "stroke_width":
                    self.attribs["stroke-width"] = getattr(self.wf, att)
                else:
                    self.attribs[att] = getattr(self.wf, att)


    @classmethod
    def description(cls):
        """Returns a text string to illustrate the widget"""
        return """
<line /> <!-- creates line with widget id, class widget_class and the given attributes -->"""


class Ellipse(ClosedWidget):
    """An svg ellipse tag
    """

    # This class does not display any error messages
    display_errors = False

    arg_descriptions = {'cx':FieldArg("text", "50", jsonset=True),
                        'cy':FieldArg("text", "50", jsonset=True),
                        'rx':FieldArg("text", "40", jsonset=True),
                        'ry':FieldArg("text", "20", jsonset=True),
                        'fill':FieldArg("text", "none", jsonset=True),
                        'stroke':FieldArg("text", "black", jsonset=True),
                        'stroke_width':FieldArg("text", "1", jsonset=True)
                       }

    def __init__(self, name=None, brief='', **field_args):
        """
        cx: centre x coords, for example 50
        cy: centre y coords, for example 50
        rx: the horizontal radius, for example 40
        ry: the vertical radius, for example 20
        fill: The fill colour, use none for no fill
        stroke: The outline edge colour
        stroke_width: The outline edge width
        """
        # pass fields to Widget
        ClosedWidget.__init__(self, name=name, brief=brief, **field_args)
        self.tag_name = "ellipse"


    def _build(self, page, ident_list, environ, call_data, lang):
        "Set the attributes"
        # Note - all arg_descriptions are attributes, apart from stroke_width which is actually
        # attribute stroke-width. So update the tag with each item from arg_descriptions
        for att in self.arg_descriptions.keys():
            if getattr(self.wf, att, ''):
                if att == "stroke_width":
                    self.attribs["stroke-width"] = getattr(self.wf, att)
                else:
                    self.attribs[att] = getattr(self.wf, att)


    @classmethod
    def description(cls):
        """Returns a text string to illustrate the widget"""
        return """
<ellipse /> <!-- creates ellipse with widget id, class widget_class and the given attributes -->"""



class Polygon(ClosedWidget):
    """An svg polygon tag
    """

    # This class does not display any error messages
    display_errors = False

    arg_descriptions = {
                        'points':FieldArgTable(['text', 'text'], jsonset=True),
                        'fill':FieldArg("text", "none", jsonset=True),
                        'stroke':FieldArg("text", "black", jsonset=True),
                        'stroke_width':FieldArg("text", "1", jsonset=True)
                       }

    def __init__(self, name=None, brief='', **field_args):
        """
        points : a list of two element lists, each inner list being a point
        fill: The fill colour, use none for no fill
        stroke: The outline edge colour
        stroke_width: The outline edge width
        """
        # pass fields to Widget
        ClosedWidget.__init__(self, name=name, brief=brief, **field_args)
        self.tag_name = "polygon"


    def _build(self, page, ident_list, environ, call_data, lang):
        "Set the attributes"

        if self.wf.fill:
            self.attribs["fill"] = self.wf.fill
        if self.wf.stroke:
            self.attribs["stroke"] = self.wf.stroke
        if self.wf.stroke_width:
            self.attribs["stroke-width"] = self.wf.stroke_width

        if not self.wf.points:
            return

        points_att = ""
        points = self.wf.points
        for x,y in points:
            points_att += "%s,%s " % (x,y)
        self.attribs['points'] = points_att   
  

    @classmethod
    def description(cls):
        """Returns a text string to illustrate the widget"""
        return """
<polygon /> <!-- creates polygon with widget id, class widget_class and the given points -->"""



class Polyline(ClosedWidget):
    """An svg polyline tag
    """

    # This class does not display any error messages
    display_errors = False

    arg_descriptions = {
                        'points':FieldArgTable(['text', 'text'], jsonset=True),
                        'fill':FieldArg("text", "none", jsonset=True),
                        'stroke':FieldArg("text", "black", jsonset=True),
                        'stroke_width':FieldArg("text", "1", jsonset=True)
                       }

    def __init__(self, name=None, brief='', **field_args):
        """
        points : a list of two element lists, each inner list being a point
        fill: The fill colour, use none for no fill
        stroke: The outline edge colour
        stroke_width: The outline edge width
        """
        # pass fields to Widget
        ClosedWidget.__init__(self, name=name, brief=brief, **field_args)
        self.tag_name = "polyline"


    def _build(self, page, ident_list, environ, call_data, lang):
        "Set the attributes"

        if self.wf.fill:
            self.attribs["fill"] = self.wf.fill
        if self.wf.stroke:
            self.attribs["stroke"] = self.wf.stroke
        if self.wf.stroke_width:
            self.attribs["stroke-width"] = self.wf.stroke_width

        if not self.wf.points:
            return

        points_att = ""
        points = self.wf.points
        for x,y in points:
            points_att += "%s,%s " % (x,y)
        self.attribs['points'] = points_att   
  

    @classmethod
    def description(cls):
        """Returns a text string to illustrate the widget"""
        return """
<polyline /> <!-- creates polyline with widget id, class widget_class and the given points -->"""



class Path(ClosedWidget):
    """An svg path tag
    """

    # This class does not display any error messages
    display_errors = False

    arg_descriptions = {'d':FieldArg("text", "", jsonset=True),
                        'fill':FieldArg("text", "none", jsonset=True),
                        'stroke':FieldArg("text", "black", jsonset=True),
                        'stroke_width':FieldArg("text", "1", jsonset=True)
                       }

    def __init__(self, name=None, brief='', **field_args):
        """
        d: The path data
        fill: The fill colour, use none for no fill
        stroke: The outline edge colour
        stroke_width: The outline edge width
        """
        # pass fields to Widget
        ClosedWidget.__init__(self, name=name, brief=brief, **field_args)
        self.tag_name = "path"


    def _build(self, page, ident_list, environ, call_data, lang):
        "Set the attributes"
        # Note - all arg_descriptions are attributes, apart from stroke_width which is actually
        # attribute stroke-width. So update the tag with each item from arg_descriptions
        for att in self.arg_descriptions.keys():
            if getattr(self.wf, att, ''):
                if att == "stroke_width":
                    self.attribs["stroke-width"] = getattr(self.wf, att)
                else:
                    self.attribs[att] = getattr(self.wf, att)

    @classmethod
    def description(cls):
        """Returns a text string to illustrate the widget"""
        return """
<path /> <!-- creates path with widget id, class widget_class and the given attributes -->"""


