####### SKIPOLE WEB FRAMEWORK #######
#
# utils.py  - some utility functions used by the skiadmin code
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

import collections, json, os, html

from ...ski import skiboot, widgets, tag
from ...ski.excepts import FailPage, ServerError
from ... import skilift


def no_ident_data(call_data, keep=None):
    "Clears call data apart from set of required values"
    required = ['editedprojname',
                'editedprojurl',
                'editedprojversion',
                'editedprojbrief',
                'editedproj',
                'adminproj',
                'extend_nav_buttons',
                'caller_ident']
    if keep:
        required.extend(keep)
    temp_storage = {key:value for key,value in call_data.items() if key in required}
    call_data.clear()
    for key,value in temp_storage.items():
        call_data[key] = value




def retrieve_edit_page(call_data, page_data):
    "Common function used by page editors, placed here to be used by multiple pages"

    page_number = call_data['page_number']
    editedprojname = call_data['editedprojname']
    info = skilift.item_info(editedprojname, page_number)

    # fills in header
    page_data[("adminhead","page_head","large_text")] = info.name
    if ("adminhead","page_head","small_text") not in page_data:
        page_data[("adminhead","page_head","small_text")] = info.brief

    page_data[('page_edit','p_ident','page_ident')] = (editedprojname,page_number)
    page_data[('page_edit','p_name','page_ident')] = (editedprojname,page_number)
    page_data[('page_edit','p_description','page_ident')] = (editedprojname,page_number)

    if "new_name" in call_data:
        page_data[('page_edit','p_rename','input_text')] = call_data["new_name"]
    else:
        page_data[('page_edit','p_rename','input_text')] = info.name

    page_data[('page_edit','p_parent','input_text')] = "%s,%s" % (editedprojname, info.parentfolder_number)

    if 'page_brief' in call_data:
        page_data[('page_edit','p_brief','input_text')] = call_data['page_brief']
    else:
        page_data[('page_edit','p_brief','input_text')] = info.brief


def save(call_data, page=None, section_name=None, section=None, widget_name=''):
    "Saves given items, widget_name is the widget to display an error"
    editedproj = call_data['editedproj']
    try:
        if page is not None:
            # save the altered page
            editedproj.save_page(page)
        if section is not None:
            # save the altered section
           editedproj.add_section(section_name, section)
    except ServerError as e:
        if (page is not None) and ('page' in call_data):
            # replace call_data['page'] with new value
            call_data['page'] = skiboot.from_ident(page.ident, import_sections=False)
        if (section is not None) and ('section_part' in call_data):
            # replace call_data['section_part'] with new value
            section = editedproj.section(section_name)
            call_data['section_part'] = section
        raise FailPage(message=e.message, widget=widget_name)


def _location_from_part_string(part_string, section_name):
    """part_string is a location string such as head-0-1, this returns a location tuple
          consisting of the leading string (such as head or section name or widget name)
                                  container integer, such as 0 for container 0, or None if no container
                                  and tuple of location integers"""
    location_list = part_string.split('-')
    # first item should be a string, rest integers, but section or widget could have a name 'this_name'
    location_string = location_list[0]
    if len(location_list) == 1:
        # no location integers
        return (location_string, None, ())
    location_integers = [ int(i) for i in location_list[1:]]
    if not section_name:
        # either a location or widget in a page
        if (location_string =='head') or (location_string =='body') or  (location_string =='svg'):
            # No widget, no container    
            return (location_string, None, tuple(location_integers))
    else:
        # so must be a section
        if location_string == section_name:
            # No widget, no container
            return (location_string, None, tuple(location_integers))
    # so location_string must be a widget name, and first integer is a container   
    if len(location_integers) == 1:
        # must be a location of a widget container
        return (location_string, location_integers[0], ())
    # must be a location within a widget container
    return (location_string, location_integers[0], tuple(location_integers[1:]))


def _part_string_from_location(location):
    """Inverse of the above"""
    part_string = location[0]
    if location[1] is not None:
        part_string = part_string + '-' + str(location[1])
    if location[2]:
        stringlist = [str(i) for i in location[2]]
        part_string = part_string + '-' + '-'.join(stringlist)
    return part_string


def part_from_location(page=None, section=None, section_name=None, location_string='', container=None, location_integers=()):
    "Returns the part given the location information, if not found, return None"
    if (page is None) and (section is None):
        return

    if page is not None:
        if (location_string == 'head') or (location_string == 'body') or (location_string == 'svg'):
            return page.get_part(location_string, location_integers)
        elif location_string in page.widgets:
            widget = page.widgets[location_string]
            if widget is not None:
                # widget is the containing widget 
                if widget.can_contain() and not (container is None):
                    return widget.get_from_container(container, location_integers)

    if section is not None:
        if location_string == section_name:
            if location_integers:
                return section.get_location_value(location_integers)
            else:
                return section
        elif location_string in section.widgets:
            widget = section.widgets[location_string]
            if widget is not None:
                # widget is the containing widget 
                if widget.can_contain() and not (container is None):
                    return widget.get_from_container(container, location_integers)


def set_part(newpart, location, page=None, section=None, section_name='', widget=None, failmessage=''):
    "Sets a part in a location"
    part_top, container, location_tuple = location
    if (page is None) and (section is None):
        raise FailPage(failmessage)
    if page is None:
        # set part in a section
        if part_top == section_name:
            # part is not embedded in a widget
            section.set_location_value(location_tuple, newpart)
        elif (widget is not None) and part_top == widget.name: 
            # location is in a widget, within a container
            widget.set_in_container(container, location_tuple, newpart)
        else:
            raise FailPage(failmessage)
    else:
        # set part in a page
        if (part_top == 'head'):
            page.head.set_location_value(location_tuple, newpart)
        elif (part_top == 'body'):
            page.body.set_location_value(location_tuple, newpart)
        elif (part_top == 'svg'):
            page.svg.set_location_value(location_tuple, newpart)
        elif (widget is not None) and part_top == widget.name: 
            # location is in a container
            widget.set_in_container(container, location_tuple, newpart)
        else:
            raise FailPage(failmessage)
 

def get_bits(call_data):
    """Returns a named tuple of (page, section, section_name, widget, location,
                                 part, part_top, part_string, field, field_arg, validator)
       if obtainable from call_data, with None for any bit unable to find"""

    Bits = collections.namedtuple('Bits', ['page',
                                           'section',
                                           'section_name',
                                           'parent_widget',
                                           'parent_container',  # an integer
                                           'widget',
                                           'location',
                                           'container',     # an integer
                                           'part',          # submitted part
                                           'container_part',# submitted container index
                                           'part_top',      # a string such as 'head' or widgename
                                           'page_top',      # a string 'head', 'body', 'svg' or None
                                           'part_string',   # a string such as 'head_0_1'
                                           'field',
                                           'field_arg',
                                           'validator'])

    # note: call_data['part'] is from a form, something like head_0_1, or sessionname_0_1 or widgetname_0_1
    # if given then this has precedence, and replaces any session 'location' data, if not given, session location is used. 

    # location is a list of leading string 'head', 'body', 'svg' or section name
    #                                          second string of widget_name
    #                                          container integer, such as 0 for container 0, or None if no container
    #                                          and tuple of location integers

    page=None               # The page instance, mutually exclusive with
    section = None          # The section instance
    section_name = None     # The section name
    parent_widget = None    # the parent widget if any
    parent_container = None # the container integer of the parent widget containing edited widget
    widget = None           # widget instance retrieved from call_data['widget_name']
    location = None         # location list, derived from session data 'part' or session data 'location'  
    container = None        # container integer, retrieved from call_data['container']
    part = None             # The part instance at location, derived from submitted 'part' or session data location
    container_part = None   # The integer submitted when a user decides to edit a container
    part_top = None         # The string such as 'head', 'body', 'svg',  widgetname
    page_top = None         # derived from part_top and widget ident, None if this is a section
    part_string = None      # The string such as 'head_0_1' derived from call_data['part'] or from session data location
    field = None            # field instance, derived from field_arg and widget
    field_arg = None        # Derived from form call_data['field_arg'], checked exists in widget, if not then None
    validator = None        # Derived from form call_data['validx'], field and widget, if not then None


    editedprojname = call_data['editedprojname']
    editedproj = skiboot.getproject(editedprojname)

    # get page or section - an error if both are present
    if 'page' in call_data:
        if 'section_name' in call_data:
            raise FailPage(message = "Section and page both present in session data")
        page = call_data['page']
        if (page.page_type != 'TemplatePage') and (page.page_type != 'SVG'):
            raise FailPage(message = "Invalid page")
    elif 'section_name' in call_data:
        if 'section' not in call_data:
            raise FailPage(message = "Section part not valid")
        section_name = call_data['section_name']
        section = call_data['section']
    else:
        return Bits(None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None)

    # 'widget' is from session data
    if 'widget_name' in call_data:
        widget_name = call_data['widget_name']
        if section:
            widget = section.widgets.get(widget_name)
        else:
            widget = page.widgets.get(widget_name)
        if widget:
            part_top = widget.name

    # 'container' is from session data, only valid if 'widget' is present
    if (widget is not None) and ('container' in call_data):
        container = call_data['container']

    # 'container_part' is from submitted data
    if 'container_part' in call_data:
        try:
            container_part = int(call_data['container_part'])
        except:
            container_part = None

    # get location and part_string from 'part' in call data - 'part' provided by responder from submitted data 
    if 'part' in call_data:
        # part is a location string such as head-0-1, or sectionname-0-1 or widgetname-0-1
        # put this into part_string, and into call_data['location']
        if call_data['part']:
            part_string = call_data['part']
            call_data['location'] = _location_from_part_string(part_string, section_name)

    elif ('part_top' in call_data) and ('part_loc' in call_data):
        # 'part_top' is the string top of a location such as 'head' or 'widgetname'
        # 'part_loc' is the string location, such as '0-1', could be empty
        if call_data['part_top'] and call_data['part_loc']:
            part_string = call_data['part_top'] + '-' + call_data['part_loc']
        elif call_data['part_top']:
             # part_loc is empty, only have the name
            part_string = call_data['part_top']
        call_data['location'] = _location_from_part_string(part_string, section_name)

    # 'part' may not be given, but 'location' may be given from stored session data
    # so use this location, derived either from 'part' or from 'location',
    # to generate part_string, part_top and part

    if 'location' in call_data:
        location = call_data['location']

        # the part text
        part_top = location[0]
        # the part sequence numbers
        if not part_string:
            part_string = _part_string_from_location(location)
        # got location, part_top and part_string

        # get part
        part_from_loc = part_from_location(page, section, section_name, location_string=location[0], container=location[1], location_integers=location[2])
        if part_from_loc is not None:
            part = part_from_loc

        # get page_top
        if page is not None:
            if (part_top == 'head') or (part_top == 'body') or (part_top == 'svg'):
                page_top = part_top
            elif part_top in page.widgets:
                widget_top = page.widgets[part_top]
                if widget_top is not None:
                    ident_top = widget_top.ident_string.split("-", 1)
                    # ident_top[0] will be of the form proj_pagenum_head
                    page_top = ident_top[0].split("_")[2]


    # rest is only valid if edited part is a widget given in session data
    if widget is None:
        return Bits(page, section, section_name, parent_widget, parent_container,
                        widget, location, container,
                        part, container_part, part_top, page_top, part_string, field, field_arg, validator)

    if page is None:
        parent_widget, parent_container = widget.get_parent_widget(section)
    else:
        ident_top = widget.ident_string.split("-", 1)
        # ident_top[0] will be of the form proj_pagenum_head
        page_top = ident_top[0].split("_")[2]
        # so this gives page_top of body, head or svg
        parent_widget, parent_container = widget.get_parent_widget(page)

    # get field_arg
    if 'field_arg' in call_data:
        field_arg = call_data['field_arg']

    if not field_arg:
        # Field not identified
        field_arg = None
        return Bits(page, section, section_name, parent_widget, parent_container,
                        widget, location, container,
                        part, container_part, part_top, page_top, part_string, field, field_arg, validator)

    if field_arg in widget.fields:
        field = widget.fields[field_arg]
    else:
        field_arg = None
        return Bits(page, section, section_name, parent_widget, parent_container,
                        widget, location, container,
                        part, container_part, part_top, page_top, part_string, field, field_arg, validator)

    # get validator
    if 'validx' in call_data:
        try:
            validx = int(call_data['validx'])
        except:
            return Bits(page, section, section_name, parent_widget, parent_container,
                        widget, location, container,
                        part, container_part, part_top, page_top, part_string, field, field_arg, validator)
        val_list = field.val_list
        if val_list:
            if (validx >= 0) and (validx < len(val_list)):
                validator = val_list[validx]

    return Bits(page, section, section_name, parent_widget, parent_container,
                        widget, location, container,
                        part, container_part, part_top, page_top, part_string, field, field_arg, validator)


def nav_boxes(call_data, page, section, pagetop=None, parent=None, widget=None, container=None):
    """Extends list of navigation boxes in call_data['extend_nav_buttons']"""

    if (page is None) and (section is None):
        raise FailPage("Page/section not identified")

    boxes = []

    if page is not None:
        if page.page_type == 'TemplatePage':
            if pagetop == 'head':
                boxes.append(['page_head', "Head", True, ''])    # label to 3320
            elif pagetop == 'body':
                boxes.append(['page_body', "Body", True, ''])    # label to 3340
        else:
            if pagetop == 'svg':
                boxes.append(['page_svg', "SVG", True, ''])    # label to 3420
    else:
        boxes.append(['back_to_section', "Section", True, ''])    # label to 7040

    if parent is not None:
        boxes.append(['back_to_parent_container', "Parent", True, ''])    # label to 44720

    if widget is not None:
        boxes.append(['back_to_widget_edit', "Widget", True, ''])    # label to 44002

    if container is not None:
        boxes.append(["back_to_container", "Container", True, ''])   # label to 44704

    if boxes:
        if 'extend_nav_buttons' in call_data:
            call_data['extend_nav_buttons'].extend(boxes)
        else:
            call_data['extend_nav_buttons'] = boxes


def domtree(partdict, part_loc, contents, part_string_list, rows=1, indent=1):
    "Creates the contents of the domtable"

    # note: if in a container
    # part_loc = widget_name + '-' + container_number
    # otherwise part_loc = body, head, svg, section_name


    indent += 1
    padding = "padding-left : %sem;" % (indent,)
    u_r_flag = False
    last_row_at_this_level = 0

    parts = partdict['parts']

    # parts is a list of items
    last_index = len(parts)-1

    #Text   #characters..      #up  #up_right  #down  #down_right   #edit   #insert   #remove

    for index, part in enumerate(parts):
        part_location_string = part_loc + '-' + str(index)
        part_string_list.append(part_location_string)
        rows += 1
        part_type, part_dict = part
        # the row text
        if part_type == 'Widget' or part_type == 'ClosedWidget':
            part_name = 'Widget ' + part_dict['name']
            if len(part_name)>40:
                part_name = part_name[:35] + '...'
            contents.append([part_name, padding, False, ''])
            part_brief = html.escape(part_dict['brief'])
            if len(part_brief)>40:
                part_brief = part_brief[:35] + '...'
            if not part_brief:
                part_brief = '-'
            contents.append([part_brief, '', False, ''])
        elif part_type == 'TextBlock':
            contents.append(['TextBlock', padding, False, ''])
            part_ref = part_dict['textref']
            if len(part_ref)>40:
                part_ref = part_ref[:35] + '...'
            if not part_ref:
                part_ref = '-'
            contents.append([part_ref, '', False, ''])
        elif part_type == 'SectionPlaceHolder':
            section_name = part_dict['placename']
            if section_name:
                section_name = "Section " + section_name
            else:
                section_name = "Section -None-"
            if len(section_name)>40:
                section_name = section_name[:35] + '...'
            contents.append([section_name, padding, False, ''])
            part_brief = html.escape(part_dict['brief'])
            if len(part_brief)>40:
                part_brief = part_brief[:35] + '...'
            if not part_brief:
                part_brief = '-'
            contents.append([part_brief, '', False, ''])
        elif part_type == 'Text':
            contents.append(['Text', padding, False, ''])
            # in this case part_dict is the text string rather than a dictionary
            if len(part_dict)<40:
                part_str = html.escape(part_dict)
            else:
                part_str = html.escape(part_dict[:35] + '...')
            if not part_str:
                part_str = '-'
            contents.append([part_str, '', False, ''])
        elif part_type == 'HTMLSymbol':
            contents.append(['Symbol', padding, False, ''])
            part_text = part_dict['text']
            if len(part_text)<40:
                part_str = html.escape(part_text)
            else:
                part_str = html.escape(part_text[:35] + '...')
            if not part_str:
                part_str = '-'
            contents.append([part_str, '', False, ''])
        elif part_type == 'Comment':
            contents.append(['Comment', padding, False, ''])
            part_text = part_dict['text']
            if len(part_text)<33:
                part_str =  "&lt;!--" + part_text + '--&gt;'
            else:
                part_str = "&lt;!--" + part_text[:31] + '...'
            if not part_str:
                part_str = '&lt;!----&gt;'
            contents.append([part_str, '', False, ''])
        elif part_type == 'ClosedPart':
            if 'attribs' in part_dict:
                tag_name = "&lt;%s ... /&gt;" % part_dict['tag_name']
            else:
                tag_name = "&lt;%s /&gt;" % part_dict['tag_name']
            contents.append([tag_name, padding, False, ''])
            part_brief = html.escape(part_dict['brief'])
            if len(part_brief)>40:
                part_brief = part_brief[:35] + '...'
            if not part_brief:
                part_brief = '-'
            contents.append([part_brief, '', False, ''])
        elif part_type == 'Part':
            if 'attribs' in part_dict:
                tag_name = "&lt;%s ... &gt;" % part_dict['tag_name']
            else:
                tag_name = "&lt;%s&gt;" % part_dict['tag_name']
            contents.append([tag_name, padding, False, ''])
            part_brief = html.escape(part_dict['brief'])
            if len(part_brief)>40:
                part_brief = part_brief[:35] + '...'
            if not part_brief:
                part_brief = '-'
            contents.append([part_brief, '', False, ''])
        else:
            contents.append(['UNKNOWN', padding, False, ''])
            contents.append(['ERROR', '', False, ''])

        # UP ARROW
        if rows == 2:
            # second line in table cannot move upwards
            contents.append(['', '', False, '' ])
        else:
            contents.append(['&uarr;', 'width : 1%;', True, part_location_string])

        # UP RIGHT ARROW
        if u_r_flag:
            contents.append(['&nearr;', 'width : 1%;', True, part_location_string])
        else:
            contents.append(['', '', False, '' ])

        # DOWN ARROW
        if (indent == 2) and (index == last_index):
            # the last line at this top indent has been added, no down arrow
            contents.append(['', '', False, '' ])
        else:
            contents.append(['&darr;', 'width : 1%;', True, part_location_string])

        # DOWN RIGHT ARROW
        # set to empty, when next line is created if down-right not applicable
        contents.append(['', '', False, '' ])

        # EDIT
        contents.append(['Edit', 'width : 1%;', True, part_location_string])

        # INSERT or APPEND
        if part_type == 'Part':
            contents.append(['Insert', 'width : 1%;text-align: center;', True, part_location_string])
        else:
            contents.append(['Append', 'width : 1%;text-align: center;', True, part_location_string])

        # REMOVE
        contents.append(['Remove', 'width : 1%;', True, part_location_string])

        u_r_flag = False
        if part_type == 'Part':
            if last_row_at_this_level and (part_dict['tag_name'] != 'script') and (part_dict['tag_name'] != 'pre'):
                # add down right arrow in previous row at this level, get loc_string from adjacent edit cell
                editcell = contents[last_row_at_this_level *9-3]
                loc_string = editcell[3]
                contents[last_row_at_this_level *9-4] = ['&searr;', 'width : 1%;', True, loc_string]
            last_row_at_this_level = rows
            rows = domtree(part_dict, part_location_string, contents, part_string_list, rows, indent)
            # set u_r_flag for next item below this one
            if  (part_dict['tag_name'] != 'script') and (part_dict['tag_name'] != 'pre'):
                u_r_flag = True
        else:
            last_row_at_this_level =rows

    return rows


