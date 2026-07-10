"""Regression test for Tableview.autofit_columns font awareness (issue #399).

autofit_columns previously hardcoded ``TkDefaultFont`` when measuring text,
so changing the table font (e.g. ``style.configure(".", font=...)``) produced
undersized columns and truncated cells. It now measures with the font actually
configured on the treeview style, falling back to ``TkDefaultFont`` when the
style does not override it.

A single root is used for the whole module because ``Style`` is a process-wide
singleton tied to one Tk root (creating a second ``Window`` is unsupported and
the style config bleeds between them).

Runnable headlessly with pytest, or directly as a script.
"""
from tkinter import font

import ttkbootstrap as ttk
from ttkbootstrap import utility
from ttkbootstrap.widgets.tableview import Tableview

COLDATA = ["Name", "Value"]
# identical long cells (wider than the headers) so both columns autofit to
# the same width and the difference between fonts is unambiguous
SAMPLE = "wwwwwwwwwwwwwwwwwwww"
ROWDATA = [(SAMPLE, SAMPLE)]

# a large, wide font that measures clearly wider than TkDefaultFont
BIG_FONT = ("Courier New", 24)


def _widths(table):
    table.autofit_columns()
    return [table.view.column(i, "width") for i in range(len(COLDATA))]


def test_autofit_is_font_aware():
    app = ttk.Window()
    app.withdraw()
    # `Style` is a process-wide singleton that outlives this root, so restore
    # the root font we override below; otherwise it leaks into later tests.
    original_dot_font = app.style.lookup(".", "font")
    try:
        table = Tableview(
            master=app, coldata=COLDATA, rowdata=ROWDATA, paginated=False
        )
        app.update_idletasks()

        # 1) default font: matches the historical TkDefaultFont behaviour
        default_widths = _widths(table)
        f = font.Font(font="TkDefaultFont")
        pad = utility.scale_size(table, 20)
        expected = f.measure(SAMPLE) + pad
        assert all(w == expected for w in default_widths)

        # 2) override the font on the root style (the technique from #322)
        app.style.configure(".", font=BIG_FONT)
        app.update_idletasks()
        big_widths = _widths(table)

        # the columns must grow to fit the wider font, not stay pinned to the
        # TkDefaultFont measurement (the #399 bug).
        big = font.Font(font=BIG_FONT)
        assert big.measure(SAMPLE) > f.measure(SAMPLE)  # sanity
        assert all(w > d for w, d in zip(big_widths, default_widths))
        assert all(w >= big.measure(SAMPLE) for w in big_widths)
    finally:
        app.style.configure(".", font=original_dot_font or "TkDefaultFont")
        app.destroy()


if __name__ == "__main__":
    test_autofit_is_font_aware()
    print("Tableview autofit font regression test passed.")
