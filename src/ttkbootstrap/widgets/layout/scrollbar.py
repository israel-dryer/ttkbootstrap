from tkinter import Misc
from tkinter.ttk import Scrollbar as ttkScrollbar

from ttkbootstrap.style.styled_widget import StyledWidget
from ttkbootstrap.ttk_types import (
    StyleColor as Color,
    ScrollbarOptions as ScrollOpts
)

try:
    from typing import Unpack, Literal
except ImportError:
    from typing_extensions import Unpack, Literal


class Scrollbar(StyledWidget, ttkScrollbar):
    """
    A themed scrollbar widget that supports ttkbootstrap color and variant styling.

    This widget inherits from `ttk.Scrollbar` and extends it with theme-aware
    styling based on the selected `color` and `variant`. It is designed to
    seamlessly blend with modern ttkbootstrap themes.

    Features:
    - Themed scrollbar styling using `color` tokens (e.g., "primary", "info")
    - Support for different `variant` types (e.g., "default", "round")
    - Dynamic theming via style engine integration
    - Compatible with vertical and horizontal orientation

    Example:
        >>> from ttkbootstrap.widgets import Scrollbar
        >>> sb = Scrollbar(root, orient="vertical", color="primary")
        >>> sb.pack(side="right", fill="y")

    Args:
        master (Misc | None): The parent container widget.
        color (Color): The scrollbar color token. Defaults to "default".
        variant (Literal['default', 'round']): The scrollbar visual variant. Defaults to "default".
        orient (Literal["vertical", "horizontal"]): The scrollbar orientation. Defaults to "vertical".
        **kwargs (ScrollOpts): Additional options passed to `ttk.Scrollbar`.
    """

    def __init__(
            self,
            master: Misc | None = None,
            color: Color = "default",
            variant: Literal['default', 'round'] = 'default',
            orient: Literal["vertical", "horizontal"] = "vertical",
            **kwargs: Unpack[ScrollOpts],
    ):
        """
        Initialize a new instance of the themed `Scrollbar` widget.

        Args:
            master (Misc | None): The parent container widget.
            color (Color): A ttkbootstrap color token (e.g., "primary", "danger").
            variant (Literal['default', 'round']): The scrollbar style variant.
            orient (Literal["vertical", "horizontal"]): The scrollbar's orientation.
            **kwargs (ScrollOpts): Additional ttk scrollbar options.
        """
        self._color = color
        self._variant = variant
        self._orient = orient

        super().__init__(master, orient=orient, **kwargs)

        self._init_style(
            "scrollbar",
            color=self._color,
            variant=self._variant,
            orient=self._orient,
            **kwargs
        )
