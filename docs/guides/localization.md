---
title: Localization
---

# Localization

This guide explains how to make ttkbootstrap applications language-aware: how text gets translated, how the active language is selected, how widgets refresh on language changes, and how to format locale-sensitive values like numbers and dates.

---

## Mental model

Localization in ttkbootstrap has three independent layers:

1. **Locale** — a single application-wide setting (e.g. `"de_DE"`) that names
   both the language for translation and the regional conventions for
   formatting. Held on `AppSettings.locale` and the active `MessageCatalog`.
2. **Translation** — looking up a *message id* and returning the version of
   that string in the active language. Driven by `MessageCatalog`, backed by
   gettext `.mo` catalogs. This is what turns `"Cancel"` into `"Abbrechen"`.
3. **Value formatting** — rendering numbers, dates, and currency according
   to regional conventions. Driven by `IntlFormatter`. This is what turns
   `1234.5` into `"1.234,5"` (de) or `"1,234.5"` (en).

Most ttkbootstrap widgets participate in both layers automatically: a `Label`
will translate its `text=`, and a `NumericEntry` will format its `value=`
using the active locale. You opt in to localization by setting the locale
once at startup; from then on, widgets follow.

!!! note "Already covered elsewhere"
    Locale-aware *value* formatting in widgets (`value_format=`) is covered
    in depth in the [Formatting guide](formatting.md). This page focuses on
    text translation, runtime language switching, and how the pieces fit
    together. Settings configuration is covered in
    [App Settings](app-settings.md).

---

## Activating localization

### Setting the locale at startup

The locale is part of `AppSettings`. You can pass it through the `settings`
argument to `App`:

```python
import ttkbootstrap as ttk

app = ttk.App(settings={"locale": "de_DE"})

ttk.Label(app, text="Cancel").pack(pady=20)

app.mainloop()
```

If `"Cancel"` is present in the German message catalog, the label renders
as `"Abbrechen"`. If it isn't, the literal text is shown.

If `locale` is not specified, ttkbootstrap auto-detects it from the system
(falling back to `"en_US"`).

### Localization mode

Whether widgets *attempt* translation is controlled by a separate
setting, `localize_mode`. It accepts three values:

| Value     | Behavior                                                |
| --------- | ------------------------------------------------------- |
| `"auto"`  | (default) Attempt translation; fall back to literal.    |
| `True`    | Always attempt translation.                             |
| `False`   | Disable localization; use literal text everywhere.      |

You can set this via `AppSettings.localize_mode` or, more conveniently, via
the top-level `localize=` argument on `App`:

```python
import ttkbootstrap as ttk

# Disable all auto-translation; literal strings only.
app = ttk.App(localize=False)

app.mainloop()
```

The same flag is also accepted per-widget as `localize=`, which overrides
the application-wide mode for that widget.

!!! note "Locale vs. localize"
    `locale` chooses *which* language and regional conventions are active.
    `localize` (and `localize_mode`) chooses *whether* widgets try to
    translate at all. You will usually only ever set `locale`.

---

## Translating text

Widgets that take a `text=` argument run it through `MessageCatalog.translate()`
when localization is active. The string you pass is treated as a message id;
the widget displays the translation if one exists, and the literal id
otherwise.

```python
import ttkbootstrap as ttk

app = ttk.App(settings={"locale": "de_DE"})

ttk.Button(app, text="Cancel").pack(pady=10)
ttk.Button(app, text="Open").pack(pady=10)

app.mainloop()
```

You can also be explicit by wrapping the text with `L()`:

```python
import ttkbootstrap as ttk
from ttkbootstrap import L

app = ttk.App(settings={"locale": "de_DE"})

ttk.Button(app, text=L("Cancel")).pack(pady=10)

app.mainloop()
```

Wrapping is only required when the call site needs to be unambiguous, or
when you want to pass formatting arguments (see below). For ordinary
widget construction the literal-string form is enough.

### Format arguments

`L()` accepts positional formatting arguments that are interpolated into
the translated string using Python `%`-formatting:

```python
from ttkbootstrap import L

text = L("Hello, %s!", "Alice")
```

The translated template is fetched first, then the arguments are
substituted. This means translators can reorder placeholders by using
positional specifiers like `%1$s`, which Tcl `msgcat` formatting handles
as a fallback.

`MessageCatalog.translate()` works the same way and is the underlying
function:

```python
from ttkbootstrap import MessageCatalog

text = MessageCatalog.translate("Hello, %s!", "Alice")
```

A common idiom in user code is to alias it once:

```python
from ttkbootstrap import MessageCatalog

_ = MessageCatalog.translate

label_text = _("Cancel")
```

---

## Catalogs

Translations live in **gettext catalogs**: pairs of `.po` (source) and
`.mo` (compiled) files organized by language under a `locales/` directory:

```
locales/
└── de/
    └── LC_MESSAGES/
        └── messages.po
        └── messages.mo
```

A `.po` file is a plain-text list of `msgid`/`msgstr` pairs:

```
msgid "Cancel"
msgstr "Abbrechen"

msgid "Hello, %s!"
msgstr "Hallo, %s!"
```

Each catalog is identified by a *domain* (the filename, default
`messages`) and a *language* (the directory name).

### Auto-discovery

ttkbootstrap auto-discovers a `locales/` directory at startup by checking
several locations in order:

1. The `TTKBOOTSTRAP_LOCALES` environment variable.
2. `src/ttkbootstrap/assets/locales` (where the library's own catalogs live).
3. A `locales/` directory next to your application.
4. The current working directory.

The library ships its own translations for built-in widget strings (dialog
buttons, calendar weekday names, error messages, and so on) under the
`ttkbootstrap` domain. Your application's catalogs typically use the
default `messages` domain.

### Compiling catalogs

You write `.po` files; gettext consumes `.mo`. Compile them with Babel
(installed with `pip install babel`):

```bash
pybabel compile -d locales -D messages
```

For ttkbootstrap's own catalogs, the project ships a helper:

```bash
python tools/make_i18n.py compile
```

!!! warning "Catalogs require Tk"
    `MessageCatalog` is a thin façade over both Python `gettext` and Tcl
    `msgcat`, so its methods need a live Tk interpreter. Always create the
    `App` first; only then call any `MessageCatalog` method.

### Loading catalogs explicitly

When ttkbootstrap can't auto-discover your catalogs (for example, a frozen
app with a non-standard layout), point `MessageCatalog.init()` at the
right directory:

```python
import ttkbootstrap as ttk
from ttkbootstrap import MessageCatalog

app = ttk.App()
MessageCatalog.init(
    locales_dir="path/to/locales",
    domain="messages",
    default_locale="de_DE",
)
```

`MessageCatalog.load()` is a separate, lower-level helper that loads
Tcl-style `.msg` files from a directory. You only need it if you're
integrating with a legacy msgcat workflow; gettext catalogs are the
recommended path.

---

## Runtime translations

You don't have to ship a compiled catalog to start translating. Use
`MessageCatalog.set()` and `set_many()` to register translations directly
from Python:

```python
import ttkbootstrap as ttk
from ttkbootstrap import MessageCatalog

app = ttk.App()

MessageCatalog.set("de", "Cancel", "Abbrechen")
MessageCatalog.set_many(
    "de",
    "Open", "Öffnen",
    "Save", "Speichern",
)

MessageCatalog.locale("de")
ttk.Button(app, text="Cancel").pack(pady=10)
ttk.Button(app, text="Open").pack(pady=10)

app.mainloop()
```

Runtime overrides take precedence over compiled catalogs and survive
locale switches. They are useful for tests, plugins, and quick iteration.

---

## Switching language at runtime

Call `MessageCatalog.locale(new_locale)` to switch languages while the
application is running. ttkbootstrap fires the `<<LocaleChanged>>` virtual
event on the root window; widgets that support automatic localization
listen for it and refresh their text.

```python
import ttkbootstrap as ttk
from ttkbootstrap import MessageCatalog

app = ttk.App(settings={"locale": "en"})

label = ttk.Label(app, text="Cancel")
label.pack(pady=20)

def to_german():
    MessageCatalog.locale("de")

def to_english():
    MessageCatalog.locale("en")

ttk.Button(app, text="Deutsch", command=to_german).pack()
ttk.Button(app, text="English", command=to_english).pack()

app.mainloop()
```

Calling `MessageCatalog.locale()` without an argument returns the active
locale code.

### Manual refresh

Code that builds widget text imperatively (concatenations, conditional
labels, dynamically-built menu items) won't re-translate by itself. Bind
`<<LocaleChanged>>` and rebuild on demand:

```python
import ttkbootstrap as ttk
from ttkbootstrap import MessageCatalog

app = ttk.App()
_ = MessageCatalog.translate

status = ttk.Label(app)
status.pack(pady=20)

def refresh():
    status.configure(text=_("Ready"))

refresh()
app.bind("<<LocaleChanged>>", lambda e: refresh())

app.mainloop()
```

---

## Reactive translations with signals

For text that depends on application state, use `LV()` for value
formatting or compose `L()` with a signal subscription. Widgets that take
a `value=` and `value_format=` (such as `NumericEntry`, `DateEntry`,
`Meter`, `FloodGauge`) automatically rebuild their display text on locale
changes:

```python
import ttkbootstrap as ttk

app = ttk.App(settings={"locale": "de_DE"})

# A currency-formatted entry that re-renders when the locale changes.
ttk.NumericEntry(app, value=1234.56, value_format="currency").pack(pady=20)

app.mainloop()
```

See the [Formatting guide](formatting.md) for the full list of supported
`value_format` strings.

For text-side reactivity tied to a `Signal`, subscribe and re-resolve:

```python
import ttkbootstrap as ttk
from ttkbootstrap import L

app = ttk.App()
count = ttk.Signal(0)

label = ttk.Label(app)
label.pack(pady=20)

def on_count(n):
    label.configure(text=L("%s items selected", n))

count.subscribe(on_count, immediate=True)

ttk.Button(app, text="Add", command=lambda: count.set(count.get() + 1)).pack()

app.mainloop()
```

---

## Formatting numbers and dates

Numeric and temporal values are localized through `IntlFormatter`. It
exposes a single `format(value, spec)` method that picks the right
strategy based on the value's type and the spec:

```python
from ttkbootstrap import IntlFormatter
from datetime import date

fmt = IntlFormatter(locale="de_DE")

fmt.format(1234.5, "decimal")         # '1.234,5'
fmt.format(0.42, "percent")           # '42 %'
fmt.format(99.99, "currency")         # '99,99 €'
fmt.format(date(2025, 12, 25), "longDate")  # '25. Dezember 2025'
```

The same specs work as widget `value_format=` arguments:

```python
import ttkbootstrap as ttk

app = ttk.App(settings={"locale": "de_DE"})

ttk.NumericEntry(app, value=99.99, value_format="currency").pack(padx=20, pady=20)

app.mainloop()
```

The full list of presets and dict-form options (precision, custom
patterns, compact forms like `"largeNumber"`) is documented in the
[Formatting guide](formatting.md).

---

## Which widgets auto-localize

| Layer        | Widgets                                                                |
| ------------ | ---------------------------------------------------------------------- |
| Text         | Any widget with a `text=` option (`Label`, `Button`, `Checkbutton`,    |
|              | `Radiobutton`, `Menubutton`, tab labels, etc.).                        |
| Value format | Widgets with `value=` + `value_format=` (`Label`, `NumericEntry`,      |
|              | `DateEntry`, `Meter`, `FloodGauge`, etc.).                             |
| Library      | Built-in dialogs (`MessageBox`, `QueryBox`, `FontDialog`, etc.) and    |
|              | calendar widgets — all use the shipped `ttkbootstrap` catalog.         |

Anything you build with raw Tcl callbacks, custom canvas drawing, or
direct attribute mutation needs the manual `<<LocaleChanged>>` refresh
shown above.

---

## Right-to-left languages

ttkbootstrap does not currently provide automatic RTL mirroring of
layouts, icons, or scrollbar gutters. Translation into Arabic, Hebrew,
and other RTL languages works at the text level — message catalogs and
runtime switching behave the same as for LTR languages — but visual
layout flips are out of scope for v2.

If you support RTL languages in production, plan for:

- Manual mirroring of grid columns and pack sides.
- Right-aligning text where the natural reading flow requires it.
- Avoiding directional iconography (back arrows, etc.) in language-
  agnostic UI.

---

## Testing with another locale

The simplest way to verify translations is to start the application with
a forced locale:

```python
import ttkbootstrap as ttk

app = ttk.App(settings={"locale": "de_DE"})
# ... build UI ...
app.mainloop()
```

For quick screenshot review, you can flip the locale from the REPL or a
keybinding:

```python
import ttkbootstrap as ttk
from ttkbootstrap import MessageCatalog

app = ttk.App()

def cycle(_event):
    cur = MessageCatalog.locale()
    MessageCatalog.locale("de" if cur.startswith("en") else "en")

app.bind("<F12>", cycle)

ttk.Label(app, text="Open").pack(pady=20)
ttk.Label(app, text="Save").pack(pady=10)

app.mainloop()
```

To audit which strings are missing translations, set the locale to a
language with a partial catalog and visually scan the UI for any text
that didn't change.

---

## Best practices

### Use stable message ids

Treat the message id as a name, not as English copy. Once translators
have worked on `"Cancel"`, renaming it to `"Cancel."` invalidates every
translation. Either keep the literal text stable, or use semantic ids
and keep an `en` catalog that maps them:

```
msgid "actions.save"
msgstr "Save"
```

### Don't concatenate translated fragments

Concatenation breaks any language with a different word order:

```python
# Wrong: assumes English subject-verb-object.
message = L("Hello") + ", " + name

# Right: let the translator place the placeholder.
message = L("Hello, %s!", name)
```

### Keep catalog domains separate

Application strings belong in a `messages` (or any custom-named) domain.
Don't add your own keys to ttkbootstrap's built-in `ttkbootstrap`
catalog — they will be lost when the library updates.

### Strip mnemonics consistently

`MessageCatalog` removes single `&` mnemonics from strings on render and
turns `&&` into a literal `&`. Don't manually add or remove ampersands
in your code; let the catalog do it.

---

## Summary

- Set the locale once via `App(settings={"locale": ...})`; the rest of
  the framework follows.
- Widget `text=` and `value=` are localized automatically.
- Use `L("key", *args)` / `MessageCatalog.translate(...)` for explicit
  translation calls.
- Switch language at runtime with `MessageCatalog.locale(code)`; widgets
  refresh on the `<<LocaleChanged>>` event.
- Use `IntlFormatter` (or widget `value_format=`) for locale-aware
  numbers and dates.
- Use `MessageCatalog.set` / `set_many` for runtime overrides;
  ship `.po` / `.mo` catalogs for production translations.

!!! link "Related"
    - [Capabilities → Localization](../capabilities/localization.md) — design rationale.
    - [Formatting](formatting.md) — `value_format` specs and `IntlFormatter` in detail.
    - [App Settings](app-settings.md) — how `locale` and `localize_mode` fit into application configuration.

---

## Next steps

- [App Structure](app-structure.md) — how applications are organized.
- [Reactivity](reactivity.md) — signals and reactive updates.
- [Formatting](formatting.md) — locale-aware value formatting in depth.
