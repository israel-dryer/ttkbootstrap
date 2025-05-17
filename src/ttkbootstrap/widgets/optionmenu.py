from tkinter import Misc, StringVar, Menu
from tkinter.ttk import Menubutton

from ttkbootstrap.ttk_types import StyleColor as Color
from ttkbootstrap.ttk_types import OptionMenuOptions as OptMenuOpts

try:
    from typing import Unpack
except ImportError:
    from typing_extensions import Unpack


class OptionMenu(Menubutton):
    """A themed drop-down list widget for selecting from a fixed set of values.

    This widget behaves like a simplified combobox using a `tk.Menu` for
    selection. The `color` parameter allows you to theme the appearance of
    the dropdown button using ttkbootstrap styles.

    Unlike `ttk.Combobox`, this widget uses radio-style menu items for
    selection and automatically updates both the menu and button text
    when a new item is selected.

    Example:
        >>> from ttkbootstrap.widgets import OptionMenu
        >>> var = tk.StringVar()
        >>> om = OptionMenu(root, variable=var, default="One", "One", "Two", "Three", color="info")
        >>> om.pack()

    Args:
        master (Misc | None): The parent container widget.
        variable (StringVar): The variable to bind the selected option to.
        default (str): The initially selected value.
        *values (str): A sequence of selectable string options.
        color (Color, optional): A ttkbootstrap color theme (e.g., "info", "primary").
        **kwargs (OptMenuOpts): Additional options accepted by `ttk.Menubutton`.
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
        """Initialize the themed OptionMenu widget.

        This constructs a styled menubutton with a bound menu that contains
        the provided values as radiobutton options.

        Args:
            master (Misc | None): The parent container.
            variable (StringVar): The associated variable to update on selection.
            default (str): The default value to display.
            *values (str): Selectable values in the menu.
            color (Color, optional): The ttkbootstrap color used to style the button.
            **kwargs (OptMenuOpts): Additional configuration options passed to the `Menubutton`.
        """
        self._color = color
        self._variant = None
        self.variable = variable

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
