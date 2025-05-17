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
    """A themed Menubutton widget that displays a dropdown menu when clicked.

    This widget extends the standard `ttk.Menubutton` and supports themed coloring
    through the `color` option, allowing it to visually integrate with the
    application's style. It is commonly used in toolbars, navigation menus, or
    grouped option sets.

    Example:
        >>> from ttkbootstrap.widgets import Menubutton
        >>> btn = Menubutton(root, text="Options", color="primary")
        >>> btn.pack()

    Args:
        master (Misc | None): The parent container widget.
        color (Color, optional): A ttkbootstrap color token (e.g., "primary", "info").
        **kwargs (MenuBtnOpts): Additional options accepted by `ttk.Menubutton`.
    """

    def __init__(
        self,
        master: Misc | None = None,
        color: Color = None,
        **kwargs: Unpack[MenuBtnOpts],
    ):
        """Initialize the themed Menubutton widget.

        Args:
            master (Misc | None): The parent widget.
            color (Color, optional): The themed color name.
            **kwargs (MenuBtnOpts): Additional keyword arguments for `ttk.Menubutton`.
        """
        self._color = color
        self._variant = None  # Menubutton does not support variants
        super().__init__(master, **kwargs)
        self._init_style(kwargs, color=color, variant="")
