
"Functions implementing part editing"

import json

from ... import skilift
from ....skilift import fromjson, editpage, editsection, item_info
from ... import FailPage, ValidateError, GoTo, ServerError

from ....ski.project_class_definition import SectionData



def retrieve_editpart(skicall):
    "Fills in the edit a part page"

    call_data = skicall.call_data
    pd = call_data['pagedata']

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
    sd_adminhead = SectionData("adminhead")
    sd_adminhead["page_head","large_text"] = "Edit the html element."
    pd.update(sd_adminhead)

    # header done, now page contents

    if (part.part_type == "Part") or (part.part_type == "Section"):
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
        pd['tag_para','para_text'] = "Element tag : <%s%s%s" % (part.tag_name, attstring, ending)
    else:
        pd['tag_para','para_text'] = "Element tag : <%s%s" % (part.tag_name, ending)

    # list table of attributes, widget tables.Table2_1
    # contents = list of lists, each inner has five elements
    # col 0 is the text to place in the first column,
    # col 1 is the text to place in the second column,
    # col 2, 3, 4 are the three get field contents of the link
    if len(atts_list):
        pd['attribs_list_para','show'] = True
        pd['attribs_list','show'] = True
        contents = []
        for index, att in enumerate(atts_list):
            row = [ att, vals_list[index], att]
            contents.append(row)
        pd['attribs_list', 'contents'] = contents
    else:
        pd['attribs_list_para','show'] = False
        pd['attribs_list','show'] = False

    # input form to change the tag name
    pd['tag_input','input_text'] = part.tag_name

    # input form to change the tag brief
    pd['tag_brief','input_text'] = part.brief

    if part.part_type == "Part":
        if part.hide_if_empty:
            pd['hidecheck','checked'] = True
        else:
            pd['hidecheck','checked'] = False
    else:
        pd['set_to_hide','show'] = False
        pd['para_to_hide','show'] = False
        pd['para_to_hide2','show'] = False
        pd['partdownload', 'show'] = False
        pd['aboutdownload', 'show'] = False


def set_tag(skicall):
    "Sets the part tag name, or brief, adds an attribute"

    call_data = skicall.call_data

    pagenumber = None
    section_name = None

    project = call_data['editedprojname']
    location = call_data['location']
    if 'page_number' in call_data:
        pagenumber = call_data['page_number']
        pchange = call_data['pchange']
    else:
        section_name = call_data['section_name']
        schange = call_data['schange']

    if (pagenumber is None) and (section_name is None):
        raise ValidateError("Page/section not identified")

    try:
        if pagenumber:
            part = editpage.page_element(project, pagenumber, pchange, location)
        else:
            part = editsection.section_element(project, section_name, schange, location)

        if part is None:
            raise FailPage("Part not identified")

        message = "A new value to edit has not been found"

        if 'tag_name' in call_data:
            tag_name = call_data["tag_name"]
            message = 'New tag set'
        else:
            tag_name = part.tag_name

        if 'tag_brief' in call_data:
            brief = call_data["tag_brief"]
            message = 'New description set'
        else:
            brief = part.brief

        attribs = part.attribs

        if 'attrib' in call_data:
            if 'val' not in call_data:
                raise FailPage("The attribute value has not been found")
            attribs.update({call_data["attrib"]:call_data["val"]})
            message = 'Attribute updated'

        if 'hide_if_empty' in call_data:
            hide = call_data['hide_if_empty']
            if hide == 'hide':
                hide_if_empty = True
                message = 'Element will be hidden if no content within it.'
            else:
                hide_if_empty = False
                message = 'Element will be shown even if no content within it.'
        else:
            hide_if_empty = part.hide_if_empty

        if pagenumber:
            call_data['pchange'] = editpage.edit_page_element(project, pagenumber, pchange, location, tag_name, brief, hide_if_empty, attribs)
        else:
            call_data['schange'] = editsection.edit_section_element(project, section_name, schange, location, tag_name, brief, hide_if_empty, attribs)

    except ServerError as e:
        raise FailPage(e.message)

    call_data['status'] = message


def remove_tag_attribute(skicall):
    "Removes the given tag attribute"

    call_data = skicall.call_data
    pd = call_data['pagedata']

    pagenumber = None
    section_name = None

    project = call_data['editedprojname']
    location = call_data['location']
    if 'page_number' in call_data:
        pagenumber = call_data['page_number']
        pchange = call_data['pchange']
    else:
        section_name = call_data['section_name']
        schange = call_data['schange']

    if (pagenumber is None) and (section_name is None):
        raise ValidateError("Page/section not identified")

    if ('attribs_list','contents') not in call_data:
        raise FailPage("A Tag attribute to remove has not been found")

    att = call_data['attribs_list','contents']

    try:
        if pagenumber:
            part = editpage.page_element(project, pagenumber, pchange, location)
        else:
            part = editsection.section_element(project, section_name, schange, location)

        if part is None:
            raise FailPage("Part not identified")

        if part.attribs and (att in part.attribs):
            # set the attribute to be removed in the input boxes so it can be edited
            pd['add_attrib', 'input_text1'] = att
            pd['add_attrib', 'input_text2'] = part.attribs[att]
        else:
            raise FailPage("A Tag attribute to remove has not been found")

        if pagenumber:
            call_data['pchange'] = editpage.del_attrib(project, pagenumber, pchange, location, att)
        else:
            call_data['schange'] = editsection.del_attrib(project, section_name, schange, location, att)

    except ServerError as e:
        raise FailPage(e.message)




def downloadpart(skicall):
    "Gets part, and returns a json dictionary, this will be sent as an octet file to be downloaded"

    call_data = skicall.call_data
    pd = call_data['pagedata']

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

    parttext, part_dict = fromjson.item_outline(project, pagenumber, section_name, call_data['location'])
    # set version and skipole as the first two items in the dictionary
    versions = skilift.versions(project)
    part_dict["skipole"] = versions.skipole
    part_dict.move_to_end('skipole', last=False)
    part_dict["version"] = versions.project
    part_dict.move_to_end('version', last=False)
    jsonstring = json.dumps(part_dict, indent=4, separators=(',', ':'))
    line_list = []
    n = 0
    for line in jsonstring.splitlines(True):
        binline = line.encode('utf-8')
        n += len(binline)
        line_list.append(binline)
    pd.mimetype = 'application/octet-stream'
    pd.content_length = str(n)
    return line_list


def create_insert(skicall):
    "Creates the html element"

    call_data = skicall.call_data

    project = call_data['editedprojname']

    try:
        part_top, container, location_integers = call_data['location']
        if call_data['newopenclosed'] == 'open':
            opentag = True
        else:
            opentag = False

        if 'page_number' in call_data:
            pagenumber = call_data['page_number']
            page_info = item_info(project, pagenumber)
            if page_info is None:
                raise FailPage("Page to edit not identified")

            if (page_info.item_type != "TemplatePage") and (page_info.item_type != "SVG"):
                raise FailPage("Page not identified")

            # page to go back to
            target = None
            if part_top == 'head':
                target = "page_head"
            elif part_top == 'body':
                target = "page_body"
            elif part_top == 'svg':
                target = "page_svg"

            if container is not None:
                target = "back_to_container"

            if target is None:
                raise FailPage("Invalid location")

            call_data['pchange'] = editpage.create_html_element_in_page(project,
                                                                        pagenumber,
                                                                        call_data['pchange'],
                                                                        call_data['location'],
                                                                        call_data['newpartname'],
                                                                        call_data['newbrief'],
                                                                        opentag)

        elif 'section_name' in call_data:
            section_name = call_data['section_name']

            if container is not None:
                target = "back_to_container"
            else:
                target = "back_to_section"

            call_data['schange'] = editsection.create_html_element_in_section(project,
                                                                              section_name,
                                                                              call_data['schange'],
                                                                              call_data['location'],
                                                                              call_data['newpartname'],
                                                                              call_data['newbrief'],
                                                                              opentag)

        else:
            raise FailPage("Either a page or section must be specified")

    except ServerError as e:
        raise FailPage(e.message)
    call_data['status'] = 'New tag inserted'
    raise GoTo(target = target, clear_submitted=True)


