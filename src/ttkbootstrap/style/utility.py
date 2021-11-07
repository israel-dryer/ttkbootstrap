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
    'input'
]

CLASSES = [
    'button',
    'progressbar',
    'checkbutton',
    'combobox',
    'entry',
    'label',
    'labelframe',
    'frame',
    'floodgauge',
    'sizegrip',
    'menubutton',
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
    'toggle'
]

# regex patterns
COLOR_PATTERN = re.compile('|'.join(COLORS))
ORIENT_PATTERN = re.compile('|'.join(ORIENTS))
CLASS_PATTERN = re.compile('|'.join(CLASSES))
TYPE_PATTERN = re.compile('|'.join(TYPES))

# ttkstyle namebuilder helper methods

def normalize_bootstyle(bootstyle, widget):
    """Convert an iterable to a string and append the func class"""
    string = ''.join(bootstyle)
    string += widget.__class__.__name__.lower()
    return string

def widget_class_from_string(string):
    """Find and return the widget class"""
    # search string for widget class pattern
    _class = re.search(CLASS_PATTERN, string.lower())
    if _class is None:
        return ''
    else:
        widget_class = _class.group(0)
        return widget_class

def widget_type_from_string(string):
    """Find and return the widget type"""
    _type = re.search(TYPE_PATTERN, string.lower())
    if _type is None:
        return ''
    else: 
        widget_type = _type.group(0)
        return widget_type

def _widget_default_orient(string):
    """Find and return the default widget orientation if a widget with
    orientation.
    """
    widget_class = widget_class_from_string(string)
    if widget_class is None:
        return ''
    if widget_class in ['progressbar', 'floodgauge', 'separator', 'scale']:
        return 'horizontal'
    elif widget_class in ['panedwindow', 'scrollbar',]:
        return 'vertical'
    else:
        return ''

def widget_orient_from_string(string):
    """Find and return widget orient, or default orient for widget if
    a widget with orientation
    """
    _orient = re.search(ORIENT_PATTERN, string.lower())
    if _orient is None:
        widget_orient = _widget_default_orient(string)
        return widget_orient
    else:
        widget_orient = _orient.group(0)
        return widget_orient

def widget_color_from_string(string):
    """Find and return widget color"""
    _color = re.search(COLOR_PATTERN, string.lower())
    if _color is None:
        return ''
    else:
        widget_color = _color.group(0)
        return widget_color

def ttkstyle_name_from_string(string):
    """Parse a string to build and return a ttkstyle name."""
    if not string:
        return
    _string = ''.join(string).lower()
    widget_color = widget_color_from_string(_string)
    widget_type = widget_type_from_string(_string)
    widget_orient = widget_orient_from_string(_string)
    widget_class = widget_class_from_string(_string)

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

def ttkstyle_method_name_from_string(string):
    """Parse a string to build and return the name of the 
    `StyleBuilderTTK` method that creates the ttk style for the target
    widget.
    """
    _string = ''.join(string).lower()
    widget_type = widget_type_from_string(_string)
    widget_class = widget_class_from_string(_string)

    if widget_type:
        widget_type = f'_{widget_type}'
    
    if widget_class:
        widget_class = f'_{widget_class}'

    if not widget_type and not widget_class:
        return ''
    else:
        method_name = f'create{widget_type}{widget_class}_style'
        return method_name

def get_ttkstyle_name(widget, **kwargs):
    ttkstyle = ''
    bootstyle = ''
    
    if all(['bootstyle' not in kwargs, 'style' not in kwargs]):
        return ''

    # extract bootstyle if exists
    if 'bootstyle' in kwargs:
        bootstyle = kwargs.pop('bootstyle')
        bootstyle = normalize_bootstyle(bootstyle, widget)

    # extract orient if exists
    if 'orient' in kwargs:
        orient = kwargs.pop('orient')
        if orient == 'h':
            orient = 'horizontal'
        elif orient == 'v':
            orient = 'vertical'
        bootstyle += orient

    # check if style is set directly
    if 'style' in kwargs:
        ttkstyle = kwargs.get('style')

    # use bootstyle ONLY if style is NOT provided directly
    if bootstyle and 'style' not in kwargs:
        ttkstyle = ttkstyle_name_from_string(bootstyle)

    return ttkstyle        

def tkupdate_method_name_from_string(string):
    """Parse a string to return the name of the `StyleBuilderTK` method 
    that updates the target tk widget style.
    """
    _string = ''.join(string).lower()
    widget_class = widget_class_from_string(_string)
    
    if widget_class:
        widget_class = f'_{widget_class}'

    method_name = f'update{widget_class}_style'
    return method_name          


if __name__ == '__main__':

    # TESTING
    #string = ['treeview', 'secondary']
    string = 'Primary.Outline.TButton'
    
    print(ttkstyle_name_from_string(string))
    print(ttkstyle_method_name_from_string(string))

