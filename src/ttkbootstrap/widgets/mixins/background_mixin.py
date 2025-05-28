from tkinter import Misc, TclError
from tkinter.ttk import Style

"""
    This is an opt-in feature for widgets that inherit the parent background color.
    This mix-in will collect the background color from the parent widget and pass it
    as **extras to the style handler. It is up to the style handler to accept and
    process this information in the widget style.

    Tkinter does not support transparency, so the best that can be done when placing a
    styled widget onto a container that is not a default color is to adjust the color
    of the widget. This requires creating a custom style for ttk widgets. The
    expectation is that the style handler will use the background passed to `extras`
    and register a custom style such as `parent_color.primary.TFrame` when a custom
    background color is used.  If implemented, you should check to make sure that
    the background color does not match the theme background to avoid registering a
    new style that is unnecessary.
"""


class BackgroundMixin(Misc):
    # set by parent class
    _extras = None
    _inherit_background = None

    # set by mixin
    _background_color = None

    def _initialize_inherited_background(self):
        self._identify_inherited_background()
        self.bind('<<ThemeChanged>>', lambda _: self._identify_inherited_background(), add=True)

    def _identify_inherited_background(self):
        parent = self.master
        if parent is None:
            return
        bg_color = None

        # Try tk widget background
        try:
            bg_color = parent.cget("background")
        except TclError:
            pass

        # Try ttk style background
        if bg_color is None:
            try:
                style = Style()
                style_name = parent.cget("style") or parent.winfo_class()
                bg_color = style.lookup(style_name, "background")
            except Exception:
                pass

        self._background_color = bg_color
        self._extras['background'] = self._background_color
