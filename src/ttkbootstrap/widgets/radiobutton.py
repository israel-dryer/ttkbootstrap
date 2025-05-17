from tkinter import Misc
from tkinter.ttk import Radiobutton as ttkRadiobutton

from ttkbootstrap.ttk_types import StyleColor as Color
from ttkbootstrap.ttk_types import RadiobuttonOptions as RadioOpts
from ttkbootstrap.styledwidget import StyledWidgetMixin

try:
    from typing import Literal, Unpack
except ImportError:
    from typing_extensions import Unpack


class Radiobutton(StyledWidgetMixin, ttkRadiobutton):
    """A themed radiobutton widget with dynamic color styling.

    This widget extends `ttk.Radiobutton` and applies ttkbootstrap styling
    using the `color` option to control the indicator and text highlight color.
    Optionally, you can specify a `variant` to alter the styling mode, though
    most use cases rely on the default style.

    Themed radiobuttons are useful for visually grouped selection controls
    where the active option should reflect a brand or theme palette.

    Example:
        >>> from ttkbootstrap.widgets import Radiobutton
        >>> rb = Radiobutton(root, text="Choice A", value="a", variable=var, color="info")
        >>> rb.pack()

    Args:
        master (Misc | None): The parent container widget.
        color (Color, optional): The highlight color theme (e.g., "info", "primary").
        **kwargs (RadiobuttonOpts): Additional options accepted by `ttk.Radiobutton`.
    """

    def __init__(
        self,
        master: Misc | None = None,
        color: Color = None,
        **kwargs: Unpack[RadioOpts],
    ):
        """Initialize the themed Radiobutton widget.

        Args:
            master (Misc | None): The parent container.
            color (Color, optional): A ttkbootstrap color token (e.g., "success", "danger").
            **kwargs (RadiobuttonOpts): Additional keyword arguments passed to `ttk.Radiobutton`.
        """
        self._color = color
        self._variant = kwargs.pop('variant', 'default')
        super().__init__(master, **kwargs)
        self._init_style(kwargs, color=color, variant=self._variant)
