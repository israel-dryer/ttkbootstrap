from tkinter import Misc
from tkinter.ttk import Checkbutton as ttkCheckbutton

from ttkbootstrap.ttk_types import StyleColor as Color, CheckbuttonOptions as CbOpts
from ttkbootstrap.styledwidget import StyledWidgetMixin

try:
    from typing import Unpack
except ImportError:
    from typing_extensions import Unpack


class Checkbutton(StyledWidgetMixin, ttkCheckbutton):
    """
    A themed checkbutton widget with support for dynamic color styling.

    This widget extends the standard `ttk.Checkbutton` by allowing the `color`
    parameter to determine the visual appearance using a themed styling system.
    The `color` defines the highlight color used when the checkbutton is active
    or selected.

    Functionally, it behaves identically to `ttk.Checkbutton`, supporting the
    same variable bindings, command callbacks, and tristate logic, while enabling
     a consistent appearance across themed applications.

    Example:
        Checkbutton(root, text="Enable feature", color="info", variable=var)

    Parameters:
        master (Misc, optional): The parent container widget.
        color (Color, optional): The color theme (e.g., "info", "warning").
        **kwargs (CbOpts): Additional options accepted by `ttk.Checkbutton`.
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
