

import re, json, os
# a search for anything none-alphanumeric and not an underscore
_AN = re.compile('[^\w_]')

from ....skilift import fromjson, off_piste, set_label, versions, lib_list, labels
from ... import FailPage, ValidateError, ServerError, GoTo

from .. import utils, css_styles

from ....ski.project_class_definition import SectionData


def retrieve_operations_data(skicall):
    "Retrieves field data for operations page"

    call_data = skicall.call_data
    pd = call_data['pagedata']

    # clears any session data, but keep status
    # so the status message is displayed after any operations
    utils.clear_call_data(call_data, keep='status')

    editedprojname = call_data['editedprojname']

    # project background color
    backcol = fromjson.get_defaults(editedprojname, key="backcol")
    if backcol:
        pd['htmlbackcol','input_text'] = backcol

    # project body class
    body_class = fromjson.get_defaults(editedprojname, key="body_class")
    if body_class:
        pd['bodyclass','input_text'] = body_class

    # get default css links for widget css_defaults
    css_list = fromjson.get_defaults(editedprojname, key='css_links')

    if css_list:
        contents = []
        for label in css_list:
            row = [label,
                   label, label, label, '',
                   True,
                   True,
                   True,
                   False]
            contents.append(row)
        # remove up arrow in row 0
        contents[0][1] = ''
        contents[0][5] = False
        # remove down arrow in row -1
        contents[-1][2] = ''
        contents[-1][6] = False
        pd['css_links', 'contents'] = contents


  #      contents: col 0 is the text to place in the first column,
  #                  col 1, 2, 3, 4 are the get field contents of links 1,2,3 and 4
  #                  col 5 - True if the first button and link is to be shown, False if not
  #                  col 6 - True if the second button and link is to be shown, False if not
  #                  col 7 - True if the third button and link is to be shown, False if not
  #                  col 8 - True if the fourth button and link is to be shown, False if not


    # get default js links for widget js_defaults
    js_list = fromjson.get_defaults(editedprojname, key='js_links')

    if js_list:
        contents = []
        for label in js_list:
            row = [label,
                   label, label, label, '',
                   True,
                   True,
                   True,
                   False]
            contents.append(row)
        # remove up arrow in row 0
        contents[0][1] = ''
        contents[0][5] = False
        # remove down arrow in row -1
        contents[-1][2] = ''
        contents[-1][6] = False
        pd['js_links', 'contents'] = contents


def handle_upload(skicall):
    "handle uploaded defaults.json file"

    call_data = skicall.call_data
    editedprojname = call_data['editedprojname']

    # get uploaded file contents
    if "upload" not in call_data:
        raise FailPage("upload missing from call data")
    file_contents = call_data["upload"]
    if not file_contents:
        raise FailPage("No data found in file")
    defaults_dict = json.loads(file_contents.decode())
    fromjson.save_defaults(editedprojname, defaults_dict)
    call_data['status'] = 'Defaults file installed'



def set_widgets_css(skicall):
    "sets default css classes into widgets"

    call_data = skicall.call_data

    editedprojname = call_data['editedprojname']
    off_piste.set_widget_css_to_default(editedprojname)
    call_data['status'] = 'Widget CSS classes set'


def submit_project_color(skicall):
    "set project default background color"

    call_data = skicall.call_data

    try:
        backcol = call_data['htmlbackcol','input_text']
    except Exception:
        raise ValidateError(message='Invalid call')
    try:
        editedprojname = call_data['editedprojname']
        # set background color in existing pages
        off_piste.set_backcol_in_pages(editedprojname, backcol)
        # set the project colour for new pages
        fromjson.set_defaults(editedprojname, 'backcol', backcol)
    except (ValidateError, ServerError) as e:
        raise FailPage(message = e.message, widget = "htmlbackcol")
    call_data['status'] = 'Project background colour set'


def set_bodyclass_in_pages(skicall):
    "sets css class into page body tags"

    call_data = skicall.call_data

    try:
        bodyclass = call_data['bodyclass','input_text']
    except Exception:
        raise ValidateError(message='Invalid call')
    # set body class in all project template pages
    editedprojname = call_data['editedprojname']
    off_piste.set_bodyclass_in_pages(editedprojname, bodyclass)
    # set the body class for new pages
    fromjson.set_defaults(editedprojname, 'body_class', bodyclass)
    if bodyclass:
        call_data['status'] = 'CSS class set in body tags'
    else:
        call_data['status'] = 'CSS class removed from body tags'


def add_default_css(skicall):
    "Add a label to the default css list"

    call_data = skicall.call_data

    editedprojname = call_data['editedprojname']

    # check label is valid
    if not "new_css_label" in call_data:
        raise FailPage(message = "label missing")

    label = call_data["new_css_label"]
    if not label:
        raise FailPage(message = "label missing")

    if _AN.search(label):
        raise FailPage(message = "The label can only contain A-Z, a-z, 0-9 and the underscore character.")

    if '_' in label:
        labelparts = label.split('_')
        if labelparts[0].isalnum() and labelparts[1].isdigit():
            raise FailPage(message = "Invalid label (Danger of confusion with a page ident).")

    if label.isdigit():
        raise FailPage(message = "Invalid label (Danger of confusion with a page ident).")

    css_list = fromjson.get_defaults(editedprojname, key='css_links')
    if label in css_list:
        raise FailPage(message = "This label is already in the list")
    css_list.append(label)
    try:
        fromjson.set_defaults(editedprojname, key='css_links', value=css_list)
    except e:
        raise FailPage(message = "Unable to save defaults.json")


def css_remove(skicall):
    "Removes css default label"

    call_data = skicall.call_data

    editedprojname = call_data['editedprojname']
    if 'css_label' in call_data:
        label = call_data['css_label']
        d_list = fromjson.get_defaults(editedprojname, 'css_links')
        if not label in d_list:
            return
        index = d_list.index(label)
        # remove
        del d_list[index]
        # save d_list
        try:
            fromjson.set_defaults(editedprojname, key='css_links', value=d_list)
        except e:
            raise FailPage(message = "Unable to save defaults.json")


def css_up(skicall):
    "Moves css default label up"

    call_data = skicall.call_data

    editedprojname = call_data['editedprojname']
    if 'css_label' in call_data:
        label = call_data['css_label']
        d_list = fromjson.get_defaults(editedprojname, 'css_links')
        if not label in d_list:
            return
        index = d_list.index(label)
        # move up
        if not index:
            return
        d_list.insert(index-1, d_list.pop(index))
        # save d_list
        try:
            fromjson.set_defaults(editedprojname, key='css_links', value=d_list)
        except e:
            raise FailPage(message = "Unable to save defaults.json")


def css_down(skicall):
    "Moves css default label down"

    call_data = skicall.call_data

    editedprojname = call_data['editedprojname']
    if 'css_label' in call_data:
        label = call_data['css_label']
        d_list = fromjson.get_defaults(editedprojname, 'css_links')
        if not label in d_list:
            return
        index = d_list.index(label)
        # move down
        if index == len(d_list)-1:
            return
        d_list.insert(index+1, d_list.pop(index))
        # save d_list
        try:
            fromjson.set_defaults(editedprojname, key='css_links', value=d_list)
        except e:
            raise FailPage(message = "Unable to save defaults.json")


def add_default_js(skicall):
    "Add a label to the default javascript list"

    call_data = skicall.call_data

    editedprojname = call_data['editedprojname']

    # check label is valid
    if not "new_js_label" in call_data:
        raise FailPage(message = "label missing")

    label = call_data["new_js_label"]
    if not label:
        raise FailPage(message = "label missing")

    if _AN.search(label):
        raise FailPage(message = "The label can only contain A-Z, a-z, 0-9 and the underscore character.")

    if '_' in label:
        labelparts = label.split('_')
        if labelparts[0].isalnum() and labelparts[1].isdigit():
            raise FailPage(message = "Invalid label (Danger of confusion with a page ident).")

    if label.isdigit():
        raise FailPage(message = "Invalid label (Danger of confusion with a page ident).")

    js_list = fromjson.get_defaults(editedprojname, key='js_links')
    if label in js_list:
        raise FailPage(message = "This label is already in the list")
    js_list. append(label)
    try:
        fromjson.set_defaults(editedprojname, key='js_links', value=js_list)
    except e:
        raise FailPage(message = "Unable to save defaults.json")


def js_remove(skicall):
    "Removes js default label"

    call_data = skicall.call_data

    editedprojname = call_data['editedprojname']
    if 'js_label' in call_data:
        label = call_data['js_label']
        d_list = fromjson.get_defaults(editedprojname, 'js_links')
        if not label in d_list:
            return
        index = d_list.index(label)
        # remove
        del d_list[index]
        # save d_list
        try:
            fromjson.set_defaults(editedprojname, key='js_links', value=d_list)
        except e:
            raise FailPage(message = "Unable to save defaults.json")


def js_up(skicall):
    "Moves js default label up"

    call_data = skicall.call_data

    editedprojname = call_data['editedprojname']
    if 'js_label' in call_data:
        label = call_data['js_label']
        d_list = fromjson.get_defaults(editedprojname, 'js_links')
        if not label in d_list:
            return
        index = d_list.index(label)
        # move up
        if not index:
            return
        d_list.insert(index-1, d_list.pop(index))
        # save d_list
        try:
            fromjson.set_defaults(editedprojname, key='js_links', value=d_list)
        except e:
            raise FailPage(message = "Unable to save defaults.json")


def js_down(skicall):
    "Moves js default label down"

    call_data = skicall.call_data

    editedprojname = call_data['editedprojname']
    if 'js_label' in call_data:
        label = call_data['js_label']
        d_list = fromjson.get_defaults(editedprojname, 'js_links')
        if not label in d_list:
            return
        index = d_list.index(label)
        # move down
        if index == len(d_list)-1:
            return
        d_list.insert(index+1, d_list.pop(index))
        # save d_list
        try:
            fromjson.set_defaults(editedprojname, key='js_links', value=d_list)
        except e:
            raise FailPage(message = "Unable to save defaults.json")


def set_javascript_to_skis(skicall):
    "Sets javascript labels to skis"

    call_data = skicall.call_data

    editedprojname = call_data['editedprojname']
    liblabels = lib_list()
    projlabels = labels(editedprojname)
    try:
        for label in liblabels:
            # label is a widget or validator javascript label, of the format "ski_basic" etc
            # which needs to be given a value of the format "skis,ski_basic"
            set_label(editedprojname, label, "skis," + label)
        if "w3_css" in projlabels:
            if projlabels["w3_css"] == "https://www.w3schools.com/w3css/4/w3.css":
                set_label(editedprojname, "w3_css", "skis,w3_css")
    except ServerError as e:
        raise FailPage(message = e.message)
    call_data['status'] = 'Special file labels now point to the skis sub project'


def set_javascript_to_cdn(skicall):
    "Sets javascript labels to cdn"

    call_data = skicall.call_data

    editedprojname = call_data['editedprojname']

    skipole_version, project_version = versions(editedprojname)
    # get this to point to https://cdn.jsdelivr.net/gh/bernie-skipole/skipole@5/skipole/skis/static/js/
    # so primary version number is used
    version_numbers = skipole_version.split(".")
    starthttp =  "https://cdn.jsdelivr.net/gh/bernie-skipole/skipole@" + version_numbers[0] + "/skipole/skis/static/js/"
    liblabels = lib_list()
    projlabels = labels(editedprojname)
    try:
        for label in liblabels:
            if label == "jquery_core":
                if projlabels[label] == "skis,jquery_core":
                    set_label(editedprojname, label, "https://cdn.jsdelivr.net/gh/jquery/jquery@3/dist/jquery.min.js")
                continue
            if label == "skipole_js":
                set_label(editedprojname, "skipole_js", starthttp +"skipole.min.js")
                continue
            # so label is a widget or validator javascript label, of the format "ski_basic" etc
            # which needs to be given a value of the format "basic.min.js"
            set_label(editedprojname, label, starthttp +label[4:]+".min.js")
        if "w3_css" in projlabels:
            if projlabels["w3_css"] == "skis,w3_css":
                set_label(editedprojname, "w3_css", "https://www.w3schools.com/w3css/4/w3.css")
    except ServerError as e:
        raise FailPage(message = e.message)
    call_data['status'] = "Special file labels now point to CDN's"


