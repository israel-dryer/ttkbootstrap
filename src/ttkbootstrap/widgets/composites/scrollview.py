"""Canvas-based scrollable container widget with mouse wheel support."""
from tkinter import Canvas
from tkinter.ttk import Widget
from typing import Any, Literal, Optional

from ttkbootstrap.widgets.primitives.frame import Frame
from ttkbootstrap.widgets.mixins.configure_mixin import configure_delegate
from ttkbootstrap.widgets.primitives.scrollbar import Scrollbar
from ttkbootstrap.widgets.types import Master


class ScrollView(Frame):
    """A canvas-based scrollable container with configurable scrollbar behavior.

    The ScrollView widget provides a scrollable area for child widgets with
    full mouse wheel support on all descendants. Scrollbars can be configured
    to appear always, never, on hover, or when scrolling, and are only visible
    when the content exceeds the available space.

    Attributes:
        canvas (Canvas): The underlying tkinter Canvas widget.
        vertical_scrollbar (Scrollbar): The vertical scrollbar widget.
        horizontal_scrollbar (Scrollbar): The horizontal scrollbar widget.
    """

    def __init__(
            self,
            master: Master = None,
            direction: Literal['horizontal', 'vertical', 'both'] = 'both',
            show_scrollbar: Literal['always', 'never', 'on-hover', 'on-scroll'] = 'always',
            autohide_delay: int = 1000,  # milliseconds for on-scroll mode
            scrollbar_style: str = 'default',
            **kwargs: Any
    ):
        """Initialize a ScrollView widget.

        Args:
            master: The parent widget.
            direction: Scroll direction - 'horizontal' for horizontal only,
                'vertical' for vertical only, or 'both' for bidirectional
                scrolling. Horizontal scrolling uses Shift+MouseWheel.
            show_scrollbar: Scrollbar visibility mode:
                - 'always': Scrollbars always visible
                - 'never': Scrollbars hidden (scrolling still works)
                - 'on-hover': Scrollbars appear when mouse enters the widget
                - 'on-scroll': Scrollbars appear when scrolling, auto-hide after delay
            autohide_delay: Time in milliseconds before auto-hiding scrollbars
                in 'on-scroll' mode. Default is 1000ms (1 second).
            scrollbar_style: The bootstyle to apply to scrollbars (e.g., 'primary',
                'success', 'danger'). If None, uses the default scrollbar style.
            **kwargs: Additional keyword arguments passed to the Frame parent class.

        Note:
            Mouse wheel scrolling is automatically enabled on all child widgets,
            including those added dynamically. For manual refresh of bindings
            after adding many widgets at once, call refresh_bindings().
        """
        super().__init__(master, **kwargs)

        # configuration
        self._direction = direction
        self._show_scrollbar = show_scrollbar
        self._autohide_delay = autohide_delay
        self._scrollbar_style = scrollbar_style

        self._child_widget = None
        self._window_id = None
        self._hide_timer = None
        self._scrolling_enabled = False
        self._hovering = False

        # Create unique bind tag for this scrollview
        self._scroll_tag = f'ScrollView_{id(self)}'

        # Detect windowing system
        self.winsys = self.tk.call("tk", "windowingsystem")

        # Bind scroll events to our custom tag
        self._setup_scroll_tag_bindings()

        # Create canvas
        self.canvas = Canvas(
            self,
            highlightthickness=0,
            borderwidth=0
        )
        self.canvas.bind("<Configure>", self._on_canvas_configure)

        # Create scrollbars
        self.vertical_scrollbar = Scrollbar(
            master=self,
            orient='vertical',
            command=self.canvas.yview,
            bootstyle=self._scrollbar_style
        )
        self.horizontal_scrollbar = Scrollbar(
            master=self,
            orient='horizontal',
            command=self.canvas.xview,
            bootstyle=self._scrollbar_style
        )

        # Configure canvas scrolling
        scroll_config = {}
        if direction in ('vertical', 'both'):
            scroll_config['yscrollcommand'] = self._on_canvas_scroll_y
        if direction in ('horizontal', 'both'):
            scroll_config['xscrollcommand'] = self._on_canvas_scroll_x

        self.canvas.configure(**scroll_config)

        # Layout
        self._layout_widgets()

        # Bind events for autohide/on-hover
        self._bind_container_events()

        # Initial scrollbar visibility
        self._update_scrollbar_visibility()

    @configure_delegate('direction')
    def _delegate_direction(self, value=None):
        if value is None:
            return self._direction
        else:
            old_direction = self._direction
            self._direction = value

            # Update canvas scroll configuration
            scroll_config = {}
            if value in ('vertical', 'both'):
                scroll_config['yscrollcommand'] = self._on_canvas_scroll_y
            else:
                scroll_config['yscrollcommand'] = None

            if value in ('horizontal', 'both'):
                scroll_config['xscrollcommand'] = self._on_canvas_scroll_x
            else:
                scroll_config['xscrollcommand'] = None

            self.canvas.configure(**scroll_config)

            # Update scrollbar visibility and layout
            self._update_scrollbar_visibility()
        return None

    @configure_delegate('show_scrollbar')
    def _delegate_show_scrollbar(self, value=None):
        if value is None:
            return self._show_scrollbar
        else:
            old_value = self._show_scrollbar
            self._show_scrollbar = value

            # Unbind old events if changing from on-hover
            if old_value == 'on-hover':
                self.unbind('<Enter>')
                self.unbind('<Leave>')
                self.canvas.unbind('<Enter>')
                self.canvas.unbind('<Leave>')
                self.vertical_scrollbar.unbind('<Enter>')
                self.vertical_scrollbar.unbind('<Leave>')
                self.horizontal_scrollbar.unbind('<Enter>')
                self.horizontal_scrollbar.unbind('<Leave>')

            # Bind new events and update scrollbar visibility
            self._bind_container_events()
            self._update_scrollbar_visibility()

            # Update scrolling enabled state
            if value in ('always', 'never', 'on-scroll'):
                if self._child_widget:
                    self.enable_scrolling()
            elif value == 'on-hover':
                # Scrolling will be enabled on hover
                self.disable_scrolling()
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
            # Apply the new bootstyle to both scrollbars
            if value:
                self.vertical_scrollbar.configure(bootstyle=value)
                self.horizontal_scrollbar.configure(bootstyle=value)
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
        """Layout the canvas and scrollbars."""
        self.canvas.grid(row=0, column=0, sticky='nsew')

        if self._direction in ('vertical', 'both'):
            self.vertical_scrollbar.grid(row=0, column=1, sticky='ns')

        if self._direction in ('horizontal', 'both'):
            self.horizontal_scrollbar.grid(row=1, column=0, sticky='ew')

        # Configure grid weights
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        # Keep scrollbars above the canvas/content when visible
        self.vertical_scrollbar.lift()
        self.horizontal_scrollbar.lift()

        # Initially hide scrollbars based on show_scrollbar setting
        if self._show_scrollbar == 'never':
            self.vertical_scrollbar.grid_remove()
            self.horizontal_scrollbar.grid_remove()
        elif self._show_scrollbar in ('on-hover', 'on-scroll'):
            self.vertical_scrollbar.grid_remove()
            self.horizontal_scrollbar.grid_remove()

    def _bind_container_events(self):
        """Bind events for the container (enter/leave for autohide)."""
        if self._show_scrollbar == 'on-hover':
            self.bind('<Enter>', self._on_container_enter)
            self.bind('<Leave>', self._on_container_leave)
            self.canvas.bind('<Enter>', self._on_container_enter)
            self.canvas.bind('<Leave>', self._on_container_leave)
            self.vertical_scrollbar.bind('<Enter>', self._on_container_enter)
            self.vertical_scrollbar.bind('<Leave>', self._on_container_leave)
            self.horizontal_scrollbar.bind('<Enter>', self._on_container_enter)
            self.horizontal_scrollbar.bind('<Leave>', self._on_container_leave)

    def _on_container_enter(self, event):
        """Handle mouse entering the container."""
        self._hovering = True
        self.enable_scrolling()
        if self._show_scrollbar == 'on-hover':
            self._show_scrollbars()

    def _on_container_leave(self, event):
        """Handle mouse leaving the container."""
        self._hovering = False
        self.disable_scrolling()
        if self._show_scrollbar == 'on-hover':
            self._hide_scrollbars()

    def _content_fits(self):
        """Return booleans for whether content fits in the viewport (x_fit, y_fit)."""
        if self._window_id:
            bbox = self.canvas.bbox(self._window_id)
        else:
            bbox = self.canvas.bbox('all')
        if not bbox:
            return True, True
        x0, y0, x1, y1 = bbox
        content_w = x1 - x0
        content_h = y1 - y0
        viewport_w = max(1, self.canvas.winfo_width())
        viewport_h = max(1, self.canvas.winfo_height())
        if viewport_w <= 1 or viewport_h <= 1:
            return True, True
        return content_w <= viewport_w, content_h <= viewport_h

    def _show_scrollbars(self):
        """Show scrollbars only if content overflows the viewport."""
        x_fit, y_fit = self._content_fits()
        if self._direction in ('vertical', 'both') and not y_fit:
            self.vertical_scrollbar.grid()
        else:
            self.vertical_scrollbar.grid_remove()
        if self._direction in ('horizontal', 'both') and not x_fit:
            self.horizontal_scrollbar.grid()
        else:
            self.horizontal_scrollbar.grid_remove()

    def _hide_scrollbars(self):
        """Hide scrollbars."""
        self.vertical_scrollbar.grid_remove()
        self.horizontal_scrollbar.grid_remove()

    def _on_canvas_configure(self, event):
        """Update visibility when the viewport size changes."""
        self._update_scrollbar_visibility()

    def _on_canvas_scroll_y(self, first, last):
        """Update vertical scrollbar position."""
        self.vertical_scrollbar.set(first, last)
        self._update_scrollbar_visibility()

    def _on_canvas_scroll_x(self, first, last):
        """Update horizontal scrollbar position."""
        self.horizontal_scrollbar.set(first, last)
        self._update_scrollbar_visibility()

    def _update_scrollbar_visibility(self):
        """Update scrollbar visibility based on current mode."""
        if self._show_scrollbar == 'always':
            self._show_scrollbars()
        elif self._show_scrollbar == 'never':
            self._hide_scrollbars()
        elif self._show_scrollbar == 'on-hover':
            # Show only while hovering and overflowing
            x_fit, y_fit = self._content_fits()
            if self._hovering and self._direction in ('vertical', 'both') and not y_fit:
                self.vertical_scrollbar.grid()
            else:
                self.vertical_scrollbar.grid_remove()

            if self._hovering and self._direction in ('horizontal', 'both') and not x_fit:
                self.horizontal_scrollbar.grid()
            else:
                self.horizontal_scrollbar.grid_remove()
        elif self._show_scrollbar == 'on-scroll':
            # Hide if no overflow; otherwise leave current visibility to scroll events
            x_fit, y_fit = self._content_fits()
            if y_fit:
                self.vertical_scrollbar.grid_remove()
            if x_fit:
                self.horizontal_scrollbar.grid_remove()

    def _on_frame_configure(self, event):
        """Update scroll region and refresh bindings on configure."""
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))
        self._update_scrollbar_visibility()

        # Refresh bindings for any newly added widgets
        if self._scrolling_enabled and self._child_widget:
            self._add_scroll_binding(self._child_widget)

    def _on_mousewheel(self, event):
        """Handle vertical mouse wheel scrolling."""
        # Check if vertical scrolling is actually possible
        if self._direction in ('vertical', 'both'):
            try:
                first, last = self.canvas.yview()
                # If first=0.0 and last=1.0, all content is visible, no need to scroll
                if first <= 0.0 and last >= 1.0:
                    return  # Content fits, don't scroll
            except:
                pass  # If we can't check, allow scrolling

        # Show scrollbar temporarily in on-scroll mode
        if self._show_scrollbar == 'on-scroll':
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
            delta = -10
        elif event.num == 5:
            delta = 10

        # Scroll vertically
        if self._direction in ('vertical', 'both') and delta != 0:
            self.canvas.yview_scroll(delta, 'units')

        # Don't return 'break' - allow event to propagate to other handlers if needed
        # But we can return None to continue normal processing

    def _on_shift_mousewheel(self, event):
        """Handle horizontal mouse wheel scrolling (Shift+MouseWheel)."""
        # Check if horizontal scrolling is actually possible
        if self._direction in ('horizontal', 'both'):
            try:
                first, last = self.canvas.xview()
                # If first=0.0 and last=1.0, all content is visible, no need to scroll
                if first <= 0.0 and last >= 1.0:
                    return  # Content fits, don't scroll
            except:
                pass  # If we can't check, allow scrolling

        # Show scrollbar temporarily in on-scroll mode
        if self._show_scrollbar == 'on-scroll':
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
            delta = -10
        elif event.num == 5:
            delta = 10

        # Scroll horizontally
        if self._direction in ('horizontal', 'both') and delta != 0:
            self.canvas.xview_scroll(delta, 'units')

        # Don't return 'break' - allow event to propagate if needed

    def _add_scroll_binding(self, widget):
        """Recursively add scroll bind tag to widget and all descendants."""
        try:
            # Get current bindtags
            tags = list(widget.bindtags())

            # Add our scroll tag if not already present
            if self._scroll_tag not in tags:
                # Insert after the widget name but before the class
                # Typical order: (widget_name, class, toplevel, 'all')
                # We want: (widget_name, scroll_tag, class, toplevel, 'all')
                if len(tags) >= 2:
                    tags.insert(1, self._scroll_tag)
                else:
                    tags.append(self._scroll_tag)
                widget.bindtags(tuple(tags))
        except:
            # Some widgets may not support bindtags
            pass

        # Recurse into all children
        for child in widget.winfo_children():
            self._add_scroll_binding(child)

    def _del_scroll_binding(self, widget):
        """Recursively remove scroll bind tag from widget and all descendants."""
        try:
            tags = list(widget.bindtags())
            if self._scroll_tag in tags:
                tags.remove(self._scroll_tag)
                widget.bindtags(tuple(tags))
        except:
            pass

        # Recurse into all children
        for child in widget.winfo_children():
            self._del_scroll_binding(child)

    def enable_scrolling(self):
        """Enable mouse wheel scrolling on canvas and all child widgets."""
        if not self._scrolling_enabled:
            # Add binding to canvas for exposed areas
            self._add_scroll_binding(self.canvas)

            # Add binding to child widget if it exists
            if self._child_widget:
                self._add_scroll_binding(self._child_widget)

            self._scrolling_enabled = True

    def disable_scrolling(self):
        """Disable mouse wheel scrolling on canvas and all child widgets."""
        if self._scrolling_enabled:
            # Remove binding from canvas
            self._del_scroll_binding(self.canvas)

            # Remove binding from child widget if it exists
            if self._child_widget:
                self._del_scroll_binding(self._child_widget)

            self._scrolling_enabled = False

    def add(self, widget: Widget = None, **kwargs: Any) -> Widget:
        """Add a widget to the scrollable area, or create and return a Frame.

        Args:
            widget (Widget | None): The widget to add. If None, creates a Frame.
            **kwargs: Additional arguments passed to canvas.create_window().

        Returns:
            Widget: The content widget (passed or created).

        Raises:
            ValueError: If the ScrollView already contains a widget and a new one is provided.
        """
        # If content exists and no widget passed, return existing (idempotent)
        if self._child_widget is not None:
            if widget is not None:
                raise ValueError("ScrollView already contains a widget. Use remove() first.")
            return self._child_widget

        # Create frame if no widget provided
        if widget is None:
            widget = Frame(self.canvas)

        self._child_widget = widget

        # Default create_window options
        window_kwargs = {'anchor': 'nw', 'window': widget}
        window_kwargs.update(kwargs)

        # Create window in canvas
        self._window_id = self.canvas.create_window(0, 0, **window_kwargs)

        # Keep scrollbars above the canvas/content
        self.vertical_scrollbar.lift()
        self.horizontal_scrollbar.lift()

        # Bind configure event to update scroll region
        widget.bind('<Configure>', self._on_frame_configure)
        self._update_scrollbar_visibility()

        # Bind configure event to update scroll region
        widget.bind('<Configure>', self._on_frame_configure)

        # Enable scrolling based on mode
        if self._show_scrollbar in ('always', 'never', 'on-scroll'):
            # Always enable scrolling for these modes
            self.enable_scrolling()
        # For 'on-hover' mode, scrolling is enabled on enter

        # Initial scroll region update
        self.canvas.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))

        return widget

    def remove(self) -> Optional[Widget]:
        """Remove the current widget from the scrollable area.

        Returns:
            The removed widget, or None if no widget was present.
        """
        if self._child_widget is None:
            return None

        widget = self._child_widget

        # Disable scrolling
        self.disable_scrolling()

        # Unbind events
        widget.unbind('<Configure>')

        # Delete canvas window
        if self._window_id:
            self.canvas.delete(self._window_id)
            self._window_id = None

        self._child_widget = None
        self._scrolling_enabled = False

        return widget

    def get_child(self) -> Optional[Widget]:
        """Get the current child widget.

        Returns:
            The child widget, or None if no widget is present.
        """
        return self._child_widget

    def refresh_bindings(self):
        """Refresh mouse wheel bindings for all widgets.

        Call this after dynamically adding many widgets at once to ensure
        mouse wheel scrolling works on all new widgets.
        """
        if self._child_widget and self._scrolling_enabled:
            # Re-enable to refresh bindings
            self.disable_scrolling()
            self.enable_scrolling()

    def yview(self, *args):
        """Query or command vertical view position."""
        return self.canvas.yview(*args)

    def xview(self, *args):
        """Query or command horizontal view position."""
        return self.canvas.xview(*args)

    def yview_moveto(self, fraction: float):
        """Scroll to a specific vertical position.

        Args:
            fraction: Position from 0.0 (top) to 1.0 (bottom).
        """
        self.canvas.yview_moveto(fraction)

    def xview_moveto(self, fraction: float):
        """Scroll to a specific horizontal position.

        Args:
            fraction: Position from 0.0 (left) to 1.0 (right).
        """
        self.canvas.xview_moveto(fraction)

    def destroy(self):
        """Clean up resources and destroy the widget."""
        # Cancel any pending timer
        if self._hide_timer:
            self.after_cancel(self._hide_timer)
            self._hide_timer = None

        # Remove scroll bindings from child widget
        if self._child_widget:
            self.disable_scrolling()

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

