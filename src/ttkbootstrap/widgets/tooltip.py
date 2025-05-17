from tkinter import Misc
from typing import Literal
from ttkbootstrap.ttk_types import StyleColor
from ttkbootstrap.widgets.label import Label
from ttkbootstrap.window import Toplevel
from ttkbootstrap import utility


class ToolTip:
    """
    A themed tooltip popup that appears on mouse hover.

    This widget creates a floating, styled `Toplevel` window that shows
    informative text beside a widget or pointer. It supports color theming,
    configurable position, display delay, optional image/icon, and text
    wrapping.

    Example:
        ToolTip(widget, text="Tooltip text", color="info", position="top right")
    """

    def __init__(
        self,
        widget: Misc,
        text: str = "widget info",
        padding: int = 10,
        justify: Literal["left", "center", "right"] = "left",
        color: StyleColor = "default",
        wraplength: int | None = None,
        delay: int = 250,
        image=None,
        position: str | None = None,
        **kwargs,
    ):
        """
        Initialize a themed ToolTip.

        Parameters:
            widget (Misc): The widget to attach the tooltip to.
            text (str): The text displayed in the tooltip.
            padding (int): Padding around the text label.
            justify (str): Text alignment ("left", "center", or "right").
            color (StyleColor): The background/foreground theme color.
            wraplength (int): Maximum width before wrapping text.
            delay (int): Delay in milliseconds before showing the tooltip.
            image (Any): Optional image or icon to show above the text.
            position (str): Tooltip anchor position relative to the widget
                (e.g., "top left", "bottom right"). If omitted, follows mouse.
            **kwargs: Additional options for the `Toplevel` window.
        """
        self.widget = widget
        self.text = text
        self.padding = padding
        self.justify = justify
        self.image = image
        self.color = color
        self.variant = "tooltip"
        self.wraplength = wraplength or utility.scale_size(self.widget, 300)
        self.toplevel = None
        self.delay = delay
        self.position = position.lower() if position else None
        self.id = None

        if self.position:
            valid_tokens = {"top", "bottom", "left", "right", "center"}
            if not all(part in valid_tokens for part in self.position.split()):
                raise ValueError(f"Invalid position string: '{self.position}'")

        # set keyword arguments
        kwargs["overrideredirect"] = True
        kwargs["master"] = self.widget
        kwargs["windowtype"] = "tooltip"
        kwargs.setdefault("alpha", 0.95)
        self.toplevel_kwargs = kwargs

        # event binding
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)
        self.widget.bind("<Motion>", self.move_tip)
        self.widget.bind("<ButtonPress>", self.leave)

    def enter(self, _):
        """Mouse enters the widget; schedule tooltip display."""
        self.schedule()

    def leave(self, _):
        """Mouse leaves the widget; hide and cancel tooltip."""
        self.unschedule()
        self.hide_tip()

    def schedule(self):
        """Schedule tooltip display after a delay."""
        self.unschedule()
        self.id = self.widget.after(self.delay, self.show_tip)

    def unschedule(self):
        """Cancel any scheduled tooltip display."""
        if self.id:
            self.widget.after_cancel(self.id)
            self.id = None

    def show_tip(self, *_):
        """Create and show the tooltip popup."""
        if self.toplevel:
            return

        self.toplevel = Toplevel(position=(0, 0), **self.toplevel_kwargs)

        label = Label(
            self.toplevel,
            color=self.color,
            variant=self.variant,
            text=self.text,
            image=self.image,
            compound="bottom",
            justify=self.justify,
            wraplength=self.wraplength,
            padding=self.padding,
        )
        label.pack(fill="both", expand=1)

        self.toplevel.update_idletasks()

        if self.position:
            x, y = self._calculate_position()
        else:
            x = self.widget.winfo_pointerx() + 25
            y = self.widget.winfo_pointery() + 10

        self.toplevel.geometry(f"+{x}+{y}")

    def move_tip(self, *_):
        """Reposition the tooltip to follow mouse or stay anchored."""
        if self.toplevel:
            if self.position:
                x, y = self._calculate_position()
            else:
                x = self.widget.winfo_pointerx() + 25
                y = self.widget.winfo_pointery() + 10
            self.toplevel.geometry(f"+{x}+{y}")

    def hide_tip(self, *_):
        """Destroy the tooltip window."""
        if self.toplevel:
            self.toplevel.destroy()
            self.toplevel = None

    def _calculate_position(self):
        """Compute screen coordinates from widget and position string."""
        w = self.widget
        tip_w, tip_h = 200, 50

        try:
            self.toplevel.update_idletasks()
            tip_w = self.toplevel.winfo_width()
            tip_h = self.toplevel.winfo_height()
        except:
            pass

        x = w.winfo_rootx()
        y = w.winfo_rooty()
        width = w.winfo_width()
        height = w.winfo_height()

        tokens = self.position.split()

        # Default values
        horiz = "center"
        vert = "bottom"

        for token in tokens:
            if token in ("top", "bottom"):
                vert = token
            elif token in ("left", "right"):
                horiz = token
            elif token == "center":
                # only set to center if not already overridden
                if vert not in ("top", "bottom"):
                    vert = "center"
                if horiz not in ("left", "right"):
                    horiz = "center"

        if vert == "top":
            y = y - tip_h - 4
        elif vert == "bottom":
            y = y + height + 4
        else:
            y = y + (height // 2) - (tip_h // 2)

        if horiz == "left":
            x = x - tip_w - 4
        elif horiz == "right":
            x = x + width + 4
        else:
            x = x + (width // 2) - (tip_w // 2)

        return x, y
