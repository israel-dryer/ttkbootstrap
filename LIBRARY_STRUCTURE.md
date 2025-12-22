# ttkbootstrap v2 Library Structure Reference

## Project Overview

| Property | Value |
|----------|-------|
| **Version** | 2.0.0a1 (Alpha) |
| **Python** | 3.10+ |
| **License** | MIT |

---

## Directory Structure

```
ttkbootstrap/
├── src/ttkbootstrap/           # Main package
│   ├── api/                    # Public API surface
│   ├── assets/                 # Themes (35 JSON) + locales (22 languages)
│   ├── cli/                    # Command-line interface
│   ├── core/                   # Utilities, signals, validation, publisher
│   ├── datasource/             # Data abstraction (memory, SQLite, file)
│   ├── dialogs/                # Dialog widgets (9 types)
│   ├── runtime/                # App, window, events, menu management
│   ├── style/                  # Styling engine + 28 widget builders
│   ├── themes/                 # Theme definitions (Python)
│   └── widgets/                # 55+ widgets
│       ├── primitives/         # 24 TTK-derived widgets
│       ├── composites/         # 31+ custom widgets
│       ├── mixins/             # Reusable behaviors
│       └── parts/              # Subcomponent implementations
├── examples/                   # Example scripts
├── tests/                      # Test files
├── docs/                       # MkDocs documentation
└── tools/                      # Utility scripts
```

---

## Core Modules

| Module | Purpose |
|--------|---------|
| **api/** | Centralized public exports for widgets, style, app, menu |
| **core/** | Color utils, signals, validation, publisher-subscriber, i18n |
| **style/** | 35+ themes, bootstyle API, widget builders, typography |
| **runtime/** | App/Window classes, events, menus, DPI handling |
| **widgets/** | Primitives, composites, mixins, parts |
| **dialogs/** | Color, date, font, form, message, query dialogs |
| **datasource/** | Unified data interface with pagination, filtering, CRUD |

---

## Widget Inventory (55+ total)

### Primitives (24)

Badge, Button, CheckButton, CheckToggle, Combobox, Entry, Frame, Label, LabelFrame, MenuButton, Notebook, OptionMenu, PanedWindow, Progressbar, RadioButton, RadioToggle, Scale, Scrollbar, SelectBox, Separator, SizeGrip, Spinbox, TreeView

### Composites (31+)

ButtonGroup, DateEntry, DatePicker, DropdownButton, Field, FloodGauge, Form, ListView, Meter, NumericEntry, PageStack, PasswordEntry, PathEntry, RadioGroup, ScrolledText, ScrollView, SpinnerEntry, TableView, TextEntry, TimeEntry, Toast, ToggleGroup, ToolTip

### Dialogs (9)

Dialog, Message, Query, ColorChooser, ColorDropper, DateDialog, FontDialog, FilterDialog, FormDialog

---

## Key Features

### Bootstyle System

Bootstrap-inspired styling with modifiers:

- **Colors:** primary, secondary, success, danger, warning, info, light, dark
- **Types:** outline, link, toggle, inverse, striped, toolbutton, square
- **Example:** `bootstyle="success-outline"`, `bootstyle="danger-link"`

### Signal/Slot System

Reactive programming pattern for widgets:

- Decoupled event handling
- Type-safe signal connections
- Publisher-subscriber architecture

### Localization (i18n)

Multi-language support with 22 languages:

ar, cs, da, de, en, es, fr, he, hi, it, ja, ko, nb, nl, pl, pt, pt_BR, sl, sv, tr, zh_CN, zh_TW

### DataSource Abstraction

Unified data interface supporting:

- Multiple backends (memory, SQLite, files)
- Pagination with configurable page size
- SQL-like filtering and sorting
- Full CRUD operations
- CSV export

### Built-in Themes (35)

cosmo, flatly, litera, minty, lumen, pulse, sandstone, united, yeti, morph, journal, simplex, cerculean, solar, superhero, darkly, cyborg, vapor, and more

---

## Module Details

### api/

| File | Purpose |
|------|---------|
| `app.py` | Application class and app context management |
| `localization.py` | Localization/i18n support |
| `menu.py` | Menu management API |
| `style.py` | Style API functions |
| `widgets.py` | Widget API re-exports |

### core/

| File | Purpose |
|------|---------|
| `colorutils.py` | Color manipulation (HSV, RGB conversions) |
| `exceptions.py` | Custom exception types |
| `publisher.py` | Publisher-subscriber pattern for events |
| `variables.py` | Tkinter variable extensions |
| `validation/` | Validation framework for input widgets |
| `signals/` | Signal/slot mechanism for reactive programming |
| `localization/` | Message catalog system |

### style/

| File | Purpose |
|------|---------|
| `bootstyle.py` | Bootstyle API for applying styles |
| `bootstyle_builder_base.py` | Base builder for bootstyles |
| `bootstyle_builder_tk.py` | Tk widget styling builder |
| `bootstyle_builder_ttk.py` | TTK widget styling builder |
| `element.py` | Style element definitions |
| `style.py` | Main Style engine class |
| `theme_provider.py` | Theme loading and management |
| `token_maps.py` | Design token mappings |
| `typography.py` | Font and text styling |
| `builders/` | 28 widget-specific style builders |

### runtime/

| File | Purpose |
|------|---------|
| `app.py` | Main App class, theme management, DPI awareness |
| `base_window.py` | Common window functionality |
| `toplevel.py` | Toplevel window support |
| `menu.py` | Menu management |
| `events.py` | Event handling system |
| `window_utilities.py` | Window utility functions |
| `utility.py` | General runtime utilities |

### widgets/

| Directory | Purpose |
|-----------|---------|
| `primitives/` | 24 basic TTK-derived widgets |
| `composites/` | 31+ complex custom widgets |
| `mixins/` | Reusable widget behaviors |
| `parts/` | Widget subcomponent implementations |

### dialogs/

| File | Purpose |
|------|---------|
| `dialog.py` | Base dialog class |
| `message.py` | Message dialogs (info, warning, error, question) |
| `query.py` | Query/input dialogs |
| `colorchooser.py` | Color selection dialog |
| `colordropper.py` | Color picker/dropper |
| `datedialog.py` | Date selection dialog |
| `fontdialog.py` | Font selection dialog |
| `filterdialog.py` | Filtering dialog |
| `formdialog.py` | Form input dialog |

### datasource/

| File | Purpose |
|------|---------|
| `base.py` | Base abstract class |
| `memory_source.py` | In-memory storage |
| `sqlite_source.py` | SQLite persistent storage |
| `file_source.py` | File-based storage (CSV, JSON) |

---

## Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| pillow | >=10, <=12 | Image processing |
| ttkbootstrap-icons | >=4 | Bootstrap icons |
| Babel | >=2.12 | Internationalization |
| python-dateutil | >=2.8 | Date utilities |
| dateparser | >=1.1 | Date parsing |

---

## Key Files by Size

| File | Size | Purpose |
|------|------|---------|
| `style/__init__.py` | 196 KB | Core styling engine |
| `widgets/composites/tableview/` | 90 KB | Advanced data table |
| `runtime/window_utilities.py` | 37 KB | Window manipulation |
| `dialogs/colorchooser.py` | 28 KB | Color picker dialog |
| `dialogs/formdialog.py` | 28 KB | Form builder dialog |
| `style/bootstyle_builder_base.py` | 25 KB | Style builder foundation |
| `dialogs/query.py` | 21 KB | Query dialogs |
| `datasource/file_source.py` | 22 KB | File-based data source |
| `widgets/mixins/signal_mixin.py` | 19 KB | Signal/event integration |
| `runtime/base_window.py` | 19 KB | Base window functionality |