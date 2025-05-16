from tkinter import Misc
from ttkbootstrap.widgets.radiobutton import Radiobutton
from ttkbootstrap.typing import StyleColor as Color, RadiobuttonOptions as RadioOpts, ToolbuttonVariant

try:
    from typing import Unpack
except ImportError:
    from typing_extensions import Unpack


class ToolRadiobutton(Radiobutton):
    """
    A styled toggleable toolbar button that behaves like a radiobutton.
    Supports `color` and `variant` styling.

    Example:
        ToolRadiobutton(root, text="Align Left", value="left", variable=group, color="secondary")
    """

    def __init__(
        self,
        master: Misc | None = None,
        color: Color = None,
        variant: ToolbuttonVariant = "default",
        **kwargs: Unpack[RadioOpts],
    ):
        """
        Initialize a ToolRadiobutton.

        Parameters:
            master (Misc | None): The parent container.
            color (Color, optional): A ttkbootstrap color token.
            variant (ToolbuttonVariant): "default" or "outline".
            **kwargs (RadioOpts): Additional standard ttk.Radiobutton options.
        """
        self._color = color
        self._variant = variant

        variant += "-toolbutton"

        super().__init__(master, **kwargs)
        self._init_style(kwargs, color=color, variant=variant)
