"""Tk (legacy tkinter) widget builders for ttkbootstrap.

Importing this package registers default builder functions for common Tk
widgets using the BootstyleBuilderTk registry. Builders receive the actual
widget instance, plus theme/color utilities via the builder object.
"""

from __future__ import annotations

# Import defaults to trigger registration
from . import defaults  # noqa: F401

__all__ = [
    'defaults',
]

