"""Scrolled text widget with configurable scrollbars."""
import tkinter
from typing import Any, Literal, Optional

from ttkbootstrap.widgets.primitives.frame import Frame
from ttkbootstrap.widgets.mixins.configure_mixin import configure_delegate
from ttkbootstrap.widgets.primitives.scrollbar import Scrollbar


class ScrolledText(Frame):
    """A text widget with configurable scrollbars and mouse wheel support.

    The ScrolledText widget provides a Text widget with scrollbars that can be
    configured to appear always, never, on hover, or when scrolling. Full mouse
    wheel support is included.

    This widget delegates all Text methods to the internal text widget, so it
    can be used just like a standard Text widget with additional scrolling
    functionality.

    Attributes:
        vertical_scrollbar (Scrollbar): The vertical scrollbar widget.
        horizontal_scrollbar (Scrollbar): The horizontal scrollbar widget.
    """

    def __init__(
            self,
            master: Optional[tkinter.Misc] = None,
            padding: int = 0,
            scroll_direction: Literal['horizontal', 'vertical', 'both'] = 'vertical',
            scrollbar_visibility: Literal['always', 'never', 'hover', 'scroll'] = 'always',
            autohide_delay: int = 1000,
            scrollbar_style: str = 'default',
            **kwargs: Any,
    ) -> None:
        """Initialize a ScrolledText widget.

        Args:
            master: The parent widget.
            padding: Padding around the frame container.
            scroll_direction: Scroll direction - 'vertical', 'horizontal', or 'both'.
                Use 'both' to enable horizontal scrolling with Shift+MouseWheel.
            scrollbar_visibility: Scrollbar visibility mode:
                - 'always': Scrollbars always visible
                - 'never': Scrollbars hidden (scrolling still works)
                - 'hover': Scrollbars appear when mouse enters
                - 'scroll': Scrollbars appear when scrolling, auto-hide after delay
            autohide_delay: Time in milliseconds before auto-hiding scrollbars
                in 'scroll' mode.
            scrollbar_style: The bootstyle for scrollbars (e.g., 'primary',
                'success', 'danger').
            **kwargs: Additional keyword arguments passed to the Text widget.

        Note:
            Legacy parameters 'autohide', 'vbar', and 'hbar' parameters work, but are deprecated. Use
            `scroll_direction` and `scrollbar_visibility` instead.
        """
        # Handle deprecated parameters
        autohide = kwargs.pop('autohide', None)
        if autohide is not None:
            scrollbar_visibility = 'hover' if autohide else 'always'

        vbar = kwargs.pop('vbar', None)
        hbar = kwargs.pop('hbar', None)
        if vbar is not None or hbar is not None:
            # Determine direction from vbar/hbar
            if hbar and vbar:
                scroll_direction = 'both'
            elif hbar:
                scroll_direction = 'horizontal'
            elif vbar:
                scroll_direction = 'vertical'
            else:
                scroll_direction = 'vertical'  # Default

        # Initialize Frame
        super().__init__(master=master, padding=padding)

        # Configuration
        self._direction = scroll_direction
        self._scrollbar_visibility = scrollbar_visibility
        self._autohide_delay = autohide_delay
        self._scrollbar_style = scrollbar_style
        self._hide_timer = None

        # Create unique bind tag for this scrolledtext
        self._scroll_tag = f'ScrolledText_{id(self)}'

        # Detect windowing system
        self.winsys = self.tk.call("tk", "windowingsystem")

        # Bind scroll events to our custom tag
        self._setup_scroll_tag_bindings()

        # Create text widget
        text_kwargs = kwargs.copy()

        # Set wrap mode based on direction
        if scroll_direction == 'both' or scroll_direction == 'horizontal':
            if 'wrap' not in text_kwargs:
                text_kwargs['wrap'] = 'none'

        self._text = tkinter.Text(self, **text_kwargs)

        # Create scrollbars
        self.vertical_scrollbar = Scrollbar(
            master=self,
            orient='vertical',
            command=self._text.yview,
            accent=scrollbar_style if scrollbar_style != 'default' else None
        )
        self.horizontal_scrollbar = Scrollbar(
            master=self,
            orient='horizontal',
            command=self._text.xview,
            accent=scrollbar_style if scrollbar_style != 'default' else None
        )

        # Configure text scrolling
        if scroll_direction in ('vertical', 'both'):
            self._text.configure(yscrollcommand=self._on_text_scroll_y)
        if scroll_direction in ('horizontal', 'both'):
            self._text.configure(xscrollcommand=self._on_text_scroll_x)

        # Layout
        self._layout_widgets()

        # Bind events for autohide/hover
        self._bind_container_events()

        # Initial scrollbar visibility
        self._update_scrollbar_visibility()

        # Add scroll bindings to text widget
        self._add_scroll_binding(self._text)

        # Delegate text methods to this widget (except geometry managers)
        for method in vars(tkinter.Text).keys():
            if any(["pack" in method, "grid" in method, "place" in method]):
                pass
            else:
                # Don't override methods that already exist
                if not hasattr(self, method):
                    setattr(self, method, getattr(self._text, method))

    @configure_delegate('scroll_direction')
    def _delegate_scroll_direction(self, value=None):
        if value is None:
            return self._direction
        else:
            self._direction = value
            # Update scrollbar visibility and layout
            self._update_scrollbar_visibility()
        return None

    @configure_delegate('scrollbar_visibility')
    def _delegate_scrollbar_visibility(self, value=None):
        if value is None:
            return self._scrollbar_visibility
        else:
            old_value = self._scrollbar_visibility
            self._scrollbar_visibility = value

            # Unbind old events if changing from hover
            if old_value == 'hover':
                self.unbind('<Enter>')
                self.unbind('<Leave>')
                self._text.unbind('<Enter>')
                self._text.unbind('<Leave>')
                self.vertical_scrollbar.unbind('<Enter>')
                self.vertical_scrollbar.unbind('<Leave>')
                self.horizontal_scrollbar.unbind('<Enter>')
                self.horizontal_scrollbar.unbind('<Leave>')

            # Bind new events and update scrollbar visibility
            self._bind_container_events()
            self._update_scrollbar_visibility()
        return None

    @configure_delegate('autohide_delay')
    def _delegate_autohide_delay(self, value=None):
        if value is None:
            return self._autohide_delay
        else:
            self._autohide_delay = value
        return None

    @configure_delegate('scrollbar_style')
    def _delegate_scrollbar_style(self, value=None):
        if value is None:
            return self._scrollbar_style
        else:
            self._scrollbar_style = value
            # Apply the new accent to both scrollbars
            if value and value != 'default':
                self.vertical_scrollbar.configure(accent=value)
                self.horizontal_scrollbar.configure(accent=value)
        return None

    def _setup_scroll_tag_bindings(self):
        """Setup bindings on our custom bind tag."""
        if self.winsys.lower() == "x11":
            self.bind_class(self._scroll_tag, "<Button-4>", self._on_mousewheel)
            self.bind_class(self._scroll_tag, "<Button-5>", self._on_mousewheel)
            self.bind_class(self._scroll_tag, "<Shift-Button-4>", self._on_shift_mousewheel)
            self.bind_class(self._scroll_tag, "<Shift-Button-5>", self._on_shift_mousewheel)
        else:
            self.bind_class(self._scroll_tag, "<MouseWheel>", self._on_mousewheel)
            self.bind_class(self._scroll_tag, "<Shift-MouseWheel>", self._on_shift_mousewheel)

    def _layout_widgets(self):
        """Layout the text widget and scrollbars."""
        self._text.grid(row=0, column=0, sticky='nsew')

        if self._direction in ('vertical', 'both'):
            self.vertical_scrollbar.grid(row=0, column=1, sticky='ns')

        if self._direction in ('horizontal', 'both'):
            self.horizontal_scrollbar.grid(row=1, column=0, sticky='ew')

        # Configure grid weights
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Initially hide scrollbars based on scrollbar_visibility setting
        if self._scrollbar_visibility == 'never':
            self.vertical_scrollbar.grid_remove()
            self.horizontal_scrollbar.grid_remove()
        elif self._scrollbar_visibility in ('hover', 'scroll'):
            self.vertical_scrollbar.grid_remove()
            self.horizontal_scrollbar.grid_remove()

    def _bind_container_events(self):
        """Bind events for the container (enter/leave for autohide)."""
        if self._scrollbar_visibility == 'hover':
            self.bind('<Enter>', self._on_container_enter)
            self.bind('<Leave>', self._on_container_leave)
            self._text.bind('<Enter>', self._on_container_enter)
            self._text.bind('<Leave>', self._on_container_leave)
            self.vertical_scrollbar.bind('<Enter>', self._on_container_enter)
            self.vertical_scrollbar.bind('<Leave>', self._on_container_leave)
            self.horizontal_scrollbar.bind('<Enter>', self._on_container_enter)
            self.horizontal_scrollbar.bind('<Leave>', self._on_container_leave)

    def _on_container_enter(self, event):
        """Handle mouse entering the container."""
        if self._scrollbar_visibility == 'hover':
            self._show_scrollbars()

    def _on_container_leave(self, event):
        """Handle mouse leaving the container."""
        if self._scrollbar_visibility == 'hover':
            self._hide_scrollbars()

    def _show_scrollbars(self):
        """Show scrollbars."""
        if self._direction in ('vertical', 'both'):
            self.vertical_scrollbar.grid()
        if self._direction in ('horizontal', 'both'):
            self.horizontal_scrollbar.grid()

    def _hide_scrollbars(self):
        """Hide scrollbars."""
        self.vertical_scrollbar.grid_remove()
        self.horizontal_scrollbar.grid_remove()

    def _on_text_scroll_y(self, first, last):
        """Update vertical scrollbar position."""
        self.vertical_scrollbar.set(first, last)

    def _on_text_scroll_x(self, first, last):
        """Update horizontal scrollbar position."""
        self.horizontal_scrollbar.set(first, last)

    def _update_scrollbar_visibility(self):
        """Update scrollbar visibility based on current mode."""
        if self._scrollbar_visibility == 'always':
            self._show_scrollbars()
        elif self._scrollbar_visibility == 'never':
            self._hide_scrollbars()

    def _on_mousewheel(self, event):
        """Handle vertical mouse wheel scrolling."""
        # Show scrollbar temporarily in scroll mode
        if self._scrollbar_visibility == 'scroll':
            self._show_scrollbars()
            if self._hide_timer:
                self.after_cancel(self._hide_timer)
            self._hide_timer = self.after(self._autohide_delay, self._hide_scrollbars)

        # Calculate delta based on platform
        delta = 0
        if self.winsys.lower() == "win32":
            delta = -int(event.delta / 120)
        elif self.winsys.lower() == "aqua":
            delta = -event.delta
        elif event.num == 4:
            delta = -1
        elif event.num == 5:
            delta = 1

        # Scroll vertically
        if self._direction in ('vertical', 'both') and delta != 0:
            self._text.yview_scroll(delta, 'units')

    def _on_shift_mousewheel(self, event):
        """Handle horizontal mouse wheel scrolling (Shift+MouseWheel)."""
        # Show scrollbar temporarily in scroll mode
        if self._scrollbar_visibility == 'scroll':
            self._show_scrollbars()
            if self._hide_timer:
                self.after_cancel(self._hide_timer)
            self._hide_timer = self.after(self._autohide_delay, self._hide_scrollbars)

        # Calculate delta based on platform
        delta = 0
        if self.winsys.lower() == "win32":
            delta = -int(event.delta / 120)
        elif self.winsys.lower() == "aqua":
            delta = -event.delta
        elif event.num == 4:
            delta = -1
        elif event.num == 5:
            delta = 1

        # Scroll horizontally
        if self._direction in ('horizontal', 'both') and delta != 0:
            self._text.xview_scroll(delta, 'units')

    def _add_scroll_binding(self, widget):
        """Add scroll bind tag to widget."""
        try:
            tags = list(widget.bindtags())
            if self._scroll_tag not in tags:
                if len(tags) >= 2:
                    tags.insert(1, self._scroll_tag)
                else:
                    tags.append(self._scroll_tag)
                widget.bindtags(tuple(tags))
        except:
            pass

    def destroy(self):
        """Clean up resources and destroy the widget."""
        # Cancel any pending timer
        if self._hide_timer:
            self.after_cancel(self._hide_timer)
            self._hide_timer = None

        # Unbind class bindings for the scroll tag
        if self.winsys.lower() == "x11":
            self.unbind_class(self._scroll_tag, "<Button-4>")
            self.unbind_class(self._scroll_tag, "<Button-5>")
            self.unbind_class(self._scroll_tag, "<Shift-Button-4>")
            self.unbind_class(self._scroll_tag, "<Shift-Button-5>")
        else:
            self.unbind_class(self._scroll_tag, "<MouseWheel>")
            self.unbind_class(self._scroll_tag, "<Shift-MouseWheel>")

        # Call parent destroy
        super().destroy()

    def __getattr__(self, name: str) -> Any:
        """Delegate unknown attribute access to the internal Text widget.

        Args:
            name: The attribute name to access.

        Returns:
            The attribute from the internal Text widget.

        Raises:
            AttributeError: If _text doesn't exist yet or doesn't have the attribute.
        """
        # Avoid infinite recursion during initialization
        if '_text' not in self.__dict__:
            raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")
        return getattr(self._text, name)

    @property
    def text(self):
        """Get the internal text widget.

        Returns:
            The underlying Text widget instance.
        """
        return self._text

