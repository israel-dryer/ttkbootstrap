"""Headless tests for the 2.0 Tableview API normalization (PR C).

Covers the parts checkable without a real display:
- the top-level / widgets-package re-exports (``ttk.Tableview`` et al.),
- the two latent-bug regressions (``delete_column(cid=...)`` and the
  right-click-menu ``master`` self-assignment),
- ``insert_row`` raising instead of printing on empty values,
- the dead code (``reset_row_sort`` / the two private builders) being gone.
"""
import pytest

import ttkbootstrap as ttk
from ttkbootstrap import widgets as _widgets
from ttkbootstrap.widgets.tableview import (
    TableColumn,
    TableHeaderRightClickMenu,
    TableRow,
    Tableview,
)


# --------------------------------------------------------------------------
# re-exports
# --------------------------------------------------------------------------

def test_tableview_reexported_at_top_level():
    assert ttk.Tableview is Tableview
    assert ttk.TableColumn is TableColumn
    assert ttk.TableRow is TableRow
    for name in ("Tableview", "TableColumn", "TableRow"):
        assert name in ttk.__all__


def test_tableview_reexported_from_widgets_package():
    assert _widgets.Tableview is Tableview
    assert _widgets.TableColumn is TableColumn
    assert _widgets.TableRow is TableRow
    for name in ("Tableview", "TableColumn", "TableRow"):
        assert name in _widgets.__all__


# --------------------------------------------------------------------------
# latent-bug regressions
# --------------------------------------------------------------------------

def _make_table(root):
    return Tableview(
        root,
        coldata=["A", "B", "C"],
        rowdata=[["a1", "b1", "c1"], ["a2", "b2", "c2"]],
    )


def test_delete_column_by_cid(root):
    # Regression: delete_column used ``self.cidmap(int(cid))`` (calling a
    # dict), which raised TypeError before it could ever delete a column.
    tv = _make_table(root)
    assert len(tv.tablecolumns) == 3
    tv.delete_column(cid=1)
    assert len(tv.tablecolumns) == 2


def test_header_rightclick_menu_master_is_the_table(root):
    # Regression: ``self.master = self.master`` never set master from the arg.
    tv = _make_table(root)
    menu = TableHeaderRightClickMenu(tv)
    assert menu.master is tv


# --------------------------------------------------------------------------
# insert_row empty-values behavior
# --------------------------------------------------------------------------

def test_insert_row_empty_values_raises(root):
    # Was a stdout ``print`` + silent ``None`` return; now a loud error.
    tv = _make_table(root)
    with pytest.raises(ValueError):
        tv.insert_row(values=[])


# --------------------------------------------------------------------------
# dead code removed
# --------------------------------------------------------------------------

def test_dead_code_removed():
    for name in ("reset_row_sort", "_build_table_rows", "_build_table_columns"):
        assert not hasattr(Tableview, name)


# --------------------------------------------------------------------------
# pagination navigation buttons (glyph icons + boundary-disable)
# --------------------------------------------------------------------------

def _make_paginated_table(root):
    # pagesize=2 over 6 rows -> 3 pages, so every boundary is reachable.
    return Tableview(
        root,
        coldata=["A", "B"],
        rowdata=[[f"a{i}", f"b{i}"] for i in range(6)],
        paginated=True,
        pagesize=2,
    )


def _nav_disabled(tv):
    return {
        "first": tv._pagefirst.instate(["disabled"]),
        "prev": tv._pageprev.instate(["disabled"]),
        "next": tv._pagenext.instate(["disabled"]),
        "last": tv._pagelast.instate(["disabled"]),
    }


def test_pagination_nav_buttons_are_ghost_icon_buttons(root):
    tv = _make_paginated_table(root)
    for btn in (tv._pagefirst, tv._pageprev, tv._pagenext, tv._pagelast):
        # apply_icon derives an ``Icon<hash>.`` style off the ghost base.
        assert "Ghost.TButton" in str(btn.cget("style"))


def test_pagination_first_page_disables_backward(root):
    tv = _make_paginated_table(root)
    tv.goto_first_page()
    state = _nav_disabled(tv)
    assert state["first"] and state["prev"]
    assert not state["next"] and not state["last"]


def test_pagination_last_page_disables_forward(root):
    tv = _make_paginated_table(root)
    tv.goto_last_page()
    state = _nav_disabled(tv)
    assert state["next"] and state["last"]
    assert not state["first"] and not state["prev"]


def test_pagination_middle_page_all_enabled(root):
    tv = _make_paginated_table(root)
    tv.goto_first_page()
    tv.goto_next_page()  # page 2 of 3
    assert not any(_nav_disabled(tv).values())


# --------------------------------------------------------------------------
# verb-rename slice: canonical names + deprecated aliases
# --------------------------------------------------------------------------

def test_row_move_verb_is_consistent(root):
    """`move_selected_row_down` matches move_selected_row_up; old name warns."""
    import warnings
    tv = _make_table(root)
    assert hasattr(tv, "move_selected_row_down")
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        tv.move_row_down()  # no selection -> no-op, but must warn
    assert any(issubclass(w.category, DeprecationWarning) for w in caught)


def test_column_show_verb_is_consistent(root):
    """`show_selected_column` replaces the odd `unhide` verb; old name warns."""
    import warnings
    tv = _make_table(root)
    assert hasattr(tv, "show_selected_column")
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        tv.unhide_selected_column()
    assert any(issubclass(w.category, DeprecationWarning) for w in caught)


def test_get_columns_deprecated_for_tablecolumns_property(root):
    import warnings
    tv = _make_table(root)
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        cols = tv.get_columns()
    assert any(issubclass(w.category, DeprecationWarning) for w in caught)
    assert cols == tv.tablecolumns


# --------------------------------------------------------------------------
# header sort indicator: font-glyph icon instead of an ASCII arrow
# --------------------------------------------------------------------------

def test_sort_shows_glyph_icon_not_ascii_arrow(root):
    tv = _make_table(root)
    cid = tv.tablecolumns[0].cid
    assert tv.view.heading(cid, "image") in ("", ())      # none before sort
    tv.sort_column_data(cid=cid, sort=0)                    # ascending
    assert tv.view.heading(cid, "image")                   # a glyph image now
    text = tv.view.heading(cid, "text")
    assert "⬆" not in text and "⬇" not in text   # no ⬆/⬇ in the text
    tv._column_sort_header_reset()
    assert tv.view.heading(cid, "image") in ("", ())       # cleared on reset
