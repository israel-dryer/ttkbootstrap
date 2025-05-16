from tkinter import Misc
from tkinter.ttk import Menubutton as ttkMenubutton

from ttkbootstrap.ttk_types import StyleColor as Color
from ttkbootstrap.ttk_types import MenubuttonOptions as MenuBtnOpts
from ttkbootstrap.styledwidget import StyledWidgetMixin

try:
    from typing import Unpack
except ImportError:
    from typing_extensions import Unpack


class Menubutton(StyledWidgetMixin, ttkMenubutton):
    """
    A themed Menubutton widget that displays a dropdown menu when clicked.

    Supports ttkbootstrap `color` theming for visual consistency in toolbars,
    headers, and action panels.

    Example:
        Menubutton(root, text="Options", color="primary")
    """

    def __init__(
        self,
        master: Misc | None = None,
        color: Color = None,
        **kwargs: Unpack[MenuBtnOpts],
    ):
        """
        Initialize a themed Menubutton.

        Parameters:
            master (Misc | None): The parent container.
            color (Color, optional): A ttkbootstrap color token.
            **kwargs (MenuBtnOpts): Additional standard ttk.Menubutton options.
        """
        self._color = color
        self._variant = None  # Menubutton does not support variants
        super().__init__(master, **kwargs)
        self._init_style(kwargs, color=color, variant="")
