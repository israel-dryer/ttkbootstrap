from tkinter import Misc
from ttkbootstrap.widgets.checkbutton import Checkbutton
from ttkbootstrap.ttk_types import StyleColor as Color, CheckbuttonOptions as CbOpts, ToolbuttonVariant

try:
    from typing import Unpack
except ImportError:
    from typing_extensions import Unpack, Literal


class ToolCheckbutton(Checkbutton):
    """A compact, themed checkbutton for use in toolbars.

    This widget behaves like a toggleable button styled for toolbar layouts.
    It extends `Checkbutton` with support for `color` and `variant` parameters,
    offering a customizable look for use cases such as formatting toggles,
    editor actions, or state indicators.

    Supported variants:
        - "default": Standard background button
        - "outline": Border-only button style

    Example:
        >>> from ttkbootstrap.widgets import ToolCheckbutton
        >>> btn = ToolCheckbutton(root, text="Bold", color="primary", variant="outline")
        >>> btn.pack()

    Args:
        master (Misc | None): The parent container widget.
        color (Color, optional): A ttkbootstrap color token (e.g., "primary", "info").
        variant (ToolbuttonVariant): Either "default" or "outline".
        **kwargs (CheckbuttonOptions): Additional options passed to `ttk.Checkbutton`.
    """

    def __init__(
        self,
        master: Misc | None = None,
        color: Color = None,
        variant: ToolbuttonVariant = "default",
        **kwargs: Unpack[CbOpts],
    ):
        """Initialize the ToolCheckbutton widget.

        Args:
            master (Misc | None): The parent container.
            color (Color, optional): Themed color to apply to the button.
            variant (ToolbuttonVariant): Visual style variant, "default" or "outline".
            **kwargs (CheckbuttonOptions): Additional configuration options.
        """
        self._color = color
        self._variant = variant

        variant += "-toolbutton"

        super().__init__(master, **kwargs)
        self._init_style(kwargs, color=color, variant=variant)
