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
    """A horizontal or vertical rule for visually separating groups of widgets.

    This widget extends `ttk.Separator` and allows you to apply a themed color
    for more consistent styling in interfaces. It supports both horizontal
    and vertical orientations.

    Example:
        >>> from ttkbootstrap.widgets import Separator
        >>> sep = Separator(root, orient="horizontal", color="secondary")
        >>> sep.pack(fill="x", pady=5)

    Args:
        master (Misc | None): The parent container widget.
        color (Color, optional): A themed color token (e.g., "secondary", "info").
        **kwargs (SeparatorOptions): Additional options accepted by `ttk.Separator`.
    """

    def __init__(
        self,
        master: Misc | None = None,
        color: Color = None,
        **kwargs: Unpack[SepOpts],
    ):
        """Initialize the themed Separator widget.

        Args:
            master (Misc | None): The parent container.
            color (Color, optional): A ttkbootstrap color token.
            **kwargs (SeparatorOptions): Additional configuration options passed to `ttk.Separator`.
        """
        self._color = color
        self._variant = None  # No variant support
        super().__init__(master, **kwargs)
        self._init_style(kwargs, color=color, variant="")
