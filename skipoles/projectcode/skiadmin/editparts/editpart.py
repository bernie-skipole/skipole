####### SKIPOLE WEB FRAMEWORK #######
#
# editpart.py  - part editing functions
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

"Functions implementing part editing"


from ....ski import skiboot, tag, widgets
from .... import skilift
from ....skilift import fromjson, editpage, editsection
from .. import utils
from ....ski.excepts import FailPage, ValidateError, GoTo, ServerError


def retrieve_editpart(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Fills in the edit a part page"

    # a skilift.part_tuple is (project, pagenumber, page_part, section_name, name, location, part_type, brief)

    pagenumber = None
    section_name = None

    if 'part_tuple' in call_data:
        part_tuple = call_data['part_tuple']
        project = part_tuple.project
        location = part_tuple.location
        pagenumber = part_tuple.pagenumber
        section_name = part_tuple.section_name
    else:
        project = call_data['editedprojname']
        location = call_data['location']
        if 'page_number' in call_data:
            pagenumber = call_data['page_number']
        else:
            section_name = call_data['section_name']

    if (pagenumber is None) and (section_name is None):
        raise ValidateError("Page/section not identified")

    call_data['location'] = location

    part = None

    try:
        if pagenumber:
            call_data['page_number'] = pagenumber
            pchange = call_data['pchange']
            part = editpage.page_element(project, pagenumber, pchange, location)
        else:
            call_data['section_name'] = section_name
            schange = call_data['schange']
            part = editsection.section_element(project, section_name, schange, location)

        if part is None:
            raise FailPage("Part not identified")
    except ServerError as e:
        raise FailPage(e.message)

    # Fill in header
    page_data[("adminhead","page_head","large_text")] = "Edit the html element."

    # header done, now page contents

    if part.part_type == "Part":
        ending = ">"
    else:
        ending = " />"

    atts_list = []
    vals_list = []
    if part.attribs:
        for att in part.attribs:
            atts_list.append(att)
        # sort atts_list
        atts_list.sort()
        attstring = ""
        for att in atts_list:
            vals_list.append(part.attribs[att])
            attstring += " %s = \"%s\"" % (att, part.attribs[att])
        page_data[('tag_para','para_text')] = "Element tag : <%s%s%s" % (part.tag_name, attstring, ending)
    else:
        page_data[('tag_para','para_text')] = "Element tag : <%s%s" % (part.tag_name, ending)

    # list table of attributes, widget tables.Table2_1
    # contents = list of lists, each inner has five elements
    # col 0 is the text to place in the first column,
    # col 1 is the text to place in the second column,
    # col 2, 3, 4 are the three get field contents of the link
    if len(atts_list):
        page_data[('attribs_list_para','show')] = True
        page_data[('attribs_list','show')] = True
        contents = []
        for index, att in enumerate(atts_list):
            row = [ att, vals_list[index], att]
            contents.append(row)
        page_data['attribs_list', 'contents'] = contents
    else:
        page_data[('attribs_list_para','show')] = False
        page_data[('attribs_list','show')] = False

    # input form to change the tag name
    page_data[('tag_input','input_text')] = part.tag_name

    # input form to change the tag brief
    page_data[('tag_brief','input_text')] = part.brief

    # input form to change hide if no contents

    # Note tag.Part covers both Part and Section, which
    # is required here, so a Section element can be
    # downloaded as if it was a Part

    if part.part_type == "Part":
        if part.hide_if_empty:
            page_data[('hidecheck','checked')] = True
        else:
            page_data[('hidecheck','checked')] = False
    else:
        page_data[('set_to_hide','show')] = False
        page_data[('para_to_hide','show')] = False
        page_data[('para_to_hide2','show')] = False
        page_data['partdownload', 'show'] = False
        page_data['aboutdownload', 'show'] = False



def set_tag(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Sets the part tag name, or brief, adds an attribute"

    editedproj = call_data['editedproj']
    widget=None

    # get data
    bits = utils.get_bits(call_data)

    page = bits.page
    section = bits.section
    widget = bits.widget
    part = bits.part
    message = ''

    if (page is None) and (section is None):
        raise FailPage("Page/section not identified")

    if part is None:
        raise FailPage("Part not identified")

    if 'tag_name' in call_data:
        part.tag_name = call_data["tag_name"]
        message = 'New tag set'
        widget_name="tag_input"
    elif 'tag_brief' in call_data:
        part.brief = call_data["tag_brief"]
        message = 'New description set'
        widget_name="tag_brief"
    elif 'attrib' in call_data:
        if 'val' not in call_data:
            raise FailPage("The attribute value has not been found")
        part.update_attribs({call_data["attrib"]:call_data["val"]})
        widget_name='add_attrib_error'
    elif 'hide_if_empty' in call_data:
        if not isinstance(part, tag.Part):
            raise FailPage("Invalid action on part")
        hide = call_data['hide_if_empty']
        if hide == 'hide':
            part.hide_if_empty = True
            message = 'Element will be hidden if no content within it.'
        else:
            part.hide_if_empty = False
            message = 'Element will be shown even if no content within it.'
        widget_name='hide_if_empty_error'
    else:
        raise FailPage("A new Tag value to edit has not been found")

    utils.save(call_data, page=page, section_name=bits.section_name, section=section, widget_name=widget_name)
    if message:
        call_data['status'] = message


def remove_tag_attribute(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Removes the given tag attribute"

    editedproj = call_data['editedproj']

    # get data
    bits = utils.get_bits(call_data)

    page = bits.page
    section = bits.section
    widget = bits.widget
    part = bits.part

    if (page is None) and (section is None):
        raise FailPage("Page/section not identified")

    if part is None:
        raise FailPage("Part not identified")

    if ('attribs_list','contents') not in call_data:
        raise FailPage("A Tag attribute to remove has not been found")
    part.del_one_attrib(call_data['attribs_list','contents'])

    utils.save(call_data, page=page, section_name=bits.section_name, section=section, widget_name='list_attribs_error')


def downloadpart(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Gets part, and returns a json dictionary, this will be sent as an octet file to be downloaded"

    project = call_data['editedprojname']

    if 'page_number' in call_data:
        pagenumber = call_data['page_number']
    else:
        pagenumber = None

    if 'section_name' in call_data:
        section_name = call_data['section_name']
    else:
        section_name = None   

    part_info = skilift.part_info(project, pagenumber, section_name, call_data['location'])

    if not part_info:
        raise FailPage("Part not identified")

    jsonstring =  fromjson.part_to_json(project, pagenumber, section_name, call_data['location'], indent=4)
    line_list = []
    n = 0
    for line in jsonstring.splitlines(True):
        binline = line.encode('utf-8')
        n += len(binline)
        line_list.append(binline)
    page_data['headers'] = [('content-type', 'application/octet-stream'), ('content-length', str(n))]
    return line_list
