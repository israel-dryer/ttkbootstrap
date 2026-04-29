---
title: Dialogs
---

# Dialogs

Dialogs are modal or transient windows used for focused interactions - displaying messages, collecting input, or presenting specialized pickers.

## Message dialogs

- [MessageDialog](messagedialog.md) - customizable message popup with buttons
- [MessageBox](messagebox.md) - static convenience methods (info, warning, error, yes/no)

## Input dialogs

- [QueryDialog](querydialog.md) - single-value input with validation
- [QueryBox](querybox.md) - static convenience methods (string, integer, float, item)
- [FormDialog](formdialog.md) - multi-field form submission

## Native vs custom dialogs

ttkbootstrap dialogs (`MessageDialog`, `ColorChooser`, `DateDialog`, etc.) are **not** OS-native windows — they are custom Tk toplevels styled to match your theme. This means they look consistent across platforms but differ from system dialogs in appearance.

For cases where OS-native behavior is required — file and directory pickers, native font or color dialogs — use Python's built-in `tkinter.filedialog`, `tkinter.colorchooser`, or `tkinter.font` modules directly. These delegate to the operating system and ignore ttkbootstrap themes.

```python
import tkinter.filedialog as fd

# Native file picker — ignores ttkbootstrap theme
path = fd.askopenfilename(title="Open file")
```

## Specialized pickers

- [Dialog](dialog.md) - base class for building custom dialogs
- [DateDialog](datedialog.md) - date selection with calendar
- [ColorChooser](colorchooser.md) - color selection
- [ColorDropper](colordropper.md) - pick color from screen
- [FontDialog](fontdialog.md) - font family, size, and style selection
- [FilterDialog](filterdialog.md) - multi-option filter selection