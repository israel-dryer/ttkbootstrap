from tkinter import Misc
from typing import Literal

from .checkbutton import Checkbutton
from ttkbootstrap.typing import StyleColor as Color, CheckbuttonOptions as CbOpts

try:
    from typing import Unpack
except ImportError:
    from typing_extensions import Unpack

SwitchVariant = Literal["round", "square"]


class Switch(Checkbutton):
    """
    A themed switch widget that behaves like a toggle control.

    This widget extends a standard checkbutton and presents a modern on/off
    toggle interface. It supports both `color` and `variant` parameters to
    customize its appearance, making it ideal for settings panels or feature toggles.

    Supported variants:
        - "round": Renders a pill-style toggle switch
        - "square": Renders a rectangular toggle switch

    Example:
        Switch(root, text="Enable notifications", color="success", variant="round")

    Parameters:
        master (Misc | None): The parent container widget.
        color (Color): The switch color theme (e.g., "success", "info").
        variant (str): Either "round" or "square".
        **kwargs (SwitchOpts): Additional options accepted by `ttk.Checkbutton`.
    """

    def __init__(
        self,
        master: Misc = None,
        color: Color = None,
        variant: SwitchVariant = "round",
        **kwargs: Unpack[CbOpts],
    ):
        """
        Initialize a styled Switch.

        Parameters:
            master (Misc, optional): The parent container.
            color (Color, optional): A ttkbootstrap color token (e.g., "success").
            variant (SwitchVariant): The switch shape: "round" or "square".
            **kwargs (CbOpts): Additional standard ttk.Checkbutton options.
        """
        self._color = color
        self._variant = variant

        variant += "-toggle"

        super().__init__(master, **kwargs)
        self._init_style(kwargs, color=color, variant=variant)
