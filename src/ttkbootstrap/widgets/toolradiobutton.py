from tkinter import Misc
from ttkbootstrap.widgets.radiobutton import Radiobutton
from ttkbootstrap.ttk_types import StyleColor as Color, RadiobuttonOptions as RadioOpts, ToolbuttonVariant

try:
    from typing import Unpack
except ImportError:
    from typing_extensions import Unpack


class ToolRadiobutton(Radiobutton):
    """
    A themed toolbar radiobutton that functions as a toggleable tool button.

    This widget behaves like a standard `Radiobutton` but is styled for use
    in a compact toolbar layout. It supports both `color` and `variant`
    parameters for visual customization, making it ideal for grouped toolbar
    controls such as alignment, mode selection, or view toggles.

    Example:
        ToolRadiobutton(root, text="Align Left", value="left", variable=group, color="secondary")

    Parameters:
        master (Misc | None): The parent container widget.
        color (Color): The button color theme (e.g., "secondary", "info").
        variant (str): The visual style variant (e.g., "outline", "solid").
        **kwargs (RadiobuttonOpts): Additional options accepted by `ttk.Radiobutton`.
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
