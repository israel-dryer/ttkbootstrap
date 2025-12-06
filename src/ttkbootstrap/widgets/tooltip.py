"""Tooltip popup widgets for ttkbootstrap.

This module provides a semi-transparent tooltip system that displays helpful
text when hovering over widgets. Tooltips automatically appear on mouse hover
and disappear when the mouse leaves the widget or on click.

Classes:
    ToolTip: Semi-transparent popup that shows text on hover

Features:
    - Automatic show/hide on mouse enter/leave events
    - Configurable delay before tooltip appears
    - Bootstrap styling support
    - Flexible positioning (follows mouse or anchored to widget)
    - Text wrapping and justification options
    - Optional image display with text

Example:
    ```python
    import ttkbootstrap as ttk
    from ttkbootstrap.constants import *
    from ttkbootstrap.tooltip import ToolTip

    app = ttk.Window()

    b1 = ttk.Button(app, text="default tooltip")
    b1.pack(side=LEFT, padx=20, pady=20)

    b2 = ttk.Button(app, text="styled tooltip")
    b2.pack(side=LEFT, padx=20, pady=20)

    # Default tooltip (follows mouse)
    ToolTip(b1, text="This is the default style")

    # Styled tooltip anchored to widget
    ToolTip(
        b2,
        text="This is dangerous",
        bootstyle=(DANGER, INVERSE),
        position="top right"
    )

    app.mainloop()
    ```
"""
from tkinter import Event, Misc
from typing import Any, Literal, Optional, Union

import ttkbootstrap as ttk
from ttkbootstrap import utility
from ttkbootstrap.constants import *


class ToolTip:
    """A semi-transparent tooltip popup window that shows text when the
    mouse is hovering over the widget and closes when the mouse is no
    longer hovering over the widget. Clicking a mouse button will also
    close the tooltip.

    ![](../assets/tooltip/tooltip.gif)

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
        """
        Parameters:

            widget (Widget):
                The tooltip window will position over this widget when
                hovering.

            text (str):
                The text to display in the tooltip window.

            padding (int):
                The padding between the text and the border of the tooltip (default=10).

            bootstyle (str):
                The style to apply to the tooltip label. You can use
                any of the standard ttkbootstrap label styles.

            wraplength (int):
                The width of the tooltip window in screenunits before the
                text is wrapped to the next line. By default, this will be
                a scaled factor of 300.

            position (str):
                If provided, will set the position of the tooltip relative to the widget.
                Valid options include combinations of "left", "right", "top", "bottom",
                and "center" separated by a space. For example: "top left" or "bottom right".
                If not provided, the tooltip will be offset from the mouse pointer.

            **kwargs (Dict):
                Other keyword arguments passed to the `Toplevel` window.
        """
        self.widget = widget
        self.text = text
        self.padding = padding
        self.justify = justify
        self.image = image
        self.bootstyle = bootstyle
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
        if "alpha" not in kwargs:
            kwargs["alpha"] = 0.95
        self.toplevel_kwargs = kwargs

        # event binding
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)
        self.widget.bind("<Motion>", self.move_tip)
        self.widget.bind("<ButtonPress>", self.leave)

    def enter(self, event: Optional[Event] = None) -> None:
        self.schedule()

    def leave(self, event: Optional[Event] = None) -> None:
        self.unschedule()
        self.hide_tip()

    def schedule(self) -> None:
        self.unschedule()
        self.id = self.widget.after(self.delay, self.show_tip)

    def unschedule(self) -> None:
        _id = self.id
        self.id = None
        if _id:
            self.widget.after_cancel(_id)

    def show_tip(self, *_: Any) -> None:
        """Create and show the tooltip window"""
        if self.toplevel:
            return

        # Create the tooltip window at a temporary position
        self.toplevel = ttk.window.Toplevel(position=(0, 0), **self.toplevel_kwargs)

        self.toplevel.withdraw()
        lbl = ttk.Label(
            master=self.toplevel,
            text=self.text,
            image=self.image,
            compound='bottom',
            justify=self.justify,
            wraplength=self.wraplength,
            padding=self.padding,
        )
        lbl.pack(fill=BOTH, expand=YES)

        if self.bootstyle:
            lbl.configure(bootstyle=self.bootstyle)
        else:
            lbl.configure(style="tooltip.TLabel")

        # Wait until size is known, then position
        self.toplevel.update_idletasks()

        if self.position:
            x, y = self._calculate_position()
        else:
            x = self.widget.winfo_pointerx() + 25
            y = self.widget.winfo_pointery() + 10

        self.toplevel.geometry(f"+{x}+{y}")
        self.toplevel.deiconify()

    def move_tip(self, *_: Any) -> None:
        """Move the tooltip window"""
        if self.toplevel:
            if self.position:
                x, y = self._calculate_position()
            else:
                x = self.widget.winfo_pointerx() + 25
                y = self.widget.winfo_pointery() + 10
            self.toplevel.geometry(f"+{x}+{y}")

    def hide_tip(self, *_: Any) -> None:
        """Destroy the tooltip window."""
        if self.toplevel:
            self.toplevel.destroy()
            self.toplevel = None

    def _calculate_position(self) -> tuple[int, int]:
        w = self.widget
        tip_w = 200  # fallback size
        tip_h = 50

        try:
            self.toplevel.update_idletasks()
            tip_w = self.toplevel.winfo_width()
            tip_h = self.toplevel.winfo_height()
        except:
            pass

        widget_x = w.winfo_rootx()
        widget_y = w.winfo_rooty()
        widget_w = w.winfo_width()
        widget_h = w.winfo_height()

        horiz = "center"
        vert = "bottom"
        tokens = self.position.split()

        for token in tokens:
            if token in ("top", "bottom", "center"):
                vert = token
            if token in ("left", "right", "center"):
                horiz = token

        # Vertical positioning
        if vert == "top":
            y = widget_y - tip_h - 4
        elif vert == "bottom":
            y = widget_y + widget_h + 4
        else:  # center
            y = widget_y + (widget_h // 2) - (tip_h // 2)

        # Horizontal positioning
        if horiz == "left":
            x = widget_x - tip_w - 4
        elif horiz == "right":
            x = widget_x + widget_w + 4
        else:  # center
            x = widget_x + (widget_w // 2) - (tip_w // 2)

        return x, y


if __name__ == "__main__":
    app = ttk.Window()

    b1 = ttk.Button(app, text="default tooltip")
    b1.pack(side=LEFT, padx=20, pady=20, fill=X, expand=YES)

    b2 = ttk.Button(app, text="styled tooltip")
    b2.pack(side=LEFT, padx=20, pady=20, fill=X, expand=YES)

    ToolTip(
        b1,
        text="Following the mouse pointer.",
    )
    ToolTip(
        b2,
        text="Anchored to the top right corner.",
        bootstyle="danger-inverse",
        position="top right"
    )

    app.mainloop()
