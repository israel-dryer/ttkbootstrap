from tkinter import Misc
from tkinter.ttk import Combobox as ttkCombobox

from ttkbootstrap.ttk_types import StyleColor as Color
from ttkbootstrap.ttk_types import ComboboxOptions as CbOpts
from ttkbootstrap.styledwidget import StyledWidgetMixin

try:
    from typing import Unpack
except ImportError:
    from typing_extensions import Unpack


class Combobox(StyledWidgetMixin, ttkCombobox):
    """
    A themed `ttk.Combobox` with ttkbootstrap color styling support.

    This widget behaves like a normal `ttk.Combobox`, but applies
    dynamic theme styling through the `color` argument. The visual
    appearance (border, arrow, focus ring, and highlight) aligns with
    the application's active theme.

    Features:
        - Themed visual styling with `color` (e.g., "primary", "success")
        - Full compatibility with `StringVar` or any Tk variable
        - Supports readonly and editable modes
        - All `ttk.Combobox` options supported

    Example:
        >>> from ttkbootstrap.widgets import Combobox
        >>> cb = Combobox(root, values=["One", "Two"], color="info", state="readonly")
        >>> cb.pack()

    Args:
        master (Misc | None, optional):
            The parent container widget.

        color (StyleColor, optional):
            A theme token that controls the visual styling.

        **kwargs (Unpack[ComboboxOptions]):
            All additional standard `ttk.Combobox` keyword arguments such as:
            `values`, `textvariable`, `width`, `postcommand`, `state`, etc.
    """

    def __init__(
        self,
        master: Misc | None = None,
        color: Color = "primary",
        **kwargs: Unpack[CbOpts],
    ):
        """
        Initialize a themed `Combobox` widget.

        Args:
            master: The parent widget container.
            color: A ttkbootstrap theme token for styling.
            **kwargs: Keyword arguments forwarded to `ttk.Combobox`.
        """
        self._color = color
        self._variant = None  # Combobox does not support style variants
        super().__init__(master, **kwargs)
        self._init_style(kwargs, color=color, variant="")

