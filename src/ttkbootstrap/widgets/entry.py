from tkinter import Misc
from tkinter.ttk import Entry as ttkEntry

from ttkbootstrap.typing import StyleColor as Color
from ttkbootstrap.typing import EntryOptions as EntryOpts
from ttkbootstrap.styledwidget import StyledWidgetMixin

try:
    from typing import Unpack
except ImportError:
    from typing_extensions import Unpack


class Entry(StyledWidgetMixin, ttkEntry):
    """
    A styled ttkbootstrap-compatible Entry widget that supports a `color`
    parameter for dynamic style generation.

    This widget wraps tkinter.ttk.Entry and applies ttkbootstrap styles
    based on the specified `color`.

    Example:
        Entry(root, textvariable=myvar, color="info")
    """

    def __init__(
        self,
        master: Misc | None = None,
        color: Color = None,
        **kwargs: Unpack[EntryOpts],
    ):
        """
        Initialize a styled Entry.

        Parameters:
            master (Misc | None): The parent container.
            color (Color, optional): A ttkbootstrap color token (e.g., "info").
            **kwargs (EntryOpts): Additional standard ttk.Entry options.
        """
        self._color = color
        self._variant = None  # Entry does not support variants
        super().__init__(master, **kwargs)
        self._init_style(kwargs, color=color, variant="")
