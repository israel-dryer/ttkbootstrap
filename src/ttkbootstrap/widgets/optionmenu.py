from tkinter import Misc, StringVar, Menu
from tkinter.ttk import Menubutton

from ttkbootstrap.typing import StyleColor as Color
from ttkbootstrap.typing import OptionMenuOptions as OptMenuOpts

try:
    from typing import Unpack
except ImportError:
    from typing_extensions import Unpack


class OptionMenu(Menubutton):
    """
    A themed drop-down list widget for selecting from a fixed set of values.

    This widget behaves like a combobox but uses a popup menu for selection.
    Supports theming through the `color` parameter.

    Example:
        OptionMenu(root, variable, "One", "One", "Two", "Three", color="info")
    """

    def __init__(
        self,
        master: Misc | None,
        variable: StringVar,
        default: str,
        *values: str,
        color: Color = None,
        **kwargs: Unpack[OptMenuOpts],
    ):
        """
        Initialize a themed OptionMenu.

        Parameters:
            master (Misc | None): The parent container.
            variable (StringVar): The associated variable to update.
            default (str): The initially selected value.
            *values (str): The selectable options.
            color (Color): A themed style color.
            **kwargs (OptMenuOpts): Additional Menubutton options.
        """
        self._color = color
        self._variant = None
        self.variable = variable

        # Create the Menubutton
        super().__init__(master, text=default, **kwargs)

        self.menu = Menu(self, tearoff=0)
        self["menu"] = self.menu
        self.variable.set(default)

        for val in values:
            self.menu.add_radiobutton(
                label=val,
                variable=self.variable,
                value=val,
                command=lambda v=val: self.configure(text=v)
            )
