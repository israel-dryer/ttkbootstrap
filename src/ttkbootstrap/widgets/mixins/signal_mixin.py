"""Signal integration mixins for ttkbootstrap widgets.

Provides seamless integration between tkinter Variables and reactive Signals,
exposing both as properties on widgets that support `textvariable` and `variable`
options. The mixins maintain bidirectional synchronization between Variables and
Signals automatically.

These mixins are thin glue layers that delegate to the core signal capability
module for normalization and binding logic.
"""

from __future__ import annotations

import tkinter as tk
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from ttkbootstrap.core.signals import Signal

from ttkbootstrap.core.capabilities.signals import (
    is_signal,
    is_variable,
    normalize_signal,
    create_signal,
    infer_default_value_for_widget,
    query_binding,
)
from ttkbootstrap.widgets.mixins.configure_mixin import configure_delegate


class TextSignalMixin:
    """Mixin providing `.textvariable` and `.textsignal` properties for text-based widgets.

    For widgets that support the `textvariable` option (Entry, Label, Button, etc.),
    this mixin exposes both the underlying tk.Variable and a reactive Signal as properties,
    maintaining bidirectional synchronization between them.

    This mixin delegates normalization and binding logic to the core signals capability.

    Attributes:
        textvariable (Variable): The underlying tk.Variable (usually StringVar).
        textsignal (Signal): The reactive Signal wrapper with subscribe/map capabilities.
    """

    def __init__(self, *args, **kwargs):
        """Initialize mixin and extract textsignal/textvariable parameters before tkinter sees them."""
        # Extract textsignal and textvariable before passing kwargs to tkinter
        textsignal_value = kwargs.pop('textsignal', None)
        textvariable_value = kwargs.pop('textvariable', None)

        # Call parent __init__
        super().__init__(*args, **kwargs)

        # Apply textsignal or textvariable after widget construction
        # Prefer textsignal if both are provided
        if textsignal_value is not None:
            self._config_delegate_set('textsignal', textsignal_value)
        elif textvariable_value is not None:
            self._config_delegate_set('textvariable', textvariable_value)

    @configure_delegate("textvariable", "textsignal")
    def _delegate_textsignal(self, value: Any = None):
        """Handle textvariable and textsignal configuration.

        Args:
            value: Signal, tk.Variable, or None for query.

        Returns:
            Current value for query path, None for set path.
        """
        # Query path - return stored value
        if value is None:
            return query_binding(
                getattr(self, '_textsignal', None),
                getattr(self, '_textvariable', None),
                self._ttk_base,  # type: ignore[misc]
                self,
                'textvariable',
            )

        # Set path - normalize and apply
        binding = normalize_signal(value, default_value="")
        if binding is not None:
            self._textsignal = binding.signal
            self._textvariable = binding.variable
            var_to_set = binding.tk_value
        else:
            # String (Tcl variable name) or other - pass through
            var_to_set = value
            if value:
                self._textvariable = value

        # Apply via base ttk widget to avoid recursion
        return self._ttk_base.configure(self, textvariable=var_to_set)  # type: ignore[misc]

    @property
    def textsignal(self) -> 'Signal[str]':
        """Get or lazily create the textsignal.

        If no textvariable has been set, creates a new Signal with empty string.
        If textvariable exists, wraps it in a Signal.

        Returns:
            The reactive Signal for this widget's text.
        """
        if not hasattr(self, '_textsignal'):
            # Create fresh signal
            binding = create_signal("")
            self._textsignal = binding.signal
            self._textvariable = binding.variable
            try:
                self._ttk_base.configure(self, textvariable=binding.tk_value)  # type: ignore[misc]
            except Exception:
                pass
        return self._textsignal

    @textsignal.setter
    def textsignal(self, value: 'Signal[str]') -> None:
        """Set the textsignal, extracting and configuring its underlying variable.

        Args:
            value: Signal to use for this widget's text.
        """
        self._delegate_textsignal(value)

    @property
    def textvariable(self) -> tk.Variable:
        """Get the underlying tk.Variable.

        If not yet created, accessing this property will trigger lazy creation
        via the textsignal property.

        Returns:
            The tk.Variable (usually StringVar) for this widget's text.
        """
        if not hasattr(self, '_textvariable'):
            # Trigger lazy creation via textsignal
            _ = self.textsignal
        return self._textvariable

    @textvariable.setter
    def textvariable(self, value: tk.Variable) -> None:
        """Set the textvariable, creating a synced Signal automatically.

        Args:
            value: tk.Variable to use for this widget's text.
        """
        self._delegate_textsignal(value)


class SignalMixin:
    """Mixin providing `.variable` and `.signal` properties for value-based widgets.

    For widgets that support the `variable` option (Checkbutton, Radiobutton, Scale, etc.),
    this mixin exposes both the underlying tk.Variable and a reactive Signal as properties,
    maintaining bidirectional synchronization between them.

    This mixin delegates normalization and binding logic to the core signals capability.

    Attributes:
        variable (Variable): The underlying tk.Variable (IntVar, DoubleVar, BooleanVar, etc.).
        signal (Signal): The reactive Signal wrapper with subscribe/map capabilities.
    """

    def __init__(self, *args, **kwargs):
        """Initialize mixin and extract signal/variable parameters before tkinter sees them."""
        # Extract signal and variable before passing kwargs to tkinter
        signal_value = kwargs.pop('signal', None)
        variable_value = kwargs.pop('variable', None)

        # Call parent __init__
        super().__init__(*args, **kwargs)

        # Apply signal or variable after widget construction
        # Prefer signal if both are provided
        if signal_value is not None:
            self._config_delegate_set('signal', signal_value)
        elif variable_value is not None:
            self._config_delegate_set('variable', variable_value)

    @configure_delegate("variable", "signal")
    def _delegate_signal(self, value: Any = None):
        """Handle variable and signal configuration.

        Args:
            value: Signal, tk.Variable, or None for query.

        Returns:
            Current value for query path, None for set path.
        """
        # Query path - return stored value
        if value is None:
            return query_binding(
                getattr(self, '_signal', None),
                getattr(self, '_variable', None),
                self._ttk_base,  # type: ignore[misc]
                self,
                'variable',
            )

        # Set path - normalize and apply
        binding = normalize_signal(value)
        if binding is not None:
            self._signal = binding.signal
            self._variable = binding.variable
            var_to_set = binding.tk_value
        else:
            # String (Tcl variable name) or other - pass through
            var_to_set = value
            if value:
                self._variable = value

        # Apply via base ttk widget to avoid recursion
        return self._ttk_base.configure(self, variable=var_to_set)  # type: ignore[misc]

    @property
    def signal(self) -> 'Signal[Any]':
        """Get or lazily create the signal.

        If no variable has been set, creates a new Signal with appropriate default
        (False for Checkbutton, 0 for Scale, etc.). If variable exists, wraps it in a Signal.

        Returns:
            The reactive Signal for this widget's value.
        """
        if not hasattr(self, '_signal'):
            # Infer default value based on widget type
            default_value = infer_default_value_for_widget(self.winfo_class())
            binding = create_signal(default_value)
            self._signal = binding.signal
            self._variable = binding.variable
            try:
                self._ttk_base.configure(self, variable=binding.tk_value)  # type: ignore[misc]
            except Exception:
                pass
        return self._signal

    @signal.setter
    def signal(self, value: 'Signal[Any]') -> None:
        """Set the signal, extracting and configuring its underlying variable.

        Args:
            value: Signal to use for this widget's value.
        """
        self._delegate_signal(value)

    @property
    def variable(self) -> tk.Variable:
        """Get the underlying tk.Variable.

        If not yet created, accessing this property will trigger lazy creation
        via the signal property.

        Returns:
            The tk.Variable (IntVar, BooleanVar, DoubleVar, etc.) for this widget's value.
        """
        if not hasattr(self, '_variable'):
            # Trigger lazy creation via signal
            _ = self.signal
        return self._variable

    @variable.setter
    def variable(self, value: tk.Variable) -> None:
        """Set the variable, creating a synced Signal automatically.

        Args:
            value: tk.Variable to use for this widget's value.
        """
        self._delegate_signal(value)


__all__ = ["TextSignalMixin", "SignalMixin"]