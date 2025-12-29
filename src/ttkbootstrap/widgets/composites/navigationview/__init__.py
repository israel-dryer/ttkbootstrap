"""NavigationView widgets for building navigation interfaces.

This package provides a complete navigation solution:

- NavigationView: Main container with pane, header, content, and footer
- NavigationViewGroup: Collapsible group of items (expander in expanded mode, popup in compact)
- NavigationViewItem: Selectable navigation item with icon and text
- NavigationViewHeader: Non-selectable section label
- NavigationViewSeparator: Visual divider between groups
"""

from ttkbootstrap.widgets.composites.navigationview.item import NavigationViewItem
from ttkbootstrap.widgets.composites.navigationview.group import NavigationViewGroup
from ttkbootstrap.widgets.composites.navigationview.header import NavigationViewHeader
from ttkbootstrap.widgets.composites.navigationview.separator import NavigationViewSeparator
from ttkbootstrap.widgets.composites.navigationview.view import NavigationView

__all__ = [
    'NavigationView',
    'NavigationViewGroup',
    'NavigationViewItem',
    'NavigationViewHeader',
    'NavigationViewSeparator',
]
