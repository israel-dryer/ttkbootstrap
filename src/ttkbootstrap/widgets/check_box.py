from tkinter import Misc
from tkinter.ttk import Checkbutton as ttkCheckbutton

from ttkbootstrap.ttk_types import (
    StyleColor as Color, CheckbuttonOptions as CbOpts
)
from ttkbootstrap.style.styled_widget import StyledWidget

try:
    from typing import Unpack
except ImportError:
    from typing_extensions import Unpack


class CheckBox(StyledWidget, ttkCheckbutton):
    """
    A themed `ttk.Checkbutton` widget with support for dynamic color styling.

    This widget extends the `ttk.Checkbutton` by allowing the `color` parameter
    to apply theme-aware styling using ttkbootstrap's theme system.

    Features:
        - Themed highlight color using ttkbootstrap tokens (e.g., "info", "warning")
        - Fully supports `tk.BooleanVar`, `tk.IntVar`, or `tk.StringVar`
        - Standard checkbutton states: on/off/alternate
        - Compatible with all `ttk.Checkbutton` configuration options

    Example:
        >>> from ttkbootstrap.widgets import CheckBox
        >>> from tkinter import BooleanVar
        >>> var = BooleanVar()
        >>> cb = CheckBox(root, text="Enable", variable=var, color="primary")
        >>> cb.pack()

    Args:
        master (Misc, optional):
            The parent container.

        color (StyleColor, optional):
            A theme token used to control the color styling (e.g., "success").

        **kwargs (Unpack[CheckbuttonOptions]):
            Any valid `ttk.Checkbutton` configuration option such as:
            `text`, `variable`, `command`, `onvalue`, `offvalue`, `state`, etc.
    """

    def __init__(
            self,
            master: Misc = None,
            color: Color = "primary",
            **kwargs: Unpack[CbOpts],
    ):
        """
        Initialize a themed `Checkbutton`.

        Args:
            master (Misc, optional):
                The widget's parent container.

            color (StyleColor, optional):
                A color token that defines the themed appearance.

            **kwargs (Unpack[CheckbuttonOptions]):
                Additional keyword arguments passed to `ttk.Checkbutton`.
        """
        self._color = color
        self._variant = "default"  # Checkbutton does not support style variants
        super().__init__(master, **kwargs)
        self._init_style('checkbutton', color=color, variant=self._variant, **kwargs)
