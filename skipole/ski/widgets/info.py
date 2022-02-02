

"""This module defines various widgets which provide information"""
import time

from .. import skiboot
from .. import tag
from . import Widget, ClosedWidget, FieldArg, FieldArgList, FieldArgTable, FieldArgDict


class ServerTimeStamp(Widget):
    """A widget containing the current server time. consists of a span with time stamp"""

    # This class does not display any error messages
    display_errors = False

    arg_descriptions = {
                        'timestamp':FieldArg("text", '', jsonset=True),
                        'utc':FieldArg("boolean", True)
                       }

    def __init__(self, name=None, brief='', **field_args):
        """
        timestamp: normally empty and timestamp will automatically be displayed, or other text can be set here.
        utc: If True, time is utc, if False it is local time
        """
        Widget.__init__(self, name=name, brief=brief, **field_args)
        self.tag_name = "span"
        self[0] = ""

    def _build(self, page, ident_list, environ, call_data, lang):
        "Build the element"
        # set timer or string
        if self.get_field_value("timestamp"):
            self[0] = self.get_field_value("timestamp")
        elif self.get_field_value("utc"):
            self[0] = time.strftime("%c", time.gmtime())
        else:
            self[0] = time.strftime("%c", time.localtime())

    @classmethod
    def description(cls):
        """Returns a text string to illustrate the widget"""
        return """
<span>  <!-- with widget id and class widget_class -->
  <!-- Normally timestamp -->
</span>
"""


class PageIdent(Widget):
    """A widget containing the given ident which is set within the text
         If no page ident is given, shows ident of the current page"""

    # This class does not display any error messages
    display_errors = False

    arg_descriptions = {'page_ident':FieldArg("ident", ''),
                        'span_text':FieldArg("text", "", jsonset=True)
                       }

    def __init__(self, name=None, brief='', **field_args):
        """
        page_ident: The ident of a page or folder, converted to string
        span_text: if given, overrides the page_ident value
        """
        Widget.__init__(self, name=name, brief=brief, **field_args)
        self.tag_name = "span"
        self[0] = ""

    def _build(self, page, ident_list, environ, call_data, lang):
        "Build the element"
        if self.get_field_value("span_text"):
            self[0] = self.get_field_value("span_text")
        elif self.get_field_value("page_ident"):
            self[0] = self.get_field_value("page_ident").to_comma_str()
        else:
            self[0] = page.ident.to_comma_str()


    @classmethod
    def description(cls):
        """Returns a text string to illustrate the widget"""
        return """
<span>  <!-- with widget id and class widget_class -->
  <!-- string value of the page_ident, or span_text -->
</span>
"""


class PageName(Widget):
    """A widget containing the given page name which is set within the text
         If no page ident is given, shows name of the current page"""

    # This class does not display any error messages
    display_errors = False

    arg_descriptions = {'page_ident':FieldArg("ident", ''),
                        'span_text':FieldArg("text", "", jsonset=True)
                       }

    def __init__(self, name=None, brief='', **field_args):
        """
        page_ident: The ident of a page or folder
        span_text: if given, overrides the page name value
        """
        Widget.__init__(self, name=name, brief=brief, **field_args)
        self.tag_name = "span"
        self[0] = ""

    def _build(self, page, ident_list, environ, call_data, lang):
        "Build the element"
        if self.get_field_value("span_text"):
            self[0] = self.get_field_value("span_text")
        elif self.get_field_value("page_ident"):
            requested_page = skiboot.get_item(self.get_field_value("page_ident"))
            if requested_page is None:
                self[0] = "Unknown page"
            else:
                self[0] = requested_page.name
        else:
            self[0] = page.name


    @classmethod
    def description(cls):
        """Returns a text string to illustrate the widget"""
        return """
<span>  <!-- with widget id and class widget_class -->
  <!-- The page name, or span_text -->
</span>
"""


class PageDescription(Widget):
    """A widget containing the page brief of the given ident which is set within the text
         If no page ident is given, shows brief of the current page"""

    # This class does not display any error messages
    display_errors = False

    arg_descriptions = {'page_ident':FieldArg("ident", ''),
                        'span_text':FieldArg("text", "", jsonset=True)
                       }

    def __init__(self, name=None, brief='', **field_args):
        """
        page_ident: The ident of a page or folder
        span_text: if given, overrides the page description value
        """
        Widget.__init__(self, name=name, brief=brief, **field_args)
        self.tag_name = "span"
        self[0] = ""

    def _build(self, page, ident_list, environ, call_data, lang):
        "Build the element"
        if self.get_field_value("span_text"):
            self[0] = self.get_field_value("span_text")
        elif self.get_field_value("page_ident"):
            requested_page = skiboot.get_item(self.get_field_value("page_ident"))
            if requested_page is None:
                self[0] = "Unknown page"
            else:
                self[0] = requested_page.brief
        else:
            self[0] = page.brief

    @classmethod
    def description(cls):
        """Returns a text string to illustrate the widget"""
        return """
<span>  <!-- with widget id and class widget_class -->
  <!-- The page description -->
</span>
"""


class ProjectName(Widget):
    """A span showing the name of the project the page is in"""

    # This class does not display any error messages
    display_errors = False

    arg_descriptions = {}

    def __init__(self, name=None, brief='', **field_args):
        """
        Shows project name
        """
        Widget.__init__(self, name=name, brief=brief, **field_args)
        self.tag_name = "span"
        self[0] = ""

    def _build(self, page, ident_list, environ, call_data, lang):
        "Build the element"        
        self[0] = page.ident.proj

    @classmethod
    def description(cls):
        """Returns a text string to illustrate the widget"""
        return """
<span>  <!-- with widget id and class widget_class -->
  <!-- the project name -->
</span>
"""


class Version(Widget):
    """A span showing the project version of the page it is in"""

    # This class does not display any error messages
    display_errors = False

    arg_descriptions = {}

    def __init__(self, name=None, brief='', **field_args):
        """
        Shows project version
        """
        Widget.__init__(self, name=name, brief=brief, **field_args)
        self.tag_name = "span"
        self[0] = ""

    def _build(self, page, ident_list, environ, call_data, lang):
        "Build the element"        
        self[0] = page.project.version

    @classmethod
    def description(cls):
        """Returns a text string to illustrate the widget"""
        return """
<span>  <!-- with widget id and class widget_class -->
  <!-- string of the project version -->
</span>
"""


class SkipoleVersion(Widget):
    """A span showing this version of the skipole framework"""

    # This class does not display any error messages
    display_errors = False

    arg_descriptions = {}

    def __init__(self, name=None, brief='', **field_args):
        """
        Shows skipole version
        """
        Widget.__init__(self, name=name, brief=brief, **field_args)
        self.tag_name = "span"
        self[0] = ""

    def _build(self, page, ident_list, environ, call_data, lang):
        "Build the element"        
        self[0] = skiboot.version()

    @classmethod
    def description(cls):
        """Returns a text string to illustrate the widget"""
        return """
<span>  <!-- with widget id and class widget_class -->
  <!-- string of the skipole framework version -->
</span>
"""


class Redirector(Widget):
    """A widget containing javascript which redirects the page to the url
       Once the page is loaded, the redirection occurs, so normally
       this is the only widget on the page
       A textblock is displayed with the link to the url if the client has javascript disabled"""

    arg_descriptions = {'url':FieldArg("text", ''),
                        'textblock_ref':FieldArg("textblock_ref", ""),
                        'text_refnotfound':FieldArg("text", "If this page does not redirect automatically, follow this link:"),
                        'text_replaceblock':FieldArg("text", "If this page does not redirect automatically, follow this link:"),
                        'linebreaks':FieldArg("boolean", True)
                       }

    def __init__(self, name=None, brief='', **field_args):
        """
        url: the url to redirect to
        textblock_ref: The reference of the TextBlock appearing in the paragraph
        text_refnotfound: text to appear if the textblock is not found
        text_replaceblock: text set here will replace the textblock
        linebreaks: Set True if linebreaks in the text are to be shown as html breaks
        """
        Widget.__init__(self, name=name, brief=brief, **field_args)
        self.tag_name = "div"
        self[0] = tag.Part(tag_name='script', attribs={"type":"text/javascript"})
        self[1] = tag.Part(tag_name='p')
        self._url = ''


    def _error_build(self, message):
        """Called if an error is raised"""
        if message:
            self._url = message


    def _build(self, page, ident_list, environ, call_data, lang):
        "Build the widget"
        if self.error_status and self._url:
            url = self._url
        else:
            url = self.get_field_value("url")

        self[0][0] = "window.location.replace(\"%s\");" % (url,)

        linebreaks = bool(self.get_field_value('linebreaks'))

        if self.get_field_value('text_replaceblock'):
            # no textblock, just the replacement text
            tblock = self.get_field_value('text_replaceblock')
            if not linebreaks:
                self[1].linebreaks = False
        else:
            # define the textblock
            tblock = self.get_field_value("textblock_ref")
            tblock.failmessage = self.get_field_value('text_refnotfound')
            tblock.linebreaks = linebreaks
            tblock.proj_ident = page.proj_ident

        self[1][0] = tblock
        self[1][1] = tag.ClosedPart(tag_name='br')
        self[1][2] = tag.Part(tag_name='a', attribs={"href":url}, text=url)


    @classmethod
    def description(cls):
        """Returns a text string to illustrate the widget"""
        return """
<div>  <!-- with widget id and class widget_class -->
  <!-- url is either the url argument, or is the error message if an error is raised on the widget -->
  <script type="text/javascript">
     <!-- window.location.replace("url"); -->
  </script>
  <p>
    <!-- text_replaceblock or the textblock text here -->
    <br />
    <a href="url"> 
        <!-- url --> 
    </a>
  </p>
</div>
"""


class ProgressBar1(Widget):
    """A div containing a progress bar"""

    # This class does not display any error messages
    display_errors = False

    arg_descriptions = {'label':FieldArg("text", "Progress:"),
                        'label_class':FieldArg("cssclass", ''),
                        'label_style':FieldArg("cssstyle", ''),
                        'text':FieldArg("text", "0%", jsonset=True),
                        'value':FieldArg("text", "0", jsonset=True),
                        'max':FieldArg("text", "100"),
                        'progress_class':FieldArg("cssclass", ''),
                        'progress_style':FieldArg("cssstyle", ''),
                       }

    def __init__(self, name=None, brief='', **field_args):
        """
        text shown in place of the bar if the client browser does not support the progress tag
        """
        Widget.__init__(self, name=name, brief=brief, **field_args)
        self.tag_name = "div"
        self[0] = tag.Part(tag_name="label", hide_if_empty=True)
        self[1] = tag.Part(tag_name='progress')

    def _build(self, page, ident_list, environ, call_data, lang):
        "build the widget"
        if self.get_field_value('label_class'):
            self[0].update_attribs({"class": self.get_field_value('label_class')})
        if self.get_field_value('label_style'):
            self[0].update_attribs({"style": self.get_field_value('label_style')})
        if self.get_field_value("label"):
            self[0][0] = self.get_field_value("label")
        # set an id in the progress tag for the 'label for' tag
        self[1].insert_id()
        self[0].update_attribs({'for':self[1].get_id()})
        if self.get_field_value('progress_class'):
            self[1].update_attribs({"class": self.get_field_value('progress_class')})
        if self.get_field_value('progress_style'):
            self[1].update_attribs({"style": self.get_field_value('progress_style')})
        if self.get_field_value("text"):
            self[1][0] = self.get_field_value("text")
        if self.get_field_value('max'):
            self[1].update_attribs({"max": self.get_field_value('max')})
        if self.get_field_value('value'):
            self[1].update_attribs({"value": self.get_field_value('value')})

    def _build_js(self, page, ident_list, environ, call_data, lang):
        """Sets progress bar id into jscript"""
        return self._make_fieldvalues(progressident = self[1].get_id())

    @classmethod
    def description(cls):
        """Returns a text string to illustrate the widget"""
        return """
<div>  <!-- with widget id and class widget_class -->
 <label> <!-- with class label_class and style label_style -->
         <!-- with contents label -->
 </label>
 <progress> <!-- with attributes value and max -->
            <!-- with contents text -->
 </progress> 
</div>
"""






