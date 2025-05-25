"""
    Simple themed tkinter widgets.

    These widgets provide a basic default style that is consistent with the overall applied
    theme. They are used internally in some places where the legacy api is required, but
    may be used as needed by UI developers as well.

    The widgets are themed by default, but you may disable this behavior the setting
    the `themed` option to False.
"""
import tkinter as tk

from ttkbootstrap.style.theme_manager import get_theme_manager


def apply_style(handler: str, widget: tk.Misc):
    manager = get_theme_manager()
    manager.active_theme.execute_handler(handler, widget)


class TkButton(tk.Button):
    def __init__(self, master=None, themed=True, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        if themed:
            apply_style('tk.button', self)
            self.bind("<<ThemeChanged>>", lambda _: apply_style('tk.button', self))


class TkCanvas(tk.Canvas):
    def __init__(self, master=None, themed=True, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        if themed:
            apply_style('tk.canvas', self)
            self.bind("<<ThemeChanged>>", lambda _: apply_style('tk.canvas', self))


class TkCheckBox(tk.Checkbutton):
    def __init__(self, master=None, themed=True, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        if themed:
            apply_style('tk.checkbutton', self)
            self.bind("<<ThemeChanged>>", lambda _: apply_style('tk.checkbutton', self))


class TkTextBox(tk.Entry):
    def __init__(self, master=None, themed=True, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        if themed:
            apply_style('tk.entry', self)
            self.bind("<<ThemeChanged>>", lambda _: apply_style('tk.entry', self))


class TkFrame(tk.Frame):
    def __init__(self, master=None, themed=True, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        if themed:
            apply_style('tk.frame', self)
            self.bind("<<ThemeChanged>>", lambda _: apply_style('tk.frame', self))


class TkLabel(tk.Label):
    def __init__(self, master=None, themed=True, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        if themed:
            apply_style('tk.label', self)
            self.bind("<<ThemeChanged>>", lambda _: apply_style('tk.label', self))


class TkLabelFrame(tk.LabelFrame):
    def __init__(self, master=None, themed=True, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        if themed:
            apply_style('tk.labelframe', self)
            self.bind("<<ThemeChanged>>", lambda _: apply_style('tk.labelframe', self))


class TkListBox(tk.Listbox):
    def __init__(self, master=None, themed=True, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        if themed:
            apply_style('tk.listbox', self)
            self.bind("<<ThemeChanged>>", lambda _: apply_style('tk.listbox', self))


class TkMenu(tk.Menu):
    def __init__(self, master=None, themed=True, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        if themed:
            apply_style('tk.menu', self)
            self.bind("<<ThemeChanged>>", lambda _: apply_style('tk.menu', self))


class TkMenuButton(tk.Menubutton):
    def __init__(self, master=None, themed=True, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        if themed:
            apply_style('tk.menubutton', self)
            self.bind("<<ThemeChanged>>", lambda _: apply_style('tk.menubutton', self))


class TkRadio(tk.Radiobutton):
    def __init__(self, master=None, themed=True, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        if themed:
            apply_style('tk.radiobutton', self)
            self.bind("<<ThemeChanged>>", lambda _: apply_style('tk.radiobutton', self))


class TkScale(tk.Scale):
    def __init__(self, master=None, themed=True, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        if themed:
            apply_style('tk.scale', self)
            self.bind("<<ThemeChanged>>", lambda _: apply_style('tk.scale', self))


class TkSpinBox(tk.Spinbox):
    def __init__(self, master=None, themed=True, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        if themed:
            apply_style('tk.spinbox', self)
            self.bind("<<ThemeChanged>>", lambda _: apply_style('tk.spinbox', self))


class TkText(tk.Text):
    def __init__(self, master=None, themed=True, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        if themed:
            apply_style('tk.text', self)
            self.bind("<<ThemeChanged>>", lambda _: apply_style('tk.text', self))


class TkTopLevel(tk.Toplevel):
    def __init__(self, master=None, themed=True, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        if themed:
            apply_style('tk.toplevel', self)
            self.bind("<<ThemeChanged>>", lambda _: apply_style('tk.toplevel', self))
