"""Common type aliases for ttkbootstrap widgets.

This module provides centralized type definitions used across all widget modules
to ensure consistency and reduce import boilerplate.
"""

from __future__ import annotations

import tkinter
from typing import Any, Callable, Optional, Union

# Master widget type - used for the `master` parameter in all widget constructors
Master = Optional[tkinter.Misc]

# Callback types
EventCallback = Callable[[tkinter.Event], None]
CommandCallback = Callable[[], Any]

# Common parameter types
WidgetKwargs = dict[str, Any]