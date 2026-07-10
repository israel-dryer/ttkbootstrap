"""Regression tests for the 2.0 removal of the character-based icons.

The legacy ``ttkbootstrap.icons`` module (the ``Emoji``/``EmojiItem`` catalog
and the base64 ``Icon`` constants) is gone. Its two first-party consumers were
rewired: the four ``Messagebox`` alert icons now render from the Bootstrap-Icons
font glyph engine, and the default window icon (the brand logo) moved to a
private constant in ``window.py``. See ``development/2_0_icon_drop_design.md``.
"""
import importlib

import pytest

import ttkbootstrap as ttk
from ttkbootstrap.dialogs.message import (
    MessageDialog,
    _ALERT_ICONS,
    _alert_icon,
)
from ttkbootstrap.window import _DEFAULT_ICON_DATA


def _icon_label_image(container):
    """Return the icon Label's image name in a create_body container, or None."""
    # create_body builds one inner container Frame; its first LEFT-packed child
    # is the icon Label when an icon was supplied.
    inner = container.winfo_children()[0]
    for w in inner.winfo_children():
        # Only Labels carry an -image option; the message lives in a sub-frame
        # that would raise on cget("image"), so gate on the class first.
        if w.winfo_class() != "TLabel":
            continue
        image = w.cget("image")
        if image:
            # Tk may hand back a 1-tuple for the -image option; normalize to str.
            return image[0] if isinstance(image, tuple) else image
    return None


def test_legacy_icons_module_is_removed():
    """The old module and its emoji/base64 surface are gone."""
    with pytest.raises(ImportError):
        importlib.import_module("ttkbootstrap.icons")


def test_top_level_icon_is_the_glyph_atom():
    """``ttk.Icon`` is the font-glyph atom, not the removed base64 container."""
    assert ttk.Icon.__module__ == "ttkbootstrap.style.icons"
    assert callable(ttk.Icon)


def test_alert_icons_render_to_valid_images(root):
    """Each of the four alert kinds renders its glyph to a live Tk image."""
    existing = set(root.tk.call("image", "names"))
    for kind in _ALERT_ICONS:
        name = _alert_icon(kind)
        assert name in root.tk.call("image", "names")
    # rendering created new images (or reused cached ones), none were dropped
    assert existing <= set(root.tk.call("image", "names"))


def test_default_messagebox_icons_use_glyphs(root):
    """A MessageDialog given a rendered glyph name shows it as an icon Label."""
    glyph = _alert_icon("warning")
    dialog = MessageDialog("careful", icon=glyph)
    frame = ttk.Frame(root)
    dialog.create_body(frame)
    assert _icon_label_image(frame) == glyph


def test_messagebox_still_accepts_base64_data(root):
    """Back-compat: a base64 data icon still builds a retained PhotoImage label."""
    dialog = MessageDialog("hello", icon=_DEFAULT_ICON_DATA)
    frame = ttk.Frame(root)
    dialog.create_body(frame)
    assert _icon_label_image(frame) is not None
    # the inline PhotoImage is retained on the dialog so it is not GC'd
    assert dialog._img is not None


def test_messagebox_bad_icon_does_not_crash(root):
    """An unusable icon string is skipped, not fatal (no icon label)."""
    dialog = MessageDialog("hello", icon="not-an-image-or-a-path")
    frame = ttk.Frame(root)
    dialog.create_body(frame)  # prints a notice, must not raise
    assert _icon_label_image(frame) is None


def test_default_window_icon_data_is_valid(root):
    """The relocated brand-logo constant still yields a 32x32 PhotoImage."""
    img = ttk.PhotoImage(data=_DEFAULT_ICON_DATA, master=root)
    assert (img.width(), img.height()) == (32, 32)
