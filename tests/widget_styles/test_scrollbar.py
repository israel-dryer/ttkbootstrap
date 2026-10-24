"""Tests for the scrollbar styles.

A thin scrollbar is a few-pixel flat thumb on a surface-matched track with no
arrows -- for narrow lists/dropdowns (combobox popdown, font dialog). Neutral by
default, or the accent when a color is given. See
`development/2_0_breaking_changes.md`.
"""
import pytest

import ttkbootstrap as ttk


def _lookup(app, style, option):
    return str(app.tk.call("ttk::style", "lookup", style, f"-{option}")).lower()


def test_thin_scrollbar_builds_arrowless_on_the_surface(root):
    """`bootstyle="thin"` builds a vertical + horizontal arrowless scrollbar
    whose track matches the surface."""
    style = root.style
    ttk.Scrollbar(root, orient="vertical", bootstyle="thin")
    ttk.Scrollbar(root, orient="horizontal", bootstyle="thin")
    root.update_idletasks()
    for st in ("Thin.Vertical.TScrollbar", "Thin.Horizontal.TScrollbar"):
        assert style.style_exists_in_theme(st)
        assert _lookup(root, st, "arrowsize") in ("0", "")
        assert _lookup(root, st, "troughcolor") == str(style.colors.bg).lower()


def test_thin_scrollbar_accepts_a_color(root):
    """A colored thin scrollbar builds its own style."""
    style = root.style
    ttk.Scrollbar(root, orient="vertical", bootstyle="primary-thin")
    root.update_idletasks()
    assert style.style_exists_in_theme("primary.Thin.Vertical.TScrollbar")


def _stretching_nodes(layout, axis_sticky):
    """Layout nodes from the thumb down that stretch along the bar: the thumb
    itself (the scrollbar sizes it) and any child sticky along the axis."""
    for name, opts in layout:
        children = opts.get("children", [])
        if name.endswith(".thumb"):
            yield name
            for child, child_opts in children:
                if set(axis_sticky) <= set(child_opts.get("sticky", "")):
                    yield child
        else:
            yield from _stretching_nodes(children, axis_sticky)


@pytest.mark.parametrize("bootstyle", ["default", "round", "thin", "primary round"])
@pytest.mark.parametrize("orient", ["vertical", "horizontal"])
def test_scrollbar_thumb_does_not_stretch_an_image(root, bootstyle, orient):
    """ttk tiles, not stretches, the middle of an image element: a 9-sliced
    image thumb with a 1px middle is redrawn from one tile per pixel of thumb
    length (milliseconds per redraw on a tall thumb). Images may only be the
    fixed-size end caps; what stretches must be a plain element. An image
    element is the one kind that reports no options."""
    sb = ttk.Scrollbar(root, orient=orient, bootstyle=bootstyle)
    root.update_idletasks()
    style = sb.cget("style")
    nodes = list(_stretching_nodes(
        root.style.layout(style), "ns" if orient == "vertical" else "we"))
    assert nodes
    for name in nodes:
        assert root.tk.call("ttk::style", "element", "options", name), name


def test_scrollbar_thumb_color_follows_state(root):
    """The thumb body darkens/lightens on hover and press, like the caps."""
    ttk.Scrollbar(root, orient="vertical")
    root.update_idletasks()

    def fill(*state):
        return str(root.tk.call("ttk::style", "lookup", "Vertical.TScrollbar",
                                "-fieldbackground", state)).lower()

    assert len({fill(), fill("active"), fill("pressed")}) == 3
