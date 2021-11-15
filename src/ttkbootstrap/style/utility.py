import re

COLORS = [
    'primary',
    'secondary',
    'success',
    'info',
    'warning',
    'danger',
    'light',
    'dark'
]

ORIENTS = [
    'horizontal',
    'vertical'
]

TYPES = [
    'outline',
    'link',
    'inverse',
    'round',
    'square',
    'striped',
    'focus',
    'input',
    'date',
    'meter'
]

CLASSES = [
    'button',
    'progressbar',
    'checkbutton',
    'combobox',
    'entry',
    'labelframe',
    'label',
    'frame',
    'floodgauge',
    'sizegrip',
    'optionmenu',
    'menubutton',
    'menu',
    'notebook',
    'panedwindow',
    'radiobutton',
    'separator',
    'scrollbar',
    'spinbox',
    'scale',
    'text',
    'toolbutton',
    'treeview',
    'toggle',
    'tk',
    'calendar',
    'listbox',
    'canvas',
    'toplevel'
]

# regex patterns
COLOR_PATTERN = re.compile('|'.join(COLORS))
ORIENT_PATTERN = re.compile('|'.join(ORIENTS))
CLASS_PATTERN = re.compile('|'.join(CLASSES))
TYPE_PATTERN = re.compile('|'.join(TYPES))

# ttkstyle namebuilder helper methods

def ttkstyle_widget_class(widget=None, string=''):
    """Find and return the widget class"""
    # find widget class from string pattern
    match = re.search(CLASS_PATTERN, string.lower())
    if match is not None:
        widget_class = match.group(0)
        return widget_class

    # find widget class from tkinter/tcl method
    if widget is None:
        return ''
    _class = widget.winfo_class()
    match = re.search(CLASS_PATTERN, _class.lower())
    if match is not None:
        widget_class = match.group(0)
        return widget_class
    else:
        return ''

def ttkstyle_widget_type(string):
    """Find and return the widget type"""
    match = re.search(TYPE_PATTERN, string.lower())
    if match is None:
        return ''
    else: 
        widget_type = match.group(0)
        return widget_type

def ttkstyle_widget_orient(widget=None, string='', **kwargs):
    """Find and return widget orient, or default orient for widget if
    a widget with orientation.
    """
    # string method (priority)
    match = re.search(ORIENT_PATTERN, string)
    widget_orient = ''

    if match is not None:
        widget_orient = match.group(0)
        return widget_orient

    # orient from kwargs
    if 'orient' in kwargs:
        _orient = kwargs.pop('orient')
        if _orient == 'h':
            widget_orient = 'horizontal'
        elif _orient == 'v':
            widget_orient = 'vertical'
        else:
            widget_orient = _orient
        return widget_orient
        
    # orient from settings
    if widget is None:
        return widget_orient
    try:
        widget_orient = str(widget.cget('orient'))
    except:
        pass

    return widget_orient

def ttkstyle_widget_color(string):
    """Find and return widget color"""
    _color = re.search(COLOR_PATTERN, string.lower())
    if _color is None:
        return ''
    else:
        widget_color = _color.group(0)
        return widget_color

def ttkstyle_name(widget=None, string='', **kwargs):
    """Parse a string to build and return a ttkstyle name."""
    style_string = ''.join(string).lower()
    widget_color = ttkstyle_widget_color(style_string)
    widget_type = ttkstyle_widget_type(style_string)
    widget_orient = ttkstyle_widget_orient(widget, style_string, **kwargs)
    widget_class = ttkstyle_widget_class(widget, style_string)

    if widget_color:
        widget_color = f'{widget_color}.'

    if widget_type:
        widget_type = f'{widget_type.title()}.'
    
    if widget_orient:
        widget_orient = f'{widget_orient.title()}.'
    
    if widget_class.startswith('t'):
        widget_class = widget_class.title()
    else:
        widget_class = f'T{widget_class.title()}'
    
    ttkstyle = f'{widget_color}{widget_type}{widget_orient}{widget_class}'
    return ttkstyle

def ttkstyle_method_name(widget=None, string=''):
    """Parse a string to build and return the name of the 
    `StyleBuilderTTK` method that creates the ttk style for the target
    widget.
    """
    style_string = ''.join(string).lower()
    widget_type = ttkstyle_widget_type(style_string)
    widget_class = ttkstyle_widget_class(widget, style_string)

    if widget_type:
        widget_type = f'_{widget_type}'
    
    if widget_class:
        widget_class = f'_{widget_class}'

    if not widget_type and not widget_class:
        return ''
    else:
        method_name = f'create{widget_type}{widget_class}_style'
        return method_name

def tkupdate_method_name(widget):
    """Lookup the tkinter style update method from the widget class"""
    widget_class = ttkstyle_widget_class(widget)
    
    if widget_class:
        widget_class = f'_{widget_class}'

    method_name = f'update{widget_class}_style'
    return method_name          
