---
title: Formatting
---

# Formatting

This guide explains how to format numbers, dates, and times in ttkbootstrap applications using locale-aware formatting—both in widgets and as a standalone utility.

---

## Overview

ttkbootstrap provides `IntlFormatter`, a locale-aware formatter that handles:

- **Numbers** — decimals, percentages, currency, large numbers
- **Dates** — various date formats from short to long
- **Times** — time-of-day formatting
- **Datetimes** — combined date and time

The formatter adapts automatically to locale conventions—decimal separators, date order, currency symbols—without manual configuration.

---

## Using formatting in widgets

Many widgets accept a `value_format` parameter that specifies how values are displayed and parsed.

### Numeric formatting

```python
# Decimal with grouping
ttk.NumericEntry(app, value=1234.56, value_format="decimal")

# Percentage
ttk.NumericEntry(app, value=0.42, value_format="percent")

# Currency
ttk.NumericEntry(app, value=99.99, value_format="currency")

# Large numbers (auto K/M/B/T)
ttk.NumericEntry(app, value=1500000, value_format="largeNumber")
```

### Date formatting

```python
# Long date: "January 15, 2025"
ttk.DateEntry(app, value_format="longDate")

# Short date: "1/15/25"
ttk.DateEntry(app, value_format="shortDate")

# Custom pattern
ttk.DateEntry(app, value_format="yyyy-MM-dd")
```

### Time formatting

```python
# Short time: "3:30 PM"
ttk.TimeEntry(app, value_format="shortTime")

# Long time: "3:30:45 PM PST"
ttk.TimeEntry(app, value_format="longTime")
```

---

## Number format presets

| Preset | Example (en_US) | Description |
|--------|-----------------|-------------|
| `decimal` | `1,234.56` | Grouped decimal |
| `fixedPoint` | `1,234.56` | Same as decimal |
| `percent` | `42%` | Percentage (input 0.42) |
| `currency` | `$99.99` | Currency with locale symbol |
| `exponential` | `1.23E+3` | Scientific notation |
| `thousands` | `1.5K` | Divide by 1,000 |
| `millions` | `1.5M` | Divide by 1,000,000 |
| `billions` | `1.5B` | Divide by 1,000,000,000 |
| `trillions` | `1.5T` | Divide by 1,000,000,000,000 |
| `largeNumber` | `1.5M` | Auto-select K/M/B/T |

### Precision control

Use a dict to control decimal places:

```python
# Percentage with no decimals
ttk.NumericEntry(app, value=0.425, value_format={"type": "percent", "precision": 0})
# Output: "43%"

# Currency with 2 decimals
ttk.NumericEntry(app, value=99, value_format={"type": "currency", "precision": 2})
# Output: "$99.00"

# Decimal with 3 decimals
ttk.NumericEntry(app, value=3.14159, value_format={"type": "decimal", "precision": 3})
# Output: "3.142"
```

### Custom number patterns

Use ICU/CLDR number patterns directly:

```python
# Always show 2 decimal places
value_format="#,##0.00"

# No grouping, 1 decimal
value_format="0.0"

# Grouping with optional decimals
value_format="#,##0.###"
```

Pattern characters:

| Character | Meaning |
|-----------|---------|
| `0` | Digit (always shown, pad with zero) |
| `#` | Digit (optional, no padding) |
| `.` | Decimal separator (locale-aware) |
| `,` | Grouping separator (locale-aware) |
| `%` | Multiply by 100 and show percent |

---

## Date format presets

| Preset | Example (en_US) | Description |
|--------|-----------------|-------------|
| `longDate` | `January 15, 2025` | Full month name, day, year |
| `shortDate` | `1/15/25` | Numeric short form |
| `monthAndDay` | `January 15` | Month and day only |
| `monthAndYear` | `January 2025` | Month and year only |
| `quarterAndYear` | `Q1 2025` | Quarter and year |
| `day` | `15` | Day of month |
| `dayOfWeek` | `Wednesday` | Full weekday name |
| `month` | `January` | Full month name |
| `quarter` | `Q1` | Quarter |
| `year` | `2025` | Year |

---

## Time format presets

| Preset | Example (en_US) | Description |
|--------|-----------------|-------------|
| `longTime` | `3:30:45 PM PST` | Full time with seconds and zone |
| `shortTime` | `3:30 PM` | Hours and minutes |
| `hour` | `15` | Hour only (24h) |
| `minute` | `30` | Minute only |
| `second` | `45` | Second only |
| `millisecond` | `123` | Milliseconds |

---

## Combined datetime presets

| Preset | Example (en_US) |
|--------|-----------------|
| `longDateLongTime` | `January 15, 2025 at 3:30:45 PM PST` |
| `shortDateShortTime` | `1/15/25, 3:30 PM` |

---

## Custom date/time patterns

Use ICU/CLDR date patterns for full control:

```python
# ISO format
value_format="yyyy-MM-dd"
# Output: "2025-01-15"

# European style
value_format="dd.MM.yyyy"
# Output: "15.01.2025"

# Time with seconds
value_format="HH:mm:ss"
# Output: "15:30:45"

# Full custom
value_format="EEEE, MMMM d, yyyy 'at' h:mm a"
# Output: "Wednesday, January 15, 2025 at 3:30 PM"
```

### Date pattern characters

| Character | Meaning | Example |
|-----------|---------|---------|
| `y` | Year | `2025` |
| `yy` | Year (2-digit) | `25` |
| `yyyy` | Year (4-digit) | `2025` |
| `M` | Month (numeric) | `1` |
| `MM` | Month (2-digit) | `01` |
| `MMM` | Month (abbreviated) | `Jan` |
| `MMMM` | Month (full) | `January` |
| `d` | Day of month | `5` |
| `dd` | Day of month (2-digit) | `05` |
| `E` | Weekday (abbreviated) | `Wed` |
| `EEEE` | Weekday (full) | `Wednesday` |
| `Q` | Quarter | `1` |
| `QQQ` | Quarter (abbreviated) | `Q1` |

### Time pattern characters

| Character | Meaning | Example |
|-----------|---------|---------|
| `H` | Hour (0-23) | `15` |
| `HH` | Hour (2-digit, 0-23) | `15` |
| `h` | Hour (1-12) | `3` |
| `hh` | Hour (2-digit, 1-12) | `03` |
| `m` | Minute | `5` |
| `mm` | Minute (2-digit) | `05` |
| `s` | Second | `9` |
| `ss` | Second (2-digit) | `09` |
| `S` | Millisecond | `1` |
| `SSS` | Millisecond (3-digit) | `001` |
| `a` | AM/PM | `PM` |

---

## Locale configuration

Formatting adapts to the active locale:

```python
from ttkbootstrap.api.i18n import IntlFormatter

# German formatting
fmt_de = IntlFormatter(locale="de_DE")
fmt_de.format(1234.56, "decimal")      # "1.234,56"
fmt_de.format(0.42, "percent")         # "42 %"

# Japanese formatting
fmt_ja = IntlFormatter(locale="ja_JP")
fmt_ja.format(1234.56, "currency")     # "¥1,235"

# French formatting
fmt_fr = IntlFormatter(locale="fr_FR")
fmt_fr.format(date(2025, 1, 15), "longDate")  # "15 janvier 2025"
```

Widgets inherit locale from the application settings:

```python
app = ttk.App(settings={"locale": "de_DE"})

# This entry uses German formatting automatically
ttk.NumericEntry(app, value=1234.56, value_format="decimal")
# Displays: "1.234,56"
```

---

## Standalone IntlFormatter

Use `IntlFormatter` directly for labels, computed values, or any formatting need:

```python
from datetime import date, datetime
from ttkbootstrap.api.i18n import IntlFormatter

fmt = IntlFormatter()  # Uses system locale

# Format numbers
fmt.format(1234567, "largeNumber")           # "1.23M"
fmt.format(0.0875, {"type": "percent", "precision": 1})  # "8.8%"
fmt.format(99.99, "currency")                # "$99.99"

# Format dates
fmt.format(date.today(), "longDate")         # "December 25, 2025"
fmt.format(date.today(), "yyyy-MM-dd")       # "2025-12-25"

# Format times
fmt.format(datetime.now(), "shortTime")      # "2:30 PM"
fmt.format(datetime.now(), "HH:mm:ss")       # "14:30:45"
```

### Parsing user input

IntlFormatter also parses formatted strings back to Python objects:

```python
fmt = IntlFormatter()

# Parse numbers
fmt.parse("1,234.56", "decimal")      # 1234.56
fmt.parse("42%", "percent")           # 0.42
fmt.parse("1.5M", "largeNumber")      # 1500000.0

# Parse dates
fmt.parse("January 15, 2025", "longDate")    # date(2025, 1, 15)
fmt.parse("2025-01-15", "yyyy-MM-dd")        # date(2025, 1, 15)

# Parse times
fmt.parse("3:30 PM", "shortTime")            # time(15, 30)
```

---

## Using with labels

Format values for display in labels:

```python
from ttkbootstrap.api.i18n import IntlFormatter

fmt = IntlFormatter()
revenue = 1234567.89
growth = 0.125

# Create formatted labels
ttk.Label(app, text=f"Revenue: {fmt.format(revenue, 'currency')}")
ttk.Label(app, text=f"Growth: {fmt.format(growth, 'percent')}")
```

---

## Format specification reference

### String shortcuts

Pass a preset name directly:

```python
value_format="decimal"
value_format="longDate"
value_format="shortTime"
```

Or a custom pattern:

```python
value_format="#,##0.00"      # Number pattern
value_format="yyyy-MM-dd"    # Date pattern
```

### Dict specifications

For full control, use a dict:

```python
# Number with precision
value_format={"type": "percent", "precision": 1}

# Currency with specific code
value_format={"type": "currency", "currency": "EUR", "precision": 2}

# Custom pattern via dict
value_format={"type": "custom", "pattern": "#,##0.00"}
```

### Number format options

| Key | Type | Description |
|-----|------|-------------|
| `type` | `str` | Preset name or `"custom"` |
| `precision` | `int` | Decimal places |
| `currency` | `str` | Currency code (e.g., `"USD"`, `"EUR"`) |
| `pattern` | `str` | ICU number pattern |

### Date format options

| Key | Type | Description |
|-----|------|-------------|
| `type` | `str` | Preset name or `"custom"` |
| `pattern` | `str` | ICU date/time pattern |

---

## Summary

- Use **presets** (`decimal`, `longDate`, `shortTime`) for common formats
- Use **custom patterns** for specific requirements
- Widgets accept `value_format` for built-in formatting
- Use `IntlFormatter` directly for labels and computed values
- Formatting adapts automatically to **locale**

---

## Additional resources

- [Localization](localization.md) — message translation and locale settings
- [App Settings](app-settings.md) — configuring application locale
- [Widgets → NumericEntry](../widgets/inputs/numericentry.md) — numeric input with formatting
- [Widgets → DateEntry](../widgets/inputs/dateentry.md) — date input with formatting
