from typing_extensions import Unpack

from ttkbootstrap.widgets.primitives.label import Label, LabelKwargs


class Badge(Label):
    """ttkbootstrap wrapper for `ttk.Label` that renders with a badge style."""

    def __init__(self, master=None, **kwargs: Unpack[LabelKwargs]):
        """Create a themed ttkbootstrap Badge.

        Keyword Args:
            text: Text to display on the badge.
            image: Image to display.
            icon: Theme-aware icon spec handled by the style system.
            icon_only: If True, removes the additional padding reserved for label text.
            compound: Placement of the image relative to text.
            anchor: Alignment of the badge content within its area.
            justify: How to justify multiple lines of text.
            localize: Determines the widget's localization mode. 'auto', True, False.
            value_format: Format specification for the badge value.
            padding: Extra space around the badge content.
            width: Width of the badge in characters.
            wraplength: Maximum width before wrapping text.
            font: Font for the badge text.
            foreground: Text color.
            background: Background color.
            relief: Border style.
            state: Widget state.
            takefocus: Whether the widget participates in focus traversal.
            style: Explicit ttk style name (overrides bootstyle).
            bootstyle: ttkbootstrap style tokens describing the badge color (defaults to 'badge' and is coerced to include '-badge').
            surface_color: Optional surface token; otherwise inherited.
            style_options: Optional dict forwarded to the style builder.
        """
        bootstyle = kwargs.pop('bootstyle', 'badge')

        # coerce to badge if not already there (in this case, the bootstyle is likely just a color).
        if 'badge' not in bootstyle:
            bootstyle = f"{bootstyle}-badge"

        kwargs['bootstyle'] = bootstyle

        super().__init__(master=master, **kwargs)
