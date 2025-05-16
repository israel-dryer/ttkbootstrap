from tkinter import Misc
from tkinter.ttk import Combobox as ttkCombobox

from ttkbootstrap.typing import StyleColor as Color
from ttkbootstrap.typing import ComboboxOptions as CbOpts
from ttkbootstrap.styledwidget import StyledWidgetMixin

try:
    from typing import Unpack
except ImportError:
    from typing_extensions import Unpack


class Combobox(StyledWidgetMixin, ttkCombobox):
    """
    A styled ttkbootstrap-compatible Combobox that supports a `color` parameter
    for dynamic style generation.

    This widget wraps tkinter.ttk.Combobox and applies ttkbootstrap theming
    based on the provided `color`.

    Example:
        Combobox(root, values=["One", "Two"], color="info")
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
