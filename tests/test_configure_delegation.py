"""Tests for the shared configure/cget delegation mixin
(`ttkbootstrap.internal.configure_delegation`) — the backbone the custom-widget
API review (Meter/Floodgauge/DateEntry/Scrolled) builds on.
"""
import tkinter as tk
from tkinter import ttk

import pytest

from ttkbootstrap.internal.configure_delegation import (
    ConfigureDelegationMixin,
    configure_delegate,
)


class _Widget(ConfigureDelegationMixin, ttk.Label):
    """A ttk.Label with one delegated option (`foo`) and one variable option."""

    def __init__(self, master, **kw):
        self._foo = 0
        self._var = tk.IntVar(master=master, value=3)
        super().__init__(master, **kw)

    @configure_delegate("foo")
    def _foo_handler(self, value):
        if value is None:
            return self._foo
        self._foo = value

    @configure_delegate("variable")
    def _var_handler(self, value):
        if value is None:
            return self._var
        self._var = value


class _Composite(ConfigureDelegationMixin, ttk.Frame):
    """A composite that routes non-delegated options to an inner Label."""

    def __init__(self, master):
        self._bar = 1
        super().__init__(master)
        self.inner = ttk.Label(self, text="x")

    def _configure_delegate_target(self):
        return self.inner

    @configure_delegate("bar")
    def _bar_handler(self, value):
        if value is None:
            return self._bar
        self._bar = value


# --------------------------------------------------------------------------
# delegated option round-trips through every access path
# --------------------------------------------------------------------------

def test_delegated_set_and_get_via_configure(root):
    w = _Widget(root)
    w.configure(foo=5)
    assert w.cget("foo") == 5
    assert w["foo"] == 5


def test_delegated_set_via_item_assignment(root):
    w = _Widget(root)
    w["foo"] = 7
    assert w.cget("foo") == 7


def test_configure_query_returns_tk_five_tuple(root):
    w = _Widget(root)
    w.configure(foo=9)
    spec = w.configure("foo")
    # (name, dbName, dbClass, default, current) — the malformed 4-tuple bug fixed.
    assert spec == ("foo", "foo", "Foo", None, 9)
    assert len(spec) == 5


def test_configure_accepts_dict_cnf(root):
    w = _Widget(root)
    w.configure({"foo": 11})
    assert w.cget("foo") == 11


def test_variable_option_returns_tcl_name(root):
    w = _Widget(root)
    # a tk Variable renders as its Tcl name string, like a real cget option
    assert w.cget("variable") == str(w._var)


# --------------------------------------------------------------------------
# non-delegated options fall through to the real widget
# --------------------------------------------------------------------------

def test_non_delegated_option_falls_through_to_widget(root):
    w = _Widget(root)
    w.configure(text="hello")
    assert w.cget("text") == "hello"


def test_unknown_option_raises(root):
    w = _Widget(root)
    with pytest.raises(tk.TclError):
        w.cget("definitely_not_an_option")


# --------------------------------------------------------------------------
# discovery: keys() and the no-arg configure() dict include delegated options
# --------------------------------------------------------------------------

def test_keys_include_delegated_options(root):
    w = _Widget(root)
    keys = w.keys()
    assert "foo" in keys and "variable" in keys
    assert "text" in keys  # real ttk.Label option still present


def test_configure_no_arg_dict_includes_delegated(root):
    w = _Widget(root)
    w.configure(foo=4)
    full = w.configure()
    assert full["foo"] == ("foo", "foo", "Foo", None, 4)
    assert "text" in full  # real options still there


# --------------------------------------------------------------------------
# inner-widget fallthrough (composite proxying to an inner widget)
# --------------------------------------------------------------------------

def test_composite_routes_passthrough_to_inner_widget(root):
    c = _Composite(root)
    c.configure(text="hey")  # ttk.Frame has no 'text'; must reach the inner Label
    assert c.cget("text") == "hey"
    assert c.inner.cget("text") == "hey"


def test_composite_still_handles_its_own_delegated_option(root):
    c = _Composite(root)
    c.configure(bar=9)
    assert c.cget("bar") == 9
    assert c["bar"] == 9
