from ttkbootstrap.widgets.primitives.checkbutton import CheckButton


class CheckToggle(CheckButton):
    """ttkbootstrap wrapper for `ttk.Checkbutton` that renders with a ToolButton style"""

    def __init__(self, master=None, **kwargs):
        """Create a themed ttkbootstrap CheckToggle.

        Keyword Args:
            text: Text to display on the toggle.
            textvariable: Tk variable linked to the text.
            textsignal: Reactive Signal linked to the text (auto-synced with textvariable).
            command: Callable invoked when the toggle changes state.
            image: Image to display.
            icon: Theme-aware icon spec handled by the style system.
            compound: Placement of the image relative to text.
            variable: Linked variable controlling the on/off state.
            signal: Reactive Signal controlling the on/off state (auto-synced with variable).
            value: Initial state for the widget's associated variable (defaults to None when unset).
            onvalue: Value set in `variable` when selected.
            offvalue: Value set in `variable` when deselected.
            padding: Extra space around the content.
            width: Width of the control in characters.
            underline: Index of character to underline in `text`.
            state: Widget state.
            takefocus: Whether the widget participates in focus traversal.
            style: Explicit ttk style name (overrides bootstyle).
            bootstyle: ttkbootstrap style tokens describing the toggle color (defaults to 'Toolbutton' and is coerced to include '-badge').
            surface_color: Optional surface token; otherwise inherited.
            style_options: Optional dict forwarded to the style builder.
        """
        bootstyle = kwargs.pop('bootstyle', 'Toolbutton')

        # coerce to toolbutton if not already there (in this case, the bootstyle is likely just a color).
        if 'toolbutton' not in bootstyle:
            bootstyle = f"{bootstyle}-toolbutton"

        kwargs['bootstyle'] = bootstyle

        super().__init__(master, **kwargs)
