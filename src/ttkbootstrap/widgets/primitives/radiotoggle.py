from ttkbootstrap.widgets.primitives.radiobutton import RadioButton


class RadioToggle(RadioButton):
    """ttkbootstrap wrapper for `ttk.Radiobutton` that renders with a toggle badge style."""

    def __init__(self, master=None, **kwargs):
        """Create a themed ttkbootstrap RadioToggle.

        Keyword Args:
            text: Text to display.
            textvariable: Tk variable linked to the text.
            textsignal: Reactive Signal linked to the text (auto-synced with textvariable).
            command: Callable invoked when the value is selected.
            image: Image to display.
            icon: Theme-aware icon spec handled by the style system.
            icon_only: Removes the additional padding added for label text.
            compound: Placement of the image relative to text.
            variable: Linked tk variable that receives the selected value.
            signal: Reactive Signal that receives the selected value (auto-synced with variable).
            value: The value assigned to `variable` when this radio is selected.
            padding: Extra space around the content.
            width: Width of the control in characters.
            underline: Index of character to underline in `text`.
            state: Widget state.
            takefocus: Whether the widget participates in focus traversal.
            style: Explicit ttk style name (overrides bootstyle).
            bootstyle: ttkbootstrap style tokens describing the toggle color (defaults to 'Toolbutton' and is coerced to include '-badge').
            surface_color: Optional surface token; otherwise inherited.
            style_options: Optional dict forwarded to the style builder.
            localize: Determines the widgets localization mode. 'auto', True, False.
        """
        bootstyle = kwargs.pop('bootstyle', 'Toolbutton')

        # coerce to toolbutton if not already there (in this case, the bootstyle is likely just a color).
        if 'toolbutton' not in bootstyle:
            bootstyle = f"{bootstyle}-toolbutton"

        kwargs['bootstyle'] = bootstyle

        super().__init__(master, **kwargs)
