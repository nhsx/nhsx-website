from modules.core.service import _groups, _collections


def test_groups_authors_property():
    g = _groups.authors
    assert isinstance(g, _groups.__model__)
    assert g.name == 'Authors'


def test_ensure_collection():
    c = _collections.ensure('Test Collection')
    assert c is not None
    assert isinstance(c, _collections.__model__)
    assert c.name == 'Test Collection'
