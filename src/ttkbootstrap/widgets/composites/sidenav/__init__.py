"""SideNav widgets for building navigation interfaces.

This package provides a complete navigation solution:

- SideNav: Main container with pane, header, content, and footer
- SideNavGroup: Collapsible group of items (expander in expanded mode, popup in compact)
- SideNavItem: Selectable navigation item with icon and text
- SideNavHeader: Non-selectable section label
- SideNavSeparator: Visual divider between groups
"""

from ttkbootstrap.widgets.composites.sidenav.item import SideNavItem
from ttkbootstrap.widgets.composites.sidenav.group import SideNavGroup
from ttkbootstrap.widgets.composites.sidenav.header import SideNavHeader
from ttkbootstrap.widgets.composites.sidenav.separator import SideNavSeparator
from ttkbootstrap.widgets.composites.sidenav.view import SideNav

# Backward compatibility aliases
NavigationView = SideNav
NavigationViewItem = SideNavItem
NavigationViewGroup = SideNavGroup
NavigationViewHeader = SideNavHeader
NavigationViewSeparator = SideNavSeparator

__all__ = [
    'SideNav',
    'SideNavGroup',
    'SideNavItem',
    'SideNavHeader',
    'SideNavSeparator',
    # Backward compatibility
    'NavigationView',
    'NavigationViewItem',
    'NavigationViewGroup',
    'NavigationViewHeader',
    'NavigationViewSeparator',
]
