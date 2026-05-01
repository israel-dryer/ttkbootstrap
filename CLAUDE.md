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

### Current handoff (2026-05-01, navigation sweep — 2/5; AppShell rewritten, navigation directory split into per-page templates)

Phases 1–7, 9A–9D are complete. **Phase 6 (screenshot pipeline) is partially
complete; 6F not started. Pass 2 (editorial review) is the active work —
the dialogs sweep (11/11), data-display sweep (8/8), and layout sweep
(12/12) are complete. The **navigation sweep is now in progress** — the
navigation template has been restructured to the slim arc, `tabs.md`
has been rewritten as the anchor, and `appshell.md` has been rewritten
at its canonical location (`docs/widgets/application/appshell.md`)
under a bespoke app-shell arc (it's an `App` subclass, not a child
widget — the navigation template never fit). The vestigial
`docs/widgets/navigation/appshell.md` redirect stub was deleted.

The navigation directory turned out to be heterogeneous; the remaining
three pages each get a different template:

- **`sidenav.md`** — true selection-driven nav chrome → uses the
  navigation template (`docs/_template/widget-navigation-template.md`)
  as designed.
- **`toolbar.md`** — action chrome strip with no selection state, no
  keyed targets, no signal → uses the **action template** (the same
  one Button / ButtonGroup / ContextMenu use). Forcing a "Navigation
  model" H2 onto Toolbar would be contrived. When picking it up, plan
  for an `Item types` subsection covering `add_button` /
  `add_label` / `add_separator` / `add_spacer` / `add_window_controls`.
- **`navigationview.md`** — 6-line deprecation stub for SideNav. Add
  `"navigationview.md"` to `SKIP_FILES` in
  `tools/check_doc_structure.py` rather than rewriting it.

The remaining 3 templates (form, overlay, selection) still need the
editorial pass at the start of each sweep (see "Template arc" below).**

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
- `widget-navigation-template.md` (anchored on `tabs.md`).
  `Navigation model` is required (it carries the keyed-targets /
  random-vs-sequential / signal-vs-imperative description that
  every navigation page needs).

Remaining 3 templates (form, overlay, selection) still lead with
`Framework integration` etc. Apply the editorial pass at the start
of each category's sweep — those categories have 0 pages written,
so the template fix is free.

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

### Widget pages — layout (`docs/widgets/layout/`, 12 pages) — DONE 12/12 (2026-05-01)

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

Last session (2026-05-01, sizegrip sweep — final layout page):

- `sizegrip.md` rewritten to the slim layout template. SizeGrip is
  the twelfth and final page in the sweep — a thin themed wrapper
  over `ttk.Sizegrip` (the dotted-triangle drag handle in the
  bottom-right of a Toplevel). Layout model section skipped (SizeGrip
  is a structural primitive, like Frame / Card / LabelFrame /
  Separator). Four things the old page got wrong or omitted, three
  of which became new bugs:
  (1) the old `Appearance` section said "For theming details and
  color tokens, see Design System." That implied SizeGrip honors the
  standard theming axes. Verified at runtime: the SizeGrip style
  builder (`style/builders/sizegrip.py:11-16`) reads only `surface`
  and writes `background`. `accent` is captured into `_accent` and
  flows into a unique resolved style name (e.g.
  `bs[…].primary.TSizegrip`) but produces an *identical* configured
  background to the default — the dot pattern is drawn by the
  platform's `Sizegrip.sizegrip` element which the builder does not
  tint. Documented as a silent no-op in Common options.
  (2) the old `Quick start` showed `ttk.SizeGrip(status).pack(side=
  "right")` without `app.resizable(True, True)`. With the toplevel
  fixed-size (the Tk default for some platforms), the drag has no
  visible effect — Tk still tracks the cursor but the toplevel
  ignores the geometry write. Documented `resizable(True, True)` as
  a precondition in Basic usage.
  (3) the old `Behavior` section claimed "the sizegrip is not
  focusable and is not intended for keyboard interaction" but never
  named the **mouse-only** interaction surface. Verified at runtime
  that `TSizegrip` binds `<Button-1>`, `<B1-Motion>`, and
  `<ButtonRelease-1>` at the bind-class level — those drive Tk's
  internal toplevel resize logic. Documented as the only interaction
  path; warned readers not to override the mouse bindings.
  (4) the old page never noted that `configure(surface=...)` raises
  `TclError`. Verified: SizeGrip is **not** in `CONTAINER_CLASSES`
  (only `TFrame` / `TLabelframe` are), so the bootstyle-wrapper's
  surface-as-accent-override path doesn't apply, and SizeGrip's
  `__init__` doesn't lift `surface` into a `_delegate_*` map.
  `sizegrip.configure(surface='primary')` →
  `TclError: unknown option "-surface"`. The
  `configure_style_options(surface=...)` escape hatch also misbehaves:
  it sets the resolved style to `Default.TSizegrip` (no hash prefix),
  silently reverting to the platform default. Documented `surface` as
  construction-time only and added to the bugs list.
  Common options consolidates into a 6-row table; deliberate negative
  `Events` section (no `on_*` helpers, no virtual events; pointed
  readers at toplevel `<Configure>` for resize tracking).

`tools/check_doc_structure.py --category layout` → 12/12 passing.
`tools/check_doc_snippets.py --run --file
docs/widgets/layout/sizegrip.md` → 0 failures (4 snippets, 1
executed). Layout sweep complete.

Earlier session (2026-05-01, separator sweep):

- `separator.md` rewritten to the slim layout template. Separator is
  the eleventh page in the sweep — a thin themed wrapper over
  `ttk.Separator` with no SignalMixin and no `on_*` helpers. Layout
  model section skipped (Separator is a transparent primitive, like
  Frame / Card / LabelFrame / Sizegrip). Four things the old page
  got wrong or omitted:
  (1) the old `Appearance` section said "If your theme exposes
  separator variants, apply them via `accent` or `style`." That
  conflates two distinct axes. `accent` is the **line color**
  (default `"border"`, which resolves through the builder to
  `b.border(surface)` — the same muted border color used by
  `Frame(show_border=True)`); `variant` is the visual variant axis
  but only `"default"` is registered, so any other variant raises
  `BootstyleBuilderError`. Documented both correctly.
  (2) the old page never named the **`thickness`** and **`length`**
  options at all, despite both being in the `SeparatorKwargs`
  TypedDict and captured into `style_options` at construction
  (`widgets/primitives/separator.py:58`). The style builder
  (`style/builders/separator.py:19-42`) reads `thickness` (default
  `1`) for the cross-axis size and `length` (default `None` →
  stretchy via sticky `ew`/`ns`) for the along-axis size; setting
  `length=N` builds the image element at fixed dimensions and
  ignores geometry-manager fill on that axis. Documented both,
  including the 40-pixel internal default that catches users who
  forget `fill=` on a manually-sized line.
  (3) the old page never noted that **reconfiguring `orient`
  after construction does not rebuild the resolved ttk style**.
  Separator is in `ORIENT_CLASSES`, so the orientation is part of
  the style key (e.g. `bs[…].primary.Vertical.TSeparator`), and
  `configure(orient=...)` only writes the Tk option without
  invalidating the cached style. Verified at runtime:
  `Separator(orient='vertical', accent='primary')
  .configure(orient='horizontal')` keeps style
  `bs[…].primary.Vertical.TSeparator` and renders with the wrong
  axis. Same bug pattern as Scrollbar (already on the bugs list).
  Documented as construction-time-only and added to the bugs list.
  (4) the old page never described the `surface` option or the
  parent-surface inheritance. Verified: a `Separator` inside a
  `Frame(surface='card')` inherits `_surface='card'`. Documented.
  Common options consolidates into a 9-row table; deliberate
  negative `Events` section (no `on_*` helpers, no virtual events).

`tools/check_doc_structure.py --category layout` → separator.md no
longer in the missing-sections list (1/12 page still pending:
sizegrip).
`tools/check_doc_snippets.py --run --file
docs/widgets/layout/separator.md` → 0 failures (6 snippets, 1
executed).

Prior session (2026-05-01, expander sweep):

- `expander.md` rewritten to the slim layout template. Expander is
  the tenth page in the sweep — a `Frame` subclass with a clickable
  header region (icon + title + chevron) on top of a permanent
  content frame that toggles via `pack()` / `pack_forget()`. Filled
  in the optional `Layout model` (header / content frame / content
  widget three-region stack) and documented the previously-undoc
  selection model. Four things the old page got wrong or omitted,
  one of which became a new bug:
  (1) the old "Programmatic control" example showed `if exp.expanded:`
  and `exp.expanded = False`. Verified at runtime that Expander has
  no `expanded` Python property (`AttributeError`); access is via
  `cget("expanded")` / `configure(expanded=...)` / `expand()` /
  `collapse()` / `toggle()`. Documented `is_selected` and `content`
  as the only true properties.
  (2) the old "Responding to toggle events" snippet used
  `exp.on_toggle(...)`. The actual helper is `on_toggled` (and
  `off_toggled`, `on_selected`, `off_selected`). Fixed and added
  the bind-id pattern. (Same `<<Toggle>>` payload `{"expanded":
  bool}` confirmed at runtime.)
  (3) the old page never described the **header vs container**
  styling split. `accent` and `variant` are intercepted in
  `Expander.__init__` (`composites/expander.py:74-75`) before the
  Frame bootstyle wrapper, so they style the inner CompositeFrame
  header — not the outer Frame. Verified:
  `Expander(accent="primary")` produces `_surface="content"`,
  `style_options={}`, rendered style `Default.TFrame` (the outer
  container is unstyled). To tint the container itself, use
  `surface=` independently from `accent`.
  (4) the old page omitted the **selection model** (signal /
  variable / value). Expander accepts `signal=` (preferred) or
  `variable=` plus `value=`, fires `<<Selected>>` with `{"value":
  ...}` on header click, and exposes the `is_selected` property
  for radio-group reads. Documented the full surface and noted
  that `_update_selection_state` (`expander.py:140-144`) is a
  deliberate placeholder — selection state is tracked but does
  **not** auto-apply the `selected` ttk state to the header
  today; pair `signal=` with `highlight=True` and call
  `expand()` from the listener, or drive
  `expander._header_frame.set_selected(True)` manually.
  Also documented: `add()` semantics (idempotent on the no-arg
  path, raises `ValueError` if a widget is passed after content
  exists), the `compact` mode (hides title, centers icon — undoc
  in old page), the `show_border=True` auto-injection of
  `padding=3` (verified: `cget('padding') == (3,)`), the keyboard
  contract (`<Tab>` walks header focus, `<Return>` / `<space>`
  toggle), and the construction-only nature of `icon_position`.
  Logged one new bug: `collapsible=False` only hides the chevron
  and gates `toggle()`. The programmatic paths `expand()` /
  `collapse()` / `configure(expanded=...)` ignore `_collapsible`
  entirely (`composites/expander.py:261-283`). Verified:
  `Expander(collapsible=False).collapse()` collapses the content
  with no warning. Either treat `collapsible=False` as a hard
  invariant or rename it to reflect that it controls only
  user-facing affordances.

`tools/check_doc_structure.py --category layout` → expander.md no
longer in the missing-sections list (2/12 pages still pending:
separator, sizegrip).
`tools/check_doc_snippets.py --run --file
docs/widgets/layout/expander.md` → 0 failures (10 snippets, 1
executed).

Prior session (2026-05-01, accordion sweep):

- `accordion.md` rewritten to the slim layout template. Accordion is
  the ninth page in the sweep — a `Frame` subclass that owns a stack
  of `Expander` widgets and enforces a mutual-exclusion policy via
  `<<Toggle>>` listeners. Filled in the optional `Layout model`
  section (key-addressed sections, optional inter-section separators,
  always-vertical stack — no horizontal mode). Five things the old
  page got wrong or omitted, three of which became new bugs:
  (1) the old `Appearance` section showed
  `ttk.Accordion(app, accent="success", variant="solid")` and treated
  `accent` as a styling shortcut for the accordion itself. Verified
  at runtime that Accordion captures `accent` and `variant` in its
  own `__init__` (they never reach `super().__init__()`), so they
  do **not** flow through the bootstyle wrapper's container reroute
  the way Frame's do — `_surface` stays at `'content'` and the
  rendered style is `Default.TFrame`. The accent is purely a
  forwarded default for child Expanders created via `add()`.
  Documented as `Accent forwarding` under Common options and noted
  that tinting the accordion's container needs `surface=…`, not
  `accent=…`.
  (2) the old `Examples & patterns / Adding sections` example
  showed `accordion.add(title="…", icon={...})` and never noted
  that **passing `accent=` (or `variant=`) to `add()` when the
  accordion has its own `accent` raises `TypeError: got multiple
  values for keyword argument 'accent'`**. Cause: the precedence
  resolution at `composites/accordion.py:128-129` is
  `accent = self._accent or kwargs.pop('accent', None)`. When
  `self._accent` is truthy, the `or` short-circuits before `pop`,
  so the per-call accent stays in `**kwargs` and collides with the
  explicit `accent=accent` passed to the Expander constructor.
  Verified at runtime
  (`Accordion(accent='primary').add(accent='success')` →
  `TypeError`). Documented as a `!!! warning` block; added to the
  bugs list.
  (3) the old `Behavior` section claimed the accordion's
  `<<AccordionChange>>` event fires whenever the expanded set
  changes. Verified at runtime that `remove(key)` does **not** fire
  the event when the removed expander was the last one — the
  `if self._expanders:` guard at
  `composites/accordion.py:210-214` suppresses the emission. Now
  documented in `Events`; added to the bugs list.
  (4) the old page never noted that `configure(show_separators=…)`
  does **not** retroactively add or remove separators between
  existing expanders. Verified: starting from `show_separators=False`
  with three expanders, calling `configure(show_separators=True)`
  leaves separator count at 0; only the next `add()` call inserts a
  separator. Documented as a runtime caveat in Layout model and
  Behavior; added to the bugs list.
  (5) the old page never noted that `expand_all()` is a no-op when
  `allow_multiple=False` and `collapse_all()` is a no-op when
  `allow_collapse_all=False` — both return silently with no
  exception. Verified: `Accordion(allow_multiple=False).expand_all()`
  leaves `accordion.expanded == []`. Documented in Behavior under
  "mode-gated".
  Also documented: the auto-keying scheme (`expander_<n>`, never
  reused), the auto-`padding=3` injection when `show_border=True`
  (verified: `cget('padding') == (3,)`), the `add(expander=existing)`
  path that *does* set `highlight=True` on the existing expander
  but does **not** apply the accordion's accent/variant, the
  keyboard-navigation contract (Tab walks headers via
  `takefocus=True` on the inner header frame; `<Return>`/`<space>`
  toggle), and the `allow_collapse_all=False` enforcement path
  (auto-expand first section at `add()` time; revert
  collapse-of-last via `expander.expand()`).

`tools/check_doc_structure.py --category layout` → accordion.md no
longer in the missing-sections list (3/12 pages still pending:
expander, separator, sizegrip).
`tools/check_doc_snippets.py --run --file
docs/widgets/layout/accordion.md` → 0 failures (6 snippets, 1
executed).

Prior session (2026-05-01, scrollview sweep):

- `scrollview.md` was already structurally aligned with the slim
  layout template; this pass was an accuracy cleanup against
  `widgets/composites/scrollview.py`. Three fixes:
  (1) the `Scrollbar variant` subsection listed only `"default"`
  and `"square"` as valid values. The Scrollbar style builder
  registers four variant keys: `"default"`, `"round"`, and
  `"rounded"` are aliases for the image-based rounded thumb;
  `"square"` is the flat solid-color path
  (`style/builders/scrollbar.py:11,177-179`). Updated the option
  list to reflect all four.
  (2) the inherited-options section claimed "ScrollView is in
  `CONTAINER_CLASSES`". The actual contents of `CONTAINER_CLASSES`
  is `{'TFrame', 'TLabelframe'}` (`style/token_maps.py:41`); what
  matters here is that `ScrollView` inherits `Frame`, so its style
  class is `TFrame` — which is what the bootstyle constructor
  wrapper checks at `style/bootstyle.py:464`. Reworded.
  (3) the **`Reconfiguration is live`** paragraph claimed that
  `configure(scroll_direction=...)` "rewires the canvas scroll
  commands, regrids the bars, and updates visibility". Verified
  at runtime that the bars are **not** regridded:
  `_delegate_scroll_direction` (`scrollview.py:121-145`) only
  rewires `xscrollcommand` / `yscrollcommand` and calls
  `_update_scrollbar_visibility()`, which in turn calls
  `_show_scrollbars()` — `self.horizontal_scrollbar.grid()`
  (no args). Test: `ScrollView(scroll_direction='vertical')` then
  `.configure(scroll_direction='both')` with content overflowing
  both axes ends up with the horizontal bar at row=1 col=0 (by
  Tk auto-placement coincidence) but `sticky=''` instead of
  `'ew'`, so it renders as a stub at the left edge of its row
  rather than spanning the canvas width. Documented as a
  construction-time-only axiom and added to the bugs list.
  Other facts already on the page were verified and kept:
  per-instance bind-tag (`ScrollView_<id>`) for mousewheel; bars
  always constructed but only initially-direction-matching ones
  gridded; gutter reservation only in `hover` and `scroll` modes
  (`_set_scrollbar_gutter` reads `winfo_reqwidth/height`
  post-`after_idle`); content widgets parented on `sv.canvas` (not
  `sv`) — `add()` defaults to a `Frame(self.canvas)`; `<Configure>`
  on the content widget drives `scrollregion` updates and is
  bound by `add()` directly (replacing any pre-existing handler
  on the content); wheel events no-op when content fits on that
  axis (so nested ScrollViews chain correctly); `grid_remove`
  auto-hide even in `'always'` mode when content fits.

`tools/check_doc_structure.py --category layout` → scrollview.md
no longer in the missing-sections list (4/12 pages still pending).
`tools/check_doc_snippets.py --run --file
docs/widgets/layout/scrollview.md` → 0 failures (9 snippets, 1
executed).

Prior session (2026-04-30, scrollbar sweep):

- `scrollbar.md` rewritten to the slim layout template. Scrollbar
  is the seventh page in the sweep — a thin themed wrapper over
  `ttk.Scrollbar` (no SignalMixin, no `on_*` helpers) whose only
  ttkbootstrap-specific surface is `accent` (thumb tint), `surface`
  (trough fill), `variant` (`default`/`round`/`rounded` →
  image-based rounded thumb; `square` → flat solid-color thumb),
  and `style_options.show_arrows`. Layout model section skipped —
  Scrollbar is a control, not a layout container; geometry is
  decided by the parent. Three things the old page got wrong or
  omitted:
  (1) the old `Quick start` framed Scrollbar as a one-way driver
  ("scroll content"). The actual contract is **two-way and
  symmetric**: `command=text.yview` lets the scrollbar drive the
  target, and `text.configure(yscrollcommand=ys.set)` lets the
  target drive the scrollbar. Wiring only one half breaks one
  direction silently. Documented as the central concept after
  the basic-usage example.
  (2) the old `Appearance` example showed
  `ttk.Scrollbar(app, accent="secondary")` and stopped there. It
  never named the **`square` vs `default` variant axis**, never
  surfaced the `show_arrows` builder option, and never explained
  that `accent` defaults to **the surface's border color** (not
  to a theme primary) — so a default scrollbar reads as a muted
  bar by design. Documented all three in `Common options` and
  added a Variants subsection.
  (3) the old `Behavior` section listed three loose facts and
  stopped. Replaced with a structured walkthrough of the view
  protocol (`xview`/`yview` command forms, `set(first, last)`
  reporting), the inherited ttk methods (`set`/`get`/`delta`/
  `fraction`/`identify`/`activate`/`state`/`instate`), and the
  **disabled state** path (`sb.state(["disabled"])` mutes the
  bar but the target keeps calling `sb.set(...)`).
  Surfaced one new bug: **reconfiguring `orient` after construction
  does not rebuild the resolved ttk style**. Verified at runtime:
  `Scrollbar(orient='vertical', accent='primary').configure(
  orient='horizontal')` keeps style
  `bs[…].primary.Vertical.TScrollbar` — up/down arrows in a
  horizontal layout. Documented as a construction-time-only
  axiom and added to the bugs list.
  Common options consolidates into a 10-row table; deliberate
  negative `Events` section (no `on_*` helpers, no virtual
  events, data flow is `command` + `set` callbacks).

`tools/check_doc_structure.py --category layout` →
scrollbar.md no longer in the missing-sections list (5/12
pages still pending).
`tools/check_doc_snippets.py --run --file
docs/widgets/layout/scrollbar.md` → 0 failures (7 snippets, 1
executed).

Prior session (2026-04-30, gridframe sweep):

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
- [x] `panedwindow.md` — resizable split regions
- [x] `scrollbar.md` — themed ttk.Scrollbar wrapper
- [x] `scrollview.md` — scrollable viewport over a content frame
- [x] `accordion.md` — mutual-exclusion stack of Expanders
- [x] `expander.md` — single collapsible region
- [x] `separator.md` — visual divider
- [x] `sizegrip.md` — bottom-right resize handle

### Widget pages — navigation (`docs/widgets/navigation/` + `appshell.md`, 5 pages) — IN PROGRESS 2/5

The "navigation directory" turned out to be heterogeneous; one
template doesn't fit all five pages. Per-page assignment:

| Page | Canonical location | Template | Status |
|---|---|---|---|
| `tabs.md` | `widgets/navigation/tabs.md` | `widget-navigation-template.md` | done (anchor) |
| `appshell.md` | `widgets/application/appshell.md` | bespoke app-shell arc | **done 2026-05-01** |
| `sidenav.md` | `widgets/navigation/sidenav.md` | `widget-navigation-template.md` | pending |
| `toolbar.md` | `widgets/navigation/toolbar.md` | **`widget-action-template.md`** (no nav model) | pending |
| `navigationview.md` | `widgets/navigation/navigationview.md` | none — deprecation stub | add to `SKIP_FILES` in `tools/check_doc_structure.py` |

Rationale for the split: AppShell extends `App` and owns the window
(not a child widget — its surface is windowing + composition, not
selection); Toolbar has no selection state, no keyed targets, no
signal (action-chrome host, not navigation). Forcing both under the
navigation template would mean contrived "Navigation model" sections
for pages that don't have one.

Template: `docs/_template/widget-navigation-template.md` (slim arc,
restructured this session). Required H2s: `Basic usage`,
`Navigation model`, `Common options`, `Behavior`, `Events`,
`When should I use WidgetName?`, `Related widgets`, `Reference`.
No `*Optional` H2s — `Navigation model` is required (every
navigation page has keyed targets and a selection-vs-imperative
distinction worth documenting).

`tabs.md` is the canonical anchor for the **navigation-template**
pages (Tabs, SideNav). AppShell uses its own arc — see the AppShell
session notes below for the structure.

Last session (2026-05-01, navigation sweep started — template
restructure + tabs anchor):

- `widget-navigation-template.md` rewritten to the slim arc.
  Old form led with `Framework integration` + `What problem it
  solves` + `Core concepts` + fragmented `Pages and views` /
  `Navigation behavior` / `Common options & patterns` / `UX
  guidance` H2s. New form: intro → `Basic usage` → `Navigation
  model` → `Common options` → `Behavior` → `Events` → `When
  should I use WidgetName?` → `Related widgets` → `Reference`.
  Mental-model section name fixed at `Navigation model`
  (covers keyed targets, random-vs-sequential, signal /
  variable / imperative, page lifecycle). No `*Optional` H2s.
- `tabs.md` rewritten as the anchor. Tabs is the simplest
  navigation primitive — pure tab-bar chrome, no content
  coupling, single selection signal/variable. Five things
  the old page got wrong or omitted, four of which became
  new bugs:
  (1) the old page documented `variant='pill'` as a working
  variant (and the docstring at `composites/tabs/tabs.py:42`
  still lists it). Verified at runtime: only `bar` and
  `default` (alias) are registered for `TabItem.TFrame`
  (`style/builders/tabitem.py:27-28`); calling
  `Tabs(variant='pill')` raises
  `BootstyleBuilderError: Builder 'pill' not found for widget
  class 'TabItem.TFrame'. Available variants: default, bar`.
  Documented the failure in a `!!! warning` block; added to
  the bugs list.
  (2) the old `Events` section listed `<<TabSelect>>` /
  `<<TabClose>>` / `<<TabAdd>>` and showed
  `tabs.bind("<<TabSelect>>", ...)` as the way to observe
  selection. Verified at runtime that `<<TabSelect>>` and
  `<<TabClose>>` are emitted **on the TabItem**
  (`composites/tabs/tabitem.py:253,261`), not on Tabs, and Tk
  virtual events do not propagate up the parent chain.
  Tabs.bind on those events silently no-ops. Only `<<TabAdd>>`
  is emitted on Tabs (`composites/tabs/tabs.py:220`). The
  class docstring's claim "Fired when a tab is selected
  (bubbled from TabItem)"
  (`composites/tabs/tabs.py:29-30`) is false. Documented as
  a `!!! warning` with the correct `home.bind("<<TabSelect>>",
  ...)` workaround; added to the bugs list.
  (3) the old page never noted that `on_tab_changed(callback)`
  and `on_tab_added(callback)` deliver **different callback
  shapes**. `on_tab_changed` is `signal.subscribe` →
  `cb(value)`; `on_tab_added` is `bind('<<TabAdd>>')` →
  `cb(event)`. Documented as a per-helper table in `Events`;
  added to the bugs list.
  (4) the old page never warned that the **first `add()` call
  unconditionally writes that tab's value to the variable**
  (`composites/tabs/tabs.py:335-336`), even if the bound
  signal already held a meaningful initial value. Verified at
  runtime: `Signal('initial')` passed to `Tabs(signal=…)` then
  `tabs.add(...)` clobbers `'initial'` with the first tab's
  value. Documented as a `!!! warning` in Navigation model;
  added to the bugs list.
  (5) the old page never noted that `tabs.remove(selected_key)`
  leaves the variable holding an orphan value that no longer
  matches any tab. Verified: after `tabs.set('home');
  tabs.remove('home')`, `tabs.get()` still returns
  `'home'`, and the bar paints nothing as selected.
  Documented as a `!!! warning` in Behavior; added to the
  bugs list.
  Also documented: `value` defaults to `key` (so
  `tabs.get()` returns a key string by default); auto-key
  scheme (`tab_<n>`); duplicate-key `add()` raises
  `ValueError`; `tab_width='stretch'` is horizontal-only
  (vertical packs ignore the `expand=True` path,
  `composites/tabs/tabs.py:319-322`); `orient` and `variant`
  are construction-only (raise `ValueError` on reconfigure,
  `tabs.py:405-417`); `closable='hover'` reserves space and
  fades the glyph in via the ttk state map; the close button
  does **not** auto-`remove()` — handlers decide.
  `TabItem` is **not a public export** (verified:
  `getattr(ttk, 'TabItem', None) is None`); users only ever
  get a TabItem instance back from `add()`.

`tools/check_doc_structure.py --category navigation` →
4/5 still failing (the 4 pages not yet rewritten); tabs.md
no longer in the missing-sections list.
`tools/check_doc_snippets.py --run --file
docs/widgets/navigation/tabs.md` → 0 failures (4 snippets,
1 executed).

Last session (2026-05-01, AppShell sweep — bespoke app-shell arc):

- `appshell.md` rewritten at its canonical location
  `docs/widgets/application/appshell.md` (NOT under
  `widgets/navigation/`). The vestigial 10-line "Moved" stub at
  `docs/widgets/navigation/appshell.md` was deleted — it pointed
  readers at outdated redirect targets, was not in the zensical
  nav (zensical lists AppShell under "Application", not
  "Navigation"), and only existed to fail the structure check
  for the navigation directory. Verified no inbound links pointed
  at the stub before deletion.
- AppShell extends `App` and owns the window/`mainloop`/`frameless`
  /settings — the navigation template never fit, so the page uses
  a bespoke app-shell arc:
  Basic usage → Anatomy (structural diagram of the shell) →
  Window options → Building the shell (`add_page` family) →
  Navigation (programmatic + `<<PageChange>>` payload) →
  Components (drop-down handles for `toolbar` / `nav` / `pages`)
  → When should I use AppShell? → Related widgets → Reference.
  The page is in `widgets/application/`, which is **not** in
  `CATEGORY_TEMPLATE_MAP` in `tools/check_doc_structure.py`, so
  no template enforcement applies (same freedom as `app.md` and
  `toplevel.md`).
- Three things the old page got wrong or omitted, two of which
  are documentation gaps and one a bug worth surfacing:
  (1) the old page documented the navigation display modes
  (`expanded` / `compact` / `minimal`) without describing how
  they actually behave. Verified at runtime
  (`composites/sidenav/view.py:296-319`):
  `expanded` — full pane, packed when `is_pane_open=True`,
  hidden via `pack_forget()` when toggled off;
  `compact` — narrow icon-only pane, always packed regardless
  of `is_pane_open`;
  `minimal` — same widths as expanded but designed to be
  hidden via the hamburger (the pane visibility is gated on
  `is_pane_open`). Documented honestly in the Window options
  table.
  (2) the old page never noted that the pre-populated toolbar
  layout is **fixed**. Verified
  (`composites/appshell.py:151-175`): the order is hamburger
  (only when `show_nav=True`) → separator → title label (only
  when `title=` is set) → spacer → window controls (only when
  `show_window_controls=True`). User-added buttons land **after**
  the spacer, so they always sit at the right edge — there's no
  way to insert before the title or to reorder the built-ins.
  Documented as a structural constraint in Anatomy.
  (3) the old page never noted the **no-toggle gap** when
  `show_toolbar=False, show_nav=True`. Verified at runtime: the
  hamburger lives on the toolbar (added by AppShell at
  `composites/appshell.py:163-167`), and the SideNav is
  constructed with `show_header=False` (`appshell.py:188`)
  regardless of toolbar presence — `show_header=False` skips
  the entire `_build_header()` call (`view.py:227`), which is
  where SideNav would normally render its own internal
  hamburger. Net effect: with `show_toolbar=False, show_nav=True`,
  the sidebar has **no built-in UI** to toggle the pane. The
  pane is still collapsible programmatically via
  `shell.nav.toggle_pane()`, but users have no affordance to do
  so unless the developer adds one. Documented as a `!!! note`
  in Anatomy. Worth fixing — either default `show_header=True`
  when `show_toolbar=False`, or add a toggle button somewhere
  visible. Added to the bugs list.
  Also documented: the full `add_page()` surface (including
  `scrollable=True` wrapping the page in a ScrollView,
  `page=` substituting a custom widget, `is_footer=True` /
  `group=` mutual exclusion, the auto-navigate-on-first-page
  behavior); the four sidebar primitives (groups, headers,
  separators, footer items) as forwarders to SideNav; the
  `<<PageChange>>` payload (`page` / `prev_page` / `prev_data`
  / `nav` / `index` / `length` / `can_back` / `can_forward`,
  plus user-supplied data dict merged at the top level — note
  the keys are `page`/`prev_page`, NOT `key`/`prev_key` as the
  old page implied); the property table for the drop-down
  handles (`toolbar` / `nav` / `pages`) including the
  `Toplevel | None` / `SideNav | None` / `PageStack` (always)
  presence semantics; the `show_nav=False` path which raises
  `RuntimeError` from `add_page()` and forces use of
  `shell.pages.add(...)` directly. Added a `!!! tip` for the
  CLI scaffolding command (`ttkb start MyApp --template appshell`)
  near the Basic usage section.

`tools/check_doc_snippets.py --run --file
docs/widgets/application/appshell.md` → 0 failures (9 snippets,
5 executed). Structure check N/A (page is in
`widgets/application/`, not under any template-enforced
category).

Pages to review:

- [x] `tabs.md` — navigation template (anchor)
- [x] `appshell.md` — bespoke app-shell arc (at `widgets/application/`)
- [ ] `sidenav.md` — navigation template
- [ ] `toolbar.md` — **action template** (no selection state)
- [ ] `navigationview.md` — deprecation stub; add to `SKIP_FILES`

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
- `Scrollbar` reconfiguration of `orient` after construction does
  **not** rebuild the resolved ttk style. `Scrollbar.__init__`
  resolves the style once (e.g. `bs[…].primary.Vertical.TScrollbar`
  via the bootstyle builder's `ORIENT_CLASSES` path), but
  `configure(orient='horizontal')` only writes the Tk `-orient`
  option — the cached `style=` string is never invalidated, so the
  widget renders up/down arrows in a horizontal layout. Verified at
  runtime: `Scrollbar(orient='vertical', accent='primary')
  .configure(orient='horizontal')` → `cget('style') ==
  'bs[…].primary.Vertical.TScrollbar'`. Either invalidate and
  rebuild the style on `orient` writes (matching what construction
  does), or document `orient` as construction-only and reject
  reconfiguration. (Surfaced by scrollbar.md rewrite, 2026-04-30.)
- `ScrollView.configure(scroll_direction=...)` does **not** regrid
  the scrollbars. `_delegate_scroll_direction`
  (`widgets/composites/scrollview.py:121-145`) only rewires the
  canvas's `xscrollcommand` / `yscrollcommand` and calls
  `_update_scrollbar_visibility()`, which calls
  `self.horizontal_scrollbar.grid()` / `.vertical_scrollbar.grid()`
  with no args. Initial grid placement uses `sticky='ns'` /
  `'ew'` (`_layout_widgets`, `:233-237`), but a bar that was
  *never* gridded at construction (because the initial
  `scroll_direction` excluded its axis) gets default Tk
  auto-placement on the post-reconfigure `.grid()` call — landing
  at the next free cell with `sticky=''`. Verified: `ScrollView
  (scroll_direction='vertical').configure(scroll_direction='both')`
  with content overflowing both axes lands the horizontal bar at
  `row=1, column=0, sticky=''`, so it renders as a stub at the
  left edge instead of spanning the canvas width. Either rebuild
  the layout (re-running `_layout_widgets` for newly-relevant
  bars) on direction change, or document `scroll_direction` as
  construction-only. (Surfaced by scrollview.md rewrite,
  2026-05-01.)
- `Accordion.add()` raises `TypeError: got multiple values for
  keyword argument 'accent'` when the accordion was constructed
  with its own `accent` and the per-call `add()` also passes
  `accent=` (same for `variant=`). Cause: the precedence resolution
  at `composites/accordion.py:128-129` — `accent = self._accent or
  kwargs.pop('accent', None)` — short-circuits before popping when
  `self._accent` is truthy, so the per-call accent stays in
  `**kwargs` and collides with the explicit `accent=accent` passed
  to the Expander constructor on the next line. Verified at runtime:
  `Accordion(accent='primary').add(accent='success')` →
  `TypeError`. Fix: always pop both keys first, then resolve
  precedence (`per_call = kwargs.pop('accent', None); accent =
  self._accent or per_call`). Decide intentionally whether
  per-call should win over accordion default or vice versa; either
  way, the collision must not crash. (Surfaced by accordion.md
  rewrite, 2026-05-01.)
- `Accordion.remove(key)` does **not** fire `<<AccordionChange>>`
  when the removed expander was the last one. The `if
  self._expanders:` guard at `composites/accordion.py:210-214`
  conditions the `event_generate(...)` call on at least one
  expander remaining. Net effect: a listener tracking "what is
  open" sees every transition except the empty → still-empty
  reset that follows the final removal — and any state derived
  from the listener (e.g. enabling a "hide all" toggle) silently
  desyncs. Either drop the guard (the empty event payload is fine
  — `expanded=[]`) or document the suppression as deliberate.
  (Surfaced by accordion.md rewrite, 2026-05-01.)
- `Accordion.configure(show_separators=True)` does **not**
  retroactively insert separators between existing expanders, and
  `configure(show_separators=False)` does not remove them. The
  delegator at `composites/accordion.py:368-374` only writes the
  flag; only future `add()` calls inject separators (they check
  `self._show_separators` at insert time, line 112). Net effect:
  a UI that toggles a "compact" preset post-construction sees the
  flag flip but the layout doesn't change. Either rebuild the
  separator strip on configure, or document as
  construction-time-effective. (Surfaced by accordion.md rewrite,
  2026-05-01.)
- `Expander.collapsible=False` only hides the chevron and gates
  `toggle()`; the programmatic paths `expand()` / `collapse()` /
  `configure(expanded=...)` ignore `self._collapsible` entirely.
  `Expander.collapse()` (`composites/expander.py:273-283`) doesn't
  consult the flag, and `_delegate_expanded`
  (`composites/expander.py:483-492`) calls `expand()` /
  `collapse()` directly. Verified at runtime:
  `Expander(collapsible=False).collapse()` collapses the content
  with no warning. Either treat `collapsible=False` as a hard
  invariant (no programmatic collapse either) or rename it to
  reflect that it only controls user-facing affordances. Also,
  `_update_selection_state` (`composites/expander.py:140-144`) is
  a deliberate placeholder — `signal=` / `variable=` selection
  fires `<<Selected>>` and updates `is_selected`, but does not
  apply the `selected` ttk state to the header. Pair with
  `highlight=True` + `expand()` from a listener for visual
  feedback today. (Surfaced by expander.md rewrite, 2026-05-01.)
- `Separator.configure(orient=...)` after construction does **not**
  rebuild the resolved ttk style. Separator is in `ORIENT_CLASSES`
  (`style/token_maps.py:42`), so the bootstyle wrapper resolves the
  style once at construction with the orientation embedded as a
  prefix (e.g. `bs[…].primary.Vertical.TSeparator`). Subsequent
  `configure(orient='horizontal')` only writes the Tk option without
  invalidating the cached `style=` string. Verified at runtime:
  `Separator(orient='vertical', accent='primary')
  .configure(orient='horizontal')` → `cget('style') ==
  'bs[…].primary.Vertical.TSeparator'`, and the line renders with
  the wrong axis. Same fix as the Scrollbar `orient` bug already on
  this list — invalidate and rebuild on `orient` writes, or document
  `orient` as construction-only and reject reconfiguration. Note
  that `LabelFrame.show_border` had a similar
  unread-by-`__init__` issue; here the option round-trips correctly
  but the cached style does not. (Surfaced by separator.md rewrite,
  2026-05-01.)
- `SizeGrip` `accent` is **silently ignored** by the style builder.
  `SizeGrip.__init__` captures `accent` into `_accent` and the
  bootstyle wrapper resolves a unique style key (e.g.
  `bs[…].primary.TSizegrip`), but the SizeGrip style builder
  (`style/builders/sizegrip.py:11-16`) reads only `surface` and
  writes `background` — there's no path that recolors the
  platform-drawn `Sizegrip.sizegrip` element. Net effect: every
  accent renders identically to the default, with the same
  configured tokens. Either (a) drop `accent` from the SizeGrip
  TypedDict and document the dot color as platform-determined, or
  (b) extend the builder to draw a custom dot pattern that honors
  accent. (Surfaced by sizegrip.md rewrite, 2026-05-01.)
- `SizeGrip.configure(surface=...)` raises `TclError: unknown option
  "-surface"`. SizeGrip is not in `CONTAINER_CLASSES`, so the
  bootstyle wrapper's surface-as-accent-override path doesn't apply,
  and `SizeGrip.__init__` doesn't add a `_delegate_surface` to lift
  the option into a Python-side configure delegator (the way Frame
  does). The escape hatch
  `sizegrip.configure_style_options(surface='primary')` does not
  raise but produces an unstyled `Default.TSizegrip` style without
  the hash prefix — silently reverting to the platform default.
  Either lift `surface` into a configure delegator (matching the
  read path that the construction wrapper already exercises) or
  document `surface` as construction-time only. (Surfaced by
  sizegrip.md rewrite, 2026-05-01.)
- `Tabs(variant='pill')` raises `BootstyleBuilderError`. The
  constructor's signature
  (`composites/tabs/tabs.py:42`) and class docstring list `'pill'`
  as a supported variant alongside `'bar'`, but no `pill` builder is
  registered for `TabItem.TFrame`
  (`style/builders/tabitem.py:27-28` only registers `'bar'` and
  `'default'`). Verified at runtime:
  `Tabs(variant='pill')` →
  `BootstyleBuilderError: Builder 'pill' not found for widget class
  'TabItem.TFrame'. Available variants: default, bar`. Either
  register a `pill` variant on `TabItem.TFrame` /
  `TabItem.TLabel` / `TabItem.TButton` (matching the rounded look
  the docstring implies) or remove `'pill'` from the type hint and
  docstring. (Surfaced by tabs.md rewrite, 2026-05-01.)
- `Tabs.<<TabSelect>>` and `Tabs.<<TabClose>>` do **not** fire on
  the `Tabs` widget — they fire only on the individual `TabItem`
  returned by `add()`. The `Tabs` class docstring
  (`composites/tabs/tabs.py:29-30`) states "Fired when a tab is
  selected (bubbled from TabItem)" / "(bubbled from TabItem)" but
  no bubbling occurs — Tk virtual events do not propagate up the
  parent chain, and `Tabs` does not call
  `event_generate(...)` to forward them. Verified at runtime:
  `tabs.bind('<<TabSelect>>', cb)` never fires; binding the same
  event on `tabs.item(key)` does. The only event actually emitted
  on `Tabs` is `<<TabAdd>>` (from `_on_add_click`,
  `composites/tabs/tabs.py:218-220`). Either forward the events
  (e.g. in `_on_tab_click` and `_on_close_click`, also
  `event_generate` on `self.master.master` — the `Tabs` —
  with the value payload) or fix the docstring and add a
  `tab.bind('<<TabSelect>>', ...)` example to the public API.
  (Surfaced by tabs.md rewrite, 2026-05-01.)
- `Tabs.on_tab_changed(callback)` and `Tabs.on_tab_added(callback)`
  deliver **different callback shapes**. `on_tab_changed`
  (`composites/tabs/tabs.py:465-474`) is backed by
  `Signal.subscribe`, so the callback receives the new selected
  *value* (`cb(value)`). `on_tab_added`
  (`composites/tabs/tabs.py:222-231`) is backed by
  `bind('<<TabAdd>>', cb)`, so the callback receives a Tk *event*
  (`cb(event)`). The framework convention elsewhere is for
  `on_*` helpers to deliver events — wrap `on_tab_changed` to
  fire `cb(event)` (where `event.data` carries `{"value":
  value}`), or rename the helper to `subscribe_tab_changed` to
  signal the different shape. (Surfaced by tabs.md rewrite,
  2026-05-01.)
- `Tabs.add()` unconditionally writes the first tab's value to the
  bound variable (`composites/tabs/tabs.py:335-336`), clobbering
  any pre-existing value held by an externally-supplied
  `signal=` / `variable=`. Verified at runtime: a `Signal('initial')`
  passed in via `Tabs(signal=sig)` ends up holding the first
  added tab's value once `add()` is called. Either guard the
  auto-select on `if self._variable.get() == ''` (or some
  default-sentinel test), or document the behavior so callers
  know to set the desired initial value *after* adding tabs.
  (Surfaced by tabs.md rewrite, 2026-05-01.)
- `Tabs.remove(key)` does not reset selection state when the
  removed tab was the active one. The variable still holds the
  orphan value, no tab paints as selected, and `tabs.get()`
  returns a stale key. Verified at runtime: `tabs.set('home');
  tabs.remove('home'); tabs.get()` returns `'home'` despite
  `tabs.keys()` no longer containing it. Either auto-fall-through
  to the next remaining tab (e.g. select index 0 of
  `self._tab_order`) or clear the variable to `''`. The current
  behavior leaves callers responsible for fixing up state every
  time they remove a tab. (Surfaced by tabs.md rewrite,
  2026-05-01.)
- `AppShell` with `show_toolbar=False, show_nav=True` ships **no
  built-in UI to toggle the sidebar pane**. The hamburger button
  lives on the toolbar and is added by AppShell itself
  (`composites/appshell.py:163-167`); when the toolbar is omitted,
  there's no hamburger anywhere. The SideNav would normally render
  its own hamburger inside its header, but AppShell hard-codes
  `show_header=False` on the inner SideNav (`appshell.py:188`)
  unconditionally — so even when `collapsible=not show_toolbar`
  flips the SideNav's collapsible flag back on, the header that
  would contain the toggle is suppressed. Net effect: the pane is
  collapsible only via `shell.nav.toggle_pane()` from code or
  keyboard, not from any visible affordance. Either pass
  `show_header=True` to the inner SideNav when `show_toolbar=False`,
  or add a fallback toggle somewhere the user can see (e.g. inside
  the body frame). (Surfaced by appshell.md rewrite, 2026-05-01.)

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
