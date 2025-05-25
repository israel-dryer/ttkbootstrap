from __future__ import annotations

from typing import TYPE_CHECKING
from ttkbootstrap.style.style_builder import StyleBuilder

if TYPE_CHECKING:
    from tkinter.ttk import Combobox
    from ttkbootstrap.style.theme import Theme


class TkComboboxPopdownStyle(StyleBuilder):

    def __init__(self, theme: Theme):
        super().__init__(theme)

    def invoke(self, widget: Combobox) -> None:
        """Update the legacy ttk.Combobox elements. This method is
        called every time the theme is changed to ensure that the
        legacy tkinter components embedded in this ttk widget are
        styled appropriate to the current theme.

        The ttk.Combobox contains several elements that are not styled
        using the ttk theme engine. This includes the **popdownwindow**
        and the **scrollbar**. Both of these widgets are configured
        manually using calls to tcl/tk.
        """
        # style colors
        shades_bg = self.theme.get_shades('background')
        shades_lt = self.theme.get_shades('light')
        foreground = self.theme.foreground
        select_background = self.theme.info
        select_foreground = self.theme.get_foreground('info')
        background = shades_bg.l1 if self.theme.is_dark_theme else shades_lt.base

        tk_settings = []
        tk_settings.extend(["-borderwidth", 0])
        tk_settings.extend(["-background", background])
        tk_settings.extend(["-foreground", foreground])
        tk_settings.extend(["-selectbackground", select_background])
        tk_settings.extend(["-selectforeground", select_foreground])

        # set popdown style
        popdown = widget.tk.eval(f"ttk::combobox::PopdownWindow {str(widget)}")
        widget.tk.call(f"{popdown}.f.l", "configure", *tk_settings)

        # set scrollbar style
        sb_style = "TCombobox.Vertical.TScrollbar"
        widget.tk.call(f"{popdown}.f.sb", "configure", "-style", sb_style)
