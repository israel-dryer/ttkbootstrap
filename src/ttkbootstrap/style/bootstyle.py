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
    tk.Button,
    tk.Label,
    tk.Text,
    tk.Frame,
    tk.Tk,
    # tk.Listbox,
    # tk.OptionMenu
)


def override_ttk_widget_constructor(func):
    """Override widget constructors with bootstyle api options"""

    def __init__wrapper(self, *args, **kwargs):

        # capture bootstyle and style arguments
        if 'bootstyle' in kwargs:
            bootstyle = kwargs.pop('bootstyle')
        else:
            bootstyle = ''

        if 'style' in kwargs:
            style = kwargs.get('style')
        else:
            style = ''

        # instantiate the widget
        func(self, *args, **kwargs)
        
        # must be called AFTER instantiation in order to use winfo_class
        #    in the `get_ttkstyle_name` method

        if style:
            ttkstyle = update_ttk_widget_style(self, style, **kwargs)
            self.configure(style=ttkstyle)
        elif bootstyle:
            ttkstyle = update_ttk_widget_style(self, bootstyle, **kwargs)
            self.configure(style=ttkstyle)

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
        if 'bootstyle' in kwargs:
            bootstyle = kwargs.pop('bootstyle')
        else:
            bootstyle = ''
        
        if 'style' in kwargs:
            style = kwargs.get('style')
            ttkstyle = update_ttk_widget_style(self, style, **kwargs)
        elif bootstyle:
            ttkstyle = update_ttk_widget_style(self, bootstyle, **kwargs)
            kwargs.update(style=ttkstyle)

        # update widget configuration
        func(self, **kwargs)

    return configure_wrapper


def update_ttk_widget_style(widget: ttk.Widget, style_string: str=None, **kwargs):
    """Update the ttk style or create if not existing.

    Parameters
    ----------
    widget: ttk.Widget
        The widget instance being updated.

    style_string : str
        The style string to evalulate. May be the `style`, `ttkstyle`
        or `bootstyle` argument depending on the context and scenario.

    **kwargs: Dict[str, Any]
        Other keyword arguments.

    Returns
    -------
    ttkstyle : str
        The ttkstyle or empty string if there is none.
    """
    style: Style = Style.get_instance()

    # get existing widget style if not provided
    if style_string is None:
        style_string = widget.cget('style')

    # do nothing if the style has not been set
    if not style_string:
        return ''

    # build style if not existing (example: theme changed)
    ttkstyle = util.ttkstyle_name(widget, style_string, **kwargs)
    if not style.exists(ttkstyle):
        widget_color = util.ttkstyle_widget_color(ttkstyle)
        method_name = util.ttkstyle_method_name(widget, ttkstyle)
        builder: StyleBuilderTTK = style.get_builder()
        builder_method = builder.name_to_method(method_name)
        builder_method(builder, widget_color)
    return ttkstyle


def setup_ttkbootstap_api():
    """Setup ttkbootstrap for use with tkinter and ttk"""
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

        # override destroy method
        widget.destroy = override_widget_destroy_method

    # TK WIDGETS
    for widget in TK_WIDGETS:

        # override widget constructor
        __init = override_tk_widget_constructor(widget.__init__)
        widget.__init__ = __init

        # override widget destroy method (quit for tk.Tk)
        if issubclass(widget, tk.Widget):
            widget.destroy = override_widget_destroy_method
        elif issubclass(widget, tk.Tk):
            widget.quit = override_widget_destroy_method


def override_tk_widget_constructor(func):
    """Override widget constructors to apply default style for tk 
    widgets
    """

    def __init__wrapper(self, *args, **kwargs):

        # instantiate the widget
        func(self, *args, **kwargs)
        update_tk_widget_style(self)

        # subscriber to <<ThemeChanged>> events
        if isinstance(self, tk.Tk):
            name = '.'
        else:
            name = self._name

        Publisher.subscribe(
            name=name,
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
    method_name = util.tkupdate_method_name(widget)
    builder: StyleBuilderTK = Style.get_builder_tk()
    builder_method = builder.name_to_method(method_name)
    builder_method(builder, widget)


def override_widget_destroy_method(self):
    """Unsubscribe widget from publication and destroy"""
    if isinstance(self, tk.Widget):
        Publisher.unsubscribe(self._name)
        tk.Widget.destroy(self)
    elif isinstance(self, tk.Tk):
        Publisher.__subscribers.clear()
        tk.Tk.quit(self)