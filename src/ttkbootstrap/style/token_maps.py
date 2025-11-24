from __future__ import annotations

COLOR_TOKENS = {
    'primary', 'secondary', 'success', 'info',
    'warning', 'danger', 'light', 'dark',
    'foreground', 'background', 'white', 'black',
    'blue', 'indigo', 'purple', 'red', 'orange',
    'yellow', 'green', 'teal', 'cyan', 'gray',
    'border'
}

WIDGET_CLASS_MAP = {
    'badge': 'TBadge',
    'button': 'TButton',
    'label': 'TLabel',
    'entry': 'TEntry',
    'frame': 'TFrame',
    'labelframe': 'TLabelframe',
    'progressbar': 'TProgressbar',
    'scale': 'TScale',
    'scrollbar': 'TScrollbar',
    'checkbutton': 'TCheckbutton',
    'radiobutton': 'TRadiobutton',
    'combobox': 'TCombobox',
    'notebook': 'TNotebook',
    'treeview': 'Treeview',
    'separator': 'TSeparator',
    'sizegrip': 'TSizegrip',
    'panedwindow': 'TPanedwindow',
    'spinbox': 'TSpinbox',
    'menubutton': 'TMenubutton',
    'field': 'TField',
    'toolbutton': 'Toolbutton',
    'tooltip': 'Tooltip'
}

WIDGET_NAME_MAP = {v: k for k, v in WIDGET_CLASS_MAP.items()}
CONTAINER_CLASSES = {'TFrame', 'TField'}
ORIENT_CLASSES = {'TProgressbar', 'TScale', 'TScrollbar', 'TPanedwindow', 'TSeparator'}
ICON_CLASSES = {'TLabel', 'TButton', 'TCheckbutton', 'TRadiobutton', 'TMenubutton'}
