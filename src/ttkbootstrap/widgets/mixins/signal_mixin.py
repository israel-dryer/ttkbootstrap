"""Signal integration mixins for ttkbootstrap widgets.

Provides seamless integration between tkinter Variables and reactive Signals,
exposing both as properties on widgets that support `textvariable` and `variable`
options. The mixins maintain bidirectional synchronization between Variables and
Signals automatically.
"""

from __future__ import annotations

import tkinter as tk
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from ttkbootstrap.core.signals import Signal

from ttkbootstrap.widgets.mixins.configure_mixin import configure_delegate


def _is_signal(obj: Any) -> bool:
    """Check if an object is a Signal using duck typing.

    Args:
        obj: Object to check

    Returns:
        True if object has Signal-like interface (var, subscribe, get, set)
    """
    return (
        hasattr(obj, 'var')
        and hasattr(obj, 'subscribe')
        and hasattr(obj, 'get')
        and hasattr(obj, 'set')
    )


def _is_variable(obj: Any) -> bool:
    """Check if an object is a tk.Variable.

    Args:
        obj: Object to check

    Returns:
        True if object is a tkinter Variable instance
    """
    return isinstance(obj, tk.Variable)


class TextSignalMixin:
    """Mixin providing `.textvariable` and `.textsignal` properties for text-based widgets.

    For widgets that support the `textvariable` option (Entry, Label, Button, etc.),
    this mixin exposes both the underlying tk.Variable and a reactive Signal as properties,
    maintaining bidirectional synchronization between them.

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
            value: Signal, tk.Variable, or None for query

        Returns:
            Current value for query path, None for set path
        """
        # Query path - return stored value
        if value is None:
            # Return textsignal if it exists
            if hasattr(self, '_textsignal'):
                return self._textsignal
            # Return textvariable if it exists
            if hasattr(self, '_textvariable'):
                return self._textvariable
            # Fallback: query the ttk widget directly
            try:
                return self._ttk_base.cget(self, 'textvariable')  # type: ignore[misc]
            except:
                return None

        # Set path - handle Signal or tk.Variable
        if _is_signal(value):
            # It's a Signal - extract the variable
            self._textsignal = value
            self._textvariable = value.var
            var_to_set = value.var
        elif _is_variable(value):
            # It's a tk.Variable - create Signal from it
            from ttkbootstrap.core.signals import Signal
            self._textvariable = value
            self._textsignal = Signal.from_variable(value)
            var_to_set = value
        else:
            # It's a string (Tcl variable name) or other - pass through
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
            The reactive Signal for this widget's text
        """
        if not hasattr(self, '_textsignal'):
            # Check if widget already has a textvariable configured
            try:
                var_name = self._ttk_base.cget(self, 'textvariable')  # type: ignore[misc]
                if var_name:
                    # There's a variable but we don't have it wrapped
                    # Create a new Variable and Signal (safest approach)
                    from ttkbootstrap.core.signals import Signal
                    self._textsignal = Signal("")
                    self._textvariable = self._textsignal.var
                    self._ttk_base.configure(self, textvariable=self._textvariable)  # type: ignore[misc]
                else:
                    # No variable - create fresh signal
                    from ttkbootstrap.core.signals import Signal
                    self._textsignal = Signal("")
                    self._textvariable = self._textsignal.var
                    self._ttk_base.configure(self, textvariable=self._textvariable)  # type: ignore[misc]
            except:
                # Fallback: create fresh signal
                from ttkbootstrap.core.signals import Signal
                self._textsignal = Signal("")
                self._textvariable = self._textsignal.var
                try:
                    self._ttk_base.configure(self, textvariable=self._textvariable)  # type: ignore[misc]
                except:
                    pass
        return self._textsignal

    @textsignal.setter
    def textsignal(self, value: 'Signal[str]') -> None:
        """Set the textsignal, extracting and configuring its underlying variable.

        Args:
            value: Signal to use for this widget's text
        """
        self._delegate_textsignal(value)

    @property
    def textvariable(self) -> tk.Variable:
        """Get the underlying tk.Variable.

        If not yet created, accessing this property will trigger lazy creation
        via the textsignal property.

        Returns:
            The tk.Variable (usually StringVar) for this widget's text
        """
        if not hasattr(self, '_textvariable'):
            # Trigger lazy creation via textsignal
            _ = self.textsignal
        return self._textvariable

    @textvariable.setter
    def textvariable(self, value: tk.Variable) -> None:
        """Set the textvariable, creating a synced Signal automatically.

        Args:
            value: tk.Variable to use for this widget's text
        """
        self._delegate_textsignal(value)


class SignalMixin:
    """Mixin providing `.variable` and `.signal` properties for value-based widgets.

    For widgets that support the `variable` option (Checkbutton, Radiobutton, Scale, etc.),
    this mixin exposes both the underlying tk.Variable and a reactive Signal as properties,
    maintaining bidirectional synchronization between them.

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
            value: Signal, tk.Variable, or None for query

        Returns:
            Current value for query path, None for set path
        """
        # Query path - return stored value
        if value is None:
            # Return signal if it exists
            if hasattr(self, '_signal'):
                return self._signal
            # Return variable if it exists
            if hasattr(self, '_variable'):
                return self._variable
            # Fallback: query the ttk widget directly
            try:
                return self._ttk_base.cget(self, 'variable')  # type: ignore[misc]
            except:
                return None

        # Set path - handle Signal or tk.Variable
        if _is_signal(value):
            # It's a Signal - extract the variable
            self._signal = value
            self._variable = value.var
            var_to_set = value.var
        elif _is_variable(value):
            # It's a tk.Variable - create Signal from it
            from ttkbootstrap.core.signals import Signal
            self._variable = value
            self._signal = Signal.from_variable(value)
            var_to_set = value
        else:
            # It's a string (Tcl variable name) or other - pass through
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
            The reactive Signal for this widget's value
        """
        if not hasattr(self, '_signal'):
            # Check if widget already has a variable configured
            try:
                var_name = self._ttk_base.cget(self, 'variable')  # type: ignore[misc]
                if var_name:
                    # There's a variable but we don't have it wrapped
                    # Create a new Variable and Signal (safest approach)
                    from ttkbootstrap.core.signals import Signal
                    # Infer default value based on widget type
                    default_value = self._infer_default_value()
                    self._signal = Signal(default_value)
                    self._variable = self._signal.var
                    self._ttk_base.configure(self, variable=self._variable)  # type: ignore[misc]
                else:
                    # No variable - create fresh signal
                    from ttkbootstrap.core.signals import Signal
                    default_value = self._infer_default_value()
                    self._signal = Signal(default_value)
                    self._variable = self._signal.var
                    self._ttk_base.configure(self, variable=self._variable)  # type: ignore[misc]
            except:
                # Fallback: create fresh signal with default value
                from ttkbootstrap.core.signals import Signal
                default_value = self._infer_default_value()
                self._signal = Signal(default_value)
                self._variable = self._signal.var
                try:
                    self._ttk_base.configure(self, variable=self._variable)  # type: ignore[misc]
                except:
                    pass
        return self._signal

    @signal.setter
    def signal(self, value: 'Signal[Any]') -> None:
        """Set the signal, extracting and configuring its underlying variable.

        Args:
            value: Signal to use for this widget's value
        """
        self._delegate_signal(value)

    @property
    def variable(self) -> tk.Variable:
        """Get the underlying tk.Variable.

        If not yet created, accessing this property will trigger lazy creation
        via the signal property.

        Returns:
            The tk.Variable (IntVar, BooleanVar, DoubleVar, etc.) for this widget's value
        """
        if not hasattr(self, '_variable'):
            # Trigger lazy creation via signal
            _ = self.signal
        return self._variable

    @variable.setter
    def variable(self, value: tk.Variable) -> None:
        """Set the variable, creating a synced Signal automatically.

        Args:
            value: tk.Variable to use for this widget's value
        """
        self._delegate_signal(value)

    def _infer_default_value(self) -> Any:
        """Infer appropriate default value based on widget type.

        Returns:
            Default value appropriate for the widget (False for Checkbutton,
            0 for Scale/Progressbar, "" for others)
        """
        widget_class = self.winfo_class()

        # Checkbutton/Radiobutton typically use boolean or int
        if widget_class in ('TCheckbutton', 'Checkbutton'):
            return False
        elif widget_class in ('TRadiobutton', 'Radiobutton'):
            return 0
        # Scale/Progressbar use numeric values
        elif widget_class in ('TScale', 'Scale', 'TProgressbar', 'Progressbar'):
            return 0.0 if widget_class in ('TScale', 'Scale') else 0
        # Default to empty string for others
        else:
            return ""


__all__ = ["TextSignalMixin", "SignalMixin"]
