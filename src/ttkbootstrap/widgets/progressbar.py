from tkinter import Misc
from tkinter.ttk import Progressbar as ttkProgressbar

from ttkbootstrap.typing import StyleColor as Color
from ttkbootstrap.typing import ProgressbarOptions as PbarOpts
from ttkbootstrap.styledwidget import StyledWidgetMixin

try:
    from typing import Unpack, Literal
except ImportError:
    from typing_extensions import Unpack, Literal

ProgressbarVariant = Literal["default", "striped"]


class Progressbar(StyledWidgetMixin, ttkProgressbar):
    """
    A styled ttkbootstrap-compatible Progressbar that supports `color` and `variant`
    styling options.

    Variants:
        - "default": solid fill style
        - "striped": animated stripe pattern

    Example:
        Progressbar(root, length=200, color="success", variant="striped", mode="indeterminate")
    """

    def __init__(
        self,
        master: Misc | None = None,
        color: Color = None,
        variant: ProgressbarVariant = "default",
        **kwargs: Unpack[PbarOpts],
    ):
        """
        Initialize a styled Progressbar.

        Parameters:
            master (Misc | None): The parent container.
            color (Color, optional): A ttkbootstrap color token (e.g., "info").
            variant (ProgressbarVariant): "default" or "striped".
            **kwargs (PbarOpts): Additional standard ttk.Progressbar options.
        """
        self._color = color
        self._variant = variant
        super().__init__(master, **kwargs)
        self._init_style(kwargs, color=color, variant=variant)
