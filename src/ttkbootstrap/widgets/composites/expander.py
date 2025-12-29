"""Expander widget - a collapsible container with header and content."""
from __future__ import annotations

from tkinter import Widget, Variable
from typing import Any, Literal, TYPE_CHECKING

from ttkbootstrap.widgets.primitives.frame import Frame
from ttkbootstrap.widgets.primitives.label import Label
from ttkbootstrap.widgets.composites.compositeframe import CompositeFrame
from ttkbootstrap.widgets.mixins import configure_delegate
from ttkbootstrap.widgets.types import Master
from ttkbootstrap.core.capabilities.signals import (
    normalize_signal,
    create_signal,
)

if TYPE_CHECKING:
    from ttkbootstrap.core.signals import Signal


class Expander(Frame):
    """A collapsible container with a clickable header and expandable content.

    The Expander displays a header with an optional icon, title, and chevron button.
    Clicking anywhere on the header toggles the visibility of the content area.

    Expander also supports selection state via `signal`/`variable` and `value`,
    similar to RadioButton. When clicked, it sets the variable to its value,
    enabling radio-group-like behavior for navigation.

    Events:
        ``<<Toggle>>``: Fired when expanded/collapsed. event.data = {'expanded': bool}
        ``<<Selected>>``: Fired when this expander is selected. event.data = {'value': Any}

    Attributes:
        expanded (bool): Current expansion state.
        content (Frame): The content container frame.
        is_selected (bool): Whether this expander's value matches the variable.
    """

    def __init__(
        self,
        master: Master = None,
        title: str = "",
        icon: str | dict = None,
        expanded: bool = True,
        collapsible: bool = True,
        icon_expanded: str | dict = None,
        icon_collapsed: str | dict = None,
        icon_position: Literal["before", "after"] = "after",
        signal: 'Signal[Any]' = None,
        variable: Variable = None,
        value: Any = None,
        **kwargs
    ):
        """Create an Expander widget.

        Args:
            master (Master): Parent widget. If None, uses the default root window.
            title (str): Header title text.
            icon (str | dict): Icon to display in header (left of title).
            expanded (bool): Initial expansion state. Default is True (expanded).
            collapsible (bool): Whether the expander can be toggled. Default is True.
            icon_expanded (str | dict): Icon spec for expanded state. Default is chevron-up.
            icon_collapsed (str | dict): Icon spec for collapsed state. Default is chevron-down.
            icon_position (Literal["before", "after"]): Position of chevron relative to title.
            signal (Signal): Reactive Signal for selection state (preferred over variable).
            variable (Variable): Tk variable for selection state (synced with signal).
            value (Any): Value to set on signal/variable when selected.
            **kwargs: Additional arguments passed to Frame. If bootstyle is provided,
                the chevron button will use that style (default: foreground-ghost).
        """
        self._header_bootstyle = kwargs.pop('bootstyle', '')
        kwargs.setdefault('padding', 3)
        kwargs.setdefault('takefocus', False)  # Outer container shouldn't take focus
        super().__init__(master, **kwargs)

        self._title = title
        self._icon = icon
        self._expanded = expanded
        self._collapsible = collapsible
        self._icon_expanded = icon_expanded
        self._icon_collapsed = icon_collapsed
        self._icon_position = icon_position
        self._content_widget = None
        self._value = value
        self._compact = False

        # Selection state - signal/variable syncing
        self._signal: Signal[Any] | None = None
        self._variable: Variable | None = None
        self._trace_id: str | None = None

        # Widget references
        self._icon_label: Label | None = None
        self._title_label: Label | None = None

        self._build_widget()

        # Set up signal/variable after widget is built
        # Prefer signal if both provided
        if signal is not None:
            self._set_signal_or_variable(signal)
        elif variable is not None:
            self._set_signal_or_variable(variable)

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
            # Direct variable
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
        # For now, just track state - visual updates can be added later
        # when a dedicated nav style is created
        pass

    @property
    def _current_chevron_icon(self):
        """Get the appropriate chevron icon for current state."""
        if self._expanded:
            return self._icon_expanded or {'name': 'chevron-up', 'size': 16}
        else:
            return self._icon_collapsed or {'name': 'chevron-down', 'size': 16}

    def _build_widget(self, bootstyle=''):
        """Build the internal widget structure."""
        bootstyle = self._header_bootstyle

        # Use CompositeFrame for header to enable hover/pressed/focus states
        self._header_frame = CompositeFrame(
            self, class_='Expander.TFrame', bootstyle=bootstyle, padding=8, takefocus=True
        )
        self._header_frame.pack(fill='x')

        # Icon (optional, before title)
        if self._icon:
            self._icon_label = Label(
                self._header_frame,
                icon=self._icon,
                icon_only=True,
                class_='Expander.TLabel',
                bootstyle=bootstyle,
                takefocus=False,
            )
            self._header_frame.register_composite(self._icon_label)
            self._icon_label.pack(side='left', padx=(0, 8))

        # Title label
        self._title_label = Label(
            self._header_frame,
            text=self._title,
            anchor='w',
            class_='Expander.TLabel',
            bootstyle=bootstyle,
            takefocus=False,
        )
        self._header_frame.register_composite(self._title_label)

        # Toggle button (chevron)
        self._toggle_button = Label(
            self._header_frame,
            icon=self._current_chevron_icon,
            icon_only=True,
            bootstyle=bootstyle,
            class_='Expander.TLabel',
            takefocus=False,
        )
        self._header_frame.register_composite(self._toggle_button)

        # Layout based on icon_position
        if self._icon_position == "before":
            self._toggle_button.pack(side='left')
            self._title_label.pack(side='left', fill='x', expand=True)
        else:
            self._title_label.pack(side='left', fill='x', expand=True)
            self._toggle_button.pack(side='right')

        # Hide button if not collapsible
        if not self._collapsible:
            self._toggle_button.pack_forget()

        # Content frame
        self._content_frame = Frame(self, padding=(8, 8))
        if self._expanded:
            self._content_frame.pack(fill='both', expand=True)

        # Bind header events
        self._bind_header_events()

    def _bind_header_events(self):
        """Make entire header clickable and keyboard accessible."""
        # Always bind for selection, even if not collapsible
        self._header_frame.bind('<Button-1>', self._on_header_click, add='+')
        self._title_label.bind('<Button-1>', self._on_header_click, add='+')
        if self._icon_label:
            self._icon_label.bind('<Button-1>', self._on_header_click, add='+')

        # Keyboard support
        self._header_frame.bind('<Return>', self._on_header_click, add='+')
        self._header_frame.bind('<space>', self._on_header_click, add='+')

    def _on_header_click(self, event=None):
        """Handle header click - select and optionally toggle."""
        # Request focus on click
        self._header_frame.focus_set()

        # Set selection if variable is configured
        if self._variable is not None and self._value is not None:
            self._variable.set(self._value)
            self.event_generate('<<Selected>>', data={'value': self._value})

        # Toggle expansion if collapsible
        if self._collapsible:
            self.toggle()

    def toggle(self):
        """Toggle expanded/collapsed state."""
        if not self._collapsible:
            return

        if self._expanded:
            self.collapse()
        else:
            self.expand()

    def expand(self):
        """Expand the content area."""
        if self._expanded:
            return

        self._expanded = True
        self._content_frame.pack(fill='both', expand=True)
        self._toggle_button.configure(icon=self._current_chevron_icon)
        self.event_generate('<<Toggle>>', data={'expanded': True})

    def collapse(self):
        """Collapse the content area."""
        if not self._expanded:
            return

        self._expanded = False
        self._content_frame.pack_forget()
        self._toggle_button.configure(icon=self._current_chevron_icon)
        self.event_generate('<<Toggle>>', data={'expanded': False})

    def select(self):
        """Select this expander (set variable to this expander's value)."""
        if self._variable is not None and self._value is not None:
            self._variable.set(self._value)

    def add(self, widget: Widget = None, **kwargs) -> Widget:
        """Add content widget, or create and return an empty frame.

        Args:
            widget (Widget | None): Optional widget to use as content. If None, creates a Frame.
            **kwargs: When widget is None, these are passed to Frame (e.g., padding, bootstyle).

        Returns:
            Widget: The content widget (passed or created).

        Raises:
            ValueError: If content already exists and widget is provided.
        """
        # If content exists and no widget passed, return existing (idempotent)
        if self._content_widget is not None:
            if widget is not None:
                raise ValueError("Expander already has content.")
            return self._content_widget

        if widget is None:
            widget = Frame(self._content_frame, **kwargs)

        self._content_widget = widget
        widget.pack(fill='both', expand=True)
        return widget

    @property
    def expanded(self) -> bool:
        """Get current expansion state."""
        return self._expanded

    @expanded.setter
    def expanded(self, value: bool):
        """Set expansion state."""
        if value:
            self.expand()
        else:
            self.collapse()

    @property
    def content(self) -> Frame:
        """Get the content frame (for direct child parenting)."""
        return self._content_frame

    @property
    def is_selected(self) -> bool:
        """Check if this expander is currently selected."""
        if self._variable is not None and self._value is not None:
            return self._variable.get() == self._value
        return False

    @property
    def value(self) -> Any:
        """Get the selection value for this expander."""
        return self._value

    @property
    def signal(self) -> 'Signal[Any] | None':
        """Get the signal for selection state."""
        return self._signal

    @signal.setter
    def signal(self, value: 'Signal[Any]'):
        """Set the signal for selection state."""
        self._set_signal_or_variable(value)

    @property
    def variable(self) -> Variable | None:
        """Get the variable for selection state."""
        return self._variable

    @variable.setter
    def variable(self, value: Variable):
        """Set the variable for selection state."""
        self._set_signal_or_variable(value)

    def on_toggle(self, callback) -> str:
        """Bind callback to ``<<Toggle>>`` events.

        Args:
            callback (Callable): Function to call when toggled. Receives event with
                event.data = {'expanded': bool}.

        Returns:
            str: Bind ID that can be passed to ``off_toggle`` to remove this callback.
        """
        return self.bind('<<Toggle>>', callback, add='+')

    def off_toggle(self, bind_id: str = None):
        """Unbind ``<<Toggle>>`` callback(s).

        Args:
            bind_id (str | None): Bind ID returned by ``on_toggle``. If None, unbinds all.
        """
        self.unbind('<<Toggle>>', bind_id)

    def on_selected(self, callback) -> str:
        """Bind callback to ``<<Selected>>`` events.

        Args:
            callback (Callable): Function to call when selected. Receives event with
                event.data = {'value': Any}.

        Returns:
            str: Bind ID that can be passed to ``off_selected`` to remove this callback.
        """
        return self.bind('<<Selected>>', callback, add='+')

    def off_selected(self, bind_id: str = None):
        """Unbind ``<<Selected>>`` callback(s).

        Args:
            bind_id (str | None): Bind ID returned by ``on_selected``. If None, unbinds all.
        """
        self.unbind('<<Selected>>', bind_id)

    @configure_delegate('title')
    def _delegate_title(self, value=None):
        """Get or set the title text."""
        if value is None:
            return self._title
        self._title = value
        self._title_label.configure(text=value)
        return None

    @configure_delegate('icon')
    def _delegate_icon(self, value=None):
        """Get or set the header icon."""
        if value is None:
            return self._icon
        self._icon = value
        if self._icon_label is not None:
            self._icon_label.configure(icon=value)
        elif value is not None:
            # Create icon label if it doesn't exist
            self._icon_label = Label(
                self._header_frame,
                icon=value,
                icon_only=True,
                class_='Expander.TLabel',
                bootstyle=self._header_bootstyle,
                takefocus=False,
            )
            self._header_frame.register_composite(self._icon_label)
            # Insert at beginning of header
            self._icon_label.pack(side='left', padx=(0, 8), before=self._title_label)
            self._icon_label.bind('<Button-1>', self._on_header_click, add='+')
        return None

    @configure_delegate('collapsible')
    def _delegate_collapsible(self, value=None):
        """Get or set whether the expander can be toggled."""
        if value is None:
            return self._collapsible
        self._collapsible = value
        if value:
            side = 'left' if self._icon_position == 'before' else 'right'
            self._toggle_button.pack(side=side)
        else:
            self._toggle_button.pack_forget()
        return None

    @configure_delegate('icon_expanded')
    def _delegate_icon_expanded(self, value=None):
        """Get or set the expanded state chevron icon."""
        if value is None:
            return self._icon_expanded
        self._icon_expanded = value
        if self._expanded:
            self._toggle_button.configure(icon=self._current_chevron_icon)
        return None

    @configure_delegate('icon_collapsed')
    def _delegate_icon_collapsed(self, value=None):
        """Get or set the collapsed state chevron icon."""
        if value is None:
            return self._icon_collapsed
        self._icon_collapsed = value
        if not self._expanded:
            self._toggle_button.configure(icon=self._current_chevron_icon)
        return None

    @configure_delegate('value')
    def _delegate_value(self, value=None):
        """Get or set the selection value."""
        if value is None:
            return self._value
        self._value = value
        return None

    @configure_delegate('compact')
    def _delegate_compact(self, value=None):
        """Get or set compact mode (hides title, shows icon only)."""
        if value is None:
            return self._compact
        self._compact = value
        if value:
            # Hide title
            if self._title_label is not None:
                self._title_label.pack_forget()
            # Center the icon
            if self._icon_label is not None:
                self._icon_label.pack_forget()
                self._icon_label.pack(expand=True)
        else:
            # Restore icon to left-aligned
            if self._icon_label is not None:
                self._icon_label.pack_forget()
                self._icon_label.pack(side='left', padx=(0, 8))
            # Re-pack title in correct position
            if self._title_label is not None:
                if self._icon_position == "before":
                    self._title_label.pack(side='left', fill='x', expand=True)
                else:
                    # Pack after icon (if exists) or at left
                    if self._icon_label is not None:
                        self._title_label.pack(side='left', fill='x', expand=True, after=self._icon_label)
                    else:
                        self._title_label.pack(side='left', fill='x', expand=True)
        return None
