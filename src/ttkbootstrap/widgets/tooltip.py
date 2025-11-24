import tkinter as tk
from tkinter import Misc
from typing import Any, Literal, Optional, Union

import ttkbootstrap as ttk
from ttkbootstrap import utility
from ttkbootstrap.constants import *


class ToolTip:
    """A semi-transparent tooltip popup that displays on hover.

    This class creates a tooltip window that appears when the mouse hovers over
    a widget and automatically closes when the mouse leaves or on click. The tooltip
    supports Bootstrap styling, custom positioning, text wrapping, and optional images.

    Examples:
        ```python
        import ttkbootstrap as ttk
        from ttkbootstrap.constants import *
        from ttkbootstrap.tooltip import ToolTip

        app = ttk.Window()
        b1 = ttk.Button(app, text="default tooltip")
        b1.pack()
        b2 = ttk.Button(app, text="styled tooltip")
        b2.pack()

        # default tooltip
        ToolTip(b1, text="This is the default style")

        # styled tooltip
        ToolTip(b2, text="This is dangerous", bootstyle=(DANGER, INVERSE))

        app.mainloop()
        ```
    """

    # Position offset from mouse pointer
    _MOUSE_OFFSET_X = 25
    _MOUSE_OFFSET_Y = 10

    # Spacing between tooltip and widget when anchored
    _WIDGET_SPACING = 1

    # Fallback dimensions for tooltip sizing
    _FALLBACK_WIDTH = 200
    _FALLBACK_HEIGHT = 50

    def __init__(
            self,
            widget: Misc,
            text: str = "widget info",
            padding: int = 10,
            justify: Literal["left", "center", "right"] = "left",
            bootstyle: Optional[Union[str, tuple[str, ...]]] = None,
            wraplength: Optional[int] = None,
            delay: int = 250,  # milliseconds
            image: Any = None,
            position: Optional[str] = None,
            **kwargs: Any,
    ) -> None:
        """Initialize a ToolTip instance for the specified widget.

        Creates a tooltip that appears after a configurable delay when the mouse
        enters the widget and disappears when the mouse leaves or on button press.
        The tooltip can either follow the mouse pointer or be anchored to a specific
        position relative to the widget.

        The tooltip window is created with semi-transparency (alpha=0.95 by default)
        and uses the Bootstrap styling system for consistent theming. Text automatically
        wraps based on the specified wraplength, and optional images can be displayed
        alongside the text.

        Args:
            widget: The tkinter widget to attach this tooltip to. The tooltip will
                appear when hovering over this widget.
            text: The text content to display in the tooltip. Supports multi-line
                text that will wrap according to wraplength. Defaults to "widget info".
            padding: The internal padding in pixels between the tooltip text and the
                tooltip border. Defaults to 10.
            justify: Text alignment within the tooltip. Valid options are "left",
                "center", or "right". Defaults to "left".
            bootstyle: Bootstrap style(s) to apply to the tooltip frame. Can be a
                single style string or tuple of styles (e.g., "danger" or
                (DANGER, INVERSE)). If None, uses default background styling.
            wraplength: Maximum width in screen units before text wraps to a new line.
                If None, defaults to a scaled value of 300 based on the widget's display.
            delay: Time in milliseconds to wait before showing the tooltip after mouse
                enters the widget. Defaults to 250ms.
            image: Optional image to display in the tooltip below the text. Should be
                a PhotoImage or compatible tkinter image object.
            position: Anchor position relative to the widget. Accepts space-separated
                combinations of "top", "bottom", "left", "right", and "center"
                (e.g., "top left", "bottom right", "center"). If None, the tooltip
                follows the mouse pointer with a small offset.
            **kwargs: Additional keyword arguments passed to the Toplevel window
                constructor. Common options include alpha, topmost, etc. The arguments
                overrideredirect, master, and windowtype are set automatically.

        Raises:
            ValueError: If position string contains invalid tokens.
        """
        # Validate position before any initialization
        if position:
            position_lower = position.lower()
            valid_tokens = {"top", "bottom", "left", "right", "center"}
            if not all(part in valid_tokens for part in position_lower.split()):
                raise ValueError(f"Invalid position string: '{position}'")
            validated_position = position_lower
        else:
            validated_position = None

        # Configuration
        self._widget = widget
        self._text = text
        self._padding = padding
        self._justify = justify
        self._bootstyle = bootstyle
        self._wraplength = wraplength if wraplength is not None else utility.scale_size(self._widget, 300)
        self._delay = delay
        self._image = image
        self._position = validated_position

        self._toplevel = None
        self._id = None

        # Set keyword arguments (create copy to avoid mutating caller's dict)
        self.toplevel_kwargs = kwargs.copy()
        self.toplevel_kwargs["overrideredirect"] = True
        self.toplevel_kwargs["master"] = self._widget
        self.toplevel_kwargs["windowtype"] = "tooltip"
        if "alpha" not in self.toplevel_kwargs:
            self.toplevel_kwargs["alpha"] = 0.95

        # event binding
        self._widget.bind("<Enter>", self._on_enter)
        self._widget.bind("<Leave>", self._on_leave)
        self._widget.bind("<Motion>", self._move_tip)
        self._widget.bind("<ButtonPress>", self._on_leave)

    def destroy(self) -> None:
        """Cleanup tooltip resources and unbind all event handlers.

        This method should be called when the tooltip is no longer needed to prevent
        memory leaks. It cancels any pending tooltip display, hides any visible tooltip,
        and removes all event bindings from the widget.
        """
        self._unschedule()
        self._hide_tip()
        self._widget.unbind("<Enter>")
        self._widget.unbind("<Leave>")
        self._widget.unbind("<Motion>")
        self._widget.unbind("<ButtonPress>")

    def _on_enter(self, _) -> None:
        """Handle mouse enter event by scheduling tooltip display."""
        self._schedule()

    def _on_leave(self, _) -> None:
        """Handle mouse leave event by canceling and hiding tooltip."""
        self._unschedule()
        self._hide_tip()

    def _schedule(self) -> None:
        """Schedule the tooltip to appear after the configured delay."""
        self._unschedule()
        self._id = self._widget.after(self._delay, self._show_tip)

    def _unschedule(self) -> None:
        """Cancel any pending scheduled tooltip display."""
        _id = self._id
        self._id = None
        if _id:
            self._widget.after_cancel(_id)

    def _show_tip(self, *_: Any) -> None:
        """Create and display the tooltip window at the appropriate position."""
        if self._toplevel:
            return

        # Check if widget still exists before showing tooltip
        try:
            if not self._widget.winfo_exists():
                return
        except tk.TclError:
            return

        # Create the tooltip window at a temporary position
        self._toplevel = ttk.window.Toplevel(position=(0, 0), **self.toplevel_kwargs)
        bootstyle = 'background[+1]-tooltip' if self._bootstyle is None else f'{self._bootstyle}-tooltip'
        frame = ttk.Frame(
            self._toplevel,
            bootstyle=bootstyle,
            padding=self._padding
        )
        frame.pack(fill=BOTH, expand=YES)

        lbl = ttk.Label(
            master=frame,
            text=self._text,
            image=self._image,
            compound='bottom',
            justify=self._justify,
            font="caption",
            wraplength=self._wraplength,
        )
        lbl.pack(fill=BOTH, expand=YES)

        # Wait until size is known, then position
        self._toplevel.update_idletasks()

        if self._position:
            x, y = self._calculate_position()
        else:
            x, y = self._get_mouse_position()

        self._toplevel.geometry(f"+{x}+{y}")

    def _move_tip(self, *_: Any) -> None:
        """Update the tooltip position based on mouse or anchor position."""
        if self._toplevel:
            if self._position:
                x, y = self._calculate_position()
            else:
                x, y = self._get_mouse_position()
            self._toplevel.geometry(f"+{x}+{y}")

    def _hide_tip(self, *_: Any) -> None:
        """Hide and destroy the tooltip window."""
        if self._toplevel:
            self._toplevel.destroy()
            self._toplevel = None

    def _get_mouse_position(self) -> tuple[int, int]:
        """Get tooltip position offset from the current mouse pointer.

        Returns:
            Tuple of (x, y) screen coordinates for the tooltip.
        """
        return (
            self._widget.winfo_pointerx() + self._MOUSE_OFFSET_X,
            self._widget.winfo_pointery() + self._MOUSE_OFFSET_Y
        )

    def _calculate_position(self) -> tuple[int, int]:
        """Calculate tooltip x, y coordinates based on position setting.

        Returns:
            Tuple of (x, y) screen coordinates for the tooltip.
        """
        w = self._widget
        tip_w = self._FALLBACK_WIDTH
        tip_h = self._FALLBACK_HEIGHT

        try:
            self._toplevel.update_idletasks()
            tip_w = self._toplevel.winfo_width()
            tip_h = self._toplevel.winfo_height()
        except (tk.TclError, AttributeError):
            # Fallback to defaults if tooltip sizing fails
            pass

        widget_x = w.winfo_rootx()
        widget_y = w.winfo_rooty()
        widget_w = w.winfo_width()
        widget_h = w.winfo_height()

        horiz = "center"
        vert = "bottom"
        tokens = self._position.split()

        for token in tokens:
            if token in ("top", "bottom", "center"):
                vert = token
            if token in ("left", "right", "center"):
                horiz = token

        # Vertical positioning
        if vert == "top":
            y = widget_y - tip_h - self._WIDGET_SPACING
        elif vert == "bottom":
            y = widget_y + widget_h + self._WIDGET_SPACING
        else:  # center
            y = widget_y + (widget_h // 2) - (tip_h // 2)

        # Horizontal positioning
        if horiz == "left":
            x = widget_x - tip_w - self._WIDGET_SPACING
        elif horiz == "right":
            x = widget_x + widget_w + self._WIDGET_SPACING
        else:  # center
            x = widget_x + (widget_w // 2) - (tip_w // 2)

        return x, y


if __name__ == "__main__":
    app = ttk.Window()


    def change_theme():
        from ttkbootstrap.style.style import use_style
        style = use_style()
        if style.theme_use() == 'dark':
            style.theme_use('light')
        else:
            style.theme_use("dark")


    b1 = ttk.Button(app, text="default tooltip", command=change_theme)
    b1.pack(side=LEFT, padx=20, pady=20, fill=X, expand=YES)

    b2 = ttk.Button(app, text="styled tooltip")
    b2.pack(side=LEFT, padx=20, pady=20, fill=X, expand=YES)

    ToolTip(b1, text="Following the mouse pointer.")
    ToolTip(
        b2,
        text="Anchored to the top right corner.",
        bootstyle="danger",
        position="top right"
    )

    app.mainloop()
