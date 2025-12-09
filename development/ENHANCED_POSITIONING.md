# Enhanced Window Positioning Features

## Overview

This document describes the enhanced window positioning features added to ttkbootstrap, including anchor-based positioning, smart dropdown positioning, and cursor-based positioning for both `Toplevel` windows and `Dialog` instances.

## Key Features

### 1. Anchor-based Positioning

Position windows relative to any widget using tkinter's standard anchor points (n, s, e, w, ne, nw, se, sw, center).

**Example:**
```python
# Show a toplevel below a button
toplevel = ttk.Toplevel()
toplevel.place_anchor(
    anchor_to=button,
    anchor_point='sw',  # button's bottom-left
    window_point='nw',  # window's top-left
    offset=(0, 5)
)
```

### 2. Smart Dropdown Positioning

Automatically position windows as dropdowns with smart above/below flipping when space is limited.

**Example:**
```python
# Show a dropdown menu
dropdown = ttk.Toplevel()
dropdown.place_dropdown(
    trigger_widget=button,
    prefer_below=True,
    align='left',
    auto_flip=True  # Flips above if no room below
)
```

### 3. Cursor Positioning

Position windows at the current mouse cursor location - perfect for context menus.

**Example:**
```python
# Show a context menu at cursor
menu = ttk.Toplevel()
menu.place_cursor(offset=(5, 5))
```

---

## Toplevel API

All `Toplevel` instances now have these positioning methods:

### `place_anchor()`
```python
toplevel.place_anchor(
    anchor_to: Widget,
    anchor_point: AnchorPoint = 'sw',
    window_point: AnchorPoint = 'nw',
    offset: Tuple[int, int] = (0, 0),
    ensure_visible: bool = True
)
```

### `place_dropdown()`
```python
toplevel.place_dropdown(
    trigger_widget: Widget,
    prefer_below: bool = True,
    align: Literal['left', 'right', 'center'] = 'left',
    offset: Tuple[int, int] = (0, 2),
    ensure_visible: bool = True,
    auto_flip: bool = True
)
```

### `place_cursor()`
```python
toplevel.place_cursor(
    offset: Tuple[int, int] = (5, 5),
    ensure_visible: bool = True
)
```

### Existing Methods (Enhanced)
- `place_center()` - Center on screen
- `place_center_on(parent)` - Center on parent widget
- `place_at(x, y)` - Position at specific coordinates

---

## Dialog API

The `Dialog.show()` method has been enhanced to support all positioning modes:

### Enhanced `show()` Method
```python
dialog.show(
    position: Optional[Tuple[int, int]] = None,
    modal: Optional[bool] = None,
    *,
    anchor_to: Optional[Widget] = None,
    anchor_point: AnchorPoint = 'sw',
    window_point: AnchorPoint = 'nw',
    offset: Tuple[int, int] = (0, 0),
    at_cursor: bool = False,
    dropdown_trigger: Optional[Widget] = None,
    dropdown_align: Literal['left', 'right', 'center'] = 'left',
    dropdown_prefer_below: bool = True
)
```

**Positioning Priority:**
1. Explicit `position` coordinates (if provided)
2. Dropdown positioning (if `dropdown_trigger` provided)
3. Anchor positioning (if `anchor_to` provided)
4. Cursor positioning (if `at_cursor=True`)
5. Default: Centered on parent

### New Convenience Methods

#### `show_anchored()`
```python
dialog.show_anchored(
    anchor_to: Widget,
    anchor_point: AnchorPoint = 'sw',
    window_point: AnchorPoint = 'nw',
    offset: Tuple[int, int] = (0, 0),
    modal: Optional[bool] = None
)
```

**Example:**
```python
dialog = Dialog(title="Options", content_builder=build_content)
dialog.show_anchored(anchor_to=button, anchor_point='sw', window_point='nw')
```

#### `show_dropdown()`
```python
dialog.show_dropdown(
    trigger_widget: Widget,
    align: Literal['left', 'right', 'center'] = 'left',
    prefer_below: bool = True,
    offset: Tuple[int, int] = (0, 2),
    modal: Optional[bool] = None
)
```

**Example:**
```python
dialog = Dialog(title="Menu", content_builder=build_menu, mode="popover")
dialog.show_dropdown(trigger_widget=button, align='left')
```

#### `show_at_cursor()`
```python
dialog.show_at_cursor(
    offset: Tuple[int, int] = (5, 5),
    modal: Optional[bool] = None
)
```

**Example:**
```python
dialog = Dialog(title="Context Menu", content_builder=build_menu, mode="popover")
dialog.show_at_cursor(offset=(10, 10))
```

---

## Anchor Point Reference

Using tkinter's standard anchor naming convention:

```
nw -------- n -------- ne
|                       |
|                       |
w        center         e
|                       |
|                       |
sw -------- s -------- se
```

- **n** = north (top center)
- **s** = south (bottom center)
- **e** = east (right center)
- **w** = west (left center)
- **ne** = northeast (top-right corner)
- **nw** = northwest (top-left corner)
- **se** = southeast (bottom-right corner)
- **sw** = southwest (bottom-left corner)
- **center** = center point

---

## Common Use Cases

### Tooltip Above Widget
```python
tooltip = ttk.Toplevel()
tooltip.place_anchor(
    anchor_to=widget,
    anchor_point='n',   # widget's top
    window_point='s',   # tooltip's bottom
    offset=(0, -5)
)
```

### Dropdown Menu Below Button
```python
menu = ttk.Toplevel()
menu.place_dropdown(
    trigger_widget=button,
    prefer_below=True,
    align='left'
)
```

### Context Menu at Click
```python
def show_context_menu(event):
    menu = ttk.Toplevel()
    menu.place_cursor(offset=(0, 0))

widget.bind("<Button-3>", show_context_menu)
```

### Dialog Below Form Field
```python
dialog = Dialog(title="Validation Error", content_builder=build_error)
dialog.show_anchored(
    anchor_to=entry_field,
    anchor_point='sw',
    window_point='nw',
    offset=(0, 2)
)
```

---

## Implementation Details

### Module Structure

- **`window_utilities.py`** - Core positioning logic
  - `WindowPositioning` - Static utility methods
  - `WindowSizing` - Size calculation utilities
  - `AnchorPoint` - Type definition for anchor points

- **`base_window.py`** - Window mixin
  - `BaseWindow` - Mixin providing positioning methods
  - Inherited by both `App` and `Toplevel`

- **`dialog.py`** - Dialog class
  - Enhanced `show()` method with all positioning options
  - Convenience methods: `show_anchored()`, `show_dropdown()`, `show_at_cursor()`

### Testing

Two demo files and two test files are provided:

**Demos:**
- `tests/demo_window_positioning.py` - Interactive Toplevel positioning demo
- `tests/demo_dialog_positioning.py` - Interactive Dialog positioning demo

**Tests:**
- `tests/test_window_positioning_api.py` - Toplevel API tests
- `tests/test_dialog_positioning_api.py` - Dialog API tests

Run the demos:
```bash
python tests/demo_window_positioning.py
python tests/demo_dialog_positioning.py
```

Run the tests:
```bash
python tests/test_window_positioning_api.py
python tests/test_dialog_positioning_api.py
```

---

## Benefits

1. **Consistent API** - Uses tkinter's standard anchor naming
2. **Type Safety** - Full type hints for IDE support
3. **Smart Defaults** - Sensible defaults for common use cases
4. **Flexible** - Multiple positioning modes available
5. **Auto-Adjustment** - Windows stay on-screen automatically
6. **Reusable** - Works for Toplevel, Dialog, and custom windows

---

## Migration Guide

### Before
```python
# Manual positioning
dialog = Dialog(...)
dialog.show(position=(100, 100))
```

### After
```python
# Anchor-based positioning
dialog = Dialog(...)
dialog.show_anchored(anchor_to=button, anchor_point='sw', window_point='nw')

# Or using show() with keywords
dialog.show(anchor_to=button, anchor_point='sw', window_point='nw')
```

All existing code continues to work - these are additions, not breaking changes.
