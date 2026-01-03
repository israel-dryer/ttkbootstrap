"""TabItem widget - a tab with optional close button."""
from __future__ import annotations

__all__ = ['TabItem']

from tkinter import TclError, Variable
from typing import Any, Callable, Literal, TYPE_CHECKING, Union

from ttkbootstrap.widgets.composites.compositeframe import CompositeFrame
from ttkbootstrap.widgets.primitives.button import Button
from ttkbootstrap.widgets.primitives.label import Label
from ttkbootstrap.widgets.mixins import configure_delegate
from ttkbootstrap.widgets.types import Master
from ttkbootstrap.core.capabilities.signals import normalize_signal

if TYPE_CHECKING:
    from ttkbootstrap.core.signals import Signal


class TabItem(CompositeFrame):
    """A tab item widget with optional close button.

    TabItem extends CompositeFrame to provide a clickable tab with coordinated
    hover/pressed/focus states across all child widgets. It supports selection
    via signal/variable and optional close functionality.

    !!! note "Events"
        - ``<<TabSelect>>``: Fired when the tab is clicked (for selection).
        - ``<<TabClose>>``: Fired when the close button is clicked.

    Attributes:
        selected (bool): Current selection state (read-only).
        value: The value associated with this tab.
    """

    def __init__(
        self,
        master: Master = None,
        text: str = "",
        icon: str | dict = None,
        compound: Literal['left', 'right', 'top', 'bottom', 'center', 'none'] = 'left',
        value: Any = None,
        variable: Variable = None,
        orient: Literal['horizontal', 'vertical'] = 'horizontal',
        signal: 'Signal[Any]' = None,
        command: Callable = None,
        closable: Union[bool, Literal['hover']] = False,
        close_command: Callable = None,
        variant: Literal['pill', 'bar'] = 'bar',
        **kwargs
    ):
        """Create a TabItem widget.

        Args:
            master: Parent widget. If None, uses the default root window.
            text: Text to display on the tab.
            icon: Icon to display on the tab (left of text).
            compound: How to position icon relative to text. One of 'left',
                'right', 'top', 'bottom', 'center', or 'none'. Default is 'left'.
            value: Value to set on signal/variable when this tab is selected.
            variable: Tk variable for selection state (synced with signal).
            orient: Orientation hint for styling ('horizontal' or 'vertical').
                Default is 'horizontal'.
            signal: Reactive Signal for selection state (preferred over variable).
            command: Callback invoked when the tab is selected.
            closable: Close button visibility. True=always visible, False=hidden,
                'hover'=visible only on hover (space reserved).
            close_command: Callback invoked when close button is clicked.
            variant: Tab style variant ('pill' or 'bar').
            **kwargs: Additional arguments passed to CompositeFrame.
        """
        self._text = text
        self._icon = icon
        self._compound = compound
        self._value = value
        self._command = command
        self._closable = closable
        self._close_command = close_command
        self._variant = variant
        self._orient = orient
        self._accent = None  # Will be set from kwargs

        # Selection state - signal/variable syncing
        self._signal: Signal[Any] | None = None
        self._variable: Variable | None = None
        self._trace_id: str | None = None

        # Determine ttk_class based on variant
        ttk_class = self._get_ttk_class(variant)

        # Extract accent for styling
        accent = kwargs.pop('accent', None)
        surface = kwargs.pop('surface', None)
        self._accent = accent  # Store for later use

        # Extract width for label (frame width doesn't work well with propagation)
        self._width = kwargs.pop('width', None)

        # Extract anchor for label
        self._anchor = kwargs.pop('anchor', 'center')

        super().__init__(
            master=master,
            ttk_class=ttk_class,
            accent=accent,
            variant=variant,
            takefocus=False,
            style_options={"orient": orient},
            **kwargs
        )

        # Build internal widgets
        self._label: Label | None = None
        self._close_button: Button | None = None

        self._build_widget(accent, surface)

        # Set up signal/variable after widget is built
        if signal is not None:
            self._set_signal_or_variable(signal)
        elif variable is not None:
            self._set_signal_or_variable(variable)

        # Bind click handler
        self.on_invoked(self._on_tab_click)

        # Bind destroy handler to clean up variable trace
        self.bind('<Destroy>', self._on_destroy, add='+')

    def _on_destroy(self, event=None):
        """Clean up variable trace when widget is destroyed."""
        if event.widget is not self:
            return
        if self._variable is not None and self._trace_id is not None:
            try:
                self._variable.trace_remove('write', self._trace_id)
            except Exception:
                pass
            self._trace_id = None

    def _get_ttk_class(self, variant: str) -> str:
        """Get the ttk class name for the given variant."""
        return 'TabItem.TFrame'

    def _build_widget(self, accent: str = None, surface: str = None):
        """Build the internal widget structure."""
        style_opts = {}
        if surface:
            style_opts['surface'] = surface

        # Pass width to label if specified
        label_opts = {}
        if self._width is not None:
            label_opts['width'] = self._width

        # Main label for text/icon
        self._label = Label(
            self,
            text=self._text,
            icon=self._icon,
            compound=self._compound,
            ttk_class='TabItem.TLabel',
            accent=accent,
            variant=self._variant,
            takefocus=False,
            anchor=self._anchor,
            **style_opts,
            **label_opts
        )
        self.register_composite(self._label)
        self._label.pack(side='left', fill='both', expand=True)

        # Close button (optional - show when closable is True or 'hover')
        if self._closable:
            self._create_close_button(accent, style_opts)

    def _create_close_button(self, accent: str = None, style_opts: dict = None):
        """Create the close button widget."""
        style_opts = style_opts or {}
        # Pass closable mode to style builder via style_options
        extra_style_options = {}
        if self._closable == 'hover':
            extra_style_options['closable'] = 'hover'
        self._close_button = Button(
            self,
            icon={'name': 'x-lg', 'size': 14},
            icon_only=True,
            ttk_class='TabItem.TButton',
            accent=accent,
            variant=self._variant,  # Use same variant as the tab for matching background
            takefocus=False,
            command=self._on_close_click,
            padding=0,
            anchor='center',
            style_options=extra_style_options,
            **style_opts
        )
        self.register_composite(self._close_button)
        self._close_button.place(relx=1.0, rely=0.5, anchor='e', x=4)

    def _set_signal_or_variable(self, value: Any):
        """Set up signal/variable binding with trace for selection updates."""
        # Remove old trace if exists
        if self._variable is not None and self._trace_id is not None:
            try:
                self._variable.trace_remove('write', self._trace_id)
            except Exception:
                pass

        # Normalize to get both signal and variable
        binding = normalize_signal(value)
        if binding is not None:
            self._signal = binding.signal
            self._variable = binding.variable
        else:
            self._variable = value
            self._signal = None

        # Add trace to update selection state
        if self._variable is not None:
            self._trace_id = self._variable.trace_add('write', self._on_variable_changed)
            # Initial update
            self._update_selection_state()

    def _on_variable_changed(self, *args):
        """Handle variable changes to update selection state."""
        self._update_selection_state()

    def _update_selection_state(self):
        """Update visual state based on selection."""
        # Guard against updates after widget destruction
        try:
            if not self.winfo_exists():
                return
        except TclError:
            return

        if self._variable is not None and self._value is not None:
            is_selected = self._variable.get() == self._value
            self.set_selected(is_selected)

    def _on_tab_click(self, event=None):
        """Handle tab click - select and invoke command."""
        # Set selection if variable is configured
        if self._variable is not None and self._value is not None:
            self._variable.set(self._value)

        # Invoke command if provided
        if self._command is not None:
            self._command()

        # Generate virtual event
        self.event_generate('<<TabSelect>>', data={'value': self._value})

    def _on_close_click(self):
        """Handle close button click."""
        # Store value before potential destruction
        value = self._value

        # Generate virtual event BEFORE close_command (which may destroy the widget)
        self.event_generate('<<TabClose>>', data={'value': value})

        # Invoke close command if provided (this may destroy the widget)
        if self._close_command is not None:
            self._close_command()

    # --- Public API ---

    def select(self):
        """Select this tab (set variable to this tab's value)."""
        if self._variable is not None and self._value is not None:
            self._variable.set(self._value)

    @property
    def value(self) -> Any:
        """Get the value associated with this tab."""
        return self._value

    @property
    def is_selected(self) -> bool:
        """Check if this tab is currently selected."""
        if self._variable is not None and self._value is not None:
            return self._variable.get() == self._value
        return self.selected

    # --- Configuration delegates ---

    @configure_delegate('text')
    def _delegate_text(self, value=None):
        """Get or set the tab text."""
        if value is None:
            return self._text
        self._text = value
        if self._label is not None:
            self._label.configure(text=value)
        return None

    @configure_delegate('icon')
    def _delegate_icon(self, value=None):
        """Get or set the tab icon."""
        if value is None:
            return self._icon
        self._icon = value
        if self._label is not None:
            self._label.configure(icon=value)
        return None

    @configure_delegate('compound')
    def _delegate_compound(self, value=None):
        """Get or set the compound (icon position relative to text)."""
        if value is None:
            return self._compound
        self._compound = value
        if self._label is not None:
            self._label.configure(compound=value)
        return None

    @configure_delegate('value')
    def _delegate_value(self, value=None):
        """Get or set the tab value."""
        if value is None:
            return self._value
        self._value = value
        self._update_selection_state()
        return None

    @configure_delegate('command')
    def _delegate_command(self, value=None):
        """Get or set the selection command."""
        if value is None:
            return self._command
        self._command = value
        return None

    @configure_delegate('close_command')
    def _delegate_close_command(self, value=None):
        """Get or set the close command."""
        if value is None:
            return self._close_command
        self._close_command = value
        return None

    @configure_delegate('closable')
    def _delegate_closable(self, value=None):
        """Get or set close button visibility (True, False, or 'hover')."""
        if value is None:
            return self._closable
        if value != self._closable:
            self._closable = value
            if value and self._close_button is None:
                self._create_close_button(self._accent)
            elif not value and self._close_button is not None:
                self._close_button.place_forget()
                self._close_button.destroy()
                self._close_button = None
        return None

    @configure_delegate('signal')
    def _delegate_signal(self, value=None):
        """Get or set the signal for selection state."""
        if value is None:
            return self._signal
        self._set_signal_or_variable(value)
        return None

    @configure_delegate('variable')
    def _delegate_variable(self, value=None):
        """Get or set the variable for selection state."""
        if value is None:
            return self._variable
        self._set_signal_or_variable(value)
        return None