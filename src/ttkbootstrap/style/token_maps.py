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
}
WIDGET_NAME_MAP = {v: k for k, v in WIDGET_CLASS_MAP.items()}
FRAME_SURFACE_CLASSES = {'TFrame', 'TLabelframe'}
