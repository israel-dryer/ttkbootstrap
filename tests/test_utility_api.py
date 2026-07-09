"""Headless tests for the 2.0 public-utility surface.

Covers that the color / scaling / platform helpers are reachable at the top
level (`ttk.<name>`) and through the canonical `ttkbootstrap.utils` package,
that `windowing_system` matches the raw Tcl call it consolidates, and that the
old `ttkbootstrap.utility` / `ttkbootstrap.colorutils` module paths still work
as warn-and-forward shims (Slice 0).
"""
import importlib
import sys

import pytest

import ttkbootstrap as ttk
from ttkbootstrap import utils


# --------------------------------------------------------------------------
# top-level exposure
# --------------------------------------------------------------------------

_UTILITY_NAMES = ("enable_high_dpi_awareness", "scale_size", "windowing_system")
_COLOR_NAMES = (
    "color_to_rgb", "color_to_hex", "color_to_hsl",
    "update_hsl_value", "contrast_color", "conform_color_model",
)


def test_public_utilities_are_top_level_and_in_all():
    for name in _UTILITY_NAMES + _COLOR_NAMES:
        assert hasattr(ttk, name), f"ttk.{name} is not exported"
        assert name in ttk.__all__, f"{name} missing from ttk.__all__"


def test_utils_package_exposes_the_full_surface():
    for name in _UTILITY_NAMES + _COLOR_NAMES:
        assert hasattr(utils, name), f"utils.{name} is missing"
        assert name in utils.__all__, f"{name} missing from utils.__all__"


def test_top_level_names_are_the_utils_objects():
    # the re-exports must be the real functions, not shadowing copies
    assert ttk.scale_size is utils.scale_size
    assert ttk.windowing_system is utils.windowing_system
    assert ttk.contrast_color is utils.contrast_color


# --------------------------------------------------------------------------
# back-compat shims (ttkbootstrap.utility / ttkbootstrap.colorutils)
# --------------------------------------------------------------------------

def test_legacy_utility_module_warns_but_forwards():
    # drop any cached module so the module-level warning re-fires regardless of
    # test order
    sys.modules.pop("ttkbootstrap.utility", None)
    with pytest.warns(DeprecationWarning, match="moved to ttkbootstrap.utils"):
        legacy_utility = importlib.import_module("ttkbootstrap.utility")
    assert legacy_utility.scale_size is utils.scale_size
    assert legacy_utility.windowing_system is utils.windowing_system


def test_legacy_colorutils_module_warns_but_forwards():
    sys.modules.pop("ttkbootstrap.colorutils", None)
    with pytest.warns(DeprecationWarning, match="moved to ttkbootstrap.utils"):
        legacy_colorutils = importlib.import_module("ttkbootstrap.colorutils")
    assert legacy_colorutils.contrast_color is utils.contrast_color
    # the model constants (not in __all__) still resolve through the shim
    assert legacy_colorutils.HEX == "hex" and legacy_colorutils.RGB == "rgb"


# --------------------------------------------------------------------------
# windowing_system
# --------------------------------------------------------------------------

def test_windowing_system_matches_raw_call(root):
    assert ttk.windowing_system(root) == root.tk.call("tk", "windowingsystem")


def test_windowing_system_returns_known_value(root):
    assert ttk.windowing_system(root) in ("win32", "aqua", "x11")


# --------------------------------------------------------------------------
# scale_size + color helpers behave through the top-level names
# --------------------------------------------------------------------------

def test_scale_size_scales_a_pair(root):
    scaled = ttk.scale_size(root, (10, 20))
    assert isinstance(scaled, list) and len(scaled) == 2


def test_color_helpers_round_trip():
    from ttkbootstrap.utils.color import HEX, RGB
    assert ttk.color_to_rgb("#ff5733", model=HEX) == (255, 87, 51)
    assert ttk.color_to_hex((255, 87, 51), model=RGB) == "#ff5733"
