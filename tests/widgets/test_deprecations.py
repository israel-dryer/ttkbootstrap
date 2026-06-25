"""Deprecation-warning regression tests (2.0).

Long-deprecated widgets that are kept through 2.x (removed in 3.0) must emit a
runtime `DeprecationWarning` when used, not merely document it in a docstring.

Runnable headlessly with pytest.
"""
import warnings

import pytest

from ttkbootstrap.widgets.floodgauge import Floodgauge, FloodgaugeLegacy


def test_floodgauge_legacy_warns_on_init(root):
    """Instantiating FloodgaugeLegacy emits a DeprecationWarning naming 3.0."""
    with pytest.warns(DeprecationWarning, match="removed in 3.0"):
        FloodgaugeLegacy(root)


def test_canvas_floodgauge_does_not_warn(root):
    """The canonical canvas Floodgauge must not warn."""
    with warnings.catch_warnings():
        warnings.simplefilter("error", DeprecationWarning)
        Floodgauge(root)