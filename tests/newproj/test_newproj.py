# Tests for project newproj

from skipoles import skilift


def test_index_template(project):
    "Checks newproj index template page 2001"
    proj, page = skilift.get_proj_page(project, pagenumber=2001, pchange=None)
    assert proj.proj_ident == 'newproj'
    assert page.name == "index_template"
    assert page.url == "/restricted/index_template"


