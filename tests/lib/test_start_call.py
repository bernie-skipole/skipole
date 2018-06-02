# Tests for project lib

from skipoles import skilift

from skipoles.projectcode import lib

def test_ident(project):
    "Checks project is lib"
    assert project == "lib"

def test_loaded(project):
    "Checks project is loaded into the framework"
    assert skilift.project_loaded(project, error_if_not=False)


def test_lib(project):
    "Tests project info obtained from skilift.project_info"
    proj_info = skilift.project_info(project)

    assert proj_info.project == "lib"
    assert proj_info.version == "0.0.1"
    assert proj_info.brief == "Library project of static files"
    assert proj_info.path == "/"
    assert proj_info.default_language == "en"
    assert proj_info.subprojects == {}


def test_start_call(project):
    "Calls start_call"

    proj = skilift.get_proj(project)

    environ = {}
    path = proj.url
    called_ident = None
    caller_ident = None
    received_cookies = {}
    ident_data = None
    lang = ('en-GB', 'en')
    option = {}
    proj_data = proj.proj_data
    # call lib start_call
    called_ident, call_data, page_data, lang = lib.start_call(environ, path, project, called_ident, caller_ident, received_cookies, ident_data, lang, option, proj_data)
    assert called_ident is None
    assert call_data == {}
    assert page_data == {}
    assert lang == lang
    


