from tkinter import Misc
from tkinter.ttk import Combobox as ttkCombobox

from ttkbootstrap.style.styled_widget import StyledWidget
from ttkbootstrap.ttk_types import (
    StyleColor as Color,
    ComboboxOptions as CbOpts
)
from ttkbootstrap.widgets.mixins import BackgroundInheritMixin

try:
    from typing import Unpack
except ImportError:
    from typing_extensions import Unpack


class Combobox(BackgroundInheritMixin, StyledWidget, ttkCombobox):

    def __init__(
        self,
        master: Misc | None = None,
        color: Color = "primary",
        **kwargs,
    ):
        """
        Initialize a themed `Combobox` widget.

        Args:
            master: The parent widget container.
            color: A ttkbootstrap theme token for styling.
            **kwargs: Keyword arguments forwarded to `ttk.Combobox`.
        """
        self._color = color
        self._variant = "default"  # Combobox does not support style variants
        self._extras = {}
        super().__init__(master, **kwargs)
        self._init_style('combobox', color=color, variant=self._variant, extras=self._extras, **kwargs)
