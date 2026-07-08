"""Headless tests for the 2.0 DateEntry API normalization (widget review PR 3).

Covers the snake_case rename + legacy aliasing (coordinated across the dialog
layer), the ConfigureDelegationMixin adoption (cget/configure round-trip +
canonical single-string ``state``), the read-from-live-text bug fix, blur
validation, the ``width`` double-apply fix, the ``value`` property, and
``date_format`` reconfigure. Nothing here opens the modal picker.
"""
import inspect
import warnings
from datetime import date, datetime

import pytest

import ttkbootstrap as ttk
from ttkbootstrap.dialogs import Querybox
from ttkbootstrap.dialogs.datepicker import DatePickerDialog
from ttkbootstrap.widgets.dateentry import DateEntry


# --- constructor: snake_case + keyword-only + legacy aliasing --------------

def test_ctor_is_keyword_only_after_master(root):
    sig = inspect.signature(DateEntry.__init__)
    params = sig.parameters
    assert params["master"].kind is inspect.Parameter.POSITIONAL_OR_KEYWORD
    for name in ("date_format", "first_weekday", "start_date", "bootstyle",
                 "popup_title", "raise_exception", "position"):
        assert params[name].kind is inspect.Parameter.KEYWORD_ONLY, name


def test_ctor_accepts_snake_case(root):
    de = DateEntry(root, first_weekday=0, start_date=datetime(2021, 6, 15))
    assert de.cget("first_weekday") == 0
    assert de.get_date() == datetime(2021, 6, 15)


def test_ctor_legacy_names_warn_and_normalize(root):
    with pytest.warns(DeprecationWarning):
        de = DateEntry(root, firstweekday=0, startdate=datetime(2020, 1, 2))
    assert de.cget("first_weekday") == 0
    assert de.get_date() == datetime(2020, 1, 2)


def test_ctor_legacy_dateformat_warns(root):
    with pytest.warns(DeprecationWarning):
        de = DateEntry(root, dateformat="%Y-%m-%d")
    assert de.cget("date_format") == "%Y-%m-%d"


# --- configure/cget round-trip via the delegation mixin --------------------

@pytest.mark.parametrize("key,value", [
    ("first_weekday", 3),
    ("start_date", datetime(2019, 3, 4)),
    ("bootstyle", "success"),
    ("date_format", "%Y-%m-%d"),
    ("width", 24),
])
def test_configure_cget_roundtrip(root, key, value):
    de = DateEntry(root)
    de.configure(**{key: value})
    assert de.cget(key) == value
    # configure(key) returns a Tk-style 5-tuple spec whose last element is value
    assert de.configure(key)[-1] == value
    # item access mirrors cget
    assert de[key] == value


def test_keys_include_custom_options(root):
    de = DateEntry(root)
    keys = de.keys()
    for name in ("first_weekday", "start_date", "bootstyle", "date_format",
                 "state", "width"):
        assert name in keys


def test_legacy_option_string_still_resolves(root):
    de = DateEntry(root, date_format="%Y-%m-%d")
    with pytest.warns(DeprecationWarning):
        assert de.cget("dateformat") == "%Y-%m-%d"
    with pytest.warns(DeprecationWarning):
        de.configure(firstweekday=2)
    assert de.cget("first_weekday") == 2


# --- canonical single-string state -----------------------------------------

def test_state_returns_string_not_dict(root):
    de = DateEntry(root)
    st = de.cget("state")
    assert isinstance(st, str)
    assert st in ("normal", "readonly", "disabled")


def test_state_set_fans_out_to_entry_and_button(root):
    de = DateEntry(root)
    de.configure(state="disabled")
    assert str(de.entry.cget("state")) == "disabled"
    assert str(de.button.cget("state")) == "disabled"
    de.configure(state="normal")
    assert str(de.entry.cget("state")) == "normal"
    assert str(de.button.cget("state")) == "normal"


def test_state_readonly_targets_entry_only(root):
    de = DateEntry(root)
    de.configure(state="readonly")
    assert str(de.entry.cget("state")) == "readonly"


# --- the core bug: read from live entry text -------------------------------

def test_get_date_reads_typed_text(root):
    de = DateEntry(root, date_format="%Y-%m-%d", start_date=datetime(2000, 1, 1))
    de.entry.delete(0, "end")
    de.entry.insert(0, "2023-12-25")
    assert de.get_date() == datetime(2023, 12, 25)


def test_get_date_falls_back_to_shadow_when_unparseable(root):
    de = DateEntry(root, date_format="%Y-%m-%d", start_date=datetime(2000, 1, 1))
    de.entry.delete(0, "end")
    de.entry.insert(0, "not a date")
    assert de.get_date() == datetime(2000, 1, 1)


def test_coerce_tries_fallback_formats(root):
    de = DateEntry(root, date_format="%Y-%m-%d")
    # ISO fallback even though it does not match the configured format exactly
    assert de._coerce_date("2022-02-02") == datetime(2022, 2, 2)
    # MM/DD/YYYY fallback
    assert de._coerce_date("03/04/2022") == datetime(2022, 3, 4)
    assert de._coerce_date("garbage") is None
    assert de._coerce_date("") is None


# --- blur validation --------------------------------------------------------

def test_blur_marks_invalid_then_clears(root):
    de = DateEntry(root, date_format="%Y-%m-%d")
    de.entry.delete(0, "end")
    de.entry.insert(0, "xxx")
    de._on_entry_blur()
    assert "invalid" in de.entry.state()
    de.entry.delete(0, "end")
    de.entry.insert(0, "2021-01-01")
    de._on_entry_blur()
    assert "invalid" not in de.entry.state()


def test_blur_empty_is_valid(root):
    de = DateEntry(root, date_format="%Y-%m-%d")
    de.entry.delete(0, "end")
    de._on_entry_blur()
    assert "invalid" not in de.entry.state()


# --- width double-apply fix -------------------------------------------------

def test_width_applies_to_entry_not_frame(root):
    de = DateEntry(root, width=17)
    assert int(de.entry.cget("width")) == 17
    # the frame itself keeps its natural (geometry-driven) width, not 17
    assert de.cget("width") == 17  # delegated to the entry


# --- value property ---------------------------------------------------------

def test_value_property_get_and_set(root):
    de = DateEntry(root, date_format="%Y-%m-%d")
    de.value = datetime(2024, 7, 4)
    assert de.value == datetime(2024, 7, 4)
    assert de.entry.get() == "2024-07-04"
    # reads live text like get_date
    de.entry.delete(0, "end")
    de.entry.insert(0, "2024-08-09")
    assert de.value == datetime(2024, 8, 9)


# --- date_format reconfigure re-renders + validates ------------------------

def test_date_format_reconfigure_rerenders(root):
    de = DateEntry(root, date_format="%Y-%m-%d", start_date=datetime(2022, 5, 6))
    assert de.entry.get() == "2022-05-06"
    de.configure(date_format="%m/%d/%Y")
    assert de.entry.get() == "05/06/2022"
    assert de.cget("date_format") == "%m/%d/%Y"


def test_date_format_reconfigure_validates(root):
    de = DateEntry(root)
    with pytest.raises(ValueError):
        de.configure(date_format="%H:%M")  # no date component


# --- set_date / get_date semantics unchanged -------------------------------

def test_set_date_accepts_date_and_datetime(root):
    de = DateEntry(root, date_format="%Y-%m-%d")
    de.set_date(date(2020, 2, 29))
    assert de.get_date() == datetime(2020, 2, 29)
    de.set_date(datetime(2021, 3, 1, 13, 45))  # time stripped
    assert de.get_date() == datetime(2021, 3, 1)


def test_set_date_clears_invalid(root):
    de = DateEntry(root, date_format="%Y-%m-%d")
    de.entry.state(["invalid"])
    de.set_date(datetime(2021, 1, 1))
    assert "invalid" not in de.entry.state()


# --- re-entrancy guard flag exists -----------------------------------------

def test_picker_reentrancy_guard(root):
    de = DateEntry(root)
    assert de._picker_open is False
    # while "open", a second call is a no-op (returns immediately)
    de._picker_open = True
    de._on_date_ask()  # must not raise / block
    assert de._picker_open is True


# --- cross-layer rename: Querybox.get_date / DatePickerDialog --------------

def test_get_date_signature_uses_snake_case():
    params = inspect.signature(Querybox.get_date).parameters
    assert "first_weekday" in params
    assert "start_date" in params
    assert "position" in params


def test_datepicker_dialog_accepts_snake_case(root):
    dlg = DatePickerDialog(
        parent=root, first_weekday=0, start_date=date(2021, 9, 9), autoshow=False,
    )
    assert dlg.first_weekday == 0
    assert dlg.start_date == date(2021, 9, 9)
    dlg.root.destroy()


def test_datepicker_dialog_legacy_names_warn(root):
    with pytest.warns(DeprecationWarning):
        dlg = DatePickerDialog(
            parent=root, firstweekday=0, startdate=date(2021, 9, 9), autoshow=False,
        )
    assert dlg.first_weekday == 0
    assert dlg.start_date == date(2021, 9, 9)
    dlg.root.destroy()


def test_datepicker_dialog_rejects_unknown_kwarg(root):
    with pytest.raises(TypeError):
        DatePickerDialog(parent=root, autoshow=False, bogus=1)

def test_legacy_dateformat_attribute_is_deprecated(root):
    """The pre-2.0 `dateformat` attribute still reads, with a warning."""
    import warnings
    de = DateEntry(root, date_format="%Y-%m-%d")
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        assert de.dateformat == "%Y-%m-%d"
    assert any(issubclass(w.category, DeprecationWarning) for w in caught)
