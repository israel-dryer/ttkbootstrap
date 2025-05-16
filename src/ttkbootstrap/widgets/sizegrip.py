from tkinter import Misc
from tkinter.ttk import Sizegrip as ttkSizegrip

from ttkbootstrap.typing import StyleColor as Color
from ttkbootstrap.typing import SizegripOptions as GripOpts
from ttkbootstrap.styledwidget import StyledWidgetMixin

try:
    from typing import Unpack
except ImportError:
    from typing_extensions import Unpack


class Sizegrip(StyledWidgetMixin, ttkSizegrip):
    """
    A themed resize handle typically placed in the bottom-right corner
    of a window or resizable frame.

    This widget provides a visual cue and mouse control for resizing
    its parent container. It supports theming through the `color` parameter.

    Example:
        Sizegrip(root, color="muted").pack(side="right", anchor="se")
    """

    def __init__(
        self,
        master: Misc | None = None,
        color: Color = None,
        **kwargs: Unpack[GripOpts],
    ):
        """
        Initialize a themed Sizegrip.

        Parameters:
            master (Misc | None): The parent container.
            color (Color, optional): A themed color token (e.g., "muted", "info").
            **kwargs (GripOpts): Additional ttk.Sizegrip options.
        """
        self._color = color
        self._variant = None
        super().__init__(master, **kwargs)
        self._init_style(kwargs, color=color, variant="")
