"""Signal binding capability for ttkbootstrap widgets.

This module provides the core framework service for binding Signals and tkinter
Variables to widgets. It handles normalization, bidirectional synchronization,
and lazy creation of Signals.

The widget mixins (TextSignalMixin, SignalMixin) delegate to these functions
to remain thin glue layers.
"""

from __future__ import annotations

import tkinter as tk
from dataclasses import dataclass
from typing import Any, Callable, TYPE_CHECKING

if TYPE_CHECKING:
    from ttkbootstrap.core.signals import Signal


# =============================================================================
# Type Detection Helpers
# =============================================================================

def is_signal(obj: Any) -> bool:
    """Check if an object is a Signal using duck typing.

    Args:
        obj: Object to check.

    Returns:
        True if object has Signal-like interface (var, subscribe, get, set).
    """
    return (
        hasattr(obj, 'var')
        and hasattr(obj, 'subscribe')
        and hasattr(obj, 'get')
        and hasattr(obj, 'set')
    )


def is_variable(obj: Any) -> bool:
    """Check if an object is a tkinter Variable.

    Args:
        obj: Object to check.

    Returns:
        True if object is a tkinter Variable instance.
    """
    return isinstance(obj, tk.Variable)


# =============================================================================
# Signal Binding Result
# =============================================================================

@dataclass
class SignalBinding:
    """Result of normalizing a Signal or Variable for widget binding.

    Attributes:
        signal: The Signal instance (created or provided).
        variable: The underlying tk.Variable for widget configuration.
        tk_value: The value to pass to the ttk widget's configure method.
    """
    signal: 'Signal[Any]'
    variable: tk.Variable
    tk_value: tk.Variable


# =============================================================================
# Normalization Functions
# =============================================================================

def normalize_signal(
    value: Any,
    *,
    default_value: Any = "",
) -> SignalBinding | None:
    """Normalize a Signal, Variable, or value into a SignalBinding.

    This function handles the conversion logic for binding signals to widgets.
    It accepts either a Signal, a tk.Variable, or passes through None/strings.

    Args:
        value: The value to normalize. Can be:
            - A Signal instance: extracts the underlying variable
            - A tk.Variable: wraps it in a Signal
            - None: returns None (no binding)
            - A string (Tcl variable name): returns None (let caller handle)
        default_value: Default value for creating new Signals (unused for
            existing Signal/Variable).

    Returns:
        A SignalBinding with the signal, variable, and tk_value, or None if
        the value cannot be normalized (e.g., string Tcl name, None).

    Examples:
        >>> from ttkbootstrap.core.signals import Signal
        >>> sig = Signal("hello")
        >>> binding = normalize_signal(sig)
        >>> binding.signal is sig
        True
        >>> binding.variable is sig.var
        True

        >>> var = tk.StringVar(value="world")
        >>> binding = normalize_signal(var)
        >>> binding.variable is var
        True
        >>> binding.signal.get()
        'world'
    """
    if value is None:
        return None

    if is_signal(value):
        # It's a Signal - extract the variable
        return SignalBinding(
            signal=value,
            variable=value.var,
            tk_value=value.var,
        )

    if is_variable(value):
        # It's a tk.Variable - wrap it in a Signal
        from ttkbootstrap.core.signals import Signal
        signal = Signal.from_variable(value)
        return SignalBinding(
            signal=signal,
            variable=value,
            tk_value=value,
        )

    # String (Tcl variable name) or other - cannot normalize
    return None


def create_signal(default_value: Any) -> SignalBinding:
    """Create a new Signal with the given default value.

    Args:
        default_value: The initial value for the Signal.

    Returns:
        A SignalBinding with the new signal, variable, and tk_value.

    Examples:
        >>> binding = create_signal("")
        >>> binding.signal.get()
        ''
        >>> binding = create_signal(0.0)
        >>> binding.signal.get()
        0.0
    """
    from ttkbootstrap.core.signals import Signal
    signal = Signal(default_value)
    return SignalBinding(
        signal=signal,
        variable=signal.var,
        tk_value=signal.var,
    )


def infer_default_value_for_widget(widget_class: str) -> Any:
    """Infer an appropriate default value based on widget class.

    Args:
        widget_class: The Tk widget class name (e.g., "TCheckbutton", "TScale").

    Returns:
        An appropriate default value for the widget type:
        - False for checkbuttons
        - 0 for radiobuttons
        - 0.0 for scales
        - 0 for progressbars
        - "" for others
    """
    # Checkbutton typically uses boolean
    if widget_class in ('TCheckbutton', 'Checkbutton'):
        return False
    # Radiobutton typically uses int
    elif widget_class in ('TRadiobutton', 'Radiobutton'):
        return 0
    # Scale uses float
    elif widget_class in ('TScale', 'Scale'):
        return 0.0
    # Progressbar uses int
    elif widget_class in ('TProgressbar', 'Progressbar'):
        return 0
    # Default to empty string
    else:
        return ""


# =============================================================================
# Query Functions
# =============================================================================

def query_binding(
    stored_signal: 'Signal[Any] | None',
    stored_variable: tk.Variable | None,
    ttk_base: type,
    widget: Any,
    option_name: str,
) -> 'Signal[Any] | tk.Variable | None':
    """Query the current signal/variable binding for a widget option.

    Returns the signal if available, otherwise the variable, otherwise
    queries the widget directly.

    Args:
        stored_signal: The cached Signal, if any.
        stored_variable: The cached Variable, if any.
        ttk_base: The ttk base class for querying.
        widget: The widget instance.
        option_name: The option name to query ("textvariable" or "variable").

    Returns:
        The Signal if stored, else the Variable if stored, else the widget's
        configured value for the option.
    """
    if stored_signal is not None:
        return stored_signal
    if stored_variable is not None:
        return stored_variable
    try:
        return ttk_base.cget(widget, option_name)
    except Exception:
        return None


__all__ = [
    "is_signal",
    "is_variable",
    "SignalBinding",
    "normalize_signal",
    "create_signal",
    "infer_default_value_for_widget",
    "query_binding",
]