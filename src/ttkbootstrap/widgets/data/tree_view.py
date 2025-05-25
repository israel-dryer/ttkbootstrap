from tkinter import Misc
from tkinter.ttk import Treeview as ttkTreeview

from ttkbootstrap.ttk_types import (
    StyleColor as Color, TreeviewOptions as TvOpts
)
from ttkbootstrap.style.styled_widget import StyledWidget

try:
    from typing import Unpack
except ImportError:
    from typing_extensions import Unpack


class Treeview(StyledWidget, ttkTreeview):

    def __init__(
            self,
            master: Misc = None,
            color: Color = "default",
            **kwargs: Unpack[TvOpts]
    ):
        self._color = color
        self._variant = "default"
        super().__init__(master, **kwargs)
        self._init_style('treeview', color=color, variant=self._variant, **kwargs)
