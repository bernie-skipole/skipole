


import re

# a search for anything none-alphanumeric and not an underscore or a dot
_TB = re.compile('[^\w\.]')


from ....skilift import item_info, editpage, editsection

from ... import FailPage, ValidateError, GoTo, ServerError

from ....ski.project_class_definition import SectionData


def retrieve_textblockref(skicall):
    "Fills in the edit textblockref page"

    call_data = skicall.call_data
    pd = call_data['pagedata']
    sd = SectionData("adminhead")

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

    tblock = None

    try:
        if pagenumber:
            call_data['page_number'] = pagenumber
            pchange = call_data['pchange']
            tblock = editpage.page_textblock(project, pagenumber, pchange, location)
        else:
            call_data['section_name'] = section_name
            schange = call_data['schange']
            tblock = editsection.section_textblock(project, section_name, schange, location)

        if tblock is None:
            raise FailPage("TextBlock not identified")
    except ServerError as e:
        raise FailPage(e.message)

    # Fill in header
    sd["page_head","large_text"] = "Edit the TextBlock."
    pd.update(sd)

    # header done, now page contents

    pd["textblock_ref","input_text"]=tblock.textref
    pd["tblock_project", "input_text"]=tblock.tblock_project
    pd["textblock_failed","input_text"]=tblock.failmessage

    pd["linebreaks","radio_values"]=['ON', 'OFF']
    pd["linebreaks","radio_text"]=['On', 'Off']
    if tblock.linebreaks:
        pd["linebreaks","radio_checked"] = 'ON'
    else:
        pd["linebreaks","radio_checked"] = 'OFF'

    pd["setescape","radio_values"]=['ON', 'OFF']
    pd["setescape","radio_text"]=['On', 'Off']
    if tblock.escape:
        pd["setescape","radio_checked"] = 'ON'
    else:
        pd["setescape","radio_checked"] = 'OFF'



def set_textblock(skicall):
    "Sets the textblock reference, fail message, linebreaks or escape"

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
            tblock = editpage.page_textblock(project, pagenumber, pchange, location)
        else:
            tblock = editsection.section_textblock(project, section_name, schange, location)

        message = "A new value to edit has not been found"

        if 'textblock_ref' in call_data:
            if _TB.search(call_data["textblock_ref"]):
                raise FailPage(message="Invalid reference")
            textref = call_data["textblock_ref"]
            message = 'New reference string set'
        else:
            textref = tblock.textref

        if 'tblock_project' in call_data:
            tblock_project = call_data['tblock_project']
            if tblock_project == project:
                message = "TextBlock sub project removed"
            elif tblock_project:
                message = 'New TextBlock sub project set'
            else:
                message = "TextBlock sub project removed"
        else:
            tblock_project = tblock.tblock_project

        if 'textblock_failed' in call_data:
            failmessage = call_data["textblock_failed"]
            message = 'New fail message set'
        else:
            failmessage = tblock.failmessage


        if 'linebreaks' in call_data:
            if call_data['linebreaks'] == 'ON':
                linebreaks = True
                message = 'Linebreaks set on'
            else:
                linebreaks = False
                message = 'Linebreaks set off'
        else:
            linebreaks = tblock.linebreaks


        if 'setescape' in call_data:
            if call_data['setescape'] == 'ON':
                escape = True
                message = 'HTML escape set on'
            else:
                escape = False
                message = 'HTML escape set off'
        else:
            escape = tblock.escape

        if pagenumber:
            call_data['pchange'] = editpage.edit_page_textblock(project, pagenumber, pchange, location, textref, tblock_project, failmessage, escape, linebreaks)
        else:
            call_data['schange'] = editsection.edit_section_textblock(project, section_name, schange, location, textref, tblock_project, failmessage, escape, linebreaks)

    except ServerError as e:
        raise FailPage(e.message)

    call_data['status'] = message


def create_insert(skicall):
    "Creates the textblock ref"

    call_data = skicall.call_data

    project = call_data['editedprojname']

    # create the textblock
    if 'textblock_ref' not in call_data:
        raise FailPage(message="Invalid reference")
    if _TB.search(call_data["textblock_ref"]):
        raise FailPage(message="Invalid reference")
    textref = call_data['textblock_ref']

    if 'tblock_project' in call_data:
        tblock_project = call_data['tblock_project']
    else:
        tblock_project = ''

    if 'textblock_failed' in call_data:
        failmessage = call_data["textblock_failed"]
    else:
        failmessage = "TextBlock not found"

    if 'linebreaks' in call_data:
        if call_data['linebreaks'] == 'ON':
            linebreaks = True
        else:
            linebreaks = False
    else:
        linebreaks = True

    if 'setescape' in call_data:
        if call_data['setescape'] == 'ON':
            escape = True
        else:
            escape = False
    else:
        escape = True


    try:
        part_top, container, location_integers = call_data['location']

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

            call_data['pchange'], new_location = editpage.create_textblock_in_page(project,
                                                                                     pagenumber,
                                                                                     call_data['pchange'],
                                                                                     call_data['location'],
                                                                                     textref,
                                                                                     failmessage,
                                                                                     escape,
                                                                                     linebreaks,
                                                                                     tblock_project=tblock_project)

        elif 'section_name' in call_data:
            section_name = call_data['section_name']

            if container is not None:
                target = "back_to_container"
            else:
                target = "back_to_section"

            call_data['schange'], new_location = editsection.create_textblock_in_section(project,
                                                                                          section_name,
                                                                                          call_data['schange'],
                                                                                          call_data['location'],
                                                                                          textref,
                                                                                          failmessage,
                                                                                          escape,
                                                                                          linebreaks,
                                                                                          tblock_project=tblock_project)

        else:
            raise FailPage("Either a page or section must be specified")

    except ServerError as e:
        raise FailPage(e.message)

    call_data['location'] = new_location
    call_data['status'] = 'New TextBlock inserted'
    raise GoTo(target = target, clear_submitted=True)

