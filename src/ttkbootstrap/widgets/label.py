from tkinter import Misc
from tkinter.ttk import Label as ttkLabel

from ttkbootstrap.ttk_types import StyleColor as Color
from ttkbootstrap.ttk_types import LabelOptions as LabelOpts
from ttkbootstrap.styledwidget import StyledWidgetMixin

try:
    from typing import Unpack
except ImportError:
    from typing_extensions import Unpack

LabelVariant = str  # Optional: could define Literal["default", "inverse"] if strict


class Label(StyledWidgetMixin, ttkLabel):
    """
    A themed label widget with support for foreground and background styling.

    This widget extends the standard `ttk.Label` and allows you to customize
    its appearance using a `color` and a `variant`. The `color` sets the
    thematic color (such as "success", "info", or "danger"), while the
    `variant` determines whether the color is applied to the text (`"default"`)
    or used as a background with inverted foreground (`"inverse"`).

    This is useful for context-sensitive labels such as status indicators,
    badges, or callouts.

    Supported variants:
        - "default": Applies color to the foreground only.
        - "inverse": Applies color to the background with contrasting text color.

    Example:
        Label(root, text="Connected", color="success", variant="inverse")

    Parameters:
        master (Misc | None): The parent container widget.
        color (Color, optional): A theme color name (e.g., "info", "danger").
        variant (str): Either "default" (text color) or "inverse" (background).
        **kwargs (LabelOpts): Additional options accepted by `ttk.Label`.
    """

    def __init__(
        self,
        master: Misc | None = None,
        color: Color = None,
        variant: LabelVariant = "default",
        **kwargs: Unpack[LabelOpts],
    ):
        """
        Initialize a styled Label.

        Parameters:
            master (Misc | None): The parent container.
            color (Color, optional): A ttkbootstrap color token (e.g., "info", "danger").
            variant (str): Either "default" or "inverse".
            **kwargs (LabelOpts): Additional standard ttk.Label options.
        """
        self._color = color
        self._variant = variant
        super().__init__(master, **kwargs)
        self._init_style(kwargs, color=color, variant=variant)
