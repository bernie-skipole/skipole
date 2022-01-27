

"""Defines widgets which may be used as page footers"""

from .. import tag
from . import Widget, FieldArg, FieldArgList, FieldArgTable, FieldArgDict


class SimpleFooter(Widget):
    """Defines a div, with a paragraph of text"""

    error_location = (0,0,0)

    arg_descriptions = {
                        'footer_text':FieldArg("text",'', jsonset=True),
                        'para_class':FieldArg("cssclass",""),
                        'error_class':FieldArg("cssclass", ""),
                        'paradiv_class':FieldArg("cssclass",""),
                       }

    def __init__(self, name=None, brief='', **field_args):
        """
         footer_text: The text to appear in the footer
         paradiv_class: css class of the div holding the footer paragraph
         para_class: css class of the footer text paragraph
         error_class: css class of the error paragraph
        """

        Widget.__init__(self, name=name, brief=brief, **field_args)
        self.tag_name = "div"
        # hidden error
        self[0] = tag.Part(tag_name="div", attribs={"style":"display:none;"})
        self[0][0] = tag.Part(tag_name="p")
        self[0][0][0] = ''
        self[1] = tag.Part(tag_name="div")
        self[1][0] = tag.Part(tag_name="p")

    def _build(self, page, ident_list, environ, call_data, lang):
        "Build the paragraph"
        self[0].set_class_style(self.wf.error_class)
        if self.error_status:
            self[0].del_one_attrib("style")
        self[1].set_class_style(self.wf.paradiv_class)
        self[1][0].set_class_style(self.wf.para_class)
        if self.wf.footer_text:
            self[1][0][0] = self.wf.footer_text
        # set an id in the footer_text paragraph
        # any label:value added to self.jlabels will be set in a javascript fieldvalues attribute for the widget
        self.jlabels['textident'] = self[1][0].insert_id()


    @classmethod
    def description(cls):
        """Returns a text string to illustrate the widget"""
        return """<div> <!-- with widget id and class widget_class -->
  <div> <!-- normally hidden div, with class error_class -->
    <p>       <!-- Any error text appears here --> </p>
  </div>
  <div>  <!-- with class paradiv_class -->
    <p>  <!-- with class para_class -->
    <!-- footer_text appears in this paragraph -->
    </p>
  </div>
</div>
"""

