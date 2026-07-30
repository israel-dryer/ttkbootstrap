"""Legacy ``tk.*`` widget styler for ttkbootstrap.

`StyleBuilderTK` styles the non-ttk widgets (Menu, Text, Canvas, ...) to match
the active theme. Split out of the monolithic `style.py` in 2.0.
"""
import tkinter as tk

from ttkbootstrap.constants import *
from ttkbootstrap.style.theme import Colors, ThemeDefinition, _accent_on_color

# Carries the menu-border repaint. A bind tag of our own rather than a binding on
# the widget, so a caller's own bind("<Map>") cannot displace it.
_MENU_HAIRLINE_TAG = "TtkbootstrapMenuHairline"


def _on_menu_map(event):
    """Repaint a popup menu's border as it is posted.

    Entries added since the last post inherit the menu background, so they would
    come up in the border color; this catches them before the menu is drawn.
    """
    from ttkbootstrap.style.engine import Style

    try:
        builder = Style.get_instance()._get_builder_tk()
        builder._paint_menu_hairline(event.widget)
    except (AttributeError, tk.TclError):
        # A menu torn down mid-post, or posted before a theme exists, keeps its
        # plain background rather than failing the post.
        pass


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

        On x11 the popup also gets the themed 1px border -- see
        `_paint_menu_hairline` for how it is drawn and why it waits for `<Map>`.
        Windows and macOS draw menus with the native OS chrome, which supplies
        the border, so they keep the borderless configuration.

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
        if self.style.scaling.windowing_system == "x11":
            self._arm_menu_hairline(widget)

    def _arm_menu_hairline(self, widget: tk.Menu):
        """Reserve the border strip and arrange for it to be painted on `<Map>`.

        The width is set now so posting the menu never has to re-run its
        geometry; while the strip is still the surface color it is invisible.
        """
        widget.configure(borderwidth=self.style.scaling.logical(1))

        if _MENU_HAIRLINE_TAG not in widget.bindtags():
            widget.bindtags((_MENU_HAIRLINE_TAG,) + widget.bindtags())
        if not widget.tk.call("bind", _MENU_HAIRLINE_TAG):
            widget.bind_class(_MENU_HAIRLINE_TAG, "<Map>", _on_menu_map)

        # A menu already posted once keeps its border across a theme change;
        # one that has never been posted waits, so a menubar is never painted.
        if getattr(widget, "_tb_menu_hairline", False):
            self._paint_menu_hairline(widget)

    def _paint_menu_hairline(self, widget: tk.Menu):
        """Draw the themed 1px border around a popup menu.

        Tk gives `tk.Menu` no border color of its own: it has no
        `highlightthickness`, `relief="solid"` is hardcoded to black, and the 3D
        reliefs derive their two shades from `-background`. The one way to a flat
        border in `colors.border` is to paint the *menu* in the border color and
        every entry in the surface color -- entries tile the whole interior of a
        popup, so only the 1px strip is left showing.

        That only holds for a popup. A menubar's entries cover just the left of
        the bar, so the border color would flood the rest of it -- which is why
        this waits for `<Map>`: a menu used as a menubar is displayed through a
        clone, so the widget styled here never maps and never gets painted.

        Entry colors are theme-managed, like those of a themed `Text`. An entry
        the user gave its own color keeps it; the rest follow the theme.
        """
        surface = self.colors.bg
        previous = getattr(widget, "_tb_menu_entry_bg", None)
        widget.configure(background=self.colors.border)

        end = widget.index("end")
        for index in range(0 if end is None else end + 1):
            current = str(widget.entrycget(index, "background"))
            if not current or current == previous:
                widget.entryconfigure(index, background=surface)

        widget._tb_menu_entry_bg = surface
        widget._tb_menu_hairline = True

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

        A standalone `Text` gets a flat, themed 1px border (matching the input
        widgets) in place of tk's native sunken relief. A container that owns
        the border -- `ScrolledText` draws a single card border around the text
        and scrollbar -- marks its inner `Text` with `_tb_borderless` to keep it
        edgeless so the two borders don't stack.

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
        if getattr(widget, "_tb_borderless", False):
            widget.configure(
                relief="flat", borderwidth=0, highlightthickness=0,
            )
        else:
            widget.configure(
                relief="flat",
                borderwidth=0,
                highlightthickness=self.style.scaling.logical(1),
                highlightbackground=self.colors.border,
                highlightcolor=self.colors.primary,
            )
