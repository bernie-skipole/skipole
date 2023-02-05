

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

    def _build(self, page, ident_list, environ, call_data, lang):
        "Build the element"
        # set timer or string
        if self.wf.timestamp:
            self[0] = self.wf.timestamp
        elif self.wf.utc:
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
    """A widget displaying the ident of a page label
       If no page label or span_text are given,
       shows ident of the current page"""

    # This class does not display any error messages
    display_errors = False

    arg_descriptions = {'page_label':FieldArg("text", ''),
                        'span_text':FieldArg("text", "", jsonset=True)
                       }

    def __init__(self, name=None, brief='', **field_args):
        """
        page_label: The label of a page or folder
        span_text: if given, overrides the page ident value
        """
        Widget.__init__(self, name=name, brief=brief, **field_args)
        self.tag_name = "span"

    def _build(self, page, ident_list, environ, call_data, lang):
        "Build the element"
        if self.wf.span_text:
            self[0] = self.wf.span_text
        elif self.wf.page_label:
            proj = skiboot.getproject(self.proj_ident)
            # its a label string of this project
            if proj is None:
                self[0] = f"Unable to resolve the ident of {self.wf.page_label}"
                return
            value = proj.resolve_label(self.wf.page_label)
            # so value is one of the tuple ident, None, or URL
            if not value:
                self[0] = f"Unable to resolve the ident of {self.wf.page_label}"
                return
            if isinstance(value, str):
                # a url
                self[0] = f"Given label points to URL rather than a page ident"
                return
            # an ident tuple
            self[0] = f"{value[0]},{value[1]}"
        else:
            self[0] = page.ident.to_comma_str()


    @classmethod
    def description(cls):
        """Returns a text string to illustrate the widget"""
        return """
<span>  <!-- with widget id and class widget_class -->
  <!-- string value of the page ident, or span_text -->
</span>
"""


class PageName(Widget):
    """A widget containing the given page name which is set within the text
         If no page ident is given, shows name of the current page"""

    # This class does not display any error messages
    display_errors = False

    arg_descriptions = {'page_ident':FieldArg("text", ''),
                        'span_text':FieldArg("text", "", jsonset=True)
                       }

    def __init__(self, name=None, brief='', **field_args):
        """
        page_ident: The label or ident of a page or folder
        span_text: if given, overrides the page name value
        """
        Widget.__init__(self, name=name, brief=brief, **field_args)
        self.tag_name = "span"

    def _build(self, page, ident_list, environ, call_data, lang):
        "Build the element"
        if self.wf.span_text:
            self[0] = self.wf.span_text
        elif self.wf.page_ident:
            proj = skiboot.getproject(self.proj_ident)
            if "/" in self.wf.page_ident:
                # its a URL
                self[0] = f"Unable to resolve {self.wf.page_ident}"
                return

            if self.wf.page_ident.isdigit():
                # Its "integer"
                try:
                    value = (self.proj_ident, int(self.wf.page_ident))
                except:
                    self[0] = f"Unable to resolve the ident of {self.wf.page_ident}"
                    return
            elif ',' in self.wf.page_ident:
                # Its a string such as "proj_ident,number"
                vallist = self.wf.page_ident.split(',')
                if len(vallist) != 2:
                    self[0] = f"Unable to resolve the ident of {self.wf.page_ident}"
                    return
                lblproj = vallist[0].strip(" ()[]\"\'")
                lblval = vallist[1].strip(" ()[]\"\'")
                if lblval.isdigit():
                    # Its "subproject, integer"
                    try:
                        value = (lblproj, int(lblval))
                    except:
                        self[0] = f"Unable to resolve the ident of {self.wf.page_ident}"
                        return
                else:
                    # Its "subproject, label"
                    subproj = skiboot.getproject(lblproj)
                    if subproj is None:
                        self[0] = f"Unable to resolve the ident of {self.wf.page_ident}"
                        return
                    value = subproj.resolve_label(lblval)
            else:
                 # its a label string of this project
                if proj is None:
                    self[0] = f"Unable to resolve the ident of {self.wf.page_ident}"
                    return
                value = proj.resolve_label(self.wf.page_ident)

            # so value is one of the tuple ident, None, or URL
            if not value:
                self[0] = f"Unable to resolve the ident of {self.wf.page_ident}"
                return
            if isinstance(value, str):
                # a url
                self[0] = f"Given label points to URL rather than an ident"
                return
            # an ident tuple, make an ident
            page_ident = skiboot.make_ident(value)
            requested_page = skiboot.get_item(page_ident)
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

    arg_descriptions = {'page_ident':FieldArg("text", ''),
                        'span_text':FieldArg("text", "", jsonset=True)
                       }

    def __init__(self, name=None, brief='', **field_args):
        """
        page_ident: The label or ident of a page or folder
        span_text: if given, overrides the page description value
        """
        Widget.__init__(self, name=name, brief=brief, **field_args)
        self.tag_name = "span"

    def _build(self, page, ident_list, environ, call_data, lang):
        "Build the element"
        if self.wf.span_text:
            self[0] = self.wf.span_text
        elif self.wf.page_ident:
            proj = skiboot.getproject(self.proj_ident)
            if "/" in self.wf.page_ident:
                # its a URL
                self[0] = f"Unable to resolve {self.wf.page_ident}"
                return

            if self.wf.page_ident.isdigit():
                # Its "integer"
                try:
                    value = (self.proj_ident, int(self.wf.page_ident))
                except:
                    self[0] = f"Unable to resolve the ident of {self.wf.page_ident}"
                    return
            elif ',' in self.wf.page_ident:
                # Its a string such as "proj_ident,number"
                vallist = self.wf.page_ident.split(',')
                if len(vallist) != 2:
                    self[0] = f"Unable to resolve the ident of {self.wf.page_ident}"
                    return
                lblproj = vallist[0].strip(" ()[]\"\'")
                lblval = vallist[1].strip(" ()[]\"\'")
                if lblval.isdigit():
                    # Its "subproject, integer"
                    try:
                        value = (lblproj, int(lblval))
                    except:
                        self[0] = f"Unable to resolve the ident of {self.wf.page_ident}"
                        return
                else:
                    # Its "subproject, label"
                    subproj = skiboot.getproject(lblproj)
                    if subproj is None:
                        self[0] = f"Unable to resolve the ident of {self.wf.page_ident}"
                        return
                    value = subproj.resolve_label(lblval)
            else:
                 # its a label string of this project
                if proj is None:
                    self[0] = f"Unable to resolve the ident of {self.wf.page_ident}"
                    return
                value = proj.resolve_label(self.wf.page_ident)

            # so value is one of the tuple ident, None, or URL
            if not value:
                self[0] = f"Unable to resolve the ident of {self.wf.page_ident}"
                return
            if isinstance(value, str):
                # a url
                self[0] = f"Given label points to URL rather than an ident"
                return
            # an ident tuple, make an ident
            page_ident = skiboot.make_ident(value)
            requested_page = skiboot.get_item(page_ident)
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
            url = self.wf.url

        self[0][0] = "window.location.replace(\"%s\");" % (url,)

        linebreaks = bool(self.wf.linebreaks)

        if self.wf.text_replaceblock:
            # no textblock, just the replacement text
            tblock = self.wf.text_replaceblock
            if not linebreaks:
                self[1].linebreaks = False
        else:
            # define the textblock
            tblock = self.wf.textblock_ref
            tblock.failmessage = self.wf.text_refnotfound
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
        self[0].set_class_style(self.wf.label_class, self.wf.label_style)
        if self.wf.label:
            self[0][0] = self.wf.label
        # set an id in the progress tag for the 'label for' tag
        for_id = self[1].insert_id()
        # any label:value added to self.jlabels will be set in a javascript fieldvalues attribute for the widget
        self.jlabels['progressident'] = for_id
        self[0].attribs['for'] = for_id

        self[1].set_class_style(self.wf.progress_class, self.wf.progress_style)
        if self.wf.text:
            self[1][0] = self.wf.text
        if self.wf.max:
            self[1].attribs["max"] = self.wf.max
        if self.wf.value:
            self[1].attribs["value"] = self.wf.value


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






