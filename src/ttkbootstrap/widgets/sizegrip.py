from tkinter import Misc
from tkinter.ttk import Sizegrip as ttkSizegrip

from ttkbootstrap.ttk_types import StyleColor as Color
from ttkbootstrap.ttk_types import SizegripOptions as GripOpts
from ttkbootstrap.styledwidget import StyledWidgetMixin

try:
    from typing import Unpack
except ImportError:
    from typing_extensions import Unpack


class Sizegrip(StyledWidgetMixin, ttkSizegrip):
    """A themed resize handle for the bottom-right corner of a window.

    This widget behaves like a standard `ttk.Sizegrip`, but allows for
    color theming via the `color` parameter to match the overall UI palette.

    The sizegrip provides a visual cue for resizability and allows the
    user to drag and resize the toplevel window or container that holds it.

    Example:
        >>> from ttkbootstrap.widgets import Sizegrip
        >>> Sizegrip(root, color="muted").pack(side="right", anchor="se")

    Args:
        master (Misc | None): The parent container widget.
        color (Color, optional): A ttkbootstrap color token (e.g., "muted", "info").
        **kwargs (SizegripOptions): Additional keyword arguments for `ttk.Sizegrip`.
    """

    def __init__(
        self,
        master: Misc | None = None,
        color: Color = None,
        **kwargs: Unpack[GripOpts],
    ):
        """Initialize the themed Sizegrip widget.

        Args:
            master (Misc | None): The parent container.
            color (Color, optional): A themed style color name.
            **kwargs (SizegripOptions): Additional options accepted by `ttk.Sizegrip`.
        """
        self._color = color
        self._variant = None
        super().__init__(master, **kwargs)
        self._init_style(kwargs, color=color, variant="")
