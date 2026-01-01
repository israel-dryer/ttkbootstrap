---
title: TabView
---

# TabView

`TabView` is a **tabbed container** that combines a `Tabs` bar with a `PageStack` for seamless
tab-based content switching.

Each tab corresponds to a page, and selecting a tab automatically navigates to its associated content.

<!--
IMAGE: TabView with content
Suggested: Horizontal tabs above content area, vertical tabs beside content
Theme variants: light / dark
-->

---

## Quick start

Create a tabbed view with pages:

```python
import ttkbootstrap as ttk

app = ttk.App()

tabview = ttk.TabView(app, height=200)
tabview.pack(fill="both", expand=True, padx=10, pady=10)

# Add tabs with content
home = tabview.add("home", text="Home", icon="house")
ttk.Label(home, text="Welcome to the Home page!").pack(padx=20, pady=20)

files = tabview.add("files", text="Files", icon="folder2")
ttk.Label(files, text="Browse your files here.").pack(padx=20, pady=20)

settings = tabview.add("settings", text="Settings", icon="gear")
ttk.Label(settings, text="Configure your settings.").pack(padx=20, pady=20)

app.mainloop()
```

---

## When to use

Use `TabView` when:

- you need tabs that switch between content panels

- users access content by category or section

- all tabs are equally important and accessible

Consider a different control when:

- navigation is sequential - use [PageStack](pagestack.md) instead

- you need a standalone tab bar - use [Tabs](../navigation/tabs.md) instead

- content must be visible simultaneously - use [PanedWindow](../layout/panedwindow.md) instead

---

## Appearance

### Variants

TabView supports two visual variants:

| Variant | Description |
|---------|-------------|
| `bar` | Default style with underline indicator and divider |
| `pill` | Rounded pill-style tabs without divider |

```python
# Bar variant (default)
tabview = ttk.TabView(app, variant="bar")

# Pill variant
tabview = ttk.TabView(app, variant="pill")
```

### Orientation

Tabs can appear above or beside the content:

```python
# Horizontal tabs above content (default)
tabview = ttk.TabView(app, orient="horizontal")

# Vertical tabs beside content
tabview = ttk.TabView(app, orient="vertical")
```

!!! link "Design System"
    See [Colors & Themes](../../design-system/colors.md) for color customization.

---

## Examples and patterns

### Adding tabs and pages

Use `add()` to create a tab and its content page:

```python
page = tabview.add("profile", text="Profile", icon="person")
# page is a Frame - add widgets to it
ttk.Label(page, text="User profile").pack()
```

The `key` uniquely identifies each tab/page pair.

### Closable tabs

Enable close buttons to allow users to remove tabs:

```python
tabview = ttk.TabView(app, enable_closing=True)
```

With `enable_closing=True`, clicking the close button automatically removes
both the tab and its page. You can also provide a custom close handler:

```python
def on_close():
    if confirm_close():
        tabview.remove("doc1")

tabview.add("doc1", text="Document", closable=True, close_command=on_close)
```

### Dynamic tabs with add button

Show an "add" button for creating new tabs:

```python
tabview = ttk.TabView(app, enable_adding=True)

counter = [0]

def on_add(event):
    counter[0] += 1
    key = f"doc{counter[0]}"
    page = tabview.add(key, text=f"Document {counter[0]}", icon="file-text")
    ttk.Label(page, text=f"Content for Document {counter[0]}").pack()

tabview.on_tab_added(on_add)
```

### Programmatic navigation

Select tabs programmatically:

```python
tabview.select("settings")
```

Get the current tab:

```python
current_key = tabview.current
```

Navigate with data:

```python
tabview.navigate("details", data={"user_id": 123})
```

### Accessing components

Access the underlying Tabs and PageStack:

```python
tabs_widget = tabview.tabs
page_stack = tabview.page_stack
```

Get a specific tab or page:

```python
tab = tabview.tab("settings")  # Returns TabItem
page = tabview.page("settings")  # Returns Frame
```

### Events

TabView emits navigation events:

- `<<TabAdd>>` - when add button is clicked
- `<<PageChange>>` - when the visible page changes

```python
def on_page_change(event):
    print(f"Now showing: {event.data['page']}")

tabview.on_page_changed(on_page_change)
```

---

## Behavior

### UX guidance

- Use descriptive tab labels

- Include icons for visual recognition

- Limit to 5-7 horizontal tabs for scannability

- Vertical tabs work well for settings or navigation-heavy interfaces

- Enable closing only when users should manage tabs (e.g., documents, browser-like interfaces)

!!! tip "Content persistence"
    Pages are retained when switching tabs. Use PageStack events if you need
    to refresh content on navigation.

---

## Additional resources

### Related widgets

- [Tabs](../navigation/tabs.md) - standalone tab bar

- [PageStack](pagestack.md) - history-based navigation

- [Notebook](notebook.md) - traditional ttk tabbed container

- [PanedWindow](../layout/panedwindow.md) - resizable multi-view layouts

### API reference

- [`ttkbootstrap.TabView`](../../reference/widgets/TabView.md)
