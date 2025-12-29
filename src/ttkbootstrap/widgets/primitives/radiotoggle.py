from ttkbootstrap.widgets.primitives.radiobutton import RadioButton
from ttkbootstrap.widgets.types import Master


class RadioToggle(RadioButton):
    """ttkbootstrap wrapper for `ttk.Radiobutton` that renders with a toggle badge style."""

    def __init__(self, master: Master = None, **kwargs):
        """Create a themed ttkbootstrap RadioToggle.

        Args:
            master: Parent widget. If None, uses the default root window.

        Other Parameters:
            text (str): Text to display.
            textvariable (Variable): Tk variable linked to the text.
            textsignal (Signal[str]): Reactive Signal linked to the text (auto-synced with textvariable).
            command (Callable): Callable invoked when the value is selected.
            image (PhotoImage): Image to display.
            icon (str | dict): Theme-aware icon spec handled by the style system.
            icon_only (bool): Removes the additional padding added for label text.
            compound (str): Placement of the image relative to text.
            variable (Variable): Linked Tk variable that receives the selected value.
            signal (Signal): Reactive Signal that receives the selected value (auto-synced with variable).
            value (Any): The value assigned to `variable` when this radio is selected.
            padding (int | tuple): Extra space around the content.
            anchor (str): Determines how the content is aligned in the container. Combination of 'n', 's', 'e', 'w', or 'center' (default).
            width (int): Width of the control in characters.
            underline (int): Index of character to underline in `text`.
            state (str): Widget state ('normal', 'active', 'disabled', 'readonly').
            takefocus (bool): Whether the widget participates in focus traversal.
            style (str): Explicit ttk style name (overrides bootstyle).
            bootstyle (str): ttkbootstrap style tokens describing the toggle color
                (defaults to 'Toolbutton' and is coerced to include '-toolbutton').
            surface_color (str): Optional surface token; otherwise inherited.
            style_options (dict): Optional dict forwarded to the style builder.
            localize (bool | Literal['auto']): Determines the widget's localization mode.
        """
        super().__init__(master, class_='Toolbutton', **kwargs)
