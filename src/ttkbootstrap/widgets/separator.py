from tkinter import Misc
from tkinter.ttk import Separator as ttkSeparator

from ttkbootstrap.ttk_types import StyleColor as Color
from ttkbootstrap.ttk_types import SeparatorOptions as SepOpts
from ttkbootstrap.styledwidget import StyledWidgetMixin

try:
    from typing import Unpack
except ImportError:
    from typing_extensions import Unpack


class Separator(StyledWidgetMixin, ttkSeparator):
    """
    A horizontal or vertical rule used to visually separate groups of widgets.

    This themed Separator supports a `color` parameter for customizing its
    appearance to match the surrounding interface.

    Example:
        Separator(root, orient="horizontal", color="secondary")
    """

    def __init__(
        self,
        master: Misc | None = None,
        color: Color = None,
        **kwargs: Unpack[SepOpts],
    ):
        """
        Initialize a themed Separator.

        Parameters:
            master (Misc | None): The parent container.
            color (Color, optional): A themed color token (e.g., "secondary", "info").
            **kwargs (SepOpts): Additional standard ttk.Separator options.
        """
        self._color = color
        self._variant = None  # No variant support
        super().__init__(master, **kwargs)
        self._init_style(kwargs, color=color, variant="")
