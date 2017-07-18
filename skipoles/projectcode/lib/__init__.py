"""
This project consists of static files only.
As there is no dynamic content, these functions do nothing
"""

def start_project(project, projectfiles, path, option):
    """This project has no start_project functionality"""
    return {}

def start_call(environ, path, project, called_ident, caller_ident, received_cookies, ident_data, lang, option, proj_data):
    "All static files in this project are available without any session tracking"
    return called_ident, {}, {}, lang

def submit_data(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "This project has no submit_data functionality"
    return

def end_call(page_ident, page_type, call_data, page_data, proj_data, lang):
    "This project has no end_call functionality"
    return
