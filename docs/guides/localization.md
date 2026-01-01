---
title: Localization
---

# Localization

This guide shows how to make ttkbootstrap applications language-aware with message catalogs and locale-aware formatting.

---

## Why Localize?

Localization makes applications usable worldwide:

- **Text** adapts to the user's language
- **Dates and numbers** follow regional conventions
- **UI** can adapt to RTL languages

ttkbootstrap treats localization as a framework-level concern, not widget-by-widget configuration.

---

## Quick Start

A localized application:

```python
import ttkbootstrap as ttk

app = ttk.App(locale="es")

# Use message keys instead of literal text
ttk.Label(app, text="greeting.hello").pack(pady=20)
ttk.Button(app, text="actions.save").pack(pady=10)

app.mainloop()
```

With a Spanish message catalog, `"greeting.hello"` resolves to `"Hola"` and `"actions.save"` to `"Guardar"`.

---

## Message Catalogs

Message catalogs map **message keys** to **translated text**.

### Catalog Structure

Organize translations by language:

```
locales/
├── en.json
├── es.json
├── fr.json
└── de.json
```

Each file contains key-value pairs:

```json
{
    "greeting.hello": "Hello",
    "greeting.welcome": "Welcome, {name}!",
    "actions.save": "Save",
    "actions.cancel": "Cancel",
    "status.ready": "Ready"
}
```

### Loading Catalogs

```python
import ttkbootstrap as ttk
from ttkbootstrap import MessageCatalog

# Load catalog from file
MessageCatalog.load("locales/en.json")
MessageCatalog.load("locales/es.json")

app = ttk.App(locale="en")
```

### Using Message Keys

Widgets automatically resolve message keys:

```python
# If "greeting.hello" exists in catalog, it's resolved
# If not, the literal string is displayed
ttk.Label(app, text="greeting.hello")
```

This behavior uses `localize="auto"` (the default):

```python
# Auto: resolve if key exists, otherwise use literal
ttk.Label(app, text="greeting.hello")  # localize="auto"

# Force localization (error if key missing)
ttk.Label(app, text="greeting.hello", localize=True)

# Disable localization (always literal)
ttk.Label(app, text="Hello, World!", localize=False)
```

---

## Message Substitution

Messages can include placeholders:

```json
{
    "greeting.welcome": "Welcome, {name}!",
    "items.count": "{count} items"
}
```

Resolve with values:

```python
from ttkbootstrap import L

# L() resolves messages with substitution
text = L("greeting.welcome", name="Alice")  # "Welcome, Alice!"
text = L("items.count", count=5)  # "5 items"
```

For reactive updates with signals:

```python
from ttkbootstrap import LV

name = ttk.Signal("Guest")

# LV() returns a signal that updates when inputs change
greeting = LV("greeting.welcome", name=name)

label = ttk.Label(app, textvariable=greeting)
```

When `name` changes, `greeting` updates automatically.

---

## Changing Language at Runtime

Switch languages without restarting:

```python
import ttkbootstrap as ttk
from ttkbootstrap import set_locale, get_locale

app = ttk.App(locale="en")

def switch_to_spanish():
    set_locale("es")

def switch_to_english():
    set_locale("en")

ttk.Button(app, text="Español", command=switch_to_spanish).pack()
ttk.Button(app, text="English", command=switch_to_english).pack()

# This label updates when locale changes
ttk.Label(app, text="greeting.hello").pack(pady=20)

app.mainloop()
```

Localized widgets re-render when the locale changes.

---

## Date and Number Formatting

Localization extends beyond text to **how values are displayed**.

### Date Formatting

```python
from ttkbootstrap import IntlFormatter
from datetime import date

formatter = IntlFormatter(locale="de")

today = date.today()
formatted = formatter.format_date(today)  # "25.12.2024" (German format)
```

### Number Formatting

```python
formatter = IntlFormatter(locale="fr")

formatted = formatter.format_number(1234567.89)  # "1 234 567,89" (French format)
formatted = formatter.format_currency(99.99, "EUR")  # "99,99 €"
```

### In Widgets

Some widgets format values automatically based on locale:

```python
app = ttk.App(locale="de")

# DateEntry displays dates in German format
ttk.DateEntry(app).pack()

# NumericEntry uses locale decimal separator
ttk.NumericEntry(app).pack()
```

---

## Patterns

### Language Selector

```python
import ttkbootstrap as ttk
from ttkbootstrap import set_locale

app = ttk.App(locale="en")

languages = [("English", "en"), ("Español", "es"), ("Français", "fr")]

selector = ttk.OptionMenu(
    app,
    values=[name for name, _ in languages],
    command=lambda name: set_locale(
        next(code for n, code in languages if n == name)
    ),
)
selector.pack(pady=20)

app.mainloop()
```

### Localized Form

```python
import ttkbootstrap as ttk

app = ttk.App(locale="en")

form = ttk.GridFrame(app, columns=["auto", 1], gap=10, padding=20)
form.pack(fill="both", expand=True)

# Labels use message keys
ttk.Label(form, text="form.username").grid()
ttk.Entry(form).grid(sticky="ew")

ttk.Label(form, text="form.password").grid()
ttk.Entry(form, show="*").grid(sticky="ew")

# Button uses message key
ttk.Button(form, text="actions.login").grid(column=1, sticky="e")

app.mainloop()
```

### Dynamic Messages

```python
import ttkbootstrap as ttk
from ttkbootstrap import LV

app = ttk.App()

# Reactive count
count = ttk.Signal(0)

# Message updates when count changes
status = LV("items.selected", count=count)

ttk.Label(app, textvariable=status).pack(pady=20)

def add_item():
    count.set(count.get() + 1)

ttk.Button(app, text="Add", command=add_item).pack()

app.mainloop()
```

---

## Best Practices

### Use Semantic Keys

```json
{
    "actions.save": "Save",
    "actions.cancel": "Cancel",
    "errors.required": "This field is required"
}
```

Not:

```json
{
    "save_button_text": "Save",
    "the_cancel_button": "Cancel"
}
```

### Keep Translations Complete

Ensure all languages have the same keys. Missing keys fall back to the key itself.

### Test RTL Languages

If supporting Arabic or Hebrew, test that layout flows correctly.

### Don't Concatenate

```python
# Bad: concatenation breaks translation
message = L("greeting.hello") + ", " + name

# Good: use placeholders
message = L("greeting.welcome", name=name)
```

---

## Summary

- Use **message keys** in widgets instead of literal text
- Load **message catalogs** for each supported language
- Use **`L()`** for static messages with substitution
- Use **`LV()`** for reactive messages bound to signals
- Use **`IntlFormatter`** for locale-aware date/number formatting
- Change language at runtime with **`set_locale()`**

!!! link "Localization Capability"
    See [Capabilities → Localization](../capabilities/localization.md) for architecture details.

---

## Next Steps

- [App Structure](app-structure.md) — how applications are organized
- [Reactivity](reactivity.md) — signals and reactive updates
- [Styling](styling.md) — working with the design system
