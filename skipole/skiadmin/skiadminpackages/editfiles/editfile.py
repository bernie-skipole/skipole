

"Functions implementing FilePage editing"


from ... import ValidateError, FailPage, ServerError

from .... import SectionData

from ... import skilift
from ....skilift import editpage

from .. import utils


def retrieve_edit_filepage(skicall):
    "Retrieves widget data for the edit file page"

    call_data = skicall.call_data
    pd = call_data['pagedata']

    # clears any session data, keeping page_number, pchange and any status message
    utils.clear_call_data(call_data, keep=["page_number", "pchange", "status"])

    project = call_data['editedprojname']
    
    if 'page_number' in call_data:
        pagenumber = call_data['page_number']
        str_pagenumber = str(pagenumber)
    else:
        raise FailPage(message = "page missing")

    if not pagenumber:
        raise FailPage(message = "Invalid page")

    try:
        pageinfo = skilift.page_info(project, pagenumber)
        if pageinfo.item_type != 'FilePage':
            raise FailPage(message = "Invalid page")

        call_data['pchange'] = pageinfo.change

        filepath, mimetype = editpage.file_parameters(project, pagenumber)
    except ServerError as e:
        raise FailPage(message = e.message)

    # fill in sections

    sd_adminhead = SectionData("adminhead")
    sd_page_edit = SectionData("page_edit")

   # fills in the data for editing page name, brief, parent, etc., 
    sd_adminhead["page_head","large_text"] = pageinfo.name
    sd_page_edit['p_ident','page_ident'] = (project,str_pagenumber)
    sd_page_edit['p_name','page_ident'] = (project,str_pagenumber)
    sd_page_edit['p_description','page_ident'] = (project,str_pagenumber)
    sd_page_edit['p_rename','input_text'] = pageinfo.name
    sd_page_edit['p_parent','input_text'] = "%s,%s" % (project, pageinfo.parentfolder_number)
    sd_page_edit['p_brief','input_text'] = pageinfo.brief

    pd.update(sd_adminhead)
    pd.update(sd_page_edit)

    pd['p_file','input_text'] = filepath
    pd['p_mime','input_text'] = mimetype
    pd['enable_cache','radio_checked'] = pageinfo.enable_cache


def submit_new_filepath(skicall):
    "Sets new page filepath"

    call_data = skicall.call_data

    project = call_data['editedprojname']
    if 'page_number' in call_data:
        pagenumber = call_data['page_number']
    else:
        raise FailPage(message = "page missing")
    if not pagenumber:
        raise FailPage(message = "Invalid page")
    pchange = call_data['pchange']
    if not 'filepath' in call_data:
        raise FailPage(message="No filepath given")
    new_filepath = call_data['filepath']
    if not new_filepath:
        raise FailPage(message="No filepath given")
    try:
        call_data['pchange'] = editpage.page_filepath(project, pagenumber, pchange, new_filepath)
    except ServerError as e:
        raise FailPage(message=e.message)
    call_data['status'] = 'Page filepath set: %s' % (new_filepath,)


def submit_mimetype(skicall):
    "Sets mimetype"

    call_data = skicall.call_data

    project = call_data['editedprojname']
    if 'page_number' in call_data:
        pagenumber = call_data['page_number']
    else:
        raise FailPage(message = "page missing")
    if not pagenumber:
        raise FailPage(message = "Invalid page")
    pchange = call_data['pchange']
    if not 'mime_type' in call_data:
        raise FailPage(message="No mimetype given")
    # Set the page mimetype
    try:
        call_data['pchange'] = editpage.page_mimetype(project, pagenumber, pchange, call_data['mime_type'])
    except ServerError as e:
        raise FailPage(message=e.message)
    call_data['status'] = 'Mimetype set'


def submit_cache(skicall):
    "Sets cache true or false"

    call_data = skicall.call_data

    # this function is duplicated in editpage, may be better to remove this file and transfer conetents to editpage
    project = call_data['editedprojname']
    pagenumber = call_data['page_number']
    pchange = call_data['pchange']
    if 'cache' not in call_data:
        raise FailPage(message="No cache instruction given")
    try:
        # Set the page cache
        if call_data['cache'] == 'True':
            enable_cache = True
            message = "Cache Enabled"
        else:
            enable_cache = False
            message = "Cache Disabled"
        call_data['pchange'] = editpage.page_enable_cache(project, pagenumber, pchange, enable_cache)
    except ServerError as e:
        raise FailPage(message=e.message)
    call_data['status'] = message


