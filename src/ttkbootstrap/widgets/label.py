from tkinter import Misc
from tkinter.ttk import Label as ttkLabel

from ttkbootstrap.typing import StyleColor as Color
from ttkbootstrap.typing import LabelOptions as LabelOpts
from ttkbootstrap.styledwidget import StyledWidgetMixin

try:
    from typing import Unpack
except ImportError:
    from typing_extensions import Unpack

LabelVariant = str  # Optional: could define Literal["default", "inverse"] if strict


class Label(StyledWidgetMixin, ttkLabel):
    """
    A styled ttkbootstrap-compatible Label that supports `color` and `variant`
    for foreground and background theming.

    Supported variants:
        - "default": regular label with colored foreground
        - "inverse": inverts foreground/background for contrast

    Example:
        Label(root, text="Status OK", color="success", variant="inverse")
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
