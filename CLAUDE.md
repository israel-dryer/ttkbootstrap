# Repo overview

ttkbootstrap is a themed widget framework and application toolkit built
on top of Tk. The library lives under `src/ttkbootstrap/` and ships
widgets, dialogs, a styling engine, data sources, an i18n stack, and an
application runtime.

The public API surface is the union of:

- `src/ttkbootstrap/__init__.py` — top-level lazy re-exports.
- `src/ttkbootstrap/api/*.py` — grouped public exports (app, widgets,
  style, dialogs, data, i18n, utils, menu, localization).

Anything not surfaced through those modules is internal.

---

## Active work: docs review and cleanup

A multi-phase documentation overhaul is in progress on branch
`docs/review-and-cleanup`. The source of truth is:

- `analysis/docs-review-and-plan.md`

Read that first when picking up any docs work. It captures:

- the documentation model (user-guide pages vs API-spec pages),
- the docstring template (Google style, plain Markdown),
- the conventions (no `bootstyle` in narrative, examples off by default,
  "spec, not user guide" — mechanical not editorial),
- the per-symbol status of the priority API surface,
- the phased plan and the decisions log.

Do not re-derive any of those from scratch — propose updates to the
plan doc instead so they survive across sessions.

### Current handoff (2026-04-30, layout sweep — 5/12, anchor + LabelFrame + Card + PackFrame + GridFrame)

Phases 1–7, 9A–9D are complete. **Phase 6 (screenshot pipeline) is partially
complete; 6F not started. Pass 2 (editorial review) is the active work —
the dialogs sweep (11/11) and data-display sweep (8/8) are complete. The
**layout sweep** is now the active sweep: the layout template was
restructured to the slim arc in commit `997a5b7`, with `frame.md` rewritten
as the canonical anchor. `labelframe.md`, `card.md`, `packframe.md`, and
`gridframe.md` are done. Remaining 7 pages: `accordion.md`, `expander.md`,
`panedwindow.md`, `scrollbar.md`, `scrollview.md`, `separator.md`,
`sizegrip.md`. Then move to one of navigation / overlays / selection /
forms / views / primitives. The remaining 4 templates (form, navigation,
overlay, selection) still need the editorial pass at the start of each
sweep (see "Template arc" below).**

### Template arc (apply to every editorial sweep)

The `widget-input-template.md` arc (Basic usage → Value model → API →
guidance) is now the universal pattern. When opening any new sweep,
audit the category's template against these principles before
touching pages:

1. **Lead with `Basic usage` after the intro.** No `Framework
   integration` lead — its content distributes into Common options,
   Behavior, Events, and Localization & reactivity.
2. **A category-appropriate mental-model section sits right after
   Basic usage** (Value model / Result value / Data model /
   Lifecycle / Selection model / Navigation model / Form model).
   Action widgets don't get one — `command` isn't a model.
3. **API consolidates into `Common options` / `Behavior` / `Events`.**
   Don't fragment with separate `Styling`, `Localization`, or
   `Binding to signals` H2s — those go inline or into Common options.
4. **`What problem it solves` and `Core concepts` are padding by
   default.** Drop them; bring back per-page only when there's
   substantive content the other sections can't carry.
5. **`When should I use X?` sits near the bottom** — readers see the
   API before the recommendation.
6. **Optional sections** are marked with `*Optional` italic prose
   under the heading; `tools/check_doc_structure.py` drops those from
   the required list.

Templates already restructured to this arc:
- `widget-input-template.md` (was already correct — anchored on
  `textentry.md`).
- `widget-dialog-template.md` (commit `7667e36`).
- `widget-action-template.md` (commit `7667e36`).
- `widget-data-display-template.md` (commit `6dae13a`, anchored on
  `label.md`). `Data model` and `Performance guidance` are
  `*Optional` so simple display widgets (Label, Badge, Progressbar,
  Floodgauge, Meter) skip them while data-bound widgets (TableView,
  TreeView, ListView) fill them in.
- `widget-layout-template.md` (commit `997a5b7`, anchored on
  `frame.md`). `Layout model` is `*Optional` so plain containers
  (Frame, Card, LabelFrame, Separator, Sizegrip) skip it while
  widgets with non-trivial geometry semantics (PackFrame, GridFrame,
  Accordion, PanedWindow, ScrollView) fill it in.

Remaining 4 templates (form, navigation, overlay, selection) still
lead with `Framework integration` etc. Apply the editorial pass at
the start of each category's sweep — those categories have 0 pages
written, so the template fix is free.

Phase 6 status (for reference):

- **6A–6E — DONE.** Image policy locked, renderer scaffold built, CLI wired,
  image-check tool added, in-frame shots rendered for all visible widget pages
  (13 batches). Shots are macOS placeholders; re-render on Windows for canonical
  assets (`python -m docs_scripts.render` on a Windows host overwrites every asset).
- **6F — NOT STARTED.** Popup and animated widgets need capture tooling beyond
  the in-frame model. See `analysis/docs-review-and-plan.md` § Phase 6F for the
  full list and the renderer mode needed.

Phase 9 (drift sweep) — DONE:

- `tools/check_doc_snippets.py` validates all 833 `python` blocks across 107
  docs files (compile check always; runtime check with `--run`). Currently 0
  failures. Run this before and after any docs edit to guard against regression.
- 22 doc files were fixed in Pass 1 (wrong class names, constructor kwargs,
  option names, theme names). See plan doc § Phase 9 for the full list.
- `OptionMenu(command=)` and `DropdownButton(command=)` now work (9C).
- `ttk.ListView` is now a public export (9D).

Open items from earlier phases (do not lose track):

- **8B** — `ListView.badge` field silently dropped in `update_data`
  (`listitem.py:725`). Code fix: add `"badge": self._update_badge` to the
  dispatch map.
- **8C** — Rendered docstring review for 22 priority symbols (needs display).

### Now: Pass 2 — Editorial review (Opus, one guide per session)

Pass 1 is done; every snippet is known to match the current API. Pass 2 is
the active work. Goal: each guide is best-in-class for its content type.

**All 14 guides in `docs/guides/` are done** (2026-04-30). Widget pages
in progress; platform/capabilities pages still to come.

**Widget pages — actions** (`docs/widgets/actions/`) — **DONE 2026-04-30
(re-reviewed against slim template).**

All 5 pages restructured to the slim action template (commit
`0fed5b8`): leading `Framework integration` dropped, `Appearance`
folded into `Common options` (with an option-summary table at the
top), real `Events` section added per page, `When to use` renamed
and moved near the bottom as `When should I use WidgetName?`,
`Additional resources` split into `Related widgets` + `Reference`.

`button.md` is the canonical anchor for the new action-page shape;
the other four (`buttongroup.md`, `contextmenu.md`,
`dropdownbutton.md`, `menubutton.md`) follow it.

`tools/check_doc_structure.py --category actions` → 5/5 pass.

**Widget pages — inputs** (`docs/widgets/inputs/`, 10 pages) — **DONE 2026-04-30.**

All 10 pages reviewed against `docs/_template/widget-input-template.md`.
Inputs use a **different template** than actions — don't carry the
actions section names over verbatim.

Last session (2026-04-30):

- `scrolledtext.md` — restructured to template; clarified that
  `ScrolledText` has **no `value`/signal/variable model** (it wraps
  `tkinter.Text`), corrected the existing claim that the container
  themes via `accent` (it's `scrollbar_style`), documented the
  delegation surface (Text methods copied at construct time, plus
  `__getattr__` fallback to `self._text`), and replaced the wrong
  default in the old Quick start (default `scrollbar_visibility` is
  `'always'`, not `'scroll'`).

Prior session (2026-04-30, two-page batch):

- `scale.md` — restructured to template; corrected event hooks
  (Scale exposes `command` / `signal.subscribe` / `<ButtonRelease-1>`,
  *not* `on_input`/`on_changed`); removed non-existent `step` option.
- `labeledscale.md` — restructured to template; clarified that
  `accent` only styles the inner scale, that `signal=` is rejected
  (use `widget.scale.signal` for reactive subs), and that range
  reconfiguration must go through the inner scale (the
  `LabeledScale.configure(minvalue=…)` path is broken — see bugs list).

`tools/check_doc_structure.py --category inputs` → 10/10 pass.

Template: `docs/_template/widget-input-template.md`. Required H2s:

- `Basic usage`
- `Value model` *(what `value` means, live vs committed changes,
  empty/none/invalid representation, signal vs variable)*
- `Common options` *(curated, not an API dump)*
- `Behavior` *(widget-specific: formatting, filtering, popup, stepping…)*
- `Events` *(`on_input` for live, `on_changed` for committed)*
- `Validation and constraints`
- `When should I use WidgetName?`
- `Related widgets`
- `Reference`

Pages to review:

- [x] `textentry.md` — **canonical input pattern**; use this as the
      reference for the inputs sweep, the way `button.md` anchored actions
- [x] `numericentry.md`
- [x] `passwordentry.md`
- [x] `pathentry.md`
- [x] `dateentry.md`
- [x] `timeentry.md`
- [x] `spinnerentry.md`
- [x] `scale.md`
- [x] `labeledscale.md`
- [x] `scrolledtext.md`

**Widget pages — dialogs** (`docs/widgets/dialogs/`, 11 pages) —
**DONE 2026-04-30 (11/11).**

Template: `docs/_template/widget-dialog-template.md` (slim arc,
restructured commit `7667e36`). Required H2s: `Basic usage`,
`Result value`, `Common options`, `Behavior`, `Events`,
`When should I use WidgetName?`, `Additional resources` (with
sub-bullets for Related widgets / Framework concepts / API
reference). Optional via `*Optional` prose: `UX guidance`.

`messagedialog.md` is the canonical anchor for the dialogs sweep.
The other 10 (`messagebox.md`, `querydialog.md`, `querybox.md`,
`formdialog.md`, `dialog.md`, `datedialog.md`, `colorchooser.md`,
`colordropper.md`, `fontdialog.md`, `filterdialog.md`) follow it.

`tools/check_doc_structure.py --category dialogs` → 11/11 pass.

Patterns / non-obvious behavior worth remembering across the
dialogs surface (full per-session detail lives in commit messages):

- `MessageDialog`, `FormDialog`, `FilterDialog` all default to
  translation-key button labels (`button.ok` / `button.cancel`)
  but have **no `localize` flag** — vanilla construction shows
  literal key strings. (Bugs list.)
- `<<DialogResult>>` event payload is `{"result": ..., "confirmed":
  bool}`; `on_dialog_result` helper passes the **full payload
  dict**, not the unwrapped result.
- `Dialog` (base) does NOT fire `<<DialogResult>>` and has no
  `on_dialog_result` helper — those are added by subclasses.
- `ColorDropperDialog.show()` is **non-blocking** (no
  `wait_window()`) — unlike every other dialog. Callers must
  trace the `result` Variable, register `on_dialog_result` after
  `show()`, or use `wait_variable()` manually.
- `FilterDialog` is a `Frame` subclass that *composes* a Dialog
  on `show()`, not a Dialog subclass — events fire on the frame,
  the event surface uses `<<SelectionChange>>` with payload
  `{"selected": list}` instead of the framework-standard
  `<<DialogResult>>`. (Bugs list.)
- `FontDialog.default_font` is a **named-font name string**
  (`"TkDefaultFont"`), NOT a `Font` instance.

(Per-session detail for each dialog rewrite — including the
specific old-page errors corrected and bug numbers surfaced — is
captured in the commit messages on `docs/review-and-cleanup`. See
`Docs: editorial review — <DialogName> ...` from 2026-04-30.)

### Widget pages — data-display (`docs/widgets/data-display/`, 8 pages) — DONE 2026-04-30

Template: `docs/_template/widget-data-display-template.md`
(restructured to slim arc commit `6dae13a`). Required H2s:

- `Basic usage`
- `Common options`
- `Behavior`
- `Events`
- `When should I use WidgetName?`
- `Related widgets`
- `Reference`

Optional (declared via `*Optional` prose under the heading):

- `Data model` — required for data-bound widgets (TableView,
  TreeView, ListView). Skip for read-only status/progress
  widgets (Label, Badge, Progressbar, Floodgauge, Meter).
- `Performance guidance` — include for widgets that scale with
  row count. Skip for lightweight status/progress widgets.

Last session (2026-04-30, treeview sweep — final data-display page):

- `treeview.md` rewritten to the slim data-display template.
  TreeView is **not** a data-bound widget (despite its position
  alongside ListView and TableView): it's a thin themed wrapper
  over `ttk.Treeview` that exposes the full ttk API
  (`insert` / `delete` / `move` / `item` / `set` /
  `selection_*` / `tag_configure` / etc.) with no datasource
  binding and no `signal=` channel. The rewrite still includes
  `Data model` and `Performance guidance` because the
  hierarchical-iid item model and the lack of virtualization
  are both first-class facts the page needs to surface. Three
  things the old page got wrong or omitted:
  (1) the old `Appearance` example showed
  `ttk.Treeview(app, accent="primary")`; the TreeView style
  builder (`style/builders/treeview.py`) does **not** consume
  `accent` at all — the actual styling tokens are
  `surface`, `select_background` (default `"primary"`),
  `header_background`, `border_color`, and `show_border`.
  Documented these in `Common options` and called out that
  `accent` is silently ignored.
  (2) the old page didn't mention the `Treeview` (lowercase)
  back-compat alias — both `ttk.Treeview` and `ttk.TreeView`
  construct the same class via `__init__.py:135`.
  (3) the old `Events` section listed `<<TreeviewSelect>>` /
  `<<TreeviewOpen>>` / `<<TreeviewClose>>` without naming
  them as ttk-emitted (no `on_*` helpers exist on TreeView)
  and without explaining how to identify the affected row
  (read `tv.selection()` / `tv.focus()` from the widget;
  `event.data` is empty for these). Replaced with a payload
  table and an example using `tv.identify_row(event.y)` for
  raw click handling.
  Also surfaced display-mode semantics (`"tree"` vs
  `"headings"` vs `"tree headings"` vs `""`), the four
  per-row item fields (`iid` / `parent` / `text` / `values` /
  `open` / `tags` / `image`), tag-based styling and
  `tag_bind`, the indicator-rendering Tk 8.6.13+ regression
  workaround, density semantics, lazy-expansion patterns for
  large hierarchies, and the `detach`/`reattach` vs
  `delete`/re-insert performance trade-off. Common options
  consolidates into a 13-row table; deliberate negative
  framing kept around the no-virtualization /
  no-datasource-binding facts.

`tools/check_doc_structure.py --category data-display` →
8/8 passing.
`tools/check_doc_snippets.py --run --file
docs/widgets/data-display/treeview.md` → 0 failures.

Earlier session (2026-04-30, tableview sweep):

- `tableview.md` rewritten to the slim data-display template.
  TableView is the **second data-bound** page in the sweep, so it
  carries `Data model` and `Performance guidance` like ListView.
  Three things the old page got wrong or omitted:
  (1) the old page framed TableView as a generic "tabular data view"
  with no mention of its **SQLite backbone**. TableView is built
  on `SqliteDataSource` (in-memory by default) — filter is a SQL
  WHERE clause, sort is ORDER BY, the search bar generates a
  `LIKE` (or `=`/`STARTS_WITH`/`ENDS_WITH`/raw SQL) WHERE clause
  across all columns. Documented `set_filters(where: str)`,
  advanced search "SQL" mode, and `set_sorting(key)` as
  **trusted-input** APIs that interpolate directly into SQL —
  surfaced as a `!!! danger` block in the rewrite.
  (2) the old `Events` section was a flat list with no payloads;
  promoted to a payload table covering all 8 events
  (`<<SelectionChange>>` carries `{records, iids}`, `<<RowClick>>`
  / `<<RowDoubleClick>>` / `<<RowRightClick>>` carry
  `{record, iid}`, `<<RowInsert>>` / `<<RowUpdate>>` /
  `<<RowDelete>>` / `<<RowMove>>` carry `{records: list[dict]}`).
  Surfaced the export-events bug as a `!!! warning`: the three
  `<<TableViewExport*>>` events are emitted on `self._tree` (the
  inner private TreeView), not on the TableView, and there are no
  `on_export_*` helpers — listeners must bind to the private
  inner widget today.
  (3) the old page omitted half the constructor surface: no
  `sorting_mode`, no `search_mode`/`search_trigger`, no
  `paging_mode`, no `enable_filtering` / `enable_header_filtering`
  / `enable_row_filtering`, no `allow_grouping` /
  `show_table_status` / `show_column_chooser` / `context_menus`,
  no `column_min_width`, no `form_options`. Consolidated all
  ~30 ctor params into a single Common options table; expanded
  the column-dict shape (`text` / `key` / `width` / `minwidth` /
  `anchor` / `align` / `dtype` / `type` / `editor` /
  `editor_options` / `readonly` / `required`) and documented
  the auto-anchor inference (numeric → "e", text → "w",
  fallback samples 20 rows).
  Also documented grouping (`set_grouping` / `clear_grouping` /
  `expand_all` / `collapse_all`), hide/unhide for rows and
  columns, virtual paging's 85 % prefetch threshold, the
  generated `FormDialog` with role-based Cancel / Delete / Save
  buttons, the `Tableview = TableView` legacy alias, and the
  page LRU cache (`page_cache_size`, default 3).

Prior session (2026-04-30, listview sweep — first data-bound page):

- `listview.md` rewritten to the slim data-display template
  (slim arc commit `6dae13a`). ListView is the **first
  data-bound** page in the sweep, so it fills in the optional
  `Data model` and `Performance guidance` sections that the
  read-only widgets (Label, Badge, Progressbar, FloodGauge,
  Meter) skipped. Three things the old page got wrong or
  omitted:
  (1) the old "Reactivity" section claimed `items=` accepts a
  `Signal` and bound it like
  `ttk.ListView(app, items=signal)`. That path doesn't bind
  anything — `items=` is iterated immediately by the internal
  `MemoryDataSource.set_data()`, so a `Signal` is either
  treated as opaque or fails outright. ListView has **no
  SignalMixin** and no signal-bound `items` channel. Mutation
  goes through `insert_item` / `update_item` / `delete_item` /
  `reload`, plus `datasource=` for external state.
  (2) the old "Data model" subsection only listed recognized
  record fields. Documented the **full `DataSourceProtocol`
  surface** (`total_count`, `get_page_from_index`,
  `is_selected`, `select_record` / `deselect_record` /
  `deselect_all`, `get_selected`, CRUD, `reload`, optional
  `move_record`) and surfaced the already-known mismatch with
  `BaseDataSource` — the framework's
  `ttkbootstrap.datasource.MemoryDataSource` /
  `SqliteDataSource` / `FileDataSource` use
  `unselect_record`/`unselect_all` and **no `is_selected`**, so
  they do not satisfy ListView's protocol as-shipped.
  (3) the old `Events` section was a flat bullet list with no
  payload information and inflated some payloads
  (`<<ItemDelete>>` was claimed to carry `event.data =
  {'record': dict}`, but `_on_item_removing` and `delete_item`
  pass no data — `event.data` arrives as `None`). Replaced
  with a payload table that names what actually arrives:
  `None` for `<<SelectionChange>>` / `<<ItemDelete>>` /
  `<<ItemDeleteFail>>` / `<<ItemInsert>>` / `<<ItemUpdate>>`;
  record dict for `<<ItemClick>>`; full drag payload for the
  three drag events.
  Also added a positive `Performance guidance` section calling
  out the `select_all()` cost (loads all records via
  `get_page_from_index(0, total)`), the `MemoryDataSource`
  index rebuild on delete/move, the per-scroll cost of
  `update_data`, and the recommendation to batch external
  updates and call `reload()` once. Common options consolidates
  into a 16-row table.

Prior session (2026-04-30, meter sweep):

- `meter.md` rewritten to the slim template. The old page was
  built around the **deprecated** legacy parameter names
  (`amountused`, `amounttotal`, `subtext`, `stripethickness`,
  `metersize`); they still work via `_coerce_legacy_params` but
  emit `DeprecationWarning`. The rewrite uses the modern names
  throughout (`value`, `maxvalue`, `subtitle`, `segment_width`,
  `size`). Three things the old page got wrong or omitted:
  (1) the old "Reactivity" section bound a `Signal` via
  `ttk.Meter(app, amountused=usage, amounttotal=100)` —
  Meter has **no SignalMixin** and **no public `variable=`
  parameter**; it owns its internal `IntVar`/`DoubleVar` and the
  reactive surface is `<<Change>>` / `on_changed()`, plus the
  four equivalent value-setter paths (`.value` property,
  `set()`, `configure(value=…)`, `step()`).
  (2) the old page never named the **four indicator shapes**
  produced by combining `segment_width` and `indicator_width`
  (solid sweep / floating wedge / segmented sweep / wedge over
  segments) — these are first-class Meter axes. Documented as a
  table.
  (3) the old `Common options` section omitted `meter_type`
  ("full" vs "semi"), `arc_range` / `arc_offset` (custom sweeps),
  and `dtype` (int/float, **construction-only** — reconfiguring
  later emits `ConfigurationWarning` and is silently ignored).
  Also documented the bouncing semantics of `step()` (flips
  direction at min/max), the interactive mode (click/drag on the
  arc, clamped through `step_size`), and that `<<Change>>` does
  not re-fire on duplicate writes. Common-options consolidates
  into a 21-row table; added a positive `Events` section
  (Meter is the only data-display widget so far that emits a
  virtual event — Label, Badge, Progressbar, and FloodGauge all
  have negative Events sections).

Earlier session (2026-04-30, floodgauge sweep):

- `floodgauge.md` rewritten to the slim template. Corrects two
  things the old page got wrong and surfaces several missing
  facts. (1) The old "Reactivity" section showed
  `ttk.FloodGauge(app, value=level)` with a `Signal` — that path
  fails type-wise (`value: int = 0`) and there's **no SignalMixin**
  on FloodGauge; the widget inherits only `ConfigureDelegationMixin`
  + `Canvas`. Reactivity goes through `variable=IntVar(...)` /
  `textvariable=StringVar(...)`. (2) The old "Behavior" claim that
  "color/style can change based on threshold values" implied a
  built-in threshold mapping; there is none — callers must
  reconfigure `accent` themselves. The rewrite documents the
  actual surface: `mask` (format string with `{}` for the value,
  the most distinctive feature), `text` (static caption when
  `mask` is unset), `thickness` (cross-axis size), the bouncing
  pulse animation in indeterminate mode, the wrapping `step()`
  semantics (`(value + amount) % (maximum + 1)`), the auto-advance
  side effect of `start()` in determinate mode, and repaint
  triggers (`<Configure>`, `<<ThemeChanged>>`, variable writes).
  Added a deliberate negative `Events` section: no virtual events,
  no `on_*` helpers — observe via `variable.trace_add(...)`.
  Common options consolidates into a 13-row table.

Even earlier session (2026-04-30, progressbar sweep):

- `progressbar.md` rewritten to the slim template. Corrects
  three things the old page got wrong or omitted:
  (1) the old "Reactivity" section showed
  `ttk.Progressbar(app, value=progress)` as the way to bind a
  Signal — that path does **not** create a binding, it sets
  `value` once to the signal's stringified repr; the right
  hook is `signal=` (or `variable=`), routed through
  `SignalMixin` to the Tcl `variable=` option ttk.Progressbar
  exposes natively.
  (2) the old page never named the `variant` axis
  (`default` / `striped` / `thin`) — it's first-class on
  ttkbootstrap Progressbar and registered in
  `style/builders/progressbar.py`.
  (3) `start(interval=10)` was wrong-by-trivia; the
  ttk default is 50 ms. Documented it as such.
  Added a deliberate negative `Events` section: Progressbar
  has no `on_*` helpers and emits no virtual events — observe
  changes via `widget.signal.subscribe(...)`. Common-options
  consolidates into a 12-row table; `length` clarified as
  along-orientation (height for vertical bars).

Earlier still (2026-04-30, badge sweep):

- `badge.md` rewritten to the slim template. Corrects the
  framing the old page papered over: Badge is **not** a Label
  with "badge styling" applied — it's a Label whose `accent`
  drives the chip *fill* (background) and whose foreground is
  auto-selected as the readable contrast color via
  `b.on_color(accent)`. This is the inverse of Label, where
  `accent` only tints foreground. Documented the `variant` axis
  (`square` default, `pill` opt-in), the actual Badge defaults
  from `widgets/primitives/badge.py` (`anchor="center"`,
  `font="-size 8"`, `variant="square"`), and the `accent or
  'primary'` fallback in the builder.
  Common-options consolidates into a 17-row table; `bootstyle`
  references and the raw-Tk `foreground`/`background` options
  removed from the surface (Badge's chip color goes through
  `accent` + `surface`).
  Added a deliberate negative `Events` section so readers don't
  hunt for `on_*` helpers Badge doesn't expose.

Earliest session (2026-04-30, label sweep — anchor):

- `label.md` rewritten as the canonical anchor for the
  data-display sweep. Frames Label as the foundational read-only
  display widget that Badge, Field labels, and several
  composites are built on. Three subtleties surfaced in
  narrative: (1) `accent` controls the **foreground** color, NOT
  a chip background — readers expecting a high-contrast pill are
  routed to Badge; (2) Label has no `on_*` event helpers and
  emits no virtual events; (3) `surface=` is the right knob if
  you need a colored background on a Label.

`tools/check_doc_structure.py --category data-display` → 8/8
passing (label, badge, progressbar, floodgauge, meter, listview,
tableview, treeview). Sweep complete.

Pages to review (canonical anchor: `label.md`):

- [x] `label.md` — anchor for the data-display sweep
- [x] `badge.md` — extends Label; compact pill chip
- [x] `progressbar.md` — linear determinate/indeterminate progress
- [x] `floodgauge.md` — canvas-drawn fill with inline label
- [x] `meter.md` — radial gauge with central readout
- [x] `listview.md` — first data-bound widget; uses Data model
- [x] `tableview.md` — second data-bound widget; SQLite-backed
- [x] `treeview.md` — thin themed wrapper over ttk.Treeview

### Widget pages — layout (`docs/widgets/layout/`, 12 pages) — IN PROGRESS 2/12

Template: `docs/_template/widget-layout-template.md` (slim arc,
restructured commit `997a5b7`). Required H2s: `Basic usage`,
`Common options`, `Behavior`, `Events`,
`When should I use WidgetName?`, `Related widgets`, `Reference`.
Optional via `*Optional` prose: `Layout model` — fill in for widgets
with non-trivial geometry semantics (PackFrame's `gap`/`orient`,
GridFrame's `columns`/`rows`, Accordion expand/collapse, PanedWindow
sashes, ScrollView viewport); skip for plain containers (Frame, Card,
LabelFrame, Separator, Sizegrip).

`frame.md` is the canonical anchor for the layout sweep, the way
`button.md` / `textentry.md` / `messagedialog.md` / `label.md`
anchored their respective categories.

Last session (2026-04-30, gridframe sweep):

- `gridframe.md` was already structurally aligned with the slim
  layout template (commit `997a5b7`); this pass was an accuracy
  cleanup against `widgets/primitives/gridframe.py`. Five fixes:
  (1) the Gap subsection's `padx=4` example claimed
  `padx=(14, 4)` for a single button, but cell (0, 0) gets no
  gap injection — only column ≥ 1 cells do. Verified at runtime:
  with `gap=10, padx=4` on a 3-button row, A→`4`, B→`(14, 4)`,
  C→`(14, 4)`. Replaced the example accordingly.
  (2) the `auto_flow` table mischaracterized dense modes as
  "search for the smallest free area"; the implementation
  iterates row-major (or column-major) from `(0, 0)` and returns
  the first cell where the rectangle fits — correct CSS-Grid
  `dense` semantics ("earlier holes get filled in") but not
  "smallest area". Reworded.
  (3) added the explicit-row-or-column footgun: passing only
  `row=` (or only `column=`) to `grid()` is silently ignored,
  since the explicit branch in `_on_child_grid` (`gridframe.py:
  407-408`) requires both. Auto-placement still runs and the
  cursor's next free cell wins. Verified at runtime: with
  `columns=3`, `Button.grid(row=5)` lands at `(0, 1)`, not
  `(5, 0)`.
  (4) added the column-major mirror caveat: just as
  `auto_flow="row"` without `columns=` stacks along a single
  row (the `_num_columns=100` placeholder), `auto_flow="column"`
  without `rows=` stacks along a single column.
  (5) tightened the `auto_flow="none"` row to call out that the
  second implicit child overlaps the first at `(0, 0)` —
  `_find_next_position` returns `(0, 0)` unconditionally in
  this mode, ignoring the `_occupied` set.
  Other key facts on the page (kept from the prior version, all
  verified): `int n` → `(weight=n, minsize=0)`; `"auto"` →
  `(0, 0)`; `"Npx"` → `(0, N)` (not a hard cap); `gap` is the
  only GridFrame-specific option wired through configure-delegate
  (`configure(gap=…)` triggers `_regrid_all`); `rows`/`columns`/
  `sticky_items`/`auto_flow` are construction-only; `propagate=
  False` only calls `grid_propagate(False)` (inverse of
  PackFrame's `pack_propagate(False)`); `grid_remove()` keeps
  the widget tracked, `grid_forget()` discards tracking.

`tools/check_doc_structure.py --category layout` → gridframe.md
not in the failing list (7/12 pages still pending).
`tools/check_doc_snippets.py --run --file
docs/widgets/layout/gridframe.md` → 0 failures (11 snippets,
1 executed).

Prior session (2026-04-30, packframe sweep):

- `packframe.md` rewritten to the slim layout template. PackFrame is
  the fourth page in the sweep — a `Frame` subclass that intercepts
  child `pack()` calls via `_on_child_pack` to inject a default
  `side` (from `direction`), a leading-edge `padx`/`pady` for `gap`,
  and optional `fill_items`/`expand_items`/`anchor_items` defaults.
  Restructured around the optional `Layout model` section (filled in
  for the first time in this sweep — Frame, LabelFrame, and Card all
  skipped it). Two narrative fixes vs the old page:
  (1) the old `Appearance` example used `accent="secondary"` and
  framed it as a styling shortcut, but didn't note that on container
  classes the bootstyle constructor wrapper rewrites `accent` as a
  `surface` override (`style/bootstyle.py:464`). Verified at runtime:
  `PackFrame(app, accent='primary')` produces `_surface='primary'`,
  `style_options={'surface': 'primary'}`, rendered style
  `bs[…].primary.TFrame`. Documented as a Common-options table row
  rather than a separate Appearance section.
  (2) the old "Behavior" bullet list never named the **direction →
  side mapping** (which is the only thing PackFrame actually does
  beyond Frame). Promoted to a 6-row table in `Layout model`:
  `vertical`/`column` → `top`, `column-reverse` → `bottom`,
  `horizontal`/`row` → `left`, `row-reverse` → `right`. Surfaced
  the gotcha that overriding `side=` per-call breaks the gap math
  because `_compute_gap` assumes every managed child uses the
  direction's side.
  Other additions: gap is implemented as a **leading** `padx`/`pady`
  on second-and-later items (verified via `pack_info`: first item
  `pady=0`, others `pady=(8, 0)` for `gap=8`); reconfiguring
  `direction`/`gap` triggers a full `_repack_all` (verified — items
  switch from `pady=(8,0), side="top"` to `padx=(12,0), side="left"`
  cleanly); `propagate=False` only sets `pack_propagate` (not
  `grid_propagate`); `before=`/`after=` reference widgets must
  already be managed by this PackFrame; raw `tkinter` widgets
  without `PackMixin` skip the hooks; `fill_items`/`expand_items`/
  `anchor_items` are read at each `pack()` call so changing them
  later only affects subsequently-added widgets.

`tools/check_doc_structure.py --category layout` → packframe.md no
longer in the missing-sections list (8/12 pages still pending).
`tools/check_doc_snippets.py --run --file
docs/widgets/layout/packframe.md` → 0 failures (6 snippets, 1
executed).

Prior session (2026-04-30, card sweep):

- `card.md` rewritten to the slim layout template. Card is the third
  page in the sweep — a `Frame` subclass with three constructor
  defaults (`accent='card'`, `show_border=True`, `padding=16`). Two
  framing fixes and several additions:
  (1) the old intro framed Card as a "convenience wrapper around
  Frame with `surface='card'` and `show_border=True` by default" —
  the actual default is `accent='card'`
  (`widgets/primitives/card.py:69`); the container-class rerouting
  in `style/bootstyle.py:464` then turns that into `surface='card'`
  because `TFrame` is in `CONTAINER_CLASSES`. Documented the real
  path and noted that the Frame style builder
  (`style/builders/frame.py:9`) reads only `surface`, not `accent`.
  Verified at runtime: `Card(app)` produces `_accent='card'`,
  `_surface='card'`, `style_options={'show_border': True,
  'surface': 'card'}`, `padding=(16,)`, style
  `bs[…].card.TFrame`.
  (2) the old page never described the `card` token itself.
  Documented that `card` is a tinted theme surface defined in
  `style/theme_provider.py:356,368` (slightly elevated tint
  relative to the page background, in both light and dark modes).
  Other additions: `padding` semantics (int / 2-tuple / 4-tuple);
  `bootstyle` mutual-exclusion with `accent`/`variant` (which
  suppresses Card's accent default); surface-cascade noted as
  inherited from Frame (Card unlike LabelFrame has the
  `_refresh_descendant_surfaces` hook for free); negative `Events`
  section so readers don't hunt for `on_*` helpers Card doesn't
  expose.

Earlier session (2026-04-30, labelframe sweep):

- `labelframe.md` rewritten to the slim layout template. LabelFrame
  is the second page in the sweep — a thin themed wrapper over
  `ttk.Labelframe` that draws a 1px border with an embedded text
  label. Three things the old page got wrong or omitted, plus
  several gaps surfaced:
  (1) the old "Appearance" example showed
  `ttk.LabelFrame(app, text="Group", style="Card.TLabelframe")`;
  `Card.TLabelframe` is **not a registered style** anywhere in the
  framework (no builder registers it). Replaced with the canonical
  surface/accent path.
  (2) the old page never mentioned the **container-accent →
  surface override** behavior. The bootstyle constructor wrapper
  treats `TLabelframe` as a `CONTAINER_CLASS` (alongside `TFrame`),
  so passing `accent="primary"` on a LabelFrame resolves to
  `surface="primary"` and tints the LabelFrame's background — not
  silently ignored. Verified at runtime: `lf._accent='primary'`,
  `lf._surface='primary'`, `lf._style_options={'surface': 'primary'}`,
  rendered style `bs[…].primary.TLabelframe`. Documented as
  `accent` and `surface` being interchangeable on container widgets.
  (3) the old page treated LabelFrame as a Frame variant, but
  LabelFrame **does not subclass Frame**. It misses Frame's
  `_refresh_descendant_surfaces` and `_refresh_descendant_input_backgrounds`
  cascade hooks, so runtime surface reconfiguration restyles only
  the LabelFrame itself — child widgets stay on their old surface.
  Documented this as a deliberate divergence in `Behavior`.
  Also surfaced: the **`show_border` gap** (the LabelFrame style
  builder reads it and defaults to True, but `LabelFrame.__init__`
  doesn't capture it from kwargs, so passing `show_border=False`
  raises `TclError: unknown option "-show_border"` — the border is
  effectively always on); the **`variant` raises** behavior (only
  `default` registered, so any other variant raises
  `BootstyleBuilderError`); the `labelwidget=` option for replacing
  the text label with a custom widget; and the standard
  geometry-propagation note.

`tools/check_doc_structure.py --category layout` → card.md no
longer in the missing-sections list (9/12 pages still pending,
all in the existing-but-pre-template state).
`tools/check_doc_snippets.py --run --file
docs/widgets/layout/card.md` → 0 failures (3 snippets, 1
executed).

Pages to review (canonical anchor: `frame.md`):

- [x] `frame.md` — anchor for the layout sweep
- [x] `labelframe.md` — titled bordered Frame variant
- [x] `card.md` — Frame subclass with `accent='card'` + border preset
- [x] `packframe.md` — Frame subclass with auto-pack + `gap`
- [x] `gridframe.md` — Frame subclass with declarative rows/columns
- [ ] `panedwindow.md` — resizable split regions
- [ ] `scrollview.md` — scrollable viewport over a content frame
- [ ] `scrollbar.md` — themed ttk.Scrollbar wrapper
- [ ] `accordion.md` — expandable sections
- [ ] `expander.md` — single collapsible region
- [ ] `separator.md` — visual divider
- [ ] `sizegrip.md` — bottom-right resize handle

### Workflow (one page per session)

1. Read the page end-to-end.
2. Find the right template under `docs/_template/`.
3. Rewrite in one pass.
4. `python tools/check_doc_structure.py --category <cat>` and
   `python tools/check_doc_snippets.py --run --file <page>` — both
   must pass.
5. Commit: `Docs: editorial review — <page title>`.

The structure check substitutes the literal `WidgetName` in the
template's H2s with the page's H1, so a page can use
`## When should I use TextEntry?` and still satisfy the template's
`## When should I use WidgetName?` requirement.

Run **one page at a time** as a deliberate session. Each session covers:

- **Structural fit** — does the page follow the right template for its content
  type? Use `python tools/check_doc_structure.py` (from Phase 5I) to flag
  missing required H2s, then judge the rest.
- **Accuracy** — snippets are clean, but does the *narrative* match the API?
  (Methods that no longer exist, options whose semantics changed.)
- **Completeness** — are concepts a good docs site would cover present?
- **Clarity** — framing, ordering, jargon.

Architectural pages (`platform/*`, `capabilities/*`, `design-system/*`,
`reference/*/index.md`) — same treatment, stronger weight on accuracy.

**Session workflow:**
1. Read the page end-to-end. Note gaps.
2. Rewrite in one pass.
3. `python tools/check_doc_snippets.py --run --file <page>` — confirm 0 failures.
4. Commit: `Docs: editorial review — <page title>`.

**Widget page priority** — do actions, inputs, dialogs, and data-display first
(highest user traffic); then layout, navigation, overlays, selection, views,
primitives.

**Bugs surfaced during guide review** (logged in plan, not yet fixed):
- `AppSettings.light_theme`/`dark_theme` defaults are `docs-light`/`docs-dark`
  (counterintuitive; should probably be `bootstrap-light`/`bootstrap-dark`)
- `follow_system_appearance` is silently no-op on Windows/Linux
- `ListView` calls `deselect_all()`/`is_selected()` on its datasource but
  `BaseDataSource` exposes `unselect_all()`/no `is_selected` — mismatch
- `Signal.map()` uses weakref; inline `textvariable=sig.map(fn)` can stop
  updating after the derived signal is GC'd
- `MessageDialog._parse_buttons` stores the `:role` suffix into deprecated
  `bootstyle` field instead of `accent`
- `ValidationMixin.on_valid`/`on_invalid`/`on_validated` callbacks receive
  the payload `dict` directly, while `TextEntryPart.on_input`/`on_changed`/
  `on_enter` callbacks receive a virtual event with `.data`. The two
  registration paths — direct `bind(...)` vs. `_on_*_command` slots
  dispatched through `_dispatch_*` — produce inconsistent callback shapes.
  Either wrap the validation handlers to fire `callback(event)` so all
  `on_*` helpers are uniform, or document the split prominently. (Surfaced
  by textentry.md rewrite, 2026-04-30.)
- `DateEntry` class docstring (`composites/dateentry.py:30`) lists
  `monthAndDate` as a preset; the actual `IntlFormatter` preset is
  `monthAndDay`. Source-only typo. (Surfaced by dateentry.md rewrite,
  2026-04-30.)
- `TimeEntry.__init__` docstring (`composites/timeentry.py:67`) lists
  `"mediumTime"` as a value-format preset, but it isn't defined in
  `IntlFormatter.DatePreset`. Source-only typo — `shortTime`/`longTime`
  are the real medium/long pair. (Surfaced by timeentry.md rewrite,
  2026-04-30.)
- `LabeledScale` configure delegators have inverted query/set branches:
  `_delegate_value`, `_delegate_minvalue`, `_delegate_maxvalue` (and
  `_delegate_dtype`) at `composites/labeledscale.py:148-177` all check
  `if value is not None: return …` (set path returns the current value
  instead of writing) `else: self.configure(from_=value)` (query path
  attempts to write `None`). Net effect: `widget.configure(value=…)`,
  `widget.configure(minvalue=…)`, `widget.configure(maxvalue=…)`, and
  `widget.cget("minvalue"/"maxvalue"/"value")` are all broken. Workarounds:
  set the property (`widget.value = …`) and reconfigure the inner scale
  (`widget.scale.configure(from_=…, to=…)`). Source bug. (Surfaced by
  labeledscale.md rewrite, 2026-04-30.)
- `MessageDialog` class docstring (`dialogs/message.py:27-28`) claims
  `show_info` / `show_warning` / `show_error` / `show_question` are
  static methods on `MessageDialog` itself, but those methods live on
  `MessageBox`. Source-only docstring error. (Surfaced by
  messagedialog.md rewrite, 2026-04-30.)
- `MessageDialog` default `buttons=None` resolves to the translation
  keys `["button.cancel", "button.ok"]` (`dialogs/message.py:75-82`),
  but `localize` is also off by default. A vanilla `MessageDialog()`
  therefore displays the literal strings `button.cancel` /
  `button.ok` to the end user. Either default `localize=True` or
  resolve through `MessageCatalog.translate` unconditionally for the
  built-in semantic keys. (Surfaced by messagedialog.md rewrite,
  2026-04-30.)
- `FormDialog` class docstring (`dialogs/formdialog.py:55`) says
  `resizable` defaults to `(True, True)`, but the signature default
  (`formdialog.py:77`) is `False` — which gets normalized to
  `(False, False)`. So a vanilla `FormDialog()` is non-resizable,
  contrary to the class docstring. Source-only docstring/signature
  mismatch — fix the docstring to match the signature, or change
  the default. (Surfaced by formdialog.md rewrite, 2026-04-30.)
- `FormDialog` shares the same default-button localization gotcha as
  `MessageDialog`: `dialogs/formdialog.py:507-509` defaults to
  `["button.cancel", "button.ok"]` translation keys, and there is
  no `localize` flag on `FormDialog` at all. The vanilla
  `FormDialog()` therefore shows literal `button.cancel` /
  `button.ok` strings to the user. Plumb a `localize` argument
  through (or resolve the built-in semantic keys
  unconditionally). (Surfaced by formdialog.md rewrite,
  2026-04-30.)
- `FormDialog.show()` always overwrites `self.result` with
  `form.data` whenever the underlying `_dialog.result` is not None
  (`dialogs/formdialog.py:204-208`). This means a custom button's
  `result=` value is silently ignored — callers who want to route
  on which submit button was pressed (e.g. "Save" vs "Save and
  close") have no way to read it back from `.result`. Either honor
  button `result=` overrides, or document that custom button-result
  routing isn't supported on FormDialog. (Surfaced by formdialog.md
  rewrite, 2026-04-30.)
- `DateDialog.on_result` callback receives the **full payload
  dict**, not the unwrapped date. The docstring at
  `dialogs/datedialog.py:368` claims "The callback receives
  `event.data["result"]` (a `datetime.date`)", but the handler
  (`dialogs/datedialog.py:382-383`) actually invokes
  `callback(getattr(event, "data", None))` — passing
  `{"result": date, "confirmed": True}`. Either unwrap the payload
  in the handler or fix the docstring. The same `on_result`
  binding target is `self._dialog.toplevel or self._master`, so
  registering before `show()` with no `master=` silently no-ops
  (returns None) — match QueryDialog's gotcha. (Surfaced by
  datedialog.md rewrite, 2026-04-30.)
- `FilterDialog.show()` does **not** reset `self.result` to `None` at
  the start of each call (`dialogs/filterdialog.py:290-358`). Only
  the underlying `Dialog`'s own `result` is reset. If a single
  FilterDialog instance is used across multiple openings, a sequence
  of [OK with selection X] → [reopen, then Cancel] returns the stale
  list X instead of `None`. Either reset `self.result = None` at the
  top of `show()`, or document that callers must reconstruct the
  dialog per opening. (Surfaced by filterdialog.md rewrite,
  2026-04-30.)
- `FilterDialog` shares the localized-default-button gotcha with
  `MessageDialog` and `FormDialog`: the OK/Cancel buttons default to
  the translation keys `"button.ok"` / `"button.cancel"`
  (`dialogs/filterdialog.py:333-340`), and there is no `localize`
  flag at all. The Select All checkbox label is also a translation
  key (`"edit.select_all"`, `dialogs/filterdialog.py:108`). A vanilla
  `FilterDialog(items=[...], enable_select_all=True)` therefore
  shows literal `button.ok` / `button.cancel` / `edit.select_all`
  strings to the user. Plumb a `localize` flag through, or resolve
  the built-in semantic keys unconditionally. (Surfaced by
  filterdialog.md rewrite, 2026-04-30.)
- `FilterDialogContent._handle_select_all`
  (`dialogs/filterdialog.py:142-149`) iterates **all** registered
  checkboxes, ignoring the current search filter. If the user types
  a search term and clicks Select All, every item — including the
  ones not currently visible due to the filter — is selected/
  deselected. Either restrict Select All to visible items only, or
  hide the Select All toggle when a search filter is active. Also,
  the Select All checkbox does not auto-update its own state when
  individual items are toggled, so its visible state can desync
  from "all items selected" reality. (Surfaced by filterdialog.md
  rewrite, 2026-04-30.)
- `FilterDialogContent._check_buttons`
  (`dialogs/filterdialog.py:140`) is keyed by item `text`, not by
  index or `value`. Items with duplicate `text` fields silently
  overwrite each other in the registry — the second checkbox
  renders, but Select All and the search filter only act on the
  second binding for that key. Key the registry by index (or by
  `value`) instead. (Surfaced by filterdialog.md rewrite,
  2026-04-30.)
- `FilterDialog` is a **`Frame` subclass that composes a `Dialog`**
  rather than extending Dialog directly
  (`dialogs/filterdialog.py:173`). This is inconsistent with every
  other dialog class in the framework and forces unique behavior:
  events fire on the FilterDialog frame instance instead of the
  toplevel; the frame is initialized as a child of `master` but
  never packed; and the event surface uses
  `<<SelectionChange>>` with payload `{"selected": list}` instead
  of the framework-standard `<<DialogResult>>` with payload
  `{"result": ..., "confirmed": bool}`. Consider refactoring to
  extend Dialog directly and aligning event names/payloads with
  the rest of the dialogs surface. (Surfaced by filterdialog.md
  rewrite, 2026-04-30.)
- `cli/demo.py:734-740` (Meter section) still constructs Meter with
  the **deprecated** legacy parameter names (`amountused`,
  `amounttotal`, `subtext`, `metersize`). Each call emits a
  `DeprecationWarning` from `_coerce_legacy_params`
  (`composites/meter.py:218-223`) on every demo run. Update the
  demo to use the modern names (`value`, `maxvalue`, `subtitle`,
  `size`). Source-only cleanup. (Surfaced by meter.md rewrite,
  2026-04-30.)
- `Meter` does not expose its internal value variable
  (`composites/meter.py:151`, `_value_var`) and accepts no
  `variable=` parameter. Reactivity is exclusively through
  `value`-setter paths and the `<<Change>>` event. This is
  inconsistent with FloodGauge (which accepts `variable=` /
  `textvariable=`) and Progressbar (which accepts `signal=` /
  `variable=`). Consider plumbing a `variable=` (and matching
  `textvariable=` for the readout) through the constructor for
  parity. (Surfaced by meter.md rewrite, 2026-04-30.)
- `ListView` virtual-event docstrings reference event names
  with mismatched suffixes that don't match the actual
  `event_generate(...)` calls. Specifically:
  `ListView.select_all` (`composites/list/listview.py:1331`)
  documents `<<SelectionChanged>>` but generates
  `<<SelectionChange>>`; `insert_item` (`listview.py:1377`)
  documents `<<ItemInserted>>` but generates `<<ItemInsert>>`;
  `update_item` (`listview.py:1398`) documents `<<ItemUpdated>>`
  but generates `<<ItemUpdate>>`; `delete_item` (`listview.py:1414`)
  documents `<<ItemDeleted>>` but generates `<<ItemDelete>>`.
  Source-only docstring typos. (Surfaced by listview.md
  rewrite, 2026-04-30.)
- `ListView` `on_*` event-helper docstrings (`listview.py:1445-1507`)
  claim each event carries `event.data = {'record': dict}` (or
  variants), but the corresponding `event_generate(...)` calls
  for `<<ItemDelete>>` / `<<ItemDeleteFail>>` / `<<ItemInsert>>` /
  `<<ItemUpdate>>` (`_on_item_removing` at `listview.py:927-929`,
  `insert_item` at `:1387`, `update_item` at `:1405`,
  `delete_item` at `:1421`) pass **no `data=`** parameter — so
  `event.data` arrives as `None` at the listener. Either pass
  the record dict through `event_generate(..., data=record)` to
  match the docstring, or fix the docstrings to say `event.data
  = None` (and tell users to read state via `get_selected()` /
  `get_datasource()`). (Surfaced by listview.md rewrite,
  2026-04-30.)
- `ListView`'s `DataSourceProtocol`
  (`composites/list/listview.py:18-129`) requires
  `is_selected(record_id) -> bool`,
  `deselect_record(record_id)`, and `deselect_all()`. The
  framework's own `BaseDataSource` (`datasource/base.py`)
  exposes `unselect_record`, `unselect_all`, and **no
  `is_selected`** abstract method. As a result, the public
  `ttkbootstrap.datasource.MemoryDataSource` /
  `SqliteDataSource` / `FileDataSource` classes do **not**
  satisfy `DataSourceProtocol` — passing one to
  `ListView(datasource=...)` will fail at the first selection
  event with `AttributeError: ... has no attribute
  'deselect_record'` (or `is_selected`). The internal
  `MemoryDataSource` *inside* `listview.py` does match.
  Resolution options: (a) rename the protocol methods to match
  `BaseDataSource` (`unselect_*`, add `is_selected` to
  `BaseDataSource`); or (b) keep ListView's names and add
  thin shims on `BaseDataSource`. This is the same protocol
  mismatch already on the bugs list — file paths and call
  sites confirmed during listview.md rewrite, 2026-04-30.
- `ListView` ships **two unrelated `MemoryDataSource` classes**:
  one private to `composites/list/listview.py:132` (used when
  `items=` is passed; satisfies the `DataSourceProtocol`),
  and one public at `datasource/memory_source.py:54` (extends
  `BaseDataSource`; does *not* satisfy the protocol — see
  previous bug). The two share a name but a different API
  surface. Consider removing the private duplicate and
  reconciling the public class against the protocol, or
  renaming the private one (e.g. `_InlineMemoryDataSource`)
  so the duplication isn't accidentally relied on. (Surfaced
  by listview.md rewrite, 2026-04-30.)
- `TableView` export events fire on the **inner private
  `_tree`**, not on the TableView itself. `_export_all`,
  `_export_selection`, and `_export_page` (`composites/tableview/
  tableview.py:1813-1833`) each call
  `self._tree.event_generate("<<TableViewExport*>>", data=rows)`.
  All other public events (`<<RowClick>>`, `<<SelectionChange>>`,
  etc.) are generated on `self`, and TableView ships
  `on_*` / `off_*` helpers for every one of those — but there
  are **no `on_export_*` helpers** at all. Net result: the
  documented `enable_exporting=True` path produces events that
  callers can only consume by binding to `tv._tree` (a private
  attribute). Either generate the export events on `self` and
  add public helpers, or drop the events and expose
  synchronous `export_all()` / `export_selection()` /
  `export_page()` methods that return the rows. (Surfaced by
  tableview.md rewrite, 2026-04-30.)
- `TableView.set_filters(where: str)` and the advanced search
  "SQL" mode interpolate user input directly into the SQL
  WHERE clause (`composites/tableview/tableview.py:1153-1188`,
  `:562-571`); `TableView.set_sorting(key, ascending)` quotes
  the column identifier but takes the raw `key` string from
  the caller (`:580-592`). All three are documented internally
  as a "trust contract" but the public docstrings don't warn
  about SQL injection risk. Either parameterize the SqliteData
  Source's `set_filter` / `set_sort` to bind values, or add a
  prominent warning to the public docstrings + a top-level
  note in the API reference. (Surfaced by tableview.md
  rewrite, 2026-04-30.)
- `TableView` ships an undocumented lowercase legacy alias
  `Tableview = TableView` at the end of
  `composites/tableview/tableview.py:2272`. The alias isn't
  re-exported through `ttkbootstrap.api` and isn't mentioned
  in any docstring — it exists only as a backwards-compat
  hook. Either deprecate it explicitly (with a
  `DeprecationWarning` on access) or document the lowercase
  spelling alongside `TableView`. (Surfaced by tableview.md
  rewrite, 2026-04-30.)
- `TableView`'s `enable_filtering` parameter is **dead** —
  documented as a master switch ("Enable filtering features",
  `composites/tableview/tableview.py:133`), but the value
  stored as `self._filtering['enabled']` is never read
  anywhere in the codebase. Only `enable_header_filtering`
  (read at `_filtering['header_menu_filtering']`) and
  `enable_row_filtering` (read at
  `_filtering['row_menu_filtering']`, line 1270) gate any
  behavior. A caller passing `enable_filtering=False` still
  gets every filter affordance. Either wire it as a true
  master switch (gate both menu options + the search bar's
  WHERE-clause emission) or remove it from the public ctor
  signature. (Surfaced by tableview.md rewrite, 2026-04-30.)
- `LabelFrame.__init__` (`widgets/primitives/labelframe.py:45-68`)
  does not call `_capture_style_options(['show_border'], kwargs)`
  the way `Frame.__init__` does, so `show_border` is not lifted
  from kwargs into `style_options`. Net effect: the LabelFrame
  style builder reads `show_border` and defaults to `True`
  (`style/builders/labelframe.py:18`), but there is no public knob
  to turn it off — passing `show_border=False` raises `TclError:
  unknown option "-show_border"` because Tk rejects the unknown
  ttk option. Either capture `show_border` (and `input_background`
  while at it) into `style_options` in `LabelFrame.__init__`, or
  document the border as non-configurable. (Surfaced by
  labelframe.md rewrite, 2026-04-30.)
- `LabelFrame` does **not subclass `Frame`** — it inherits
  directly from `ttk.LabelFrame`, missing Frame's overridden
  `configure_style_options`, `_refresh_descendant_surfaces`, and
  `_refresh_descendant_input_backgrounds`. Net effect: runtime
  surface reconfiguration on a LabelFrame restyles only the
  LabelFrame itself; child widgets stay on their old surface. The
  divergence is unintentional given that `TLabelframe` is already
  in `CONTAINER_CLASSES` and is treated as a container everywhere
  else. Either make `LabelFrame` subclass `Frame` (mixing the
  cascade behavior) or duplicate the cascade hooks. (Surfaced by
  labelframe.md rewrite, 2026-04-30.)
- `frame.md` (already shipped on this branch, commit `997a5b7`)
  contains two narrative inaccuracies surfaced while reviewing
  LabelFrame against the same constructor path:
  (1) the page claims `accent` and `variant` are "silently ignored
  by the Frame style builder" — but `Bootstyle.override_ttk_widget_constructor`
  treats container classes (including `TFrame`) specially and
  turns `accent` into a surface override before the builder runs.
  Verified: `Frame(app, accent="primary")` produces
  `_surface='primary'`, `style_options={'surface': 'primary'}`,
  and rendered style `bs[…].primary.TFrame`. The `variant` claim
  is also imprecise — passing a non-default variant raises
  `BootstyleBuilderError` rather than being silently ignored.
  (2) the surface-cascade example shows
  `section.configure(surface="card")`, but ttk.Frame doesn't
  accept `-surface` and that call raises `TclError`. The actual
  runtime cascade path is `section.configure_style_options(surface="card")`,
  which Frame overrides with the descendant-refresh hook.
  Both points warrant a frame.md fixup pass. (Surfaced by
  labelframe.md rewrite, 2026-04-30.)

**Renderer conventions** (when authoring new factories — read the
existing `docs_scripts/shots/*.py` for live examples):

- Factory signature: `def factory(parent: Widget) -> Optional[Callable]`.
  `parent` is a renderer-supplied padded `Frame`; build widgets into it.
- Return a `finalize` callable when the shot needs visual state flags
  (`state(["focus"])`, `state(["hover"])`) applied at capture time —
  Tk may otherwise clear them between deiconify and grab.
- Use `widget.focus_set()` for true focus rings; the state flag alone
  isn't always honored by ttk styles.
- **Don't** use `pack_propagate(False)` on a Frame with `width=` but no
  `height=` — height defaults to 0 and the shot renders blank. Either
  set both, or drop the propagate call.
- The renderer deliberately does NOT use `override_redirect=True` or
  `focus_force()` — both kill WM focus event propagation and flatten
  focus/hover visuals.

**Authoring loop for a new widget shot:**

1. Read `docs/widgets/<category>/<name>.md` to find the `IMAGE:`
   placeholder spec or pick a sensible default composition.
2. Add or extend a factory in `docs_scripts/shots/<category>.py`.
3. Add a `[[shots]]` entry to `docs_scripts/screenshots.toml`.
4. Render: `python -m docs_scripts.render --slug widgets-<name>`.
5. View output at `docs/assets/{light,dark}/widgets-<name>.png`.
6. Replace the `IMAGE:` block (or insert a new `<figure markdown>`
   block) in the .md file with the canonical light + dark refs.
7. Run `python tools/check_doc_images.py` to confirm 0 missing.
8. Commit factory + manifest + .md + PNGs together; commit message
   format: `Docs: screenshots for X, Y, Z (6E batch N)`.

The plan doc (`analysis/docs-review-and-plan.md`) has the full
architecture decisions log.

---

## Documentation toolchain

- **Zensical** (separate from plain MkDocs), not Sphinx. Configuration:
  `zensical.toml`. Install via `pip install -e ".[docs]"`. Serve with
  `.venv/bin/zensical serve -o`.
- **Plain Markdown only** in docstrings — no reST roles like `:func:`,
  `:param:`, or `.. note::`. The MkDocs `admonition` extension is
  enabled, so `!!! note "Heading"` blocks are allowed in docstrings.
- **mkdocstrings** renders the API reference from source docstrings
  using the Google convention. Reference pages are bare
  `::: module.Class` directives. Class docstrings carry narrative and
  `Attributes:`; `__init__` docstrings carry `Args:`. Both render —
  don't relocate, fill gaps.

---

## Linting and validation

Public-API docstring discipline is enforced by ruff `D` rules with the
Google convention, configured in `pyproject.toml` under `[tool.ruff]`.
Run from the repo root:

```bash
.venv/bin/ruff check src/ttkbootstrap
```

Internal directories (`widgets/mixins`, `widgets/internal`,
`widgets/parts`, `style/builders`, `style/builders_tk`,
`core/capabilities`, `core/mixins`, `cli`, `assets`) are blanket-ignored
in `[tool.ruff.lint.per-file-ignores]`.

Public-surface files whose docstrings haven't yet been brought to spec
are listed individually in the same block. Each entry is removed once
that file passes:

```bash
.venv/bin/ruff check --select D --isolated src/ttkbootstrap/path/to/file.py
```

Use `--isolated` to bypass `pyproject.toml` and see the real violations
the ignore is currently suppressing.

---

## Conventions

- One canonical import in examples: `import ttkbootstrap as ttk`.
- The `bootstyle` parameter is **deprecated**. In descriptive prose,
  describe styling via the canonical tokens (`accent`, `variant`,
  `density`, `surface`, `show_border`). The `bootstyle` parameter is
  still marked DEPRECATED in argument docs for users who haven't
  migrated.
- Class docstrings describe what something **is** and **does**
  mechanically. Don't write "when to use this," "best for…," or
  comparisons to sibling classes — those belong in user-guide pages
  under `docs/widgets/` or `docs/guides/`.
- Examples in docstrings are off by default. Add an `Examples:` section
  only when the call shape is non-obvious from the signature alone
  (decorators, context managers, abstract subclassing patterns,
  ambiguous polymorphic args). "Construct it and pack it" doesn't
  qualify.

---

## Branches and commits

- Active feature work for v2 lives on `release/v2`.
- The docs review effort lives on `docs/review-and-cleanup`.
- Commit messages on this branch use the format
  `Docs review phase N: <summary>` for phase-scoped commits and
  `Docs: <summary>` for individual file cleanups.
