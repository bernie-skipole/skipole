# Tests for project newproj

from skipoles import skilift


def test_index_template(project):
    "Checks newproj index template page 2001"
    proj, page = skilift.get_proj_page(project, pagenumber=2001, pchange=None)
    assert proj.proj_ident == 'newproj'
    assert page.name == "index_template"
    assert page.url == "/restricted/index_template"



def test_add_subproject(project):
    "Tests skilift.add_sub_project"
    # lib should already be loaded
    assert skilift.project_loaded("lib", error_if_not=False)
    # remove it
    skilift.remove_sub_project("lib")
    assert not skilift.project_loaded("lib", error_if_not=False)
    # and add it again
    skilift.add_sub_project("lib")
    assert skilift.project_loaded("lib", error_if_not=False)


def test_labels(project):
    "Tests skilit.get_itemnumber, and labels home and general_json"
    assert skilift.get_itemnumber(project, "home") == 1
    assert skilift.get_itemnumber(project, "general_json") == 2002
