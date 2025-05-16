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
    A themed entry widget with support for dynamic color styling.

    This widget extends the standard `ttk.Entry` by applying a style derived
    from the provided `color`. The color affects elements like the border
    and focus ring to visually align with the overall theme.

    It retains the full behavior of a normal entry widget, supporting text
    input, validation, and variable binding, while offering a more customized
    appearance through theming.

    Example:
        Entry(root, textvariable=myvar, color="info")

    Parameters:
        master (Misc | None): The parent container widget.
        color (Color, optional): The color theme (e.g., "info", "primary").
        **kwargs (EntryOpts): Additional options accepted by `ttk.Entry`.
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
