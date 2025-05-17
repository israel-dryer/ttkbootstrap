from tkinter import Misc
from tkinter.ttk import Label as ttkLabel

from ttkbootstrap.ttk_types import StyleColor as Color
from ttkbootstrap.ttk_types import LabelOptions as LabelOpts
from ttkbootstrap.styledwidget import StyledWidgetMixin

try:
    from typing import Unpack
except ImportError:
    from typing_extensions import Unpack

LabelVariant = str  # Optionally: Literal["default", "inverse"]


class Label(StyledWidgetMixin, ttkLabel):
    """A themed label widget with support for foreground and background styling.

    This class extends the standard `ttk.Label` and supports styling through
    both `color` and `variant`. The `color` defines the theme (e.g. "info",
    "success", "danger"), and the `variant` controls how that color is applied.

    - If `variant` is `"default"` or None, the color is applied to the text.
    - If `variant` is `"inverse"`, the color is applied to the background and
      the text color is automatically chosen for contrast.

    This widget is useful for creating contextual indicators like badges,
    status pills, and callouts.

    Example:
        >>> from ttkbootstrap.widgets import Label
        >>> lbl = Label(root, text="Connected", color="success", variant="inverse")
        >>> lbl.pack()

    Args:
        master (Misc | None): The parent container widget.
        color (Color, optional): A ttkbootstrap color token (e.g., "info", "danger").
        variant (str, optional): "default" (text color) or "inverse" (background color).
        **kwargs (LabelOpts): Additional options accepted by `ttk.Label`.
    """

    def __init__(
        self,
        master: Misc | None = None,
        color: Color = None,
        variant: LabelVariant = None,
        **kwargs: Unpack[LabelOpts],
    ):
        """Initialize the themed Label widget.

        Args:
            master (Misc | None): The parent widget.
            color (Color, optional): The themed color name.
            variant (str, optional): Either "default" (foreground color) or "inverse" (background color).
            **kwargs (LabelOpts): Additional `ttk.Label` configuration options.
        """
        self._color = color
        self._variant = variant
        super().__init__(master, **kwargs)
        self._init_style(kwargs, color=color, variant=variant)
