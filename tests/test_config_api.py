"""Headless tests for the 2.0 deferred-config seam (Slice 5).

The pending-apply registry lets pre-root setters (`ttk.default_button(...)`, and
later `set_locale`/`set_global_family`) record intent before `App()` exists and
be flushed when the root comes up; if a root already exists, the setter applies
immediately. `default_button` is the proof tenant.
"""
import inspect

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
    value_before = config._pending_default_button
    try:
        yield root
    finally:
        root.style.default_button = before
        config._pending.clear()
        config._pending.update(pending_before)
        config._pending_default_button = value_before


# --------------------------------------------------------------------------
# exposure
# --------------------------------------------------------------------------

def test_default_button_is_exported():
    assert ttk.default_button is config.default_button
    assert "default_button" in ttk.__all__
    from ttkbootstrap import utils
    assert utils.default_button is config.default_button
    assert "default_button" in utils.__all__


def test_app_and_style_default_button_arg_is_sentinel_none():
    # the None sentinel is what lets an explicit arg be distinguished from the
    # default and so win over a pre-root ttk.default_button() setting
    assert inspect.signature(App.__init__).parameters["default_button"].default is None
    assert inspect.signature(StyleClass.__init__).parameters["default_button"].default is None


# --------------------------------------------------------------------------
# getter / live setter (root already exists)
# --------------------------------------------------------------------------

def test_getter_returns_current_default(root):
    assert ttk.default_button() == root.style.default_button


def test_live_set_warns_and_applies_for_future_builds(restore_default_button):
    root = restore_default_button
    with pytest.warns(UserWarning, match="after the application root was created"):
        ttk.default_button("primary")
    assert root.style.default_button == "primary"
    assert ttk.default_button() == "primary"  # getter reflects the live value


# --------------------------------------------------------------------------
# pre-root queue + flush
# --------------------------------------------------------------------------

def test_pre_root_setter_queues_then_flush_applies(restore_default_button, monkeypatch):
    root = restore_default_button
    config._pending.clear()
    config._pending_default_button = None

    # simulate "no root yet" so the setter queues instead of applying live
    monkeypatch.setattr(Style, "instance", None)
    with _no_warning():  # the pre-root queue path must be silent (no warning)
        result = ttk.default_button("info")
    assert result == "info"
    assert config.default_button() == "info"       # pre-root getter = the pending value
    assert "default_button" in config._pending      # queued, not applied

    # root is back -> flush runs the queued applier
    monkeypatch.undo()
    config.flush_pending_config()
    assert root.style.default_button == "info"
    assert not config._pending                       # queue cleared


def test_defer_applies_immediately_when_root_exists(restore_default_button):
    root = restore_default_button
    config._pending.clear()
    calls = []
    config.defer("probe", lambda: calls.append(True))
    # a root exists (the session root), so defer runs now and queues nothing
    assert calls == [True]
    assert "probe" not in config._pending


class _no_warning:
    """Assert the block emits no warning (the pre-root queue path is silent)."""

    def __enter__(self):
        import warnings

        self._cm = warnings.catch_warnings()
        self._cm.__enter__()
        warnings.simplefilter("error")
        return self

    def __exit__(self, *exc):
        return self._cm.__exit__(*exc)
