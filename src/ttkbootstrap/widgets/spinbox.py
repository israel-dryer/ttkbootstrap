from tkinter import Misc
from tkinter.ttk import Spinbox as ttkSpinbox

from ttkbootstrap.ttk_types import StyleColor as Color
from ttkbootstrap.ttk_types import SpinboxOptions as SpinOpts
from ttkbootstrap.styledwidget import StyledWidgetMixin

try:
    from typing import Unpack
except ImportError:
    from typing_extensions import Unpack


class Spinbox(StyledWidgetMixin, ttkSpinbox):
    """
    A themed Spinbox widget for numeric or text-based selection from a fixed range.

    Supports theming through a `color` parameter and provides increment/decrement
    controls for stepping through values.

    Example:
        Spinbox(root, from_=0, to=10, color="primary", width=10)
    """

    def __init__(
        self,
        master: Misc | None = None,
        color: Color = None,
        **kwargs: Unpack[SpinOpts],
    ):
        """
        Initialize a themed Spinbox.

        Parameters:
            master (Misc | None): The parent container.
            color (Color, optional): A ttkbootstrap color token.
            **kwargs (SpinOpts): Additional standard ttk.Spinbox options.
        """
        self._color = color
        self._variant = None
        super().__init__(master, **kwargs)
        self._init_style(kwargs, color=color, variant="")
