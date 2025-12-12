# Localization (Message Catalog + Babel/gettext)

ttkbootstrap uses a unified message catalog that bridges Python gettext (compiled with Babel) and Tcl/Tk msgcat. Catalogs are distributed with the package under `ttkbootstrap/assets/locales`.

Highlights
- Use `_ = MessageCatalog.translate` in code to mark strings.
- Style auto-initializes the catalog and auto-discovers shipped catalogs.
- Switch language at runtime with `MessageCatalog.locale('de')`.
- A virtual event `<<LocaleChanged>>` is emitted on language changes so UIs can refresh.
- Runtime overrides (`set`, `set_many`) let you add translations that aren't in the catalogs yet.

Directory structure
- `src/ttkbootstrap/assets/locales/<lang>/LC_MESSAGES/ttkbootstrap.po`
- `src/ttkbootstrap/assets/locales/<lang>/LC_MESSAGES/ttkbootstrap.mo`

Marking strings for translation
- In modules that render UI:
  - `from ttkbootstrap.core.localization import MessageCatalog`
  - `_ = MessageCatalog.translate`
  - Example: `ttk.Label(root, text=_('Cancel'))`
- Formatting:
  - `_("File: %s", name)` uses Python `%` formatting.
  - Legacy Tcl printf like `%1$s` are supported via a formatting fallback.

Language switching
- Change language at runtime:
  - `MessageCatalog.locale('fr')`
  - Bind a refresh: `root.bind('<<LocaleChanged>>', lambda e: refresh())`

Runtime overrides (non-compiled messages)
- Add translations for a locale during runtime:
  - Single: `MessageCatalog.set('fr', 'Hello', 'Bonjour')`
  - Many: `MessageCatalog.set_many('de', 'Open','Oeffnen', 'Cancel','Abbrechen')`
  - Emit refresh if you're already in that locale: `root.event_generate('<<LocaleChanged>>')`

Developer workflow (Babel)
- Config lives at project root: `babel.cfg` (extracts from `src/**/*.py` and `_()`/gettext keywords).
- Use the helper to manage catalogs (defaults to `src/ttkbootstrap/assets/locales` and domain `ttkbootstrap`):
  - Extract template: `python tools/make_i18n.py extract`
  - Init locales: `python tools/make_i18n.py init -l de fr`
  - Update catalogs: `python tools/make_i18n.py update`
  - Compile catalogs: `python tools/make_i18n.py compile`
- The compiled `.mo` files are shipped in the wheel from `assets/locales`.

Tools
- `tools/make_i18n.py` — primary helper for extract/init/update/compile (targets `assets/locales`).
- `tools/audit_messages.py` — optional QA to spot duplicates and accelerator issues.
  - Scans `src/ttkbootstrap/assets/locales` by default.
  
Note: Legacy migration helpers (e.g., `convert_msgs_to_po.py`, `sync_locales_to_package.py`) have been removed. The workflow compiles directly to `assets/locales`.

Contribution notes
- Prefer base locales (`de`, `fr`, `nl`) unless region-specific differences are required (for example `pt_BR`).
- Avoid embedding mnemonics `&` in messages; MessageCatalog strips them when rendering.
- Keep message ids consistent (case and punctuation) to avoid duplicates.
- Optional: audit keys with `python tools/audit_messages.py`.

Demos
- `examples/localization_widgets_demo.py` - shows `_()` usage and `<<LocaleChanged>>` auto-refresh.
- `examples/runtime_overrides_demo.py` - shows `set`/`set_many` for messages not in catalogs yet.

Contributors
- Where to place translations:
  - Add or edit `.po` files under `src/ttkbootstrap/assets/locales/<lang>/LC_MESSAGES/ttkbootstrap.po`.
  - Compile to `.mo` with `python tools/make_i18n.py compile`.
- Workflow for a new language:
  1) Extract: `python tools/make_i18n.py extract`
  2) Init: `python tools/make_i18n.py init -l <lang>`
  3) Translate the new `.po` file
  4) Compile: `python tools/make_i18n.py compile`
- Minimum keys to translate for a new language (baseline UI):
  - OK, Ok, Retry, Delete, Next, Prev, Previous
  - Yes, No, Open, Close, Add, Remove, Submit, Cancel
  - Family, Weight, Slant, Effects, Preview, Size
  - Should be of data type, Invalid data type
  - Number cannot be greater than, Number cannot be less than, Out of range
  - The quick brown fox jumps over the lazy dog.
  - Font Selector, Color Chooser, Advanced, Themed, Standard
  - Current, New, Hue, Sat, Lum, Hex, Red, Green, Blue
  - color dropper, Search, Page, of
  - Reset table, Columns, Move, Align
  - Hide column, Delete column, Show All
  - Move to left, Move to right, Move to first, Move to last
  - Align left, Align center, Align right
  - Sort, Filter, Export, Delete selected rows
  - Sort Ascending, Sort Descending, Clear filters
  - Filter by cell's value, Hide select rows, Show only select rows
  - Export all records, Export current page, Export current selection, Export records in filter
  - Move up, Move down, Move to top, Move to bottom
  - Mo, Tu, We, Th, Fr, Sa, Su
