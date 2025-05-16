from tkinter import Misc
from tkinter.ttk import Checkbutton as ttkCheckbutton

from ttkbootstrap.typing import StyleColor as Color, CheckbuttonOptions as CbOpts
from ttkbootstrap.styledwidget import StyledWidgetMixin

try:
    from typing import Unpack
except ImportError:
    from typing_extensions import Unpack


class Checkbutton(StyledWidgetMixin, ttkCheckbutton):
    """
    A styled ttkbootstrap-compatible Checkbutton that supports a `color`
    parameter for dynamic style generation.

    This widget wraps tkinter.ttk.Checkbutton and applies ttkbootstrap styles
    based on the specified `color`.

    Unlike Button or Toolbutton, this does not support a `variant`.
    """

    def __init__(
        self,
        master: Misc = None,
        color: Color = None,
        **kwargs: Unpack[CbOpts],
    ):
        """
        Initialize a styled Checkbutton.

        Parameters:
            master (Misc, optional): The parent container.
            color (Color, optional): A ttkbootstrap color token (e.g., "info").
            **kwargs (CbOpts): Additional standard ttk.Checkbutton options.
        """
        self._color = color
        self._variant = None  # Explicitly no variant support
        super().__init__(master, **kwargs)
        self._init_style(kwargs, color=color, variant="")
