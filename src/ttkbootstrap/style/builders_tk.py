"""Legacy ``tk.*`` widget styler for ttkbootstrap.

`StyleBuilderTK` styles the non-ttk widgets (Menu, Text, Canvas, ...) to match
the active theme. Split out of the monolithic `style.py` in 2.0.
"""
import tkinter as tk

from ttkbootstrap.constants import *
from ttkbootstrap.style.theme import Colors, ThemeDefinition, _accent_on_color


class StyleBuilderTK:
    """Styles legacy tkinter widgets (not ttk) to match the active theme.

    The methods here update tk widget style configurations internally and
    are not intended to be called by the end user. All legacy tkinter
    widgets are restyled via a callback whenever the theme changes.

    Some ttk widgets contain legacy components that must be updated too,
    such as the Combobox popdown, so this ensures they stay in sync with
    the current theme.
    """

    def __init__(self):
        # local import breaks the builders<-engine cycle (engine imports builders)
        from ttkbootstrap.style.engine import Style

        self.style = Style.get_instance()
        self.master = self.style.master

    @property
    def theme(self) -> ThemeDefinition:
        """A reference to the `ThemeDefinition` object for the current
        theme."""
        return self.style.theme

    @property
    def colors(self) -> Colors:
        """A reference to the `Colors` object for the current theme."""
        return self.style.colors

    @property
    def is_light_theme(self) -> bool:
        """Returns `True` if the theme is _light_, otherwise `False`."""
        return self.style.theme.mode == LIGHT

    def update_tk_style(self, widget: tk.Tk):
        """Update the window style.

        Parameters:

            widget (tkinter.Tk):
                The tk object to update.
        """
        widget.configure(background=self.colors.bg)
        # add default initial font for text widget
        widget.option_add('*Text*Font', 'TkDefaultFont')

    def update_toplevel_style(self, widget: tk.Toplevel):
        """Update the toplevel style.

        Parameters:

            widget (tkinter.Toplevel):
                The toplevel object to update.
        """
        widget.configure(background=self.colors.bg)

    def update_canvas_style(self, widget: tk.Canvas):
        """Update the canvas style.

        Parameters:

            widget (tkinter.Canvas):
                The canvas object to update.
        """
        # if self.is_light_theme:
        #     bordercolor = self.colors.border
        # else:
        #     bordercolor = self.colors.selectbg

        widget.configure(
            background=self.colors.bg,
            highlightthickness=0,
            # highlightbackground=bordercolor,
        )

    def update_button_style(self, widget: tk.Button):
        """Update the button style.

        Parameters:

            widget (tkinter.Button):
                The button object to update.
        """
        background = self.colors.primary
        foreground = _accent_on_color(background)
        activebackground = Colors.update_hsv(self.colors.primary, vd=-0.1)

        widget.configure(
            background=background,
            foreground=foreground,
            relief="flat",
            borderwidth=0,
            activebackground=activebackground,
            highlightbackground=foreground,
        )

    def update_label_style(self, widget: tk.Label):
        """Update the label style.

        Parameters:

            widget (tkinter.Label):
                The label object to update.
        """
        widget.configure(foreground=self.colors.fg, background=self.colors.bg)

    def update_frame_style(self, widget: tk.Frame):
        """Update the frame style.

        Parameters:

            widget (tkinter.Frame):
                The frame object to update.
        """
        widget.configure(background=self.colors.bg)

    def update_checkbutton_style(self, widget: tk.Checkbutton):
        """Update the checkbutton style.

        Parameters:

            widget (tkinter.Checkbutton):
                The checkbutton object to update.
        """
        widget.configure(
            activebackground=self.colors.bg,
            activeforeground=self.colors.primary,
            background=self.colors.bg,
            foreground=self.colors.fg,
            selectcolor=self.colors.bg,
        )

    def update_radiobutton_style(self, widget: tk.Radiobutton):
        """Update the radiobutton style.

        Parameters:

            widget (tkinter.Radiobutton):
                The radiobutton object to update.
        """
        widget.configure(
            activebackground=self.colors.bg,
            activeforeground=self.colors.primary,
            background=self.colors.bg,
            foreground=self.colors.fg,
            selectcolor=self.colors.bg,
        )

    def update_entry_style(self, widget: tk.Entry):
        """Update the entry style.

        Parameters:

            widget (tkinter.Entry):
                The entry object to update.
        """
        bordercolor = self.colors.border

        widget.configure(
            relief="flat",
            highlightthickness=self.style.scaling.logical(1),
            foreground=self.colors.inputfg,
            highlightbackground=bordercolor,
            highlightcolor=self.colors.primary,
            background=self.colors.inputbg,
            insertbackground=self.colors.inputfg,
            insertwidth=self.style.scaling.logical(1),
        )

    def update_scale_style(self, widget: tk.Scale):
        """Update the scale style.

        Parameters:

            widget (tkinter.Scale):
                The scale object to update.
        """
        bordercolor = self.colors.border

        activecolor = Colors.update_hsv(self.colors.primary, vd=-0.2)
        widget.configure(
            background=self.colors.primary,
            showvalue=False,
            sliderrelief="flat",
            borderwidth=0,
            activebackground=activecolor,
            highlightthickness=self.style.scaling.logical(1),
            highlightcolor=bordercolor,
            highlightbackground=bordercolor,
            troughcolor=self.colors.inputbg,
        )

    def update_spinbox_style(self, widget: tk.Spinbox):
        """Update the spinbox style.

        Parameters:

            widget (tkinter.Spinbox):
                The spinbox object to update.
        """
        bordercolor = self.colors.border

        widget.configure(
            relief="flat",
            highlightthickness=self.style.scaling.logical(1),
            foreground=self.colors.inputfg,
            highlightbackground=bordercolor,
            highlightcolor=self.colors.primary,
            background=self.colors.inputbg,
            buttonbackground=self.colors.inputbg,
            insertbackground=self.colors.inputfg,
            insertwidth=self.style.scaling.logical(1),
            # these options should work, but do not have any affect
            buttonuprelief="flat",
            buttondownrelief="sunken",
        )

    def update_listbox_style(self, widget: tk.Listbox):
        """Update the listbox style.

        Parameters:

            widget (tkinter.Listbox):
                The listbox object to update.
        """
        bordercolor = self.colors.border

        widget.configure(
            foreground=self.colors.inputfg,
            background=self.colors.inputbg,
            selectbackground=self.colors.selectbg,
            selectforeground=self.colors.selectfg,
            highlightcolor=self.colors.primary,
            highlightbackground=bordercolor,
            highlightthickness=self.style.scaling.logical(1),
            activestyle="none",
            relief="flat",
        )

    def update_menubutton_style(self, widget: tk.Menubutton):
        """Update the menubutton style.

        Parameters:

            widget (tkinter.Menubutton):
                The menubutton object to update.
        """
        activebackground = Colors.update_hsv(self.colors.primary, vd=-0.2)
        widget.configure(
            background=self.colors.primary,
            foreground=_accent_on_color(self.colors.primary),
            activebackground=activebackground,
            activeforeground=_accent_on_color(activebackground),
            borderwidth=0,
        )

    def update_menu_style(self, widget: tk.Menu):
        """Update the menu style.

        Parameters:

            widget (tkinter.Menu):
                The menu object to update.
        """
        widget.configure(
            tearoff=False,
            activebackground=self.colors.selectbg,
            activeforeground=self.colors.selectfg,
            foreground=self.colors.fg,
            selectcolor=self.colors.primary,
            background=self.colors.bg,
            relief="flat",
            borderwidth=0,
        )

    def update_labelframe_style(self, widget: tk.LabelFrame):
        """Update the labelframe style.

        Parameters:

            widget (tkinter.LabelFrame):
                The labelframe object to update.
        """
        bordercolor = self.colors.border

        widget.configure(
            highlightcolor=bordercolor,
            foreground=self.colors.fg,
            borderwidth=self.style.scaling.logical(1),
            highlightthickness=0,
            background=self.colors.bg,
        )

    def update_text_style(self, widget: tk.Text):
        """Update the text style.

        Only the colors are themed; the border/relief is intentionally left at
        tk's default so a surrounding container can own it -- `ScrolledText`
        draws a single card border and keeps the inner `Text` borderless. A
        standalone `Text` keeps its native border; set `highlightthickness` /
        `highlightbackground` yourself for a themed one.

        Parameters:

            widget (tkinter.Text):
                The text object to update.
        """
        widget.configure(
            background=self.colors.inputbg,
            foreground=self.colors.inputfg,
            insertbackground=self.colors.inputfg,
            selectbackground=self.colors.selectbg,
            selectforeground=self.colors.selectfg,
            insertwidth=self.style.scaling.logical(1),
            padx=self.style.scaling.logical(5),
            pady=self.style.scaling.logical(5),
        )
