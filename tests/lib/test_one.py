# Tests for project lib

from skipoles import skilift

def test_ident(project):
    assert project == "lib"

def test_language(project):
    assert skilift.project_loaded(project, error_if_not=False)
