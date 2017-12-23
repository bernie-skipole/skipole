####### SKIPOLE WEB FRAMEWORK #######
#
# editpage.py  - page editing functions
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
#   you may not use this file except in compliance with the License.from ....ski.skiboot import *
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

"Functions implementing admin page editing"

from ....ski import skiboot, tag, widgets
from ....ski.excepts import ValidateError, FailPage, ServerError, GoTo
from ....skilift import fromjson, part_info, part_contents, editsection

from .. import utils, css_styles


def _ident_to_str(ident):
    "Returns string ident or label"
    if isinstance(ident, skiboot.Ident):
        return ident.to_comma_str()
    if ident is None:
        return ''
    return str(ident)


def retrieve_page_edit(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Retrieves data for the edit page"

    editedproj = call_data['editedproj']

    # 'edit_page' is from a form, not from session data

    if 'edit_page' in call_data:
        page = skiboot.from_ident(call_data['edit_page'])
        del call_data['edit_page']
    elif 'page_number' in call_data:
        page = skiboot.from_ident((call_data['editedprojname'], call_data['page_number']))
    elif 'page' in call_data:
        page = skiboot.from_ident(call_data['page'])
    else:
        raise FailPage(message = "page missing")

    if (not page) or (page not in editedproj):
        raise FailPage(message = "Invalid page")

    if page.page_type != 'TemplatePage':
        raise FailPage(message = "Invalid page")

    # set page into call_data
    call_data['page'] = page
    call_data['page_number'] = page.ident.num

    # fills in the data for editing page name, brief, parent, etc., 
    utils.retrieve_edit_page(call_data, page_data)

    # add links to head and body into left navigation
    call_data['extend_nav_buttons'] = [['page_head', "Head", True, ''], ['page_body', "Body", True, '']]

    # page language
    page_data[("setlang","input_text")] = page.lang

    # default error widget
    page_data[("default_e_widg","input_text")] = page.default_error_widget.to_str_tuple()

    # sets last_scroll flag
    page_data[("lastscrollcheck","checked")] = page.last_scroll

    # fills in the backcol checkbox
    if page.show_backcol:
        page_data[("backcolcheck","checked")] = True
        page_data[('red', 'disabled')] = False
        page_data[('green', 'disabled')] = False
        page_data[('blue', 'disabled')] = False
    else:
        page_data[("backcolcheck","checked")] = False
        page_data[('red', 'disabled')] = True
        page_data[('green', 'disabled')] = True
        page_data[('blue', 'disabled')] = True

    # fills in the JSON refresh checkbox
    if page.interval and page.interval_target:
        page_data[("refreshcheck","checked")] = True
        page_data[('interval', 'disabled')] = False
        page_data[('interval_target', 'disabled')] = False
        page_data[('interval', 'input_text')] = str(page.interval)
        page_data[('interval_target', 'input_text')] = _ident_to_str(page.interval_target)
    else:
        page_data[("refreshcheck","checked")] = False
        page_data[('interval', 'disabled')] = True
        page_data[('interval_target', 'disabled')] = True
        page_data[('interval', 'input_text')] = '0'
        page_data[('interval_target', 'input_text')] = ''

    r, g, b = css_styles.hex_int(page.backcol)
    page_data[('red', 'input_text')] = str(r)
    page_data[('green', 'input_text')] = str(g)
    page_data[('blue', 'input_text')] = str(b)

    # remove any unwanted fields from session call_data
    if 'location' in call_data:
        del call_data['location']
    if 'field_arg' in call_data:
        del call_data['field_arg']
    if 'validx' in call_data:
        del call_data['validx']
    if 'module' in call_data:
        del call_data['module']
    if 'widget_name' in call_data:
        del call_data['widget_name']
    if 'container' in call_data:
        del call_data['container']
    if 'widgetclass' in call_data:
        del call_data['widgetclass']



def retrieve_page_head(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Gets data for the page head"

    editedproj = call_data['editedproj']

    if 'page' in call_data:
        if call_data['page'].page_type == 'TemplatePage':
            # page given from session data
            page = call_data['page']
        else:
            raise FailPage(message = "Invalid page")
        if not page in editedproj:
            raise FailPage(message = "Invalid page")
    else:
        raise FailPage(message = "page missing")

    page_ident = str(page.ident)

    # fills in header

    page_data[("adminhead","page_head","large_text")] = page.name + ' head'

    if 'status' in call_data:
        page_data[("adminhead","page_head","small_text")] = call_data['status']
    else:
        page_data[("adminhead","page_head","small_text")] = page.brief

    call_data['extend_nav_buttons'] = [['back_to_page', "Back to page", True, '']]

    #        contents: A list for every element in the table, should be row*col lists
    #              col 0 - text string (This will be either text to display, button text, or Textblock reference)
    #               col 1 - True if this is a TextBlock, False if not
    #               col 2 - A 'style' string set on the td cell, if empty string, no style applied
    #               col 3 - Link ident, if empty, only text will be shown, not a button
    #                             if given, a link will be set with button_class applied to it
    #              col 4 - The get field value of the button link, empty string if no get field, ignored if no link ident given

    page_data['editparts', 'parts', 'cols']  = 9
    rows = 1

    if page.head.attribs:
        head_string = '<head ... >'
    else:
        head_string = '<head>'

    head_brief = page.head.brief

    if len( head_brief)>40:
        head_brief =  head_brief[:35] + '...'
    if not  head_brief:
         head_brief = '-'

    no_link = [False, '', '']
    empty = ['', False, '', '']

    contents = [
                               [head_string] + no_link,              # col 0 the <head> text
                               [ head_brief] + no_link,
                               empty,                                       # no up arrow for top line
                               empty,                                       # no up_right arrow for top line
                               empty,                                       # no down arrow for top line
                               empty,                                       # no down_right arrow for top line
                               ['Edit', False, 'width : 1%;', 'get_part_edit', 'head'],                 # edit - link to part_edit = 43101
                               ['Insert', False, 'width : 1%;text-align: center;', 'new_insert', 'head'],             # insert - link to page 43102
                               empty                                       # no remove image for top line
                            ]

    rows = utils.extendparts(rows, page.head, 'head', contents, no_link, empty)

    page_data['editparts', 'parts', 'contents']  = contents
    page_data['editparts', 'parts', 'rows']  = rows

    # remove any unwanted fields from session call_data
    if 'location' in call_data:
        del call_data['location']
    if 'field_arg' in call_data:
        del call_data['field_arg']
    if 'validx' in call_data:
        del call_data['validx']
    if 'module' in call_data:
        del call_data['module']
    if 'widget_name' in call_data:
        del call_data['widget_name']
    if 'container' in call_data:
        del call_data['container']
    if 'widgetclass' in call_data:
        del call_data['widgetclass']


def retrieve_page_body(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Gets data for the page body"

    editedproj = call_data['editedproj']

    if 'page' in call_data:
        if call_data['page'].page_type == 'TemplatePage':
            # page given from session data
            page = call_data['page']
        else:
            raise FailPage(message = "Invalid page")
        if not page in editedproj:
            raise FailPage(message = "Invalid page")
    else:
        raise FailPage(message = "page missing")

    page_ident = str(page.ident)

    page_data[("adminhead","page_head","large_text")] = page.name + ' body'

    if 'status' in call_data:
        page_data[("adminhead","page_head","small_text")] = call_data['status']
    else:
        page_data[("adminhead","page_head","small_text")] = page.brief

    call_data['extend_nav_buttons'] = [['back_to_page', "Back to page", True, '']]


    #        contents: A list for every element in the table, should be row*col lists
    #              col 0 - text string (This will be either text to display, button text, or Textblock reference)
    #               col 1 - True if this is a TextBlock, False if not
    #               col 2 - A 'style' string set on the td cell, if empty string, no style applied
    #               col 3 - Link ident, if empty, only text will be shown, not a button
    #                             if given, a link will be set with button_class applied to it
    #              col 4 - The get field value of the button link, empty string if no get field, ignored if no link ident given

    page_data['editparts', 'parts', 'cols']  = 9
    rows = 1

    if page.body.attribs:
        body_string = '<body ... >'
    else:
        body_string = '<body>'

    body_brief = page.body.brief
    if len(body_brief)>40:
        body_brief = body_brief[:35] + '...'
    if not body_brief:
        body_brief = '-'

    no_link = [False, '', '']
    empty = ['', False, '', '']

    contents = [
                   [body_string] + no_link,              # col 0 the <body> text
                   [body_brief] + no_link,
                   empty,                                       # no up arrow for top line
                   empty,                                       # no up_right arrow for top line
                   empty,                                       # no down arrow for top line
                   empty,                                       # no down_right arrow for top line
                   ['Edit', False, 'width : 1%;', 'get_part_edit', 'body'],                 # edit - link to part_edit = 43101
                   ['Insert', False, 'width : 1%;text-align: center;', 'new_insert', 'body'],             # insert - link to page 43102
                   empty                                       # no remove image for top line
                ]

    rows = utils.extendparts(rows, page.body, 'body', contents, no_link, empty)

    page_data['editparts', 'parts', 'contents']  = contents
    page_data['editparts', 'parts', 'rows']  = rows

    # remove any unwanted fields from session call_data
    if 'location' in call_data:
        del call_data['location']
    if 'field_arg' in call_data:
        del call_data['field_arg']
    if 'validx' in call_data:
        del call_data['validx']
    if 'module' in call_data:
        del call_data['module']
    if 'widget_name' in call_data:
        del call_data['widget_name']
    if 'container' in call_data:
        del call_data['container']
    if 'widgetclass' in call_data:
        del call_data['widgetclass']


def retrieve_svgpage_edit(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Retrieves widget data for the svg edit page"
    editedproj = call_data['editedproj']

    # 'edit_page' is from a form, not from session data

    if 'edit_page' in call_data:
        page = skiboot.from_ident(call_data['edit_page'])
        del call_data['edit_page']
    elif 'page_number' in call_data:
        page = skiboot.from_ident((call_data['editedprojname'], call_data['page_number']))
    elif 'page' in call_data:
        page = skiboot.from_ident(call_data['page'])
    else:
        raise FailPage(message = "page missing")

    if (not page) or (page not in editedproj):
        raise FailPage(message = "Invalid page")

    if page.page_type != 'SVG':
        raise FailPage(message = "Invalid page")

    # set page into call_data
    call_data['page'] = page
    call_data['page_number'] = page.ident.num

    # fills in the data for editing page name, brief, parent, etc., 
    utils.retrieve_edit_page(call_data, page_data)

    # add link to svg into left navigation
    call_data['extend_nav_buttons'] = [['page_svg', "SVG", True, '']]

    page_data['enable_cache:radio_checked'] = page.enable_cache

    # remove any unwanted fields from session call_data
    if 'location' in call_data:
        del call_data['location']
    if 'field_arg' in call_data:
        del call_data['field_arg']
    if 'validx' in call_data:
        del call_data['validx']
    if 'module' in call_data:
        del call_data['module']
    if 'widget_name' in call_data:
        del call_data['widget_name']
    if 'container' in call_data:
        del call_data['container']
    if 'widgetclass' in call_data:
        del call_data['widgetclass']


def retrieve_page_svg(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Gets data for the page svg part"

    editedproj = call_data['editedproj']

    if 'page' in call_data:
        if call_data['page'].page_type == 'SVG':
            # page given from session data
            page = call_data['page']
        else:
            raise FailPage(message = "Invalid page")
        if not page in editedproj:
            raise FailPage(message = "Invalid page")
    else:
        raise FailPage(message = "page missing")

    page_ident = str(page.ident)

    # fills in header

    page_data[("adminhead","page_head","large_text")] = "Edit: " + page.name

    if 'status' in call_data:
        page_data[("adminhead","page_head","small_text")] = call_data['status']
    else:
        page_data[("adminhead","page_head","small_text")] = page.brief

    call_data['extend_nav_buttons'] = [['back_to_svgpage', "Back to page", True, '']]

    #        contents: A list for every element in the table, should be row*col lists
    #              col 0 - text string (This will be either text to display, button text, or Textblock reference)
    #               col 1 - True if this is a TextBlock, False if not
    #               col 2 - A 'style' string set on the td cell, if empty string, no style applied
    #               col 3 - Link ident, if empty, only text will be shown, not a button
    #                             if given, a link will be set with button_class applied to it
    #              col 4 - The get field value of the button link, empty string if no get field, ignored if no link ident given

    page_data['editparts', 'parts', 'cols']  = 9
    rows = 1

    if page.svg.attribs:
        svg_string = '<svg ... >'
    else:
        svg_string = '<svg>'

    svg_brief = page.svg.brief

    if len( svg_brief)>40:
        svg_brief =  svg_brief[:35] + '...'
    if not svg_brief:
         svg_brief = '-'

    no_link = [False, '', '']
    empty = ['', False, '', '']

    contents = [
                   [svg_string] + no_link,              # col 0 the <svg> text
                   [svg_brief] + no_link,
                   empty,                                       # no up arrow for top line
                   empty,                                       # no up_right arrow for top line
                   empty,                                       # no down arrow for top line
                   empty,                                       # no down_right arrow for top line
                   ['Edit', False, 'width : 1%;', 'get_part_edit', 'svg'],                 # edit - link to part_edit = 43101
                   ['Insert', False, 'width : 1%;text-align: center;', 'new_insert', 'svg'],             # insert - link to page 43102
                   empty                                       # no remove image for top line
                ]

    rows = utils.extendparts(rows, page.svg, 'svg', contents, no_link, empty)

    page_data['editparts', 'parts', 'contents']  = contents
    page_data['editparts', 'parts', 'rows']  = rows

    # remove any unwanted fields from session call_data
    if 'location' in call_data:
        del call_data['location']
    if 'field_arg' in call_data:
        del call_data['field_arg']
    if 'validx' in call_data:
        del call_data['validx']
    if 'module' in call_data:
        del call_data['module']
    if 'widget_name' in call_data:
        del call_data['widget_name']
    if 'container' in call_data:
        del call_data['container']
    if 'widgetclass' in call_data:
        del call_data['widgetclass']


def set_html_lang(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Sets page background colour in the html tag"
    editedproj = call_data['editedproj']

    if 'page' in call_data:
        if call_data['page'].page_type == 'TemplatePage':
            # page given from session data
            page = call_data['page']
        else:
            raise FailPage(message = "Invalid page")
        if not page in editedproj:
            raise FailPage(message = "Invalid page")
    else:
        raise FailPage(message = "page missing")
    if 'setlang' not in call_data:
        raise FailPage(message = "Invalid language")
    page.lang = call_data['setlang']
    # save the page
    utils.save(call_data, page=page, widget_name="setlang")
    call_data['status'] = "Page lang set to %s" % call_data['setlang']


def submit_backcol(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Sets page background colour"
    editedproj = call_data['editedproj']

    if 'page' in call_data:
        if call_data['page'].page_type == 'TemplatePage':
            # page given from session data
            page = call_data['page']
        else:
            raise FailPage(message = "Invalid page")
        if not page in editedproj:
            raise FailPage(message = "Invalid page")
    else:
        raise FailPage(message = "page missing")

    try:
        if ('enabled' not in call_data) or (not call_data['enabled']):
            # disable the background colour
            page.show_backcol = False
            text = 'Page background color not applied'
        else:
            page.show_backcol = True
            r = int(call_data['red'])
            g = int(call_data['green'])
            b = int(call_data['blue'])
            if r<0 or r>255: r=0
            if g<0 or g>255: g=0
            if b<0 or b>255: b=0
            page.backcol = css_styles.int_hex(r, g, b)
            text = 'Page background color set to %s' % page.backcol
    except:
        raise FailPage(message="Invalid background colour", widget="backcol")
    # save the page
    utils.save(call_data, page=page, widget_name="backcol")
    call_data['status'] = text


def submit_last_scroll(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Sets page last_scroll flag"

    editedproj = call_data['editedproj']

    if 'page' in call_data:
        if call_data['page'].page_type == 'TemplatePage':
            # page given from session data
            page = call_data['page']
        else:
            raise FailPage(message = "Invalid page")
        if not page in editedproj:
            raise FailPage(message = "Invalid page")
    else:
        raise FailPage(message = "page missing")

    try:
        if ('scroll' not in call_data) or (not call_data['scroll']):
            # disable the last_scroll flag
            page.last_scroll = False
            text = 'Page will not display at previous scroll position'
        else:
            page.last_scroll = True
            text = 'Page will be displayed at the last scroll position'
    except:
        raise FailPage(message="Error setting last_scroll")
    # save the page
    utils.save(call_data, page=page)
    call_data['status'] = text


def submit_refresh(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Sets JSON refresh facility"

    editedproj = call_data['editedproj']

    if 'page' in call_data:
        if call_data['page'].page_type == 'TemplatePage':
            # page given from session data
            page = call_data['page']
        else:
            raise FailPage(message = "Invalid page")
        if not page in editedproj:
            raise FailPage(message = "Invalid page")
    else:
        raise FailPage(message = "page missing")

    interval = 0
    interval_target = None

    try:
        if ('refreshcheck', 'checkbox') not in call_data:
            interval = 0
        elif call_data['refreshcheck', 'checkbox'] != 'enable_refresh':
            interval = 0
        elif ('interval', 'input_text') not in call_data:
            interval = 0
        elif call_data['interval', 'input_text'] == '0':
            interval = 0
        elif ('interval_target', 'input_text') not in call_data:
            interval = 0
        elif not call_data['interval_target', 'input_text']:
            interval = 0
        else:
            interval = int(call_data['interval', 'input_text'])
            interval_target = skiboot.make_ident_or_label(call_data['interval_target', 'input_text'], proj_ident=editedproj.proj_ident)
    except:
        raise FailPage(message="Error setting JSON refresh")
    # set page attributes
    if (interval == 0) or (not interval_target):
        text = 'JSON refresh facility disabled'
        page.interval = 0
        page.interval_target = None
    else:
        text = 'JSON refresh facility enabled'
        page.interval = interval
        # if interval target is an ident of this project, only store an integer
        if isinstance(interval_target, skiboot.Ident):
            if interval_target.proj == editedproj.proj_ident:
                page.interval_target = interval_target.num
            else:
                # ident is another project, put the full ident
                page.interval_target = interval_target.to_comma_str()
        else:
            page.interval_target = interval_target

    # save the page
    utils.save(call_data, page=page)
    call_data['status'] = text


def submit_default_error_widget(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Sets page default_error_widget"

    editedproj = call_data['editedproj']

    if 'page' in call_data:
        if call_data['page'].page_type == 'TemplatePage':
            # page given from session data
            page = call_data['page']
        else:
            raise FailPage(message = "Invalid page")
        if not page in editedproj:
            raise FailPage(message = "Invalid page")
    else:
        raise FailPage(message = "page missing")

    if ('e_widg' not in call_data) or (not call_data['e_widg']):
        raise FailPage(message="Error setting default error widget")
    page.default_error_widget = call_data['e_widg']
    # save the page
    utils.save(call_data, page=page)
    call_data['status'] = "default error widget set"


def move_up(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Move part in the page or section up"
    editedproj = call_data['editedproj']

    # get data
    bits = utils.get_bits(call_data)

    page = bits.page
    section = bits.section
    widget = bits.widget
    container = bits.container
    location = bits.location
    part = bits.part

    if (page is None) and (section is None):
        raise FailPage("Page/section not identified")

    if part is None:
        raise FailPage("Part not identified")

    label = None
    # top used to specify part from which location is deleted
    top = None

    if page is not None:
        if (page.page_type != 'TemplatePage') and (page.page_type != 'SVG'):
            raise FailPage(message = "Invalid page")
        # page to go back to
        if bits.part_top == 'head':
            label = "page_head"   # label to 3320
            top = page.head
        elif bits.part_top == 'body':
            label = "page_body"   # label to 3340
            top = page.body
        elif bits.part_top == 'svg':
            label = "page_svg"   # label to 3420
            top = page.svg

    if section is not None:
        if bits.part_top == bits.section_name:
            label = "back_to_section"   # label to 7040
            top = section

    # could be a widget container
    if label is None:
        if (widget is not None) and (container is not None) and (bits.part_top == widget.name): 
            label = "back_to_container"   # label to 44704
            top = widget.get_container_part(container)
            part_integers = location[2]
        else:
            raise FailPage("Invalid location")
    else:
        part_integers = location[2]

    if (len(part_integers) == 1) and (part_integers[0] == 0):
        # at top, cannot be moved
        raise FailPage("Cannot be moved up")
    if part_integers[-1] == 0:
        # move up to next level
        new_location = (location[0], location[1], location[2][:-1])
    else:
        # swap parts on same level
        new_index = list(part_integers[:-1])
        new_index.append(part_integers[-1] - 1)
        new_location = (location[0], location[1], new_index)

    # delete part from current location
    top.del_location_value(part_integers)
    # insert it into new location
    top.insert_location_value(new_location[2], part)

    # after a move, location is wrong, so remove from call_data
    if 'location' in call_data:
        del call_data['location']
    if 'part' in call_data:
        del call_data['part']
    if 'part_top' in call_data:
        del call_data['part_top']
    if 'part_loc' in call_data:
        del call_data['part_loc']
    utils.save(call_data, page=page, section_name=bits.section_name, section=section)
    raise GoTo(target = label, clear_submitted=True)


def move_up_right(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Move part in the page or section up and right"

    editedproj = call_data['editedproj']

    # get data
    bits = utils.get_bits(call_data)

    page = bits.page
    section = bits.section
    widget = bits.widget
    container = bits.container
    location = bits.location
    part = bits.part

    if (page is None) and (section is None):
        raise FailPage("Page/section not identified")

    if part is None:
        raise FailPage("Part not identified")

    label = None
    # top used to specify part from which location is deleted
    top = None

    if page is not None:
        if (page.page_type != 'TemplatePage') and (page.page_type != 'SVG'):
            raise FailPage(message = "Invalid page")
        # page to go back to
        if bits.part_top == 'head':
            label = "page_head"   # label to 3320
            top = page.head
        elif bits.part_top == 'body':
            label = "page_body"   # label to 3340
            top = page.body
        elif bits.part_top == 'svg':
            label = "page_svg"   # label to 3420
            top = page.svg

    if section is not None:
        if bits.part_top == bits.section_name:
            label = "back_to_section"   # label to 7040
            top = section

    # could be a widget container
    if label is None:
        if (widget is not None) and (container is not None) and (bits.part_top == widget.name): 
            label = "back_to_container"   # label to 44704
            top = widget.get_container_part(container)
            part_integers = location[2]
        else:
            raise FailPage("Invalid location")
    else:
        part_integers = location[2]

    if part_integers[-1] == 0:
        # at top of a part, cannot be moved
        raise FailPage("Cannot be moved up")
    new_parent_index = list(part_integers[:-1])
    new_parent_index.append(part_integers[-1] - 1)
    new_parent = top.get_location_value(new_parent_index)
    if new_parent is None:
        raise FailPage("Cannot be moved up")
    if not isinstance(new_parent, tag.Part):
        raise FailPage("Cannot be moved up")
    if isinstance(new_parent, widgets.Widget):
        raise FailPage("Cannot be moved up")
    new_location =  (location[0], location[1], tuple(new_parent_index + [len(new_parent)]))

    # delete part from current location
    top.del_location_value(part_integers)
    # insert it into new location
    top.insert_location_value(new_location[2], part)

    # after a move, location is wrong, so remove from call_data
    if 'location' in call_data:
        del call_data['location']
    if 'part' in call_data:
        del call_data['part']
    if 'part_top' in call_data:
        del call_data['part_top']
    if 'part_loc' in call_data:
        del call_data['part_loc']
    utils.save(call_data, page=page, section_name=bits.section_name, section=section)
    raise GoTo(target = label, clear_submitted=True)


def move_down(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Move part in the page or section down"

    editedproj = call_data['editedproj']

    # get data
    bits = utils.get_bits(call_data)

    page = bits.page
    section = bits.section
    widget = bits.widget
    container = bits.container
    location = bits.location
    part = bits.part

    if (page is None) and (section is None):
        raise FailPage("Page/section not identified")

    if part is None:
        raise FailPage("Part not identified")

    label = None
    # top used to specify part from which location is deleted
    top = None

    if page is not None:
        if (page.page_type != 'TemplatePage') and (page.page_type != 'SVG'):
            raise FailPage(message = "Invalid page")
        # page to go back to
        if bits.part_top == 'head':
            label = "page_head"   # label to 3320
            top = page.head
        elif bits.part_top == 'body':
            label = "page_body"   # label to 3340
            top = page.body
        elif bits.part_top == 'svg':
            label = "page_svg"   # label to 3420
            top = page.svg

    if section is not None:
        if bits.part_top == bits.section_name:
            label = "back_to_section"   # label to 7040
            top = section

    # could be a widget container
    if label is None:
        if (widget is not None) and (container is not None) and (bits.part_top == widget.name): 
            label = "back_to_container"   # label to 44704
            top = widget.get_container_part(container)
            part_integers = location[2]
        else:
            raise FailPage("Invalid location")
    else:
        part_integers = location[2]


    if len(part_integers) == 1:
        # Just at immediate level below top
        if part_integers[0] == (len(top) -1):
            # At end, cannot be moved
            raise FailPage("Cannot be moved down")
        new_location = (location[0], location[1], (part_integers[0]+2,))
    else:
        parent_index = list(part_integers[:-1])
        parent = top.get_location_value(parent_index)
        if part_integers[-1] == (len(parent)-1):
            # At end of a part, so move up a level
            new_index = list(parent_index[:-1])
            new_index.append(parent_index[-1] + 1)
            new_location =  (location[0], location[1],tuple(new_index))
        else:
            # just insert into current level
            parent_index.append(part_integers[-1] + 2)
            new_location =  (location[0], location[1], tuple(parent_index))


    # insert it into new location
    top.insert_location_value(new_location[2], part)
    # delete part from current location
    top.del_location_value(part_integers)

    # after a move, location is wrong, so remove from call_data
    if 'location' in call_data:
        del call_data['location']
    if 'part' in call_data:
        del call_data['part']
    if 'part_top' in call_data:
        del call_data['part_top']
    if 'part_loc' in call_data:
        del call_data['part_loc']
    utils.save(call_data, page=page, section_name=bits.section_name, section=section)
    raise GoTo(target = label, clear_submitted=True)


def move_down_right(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Move part in the page or section down and to the right"

    editedproj = call_data['editedproj']

    # get data
    bits = utils.get_bits(call_data)

    page = bits.page
    section = bits.section
    widget = bits.widget
    container = bits.container
    location = bits.location
    part = bits.part

    if (page is None) and (section is None):
        raise FailPage("Page/section not identified")

    if part is None:
        raise FailPage("Part not identified")

    label = None
    # top used to specify part from which location is deleted
    top = None

    if page is not None:
        if (page.page_type != 'TemplatePage') and (page.page_type != 'SVG'):
            raise FailPage(message = "Invalid page")
        # page to go back to
        if bits.part_top == 'head':
            label = "page_head"   # label to 3320
            top = page.head
        elif bits.part_top == 'body':
            label = "page_body"   # label to 3340
            top = page.body
        elif bits.part_top == 'svg':
            label = "page_svg"   # label to 3420
            top = page.svg

    if section is not None:
        if bits.part_top == bits.section_name:
            label = "back_to_section"   # label to 7040
            top = section

    # could be a widget container
    if label is None:
        if (widget is not None) and (container is not None) and (bits.part_top == widget.name): 
            label = "back_to_container"   # label to 44704
            top = widget.get_container_part(container)
            part_integers = location[2]
        else:
            raise FailPage("Invalid location")
    else:
        part_integers = location[2]


    if len(part_integers) == 1:
        parent = top
    else:
        parent_index = list(part_integers[:-1])
        parent = top.get_location_value(parent_index)
    if part_integers[-1] == (len(parent) -1):
        # At end of a block, cannot be moved
        raise FailPage("Cannot be moved down - 882")
    new_parent_index = list(part_integers[:-1])
    new_parent_index.append(part_integers[-1] + 1)
    new_parent = top.get_location_value(new_parent_index)
    if new_parent is None:
        raise FailPage("Cannot be moved down")
    if not isinstance(new_parent, tag.Part):
        raise FailPage("Cannot be moved down")
    if isinstance(new_parent, widgets.Widget):
        raise FailPage("Cannot be moved down")
    new_location = (location[0], location[1], tuple(new_parent_index+[0]))

    # insert it into new location
    top.insert_location_value(new_location[2], part)
    # delete part from current location
    top.del_location_value(part_integers)

    # after a move, location is wrong, so remove from call_data
    if 'location' in call_data:
        del call_data['location']
    if 'part' in call_data:
        del call_data['part']
    if 'part_top' in call_data:
        del call_data['part_top']
    if 'part_loc' in call_data:
        del call_data['part_loc']
    utils.save(call_data, page=page, section_name=bits.section_name, section=section)
    raise GoTo(target = label, clear_submitted=True)


def remove_part(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Removes a part"

    editedproj = call_data['editedproj']

    # get data
    bits = utils.get_bits(call_data)

    page = bits.page
    section = bits.section
    widget = bits.widget
    container = bits.container
    location = bits.location

    # once item is deleted, no info on the item should be
    # left in call_data
    if 'location' in call_data:
        del call_data['location']
    if 'part' in call_data:
        del call_data['part']
    if 'part_loc' in call_data:
        del call_data['part_loc']

    # label used in GoTo jump to return to the point where item is inserted
    label = None
    # top used to specify part from which location is deleted
    top = None

    if page is not None:
        call_data['page'] = page
        if (page.page_type != 'TemplatePage') and (page.page_type != 'SVG'):
            raise FailPage(message = "Invalid page")
        # page to go back to
        if bits.part_top == 'head':
            label = "page_head"   # label to 3320
            top = page.head
        elif bits.part_top == 'body':
            label = "page_body"   # label to 3340
            top = page.body
        elif bits.part_top == 'svg':
            label = "page_svg"   # label to 3420
            top = page.svg

    if section is not None:
        if bits.part_top == bits.section_name:
            label = "back_to_section"   # label to 7040
            top = section

    # could be a widget container
    if label is None:
        if (widget is not None) and bits.part_top == widget.name: 
            label = "back_to_container"   # label to 44704
        else:
            raise FailPage("Invalid location")

    if (top is None) and (container is None):
        raise FailPage("Invalid location")

    # remove the item
    try:
        if top is None:
            # delete from widget container
            widget.del_from_container(location[1], location[2])
            call_data['location'] = (bits.part_top, location[1], ())
        else:
            top.del_location_value(location[2])
    except:
        raise FailPage("Unable to delete item")

    utils.save(call_data, page=page, section_name=bits.section_name, section=section)

    call_data['status'] = 'Item deleted'
    raise GoTo(target = label, clear_submitted=True)


def submit_cache(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Sets cache true or false"
    # the page to have a new mimetype should be given by session data
    if 'page' not in call_data:
        raise FailPage(message = "page missing")
    page = call_data['page']
    if page.page_type != 'SVG':
        raise ValidateError("Invalid page type")
    if not 'cache' in call_data:
        raise FailPage(message="No cache instruction given", widget="cache_submit")
    # Set the page cache
    if call_data['cache'] == 'True':
        page.enable_cache = True
        message = "Cache Enabled"
    else:
        page.enable_cache = False
        message = "Cache Disabled"
    # save the altered page in the database
    utils.save(call_data, page=page, widget_name='cache_submit')
    call_data['status'] = message


################## JSON PAGE #############################


def retrieve_edit_jsonpage(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Retrieves widget data for the edit json page"
    editedproj = call_data['editedproj']

    # 'edit_page' is from a form, not from session data

    if 'edit_page' in call_data:
        page = skiboot.from_ident(call_data['edit_page'])
        del call_data['edit_page']
    elif 'page_number' in call_data:
        page = skiboot.from_ident((call_data['editedprojname'], call_data['page_number']))
    elif 'page' in call_data:
        page = skiboot.from_ident(call_data['page'])
    else:
        raise FailPage(message = "page missing")

    if (not page) or (page not in editedproj):
        raise FailPage(message = "Invalid page")

    if page.page_type != 'JSON':
        raise FailPage(message = "Invalid page")

    # set page into call_data
    call_data['page'] = page
    call_data['page_number'] = page.ident.num

    # fills in the data for editing page name, brief, parent, etc., 
    utils.retrieve_edit_page(call_data, page_data)

    page_data['enable_cache:radio_checked'] = page.enable_cache

    if page.content:
        # If page has contents, show the table of widgfields, values
        contents = []
        for widgfield,value in page.content.items():
            wf = skiboot.make_widgfield(widgfield)
            if not wf:
                continue
            wfstrtuple = wf.to_str_tuple()
            if value is True:
                contents.append([wfstrtuple,'True',widgfield])
            elif value is False:
                contents.append([wfstrtuple,'False',widgfield])
            else:
                contents.append([wfstrtuple,value,widgfield])
        if contents:
            page_data['field_values_list','show'] = True
            page_data['field_values_list','contents'] = contents
        else:
            page_data['field_values_list','show'] = False
    else:
        page_data['field_values_list','show'] = False


def set_json_cache(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Sets cache true or false"
    if 'page' not in call_data:
        raise FailPage(message = "page missing")
    page = call_data['page']
    if page.page_type != 'JSON':
        raise FailPage("Invalid page type")
    if not ('enable_cache', 'radio_checked') in call_data:
        raise FailPage(message="No cache instruction given", widget="cache_submit")
    # Set the page cache
    if call_data[('enable_cache', 'radio_checked')] == 'True':
        page.enable_cache = True
        message = "Cache Enabled"
    else:
        page.enable_cache = False
        message = "Cache Disabled"
    # save the altered page in the database
    utils.save(call_data, page=page, widget_name='cache_submit')
    call_data['status'] = message


def remove_json_widgfield(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Removes widgfield from JSON page"
    if 'page' not in call_data:
        raise FailPage(message = "page missing")
    page = call_data['page']
    if page.page_type != 'JSON':
        raise FailPage("Invalid page type")
    if not ('field_values_list','contents') in call_data:
        raise FailPage(message="No widgfield given")
    widgfield = call_data['field_values_list','contents']
    if widgfield in page.content:
        page.del_widgfield(widgfield)
        # save the altered page in the database
        utils.save(call_data, page=page)
        call_data['status'] = "Widgfield removed"
    else:
        raise FailPage(message="Widgfield not recognised")

def add_json_widgfield(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Adds a widgfield to JSON page"
    if 'page' not in call_data:
        raise FailPage(message = "page missing")
    page = call_data['page']
    if page.page_type != 'JSON':
        raise FailPage("Invalid page type")
    if not ('jsonwidgfield', 'input_text') in call_data:
        raise FailPage(message="No widgfield given")
    widgfield = call_data[ 'jsonwidgfield', 'input_text']
    if call_data['jsontrue', 'button_text'] == 'True':
        value = True
    elif call_data['jsonfalse', 'button_text'] == 'False':
        value = False
    elif call_data['jsontext', 'input_text']:
        value = call_data['jsontext', 'input_text']
    else:
        value = ''
    page.add_widgfield(widgfield, value)
    # save the altered page in the database
    utils.save(call_data, page=page)
    call_data['status'] = "Widgfield added"



def downloadpage(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Gets template or SVG page, and returns a json dictionary, this will be sent as an octet file to be downloaded"
    if 'page' not in call_data:
        raise FailPage(message = "page missing")
    page = call_data['page']
    if (page.page_type != 'TemplatePage') and (page.page_type != 'SVG'):
        raise FailPage("Invalid page type")
    project = call_data['editedproj']
    jsonstring =  fromjson.page_to_json(project.proj_ident, page.ident.num, indent=4)
    line_list = []
    n = 0
    for line in jsonstring.splitlines(True):
        binline = line.encode('utf-8')
        n += len(binline)
        line_list.append(binline)
    page_data['headers'] = [('content-type', 'application/octet-stream'), ('content-length', str(n))]
    return line_list



def edit_section_dom(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Called by domtable to edit an item in a section"
    if ('editdom', 'domtable', 'contents') not in call_data:
        raise FailPage(message = "item to edit missing")
    editedprojname = call_data['editedprojname']
    part = call_data['editdom', 'domtable', 'contents']

    # so part is section name with location string of integers

    # create location which is a tuple or list consisting of three items:
    # a string of section name
    # a container integer, in this case always None
    # a tuple or list of location integers
    location_list = part.split('-')
    # first item should be a string, rest integers
    if len(location_list) == 1:
        # no location integers, so location_list[0] is the section name
        # edit the top section html part
        call_data['part'] = part
        raise GoTo(target = 53007, clear_submitted=True)

    location_integers = [ int(i) for i in location_list[1:]]
    part_tuple = part_info(editedprojname, None, location_list[0], [location_list[0], None, location_integers])
    if part_tuple is None:
        raise FailPage("Item to edit has not been recognised")

    if part_tuple.widget_name:
        # item to edit is a widget
        call_data['part'] = part                 ################ note, in future pass part_tuple rather than part
        raise GoTo(target = 54006, clear_submitted=True)  # calls a del widget_name responder, may be removable in future
    if part_tuple.part_type == "Part":
        # edit the html part
        call_data['part'] = part                 ################ note, in future pass part_tuple rather than part
        raise GoTo(target = 53007, clear_submitted=True)
    if part_tuple.part_type == "ClosedPart":
        # edit the html closed part
        call_data['part'] = part                 ################ note, in future pass part_tuple rather than part
        raise GoTo(target = 53007, clear_submitted=True)
    if part_tuple.part_type == "HTMLSymbol":
        # edit the symbol
        call_data['part'] = part                 ################ note, in future pass part_tuple rather than part
        raise GoTo(target = 51107, clear_submitted=True)
    if part_tuple.part_type == "str":
        # edit the text
        call_data['part'] = part                 ################ note, in future pass part_tuple rather than part
        raise GoTo(target = 51017, clear_submitted=True)
    if part_tuple.part_type == "TextBlock":
        # edit the TextBlock
        call_data['part'] = part                 ################ note, in future pass part_tuple rather than part
        raise GoTo(target = 52017, clear_submitted=True)
    if part_tuple.part_type == "Comment":
        # edit the Comment
        call_data['part'] = part                 ################ note, in future pass part_tuple rather than part
        raise GoTo(target = 51207, clear_submitted=True)

    # note : a sectionplaceholder cannot appear in a section
    raise FailPage("Item to edit has not been recognised")


def add_to_section_dom(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    """Called by domtable to either insert or append an item in a section
       sets page_data to populate the insert or append page and then go to appropriate template page"""

    if ('editdom', 'domtable', 'contents') not in call_data:
        raise FailPage(message = "item to edit missing")
    editedprojname = call_data['editedprojname']
    part = call_data['editdom', 'domtable', 'contents']
    location_list = part.split('-')
    # first item should be a string, rest integers
    if len(location_list) == 1:
        # no location integers, so location_list[0] is the section name
        location_integers = ()
    else:
        location_integers = tuple( int(i) for i in location_list[1:] )
    section_name = location_list[0]

    # location is a tuple of section_name, None for no container, tuple of location integers
    location = (section_name, None, location_integers)
    # get part_tuple from project, pagenumber, section_name, location
    part_tuple = part_info(editedprojname, None, section_name, location)
    if part_tuple is None:
        raise FailPage("Item to append to has not been recognised")
    # goto either the install or append page

    call_data['part'] = part                 ################ note, in future pass part_tuple rather than part
    call_data['location'] = location         ########## also part_tuple should replace location

    page_data[("adminhead","page_head","small_text")] = "Pick an item type"

    # navigator boxes
    boxes = [['back_to_section', section_name, True, '']]    # label to 7040
    if 'extend_nav_buttons' in call_data:
        call_data['extend_nav_buttons'].extend(boxes)
    else:
        call_data['extend_nav_buttons'] = boxes

    # Fill in menu of items, Part items have insert, others have append
    # as this is to be input into a section, a further section is not present in this list


    if (part_tuple.part_type == "Part") or (part_tuple.part_type == "Section"):
        # insert
        page_data[("adminhead","page_head","large_text")] = "Choose an item to insert"
        page_data[("insertlist","links")] = [
                                                ["Insert text", "inserttext", ""],
                                                ["Insert a TextBlock", "insert_textblockref", ""],
                                                ["Insert html symbol", "insertsymbol", ""],
                                                ["Insert comment", "insertcomment", ""],
                                                ["Insert an html element", "part_insert", ""],
                                                ["Insert a Widget", "list_widget_modules", ""]
                                            ]
        raise GoTo(target = '23609', clear_submitted=True)
    else:
        # append
        page_data[("adminhead","page_head","large_text")] = "Choose an item to append"
        page_data[("appendlist","links")] = [
                                                ["Append text", "inserttext", ""],
                                                ["Append a TextBlock", "insert_textblockref", ""],
                                                ["Append html symbol", "insertsymbol", ""],
                                                ["Append comment", "insertcomment", ""],
                                                ["Append an html element", "part_insert", ""],
                                                ["Append a Widget", "list_widget_modules", ""]
                                            ]
        raise GoTo(target = '23509', clear_submitted=True)


def remove_section_dom(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Called by domtable to remove an item in a section"

    if ('editdom', 'domtable', 'contents') not in call_data:
        raise FailPage(message = "item to edit missing")
    editedprojname = call_data['editedprojname']
    part = call_data['editdom', 'domtable', 'contents']

    # so part is section name with location string of integers

    # create location which is a tuple or list consisting of three items:
    # a string of section name
    # a container integer, in this case always None
    # a tuple or list of location integers
    location_list = part.split('-')
    # first item should be a string, rest integers
    if len(location_list) == 1:
        # no location integers
        raise FailPage("Item to remove has not been recognised")

    location_integers = tuple( int(i) for i in location_list[1:] )
    section_name = location_list[0]

    # location is a tuple of section_name, None for no container, tuple of location integers
    location = (section_name, None, location_integers)
    # get part_tuple from project, pagenumber, section_name, location
    part_tuple = part_info(editedprojname, None, section_name, location)
    if part_tuple is None:
        raise FailPage("Item to remove has not been recognised")

    # once item is deleted, no info on the item should be
    # left in call_data - this may not be required in future
    if 'location' in call_data:
        del call_data['location']
    if 'part' in call_data:
        del call_data['part']
    if 'part_loc' in call_data:
        del call_data['part_loc']

    # remove the item
    try:
        editsection.del_item(part_tuple)
    except ServerError as e:
        raise FailPage(message = e.message)

    call_data['status'] = 'Item deleted'


def move_up_in_section_dom(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Called by domtable to move an item in a section up"

    if ('editdom', 'domtable', 'contents') not in call_data:
        raise FailPage(message = "item to edit missing")
    editedprojname = call_data['editedprojname']
    part = call_data['editdom', 'domtable', 'contents']

    # so part is section name with location string of integers

    # create location which is a tuple or list consisting of three items:
    # a string of section name
    # a container integer, in this case always None
    # a tuple or list of location integers
    location_list = part.split('-')
    # first item should be a string, rest integers
    if len(location_list) == 1:
        # no location integers
        return
    else:
        location_integers = tuple( int(i) for i in location_list[1:] )
    section_name = location_list[0]

    # location is a tuple of section_name, None for no container, tuple of location integers
    location = (section_name, None, location_integers)
    # get part_tuple from project, pagenumber, section_name, location
    part_tuple = part_info(editedprojname, None, section_name, location)
    if part_tuple is None:
        raise FailPage("Item to move has not been recognised")

    if (len(location_integers) == 1) and (location_integers[0] == 0):
        # at top, cannot be moved
        raise FailPage("Cannot be moved up")

    if location_integers[-1] == 0:
        # move up to next level
        new_location_integers = location_integers[:-1]
    else:
        # swap parts on same level
        new_location_integers = list(location_integers[:-1])
        new_location_integers.append(location_integers[-1] - 1)

    # after a move, location is wrong, so remove from call_data
    if 'location' in call_data:
        del call_data['location']
    if 'part' in call_data:
        del call_data['part']
    if 'part_top' in call_data:
        del call_data['part_top']
    if 'part_loc' in call_data:
        del call_data['part_loc']

    # move the item
    try:
        editsection.move_item(editedprojname, section_name, location_integers, new_location_integers)
    except ServerError as e:
        raise FailPage(message = e.message)


def move_up_right_in_section_dom(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Called by domtable to move an item in a section up and to the right"

    if ('editdom', 'domtable', 'contents') not in call_data:
        raise FailPage(message = "item to edit missing")
    editedprojname = call_data['editedprojname']
    part = call_data['editdom', 'domtable', 'contents']

    # so part is section name with location string of integers

    # create location which is a tuple or list consisting of three items:
    # a string of section name
    # a container integer, in this case always None
    # a tuple or list of location integers
    location_list = part.split('-')
    # first item should be a string, rest integers
    if len(location_list) == 1:
        # no location integers, so location_list[0] is the section name
        return
    else:
        location_integers = tuple( int(i) for i in location_list[1:] )
    section_name = location_list[0]

    # location is a tuple of section_name, None for no container, tuple of location integers
    location = (section_name, None, location_integers)
    # get part_tuple from project, pagenumber, section_name, location
    part_tuple = part_info(editedprojname, None, section_name, location)
    if part_tuple is None:
        raise FailPage("Item to move has not been recognised")

    if location_integers[-1] == 0:
        # at top of a part, cannot be moved
        raise FailPage("Cannot be moved up")
    new_parent_integers = list(location_integers[:-1])
    new_parent_integers.append(location_integers[-1] - 1)
    new_parent_location = (section_name, None, new_parent_integers)

    new_parent_tuple = part_info(editedprojname, None, section_name, new_parent_location)

    if new_parent_tuple is None:
        raise FailPage("Cannot be moved up")
    if new_parent_tuple.part_type != "Part":
        raise FailPage("Cannot be moved up")

    items_in_new_parent = len(part_contents(editedprojname, None, section_name, new_parent_location))

    new_location_integers =  tuple(new_parent_integers + [items_in_new_parent])

    # after a move, location is wrong, so remove from call_data
    if 'location' in call_data:
        del call_data['location']
    if 'part' in call_data:
        del call_data['part']
    if 'part_top' in call_data:
        del call_data['part_top']
    if 'part_loc' in call_data:
        del call_data['part_loc']

    # move the item
    try:
        editsection.move_item(editedprojname, section_name, location_integers, new_location_integers)
    except ServerError as e:
        raise FailPage(message = e.message)










