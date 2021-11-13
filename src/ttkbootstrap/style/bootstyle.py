import tkinter as tk
from tkinter import ttk
import ttkbootstrap.style.utility as util
from ttkbootstrap.style.style import Style
from ttkbootstrap.style.style_builder import StyleBuilderTK, StyleBuilderTTK
from ttkbootstrap.style.publisher import Publisher, Channel

TTK_WIDGETS = (
    ttk.Button,
    ttk.Checkbutton,
    ttk.Combobox,
    ttk.Entry,
    ttk.Frame,
    ttk.Labelframe,
    ttk.Label,
    ttk.Menubutton,
    ttk.Notebook,
    ttk.Panedwindow,
    ttk.Progressbar,
    ttk.Radiobutton,
    ttk.Scale,
    ttk.Scrollbar,
    ttk.Separator,
    ttk.Sizegrip,
    ttk.Spinbox,
    ttk.Treeview,
    ttk.OptionMenu,
)

TK_WIDGETS = (
    tk.Tk,
    tk.Toplevel,
    tk.Button,
    tk.Label,
    tk.Text,
    tk.Frame,
    tk.Checkbutton,
    tk.Radiobutton,
    tk.Entry,
    tk.Scale,
    tk.Spinbox,
    tk.Listbox,
    tk.Menu,
    tk.Menubutton,
    tk.LabelFrame,
    tk.Canvas
)


def override_ttk_widget_constructor(func):
    """Override widget constructors with bootstyle api options"""

    def __init__(self, *args, **kwargs):

        # capture bootstyle and style arguments
        if 'bootstyle' in kwargs:
            bootstyle = kwargs.pop('bootstyle')
        else:
            bootstyle = ''

        if 'style' in kwargs:
            style = kwargs.pop('style') or ''
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
        else:
            ttkstyle = update_ttk_widget_style(self, 'default', **kwargs)
            self.configure(style=ttkstyle)

    return __init__


def override_ttk_widget_configure(func):

    def configure(self, cnf=None, **kwargs):
        # get configuration
        if cnf == 'bootstyle':
            return self.cget('style')
        elif cnf is not None:
            return self.cget(cnf)

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

    return configure


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
    style = Style()

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

    # subscribe popdown style to theme changes
    if widget.winfo_class() == 'TCombobox':
        builder: StyleBuilderTTK = style.get_builder()
        Publisher.subscribe(
            name=widget._name, 
            func=lambda w=widget: builder.update_combobox_popdown_style(w), 
            channel=Channel.STD
        )
        builder.update_combobox_popdown_style(widget)

    return ttkstyle


def setup_ttkbootstap_api():
    """Setup ttkbootstrap for use with tkinter and ttk"""

    # TTK WIDGETS
    for widget in TTK_WIDGETS:
        # override widget constructor
        _init = override_ttk_widget_constructor(widget.__init__)
        widget.__init__ = _init

        # override configure method
        _configure = override_ttk_widget_configure(widget.configure)
        widget.configure = _configure

        # override get and set methods
        def __setitem(self, key, val): return _configure(self, **{key: val})
        def __getitem(self, key): return _configure(self, cnf=key)
        if widget.__name__ != 'OptionMenu': # this has it's own override
            widget.__setitem__ = __setitem
            widget.__getitem__ = __getitem

    # TK WIDGETS
    for widget in TK_WIDGETS:

        # override widget constructor
        _init = override_tk_widget_constructor(widget.__init__)
        widget.__init__ = _init

        # override widget destroy method (quit for tk.Tk)
        widget.destroy = override_widget_destroy_method

def update_tk_widget_style(widget):
    """Lookup the widget name and call the appropriate update 
    method
    
    Parameters
    ----------
    widget : object
        The tcl/tk name given by `tk.Widget.winfo_name()`
    """
    try:
        style = Style()
        method_name = util.tkupdate_method_name(widget)
        builder = style.get_builder_tk()
        builder_method = getattr(StyleBuilderTK, method_name)
        builder_method(builder, widget)
    except:
        """Must pass here to prevent a failure when the user calls
        the `Style`method BEFORE an instance of `Tk` is instantiated.
        This will defer the update of the `Tk` background until the end
        of the `BootStyle` object instantiation (created by the `Style`
        method)"""
        pass


def override_tk_widget_constructor(func):
    """Override widget constructors to apply default style for tk 
    widgets
    """

    def __init__wrapper(self, *args, **kwargs):

        # instantiate the widget
        func(self, *args, **kwargs)
        
        Publisher.subscribe(
            name=str(self),
            func=lambda w=self: update_tk_widget_style(w),
            channel=Channel.STD
        )
        update_tk_widget_style(self)

    return __init__wrapper


def override_widget_destroy_method(self):
    """Unsubscribe widget from publication and destroy"""
    if isinstance(self, tk.Widget):
        Publisher.unsubscribe(self._name)
        super(tk.Widget, self).destroy()
    elif isinstance(self, tk.Tk):
        Publisher.clear_subscribers()
        super(tk.Tk, self).quit()
    elif isinstance(self, tk.Toplevel):
        Publisher.clear_subscribers()
        super(tk.Toplevel, self).destroy()
