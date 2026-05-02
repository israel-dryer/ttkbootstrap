---
title: Localization
---

# Localization

Localization in ttkbootstrap covers two independent axes:

- **Translation** — turning a key like `'button.cancel'` into `'OK'`
  / `'Abbrechen'` / `'キャンセル'` based on the active locale. Handled
  by `MessageCatalog`, which bridges Tcl `msgcat` and Python `gettext`
  catalogs.
- **Value formatting** — turning `1234.56` into `'$1,234.56'` /
  `'1.234,56 €'` / `'¥1,234'` based on the active locale. Handled by
  `IntlFormatter`, which wraps Babel's date / number / currency
  helpers behind a DevExtreme-style preset vocabulary
  (`'longDate'`, `'currency'`, `'largeNumber'`, …).

Widget integration is automatic: `LocalizationMixin` (on Label,
Button, CheckButton, RadioButton, MenuButton, LabelFrame) wraps
`text=` literals as translation keys when the global mode is `'auto'`
(the default), subscribes to `<<LocaleChanged>>`, and refreshes the
displayed text when the locale switches at runtime.

This page is the spec. For end-user workflow ("how do I add German
translations to my app?") see
[Guides → Localization](../guides/localization.md).

---

## At a glance

| Surface | Where it lives | What it does |
|---|---|---|
| `MessageCatalog` | `ttk.MessageCatalog` | Static facade over Tcl `msgcat` and Python `gettext`; sets / queries the active locale, registers translations, runs lookups |
| `L(key, *args)` | `ttk.L` | Build a `LocalizedTextSpec` for an explicit translation key (e.g. `text=L('button.save')`) |
| `LV(value, fmt)` | `ttk.LV` | Build a `LocalizedValueSpec` for a number / date / time formatted per locale (e.g. `text=LV(1234.56, 'currency')`) |
| `IntlFormatter` | `ttk.IntlFormatter` | Locale-aware formatter / parser; usable standalone or via the `value_format=` widget kwarg |
| `LocalizationMixin` | inherited by `Label`, `Button`, `CheckButton`, `RadioButton`, `MenuButton`, `LabelFrame` | Wraps `text=` literals, subscribes to `<<LocaleChanged>>`, refreshes on locale switch |
| `localize=True/False/'auto'` | widget kwarg | Per-widget override of the global localize mode |
| `value_format=` | widget kwarg | Format spec for non-string `text=` / `textsignal=` values |
| `<<LocaleChanged>>` | virtual event on root | Fires after `MessageCatalog.locale(new_locale)`; payload `{"locale": "<code>"}` |
| `AppSettings.locale` | dataclass field | Initial locale; falls back to `detect_locale()` (process / system locale → `en_US`) |
| `AppSettings.localize_mode` | dataclass field | `'auto'` (default), `True`, or `False` — controls whether widget literals are auto-wrapped |

---

## Initialization

`App.__init__()` calls `MessageCatalog.init(...)` automatically with
domain `'ttkbootstrap'` and the resolved settings locale. The locales
directory is auto-discovered in this order:

1. `$TTKBOOTSTRAP_LOCALES` environment variable
2. `src/ttkbootstrap/assets/locales` (the bundled framework catalogs)
3. `<package>/localization/locales` / `<package>/locales`
4. `<repo>/locales`
5. `./locales` (current working directory)

Pre-`App` calls to `MessageCatalog.translate(...)` raise
`RuntimeError: No current App instance is set.` because the lookup
needs a live Tk interpreter for the msgcat command. Always construct
`App` first.

The framework ships catalogs for ~20 locales (en, de, fr, es, it,
pt, pt_BR, nl, sv, da, nb, pl, cs, sl, ja, ko, hi, he, ar, bg)
covering the built-in semantic keys (`button.ok`, `button.cancel`,
`edit.select_all`, etc.). Application keys live in your own
catalog directory (see Guides → Localization).

---

## Translation: `MessageCatalog`

`MessageCatalog` is a static facade — never instantiated. All methods
are class-level.

| Method | Purpose |
|---|---|
| `translate(key, *args)` | Look up `key` in the active locale; format with `args` |
| `locale(new_locale=None)` | Get / set the active locale; emits `<<LocaleChanged>>` on set |
| `set(locale, key, translated)` | Register a single runtime translation |
| `set_many(locale, k1, v1, k2, v2, ...)` | Bulk register translations |
| `load(dirname)` | Load a directory of Tcl `.msg` files via `::msgcat::mcload` |
| `preferences()` | Tcl msgcat fallback chain for the active locale |
| `max(*keys)` | Length of the longest translation across the given keys |
| `init(...)` | (Re-)initialize the bridge; called automatically by `App` |

### Lookups

```python
import ttkbootstrap as ttk

app = ttk.App()

ttk.MessageCatalog.set('en_US', 'greeting', 'Hello, %s!')
ttk.MessageCatalog.set('fr_FR', 'greeting', 'Bonjour, %s!')

ttk.MessageCatalog.translate('greeting', 'Israel')
# 'Hello, Israel!'

ttk.MessageCatalog.locale('fr_FR')
ttk.MessageCatalog.translate('greeting', 'Israel')
# 'Bonjour, Israel!'

app.mainloop()
```

Resolution order (first hit wins):

1. **Runtime override** for the active locale (registered via `set`
   / `set_many`). Tcl `msgcat` is consulted for `%1$s`-style
   positional formatting when format args are supplied.
2. **Gettext catalog** (compiled `.mo` under
   `<dir>/<locale>/LC_MESSAGES/<domain>.mo`).
3. **Tcl msgcat** fallback (legacy `.msg` files loaded via `load`).
4. **The key itself** if no translation is found.

Format args use Python `%`-style formatting (`'%s'`, `'%d'`); the
implementation falls back to Tcl `format` semantics when Python
formatting fails (this is what makes `%1$s` positional specifiers
work for legacy translations).

### Switching at runtime

```python
ttk.MessageCatalog.locale('de_DE')   # writes new locale, fires <<LocaleChanged>>
ttk.MessageCatalog.locale()          # query current locale
```

`locale(new_locale)` does three things:

1. Reinstalls the gettext translator for the requested language
   (with base-language fallback: `de_DE` → `de` if no exact match).
2. Calls `::msgcat::mclocale` so Tcl side stays in sync.
3. Fires `<<LocaleChanged>>` on the root window with payload
   `{"locale": new_locale}` and `when="tail"` (so the event drains
   after the current callback returns, avoiding re-entrant dispatch).

**Locale codes are normalized.** Input forms `de-de`, `de_DE`, and
`de` all produce gettext-style `de_DE`. Tcl msgcat uses the
lowercased form, so `MessageCatalog.locale()` returns `'de_de'` when
queried (lowercase), even though `'de_DE'` is what you passed in.

### Ampersand stripping

When `strip_ampersands=True` (the default), single `&` markers in
translations are removed and `&&` becomes a literal `&`:

```python
ttk.MessageCatalog.set('en_US', 'menu.file', '&File')
ttk.MessageCatalog.translate('menu.file')
# 'File'        — the mnemonic & is stripped
```

Useful when the same catalog is shared with platforms that consume
the `&` as an Alt-key marker (Win32 / GTK menus). Toggle via
`MessageCatalog.init(strip_ampersands=False)`.

---

## Value formatting: `IntlFormatter`

`IntlFormatter` wraps Babel's locale-aware formatters behind a
preset vocabulary. Standalone usage:

```python
fmt_us = ttk.IntlFormatter(locale='en_US')
fmt_de = ttk.IntlFormatter(locale='de_DE')

fmt_us.format(1234.56, 'decimal')          # '1,234.56'
fmt_de.format(1234.56, 'decimal')          # '1.234,56'
fmt_us.format(0.42, 'percent')             # '42%'
fmt_us.format(1234.5, 'currency')          # '$1,234.50'
fmt_de.format(1234.5, {'type': 'currency', 'currency': 'EUR'})
# '1.234,50 €'

from datetime import date
fmt_us.format(date(2026, 5, 2), 'longDate')  # 'May 2, 2026'
fmt_de.format(date(2026, 5, 2), 'longDate')  # '2. Mai 2026'
```

`format(value, spec)` dispatches on `value`'s type
(int / float / date / datetime / time → preset; everything else →
`str(value)`) and on `spec`'s shape (string preset / dict options /
CLDR pattern containing `#` or `0`).

If `locale=` is omitted at construction, `detect_locale()` resolves
it from the current process locale (`locale.getlocale()`), the system
default (`locale.getdefaultlocale()`), then `'en_US'`.

### Number presets

| Preset | Example output (en_US) | Notes |
|---|---|---|
| `'decimal'` (or `'fixedPoint'`) | `'1,234.56'` | General locale-aware decimal |
| `'percent'` | `'42%'` | Multiplies by 100; respects the locale's `%` placement |
| `'currency'` | `'$1,234.56'` | Dict `{'type': 'currency', 'currency': 'EUR', 'precision': 2}` for explicit currency / precision; default currency inferred from locale's territory |
| `'exponential'` | `'1.23456E5'` | Scientific notation |
| `'thousands'` / `'millions'` / `'billions'` / `'trillions'` | `'45K'`, `'1.235M'` | Force a specific compact suffix |
| `'largeNumber'` | `'1.235M'` | Auto-pick the largest fitting suffix |
| CLDR pattern (e.g. `'#,##0.00'`, `'0000.00'`) | `'12.34'` → `'0012.34'` | Treated as `'custom'` when the string contains `#` or `0` |

Dict form accepts `{type, precision, currency, pattern, use_grouping}`.

### Date / time presets

| Preset | Example (en_US) | Example (de_DE) |
|---|---|---|
| `'longDate'` | `'May 2, 2026'` | `'2. Mai 2026'` |
| `'shortDate'` | `'5/2/26'` | `'02.05.26'` |
| `'monthAndDay'` | `'May 2'` | `'2. Mai'` |
| `'monthAndYear'` | `'May 2026'` | `'Mai 2026'` |
| `'quarterAndYear'` | `'Q2 2026'` | `'Q2 2026'` |
| `'longTime'` / `'shortTime'` | `'2:30:00 PM'` / `'2:30 PM'` | `'14:30:00'` / `'14:30'` |
| `'longDateLongTime'` / `'shortDateShortTime'` | `'May 2, 2026 at 2:30:00 PM EDT'` / `'5/2/26, 2:30 PM'` | `'2. Mai 2026 um 14:30:00 GMT+0'` / `'02.05.26, 14:30'` |
| `'day'` / `'month'` / `'year'` / `'quarter'` / `'dayOfWeek'` / `'hour'` / `'minute'` / `'second'` / `'millisecond'` | Single-component renders | |
| CLDR pattern (e.g. `'yyyy-MM-dd'`) | Treated as `'custom'` if the string is not a known preset | |

!!! danger "Time-only formatting is broken"

    `IntlFormatter.format(time_obj, 'shortTime')` — and every other
    time-only preset (`'longTime'`, `'hour'`, `'minute'`, `'second'`,
    `'millisecond'`) — raises `TypeError: tzinfo argument must be
    None or of a tzinfo subclass, not type 'str'`. Cause:
    `_format_time` at `core/localization/intl_format.py:441-446`
    calls `format_time(t, 'short', self.locale)`. Babel's
    `format_time` signature is `format_time(time, format, tzinfo,
    locale)` — the third positional is `tzinfo`, not `locale`, so
    the locale string lands in the wrong slot. Fix: replace each
    `format_time(..., self.locale)` with
    `format_time(..., locale=self.locale)` (or insert `None` as the
    `tzinfo` positional). Workaround: format from a `datetime`
    instead of a bare `time`, or call Babel's `format_time` directly
    with `locale=` as a kwarg.

    Date-only and datetime presets are unaffected — Babel's
    `format_date` and `format_datetime` have `locale` as their third
    positional parameter, which matches the IntlFormatter calls.

### Parsing

`fmt.parse(text, spec)` is the inverse:

```python
fmt_de.parse('1.234,56', 'decimal')       # 1234.56
fmt_us.parse('1.5M', 'largeNumber')       # 1500000.0
fmt_us.parse('50%', 'percent')            # 0.5
fmt_us.parse('May 2, 2026', 'longDate')   # date(2026, 5, 2)
```

Numbers go through Babel's `parse_decimal` plus a regex for compact
suffix handling. Temporal values try `dateparser` first (handles
multilingual free-form like `'15 juillet 2025'`) and fall back to
`python-dateutil`. Empty input returns `None`; malformed temporal
input raises `ValueError`.

The `day_first=True` / `year_first=True` constructor flags are
hints for ambiguous numeric dates (`'02/05/2026'` is May 2 with
`day_first=False`, February 5 with `day_first=True`).

---

## Widget integration: `LocalizationMixin`

`Label`, `Button`, `CheckButton`, `RadioButton`, `MenuButton`, and
`LabelFrame` inherit `LocalizationMixin`. The mixin:

1. Reads the global `localize_mode` from `AppSettings`
   (default `'auto'`) and accepts a per-widget override via
   `localize=`.
2. On construction, examines `text=`. If localization is enabled, it
   wraps the value in a `LocalizedTextSpec` and resolves it to the
   current locale's translation.
3. Subscribes to `<<LocaleChanged>>` on the toplevel and refreshes
   the displayed text when the locale changes.

```python
import ttkbootstrap as ttk

app = ttk.App()

ttk.MessageCatalog.set('en_US', 'app.title', 'My App')
ttk.MessageCatalog.set('fr_FR', 'app.title', 'Mon Appli')

# 'auto' mode (default): the literal 'app.title' is used as a key
title = ttk.Label(app, text='app.title')
title.pack()
title.cget('text')                    # 'My App'

ttk.MessageCatalog.locale('fr_FR')
title.cget('text')                    # 'Mon Appli'  (auto-refreshed)

# localize=False: the literal is shown as-is, no lookup
literal = ttk.Label(app, text='app.title', localize=False)
literal.cget('text')                  # 'app.title'

app.mainloop()
```

Three decisions to be aware of:

- **Auto mode is permissive.** Every string `text=` is treated as a
  potential key. If no translation exists, the key itself is shown —
  so `text='Hello, world!'` works as plain text *and* doubles as a
  translation key if you later register one. The only hazard is
  accidentally collide with an existing key.
- **Empty-string and `None` text are skipped.** The mixin does not
  register them, so they never trigger lookups.
- **Refresh is per-widget.** Each widget instance subscribes
  individually to `<<LocaleChanged>>`. There's no central
  `refresh_all()` — destroying a widget unsubscribes it.

### Explicit specs: `L(key)` and `LV(value, fmt)`

When you want to be explicit (or when the literal text would otherwise
*not* be wrapped — e.g. `localize=False` is in effect globally):

```python
from ttkbootstrap import L, LV

# Translation, regardless of the global mode
ttk.Label(app, text=L('app.title'))

# Locale-aware value formatting
ttk.Label(app, text=LV(1234.56, 'currency'))   # '$1,234.56' / '1.234,56 €'
```

Both specs participate in `<<LocaleChanged>>` refresh.

### Reactive value formatting: `value_format=`

When a label / button is bound to a `textsignal` carrying numeric
data, pass `value_format=` to format it through `IntlFormatter` on
every write:

```python
from ttkbootstrap.core.signals import Signal

price = Signal(1234.56)
ttk.Label(app, textsignal=price, value_format='currency').pack()
# Renders '$1,234.56' (en_US), updates whenever `price` changes,
# and re-renders on locale switch.
```

Internally the mixin replaces the widget's bound variable with a
private `Signal[str]` that subscribes to the source signal, formats
the value, and writes the result. The original signal stays
type-correct (`float` in this example) while the widget displays
the formatted string.

---

## Putting it together

```python
import ttkbootstrap as ttk
from ttkbootstrap import L, LV
from ttkbootstrap.core.signals import Signal
from datetime import date

app = ttk.App()

ttk.MessageCatalog.set('en_US', 'price.label', 'Price')
ttk.MessageCatalog.set('de_DE', 'price.label', 'Preis')

price = Signal(1234.56)

ttk.Label(app, text=L('price.label')).pack()
ttk.Label(app, textsignal=price, value_format='currency').pack()
ttk.Label(app, text=LV(date(2026, 5, 2), 'longDate')).pack()

# A debug button to flip locales
def cycle():
    cur = ttk.MessageCatalog.locale()
    ttk.MessageCatalog.locale('de_DE' if cur.startswith('en') else 'en_US')

ttk.Button(app, text='Toggle locale', command=cycle).pack()

app.mainloop()
```

Click "Toggle locale" — the label, the formatted price, and the
formatted date all refresh because each widget participates in the
`<<LocaleChanged>>` event.

---

## Where to read next

- *"How do I add a new language to my app?"* — register translations
  with `MessageCatalog.set_many` at startup, or compile a `.mo`
  catalog under `locales/<lang>/LC_MESSAGES/<domain>.mo` and point
  `$TTKBOOTSTRAP_LOCALES` at the parent. See
  [Guides → Localization](../guides/localization.md).
- *"How do I switch locale at runtime?"* —
  `ttk.MessageCatalog.locale('de_DE')` from anywhere; widgets that
  use `LocalizationMixin` refresh automatically.
- *"How do I show a localized number that updates with a Signal?"* —
  `Label(app, textsignal=sig, value_format='currency')`.
- *"Which widgets refresh on locale change?"* — anything that
  inherits `LocalizationMixin` (`Label`, `Button`, `CheckButton`,
  `RadioButton`, `MenuButton`, `LabelFrame`), plus widgets that
  explicitly handle `<<LocaleChanged>>` themselves
  (`Calendar`, `DateEntry`, `TimeEntry`, `NumericEntry`,
  `TableView`, `Notebook` for tab labels, several dialogs).
- *"What's the relationship to virtual events and signals?"* —
  `<<LocaleChanged>>` is one of the framework-emitted events
  documented in
  [Signals & Events → Virtual events](signals/virtual-events.md);
  `value_format=` reads the same `Signal` channel covered in
  [Signals & Events → Signals](signals/signals.md).
- *"What's set per-locale at the App level?"* —
  `AppSettings.locale`, `AppSettings.localize_mode`, plus the
  derived `language` / `date_format` / `time_format` /
  `number_decimal` / `number_thousands` fields. See
  [Configuration](configuration.md).
