from tkinter import Misc, StringVar
from typing import Callable, Optional, Sequence, Union, Literal
from uuid import uuid4

from ..layout import Frame
from .radio_button import RadioButton
from .radio_button_toggle import RadioButtonToggle
from ..mixins import OnChangeMixin, VariableMixin
from ...ttk_types import StyleColor

Orient = Literal["horizontal", "vertical"]


class RadioGroup(Frame, OnChangeMixin, VariableMixin):
    """
    A container for managing a group of styled Radio widgets that share a common group.
    You may specify either "radio" or "toggle" to set the visual type. If you choose
    toggle, you may also specify an optional icon in the 3rd position (label, value, icon).

    Args:
        master (Misc): Parent widget.
        options (Sequence[tuple[str, Union[str, int]]]): List of [(label, value, icon), ...] items to create radio buttons from..
        selected (Union[str, int, None]): The initially selected value.
        color (StyleColor): Named color theme for all buttons.
        orient (Literal["horizontal", "vertical"]): Layout direction.
        gap (int): The space between buttons.
        type (Literal["radio", "toggle"]): The type of radio button to use.
        on_change (Callable[[Union[str, int]], None]): Callback on value change.
        **kwargs: Additional Frame options.
    """

    def __init__(
        self,
        master: Optional[Misc],
        options: Sequence,
        selected: Union[str, int, None] = None,
        color: StyleColor = "primary",
        orient: Orient = "horizontal",
        gap: int = 8,
        type: Literal["radio", "toggle"] = "radio",
        on_change: Optional[Callable[[Union[str, int]], None]] = None,
        **kwargs,
    ):
        super().__init__(master, **kwargs)
        self._group_id = str(uuid4())  # shared group name
        self._buttons: list[RadioButton] = []
        self._orient = orient
        self._on_change = on_change
        self._gap = gap
        self._type = type

        self._variable = StringVar(self.widget.master, selected, self._group_id)

        if self._on_change:
            self.on_change = self._on_change

        for option in options:
            if len(option) == 2:
                label, value = option
                icon = None
            elif len(option) == 3:
                label, value, icon = option
            else:
                raise ValueError(
                    "Invalid option format. Expected (label, value, icon) or (label, value)."
                )
            print(label, value, icon)
            self.add_button(label, value, icon, selected == value, color)

    def add_button(
        self,
        label: str,
        value: Union[str, int],
        icon: Optional[str] = None,
        selected: bool = False,
        color: StyleColor = "primary"
    ):
        """Add a new radio button to the group."""
        if self._type == "radio":
            btn = RadioButton(
                self.widget.master,
                text=label,
                value=value,
                selected=selected,
                group=self._group_id,
                color=color
            )
        else:
            btn = RadioButtonToggle(
                self.widget.master,
                text=label,
                value=value,
                icon=icon,
                selected=selected,
                group=self._group_id,
                color=color
            )
        if self._orient == "horizontal":
            btn.widget.pack(side="left", padx=self._gap, pady=2)
        else:
            btn.widget.pack(anchor="w", pady=self._gap)

        self._buttons.append(btn)
