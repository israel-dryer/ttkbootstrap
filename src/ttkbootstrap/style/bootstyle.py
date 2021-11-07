import tkinter as tk
from tkinter import ttk
from ttkbootstrap.constants import DEFAULT
from ttkbootstrap.style.style import Style
from ttkbootstrap.style.style_builder import StyleBuilderTK, StyleBuilderTTK
import ttkbootstrap.style.utility as util
from ttkbootstrap.style.publisher import Publisher, Channel

TTK_WIDGETS = (
    ttk.Button,
    ttk.Checkbutton,
    ttk.Combobox,
    ttk.Entry,
    ttk.Frame,
    ttk.Label,
    ttk.Labelframe,
    ttk.Menubutton,
    ttk.Notebook,
    # ttk.OptionMenu,
    ttk.Panedwindow,
    ttk.Progressbar,
    ttk.Radiobutton,
    ttk.Scale,
    ttk.Scrollbar,
    ttk.Separator,
    ttk.Sizegrip,
    ttk.Spinbox,
    ttk.Treeview
)

TK_WIDGETS = (
    # tk.Button,
    # tk.Frame,
    # tk.Label,
    # tk.Listbox,
    tk.Text,
    # tk.OptionMenu
)


def override_ttk_widget_constructor(func):
    """Override widget constructors with bootstyle api options"""

    def __init__wrapper(self, *args, **kwargs):

        ttkstyle = util.get_ttkstyle_name(self, **kwargs)

        if ttkstyle:
            kwargs.update(style=ttkstyle)

        if 'bootstyle' in kwargs:
            kwargs.pop('bootstyle')

        # instantiate the widget
        func(self, *args, **kwargs)

        # create style if not existing
        if ttkstyle is not None:
            update_ttk_widget_style(self, ttkstyle)

        # subscriber to <<ThemeChanged>> events
        Publisher.subscribe(
            name=self._name,
            func=lambda widget=self: update_ttk_widget_style(widget),
            channel=Channel.TTK
        )

    return __init__wrapper


def override_ttk_widget_configure(func):

    def configure_wrapper(self, cnf=None, **kwargs):
        # get configuration
        if cnf == 'bootstyle':
            return func(self, 'style')
        elif cnf is not None:
            return func(self, cnf)

        # set configuration
        ttkstyle = util.get_ttkstyle_name(self, **kwargs)
        if ttkstyle:
            kwargs.update(style=ttkstyle)
            update_ttk_widget_style(self, ttkstyle)

        if 'bootstyle' in kwargs:
            kwargs.pop('bootstyle')

        func(self, **kwargs)

    return configure_wrapper


def update_ttk_widget_style(widget: ttk.Widget, style_string: str = None):
    """Update the ttk style or create if not existing.

    Parameters
    ----------
    widget: ttk.Widget
        The widget instance being updated.

    style_string : str
        The style string to evalulate. May be the `style`, `ttkstyle`
        or `bootstyle` argument depending on the context and scenario.
    """
    style: Style = Style.get_instance()

    # get widget style if not provided
    if style_string is None:
        style_string = widget.cget('style')

    # do nothing if the style has not been set
    if not style_string:
        return

    # build style if not existing
    style_string += util.normalize_bootstyle(style_string, widget)
    ttkstyle = util.ttkstyle_name_from_string(style_string)
    if not style.exists(ttkstyle):
        widget_color = util.widget_color_from_string(ttkstyle)
        method_name = util.ttkstyle_method_name_from_string(ttkstyle)
        builder: StyleBuilderTTK = style.get_builder()
        builder_method = builder.name_to_method(method_name)
        builder_method(builder, widget_color)


def setup_ttkbootstap_api():
    
    # TTK WIDGETS
    for widget in TTK_WIDGETS:
        # override widget constructor
        __init = override_ttk_widget_constructor(widget.__init__)
        widget.__init__ = __init

        # override configure method
        __configure = override_ttk_widget_configure(widget.configure)
        widget.configure = __configure

        # override get and set methods
        def __setitem(self, key, val): return __configure(self, **{key: val})
        def __getitem(self, key): return __configure(self, cnf=key)
        widget.__setitem__ = __setitem
        widget.__getitem__ = __getitem

    # TK WIDGETS
    for widget in TK_WIDGETS:

        # override widget constructor
        __init = override_tk_widget_constructor(widget.__init__)
        widget.__init__ = __init


def override_tk_widget_constructor(func):
    """Override widget constructors to apply default style for tk 
    widgets
    """

    def __init__wrapper(self, *args, **kwargs):

        # instantiate the widget
        func(self, *args, **kwargs)
        update_tk_widget_style(self)

        # subscriber to <<ThemeChanged>> events
        Publisher.subscribe(
            name=self._name,
            func=lambda widget=self: update_tk_widget_style(widget),
            channel=Channel.STD
        )
    return __init__wrapper

def update_tk_widget_style(widget: tk.Widget):
    """Update the tk widget style

    Parameters
    ----------
    widget: tk.Widget
        The widget instance being updated.
    """
    print(widget.cget('background'))
    style: Style = Style.get_instance()
    widget_class = widget.__class__.__name__
    method_name = util.tkupdate_method_name_from_string(widget_class)
    builder: StyleBuilderTK = style.get_builder_tk()
    builder_method = builder.name_to_method(method_name)
    builder_method(builder, widget)
