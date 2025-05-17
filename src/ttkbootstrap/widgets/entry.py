from tkinter import Misc
from tkinter.ttk import Entry as ttkEntry

from ttkbootstrap.ttk_types import StyleColor as Color
from ttkbootstrap.ttk_types import EntryOptions as EntryOpts
from ttkbootstrap.styledwidget import StyledWidgetMixin

try:
    from typing import Unpack
except ImportError:
    from typing_extensions import Unpack


class Entry(StyledWidgetMixin, ttkEntry):
    """A themed entry widget with support for dynamic color styling.

    This class extends the standard ttk.Entry widget by applying a
    ttkbootstrap-compatible style based on the specified color. This affects
    the focus ring, border, and overall visual theming.

    It retains all functionality of the standard entry widget, including text
    input, validation, and variable binding, while offering an enhanced appearance.

    Example:
        >>> entry = Entry(root, textvariable=myvar, color="info")

    Args:
        master (Misc | None): The parent container widget.
        color (Color, optional): The style color theme (e.g., "info", "primary").
        **kwargs (EntryOpts): Additional keyword arguments accepted by ttk.Entry.
    """

    def __init__(
        self,
        master: Misc | None = None,
        color: Color = None,
        **kwargs: Unpack[EntryOpts],
    ):
        """Initialize the themed Entry widget.

        Applies ttkbootstrap color styling at initialization. Entry does not
        support visual variants.

        Args:
            master (Misc | None): The parent widget.
            color (Color, optional): A ttkbootstrap color name.
            **kwargs (EntryOpts): Additional options passed to ttk.Entry.
        """
        self._color = color
        self._variant = None  # Entry does not support variants
        super().__init__(master, **kwargs)
        self._init_style(kwargs, color=color, variant="")
