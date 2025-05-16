from tkinter import Misc
from tkinter.ttk import Radiobutton as ttkRadiobutton

from ttkbootstrap.typing import StyleColor as Color
from ttkbootstrap.typing import RadiobuttonOptions as RadioOpts
from ttkbootstrap.styledwidget import StyledWidgetMixin

try:
    from typing import Unpack
except ImportError:
    from typing_extensions import Unpack


class Radiobutton(StyledWidgetMixin, ttkRadiobutton):
    """
    A themed radiobutton widget with support for dynamic color styling.

    This widget extends the standard `ttk.Radiobutton` by applying a custom
    style based on the provided `color`. The color affects the indicator and
    text appearance when selected, allowing for visually distinct radio groups.

    Ideal for grouped selections where consistent theming and visual clarity
    are desired.

    Example:
        Radiobutton(root, text="Choice A", value="a", variable=var, color="info")

    Parameters:
        master (Misc | None): The parent container widget.
        color (Color): The highlight color theme (e.g., "info", "primary").
        **kwargs (RadiobuttonOpts): Additional options accepted by `ttk.Radiobutton`.
    """

    def __init__(
        self,
        master: Misc | None = None,
        color: Color = None,
        **kwargs: Unpack[RadioOpts],
    ):
        """
        Initialize a styled Radiobutton.

        Parameters:
            master (Misc | None): The parent container.
            color (Color, optional): A ttkbootstrap color token (e.g., "info", "primary").
            **kwargs (RadioOpts): Additional standard ttk.Radiobutton options.
        """
        self._color = color
        self._variant = None  # Radiobuttons do not support variants
        super().__init__(master, **kwargs)
        self._init_style(kwargs, color=color, variant="")
