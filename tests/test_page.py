from pypcom.page import Page


def test_page():
    page = Page(1)
    assert isinstance(page, Page)
