import tkinter as tk
from tkinter import ttk
import re

WIDGET_LOOKUP = {
    "button": "TButton",
    "btn": "TButton",
    "progressbar": "TProgressbar",
    "progress": "TProgressbar",
    "check": "TCheckbutton",
    "checkbutton": "TCheckbutton",
    "checkbtn": "TCheckbutton",
    "combo": "TCombobox",
    "combobox": "TCombobox",
    "entry": "TEntry",
    "frame": "TFrame",
    "inputframe": "Input.TFrame",
    "floodgauge": "TFloodgauge",
    "gauge": "TFloodgauge",
    "grip": "TSizegrip",
    "lbl": "TLabel",
    "labelframe": "TLabelframe",
    "lblframe": "TLabelframe",
    "lblfrm": "TLabelframe",
    "label": "TLabel",
    "menubutton": "TMenubutton",
    "radio": "TRadiobutton",
    "radiobutton": "TRadiobutton",
    "radiobtn": "TRadiobutton",
    "round": "Roundtoggle.Toolbutton",
    "roundtoggle": "Roundtoggle.Toolbutton",
    "roundedtoggle": "Roundtoggle.Toolbutton",
    "separator": "TSeparator",
    "scrollbar": "TScrollbar",
    "sizegrip": "TSizegrip",
    "spinbox": "TSpinbox",
    "scale": "TScale",
    "slider": "TScale",
    "square": "Squaretoggle.Toolbutton",
    "squaretoggle": "Squaretoggle.Toolbutton",
    "squaredtoggle": "Squaretoggle.Toolbutton",
    "toggle": "Toggle.Toolbutton",
    "toolbutton": "Toolbutton",
    "tool": "Toolbutton",
    "tree": "Treeview",
    "treeview": "Treeview",
}

WIDGET_PATTERN = "|".join(WIDGET_LOOKUP.keys())
COLOR_PATTERN = re.compile(r"primary|secondary|success|info|warning|danger|light|dark")
ORIENT_PATTERN = re.compile(r"horizontal|vertical")
STYLE_PATTERN = re.compile(
    r"outline|link|inverse|rounded|striped|squared|focusframe"
)

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


def __setitem(widget, key, value):
    widget.configure(**{key: value})


def __getitem(widget, key):
    if 'bootstyle' in key:
        return getattr(widget, '_bootstyle')
    else:
        return widget.tk.call(widget.name, 'configure', '-'+key)


def inject_bootstyle_keyword_api():
    """Inject the style keyword API into the ttk widget constructor
    and widget configure method
    """

    def bootstyle_wrapper(widget, func):

        # create private variable for bootstyle
        setattr(widget, '_bootstyle', '')

        def inner(*args, **kwargs):
            # use style if exists; remove bootstyle in this case
            if 'style' in kwargs:
                if 'bootstyle' in kwargs:
                    kwargs.pop('bootstyle')
                func(*args, **kwargs)

            # parse the bootstyle keywords to create a ttk style
            elif 'bootstyle' in kwargs:

                # save a copy of the bootstyle keywords
                widget._bootstyle = kwargs.pop('bootstyle')

                # get widget class and orientation
                _class = widget.__name__
                _orient = kwargs.get('orient')

                # standardize the orientation naming convention
                if _orient == 'h':
                    _orient = tk.HORIZONTAL
                elif _orient == 'v':
                    _orient = tk.VERTICAL

                # create and set the ttk style
                ttkstyle = create_ttk_style(
                    bootstyle=widget._bootstyle,
                    widget_class=_class,
                    widget_orient=_orient
                )
                func(*args, style=ttkstyle, **kwargs)
            else:
                # neither `style` or `bootstyle` arguments are present
                # pass through to the enclosed method
                func(*args, **kwargs)
        return inner

    for widget in TTK_WIDGETS:
        widget.__init__ = bootstyle_wrapper(widget, widget.__init__)
        widget.configure = bootstyle_wrapper(widget, widget.configure)
        widget.config = widget.configure
        # widget.__setitem__ = __setitem
        # widget.__getitem__ = __getitem


def normalize_style(bootstyle):
    """Remove all spaces and capitalization in the style keywords and
    return the resulting string
    Parameters
    ----------
    bootstyle : Union[str, Iterable]
        A string of widget style keywords.

    Returns
    -------
    str
        A string with all spaces and capitalization removed.
    """
    if bootstyle:
        return "".join(bootstyle).lower()
    else:
        return ""


def find_bootstyle_widget_class(style_keywords, widget_class) -> str:
    """Extract and return the widget class.
    The matching style is based on a regex pattern match from widget
    types in the WIDGET_PATTERN constant. If not found, then the
    fallback widget_class is returned.
    The reason for this distinction is because it is possible to style
    one type of widget with the style of another... for example, one
    can use a TButton style on a TLabel widget and inherit the hover
    effects, etc... from the button on the label. So, the expected
    style widget class must be evaluated before falling back to the
    actual widget_class of the widget.

    Parameters
    ----------
    style_keywords : str
        A string of widget style keywords.

    widget_class : str
        The Class.function name from which the widget class will be
        derived.

    Returns
    -------
    str
        The matching widget_class pattern or the fallback widget
        class.
    """
    widget_class_match = re.search(WIDGET_PATTERN, widget_class.lower())
    bootstyle_match = re.search(WIDGET_PATTERN, style_keywords.lower())

    if bootstyle_match:
        return WIDGET_LOOKUP.get(bootstyle_match.group(0))
    else:
        return WIDGET_LOOKUP.get(widget_class_match.group(0))


def find_widget_color(style_keywords):
    """Extract and return the style color from the style keywords.
    The matching color is based on a regex pattern match from color
    patterns in the COLOR_PATTERN constant.
    Parameters
    ----------
    style_keywords: str
        A string of widget style keywords.

    Returns
    -------
    str
        A matching style color.
    """
    match = re.search(COLOR_PATTERN, style_keywords)
    return "" if not match else match.group(0) + "."


def find_bootstyle_orient(style_keywords, widget_class, orient=None):
    """Extract, modify, and return the widget style orientation.
    Returns a lowercased orientation appended with a "." if an
    orientation is present. This is required to build the style name
    provided to ttk. Otherwise, an empty string is returned.
    """
    if tk.HORIZONTAL in style_keywords.lower():
        return 'Horizontal.'
    if tk.VERTICAL in style_keywords.lower():
        return 'Vertical.'
    if orient is not None:
        return f"{orient.title()}."
    elif widget_class in ["TProgressbar", "TScale", "TSeparator"]:
        return "Horizontal."
    elif widget_class in ["TPanedwindow", "TScrollbar"]:
        return "Vertical."
    else:
        return ""


def find_bootstyle_type(style_keywords):
    """Extract and return the style type from the style keywords.
    The matching style is based on a regex pattern match from style
    types in the STYLE_PATTERN constant. If found, a "." is appended to
    the end so that a ttk style can be built. Otherwise, an empty
    string is returned.
    Parameters
    ----------
    style_keywords: str
        A string of widget style keywords.

    Returns
    -------
    str
        A matching style style.
    """
    match = re.search(STYLE_PATTERN, style_keywords)
    return "" if not match else match.group(0).title() + "."


def create_ttk_style(bootstyle, widget_class, widget_orient=None):
    """Parse the raw style keywords and build a real ttk style name
    that will be used when building the widget style. These style
    keywords trigger different settings and procedures in the
    theme_builder.
    """
    style_keywords = normalize_style(bootstyle)
    _color = find_widget_color(style_keywords)
    _type = find_bootstyle_type(style_keywords)
    _class = find_bootstyle_widget_class(style_keywords, widget_class)
    _orient = find_bootstyle_orient(style_keywords, _class, widget_orient)
    return f"{_color}{_type}{_orient}{_class}"
