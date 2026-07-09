"""Mixin API delivery tests (2.0 Workstream C / PR 3).

The bootstyle/autostyle API is delivered through concrete subclasses
(`BootMixin`/`AutoStyleMixin`) re-exported from `ttkbootstrap`, not an
import-time monkey-patch of tkinter. These tests pin that contract: the blessed
widgets carry the API, importing ttkbootstrap leaves stock tkinter untouched,
and the opt-in helpers (`bootify`, `apply_bootstyle`, `enable_global_api`)
behave as designed.

NOTE: tests run top-to-bottom within this module. `enable_global_api()` is an
irreversible, process-wide switch, so the test that asserts stock tkinter is
*unpatched* must come before the test that enables the global API.
"""
import tkinter
from tkinter import ttk as tkttk

import pytest

import ttkbootstrap as ttk
from ttkbootstrap.style import BootMixin, AutoStyleMixin


# --------------------------------------------------------------------------- #
# Shape of the blessed classes
# --------------------------------------------------------------------------- #
def test_blessed_ttk_widget_is_bootmixin_subclass():
    assert issubclass(ttk.Button, BootMixin)
    assert issubclass(ttk.Button, tkttk.Button)


def test_blessed_tk_widget_is_autostylemixin_subclass():
    assert issubclass(ttk.Canvas, AutoStyleMixin)
    assert issubclass(ttk.Canvas, tkinter.Canvas)


def test_stock_tkinter_is_unpatched_by_default(root):
    """Importing ttkbootstrap must not mutate the stock tkinter classes.

    Must run before any test calls enable_global_api() (see module docstring).
    """
    assert not issubclass(tkttk.Button, BootMixin)
    with pytest.raises(tkinter.TclError):
        tkttk.Button(root, bootstyle="success")


# --------------------------------------------------------------------------- #
# bootstyle resolution via the concrete subclass
# --------------------------------------------------------------------------- #
def test_bootstyle_kwarg_resolves_to_ttk_style(root):
    b = ttk.Button(root, bootstyle="success")
    assert b.cget("style") == "success.TButton"


def test_no_bootstyle_applies_default(root):
    b = ttk.Button(root)
    assert b.cget("style") == "TButton"


def test_configure_bootstyle_updates_style(root):
    b = ttk.Button(root, bootstyle="success")
    b.configure(bootstyle="danger")
    assert b.cget("style") == "danger.TButton"
    # config alias mirrors configure
    b.config(bootstyle="info")
    assert b.cget("style") == "info.TButton"


def test_item_access_routes_bootstyle(root):
    b = ttk.Button(root)
    b["bootstyle"] = "warning"
    assert b["bootstyle"] == "warning.TButton"
    # a non-style item still behaves normally
    b["text"] = "Save"
    assert b["text"] == "Save"


def test_tuple_bootstyle_back_compat(root):
    """The legacy tuple form still resolves, but now warns (Workstream D, D2:
    warn-and-normalize through 2.x, removed in 3.0)."""
    with pytest.warns(DeprecationWarning, match="tuple/list bootstyle"):
        b = ttk.Button(root, bootstyle=("success", "outline"))
    assert b.cget("style") == "success.Outline.TButton"


def test_optionmenu_constructs_and_keeps_item_access(root):
    var = tkinter.StringVar(master=root)
    om = ttk.OptionMenu(root, var, "a", "a", "b", bootstyle="info")
    assert isinstance(om, BootMixin)
    # OptionMenu keeps tkinter's __getitem__ (menu-item access), not BootMixin's
    # bootstyle routing -- 'menu' must still resolve to the attached Menu widget
    # (BootMixin's __getitem__ would have returned the style string instead).
    assert isinstance(om["menu"], tkinter.Menu)


# --------------------------------------------------------------------------- #
# fluent geometry: pack/grid/place return the widget
# --------------------------------------------------------------------------- #
def test_pack_returns_self_and_places_widget(root):
    b = ttk.Button(root)
    assert b.pack(padx=5) is b
    assert b.winfo_manager() == "pack"
    # the *_configure spelling is covered too
    assert b.pack_configure(padx=10) is b


def test_grid_returns_self_and_places_widget(root):
    f = ttk.Frame(root)
    b = ttk.Button(f)
    assert b.grid(row=0, column=0) is b
    assert b.winfo_manager() == "grid"
    assert b.grid_configure(padx=2) is b


def test_place_returns_self_and_places_widget(root):
    f = ttk.Frame(root)
    b = ttk.Button(f)
    assert b.place(x=0, y=0) is b
    assert b.winfo_manager() == "place"
    assert b.place_configure(x=5) is b


def test_fluent_geometry_on_autostyle_tk_widget(root):
    c = ttk.Canvas(root)
    assert c.pack() is c
    assert c.winfo_manager() == "pack"


def test_construct_and_pack_in_one_expression(root):
    b = ttk.Button(root, text="Save", bootstyle="success").pack(padx=10)
    assert isinstance(b, ttk.Button)
    assert b.cget("style") == "success.TButton"
    assert b.winfo_manager() == "pack"


# --------------------------------------------------------------------------- #
# autostyle (tk) path + opt-out
# --------------------------------------------------------------------------- #
def test_autostyle_widget_is_stamped(root):
    c = ttk.Canvas(root)
    assert hasattr(c, "_theme_version")


def test_autostyle_false_opts_out(root):
    c = ttk.Canvas(root, autostyle=False, background="#abcdef")
    assert getattr(c, "_tb_no_autostyle", False) is True
    assert not hasattr(c, "_theme_version")
    assert c.cget("background") == "#abcdef"


# --------------------------------------------------------------------------- #
# Opt-in helpers
# --------------------------------------------------------------------------- #
def test_bootify_wraps_arbitrary_ttk_class(root):
    Wrapped = ttk.bootify(tkttk.Button)
    assert issubclass(Wrapped, BootMixin)
    w = Wrapped(root, bootstyle="warning")
    assert w.cget("style") == "warning.TButton"


def test_apply_bootstyle_styles_existing_instance(root):
    b = tkttk.Button(root)  # a stock, unwrapped widget
    returned = ttk.apply_bootstyle(b, "danger")
    assert returned == "danger.TButton"
    assert b.cget("style") == "danger.TButton"


def test_enable_global_api_is_idempotent_and_styles_stock_widgets(root):
    """Runs last: enabling the global API is an irreversible process-wide switch."""
    ttk.enable_global_api()
    ttk.enable_global_api()  # second call must be a no-op, not an error

    # a stock ttk widget now accepts bootstyle
    b = tkttk.Button(root, bootstyle="success")
    assert b.cget("style") == "success.TButton"

    # the blessed subclass still resolves exactly once (guard defers to mixin)
    b2 = ttk.Button(root, bootstyle="info")
    assert b2.cget("style") == "info.TButton"
