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
    """
    A styled `Text` widget with optional vertical and horizontal scrollbars.

    This widget wraps the standard Tkinter `Text` widget with enhanced
    scrollbar integration using themed `ttkbootstrap` scrollbars.

    Features:
    ---------
    - Vertical and/or horizontal scrollbars
    - Optional autohide behavior for scrollbars
    - Scrollbar styling via `color` and `variant`
    - Full `Text` widget API passthrough
    - Customizable geometry and padding
    - Wraps text by default unless horizontal scrollbar is used

    Notes:
    ------
    - This widget is functionally identical to `tkinter.Text` with
      added scrollbars.
    - See https://tcl.tk/man/tcl8.6/TkCmd/text.htm for full `Text` options.

    Example:
    --------
    ```python
    import ttkbootstrap as ttk
    from ttkbootstrap.constants import *

    app = ttk.Window()
    st = ttk.ScrolledText(app, padding=5, height=10, autohide=True)
    st.pack(fill=BOTH, expand=YES)
    st.insert(END, 'Insert your text here.')
    app.mainloop()
    ```
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
        """
        Initialize a new `ScrolledText` widget.

        Parameters:
            master (Widget, optional):
                The parent container for the widget.

            padding (int, optional):
                Padding around the `Text` widget.

            color (StyleColor, optional):
                A ttkbootstrap color keyword for scrollbar and focus styling.

            variant (Literal['default', 'round'], optional):
                Style variant for the scrollbars. Default is "default".

            autohide (bool, optional):
                If True, scrollbars will hide unless hovered over.

            vbar (bool, optional):
                If True, show a vertical scrollbar. Default is True.

            hbar (bool, optional):
                If True, show a horizontal scrollbar and disable wrapping.

            **kwargs (EntryOptions, optional):):
                Additional keyword arguments passed to the underlying `Text` widget.
        """
        super().__init__(master, padding=padding)

        self._text = Text(self, padx=50, **kwargs)
        self._vbar = None
        self._hbar = None

        # Delegate all Text widget methods (excluding geometry) to self
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
        """Update the scrollbar position and width if horizontal bar is shown."""
        if self._hbar:
            self.update_idletasks()
            text_width = self.winfo_width()
            vbar_width = self._vbar.winfo_width() if self._vbar else 0
            relx = (text_width - vbar_width) / text_width
            self._hbar.place(rely=1.0, relwidth=relx)

    @property
    def text(self):
        """Return the internal `Text` widget instance."""
        return self._text

    @property
    def hbar(self):
        """Return the internal horizontal scrollbar instance."""
        return self._hbar

    @property
    def vbar(self):
        """Return the internal vertical scrollbar instance."""
        return self._vbar

    def hide_scrollbars(self, *_):
        """Hide both scrollbars (if present)."""
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
        """Show both scrollbars (if present)."""
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
        """Enable autohide: show on mouse enter, hide on mouse leave."""
        self.bind("<Enter>", self.show_scrollbars)
        self.bind("<Leave>", self.hide_scrollbars)
