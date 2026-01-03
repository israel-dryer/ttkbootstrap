from typing_extensions import Unpack

from ttkbootstrap.widgets.primitives.label import Label, LabelKwargs
from ttkbootstrap.widgets.types import Master


class Badge(Label):
    """ttkbootstrap wrapper for `ttk.Label` that renders with a badge style."""

    def __init__(self, master: Master = None, **kwargs: Unpack[LabelKwargs]):
        """Create a themed ttkbootstrap Badge.

        Args:
            master: Parent widget. If None, uses the default root window.

        Other Parameters:
            text (str): Text to display on the badge.
            image (PhotoImage): Image to display.
            icon (str | dict): Theme-aware icon spec handled by the style system.
            icon_only (bool): If True, removes the additional padding reserved for label text.
            compound (str): Placement of the image relative to text.
            anchor (str): Alignment of the badge content within its area.
            justify (str): How to justify multiple lines of text.
            localize (bool | Literal['auto']): Determines the widget's localization mode.
            value_format (str | dict): Format specification for the badge value.
            padding (int | tuple): Extra space around the badge content.
            width (int): Width of the badge in characters.
            wraplength (int): Maximum width before wrapping text.
            font (str | Font): Font for the badge text.
            foreground (str): Text color.
            background (str): Background color.
            relief (str): Border style.
            state (str): Widget state.
            takefocus (bool): Whether the widget participates in focus traversal.
            style (str): Explicit ttk style name (overrides accent/variant).
            accent (str): Accent token for styling, e.g. 'primary', 'success', 'danger'.
            variant (str): Shape of badge. 'pill' or 'square' (default).
            bootstyle (str): DEPRECATED - Use `accent` and `variant` instead.
                Combined style tokens (defaults to 'badge').
            surface_color (str): Optional surface token; otherwise inherited.
            style_options (dict): Optional dict forwarded to the style builder.
        """
        kwargs.setdefault('ttk_class', 'TBadge')
        super().__init__(master=master, **kwargs)
