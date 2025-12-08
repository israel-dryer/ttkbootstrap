"""Signal integration mixins for ttkbootstrap widgets.

Provides seamless integration between tkinter Variables and reactive Signals,
exposing both as properties on widgets that support `textvariable` and `variable`
options. The mixins maintain bidirectional synchronization between Variables and
Signals automatically.

Architecture
------------
Two mixins are provided:

1. **TextSignalMixin**: For widgets with `textvariable` support
   - Entry, Label, Button, Combobox, Spinbox, etc.
   - Exposes: `.textvariable` and `.textsignal` properties

2. **SignalMixin**: For widgets with `variable` support
   - Checkbutton, Radiobutton, Scale, Progressbar, etc.
   - Exposes: `.variable` and `.signal` properties

Both mixins use the `@configure_delegate` pattern to intercept configuration at
construction time and via `configure()` calls, ensuring Variables and Signals
remain synchronized regardless of how they're set.

Synchronization Behavior
------------------------
The mixins maintain a bidirectional sync:

- Setting a `Signal` extracts its underlying `tk.Variable` and configures the widget
- Setting a `tk.Variable` wraps it in a `Signal` using `Signal.from_variable()`
- Changes to either the Signal or Variable are reflected in both
- Accessing properties lazily creates the pair if not already present

Usage
-----
Basic usage with Entry (TextSignalMixin)::

    from ttkbootstrap import ttk
    from ttkbootstrap.core.signals import Signal

    # Create entry with signal at construction
    sig = Signal("initial")
    entry = ttk.Entry(root, textsignal=sig)

    # Access synced variable
    print(entry.textvariable.get())  # "initial"

    # Subscribe to changes
    entry.textsignal.subscribe(lambda v: print(f"Changed to: {v}"))

    # Lazy creation via property
    entry2 = ttk.Entry(root)
    entry2.textsignal.set("hello")  # Creates signal on first access

Basic usage with Checkbutton (SignalMixin)::

    from ttkbootstrap import ttk
    from ttkbootstrap.core.signals import Signal

    # Create checkbutton with signal
    checked = Signal(False)
    cb = ttk.Checkbutton(root, text="Agree", signal=checked)

    # Subscribe to state changes
    checked.subscribe(lambda v: print(f"Checked: {v}"))

    # Access underlying variable
    print(cb.variable.get())  # False

Setting variables after construction::

    entry = ttk.Entry(root)

    # Set via configure - creates synced signal
    var = tk.StringVar(value="test")
    entry.configure(textvariable=var)

    # Signal is automatically created and synced
    entry.textsignal.subscribe(lambda v: print(v))

Integration with TTKWrapperBase
-------------------------------
These mixins are designed to be mixed into TTKWrapperBase subclasses:

    class Entry(TextSignalMixin, TTKWrapperBase, ttk.Entry):
        ...

The `@configure_delegate` decorator ensures the mixins intercept both constructor
kwargs and runtime `configure()` calls, maintaining sync automatically.

Notes
-----
- Signals are created lazily on first property access if not explicitly set
- Setting a Signal or Variable via constructor, `configure()`, or properties all work
- The underlying tk.Variable is always what's actually configured on the ttk widget
- Changing the Signal updates the Variable (and vice versa) via Signal's trace mechanism
- Type inference follows Signal's behavior: int→IntVar, str→StringVar, etc.
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

    Properties:
        textvariable: The underlying tk.Variable (usually StringVar)
        textsignal: The reactive Signal wrapper with subscribe/map capabilities

    Configuration Options:
        textvariable: Set the tk.Variable (creates synced Signal automatically)
        textsignal: Set the Signal (extracts and configures underlying Variable)

    Examples:
        # Set Signal at construction
        sig = Signal("hello")
        entry = Entry(root, textsignal=sig)
        entry.textvariable.get()  # "hello"

        # Set Variable at construction
        var = tk.StringVar(value="world")
        label = Label(root, textvariable=var)
        label.textsignal.subscribe(print)  # Synced Signal created

        # Lazy creation via property
        button = Button(root, text="Click")
        button.textsignal.set("Updated")  # Signal/Variable created on access

        # Runtime configuration
        entry.configure(textsignal=Signal("new"))
    """

    def __init__(self, *args, **kwargs):
        """Initialize mixin and extract textsignal parameter before tkinter sees it."""
        # Extract textsignal before passing kwargs to tkinter
        textsignal_value = kwargs.pop('textsignal', None)

        # Call parent __init__
        super().__init__(*args, **kwargs)

        # Apply textsignal after widget construction
        if textsignal_value is not None:
            self._config_delegate_set('textsignal', textsignal_value)

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

    Properties:
        variable: The underlying tk.Variable (IntVar, DoubleVar, BooleanVar, etc.)
        signal: The reactive Signal wrapper with subscribe/map capabilities

    Configuration Options:
        variable: Set the tk.Variable (creates synced Signal automatically)
        signal: Set the Signal (extracts and configures underlying Variable)

    Examples:
        # Set Signal at construction
        checked = Signal(False)
        cb = Checkbutton(root, text="Agree", signal=checked)
        cb.variable.get()  # False

        # Set Variable at construction
        var = tk.IntVar(value=50)
        scale = Scale(root, from_=0, to=100, variable=var)
        scale.signal.subscribe(lambda v: print(f"Value: {v}"))

        # Lazy creation via property
        radio = Radiobutton(root, text="Option A", value=1)
        radio.signal.set(1)  # Signal/Variable created on access

        # Runtime configuration
        cb.configure(signal=Signal(True))
    """

    def __init__(self, *args, **kwargs):
        """Initialize mixin and extract signal parameter before tkinter sees it."""
        # Extract signal before passing kwargs to tkinter
        signal_value = kwargs.pop('signal', None)

        # Call parent __init__
        super().__init__(*args, **kwargs)

        # Apply signal after widget construction
        if signal_value is not None:
            self._config_delegate_set('signal', signal_value)

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
