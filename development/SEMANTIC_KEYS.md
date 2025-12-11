# Semantic Message IDs for ttkbootstrap

This document explains how to use semantic message IDs instead of English text as translation keys.

## Backwards Compatibility

**Good news:** The English locale supports **both** semantic keys AND legacy English text!

```python
# Both of these work identically:
ttk.Button(app, text='button.ok')  # NEW: Semantic key
ttk.Button(app, text='OK')          # OLD: Legacy text (still works!)
```

This means:
- ✅ **Existing code works without changes** - keep using `text='OK'`
- ✅ **New code can use semantic keys** - migrate to `text='button.ok'`
- ✅ **Mix both approaches** - no breaking changes during transition

## Key Feature: Automatic Widget Localization

**ttkbootstrap widgets automatically localize their text** - you don't need to manually call `_()`:

```python
# Just pass the semantic key directly!
ttk.Button(app, text='button.ok')        # Automatically shows "OK"
ttk.Label(app, text='font.family')       # Automatically shows "Family"
```

The `LocalizationMixin` built into widgets handles translation automatically.

## What Are Semantic Keys?

Instead of using English text as the msgid:
```python
_("OK")  # English text as key (manual translation)
```

You can use descriptive keys:
```python
_("button.ok")        # Semantic key (manual translation)
# OR
text='button.ok'      # Semantic key (automatic in widgets)
```

## Benefits

1. **Context-aware**: `button.ok` vs `dialog.ok` can have different translations
2. **Consistent**: Same key always means the same thing across the codebase
3. **Refactoring-friendly**: Change English text without touching code
4. **Better organization**: Keys are grouped by category

## Available Keys

### Buttons
```python
_("button.ok")          # OK
_("button.cancel")      # Cancel
_("button.yes")         # Yes
_("button.no")          # No
_("button.save")        # Save
_("button.delete")      # Delete
_("button.submit")      # Submit
_("button.add")         # Add
_("button.remove")      # Remove
_("button.open")        # Open
_("button.close")       # Close
_("button.next")        # Next
_("button.previous")    # Previous
_("button.apply")       # Apply
```

### Font Dialog
```python
_("font.family")        # Family
_("font.size")          # Size
_("font.weight")        # Weight
_("font.slant")         # Slant
_("font.effects")       # Effects
_("font.preview")       # Preview
_("font.selector")      # Font Selector
_("font.preview_text")  # The quick brown fox jumps over the lazy dog.
```

### Color Chooser
```python
_("color.chooser")      # Color Chooser
_("color.red")          # Red
_("color.green")        # Green
_("color.blue")         # Blue
_("color.hue")          # Hue
_("color.sat")          # Sat
_("color.lum")          # Lum
_("color.hex")          # Hex
_("color.current")      # Current
_("color.new")          # New
_("color.dropper")      # color dropper
_("color.advanced")     # Advanced
_("color.themed")       # Themed
_("color.standard")     # Standard
```

### Validation Messages
```python
_("validation.should_be_type")   # Should be of data type
_("validation.invalid_type")     # Invalid data type
_("validation.greater_than")     # Number cannot be greater than
_("validation.less_than")        # Number cannot be less than
_("validation.out_of_range")     # Out of range
```

### Table View
```python
_("table.search")           # Search
_("table.page")             # Page
_("table.of")               # of
_("table.sort")             # Sort
_("table.filter")           # Filter
_("table.export")           # Export
_("table.columns")          # Columns
_("table.reset")            # Reset table
_("table.sort_asc")         # Sort Ascending
_("table.sort_desc")        # Sort Descending
_("table.clear_filters")    # Clear filters
_("table.delete_selected")  # Delete selected rows
_("table.move_up")          # Move up
_("table.move_down")        # Move down
_("table.align_left")       # Align left
_("table.align_center")     # Align center
_("table.align_right")      # Align right
# ... and many more table.* keys
```

### Days of Week
```python
_("day.mo")             # Mo
_("day.tu")             # Tu
_("day.we")             # We
_("day.th")             # Th
_("day.fr")             # Fr
_("day.sa")             # Sa
_("day.su")             # Su
```

### Dialogs
```python
_("dialog.error")       # Error
_("dialog.warning")     # Warning
_("dialog.info")        # Information
_("dialog.question")    # Question
_("dialog.confirm")     # Confirm
```

### File Operations
```python
_("file.new")           # New
_("file.open")          # Open
_("file.save")          # Save
_("file.save_as")       # Save As
_("file.close")         # Close
_("file.exit")          # Exit
```

### Edit Operations
```python
_("edit.cut")           # Cut
_("edit.copy")          # Copy
_("edit.paste")         # Paste
_("edit.undo")          # Undo
_("edit.redo")          # Redo
_("edit.select_all")    # Select All
```

### Help
```python
_("help.about")         # About
_("help.help")          # Help
_("help.documentation") # Documentation
```

## Usage Example

```python
import ttkbootstrap as ttk
from ttkbootstrap import MessageCatalog

app = ttk.App()

# Set locale to English (to use semantic keys)
MessageCatalog.locale('en')

# Use semantic keys in your UI - widgets automatically localize!
ttk.Button(app, text='button.ok').pack()
ttk.Button(app, text='button.cancel').pack()
ttk.Label(app, text='font.family').pack()

# No need to call _() on widget text - localization is built-in!
# But you can still use _() for manual translation if needed:
from ttkbootstrap import MessageCatalog
_ = MessageCatalog.translate
message = _('validation.invalid_type')  # For non-widget text

app.mainloop()
```

## When to Use `_()` vs Direct Keys

### Use Direct Keys (Automatic Localization)
For widget text parameters - localization happens automatically:
```python
ttk.Button(app, text='button.ok')           # ✓ Automatic
ttk.Label(app, text='font.family')          # ✓ Automatic
ttk.LabelFrame(app, text='dialog.confirm')  # ✓ Automatic
```

### Use `_()` (Manual Translation)
For non-widget text, string formatting, or logic:
```python
_ = MessageCatalog.translate

# String variables
error_msg = _('validation.invalid_type')

# String formatting
message = f"{_('table.page')} 1 {_('table.of')} 10"

# Conditional logic
status = _('button.ok') if success else _('dialog.error')

# Print statements, logging, etc.
print(_('button.save'))
```

## Adding Your Own Keys

To add custom semantic keys:

1. Edit `src/ttkbootstrap/assets/locales/en/LC_MESSAGES/ttkbootstrap.po`
2. Add your entries:
   ```
   msgid "myapp.welcome"
   msgstr "Welcome to My App"
   ```
3. Compile: `python tools/make_i18n.py compile`
4. Use in code: `_('myapp.welcome')`

## Translating to Other Languages

When creating translations for other languages, map the same semantic keys:

**French (fr):**
```
msgid "button.ok"
msgstr "D'accord"

msgid "button.cancel"
msgstr "Annuler"
```

**German (de):**
```
msgid "button.ok"
msgstr "OK"

msgid "button.cancel"
msgstr "Abbrechen"
```

## Migration Guide

You can migrate from legacy English text to semantic keys at your own pace:

### Option 1: Keep Using Legacy Text (No Migration)
```python
# Your existing code continues to work
ttk.Button(app, text='OK')
ttk.Label(app, text='Cancel')
```

### Option 2: Gradual Migration
```python
# Mix old and new - both work!
ttk.Button(app, text='button.ok')      # NEW: Semantic
ttk.Label(app, text='Cancel')          # OLD: Legacy
ttk.Button(app, text='button.save')   # NEW: Semantic
```

### Option 3: Full Migration (Recommended for New Projects)
```python
# Use semantic keys everywhere
ttk.Button(app, text='button.ok')
ttk.Button(app, text='button.cancel')
ttk.Button(app, text='button.save')
```

### Why Migrate to Semantic Keys?

**Benefits:**
- **Better context:** `table.search` vs `dialog.search` can have different translations
- **Consistency:** Keys don't change even if English text changes
- **Organization:** Grouped by category (button.*, font.*, etc.)
- **Future-proof:** Easier to manage translations across languages

**No pressure:**
- Legacy text will continue to work indefinitely
- Migrate only if semantic keys benefit your project

## See Full List

Check `src/ttkbootstrap/assets/locales/en/LC_MESSAGES/ttkbootstrap.po` for the complete list of available semantic keys.
