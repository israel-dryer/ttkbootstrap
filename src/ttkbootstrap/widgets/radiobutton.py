from tkinter import Misc
from tkinter.ttk import Radiobutton as ttkRadiobutton

from ttkbootstrap.typing import StyleColor as Color
from ttkbootstrap.typing import RadiobuttonOptions as RadioOpts
from ttkbootstrap.styledwidget import StyledWidgetMixin

try:
    from typing import Unpack
except ImportError:
    from typing_extensions import Unpack


class Radiobutton(StyledWidgetMixin, ttkRadiobutton):
    """
    A styled ttkbootstrap-compatible Radiobutton that supports a `color`
    parameter for dynamic style generation.

    Example:
        Radiobutton(root, text="Choice A", value="a", variable=var, color="info")
    """

    def __init__(
        self,
        master: Misc | None = None,
        color: Color = None,
        **kwargs: Unpack[RadioOpts],
    ):
        """
        Initialize a styled Radiobutton.

        Parameters:
            master (Misc | None): The parent container.
            color (Color, optional): A ttkbootstrap color token (e.g., "info", "primary").
            **kwargs (RadioOpts): Additional standard ttk.Radiobutton options.
        """
        self._color = color
        self._variant = None  # Radiobuttons do not support variants
        super().__init__(master, **kwargs)
        self._init_style(kwargs, color=color, variant="")
