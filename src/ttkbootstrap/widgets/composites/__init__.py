"""Composite ttkbootstrap widgets."""

from ttkbootstrap.widgets.composites.accordion import Accordion
from ttkbootstrap.widgets.composites.compositeframe import Composite, CompositeFrame
from ttkbootstrap.widgets.composites.expander import Expander
from ttkbootstrap.widgets.composites.list import ListItem, ListView, MemoryDataSource, DataSourceProtocol
from ttkbootstrap.widgets.composites.menubar import MenuBar
from ttkbootstrap.widgets.composites.sidenav import (
    SideNav,
    SideNavItem,
    SideNavGroup,
    SideNavHeader,
    SideNavSeparator,
)
from ttkbootstrap.widgets.composites.tabs import Tabs, TabView
from ttkbootstrap.widgets.composites.selectbox import SelectBox
from ttkbootstrap.widgets.composites.toolbar import Toolbar

# Backward compatibility aliases
NavigationView = SideNav
NavigationViewItem = SideNavItem
NavigationViewGroup = SideNavGroup
NavigationViewHeader = SideNavHeader
NavigationViewSeparator = SideNavSeparator

__all__ = [
    'Accordion',
    'Composite',
    'CompositeFrame',
    'Expander',
    'ListItem',
    'ListView',
    'MemoryDataSource',
    'DataSourceProtocol',
    'MenuBar',
    'SideNav',
    'SideNavItem',
    'SideNavGroup',
    'SideNavHeader',
    'SideNavSeparator',
    'Tabs',
    'TabView',
    'SelectBox',
    'Toolbar',
    # Backward compatibility
    'NavigationView',
    'NavigationViewGroup',
    'NavigationViewItem',
    'NavigationViewHeader',
    'NavigationViewSeparator',
]
