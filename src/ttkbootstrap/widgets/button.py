from tkinter import Misc
from tkinter.ttk import Button as ttkButton

from ttkbootstrap.ttk_types import (
    StyleColor,
    ButtonStyleVariant as Variant,
    ButtonOptions as BtnOpts,
)
from ttkbootstrap.styledwidget import StyledWidgetMixin

try:
    from typing import Unpack
except ImportError:
    from typing_extensions import Unpack


class Button(StyledWidgetMixin, ttkButton):
    """
    A themed ttk Button widget with support for dynamic color and variant styling.

    This widget extends `ttk.Button` by applying a theme-aware style based on
    `color` and `variant` parameters. It supports all standard `ttk.Button`
    behavior, while enabling modern theming using ttkbootstrap.

    Features:
        - Themed color support using keywords like "primary", "danger", etc.
        - Variant styling such as "outline", "link", and "default"
        - Full compatibility with `ttk.Button` options and callbacks

    Example:
        >>> from ttkbootstrap.widgets import Button
        >>> btn = Button(root, text="Submit", color="primary", variant="outline")

    Args:
        master (Misc, optional):
            The parent widget.

        color (StyleColor, optional):
            A color token from the current theme (e.g., "primary", "warning").

        variant (Variant, optional):
            The button's visual style (e.g., "default", "outline", "link").

        **kwargs (Unpack[BtnOpts]):
            Additional `ttk.Button` options such as `text`, `command`, `state`, etc.
    """

    def __init__(
        self,
        master: Misc = None,
        color: StyleColor = None,
        variant: Variant = "default",
        **kwargs: Unpack[BtnOpts],
    ):
        """
        Initialize a new themed Button.

        Args:
            master (Misc, optional):
                The parent container widget.

            color (StyleColor, optional):
                A color keyword that maps to the theme's palette.

            variant (Variant):
                The button variant style such as "default", "outline", or "link".

            **kwargs (Unpack[BtnOpts]):
                Any standard `ttk.Button` options.
        """
        self._color = color
        self._variant = variant
        super().__init__(master, **kwargs)
        self._init_style(kwargs, color=color, variant=variant)
