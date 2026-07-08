"""Headless API tests for the 2.0 Scrolled widget rewrite (widget review PR 5).

Covers the ScrolledFrame Canvas-viewport rewrite (back-compat contract, tuple
`yview`, no pre-realize div-by-zero, container-leak-fixing `destroy`, class-tag
mousewheel seam) and the ScrolledText mixin delegation + grid layout (no
hbar-without-vbar crash). Uses the shared `root` fixture from conftest.
"""
import warnings

import pytest

import ttkbootstrap as ttk
from ttkbootstrap.widgets.scrolled import ScrolledFrame, ScrolledText


# --------------------------------------------------------------------------- #
# ScrolledFrame
# --------------------------------------------------------------------------- #
def test_children_parent_to_the_content_frame(root):
    sf = ScrolledFrame(root)
    sf.pack(fill="both", expand=True)
    child = ttk.Checkbutton(sf, text="x")
    assert child.winfo_parent() == str(sf)


def test_container_attribute_exists(root):
    sf = ScrolledFrame(root)
    assert sf.container is not None
    assert bool(sf.container.winfo_exists())


def test_pack_forwards_to_the_container(root):
    sf = ScrolledFrame(root)
    sf.pack(fill="both", expand=True)
    sf.update_idletasks()
    # sf.pack() forwards to the container (the whole assembly), so the container
    # is the pack-managed widget -- not the content frame.
    assert sf.container.winfo_manager() == "pack"
    assert bool(sf.container.pack_info())


def test_yview_returns_a_two_tuple(root):
    sf = ScrolledFrame(root)
    sf.pack(fill="both", expand=True)
    ttk.Label(sf, text="x").pack()
    sf.update_idletasks()
    view = sf.yview()
    assert isinstance(view, tuple) and len(view) == 2
    assert view is not None  # the old impl returned None


def test_no_div_by_zero_before_realize(root):
    # Constructing + immediately laying out must not raise (the old _measures
    # divided by an unrealized container height).
    sf = ScrolledFrame(root)
    sf.pack(fill="both", expand=True)
    for i in range(30):
        ttk.Label(sf, text=f"row {i}").pack()
    sf.update_idletasks()  # would raise ZeroDivisionError under the old code path
    assert bool(sf.container.winfo_exists())


def test_destroy_tears_down_the_container(root):
    sf = ScrolledFrame(root)
    sf.pack(fill="both", expand=True)
    ttk.Label(sf, text="x").pack()
    sf.update_idletasks()
    container = sf.container
    canvas = sf._canvas
    sf.destroy()
    assert not bool(container.winfo_exists())  # the old no-op destroy leaked this
    assert not bool(canvas.winfo_exists())


def test_ancestor_cascade_destroy_is_clean(root):
    holder = ttk.Frame(root)
    holder.pack(fill="both", expand=True)
    sf = ScrolledFrame(holder)
    sf.pack(fill="both", expand=True)
    ttk.Label(sf, text="x").pack()
    sf.update_idletasks()
    container = sf.container
    holder.destroy()  # must not raise a double-destroy TclError
    assert not bool(container.winfo_exists())


def test_mousewheel_class_tag_toggles_with_scrolling(root):
    sf = ScrolledFrame(root)
    sf.pack(fill="both", expand=True)
    child = ttk.Label(sf, text="x")
    child.pack()
    sf.update_idletasks()

    sf.enable_scrolling()
    assert sf._wheel_tag in child.bindtags()

    sf.disable_scrolling()
    assert sf._wheel_tag not in child.bindtags()


def test_legacy_autohide_and_scrollheight_warn(root):
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        sf = ScrolledFrame(root, autohide=True, scrollheight=400)
    kinds = [w for w in caught if issubclass(w.category, DeprecationWarning)]
    assert len(kinds) == 2
    assert sf.auto_hide is True


def test_vscroll_alias_and_vbar_property(root):
    sf = ScrolledFrame(root)
    assert sf.vbar is sf.vscroll
    assert sf.hbar is None


def test_autohide_scrollbar_toggles(root):
    sf = ScrolledFrame(root)
    assert sf.auto_hide is False
    sf.autohide_scrollbar()
    assert sf.auto_hide is True
    sf.autohide_scrollbar()
    assert sf.auto_hide is False


# --------------------------------------------------------------------------- #
# ScrolledText
# --------------------------------------------------------------------------- #
def test_configure_and_cget_reach_the_text(root):
    st = ScrolledText(root, height=5)
    st.pack()
    st.configure(font=("Helvetica", 13))
    assert str(st.cget("font")) == "Helvetica 13"
    st.configure(wrap="word")
    assert str(st.cget("wrap")) == "word"


def test_method_delegation_to_text(root):
    st = ScrolledText(root, height=5)
    st.pack()
    st.insert("end", "hello world")
    assert st.get("1.0", "end").strip() == "hello world"


def test_hbar_without_vbar_constructs(root):
    # Old code raised AttributeError in _on_configure for this combination.
    st = ScrolledText(root, hbar=True, vbar=False)
    st.pack()
    st.update_idletasks()
    assert st.vbar is None
    assert st.hbar is not None
    assert str(st.cget("wrap")) == "none"  # hbar forces wrap=none


def test_scrolledtext_legacy_autohide_warns(root):
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        st = ScrolledText(root, autohide=True)
    assert any(issubclass(w.category, DeprecationWarning) for w in caught)
    assert st.auto_hide is True


def test_scrolledtext_autohide_scrollbar_toggles(root):
    st = ScrolledText(root)
    assert st.auto_hide is False
    st.autohide_scrollbar()
    assert st.auto_hide is True