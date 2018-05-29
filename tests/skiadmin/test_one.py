# Tests for project skiadmin

from skipoles import skilift

def test_ident(project):
    assert project == "skiadmin"

def test_language(project):
    assert skilift.project_loaded(project, error_if_not=False)
