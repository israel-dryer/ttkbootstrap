from tkinter import Misc
from ttkbootstrap.widgets.radiobutton import Radiobutton
from ttkbootstrap.ttk_types import StyleColor as Color, RadiobuttonOptions as RadioOpts, ToolbuttonVariant

try:
    from typing import Unpack
except ImportError:
    from typing_extensions import Unpack


class ToolRadiobutton(Radiobutton):
    """A themed radiobutton styled for toolbar usage.

    This widget extends `Radiobutton` with styling to appear as a compact
    toolbar button. It supports the `color` and `variant` parameters for
    theme-based customization, and is suitable for grouped toggle controls
    such as text alignment or mode selection in toolbars.

    Supported variants:
        - "default": Standard filled button
        - "outline": Border-only toolbar style

    Example:
        >>> from ttkbootstrap.widgets import ToolRadiobutton
        >>> group = StringVar(value="left")
        >>> btn = ToolRadiobutton(root, text="Align Left", value="left", variable=group, color="secondary")
        >>> btn.pack()

    Args:
        master (Misc | None): The parent container widget.
        color (Color, optional): A ttkbootstrap color token (e.g., "primary", "secondary").
        variant (ToolbuttonVariant): "default" or "outline".
        **kwargs (RadiobuttonOptions): Additional keyword arguments passed to `ttk.Radiobutton`.
    """

    def __init__(
        self,
        master: Misc | None = None,
        color: Color = None,
        variant: ToolbuttonVariant = "default",
        **kwargs: Unpack[RadioOpts],
    ):
        """Initialize the ToolRadiobutton widget.

        Args:
            master (Misc | None): The parent container.
            color (Color, optional): A ttkbootstrap color token.
            variant (ToolbuttonVariant): The button style variant, "default" or "outline".
            **kwargs (RadiobuttonOptions): Additional options passed to `ttk.Radiobutton`.
        """
        self._color = color
        self._variant = variant

        variant += "-toolbutton"

        super().__init__(master, **kwargs)
        self._init_style(kwargs, color=color, variant=variant)
