from ttkbootstrap.widgets.primitives.checkbutton import CheckButton
from ttkbootstrap.widgets.types import Master


class CheckToggle(CheckButton):
    """ttkbootstrap wrapper for `ttk.Checkbutton` that renders with a ToolButton style"""

    def __init__(self, master: Master = None, **kwargs):
        """Create a themed ttkbootstrap CheckToggle.

        Args:
            master: Parent widget. If None, uses the default root window.

        Other Parameters:
            text (str): Text to display on the toggle.
            textvariable (Variable): Tk variable linked to the text.
            textsignal (Signal[str]): Reactive Signal linked to the text (auto-synced with textvariable).
            command (Callable): Callable invoked when the toggle changes state.
            image (PhotoImage): Image to display.
            icon (str | dict): Theme-aware icon spec handled by the style system.
            icon_only (bool): If True, removes the additional padding reserved for text.
            compound (str): Placement of the image relative to text.
            variable (Variable): Linked variable controlling the on/off state.
            signal (Signal): Reactive Signal controlling the on/off state (auto-synced with variable).
            value (Any): Initial state for the widget's associated variable (defaults to None when unset).
            onvalue (Any): Value set in `variable` when selected.
            offvalue (Any): Value set in `variable` when deselected.
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
