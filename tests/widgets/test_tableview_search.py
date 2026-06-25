"""Regression tests for Tableview search (PR #1065).

Search terms containing regex-special characters (``.``, ``(``, ``+``,
``$``, etc.) must match literally. Previously the criteria was escaped
with ``re.escape`` but then matched with ``in``, so any special
character broke the search entirely.

Runnable headlessly with pytest.
"""
from ttkbootstrap.widgets.tableview import Tableview

COLDATA = ["Name", "Value"]
ROWDATA = [
    ("alpha", "a.b"),      # contains '.'
    ("beta", "c(d)e"),     # contains '(' ')'
    ("gamma", "x+y"),      # contains '+'
    ("delta", "price $5"),  # contains '$'
    ("eps", "plain"),      # no special chars
]


def _make_table(app):
    return Tableview(
        master=app, coldata=COLDATA, rowdata=ROWDATA, paginated=False
    )


def _search(table, criteria, *columns):
    table.search_table_data(criteria, *columns)
    names = sorted(r.values[0] for r in table.tablerows_filtered)
    table.reset_row_filters()
    return names


def test_special_characters_match_literally(root):
    table = _make_table(root)
    assert _search(table, "a.b") == ["alpha"]
    assert _search(table, "(d)") == ["beta"]
    assert _search(table, "x+y") == ["gamma"]
    assert _search(table, "$5") == ["delta"]


def test_plain_text_still_matches(root):
    table = _make_table(root)
    assert _search(table, "plain") == ["eps"]


def test_column_specific_search(root):
    table = _make_table(root)
    # 'a.b' is literal special-char text in the Value column only
    assert _search(table, "a.b", "Value") == ["alpha"]
    # scoping the same query to the Name column finds nothing
    assert _search(table, "a.b", "Name") == []