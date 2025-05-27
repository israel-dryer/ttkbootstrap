from tkinter import Misc
from tkinter.ttk import Radiobutton as ttkRadiobutton

from ..mixins import BackgroundInheritMixin
from ...ttk_types import StyleColor
from ...style.styled_widget import StyledWidget

try:
    from typing import Unpack
except ImportError:
    from typing_extensions import Unpack


class RadioToggle(BackgroundInheritMixin, StyledWidget, ttkRadiobutton):

    def __init__(
        self,
        master: Misc = None,
        color: StyleColor = "primary",
        **kwargs
    ):
        self._color = color
        self._variant = "default"
        self._extras = {}
        super().__init__(master, **kwargs)
        self._init_style(
            'radiobutton.toggle',
            color=color, variant=self._variant, extras=self._extras, **kwargs)
