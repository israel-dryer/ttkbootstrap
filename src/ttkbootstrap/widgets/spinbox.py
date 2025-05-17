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
    """A themed Spinbox widget for selecting from a fixed range of values.

    This widget extends `ttk.Spinbox` and adds theme support using the
    `color` parameter to style the background and arrow controls.

    It is useful for numeric inputs or stepping through predefined options.

    Example:
        >>> from ttkbootstrap.widgets import Spinbox
        >>> sb = Spinbox(root, from_=0, to=10, color="primary", width=10)
        >>> sb.pack()

    Args:
        master (Misc | None): The parent container widget.
        color (StyleColor, optional): A ttkbootstrap color token (e.g., "primary", "info").
        **kwargs (SpinboxOptions): Additional keyword arguments for `ttk.Spinbox`.
    """

    def __init__(
        self,
        master: Misc | None = None,
        color: Color = None,
        **kwargs: Unpack[SpinOpts],
    ):
        """Initialize the themed Spinbox widget.

        Args:
            master (Misc | None): The parent container.
            color (StyleColor, optional): The style color applied to the Spinbox.
            **kwargs (SpinboxOptions): Configuration options passed to `ttk.Spinbox`.
        """
        self._color = color
        self._variant = None
        super().__init__(master, **kwargs)
        self._init_style(kwargs, color=color, variant="")
