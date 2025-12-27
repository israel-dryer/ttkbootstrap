"""Expander widget - a collapsible container with header and content."""
from tkinter import Widget
from typing import Literal

from ttkbootstrap.widgets.primitives.frame import Frame
from ttkbootstrap.widgets.primitives.button import Button
from ttkbootstrap.widgets.primitives.label import Label
from ttkbootstrap.widgets.mixins import configure_delegate
from ttkbootstrap.widgets.types import Master


class Expander(Frame):
    """A collapsible container with a clickable header and expandable content.

    The Expander displays a header with a title and chevron button. Clicking
    anywhere on the header toggles the visibility of the content area.

    Events:
        ``<<Toggle>>``: Fired when expanded/collapsed. event.data = {'expanded': bool}

    Attributes:
        expanded (bool): Current expansion state.
        content (Frame): The content container frame.
    """

    def __init__(
        self,
        master: Master = None,
        title: str = "",
        expanded: bool = True,
        collapsible: bool = True,
        icon_expanded: str | dict = None,
        icon_collapsed: str | dict = None,
        icon_position: Literal["before", "after"] = "after",
        **kwargs
    ):
        """Create an Expander widget.

        Args:
            master (Master): Parent widget. If None, uses the default root window.
            title (str): Header title text.
            expanded (bool): Initial expansion state. Default is True (expanded).
            collapsible (bool): Whether the expander can be toggled. Default is True.
            icon_expanded (str | dict): Icon spec for expanded state. Default is chevron-up.
            icon_collapsed (str | dict): Icon spec for collapsed state. Default is chevron-down.
            icon_position (Literal["before", "after"]): Position of chevron relative to title.
            **kwargs: Additional arguments passed to Frame. If bootstyle is provided,
                the chevron button will use that style (default: foreground-ghost).
        """
        bootstyle = kwargs.get('bootstyle', '')
        kwargs.setdefault('padding', 3)
        super().__init__(master, **kwargs)

        self._title = title
        self._expanded = expanded
        self._collapsible = collapsible
        self._icon_expanded = icon_expanded
        self._icon_collapsed = icon_collapsed
        self._icon_position = icon_position
        self._content_widget = None

        self._build_widget(bootstyle)

    @property
    def _current_icon(self):
        """Get the appropriate icon for current state."""
        if self._expanded:
            return self._icon_expanded or {'name': 'chevron-up', 'size': 16}
        else:
            return self._icon_collapsed or {'name': 'chevron-down', 'size': 16}

    def _build_widget(self, bootstyle=''):
        """Build the internal widget structure."""
        # Header frame (clickable)
        self._header_frame = Frame(self, padding=(8, 4, 4, 4))
        self._header_frame.pack(fill='x')

        # Title label
        self._title_label = Label(self._header_frame, text=self._title, anchor='w')

        # Toggle button (chevron) - use bootstyle if provided, else foreground-ghost
        chevron_style = bootstyle if bootstyle else "foreground-ghost"
        self._toggle_button = Button(
            self._header_frame,
            icon=self._current_icon,
            icon_only=True,
            bootstyle=chevron_style,
            command=self.toggle
        )

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
        if not self._collapsible:
            return

        # Click on header (button has its own command)
        self._header_frame.bind('<Button-1>', lambda e: self.toggle())
        self._title_label.bind('<Button-1>', lambda e: self.toggle())

        # Keyboard support
        self._header_frame.bind('<Return>', lambda e: self.toggle())
        self._header_frame.bind('<space>', lambda e: self.toggle())

        # Make header focusable
        self._header_frame.configure(takefocus=True)

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
        self._toggle_button.configure(icon=self._current_icon)
        self.event_generate('<<Toggle>>', data={'expanded': True})

    def collapse(self):
        """Collapse the content area."""
        if not self._expanded:
            return

        self._expanded = False
        self._content_frame.pack_forget()
        self._toggle_button.configure(icon=self._current_icon)
        self.event_generate('<<Toggle>>', data={'expanded': False})

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

    def on_toggle(self, callback) -> str:
        """Bind callback to `<<Toggle>>` events.

        Args:
            callback (Callable): Function to call when toggled. Receives event with
                event.data = {'expanded': bool}.

        Returns:
            str: Bind ID that can be passed to `off_toggle` to remove this callback.
        """
        return self.bind('<<Toggle>>', callback, add='+')

    def off_toggle(self, bind_id: str = None):
        """Unbind `<<Toggle>>` callback(s).

        Args:
            bind_id (str | None): Bind ID returned by `on_toggle`. If None, unbinds all.
        """
        self.unbind('<<Toggle>>', bind_id)

    @configure_delegate('title')
    def _delegate_title(self, value=None):
        """Get or set the title text."""
        if value is None:
            return self._title
        self._title = value
        self._title_label.configure(text=value)
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
            self._bind_header_events()
        else:
            self._toggle_button.pack_forget()
        return None

    @configure_delegate('icon_expanded')
    def _delegate_icon_expanded(self, value=None):
        """Get or set the expanded state icon."""
        if value is None:
            return self._icon_expanded
        self._icon_expanded = value
        if self._expanded:
            self._toggle_button.configure(icon=self._current_icon)
        return None

    @configure_delegate('icon_collapsed')
    def _delegate_icon_collapsed(self, value=None):
        """Get or set the collapsed state icon."""
        if value is None:
            return self._icon_collapsed
        self._icon_collapsed = value
        if not self._expanded:
            self._toggle_button.configure(icon=self._current_icon)
        return None
