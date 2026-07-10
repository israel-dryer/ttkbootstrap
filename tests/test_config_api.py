"""Headless tests for the 2.0 deferred-config seam (Slice 5).

The pending-apply registry lets pre-root setters (`ttk.set_default_button(...)`,
and later `set_locale`/`set_global_family`) record intent before `App()` exists
and be flushed when the root comes up; if a root already exists, the setter
applies immediately. `set_default_button` is the proof tenant.
"""
import inspect
import warnings

import pytest

import ttkbootstrap as ttk
from ttkbootstrap.style import Style
from ttkbootstrap.style.engine import Style as StyleClass
from ttkbootstrap.utils import config
from ttkbootstrap.window import App


@pytest.fixture
def restore_default_button(root):
    """Snapshot + restore the live default_button and the pending registry so a
    test that pokes them does not leak into the next."""
    before = root.style.default_button
    pending_before = dict(config._pending)
    try:
        yield root
    finally:
        root.style.default_button = before
        config._pending.clear()
        config._pending.update(pending_before)


# --------------------------------------------------------------------------
# exposure
# --------------------------------------------------------------------------

def test_set_default_button_is_exported():
    assert ttk.set_default_button is config.set_default_button
    assert "set_default_button" in ttk.__all__
    from ttkbootstrap import utils
    assert utils.set_default_button is config.set_default_button
    assert "set_default_button" in utils.__all__


def test_app_and_style_default_button_arg_is_sentinel_none():
    # the None sentinel is what lets an explicit arg be distinguished from the
    # default and so win over a pre-root ttk.set_default_button() setting
    assert inspect.signature(App.__init__).parameters["default_button"].default is None
    assert inspect.signature(StyleClass.__init__).parameters["default_button"].default is None


# --------------------------------------------------------------------------
# live setter (root already exists)
# --------------------------------------------------------------------------

def test_live_set_warns_and_applies_for_future_builds(restore_default_button):
    root = restore_default_button
    with pytest.warns(UserWarning, match="after the application root was created"):
        ttk.set_default_button("primary")
    assert root.style.default_button == "primary"


# --------------------------------------------------------------------------
# pre-root queue + flush
# --------------------------------------------------------------------------

def test_pre_root_setter_queues_then_flush_applies(restore_default_button, monkeypatch):
    root = restore_default_button
    config._pending.clear()

    # simulate "no root yet" so the setter queues instead of applying live; the
    # queue path must be silent (no warning)
    monkeypatch.setattr(Style, "instance", None)
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        ttk.set_default_button("info")
    assert "default_button" in config._pending      # queued, not applied

    # root is back -> flush runs the queued applier (which captured "info")
    monkeypatch.undo()
    config.flush_pending_config()
    assert root.style.default_button == "info"
    assert not config._pending                       # queue cleared


def test_defer_applies_immediately_when_root_exists(restore_default_button):
    config._pending.clear()
    calls = []
    config.defer("probe", lambda: calls.append(True))
    # a root exists (the session root), so defer runs now and queues nothing
    assert calls == [True]
    assert "probe" not in config._pending
