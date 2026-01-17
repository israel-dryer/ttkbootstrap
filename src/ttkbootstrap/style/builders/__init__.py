"""Style builder functions for ttkbootstrap widgets.

This package contains individual builder functions organized by widget type.
Each builder is registered with the BootstyleBuilder registry using decorators.

Builder modules are automatically imported to trigger registration.
"""

from __future__ import annotations

from . import (
    badge, button, checkbutton, combobox, entry, expander, frame, label, labelframe, menubutton, navigationview,
    notebook, panedwindow, progressbar, radiobutton, scale, scrollbar, separator, sizegrip, spinbox, switch,
    treeview, toolbutton, tooltip, field, buttongroup, listview, calendar, contextmenu, tabitem, menubar
)

# Import all builder modules to trigger registration

__all__ = [
    'badge',
    'button',
    'expander',
    'frame',
    'label',
    'navigationview',
    'radiobutton',
    'checkbutton',
    'switch',
    'progressbar',
    'scale',
    'scrollbar',
    'menubutton',
    'entry',
    'field',
    'separator',
    'combobox',
    'labelframe',
    'notebook',
    'panedwindow',
    'sizegrip',
    'spinbox',
    'treeview',
    'toolbutton',
    'tooltip',
    'buttongroup',
    'listview',
    'calendar',
    'contextmenu',
    'menubar',
    'tabitem'
]
