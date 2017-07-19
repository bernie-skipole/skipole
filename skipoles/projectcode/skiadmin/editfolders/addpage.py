####### SKIPOLE WEB FRAMEWORK #######
#
# addpage.py  - get and put functions for the add page
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


import os, inspect, re

from ....ski import skiboot, responders, tag
from ....ski.excepts import ValidateError, FailPage, ServerError
from ....ski.page_class_definition import CSS, FilePage, RespondPage, JSON
from ....ski.widgets import links
from ....skilift import fromjson

from .. import utils, css_styles

# a search for anything none-alphanumeric and not an underscore
_AN = re.compile('[^\w]')

# a search for anything none-alphanumeric, not a dot and not an underscore
_AND = re.compile('[^\w\.]')



def retrieve_add_page(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):

    editedproj = call_data['editedproj']
    adminproj = call_data['adminproj']

    if 'edited_folder' not in call_data:
        raise FailPage(message = "Folder missing")

    parent = skiboot.from_ident(call_data['edited_folder'], proj_ident=editedproj. proj_ident)
    if parent.page_type != "Folder":
        raise FailPage(message = "Invalid folder")
    if not parent in editedproj:
        raise FailPage(message = "Invalid folder")

    parent_ident = str(parent.ident)

    page_data[("adminhead","page_head","large_text")] = "Add page to : %s" % (parent.url,)
    page_data[("adminhead","page_head","small_text")] = "Choose options to add the page:"

    page_data['st1:parent'] = parent_ident

    # rb1: page type checked
    if 'radio_checked' in call_data:
        page_data['rb1:radio_checked'] = call_data['radio_checked']

    page_data[('rb1','radio_values')] = ['page', 'responder', 'svg', 'css', 'json', 'file', 'copy']
    page_data[('rb1','radio_text')] = ['Template page',
                                           'Responder',
                                           'SVG Image page',
                                           'CSS page',
                                           'JSON page',
                                           'File Link page',
                                           'Copy an existing page']

    # st1: new page name
    if 'new_page' in call_data:
        page_data['it4:new_page'] = call_data['new_page']

    # it2: text input for page brief
    if ('page_brief' in call_data) and call_data['page_brief']:
        page_data['it2:page_brief'] = call_data['page_brief']

    # it3: page ident number
    if 'page_ident_number' in call_data:
        page_data['it3:page_ident_number'] = str(call_data['page_ident_number'])
    else:
        page_data['it3:page_ident_number'] = str(editedproj.next_ident().num)


def _check_data(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    editedproj = call_data['editedproj']
    if 'edited_folder' not in call_data:
        raise FailPage(message = "Folder missing")
    parent_ident = skiboot.Ident.to_ident(call_data['edited_folder'], editedproj.proj_ident)
    # parent folder is the folder from memory, not a copy
    parent =  editedproj.get_item(parent_ident)
    if parent.page_type != "Folder":
        raise FailPage(message = "Invalid folder")

    # Get the new ident
    if 'page_ident_number' not in call_data:
        raise FailPage(message = "The ident of the new page has not been found", widget='st1')
    new_ident = skiboot.make_ident(call_data['page_ident_number'], proj_ident=editedproj.proj_ident)
    if new_ident is None:
        raise FailPage(message = "The ident of the new page is invalid", widget='st1')
    
    # Get the new page name
    if 'new_page' not in call_data:
        raise FailPage(message = "The name of the new page has not been found", widget='st1')
    new_name = call_data['new_page']
    if new_name in parent:
        raise FailPage(message = "The name of the new page already exists in this folder", widget='st1')
    # Get the new page brief
    if 'page_brief' in call_data:
        new_brief = call_data['page_brief']
    else:
        new_brief = 'New Page'
    return parent, new_ident, new_name, new_brief


def _make_head(page, proj_ident, page_ident, title="", css_links=[], js_links=[]):
    """Used when creating a new template page to make a default header
       css_links is the list of css page labels to include
       js_links is the list of javascript page labels to include
       """
    head = page.head

    head[0] = tag.ClosedPart(tag_name="meta",
                                  attribs = {"charset":"utf-8"})
    head[0].brief = "The charset meta declaration"
    head[1] = tag.ClosedPart(tag_name="meta",
                                  attribs = {"name":"viewport",
                                             "content":"width=device-width, initial-scale=1"})
    head[1].brief = "The viewport meta declaration"
    head[2] = tag.Part(tag_name="title")
    head[2].brief = "The page title element"
    if title:
        head[2][0] = title
    else:
        head[2][0] = "Page %s" % (page_ident.num)
    if css_links:
        for label in css_links:
            csslink = tag.ClosedPart(tag_name = "link",
                                                                   attribs={"href": "{" + label + "}",
                                                                                       "rel":"stylesheet",
                                                                                       "type":"text/css"},
                                                                   brief='css link to %s' % (label,))
            head.append(csslink)
    if js_links:
        for label in js_links:
            scriptlink = tag.Part(tag_name = "script", attribs={"src":"{" + label + "}"}, brief='script link to %s' % (label,))
            head.append(scriptlink)



def submit_new_template(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Create a new template page"
    editedproj = call_data['editedproj']
    adminproj = call_data['adminproj']
    # first get submitted data for the new page
    parent, new_ident, new_name, new_brief = _check_data(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang)
    # check name is alphanumric, dot or underscore only
    if _AND.search(new_name):
        raise FailPage(message = "Templates page names must be alphanumric, dot or underscore only", widget='st1')
    # create a new page and add to the given parent folder
    backcol = fromjson.get_defaults(editedproj.proj_ident, key="backcol")
    if backcol is None:
        backcol = "#FFFFFF"
    from ....ski.page_class_definition import TemplatePage
    newpage = TemplatePage(name=new_name, brief=new_brief, backcol=backcol)
    css_links = fromjson.get_defaults(editedproj.proj_ident, key="css_links")
    js_links = fromjson.get_defaults(editedproj.proj_ident, key="js_links")
    _make_head(newpage, editedproj.proj_ident, new_ident, title="", css_links=css_links, js_links=js_links)
    # add this new page to the parent folder
    page = parent.add_page(newpage, new_ident)
    #  clear and re-populate call_data for edit page
    utils.no_ident_data(call_data, keep=['folder_number'])
    call_data['page'] = page
    call_data['status'] = 'Page %s added' % (new_name,)


def submit_new_svg(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Create a new svg page"
    editedproj = call_data['editedproj']
    adminproj = call_data['adminproj']
    # first get submitted data for the new page
    parent, new_ident, new_name, new_brief = _check_data(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang)
    # create a new page and add to the given parent folder
    from ....ski.page_class_definition import SVG
    if 'width' in call_data:
        width = call_data['width']
    else:
        width = '100'
    if 'height' in call_data:
        height = call_data['height']
    else:
        height = '100'
    page = SVG(name=new_name, brief=new_brief, width=width, height=height)
    # add this new svg to the parent folder
    parent.add_page(page, new_ident)
    #  clear and re-populate call_data for edit page
    utils.no_ident_data(call_data, keep=['folder_number'])
    call_data['page'] = page
    call_data['status'] = 'SVG %s added' % (new_name,)


def retrieve_new_svg(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Gets data for a create svg image page"
    editedproj = call_data['editedproj']
    adminproj = call_data['adminproj']

    # first get submitted data for the new page
    parent, new_ident, new_name, new_brief = _check_data(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang)

    parent_ident = str(parent.ident)

    page_data[("adminhead","page_head","large_text")] = "Add SVG image page to : %s" % (parent.url,)
    page_data[("adminhead","page_head","small_text")] = "Choose options to create the svg page:"

    # information paragraphs
    page_data[('page_name_text','para_text')] = "New page name : " + new_name
    page_data[('page_brief_text','para_text')] = "Description   : " + new_brief

    # information hidden fields
    page_data[('dimensions','hidden_field1')] = parent_ident
    page_data[('dimensions','hidden_field2')] = new_name
    page_data[('dimensions','hidden_field3')] = new_brief
    page_data[('dimensions','hidden_field4')] = new_ident


def submit_new_css(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Create a new css page"
    # first get submitted data for the new page
    parent, new_ident, new_name, new_brief = _check_data(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang)
    # create a new page and add to the given parent folder
    page = CSS(name=new_name, brief=new_brief, style={})
    # add this new css to the parent folder
    parent.add_page(page, new_ident)
    #  clear and re-populate call_data for edit page
    utils.no_ident_data(call_data, keep=['folder_number'])
    # add new page ident to call_data so the page can be edited
    call_data['page'] = str(page.ident)
    call_data['status'] = 'CSS page %s added' % (new_name,)


def submit_new_json(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Create a new json page"
    # first get submitted data for the new page
    parent, new_ident, new_name, new_brief = _check_data(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang)
    # create a new page and add to the given parent folder
    page = JSON(name=new_name, brief=new_brief)
    # add this new json page to the parent folder
    parent.add_page(page, new_ident)
    #  clear and re-populate call_data for edit page
    utils.no_ident_data(call_data, keep=['folder_number'])
    # Currently, after adding a json page, go back to edit folder
    # however if in future it is required to go to the page edit
    # then session data will need to have the page in it, so the following line
    # will need to be inserted
    #call_data['page'] = str(page.ident)
    call_data['status'] = 'JSON page %s added' % (new_name,)


def submit_new_file(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Create a new file page"
    # first get submitted data for the new page
    parent, new_ident, new_name, new_brief = _check_data(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang)
    # get the submitted filepath this page links to
    filepath = call_data['filepath']
    # should add checks to ensure this is a valid filepath
    # create a new page and add to the given parent folder
    page = FilePage(name=new_name, brief=new_brief, filepath=filepath)
    # add this filepage to the parent folder
    parent.add_page(page, new_ident)
    #  clear and re-populate call_data for edit page
    utils.no_ident_data(call_data, keep=['folder_number'])
    call_data['status'] = 'File link page %s added' % (new_name,)


def retrieve_new_file(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Gets data for a create filepage"
    editedproj = call_data['editedproj']
    adminproj = call_data['adminproj']

    # first get submitted data for the new page
    parent, new_ident, new_name, new_brief = _check_data(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang)

    parent_ident = str(parent.ident)

    page_data[("adminhead","page_head","large_text")] = "Add File Link page to : %s" % (parent.url,)
    page_data[("adminhead","page_head","small_text")] = "Choose options to create the file page:"

    # information paragraphs
    page_data['page_name_text:para_text'] = "New page name : " + new_name
    page_data['page_brief_text:para_text'] = "Description   : " + new_brief

    # information hidden fields
    page_data['setfilepath','pagename'] = new_name
    page_data['setfilepath','pagebrief'] = new_brief
    page_data['setfilepath','pageident'] = new_ident

    # top descriptive text
    page_data['top_text:para_text'] = """The filepath set here should be relative to the projectfiles folder, so for a file
called myfile in the static directory, the path should be %s""" % (os.path.join(editedproj.proj_ident, 'static', "myfile"),)

    # the submit filepath text input
    page_data['setfilepath:input_text'] = os.path.join(editedproj.proj_ident, 'static', new_name)
    page_data['setfilepath:parent'] = parent_ident


def submit_new_responder(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Create a new responder page"
    editedproj = call_data['editedproj']
    # first get submitted data for the new page
    parent, new_ident, new_name, new_brief = _check_data(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang)
    # responder class name
    responder_class = call_data['responder_class']
    for cls in inspect.getmembers(responders, inspect.isclass):
        if cls[0] == responder_class:
            # create a responder - no data args set as yet
            responder = cls[1]()
            break
    else:
        raise FailPage("Responder to be created not found")
    # create a new page and add to the given parent folder
    page = RespondPage(name=new_name, brief=new_brief, responder=responder)
    # add this new responder to the parent folder
    parent.add_page(page, new_ident)
    #  clear and re-populate call_data for edit page
    utils.no_ident_data(call_data, keep=['folder_number'])
    # add new page ident to call_data so the page can be edited
    call_data['page'] = str(page.ident)
    call_data['status'] = 'Responder %s - type %s added' % (new_name, responder_class)


def retrieve_new_responder(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Gets data for a create respondpage"

    editedproj = call_data['editedproj']
    adminproj = call_data['adminproj']

    # first get submitted data for the new page
    parent, new_ident, new_name, new_brief = _check_data(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang)

    parent_ident = str(parent.ident)

    page_data[("adminhead","page_head","large_text")] = "Add a responder page to : %s" % (parent.url,)
    page_data[("adminhead","page_head","small_text")] = "Choose options to create the responder:"

    # information paragraphs
    page_data['page_name_text:para_text'] = "New page name : " + new_name
    page_data['page_brief_text:para_text'] = "Description   : " + new_brief

    page_data['responderlinks','buttons'] =[]

    #    buttons: col 0 is the visible text to place on the button,
    #                col 1 is the reference string of a textblock to appear in the column adjacent to the button


    for cls in inspect.getmembers(responders, inspect.isclass):
        if issubclass(cls[1], responders.Respond):
            if cls[0] == 'Respond': continue
            page_data['responderlinks','buttons'].append([cls[0],  # the name of the respond object
                                                         cls[1].description_ref()])       # textblock description ref of the responder

    # the hidden fields
    page_data['responderlinks:hidden_field1'] = parent_ident
    page_data['responderlinks:hidden_field2'] = new_name
    page_data['responderlinks:hidden_field3'] = new_brief
    page_data['responderlinks:hidden_field4'] = new_ident



def submit_copy_page(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Copy a page"
    editedproj = call_data['editedproj']
    # first get submitted data for the new page
    parent, new_ident, new_name, new_brief = _check_data(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang)
    # Get a copy of the page
    if 'copyident' not in call_data:
        raise FailPage(message = "The ident of the page to be copied has not been found", widget='copyident')
    orig_page = skiboot.from_ident(call_data['copyident'], proj_ident=editedproj.proj_ident)
    if orig_page.page_type == "Folder":
        raise FailPage(message = "Invalid item to be copied", widget='copyident')
    # check template page name
    if (orig_page.page_type == "TemplatePage") and _AND.search(new_name):
        # check name is alphanumric, dot or underscore only
        raise FailPage(message = "Templates page names must be alphanumric, dot or underscore only", widget='copyident')
    # create new page
    new_page = orig_page.copy(name=new_name, brief = new_brief)
    # add page to parent
    parent.add_page(new_page, new_ident)
    edited_folder = call_data['edited_folder']
    utils.no_ident_data(call_data)
    call_data['edited_folder'] = edited_folder
    call_data['folder_number'] = parent.ident.num
    call_data['status'] = 'Page %s added' % (new_name,)


def retrieve_new_copypage(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Gets data for a create a page copy"

    editedproj = call_data['editedproj']
    adminproj = call_data['adminproj']

    # first get submitted data for the new page
    parent, new_ident, new_name, new_brief = _check_data(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang)

    parent_ident = str(parent.ident)

    page_data[("adminhead","page_head","large_text")] = "Add a page copy to : %s" % (parent.url,)
    page_data[("adminhead","page_head","small_text")] = "Choose options to create the page copy:"

    # information paragraphs
    page_data['page_name_text:para_text'] = "New page name : " + new_name
    page_data['page_brief_text:para_text'] = "Description   : " + new_brief

    # information hidden fields
    page_data['copyident','pagename'] = new_name
    page_data['copyident','pagebrief'] = new_brief
    page_data['copyident','pageident'] = new_ident
    page_data['copyident','parent'] = parent_ident

    page_data['upload','pagename'] = new_name
    page_data['upload','pagebrief'] = new_brief
    page_data['upload','pageident'] = new_ident
    page_data['upload','parent'] = parent_ident


    # top descriptive text
    page_data['top_text:para_text'] = """To copy a page, either the ident number of an existing page to be copied is required, alternatively - a previously downloaded page definition file can be uploaded."""

    # the submit ident text input
    if 'copyident' in call_data:
        page_data['copyident','input_text'] = call_data['copyident']


def submit_upload_page(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Copy a page from uploaded file"
    editedproj = call_data['editedproj']
    # first get submitted data for the new page
    parent, new_ident, new_name, new_brief = _check_data(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang)
    if _AND.search(new_name):
        # check name is alphanumric, dot or underscore only
        raise FailPage(message = "Invalid page name", widget='upload')
    # get file contents
    if "upload" not in call_data:
        raise FailPage("upload missing from call data")
    file_contents = call_data["upload"]
    json_string = file_contents.decode(encoding='utf-8')
    # create the page
    try:
        fromjson.create_page(editedproj.proj_ident, parent.ident.num, new_ident.num, new_name, new_brief, json_string)
    except ServerError as e:
        raise FailPage(message = e.message)
    edited_folder = call_data['edited_folder']
    utils.no_ident_data(call_data)
    call_data['edited_folder'] = edited_folder
    call_data['folder_number'] = parent.ident.num
    call_data['status'] = 'Page %s added' % (new_name,)



