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

### Current handoff (2026-05-03, bug-fix sessions 5–6 DONE — next-session entry point)

**Read this section first.** The full per-page session notes below
this handoff are historical context — useful when picking up
specific work, not required reading to get oriented.

Pass 2 (editorial review) is COMPLETE across every section. Phases
1–7 and 9A–9D are also complete. The cross-cutting link consistency
pass is also complete (commit `e07c372`).

**Remaining work gated on a running display:**

1. **Phase 6F — popup / animated screenshot capture.** Surfaces
   today as 1 known `IMAGE:` placeholder (`selectbox.md`) plus
   missing imagery on the 11 dialog pages and 7 animated-widget
   pages (Toast, Tooltip, Accordion, Expander, PageStack,
   FloodGauge, Meter). Needs (a) a renderer mode that captures a
   `Toplevel` bbox after the popup is realized but before any
   modal `grab_set` blocks the parent loop, and (b) an MP4/GIF
   recording path for animations. The plan doc
   (`analysis/docs-review-and-plan.md` § Phase 6F) has the full
   list and the renderer mode needed.

2. **Phase 8C — rendered docstring review for 22 priority symbols.**
   Run `zensical serve -o` and visually verify mkdocstrings
   rendering matches the spec model on `App`, `AppShell`, `Form`,
   `TableView`, `MessageDialog`, `BaseDataSource`, etc. — no
   orphan `Examples:`, no broken cross-links, both `Attributes:`
   and `Args:` rendering side-by-side.

**Bug-fix sessions 5–6 (2026-05-03) — CLOSED.**

Commits: `dffb234` (session 5, 7 bugs) + `0d98bc6` + `03945a4` (session 6, 20 bugs).
27 bugs fixed, 24 warning/danger blocks removed from docs.

Session 5 fixes (dialog localization + ListView CRUD payloads):
- `MessageDialog` defaults `localize=True` (`dialogs/message.py:72`)
- `FormDialog` default buttons go through `MessageCatalog.translate` (`formdialog.py:507-509`)
- `FilterDialog` button labels and "Select All" go through `MessageCatalog.translate` (`filterdialog.py:108,333-335`)
- `ListView.<<ItemInsert>>` carries `{'record': dict}` (`listview.py:1387`)
- `ListView.<<ItemUpdate>>` carries `{'record': dict}` (partial update, `listview.py:1405`)
- `ListView.<<ItemDelete>>` carries `{'record_id': Any}` (`listview.py:927,1421`)
- `ListView.<<ItemDeleteFail>>` carries `{'record_id': Any, 'error': str}` (`listview.py:929`)

Session 6 fixes:
- `ValidationResult.__bool__` returns `is_valid` (`core/validation/validation_result.py`)
- `ValidationRule('custom')` no `func=` now fails instead of silently passing (`validation_rules.py`)
- `RadioGroup.values()` returns actual radio values not keys (`radiogroup.py`)
- `IntlFormatter._format_time` uses `locale=` kwarg — time-only formatting fixed (`intl_format.py`)
- `IconSpec.color` theme tokens resolved through style engine before PIL (`bootstyle_builder_base.py`)
- `Tabs(variant='pill')` raises `ValueError` at construction, not at `add()` (`tabs.py`)
- `Tabs` forwards `<<TabSelect>>` and `<<TabClose>>` to the Tabs widget after each `add()` (`tabs.py`)
- `PageStack.<<PageUnmount>>` carries `{'page', 'prev_page', 'prev_data'}` (`pagestack.py`)
- `Notebook.insert()` validates key before `super().insert()` — no orphan tabs (`notebook.py`)
- `Notebook.insert()` applies `**kwargs` to existing widget via `configure()` (`notebook.py`)
- `FilterDialog.show()` resets `self.result = None` at start (`filterdialog.py`)
- `Toolbar.add_widget()` raises `ValueError` for wrong parent (`toolbar.py`)
- `SideNav(display_mode='minimal')` defaults `is_pane_open=False` (`sidenav/view.py`)
- `TableView` export events fire on `self` not `self._tree` (`tableview.py`)
- `ToolTip` second attach destroys prior instance cleanly (`tooltip.py`)

**Remaining warning/danger blocks (18 total) — all documented behavior / CPython / design intent.**
No code changes are needed for any of these.

| Block | File | Category |
|---|---|---|
| `state()` requires iterable, not string | `capabilities/state-and-interaction.md:87` | Documented gotcha |
| `app.settings.theme` decoupled from `Style.theme_use()` | `capabilities/configuration.md:224` | Architectural design |
| `unbind(seq, fid)` broken on Python 3.13 | `capabilities/signals/callbacks.md:139` | CPython bug |
| Exception handling asymmetry `immediate=True` | `capabilities/signals/signals.md:239` | Documented behavior |
| `clear_cache()` breaks live widgets | `capabilities/icons/images.md:162` | Documented contract |
| SQL injection contract | `guides/datasource.md:117` | Documented trusted-input |
| Catalogs require Tk | `guides/localization.md:223` | Documented constraint |
| Hamburger ≠ show/hide in expanded mode | `widgets/navigation/sidenav.md:201` | Navigation design |
| `surface=` overridden by `inherit_surface=True` | `widgets/primitives/text.md:359` + `canvas.md:290` | Wrapper design |
| `_surface` does not tint Text widget | `widgets/primitives/text.md:368` | Builder design |
| SQL injection contract | `widgets/data-display/tableview.md:302` | Documented trusted-input |
| Pages must be parented to stack | `widgets/views/pagestack.md:135` | Documented constraint |
| Sensitive data | `widgets/inputs/passwordentry.md:78` | Security advisory |
| Deprecated NavigationView | `widgets/navigation/navigationview.md:7` + `reference/…:3` | Intentional |
| (cross-ref to callbacks danger) | `capabilities/signals/virtual-events.md:330` | Cross-reference |

Run `python tools/check_doc_snippets.py --run` before and after any
further changes to guard against regressions.

**Bug-fix session 4 (2026-05-03) — CLOSED. Commit: `1ca3743`.**

Fixed (10 bugs, docs updated to match each):

- `AppSettings.light_theme`/`dark_theme` now default to
  `'bootstrap-light'`/`'bootstrap-dark'` instead of `docs-light`/
  `docs-dark` (`runtime/app.py:302-303`). Docs updated in 5 pages.
- `Signal.map()` GC-sensitivity fixed — closure now holds a strong
  reference to the derived signal so inline `textvariable=sig.map(fn)`
  patterns keep working after construction (`core/signals/signal.py:234`).
- `Toast.show()` called twice no longer leaks the first Toplevel —
  `_build_toast()` destroys the previous Toplevel before creating a
  new one (`composites/toast.py:219`).
- `Toast.configure(bootstyle=...)` now syncs `_accent` so the next
  `show()` paints with the updated styling (`composites/toast.py:152`).
- `CheckButton.set(None)` now enters the indeterminate (`alternate`)
  ttk state instead of raising `TypeError` (`primitives/checkbutton.py:111`).
- `Switch(bootstyle='primary')` now always sets `variant='switch'`
  regardless of `bootstyle` presence (`primitives/switch.py:43`).
- `Entry.configure(surface=...)` no longer raises `TclError` — added
  `_delegate_surface` that calls `rebuild_style()` (`primitives/entry.py`).
  Same fix applied to `Combobox` and `Spinbox`.
- `Entry.configure(density=...)` now rebuilds the ttk style (not just
  the font) — `_delegate_density` now calls `rebuild_style()` after
  updating `_style_options` (`primitives/entry.py`). Same fix applied
  to `Combobox` and `Spinbox`.
- `pack_propagate()` / `grid_propagate()` query (no-arg call) now
  returns the current propagation state — fixed by calling
  `super().pack_propagate()` / `super().grid_propagate()` without
  args when `flag is None` (`core/capabilities/pack.py:112`,
  `core/capabilities/grid.py:113`).

**Bug-fix session 3 (2026-05-03) — CLOSED. Commit: `417abe4`.**

Fixed (10 bugs, docs updated to match each):

- `SelectBox.configure(value=X)` inverted delegate — swapped
  `if value is not None` branches in `_delegate_value`
  (`composites/selectbox.py:493`).
- `SelectBox.<<Change>>` now fires on the SelectBox itself — added
  `self.event_generate(...)` after the inner `entry_widget` emit
  (`selectbox.py:536`).
- `Calendar.set()` / `set_range()` now enforce `min_date`,
  `max_date`, and `disabled_dates` — call `_is_disabled()` and
  return early on invalid dates (`composites/calendar.py`).
- `Calendar.set_range(None, None)` now clears `_selected_date` —
  fallback changed from `self._selected_date` to `None`
  (`calendar.py:286`).
- `PageStack.remove(key)` now rewrites `_history` to strip orphan
  entries and adjusts `_index` accordingly
  (`composites/pagestack.py:125`).
- `PageStack.add(key, page, **kwargs)` now forwards `**kwargs` via
  `page.configure(**kwargs)` when `page=` is provided
  (`pagestack.py:107`).
- `TabView.navigate(key, data=...)` double history push fixed —
  suppresses variable trace during navigate so only one
  `pagestack.navigate()` runs (`tabs/tabview.py:220`).
- `Tabs.add()` no longer clobbers signal initial value — guards
  auto-select on `not self._variable.get()` (`tabs/tabs.py:335`).
- `Tabs.remove(key)` now falls through to next tab (or `""`) when
  the active tab is removed (`tabs/tabs.py:354`).
- `RadioGroup(accent=...)` now reaches child radios — restores
  `_accent` after `super().__init__()`, same fix ToggleGroup had
  (`composites/radiogroup.py:106`).

**Bug-fix session 1 (2026-05-03) — CLOSED. Commits: `8deee17`
`64002c6` `dfa11f7` `280d95f` `906c0f6` `1cc06b2` `42ee1dd`.**

Fixed (15 bugs, docs updated to match each):

- `ValidationRule('compare')` removed from `RuleType` literal (was
  silent no-op; `core/validation/types.py`).
- `ValidationMixin.validate()` docstring fixed — return is "True if
  all rules passed", not "True if performed regardless of result"
  (`validation_mixin.py:99`).
- `add_validation_rule()` docstring example: `min_length=` → `min=`
  (`validation_mixin.py:77`).
- Form `field_signal()`/`field_textsignal()` — now reads both
  `signal`/`textsignal` (Field subclasses) and `_signal`/`_textsignal`
  (raw SignalMixin subclasses) (`composites/form.py:598`).
- Form unknown editor names now emit `UserWarning` instead of
  silently building a TextEntry (`composites/form.py:574`).
- Form `columns=` accepted as alias for `col_count=` (`form.py:170`).
- `TabsItem.label` annotated as reserved/not rendered (`form.py:98`).
- `Calendar.set(None)` now clears selection instead of silently
  returning (`composites/calendar.py:216`).
- `Calendar.__init__` clamps `_display_date` into `[min_date,
  max_date]` window so the widget doesn't open stranded
  (`calendar.py:183`).
- Docstring fixes: `DateEntry` `monthAndDate`→`monthAndDay`;
  `TimeEntry` removed bogus `"mediumTime"` preset; `FormDialog`
  `resizable` default `False`; `MessageDialog` `show_info` etc.
  live on `MessageBox`; `demo.py` Meter uses modern param names.
- `Notebook.on_tab_changed` event name: `<<NotebookTabChange>>` →
  `<<NotebookTabChanged>>` — restores the entire enriched event
  mechanism (`notebook.py:570`).
- `LabeledScale` configure delegates: inverted query/set branches
  fixed on `_delegate_value`, `_delegate_minvalue`,
  `_delegate_maxvalue` (`composites/labeledscale.py:148`).
- `OptionMenu.<<Change>>` double-fire: `_bind_change_event()` now
  called once (via delegate); redundant explicit call removed
  (`optionmenu.py:116,119`).
- `TabView.remove(key)` `KeyError`: `add()` now passes `key=key` to
  `Tabs.add()` so both sides share the key string; `remove()` passes
  the string key not the widget. Also restores `enable_closing`
  (`tabs/tabview.py:166,194`).
- `Notebook.remove(tab)`/`forget(tab)` `TypeError`: MRO conflict
  bypassed by calling `ttk.Notebook.forget(self, tabid)` directly
  (`notebook.py:379,385`).

**Next session (no display needed): continue the bug list.**

The 10-bug list from session 2 is fully closed. Remaining bugs are
still logged in the per-page notes below (search "Surfaced by").
The next-highest-value bugs without a display requirement (search
the per-page notes for specifics):

- `ToggleGroup.set(value)` does not validate against known keys
  (same shape as the RadioGroup orphan-value bug).
- `OptionMenu.set(value)` does not validate against `options=`.
- `SelectBox.value = "not_in_items"` is accepted even when
  `allow_custom_values=False`.
- `SideNav.select(key)` does not validate key.
- `Accordion.add()` raises `TypeError` when accordion has `accent`
  and per-call `add()` also passes `accent=`.
- `Accordion.remove(key)` suppresses `<<AccordionChange>>` when
  removing the last expander.
- `Accordion.configure(show_separators=...)` does not retroactively
  add/remove separators.
- `Expander.collapsible=False` does not gate programmatic
  `expand()`/`collapse()` paths.

Run `python tools/check_doc_snippets.py --run` before and after each
fix to guard against regressions. Update the relevant `.md` page to
remove the `!!! warning`/`!!! danger` block and replace with
accurate prose after each fix.

Sweep status (closed):

- **Guides** (14/14) — DONE 2026-04-30.
- **Widgets** — DONE: dialogs 11/11, inputs 12/12 (Form moved here from
  the deleted `forms/` category 2026-05-02), data-display 8/8,
  layout 12/12, navigation 5/5, overlays 2/2, selection 9/9, views 3/3,
  primitives 5/5, actions 5/5.
- **Platform** (17/17) — DONE 2026-05-01.
- **Capabilities** (18/18) — DONE 2026-05-02. All four sub-sections
  closed (Signals & Events 4/4, Layout 4/4, Validation 3/3,
  Icons & Images 3/3) plus the four standalone pages
  (`layout-props.md`, `state-and-interaction.md`, `configuration.md`,
  `localization.md`).
- **Design System** (6/6) — DONE 2026-05-02.

Phase 8B (ListView.badge dispatch fix) shipped in commit `d6317b0`
(2026-05-02). 8C (rendered review) is the only Phase 8 item still
open and requires a display.

**Form relocation (2026-05-02).** The `form.md` page was moved from
`widgets/forms/` to `widgets/inputs/`. Rationale: a category of one
is awkward, and `Form` is fundamentally an input — its API surface
(`.value` / `.data` / `validate()` / `field(key)`) matches the input
shape, and it produces a value (a `dict[str, Any]`). Same precedent
as the `selectbox.md` move from `selection/` to `inputs/`. Logistics
done in the move commit:

- `git mv docs/widgets/forms/form.md docs/widgets/inputs/form.md`
- `docs/widgets/forms/` directory removed
- `docs/_template/widget-form-template.md` deleted (uses the input
  template now; `Form model` content lives in the page-level
  `Value model` H2)
- `tools/check_doc_structure.py` — `forms` entry dropped from
  `CATEGORY_TEMPLATE_MAP`
- `zensical.toml` — Form moved from a solo "Forms" menu to the
  bottom of the "Inputs" menu (after `TimeEntry`)
- `docs_scripts/screenshots.toml` — `[[shots]]` entry repointed
  (slug `widgets-form` unchanged; factory module name unchanged)
- 16 inbound link updates across 14 files

Last session (2026-05-02, Form sweep — input template):

- `form.md` rewritten to the slim input arc anchored on
  `textentry.md`. Form is the heaviest input in the framework — a
  `Frame` subclass that builds a labeled grid of editor widgets
  from a list of `FieldItem` / `GroupItem` / `TabsItem` specs (or
  inferred from a `data` dict). The page rebuilds the spec
  vocabulary from scratch against the dataclass + `_normalize_items`
  / `_build_field` source, producing two reference tables (one for
  spec item shapes, one for editor names) plus a dtype-inference
  table.
- Seven runtime-verified bugs surfaced; all seven are real API
  gotchas, not just doc gaps:
  (1) **`form.field_signal()` and `form.field_textsignal()` always
  return `None` for Field-based editors** — the build path reads
  `_signal` (with underscore), but Field exposes the attribute as
  `signal`. Workaround: `form.field(key).signal`.
  (2) **Spec keys outside `FieldItem` are silently dropped.** The
  pre-rewrite docs page used `value=`, `required=`, `validate=`,
  `help=`, `message=` in the spec dict — none of which are read by
  `_normalize_items`. Initial values must come from `data=`; rules
  attach via `form.field(key).add_validation_rule(...)`.
  (3) **Unknown editor names silently fall through to `TextEntry`.**
  `editor='select'`, `editor='int'`, `editor='bogus'` all hit the
  fallback `else` branch in `_build_field` and build a TextEntry
  with no warning.
  (4) **`columns=` (the documented kwarg) raises `TclError`** — the
  actual kwarg is `col_count=`. The pre-rewrite page advertised
  `columns=2`.
  (5) **`numericentry` editor without `dtype` round-trips strings.**
  `_coerce_value` only coerces when `dtype` is set; the auto-built
  variable is a `StringVar` unless `dtype in ('int', int, 'float',
  float)`. Pair `numericentry` with `dtype='int'` or `'float'`
  explicitly.
  (6) **`TabsItem.label` is a dead dataclass field** — never
  rendered anywhere. `TabItem.label` (per-tab) is the one that
  becomes the tab caption.
  (7) **`set_field_value(key, v)` on `visible=False` writes to
  `_data` but no widget exists.** Useful for hidden round-trip
  fields, but inconsistent with the docstring; documented as
  intended behavior on the page.
- Four equivalent reads (`form.data` / `form.value` / `form.get()` /
  `form.cget('data')`) and two equivalent writes (`form.set(...)` /
  `form.value = ...` / `form.configure(data=...)`) documented in
  Value model.
- Other facts surfaced and documented: footer-button command shape
  (`cb(form)` — single positional argument, not no-args); button
  ordering (right-to-left in `pack(side='right')`, primary lands
  on the right edge); `editor_options` filtering for non-Field
  editors (`show_message` / `required` / `validator` filtered out
  for `Spinbox` / `Text` / `Switch` / `CheckButton` / `Scale`);
  `form.set(...)` suspends `on_data_changed` for the duration of
  the bulk write; `Form.validate()` trigger gating (only `'always'`
  and `'manual'` triggered rules run — blur-triggered rules are
  skipped); the synthetic event emission for each rule that runs
  (`<<Valid>>` / `<<Invalid>>` / `<<Validate>>` on the inner
  editor); the role-to-(accent, variant) table for footer buttons.
- Snippet check: 19 snippets, 1 executed, 0 failures. Structure
  check: 12 inputs files, all pass.

**Capabilities sweep — convention notes (2026-05-01).** The capabilities
directory has 18 pages (not the ~12 mentioned in the prior handoff).
Per `zensical.toml:168-196` the nav groups them as:

| Section | Pages |
|---|---|
| Signals & Events | `signals/index.md`, `signals/signals.md`, `signals/callbacks.md`, `signals/virtual-events.md` |
| Layout | `layout/index.md`, `layout/containers.md`, `layout/spacing.md`, `layout/scrolling.md` |
| Validation | `validation/index.md`, `validation/rules.md`, `validation/results.md` |
| Icons & Images | `icons/index.md`, `icons/icons.md`, `icons/images.md` |
| (standalone) | `layout-props.md`, `state-and-interaction.md`, `configuration.md`, `localization.md` |

`docs/capabilities/` is **not** in `CATEGORY_TEMPLATE_MAP` in
`tools/check_doc_structure.py`, so no template enforcement applies (same
freedom as platform/, design-system/, widgets/application/, widgets/
primitives/). The patterns that emerged from the platform sweep apply
here too — replace abstract "X is a shared behavior" framing with
concrete API surface; verify claims at runtime; nav-aligned topic
lists with substantive blurbs (not 3-word labels).

Last session (2026-05-02, design-system sweep — full
section closed 6/6 in one session):

- Six pages rewritten in nav order: `index.md` (commit
  `177c4ae`), `colors.md` (`4c0f54b`), `variants.md`
  (`21fa9ae`), `typography.md` (`6d3df1c`), `icons.md`
  (`1d08bcf`), `custom-themes.md` (`fb5ba98`). All previously
  consisted of 60–110 lines of abstract design-philosophy
  framing that named no concrete API surface.
- Two new bugs surfaced and added to the bugs list (the
  per-page detail lives in the commit messages):
  (1) `ttk.set_theme(name)` may silently fail to switch to a
  user-registered theme; `Style().theme_use(name)` is the
  reliable path. Verified at runtime — `set_theme` calls
  `get_style().theme_use(name)`, but the Style instance
  resolution goes through a different path than `Style()`
  returns directly, and the theme switch doesn't propagate.
  Worth investigating (`runtime/app.py:574,771` and
  `style/style.py:405-415`); the fix is likely to ensure
  `get_style()` returns the same instance as `Style()`.
  Documented in custom-themes.md as a `!!! note`; the
  reliable path (`Style().theme_use(name)`) is the
  documented one.
  (2) Inline `font="not-a-real-token"` falls through silently
  to Tk's default font with no warning — easy footgun if a
  token name is misspelled. Documented in typography.md as a
  `!!! note` with the workaround (token spellings are
  validated only when modifiers are present, e.g.
  `font="not-a-real-token[bold]"` parses through the
  modifier path and falls back correctly to a `body[bold]`-
  shaped resolution).
- Cross-cutting findings re-confirmed at runtime and used to
  ground every page:
  (a) The four token vocabularies (`accent` / `variant` /
  `font` / `icon`) and the kwargs that consume them.
  (b) The full color-token surface: 8 brand semantics + 5
  surfaces + 5 on_<surface> + 5 secondary + 2 strokes
  (`stroke` / `stroke_subtle` — note that `border` and
  `border_subtle` are NOT valid tokens and raise) + 11 shade
  families with auto-generated 9-step spectra.
  (c) Per-widget variant registry from
  `BootstyleBuilderTTk._builder_registry`: Button (default,
  solid, outline, ghost, link, text), MenuButton (no link),
  Toolbutton (no link/text), CheckButton (default + switch),
  Notebook (default, bar, pill, tab), Tabs (default, bar
  only — `pill` is a known bug), Badge (square, pill),
  Progressbar (default, striped, thin), Scrollbar (default,
  square, round, rounded), ButtonGroup (default, solid,
  outline, ghost), everything else default-only.
  (d) The 14 typography tokens (the existing page omitted
  `heading-sm`) and the inline modifier syntax including
  size tokens (`xs`/`sm`/`md`/`lg`/`xl`/`xxl` =
  8/10/12/14/16/18 pt), `+N`/`-N` token deltas, and the
  alias `strikethrough` / `strike` for `overstrike`.
  (e) Bootstrap Icons v1.13.1: 705 fill glyphs + 2,746
  outline glyphs (~3,400 total unique names); outline is
  the default style; the catalog at icons.getbootstrap.com
  matches names one-for-one.
  (f) Theme JSON schema: 9 required top-level fields plus
  `shades` and `semantic` maps. Surface tokens, on-surface
  foregrounds, stroke colors, and the 9-step shade spectrum
  are all auto-derived from the literals — a custom theme
  needs only ~17 hex values plus the semantic map.
  (g) Custom theme registration via
  `register_user_theme(name, path)` and switching via
  `Style().theme_use(name)` works end-to-end, verified at
  runtime with a generated `demo-dark` theme.
- Snippet check: 17 snippets across the 6 pages, 14
  executed, 0 failures. All cross-links resolve.

Earlier session (2026-05-02, capabilities/layout-props.md —
first standalone capabilities page after Icons & Images
closed):

- Full rewrite. Old page was 124 lines of abstract framing
  ("What are layout properties?", "Common layout properties",
  "Container interpretation", "Declarative layout intent",
  "Layout timing", "Interaction with scrolling", "ttkbootstrap
  guidance", "Common pitfalls") that **named no concrete kwargs
  at all** — `side`, `fill`, `expand`, `sticky`, `row`,
  `column`, `relx`, `rely`, `bordermode`, `before`, `after`,
  `in_` were all absent. Same generic-Tk-tutorial shape as the
  rest of the pre-rewrite capabilities pages (signals/index.md,
  layout/index.md, validation/index.md, icons/index.md before
  their rewrites).
- New version is the per-kwarg reference page that ~17 widget /
  layout pages link to (`Layout properties` is the third bullet
  in every layout-widget Reference list — frame.md, packframe.md,
  gridframe.md, scrollview.md, scrollbar.md, accordion.md,
  expander.md, panedwindow.md, separator.md, sizegrip.md,
  labelframe.md, plus `widgets/layout/*.md` siblings, plus the
  capabilities/layout/* pages and the form-widget template). It
  leads with a 3-row at-a-glance table comparing the three
  managers (layout shape / per-call kwargs / container setup
  needed), then per-manager kwarg tables and per-section blurbs:
  `pack` (11 kwargs), `grid` (10 kwargs), `place` (12 kwargs);
  composition rules (single-manager-per-parent, `*_forget` vs
  `grid_remove` table, container-injected defaults from
  PackFrame / GridFrame, method chaining); container-side
  methods (propagate, rowconfigure, columnconfigure, slaves,
  grid_size); a directive cross-link section.
- One real bug surfaced and verified at runtime:
  **`pack_propagate()` and `grid_propagate()` mixin methods
  always return `None` on query.** Cause: the mixin methods at
  `core/capabilities/pack.py:99-111` and
  `core/capabilities/grid.py:112-124` always pass `flag` through
  to `super().pack_propagate(flag)` / `super().grid_propagate(flag)`,
  including when `flag=None`. CPython `tkinter.Misc.pack_propagate`
  / `grid_propagate` distinguish the query path from the setter
  path by a private `['_noarg_']` sentinel — so passing `None`
  dispatches as the setter (a no-op-ish set) and the query path
  is never taken. Verified at runtime: `f.pack_propagate()`
  returns `None` even on a fresh widget where the underlying Tk
  value is `True`. The propagation state itself is preserved
  correctly (the underlying Tcl `pack propagate <w>` reports the
  right value, accessible via
  `widget.tk.call('pack', 'propagate', widget._w)`); only the
  Python-side query is broken. Fix: use a sentinel like
  `_NO_ARG = object()` and conditionally pass `flag` only when
  it's not the sentinel — `if flag is _NO_ARG: return
  super().pack_propagate(); else: super().pack_propagate(flag)`.
  Documented as a `!!! warning` block in Container-side methods
  with the workaround. Added to the bugs list.
- Eight runtime checks performed and documented:
  (1) Default kwargs from `pack_info()`: `side='top'`,
  `fill='none'`, `expand=0`, `anchor='center'`, `padx=0`,
  `pady=0`, `ipadx=0`, `ipady=0`. From `grid_info()`: `row=0`,
  `column=0`, `columnspan=1`, `rowspan=1`, `sticky=''`,
  `padx=0`, `pady=0`, `ipadx=0`, `ipady=0`. From
  `place_info()`: `x='0'`, `y='0'`, `relx='0'`, `rely='0'`,
  `width=''`, `height=''`, `relwidth=''`, `relheight=''`,
  `anchor='nw'`, `bordermode='inside'` — note that the `place`
  size kwargs default to the empty string (not `0`), which Tk
  reads as "use the widget's own requested size."
  (2) Mixing managers raises the documented TclError: `cannot
  use geometry manager grid inside .!frame which already has
  slaves managed by pack` (and vice versa). `place` overlays
  either safely.
  (3) Bad values raise loud TclErrors with descriptive
  messages: `pack(fill='z')` → `bad fill style "z": must be
  none, x, y, or both`; `grid(sticky='z')` → `bad stickyness
  value "z": must be a string containing n, e, s, and/or w`;
  `pack(side='center')` → `bad side "center": must be top,
  bottom, left, or right`; `place(bordermode='z')` → `bad
  bordermode "z": must be inside, outside, or ignore`.
  (4) `expand=` normalization at the Tk boundary: `True`/`1`/
  `'yes'`/`'true'` → `1`; `False`/`0`/`'no'`/`'false'` → `0`.
  Verified all eight value forms.
  (5) `sticky=` accepts a string of n/s/e/w (any combination,
  any order), a tuple of those letters, or a comma-separated
  string. All three forms (`'wsen'`, `('n','s','e','w')`,
  `'n,s,e,w'`) round-trip via `grid_info()` to the canonical
  `'nesw'`.
  (6) `winfo_manager()` reports `''` (empty) before any
  geometry call, the manager name afterwards, and reverts to
  `''` after `pack_forget()` / `grid_forget()` / `place_forget()`.
  Switching managers on a single widget is supported (last call
  wins); the previous manager's info is gone.
  (7) `*_forget` vs `grid_remove`: `pack_forget()` makes
  `pack_info()` raise `TclError: window ".!label" isn't packed`;
  `grid_forget()` makes `grid_info()` return `{}`;
  `place_forget()` makes `place_info()` return `{}`;
  `grid_remove()` is the only one that *preserves* the
  configuration for a later `widget.grid()` no-arg restore.
  Verified `grid_remove()` round-trip with `row=2, column=3,
  sticky='nsew', padx=5` — all four kwargs persist through
  the remove → re-grid cycle.
  (8) `grid_size()` reports the bounding box of cells *that
  have children* (or have been configured). A fresh Frame
  reports `(0, 0)`; after a single `grid(row=2, column=3)` it
  reports `(4, 3)` — implicit zero-size placeholders fill the
  rest. The `pack(before=widget)` / `pack(after=widget)`
  ordering also verified at runtime — three labels A, B, C
  added with `c.pack(before=b)` give `pack_slaves()` order
  `['A', 'C', 'B']`.
- Snippet check: 10 snippets, 1 executed, 0 failures. All 5
  cross-links resolve (siblings: `layout/index.md`,
  `layout/containers.md`, `layout/spacing.md`; platform:
  `geometry-and-layout.md`, `widget-lifecycle.md`).
- **Capabilities sweep: 17/18 done.** Remaining:
  `state-and-interaction.md`, `localization.md`.

Earlier session (2026-05-02, capabilities/icons/images.md —
final Icons & Images page, sub-section closed 3/3):

- Full rewrite. Old page was 144 lines of abstract framing
  ("Images as shared resources", "Image lifetime
  management", "Image caching", "DPI awareness", "Image
  formats", "Images and styling", "Performance
  considerations", "ttkbootstrap guidance", "Common
  pitfalls") with **zero references to the actual `Image`
  API**. The four constructors (`open` / `from_pil` /
  `from_bytes` / `transparent`), the cache management
  surface (`cache_info` / `clear_cache` / `get_cached` /
  `set_cached`), the per-method default cache keys, the
  `key=` override, and `ImageCacheInfo` were all absent.
- New version is the spec page for the `Image` utility (the
  `index.md` covers the surface; this page goes deeper). It
  leads with an 8-row at-a-glance table covering the four
  constructors plus the four cache-management methods, then
  per-section blurbs: constructing images (Pillow's role,
  what gets returned, format support); cache identity (the
  four default key shapes with the rationale for each, and
  worked examples of the `key=` override for
  versioning / cross-source identity / set_cached stash);
  cache lifetime (`cache_info` / `clear_cache` / `get_cached` /
  `set_cached` semantics, `ImageCacheInfo` is a frozen
  dataclass); the GC contract as a `!!! danger` block (with
  the runtime-verified failure mode of `clear_cache` while
  widgets are alive); the pinning idiom (raw-Tk
  attribute-pin pattern vs `Image.*` automatic pinning);
  when `Image` is the wrong tool (Bootstrap icons,
  state-aware imagery, throwaway raster).
- Eight runtime checks performed and documented:
  (1) Default cache keys: `Image.transparent(16, 16)` returns
  the same object on second call; `Image.transparent(32, 32)`
  is a separate slot. `Image.cache_info().items` reflects
  the count; `Image.clear_cache()` zeroes it.
  (2) `Image.from_pil(pil_a)` and `Image.from_pil(pil_a.copy())`
  produce **different** PhotoImage objects — `from_pil` keys by
  `id(image)`, so PIL copies bypass the cache. Documented as
  expected behavior; the alternative (content-hashing every PIL
  image) would be expensive.
  (3) `Image.from_bytes(data)` keys by `md5(data)` hex digest;
  identical byte sequences hit the same slot regardless of
  source.
  (4) `Image.set_cached(key, img)` returns `img` (chainable);
  `Image.get_cached(missing_key)` returns `None`.
  (5) **`Image` is exported at `ttk.Image`** (verified
  `ttk.Image is core.images.Image`). Re-exported from
  `ttkbootstrap.api.utils`.
  (6) **`ImageCacheInfo` is a frozen dataclass** — verified
  `info.items = 99` raises `FrozenInstanceError`. Future
  versions can add hit/miss counters without breaking
  callers; the page tells readers to rely on the field name,
  not the order or count.
  (7) **The GC contract: `clear_cache()` while a widget
  displays a cached image breaks the widget.** Verified at
  runtime — `Image.transparent(20, 20)` referenced by a Label
  via `image=img`, then `Image.clear_cache()` + `gc.collect()`
  + `update_idletasks()` results in `app.tk.call('image',
  'type', tcl_image_name)` raising
  `TclError: image "(...)" doesn't exist`. The widget retains
  the Tcl image *name* on its `image=` config but no Python
  reference to the `PhotoImage` object — once the cache is
  the last strong ref and gets dropped, the Python finalizer
  destroys the `PhotoImage` which destroys the underlying Tcl
  image, and the widget goes blank with no exception. This
  isn't a bug — it's the documented contract — but it's the
  only failure mode a caller can plausibly trigger, so the
  `!!! danger` block leads with a runtime-verified example
  and the recommended scoping pattern (clear after window
  destruction, never while it's open).
  (8) Cache key form for `Image.open` is
  `('file', resolved_absolute_path)` — `Path(p).expanduser()
  .resolve()` is called once at the top of `open`, so
  `'logo.png'`, `'./logo.png'`, and `'~/proj/logo.png'`
  collapse to the same slot when they resolve to the same
  file.
- No new bugs surfaced. The `Image` utility is a small,
  self-contained module (`core/images.py`, 284 lines); the
  surface is correct and the contracts match the
  implementation. The behaviors that *could* surprise users
  (`from_pil` not content-hashing; `clear_cache` breaking
  live widgets) are documented contracts rather than bugs —
  the alternative implementations would be worse (expensive
  hashing, reference cycles, or per-widget weakref
  bookkeeping that defeats the whole point of caching).
- Snippet check: 6 snippets, 5 executed, 0 failures. Block
  with `tk.PhotoImage(file='logo.png')` was changed to
  `tk.PhotoImage(width=20, height=20)` because raw Tk's
  file-not-found path raises `_tkinter.TclError`, not
  `FileNotFoundError`, so it bypasses the snippet runner's
  acceptable-error whitelist. The `Image.open('logo.png')`
  example is fine — PIL raises `FileNotFoundError` which the
  whitelist accepts. All 4 cross-links resolve (siblings:
  `index.md`, `icons.md`; platform: `images-and-dpi.md`;
  guides: `icons.md`).
- **Capabilities sweep: 16/18 done.** Icons & Images
  sub-section closed (3/3). Remaining: `layout-props.md`,
  `state-and-interaction.md`, `localization.md`.

Earlier session (2026-05-02, capabilities/icons/icons.md —
2/3 in Icons & Images sub-section):

- Targeted accuracy pass — page was already structurally
  sound (Provider resolution / State integration /
  Theme-driven coloring / DPI scaling / Caching arc; real
  TTK state expressions; bug-list cross-reference for the
  theme-token PIL crash). Three precision items fixed
  vs the prior version, all surfaced by runtime checks:
  (1) **`cget('icon')` does not return the normalized
  dict** — it returns the *original* dict the user passed.
  Verified: `Button(icon={'name': 'gear'}).cget('icon')`
  returns `{'name': 'gear'}` (no `size` key added);
  `Button(icon={'name': 'gear', 'size': 24}).cget('icon')`
  returns `{'name': 'gear', 'size': 24}` (size NOT
  DPI-scaled at the cget boundary). The DPI scaling and
  default-size injection happen inside
  `map_stateful_icons` on the spec passed to
  `_image_for`, not on the stored config. Reworded the
  Theme-driven coloring section's cget claim.
  (2) **`_TtkBootstrapIconProvider`'s `y_bias=0.02`
  matches the `BootstrapFontProvider` default** (verified:
  both `_TtkBootstrapIconProvider().y_bias` and
  `BootstrapFontProvider().y_bias` return 0.02). The
  source comment at `style/bootstyle_builder_base.py:24-25`
  claims "ttkbootstrap buttons need y_bias=0.08 for proper
  vertical alignment of icons with text" but the constant
  `_ICON_Y_BIAS = 0.02` contradicts that comment — looks
  like an incomplete refactor. Either way, the page now
  describes the provider as bypassing
  `BootstrapFontProvider.__init__` to call
  `BaseFontProvider.__init__` directly so the framework
  can pin `y_bias` / `default_style` / `styles`
  explicitly, and notes that the pinned 0.02 matches the
  upstream default rather than overriding it. (Not added
  to the bugs list — the source comment vs. constant
  divergence is a code-comment cleanup, not a behavior
  bug.)
  (3) **The "two widgets do not share a `PhotoImage`"
  framing in the Caching section was misleading.** Two
  widgets with identical accent / variant / `style_options`
  / icon resolve to the same `bs[<hash>].…` style key,
  which is registered with ttk once — so they share the
  ttk style entry's image element at the ttk layer.
  Verified: `Button(text='1', icon='star')` and
  `Button(text='2', icon='star')` both resolve to
  `bs[1e950e80].Solid.TButton`. Reworded to lead with
  ttk-style-layer sharing as the primary mechanism, with
  the per-call PhotoImage cache framed as
  within-rebuild deduplication, not a cross-widget
  contract.
- All five existing claims that *were* accurate held up
  under runtime checks: provider lazy-init pattern (verified
  `b._icon_provider_initialized` flips False → True after
  the first icon-bearing widget renders), the
  `name='empty'` short-circuit (returns a transparent
  PhotoImage skipping the provider), the `_match_override`
  token-vs-exact form table, the `_derive_expr` token
  derivations (`'hover'` → `'hover !disabled'`,
  `'pressed'` → `'pressed !disabled'`,
  `'selected'` → `'selected !disabled'`), and the
  `Style().style_builder.color('primary')` workaround for
  the theme-token bug (verified: `→ '#4D76F6'`).
- Snippet check: 4 snippets, 4 executed, 0 failures. All
  cross-links resolve (siblings: `index.md`, `images.md`;
  platform: `images-and-dpi.md`; guides: `icons.md`;
  design system: `icons.md`).
- **Icons & Images sub-section status: 2/3** —
  `index.md` and `icons.md` done. Next page in the sweep:
  `capabilities/icons/images.md`.

Earlier session (2026-05-02, capabilities/icons/index.md —
opens Icons & Images sub-section, 1/3):

- Full rewrite. Old page was 107 lines of abstract framing
  ("Icons vs images", "Icons as a capability", "Images as a
  capability", "Relationship to styling", "Performance
  considerations", "ttkbootstrap guidance", "Common pitfalls")
  with **zero references to the actual API surface** —
  `BootstrapIcon`, `IconSpec`, `Image`, the `icon=` widget kwarg,
  the `IconMixin` primitives, the per-state override path were
  all absent. Same generic-Tk-tutorial shape as the rest of the
  pre-rewrite signals/layout/validation pages.
- New version leads with the three concrete pieces of API users
  actually touch (`BootstrapIcon` / `IconSpec` / `Image`) in a
  4-row at-a-glance table, then per-section blurbs naming the
  five `IconMixin` primitives (`Button`, `Label`, `CheckButton`,
  `RadioButton`, `MenuButton`) and the ~15 composites that
  forward `icon=` to one of those primitives or to their own
  internal renderer.
- One real bug surfaced and verified at runtime:
  **theme tokens like `'primary'` crash when supplied as
  `IconSpec.color`** (or in a per-state override's `color`).
  Cause: `_image_for` at
  `style/bootstyle_builder_base.py:684` calls
  `BootstrapIcon(name=name, size=size, color=color)` directly
  without resolving the token through `self.color(...)` — so
  PIL receives the literal string `'primary'` and raises
  `ValueError: unknown color specifier: 'primary'` from
  `PIL/ImageColor.py:125`. Verified at runtime:
  `Button(icon={'name': 'star', 'color': 'primary'})` →
  ValueError. The path that DOES work for users today is to
  **omit `color`** entirely — when omitted, the icon inherits
  the widget's foreground state map (already resolved to hex
  values by the style builder before being handed to
  `_image_for` via `foreground_spec`). Hex strings (`'#ff6600'`)
  and PIL named colors (`'red'`, `'navy'`) also work directly.
  Documented as a `!!! danger` block in the BootstrapIcon
  section with the resolve-yourself workaround
  (`app.style.builder.color('primary')` to convert to hex
  first). Added to the bugs list. Worth fixing — the
  natural user expectation is that theme tokens work
  everywhere they appear in widget kwargs.
- Documented (some new, some restated): the `IconSpec`
  TypedDict shape (`name` / `size` / `color` / `state`) at
  `style/bootstyle_builder_base.py:68`; the per-state override
  shape (`IconStateMap` with `name` and/or `color`); ttk
  state-expression syntax (`'disabled'`, `'hover !disabled'`,
  `'pressed !disabled'`, `'selected'`); the
  `cget` round-trip behavior for `icon=` (string returns
  string, dict returns normalized dict); the recommended
  no-color path that inherits the widget's foreground; the
  `icon_only=True` companion option from `IconMixin`; the
  reconfigurable-at-runtime nature of both options; the
  five-method `Image` surface (`open` / `from_pil` /
  `from_bytes` / `transparent` plus `cache_info` /
  `clear_cache` / `get_cached` / `set_cached`); the cache-key
  scheme per method; the `key=` override for explicit
  versioning; the connection back to the platform-level
  pinning gotcha (Image.* keeps its own strong references so
  callers don't have to).
- Snippet check: 3 snippets, 3 executed, 0 failures. All 8
  cross-links resolve (siblings: `icons.md`, `images.md`;
  platform: `images-and-dpi.md`; guides: `icons.md`; design
  system: `icons.md`). The "Where to read next" closer is the
  same directive-cross-link shape established in the validation
  and layout sub-sections.
- **Icons & Images sub-section status: 1/3** — `index.md` done.
  Next pages in the sweep: `capabilities/icons/icons.md`, then
  `capabilities/icons/images.md`. Note that the existing
  `icons.md` is **already much closer to the rewrite shape**
  than other pre-rewrite capabilities pages — it leads with a
  Provider resolution / State integration / Theme-driven
  coloring / DPI scaling / Caching arc and references real
  TTK state expressions. Likely a targeted accuracy pass
  rather than a full rewrite, with verification of the
  provider-priority claim (and the just-surfaced theme-token
  bug should be cross-referenced there).

Earlier session (2026-05-02, capabilities/validation/results.md —
final Validation page, sub-section closed 3/3):

- Full rewrite. Old page was 137 lines of abstract framing
  ("What is a validation result?", "Valid vs invalid vs warning",
  "Aggregating results", "Driving UI feedback", "Relationship
  to widgets", "Integration with signals", "Timing and user
  experience", "ttkbootstrap guidance", "Common pitfalls") with
  zero references to the actual `ValidationResult` API —
  hallucinated a `'warning'` severity level, multi-message lists,
  and aggregation features that do not exist on the object. Same
  pre-rewrite shape as the rest of the validation/layout/signals
  pages.
- New version leads with the actual two-attribute surface
  (`is_valid: bool`, `message: str`) in a 2-row at-a-glance table
  and states explicitly that's the entire surface — no severity,
  no multi-message, no rule reference, no contextual data, no
  `__eq__`, no `__repr__`, no `__hash__`. Per-section blurbs:
  constructing a result, reading the fields, the result vs event
  payload distinction, where the result appears, what's not here,
  standalone use, where to read next.
- Two findings worth surfacing (one new bug, one reframing of an
  existing API claim):
  (1) **`bool(ValidationResult(False))` is `True`.** No
  `__bool__` override exists on the class
  (`core/validation/validation_result.py` is 23 lines, no dunder
  methods). Net effect: `if rule.validate(value): ...` is a silent
  always-truthy footgun. Verified at runtime. The framework
  itself does not hit this — `ValidationRule.validate()` and
  `ValidationMixin.validate()` access `result.is_valid` explicitly
  — but standalone-use callers can. Documented as a `!!! danger`
  block in Reading the result with the correct usage.
  (2) **`ValidationMixin.validate()`'s docstring at
  `widgets/mixins/validation_mixin.py:99-100` claims the return
  is "True if validation was performed (regardless of result)".**
  The actual return semantics are: returns `True` only when at
  least one rule ran AND every rule passed; returns `False` on the
  first invalid result and on the no-rules case (the early-return
  at line 117 plus the `return ran_rule` at line 124, which
  short-circuits on first failure before flipping ran_rule's
  meaning). Verified at runtime: `inner.validate('Alice', trigger=
  'manual')` → True (passed); `inner.validate('', trigger=
  'manual')` → False (failed). Documented as a `!!! warning` in
  Where the result appears; added to the bugs list as a docstring
  fix (the implementation is more useful than the docstring; fix
  the docstring).
- Surfaced the central distinction between `ValidationResult`
  (returned by `ValidationRule.validate()`, the only place users
  see the object) and the **event payload `dict`** (`{value,
  is_valid, message}` delivered by `<<Valid>>` / `<<Invalid>>` /
  `<<Validate>>` and to the `on_valid` / `on_invalid` /
  `on_validated` helpers). The conversion happens in
  `ValidationMixin.validate` at lines 103-122 — read the result's
  `.is_valid` and `.message` fields, pack into a dict, emit. So
  handlers reading `event.data` always get a dict, never a
  `ValidationResult`. Same pattern in `Form.validate()`. This was
  already documented on `index.md` and `rules.md` as the event
  payload shape, but never connected back to "the result object
  itself never reaches the event handler" — added a
  Result vs event payload section that names this explicitly.
- One subtle public-surface fact worth noting: **`ValidationResult`
  is mutable and accepts `is_valid=True` with a non-empty
  message**. Verified at runtime. The framework never produces
  that shape (`_default_message()` is consulted only on failure)
  and the public flow expects an immutable carrier, but the
  attribute setters are not protected. Documented in
  Constructing a result as a behavioral note rather than a bug —
  the contract is clear from the attribute table.
- Snippet check: 8 snippets, 0 executed, 0 failures. All 9
  cross-links resolve (siblings: `rules.md`, `index.md`;
  callbacks: `signals/callbacks.md`; widgets:
  `dialogs/formdialog.md`, `inputs/textentry.md`,
  `inputs/numericentry.md`, `inputs/dateentry.md`,
  `inputs/spinnerentry.md`, `inputs/selectbox.md`). The
  in-page anchor `index.md#reading-the-result` and
  `rules.md#messages` both verified against the section
  headings.
- **Validation sub-section is now complete** (3/3 pages done in
  nav order: `index.md`, `rules.md`, `results.md`). Note:
  `rules.md` was already shipped on this branch in commit
  `d9202b4`; the prior handoff was stale. Next sub-section in
  the sweep: Icons & Images (3 pages — `icons/index.md`,
  `icons/icons.md`, `icons/images.md`).

Earlier session (2026-05-02, capabilities/validation/index.md —
opens Validation sub-section, 1/3):

- Full rewrite. Old page was 121 lines of abstract framing
  ("What is validation?", "Validation as a capability",
  "Rules and results", "Timing and lifecycle", "Relationship
  to signals and callbacks", "UI feedback", "ttkbootstrap
  guidance", "Common pitfalls") with zero references to
  ttkbootstrap's actual validation surface — no
  `ValidationRule`, no `ValidationResult`, no `add_validation_rule`,
  no `<<Valid>>`/`<<Invalid>>`/`<<Validate>>`, no `Form.validate()`,
  no `required=True` shortcut. Same pre-rewrite shape as the
  signals/layout pages.
- New version leads with a 4-row at-a-glance table covering the
  full surface (`ValidationRule` / `ValidationResult` /
  `ValidationMixin` / `Form.validate()`) across (where it lives /
  what it does). Then per-section blurbs: adding a rule (with
  the `required=True` constructor shortcut and the
  `add_validation_rules([...])` replace-list path); when rules
  fire (the 5-row trigger-defaults table, plus the 50ms debounce
  fact and the manual-trigger escape hatch); reading the result
  (the 3-row events table noting the `<<Validate>>` event /
  `on_validated` helper name asymmetry, and the dict-payload
  divergence from the rest of the on_* helpers); form-level
  validation; "what's not here" (no async, no cross-field, no
  `compare`, `min`/`max` only); directive cross-link section
  with 5 questions.
- Two bugs surfaced and verified at runtime, both new:
  (1) **`ValidationRule('compare')` is a silent no-op.** The
  `RuleType` literal at `core/validation/types.py:4` lists
  `'compare'` as a supported rule type, but `ValidationRule.validate()`
  (`core/validation/validation_rules.py:48-86`) has no `elif self.type
  == 'compare'` branch — so `ValidationRule('compare').validate('anything')`
  returns `is_valid=True` for any input. Either implement the
  rule (presumably comparing against a reference value passed in
  `params`) or remove `'compare'` from the Literal so callers get
  a static-type error. Documented as a "What's not here" bullet
  on the page; added to the bugs list.
  (2) **`stringLength` accepts `min`/`max`, not `min_length`/`max_length`.**
  The `ValidationMixin.add_validation_rule` docstring at
  `widgets/mixins/validation_mixin.py:78` shows `min_length=5`
  as the example kwarg, but `ValidationRule.validate` reads
  `params.get("min", 0)` and `params.get("max", float("inf"))`
  (`validation_rules.py:73-74`). `min_length`/`max_length`
  are silently swallowed into `params` and never read; the
  rule falls back to its default range and accepts everything.
  Verified at runtime:
  `ValidationRule('stringLength', min=5).validate('abc').is_valid`
  → `False`; `ValidationRule('stringLength', min_length=5).validate('abc').is_valid`
  → `True`. Either fix the docstring example to `min=`/`max=` or
  accept both spellings in `validate()`. Added to the bugs list.
- Verified the on_valid/on_invalid/on_validated callback shape
  at runtime — they receive the **payload dict directly** (not
  a Tk event with `.data`), confirming the asymmetry already on
  the bugs list and now documented as a "deliberate divergence"
  in the page.
- Snippet check: 6 snippets, 1 executed, 0 failures. All 8
  cross-links resolve (siblings: `rules.md`, `results.md`;
  callbacks: `signals/callbacks.md`; widgets:
  `dialogs/formdialog.md`, `inputs/textentry.md`,
  `inputs/numericentry.md`, `inputs/dateentry.md`,
  `inputs/spinnerentry.md`).
- **Validation sub-section status: 1/3** — `index.md` done.
  Next pages in the sweep: `capabilities/validation/rules.md`,
  then `capabilities/validation/results.md`.

Earlier session (2026-05-02, capabilities/layout/scrolling.md —
final layout page, sub-section closed 4/4):

- Full rewrite. Old page was 124 lines of abstract framing
  ("Scrolling as a layout concern", "Scrollable containers",
  "Content size and updates", "Vertical and horizontal
  scrolling", "Mouse wheel handling", "Performance
  considerations", "ttkbootstrap guidance", "Common pitfalls")
  with zero references to ttkbootstrap's actual scrolling
  surface — no `ScrollView`, no `Scrollbar`, no
  `xscrollcommand`/`yscrollcommand` protocol, no
  `scroll_direction`, no `scrollbar_visibility`, no
  `ScrolledText`. Same generic-Tk-tutorial shape as the other
  pre-rewrite layout pages.
- New version leads with a 3-row at-a-glance table covering the
  three scroll-path categories (built-in widget scrolling /
  ScrollView for arbitrary widget trees / pre-bundled
  composites). Then per-section blurbs: the two-way scrollbar
  protocol (`command=` + `xscrollcommand=`/`yscrollcommand=`)
  with the central "wiring only one half breaks one direction
  silently" axiom; ScrollView mechanics with the four
  framework-specific gotchas (parent-on-`sv.canvas` not `sv`;
  auto scrollregion via `<Configure>`; per-instance bindtag
  for normalized mousewheel; gutter reservation in `hover` and
  `scroll` modes); pre-bundled scrollers; choosing an axis;
  pitfalls.
- All claims grounded in either the prior `scrollview.md`
  sweep notes (verified at runtime in that session) or
  on-page source reads — no new runtime verification needed
  this session because ScrollView's behavior was already
  tested thoroughly during the widgets sweep. The new content
  rephrases that knowledge for the capabilities-page audience
  (who arrived from the layout-overview path, not the widget
  page) and emphasizes the protocol contract and choosing-
  the-right-path framing.
- Snippet check: 2 snippets, 2 executed, 0 failures. All 9
  cross-links resolve (siblings: `containers.md`; widgets:
  `scrollview.md`, `scrollbar.md`, `scrolledtext.md`,
  `tableview.md`, `treeview.md`, `listview.md`,
  `canvas.md`; platform: `events-and-bindings.md`).
- **Layout sub-section is now complete** (4/4 pages done in
  nav order). Next sub-section in the sweep: Validation
  (3 pages — `validation/index.md`, `validation/rules.md`,
  `validation/results.md`).

Earlier session (2026-05-01, capabilities/layout/spacing.md):

- Full rewrite. Old page was 122 lines of abstract framing
  ("Types of spacing", "Padding vs margins", "Consistent
  spacing", "Spacing and resizing", "Vertical vs horizontal
  spacing", "Responsive considerations", "ttkbootstrap
  guidance", "Common pitfalls") with **zero references to
  ttkbootstrap's actual spacing options** — no `padding=`,
  no `padx`/`pady`, no `ipadx`/`ipady`, no `gap=`, no
  `density=`. Same generic-Tk-tutorial shape as the
  pre-rewrite `signals/index.md` /
  `signals/callbacks.md` / `signals/virtual-events.md` /
  `layout/index.md` / `layout/containers.md`.
- New version leads with a 5-row at-a-glance table covering
  every spacing knob in the framework (`padding=` / `padx`+
  `pady` / `ipadx`+`ipady` / `gap=` / `density=`) across
  (where it lives / what it does / accepted by). Per-knob
  blurbs name the actual API surface. Closes with a
  composition-rules section explaining how the five knobs
  interact at the parent/child boundary, and a directive
  cross-link section.
- Six concrete claims and behaviors verified at runtime:
  (1) `padding=` accepts three shapes: int (all four sides),
  2-tuple `(h, v)`, 4-tuple `(l, t, r, b)`. Verified on
  `Frame(app, padding=10)` → `cget('padding') == (10,)`,
  `padding=(10, 20)` → `(10, 20)`, `padding=(5, 10, 15, 20)`
  → `(5, 10, 15, 20)`.
  (2) `PackFrame` injects gap as **leading** `padx`/`pady` on
  the second-and-later children only. Verified at runtime
  with `direction='vertical', gap=8` and three buttons:
  first button `pady=0`, others `pady=(8, 0)`. Same shape
  in horizontal mode (`padx=(N, 0)`).
  (3) `GridFrame` injects gap as leading `padx` on column ≥ 1
  and leading `pady` on row ≥ 1. The `(0, 0)` cell receives
  no gap injection. Verified at runtime with `columns=3,
  gap=10` and 5 buttons: cell `(0, 0)` → `padx=0, pady=0`;
  cell `(0, 1)` → `padx=(10, 0), pady=0`; cell `(1, 1)` →
  `padx=(10, 0), pady=(10, 0)`.
  (4) `GridFrame` **merges** user `padx=N` with the gap
  rather than replacing. Verified at runtime: with `gap=10`
  and a per-call `padx=4`, cell `(0, 0)` reaches the cell as
  `4` unchanged (no gap injection); cell `(0, 1)` reaches as
  `(14, 4)` — leading edge sums to 14, trailing edge stays
  4. The merge function is `_merge_padding`
  (`widgets/primitives/gridframe.py:274-283`).
  (5) `density='compact'` swaps three things at once: the
  font (`body` → `caption`, ~13 pt → ~11 pt on macOS), the
  button padding (scaled `(8, 0)` → `(6, 5, 6, 3)` — extra
  top padding to center text in the smaller row), and the
  field height (33 px → 26 px scaled). Helpers: `button_font`
  / `button_padding` / `field_height` /
  `normalize_button_density` at
  `style/builders/utils.py:152-329`. Verified: a default
  TextEntry has `winfo_reqheight()=42`, a compact one
  `winfo_reqheight()=33`.
  (6) `density=` is **not universal**. Surface-tested 12
  classes:
    - Accepts: `Button`, `MenuButton`, `OptionMenu`,
      `CheckToggle`, `RadioToggle`, `Toolbar`, `TextEntry`,
      `Spinbox`, `Combobox`, `Label`, `TreeView`.
    - Rejects with `TclError: unknown option "-density"`:
      `Frame`, `Card`, `LabelFrame`, `PackFrame`,
      `GridFrame`, `CheckButton`, `RadioButton`, `Switch`,
      `Tabs`, `SideNav`, `PageStack`.
  Cross-referenced the existing density-reconfigure bug
  already on the bugs list (Entry / Combobox / Spinbox —
  `configure(density=…)` updates only the font, not the
  resolved ttk style key, so the underlying image element
  height persists).
- One framing fix worth carrying forward: there is **no
  widget-level margin option** in Tk. What CSS calls "margin"
  is expressed from the parent's side via `padx`/`pady` on
  the child's `pack()` / `grid()` call — the page leads with
  that distinction so readers don't search for a non-existent
  `margin=` kwarg.
- Snippet check: 7 snippets, 7 executed, 0 failures. All
  cross-links resolve (siblings: `index.md`, `containers.md`,
  `scrolling.md`; parent: `../layout-props.md`; widget:
  `../../widgets/layout/gridframe.md`; platform:
  `geometry-and-layout.md`, `widget-lifecycle.md`).
- **Layout sub-section status: 3/4** — `index.md`,
  `containers.md`, and `spacing.md` done. Next page in the
  sweep: `capabilities/layout/scrolling.md`.

Earlier session (2026-05-01, capabilities/layout/containers.md):

- Full rewrite. Old page was 163 lines of abstract framing
  ("What is a container?", "Container ownership and layout
  context", "Single responsibility", "Composition over per-widget
  tuning", "Nested containers", "Common pitfalls") — same generic
  Tk-tutorial shape as pre-rewrite `signals/index.md` /
  `signals/callbacks.md` / `signals/virtual-events.md` /
  `layout/index.md`. Almost no references to ttkbootstrap's
  actual container surface (PackFrame, GridFrame, ScrollView
  mentioned briefly; LabelFrame / Card / PanedWindow / Accordion
  / Expander / Notebook / TabView / PageStack absent).
- New version leads with a 12-row at-a-glance table covering
  every container in the framework across (role / primary API /
  geometry policy). Three categories called out explicitly: passive
  (Frame / Card / LabelFrame), opinionated (PackFrame /
  GridFrame), specialized (ScrollView / PanedWindow / Accordion /
  Expander / Notebook / TabView / PageStack). Per-section blurbs
  with code examples lifted from the matching widget pages.
- Three concrete claims and behaviors verified at runtime:
  (1) Frame's `_refresh_descendant_surfaces` hook
  (`widgets/primitives/frame.py:110`) walks every descendant
  whose `_surface` matches the OLD surface and retints them on
  `configure_style_options(surface=…)`. `input_background`
  cascades the same way through
  `_refresh_descendant_input_backgrounds`. Documented as the
  "Surfaces cascade" section, including the exclude-explicit-pin
  rule (descendants with `_style_options['surface']` set are
  excluded).
  (2) The cascade-divergence on LabelFrame is restated from the
  bugs list: LabelFrame does NOT subclass Frame, so children
  inside a LabelFrame keep their old surface when the LabelFrame's
  surface changes. The TypedDict comparison confirms this — the
  three classes carry different kwarg surfaces (Frame includes
  `input_background` and `show_border`; Card omits
  `input_background`; LabelFrame omits both `input_background`
  and `show_border`, plus adds `text` / `labelanchor` /
  `relief` / `borderwidth` / `localize`).
  (3) The "geometry managers don't mix" claim restated from the
  layout/index.md sweep, with the verified Tk error text — the
  same `cannot use geometry manager grid inside .!frame which
  already has slaves managed by pack` message. `place` overlays
  pack OR grid safely (verified).
- LabelFrame `show_border=False` raises `TclError: unknown option
  "-show_border"` — confirmed at runtime; already on the bugs
  list. Card defaults verified: `_surface='card'`, `_accent='card'`,
  `padding=(16,)`, `style_options={'show_border': True, 'surface':
  'card'}`.
- Snippet check: 7 snippets, 7 executed, 0 failures. All 20
  cross-links resolve (siblings: `index.md`, `spacing.md`,
  `scrolling.md`; parent: `../layout-props.md`; platform:
  `geometry-and-layout.md`, `widget-lifecycle.md`; widgets:
  `frame.md`, `card.md`, `labelframe.md`, `packframe.md`,
  `gridframe.md`, `scrollview.md`, `panedwindow.md`,
  `accordion.md`, `expander.md`, `notebook.md`, `tabview.md`,
  `pagestack.md`, `appshell.md`, `toolbar.md`).
- **Layout sub-section status: 2/4** — `index.md` and
  `containers.md` done. Next pages in the sweep:
  `capabilities/layout/spacing.md`, then
  `capabilities/layout/scrolling.md`.

Earlier session (2026-05-01, capabilities/layout/index.md):

- Full rewrite. Old page was 122 lines of abstract framing
  ("Layout as a capability", "Geometry managers", "Container
  responsibility", "Declarative intent", "Scrolling as layout",
  "Common pitfalls") with zero references to ttkbootstrap's
  actual API surface — no `PackFrame`, no `GridFrame`, no
  `ScrollView`, no concrete kwargs. Same generic-Tk-tutorial
  shape as pre-rewrite `signals/index.md`, `signals/callbacks.md`,
  and `signals/virtual-events.md`.
- New version leads with a 6-column at-a-glance table comparing
  `pack` / `grid` / `place` / `PackFrame` / `GridFrame` /
  `ScrollView` across (layout shape / per-child kwargs /
  container kwargs / mixing in one parent / best for). Then
  per-mechanism blurbs that name the actual API
  (`PackFrame(direction=, gap=, fill_items=, expand_items=,
  anchor_items=)`, `GridFrame(rows=, columns=, gap=,
  sticky_items=, auto_flow=)`, `ScrollView(scroll_direction=,
  scrollbar_visibility=)`) and code examples lifted from the
  matching widget pages. Closes with a "Containers vs widgets"
  framing (parent owns layout policy; child requests size and
  passes per-call kwargs) and a directive 8-question
  cross-link section.
- Three concrete claims verified at runtime:
  (1) `pack` and `grid` cannot be mixed in the same parent —
  Tk raises `_tkinter.TclError: cannot use geometry manager
  grid inside .!frame which already has slaves managed by pack`
  (and vice versa). `place` overlays either safely.
  (2) Container defaults: `Frame` → `padding=''` (Tcl empty),
  `_surface='content'`; `PackFrame` → `direction='vertical'`,
  `gap=0`; `GridFrame` → `_num_columns=100` (placeholder when
  no columns passed), `_num_rows=100`, `_gap=(0, 0)`,
  `_auto_flow='row'`; `ScrollView` → `scroll_direction='both'`,
  `scrollbar_visibility='always'`. (Note: ScrollView's default
  `scrollbar_visibility='always'` matches the correction
  surfaced in the prior `scrolledtext.md` sweep — old guides
  said `'scroll'`.)
  (3) All twelve top-level layout exports resolve at
  `ttkbootstrap.<Name>`: Frame, PackFrame, GridFrame,
  ScrollView, PanedWindow, LabelFrame, Card, Accordion,
  Expander, Separator, SizeGrip, Scrollbar.
- Snippet check: 4 snippets, 1 executed, 0 failures. All 12
  cross-links resolve (siblings: `containers.md`, `spacing.md`,
  `scrolling.md`; parent: `../layout-props.md`; platform:
  `geometry-and-layout.md`, `widget-lifecycle.md`; widgets:
  `packframe.md`, `gridframe.md`, `scrollview.md`,
  `panedwindow.md`, `contextmenu.md`, `tooltip.md`).
- **Layout sub-section status: 1/4** — `index.md` done. Next
  pages in the sweep: `capabilities/layout/containers.md`,
  `capabilities/layout/spacing.md`,
  `capabilities/layout/scrolling.md`.

Earlier session (2026-05-01, capabilities/signals/virtual-events.md):

- Full rewrite. Old page was 150 lines of abstract framing
  ("What is a virtual event?", "Why virtual events exist",
  "Generating virtual events", "Naming conventions", "Common
  pitfalls") that **never named a single concrete event the framework
  emits**. Read like a generic Tk tutorial — same shape as the
  pre-rewrite `signals/index.md` and `signals/callbacks.md`.
- New version leads with two ttkbootstrap-specific extensions over
  stock Tk: (a) arbitrary Python payloads on `event.data` (stock Tcl
  forces strings), (b) the framework's emitted-events naming
  convention. Then per-section coverage of subscribing
  (`bind` + `add="+"`), emitting (`event_generate(seq, data=...)`,
  `when=now/tail` semantics), the no-bubble axiom with the bug-list
  table of false-bubble claims (Tabs, TabView, SideNav, PageStack,
  SelectBox), framework-emitted events as four scoped tables
  (cross-cutting / selection / lifecycle-and-navigation /
  widget-specific), Tk's stock virtual events (clipboard /
  navigation), naming conventions, and pitfalls.
- Six concrete behaviors verified at runtime, several worth noting
  for the cross-section:
  (1) **Default `when="now"` fires synchronously**, inline in the
  `event_generate` call. `when="tail"` queues to the regular event
  queue (drained by `update()`, NOT `update_idletasks`). Verified:
  with `event_generate("<<X>>", when="tail")` then a list-append
  after the call, ordering is `['after gen', ..., 'handler']` only
  after `app.update()`. The framework's `MessageCatalog.locale()`
  uses `when="tail"` deliberately so it can emit
  `<<LocaleChanged>>` without re-entering the dispatch loop
  mid-callback.
  (2) **Generating an unbound virtual event is silent** — no
  exception, no warning. This is how the framework emits
  `<<Selected>>` on every selection-aware widget without forcing
  every host to register a handler.
  (3) **Virtual events do not bubble.** Verified — a
  `<<X>>` emitted on a child widget never reaches a `bind` on
  the parent. Documented with the explicit re-emit relay pattern
  and a 5-row table of widgets that *claim* to bubble but don't
  (Tabs, TabView, SideNav, PageStack, SelectBox).
  (4) **`event.data` round-trips arbitrary Python objects intact.**
  Verified that `dict`, `list`, `tuple`, etc. arrive as the same
  type with `==` equality. The framework's `BindingsMixin`
  (`core/capabilities/bind.py:140-154`) is what enables this.
  (5) **`event.data` arrives as `None` on non-virtual events** and
  on virtual events emitted without `data=`. Documented as a
  table-row distinction.
  (6) **`<<ThemeChanged>>` is Tk-stock** (fires on root when
  `Style.theme_use(...)` is called); **`<<LocaleChanged>>` is
  framework-emitted** by `MessageCatalog.locale(new_locale)` with
  payload `{"locale": new_locale}`. Both verified at runtime.
- Two existing bugs already on the bugs list referenced in the
  new page (no new bugs surfaced this session): the no-bubble
  failure cases listed above, and the Python 3.13 / Tk 8.6
  `unbind(seq, fid)` bug for `add="+"` bindings (cross-linked to
  `callbacks.md`'s `!!! danger` block). Snippet check: 7
  snippets, 1 executed, 0 failures. All cross-links resolve.
- **Signals & Events sub-section is now complete** (4/4 pages
  done in nav order). Next page in the sweep:
  `capabilities/layout/index.md`.

Earlier session (2026-05-01, capabilities/signals/callbacks.md):

- Full rewrite. Old page was 148 lines of abstract framing
  ("What is a callback?", "Callback execution model", "Widget command
  callbacks", "Event bindings") with **zero references to ttkbootstrap's
  actual API surface** — no mention of `command=`, `bind()`, `add="+"`,
  the `on_*` / `off_*` helpers, `report_callback_exception`, or even
  the existence of the framework's helper layer. Reads like a generic
  Tk tutorial.
- New version leads with a 4-row at-a-glance table comparing the three
  registration surfaces (`command=` / `widget.bind` / `widget.on_*`),
  then per-surface concrete sections naming the actual API. Mirrors
  the structure of `index.md` (4-row at-a-glance table) and
  `signals.md` (lead with the API, follow with rationale).
- Five concrete claims surfaced and verified at runtime:
  (1) **`command=` does NOT fire on programmatic value writes** —
  only on user invocation. Restated from index.md but with the full
  per-widget table (Button, Toolbutton, MenuButton, DropdownButton,
  CheckButton, Switch, CheckToggle, RadioButton, RadioToggle,
  OptionMenu, Scale, Spinbox) and the firing condition for each
  (Scale fires repeatedly during drag; Spinbox fires only on
  stepping; OptionMenu's set() does not fire — but see the
  double-fire bug in OptionMenu's own page).
  (2) **`widget.bind(seq, fn)` without `add="+"` silently
  *replaces* any prior binding on `seq`.** Verified at runtime:
  `bind('<<X>>', a); bind('<<X>>', b); event_generate('<<X>>')` →
  only `b` fires. With `add="+"`, both fire. The framework's `on_*`
  helpers all use `add="+"` internally so mixing them with raw
  binds is safe; mixing two raw binds is the bug. Documented as
  the central "almost always what you want" axiom under the
  `widget.bind` section.
  (3) **`widget.bind` returns a string id ending in `wrapper`;
  `signal.subscribe` returns a string id ending in `traced_callback`.**
  Verified at runtime
  (`fid = '4690485056wrapper'`, `sid = '4684328192traced_callback'`).
  Useful for telling at a glance which observation surface a given
  helper wraps when you don't have the source open.
  (4) **The `on_* / off_*` helpers come in three callback shapes**,
  not one: bind passthrough (cb receives event with raw `event.data`),
  bind+enrich (cb receives event with synthesized `event.data` built
  from widget state at firing time — e.g. `TextEntryPart.on_enter`
  rebuilds `{value, text}` even though `<Return>` carries no data),
  and signal subscribe (cb receives the new value, no event wrapper).
  Documented as a 3-row table with the three flavors named explicitly
  and an example of each. Plus a fourth shape on dialog-result
  helpers (`MessageDialog.on_dialog_result(cb)` unwraps `event.data`
  to pass the payload dict directly to `cb` — already on the bugs
  list).
  (5) **Exceptions in any callback land in
  `tk.Tk.report_callback_exception`** — printed to stderr as the
  standard "Exception in Tkinter callback" trace, then discarded.
  The event loop continues. Verified at runtime
  (`Button(command=lambda: raise ValueError('boom!')).invoke()`
  prints the trace and the UI keeps running). Override by
  reassigning `app.report_callback_exception = handler`. Cross-link
  to `signals.md`'s `immediate=True` swallow-asymmetry warning.
- **One real bug surfaced and added to the bugs list:**
  `widget.unbind(seq, fid)` is broken for `add="+"` bindings on
  Python 3.13 / Tk 8.6. The CPython 3.13 `Misc._unbind`
  (`tkinter/__init__.py` ~line 1450) filters bind script lines for
  the prefix `if {"[<fid> ` — the wrapper form Tk uses for
  non-`add` bindings. Bindings registered with `add="+"` produce
  raw script lines starting with the bare fid, so the filter never
  matches: no lines are removed but `Tcl.deletecommand(fid)` still
  runs, leaving dangling references in the bind script. Subsequent
  `event_generate(seq)` then dispatches to the deleted proc and
  aborts the entire binding sequence silently — *every* handler on
  `seq` (not just the targeted one) stops firing. Verified on
  Python 3.13.9 / Tk 8.6 with two `add="+"` bindings, one
  `unbind(seq, fid)` call, then `event_generate` produces zero
  invocations. **Every `off_*` helper in the framework is implicated**
  because every `on_*` helper passes `add="+"` (or `add=True`). The
  documented workaround is `widget.unbind(seq)` to detach everything
  and re-bind the handlers you want to keep, or hold a single
  dispatcher closure and switch its body via a flag instead of
  unbinding. This is technically a CPython tkinter bug, not a
  ttkbootstrap bug, but it impacts the entire framework's `off_*`
  surface today and is worth flagging at the framework level.
  Added to the bugs list as a `!!! danger` block.
- Snippet check: 16 snippets, 1 executed, 0 failures. All 7
  cross-links resolve (`index.md`, `signals.md`,
  `virtual-events.md`, three platform pages, one widget page).

Earlier session (2026-05-01, capabilities/signals/signals.md):

- Targeted edits over the existing page (it was already structurally
  sound). Added a new "Constructing a signal" section that surfaces
  the previously-undoc `name=` and `master=` ctor kwargs and the
  precondition that a default root must already exist (Signal cannot
  be constructed before the App). Surfaced the `coerce=` parameter
  on `from_variable` with a worked use case. Added a brief
  `__getattr__`-proxy note (signal.trace_info() etc. work
  transparently) at the end of "Reading and writing the value".
- Three new findings surfaced in "Subscribing", all verified at
  runtime:
  (1) `unsubscribe(unknown_fid)` and a double-`unsubscribe(fid)`
  are silent — `_SignalTrace.remove` (`signal.py:60-68`) swallows
  `tk.TclError` and pops a missing fid as None. Worth knowing for
  cleanup paths that may double-unsubscribe.
  (2) Subscribing the **same callable twice** registers two
  distinct fids; both fire on every write; detaching one leaves
  the other live. Verified at runtime
  (`subscribers count == 2` after two `subscribe(cb)` calls;
  one `set('x')` call produces 2 invocations of `cb`). Intentional
  per source comment at `signal.py:97` ("Map fid -> callback to
  allow multiple subscriptions of same function") — composite
  widgets that wire the same handler through multiple paths rely
  on this. Documented as an intentional contract, not a bug. Tied
  loosely to the OptionMenu `<<Change>>` double-fire bug already
  on the bugs list — that bug is the failure mode of the same
  feature when used unintentionally.
  (3) **Exception handling asymmetry between `immediate=True`
  and write-driven dispatch.** Exceptions raised during the
  `immediate=True` invocation are silently swallowed (the
  `try/except Exception: pass` at `signal.py:266-268`).
  Exceptions raised during write-driven dispatch propagate to
  Tk's `report_callback_exception` and print to stderr (the
  standard "Exception in Tkinter callback" trace). Verified at
  runtime: a subscriber raising `ValueError` with
  `immediate=True` is silent at registration, but the same
  subscriber raising `ZeroDivisionError` on a `set()` produces
  the Tk traceback to stderr. Documented as a `!!! warning`
  block. Worth considering as a real bug — either swallow both
  (less likely the desirable behavior) or propagate both
  (consistent error surfacing); the current asymmetry is
  surprising. Not added to the bugs list since it lives at the
  Tk dispatch boundary and the immediate path's `except` is a
  deliberate "don't fail subscription due to callback error"
  guard.
- Snippet check: 16 snippets, 8 executed, 0 failures. All
  cross-links resolve (`index.md`, `callbacks.md`,
  `virtual-events.md`, `../configuration.md`, two
  platform pages).

Earlier session (2026-05-01, capabilities/signals/index.md):

- Rewrote the Signals & Events section landing. Old page was 112 lines
  of abstract framing ("What is a callback?", "What is a signal?",
  "Why virtual events exist") with no API surface, no decision rubric,
  and a hand-wavy "1. user action triggers callback → 2. callback
  updates signal → 3. widget emits virtual event" flow that doesn't
  reflect how the library actually composes the three mechanisms.
  New version leads with a 6-row at-a-glance table comparing
  Callback / Virtual event / Signal across (registered with /
  listener receives / multiple listeners / fires on / decoupled /
  best for), then per-mechanism blurbs that name the actual API
  (`Signal[T]` from `ttkbootstrap.Signal`, `signal=` / `variable=` /
  `textsignal=` / `textvariable=` widget kwargs, `command=` only
  fires on user invocation, `widget.event_generate(...)` /
  `widget.bind('<<Name>>', cb)`).
- Three concrete claims surfaced and verified at runtime:
  (1) `command=` does NOT fire on programmatic value writes — only
  on user invocation (click, Enter, `widget.invoke()`). Verified
  with `CheckButton(signal=sig, command=cmd); sig.set(True)` →
  command not called; `cb.invoke()` → command called. Signal
  subscribers fire on every variable write. The "user intent vs
  any state change" asymmetry is the central reason both mechanisms
  exist.
  (2) `Signal.set(value)` enforces strict `type(value) is
  self._type` — `Signal(0).set(True)` raises `TypeError: Expected
  int, got bool` because of the bool-is-int subclass strictness.
  Worth documenting in `signals.md` (the next page in the sweep).
  (3) Subscriber dispatch order is **reverse insertion order**
  (Tk variable-trace ordering quirk). Two subscribers `a` then
  `b`: `b` fires before `a`. Probably worth mentioning in
  `signals.md`; not load-bearing for the index.
- Carried forward from the platform sweep convention: the page
  cross-links to platform pages (`event-loop.md`,
  `events-and-bindings.md`) for the underlying mechanism, and
  flags the two virtual-event pitfalls already on the bugs list
  up front (no parent-chain propagation; `add="+"` to keep prior
  bindings).
- `signal.subscribe(...)` callback shape is `cb(value)`, not
  `cb(event)` — different from `bind('<<Change>>', cb)` whose
  callback receives a Tk event with `.data`. Explicitly contrasted
  in the table.
- Snippet check: 2 snippets, 1 executed, 0 failures. All 8
  cross-links resolve.

Earlier session (2026-05-01, capabilities/index.md):

- Rewrote with three primary changes vs the old version:
  (1) Topic list rebuilt to match the zensical nav. Old "Next steps"
  listed only 4 of 7 nav sections (signals, layout, validation, icons),
  missing `layout-props.md`, `state-and-interaction.md`,
  `configuration.md`, and `localization.md`. New version groups all 18
  pages under five thematic headings (Reactivity / Layout / Input and
  feedback / Visual assets / Configuration and localization), parallel
  to platform/index.md.
  (2) Replaced abstract framing ("What is a capability?", "Why
  capabilities exist", "How capabilities are implemented") with a
  concrete "Capabilities vs Platform vs Guides" section. The old page
  claimed "capabilities are mixins" — only true for some (e.g. the
  `LocalizationMixin` family in `core/capabilities/`); Signals are a
  class system, validation is a rule engine, configuration is a
  dataclass plus widget kwargs. The collision with `reference/
  capabilities/` (which IS literally the mixins page tree) made the
  framing ambiguous.
  (3) "When to read this section" now lists eight concrete questions,
  each linking to the page that answers it — directive rather than
  philosophical.
- All 22 cross-links resolve. Snippet check: 113 files, 919 snippets,
  0 failures.

Earlier session (2026-04-30, capabilities/configuration.md): see
commit `938e7fc`.

Pages to review (capabilities sweep, 18 total):

- [x] `index.md` — section landing
- [x] `signals/index.md` — Signals & Events overview
- [x] `signals/signals.md` — `Signal` class
- [x] `signals/callbacks.md` — command/bind/subscribe
- [x] `signals/virtual-events.md` — virtual events
- [x] `layout/index.md` — layout overview
- [x] `layout/containers.md` — Frame family
- [x] `layout/spacing.md` — padding, gap, density
- [x] `layout/scrolling.md` — ScrollView
- [x] `validation/index.md` — validation overview
- [x] `validation/rules.md` — rule types
- [x] `validation/results.md` — `ValidationResult`
- [x] `icons/index.md` — icons & images overview
- [x] `icons/icons.md` — `BootstrapIcon`
- [x] `icons/images.md` — `Image` utility
- [x] `layout-props.md` — pack/grid/place kwargs
- [ ] `state-and-interaction.md` — widget state, focus, grabs
- [x] `configuration.md` — `AppSettings` + widget kwargs
- [ ] `localization.md` — `MessageCatalog` + `IntlFormatter`

**Cross-cutting feedback shipped this session:** the user signaled
that Canvas and Text "warrant more expansive write-ups given their
nature" (i.e. they are unique, powerful widgets where the slim
primitives arc undersells the API). Apply this to any future
foundational primitive: more per-type detail (Canvas item-type
options, Text tag styling matrix), more patterns (rubber-band,
snap-to-grid, animation, embedded widgets, image+PIL recipe), a
dedicated Performance section breakout, and an expanded Behavior
section. Both `canvas.md` and `text.md` now follow this expanded
treatment — see their per-page session notes below.

**SelectBox relocation (2026-05-01).** The `selectbox.md` page was
moved from `widgets/selection/` to `widgets/inputs/`. Rationale: a
combobox-style widget shares the entry-style chrome (border, focus
ring, type-ahead text field when `allow_custom_values=True`) of
TextEntry/NumericEntry/DateEntry — the look-and-feel argument
beats the "produces a chosen value" classification. Same precedent
as `toolbar.md` (navigation → application). Logistics done in the
move commit:
- `git mv docs/widgets/selection/selectbox.md docs/widgets/inputs/selectbox.md`
- `zensical.toml` — moved from Selection menu to Inputs menu (between
  ScrolledText and SpinnerEntry, near the text-based inputs)
- 14 files / 31 inbound link updates
- when reviewing, use the **inputs template**
  (`docs/_template/widget-input-template.md`) and lead with
  `Value model`, not `Selection model`. The selection-template
  framing (independent-vs-mutex / shared-variable) is the wrong fit
  for a single-cell text-input-with-dropdown.

**Cross-cutting commit shipped this session:** the appearance
subsection heading is now consistently **`Colors & Styling`** (with
ampersand and capital S) across all widget pages — replacing both
`Theming` (used by 3 freshly-reviewed selection pages) and
`Colors and styling` (the older form, used by 8 pre-review selection
+ primitives pages). Apply this convention to every subsequent
sweep. One inline `**Theming.**` lead-in on `data-display/label.md`
was also normalized for consistency. "Theming" mentions that point
at the user-guide `Theming` page (Related-guides bullets etc.) were
left alone — those are guide names, not section labels.

**Platform sweep — convention notes (2026-05-01).** Architectural
pages (`platform/*`, `capabilities/*`, `design-system/*`) don't follow
the widget templates and aren't in `CATEGORY_TEMPLATE_MAP`. The
editorial sweep produced one consistent pattern across all 17
platform pages worth applying to capabilities and design-system:

1. **Replace abstractions with verified-at-runtime facts.** Almost
   every "thin" platform page led with generic "Tk has an event
   loop" / "ttk has styles" framing. The rewrites lead with concrete
   API surface (default bindtag tuple, resolved style names, three
   window classes) verified by running code at the start of the
   session.
2. **Snippets are runtime-validated.** Use `tools/check_doc_snippets.py
   --run --file <path>` after every rewrite. The check caught one
   genuine bug: the page incorrectly showed `ttk.Toplevel(parent,
   title=...)` — `Toplevel.__init__` takes `title` as the first
   positional argument, with master through `**kwargs`. Worth
   cross-checking when widgets reference Toplevel construction.
3. **Cross-link the surfaced bugs.** Where a platform page describes
   behavior already on the bugs list (e.g. the `App.override_redirect`
   / `Toplevel.overrideredirect` / `AppShell.frameless` naming
   inconsistency), name the bug explicitly with file:line context so
   readers landing here see the connection.

Two pages required no edits — `accessibility.md` (Phase 4C) and
`cli.md` (PR #1051) were already in the right shape. `threading-and-
async.md` (Phase 4A) and `platform-differences.md` (Phase 4B) needed
only light touch-ups. The other 13 got rewrites or substantial
expansions.

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
- `widget-overlay-template.md` (anchored on `tooltip.md`).
  `Lifecycle` is required (it carries the trigger / visibility /
  dismissal / blocking-vs-non-blocking framing that every overlay
  page needs). No `*Optional` H2s.
- `widget-selection-template.md` (anchored on `checkbutton.md`).
  `Selection model` is required (it carries the value-type /
  independent-vs-mutex / initial-state / commit-semantics framing
  that every selection page needs). No `*Optional` H2s.

Remaining 1 template (form) still leads with `Framework integration`
etc. Apply the editorial pass at the start of the form sweep — that
category has 0 pages written, so the template fix is free.

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

**All 14 guides in `docs/guides/` are done** (2026-04-30). Every
section under `docs/` has now had the editorial pass:
guides 14/14, widgets (all categories), platform 17/17,
capabilities 18/18, design-system 6/6.

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

**Widget pages — inputs** (`docs/widgets/inputs/`, 11 pages) — **DONE 11/11 (2026-05-01).**

The original 10 pages passed the editorial pass on 2026-04-30.
`selectbox.md` was relocated here from `widgets/selection/` on
2026-05-01 (see the "SelectBox relocation" callout in the current
handoff) and rewritten under the inputs template the same day
(commit `d495951`).

All 11 pages reviewed against `docs/_template/widget-input-template.md`.
Inputs use a **different template** than actions — don't carry the
actions section names over verbatim.

Last session (2026-05-01, selectbox sweep — final inputs page):

- `selectbox.md` rewritten to the slim inputs template at its new
  location. SelectBox is the eleventh and final page in the sweep
  — a `Field` subclass that renders a label + entry + message line
  + chevron button, with a popup list of `items` opened on click.
  Three modes (read-only default; editable + filter via
  `enable_search`; editable + free-form via `allow_custom_values`)
  and four behavioral combinations of those flags. Restructured
  around `Value model` (the core selection-string framing) and
  surfaced four runtime-verified bugs:
  (1) `<<Change>>` is fired on `entry_widget`, not on the SelectBox
  itself (`composites/selectbox.py:536`). Tk virtual events do not
  propagate up the parent chain, so `sb.bind('<<Change>>', cb)`
  silently no-ops. The `on_changed` helper still works because
  `Field.__init__` forwards it (`field.py:263` —
  `self.on_changed = self._entry.on_changed`). Same shape as the
  Tabs `<<TabSelect>>` bug already on the bugs list.
  (2) `sb.value = "not_in_items"` is silently accepted even when
  `allow_custom_values=False`. The setter writes through to the
  Field's value, the entry shows the orphan as plain text,
  `selected_index` returns `-1`, and `<<Change>>` fires as if it
  were a normal selection. Same shape as OptionMenu /
  ToggleGroup orphan-value bugs already on the bugs list.
  (3) `sb.configure(value=X)` is broken — `_delegate_value`
  (`composites/selectbox.py:493-499`) has the same inverted query
  /set branches as LabeledScale's broken delegators: the set
  path returns the current value, the query path attempts to
  write `None`. Workaround: use the property setter
  (`sb.value = X`).
  (4) `sb.configure(dropdown_button_icon=...)` raises
  `TclError: unknown option`. The icon is captured at
  construction into the addon and there's no delegate to lift
  it back into the configure surface.
  Also documented: the four behavioral modes (`enable_search` ×
  `allow_custom_values`) as a 4-row table; Tk's combobox-style
  popup positioning (below the entry by default, flips above
  when there isn't enough room — matches `PlacePopdown`); the
  implicit "first filtered item commits on close" rule for
  `enable_search=True, allow_custom_values=False` (popup close
  via Escape / Tab / click-outside still selects the first
  filter match, supporting type-prefix-then-Tab UX); the keyboard
  contract (Down / Up move the highlight, Enter / Tab commit,
  Escape closes); reconfiguration semantics (`items`,
  `allow_custom_values`, `enable_search` are live-reconfigurable;
  `value` and `dropdown_button_icon` are construction-only —
  but for different reasons).
  Also fixed broken sibling links (the old page used relative
  paths `optionmenu.md` / `radiogroup.md` / `checkbutton.md`
  that no longer resolve from `widgets/inputs/`); rewritten with
  `../selection/` prefixes.

`tools/check_doc_structure.py --category inputs` → 11/11 pass.
`tools/check_doc_snippets.py --run --file
docs/widgets/inputs/selectbox.md` → 0 failures (6 snippets, 1
executed).

Earlier session (2026-04-30):

- `scrolledtext.md` — restructured to template; clarified that
  `ScrolledText` has **no `value`/signal/variable model** (it wraps
  `tkinter.Text`), corrected the existing claim that the container
  themes via `accent` (it's `scrollbar_style`), documented the
  delegation surface (Text methods copied at construct time, plus
  `__getattr__` fallback to `self._text`), and replaced the wrong
  default in the old Quick start (default `scrollbar_visibility` is
  `'always'`, not `'scroll'`).

Older session (2026-04-30, two-page batch):

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
- [x] `selectbox.md` — relocated from `widgets/selection/`
      2026-05-01; rewritten under the inputs template the same day

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

### Widget pages — navigation (`docs/widgets/navigation/` + `appshell.md` + `toolbar.md`, 5 pages) — DONE 5/5 (2026-05-01)

The "navigation directory" turned out to be heterogeneous; one
template didn't fit all five pages. Per-page assignment:

| Page | Canonical location | Template | Status |
|---|---|---|---|
| `tabs.md` | `widgets/navigation/tabs.md` | `widget-navigation-template.md` | done (anchor) |
| `appshell.md` | `widgets/application/appshell.md` | bespoke app-shell arc | **done 2026-05-01** |
| `sidenav.md` | `widgets/navigation/sidenav.md` | `widget-navigation-template.md` | **done 2026-05-01** |
| `toolbar.md` | `widgets/application/toolbar.md` | `widget-action-template.md` (with `Item types` subsection) | **done 2026-05-01** — relocated from `widgets/navigation/`; no longer in CATEGORY_TEMPLATE_MAP enforcement |
| `navigationview.md` | `widgets/navigation/navigationview.md` | none — deprecation stub | **done 2026-05-01** — added to `SKIP_FILES` in `tools/check_doc_structure.py` |

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

Last session (2026-05-01, SideNav sweep + NavigationView SKIP_FILES):

- `sidenav.md` rewritten to the slim navigation template. SideNav is
  the second page using the nav template (after Tabs) — primary
  navigation chrome with three display modes, scrollable items,
  collapsible groups, and a footer area; selection drives a single
  shared variable (no page coupling). Restructured around the slim
  arc: intro → Basic usage → Navigation model (channels table + item
  types table + lookup/removal) → Common options (single 11-row
  table) → Behavior (display modes, pane state vs display mode,
  groups, header layout, reconfiguration) → Events (combined
  SideNav-level and item/group-level table) → When → Related →
  Reference. Four runtime-verified bugs surfaced; all four are real
  API gotchas, not just doc gaps:
  (1) `nav.select(key)` does **not** validate `key`. The variable
  gets the orphan key, `<<SelectionChanged>>` fires with that key
  in `event.data`, and `selected_key` returns it — but no item
  paints as selected because the indicator update gates on `key in
  self._items` / `self._footer_items` (`view.py:402-410`). Verified
  at runtime: `nav.select('phantom')` → `nav.selected_key ==
  'phantom'`. Same shape as the Tabs orphan-key bug. Documented as
  a `!!! warning` in Navigation model.
  (2) `display_mode='minimal'` does **not** start hidden. Despite
  the conceptual framing ("hidden until toggled" — claimed in the
  old page and weakly suggested by `_apply_display_mode`'s
  `if self._is_pane_open` branch at `view.py:312`), the constructor
  default for `is_pane_open` is `True`
  (`view.py:110`). So a vanilla
  `SideNav(display_mode='minimal')` shows the pane in full; the
  user has to pass both `display_mode='minimal',
  is_pane_open=False` to get the hidden-until-toggled behavior the
  name implies. Documented as a `!!! warning` in Behavior.
  (3) `toggle_pane()` semantics depend on the current mode and
  trip up the obvious "hamburger toggles visibility" mental model.
  In `expanded` mode it switches to `compact` (and vice versa),
  emitting `<<DisplayModeChanged>>` (`view.py:797-799`). Only in
  `minimal` mode does it actually toggle visibility, emitting
  `<<PaneToggled>>` (`view.py:791-795`). Verified at runtime:
  starting from `expanded`, `toggle_pane()` → `display_mode ==
  'compact'`, `is_pane_open` still `True`. So the hamburger button
  AppShell wires up does **not** show / hide the sidebar in
  expanded mode — it shrinks it. Documented as a `!!! warning` in
  Behavior with the visual axis-table; surfaced the workarounds
  (use `minimal` mode for true show / hide, or wire the hamburger
  to `nav.close_pane()` / `nav.open_pane()` directly).
  (4) `pane_width` is silently ignored in `compact` mode. The
  `compact` branch of `_apply_display_mode` (`view.py:308-310`)
  hard-codes `width=self.PANE_WIDTH_COMPACT` (52 px) regardless of
  the constructor's `pane_width=` argument. Verified at runtime:
  `SideNav(display_mode='compact', pane_width=400)` ends up with
  `_pane_frame.cget('width') == 52`. Documented in the Common
  options table.
  Also documented (some new, some restated): `select()` writes
  through the same code path as user clicks (so observers see one
  event for both); `accent` is **read-only after construction**
  (verified — `_delegate_accent` at `view.py:887-893` returns
  early on writes, no rebuild); `remove_item(missing_key)` is a
  silent no-op while `add_item` raises `ValueError` on duplicate
  keys (asymmetric); footer items participate in the **same
  selection group** as main items (single `_selection_var`); the
  `node()` lookup checks both main and footer items but raises
  `KeyError` on miss; `<<ItemInvoked>>` fires on the
  `SideNavItem`, `<<GroupExpanding>>` / `<<GroupCollapsed>>` fire
  on the `SideNavGroup` (Tk virtual events do not bubble — same
  pattern as Tabs / TabItem); `compact` groups render a
  `ContextMenu` flyout to the right (`group.py:325`) instead of
  expanding inline, and `group.expand()` / `collapse()` are no-ops
  in compact (`group.py:376-388`); the pane chrome lives on a
  `surface='chrome'` Frame internally (`view.py:201`); the visual
  order in the pane (top → bottom) is hamburger → separator →
  toolbar header → scrollable items → footer separator → footer
  items.
- `tools/check_doc_structure.py` — added `"navigationview.md"` to
  `SKIP_FILES` (with a comment explaining why: it's a 6-line
  deprecation redirect that points at SideNav). The
  `NavigationView`/`NavigationViewItem`/`NavigationViewGroup`/
  `NavigationViewHeader`/`NavigationViewSeparator` symbols are still
  exported from `widgets/composites/sidenav/__init__.py:18-23` as
  back-compat aliases, but the page itself is just a redirect.
  Holding it to the navigation template would force template
  content into a page whose only job is "use the new name".

`tools/check_doc_structure.py --category navigation` →
3 files checked, 1 failed (only toolbar.md remains, and it's
failing against the **navigation** template — which it isn't
supposed to follow per the per-page assignment table above).
`tools/check_doc_snippets.py --run --file
docs/widgets/navigation/sidenav.md` → 0 failures (4 snippets,
1 executed).

Last session (2026-05-01, toolbar sweep — final navigation page,
relocated to widgets/application/):

- The "where does toolbar live?" question was settled in favor of
  **`docs/widgets/application/`** alongside AppShell — neither
  `actions/` (the action-template fit but the directory is for
  individual action *primitives*, not action *containers*) nor
  `navigation/` (no selection, no keyed targets — fails the nav
  template). Moved via `git mv`; cross-refs updated in 4 files
  (`zensical.toml` — Toolbar promoted from Navigation menu to
  Application menu alongside App/AppShell/Toplevel;
  `docs/guides/navigation.md`; `docs/guides/toolbars.md`;
  `docs/widgets/application/appshell.md`). The stub-deletion path
  used for AppShell wasn't repeated here — the navigation/toolbar.md
  rename was clean enough.
- `toolbar.md` rewritten to the slim action template at the new
  location. Toolbar is the second non-action page using the action
  template (after AppShell's bespoke arc), and it earned a
  custom **`Item types`** subsection up front covering the five
  builders (`add_button` / `add_label` / `add_separator` /
  `add_spacer` / `add_widget`) — that's the page's central API
  and consolidates a 5-row table plus per-builder behavior. The
  optional `Patterns` subsection is filled in for the custom-titlebar
  + frameless-window composition (the dominant non-AppShell use
  case) and a menubar-via-MenuButton recipe (since ttkbootstrap
  doesn't ship a distinct `MenuBar` widget).
- Three things the old page got wrong or omitted, two of which
  became new bugs:
  (1) the old `Quick start` showed the toolbar as a standalone
  bar with `surface="chrome"` — fine — but the framing throughout
  treated `accent` as a styling shortcut. Verified at runtime that
  Toolbar (a `Frame` subclass) is in `CONTAINER_CLASSES`, so
  `accent="primary"` is rerouted by the bootstyle wrapper to
  `surface="primary"` — it tints the toolbar's background, not its
  frame. Documented in Common options and pointed callers at
  `surface=` for clarity.
  (2) the old page never warned that **`add_widget()` does not
  validate the widget's parent**. The source docstring
  (`widgets/composites/toolbar.py:329-345`) says the widget must be
  parented to `toolbar.content`, but `add_widget` only calls
  `widget.pack(**pack_kwargs)` — a widget parented to anything else
  still gets call-`pack`-ed, just at its *actual parent's* location,
  which is silently nowhere visible inside the toolbar. Verified at
  runtime: `Entry(app)` followed by `tb.add_widget(ent)` packs the
  Entry into `app`, not into `tb.content`. Documented as a `!!!
  warning` block in `Item types`; added to the bugs list.
  (3) the old page never noted that **`density` and `button_variant`
  defaults are read at `add_button()` time**. Reconfiguring them
  later via `tb.configure(density='default')` only affects subsequent
  `add_button()` calls — existing buttons keep their original
  values. Verified at runtime. Documented in Behavior; not a bug,
  but easy to misread as retroactive given the configure-delegate.
- Surfaced one additional bug at the snippet-validation step: the
  three application-window classes use **inconsistent kwarg names**
  for the "remove OS chrome" option:
    - `App.override_redirect=True` (with underscore)
    - `Toplevel.overrideredirect=True` (no underscore — matches
      Tk's native `wm overrideredirect`)
    - `AppShell.frameless=True` (renamed entirely)
  Verified all three at runtime
  (`App(frameless=True)` → `TypeError: unexpected keyword`,
  `Toplevel(frameless=True)` → `TclError: unknown option
  "-frameless"`, both `App(override_redirect=True)` and
  `Toplevel(overrideredirect=True)` succeed). Documented in
  `Common options & dragging` with the per-class kwarg-name table
  inline, and added to the bugs list. Either harmonize on a single
  spelling across the three classes, or document the divergence
  in a top-level note. (Surfaced by toolbar.md rewrite,
  2026-05-01.)
- Maximize toggle uses `winfo_toplevel().state('zoomed')` — Windows
  canonical, accepted on macOS but on some Linux WMs is a no-op.
  Documented as a cross-platform caveat in Behavior; not added to
  the bugs list since the unreliability sits at Tk's wm-state
  layer, not Toolbar's.

`tools/check_doc_structure.py --category navigation` → 2 files
checked, all pass (toolbar.md no longer in this directory; tabs.md
and sidenav.md remain). `widgets/application/` is not in
`CATEGORY_TEMPLATE_MAP`, so the new toolbar.md location has no
template enforcement.
`tools/check_doc_snippets.py --run --file
docs/widgets/application/toolbar.md` → 0 failures (10 snippets,
2 executed).

Pages to review:

- [x] `tabs.md` — navigation template (anchor)
- [x] `appshell.md` — bespoke app-shell arc (at `widgets/application/`)
- [x] `sidenav.md` — navigation template
- [x] `toolbar.md` — action template (at `widgets/application/`)
- [x] `navigationview.md` — deprecation stub; SKIP_FILES'd

### Widget pages — overlays (`docs/widgets/overlays/`, 2 pages) — DONE 2/2 (2026-05-01)

Template: `docs/_template/widget-overlay-template.md` (slim arc,
restructured this session). Required H2s: `Basic usage`,
`Lifecycle`, `Common options`, `Behavior`, `Events`,
`When should I use WidgetName?`, `Related widgets`, `Reference`.
No `*Optional` H2s — `Lifecycle` is required (every overlay page
has a trigger / visibility / dismissal / blocking story worth
documenting).

`tooltip.md` is the canonical anchor for the overlays sweep, the
way `button.md` / `textentry.md` / `messagedialog.md` / `label.md` /
`frame.md` / `tabs.md` anchored their respective categories.

Last session (2026-05-01, overlays sweep started — template
restructure + tooltip anchor):

- `widget-overlay-template.md` rewritten to the slim arc.
  Old form led with `Framework integration` + `What problem it
  solves` + `Core concepts` + fragmented `Content and
  presentation` / `Positioning` / `Behavior and lifecycle` /
  `Events and callbacks` / `UX guidance` H2s. New form: intro →
  `Basic usage` → `Lifecycle` → `Common options` → `Behavior` →
  `Events` → `When should I use WidgetName?` → `Related widgets`
  → `Reference`. Mental-model section name fixed at `Lifecycle`
  (covers trigger model, visibility window, dismissal,
  blocking-vs-non-blocking, one-shot-vs-reusable). No
  `*Optional` H2s.
- `tooltip.md` rewritten as the anchor. Three things the old
  page got wrong or omitted, two of which became new bugs:
  (1) the old page used `# Tooltip` as the H1 (single capital
  T), but the public class name is `ToolTip`
  (`getattr(ttk, 'Tooltip', None) is None`; the export at
  `api/widgets.py:75` is `ToolTip`). Fixed the H1 to match the
  public name.
  (2) the old page never noted that `ToolTip(widget, ...)`
  uses **hard binds** (`widget.bind("<Enter>", ...)` without
  `add="+"`) and silently overwrites any existing
  `<Enter>` / `<Leave>` / `<Motion>` / `<ButtonPress>` binding
  on the target widget. Verified at runtime: a pre-bound
  `<Enter>` handler that fires before tooltip attachment
  stops firing afterward. Documented in Behavior with a
  workaround (bind your handlers *first*, attach the tooltip
  *after*); added to the bugs list.
  (3) the old page never noted that **two `ToolTip(widget,
  ...)` calls on the same widget cause the second to win** —
  the second's bindings overwrite the first's, and the first
  becomes inert (its `_show_tip` never runs because the
  binding no longer points at it; it's also not garbage-
  collected automatically because it still owns references
  through the closure). Verified at runtime: with
  `t1 = ToolTip(btn, text='first', delay=0)` and
  `t2 = ToolTip(btn, text='second', delay=0)`, hovering
  produces `t1._toplevel is None`, `t2._toplevel` populated.
  Documented in Behavior as a `!!! warning`; added to the
  bugs list.
  Also documented: `ToolTip` is **not a widget** (no
  `configure`/`cget`/parent — controller object that owns a
  Toplevel created on hover); the only public surface is
  `__init__` and `destroy`; to change `text` etc., destroy
  and recreate; the nine-point anchor model
  (`anchor_point`/`window_point`, default `window_point` is
  geometric opposite); `auto_flip` (bool / `'vertical'` /
  `'horizontal'`); the macOS chromeless path
  (`windowtype="tooltip"` triggers `MacWindowStyle "help
  none"` since `overrideredirect` is silently skipped on Aqua
  per `BaseWindow`); the `accent='background[+1]'` default;
  the internal `variant='tooltip'` Frame style
  (`style/builders/tooltip.py`); the `image=` field rendering
  via `compound='bottom'`; `wraplength` defaulting to
  `scale_size(widget, 300)` (DPI-scaled); the deliberate
  negative `Events` section (no virtual events, no `on_*`
  helpers — bind to the target widget's `<Enter>` /
  `<Leave>` directly *before* attaching the tooltip).

Last session (2026-05-01, toast sweep — final overlay page):

- `toast.md` rewritten to the slim overlay template. Toast is the
  second and final page in the sweep — a programmatically-shown,
  non-blocking notification overlay. Like ToolTip, Toast is **not a
  widget** (controller object that owns a Toplevel created on
  `show()`), but unlike ToolTip it survives across show/hide cycles
  (the same instance can be reshown). Three things the old page got
  wrong or omitted, three of which became new bugs:
  (1) the old page never noted that **calling `show()` twice on the
  same Toast instance leaks the first Toplevel**. `show()` builds a
  new Toplevel and writes it to `_toplevel` without destroying the
  previous one (`composites/toast.py:188-190`). The first Toplevel
  remains mapped on screen until the application exits. Verified at
  runtime: `t.show()` → `first = t._toplevel`; `t.show()` →
  `second = t._toplevel`; `first is not second` and both
  `winfo_exists() == 1`. Documented as a `!!! warning` in
  Lifecycle; added to the bugs list.
  (2) the old page never noted that **`configure(bootstyle=...)`
  post-construction is silently a no-op for styling**. The
  legacy-bootstyle bridge runs only at `__init__`
  (`composites/toast.py:102` — `self._accent = accent or bootstyle`);
  `configure(bootstyle=...)` writes `_bootstyle` but doesn't update
  `_accent`. Verified: `Toast(bootstyle='success')` → `cget('accent')
  == 'success'`; subsequent `configure(bootstyle='danger')` →
  `cget('accent') == 'success'` (unchanged). Documented in Common
  options; added to the bugs list.
  (3) the old page never described the **`on_dismissed` payload
  contract**. The callback fires with `None` for auto-dismiss /
  close-button / `hide()` paths, but with the **full button options
  dict (including the `command` callable!)** for custom-button
  clicks (`composites/toast.py:297-303`). Verified at runtime: a
  `buttons=[{'text': 'Yes', 'command': btn_cmd, 'accent':
  'success'}]` invocation yields `data ==
  {'text': 'Yes', 'command': <function btn_cmd>, 'accent':
  'success'}` in the dismiss handler. The unwrap-aware shape is
  awkward: callers routing on which button was pressed must read
  `data["text"]` (or another marker key), and the dict still
  contains the `command` reference under `data["command"]`. Either
  unwrap to a sanitized payload (e.g. only `text`/`accent`/the
  caller-supplied `result=`) or document the contract loudly.
  Documented as the central Events table; added to the bugs list.
  Also documented: the `show(merge=True/False)` semantics
  (default `True` merges; `False` clears all options first); the
  reusable Toast pattern (one instance, many shows); the platform
  default position (mac/Win bottom-right `-25-75`, Linux X11
  top-right `+25+25`) via `WindowPositioning.position_anchored`;
  the macOS chromeless path (`windowtype='tooltip'` →
  `MacWindowStyle 'help none'`); `topmost=True` and `alpha=0.97`
  on the Toplevel; the `IconSpec` dict shape (`{name, size, color}`)
  and the `color` constraint (PIL color names / hex only — theme
  tokens like `'success'` raise in PIL); `memo` field rendering in
  the header with muted styling; that destroying via
  `destroy()` skips the `on_dismissed` callback entirely.

`tools/check_doc_structure.py --category overlays` → 2 files
checked, all pass.
`tools/check_doc_snippets.py --run --file
docs/widgets/overlays/toast.md` → 0 failures (9 snippets, 5
executed).

Pages to review (canonical anchor: `tooltip.md`):

- [x] `tooltip.md` — anchor for the overlays sweep
- [x] `toast.md`

### Widget pages — selection (`docs/widgets/selection/`, 9 pages) — DONE 9/9 (2026-05-01)

**Note:** `selectbox.md` was moved out of this category on
2026-05-01 (now lives at `widgets/inputs/selectbox.md`). The page
count was 10 originally; it's now 9. See the
"SelectBox relocation" callout in the current handoff for context.

Template: `docs/_template/widget-selection-template.md` (slim arc,
restructured this session). Required H2s: `Basic usage`,
`Selection model`, `Common options`, `Behavior`, `Events`,
`When should I use WidgetName?`, `Related widgets`, `Reference`.
No `*Optional` H2s — `Selection model` is required (every selection
page has a value-type / independent-vs-mutex / initial-state story
worth documenting up front).

`checkbutton.md` is the canonical anchor for the selection sweep,
the way `button.md` / `textentry.md` / `messagedialog.md` /
`label.md` / `frame.md` / `tabs.md` / `tooltip.md` anchored their
respective categories.

Last session (2026-05-01, calendar sweep — final selection page):

- `calendar.md` rewritten to the slim selection template. Calendar
  is the ninth and final page in the sweep — an inline date picker
  (single or range mode) that produces `datetime.date` values. The
  selection model section frames the two-mode split up front
  (single-mode `cal.value` returns a `date`; range-mode `cal.range`
  returns a `(start, end | None)` tuple), documents the silent-
  write contract for `set()` / `set_range()` / property setters /
  `configure(date=...)` (none of them fire `<<DateSelect>>`), and
  notes that Calendar has no shared-variable channel — no `signal=`,
  no `variable=`, observers bind `<<DateSelect>>` or read directly.
  Four runtime-verified bugs surfaced; all four are real API
  gotchas, not just doc gaps:
  (1) `Calendar(min_date=…, max_date=…)` without `value=` /
  `start_date=` opens at today's month unconditionally
  (`composites/calendar.py:166-168`). If today falls outside the
  configured window, every navigation candidate fails the clamp at
  `_is_month_allowed` (`calendar.py:850-855`) and both chevrons are
  blocked immediately. The user sees an unselectable view with no
  way to navigate. Verified at runtime: today=2026-05-01,
  `Calendar(min_date=date(2025,6,1), max_date=date(2025,8,31))` →
  display=2026-05-01, prev/next both rejected. Documented as a
  `!!! warning` in Behavior; added to the bugs list.
  (2) `cal.set(None)` and `cal.value = None` are silently no-ops.
  `set()` calls `_coerce_date(value)` which returns `None` for
  `None` input, then early-returns at `calendar.py:217-218`. The
  docstring at `calendar.py:214` claims "or None to clear
  selection" — false. Either honor `None` (clear `_selected_date`,
  `_range_start`, `_range_end`) or remove the docstring claim.
  Documented in Selection model; added to the bugs list.
  (3) `set()` / `set_range()` / `value` property setter /
  `configure(date=...)` all bypass `min_date` / `max_date` /
  `disabled_dates`. The interactive paths
  (`_on_date_selected_by_date` at `calendar.py:783-784`) check
  `_is_disabled` and reject; the programmatic paths do not.
  Verified: `Calendar(min_date=date(2025,6,1),
  max_date=date(2025,6,30)).set(date(2025,12,25))` succeeds.
  Documented as a `!!! warning` in Selection model; added to the
  bugs list.
  (4) In range mode, `cal.range = None` / `cal.set_range(None,
  None)` clears `_range_start` and `_range_end` but does NOT
  clear `_selected_date`. `set_range`'s normalization at
  `calendar.py:274` uses `e if e else (s if s else
  self._selected_date)` — when both arguments are `None`, the
  fallback keeps the old end-date. Net effect: `cal.range`
  reports `(None, None)` while `cal.value` and `cal.get()`
  return a stale date. Documented as a `!!! warning` in Selection
  model with a recommendation to read `cal.range` (not
  `cal.value`) in range mode; added to the bugs list.
  Also documented (some new, some restated): the title-click-
  resets-to-initial-date behavior (clicking the centered `Month
  Year` label calls `_on_reset_date` which restores the
  constructor's initial state, navigates display to that month,
  and emits `<<DateSelect>>` — undocumented in the old page); the
  right-click bindings on the year chevrons (`bind_right_click` is
  an alias for left-click — same handler); the range-mode click
  rules (1st = start, 2nd = end with auto-swap when end < start,
  3rd = new range starting from the click); the four
  `calendar-*` Toolbutton style variants (`calendar-day` /
  `calendar-date` / `calendar-range` / `calendar-outside`,
  registered in `style/builders/calendar.py`) and that they are
  not user-overridable through public options;
  `first_weekday=None` resolution (Babel's
  `Locale.parse(...).first_week_day`, falls back to Monday on
  failure, resolved once at construction); the
  `<<LocaleChanged>>` re-render path (weekday tokens via
  `MessageCatalog.translate`, month/year via
  `babel.dates.format_skeleton('yMMMM', ...)`); the keyboard
  contract (Tab walks in-month non-disabled cells in row-major
  order; `<space>` / `<Return>` invoke; no arrow-key grid
  navigation today); `show_outside_days` defaults that diverge
  by mode (`True` for single, `False` for range); the
  `value=` / `start_date=` aliasing (when `start_date is None`
  and `value is not None`, the constructor copies `value` into
  `start_date` at `calendar.py:163-164`); the construction-only
  semantics for `selection_mode`, `show_outside_days`,
  `show_week_numbers`, `first_weekday`, `min_date`, `max_date`,
  and `disabled_dates`. Common options consolidates into a
  13-row table.

`tools/check_doc_structure.py --category selection` → 9/9 pass.
`tools/check_doc_snippets.py --run --file
docs/widgets/selection/calendar.md` → 0 failures (4 snippets, 1
executed). Selection sweep complete.

Earlier session (2026-05-01, selection sweep started — template
restructure + checkbutton anchor):

- `widget-selection-template.md` rewritten to the slim arc.
  Old form led with `Framework integration` + `Overview` + a long
  fragmented body (`Variants` / `How the value works` / `Binding to
  signals or variables` / `Validation and constraints` / `Colors and
  styling` / `Localization` / `Additional resources`). New form:
  intro → `Basic usage` → `Selection model` → `Common options` →
  `Behavior` → `Events` → `When should I use WidgetName?` →
  `Related widgets` → `Reference`. Mental-model section name fixed
  at `Selection model` (covers value type, independent vs
  mutually-exclusive, initial state, indeterminate / empty / no-
  selection, commit semantics). No `*Optional` H2s.
- `checkbutton.md` rewritten as the anchor. CheckButton is the
  boolean selection primitive that Switch and CheckToggle subclass.
  Three things the old page got wrong or omitted, two of which
  became new bugs:
  (1) the old page claimed `value=None` "places the checkbutton in
  an indeterminate state" as if it were a stable, addressable third
  value. Verified at runtime: `value=None` + default `BooleanVar`
  shows `('alternate',)` at construction only because the Tcl
  variable is unset (matches default `tristatevalue=""`). After the
  first user click, the variable cycles between True and False
  only — alternate is **not reachable** programmatically.
  Documented honestly in Selection model with a `!!! warning` block.
  (2) the old page never noted that **`cb.set(None)` raises
  TypeError**. `BooleanVar` cannot hold `None`, so the indeterminate
  state has no programmatic re-entry path post-construction.
  Verified at runtime: `cb.set(None)` →
  `TypeError: getboolean() argument must be str, not None`.
  Documented in Selection model and Events; added to the bugs list
  as a real API gap (either expose `tristatevalue=` and switch to
  `StringVar` when `value=None`, or document the limitation
  loudly).
  (3) the old page conflated `command=` with signal subscriptions —
  saying both fired "when the value toggles." Verified at runtime
  that `command=` fires **only** on user invocation (click or
  `.invoke()`), while `signal.subscribe(fn)` and
  `variable.trace_add('write', fn)` fire on every variable write
  (programmatic or user-driven). The asymmetry matters for users
  building "save on user intent" handlers vs "react to any state
  change" listeners. Documented as a 3-row table in Events with
  per-path timing.
  Also documented: the actual variant axis (`default` and `switch`
  are the only two registered; `pill` / `round` / `square` raise
  `BootstyleBuilderError`); the construction-time-only nature of
  `value=` when `signal=` / `variable=` aren't passed (and the
  bound variable's pre-existing value wins when they are passed);
  the post-construction `configure(value=...)` path which **does**
  write through to the variable; the absence of virtual events and
  `on_*` helpers (CheckButton has no `<<Changed>>`); the deprecated
  `bootstyle` argument and its replacement by `accent` + `variant`.
  Common options consolidates into a 22-row table with a Theming
  and variants subsection underneath.

`tools/check_doc_structure.py --category selection` →
checkbutton.md no longer in the missing-sections list (9/10 pages
still pending).
`tools/check_doc_snippets.py --run --file
docs/widgets/selection/checkbutton.md` → 0 failures (5 snippets, 3
executed).

Mid-session (2026-05-01, switch + checkbutton anchor cleanup):

- `switch.md` rewritten to the slim selection template. As a
  CheckButton subclass with `variant='switch'` baked in
  (`widgets/primitives/switch.py:43-44`), the rewrite focuses on
  the divergences from the parent: no indeterminate state (the
  switch style builder has no `alternate` mapping; forcing
  `state(['alternate'])` is visually invisible); `density` is not
  valid (raises TclError; the CheckButton builder reads only
  `accent` and `surface`); the constructor unconditionally writes
  `variant='switch'` when `bootstyle` is not in kwargs (passing
  `variant='default'` to a Switch is silently overridden); the
  deprecated `bootstyle=` path bypasses the variant assignment
  entirely, so `Switch(bootstyle='primary')` renders as a regular
  CheckButton with a check-box indicator (different widget shape).
  Surfaced 3 new bugs (see bugs list).
- `checkbutton.md` cleanup pass — dropped the misleading `variant`
  row from the common-options table and renamed `Theming and
  variants` → `Theming` (later renamed to `Colors & Styling` in the
  cross-cutting commit). CheckButton has effectively one variant —
  the `switch` registration exists solely to back the dedicated
  `Switch` class.

Mid-session (2026-05-01, checktoggle):

- `checktoggle.md` rewritten. CheckToggle is a CheckButton subclass
  with `class_='Toolbutton'` (different ttk style class entirely,
  not a CheckButton variant). Three real divergences from the
  parent surfaced:
  (1) **the default variable is a `StringVar`** with `onvalue='1'`
  / `offvalue='0'`, NOT a `BooleanVar` (different from CheckButton
  and Switch). Net effect: `ct.set(None)` does NOT raise — it
  writes the string `'None'` silently, and the widget paints
  unpressed because the value matches neither onvalue nor offvalue.
  Callers relying on the BooleanVar guard must special-case
  CheckToggle.
  (2) there is a real **3-variant axis** here (`default` aliasing
  `solid`, `outline`, `ghost`) that CheckButton lacks. No `link` /
  `text` variants — those exist on Button but not on Toolbutton.
  (3) **`density='compact'` works** (captured into `style_options`
  by `_capture_density_option`); CheckButton itself doesn't accept
  `density=` at all.

Mid-session (2026-05-01, radiobutton + radiogroup):

- `radiobutton.md` rewritten as the mutually-exclusive sibling of
  CheckButton. The shared-variable selection model is the central
  framing. Three things the old page got wrong or omitted:
  (1) `widget.value` reads the **shared selection**, not the
  radio's own constructor `value=`. With three radios sharing a
  signal, all three return the same `.value`. Documented with an
  explicit example.
  (2) "group" is purely emergent from sharing `signal=` /
  `variable=` — not a class-level concept. Forgetting to share
  makes each radio its own independent group of one.
  (3) the default variable type is `IntVar` (initial `0`) —
  different from CheckButton/Switch (`BooleanVar`) and CheckToggle
  (`StringVar`).
  Also: only one variant (`default` for `TRadiobutton`); `density=`
  not valid (raises TclError); reconfiguring `value=` changes the
  constant this radio writes when clicked, NOT the current
  selection.
- `radiogroup.md` rewritten. Frames the group as "owns the shared
  variable; `add()` wires children automatically." Surfaced 2 new
  bugs (constructor `accent=` doesn't reach children;
  `RadioGroup.values()` returns keys not values).
- **radiobutton.md regression caught and fixed** while reviewing
  RadioGroup: the original claim that arrow keys don't auto-cycle
  was wrong. Tk's stock `TRadiobutton` class binding `<Up>` /
  `<Down>` is `ttk::button::RadioTraverse`, which IS the auto-cycle
  behavior. RadioGroup adds NO extra bindings (verified in source).
  Replaced the claim with the truth (Up/Down traverse via the ttk
  class binding; Left/Right not bound) and dropped the false
  "arrow-key navigation" RadioGroup feature claim from the
  related-widgets bullet.

Mid-session (2026-05-01, radiotoggle + togglegroup):

- `radiotoggle.md` rewritten. RadioToggle is a RadioButton subclass
  with `ttk_class='Toolbutton'` (NOT `class_='Toolbutton'` like
  CheckToggle). The bindtag distinction matters: RadioToggle keeps
  the `TRadiobutton` bindtag (and therefore the stock `<Up>`/
  `<Down>` arrow traversal via `ttk::button::RadioTraverse`),
  while CheckToggle changes its actual `class_` and loses the
  `TCheckbutton` bindtag (no arrow traversal). 3 real Toolbutton
  variants (default/solid/outline/ghost) — same as CheckToggle.
- `togglegroup.md` rewritten. ToggleGroup is the segmented-strip
  companion to RadioGroup, but mode-driven: `mode='single'` builds
  RadioToggle children sharing a StringVar; `mode='multi'` builds
  CheckToggle children sharing a SetVar. Position-aware ButtonGroup
  styling (`before`/`center`/`after`) gives the strip rounded outer
  corners and square inner edges — `_update_button_positions()`
  re-segments after every add/remove.
  Several differences from RadioGroup: no `text=`/`labelanchor=`
  group label (raises TclError); no `state=` configure at the group
  level (per-child via `configure_item`); `remove(key)` is silent
  on miss (RadioGroup raises KeyError); ToggleGroup correctly
  forwards `accent` at construction because the implementation
  explicitly restores `self._accent` after `super().__init__()`
  (lines 96-98 of the source) — RadioGroup is missing that fix
  today and the bug there remains; `mode` is construction-only.
  Surfaced 1 new bug (`set(...)` doesn't validate against known
  keys — str-type check only; `g.set('unknown')` writes the orphan
  value through and no child paints selected).

Mid-session (2026-05-01, optionmenu):

- `optionmenu.md` rewritten. OptionMenu is a MenuButton subclass
  that opens a ContextMenu of radiobutton items sharing one
  StringVar. Frames it as "button + popup menu, simpler than
  SelectBox." Surfaced 3 new bugs:
  (1) `<<Change>>` and `command=` fire **twice** per write —
  `_bind_change_event` is called twice during `__init__` (once
  indirectly via `self.configure(textvariable=self._textvariable)`
  → `_delegate_textsignal`, and once explicitly at the end of
  `__init__`). The `if self._bind_id is not None` guard runs
  against `self._bind_id`, but only the second call assigns the
  result — so the first call's bind_id is never tracked or
  unsubscribed. Net effect: 2 subscribers on the textsignal,
  every variable write fires `<<Change>>` twice, and any
  `command=` callback runs twice per change. `on_changed`
  listeners must be idempotent until fixed.
  (2) `set(...)` does not validate against `options=` — same
  shape as the ToggleGroup bug. `m.set('not_in_list')` succeeds,
  writes the orphan value, no menu radiobutton paints selected,
  and `<<Change>>` still fires.
  (3) `value=` clobbers `textsignal=` / `textvariable=` initial
  value. When both are passed, the constructor's `value=` arg
  wins and is written into the bound variable — opposite of
  RadioButton (where signal value wins). Workaround: omit
  `value=` when binding a signal.
  Also documents: variants from MenuButton (solid/outline/ghost/
  text — no link or pill); `density` not exposed at OptionMenu
  level (the underlying MenuButton accepts it but OptionMenu
  doesn't capture it from kwargs); popup positioning (anchor=nw,
  attach=sw, scaled offset; minwidth bumped to button width on
  show); keyboard contract (Return/KP_Enter open the menu; arrow/
  Return/Escape live on the ContextMenu); `set()` always coerces
  to string via `str(value)`.

Pages to review (canonical anchor: `checkbutton.md`):

- [x] `checkbutton.md` — anchor for the selection sweep
- [x] `switch.md` — CheckButton subclass with slider indicator
- [x] `checktoggle.md` — CheckButton subclass with toolbutton chrome
- [x] `radiobutton.md` — mutually-exclusive selection primitive
- [x] `radiogroup.md` — manages a group of radios as one control
- [x] `radiotoggle.md` — RadioButton subclass with toolbutton chrome
- [x] `togglegroup.md` — RadioGroup using toolbutton-style children
- [x] `optionmenu.md` — list-based selection (button + dropdown menu)
- [x] `calendar.md` — date selection grid

(`selectbox.md` was moved to `widgets/inputs/`; it is now tracked
under the inputs sweep, not selection.)

### Widget pages — views (`docs/widgets/views/`, 3 pages) — DONE 3/3 (2026-05-01)

Template: **`widget-navigation-template.md`** (reused, not cloned).
The navigation template's required H2s (`Basic usage` →
`Navigation model` → `Common options` → `Behavior` → `Events` →
`When should I use WidgetName?` → `Related widgets` → `Reference`)
fit all three views pages — keyed-target enumeration plus a
selection-vs-imperative distinction is exactly what PageStack /
TabView / Notebook all need. `views` was added to
`CATEGORY_TEMPLATE_MAP` in `tools/check_doc_structure.py` pointing
at the navigation template, rather than cloning a dedicated
`widget-view-template.md` — the template is general enough that
duplication would just create drift risk. (If a future view widget
needs a meaningfully different "Page model" framing, fork then.)

`pagestack.md` is the canonical anchor for the views sweep, the way
`button.md` / `textentry.md` / `messagedialog.md` / `label.md` /
`frame.md` / `tabs.md` / `tooltip.md` / `checkbutton.md` anchored
their respective categories. PageStack is the foundational
primitive — TabView composes it with Tabs, AppShell exposes it as
`shell.pages`.

Last session (2026-05-01, views sweep started — pagestack anchor):

- `pagestack.md` rewritten to the navigation template. PageStack is
  a `Frame` subclass that owns a registry of keyed pages and shows
  one at a time, plus a linear `(key, data)` history with
  push/back/forward semantics. Restructured around the slim
  navigation arc with `Navigation model` covering keyed pages,
  sequential history, imperative-only observation (no `signal=` /
  `variable=`), and the page lifecycle (mount/unmount events).
  Four runtime-verified bugs surfaced; all four are real API
  gotchas, not just doc gaps:
  (1) `<<PageUnmount>>` is fired without a `data=` argument
  (`composites/pagestack.py:188`), so handlers receive
  `event.data is None` while the other three navigation events
  (`<<PageWillMount>>`, `<<PageMount>>`, `<<PageChange>>`) all
  carry the full payload. Verified at runtime: a binding on
  `<<PageUnmount>>` receives `None`. Either pass the same payload
  (the navigation has the same `prev_page` / `prev_data` /
  `index` info available at line 187) or document the asymmetry.
  Documented as a `!!! warning` in Events; added to the bugs list.
  (2) `<<PageUnmount>>` and `<<PageWillMount>>` fire on the page
  *widget*, not on the PageStack
  (`composites/pagestack.py:188,208`). Tk virtual events do not
  propagate up the parent chain, so binding either event on the
  stack itself silently no-ops. The class docstring at
  `composites/pagestack.py:44-50` lists all four events under
  "Triggered when..." without naming the emission target —
  reading it implies all four bubble to the stack. Same shape as
  the Tabs `<<TabSelect>>` / SideNav `<<ItemInvoked>>` bugs
  already on this list. Documented as a `!!! warning` with the
  correct `page.bind('<<PageUnmount>>', ...)` workaround.
  (3) `stack.remove(key)` orphans history. The implementation
  (`composites/pagestack.py:114-129`) destroys the page widget
  and removes it from `_pages`, but does not rewrite `_history`
  or `_index` (the only history fix-up is clearing `_current` to
  `None` if the removed key was active). Subsequent `back()` or
  `forward()` walking onto the orphan slot raises
  `NavigationError` from `navigate()`'s existence check. Verified
  at runtime: with `history=[a,b,c]`, `index=2`, `current=c`,
  `stack.remove('b')` leaves `history` unchanged; `stack.back()`
  raises `NavigationError: Page b does not exist`. Either rewrite
  history to drop orphan entries (and adjust `_index` accordingly)
  or document the precondition that callers must only remove
  pages outside their active history. Documented as a `!!!
  warning` in Behavior; added to the bugs list.
  (4) `stack.add(key, page, **kwargs)` silently drops `**kwargs`
  when `page=` is provided. The signature is
  `add(self, key, page=None, **kwargs)` and the kwargs only feed
  the auto-created Frame in the `if page is None` branch
  (`composites/pagestack.py:106-107`). Verified at runtime:
  `stack.add('foo', existing_frame, padding=99)` returns the
  passed frame with its original `padding=(5,)`, never `99`.
  Either raise `TypeError` when both `page=` and kwargs are
  passed, or apply the kwargs by calling
  `page.configure(**kwargs)` after registration. Documented as a
  `!!! warning` in Common options; added to the bugs list.
  Also documented (some new, some restated): `add(key,
  widget_with_other_master)` does **not** reparent — verified at
  runtime that `stack.winfo_children()` is empty when the widget's
  `master` is some other frame (the page is registered but never
  visually attached to the stack); caller-supplied `data` keys
  passed to `navigate(data=...)` are silently overwritten when
  they collide with the navigation keys (`page`, `prev_page`,
  `prev_data`, `nav`, `index`, `length`, `can_back`,
  `can_forward`); PageStack does **not** auto-mount the first
  page on `add()` — different from `Tabs` which writes the first
  added value to its selection variable; `replace=True` overrides
  the current entry only when there *is* a current entry, so the
  flag is silently ignored when called with no prior `navigate()`;
  the mount sequence (`_unmount_event` → `pack_forget` →
  `_will_mount_event` → `pack` → `_mount_event` → `_change_event`)
  means `<<PageWillMount>>` fires before geometry-management,
  while `<<PageMount>>` fires after; the `on_page_changed` /
  `off_page_changed` helpers wrap `<<PageChange>>` only — the
  other three events have no helper. Common options consolidates
  into a 4-row table (no widget-specific options; just inherited
  Frame surface).

`tools/check_doc_structure.py --category views` →
3 files checked, 2 still failing (tabview.md and notebook.md);
pagestack.md no longer in the missing-sections list.
`tools/check_doc_snippets.py --run --file
docs/widgets/views/pagestack.md` → 0 failures (7 snippets, 1
executed).

Last session (2026-05-01, tabview sweep — 2/3):

- `tabview.md` rewritten to the navigation template. TabView is the
  second page in the sweep — a `Frame` that owns a `Tabs` bar plus a
  `PageStack`, wired together by a shared `tk.StringVar` so a tab
  click drives `pagestack.navigate(key)` via a variable trace.
  Restructured around the slim navigation arc with `Navigation
  model` covering keyed targets (tabs and pages share the same key,
  the TabItem's `value` *is* the key), random-access selection,
  imperative-only observation (no `signal=` / `variable=` on
  TabView itself), and the auto-select-first-tab semantics. **Five
  runtime-verified bugs surfaced**, three of which are real API
  failures (not just doc gaps):
  (1) **`tabview.remove(key)` always raises `KeyError`.** The
  implementation at `composites/tabs/tabview.py:194` calls
  `self._tabs.remove(tab)` where `tab` is the **TabItem widget**,
  but `Tabs.remove(key: str)` expects a **string key** and looks
  up the dict entry. The dict (`Tabs._tabs`) is keyed by Tabs's
  auto-generated string keys (`tab_0`, `tab_1`, …; TabView calls
  `Tabs.add(...)` with no `key=` so they're auto-generated), so a
  TabItem reference never matches and Tabs raises
  `KeyError: "No tab with key '<TabItem path>'"`. Verified at
  runtime: `tabview.add('home', ...); tabview.remove('home')` →
  KeyError. **The same crash hits the X-button path** because
  `tabview.add(...)` wires the close_command (when `enable_closing`
  / `closable=True`) to `lambda: self.remove(key)` — clicking X on
  a closable tab raises the same KeyError from inside the Tk
  callback. So `enable_closing` is functionally broken in current
  code. Fix: pass the right key. Either look up the Tabs-internal
  key by walking `self._tabs._tabs.items()` and matching on the
  TabItem reference, or change `Tabs.add()` to accept and respect
  a caller-supplied `key=` from TabView. Documented as a `!!!
  danger` block in Behavior; added to the bugs list.
  (2) **`tabview.navigate(key, data=...)` pushes history twice.**
  The implementation at `composites/tabs/tabview.py:218-228` writes
  the key through `self._tab_variable.set(key)` first, which
  triggers the variable trace `_on_tab_selected` → calls
  `self._page_stack.navigate(key)` with **no** data (history push
  #1, with empty data). Then it calls `self._page_stack.navigate(
  key, data=data)` itself (history push #2, with caller data). Net
  effect: two `<<PageChange>>` events fire per call (first with
  empty `data`, second with the caller's), and history grows by
  two entries. Verified at runtime
  (`history=[('home',{}),('files',{}),('home',{}),('home',{'x':1
  })]` after `add('home') add('files') select('files')
  navigate('home', data={'x':1})`). Fix options: (a) skip the
  trace path when `data` is provided and call
  `self._page_stack.navigate(...)` once explicitly, (b) plumb the
  data through the variable trace so the trace handler picks it up
  somehow (cleaner: add a one-shot pending-data slot read and
  cleared by `_on_tab_selected`). Documented as a `!!! warning`
  in Navigation model with the `tabview.page_stack_widget.navigate(
  key, data=...)` workaround; added to the bugs list.
  (3) **`<<TabSelect>>` and `<<TabClose>>` do not fire on TabView.**
  The class docstring at `composites/tabs/tabview.py:23-27` lists
  all four events (`<<TabSelect>>`, `<<TabClose>>`, `<<TabAdd>>`,
  `<<PageChange>>`) under "Events", but only `<<PageChange>>` and
  `<<TabAdd>>` actually reach the TabView (forwarded via
  `on_page_changed` / `on_tab_added` to the inner widgets).
  `<<TabSelect>>` and `<<TabClose>>` are emitted on the individual
  `TabItem` (same shape as the Tabs bug already on the bugs list)
  and Tk virtual events do not propagate up the parent chain — so
  `tabview.bind("<<TabSelect>>", ...)` silently no-ops. Verified at
  runtime. Fix: forward the events with a second `event_generate`
  in `_on_tab_click` / `_on_close_click` paths, or fix the
  docstring and document `tab.bind('<<TabSelect>>', ...)` as the
  correct pattern. Documented as a `!!! warning` in Events; added
  to the bugs list (this one is the same root cause as the Tabs
  bubbling bug, but TabView's docstring repeats the false claim
  for itself).
  Also surfaced (no new bug, just doc fixes vs the existing
  page):
  - the existing page used `tabview.tabs` (no parens) and
    `tabview.page_stack` to refer to the inner widgets, but those
    properties don't exist by those names — `tabview.tabs` is a
    method (returning a tuple of TabItems), and `tabview.page_stack`
    raises `AttributeError`. The actual properties are
    `tabs_widget` and `page_stack_widget`. Fixed in the rewrite.
  - the existing page documented `variant='pill'` as a working
    variant (matching the constructor signature). The TabView
    constructor succeeds, but the very first `add()` call raises
    `BootstyleBuilderError: Builder 'pill' not found for widget
    class 'TabItem.TFrame'`. Same root cause as the Tabs `pill`
    bug already on the list — TabView inherits the bug because it
    constructs a Tabs widget that constructs TabItems with no
    `pill` builder registered. Documented as a `!!! warning` in
    Common options.
  - `tabview.add(key, page=existing, padding=99)` silently drops
    `padding=99` because PageStack's `add()` only feeds kwargs to
    the auto-created Frame in the `page is None` branch — same
    shape as the PageStack kwargs-drop bug already on the list.
    Documented as a Common-options note pointing at the
    PageStack bug.
  - `tabview.select('phantom')` and `tabview.navigate('phantom')`
    are silent no-ops. Validated against `_tab_map` before
    writing the variable. Inconsistent with Tabs's permissive
    `set('phantom')` (which writes the orphan value through), but
    intentional here since TabView would otherwise stack-trace
    further down.

`tools/check_doc_structure.py --category views` →
3 files checked, 1 still failing (notebook.md remains);
tabview.md no longer in the missing-sections list.
`tools/check_doc_snippets.py --run --file
docs/widgets/views/tabview.md` → 0 failures (6 snippets, 1
executed).

Last session (2026-05-01, notebook sweep — final views page,
sweep closed 3/3):

- `notebook.md` rewritten to the navigation template. Notebook is
  the third and final page in the sweep — a thin themed wrapper
  over `tkinter.ttk.Notebook` that adds a key-based tab registry,
  locale-aware tab labels, and a (broken — see below) enriched
  event surface. Restructured around the slim navigation arc with
  `Navigation model` covering the parallel registries
  (`_key_registry`, `_tk_to_key`, ttk's tab list), the three tab
  reference forms (key / index / widget), the imperative-only
  selection model (no `signal=` / `variable=`), and the
  auto-select-first-tab semantics. **Six runtime-verified bugs
  surfaced**, four of which are real API failures (not just doc
  gaps):
  (1) **`on_tab_changed` / `on_tab_activated` /
  `on_tab_deactivated` never fire.** The constructor binds
  `<<NotebookTabChange>>` (present tense, no `'d'`) at
  `widgets/primitives/notebook.py:570,485,509`, but Tk's underlying
  ttk.Notebook emits `<<NotebookTabChanged>>` (past tense, with
  `'d'`). Verified at runtime: binding directly to
  `<<NotebookTabChanged>>` fires on programmatic and click
  selection, but `nb.on_tab_changed(cb)` never fires. The wrapper
  that synthesizes the activate / deactivate events for the
  lifecycle pair is also bound to the wrong name, so they're
  never generated either — the entire enriched event mechanism is
  dead. The internal `_last_selected` /
  `_last_change_reason` / `_last_change_via` state is maintained
  but never observed. Documented as a `!!! danger` block in
  Events with the workaround (bind directly to
  `<<NotebookTabChanged>>` and read selection state from the
  widget); added to the bugs list.
  (2) **`nb.remove(tab)` and `nb.forget(tab)` always raise
  `TypeError`.** MRO conflict: `WidgetCapabilitiesMixin.forget`
  appears in the MRO before `tkinter.ttk.Notebook.forget`, and the
  former takes no positional arguments (it's the
  `pack_forget`/`grid_forget` shim). Calling
  `super().forget(tabid)` from `Notebook.remove` /
  `Notebook.forget` therefore raises
  `TypeError: WidgetCapabilitiesMixin.forget() takes 1 positional
  argument but 2 were given`. Verified at runtime. `nb.hide(tab)`
  works because there's no upstream `hide` override — only `forget`
  has the conflict. Documented as a `!!! danger` block in Behavior
  with a workaround (`tkinter.ttk.Notebook.forget(nb, tabid)` plus
  manual registry cleanup); added to the bugs list.
  (3) **Failed `add()` / `insert()` leaves orphan tabs.** Both
  validation steps inside `_make_key`
  (`widgets/primitives/notebook.py:147-154`) — duplicate-key check
  and empty-string check — run *after* `super().insert()` has
  already added the auto-created Frame to the underlying ttk
  notebook. Verified: a single `nb.add(text='OK', key='ok')` then
  `nb.add(text='Bad', key='')` (raises `ValueError`) leaves
  `nb.keys() == ('ok', '')` and `len(nb.tabs()) == 2`. The orphan
  tab has no entry in `_key_registry` / `_tk_to_key` and no public
  way to remove it (the broken `remove()` aside). Either validate
  the key before `super().insert()`, or roll back the ttk insert
  on validation failure. Documented as a `!!! warning` in
  Behavior; added to the bugs list.
  (4) **`add()` / `insert()` with an existing widget silently
  drops extra kwargs.** When the first positional argument is
  `None`, kwargs flow into `Frame(self, **kwargs)` (correct).
  When a widget is passed, the kwargs are not applied to it.
  Verified: `existing = ttk.Frame(nb, padding=5);
  nb.add(existing, key='x', text='X', padding=99)` leaves
  `existing.cget('padding') == (5,)`. Same shape as the PageStack
  kwargs-drop bug already on this list. Either raise `TypeError`
  or call `widget.configure(**kwargs)` post-registration.
  Documented as a `!!! warning` in Common options; added to the
  bugs list.
  Also documented (some new, some restated): the four registered
  variants (`default`, alias `tab`; `bar`; `pill` — all work,
  unlike the Tabs `pill` bug); no `orient=` option (Notebook is
  horizontal-only — verified `TclError: unknown option "-orient"`,
  the `# TODO add styles in the future that are geared towards
  left direction navigation` in `style/builders/notebook.py:6`
  still applies); auto-select-first-tab on initial `add()`;
  duplicate keys raise `NavigationError`; empty-string keys raise
  `ValueError`; auto-key naming (`tab1`, `tab2`, … never
  reused for the lifetime of the notebook); the locale-token
  registry that re-translates tab labels on
  `<<LocaleChanged>>`; `tab()` / `configure_item()` aliasing;
  `forget()` vs `remove()` registry semantics (when they work —
  `remove()` clears all three registries; `forget()` only clears
  the locale token); the trip-up where `_to_tab_id` falls back to
  treating an unknown string as a Tk widget path (the source of
  "Invalid slave specification" errors when stale keys escape
  caller bookkeeping).

`tools/check_doc_structure.py --category views` → 3 files
checked, all pass.
`tools/check_doc_snippets.py --run --file
docs/widgets/views/notebook.md` → 0 failures (10 snippets, 1
executed).

Pages to review (canonical anchor: `pagestack.md`):

- [x] `pagestack.md` — anchor for the views sweep
- [x] `tabview.md` — composes Tabs + PageStack
- [x] `notebook.md` — wraps `ttk.Notebook` with key-based registry

### Widget pages — primitives (`docs/widgets/primitives/`, 5 pages) — DONE 5/5 (2026-05-01)

The primitives directory is **not** in `CATEGORY_TEMPLATE_MAP`
(`tools/check_doc_structure.py`), so no template enforcement applies
— same freedom as `widgets/application/`. Per-page template
assignment is by closest fit:

| Page | Closest template | Notes |
|---|---|---|
| `entry.md` | input template | foundational input primitive; backs TextEntry / NumericEntry / DateEntry / PasswordEntry |
| `combobox.md` | input template | thin `ttk.Combobox` wrapper; used by QueryBox dialogs (NOT SelectBox — SelectBox builds its own popdown) |
| `spinbox.md` | input template | thin `ttk.Spinbox` wrapper; primitive backing SpinnerEntry (NumericEntry uses TextEntryPart, not Spinbox); also used by ColorChooser dialog |
| `text.md` | bespoke (Content model) | multi-line `tkinter.Text`; primitive backing ScrolledText |
| `canvas.md` | bespoke (Drawing model) | drawing primitive; backs Meter / FloodGauge and any custom rendering |

The framing across all five pages: **acknowledge the primitive,
recommend the composite for app-level UX, and only document the raw
ttk surface as the place to drop down to when building a custom
composite or needing a Tk option the composite doesn't expose.**

`entry.md` is the canonical anchor (the way `button.md` /
`textentry.md` / `messagedialog.md` / `label.md` / `frame.md` /
`tabs.md` / `tooltip.md` / `checkbutton.md` / `pagestack.md`
anchored their respective categories). The other four primitive
pages should follow its arc.

Last session (2026-05-01, entry sweep started — primitives anchor):

- `entry.md` rewritten to the slim input arc. Entry is the
  foundational input primitive — a thin themed wrapper over
  `ttk.Entry` that adds `accent` / `density` / `surface` styling
  tokens and a reactive `textsignal` channel via `TextSignalMixin`.
  Three things the old page got wrong or omitted, three of which
  became new bugs:
  (1) the old `Appearance` section listed `accent` and `style` as
  the only styling knobs and never described the actual surface.
  Verified at runtime: only the `default` variant is registered
  (`style/builders/entry.py:19` — `register_builder('default',
  'TEntry')`); `Entry(variant='solid')` raises
  `BootstyleBuilderError`. The `surface` token is accepted at
  construction but **`entry.configure(surface=...)` raises
  `TclError: unknown option "-surface"`** — Entry has no
  `_delegate_surface`, so the only post-construction path is the
  `entry.configure_style_options(surface='primary')` escape hatch
  (which Frame's surface-cascade hook also drives). Documented in
  Common options and Behavior; added to the bugs list.
  (2) the old page never described the `density` axis or its
  reconfigure quirk. Verified at runtime that
  `entry.configure(density=...)` updates only the **font** —
  `_delegate_density` (`widgets/primitives/entry.py:94-103`) calls
  `self.configure(font='caption' or 'body')` and writes the new
  density into `_style_options`, but does **not** rebuild the
  resolved ttk style. Net effect: a default-density Entry
  reconfigured to compact keeps `Default.TEntry` as its style (no
  hash prefix at all in the vanilla case, or the original
  `bs[hash].Default.TEntry` style otherwise) and renders with the
  default-density image element + padding. Only the font shrinks.
  Documented as a `!!! warning` in Behavior; added to the bugs
  list.
  (3) the old page never noted that `input_background` is **not** a
  constructor kwarg on `Entry` — it's only reachable via
  `style_options={'input_background': '...'}` or by inheriting from
  a parent `Frame(input_background=...)`. The Frame surface-cascade
  hook (`_refresh_descendant_input_backgrounds`) propagates the
  parent value at construction. Documented in Common options as a
  `!!! note` block.
  Also documented (some new, some restated): the lazy
  `textsignal`/`textvariable` creation when neither is passed; the
  `textsignal` wins over `textvariable` precedence; the
  `state="readonly"` semantics (selection works, typing does not,
  focus traversal still includes); the `cget('variant')` returning
  `None` (variant tokens aren't round-tripped through Tk options);
  `entry.configure(accent=...)` does rebuild the style correctly;
  the `density='compact'` pre-init sets `font='caption'` in
  `__init__` (`entry.py:89-91`) — that's the construction-time
  path that works; the deliberate negative `Events` section (no
  `<<Change>>`, no `on_*` helpers — Entry is a passthrough; framework
  events live on TextEntry).

`tools/check_doc_snippets.py --run --file
docs/widgets/primitives/entry.md` → 0 failures (5 snippets, 1
executed). No structure check (primitives is not in
`CATEGORY_TEMPLATE_MAP`).

Last session (2026-05-01, combobox sweep — 2/5):

- `combobox.md` rewritten to the slim input arc, anchored on
  `entry.md`. Combobox is the second page in the sweep — a thin
  themed wrapper over `ttk.Combobox` that adds `accent` /
  `density` / `surface` / `input_background` styling tokens, a
  reactive `textsignal` channel via `TextSignalMixin`, and a
  postcommand wrapper that re-styles the popdown on every open
  and on `<<ThemeChanged>>` (without it the popdown's embedded
  listbox/scrollbar would not track theme changes — that's the
  main thing the wrapper adds beyond `ttk.Combobox`). Three
  things the old page got wrong or omitted:
  (1) the old page (and the original primitives table in this
  doc) framed Combobox as the primitive backing SelectBox.
  Verified by grep: only `dialogs/query.py` (QueryBox) imports
  `Combobox` from `widgets.primitives`; SelectBox builds its
  own popdown out of a `TextEntryPart` + a custom popup
  (`composites/selectbox.py`), not on `ttk.Combobox` at all.
  Reframed Combobox as the "drop down to ttk" path, not as the
  SelectBox backbone, and corrected the Notes column in the
  primitives table above.
  (2) the old page never described the actual styling surface.
  Only the `default` variant is registered (`Combobox(variant=
  'solid')` raises `BootstyleBuilderError`); `surface` and
  `density` are accepted at construction; `input_background` is
  not a constructor kwarg — pass it via `style_options=
  {'input_background': '...'}` or set it on a parent
  `Frame(input_background='...')` for cascade. Verified at
  runtime that the cascade works.
  (3) the old page treated `state='readonly'` as a value
  constraint. It only constrains *user typing* — programmatic
  `combo.set('orphan')` on a readonly Combobox writes the orphan
  string through, paints it as plain text, and `current()`
  returns `-1`. Same family as the SelectBox / OptionMenu /
  ToggleGroup orphan-value bugs already on the bugs list, but
  this is the standard ttk.Combobox contract — documented as
  expected behavior rather than a bug.
  Surfaced two configure-time issues (already on the bugs list
  for Entry; same root cause in Combobox):
  - `combo.configure(surface=...)` raises `TclError: unknown
    option "-surface"` — Combobox accepts `surface=` at
    construction but has no `_delegate_surface`.
  - `combo.configure(density=...)` updates the entry's font
    only; the resolved ttk style is not rebuilt, so the
    underlying image element key and padding from the
    construction-time density persist. Default-density
    Comboboxes reconfigured to `compact` get the smaller
    caption font but keep their default-height row. Verified
    at runtime.
  Documented as Behavior caveats with cross-references rather
  than logging duplicate bug entries — they're the same shape
  as the Entry bugs already on the list.
  Also documented: `<<ComboboxSelected>>` fires only on user
  selection from the dropdown (not on `combo.set(...)`, not on
  user typing — verified at runtime); the postcommand wrapper
  preserves the user's `postcommand=` callback (calls it after
  the styling pass); `current()` returns `-1` when the text
  doesn't match any value in `values`; `cget('density')` /
  `cget('accent')` / `cget('surface')` all return `None` for
  the Python-side options (different from `cget('variant')`
  which returns the literal `'default'`); the deprecated
  `bootstyle=` path bridges to `accent=` correctly.

`tools/check_doc_snippets.py --run --file
docs/widgets/primitives/combobox.md` → 0 failures (2 snippets,
1 executed). No structure check (primitives is not in
`CATEGORY_TEMPLATE_MAP`).

Earlier session (2026-05-01, spinbox sweep — 3/5):

- `spinbox.md` rewritten to the slim input arc, anchored on
  `entry.md`. Spinbox is the third page in the sweep — a thin
  themed wrapper over `ttk.Spinbox` that adds `accent` /
  `density` / `surface` / `input_background` styling tokens and
  a reactive `textsignal` channel via `TextSignalMixin`. Unlike
  Combobox, Spinbox does **not** wrap any popdown / postcommand
  machinery — it's purely a styling and signal-binding wrapper.
  Three things the old page got wrong or omitted:
  (1) the old page (and the primitives table in this doc) said
  Spinbox is the primitive backing NumericEntry / SpinnerEntry.
  Verified by grep: `widgets/parts/spinnerentry_part.py:12`
  imports Spinbox, but `widgets/composites/numericentry.py`
  imports `Button` only — NumericEntry uses TextEntryPart, not
  Spinbox. Reframed: Spinbox backs SpinnerEntry only; also used
  by `dialogs/colorchooser.py` and `widgets/composites/form.py`.
  Corrected the Notes column in the primitives table.
  (2) the old page treated `command=` as a generic "value
  changed" callback. Verified at runtime that `command=` fires
  **only on stepping** (arrow click, Up/Down key, programmatic
  `<<Increment>>` / `<<Decrement>>`). It does NOT fire on
  `spin.set(...)`, on user typing, or on focus events. Same
  shape as Combobox's `<<ComboboxSelected>>` (only on dropdown
  selection). Documented as a four-row table in Events covering
  the four observation paths (command callback, virtual events,
  textsignal, KeyRelease).
  (3) the old page treated `state="readonly"`, `from_/to=`, and
  `format=` as value constraints. Verified at runtime:
  - `spin.set(99)` on a `from_=0, to=10` Spinbox writes `'99'`
    through unchanged (no clamping at all).
  - `format='%.2f'` reformats values **only when stepping**
    (arrow click, Increment/Decrement). `spin.set(0.5)` writes
    `'0.5'` literally even with `format='%.2f'` set.
  - `state='readonly'` blocks user typing only — programmatic
    `set()` accepts any value, including out-of-range and
    not-in-`values`.
  Documented as a unified Value-model section emphasizing that
  Spinbox does no parsing, clamping, or formatting on its own —
  the validation surface is on SpinnerEntry / NumericEntry.
  Surfaced two configure-time issues (already on the bugs list
  for Entry; same root cause in Spinbox):
  - `spin.configure(surface=...)` raises `TclError: unknown
    option "-surface"` — Spinbox accepts `surface=` at
    construction but has no `_delegate_surface`.
  - `spin.configure(density=...)` updates the entry's font
    only; the resolved ttk style is not rebuilt. Verified at
    runtime: `Spinbox(...).configure(density='compact')` →
    style stays `Default.TSpinbox` (no hash) with font
    `caption`. Default-density Spinboxes reconfigured to
    compact get the smaller font but keep their
    default-height row.
  Documented as Behavior caveats with cross-references rather
  than logging duplicate bug entries — they're the same shape
  as the Entry bugs already on the list.
  Also documented: when both `values=` and `from_/to=` are
  passed, `values` wins for stepping but both round-trip via
  `cget`; default `increment` is `1`; `cget('density')` and
  `cget('variant')` both return `None` (different from Combobox
  where `cget('variant')` returns `'default'`); the deprecated
  `bootstyle=` path bridges to `accent=` correctly; the stepping
  pipeline (read → +/- increment OR list-position → clamp/wrap →
  format → write → fire command + virtual event).

`tools/check_doc_snippets.py --run --file
docs/widgets/primitives/spinbox.md` → 0 failures (6 snippets,
1 executed). No structure check (primitives is not in
`CATEGORY_TEMPLATE_MAP`).

Earlier session (2026-05-01, text sweep — 4/5):

- `text.md` already in good structural shape from a prior pass;
  this session was an accuracy and precision pass, not a full
  rewrite. The page follows the bespoke Content-model arc
  prescribed for text/canvas (intro → Basic usage → Content
  model → Common options → Behavior → Events → Patterns → When
  → Related → Reference). `ttk.Text is tk.Text` (re-export, not
  a subclass); the framework integration is the install-time
  wrapper `Bootstyle.override_tk_widget_constructor` applied to
  `tk.Text`, which captures `autostyle` / `inherit_surface` /
  `surface` kwargs, sets `_surface` on the widget, then calls
  the registered `Text` builder
  (`style/builders_tk/defaults.py:66-86`) to paint theme colors
  and registers the widget for `<<ThemeChanged>>`. Three
  precision fixes vs the prior version, one of which surfaced
  a new bug:
  (1) the prior page conflated `surface=` / `inherit_surface=`
  semantics. Verified at runtime that `inherit_surface=True`
  (the default — pulled from `AppSettings.inherit_surface_color`
  at `style/bootstyle.py:561-563`) **silently overrides** the
  explicit `surface=` argument with the parent's
  `_surface`. Net effect: `ttk.Text(parent, surface='card')`
  with default `inherit_surface=True` ends up with
  `_surface='content'` (parent's surface), NOT `'card'` —
  callers must also pass `inherit_surface=False` to pin a
  surface explicitly. Documented as a `!!! warning` block in
  the Autostyle keywords subsection; added to the bugs list.
  (Worth noting: this same pattern likely affects every
  Tk-class autostyle widget — Frame/Label/Button/Entry/Text/
  Canvas/Listbox/Menu/etc. — but I only verified it on Text.)
  (2) the prior page said "the autostyle wrapper sets
  `option_add('*Text*Font', 'TkDefaultFont')` on the root
  window so every Text widget picks up the framework's default
  text font." The `option_add` call actually lives in the
  root-window `Tk` builder (`style/builders_tk/defaults.py:12`),
  invoked once at App construction — not in the per-Text
  wrapper. Reworded to attribute it correctly. The end-user
  effect is the same (every Text gets `TkDefaultFont` instead
  of Tk's stock `TkFixedFont`), but the previous wording
  implied the per-Text wrapper sets it on every construction.
  Verified runtime defaults: `padx=5`, `pady=5`,
  `highlightthickness=0`, `font='TkDefaultFont'`. With
  `autostyle=False`: `padx=1`, `highlightthickness=3` (Tk
  defaults) but `font='TkDefaultFont'` still applies because
  the root-level `option_add` already ran.
  (3) clarified that `_surface` is captured even when
  `autostyle=False` (verified — `style/bootstyle.py:580` runs
  before the `if not auto_style: return` guard at line 582).
  The widget is not registered for `<<ThemeChanged>>` and the
  builder is not called, but `widget._surface` is still
  populated. Worth knowing for callers who roll their own
  styling and want to read the captured surface token.
  Also verified: the existing `!!! warning` about `surface=`
  not tinting the Text widget is correct — the Text builder
  reads `'background'` directly (the page-level theme token),
  ignoring the `surface` argument that other builders honor
  (Frame, Label, Canvas, etc. all read
  `options.get('surface', 'content')`). Reworded the warning
  to lead with `_surface` rather than `surface=` since the
  inheritance path means `_surface` is the relevant axis even
  when no `surface=` was passed; the painted background is
  always the page background regardless.
  Other accuracy items confirmed at runtime and kept on the
  page:
  - `state="disabled"` silently no-ops both user input AND
    programmatic `insert()` / `delete()` (`text.insert('end',
    ' world')` on a disabled widget returns no error and
    leaves content unchanged).
  - `accent` / `variant` / `density` are not valid kwargs —
    each raises `TclError: unknown option "-<name>"`.
  - `<<Modified>>` fires once per transition from clear to set
    (re-armed by `text.edit_modified(False)`); does not fire
    while disabled.
  - `ttk.IntVar` is exported (referenced in the
    `text.search(..., count=ttk.IntVar())` example).
  - `Listbox` is **not** exported by `ttk` (`hasattr(ttk,
    'Listbox') is False`). Only `ListView` is. The Tk builder
    for `Listbox` exists in
    `style/builders_tk/defaults.py:142-159` for users who pull
    `tk.Listbox` directly, but ttkbootstrap ships no top-level
    re-export.

`tools/check_doc_snippets.py --run --file
docs/widgets/primitives/text.md` → 0 failures (11 snippets,
1 executed). No structure check (primitives is not in
`CATEGORY_TEMPLATE_MAP`).

Last session (2026-05-01, canvas sweep — 5/5, sweep closed):

- `canvas.md` rewritten to the slim primitives arc anchored on
  `text.md`, then expanded per the user's mid-session note that
  Canvas warrants a more expansive write-up given its nature.
  Canvas is the fifth and final page in the sweep — `tk.Canvas`
  re-exported from the top-level namespace
  (`ttkbootstrap.Canvas is tkinter.Canvas` — verified at
  runtime), styled by the same `Bootstyle.override_tk_widget_constructor`
  wrapper that handles Text and Listbox. The Canvas-specific
  builder (`style/builders_tk/defaults.py:89-92`) reads
  `options.get('surface', 'content')` and writes `background`
  + `highlightthickness=0`. **Unlike Text**, Canvas honors
  `surface=` in the painted output — a Canvas in a
  `Frame(surface='card')` actually paints with the card
  background. Documented as a positive distinction from Text in
  the Autostyle keywords subsection.
- Confirmed at runtime that the `inherit_surface` overrides
  `surface=` bug surfaced by text.md applies identically to
  Canvas: `Canvas(parent, surface='card')` with default
  `inherit_surface=True` ends up with `_surface='content'`
  (parent's surface), background `#ffffff` (page background).
  Adding `inherit_surface=False` produces the expected `_surface=
  'card'`, background `#f5f5f5`. This is the same wrapper-level
  bug already on the bugs list (logged by text.md sweep) — not
  a new entry; just additional confirmation that it spans every
  Tk-class autostyle widget.
- Three additional accuracy items confirmed at runtime:
  (1) **Canvas-level `state="disabled"` does NOT block
  programmatic edits.** Verified: `Canvas(state='disabled')`
  still allows `create_*`, `coords()`, `move()`, `delete()` to
  proceed. What it does is restyle items into their
  `disabledfill` / `disabledoutline` colors and stop delivering
  events to tag and item bindings. Different from `tk.Text`
  where disabled silently no-ops `insert`/`delete`. Items have
  their own independent `state` axis (`normal` / `disabled` /
  `hidden`); per-item `state="hidden"` is the right tool for
  hiding without losing the item id, tags, or bindings.
  (2) **`autostyle=False` defaults change.** With
  `autostyle=True` (default): `highlightthickness=0`,
  `background='#ffffff'` (resolved surface). With
  `autostyle=False`: `highlightthickness=3`,
  `background='systemWindowBackgroundColor'` (Tk defaults). The
  `_surface` attribute is still captured.
  (3) `accent`, `variant`, `density` all rejected with
  `TclError: unknown option "-<name>"`. Documented as not
  valid kwargs.
- Per-user expansion (deeper than the slim primitives arc
  prescribes):
  - Item-types subsection under Drawing model with per-type
    options for line (`arrow`/`smooth`/`splinesteps`/`capstyle`/
    `joinstyle`), arc (`start`/`extent`/`style`), text
    (`anchor`/`justify`/`width`), polygon (`smooth`),
    image (PIL routing), bitmap (built-in names), window
    (parent-must-be-canvas precondition).
  - Common-item-options table (state, tags, activefill /
    activeoutline / activewidth, disabledfill / disabledoutline /
    disabledwidth, stipple / outlinestipple, dash /
    dashoffset).
  - Stacking-order subsection (`tag_raise` / `tag_lower` /
    `find_above` / `find_below`).
  - Patterns: rubber-band selection rectangle (`find_enclosed`
    + `dash` outline), snap-to-grid (round to step, pair with
    `xscrollincrement`), animation via `after` (mutate in
    place, no `update()` in the loop), embedded child widgets
    (`create_window` parent precondition, bbox semantics,
    bindings precedence), image embedding via PIL (the
    `c.image_ref = img` reference-keeping idiom that prevents
    GC), PostScript export option surface.
  - Dedicated Performance section breakout with six numbered
    rules (mutate-not-recreate, tag-every-group, hide-instead-
    of-delete, `bbox` is O(n), virtualize past ~10k items,
    batch-then-yield).
  - More Behavior content: theme reapplication only resets
    `background` and `highlightthickness` (item colors are not
    theme-managed); `scrollregion=()` resets but `None` is
    undefined; stale ids resolve to nothing rather than
    raising.

`tools/check_doc_snippets.py --run --file
docs/widgets/primitives/canvas.md` → 0 failures (17 snippets,
1 executed). No structure check (primitives is not in
`CATEGORY_TEMPLATE_MAP`).

**Sweep closed.** All 5 primitive pages now follow the slim
input arc anchored on `entry.md` (with `text.md` and `canvas.md`
expanded beyond the slim arc per the user's note about their
power and uniqueness — the bespoke "Content model" / "Drawing
model" sections plus dedicated Performance breakouts and richer
Patterns sections).

Last session (2026-05-01, text.md expansion follow-up):

- `text.md` expanded beyond the slim arc to match the depth of
  the canvas.md expansion. The page grew from 11 → 25 snippets,
  with the following new and expanded subsections:
  - Indices — added long-form modifier syntax (`5 chars` /
    `1 lines`), display-vs-logical chars/lines, `@x,y` screen
    coordinate, modifier chaining rules, `text.count()` units
    (chars / displaychars / lines / displaylines / indices /
    displayindices / xpixels / ypixels).
  - Tags — added the full `tag_configure` styling option matrix
    as a 16-row table (font / foreground / background /
    selectforeground / selectbackground / underline / overstrike
    / underlinefg / overstrikefg / relief / borderwidth /
    justify / lmargin1 / lmargin2 / rmargin / lmargincolor /
    rmargincolor / spacing1 / spacing2 / spacing3 / wrap / tabs
    / tabstyle / elide / bgstipple / fgstipple / offset). Added
    `tag_nextrange` / `tag_prevrange` walking pattern and the
    note about the `"sel"` special tag for selection mutation.
  - Marks — added the method-surface table
    (mark_set / mark_unset / mark_gravity / mark_names /
    mark_next / mark_previous), default-gravity rule
    (user-created marks default to `right`), the `tk::` /
    project-prefix naming convention.
  - Embedded objects — documented `window_create` options
    (`align` / `padx` / `pady` / `stretch` / `create=callable`
    deferred-instantiation), `image_create` options
    (`align` / `padx` / `pady` / `name=`), the parent-must-be-
    text precondition for windows, the image-reference-keeping
    idiom (`text.image_ref = img`), and the `text.dump(…,
    window=True)` tool for finding embeds.
  - **NEW: Selection** subsection under Content model —
    `tag_ranges("sel")` / `tag_add("sel", …)` /
    `tag_remove("sel", …)`, the cursor (`"insert"` mark) vs
    selection distinction, `text.see(index)` for scroll-to.
  - Undo and editing model — expanded with the full method-
    surface table (edit_undo / edit_redo / edit_separator /
    edit_reset / edit_modified / edit("undo" / "redo")) and
    `autoseparators=True` heuristic notes.
  - Tag-bound events — added the return-`"break"` pattern for
    suppressing class bindings under tag handlers.
  - **NEW: Search** section after Events — full option
    reference (forwards / backwards / exact / regexp / nocase /
    elide / count / stopindex), the canonical "find every
    match" loop with zero-width-match guard.
  - **NEW: Scrolling** section — view methods table (xview /
    yview / xview_moveto / yview_moveto / xview_scroll /
    yview_scroll / see / scan_mark / scan_dragto), scrollbar-
    pairing symmetry note (without `yscrollcommand=sb.set`,
    other scroll paths leave the scrollbar thumb stale).
  - Patterns — added line-numbers gutter (paired Text widget,
    yview sync), syntax highlighting (regex pass per
    `<<Modified>>`, with note on incremental scoping), find-
    and-replace (with `edit_separator` boundaries for one-shot
    undo), inline-widget embedding via `window_create`,
    save/restore selection via `tag_ranges("sel")`.
  - **NEW: Performance** section before "When should I use
    Text?" — eight numbered rules (batch inserts, single
    redraw window, tag-once-configure-many, tag stacking
    matters, `<<Modified>>` once-per-transition gotcha, cap
    buffer for log views, `see` over `yview_moveto` for tail
    UIs, `dump` is for serialization not normal reads).

`tools/check_doc_snippets.py --run --file
docs/widgets/primitives/text.md` → 0 failures (25 snippets, 1
executed). No structure check (primitives is not in
`CATEGORY_TEMPLATE_MAP`).

Pages to review (canonical anchor: `entry.md`):

- [x] `entry.md` — anchor for the primitives sweep
- [x] `combobox.md` — thin `ttk.Combobox` wrapper
- [x] `spinbox.md` — thin `ttk.Spinbox` wrapper
- [x] `text.md` — multi-line text primitive (expanded arc per user note)
- [x] `canvas.md` — drawing primitive (expanded arc per user note)

### Platform pages (`docs/platform/`, 17 pages) — DONE 17/17 (2026-05-01)

Architectural pages — not in `CATEGORY_TEMPLATE_MAP`, no template
enforcement. The structural convention that emerged: most pages
benefit from replacing abstract "Tk has X" framing with concrete,
verified-at-runtime facts about ttkbootstrap's actual API surface.

**Cross-cutting pattern applied:** every page rewritten in this
sweep grounds claims in runtime checks (capturing actual style
names, default bindtag tuples, autostyle wrapper coverage, etc.).
Snippets all pass `tools/check_doc_snippets.py --run`.

Per-page treatment (commit hashes listed; see commit messages for
the full per-page detail):

| Page | Commit | Treatment | Snippets |
|---|---|---|---|
| `index.md` | `3c59ed9` | Rewrite — topic list rebuilt to match `zensical.toml` nav (added 6 missing pages), broken-indentation list fixed | 0 |
| `tk-vs-ttk.md` | `65dc809` | Rewrite — actual import surface (subclass vs identity), 16 autostyled Tk classes, `inherit_surface` override trap | 3 |
| `event-loop.md` | `d7f63cb` | Rewrite — fixed wrong claim that `wait_*` doesn't recurse the loop, added queue model, `update` vs `update_idletasks` | 4 |
| `events-and-bindings.md` | `f12d6ea` | Rewrite — bindtag walk grounded in runtime tuple, `add="+"` trap, Shortcuts cross-platform `Mod`, non-bubbling virtual events | 10 |
| `geometry-and-layout.md` | `e3df73b` | Rewrite — full pack/grid/place mechanics, `winfo_reqwidth` vs `winfo_width`, propagation rules | 9 |
| `widget-lifecycle.md` | `91e5b8c` | Rewrite — three-phase model (created/managed/mapped), `<<ThemeChanged>>` as lifecycle event, image GC pin idiom | 7 |
| `ttk-styles-elements.md` | `118a1cb` | Rewrite — resolved style name format `bs[<hash>].<accent>.<orient>.<variant>.T<Class>`, `CONTAINER_CLASSES` / `ORIENT_CLASSES` reroute rules, captured `_token` attributes for debugging | 9 |
| `images-and-dpi.md` | `441eae1` | Targeted — full `Image` utility surface, `BootstrapIcon`, intro tightening; per-OS DPI sections kept (Phase 4D) | 9 |
| `platform-differences.md` | `8ca3252` | Light — Quit shortcut row added; cross-link to events-and-bindings; minor tightening (Phase 4B was already comprehensive) | 6 |
| `accessibility.md` | — | Verified, no edits (Phase 4C is already in good shape) | 4 |
| `windows.md` | `d5eea28` | Rewrite — three window classes (App / Toplevel / AppShell), frameless-kwarg inconsistency table, modality split (grab vs wait), `WM_DELETE_WINDOW`, `<Destroy>` filter pattern | 8 |
| `threading-and-async.md` | — | Verified, no edits (Phase 4A is already in good shape) | 8 |
| `debugging.md` | `62b2935` | Targeted — fixed mislabeled `theme_names()` comment; expanded style-debugging vocabulary (Style.layout / lookup / map); added captured token attributes section | 9 |
| `performance.md` | `fe4db05` | Rewrite — five ranked bottlenecks (blocking I/O, eager construction, layout thrashing, image regen, theme switch), lazy construction patterns, measuring via `time.perf_counter` / cProfile | 8 |
| `cli.md` | — | Verified, no edits (PR #1051 left it complete and accurate) | 1 |
| `project-structure.md` | `e013934` | Rewrite — fixed two broken links to nonexistent `docs/build/` pages; CLI-first reframing (canonical `ttkb start` layouts first, manual layout as alternative); added `ttkb.toml` section | 4 |
| `build-and-ship.md` | `271f46b` | Targeted — `[build.datas].include` pattern for assets, `[build.icon].path` schema with per-OS format notes; per-OS shipping sections kept (Phase 4E) | 1 |

Bugs surfaced during the platform sweep (added to the bugs list):

- **Toplevel.__init__ signature footgun.** `Toplevel.__init__(self,
  title="ttkbootstrap", ...)` takes `title` as the first positional
  argument; the master/parent flows through `**kwargs` and is
  passed through to `tkinter.Toplevel.__init__`. Net effect:
  `ttk.Toplevel(app, title="...")` raises
  `TypeError: __init__() got multiple values for argument 'title'`
  because `app` resolves to `title` positionally first. Caught by
  the runtime snippet check on `windows.md`. Workaround: always
  pass `master=app` as a kwarg. The unusual signature is at
  `runtime/toplevel.py:30-47` — every other window class
  (`App`, `AppShell`) puts the master/parent first.
- **`docs/platform/project-structure.md` had two broken admonition
  links** to `../build/app-runtime.md` and
  `../build/app-configuration.md` — there is no `docs/build/`
  directory. Fixed in the project-structure rewrite. Reference
  links elsewhere should be checked next sweep — running
  `tools/check_doc_links.py` would surface any others.
- **The `inherit_surface=True` overrides explicit `surface=`**
  bug surfaced earlier on text.md and canvas.md was confirmed
  to be a wrapper-level issue at `style/bootstyle.py:575-578`,
  affecting every Tk-class autostyle widget (Frame, Label,
  Button, Entry, Text, Canvas, Listbox, Menu, etc.). Only Text
  and Canvas were verified at runtime; documented in
  `tk-vs-ttk.md` as a wrapper-level fact for users. Already on
  the bugs list.

Pages reviewed (in commit order):

- [x] `index.md` — section landing
- [x] `tk-vs-ttk.md` — Tk vs ttk widget systems
- [x] `event-loop.md` — mainloop, after, queues
- [x] `events-and-bindings.md` — bindtags, scopes, add="+"
- [x] `geometry-and-layout.md` — pack/grid/place
- [x] `widget-lifecycle.md` — created/managed/mapped
- [x] `ttk-styles-elements.md` — resolved style names, builders
- [x] `images-and-dpi.md` — Image utility, BootstrapIcon, per-OS DPI
- [x] `platform-differences.md` — per-OS behavior matrix
- [x] `accessibility.md` — keyboard nav, focus rings (verified)
- [x] `windows.md` — App / Toplevel / AppShell
- [x] `threading-and-async.md` — worker patterns (verified)
- [x] `debugging.md` — logging, exceptions, style introspection
- [x] `performance.md` — five bottleneck patterns
- [x] `cli.md` — `ttkb` command surface (verified)
- [x] `project-structure.md` — CLI-first layout
- [x] `build-and-ship.md` — packaging + shipping

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
- `SideNav.select(key)` does **not** validate `key`. The bound
  variable is set unconditionally, the `<<SelectionChanged>>` event
  fires with `event.data = {"key": key}`, and `selected_key`
  returns the orphan key — but no item paints as selected because
  `_on_selection_changed` (`composites/sidenav/view.py:402-410`)
  gates the visual update on `key in self._items` /
  `self._footer_items`. Verified at runtime:
  `nav.select('phantom')` → `nav.selected_key == 'phantom'` and
  the bar paints nothing as active. Either validate against
  `node_keys()` / `footer_node_keys()` and raise on miss, or no-op
  silently. Same shape as the Tabs orphan-key bug already on this
  list. (Surfaced by sidenav.md rewrite, 2026-05-01.)
- `SideNav(display_mode='minimal')` does **not** start hidden. The
  conceptual framing of `minimal` is "hidden until toggled" (and
  `_apply_display_mode` at `composites/sidenav/view.py:311-317`
  hides the pane only when `is_pane_open=False`), but the
  constructor default for `is_pane_open` is `True`
  (`view.py:110`). So a vanilla
  `SideNav(display_mode='minimal')` shows the pane in full at
  startup, identical to `expanded` mode. Either default
  `is_pane_open=False` when `display_mode='minimal'`, or rename
  the mode to better reflect that the visibility is independently
  controlled. (Surfaced by sidenav.md rewrite, 2026-05-01.)
- `SideNav.toggle_pane()` does **different things** depending on
  `display_mode`. In `expanded` mode it switches to `compact` (and
  vice versa) emitting `<<DisplayModeChanged>>`
  (`composites/sidenav/view.py:796-799`). Only in `minimal` mode
  does it toggle pane visibility, emitting `<<PaneToggled>>`
  (`view.py:791-795`). Verified at runtime: starting from
  `expanded`, `toggle_pane()` → `display_mode == 'compact'`,
  `is_pane_open` still `True`. The default hamburger button
  AppShell wires up calls `toggle_pane()` directly
  (`appshell.py:165` → `appshell._toggle_nav` →
  `nav.toggle_pane()`), so users in `expanded` mode who click the
  hamburger expecting "hide the sidebar" get a shrink to icon-only
  instead. Either rename / split the method (e.g. `cycle_mode()`
  for the expanded↔compact dance and `toggle_visibility()` for
  open / close), or document the dual semantics prominently and
  rewire AppShell's hamburger to use `open_pane()` / `close_pane()`.
  (Surfaced by sidenav.md rewrite, 2026-05-01.)
- `SideNav(display_mode='compact', pane_width=N)` silently ignores
  `pane_width=N`. The `compact` branch of `_apply_display_mode`
  (`composites/sidenav/view.py:308-310`) hard-codes
  `width=self.PANE_WIDTH_COMPACT` (52 px) and writes that into the
  pane frame regardless of the constructor's `pane_width`
  argument. Verified at runtime: pane width is 52 px even when
  `pane_width=400`. Either honor `pane_width` in compact mode (so
  callers can build a wider icon strip), or accept a separate
  `compact_pane_width=` argument. (Surfaced by sidenav.md rewrite,
  2026-05-01.)
- `Toolbar.add_widget(widget)` does **not** validate that `widget`
  is parented to `toolbar.content`. The source docstring
  (`widgets/composites/toolbar.py:329-345`) says the widget must be
  parented to `toolbar.content`, but the implementation only calls
  `widget.pack(**pack_kwargs)` (lines 342-344). A widget parented to
  any other frame still gets packed, but at *that* frame's location
  — silently, with no error — so the developer's "I added it to the
  toolbar" mental model breaks invisibly. Verified at runtime:
  `Entry(app)` followed by `tb.add_widget(ent)` packs the Entry into
  `app`, not into `tb.content`. Either reparent with
  `widget.pack(in_=self._content_frame, ...)` so the call still
  works regardless of how the widget was constructed, or raise a
  `ValueError` when `widget.master is not self._content_frame`. The
  silent-misplacement form is the worst option. (Surfaced by
  toolbar.md rewrite, 2026-05-01.)
- **Naming inconsistency across `App` / `Toplevel` / `AppShell` for
  the "remove OS window chrome" option.** `App` exposes
  `override_redirect=True` (with underscore;
  `runtime/app.py:514,554`); `Toplevel` exposes `overrideredirect=True`
  (no underscore, matching Tk's native `wm overrideredirect`;
  `runtime/toplevel.py:40`); `AppShell` exposes `frameless=True`
  (renamed entirely; `composites/appshell.py:61,98,110`). All three
  set the same underlying `wm overrideredirect` attribute. Verified
  at runtime: `App(frameless=True)` raises `TypeError: unexpected
  keyword`; `Toplevel(frameless=True)` raises `TclError: unknown
  option "-frameless"`; `App(override_redirect=True)` and
  `Toplevel(overrideredirect=True)` and `AppShell(frameless=True)`
  all succeed. Either pick one spelling across all three classes
  (most uniform: `frameless=True` everywhere, since it reads as
  intent rather than as a Tk implementation detail), or accept all
  three as aliases on each class. The current state is a tripwire
  for users moving snippets between `App`/`Toplevel`/`AppShell`.
  (Surfaced by toolbar.md rewrite, 2026-05-01.)
- `ToolTip(widget, ...)` silently overwrites any pre-existing
  `<Enter>` / `<Leave>` / `<Motion>` / `<ButtonPress>` binding on
  the target widget. The constructor uses hard binds
  (`widgets/composites/tooltip.py:122-125` — `widget.bind("<Enter>",
  self._on_enter)` etc., without `add="+"`), so a user handler
  attached before the tooltip is silently replaced. Verified at
  runtime: a pre-bound `<Enter>` handler that fires before tooltip
  attachment stops firing afterward (`event_generate("<Enter>")`
  produces no callback hits). Either rewrite the binds with
  `add="+"` so user handlers and tooltip handlers coexist, or
  document the clobbering as deliberate and require users to bind
  *after* attaching the tooltip. (Surfaced by tooltip.md rewrite,
  2026-05-01.)
- `ToolTip` does not support multiple instances on the same widget.
  A second `ToolTip(widget, ...)` call overwrites the first's
  bindings (same hard-bind path as above), so the first instance
  becomes inert — its `_show_tip` never runs because the binding no
  longer points at it. The first instance is also not garbage-
  collected automatically (it retains references through closures).
  Verified at runtime: `t1 = ToolTip(btn, text='first', delay=0)`
  followed by `t2 = ToolTip(btn, text='second', delay=0)` produces
  `t1._toplevel is None` and `t2._toplevel` populated after a
  hover cycle. Either detect a previously-attached tooltip and
  raise / replace deterministically, or use `add="+"` for the
  binds (allowing both tooltips to attempt to show, which is also
  weird). The current silent-takeover form is the worst option.
  (Surfaced by tooltip.md rewrite, 2026-05-01.)
- `Toast.show()` called twice on the same instance leaks the first
  Toplevel. The implementation
  (`widgets/composites/toast.py:184-190`) clears options if
  `merge=False`, then unconditionally calls `_build_toast()` which
  creates a fresh Toplevel and writes it to `self._toplevel` — the
  previous Toplevel is **never destroyed**, just abandoned. Verified
  at runtime: `t.show()` followed by `t.show()` produces two
  `Toplevel` instances, both `winfo_exists() == 1`, and
  `t._toplevel` references only the second. The first stays mapped
  on screen and is garbage-collected only when the application
  exits. Either destroy the previous Toplevel at the top of `show()`
  (call `self.destroy()` first) or document the precondition that
  callers must `hide()` between successive `show()` calls. (Surfaced
  by toast.md rewrite, 2026-05-01.)
- `Toast.configure(bootstyle=...)` is silently a no-op for styling
  after construction. The legacy-bootstyle bridge runs only at
  `__init__` (`widgets/composites/toast.py:102` —
  `self._accent = accent or bootstyle`); subsequent
  `configure(bootstyle=...)` writes `_bootstyle` (since `bootstyle`
  is in `_config_keys`) but does **not** update `_accent`. The next
  `show()` therefore paints with the original accent. Verified at
  runtime: `Toast(bootstyle='success')` → `cget('accent') ==
  'success'`; `t.configure(bootstyle='danger')` → `cget('accent') ==
  'success'` (unchanged). Either route bootstyle reconfiguration
  through `_accent` for consistency, or remove `bootstyle` from
  `_config_keys` to fail loudly. (Surfaced by toast.md rewrite,
  2026-05-01.)
- `Toast.on_dismissed(data)` callback delivers the **full button
  options dict (including the `command` callable!)** when the toast
  is dismissed via a custom button. The wrapper at
  `widgets/composites/toast.py:297-303` calls
  `self._handle_on_dismissed(options)` where `options` is the same
  dict passed by the caller in `buttons=`, with no sanitization.
  Verified at runtime: a `buttons=[{'text': 'Yes', 'command':
  btn_cmd, 'accent': 'success'}]` invocation yields `data ==
  {'text': 'Yes', 'command': <function btn_cmd>, 'accent':
  'success'}` in the dismiss handler. Auto-dismiss / close-button /
  programmatic `hide()` paths all deliver `None`. The asymmetric
  payload makes routing-by-button awkward (callers must read
  `data["text"]`, or stash a sentinel marker key) and surfaces the
  raw callable in any logged payload. Either deliver a sanitized
  shape (e.g. only `text` and a caller-supplied `result=`) or
  unwrap to the button's text/result by default. (Surfaced by
  toast.md rewrite, 2026-05-01.)
- `CheckButton`'s indeterminate (`alternate`) state has **no
  programmatic re-entry path**. The default `BooleanVar` cannot hold
  `None` — `cb.set(None)` raises
  `TypeError: getboolean() argument must be str, not None` from
  `tkinter.BooleanVar.set` (`widgets/primitives/checkbutton.py:113`
  → CPython `tkinter/__init__.py:639`). The state is only reachable
  on a fresh widget where the constructor short-circuits the `set()`
  call (`checkbutton.py:104` — `if initial_value is not None and not
  signal_provided and not variable_provided`), leaving the Tcl
  variable initially unset (matches default `tristatevalue=""`).
  After the first user click, the variable cycles between the bound
  on/off values only, and indeterminate is unreachable. Either
  expose `tristatevalue=` and switch to `StringVar` when `value=None`
  or no value is provided, or accept `None` in `set()` and route it
  through a Tcl-level unset of the variable. As-is, the
  documented "indeterminate" semantics are construction-only and
  not addressable post-construction. (Surfaced by checkbutton.md
  rewrite, 2026-05-01.)
- `Switch(bootstyle='primary')` **bypasses the `variant='switch'`
  assignment** and renders as a regular CheckButton with a check-box
  indicator, NOT a switch. Cause: `widgets/primitives/switch.py:43-44`
  reads `if 'bootstyle' not in kwargs: kwargs['variant'] = 'switch'`
  — the deprecated `bootstyle=` path skips the variant assignment
  entirely. Verified at runtime: `Switch(bootstyle='primary')` →
  `style='bs[…].primary.TCheckbutton'` (a CheckButton style), while
  `Switch(accent='primary')` → `style='bs[…].primary.Switch.TCheckbutton'`
  (the slider). Either always force `variant='switch'` regardless
  of bootstyle, or document loudly that `bootstyle=` on Switch is
  unsafe. (Surfaced by switch.md rewrite, 2026-05-01.)
- `Switch.variant=` is **silently overridden** in `__init__`. Same
  source line — when `bootstyle` is not in kwargs, the constructor
  unconditionally writes `kwargs['variant'] = 'switch'`, clobbering
  any user-supplied `variant=` arg. Net effect: `Switch(variant=
  'default')` is silently treated as `variant='switch'`. Either
  raise on incompatible variants or preserve user-supplied values.
  (Surfaced by switch.md rewrite, 2026-05-01.)
- `CheckToggle.set(None)` **does NOT raise** (different from
  CheckButton and Switch). The default variable is a `StringVar`
  (because CheckToggle uses `class_='Toolbutton'` instead of
  `TCheckbutton`), so `set(None)` coerces `None` to the string
  `'None'` and silently writes it. The widget paints unpressed
  because `'None'` matches neither `onvalue` ('1') nor `offvalue`
  ('0'). Callers relying on the BooleanVar guard for tri-state
  behavior must special-case CheckToggle. (Surfaced by
  checktoggle.md rewrite, 2026-05-01.)
- `RadioGroup(accent='success')` **at construction does NOT reach
  child radios.** `RadioGroup.__init__` correctly captures
  `kwargs.pop('accent', None)` into `self._accent`, but
  `super().__init__()` (the Frame init path) then resets
  `self._accent` to `None` before the constructor returns —
  verified at runtime by patched tracing. As a result, child
  radios added via `add()` are constructed with `accent=None` and
  paint with the default style. **Workarounds:** call
  `g.configure(accent='...')` AFTER construction (the
  `_delegate_accent` path forwards correctly), or pass `accent=...`
  per-call via `add('A', 'a', accent='...')`. ToggleGroup has the
  fix in source (`composites/togglegroup.py:96-98` — explicitly
  restores `self._accent` after `super().__init__()`); RadioGroup
  needs the same patch. (Surfaced by radiogroup.md rewrite,
  2026-05-01.)
- `RadioGroup.values()` **returns keys, not values.** The
  implementation at `composites/radiogroup.py:465-472` is
  `return tuple(self._buttons.keys())`. When `key` defaults to
  `value` (the common path), this is a tautology and works by
  accident. When `key='foo', value='bar'` is passed, `g.keys()` and
  `g.values()` both return `('foo',)` — `g.values()` does not
  surface `'bar'`. Walk `g.items()` and read each radio's
  `cget('value')` if you need the actual values. Either fix to
  return per-button `value`s, or remove the method to avoid the
  confusing duplication. (Surfaced by radiogroup.md rewrite,
  2026-05-01.)
- `ToggleGroup.set(value)` **does NOT validate against known
  keys.** The implementation at `composites/togglegroup.py:267-272`
  enforces only the type (str for single, set for multi); there's
  no membership check. Verified at runtime: with `g.add('A','a')`,
  `g.set('unknown')` succeeds — `g.value == 'unknown'`, no child
  paints selected, and the unsubscribed value silently writes
  through to the underlying variable. Inconsistent with
  RadioGroup's `set(...)`, which raises `ValueError` on unknown
  keys. (Surfaced by togglegroup.md rewrite, 2026-05-01.)
- `OptionMenu.<<Change>>` (and `command=`) **fires twice per
  write.** The constructor calls `_bind_change_event()` twice
  during `__init__`: once indirectly via `self.configure(
  textvariable=self._textvariable)` at
  `widgets/primitives/optionmenu.py:116` (which routes through
  `_delegate_textsignal` → `_bind_change_event`), and once
  explicitly at line 119. The `if self._bind_id is not None`
  guard inside `_bind_change_event` runs against `self._bind_id`,
  but only the second call assigns the result to it — so the
  first call's bind_id is never tracked, never unsubscribed, and
  the second call adds another subscription on top. Verified at
  runtime: `len(m.textsignal._subscribers) == 2` immediately
  after construction. Net effect: every variable write fires
  `<<Change>>` twice, and any `command=` callback runs twice per
  change. `on_changed` listeners and `command=` callbacks must
  be idempotent until fixed. Likely fix: the explicit line 119
  call is redundant (the configure path already wires up the
  emitter); remove it, or assign self._bind_id from the first
  call so the guard short-circuits the second. (Surfaced by
  optionmenu.md rewrite, 2026-05-01.)
- `OptionMenu.set(value)` **does NOT validate against `options=`.**
  Same shape as the ToggleGroup bug — `m.set('not_in_list')`
  succeeds, writes the orphan value to the variable, no menu
  radiobutton paints selected, and `<<Change>>` still fires.
  Either validate against `options` and raise on miss (matching
  RadioGroup's behavior), or document the permissive contract
  loudly. (Surfaced by optionmenu.md rewrite, 2026-05-01.)
- `OptionMenu(value='A', textsignal=Signal('B'))` — **`value=`
  clobbers the signal's pre-existing value.** When both are
  passed, the constructor's `value=` arg wins and is written
  into the bound variable, replacing whatever the signal held.
  This is opposite of how RadioButton handles `signal=` + `value=`
  (where the signal value wins). Workaround: omit `value=` when
  binding a pre-existing signal. (Surfaced by optionmenu.md
  rewrite, 2026-05-01.)
- `SelectBox.<<Change>>` is fired on `entry_widget`, **not** on the
  SelectBox itself. The `.value` setter calls
  `self.entry_widget.event_generate('<<Change>>', ...)` at
  `composites/selectbox.py:536`. Tk virtual events do not propagate
  up the parent chain, so `sb.bind('<<Change>>', cb)` silently
  no-ops. The `on_changed` helper still works because Field forwards
  it (`composites/field.py:263` —
  `self.on_changed = self._entry.on_changed`), but users binding
  the event directly hit a silent failure. Same shape as the Tabs
  `<<TabSelect>>` bug already on this list — fix is to forward via
  `self.event_generate('<<Change>>', ...)` after the inner emit.
  (Surfaced by selectbox.md rewrite, 2026-05-01.)
- `SelectBox.value = "not_in_items"` is silently accepted even when
  `allow_custom_values=False`. The setter writes through the
  Field's `value` property unconditionally, the entry widget shows
  the orphan as plain text, `selected_index` returns `-1`, and
  `<<Change>>` fires as if it were a normal selection.
  Constructor-time `value=Z` (Z not in items) has the same shape.
  Same family as the OptionMenu / ToggleGroup orphan-value bugs
  already on this list. Either validate against `items` and raise
  on miss when `allow_custom_values=False`, or document the
  permissive contract loudly. (Surfaced by selectbox.md rewrite,
  2026-05-01.)
- `SelectBox.configure(value=X)` is broken — same inverted-delegate
  pattern as LabeledScale's broken delegators already on this list.
  `_delegate_value` (`composites/selectbox.py:493-499`) returns
  `self.value` from the set path and tries to write `None` from the
  query path:
  ```python
  if value is not None:
      return self.value
  else:
      self.value = value
      return None
  ```
  Net effect: `sb.configure(value='B')` returns the raw widget
  config dict instead of writing; `sb.cget('value')` returns
  `None`. Workaround: use the property setter (`sb.value = X`).
  Fix: invert the branches to match every other `_delegate_*`
  on the page. (Surfaced by selectbox.md rewrite, 2026-05-01.)
- `SelectBox.configure(dropdown_button_icon=...)` raises
  `TclError: unknown option "-dropdown_button_icon"`. The icon
  is captured into the `dropdown` addon at construction
  (`composites/selectbox.py:87,97`) and there is no configure
  delegate to lift it back into the configure surface. Either
  add a `_delegate_dropdown_button_icon` that calls
  `self.addons['dropdown'].configure(icon=...)`, or document
  the option as construction-time only. (Surfaced by
  selectbox.md rewrite, 2026-05-01.)
- `Calendar(min_date=…, max_date=…)` without `value=` /
  `start_date=` opens with both chevrons permanently disabled
  whenever today's month is outside the configured window. The
  constructor sets `_display_date = date(today.year, today.month,
  1)` unconditionally (`composites/calendar.py:166-168`); the
  navigation handlers then walk `_display_date` by ±1 month / year
  and gate on `_is_month_allowed` (`calendar.py:850-855`), which
  rejects any candidate whose first-of-month is outside
  `[min_date.replace(day=1), max_date.replace(day=1)]`. From an
  out-of-range starting position every adjacent candidate is
  out-of-range too, so the user is stranded. Verified at runtime
  (`today=2026-05-01`, `min=date(2025,6,1)`,
  `max=date(2025,8,31)` → display stays at 2026-05-01, prev/next
  both rejected). Either clamp `_display_date` into
  `[min_date, max_date]` at the end of `__init__` (snap to
  `min_date.replace(day=1)` if today < min, or
  `max_date.replace(day=1)` if today > max), or document the
  precondition that `min_date` / `max_date` must be paired with
  an in-range `value=`. (Surfaced by calendar.md rewrite,
  2026-05-01.)
- `Calendar.set(None)` and the `value` property setter with `None`
  are silently no-ops, despite the docstring at
  `composites/calendar.py:214` claiming "or None to clear
  selection". `set()` calls `_coerce_date(value)` (which returns
  `None` for `None` input) and early-returns at
  `calendar.py:217-218`. Net effect: there is no programmatic path
  to clear the selection in single mode — `cal.value = None` looks
  like it should work, but the value sticks. Either honor `None`
  (clear `_selected_date`, `_range_start`, `_range_end` and
  re-render) or remove the docstring claim. (Surfaced by
  calendar.md rewrite, 2026-05-01.)
- `Calendar.set()`, `set_range()`, the `value` / `range` property
  setters, and `configure(date=...)` all bypass `min_date`,
  `max_date`, and `disabled_dates`. The interactive path
  (`_on_date_selected_by_date` at `composites/calendar.py:783-784`)
  checks `_is_disabled` and refuses out-of-range or disabled
  clicks, but the programmatic setters write the date directly.
  Verified: `Calendar(min_date=date(2025,6,1),
  max_date=date(2025,6,30)).set(date(2025,12,25))` succeeds, and
  `Calendar(disabled_dates=[date(2025,12,25)]).set(date(2025,12,25))`
  also succeeds. Either re-validate inside the setters and raise /
  no-op on out-of-range, or document the divergence in the
  setters' docstrings. (Surfaced by calendar.md rewrite,
  2026-05-01.)
- In range mode, `Calendar.range = None` and `set_range(None,
  None)` clear `_range_start` and `_range_end` but do **not**
  clear `_selected_date`. The fallback at
  `composites/calendar.py:274` (`self._selected_date = e if e else
  (s if s else self._selected_date)`) keeps the previous
  `_selected_date` when both arguments coerce to `None`. Net
  effect: `cal.range` reports `(None, None)`, the grid paints no
  cell as selected (because `_is_selected` short-circuits on
  `not self._range_start`), but `cal.value` and `cal.get()`
  return a *stale* date. Verified: after
  `cal = Calendar(selection_mode='range',
  start_date=date(2025,6,1), end_date=date(2025,6,30))` then
  `cal.range = None`, `cal.value` is still `date(2025,6,30)`.
  Either also clear `_selected_date` when both range arguments
  are `None`, or document that `cal.value` is meaningless in
  range mode and callers must read `cal.range`. (Surfaced by
  calendar.md rewrite, 2026-05-01.)
- `PageStack.<<PageUnmount>>` is fired without a `data=` argument
  (`composites/pagestack.py:188`), so handlers receive
  `event.data is None`, while the other three navigation events
  carry the full payload. The class docstring at
  `composites/pagestack.py:44-50` lists all four under "all events
  provide event.data with keys ..." — false for `<<PageUnmount>>`.
  Either pass the same payload (the navigation has the same
  `prev_page` / `prev_data` / `index` info available at
  `pagestack.py:187`) or document the asymmetry. (Surfaced by
  pagestack.md rewrite, 2026-05-01.)
- `PageStack` `<<PageUnmount>>` and `<<PageWillMount>>` fire on the
  page *widget*, not on the PageStack
  (`composites/pagestack.py:188,208`). Tk virtual events do not
  propagate up the parent chain, so binding either event on the
  stack itself silently no-ops. The class docstring lists all four
  events together without naming the emission target — implying
  bubble. Same shape as the Tabs `<<TabSelect>>` / SideNav
  `<<ItemInvoked>>` bugs already on this list. Either forward
  these two events to the stack via a second `event_generate(...)`
  call, or document the binding target alongside each event in
  the class docstring. (Surfaced by pagestack.md rewrite,
  2026-05-01.)
- `PageStack.remove(key)` orphans `_history`. The implementation
  (`composites/pagestack.py:114-129`) destroys the page widget and
  removes it from `_pages`, but does not rewrite `_history` or
  `_index` (the only history fix-up is clearing `_current` to
  `None` if the removed key was active). Subsequent `back()` or
  `forward()` walking onto the orphan slot raises
  `NavigationError` from `navigate()`'s existence check. Verified
  at runtime: with `history=[a,b,c]`, `index=2`, `current=c`,
  `stack.remove('b')` leaves `history` unchanged; `stack.back()`
  → `NavigationError: Page b does not exist`. Either rewrite
  history to drop orphan entries (and adjust `_index` to step
  past them) or document the precondition that callers must only
  remove pages outside their active history. (Surfaced by
  pagestack.md rewrite, 2026-05-01.)
- `PageStack.add(key, page, **kwargs)` silently drops `**kwargs`
  when `page=` is provided. The signature is
  `add(self, key, page=None, **kwargs)` and the kwargs only feed
  the auto-created Frame in the `if page is None` branch
  (`composites/pagestack.py:106-107`). Verified at runtime:
  `stack.add('foo', existing_frame, padding=99)` returns the
  passed frame with its original `padding=(5,)`, never `99`.
  Either raise `TypeError` when both `page=` and kwargs are
  passed, or apply the kwargs by calling
  `page.configure(**kwargs)` after registration. (Surfaced by
  pagestack.md rewrite, 2026-05-01.)
- **`TabView.remove(key)` always raises `KeyError`.** The
  implementation at `composites/tabs/tabview.py:194` calls
  `self._tabs.remove(tab)` where `tab` is the **TabItem widget**
  popped from `self._tab_map`, but `Tabs.remove(key: str)` (at
  `composites/tabs/tabs.py:340-355`) expects a **string key** and
  rejects anything else with `KeyError: "No tab with key '<key>'"`.
  Tabs's internal dict is keyed by auto-generated strings
  (`tab_0`, `tab_1`, …; TabView calls `Tabs.add(...)` with no
  `key=` argument so they're auto-generated), so the TabItem
  reference never matches. **The same crash hits the X-button
  path** because `tabview.add(...)` wires the default
  `close_command` (when `enable_closing` / `closable=True`) to
  `lambda: self.remove(key)` — clicking X on a closable tab
  raises the same `KeyError` from inside the Tk button callback.
  Verified at runtime: `tv.add('home'); tv.remove('home')` →
  KeyError, and `tv.add('docs', closable=True);
  tv.tab('docs').cget('close_command')()` → KeyError. Net effect:
  `tabview.remove()` is unusable, and `enable_closing=True` /
  `enable_closing='hover'` are functionally broken.
  Fix: walk `self._tabs._tabs.items()` to find the
  Tabs-internal key matching the TabItem reference and pass that
  string to `Tabs.remove(...)`, or change `TabView` to pass a
  caller-supplied `key=` to `Tabs.add(...)` so the Tabs-internal
  key matches the TabView key. (Surfaced by tabview.md rewrite,
  2026-05-01.)
- **`TabView.navigate(key, data=...)` pushes history twice and
  fires `<<PageChange>>` twice.** The implementation at
  `composites/tabs/tabview.py:218-228` writes the key through
  `self._tab_variable.set(key)` first, which triggers the variable
  trace `_on_tab_selected` → calls `self._page_stack.navigate(
  key)` with **no** data (history push #1, with empty data). Then
  it calls `self._page_stack.navigate(key, data=data)` itself
  (history push #2, with caller data). Verified at runtime: after
  `add('home') add('files') select('files') navigate('home',
  data={'x':1})`, `pagestack._history == [('home', {}), ('files',
  {}), ('home', {}), ('home', {'x': 1})]`. Net effect: history
  grows by 2 entries per call, listeners fire twice with
  inconsistent payloads (first empty `data`, second the caller's
  data). Fix options: (a) skip the trace path for navigate-with-
  data and call `self._page_stack.navigate(...)` once with the
  data, plus a separate `self._tab_variable.set(key)` write that
  the trace's "already on this page" guard short-circuits; (b)
  add a one-shot pending-data slot read and cleared by
  `_on_tab_selected`. Workaround until fixed: avoid
  `tabview.navigate(...)` entirely and call
  `tabview.page_stack_widget.navigate(key, data=...)` plus
  `tabview.select(key)` directly. (Surfaced by tabview.md
  rewrite, 2026-05-01.)
- **`TabView.<<TabSelect>>` and `<<TabClose>>` do not fire on the
  TabView.** The class docstring at
  `composites/tabs/tabview.py:23-27` lists `<<TabSelect>>`,
  `<<TabClose>>`, `<<TabAdd>>`, and `<<PageChange>>` under
  "Events", but only the latter two reach the TabView itself
  (forwarded via `on_page_changed` / `on_tab_added` to the inner
  PageStack / Tabs widgets). `<<TabSelect>>` and `<<TabClose>>`
  are emitted on the individual `TabItem` (same root cause as the
  Tabs bubbling bug already on this list — `TabItem.event_generate
  (...)` does not propagate up the parent chain), so
  `tabview.bind("<<TabSelect>>", cb)` silently no-ops. Verified at
  runtime. Fix: forward in the
  `_on_tab_click` / `_on_close_click` paths with a second
  `event_generate` on `self.master.master.master` (the
  TabView) carrying the value payload, or fix the docstring and
  add a `tab.bind('<<TabSelect>>', ...)` example. (Surfaced by
  tabview.md rewrite, 2026-05-01.)
- `TabView(variant='pill')` succeeds at construction but **the
  first `add()` call raises `BootstyleBuilderError`**. Same root
  cause as the Tabs `pill` bug already on this list — TabView
  forwards `variant` to the inner Tabs which forwards it to each
  TabItem, and the TabItem.TFrame style builder registers only
  `'default'` and `'bar'` (`style/builders/tabitem.py:27-28`).
  Verified at runtime: `tv = TabView(variant='pill')` succeeds,
  `tv.add('home', text='Home')` →
  `BootstyleBuilderError: Builder 'pill' not found for widget
  class 'TabItem.TFrame'. Available variants: default, bar`.
  Either register the `pill` variant on TabItem.TFrame /
  TabItem.TLabel / TabItem.TButton or remove `'pill'` from
  TabView's signature and docstring. (Surfaced by tabview.md
  rewrite, 2026-05-01.)
- **`Notebook.on_tab_changed` / `on_tab_activated` /
  `on_tab_deactivated` never fire** — the entire enriched event
  mechanism is bound to the wrong virtual event name.
  `widgets/primitives/notebook.py:570,485,509` bind
  `<<NotebookTabChange>>` (present tense, no `'d'`), but Tk's
  underlying `ttk.Notebook` emits `<<NotebookTabChanged>>` (past
  tense, with `'d'`). Verified at runtime: a direct bind to
  `<<NotebookTabChanged>>` fires on programmatic and click
  selection, but `nb.on_tab_changed(cb)` never fires. The
  `wrapper` function inside `on_tab_changed` is what synthesizes
  the activate / deactivate lifecycle events via
  `event_generate(...)`, but since the wrapper itself never runs,
  those events are never generated either — and the
  `_last_selected` / `_last_change_reason` / `_last_change_via`
  state the source maintains for the enriched payload is never
  observed. Workaround until fixed: bind directly to
  `<<NotebookTabChanged>>` and read `nb.select()` /
  `nb._tk_to_key.get(...)` from the widget. Fix: change the bind
  string in three places to the past-tense name and update the
  three internal `event_generate` calls to match the chosen
  spelling for the synthetic activate / deactivate events.
  (Surfaced by notebook.md rewrite, 2026-05-01.)
- **`Notebook.remove(tab)` and `Notebook.forget(tab)` always raise
  `TypeError: WidgetCapabilitiesMixin.forget() takes 1 positional
  argument but 2 were given`.** MRO conflict:
  `WidgetCapabilitiesMixin.forget` (the
  `pack_forget`/`grid_forget` shim, takes no positional arguments)
  appears in the MRO at `core/mixins/widget.py` *before*
  `tkinter.ttk.Notebook.forget(tabid)`, so
  `super().forget(tabid)` from
  `Notebook.remove`/`Notebook.forget` dispatches to the wrong
  method. Verified at runtime. `Notebook.hide(tab)` works because
  there is no upstream `hide` override above ttk.Notebook in the
  MRO. Workaround:
  `tkinter.ttk.Notebook.forget(nb, nb._to_tab_id(tab))` plus
  manual cleanup of `_tk_to_key`, `_key_registry`, and
  `_tab_locale_tokens`. Fix options: (a) call
  `ttk.Notebook.forget(self, tabid)` directly instead of via
  `super()`; (b) push the `WidgetCapabilitiesMixin.forget` shim
  later in the MRO so it doesn't shadow ttk's `forget`; (c) rename
  the mixin's geometry-forget to something other than `forget`.
  (Surfaced by notebook.md rewrite, 2026-05-01.)
- `Notebook.add()` / `Notebook.insert()` validation errors leave
  orphan tabs in the strip. Both validation steps inside
  `_make_key` (`widgets/primitives/notebook.py:147-154`) — the
  duplicate-key `NavigationError` and the empty-string
  `ValueError` — run *after* `super().insert()` has already added
  the auto-created Frame to the underlying ttk notebook. Verified
  at runtime: a single `nb.add(text='OK', key='ok')` followed by
  `nb.add(text='Bad', key='')` (raises `ValueError`) leaves
  `nb.keys() == ('ok', '')` and `len(nb.tabs()) == 2`. The orphan
  has no entry in `_key_registry` / `_tk_to_key`, and there is no
  public way to remove it (the broken `remove()` aside — see the
  separate bug). Either validate the key before `super().insert()`
  runs, or roll back the ttk insert on validation failure.
  (Surfaced by notebook.md rewrite, 2026-05-01.)
- `Notebook.add()` / `Notebook.insert()` with an existing widget
  silently drops extra kwargs. When the first positional argument
  is `None`, `**kwargs` flows into `Frame(self, **kwargs)`
  (correct). When a widget is passed, `**kwargs` is ignored —
  not applied to the existing widget, not raised on. Verified at
  runtime: `existing = ttk.Frame(nb, padding=5);
  nb.add(existing, key='x', text='X', padding=99)` leaves
  `existing.cget('padding') == (5,)`. Same shape as the PageStack
  kwargs-drop bug already on this list. Either raise `TypeError`
  when both an existing widget and extra kwargs are passed, or
  apply the kwargs via `widget.configure(**kwargs)`
  post-registration. (Surfaced by notebook.md rewrite,
  2026-05-01.)
- `Entry.configure(surface=...)` raises `TclError: unknown option
  "-surface"`. Entry accepts `surface=` at construction (captured
  into `_surface` and factored into the resolved style key), but
  the class doesn't add a `_delegate_surface` to lift the option
  into a Python-side configure delegator the way Frame does. The
  escape hatch `entry.configure_style_options(surface='primary')`
  works (it updates `_style_options` and `_surface` but does **not**
  rebuild the resolved ttk style — see Frame's
  `_refresh_descendant_surfaces` hook for how the cascade fixes
  this when the parent surface changes). Same family as the
  Sizegrip surface bug already on this list. Either lift `surface`
  into a configure delegator that rebuilds the resolved style, or
  document `surface` as construction-time only on Entry.
  (Surfaced by entry.md rewrite, 2026-05-01.)
- `Entry.configure(density=...)` updates only the **font** — the
  resolved ttk style is not rebuilt. `_delegate_density`
  (`widgets/primitives/entry.py:94-103`) calls
  `self.configure(font='caption' or 'body')` and writes the new
  density into `_style_options`, but `configure_style_options(...)`
  does not trigger a style rebuild. Net effect: the underlying
  image element key and padding from the construction-time density
  persist; only the font shrinks/grows. Verified at runtime: a
  vanilla `Entry(app)` (style `Default.TEntry`) reconfigured with
  `entry.configure(density='compact')` keeps style `Default.TEntry`
  and renders with the default-density image element + a caption
  font — visually inconsistent. Construction-time
  `Entry(density='compact')` works correctly because the style
  builder reads the captured `style_options` dict. Either rebuild
  the style on density writes (matching what construction does),
  or document `density` as construction-only and reject
  reconfiguration. (Surfaced by entry.md rewrite, 2026-05-01.)
- The Tk-class autostyle wrapper (`Bootstyle.override_tk_widget_constructor`
  at `style/bootstyle.py:553-599`) silently overrides the explicit
  `surface=` argument with the parent's `_surface` whenever
  `inherit_surface=True` — which is the default, pulled from
  `AppSettings.inherit_surface_color`. The branch at
  `style/bootstyle.py:575-578` is `if inherit_surface: surface_token
  = parent_surface_token else: surface_token = surface_token or
  'content'` — `surface_token` is *replaced*, not *defaulted*, when
  inheritance is on. Net effect: `ttk.Text(parent, surface='card')`
  ends up with `_surface='content'` (parent's surface), NOT
  `'card'`. Callers must pass both `surface='card',
  inherit_surface=False` to pin a surface explicitly. Verified at
  runtime on Text; the same wrapper applies to every Tk-class
  autostyle widget (Frame, Label, Button, Entry, Text, Canvas,
  Listbox, Menu, etc.), so this likely affects all of them — only
  Text was verified during this sweep. Either change the resolution
  to "explicit `surface=` wins; otherwise inherit"
  (`surface_token = surface_token if surface_token else (
  parent_surface_token if inherit_surface else 'content')`), or
  document the precondition that `surface=` requires
  `inherit_surface=False`. (Surfaced by text.md rewrite,
  2026-05-01.)
- `Toplevel.__init__` has an unusual signature footgun: the **first
  positional argument is `title`**, not `master` /  parent. The
  master/parent flows through `**kwargs` and is forwarded to
  `tkinter.Toplevel.__init__` (`runtime/toplevel.py:30-73`). Net
  effect: `ttk.Toplevel(app, title="...")` raises
  `TypeError: __init__() got multiple values for argument 'title'`
  because `app` resolves positionally to `title` first. Verified at
  runtime via the snippet check on `windows.md`. Workaround: always
  pass the parent as `master=app` (kwarg). Inconsistent with `App`
  and `AppShell` (which also take `title` as a kwarg) and with the
  raw `tkinter.Toplevel` (which takes `master` as the first
  positional). Either reorder the signature to put `master` first
  (breaking change), or add an explicit `master` positional /
  keyword-only param so the wrong call shape raises a clearer
  error. (Surfaced by windows.md rewrite, 2026-05-01.)
- **`widget.unbind(seq, fid)` is broken for `add="+"` bindings on
  Python 3.13 / Tk 8.6.** This is a CPython tkinter bug, not a
  ttkbootstrap bug, but it impacts every `off_*` helper in the
  framework because every `on_*` helper passes `add="+"` (or
  `add=True`). Cause: `Misc._unbind` in CPython 3.13's
  `tkinter/__init__.py` filters bind script lines for the prefix
  `if {{"[<fid> ` — the wrapper form Tk uses for non-`add`
  bindings (`if {{"[<fid> %d %# ...]" == "break"}} break`). Bindings
  registered with `add="+"` produce raw script lines starting with
  the bare fid (`<fid> %d %# ...`), so the prefix-match never finds
  them: no lines are removed but `Tcl.deletecommand(fid)` still
  runs, leaving dangling references in the bind script. Subsequent
  `event_generate(seq)` then dispatches to the deleted proc and
  aborts the entire binding sequence silently — every handler on
  `seq` (not just the targeted one) stops firing. Verified on
  Python 3.13.9 / Tk 8.6: two `add="+"` bindings → one
  `unbind(seq, fid)` → zero invocations on event_generate. The
  documented workaround in `callbacks.md` is `widget.unbind(seq)`
  to detach everything and re-bind the handlers you want to keep,
  or hold a single dispatcher closure and switch its body via a
  flag instead of unbinding. Worth tracking upstream
  (CPython issue) and considering a framework-side override of
  `Misc._unbind` that handles both line forms. (Surfaced by
  callbacks.md rewrite, 2026-05-01.)
- **`ValidationRule('compare')` is a silent no-op.** The `RuleType`
  literal at `core/validation/types.py:4` lists `'compare'` as a
  supported rule type alongside `'required'`, `'email'`, `'pattern'`,
  `'stringLength'`, and `'custom'`, but `ValidationRule.validate()`
  (`core/validation/validation_rules.py:48-86`) has no `elif self.type
  == 'compare'` branch. Net effect: the construction succeeds, the
  rule joins the widget's rule list normally, and every call to
  `rule.validate(value)` falls through to the `return ValidationResult
  (True)` at line 86 — so a `'compare'` rule reports every input as
  valid, regardless of what it was supposed to compare against.
  Verified at runtime: `ValidationRule('compare').validate('anything').is_valid`
  → `True`. Either implement the rule (presumably comparing against
  a reference value passed in `params`, e.g. `func`-style or a
  named widget reference) or remove `'compare'` from the Literal so
  IDEs and type-checkers reject the call shape. (Surfaced by
  validation/index.md rewrite, 2026-05-02.)
- **`ValidationRule('stringLength', min_length=N, max_length=N)` is
  silently ignored.** The rule's `validate()` method reads
  `params.get("min", 0)` and `params.get("max", float("inf"))`
  (`core/validation/validation_rules.py:73-74`), so passing
  `min_length` / `max_length` (the names used in the
  `ValidationMixin.add_validation_rule` docstring example at
  `widgets/mixins/validation_mixin.py:78`, `min_length=5`) writes
  the values into `params` but never reads them — the rule falls back
  to its default `min=0` / `max=∞` and accepts any string. Verified
  at runtime: `ValidationRule('stringLength', min=5).validate('abc').is_valid`
  → `False` (the correct, working call); `ValidationRule('stringLength',
  min_length=5).validate('abc').is_valid` → `True` (silently
  permissive). Either fix the docstring example to use `min=`/`max=`,
  or accept both spellings in `validate()` so the docstring example
  works as written. (Surfaced by validation/index.md rewrite,
  2026-05-02.)
- **`ValidationMixin.validate()`'s docstring lies about the return
  value.** The docstring at `widgets/mixins/validation_mixin.py:99-100`
  says the method returns "True if validation was performed
  (regardless of result)." The actual return semantics are: returns
  `True` only when at least one rule ran AND every rule passed;
  returns `False` on the first invalid result (early-return at line
  117) and on the no-rules case (`return ran_rule` at line 124,
  where `ran_rule` is `False` because no rule's filter matched).
  Verified at runtime via the inner part:
  `inner.validate('Alice', trigger='manual')` → `True` with a
  required rule (passed); `inner.validate('', trigger='manual')` →
  `False` with the same rule (failed); `entry2.validate('x',
  trigger='manual')` → `False` with no rules (ran_rule stayed False).
  The "True if validation was performed" claim is the *opposite* of
  reality — validation was performed in case 1 (returns True) and
  in case 2 (returns False). The current implementation is more
  useful than the docstring (it answers "did this value pass?"); the
  fix is to update the docstring to "True if all applicable rules
  passed, False otherwise" rather than to change the
  implementation. `Field.validation()` is `self._entry.validate`
  forwarding (`composites/field.py:281`), so the same
  return-semantics bug applies to the public-facing
  `widget.validation(value)` call. (Surfaced by validation/results.md
  rewrite, 2026-05-02.)
- **`ValidationResult` has no `__bool__`.** This is technically a
  framework hardening gap rather than a bug, but worth noting:
  `bool(ValidationResult(False))` returns `True` because the class
  inherits the default truthy-by-identity behavior. The framework
  itself never hits this — `ValidationRule.validate()` and
  `ValidationMixin.validate()` always read `result.is_valid`
  explicitly — but standalone-use callers writing
  `if rule.validate(value): ...` get a silent always-true
  short-circuit. Either add `__bool__ = lambda self: self.is_valid`
  or document the gap loudly. There is also no `__eq__`,
  `__repr__`, or `__hash__` on the class. Documented as a
  `!!! danger` block in `validation/results.md`. (Surfaced by
  validation/results.md rewrite, 2026-05-02.)
- **Theme tokens crash when supplied as `IconSpec.color` (or in a
  per-state `color` override).** The icon-resolution helper
  `_image_for` at `style/bootstyle_builder_base.py:684` calls
  `BootstrapIcon(name=name, size=size, color=color)` directly
  without resolving the token through `self.color(...)` first — so
  PIL receives the literal string (e.g., `'primary'`) and raises
  `ValueError: unknown color specifier: 'primary'` from
  `PIL/ImageColor.py:125`. Verified at runtime:
  `Button(icon={'name': 'star', 'color': 'primary'})` →
  `ValueError`. This contradicts the user expectation that theme
  tokens work everywhere they appear in widget kwargs. The
  no-color path (where the icon inherits the widget's foreground
  state map) works correctly because the `foreground_spec`
  argument arrives at `_image_for` already-resolved to hex
  strings by the style builder. Hex strings (`'#ff6600'`) and PIL
  named colors (`'red'`, `'navy'`) also work directly. Fix:
  resolve `color` through `self.color(color, surface=...)` (the
  same helper the rest of the builder uses) before passing into
  `BootstrapIcon`. Workaround for users today: omit `color` to
  inherit the foreground, use a hex value, or call
  `app.style.builder.color('primary')` to convert the token to
  hex first. (Surfaced by capabilities/icons/index.md rewrite,
  2026-05-02.)
- **`pack_propagate()` and `grid_propagate()` mixin methods always
  return `None` on query.** The mixin methods at
  `core/capabilities/pack.py:99-111` and
  `core/capabilities/grid.py:112-124` always pass `flag` through to
  `super().pack_propagate(flag)` / `super().grid_propagate(flag)`,
  including when `flag=None`. CPython `tkinter.Misc.pack_propagate`
  / `grid_propagate` distinguish the query path from the setter path
  by a private `['_noarg_']` sentinel — so passing `None` dispatches
  as the setter and the query path is never taken. Verified at
  runtime: `f.pack_propagate()` → `None` even on a fresh widget
  where the underlying Tk value is `True`. The propagation state
  itself is preserved (the underlying Tcl `pack propagate <w>`
  reports the right value), but the helper return is unusable for
  reading state. Workaround:
  `widget.tk.call('pack', 'propagate', widget._w)` returns the raw
  Tk integer; same for `grid`. Fix: use a private sentinel
  (`_NO_ARG = object()`) and conditionally pass `flag` only when
  it's not the sentinel — `if flag is _NO_ARG: return
  super().pack_propagate(); else: super().pack_propagate(flag)`.
  Same shape applies to both pack and grid. (Surfaced by
  capabilities/layout-props.md rewrite, 2026-05-02.)
- **`Form.field_signal(key)` and `Form.field_textsignal(key)` always
  return `None` for Field-based editors.** The build path at
  `composites/form.py:598-603` reads
  `getattr(field_widget, "_signal", None)` and
  `getattr(field_widget, "_textsignal", None)` — but `Field` exposes
  the attributes as `signal` / `textsignal` (no underscore). Only
  direct `SignalMixin` subclasses (`CheckButton`, `Switch`, `Scale`,
  `RadioToggle`) own `_signal`, so they're the only editors that
  populate `Form._signals` / `_textsignals`. Every Field-based editor
  (`TextEntry`, `NumericEntry`, `SelectBox`, `DateEntry`,
  `PasswordEntry`, `Spinbox`, `Combobox`) returns `None`. The
  deprecated `get_field_signal` / `get_field_textsignal` aliases
  inherit the same bug. Workaround: `form.field(key).signal` works
  for every editor. Fix: try both attribute names in the build
  path, or remove the helpers and tell users to go through
  `form.field(key).signal`. (Surfaced by widgets/inputs/form.md
  rewrite, 2026-05-02.)
- **Form spec keys outside `FieldItem` are silently dropped.**
  `_normalize_items` (`composites/form.py:627-686`) only reads
  `key`, `label`, `dtype`, `readonly`, `visible`, `column`, `row`,
  `columnspan`, `rowspan`, `editor`, `editor_options`. The
  pre-rewrite docs page used spec keys like `value=`, `required=`,
  `validate=`, `help=`, `message=` — all of which were accepted by
  the dict literal but never reached the widget. Verified at
  runtime: `Form(items=[{"key": "x", "value": "Alice", "required":
  True, "validate": "email"}])` → field value `''`, no rules
  attached. Either validate spec keys at normalize time and raise on
  unknown ones, or document loudly that the only path for initial
  values is `data=` and the only path for rules is
  `form.field(key).add_validation_rule(...)`. (Surfaced by
  widgets/inputs/form.md rewrite, 2026-05-02.)
- **Form unknown editor names silently fall through to TextEntry.**
  `_build_field` at `composites/form.py:506-581` has a chain of
  explicit `editor == 'X'` branches with a final `else: TextEntry`
  fallback. A misspelled editor name (`'select'`, `'int'`,
  `'bogus'`) hits the fallback and silently constructs a TextEntry
  with no warning. Verified at runtime. Either validate `editor`
  against `EditorType` at normalize time (raise `ValueError` on
  miss), or emit a warning when the fallback fires.
  (Surfaced by widgets/inputs/form.md rewrite, 2026-05-02.)
- **Form `numericentry` editor without `dtype` round-trips strings.**
  `_read_value_from_widget` (`composites/form.py:717-738`) calls
  `_coerce_value(item.dtype, value)` — but `_coerce_value` only
  coerces when `dtype` is set; otherwise the raw widget value passes
  through unchanged. NumericEntry's variable is auto-built as an
  `IntVar` only when `dtype in ('int', int, 'float', float)` —
  otherwise it's a `StringVar`. Net effect: `Form(items=[{"key":
  "n", "editor": "numericentry"}])` then `form.set({"n": 7})` →
  `form.data["n"] == '7'` (string). Either default `dtype` from
  `editor` (`numericentry` → `int`) when not specified, or document
  loudly that `editor='numericentry'` without `dtype` returns
  strings. (Surfaced by widgets/inputs/form.md rewrite,
  2026-05-02.)
- **`Form` rejects `columns=` (the documented kwarg) — actual is
  `col_count=`.** The pre-rewrite docs page advertised
  `Form(app, columns=2)`, but the real constructor signature
  (`composites/form.py:139-153`) accepts `col_count`. The wrong name
  flows through `**kwargs` to the underlying ttk Frame and raises
  `TclError: unknown option "-columns"` from
  `tkinter/__init__.py:2780`. Either accept `columns=` as an alias,
  or update every docs example to use `col_count=`. The page now
  documents `col_count=` as a `!!! note` block. (Surfaced by
  widgets/inputs/form.md rewrite, 2026-05-02.)
- **`TabsItem.label` is a dead dataclass field.** The dataclass at
  `composites/form.py:93-104` declares `label: str | None = None`,
  but the build path (`composites/form.py:480-489`) constructs the
  Notebook using only `width=` / `height=` and walks
  `tabs` directly — `item.label` is never read. Verified at
  runtime: `TabsItem(label="MY-LABEL", tabs=[...])` produces a
  Notebook with no "MY-LABEL" anywhere in the widget tree. Either
  render the label as a section heading above the Notebook (e.g.
  via a `Label` or `LabelFrame` wrapper), or remove the field from
  the dataclass. (Surfaced by widgets/inputs/form.md rewrite,
  2026-05-02.)
- **`Form.set_field_value(key, v)` on `visible=False` writes to
  `_data` but no widget exists.** The check
  (`composites/form.py:331-335`) tests `key in self._items_by_key`
  (which contains the FieldItem even for invisible fields), then
  calls `_apply_value_to_widget(...)` (which silently no-ops because
  `_widgets.get(key)` returns `None`), then writes `self._data[key]
  = value`. Net effect: invisible fields ARE in `form.data` and
  ARE writable via `set_field_value`, but no UI reflects them.
  Useful pattern for hidden round-trip fields (IDs, schema versions),
  but inconsistent with the docstring "Set the value of the field"
  — there's no field, only a dict slot. The page documents this as
  intended behavior. (Surfaced by widgets/inputs/form.md rewrite,
  2026-05-02.)

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
