"""Headless tests for the 2.0 public-utility surface.

Covers that the utility/colorutils helpers are reachable at the top level
(`ttk.<name>`) and that the new `windowing_system` helper matches the raw Tcl
call it consolidates.
"""
import ttkbootstrap as ttk
from ttkbootstrap import colorutils, utility


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


def test_top_level_names_are_the_module_objects():
    # the re-exports must be the real functions, not shadowing copies
    assert ttk.scale_size is utility.scale_size
    assert ttk.windowing_system is utility.windowing_system
    assert ttk.contrast_color is colorutils.contrast_color


# --------------------------------------------------------------------------
# windowing_system
# --------------------------------------------------------------------------

def test_windowing_system_matches_raw_call(root):
    assert ttk.windowing_system(root) == root.tk.call("tk", "windowingsystem")


def test_windowing_system_returns_known_value(root):
    assert ttk.windowing_system(root) in ("win32", "aqua", "x11")


# --------------------------------------------------------------------------
# scale_size + colorutils behave through the top-level names
# --------------------------------------------------------------------------

def test_scale_size_scales_a_pair(root):
    scaled = ttk.scale_size(root, (10, 20))
    assert isinstance(scaled, list) and len(scaled) == 2


def test_colorutils_round_trip():
    assert ttk.color_to_rgb("#ff5733", model=colorutils.HEX) == (255, 87, 51)
    assert ttk.color_to_hex((255, 87, 51), model=colorutils.RGB) == "#ff5733"
