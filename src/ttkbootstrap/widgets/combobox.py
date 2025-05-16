from tkinter import Misc
from tkinter.ttk import Combobox as ttkCombobox

from ttkbootstrap.ttk_types import StyleColor as Color
from ttkbootstrap.ttk_types import ComboboxOptions as CbOpts
from ttkbootstrap.styledwidget import StyledWidgetMixin

try:
    from typing import Unpack
except ImportError:
    from typing_extensions import Unpack


class Combobox(StyledWidgetMixin, ttkCombobox):
    """
    A themed combobox widget with support for dynamic color styling.

    This widget extends the standard `ttk.Combobox` by applying a custom
    style derived from the given `color`. This color affects the active
    border, arrow button, and selected item styling to provide visual
    consistency with the application's theme.

    It behaves the same as a standard combobox, supporting value selection,
    data binding, and editable input, while allowing for a more customized
    appearance.

    Example:
        Combobox(root, values=["One", "Two", "Three"], color="info")

    Parameters:
        master (Misc | None): The parent container widget.
        color (Color, optional): The color theme (e.g., "info", "primary").
        **kwargs (CbOpts): Additional options accepted by `ttk.Combobox`.
    """

    def __init__(
        self,
        master: Misc | None = None,
        color: Color = None,
        **kwargs: Unpack[CbOpts],
    ):
        """
        Initialize a styled Combobox.

        Parameters:
            master (Misc | None): The parent container.
            color (Color, optional): A ttkbootstrap color token (e.g., "info").
            **kwargs (CbOpts): Additional standard ttk.Combobox options.
        """
        self._color = color
        self._variant = None  # Explicitly no variant support
        super().__init__(master, **kwargs)
        self._init_style(kwargs, color=color, variant="")
