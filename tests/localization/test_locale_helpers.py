"""Headless tests for the 2.0 localization slice (Slice 3).

Covers the msgcat bug fixes (`tk.call` escaping, `preferences()` no-drop,
locale normalization, the `<<LocaleChanged>>` event) and the ergonomic helpers
(`L`, `LocaleVar`, `set_locale`). Uses a throwaway locale code (`zz`) so no
bundled `.msg` catalog is auto-loaded -- in particular it never touches `nl`,
whose Tk-packaged catalog is unreadable in this environment.
"""
import warnings

import pytest

import ttkbootstrap as ttk
from ttkbootstrap import localization
from ttkbootstrap.localization import MessageCatalog, L, LocaleVar, set_locale
from ttkbootstrap.localization.msgcat import normalize_locale
from ttkbootstrap.style import Style
from ttkbootstrap.utils import config


@pytest.fixture
def locale_reset(root):
    """Snapshot + restore the active locale and pending config around a test."""
    before = MessageCatalog.locale()
    pending_before = dict(config._pending)
    try:
        yield root
    finally:
        MessageCatalog.locale(before or "en")
        config._pending.clear()
        config._pending.update(pending_before)


# --------------------------------------------------------------------------
# exposure
# --------------------------------------------------------------------------

def test_helpers_exported_at_top_level():
    assert ttk.L is L
    assert ttk.LocaleVar is LocaleVar
    assert ttk.set_locale is set_locale
    for name in ("L", "LocaleVar", "set_locale"):
        assert name in ttk.__all__


def test_helpers_exported_through_utils():
    from ttkbootstrap import utils

    assert utils.L is L
    assert utils.set_locale is set_locale
    assert utils.LocaleVar is LocaleVar
    for name in ("L", "LocaleVar", "set_locale"):
        assert name in utils.__all__


# --------------------------------------------------------------------------
# normalize_locale
# --------------------------------------------------------------------------

@pytest.mark.parametrize(
    "raw, expected",
    [("de-DE", "de_de"), ("pt_BR", "pt_br"), ("EN", "en"), ("zh_CN", "zh_cn")],
)
def test_normalize_locale(raw, expected):
    assert normalize_locale(raw) == expected


# --------------------------------------------------------------------------
# msgcat bug fixes
# --------------------------------------------------------------------------

def test_translate_passes_special_chars_without_mangling(locale_reset):
    # braces / brackets / dollar in an argument used to break the eval path
    template = "value: '%s'"
    assert MessageCatalog.translate(template, "[a] {b} $c") == "value: '[a] {b} $c'"


def test_preferences_has_no_empty_entries(locale_reset):
    prefs = MessageCatalog.preferences()
    assert isinstance(prefs, list)
    assert "" not in prefs


def test_locale_normalizes_on_set(locale_reset):
    # "ZZ" -> "zz"; a throwaway code so no bundled catalog is loaded
    MessageCatalog.locale("ZZ")
    assert MessageCatalog.locale() == "zz"


def test_locale_change_emits_event(locale_reset):
    root = locale_reset
    root.update()  # drain any <<LocaleChanged>> events queued by prior teardowns
    fired = []
    funcid = root.bind("<<LocaleChanged>>", lambda e: fired.append(True), add="+")
    try:
        MessageCatalog.locale("zz")
        root.update()
        assert fired == [True]
    finally:
        root.unbind("<<LocaleChanged>>", funcid)


# --------------------------------------------------------------------------
# L()
# --------------------------------------------------------------------------

def test_L_translates_then_python_formats(locale_reset):
    MessageCatalog.set("zz", "Hello, {}!", "Zzhello, {}!")
    MessageCatalog.locale("zz")
    assert L("Hello, {}!", "world") == "Zzhello, world!"


def test_L_untranslated_falls_back_to_source(locale_reset):
    MessageCatalog.locale("zz")
    assert L("Untranslated {0}", "x") == "Untranslated x"


# --------------------------------------------------------------------------
# LocaleVar
# --------------------------------------------------------------------------

def test_localevar_translates_on_locale_change(locale_reset):
    root = locale_reset
    MessageCatalog.set("zz", "Cat", "Kat")
    MessageCatalog.locale("en")
    var = LocaleVar(root, "Cat")
    assert var.get() == "Cat"          # english source, no translation
    MessageCatalog.locale("zz")        # emits <<LocaleChanged>>
    root.update()
    assert var.get() == "Kat"          # var re-translated itself
    var.stop_tracking()


def test_localevar_stop_tracking_releases_binding(locale_reset):
    root = locale_reset
    MessageCatalog.set("zz", "Dog", "Hond")
    MessageCatalog.locale("en")
    var = LocaleVar(root, "Dog")
    var.stop_tracking()
    MessageCatalog.locale("zz")
    root.update()
    assert var.get() == "Dog"          # unchanged: no longer tracking


def test_localevar_formats_args(locale_reset):
    MessageCatalog.locale("en")
    var = LocaleVar(None, "Count: {}", 3)
    assert var.get() == "Count: 3"
    var.stop_tracking()


# --------------------------------------------------------------------------
# set_locale (deferred-config seam)
# --------------------------------------------------------------------------

def test_set_locale_applies_live_when_root_exists(locale_reset):
    set_locale("zz")
    assert MessageCatalog.locale() == "zz"


def test_set_locale_queues_before_root(locale_reset, monkeypatch):
    config._pending.clear()
    monkeypatch.setattr(Style, "instance", None)
    with warnings.catch_warnings():
        warnings.simplefilter("error")   # queue path must be silent
        set_locale("zz")
    assert "locale" in config._pending    # queued, not applied

    monkeypatch.undo()
    config.flush_pending_config()
    assert MessageCatalog.locale() == "zz"
    assert not config._pending
