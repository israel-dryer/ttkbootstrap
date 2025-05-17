from tkinter import Text
from ttkbootstrap.widgets.frame import Frame
from ttkbootstrap.widgets.scrollbar import Scrollbar
from typing import Literal
from ttkbootstrap.ttk_types import StyleColor, TextOptions

try:
    from typing import Unpack
except ImportError:
    from typing_extensions import Unpack


class ScrolledText(Frame):
    """A styled `Text` widget with optional vertical and horizontal scrollbars.

    This widget wraps the standard `tkinter.Text` widget and enhances it
    with themed `ttkbootstrap` scrollbars. It supports automatic scrollbar
    hiding, horizontal and vertical orientation, and full passthrough to
    native `Text` methods.

    Features:
    - Themed scrollbars (vertical and/or horizontal)
    - Optional autohide functionality
    - Full access to `Text` widget methods
    - Proper layout delegation and customization support

    Example:
        >>> from ttkbootstrap.widgets import ScrolledText
        >>> st = ScrolledText(root, padding=5, height=10, autohide=True)
        >>> st.pack(fill="both", expand=True)
        >>> st.insert("end", "Insert your text here.")

    Args:
        master (Widget, optional): The parent container.
        padding (int, optional): Padding around the internal `Text` widget.
        color (StyleColor, optional): Color used to theme the scrollbar(s).
        variant (Literal["default", "round"], optional): Scrollbar style variant.
        autohide (bool, optional): Whether to autohide scrollbars on hover.
        vbar (bool, optional): Whether to display a vertical scrollbar.
        hbar (bool, optional): Whether to display a horizontal scrollbar (disables text wrapping).
        **kwargs (TextOptions): Additional configuration options passed to `Text`.
    """

    def __init__(
        self,
        master=None,
        padding=2,
        color: StyleColor = None,
        variant: Literal['default', 'round'] = "default",
        autohide: bool = False,
        vbar: bool = True,
        hbar: bool = False,
        **kwargs: Unpack[TextOptions],
    ):
        """Initialize a themed ScrolledText widget.

        This constructor creates a `Text` widget wrapped inside a `Frame`, with
        optional themed vertical and horizontal scrollbars. Scrollbar styles can
        be customized using the `color` and `variant` parameters. When `autohide`
        is enabled, scrollbars appear only when the mouse enters the widget.

        All `Text` widget methods are exposed on this widget, making it a drop-in
        replacement for `tk.Text`.

        Args:
            master (Widget, optional): The parent widget.
            padding (int, optional): Padding around the inner `Text` widget. Default is 2.
            color (StyleColor, optional): Themed color name for the scrollbar.
            variant (Literal['default', 'round'], optional): Scrollbar style variant. Defaults to "default".
            autohide (bool, optional): If True, scrollbars appear only on hover. Defaults to False.
            vbar (bool, optional): If True, display a vertical scrollbar. Defaults to True.
            hbar (bool, optional): If True, display a horizontal scrollbar and disable text wrapping. Defaults to False.
            **kwargs (TextOptions): Additional options passed directly to the `Text` widget.
        """
        super().__init__(master, padding=padding)

        self._text = Text(self, padx=50, **kwargs)
        self._vbar = None
        self._hbar = None

        # Delegate Text methods (excluding geometry) to self
        for method in vars(Text).keys():
            if not any(m in method for m in ("pack", "grid", "place")):
                setattr(self, method, getattr(self._text, method))

        if vbar:
            self._vbar = Scrollbar(
                master=self,
                color=color,
                variant=variant,
                command=self._text.yview,
                orient="vertical",
            )
            self._vbar.place(relx=1.0, relheight=1.0, anchor="ne")
            self._text.configure(yscrollcommand=self._vbar.set)

        if hbar:
            self._hbar = Scrollbar(
                master=self,
                color=color,
                variant=variant,
                command=self._text.xview,
                orient="horizontal",
            )
            self._hbar.place(rely=1.0, relwidth=1.0, anchor="sw")
            self._text.configure(xscrollcommand=self._hbar.set, wrap="none")

        self._text.pack(side="left", fill="both", expand=1)

        if self._hbar:
            self.update_idletasks()
            self._text_width = self.winfo_reqwidth()
            self._scroll_width = self.winfo_reqwidth()

        self.bind("<Configure>", self._on_configure)

        if autohide:
            self.autohide_scrollbar()
            self.hide_scrollbars()

    def _on_configure(self, *_):
        """Update the horizontal scrollbar’s placement to account for vertical bar width."""
        if self._hbar:
            self.update_idletasks()
            text_width = self.winfo_width()
            vbar_width = self._vbar.winfo_width() if self._vbar else 0
            relx = (text_width - vbar_width) / text_width
            self._hbar.place(rely=1.0, relwidth=relx)

    @property
    def text(self):
        """tkinter.Text: Return the internal `Text` widget instance."""
        return self._text

    @property
    def hbar(self):
        """Scrollbar | None: Return the horizontal scrollbar instance, if present."""
        return self._hbar

    @property
    def vbar(self):
        """Scrollbar | None: Return the vertical scrollbar instance, if present."""
        return self._vbar

    def hide_scrollbars(self, *_):
        """Hide both scrollbars, if present."""
        if self._vbar:
            try:
                self._vbar.lower(self._text)
            except AttributeError:
                pass
        if self._hbar:
            try:
                self._hbar.lower(self._text)
            except AttributeError:
                pass

    def show_scrollbars(self, *_):
        """Show both scrollbars, if present."""
        if self._vbar:
            try:
                self._vbar.lift(self._text)
            except AttributeError:
                pass
        if self._hbar:
            try:
                self._hbar.lift(self._text)
            except AttributeError:
                pass

    def autohide_scrollbar(self, *_):
        """Enable autohide mode: show scrollbars on mouse enter, hide on leave."""
        self.bind("<Enter>", self.show_scrollbars)
        self.bind("<Leave>", self.hide_scrollbars)
