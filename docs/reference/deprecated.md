# Deprecated Names

These names are still importable from `ttkbootstrap` for backwards compatibility but will be removed in a future version.
Each raises a `DeprecationWarning` at import time pointing to the replacement.

## Widget aliases

| Deprecated name | Replacement | Notes |
|---|---|---|
| `Checkbutton` | `CheckButton` | Spelling aligned with ttkbootstrap conventions |
| `Radiobutton` | `RadioButton` | Spelling aligned with ttkbootstrap conventions |
| `Labelframe` | `LabelFrame` | Spelling aligned with ttkbootstrap conventions |
| `Panedwindow` | `PanedWindow` | Spelling aligned with ttkbootstrap conventions |
| `Treeview` | `TreeView` | Spelling aligned with ttkbootstrap conventions |
| `Tableview` | `TableView` | Spelling aligned with ttkbootstrap conventions |
| `DatePicker` | `Calendar` | Widget renamed in v2 |

## Navigation widget aliases

| Deprecated name | Replacement | Notes |
|---|---|---|
| `NavigationView` | `SideNav` | Widget renamed in v2 |
| `NavigationViewItem` | `SideNavItem` | Widget renamed in v2 |
| `NavigationViewGroup` | `SideNavGroup` | Widget renamed in v2 |
| `NavigationViewHeader` | `SideNavHeader` | Widget renamed in v2 |
| `NavigationViewSeparator` | `SideNavSeparator` | Widget renamed in v2 |

## Migrating

Replace the old name with the new one in your imports and widget constructors:

```python
# Before
from ttkbootstrap import NavigationView, NavigationViewItem

# After
import ttkbootstrap as ttk
nav = ttk.SideNav(app)
item = ttk.SideNavItem(nav, key="home", text="Home")
```

For a full v1 → v2 migration guide see [Guides → Migrating](../guides/migrating.md) (coming soon).
