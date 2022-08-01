
"Contains link widgets"

from urllib.parse import quote

from .. import skiboot, tag
from . import Widget, ClosedWidget, ClickEventMixin, FieldArg, FieldArgList, FieldArgTable, FieldArgDict




class IconLink(Widget):
    """A link with two optional get fields to the page with the given ident, label or url,
       with svg content"""

    _container = ((0,0),)

    # This class does not display any error messages
    display_errors = False

    arg_descriptions = {'link_ident':FieldArg("url", ''),
                        'get_field1':FieldArg("text", "", valdt=True),
                        'get_field2':FieldArg("text","", valdt=True),
                        'svg_class':FieldArg("cssclass", ""),
                        'svg_style':FieldArg("cssstyle", ""),
                        'target':FieldArg("text", ""),
                        'force_ident':FieldArg("boolean", False),
                        'svg_width':FieldArg("text", "100"),
                        'svg_height':FieldArg("text", "100"),
                        'svg_viewBox':FieldArg("text", ""),
                        'svg_preserveAspectRatio':FieldArg("text", ""),
                        'transform':FieldArg("text", "")
                        }

    def __init__(self, name=None, brief='', **field_args):
        """
        link_ident: The url, ident or label to link with
        get_field1: Optional 'get' string set in the target url
        get_field2: Optional second 'get' string set in the target url
        svg_class: the class attribute of the svg element holding the container
        svg_style: the style attribute of the svg element holding the container
        target: if given, the target attribute will be set
        force_ident: If True then the page ident will be included, even if no get fields set
                     If False, the page ident will only be included if a get field is set
        """
        Widget.__init__(self, name=name, brief=brief, **field_args)
        self.tag_name = "a"
        # The location 0,0 is available as a container
        self[0] = tag.Part(tag_name="svg")
        self[0][0] = tag.Part(tag_name="g")
        self[0][0][0] = ''

    def _build(self, page, ident_list, environ, call_data, lang):
        "Build the link"
        if not self.wf.link_ident:
            self._error = "Warning: broken link"
            return
        url = self.get_url(self.wf.link_ident)
        if not url:
            self._error = "Warning: broken link"
            return
        # create a url for the href
        get_fields = {self.get_formname("get_field1"):self.wf.get_field1,
                      self.get_formname("get_field2"):self.wf.get_field2}
        # add get fields and page ident_data to the url (defined in tag.ParentPart)
        self.attribs["href"] = self.make_get_url(page, url, get_fields, self.wf.force_ident)
        if self.wf.target:
            self.attribs["target"] = self.wf.target

        # the svg tag holding the container
        if self.wf.svg_class:
            self[0].attribs["class"] = self.wf.svg_class
        if self.wf.svg_style:
            self[0].attribs["style"] = self.wf.svg_style
        if self.wf.svg_width:
            self[0].attribs["width"] = self.wf.svg_width
        if self.wf.svg_height:
            self[0].attribs["height"] = self.wf.svg_height
        if self.wf.svg_viewBox:
            self[0].attribs["viewBox"] = self.wf.svg_viewBox
        if self.wf.svg_preserveAspectRatio:
            self[0].attribs["preserveAspectRatio"] = self.wf.svg_preserveAspectRatio

        if self.wf.transform:
            self[0][0].attribs["transform"] = self.wf.transform


    @classmethod
    def description(cls):
        """Returns a text string to illustrate the widget"""
        return """
<a href="#">  <!-- with widget id and class widget_class and href the url -->
    <svg> <!-- with the specified svg attributes -->
      <g> <!-- with transform attribute if given -->
         <!-- container 0 for further svg elements -->
      </g>
    </svg>
</a>"""



class ContainerLink1(Widget):
    """A link to the page with the given ident, label or url, and two optional get fields.
       The link a tag is the parent of a container into which further html can be inserted"""

    _container = ((),)

    # This class does not display any error messages
    display_errors = False

    arg_descriptions = {'link_ident':FieldArg("url", ''),
                        'get_field1':FieldArg("text", "", valdt=True, jsonset=True),
                        'get_field2':FieldArg("text","", valdt=True, jsonset=True),
                        'target':FieldArg("text", ""),
                        'force_ident':FieldArg("boolean", False)
                       }

    def __init__(self, name=None, brief='', **field_args):
        """
        link_ident: The url, ident or label to link with
        get_field1: Optional 'get' string set in the target url
        get_field2: Optional second 'get' string set in the target url
         target: if given, the target attribute will be set
        force_ident: If True then the page ident will be included, even if no get fields set
                     If False, the page ident will only be included if a get field is set
        """
        Widget.__init__(self, name=name, brief=brief, **field_args)
        self.tag_name = "a"
        # where content can be placed
        self[0] = ''

    def _build(self, page, ident_list, environ, call_data, lang):
        "Build the link"
        # self[0] is initially set as the empty string ''
        if not self.wf.link_ident:
            self._error = "Warning: broken link"
            return
        url = self.get_url(self.wf.link_ident)
        if not url:
            self._error = "Warning: broken link"
            return
        # create a url for the href
        get_fields = {self.get_formname("get_field1"):self.wf.get_field1,
                      self.get_formname("get_field2"):self.wf.get_field2}
        # add get fields and page ident_data to the url (defined in tag.ParentPart)
        self.attribs["href"] = self.make_get_url(page, url, get_fields, self.wf.force_ident)
        if self.wf.target:
            self.attribs["target"] = self.wf.target

    @classmethod
    def description(cls):
        """Returns a text string to illustrate the widget"""
        return """
<a href="#">  <!-- with widget id and class widget_class and href the url -->
      <!-- container 0 for further html -->
</a>"""


class ContainerLink2(Widget):
    """A link to the page with the given ident, label or url, and two optional get fields.
       get_fields are JSON settable
       Can request a json return if json_ident set
       The link a tag is the parent of a container into which further html can be inserted
       Always sends page ident"""

    _container = ((),)

    # This class does not display any error messages
    display_errors = False

    arg_descriptions = {'json_ident':FieldArg("url", ''),
                        'link_ident':FieldArg("url", 'no_javascript'),
                        'get_field1':FieldArg("text", "", valdt=True, jsonset=True),
                        'get_field2':FieldArg("text","", valdt=True, jsonset=True)
                       }

    def __init__(self, name=None, brief='', **field_args):
        """
        json_ident: The url, ident or label to link, expecting a json file to be returned
        link_ident: The url, ident or label to link with if the client does not have javascript, or json_ident left blank
        get_field1: Optional 'get' string set in the target url
        get_field2: Optional second 'get' string set in the target url
        """
        Widget.__init__(self, name=name, brief=brief, **field_args)
        self.tag_name = "a"
        # where content can be placed
        self[0] = ''


    def _build(self, page, ident_list, environ, call_data, lang):
        "Build the link"

        if not self.wf.link_ident:
            # setting self._error replaces the entire tag
            self._error = "Warning: No link ident"
            return


        url = self.get_url(self.wf.link_ident)
        if not url:
            self._error = "Warning: broken link"
            return
        # create a url for the href
        get_fields = {self.get_formname("get_field1"):self.wf.get_field1,
                      self.get_formname("get_field2"):self.wf.get_field2}

        # add get fields and page ident_data to the url (defined in tag.ParentPart)
        self.attribs["href"] = self.make_get_url(page, url, get_fields, True)

        if self.wf.json_ident:
            jsonurl = self.get_url(self.wf.json_ident)
            # any label:value added to self.jlabels will be set in a javascript fieldvalues attribute for the widget
            if jsonurl:
                self.jlabels['url'] = jsonurl


    def _build_js(self, page, ident_list, environ, call_data, lang):
        """Sets a click event handler"""
        ident=self.get_id()
        return f"""  $("#{ident}").click(function (e) {{
    SKIPOLE.widgets['{ident}'].eventfunc(e);
    }});
"""

    @classmethod
    def description(cls):
        """Returns a text string to illustrate the widget"""
        return """
<a href="#">  <!-- with widget id and class widget_class and href the url -->
      <!-- container 0 for further html -->
</a>"""



class Link(Widget):
    """A link to the page with the given ident, label or url, with a text string as the
       visible content and two optional get fields.
       On error replace the link by the error message"""

    # This class does not display any error messages
    display_errors = False

    arg_descriptions = {'link_ident':FieldArg("url", ''),
                        'get_field1':FieldArg("text", "", valdt=True, jsonset=True),
                        'get_field2':FieldArg("text","", valdt=True, jsonset=True),
                        'content':FieldArg("text", "", jsonset=True),
                        'target':FieldArg("text", ""),
                        'force_ident':FieldArg("boolean", False)
                       }

    def __init__(self, name=None, brief='', **field_args):
        """
        link_ident: The url, ident or label to link with
        get_field1: Optional 'get' string set in the target url
        get_field2: Optional second 'get' string set in the target url
        content: The text to be placed within the link, if none given, the page url will be used
        target: if given, the target attribute will be set
        force_ident: If True then the page ident will be included, even if no get fields set
                     If False, the page ident will only be included if a get field is set
        """
        Widget.__init__(self, name=name, brief=brief, **field_args)
        self.tag_name = "a"
        # where content can be placed
        self[0] = ''

    def _build(self, page, ident_list, environ, call_data, lang):
        "Build the link"
        # self[0] is initially set as the empty string ''
        if self.wf.content:
            self[0] = self.wf.content
        if not self.wf.link_ident:
            self._error = "Warning: broken link"
            return
        url = self.get_url(self.wf.link_ident)
        if not url:
            self._error = "Warning: broken link"
            return
        if not self[0]:
            # if no content, place the page url as content
            self[0] = url
        # create a url for the href
        get_fields = {self.get_formname("get_field1"):self.wf.get_field1,
                      self.get_formname("get_field2"):self.wf.get_field2}
        # add get fields and page ident_data to the url (defined in tag.ParentPart)
        self.attribs["href"] = self.make_get_url(page, url, get_fields, self.wf.force_ident)
        if self.wf.target:
            self.attribs["target"] = self.wf.target

    @classmethod
    def description(cls):
        """Returns a text string to illustrate the widget"""
        return """
<a href="#">  <!-- with widget id and class widget_class and href the url -->
  <!-- content or url if no content given -->
</a>"""


class LinkToWidget(Widget):
    """A link to a widget on the same page
       On error replace the link by the error message"""

    # This class does not display any error messages
    display_errors = False

    arg_descriptions = {'content':FieldArg("text", "", jsonset=True),
                        'towidget':FieldArg("text", "", jsonset=True)
                       }

    def __init__(self, name=None, brief='', **field_args):
        """
        content: The text to be placed within the link, if none given, the towidget id will be used
        towidget: widget name, or sectionalias,widgetname
        """
        Widget.__init__(self, name=name, brief=brief, **field_args)
        self.tag_name = "a"
        # where content can be placed
        self[0] = ''

    def _build(self, page, ident_list, environ, call_data, lang):
        "Build the link"
        # self[0] is initially set as the empty string ''
        if self.wf.content:
            self[0] = self.wf.content
        wdgetname = self.wf.towidget
        if not wdgetname:
            self._error = "Warning: broken link"
            return
        widget_id = '#' + str( skiboot.make_widgfield(wdgetname, widgetonly=True) )
        if not self[0]:
            # if no content, place the widget id as content
            self[0] = widget_id
        self.attribs["href"] = widget_id

    @classmethod
    def description(cls):
        """Returns a text string to illustrate the widget"""
        return """
<a href="#target_widget_id">  <!-- with widget id and class widget_class -->
  <!-- content -->
</a>"""



class ImageOrTextLink(Widget):
    """A link to the page with the given ident, with four optional get fields.
       The displayed contents of the link is either an image page given by img_link
       or the text given by link_text
       If no link_ident is given, this is not an error - the img or text will simply
       be displayed in a span without a link.
       If no link or image or text is displayed, no widget will be shown
       On error replace the link by the error message"""

    # This class does not display any error messages
    display_errors = False

    arg_descriptions = {'link_ident':FieldArg("url",''),
                        'img_link':FieldArg("url",''),
                        'width':FieldArg("text", "100"),
                        'height':FieldArg("text", "100"),
                        'link_text':FieldArg("text", ""),
                        'get_field1':FieldArg("text", "", valdt=True),
                        'get_field2':FieldArg("text", "", valdt=True),
                        'get_field3':FieldArg("text", "", valdt=True),
                        'get_field4':FieldArg("text", "", valdt=True),
                        'target':FieldArg("text", ""),
                        'force_ident':FieldArg("boolean", False)
                       }

    def __init__(self, name=None, brief='', **field_args):
        """
        link_ident: The target page link ident
        img_link: The ident of the image page
        width: The width of the image, ignored if text is to be displayed
        height: The height of the image, ignored if text is to be displayed
        link_text: If given, this text will be used instead of an image
        get_field1: Optional 'get' string set in the target url
        get_field2: Optional second 'get' string set in the target url
        get_field3: Optional third 'get' string set in the target url
        get_field4: Optional fourth 'get' string set in the target url
        target: if given, the target attribute will be set
        force_ident: If True then the page ident will be included, even if no get fields set
                     If False, the page ident will only be included if a get field is set
        """
        Widget.__init__(self, name=name, brief=brief, **field_args)
        self.tag_name = "a"


    def _build(self, page, ident_list, environ, call_data, lang):
        "Build the link"

        if self.wf.link_ident:
            justurl = self.get_url(self.wf.link_ident)
            if justurl:
                # create a url for the href
                get_fields = {self.get_formname("get_field1"):self.wf.get_field1,
                              self.get_formname("get_field2"):self.wf.get_field2,
                              self.get_formname("get_field3"):self.wf.get_field3,
                              self.get_formname("get_field4"):self.wf.get_field4}
                self.attribs["href"] = self.make_get_url(page, justurl, get_fields, self.wf.force_ident)
                if self.wf.target:
                    self.attribs["target"] = self.wf.target
            else:
                self.tag_name="span"
        else:
            justurl = ''
            self.tag_name="span"

        if self.wf.link_text:
            self[0] = self.wf.link_text
        elif self.wf.img_link:
            imageurl = self.get_url(self.wf.img_link)
            if imageurl:
                if self.wf.width and self.wf.height:
                    self[0] = tag.ClosedPart(tag_name="img", attribs={"src": quote(imageurl, safe='/:'),
                                                                      'width':self.wf.width,
                                                                      'height':self.wf.height})
                elif self.wf.width:
                    self[0] = tag.ClosedPart(tag_name="img", attribs={"src": quote(imageurl, safe='/:'),
                                                                      'width':self.wf.width})
                elif self.wf.height:
                    self[0] = tag.ClosedPart(tag_name="img", attribs={"src": quote(imageurl, safe='/:'),
                                                                      'height':self.wf.height})
                else:
                    self[0] = tag.ClosedPart(tag_name="img", attribs={"src": quote(imageurl, safe='/:')})
            else:
                # No image url, so show the text
                self[0] = self.wf.img_link
        elif justurl:
            # if no image ident or text, place the link page url as content, without the get fields
            self[0] = justurl
        else:
            # no text or link - nothing to show
            self[0] = ''
            self.show = False

    @classmethod
    def description(cls):
        """Returns a text string to illustrate the widget"""
        return """
<a href="#">  <!-- with widget id and class widget_class and href the url -->
  <!-- The link_text, if any. If no text given, then the following image -->
  <img src="#" />   <!-- with src set to url of img_ident -->
</a>"""


class CloseButton(ClickEventMixin, Widget):
    """A link button that closes a given section/widget, or if javascript is disabled, calls a link"""

    # This class does not display any error messages
    display_errors = False

    arg_descriptions = {'link_ident':FieldArg("url", ''),
                        'get_field1':FieldArg("text", "", valdt=True),
                        'get_field2':FieldArg("text","", valdt=True),
                        'target_section':FieldArg("text", ""),
                        'target_widget':FieldArg("text", ""),
                       }

    def __init__(self, name=None, brief='', **field_args):
        """
        link_ident: The link to an html page taken if the client does not have javascript
        get_field1: Optional 'get' string set in the target url
        get_field2: Optional second 'get' string set in the target url
        """
        Widget.__init__(self, name=name, brief=brief, **field_args)
        self.tag_name = "a"
        self.attribs["role"] = "button"
        self[0] = tag.HTMLSymbol("&times;")

    def _build(self, page, ident_list, environ, call_data, lang):
        "Build the link"
        if self.wf.link_ident:
            url = self.get_url(self.wf.link_ident)
            if url:
                # create a url for the href
                get_fields = {self.get_formname("get_field1"):self.wf.get_field1,
                              self.get_formname("get_field2"):self.wf.get_field2}
                self.attribs["href"] = self.make_get_url(page, url, get_fields, True)
        # any label:value added to self.jlabels will be set in a javascript fieldvalues attribute for the widget
        if self.wf.target_section:
            self.jlabels['target_section'] = self.wf.target_section
        if self.wf.target_widget:
            self.jlabels['target_widget'] = self.wf.target_widget


    @classmethod
    def description(cls):
        """Returns a text string to illustrate the widget"""
        return """
<a role="button" href="#"> <!-- with widget id and class widget_class, and the href link will be the url of the link_ident -->
      <!-- However if javascipt enabled the link will not be called, but the target widget will be hidden -->
      <!-- Content is the &times; symbol -->
</a>"""


class OpenButton(ClickEventMixin, Widget):
    """A link button that opens a given section/widget, or if javascript is disabled, calls a link"""

    # This class does not display any error messages
    display_errors = False

    arg_descriptions = {'link_ident':FieldArg("url", ''),
                        'get_field1':FieldArg("text", "", valdt=True),
                        'get_field2':FieldArg("text","", valdt=True),
                        'target_section':FieldArg("text", ""),
                        'target_widget':FieldArg("text", ""),
                       }

    def __init__(self, name=None, brief='', **field_args):
        """
        link_ident: The link to an html page taken if the client does not have javascript
        get_field1: Optional 'get' string set in the target url
        get_field2: Optional second 'get' string set in the target url
        """
        Widget.__init__(self, name=name, brief=brief, **field_args)
        self.tag_name = "a"
        self.attribs["role"] = "button"
        self[0] = tag.HTMLSymbol("&#9776;")

    def _build(self, page, ident_list, environ, call_data, lang):
        "Build the link"

        if self.wf.link_ident:
            url = self.get_url(self.wf.link_ident)
            if url:
                # create a url for the href
                get_fields = {self.get_formname("get_field1"):self.wf.get_field1,
                              self.get_formname("get_field2"):self.wf.get_field2}
                self.attribs["href"] = self.make_get_url(page, url, get_fields, True)
        # any label:value added to self.jlabels will be set in a javascript fieldvalues attribute for the widget
        if self.wf.target_section:
            self.jlabels['target_section'] = self.wf.target_section
        if self.wf.target_widget:
            self.jlabels['target_widget'] = self.wf.target_widget


    @classmethod
    def description(cls):
        """Returns a text string to illustrate the widget"""
        return """
<a role="button" href="#"> <!-- with widget id and class widget_class, and the href link will be the url of the link_ident -->
      <!-- However if javascipt enabled the link will not be called, but the target widget will be displayed -->
      <!-- Content is the &#9776; hamburger symbol -->
</a>"""



class OpenButton2(ClickEventMixin, Widget):
    """A link button that opens a given section/widget, or if javascript is disabled, calls a link"""

    # This class does not display any error messages
    display_errors = False

    arg_descriptions = {'link_ident':FieldArg("url", ''),
                        'hide':FieldArg("boolean", False, jsonset=True),
                        'get_field1':FieldArg("text", "", valdt=True, jsonset=True),
                        'get_field2':FieldArg("text","", valdt=True, jsonset=True),
                        'target_section':FieldArg("text", ""),
                        'target_widget':FieldArg("text", ""),
                        'content':FieldArg("text", "Open", jsonset=True)
                       }

    def __init__(self, name=None, brief='', **field_args):
        """
        link_ident: The link to an html page taken if the client does not have javascript
        get_field1: Optional 'get' string set in the target url
        get_field2: Optional second 'get' string set in the target url
        content: The text to be placed within the link
        hide: If True the button will be hidden
        """
        Widget.__init__(self, name=name, brief=brief, **field_args)
        self.tag_name = "a"
        self.attribs["role"] = "button"
        # where content can be placed
        self[0] = 'Open'

    def _build(self, page, ident_list, environ, call_data, lang):
        "Build the link"
        if self.wf.content:
            self[0] = self.wf.content
        # Hides widget if hide is True
        self.widget_hide(self.wf.hide)

        if self.wf.link_ident:
            url = self.get_url(self.wf.link_ident)
            if url:
                # create a url for the href
                get_fields = {self.get_formname("get_field1"):self.wf.get_field1,
                              self.get_formname("get_field2"):self.wf.get_field2}
                self.attribs["href"] = self.make_get_url(page, url, get_fields, True)
        # any label:value added to self.jlabels will be set in a javascript fieldvalues attribute for the widget
        if self.wf.target_section:
            self.jlabels['target_section'] = self.wf.target_section
        if self.wf.target_widget:
            self.jlabels['target_widget'] = self.wf.target_widget


    @classmethod
    def description(cls):
        """Returns a text string to illustrate the widget"""
        return """
<a role="button" href="#"> <!-- with widget id and class widget_class, and the href link will be the url of the link_ident -->
      <!-- However if javascipt enabled the link will not be called, but the target widget will be displayed -->
      <!-- The text of the content field will be set here -->
</a>"""



class JSONButtonLink(ClickEventMixin, Widget):
    """A button link to the JSON page with the given ident, label or url.
       Can send session or local storage values.
       On error replace the button text
       by the error message, and set widget class to error_class. You will
       need to provide a css button"""

    error_location = 0

    arg_descriptions = {'json_ident':FieldArg("url", ''),
                        'link_ident':FieldArg("url", 'no_javascript'),
                        'hide':FieldArg("boolean", False, jsonset=True),
                        'button_text':FieldArg("text", "", jsonset=True),
                        'button_wait_text':FieldArg("text", "Please wait..."),
                        'get_field1':FieldArg("text", "", valdt=True, jsonset=True),
                        'get_field2':FieldArg("text","", valdt=True, jsonset=True),
                        'session_storage':FieldArg("text", "", valdt=True),
                        'local_storage':FieldArg("text","", valdt=True),
                        'error_class':FieldArg("cssclass", "")
                       }

    def __init__(self, name=None, brief='', **field_args):
        """
        json_ident: The url, ident or label to link, expecting a json file to be returned
        link_ident: The link to an html page taken if the client does not have javascript
        hide: if True, and no error, button will be hidden
        button_text: The text to be placed within the link, if none given, the page url will be used
        button_wait_text: A 'please wait' message shown on the button while the call is made
        get_field1: Optional 'get' string set in the target url
        get_field2: Optional second 'get' string set in the target url
        session_storage: A session storage key, this widgfield returns the stored value if anything
        local_storage: A local storage key, this widgfield returns the stored value if anything
        widget_class: The class applied to the widget, should describe a button
        error_class: class which replaces widget_class on error
        """
        Widget.__init__(self, name=name, brief=brief, **field_args)
        self.tag_name = "a"
        self.attribs["role"] = "button"
        # on error, button text is replaced by error message
        self[0] = ''

    def _build(self, page, ident_list, environ, call_data, lang):
        "Build the link"
        if self.error_status and self.wf.error_class:
            self.attribs['class'] = self.wf.error_class
        # Hides widget if no error and hide is True
        self.widget_hide(self.wf.hide)
        if self.wf.json_ident:
            json_url = self.get_url(self.wf.json_ident)
        else:
            json_url = ''
        if self.wf.link_ident:
            html_url = self.get_url(self.wf.link_ident)
        else:
            html_url = ''
        if not html_url:
            if self.wf.error_class:
                self.attribs['class'] = self.wf.error_class
            self[0] = "Warning: broken link"
            return
        if self.wf.button_text:
            self[0] = self.wf.button_text
        else:
            self[0] = html_url
        # create a url for the href
        get_fields = {self.get_formname("get_field1"):self.wf.get_field1,
                      self.get_formname("get_field2"):self.wf.get_field2}
        self.attribs["href"] = self.make_get_url(page, html_url, get_fields, True)

        # any label:value added to self.jlabels will be set in a javascript fieldvalues attribute for the widget
        if self.wf.button_wait_text:
            self.jlabels['button_wait_text'] = self.wf.button_wait_text
        if self.wf.error_class:
            self.jlabels['error_class'] = self.wf.error_class
        if self.wf.widget_class:
            self.jlabels['widget_class'] = self.wf.widget_class
        if self.wf.session_storage:
            self.jlabels['session_storage'] = self.wf.session_storage
        if self.wf.local_storage:
            self.jlabels['local_storage'] = self.wf.local_storage
        if json_url:
            self.jlabels['json_url'] = json_url
        if html_url:
            self.jlabels['html_url'] = html_url

    @classmethod
    def description(cls):
        """Returns a text string to illustrate the widget"""
        return """
<a role="button" href="#">
      <!-- with widget id and class widget_class, and the href link will be the url of the link_ident -->
      <!-- However if javascipt enabled the json_ident link will be called on button click -->
      <!-- the button will show the button_text, and button_wait_text while pressed (if the
           client browser has javascript enabled). -->
</a>"""


class ButtonLink1(Widget):
    """A button link to the page with the given ident, label or url,
       and four optional get fields.  On error replace the button text
       by the error message, and set widget class to error_class. You will
       need to provide a css button"""

    error_location = 0

    arg_descriptions = {'link_ident':FieldArg("url", ''),
                        'hide':FieldArg("boolean", False, jsonset=True),
                        'get_field1':FieldArg("text", "", valdt=True),
                        'get_field2':FieldArg("text","", valdt=True),
                        'get_field3':FieldArg("text", "", valdt=True),
                        'get_field4':FieldArg("text","", valdt=True),
                        'button_text':FieldArg("text", "", jsonset=True),
                        'error_class':FieldArg("cssclass", ""),
                        'target':FieldArg("text", ""),
                        'force_ident':FieldArg("boolean", False)
                       }

    def __init__(self, name=None, brief='', **field_args):
        """
        link_ident: The url, ident or label to link with
        hide: if True, and no error, button will be hidden
        get_field1: Optional 'get' string set in the target url
        get_field2: Optional second 'get' string set in the target url
        get_field3: Optional third 'get' string set in the target url
        get_field4: Optional fourt 'get' string set in the target url
        button_text: The text to be displayed within the button. If none given, the page url will be used.
        widget_class: The class applied to the widget, should describe a button
        error_class: class which replaces widget_class on error
        target: if given, the target attribute will be set
        force_ident: If True then the page ident will be included, even if no get fields set
                     If False, the page ident will only be included if a get field is set
        """
        Widget.__init__(self, name=name, brief=brief, **field_args)
        self.tag_name = "a"
        self.attribs["role"] = "button"
        # on error, button text is replaced by error message
        self[0] = ''

    def _build(self, page, ident_list, environ, call_data, lang):
        "Build the link"
        if self.error_status and self.wf.error_class:
            self.attribs['class'] = self.wf.error_class
        # Hides widget if no error and hide is True
        self.widget_hide(self.wf.hide)
        if not self.wf.link_ident:
            if self.wf.error_class:
                self.attribs['class'] = self.wf.error_class
            self[0] = "Warning: broken link"
            return
        url = self.get_url(self.wf.link_ident)
        if not url:
            if self.wf.error_class:
                self.attribs['class'] = self.wf.error_class
            self[0] = "Warning: broken link"
            return
        if self.wf.button_text:
            self[0] = self.wf.button_text
        else:
            self[0] = url
        # create a url for the href
        get_fields = {self.get_formname("get_field1"):self.wf.get_field1,
                      self.get_formname("get_field2"):self.wf.get_field2,
                      self.get_formname("get_field3"):self.wf.get_field3,
                      self.get_formname("get_field4"):self.wf.get_field4}
        url = self.make_get_url(page, url, get_fields, self.wf.force_ident)
        self.attribs["href"] = url
        if self.wf.target:
            self.attribs["target"] = self.wf.target
        # any label:value added to self.jlabels will be set in a javascript fieldvalues attribute for the widget
        self.jlabels['error_class'] = self.wf.error_class
        self.jlabels['widget_class'] = self.wf.widget_class

    @classmethod
    def description(cls):
        """Returns a text string to illustrate the widget"""
        return """
<a role="button" href="#">
 <!-- with widget id and class widget_class, and the href link will be the url of the link_ident with the get_fields -->
 <!-- the button will show the button_text, on error this will be replaced by the error message -->
</a>"""



class ButtonLink2(Widget):
    """A div holding a button link to the page with the given ident, label or url,
       and two optional get fields."""

    error_location = (0,0,0)

    arg_descriptions = {'json_ident':FieldArg("url", ''),
                        'link_ident':FieldArg("url", 'no_javascript'),
                        'hide':FieldArg("boolean", False, jsonset=True),
                        'button_text':FieldArg("text", "Submit", jsonset=True),
                        'button_wait_text':FieldArg("text", "Please wait..."),
                        'button_class':FieldArg("cssclass", ""),
                        'button_style':FieldArg("cssstyle", ""),
                        'get_field1':FieldArg("text", "", valdt=True, jsonset=True),
                        'get_field2':FieldArg("text","", valdt=True, jsonset=True),
                        'error_class':FieldArg("cssclass", ""),
                        'buttondiv_class':FieldArg("cssclass", ""),
                        'buttondiv_style':FieldArg("cssstyle", "")
                       }

    def __init__(self, name=None, brief='', **field_args):
        """
        json_ident: The url, ident or label to link, expecting a json file to be returned
        link_ident: The link to an html page taken if the client does not have javascript
        hide: if True, and no error, button will be hidden
        button_text: The text to be placed within the link, if none given, the page url will be used
        button_wait_text: A 'please wait' message shown on the button
        button_class: A CSS class applied to the button
        button_style: A CSS style applied to the button
        buttondiv_class: A CSS class applied to the div containing the button
        buttondiv_style: A CSS style applied to the div containing the button
        get_field1: Optional 'get' string set in the target url
        get_field2: Optional second 'get' string set in the target url
        widget_class: The class applied to the widget
        error_class: class given to normally hidden error div
        """

        Widget.__init__(self, name=name, brief=brief, **field_args)
        self.tag_name = "div"
        # error div at 0
        self[0] = tag.Part(tag_name="div", attribs={"style":"display:none;"})
        self[0][0] = tag.Part(tag_name="p")
        self[0][0][0] = ''
        # buttondiv
        self[1] = tag.Part(tag_name="div")
        self[1][0] = tag.Part(tag_name="a", attribs={"role":"button"})


    def _build(self, page, ident_list, environ, call_data, lang):
        "Build the link"
        # Hides widget if no error and hide is True
        self.widget_hide(self.wf.hide)
        if self.wf.error_class:
            self[0].attribs["class"] = self.wf.error_class
        if self.error_status:
            del self[0].attribs["style"]
        if not self.wf.link_ident:
            # setting self._error replaces the entire tag
            self._error = "Warning: No link ident"
            return
        # any label:value added to self.jlabels will be set in a javascript fieldvalues attribute for the widget
        if self.wf.json_ident:
            self.jlabels['url'] = self.get_url(self.wf.json_ident)
        self.jlabels['button_wait_text'] = self.wf.button_wait_text

        # set buttondiv
        if self.wf.buttondiv_class:
            self[1].attribs["class"] = self.wf.buttondiv_class
        if self.wf.buttondiv_style:
            self[1].attribs["style"] = self.wf.buttondiv_style
        # set button class
        if self.wf.button_class:
            self[1][0].attribs["class"] = self.wf.button_class
        # set button style
        if self.wf.button_style:
            self[1][0].attribs["style"] = self.wf.button_style
        # get url and button text
        url = self.get_url(self.wf.link_ident)
        if not url:
            # setting self._error replaces the entire tag
            self._error = "Warning: Invalid link"
            return
        if self.wf.button_text:
            self[1][0][0] = self.wf.button_text
        else:
            self[1][0][0] = url
        # create a url for the href
        get_fields = {self.get_formname("get_field1"):self.wf.get_field1,
                      self.get_formname("get_field2"):self.wf.get_field2}
        self[1][0].attribs["href"] = self.make_get_url(page, url, get_fields, True)


    def _build_js(self, page, ident_list, environ, call_data, lang):
        """Sets a click event handler"""
        ident=self.get_id()
        return f"""  $("#{ident} a").click(function (e) {{
    SKIPOLE.widgets['{ident}'].eventfunc(e);
    }});
"""

    @classmethod
    def description(cls):
        """Returns a text string to illustrate the widget"""
        return """
<div> <!-- with widget id and class widget_class -->
  <div> <!-- normally hidden div, with class error_class -->
    <p> <!-- Any error text appears here --> </p>
  </div>
  <div> <!-- class attribute set to buttondiv_class, style to buttondiv_style -->
    <a role="button" href="#">
      <!-- With class set by button_class, and the href link will be the url of the link_ident -->
      <!-- However if javascipt enabled the json_ident link will be called on button click -->
      <!-- the button will show the button_text. -->
    </a>
  </div>
</div>"""



class MessageButton(Widget):
    """A div containing a link with a hidden 'message div'. When the link is called the
       message div is displayed and contains a further div with a paragraph
       of text and an X button which hides the message.
       Typically calling a link will be so fast the message will not be displayed, so this
       widget could be used with a link which calls a very slow loading page, or
       perhaps a please wait until the message is updated via json."""

    # This class does not display any error messages
    display_errors = False

    arg_descriptions = {'hide':FieldArg("boolean", True, jsonset=True),
                        'para_text':FieldArg("text", "Please wait...", jsonset=True),
                        'pre_line':FieldArg("boolean", True),
                        'messagediv_class':FieldArg("cssclass", ""),
                        'boxdiv_class':FieldArg("cssclass", ""),
                        'inner_class':FieldArg("cssclass", ""),
                        'inner_style':FieldArg("cssstyle", ""),
                        'xdiv_class':FieldArg("cssclass", ""),
                        'xdiv_style':FieldArg("cssstyle", ""),
                        'x_class':FieldArg("cssclass", ""),
                        'link_ident':FieldArg("url", 'no_javascript'),
                        'json_ident':FieldArg("url", ''),
                        'button_text':FieldArg("text", "Submit"),
                        'button_class':FieldArg("cssclass", ""),
                        'buttondiv_class':FieldArg("cssclass", ""),
                        'buttondiv_style':FieldArg("cssstyle", ""),
                        'get_field1':FieldArg("text", "", valdt=True),
                        'get_field2':FieldArg("text","", valdt=True),
                        'target':FieldArg("text", "_blank"),
                        'force_ident':FieldArg("boolean", False)
            }


    def __init__(self, name=None, brief='', **field_args):
        """
        hide: If True, sets display: none; on the message, can be set/unset via JSON file
              If False, sets display:block
        para_text: The text appearing in the paragraph
        pre_line: If True, sets style="white-space: pre-line;" into the paragraph which preserves
                  new line breaks
        messagediv_class: class of the div holding message
        boxdiv_class: class of the box holding paragraph and X button
        inner_class: The CSS class of the div holding the paragraph
        buttondiv_class: The class of the div holding the button
        """
        Widget.__init__(self, name=name, brief=brief, **field_args)
        self.tag_name = "div"
        # message div
        self[0] = tag.Part(tag_name="div")
        # boxdiv
        self[0][0] = tag.Part(tag_name="div")
        # div holding X button
        self[0][0][0] = tag.Part(tag_name="div")
        self[0][0][0][0] = tag.Part(tag_name="button")
        self[0][0][0][0][0] = tag.HTMLSymbol("&times;")
        # The location 0,0,1 is the inner div holding the text paragraph
        self[0][0][1] = tag.Part(tag_name="div")
        self[0][0][1][0] = tag.Part(tag_name="p")
        # do not set any linebreaks, leave that to pre-line
        self[0][0][1][0].linebreaks = False
        self[0][0][1][0][0] = ''
        # buttondiv and button
        self[1] = tag.Part(tag_name="div")
        self[1][0] = tag.Part(tag_name="a", attribs={"role":"button"})
        self._jsonurl = ''


    def _build(self, page, ident_list, environ, call_data, lang):
        "build the box"
        # link button
        if not self.wf.link_ident:
            # setting self._error replaces the entire tag
            self._error = "Warning: No link ident"
            return
        # set an id in the message box
        self.jlabels['messagebox_id'] = self[0].insert_id()
        if self.wf.messagediv_class:
            self[0].attribs["class"] = self.wf.messagediv_class
        # Hides message block hide if is True
        if self.wf.hide:
            self[0].set_hide()
        else:
            self[0].set_block()
        # boxdiv
        if self.wf.boxdiv_class:
            self[0][0].attribs["class"] = self.wf.boxdiv_class
        # buttondiv
        self[0][0][0].set_class_style(self.wf.xdiv_class, self.wf.xdiv_style)

        # x button
        if self.wf.x_class:
            self[0][0][0][0].attribs["class"] = self.wf.x_class
        # inner div
        self[0][0][1].set_class_style(self.wf.inner_class, self.wf.inner_style)

        # paragraph
        if self.wf.pre_line:
            self[0][0][1][0].attribs["style"] = "white-space: pre-line;"
        self[0][0][1][0][0] = self.wf.para_text
        # set buttondiv
        self[1].set_class_style(self.wf.buttondiv_class, self.wf.buttondiv_style)

        # set button class
        if self.wf.button_class:
            self[1][0].attribs["class"] = self.wf.button_class
        # get json url
        if self.wf.json_ident:
            self.jlabels['url'] = self.get_url(self.wf.json_ident)
        # get url and button text
        url = self.get_url(self.wf.link_ident)
        if not url:
            # setting self._error replaces the entire tag
            self._error = "Warning: Invalid link"
            return
        if self.wf.button_text:
            self[1][0][0] = self.wf.button_text
        else:
            self[1][0][0] = url
        # create a url for the href
        get_fields = {self.get_formname("get_field1"):self.wf.get_field1,
                      self.get_formname("get_field2"):self.wf.get_field2}
        self[1][0].attribs["href"] = self.make_get_url(page, url, get_fields, self.wf.force_ident)
        if self.wf.target:
            self[1][0].attribs["target"] = self.wf.target


    def _build_js(self, page, ident_list, environ, call_data, lang):
        """Sets a click event handler on the a button"""
        ident=self.get_id()
        return f"""  $("#{ident} a").click(function (e) {{
    SKIPOLE.widgets['{ident}'].eventfunc(e);
    }});
  $("#{ident} button").click(function (e) {{
    SKIPOLE.widgets['{ident}'].eventfunc(e);
    }});
"""


    @classmethod
    def description(cls):
        """Returns a text string to illustrate the widget"""
        return """
<div> <!-- with widget id and class widget_class -->
  <div> <!-- With messagediv_class -->
      <div> <!-- With boxdiv_class -->
        <div> <!-- with class set by xdiv_class and style by xdiv_style -->
          <button>
            <!-- With class set by x_class -->
            <!-- the button will show the &times; symbol -->
          </button>
        </div>
        <div> <!-- With class set by inner_class -->
          <p style = "white-space: pre-line;"> <!-- style set if pre_line is True -->
            <!-- para_text appears in this paragraph -->
          </p>
        </div>
      </div>
  </div>
  <div> <!-- with class set by buttondiv_class and style by buttondiv_style -->
    <a role="button" href="#">
      <!-- With class set by button_class, and the href link will be the url of the link_ident -->
      <!-- the button will show the button_text. -->
    </a>
  </div>
</div>"""


class ImageLink1(Widget):
    """A link to the page with the given ident, with three optional get fields.
       The displayed contents of the link is an image page given by img_ident"""

    # This class does not display any error messages
    display_errors = False

    arg_descriptions = {'link_ident':FieldArg("url", ''),
                        'img_ident':FieldArg("url", ''),
                        'hover_img_ident':FieldArg("url", ''),
                        'target':FieldArg("text", ""),
                        'width':FieldArg("text","100"),
                        'height':FieldArg("text","100"),
                        'align':FieldArg("text",""),
                        'get_field1':FieldArg("text","", valdt=True),
                        'get_field2':FieldArg("text","", valdt=True),
                        'get_field3':FieldArg("text","", valdt=True),
                        'force_ident':FieldArg("boolean",False)
                       }

    def __init__(self, name=None, brief='', **field_args):
        """
        link_ident: The target page link ident, label or url
        img_ident: The ident of the image page
        hover_img_ident: The ident of an image page shown when hovering over the link
        target: if given, the target attribute will be set
        width: The width of the image
        height: The height of the image
        get_field1: Optional 'get' string set in the target url
        get_field2: Optional second 'get' string set in the target url
        get_field3: Optional third 'get' string set in the target url
        force_ident: If True then the page ident will be included, even if no get fields set
                     If False, the page ident will only be included if a get field is set
        """
        Widget.__init__(self, name=name, brief=brief, **field_args)
        self.tag_name = "a"
        self[0] = tag.ClosedPart(tag_name="img")
        self._hover_img_url = ''
        self._img_url = ''

    def _build(self, page, ident_list, environ, call_data, lang):
        "Build the link"
        if self.get_field_value('width') and self.get_field_value('height'):
            self[0].attribs = {'width':self.get_field_value('width'), 'height':self.get_field_value('height')}
        elif self.get_field_value('width'):
            self[0].attribs = {'width':self.get_field_value('width')}
        elif self.get_field_value('height'):
            self[0].attribs = {'height':self.get_field_value('height')}
        if self.get_field_value('align'):
            self[0].update_attribs({'align':self.get_field_value('align')})
        if self.get_field_value("target"):
            self.update_attribs({"target":self.get_field_value("target")})
        if not self.get_field_value("link_ident"):
            self._error = "Warning: broken link"
            return
        url = self.get_url(self.get_field_value("link_ident"))
        if not url:
            self._error = "Warning: broken link"
            return
        justurl = url
        # create a url for the href
        get_fields = {self.get_formname("get_field1"):self.get_field_value("get_field1"),
                      self.get_formname("get_field2"):self.get_field_value("get_field2"),
                      self.get_formname("get_field3"):self.get_field_value("get_field3")}
        url = self.make_get_url(page, url, get_fields, self.get_field_value("force_ident"))
        self.update_attribs({"href": url})
        if not self.get_field_value("img_ident"):
            # if no image ident, place the link page url as content, without the get fields
            self[0] = justurl
            return
        img_url = self.get_url(self.get_field_value("img_ident"))
        if not img_url:
            self[0] = justurl
            return
        else:
            self._img_url = quote(img_url, safe='/:')
            self[0].update_attribs({"src": self._img_url})
        hover_img_url = self.get_url(self.get_field_value("hover_img_ident"))
        if hover_img_url:
            self._hover_img_url = quote(hover_img_url, safe='/:')


    def _build_js(self, page, ident_list, environ, call_data, lang):
        """Sets a hover event handler"""
        if (not self._img_url) or (not self._hover_img_url):
            return ''
        return """  $("#{ident}").hover(function (e) {{
    $("img", this).attr('src', '{hover_img_url}');
      }}, function (e) {{
    $("img", this).attr('src', '{img_url}');
      }});
""".format(ident = self.get_id(), hover_img_url = self._hover_img_url, img_url = self._img_url)

    @classmethod
    def description(cls):
        """Returns a text string to illustrate the widget"""
        return """
<a href="#">  <!-- with widget id and class widget_class and href the url -->
  <img src="#" />   <!-- with src set to url of img_ident -->
</a>"""



class Image1(ClosedWidget):
    """An image"""

    # This class does not display any error messages
    display_errors = False

    arg_descriptions = {'img_url':FieldArg("text", '', jsonset=True),
                        'width':FieldArg("text","100"),
                        'height':FieldArg("text","100"),
                        'alt':FieldArg("text","")
                       }

    def __init__(self, name=None, brief='', **field_args):
        """
        img_url: The src url string (not ident) of the image page
        width: The width of the image
        height: The height of the image
        alt: The alt attribute
        """
        ClosedWidget.__init__(self, name=name, brief=brief, **field_args)
        self.tag_name = "img"

    def _build(self, page, ident_list, environ, call_data, lang):
        "Build the link"
        if self.get_field_value('width'):
            self.update_attribs({'width':self.get_field_value('width')})
        if self.get_field_value('height'):
            self.update_attribs({'height':self.get_field_value('height')})
        if self.get_field_value('alt'):
            self.update_attribs({'alt':self.get_field_value('alt')})

        if not self.get_field_value("img_url"):
            self._error = "Warning: broken link"
        else:
            self.update_attribs({"src": quote(self.get_field_value("img_url"), safe='/:')})

    @classmethod
    def description(cls):
        """Returns a text string to illustrate the widget"""
        return """
<img src="#" />   <!-- with src set to img_url -->
"""


class LinkTextBlockTable1(Widget):
    "A table of links to a page, with link text, two get fields and a TextBlock"

    # This class does not display any error messages
    display_errors = False

    arg_descriptions = {'link_ident':FieldArg("url", ""),
                        'header_class':FieldArg("cssclass",""),
                        'even_class':FieldArg("cssclass", ""),
                        'odd_class':FieldArg("cssclass", ""),
                        'col1_link_title':FieldArg('text', ''),
                        'col2_text_title':FieldArg('text', ''),
                        'show_get_field1':FieldArg("boolean", True, valdt=True),
                        'show_get_field2':FieldArg("boolean", True, valdt=True),
                        'link_table':FieldArgTable(['text', 'text', 'text', 'textblock_ref', 'text', 'text']),               # coltypes
                        'force_ident':FieldArg("boolean", False)
                        }

    def __init__(self, name=None, brief='', **field_args):
        """
        link_ident: The target page link ident, url or label
        header_class: class of the header row, if empty string, then no class will be applied
        even_class: class of even rows, if empty string, then no class will be applied
        odd_class: class of odd rows, if empty string, then no class will be applied
        col1_link_title: The title of the first column, above the links
        col2_text_title: The title of the second colum, above the textblock
        show_get_field1: If True, enables the get field, the name of this variable is used as the field name
        show_get_field2: If True, enables the second get field, the name of this variable is used as the field name
        link_table: col 0 is the visible text to place in the link,
                    col 1 is the get field of the link
                    col 2 is the get field of the link
                    col 3 is the reference string of a textblock to appear in the column adjacent to the link
                    col 4 is text to appear if the reference cannot be found in the database
                    col 5 normally empty string, if set to text it will replace the textblock
        force_ident: If True then the page ident will be included, even if no get fields set
                     If False, the page ident will only be included if a get field is set
        """
        Widget.__init__(self, name=name, brief=brief, **field_args)
        self.tag_name = "table"


    def _build(self, page, ident_list, environ, call_data, lang):
        "Build the table"
        table = self.get_field_value("link_table")
        title1 = self.get_field_value("col1_link_title")
        title2 = self.get_field_value("col2_text_title")

        # set even row colour
        if self.get_field_value('even_class'):
            evenclass = self.get_field_value('even_class')
        else:
            evenclass = ''
        # set odd row colour
        if self.get_field_value('odd_class'):
            oddclass = self.get_field_value('odd_class')
        else:
            oddclass = ''
        # set header row colour
        if self.get_field_value('header_class'):
            headerclass = self.get_field_value('header_class')
        else:
            headerclass = ''

        for num, row in enumerate(table):
            if title1 or title2:
                rownumber = num+1
            else:
                rownumber = num
            if (not num) and (title1 or title2):
                if headerclass:
                    self[0]  = tag.Part(tag_name="tr", attribs={"class":headerclass})
                else:
                    self[0]  = tag.Part(tag_name="tr")
                if title1:
                    self[0][0] = tag.Part(tag_name="th", text=title1)
                else:
                    self[0][0] = tag.Part(tag_name="th")
                if title2:
                    self[0][1] = tag.Part(tag_name="th", text=title2)
                else:
                    self[0][1] = tag.Part(tag_name="th")
            if evenclass and (rownumber % 2):
                self[rownumber]  = tag.Part(tag_name="tr", attribs={"class":evenclass})
            elif oddclass and not (rownumber % 2):
                self[rownumber]  = tag.Part(tag_name="tr", attribs={"class":oddclass})
            else:
                self[rownumber]  = tag.Part(tag_name="tr")
            # each row has parameters 0 to 5
            self[rownumber][0] = tag.Part(tag_name="td")
            if row[0]:
                content = row[0]
            else:
                content = "?"
            self[rownumber][0][0]= Link(link_ident=self.get_field_value("link_ident"),
                                        get_field1=row[1],
                                        get_field2=row[2],
                                        content=content,
                                        force_ident=self.get_field_value("force_ident"))
            self[rownumber][0][0].set_name('get_field1', self.get_name("show_get_field1"))
            self[rownumber][0][0].set_name('get_field2', self.get_name("show_get_field2"))
            if not self.get_field_value("show_get_field1"):
                self[rownumber][0][0].set_field_value('get_field1','')
            if not self.get_field_value("show_get_field2"):
                self[rownumber][0][0].set_field_value('get_field2','')
            # second column
            self[rownumber][1] = tag.Part(tag_name="td")
            # Set the text column, row[3] is a textblock
            if row[5]:
                # override the textblock
                self[rownumber][1][0] = row[5]
                continue
            if (not row[3]) and row[4]:
                self[rownumber][1][0] = row[4]
                continue
            if row[3]:
                if row[4]:
                    row[3].failmessage = row[4]
                self[rownumber][1][0] = row[3]
            else: 
                self[rownumber][1][0] = ''

    @classmethod
    def description(cls):
        """Returns a text string to illustrate the widget"""
        return """
<table>  <!-- with widget id and class widget_class -->
  <tr> <!-- with class header_class -->
    <th> <!-- col1_link_title --> </th>   <th> <!-- col2_text_title --> </th>
  </tr>
  <tr> <!-- with class  odd_class -->
    <td> <!-- link and link text--> </td>   <td> <!-- textblock --> </td>
  </tr>
  <!-- rows repeated for each link, with odd and even row classes -->
</table>"""



class LinkTextBlockTable2(Widget):
    "A 3 column table of links to a page, with link text, two get fields, a text string and a TextBlock"

    # This class does not display any error messages
    display_errors = False

    arg_descriptions = {'link_ident':FieldArg("url", ""),
                        'header_class':FieldArg("cssclass",""),
                        'even_class':FieldArg("cssclass", ""),
                        'odd_class':FieldArg("cssclass", ""),
                        'col_link_title':FieldArg('text', ''),
                        'col_text_title':FieldArg('text', ''),
                        'col_textblock_title':FieldArg('text', ''),
                        'show_get_field1':FieldArg("boolean", True, valdt=True),
                        'show_get_field2':FieldArg("boolean", True, valdt=True),
                        'link_table':FieldArgTable(['text', 'text', 'text', 'text', 'textblock_ref', 'text', 'text']),
                        'force_ident':FieldArg("boolean", False)
                        }


    def __init__(self, name=None, brief='', **field_args):
        """
        link_ident: The target page link ident, url or label
        header_class: class of the header row, if empty string, then no class will be applied
        even_class: class of even rows, if empty string, then no class will be applied
        odd_class: class of odd rows, if empty string, then no class will be applied
        col_link_title: The title of the first column, above the links
        col_text_title: The title of the second colum, above the text
        col_textblock_title: The title of the second colum, above the textblock
        show_get_field1: If True, enables the get field, the name of this variable is used as the field name
        show_get_field2: If True, enables the second get field, the name of this variable is used as the field name
        link_table: col 0 is the visible text to place in the link,
                    col 1 is the get field of the link
                    col 2 is the get field of the link
                    col 3 is the text to appear in the second table column
                    col 4 is the reference string of a textblock to appear in the third table column
                    col 5 is text to appear if the reference cannot be found in the database
                    col 6 normally empty string, if set to text it will replace the textblock
        force_ident: If True then the page ident will be included, even if no get fields set
                     If False, the page ident will only be included if a get field is set
        """
        Widget.__init__(self, name=name, brief=brief, **field_args)
        self.tag_name = "table"
        self.update_attribs({"style":"border-spacing:0;border-collapse:collapse;"})


    def _build(self, page, ident_list, environ, call_data, lang):
        "Build the table"
        table = self.get_field_value("link_table")
        title1 = self.get_field_value("col_link_title")
        title2 = self.get_field_value("col_text_title")
        title3 = self.get_field_value("col_textblock_title")

        # set even row colour
        if self.get_field_value('even_class'):
            evenclass = self.get_field_value('even_class')
        else:
            evenclass = ''
        # set odd row colour
        if self.get_field_value('odd_class'):
            oddclass = self.get_field_value('odd_class')
        else:
            oddclass = ''
        # set header row colour
        if self.get_field_value('header_class'):
            headerclass = self.get_field_value('header_class')
        else:
            headerclass = ''

        for num, row in enumerate(table):
            if title1 or title2 or title3:
                rownumber = num+1
            else:
                rownumber = num
            if (not num) and (title1 or title2):
                if headerclass:
                    self[0]  = tag.Part(tag_name="tr", attribs={"class":headerclass})
                else:
                    self[0]  = tag.Part(tag_name="tr")
                if title1:
                    self[0][0] = tag.Part(tag_name="th", text=title1)
                else:
                    self[0][0] = tag.Part(tag_name="th")
                if title2:
                    self[0][1] = tag.Part(tag_name="th", text=title2)
                else:
                    self[0][1] = tag.Part(tag_name="th")
                if title3:
                    self[0][2] = tag.Part(tag_name="th", text=title3)
                else:
                    self[0][2] = tag.Part(tag_name="th")
            if evenclass and (rownumber % 2):
                self[rownumber]  = tag.Part(tag_name="tr", attribs={"class":evenclass})
            elif oddclass and not (rownumber % 2):
                self[rownumber]  = tag.Part(tag_name="tr", attribs={"class":oddclass})
            else:
                self[rownumber]  = tag.Part(tag_name="tr")
            # each row has parameters 0 to 6

            # first column, the link column
            self[rownumber][0] = tag.Part(tag_name="td")
            if row[0]:
                content = row[0]
            else:
                content = "?"
            self[rownumber][0][0]= Link(link_ident=self.get_field_value("link_ident"),
                                        get_field1=row[1],
                                        get_field2=row[2],
                                        content=content,
                                        force_ident=self.get_field_value("force_ident"))
            self[rownumber][0][0].set_name('get_field1', self.get_name("show_get_field1"))
            self[rownumber][0][0].set_name('get_field2', self.get_name("show_get_field2"))
            if not self.get_field_value("show_get_field1"):
                self[rownumber][0][0].set_field_value('get_field1','')
            if not self.get_field_value("show_get_field2"):
                self[rownumber][0][0].set_field_value('get_field2','')

            # second column, the text string column
            self[rownumber][1] = tag.Part(tag_name="td")
            self[rownumber][1][0] = row[3]

            # third column, the TextBlock column
            self[rownumber][2] = tag.Part(tag_name="td")
            # Set the text column, row[4] is a textblock
            if row[6]:
                # override the textblock
                self[rownumber][2][0] = row[6]
                continue
            if (not row[4]) and row[5]:
                self[rownumber][2][0] = row[5]
                continue
            if row[4]:
                if row[5]:
                    row[4].failmessage = row[5]
                self[rownumber][2][0] = row[4]
            else: 
                self[rownumber][2][0] = ''

    @classmethod
    def description(cls):
        """Returns a text string to illustrate the widget"""
        return """
<table>  <!-- with widget id and class widget_class -->
  <tr> <!-- with class header_class -->
    <th> <!-- col_link_title --> </th>   <th> <!-- col_text_title --> </th>   <th> <!-- col_textblock_title --> </th>
  </tr>
  <tr> <!-- with class  odd_class -->
    <td> <!-- link and link text--> </td>   <td> <!-- text string --> </td>  <td> <!-- textblock --> </td>
  </tr>
  <!-- rows repeated for each link, with odd and even row classes -->
</table>"""


class ListLinks(Widget):
    """A list of links, each with one get field"""

    # This class does not display any error messages
    display_errors = False

    arg_descriptions = {
                        'li_class':FieldArg("cssclass", ""),
                        'link_class':FieldArg("cssclass", ""),
                        'target':FieldArg("text", ""),
                        'force_ident':FieldArg("boolean", False),
                        'links':FieldArgTable(['text', 'url', 'text'], valdt=True)
                        }

    def __init__(self, name=None, brief='', **field_args):
        """
        li_class: class to set in each li element
        link_class: class to set in each a element
        target: if given, the target attribute will be set on each link
        force_ident: If True then the page ident will be included, even if no get field set
                     If False, the page ident will only be included if a get field is set
        links: col 0 is the text to place in link,
                     col 1 is the link ident, label or url
                     col 2 is the get field contents of the link, empty if not used
                     the name of this field is used as the widgfield of the get data returned
        """
        Widget.__init__(self, name=name, brief=brief, **field_args)
        self.tag_name = "ul"


    def _build(self, page, ident_list, environ, call_data, lang):
        "Build the list"
        fieldlist = self.get_field_value('links')
        li_class = self.get_field_value('li_class')
        link_class = self.get_field_value('link_class')
        target = self.get_field_value('target')
        force_ident = self.get_field_value('force_ident')
        # create rows
        for rownumber, row in enumerate(fieldlist):
            if li_class:
                self[rownumber] = tag.Part(tag_name="l")
            else:
                self[rownumber] = tag.Part(tag_name="li")
            self[rownumber][0] = Link(widget_class = link_class,
                                       link_ident = row[1],
                                       get_field1 = row[2],
                                       content = row[0],
                                       target = target,
                                       force_ident = force_ident   )
            self[rownumber][0].set_name('get_field1',  self.get_name('links'))


    @classmethod
    def description(cls):
        """Returns a text string to illustrate the widget"""
        return """
<ul>  <!-- with widget id and class widget_class -->
  <li> <!-- with class  given by li_class -->
    <a href="#">  <!-- with class link_class and href the url -->
    <!-- content or url if no content given -->
    </a>
  <li>
  <!-- rows repeated -->
</ul>"""



class Table1_Links(Widget):
    """A table of two columns, the first column being text, the second links
       The first row is two header titles
       Note : there is no error display"""

    # This class does not display any error messages
    display_errors = False

    arg_descriptions = {'header_class':FieldArg("cssclass",""),
                        'even_class':FieldArg("cssclass", ""),
                        'odd_class':FieldArg("cssclass", ""),
                        'link_class':FieldArg("cssclass", ""),
                        'link_style':FieldArg("cssstyle", ""),
                        'title1':FieldArg('text', ''),
                        'title2':FieldArg('text', ''),
                        'col1':FieldArgList('text', valdt=False),
                        'col2':FieldArgList('text', valdt=False),
                        'col2_links':FieldArgList('url', valdt=False),
                        'col2_getfields':FieldArgList('text', valdt=True),
                        'col1_class':FieldArg("cssclass",""),          # class applied to every td in the first column
                        'col2_class':FieldArg("cssclass",""),          # class applied to every td in the second column
                        'force_ident':FieldArg("boolean", False)
                        }

    def __init__(self, name=None, brief='', **field_args):
        """
        header_class: class of the header row, if empty string, then no class will be applied
        even_class: class of even rows, if empty string, then no class will be applied
        odd_class: class of odd rows, if empty string, then no class will be applied
        link_class: class of the a tags
        link_style: style of the a tags
        title1: The header title over the first text column
        title2: The header title over the second text column
        col1 : A list of text strings to place in the first column
        col2: A list of text strings to place in the second column, these will be the link text
        col2_links: A list of links for the second column
        col2_getfields: A list of get fields for the second column
        col1_class: class applied to every td in the first column
        col2_class: class applied to every td in the second column
        force_ident: If True then the page ident will be included, even if no get field set
                     If False, the page ident will only be included if a get field is set
        """
        Widget.__init__(self, name=name, brief=brief, **field_args)
        self.tag_name = "table"

    def _build(self, page, ident_list, environ, call_data, lang):
        "Build the table"
        col1 = self.get_field_value("col1")
        col2 = self.get_field_value("col2")
        col2_links = self.get_field_value("col2_links")
        col2_getfields = self.get_field_value("col2_getfields")
        # create rows, same length as col2_links
        rows = max( len(col1), len(col2), len(col2_links) )
        header = 0
        if self.get_field_value('title1') or self.get_field_value('title2'):
            header = 1
            if self.get_field_value('header_class'):
                self[0] = tag.Part(tag_name='tr', attribs={"class":self.get_field_value('header_class')})
            else:
                self[0] = tag.Part(tag_name='tr')
            self[0][0] = tag.Part(tag_name='th', text = self.get_field_value('title1'))
            self[0][1] = tag.Part(tag_name='th', text = self.get_field_value('title2'))
        # set even row colour
        if self.get_field_value('even_class'):
            even = self.get_field_value('even_class')
        else:
            even = ''
        # set odd row colour
        if self.get_field_value('odd_class'):
            odd = self.get_field_value('odd_class')
        else:
            odd = ''

        if len(col1) < rows:
            col1.extend(['']*(rows - len(col1)))    # pad col1 with ''
        if len(col2_links) < rows:
            col2_links.extend(['']*(rows - len(col2_links)))  # pad links with ''
        if len(col2_getfields) < rows:
            col2_getfields.extend(['']*(rows - len(col2_getfields)))  # pad getfields with ''
        if len(col2) < rows:
            col2.extend(['']*(rows - len(col2)))    # pad col2 with ''

        col1_class = self.get_field_value("col1_class")
        col2_class = self.get_field_value("col2_class")
        link_class = self.get_field_value("link_class")
        link_style = self.get_field_value("link_style")

        for index in range(rows):
            rownumber = index+header
            if even and (rownumber % 2) :
                self[rownumber] = tag.Part(tag_name="tr", attribs={"class":even})
            elif odd and not (rownumber % 2):
                self[rownumber] = tag.Part(tag_name='tr', attribs={"class":odd})
            else:
                self[rownumber] = tag.Part(tag_name='tr')
            if col1_class:
                self[rownumber][0] = tag.Part(tag_name='td', text = col1[index], attribs={"class":col1_class})
            else:
                self[rownumber][0] = tag.Part(tag_name='td', text = col1[index])
            if col2_class:
                self[rownumber][1] = tag.Part(tag_name='td', attribs={"class":col2_class})
            else:
                self[rownumber][1] = tag.Part(tag_name='td')

            if col2_links[index]:
                # self[rownumber][1][0] must now be set with the link
                if link_class and link_style:
                    attribs = {"class":link_class, "style":link_style}
                elif link_class:
                    attribs = {"class":link_class}
                elif link_style:
                    attribs = {"style":link_style}
                else:
                    attribs = None

                if attribs:
                    self[rownumber][1][0] = tag.Part(tag_name='a', attribs = attribs)
                else:
                    self[rownumber][1][0] = tag.Part(tag_name='a')

                url = self.get_url(col2_links[index])
                if url:
                    if col2[index]:
                        self[rownumber][1][0][0] = col2[index]
                    else:
                        self[rownumber][1][0][0] = url
                    # create a url for the href
                    if col2_getfields[index]:
                        get_fields = {self.get_formname("col2_getfields"):col2_getfields[index]}
                        url = self.make_get_url(page, url, get_fields, self.get_field_value("force_ident"))
                    else:
                        url = self.make_get_url(page, url, {}, self.get_field_value("force_ident"))
                    self[rownumber][1][0].update_attribs({"href": url})
                else:
                   self[rownumber][1][0] = "Warning: broken link"
            else:
                # self[rownumber][1][0] must now be set with text only
                self[rownumber][1][0] = col2[index]


    @classmethod
    def description(cls):
        """Returns a text string to illustrate the widget"""
        return """
<table>  <!-- with widget id and class widget_class -->
  <tr> <!-- with header class -->
    <th> <!-- title1 --> </th>
    <th> <!-- title2 --> </th>
  </tr>
  <tr> <!-- with class  from even or odd classes -->
    <td> <!-- with col1_class and col1 text string --> </td>
    <td> <!-- with col2_class -->
      <a href="#">
      <!-- With class set by link_class, and the href link will be from col2_links -->
      <!-- and get field from col2_getfields
      <!-- the link will show text from col2 -->
    </td>
  </tr>
  <!-- rows repeated -->
</table>"""


class Table2_Links(Widget):
    """A table of two columns, the first column being text, the second links
       with either html or json links
       with CSS class and style for each link
       The first row is two header titles
       Note : there is no error display"""

    # This class does not display any error messages
    display_errors = False

    arg_descriptions = {'header_class':FieldArg("cssclass",""),
                        'even_class':FieldArg("cssclass", ""),
                        'odd_class':FieldArg("cssclass", ""),
                        'link_classes':FieldArgList("cssclass", ""),
                        'link_styles':FieldArgList("cssstyle", ""),
                        'title1':FieldArg('text', ''),
                        'title2':FieldArg('text', ''),
                        'col1':FieldArgList('text', valdt=False),
                        'col2':FieldArgList('text', valdt=False),
                        'col2_link_idents':FieldArgList('url', valdt=False),
                        'col2_json_idents':FieldArgList('url', valdt=False),
                        'col2_getfields':FieldArgList('text', valdt=True),
                        'col1_class':FieldArg("cssclass",""),          # class applied to every td in the first column
                        'col2_class':FieldArg("cssclass",""),          # class applied to every td in the second column
                        'force_ident':FieldArg("boolean", False)
                        }

    def __init__(self, name=None, brief='', **field_args):
        """
        header_class: class of the header row, if empty string, then no class will be applied
        even_class: class of even rows, if empty string, then no class will be applied
        odd_class: class of odd rows, if empty string, then no class will be applied
        link_classes: list of classes of the a tags
        link_styles: list of styles of the a tags
        title1: The header title over the first text column
        title2: The header title over the second text column
        col1 : A list of text strings to place in the first column
        col2: A list of text strings to place in the second column, these will be the link text
        col2_link_idents: A list of links for the second column, called if the item in col2_json_idents is empty
                          If a link item is empty, the table cell will have text only
        col2_json_idents: A list of links for the second column, requests a json page to be returned
        col2_getfields: A list of get fields for the second column
        col1_class: class applied to every td in the first column
        col2_class: class applied to every td in the second column
        force_ident: If True then the page ident will be included, even if no get field set
                     If False, the page ident will only be included if a get field is set
        """
        Widget.__init__(self, name=name, brief=brief, **field_args)
        self.tag_name = "table"
        self._col2_json_idents = []

    def _build(self, page, ident_list, environ, call_data, lang):
        "Build the table"
        col1 = self.get_field_value("col1")
        col2 = self.get_field_value("col2")
        col2_link_idents = self.get_field_value("col2_link_idents")
        col2_json_idents = self.get_field_value("col2_json_idents")
        col2_getfields = self.get_field_value("col2_getfields")
        link_classes = self.get_field_value("link_classes")
        link_styles = self.get_field_value("link_styles")
        # create rows, same length as col2_link_idents
        rows = len(col2_link_idents)
        header = 0
        if self.get_field_value('title1') or self.get_field_value('title2'):
            header = 1
            # and add an empty json link to self._col2_json_idents
            self._col2_json_idents.append('')
            if self.get_field_value('header_class'):
                self[0] = tag.Part(tag_name='tr', attribs={"class":self.get_field_value('header_class')})
            else:
                self[0] = tag.Part(tag_name='tr')
            self[0][0] = tag.Part(tag_name='th', text = self.get_field_value('title1'))
            self[0][1] = tag.Part(tag_name='th', text = self.get_field_value('title2'))
        # set even row colour
        if self.get_field_value('even_class'):
            even = self.get_field_value('even_class')
        else:
            even = ''
        # set odd row colour
        if self.get_field_value('odd_class'):
            odd = self.get_field_value('odd_class')
        else:
            odd = ''

        if len(col1) < rows:
            col1.extend(['']*(rows - len(col1)))    # pad col1 with ''
        if len(col2_json_idents) < rows:
            col2_json_idents.extend(['']*(rows - len(col2_json_idents)))  # pad links with ''
        if len(col2_getfields) < rows:
            col2_getfields.extend(['']*(rows - len(col2_getfields)))  # pad getfields with ''
        if len(col2) < rows:
            col2.extend(['']*(rows - len(col2)))    # pad col2 with ''

        for item in col2_json_idents:
            if item:
                self._col2_json_idents.append( self.get_url(item) )
            else:
                self._col2_json_idents.append('')

        if len(link_classes) < rows:
            link_classes.extend(['']*(rows - len(link_classes)))    # pad link_classes with ''
        if len(link_styles) < rows:
            link_styles.extend(['']*(rows - len(link_styles)))    # pad link_styles with ''

        col1_class = self.get_field_value("col1_class")
        col2_class = self.get_field_value("col2_class")

        for index in range(rows):
            rownumber = index+header
            if even and (rownumber % 2) :
                self[rownumber] = tag.Part(tag_name="tr", attribs={"class":even})
            elif odd and not (rownumber % 2):
                self[rownumber] = tag.Part(tag_name='tr', attribs={"class":odd})
            else:
                self[rownumber] = tag.Part(tag_name='tr')
            if col1_class:
                self[rownumber][0] = tag.Part(tag_name='td', text = col1[index], attribs={"class":col1_class})
            else:
                self[rownumber][0] = tag.Part(tag_name='td', text = col1[index])
            if col2_class:
                self[rownumber][1] = tag.Part(tag_name='td', attribs={"class":col2_class})
            else:
                self[rownumber][1] = tag.Part(tag_name='td')

            if col2_link_idents[index]:
                # self[rownumber][1][0] must now be set with the link
                if link_classes[index] and link_styles[index]:
                    attribs = {"class":link_classes[index], "style":link_styles[index]}
                elif link_classes[index]:
                    attribs = {"class":link_classes[index]}
                elif link_styles[index]:
                    attribs = {"style":link_styles[index]}
                else:
                    attribs = None

                if attribs:
                    self[rownumber][1][0] = tag.Part(tag_name='a', attribs = attribs)
                else:
                    self[rownumber][1][0] = tag.Part(tag_name='a')

                url = self.get_url(col2_link_idents[index])
                if url:
                    if col2[index]:
                        self[rownumber][1][0][0] = col2[index]
                    else:
                        self[rownumber][1][0][0] = url
                    # create a url for the href
                    if col2_getfields[index]:
                        get_fields = {self.get_formname("col2_getfields"):col2_getfields[index]}
                        url = self.make_get_url(page, url, get_fields, self.get_field_value("force_ident"))
                    else:
                        url = self.make_get_url(page, url, {}, self.get_field_value("force_ident"))
                    self[rownumber][1][0].update_attribs({"href": url})
                else:
                   self[rownumber][1][0] = "Warning: broken link"
            else:
                # self[rownumber][1][0] must now be set with text only
                if col2[index]:
                    self[rownumber][1][0] = col2[index]


    def _build_js(self, page, ident_list, environ, call_data, lang):
        """Sets a click event handler"""
        jscript = """  $("#{ident} a").click(function (e) {{
    SKIPOLE.widgets['{ident}'].eventfunc(e);
    }});
""".format(ident = self.get_id())
        return jscript + self._make_fieldvalues(jurls=self._col2_json_idents)




    @classmethod
    def description(cls):
        """Returns a text string to illustrate the widget"""
        return """
<table>  <!-- with widget id and class widget_class -->
  <tr> <!-- with header class -->
    <th> <!-- title1 --> </th>
    <th> <!-- title2 --> </th>
  </tr>
  <tr> <!-- with class  from even or odd classes -->
    <td> <!-- with col1_class and col1 text string --> </td>
    <td> <!-- with col2_class -->
      <a href="#">
      <!-- With class set by item in link_classes, and the href link will be from col2_links -->
      <!-- and get field from col2_getfields
      <!-- the link will show text from col2 -->
    </td>
  </tr>
  <!-- rows repeated -->
</table>"""



class Table1_Button(Widget):
    """A table of a single text column, followed by a button link column
       There is a header and title over the text column,
       the button link can have one get field"""

    # This class does not display any error messages
    display_errors = False

    arg_descriptions = {
                        'header_class':FieldArg("cssclass",""),
                        'even_class':FieldArg("cssclass", ""),
                        'odd_class':FieldArg("cssclass", ""),
                        'maximize_text_col':FieldArg('boolean',True),
                        'hide':FieldArg("boolean", False, jsonset=True),
                        'title1':FieldArg('text', ''),
                        'button_class':FieldArg("cssclass", ""),
                        'button_text':FieldArg('text', ''),
                        'link_ident':FieldArg("url", 'no_javascript'),
                        'json_ident':FieldArg("url", ''),
                        'contents':FieldArgTable(['text', 'text'], valdt=True)
                        }

    def __init__(self, name=None, brief='', **field_args):
        """
        header_class: class of the header row
        even_class: class of even rows, if empty string, then no class will be applied
        odd_class: class of odd rows, if empty string, then no class will be applied
        maximize_text_col: If True the text column is made large, with the button columns reduced to the size of the buttons
        hide: if True, table will be hidden
        title1: The header title over the text column
        button_class: The CSS class to apply to the buttons
        button_text: Text on the link button
        link_ident: The target page link ident, label or url, if javascript not available
        json_ident: The url, ident or label to link, expecting a json file to be returned
        contents: col 0 is the text string to place in the first column,
                  col 1 is the get field contents of the button link
                  This fieldname used as the widgfield
        """
        Widget.__init__(self, name=name, brief=brief, **field_args)
        self.tag_name = "table"
        self._jsonurl =''

    def _build(self, page, ident_list, environ, call_data, lang):
        "Build the table"
        # Hides widget if no error and hide is True
        self.widget_hide(self.get_field_value("hide"))
        fieldtable = self.get_field_value("contents")
        header = 0
        if self.get_field_value('title1'):
            header = 1
            if self.get_field_value('header_class'):
                self[0] = tag.Part(tag_name='tr', attribs={"class":self.get_field_value('header_class')})
            else:
                self[0] = tag.Part(tag_name='tr')
            if self.get_field_value('maximize_text_col'):
                self[0][0] = tag.Part(tag_name='th', text = self.get_field_value('title1'), attribs={"style":"width : 100%;"})
            else:
                self[0][0] = tag.Part(tag_name='th', text = self.get_field_value('title1'))
            self[0][1] = tag.Part(tag_name='th')
        # set even row colour
        if self.get_field_value('even_class'):
            even = self.get_field_value('even_class')
        else:
            even = ''
        # set odd row colour
        if self.get_field_value('odd_class'):
            odd = self.get_field_value('odd_class')
        else:
            odd = ''
        if self.get_field_value("json_ident"):
            self._jsonurl = self.get_url(self.get_field_value("json_ident"))
        # create rows
        for index, row in enumerate(fieldtable):
            rownumber = index+header
            if even and (rownumber % 2) :
                self[rownumber] = tag.Part(tag_name="tr", attribs={"class":even})
            elif odd and not (rownumber % 2):
                self[rownumber] = tag.Part(tag_name='tr', attribs={"class":odd})
            else:
                self[rownumber] = tag.Part(tag_name='tr')
            # first column is text
            if self.get_field_value('maximize_text_col'):
                self[rownumber][0] = tag.Part(tag_name='td', text = row[0], attribs={"style":"width : 100%;"})
            else:
                self[rownumber][0] = tag.Part(tag_name='td', text = row[0])
            # Next column is a button link
            self[rownumber][1] = tag.Part(tag_name='td')
            if self.get_field_value('button_class'):
                self[rownumber][1][0] = tag.Part(tag_name='a', attribs = {"role":"button", "class":self.get_field_value('button_class')})
            else:
                self[rownumber][1][0] = tag.Part(tag_name='a', attribs = {"role":"button"})
            self[rownumber][1][0].htmlescaped=False
            if self.get_field_value("link_ident"):
                url = self.get_url(self.get_field_value("link_ident"))
                if url:
                    if self.get_field_value("button_text"):
                        self[rownumber][1][0][0] = self.get_field_value("button_text")
                    else:
                        self[rownumber][1][0][0] = url
                    # create a url for the href
                    get_fields = {self.get_formname("contents"):row[1]}
                    url = self.make_get_url(page, url, get_fields, True)
                    self[rownumber][1][0].update_attribs({"href": url})
                else:
                   self[rownumber][1][0] = "Warning: broken link"
            else:
                self[rownumber][1][0] = "Warning: broken link"


    def _build_js(self, page, ident_list, environ, call_data, lang):
        """Sets a click event handler"""
        if not self._jsonurl:
            return
        jscript = """  $("#{ident} a").click(function (e) {{
    SKIPOLE.widgets['{ident}'].eventfunc(e);
    }});
""".format(ident = self.get_id())
        return jscript + self._make_fieldvalues( url=self._jsonurl)

    @classmethod
    def description(cls):
        """Returns a text string to illustrate the widget"""
        return """
<table>  <!-- with widget id and class widget_class -->
                   <!-- and attribute style=display:none if hide is True -->
  <tr> <!-- with header class -->
    <th> <!-- title1 --> </th>
    <th></th>
  </tr>
  <tr> <!-- with class from even or odd classes -->
    <td> <!-- text string --> </td>
    <td>
      <a role="button" href="#">
      <!-- With class set by button_class, and the href link will be the url of the link_ident with get field -->
      <!-- the button will show the button_text  (not html escaped) -->
      </a>
    </td>
  </tr>
  <!-- rows repeated -->
</table>"""


class Table2_Button(Widget):
    """A table of a two text columns, followed by a button link
       There is a header and titles over the two text columns,
       the button link can have one get field"""

    # This class does not display any error messages
    display_errors = False

    arg_descriptions = {
                        'header_class':FieldArg("cssclass",""),
                        'even_class':FieldArg("cssclass", ""),
                        'odd_class':FieldArg("cssclass", ""),
                        'hide':FieldArg("boolean", False, jsonset=True),
                        'title1':FieldArg('text', ''),
                        'title2':FieldArg('text', ''),
                        'button_class':FieldArg("cssclass", ""),
                        'button_text':FieldArg('text', ''),
                        'link_ident':FieldArg("url", 'no_javascript'),
                        'json_ident':FieldArg("url", ''),
                        'contents':FieldArgTable(['text', 'text', 'text'], valdt=True)
                        }

    def __init__(self, name=None, brief='', **field_args):
        """
        header_class: class of the header row
        even_class: class of even rows, if empty string, then no class will be applied
        odd_class: class of odd rows, if empty string, then no class will be applied
        hide: if True, table will be hidden
        title1: The header title over the first text column
        title2: The header title over the second text column
        button_class: The CSS class to apply to the buttons
        button_text: Text on the link button
        link_ident: The target page link ident, label or url, if javascript not available
        json_ident: The url, ident or label to link, expecting a json file to be returned
        contents: col 0 and 1 are the text strings to place in the first two columns,
                  col 2 is the get field contents of the button link
                  This fieldname used as the widgfield
        """
        Widget.__init__(self, name=name, brief=brief, **field_args)
        self.tag_name = "table"
        self._jsonurl =''


    def _build(self, page, ident_list, environ, call_data, lang):
        "Build the table"
        # Hides widget if no error and hide is True
        self.widget_hide(self.get_field_value("hide"))
        fieldtable = self.get_field_value("contents")
        header = 0
        if self.get_field_value('title1') or self.get_field_value('title2'):
            header = 1
            if self.get_field_value('header_class'):
                self[0] = tag.Part(tag_name='tr', attribs={"class":self.get_field_value('header_class')})
            else:
                self[0] = tag.Part(tag_name='tr')
            self[0][0] = tag.Part(tag_name='th', text = self.get_field_value('title1'))
            self[0][1] = tag.Part(tag_name='th', text = self.get_field_value('title2'))
            self[0][2] = tag.Part(tag_name='th')
        # set even row colour
        if self.get_field_value('even_class'):
            even = self.get_field_value('even_class')
        else:
            even = ''
        # set odd row colour
        if self.get_field_value('odd_class'):
            odd = self.get_field_value('odd_class')
        else:
            odd = ''
        if self.get_field_value("json_ident"):
            self._jsonurl = self.get_url(self.get_field_value("json_ident"))
        # create rows
        for index, row in enumerate(fieldtable):
            rownumber = index+header
            if even and (rownumber % 2) :
                self[rownumber] = tag.Part(tag_name="tr", attribs={"class":even})
            elif odd and not (rownumber % 2):
                self[rownumber] = tag.Part(tag_name='tr', attribs={"class":odd})
            else:
                self[rownumber] = tag.Part(tag_name='tr')
            # first two columns are text
            self[rownumber][0] = tag.Part(tag_name='td', text = row[0])
            self[rownumber][1] = tag.Part(tag_name='td', text = row[1])
            # Next column is a button link
            self[rownumber][2] = tag.Part(tag_name='td', attribs={"style":"width : 1%;"})
            if self.get_field_value('button_class'):
                self[rownumber][2][0] = tag.Part(tag_name='a', attribs = {"role":"button", "class":self.get_field_value('button_class')})
            else:
                self[rownumber][2][0] = tag.Part(tag_name='a', attribs = {"role":"button"})
            self[rownumber][2][0].htmlescaped=False
            if self.get_field_value("link_ident"):
                url = self.get_url(self.get_field_value("link_ident"))
                if url:
                    if self.get_field_value("button_text"):
                        self[rownumber][2][0][0] = self.get_field_value("button_text")
                    else:
                        self[rownumber][2][0][0] = url
                    # create a url for the href
                    get_fields = {self.get_formname("contents"):row[2]}
                    url = self.make_get_url(page, url, get_fields, True)
                    self[rownumber][2][0].update_attribs({"href": url})
                else:
                   self[rownumber][2][0] = "Warning: broken link"
            else:
                self[rownumber][2][0] = "Warning: broken link"

    def _build_js(self, page, ident_list, environ, call_data, lang):
        """Sets a click event handler"""
        if not self._jsonurl:
            return
        jscript = """  $("#{ident} a").click(function (e) {{
    SKIPOLE.widgets['{ident}'].eventfunc(e);
    }});
""".format(ident = self.get_id())
        return jscript + self._make_fieldvalues( url=self._jsonurl)


    @classmethod
    def description(cls):
        """Returns a text string to illustrate the widget"""
        return """
<table>  <!-- with widget id and class widget_class -->
                   <!-- and attribute style=display:none if hide is True -->
  <tr> <!-- with header class -->
    <th> <!-- title 1 --> </th>
    <th> <!-- title 2 --> </th>
    <th></th>
  </tr>
  <tr> <!-- with class  from even or odd classes -->
    <td> <!-- text string --> </td>
    <td> <!-- text string --> </td>
    <td>
      <a role="button" href="#">
      <!-- With class set by button_class, and the href link will be the url of the link_ident with get field -->
      <!-- the button will show the button_text  (not html escaped) -->
      </a>
    </td>
  </tr>
  <!-- rows repeated -->
</table>"""



class Table3_Buttons2(Widget):
    """A table of three text columns, followed by two button link columns
       The first row is three headers - over the three text columns"""

    # This class does not display any error messages
    display_errors = False

    arg_descriptions = {'header_class':FieldArg("cssclass",""),
                        'even_class':FieldArg("cssclass", ""),
                        'odd_class':FieldArg("cssclass", ""),
                        'title1':FieldArg('text', ''),
                        'title2':FieldArg('text', ''),
                        'title3':FieldArg('text', ''),
                        'button_class':FieldArg("cssclass", ""),
                        'link_ident1':FieldArg("url",''),
                        'json_ident1':FieldArg("url", ''),
                        'button_text1':FieldArg('text', ''),
                        'button_wait_text1':FieldArg("text", ''),
                        'get_field1_1':FieldArg('boolean',True, valdt=True),
                        'get_field1_2':FieldArg('boolean',True, valdt=True),
                        'link_ident2':FieldArg("url",''),
                        'json_ident2':FieldArg("url", ''),
                        'button_text2':FieldArg('text', ''),
                        'button_wait_text2':FieldArg("text", ''),
                        'get_field2_1':FieldArg("boolean", True, valdt=True),
                        'get_field2_2':FieldArg("boolean",True, valdt=True),
                        'contents':FieldArgTable(['text', 'text', 'text', 'text', 'text', 'text', 'text', "boolean", "boolean"])
                        }

    def __init__(self, name=None, brief='', **field_args):
        """
        header_class: class of the header row, if empty string, then no class will be applied
        even_class: class of even rows, if empty string, then no class will be applied
        odd_class: class of odd rows, if empty string, then no class will be applied
        title1: The header title over the first text column
        title2: The header title over the second text column
        title3: The header title over the third text column
        button_class: The CSS class to apply to the buttons
        link_ident1: The target page link ident of the first link, if json_ident1 not present or no javascript
        json_ident1: The target JSON page link ident of the first link
        button_text1: Text on the first link button
        button_wait_text1: A 'please wait' message shown on button1
        link_ident2: The target page link ident of the second link, if json_ident2 not present or no javascript
        json_ident2: The target JSON page link ident of the second link
        button_text2: Text on the second link button
        button_wait_text2: A 'please wait' message shown on button2
        get_field1_1: The field name is the name (not value) of the get field 1 of the first link, value is bool: True, if get field exists, False if not 
        get_field1_2: The field name is the name (not value) of the get field 2 of the first link, value is bool: True, if get field exists, False if not
        get_field2_1: The field name is the name (not value) of the get field 1 of the second link, value is bool: True, if get field exists, False if not
        get_field2_2: The field name is the name (not value) of the get field 2 of the second link, value is bool: True, if get field exists, False if not
        contents: col 0, 1 and 2 is the text to place in the first three columns,
                    col 3, 4 is the two get field contents of the first link
                    col 5, 6 is the two get field contents of the second link
                    col 7 - True if the first button and link is to be shown, False if not
                    col 8 - True if the second button and link is to be shown, False if not
        """
        Widget.__init__(self, name=name, brief=brief, **field_args)
        self.tag_name = "table"
        self._url1 = ''
        self._jsonurl1 = ''
        self._url2 = ''
        self._jsonurl2 = ''


    def _build(self, page, ident_list, environ, call_data, lang):
        "Build the table"
        if self.get_field_value("json_ident1"):
            self._jsonurl1 = self.get_url(self.get_field_value("json_ident1"))
        if self.get_field_value("json_ident2"):
            self._jsonurl2 = self.get_url(self.get_field_value("json_ident2"))
        if self.get_field_value("link_ident1"):
            self._url1 = self.get_url(self.get_field_value("link_ident1"))
        if self.get_field_value("link_ident2"):
            self._url2 = self.get_url(self.get_field_value("link_ident2"))
        fieldtable = self.get_field_value("contents")
        header = 0
        if self.get_field_value('title1') or self.get_field_value('title2') or self.get_field_value('title3'):
            header = 1
            if self.get_field_value('header_class'):
                self[0] = tag.Part(tag_name='tr', attribs={"class":self.get_field_value('header_class')})
            else:
                self[0] = tag.Part(tag_name='tr')
            self[0][0] = tag.Part(tag_name='th', text = self.get_field_value('title1'))
            self[0][1] = tag.Part(tag_name='th', text = self.get_field_value('title2'))
            self[0][2] = tag.Part(tag_name='th', text = self.get_field_value('title3'))
            self[0][3] = tag.Part(tag_name='th')
            self[0][4] = tag.Part(tag_name='th')
        # set even row colour
        if self.get_field_value('even_class'):
            even = self.get_field_value('even_class')
        else:
            even = ''
        # set odd row colour
        if self.get_field_value('odd_class'):
            odd = self.get_field_value('odd_class')
        else:
            odd = ''
        # create rows
        for index, row in enumerate(fieldtable):
            rownumber = index+header
            if even and (rownumber % 2) :
                self[rownumber] = tag.Part(tag_name="tr", attribs={"class":even})
            elif odd and not (rownumber % 2):
                self[rownumber] = tag.Part(tag_name='tr', attribs={"class":odd})
            else:
                self[rownumber] = tag.Part(tag_name='tr')
            # first three columns are text
            self[rownumber][0] = tag.Part(tag_name='td', text = row[0])
            self[rownumber][1] = tag.Part(tag_name='td', text = row[1])
            self[rownumber][2] = tag.Part(tag_name='td', text = row[2])

            # Next two columns are button links

            self[rownumber][3] = tag.Part(tag_name='td')
            if row[7]:
                # reduce button column to minimum size
                self[rownumber][3].attribs={"style":"width : 1%;"}
                g1 = row[3] if self.get_field_value('get_field1_1') else ''
                g2 = row[4] if self.get_field_value('get_field1_2') else ''
                if self.get_field_value('button_class'):
                    self[rownumber][3][0] = tag.Part(tag_name='a', attribs = {"role":"button", "class":self.get_field_value('button_class')})
                else:
                    self[rownumber][3][0] = tag.Part(tag_name='a', attribs = {"role":"button"})
                self[rownumber][3][0].htmlescaped=False
                if self._url1:
                    if self.get_field_value("button_text1"):
                        self[rownumber][3][0][0] = self.get_field_value("button_text1")
                    else:
                        self[rownumber][3][0][0] = self._url1
                    # create a url for the href
                    get_fields = {self.get_formname("get_field1_1"):g1,
                                                 self.get_formname("get_field1_2"):g2}
                    url = self.make_get_url(page, self._url1, get_fields, True)
                    self[rownumber][3][0].update_attribs({"href": url})
                else:
                    self[rownumber][3][0] = "Warning: broken link"

            self[rownumber][4] = tag.Part(tag_name='td')
            if row[8]:
                # reduce button column to minimum size
                self[rownumber][4].attribs={"style":"width : 1%;"}
                g3 = row[5] if self.get_field_value('get_field2_1') else ''
                g4 = row[6] if self.get_field_value('get_field2_2') else ''
                if self.get_field_value('button_class'):
                    self[rownumber][4][0] = tag.Part(tag_name='a', attribs = {"role":"button", "class":self.get_field_value('button_class')})
                else:
                    self[rownumber][4][0] = tag.Part(tag_name='a', attribs = {"role":"button"})
                self[rownumber][4][0].htmlescaped=False
                if self._url2:
                    if self.get_field_value("button_text2"):
                        self[rownumber][4][0][0] = self.get_field_value("button_text2")
                    else:
                        self[rownumber][4][0][0] = self._url2
                    # create a url for the href
                    get_fields = {self.get_formname("get_field2_1"):g3,
                                                 self.get_formname("get_field2_2"):g4}
                    url = self.make_get_url(page, self._url2, get_fields, True)
                    self[rownumber][4][0].update_attribs({"href": url})
                else:
                    self[rownumber][4][0] = "Warning: broken link"

    def _build_js(self, page, ident_list, environ, call_data, lang):
        """Sets a click event handler"""
        jscript = """  $("#{ident} a").click(function (e) {{
    SKIPOLE.widgets['{ident}'].eventfunc(e);
    }});
""".format(ident = self.get_id())
        return jscript + self._make_fieldvalues('button_wait_text1', 'button_wait_text2', url1=self._jsonurl1, url2=self._jsonurl2)


    @classmethod
    def description(cls):
        """Returns a text string to illustrate the widget"""
        return """
<table>  <!-- with widget id and class widget_class -->
  <tr> <!-- with header class -->
    <th> <!-- title 1 --> </th>
    <th> <!-- title 2 --> </th>
    <th> <!-- title 3 --> </th>
    <th></th>
    <th></th>
  </tr>
  <tr> <!-- with class  from even or odd classes -->
    <td> <!-- text string --> </td>
    <td> <!-- text string --> </td>
    <td> <!-- text string --> </td>
    <td>
      <a role="button" href="#">
      <!-- With class set by button_class, and the href link will be the url of the link_ident1 with the two get_fields -->
      <!-- the button will show the button_text1  (not html escaped) -->
      </a>
    </td>
    <td>
      <a role="button" href="#">
      <!-- With class set by button_class, and the href link will be the url of the link_ident2 with the two get_fields -->
      <!-- the button will show the button_text2  (not html escaped) -->
      </a>
    </td>
  </tr>
  <!-- rows repeated -->
</table>"""


class Table1_Buttons4(Widget):
    """A table of a single text column, followed by four button links
       There is no header row or column titles, each button link can have one get field"""

    # This class does not display any error messages
    display_errors = False

    arg_descriptions = {'even_class':FieldArg("cssclass", ""),
                        'odd_class':FieldArg("cssclass", ""),
                        'maximize_text_col':FieldArg('boolean',True),
                        'button_class':FieldArg("cssclass", ""),
                        'button_text1':FieldArg('text', ''),
                        'link_ident1':FieldArg("url", ''),
                        'btn_col1':FieldArg("boolean", True, valdt=True),
                        'button_text2':FieldArg('text', ''),
                        'link_ident2':FieldArg("url", ''),
                        'btn_col2':FieldArg("boolean", True, valdt=True),
                        'button_text3':FieldArg('text', ''),
                        'link_ident3':FieldArg("url", ''),
                        'btn_col3':FieldArg("boolean", True, valdt=True),
                        'button_text4':FieldArg('text', ''),
                        'link_ident4':FieldArg("url", ''),
                        'btn_col4':FieldArg("boolean", True, valdt=True),
                        'contents':FieldArgTable(['text', 'text', 'text', 'text', 'text', 'boolean', 'boolean', "boolean", "boolean"]),
                        'col0_classes':FieldArgList('cssclass')
                        }

    def __init__(self, name=None, brief='', **field_args):
        """
        even_class: class of even rows, if empty string, then no class will be applied
        odd_class: class of odd rows, if empty string, then no class will be applied
        maximize_text_col: If True the text column is made large, with the button columns reduced to the size of the buttons
        button_class: The CSS class to apply to the buttons
        button_text1: Text on the first link button
        button_text2: Text on the second link button
        button_text3: Text on the third link button
        button_text4: Text on the fourth link button
        link_ident1: The target page link ident of the first link
        link_ident2: The target page link ident of the second link
        link_ident3: The target page link ident of the third link
        link_ident4: The target page link ident of the fourth link
        btn_col1: The field name is the name (not value) of the get field of the first link, value is bool: True, if column exists, False if not 
        btn_col2: The field name is the name (not value) of the get field of the second link, value is bool: True, if column exists, False if not
        btn_col3: The field name is the name (not value) of the get field of the third link, value is bool: True, if column exists, False if not
        btn_col4: The field name is the name (not value) of the get field of the fourth link, value is bool: True, if column exists, False if not
        contents: col 0 is the text to place in the first column,
                    col 1, 2, 3, 4 are the get field contents of links 1,2,3 and 4
                    col 5 - True if the first button and link is to be shown, False if not
                    col 6 - True if the second button and link is to be shown, False if not
                    col 7 - True if the third button and link is to be shown, False if not
                    col 8 - True if the fourth button and link is to be shown, False if not
        col0_classes: if given is a list of CSS classes to apply to each td of the text column
        """
        Widget.__init__(self, name=name, brief=brief, **field_args)
        self.tag_name = "table"


    def _build(self, page, ident_list, environ, call_data, lang):
        "Build the table"
        fieldtable = self.get_field_value("contents")
        col0_classes = self.get_field_value("col0_classes")
        # set even row colour
        if self.get_field_value('even_class'):
            even = self.get_field_value('even_class')
        else:
            even = ''
        # set odd row colour
        if self.get_field_value('odd_class'):
            odd = self.get_field_value('odd_class')
        else:
            odd = ''
        # create rows
        for rownumber, row in enumerate(fieldtable):
            if even and (rownumber % 2) :
                self[rownumber] = tag.Part(tag_name="tr", attribs={"class":even})
            elif odd and not (rownumber % 2):
                self[rownumber] = tag.Part(tag_name='tr', attribs={"class":odd})
            else:
                self[rownumber] = tag.Part(tag_name='tr')
            # first column is text, set css class and style
            try:
                css_class = col0_classes[rownumber]
            except IndexError:
                css_class = ''
            if css_class:
                if self.get_field_value('maximize_text_col'):
                    self[rownumber][0] = tag.Part(tag_name='td', text = row[0], attribs={"class":css_class, "style":"width : 100%;"})
                else:
                    self[rownumber][0] = tag.Part(tag_name='td', text = row[0], attribs={"class":css_class})
            else:
                if self.get_field_value('maximize_text_col'):
                    self[rownumber][0] = tag.Part(tag_name='td', text = row[0], attribs={"style":"width : 100%;"})
                else:
                    self[rownumber][0] = tag.Part(tag_name='td', text = row[0])
            # Next four columns are button links
            if self.get_field_value('btn_col1'):
                btn_col1 = tag.Part(tag_name='td')
                if row[5]:
                    g1 = row[1] if row[1] else ''
                    if self.get_field_value('button_class'):
                        btn_col1[0] = tag.Part(tag_name='a', attribs = {"role":"button", "class":self.get_field_value('button_class')})
                    else:
                        btn_col1[0] = tag.Part(tag_name='a', attribs = {"role":"button"})
                    btn_col1[0].htmlescaped=False
                    if self.get_field_value("link_ident1"):
                        url = self.get_url(self.get_field_value("link_ident1"))
                        if url:
                            if self.get_field_value("button_text1"):
                                btn_col1[0][0] = self.get_field_value("button_text1")
                            else:
                                btn_col1[0][0] = url
                            # create a url for the href
                            url = self.make_get_url(page, url, {self.get_formname("btn_col1"):g1}, True)
                            btn_col1[0].update_attribs({"href": url})
                        else:
                           btn_col1[0] = "Warning: broken link"
                    else:
                        btn_col1[0] = "Warning: broken link"
                self[rownumber].append(btn_col1)
            if self.get_field_value('btn_col2'):
                btn_col2 = tag.Part(tag_name='td')
                if row[6]:
                    g2 = row[2] if row[2] else ''
                    if self.get_field_value('button_class'):
                        btn_col2[0] = tag.Part(tag_name='a', attribs = {"role":"button", "class":self.get_field_value('button_class')})
                    else:
                        btn_col2[0] = tag.Part(tag_name='a', attribs = {"role":"button"})
                    btn_col2[0].htmlescaped=False
                    if self.get_field_value("link_ident2"):
                        url = self.get_url(self.get_field_value("link_ident2"))
                        if url:
                            if self.get_field_value("button_text2"):
                                btn_col2[0][0] = self.get_field_value("button_text2")
                            else:
                                btn_col2[0][0] = url
                            # create a url for the href
                            url = self.make_get_url(page, url, {self.get_formname("btn_col2"):g2}, True)
                            btn_col2[0].update_attribs({"href": url})
                        else:
                            btn_col2[0] = "Warning: broken link"
                    else:
                        btn_col2[0] = "Warning: broken link"
                self[rownumber].append(btn_col2)
            if self.get_field_value('btn_col3'):
                btn_col3 = tag.Part(tag_name='td')
                if row[7]:
                    g3 = row[3] if row[3] else ''
                    if self.get_field_value('button_class'):
                        btn_col3[0] = tag.Part(tag_name='a', attribs = {"role":"button", "class":self.get_field_value('button_class')})
                    else:
                        btn_col3[0] = tag.Part(tag_name='a', attribs = {"role":"button"})
                    btn_col3[0].htmlescaped=False
                    if self.get_field_value("link_ident3"):
                        url = self.get_url(self.get_field_value("link_ident3"))
                        if url:
                            if self.get_field_value("button_text3"):
                                btn_col3[0][0] = self.get_field_value("button_text3")
                            else:
                                btn_col3[0][0] = url
                            # create a url for the href
                            url = self.make_get_url(page, url, {self.get_formname("btn_col3"):g3}, True)
                            btn_col3[0].update_attribs({"href": url})
                        else:
                           btn_col3[0] = "Warning: broken link"
                    else:
                        btn_col3[0] = "Warning: broken link"
                self[rownumber].append(btn_col3)
            if self.get_field_value('btn_col4'):
                btn_col4 = tag.Part(tag_name='td')
                if row[8]:
                    g4 = row[4] if row[4] else ''
                    if self.get_field_value('button_class'):
                        btn_col4[0] = tag.Part(tag_name='a', attribs = {"role":"button", "class":self.get_field_value('button_class')})
                    else:
                        btn_col4[0] = tag.Part(tag_name='a', attribs = {"role":"button"})
                    btn_col4[0].htmlescaped=False
                    if self.get_field_value("link_ident4"):
                        url = self.get_url(self.get_field_value("link_ident4"))
                        if url:
                            if self.get_field_value("button_text4"):
                                btn_col4[0][0] = self.get_field_value("button_text4")
                            else:
                                btn_col4[0][0] = url
                            # create a url for the href
                            url = self.make_get_url(page, url, {self.get_formname("btn_col4"):g4}, True)
                            btn_col4[0].update_attribs({"href": url})
                        else:
                           btn_col4[0] = "Warning: broken link"
                    else:
                        btn_col4[0] = "Warning: broken link"
                self[rownumber].append(btn_col4)


    @classmethod
    def description(cls):
        """Returns a text string to illustrate the widget"""
        return """
<table>  <!-- with widget id and class widget_class -->
  <tr> <!-- with class  from even or odd classes -->
    <td> <!-- with style = width : 100% if maximize_text_col is True -->
         <!-- and with a class from col0_classes list if a list is given -->
      <!-- text string -->
    </td>
    <td>  <!-- Exists if btn_col1 is True -->
      <a role="button" href="#">
      <!-- With class set by button_class, and the href link will be the url of the link_ident1 with get field -->
      <!-- the button will show the button_text1 (not html escaped) -->
      </a>
    </td>
    <td>  <!-- Exists if btn_col2 is True -->
      <a role="button" href="#">
      <!-- With class set by button_class, and the href link will be the url of the link_ident2 with get field -->
      <!-- the button will show the button_text2 (not html escaped) -->
      </a>
    </td>
    <td>  <!-- Exists if btn_col3 is True -->
      <a role="button" href="#">
      <!-- With class set by button_class, and the href link will be the url of the link_ident3 with get field -->
      <!-- the button will show the button_text3 (not html escaped) -->
      </a>
    </td>
    <td>  <!-- Exists if btn_col4 is True -->
      <a role="button" href="#">
      <!-- With class set by button_class, and the href link will be the url of the link_ident4 with get field -->
      <!-- the button will show the button_text4 (not html escaped) -->
      </a>
    </td>
  </tr>
  <!-- rows repeated -->
</table>"""


class GeneralButtonTable2(Widget):
    """A table of buttons and text."""

    # This class does not display any error messages
    display_errors = False

    arg_descriptions = {
                        'dragrows':FieldArgTable(["boolean", "text"], valdt=True, jsonset=True),
                        'droprows':FieldArgTable(["boolean", "text"], valdt=True, jsonset=True),
                        'dropident':FieldArg("url", ""),
                        'cols':FieldArgTable(['url', 'url']),
                        'even_class':FieldArg("cssclass", ""),
                        'odd_class':FieldArg("cssclass", ""),
                        'hide':FieldArg("boolean", False, jsonset=True),
                        'button_class':FieldArg("cssclass", ""),
                        'contents':FieldArgTable(['text', 'text', 'boolean', 'text'], valdt=True, jsonset=True)
                        }

    def __init__(self, name=None, brief='', **field_args):
        """
        dragrows: A two element list for every row in the table, could be empty if no drag operation
                  col 0 - True if draggable, False if not
                  col 1 - If col 0 is True, this is data sent with the call wnen a row is dropped
        droprows: A two element list for every row in the table, could be empty if no drop operation
                  col 0 - True if droppable, False if not
                  col 1 - text to send with the call when a row is dropped here
        dropident: ident or label of target, called when a drop occurs which returns a JSON page
        cols: A two element list for every column in the table, must be given with empty values if no links
                  col 0 - target HTML page link ident of buttons in each column, if col1 not present or no javascript
                  col 1 - target JSON page link ident of buttons in each column, 
              col0, col1 values should be emty strings if no url applied to column
        even_class: class of even rows, if empty string, then no class will be applied
        odd_class: class of odd rows, if empty string, then no class will be applied
        hide: if True, table will be hidden
        button_class: The CSS class to apply to the buttons
        contents: A list for every element in the table, should be row*col lists
                   col 0 - text string, either text to display or button text
                   col 1 - A 'style' string set on the td cell, if empty string, no style applied
                   col 2 - Is button? If False only text will be shown, not a button, button class will not be applied
                           If True a link to link_ident/json_ident will be set with button_class applied to it
                   col 3 - The get field value of the button link, empty string if no get field
 
                  This fieldname used as the widgfield for the get data
        """
        Widget.__init__(self, name=name, brief=brief, **field_args)
        self.tag_name = "table"
        self._jsonurl_list = []
        self._dropurl = ''
        self._htmlurl_list = []
        self._button_class = ''
        self._even = ''
        self._odd = ''


    def _build(self, page, ident_list, environ, call_data, lang):
        "Build the table"
        # Hides widget if no error and hide is True
        self.widget_hide(self.get_field_value("hide"))
        fieldtable = self.get_field_value("contents")
        self._button_class = self.get_field_value('button_class')
        get_field_name = self.get_formname("contents")
        dragtable = self.get_field_value("dragrows")
        droptable = self.get_field_value("droprows")
        colidents = self.get_field_value("cols")
        cols = len(colidents)
        if not cols:
            self.show = False
            return
        elements = len(fieldtable)
        rows = elements//cols
        if elements != rows*cols:
            self._error = "Invalid table size : number of columns does not match table length"
            return
        if dragtable and (len(dragtable) != rows):
            self._error = "Invalid table size : dragrows length does not match table rows"
            return
        if droptable and (len(droptable) != rows):
            self._error = "Invalid table size : droprows length does not match table rows"
            return
        # list of json url's
        self._jsonurl_list = [ self.get_url(item[1]) for item in colidents ]
        # list of html url's
        self._htmlurl_list = [ self.get_url(item[0]) for item in colidents ]
        # dropurl
        self._dropurl = self.get_url(self.get_field_value("dropident"))
        # set even row class
        if self.get_field_value('even_class'):
            self._even = self.get_field_value('even_class')
        # set odd row class
        if self.get_field_value('odd_class'):
            self._odd = self.get_field_value('odd_class')
        # cell  increments for every table cell
        cell = -1
        # create rows
        for rownumber  in range(rows):
            if self._even and (rownumber % 2) :
                self[rownumber] = tag.Part(tag_name="tr", attribs={"class":self._even})
            elif self._odd and not (rownumber % 2):
                self[rownumber] = tag.Part(tag_name='tr', attribs={"class":self._odd})
            else:
                self[rownumber] = tag.Part(tag_name='tr')
            if dragtable:
                if dragtable[rownumber][1]:
                    dragdata = dragtable[rownumber][1]
                else:
                    dragdata = ""
                if dragtable[rownumber][0]:
                    self[rownumber].update_attribs(
{"style":"cursor:move;",
 "draggable":"true",
 "ondragstart":"SKIPOLE.widgets['{ident}'].dragstartfunc(event, '{data}')".format(ident = self.get_id(),
                                                                                  data = dragdata)})
            if droptable:
                if droptable[rownumber][1]:
                    dropdata = droptable[rownumber][1]
                else:
                    dropdata = ""
                if droptable[rownumber][0]:
                    self[rownumber].update_attribs(
{"ondrop":"SKIPOLE.widgets['{ident}'].dropfunc(event, '{data}')".format(ident = self.get_id(), data = dropdata),
 "ondragover":"SKIPOLE.widgets['{ident}'].allowdropfunc(event)".format(ident = self.get_id())})
            for colnumber in range(cols):
                cell += 1
                element = fieldtable[cell]
                # cell text
                if element[0]:
                    celltext = element[0]
                else:
                    celltext = ''
                # cell class
                if element[1]:
                    self[rownumber][colnumber] = tag.Part(tag_name='td', attribs={"style":element[1]})
                else:
                    self[rownumber][colnumber] = tag.Part(tag_name='td')
                # get html url for this column
                url = self._htmlurl_list[colnumber]
                # is it a button link
                if url and element[2]:
                    # its a link, apply button class
                    if self._button_class:
                        self[rownumber][colnumber][0] = tag.Part(tag_name='a', attribs = {"role":"button", "class":self._button_class})
                    else:
                        self[rownumber][colnumber][0] = tag.Part(tag_name='a', attribs = {"role":"button"})
                     # apply button text
                    if celltext:
                        self[rownumber][colnumber][0][0] = celltext
                        self[rownumber][colnumber][0].htmlescaped = False
                    else:
                        self[rownumber][colnumber][0][0] = url
                    # create a url for the href
                    cellurl = self.make_get_url(page, url, {get_field_name:element[3]}, True)
                    # apply url and href
                    self[rownumber][colnumber][0].update_attribs({"href": cellurl})
                else:
                    # not a link
                    self[rownumber][colnumber][0] = celltext
                    self[rownumber][colnumber].htmlescaped = False

    def _build_js(self, page, ident_list, environ, call_data, lang):
        """Sets a click event handler"""
        jscript = """  $("#{ident} a").click(function (e) {{
    SKIPOLE.widgets['{ident}'].eventfunc(e);
    }});
""".format(ident = self.get_id())
        if self._jsonurl_list or self._dropurl or self._htmlurl_list:
            return jscript + self._make_fieldvalues(json_url=self._jsonurl_list,
                                                    dropurl=self._dropurl,
                                                    html_url = self._htmlurl_list,
                                                    button_class = self._button_class,
                                                    even_class = self._even,
                                                    odd_class = self._odd)
        return jscript


class ProjectiFrame(Widget):
    """An iframe displaying a given sub project, with name of
       the sub project or sectionalias-subproject if the iframe is in a section"""

    # This class does not display any error messages
    display_errors = False

    arg_descriptions = {'project':FieldArg("text", ""),
                        'width':FieldArg("text", "800"),
                        'height':FieldArg("text", "800")
                       }

    def __init__(self, name=None, brief='', **field_args):
        """
        sub_project: The name of the sub project displayed in the iframe
        width: The width in pixels of the iframe
        height: the height in pixels of the iframe
        """
        Widget.__init__(self, name=name, brief=brief, **field_args)
        self.tag_name = "iframe"


    def _build(self, page, ident_list, environ, call_data, lang):
        "Build the iframe"
        proj_ident = self.get_field_value("project")
        if not proj_ident:
            self._error = "Warning: project for iframe is not given"
            return
        if not skiboot.is_project(proj_ident):
            self._error = "Warning: project %s for iframe has not been found" % proj_ident
            return
        project_url = skiboot.getproject(proj_ident).url
        if self.placename:
            iframename = self.placename + "-" + proj_ident
        else:
            iframename = proj_ident
        self.update_attribs({"width": self.get_field_value("width"),
                             "height": self.get_field_value("height"),
                             "name": iframename,
                             "src": project_url})


    @classmethod
    def description(cls):
        """Returns a text string to illustrate the widget"""
        return """
<iframe src="#">  <!-- with widget id and class widget_class
    and src the url of the project
    the name attribute will be the project name
    or sectionaliasname-project if the widget is in a section
    and height and width as given -->
</iframe>"""



class GeneralButtonTable1(Widget):
    """A table of buttons and text. Bottons include ability to send stored data"""

    # This class does not display any error messages
    display_errors = False

    arg_descriptions = {
                        'dragrows':FieldArgTable(["boolean", "text"], valdt=True, jsonset=True),
                        'droprows':FieldArgTable(["boolean", "text"], valdt=True, jsonset=True),
                        'dropident':FieldArg("url", ""),
                        'cols':FieldArgTable(['url', 'url', 'text'], valdt=True),
                        'even_class':FieldArg("cssclass", ""),
                        'odd_class':FieldArg("cssclass", ""),
                        'hide':FieldArg("boolean", False, jsonset=True),
                        'button_class':FieldArg("cssclass", ""),
                        'contents':FieldArgTable(['text', 'text', 'boolean', 'text'], valdt=True, jsonset=True)
                        }

    def __init__(self, name=None, brief='', **field_args):
        """
        dragrows: A two element list for every row in the table, could be empty if no drag operation
                  col 0 - True if draggable, False if not
                  col 1 - If col 0 is True, this is data sent with the call wnen a row is dropped
        droprows: A two element list for every row in the table, could be empty if no drop operation
                  col 0 - True if droppable, False if not
                  col 1 - text to send with the call when a row is dropped here
        dropident: ident or label of target, called when a drop occurs which returns a JSON page
        cols: A three element list for every column in the table, must be given with empty values if no links
                  col 0 - target HTML page link ident of buttons in each column, if col1 not present or no javascript
                  col 1 - target JSON page link ident of buttons in each column,
                  col 2 - key of stored local data to send, empty if not used
                  The 'cols' fieldname will be used as the widgfield for the sent data
              col0, col1 values should be emty strings if no url applied to column
        even_class: class of even rows, if empty string, then no class will be applied
        odd_class: class of odd rows, if empty string, then no class will be applied
        hide: if True, table will be hidden
        button_class: The CSS class to apply to the buttons
        contents: A list for every element in the table, should be row*col lists
                   col 0 - text string, either text to display or button text
                   col 1 - A 'style' string set on the td cell, if empty string, no style applied
                   col 2 - Is button? If False only text will be shown, not a button, button class will not be applied
                           If True a link to link_ident/json_ident will be set with button_class applied to it
                   col 3 - The get field value of the button link, empty string if no get field
                  This fieldname used as the widgfield for the get data
        """
        Widget.__init__(self, name=name, brief=brief, **field_args)
        self.tag_name = "table"
        self._jsonurl_list = []
        self._dropurl = ''
        self._htmlurl_list = []
        self._storagekey_list = []


    def _build(self, page, ident_list, environ, call_data, lang):
        "Build the table"
        # Hides widget if no error and hide is True
        self.widget_hide(self.get_field_value("hide"))
        fieldtable = self.get_field_value("contents")
        get_field_name = self.get_formname("contents")
        dragtable = self.get_field_value("dragrows")
        droptable = self.get_field_value("droprows")
        colidents = self.get_field_value("cols")
        cols = len(colidents)
        if not cols:
            self.show = False
            return
        elements = len(fieldtable)
        rows = elements//cols
        if elements != rows*cols:
            self._error = "Invalid table size : number of columns does not match table length"
            return
        if dragtable and (len(dragtable) != rows):
            self._error = "Invalid table size : dragrows length does not match table rows"
            return
        if droptable and (len(droptable) != rows):
            self._error = "Invalid table size : droprows length does not match table rows"
            return
        # list of json url's
        self._jsonurl_list = [ self.get_url(item[1]) for item in colidents ]
        # list of html url's
        self._htmlurl_list = [ self.get_url(item[0]) for item in colidents ]
        # list of storage key's
        self._storagekey_list = [ item[2] for item in colidents ]
        # dropurl
        self._dropurl = self.get_url(self.get_field_value("dropident"))
        # set even row class
        _even = None
        if self.get_field_value('even_class'):
            _even = self.get_field_value('even_class')
        # set odd row class
        _odd = None
        if self.get_field_value('odd_class'):
            _odd = self.get_field_value('odd_class')
        # cell  increments for every table cell
        cell = -1
        # create rows
        for rownumber  in range(rows):
            if _even and (rownumber % 2) :
                self[rownumber] = tag.Part(tag_name="tr", attribs={"class":_even})
            elif _odd and not (rownumber % 2):
                self[rownumber] = tag.Part(tag_name='tr', attribs={"class":_odd})
            else:
                self[rownumber] = tag.Part(tag_name='tr')
            if dragtable:
                if dragtable[rownumber][1]:
                    dragdata = dragtable[rownumber][1]
                else:
                    dragdata = ""
                if dragtable[rownumber][0]:
                    self[rownumber].update_attribs(
{"style":"cursor:move;",
 "draggable":"true",
 "ondragstart":"SKIPOLE.widgets['{ident}'].dragstartfunc(event, '{data}')".format(ident = self.get_id(),
                                                                                  data = dragdata)})
            if droptable:
                if droptable[rownumber][1]:
                    dropdata = droptable[rownumber][1]
                else:
                    dropdata = ""
                if droptable[rownumber][0]:
                    self[rownumber].update_attribs(
{"ondrop":"SKIPOLE.widgets['{ident}'].dropfunc(event, '{data}')".format(ident = self.get_id(), data = dropdata),
 "ondragover":"SKIPOLE.widgets['{ident}'].allowdropfunc(event)".format(ident = self.get_id())})
            for colnumber in range(cols):
                cell += 1
                element = fieldtable[cell]
                # cell text
                if element[0]:
                    celltext = element[0]
                else:
                    celltext = ''
                # cell class
                if element[1]:
                    self[rownumber][colnumber] = tag.Part(tag_name='td', attribs={"style":element[1]})
                else:
                    self[rownumber][colnumber] = tag.Part(tag_name='td')
                # get html url for this column
                url = self._htmlurl_list[colnumber]
                # is it a button link
                if url and element[2]:
                    # its a link, apply button class
                    if self.get_field_value('button_class'):
                        self[rownumber][colnumber][0] = tag.Part(tag_name='a', attribs = {"role":"button", "class":self.get_field_value('button_class')})
                    else:
                        self[rownumber][colnumber][0] = tag.Part(tag_name='a', attribs = {"role":"button"})
                     # apply button text
                    if celltext:
                        self[rownumber][colnumber][0][0] = celltext
                        self[rownumber][colnumber][0].htmlescaped = False
                    else:
                        self[rownumber][colnumber][0][0] = url
                    # create a url for the href
                    cellurl = self.make_get_url(page, url, {get_field_name:element[3]}, True)
                    # apply url and href
                    self[rownumber][colnumber][0].update_attribs({"href": cellurl})
                else:
                    # not a link
                    self[rownumber][colnumber][0] = celltext
                    self[rownumber][colnumber].htmlescaped = False

    def _build_js(self, page, ident_list, environ, call_data, lang):
        """Sets a click event handler"""
        jscript = """  $("#{ident} a").click(function (e) {{
    SKIPOLE.widgets['{ident}'].eventfunc(e);
    }});
""".format(ident = self.get_id())
        if self._jsonurl_list or self._dropurl or self._htmlurl_list:
            return jscript + self._make_fieldvalues('even_class',
                                                    'odd_class',
                                                    'button_class',
                                                    json_url=self._jsonurl_list,
                                                    dropurl=self._dropurl,
                                                    html_url = self._htmlurl_list,
                                                    keys = self._storagekey_list)
        return jscript



class Audio1(Widget):
    """An audio, can be set to play via JSON call"""

    # This class does not display any error messages
    display_errors = False

    arg_descriptions = {'mp3_ident':FieldArg("url", ''),
                        'wav_ident':FieldArg("url", ''),
                        'ogg_ident':FieldArg("url", ''),
                        'controls':FieldArg("boolean", False),
                        'play':FieldArg("boolean", False, jsonset=True)
                       }

    def __init__(self, name=None, brief='', **field_args):
        """
        mp3_ident: The src ident of an mp3 file
        wav_ident: The src ident of an wav file
        ogg_ident: The src ident of an ogg file
        controls: If True sets the controls attribute
        play: If True, sets autoplay attribute, if set True by JSON, causes the file to play 
        """
        Widget.__init__(self, name=name, brief=brief, **field_args)
        self.tag_name = "audio"


    def _build(self, page, ident_list, environ, call_data, lang):
        "Build the audio"

        if self.get_field_value('controls'):
            self.update_attribs({'controls':'controls'})
        if self.get_field_value('play'):
            self.update_attribs({'autoplay':'autoplay'})
        if self.get_field_value("mp3_ident"):
            mp3url = self.get_url(self.get_field_value("mp3_ident"))
            self.append( tag.ClosedPart(tag_name="source", attribs= {"src": mp3url, "type":"audio/mpeg"}) )
        if self.get_field_value("wav_ident"):
            wavurl = self.get_url(self.get_field_value("wav_ident"))
            self.append( tag.ClosedPart(tag_name="source", attribs= {"src": wavurl, "type":"audio/wav"}) )
        if self.get_field_value("ogg_ident"):
            oggurl = self.get_url(self.get_field_value("ogg_ident"))
            self.append( tag.ClosedPart(tag_name="source", attribs= {"src": oggurl, "type":"audio/ogg"}) )


    @classmethod
    def description(cls):
        """Returns a text string to illustrate the widget"""
        return """
 <audio>  <!-- with controls and autoplay attributes if they are set True -->
  <source src="#" type="audio/mpeg" />  <!-- with src set to url of ident/label mp3_ident -->
  <source src="#" type="audio/wav" />   <!-- with src set to url of ident/label wav_ident -->
  <source src="#" type="audio/ogg" />    <!-- with src set to url of ident/label ogg_ident -->
</audio> 
"""


class Audio2(Widget):
    """An audio, can be set to play via JSON call"""

    # This class does not display any error messages
    display_errors = False

    arg_descriptions = {'src_mp3':FieldArg("text", '', jsonset=True),
                        'src_wav':FieldArg("text", '', jsonset=True),
                        'src_ogg':FieldArg("text", '', jsonset=True),
                        'controls':FieldArg("boolean", False),
                        'play':FieldArg("boolean", False, jsonset=True)
                       }

    def __init__(self, name=None, brief='', **field_args):
        """
        src_mp3: The src url string (not ident) of an mp3 file
        src_wav: The src url string (not ident) of a wav file
        src_ogg: The src url string (not ident) of an ogg file
        controls: If True sets the controls attribute
        play: If True, sets autoplay attribute, if set True by JSON, causes the file to play 
        """
        Widget.__init__(self, name=name, brief=brief, **field_args)
        self.tag_name = "audio"


    def _build(self, page, ident_list, environ, call_data, lang):
        "Build the audio"

        if self.get_field_value('controls'):
            self.update_attribs({'controls':'controls'})
        if self.get_field_value('play'):
            self.update_attribs({'autoplay':'autoplay'})
        if self.get_field_value("src_mp3"):
            self.append( tag.ClosedPart(tag_name="source", attribs= {"src": quote(self.get_field_value("src_mp3"), safe='/:'), "type":"audio/mpeg"}) )
        if self.get_field_value("src_wav"):
            self.append( tag.ClosedPart(tag_name="source", attribs= {"src": quote(self.get_field_value("src_wav"), safe='/:'), "type":"audio/wav"}) )
        if self.get_field_value("src_ogg"):
            self.append( tag.ClosedPart(tag_name="source", attribs= {"src": quote(self.get_field_value("src_ogg"), safe='/:'), "type":"audio/ogg"}) )


    @classmethod
    def description(cls):
        """Returns a text string to illustrate the widget"""
        return """
 <audio>  <!-- with controls and autoplay attributes if they are set True -->
  <source src="#" type="audio/mpeg" />  <!-- with src set to src_mp3 -->
  <source src="#" type="audio/wav" />   <!-- with src set to src_wav -->
  <source src="#" type="audio/ogg" />    <!-- with src set to src_ogg -->
</audio> 
"""

