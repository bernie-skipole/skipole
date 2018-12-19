# Tests for project newproj

from skipoles import skilift

from skipoles.projectcode import newproj

class SkiCall(object):

    def __init__(self, environ, path, project, rootproject, caller_ident, received_cookies, ident_data, lang, option, proj_data):

        self.environ = environ
        self.path = path
        self.project = project
        self.rootproject = project
        self.caller_ident = caller_ident
        self.received_cookies = received_cookies
        self.ident_data = ident_data
        self.lang = lang
        self.option = option
        self.proj_data = proj_data

        self.ident_list = []
        self.submit_list = []
        self.submit_dict = {}
        self.call_data = {}
        self.page_data = {}

def test_ident(project):
    "Checks project is newproj"
    assert project == "newproj"

def test_loaded(project):
    "Checks project is loaded into the framework"
    assert skilift.project_loaded(project, error_if_not=False)

def test_newproj(project):
    "Tests project info obtained from skilift.project_info"
    proj_info = skilift.project_info(project)

    assert proj_info.project == "newproj"
    assert proj_info.version == "0.0.1"
    assert proj_info.brief == "New Project"
    assert proj_info.path == "/"
    assert proj_info.default_language == "en"
    assert 'lib' in proj_info.subprojects

def test_start_call(project):
    "Calls start_call"

    proj = skilift.get_proj(project)

    environ = {}
    path = proj.url
    rootproject = True
    called_ident = None
    caller_ident = None
    received_cookies = {}
    ident_data = None
    lang = ('en-GB', 'en')
    option = {}
    proj_data = proj.proj_data

    skicall = SkiCall(environ, path, project, rootproject, caller_ident, received_cookies, ident_data, lang, option, proj_data)

    # call newproj start_call
    called_ident = newproj.start_call(called_ident, skicall)
    assert called_ident is None

    



