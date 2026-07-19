"""Headless tests for font-aware Treeview/Tableview row height (#1160).

`rowheight` was computed from `TkDefaultFont` at build time, so a font the user
actually configured was ignored and taller text was clipped. It now derives from
the font the style will really use.

Assertions are relative (grew vs. the default) rather than absolute pixel counts,
since font metrics vary by platform and DPI.

The styles touched here are shared, so an autouse fixture restores their font and
rebuilds them; `font` is a durable option (#1238) and would otherwise leak.
"""
import pytest

import ttkbootstrap as ttk
from ttkbootstrap.widgets.tableview import Tableview

BIG = "-size 30"


def _rowheight(app, style_name):
    return int(app.tk.call("ttk::style", "lookup", style_name, "-rowheight"))


def _rebuild(app, variant):
    app.style._get_builder().build_style(variant, "treeview", "default")


@pytest.fixture(autouse=True)
def _isolate(root):
    yield
    style = root.style
    style.reset_style_options()
    for name in ("Treeview", "Table.Treeview"):
        style._build_configure(name, font="TkDefaultFont")
    for variant in ("default", "table"):
        try:
            _rebuild(root, variant)
        except Exception:
            pass


# --- the row follows the configured font -----------------------------------

def test_treeview_rowheight_follows_configured_font(root):
    _rebuild(root, "default")
    before = _rowheight(root, "Treeview")
    root.style.configure("Treeview", font=BIG)
    _rebuild(root, "default")
    assert _rowheight(root, "Treeview") > before


def test_table_treeview_rowheight_follows_configured_font(root):
    _rebuild(root, "table")
    before = _rowheight(root, "Table.Treeview")
    root.style.configure("Table.Treeview", font=BIG)
    _rebuild(root, "table")
    assert _rowheight(root, "Table.Treeview") > before


def test_rowheight_accepts_tuple_font(root):
    """The #322 technique passes a ("family", size) tuple, not a named font."""
    _rebuild(root, "table")
    before = _rowheight(root, "Table.Treeview")
    root.style.configure("Table.Treeview", font=("Courier", 30))
    _rebuild(root, "table")
    assert _rowheight(root, "Table.Treeview") > before


def test_variant_inherits_ancestor_font(root):
    """A font on the base class sizes a variant built afterwards."""
    _rebuild(root, "default")
    before = _rowheight(root, "Treeview")
    root.style.configure("Treeview", font=BIG)
    ttk.Treeview(root, bootstyle="danger")  # builds danger.Treeview fresh
    assert _rowheight(root, "danger.Treeview") > before


def test_tableview_widget_rows_follow_font(root):
    """End-to-end through the real widget, not just the recipe.

    Uses a color variant so the widget genuinely builds a new style, matching
    the real flow (configure the font, then create the first such widget). A
    style that already exists is not rebuilt, so a font set afterwards does not
    resize it -- the deferred live-recompute case.
    """
    _rebuild(root, "table")
    before = _rowheight(root, "Table.Treeview")
    root.style.configure("Table.Treeview", font=BIG)
    Tableview(
        root,
        coldata=["Name", "Value"],
        rowdata=[("alpha", "one")],
        bootstyle="info",
    )
    assert _rowheight(root, "info.Table.Treeview") > before


# --- defaults still sane ----------------------------------------------------

def test_default_rowheight_is_positive(root):
    _rebuild(root, "default")
    _rebuild(root, "table")
    assert _rowheight(root, "Treeview") > 0
    assert _rowheight(root, "Table.Treeview") > 0


def test_grid_row_is_taller_than_plain_row(root):
    """Table.Treeview adds ~half an ascent of breathing room; Treeview does not."""
    _rebuild(root, "default")
    _rebuild(root, "table")
    assert _rowheight(root, "Table.Treeview") > _rowheight(root, "Treeview")


def test_unset_font_falls_back_to_default_metrics(root):
    """With no configured font the row is still sized (TkDefaultFont fallback)."""
    root.style.reset_style_options()
    root.style._build_configure("Treeview", font="TkDefaultFont")
    _rebuild(root, "default")
    assert _rowheight(root, "Treeview") > 0
