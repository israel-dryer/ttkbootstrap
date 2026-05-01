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

### Current handoff (2026-04-30, dialogs sweep — 8/11 done)

Phases 1–7, 9A–9D are complete. **Phase 6 (screenshot pipeline) is partially
complete; 6F not started. Pass 2 (editorial review) is the active work —
dialogs sweep is in progress: messagedialog, messagebox, querydialog,
querybox, formdialog, dialog (base), datedialog, and colorchooser are
done; colordropper, fontdialog, and filterdialog remain.**

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

Remaining 6 templates (data-display, form, layout, navigation,
overlay, selection) still lead with `Framework integration` etc.
Apply the editorial pass at the start of each category's sweep —
those categories have 0 pages written, so the template fix is free.

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

### Now: Widget pages — dialogs (`docs/widgets/dialogs/`, 11 pages)

Template: `docs/_template/widget-dialog-template.md` (slim arc).
Required H2s:

- `Basic usage`
- `Result value`
- `Common options`
- `Behavior`
- `Events`
- `When should I use WidgetName?`
- `Additional resources` (with sub-bullets for Related widgets,
  Framework concepts, API reference)

Optional (declared via `*Optional` prose under the heading):

- `UX guidance` — include when the dialog has real prescriptive
  advice (button labels, default placement, alert use). Skip for
  base classes (`Dialog`) and specialty interactions
  (`ColorDropper`).

Last session (2026-04-30, colorchooser sweep):

- `colorchooser.md` rewritten to the slim template (`86a0ced`).
  Frames the page as the modal wrapping `ColorChooser` — three-tab
  notebook (Advanced spectrum, Themed swatches, Standard swatches)
  + synchronized RGB/HSL/Hex spinners + the Windows/Linux-only
  eyedropper that opens a `ColorDropperDialog` and traces the
  sampled hex back into the chooser. Intro disambiguates the
  page-slug-vs-class-name mismatch (slug is `ColorChooser`, class
  is `ColorChooserDialog`; bare `ColorChooser` is the inline
  widget).
  Result-value section documents the actual `ColorChoice` namedtuple
  shape — `(rgb=(r,g,b), hsl=(h,s,l), hex='#rrggbb')` — instead of
  the old "hex string or rgb tuple" hedge. All three representations
  are exposed simultaneously.
  Common-options table lists only the three constructor args that
  exist (`master`, `title`, `initial_color`); the old page listed
  a fictitious `format` (hex/rgb) option which doesn't exist.
  Title default `"color.chooser"` is flagged as a translation key
  auto-resolved by `BaseWindow._setup_window`. Internal labels
  (tab names, field labels, preview captions) are also translation
  keys against `MessageCatalog` — a locale that doesn't supply them
  will display literal `color.advanced` / `color.hue:` strings.
  Behavior section calls out two non-obvious bindings inherited
  from the footer-builder Dialog shape: **no Enter binding** (no
  button is registered as `default=True`, so the OK button styled
  `accent=PRIMARY` doesn't get the Enter accelerator) and **Escape
  destroys directly without invoking `_on_cancel`** (since no
  button has `role="cancel"`, Dialog's fallback path runs
  `toplevel.destroy()` and skips the cancel callback — `.result`
  ends up as None either way because `show()` resets it at start).
  The macOS-only omission of the eyedropper button is documented
  explicitly (Tk on aqua doesn't support the underlying screen-grab
  mechanism, so the dropper widget is never built into the footer).
  Events section documents the `<<DialogResult>>` payload
  (`{"result": ColorChoice|None, "confirmed": bool}`), the
  `on_dialog_result(callback)` helper that receives the **payload
  dict** (matching DateDialog's behavior — same payload-vs-unwrap
  ambiguity, but ColorChooserDialog's docstring doesn't make the
  same mis-claim DateDialog's does), and the same
  register-after-master gotcha already documented for DateDialog
  and QueryDialog: registering before `show()` with no `master=`
  binds against `self._master or self._dialog.toplevel` which is
  None pre-show, so the helper returns None silently.
  Corrects three errors from the old page: result-value
  oversimplified to "hex string or rgb tuple" (it's a namedtuple
  with all three), "Enter confirms / Escape cancels (typical)"
  (Enter does nothing on the dialog level; Escape destroys without
  calling `_on_cancel`), and the bogus `format` constructor option.

Prior session (2026-04-30, datedialog sweep):

- `datedialog.md` rewritten to the slim template.
  Frames the page around the dialog's actual commit semantics —
  there is **no OK/Cancel footer** (`buttons=[]` in source); a
  click on a non-disabled day commits and closes. Result-value
  section explains that `<<DialogResult>>` fires only on commit
  (with `event.data = {"result": date, "confirmed": True}`),
  navigation/reset clicks are filtered out by
  `_DialogCalendar._last_trigger_reason`, and cancel paths
  (Escape, WM close, popover outside-click) leave `.result` as
  None and emit no event.
  Common-options table covers all twelve constructor args, with
  the calendar-side options (min/max, disabled_dates,
  show_outside_days, show_week_numbers, first_weekday) noted as
  forwarded through to the embedded Calendar. Behavior section
  splits modal/popover modes (popover = `close_on_click_outside`),
  documents the click-to-commit shape, the default positioning
  fallback (parent's bottom-right rather than centering — unlike
  most dialogs), and the override-redirect macOS caveat.
  UX guidance prescribes anchoring popovers to triggers,
  pre-disabling impossible dates instead of post-validating,
  setting `first_weekday` from locale, and not trying to do
  ranges with `DateDialog` (it commits on first click).
  Corrects four issues in the old page: it described OK/Cancel
  buttons (none exist), listed `<<Changed>>` / `<<Accepted>>` /
  `<<Cancelled>>` events (only `<<DialogResult>>` exists, only on
  commit), hedged `min_date`/`max_date` as "(if supported)" (they
  are), and described business-rule validation paths that don't
  exist (validation is by `disabled_dates` + bounds only).

Prior session (2026-04-30, dialog (base) sweep):

- `dialog.md` rewritten to the slim template (`644e5a0`).
  Frames the page as the **builder-pattern base class** — composition
  via `content_builder` / `footer_builder` callbacks plus a button
  list, not inheritance — and the place readers drop down to when
  the specialized subclasses don't fit. The intro now lists every
  specialized subclass it underpins (MessageDialog, QueryDialog,
  FormDialog, FontDialog, ColorChooserDialog, DateDialog,
  FilterDialog) so readers entering from any of them can route
  back here.
  Result-value section flags the central distinction from the
  subclasses: base `Dialog` does **not** fire `<<DialogResult>>`
  and has no `on_dialog_result` helper — those are added by
  subclasses that generate the event themselves. Readers needing
  an event-style hook on the base class are pointed at button
  `command` callbacks (which receive the Dialog instance and run
  before `result` is assigned and the toplevel is destroyed). Also
  documents the `closes=False` button behavior (runs `command` but
  does not close or assign `.result`) — useful for "Apply" buttons.
  One Common-options table covers all twelve constructor args plus
  a second table for the eight `DialogButton` fields. Behavior
  section adds: a modes table (modal / popover / sheet) clarifying
  that sheet mode is macOS-only and falls back to plain modal
  elsewhere; the **default-button rule difference** from
  MessageDialog (Dialog does NOT auto-promote the last button —
  you must set `default=True` explicitly or there's no Enter
  binding); the Escape fallback (no cancel-role button → Escape
  destroys the dialog directly with `result=None`); the
  positioning priority for `show()` (position → anchor_to → center
  on parent); and the frameless option's recommended use
  (popover-anchored menus).
  Per the slim-dialog template, omits the optional UX-guidance
  section (this is a base class — prescriptive advice belongs on
  the specialized subclasses).
  Corrects two errors from the old page: it described buttons as
  plain strings (`"OK"`, `"Cancel"`) — that syntax works on
  MessageDialog (which has its own `_parse_buttons`), not on
  `Dialog`. Base `Dialog._normalize_buttons` only accepts
  `DialogButton` instances or dicts. The old page also listed
  `message` and `default` as Dialog options — neither exists on
  the base class (those are MessageDialog options).

Prior session (2026-04-30, formdialog sweep):

- `formdialog.md` rewritten to the slim template (`a326698`).
  Frames the dialog as a thin Dialog shell wrapping a Form
  composite. One Result-value paragraph documents that
  `.result` is `form.data` on submit / `None` on cancel, that
  values are coerced by `dtype` before return, and — critically
  — that FormDialog does **not** fire `<<DialogResult>>`
  (unlike MessageDialog and QueryDialog). One Common-options
  table covers all twelve constructor args, plus the
  localization caveat shared with MessageDialog (default
  buttons are translation keys, not strings). Behavior splits
  validation-on-submit (form stays open and focuses the first
  invalid field) from the custom-button command convention
  (callbacks receive the FormDialog instance and can return
  `False` to keep the dialog open).
  Corrects three issues from the old page: the old "Common
  options" listed `fields`, `initial`, and `validate_on_submit`
  — none exist (the real options are `data`, `items`, and
  automatic validation on every non-cancel button); the old
  page hedged the result type as "implementation-dependent"
  (it isn't — it's `dict[str, Any]` on submit, `None` on
  cancel); and the old page implied `.result` might be a
  custom button-result value (in practice, FormDialog.show()
  overwrites `.result` with `form.data` on commit regardless
  of the button's `result=` setting).
  Surfaces three non-obvious behaviors worth flagging:
  `on_data_changed` fires on every keystroke (it is **not**
  the submission callback), button `command` callbacks
  receive the FormDialog and can abort the close by returning
  `False`, and the dialog always wraps the form in a vertical
  ScrollView with the scrollbar visible by default to prevent
  layout jumps.

Earlier session (2026-04-30, querybox sweep):

- `querybox.md` rewritten to the slim template (`fc5484d`).
  Treats the page as the umbrella **facade** over the framework's
  input dialogs: one Result-value table maps each of the seven
  helpers to its underlying dialog (QueryDialog for `get_string`
  / `get_integer` / `get_float` / `get_item`; DateDialog for
  `get_date`; ColorChooserDialog for `get_color`; FontDialog for
  `get_font`) and the typed return value, one Common-options
  table covers the shared shape and per-helper extras, Behavior
  splits the QueryDialog-backed validation rules from the
  delegating helpers.
  Corrects three errors from the old page: there is **no
  `get_password` helper** (the old page documented one), the old
  page was missing three of the seven helpers (`get_color`,
  `get_font`, `get_date`/`get_item` not called out), and the
  scaffolding was the pre-overhaul `Quick start` / `When to use`
  / `Examples & patterns` shape.
  Surfaces three non-obvious behaviors: `on_result` is supported
  on the QueryDialog-backed helpers and `get_date` but **not** on
  `get_color` or `get_font` (their helper signatures don't expose
  it); `get_string` accepts `value_format` (forwarded to
  TextEntry's ICU parser); the QueryDialog-backed helpers forward
  extra kwargs (`width`, `padding`) into QueryDialog.

Even earlier session (2026-04-30, querydialog sweep):

- `querydialog.md` rewritten to the slim template (`f21e913`).
  Frames the dialog as "prompt for one value" — the input widget
  swaps based on `datatype` (`TextEntry` / `NumericEntry` /
  `DateEntry`) or on `items` (filterable `Combobox`). One Result-
  value table maps `datatype` → `.result` type, one Common-options
  table covers all twelve constructor args (the old page was
  missing `width`, `padding`, `master`, `increment`).
  Corrects two errors from the old page: `command=` is not a
  constructor kwarg (no such option exists), and "invalid input
  shows an error message" is only true for the `Combobox` and
  old-style numeric paths — the Field widgets keep the dialog open
  silently with their own inline error feedback. The new page
  documents both validation branches and adds explicit guidance to
  test `result is not None` (since `""` and `0` are valid answers)
  and to pass `master=` if registering `on_dialog_result` before
  `show()`.

Earliest session (2026-04-30, messagebox sweep):

- `messagebox.md` rewritten to the slim template (`58977e7`).
  Treats the page as a thin **facade** over `MessageDialog`:
  documents the per-helper button sets and return-value space in
  one table (Result value), the single-line call shape (Basic
  usage), the kwargs forwarded to MessageDialog (Common options),
  and the on_result callback as the only event hook (Events).
  Corrects three API errors from the old page: every helper takes
  positional `message` first then `title` (not keyword `title=`),
  the parent argument is `master=` (not `parent=`), and there is
  no `MessageBox.show(...)` static method.
  Surfaces two non-obvious behaviors worth flagging in narrative:
  `MessageBox` always passes `localize=True` (so returned strings
  reflect the active locale — branching on `result == "Yes"` will
  break under translation), and `yesno` has no Escape binding
  because its first label is "No" not "Cancel" (use `yesnocancel`
  if you need keyboard dismissal).

(Earlier dialogs-sweep history — template restructure `7667e36`,
messagedialog re-review `942642c` — is captured in the "Templates
already restructured" block at the top of this handoff and in the
checked rows of the page checklist below.)

`tools/check_doc_structure.py --category dialogs` → 8/11 passing
(messagedialog, messagebox, querydialog, querybox, formdialog,
dialog, datedialog, colorchooser).

Pages to review (canonical anchor pattern: `messagedialog.md`):

- [x] `messagedialog.md` — anchor for the dialogs sweep
- [x] `messagebox.md` — facade over MessageDialog
- [x] `querydialog.md`
- [x] `querybox.md` — umbrella facade over QueryDialog/DateDialog/ColorChooserDialog/FontDialog
- [x] `formdialog.md`
- [x] `dialog.md` — base class
- [x] `datedialog.md`
- [x] `colorchooser.md`
- [ ] `colordropper.md`
- [ ] `fontdialog.md`
- [ ] `filterdialog.md`

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
