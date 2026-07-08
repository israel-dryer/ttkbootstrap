# ttkbootstrap 2.0 — Remaining Shipped-Widget API Review (design pass)

> Design pass for the **second** shipped-widget API normalization workstream:
> the custom widgets NOT covered by the first pass (`Window`/dialogs/`Tableview`,
> `2_0_shipped_widget_api_design.md`). Follows the 2.0 hard rule (design pass
> before implementation). Pair with `2_0_plan.md`, `2_0_handoff.md`, and the
> first pass's design doc.
>
> **Status: DRAFT — some forks resolved (2026-07-07), a bootstack mechanism-mining
> pass is folding in before finalize.** Ground truth in §3 was produced by seven
> parallel survey agents, each auditing one widget module against a fixed rubric
> (constructor, naming, methods, configure/cget, re-export, dead code, latent bugs,
> lifecycle/leaks, deprecation surface); spot-verified against source.
>
> **Author decisions locked so far (2026-07-07):**
> - Meter/LabeledScale value backing → **`DoubleVar`** (honor `Union[int,float]` +
>   the format string; documented behavior change). §7 Q2 resolved.
> - Constructors → **keyword-only** after the leading positional(s), matching the
>   normalized `Window`/dialogs. Documented breaking, low incidence. §4.7 resolved.
> - **Mine bootstack for borrowable mechanisms** on every widget before writing code
>   (per the standing `borrow-bootstack-mechanisms-not-api` steer) — a 6-widget
>   comparison pass is underway; its borrowable mechanisms fold into §5 per widget.

## 1. Why this, why now

The author directed (2026-07-07): **all shipped widgets should get a 2.0 API
review.** The first pass deliberately scoped to `Window`/dialogs/`Tableview`
(§2 of that doc). This pass covers the rest of `src/ttkbootstrap/widgets/`, so
the Workstream-H docs are written against normalized signatures (same rationale
as the first pass — do the API pass before the docs).

It also cleans up **two live regressions the first pass introduced**: `ToolTip`
and `ToastNotification` inject legacy `overrideredirect`/`windowtype` kwargs into
`Toplevel`, so after PR B's Window normalization they emit `DeprecationWarning`s
from ttkbootstrap's own code on every tooltip hover / toast show (§3f/§3g).

Carries warn-and-normalize compat through `style/_compat.py` per the tiered
policy (2.0 renames warn through 2.x, removed in 3.0). `import ttkbootstrap`
stays warning-free.

## 2. Scope & non-goals

**In scope (7 modules / 8 classes):**
- `widgets/meter.py` — `Meter`
- `widgets/floodgauge.py` — `Floodgauge` (and the deprecated `FloodgaugeLegacy`)
- `widgets/dateentry.py` — `DateEntry`
- `widgets/labeledscale.py` — `LabeledScale`
- `widgets/scrolled.py` — `ScrolledText`, `ScrolledFrame`
- `widgets/tooltip.py` — `ToolTip`
- `widgets/toast.py` — `ToastNotification`

**Non-goals:**
- No theme/style-engine changes (Workstreams A/D/E are done).
- No new widgets/features. Consolidation, bug/leak fixes, discoverability.
- `FloodgaugeLegacy` API is **not** normalized — it already warns at runtime and
  is slated for 3.0 removal (§4.6). Only its trace leak is a candidate.
- The BootMixin ttk-wrapper widgets in `__init__.py` (`Button`, `Label`, …) are
  out — they inherit ttk's API + `bootstyle`/`icon`; nothing custom to normalize.
- `Tableview`'s deferred method-verb rename remains its own later slice.

## 3. Ground-truth inventory (per-widget summary)

Severity legend: **BUG** = crashes / wrong result; **LEAK** = lifecycle;
**NAME** = snake_case convention; **CONTRACT** = configure/cget/re-export gap;
**ROT** = dead code / docstring.

### 3a. Meter — the heaviest normalization target
- **NAME (large):** ~19 run-together constructor kwargs (`arcrange`, `arcoffset`,
  `amountmin/total/used`, `amountformat`, `wedgesize`, `metersize`, `metertype`,
  `meterthickness`, `showtext`, `stripethickness`, `textleft/right`, `textfont`,
  `subtextstyle`, `subtextfont`, `stepsize`) + 5 public `*var` attributes
  (`amountusedvar`, `amounttotalvar`, `labelvar`, `amountminvar`,
  `amountuseddisplayvar`) + child-widget attrs (`meterframe`, `textframe`). None
  forward a Tk name → all violate the convention. Compat must alias **kwargs +
  `configure`/`__getitem__` option strings + attributes**.
- **CONTRACT:** no `cget` override (custom options unreadable via `cget`);
  `amountformat` is construction-only (absent from configure/query).
- **BUG:** `metersize` double-scales on configure round-trip (grows the widget);
  `meterthickness` scales at construction but not on configure; `subtextstyle`
  reconfigure applies the wrong style suffix (and skips the left/right labels);
  `IntVar` backing truncates floats despite `Union[int,float]` + a format string;
  the `<<Configure>>` (double-bracket) resize bind is dead (never fires).
- **ROT:** stale docstring names a non-existent `meterstyle` param; a broad
  `except AttributeError: return` in `_configure_set` can hide real errors.
- **LEAK:** clean — the one write-trace is removed in `destroy()`, no `after` loops.

### 3b. Floodgauge — naming clean, contract gaps
- **NAME:** none (single-word options; `mask`/`thickness` authored-but-clean;
  `value`/`maximum`/`mode`/`orient`/`length`/`variable`/`text`/`font` mirror
  ttk.Progressbar — keep).
- **CONTRACT:** `mode` and `orient` are construction-only — passing them through
  `configure`/`cget` raises `TclError` and they're absent from `keys()`;
  `configure(opt)` returns a malformed 4-tuple (Tk spec is a 5-tuple).
- **BUG:** `maximum=0` → `ZeroDivisionError` in `_draw` (no guard);
  `cget("text")` returns the *masked* string, not the user's text (mask clobbers
  `textvariable`); `start(step_size, interval)` silently diverges from
  ttk.Progressbar's `start(interval)` — not drop-in.
- **ROT:** docstring font default (`Helvetica 14 bold`) ≠ code (`Helvetica 12`).

### 3c. DateEntry — cross-layer rename + typed-input bug
- **NAME:** `dateformat` → `date_format`, `firstweekday` → `first_weekday`,
  `startdate` → `start_date`. Surfaced in constructor + `configure` strings + the
  `dateformat` property. **These same names are echoed in `Querybox.get_date` /
  `DatePickerDialog`** (kept by PR A) — so a coordinated cross-layer rename.
- **CONTRACT:** no `cget` override; `configure(cnf="state")` returns a **dict**,
  not a ttk string; `popup_title`/`raise_exception` are construction-only.
- **BUG:** `get_date()` returns the stored `_startdate`, never the entry's typed
  text — manual keyboard edits are silently ignored; `state` else-branch uses the
  value as the key (`kwargs[v]=v`); `width` is double-applied (Frame + Entry);
  `dateformat` reconfigure skips validation.
- **GOOD:** DatePickerDialog integration is correctly on the PR A contract
  (None-on-cancel honored; cancelled picker leaves the entry untouched). Only
  `position=` is unadopted. Lifecycle clean (no binds/traces/after).

### 3d. LabeledScale — a stdlib reimplementation with a dead feature
- **RELATION:** reimplements CPython's `ttk.LabeledScale` on top of ttkbootstrap
  `Frame`; adds only `bootstyle` + a `compound` label-position option.
- **BUG:** `compound` is **dead-on-arrival** — `super().__init__(**kwargs)` runs
  *before* `compound` is popped, so `LabeledScale(compound=…)` forwards it to
  `ttk.Frame` → `TclError`; the Frame is also initialized **twice**.
- **CONTRACT:** no configure/cget round-trip (all distinctive options are
  construction-only; `_bootstyle` stored but never reused).
- **LEAK:** `destroy()` nulls `.scale`/`.label` while a queued
  `after_idle(adjust_label)` can still fire → use-after-destroy `AttributeError`
  (idle call never cancelled). Zero test coverage.
- **NAME:** clean.

### 3e. Scrolled (ScrolledText / ScrolledFrame) — un-exported + leaky
- **CONTRACT (severe):** **neither class is re-exported** — absent from top-level
  `ttkbootstrap` AND not even imported in `widgets/__init__.py` (not in `__all__`).
  Sole import path is `ttkbootstrap.widgets.scrolled`. `configure`/`cget` fall
  through to the Frame (Text/content options can't round-trip through the wrapper).
- **LEAK:** `ScrolledFrame.destroy()` is a no-op override that leaks `self.container`
  and `self.vscroll` (`self` is the *content* child; destroying it never reaches
  the parent container).
- **BUG:** `ScrolledText._on_configure` → `AttributeError` when
  `hbar=True, vbar=False`; `ScrolledFrame._measures` div-by-zero before realize;
  `yview` returns `None` instead of the `(first,last)` tuple.
- **NAME/consistency:** `autohide` → `auto_hide`, `scrollheight` → `scroll_height`;
  `vbar` (ScrolledText) vs `vscroll` (ScrolledFrame) for the same concept;
  `autohide_scrollbar` means two different things across the classes.
- **ROT:** dead eager-delegation loop (post-mixin `vars(ttk.Text)` no longer holds
  methods), dead `_on_configure`/`_text_width`/`_scroll_width`, 4 bare `except:`,
  `vbar`/`hbar` docstring error.

### 3f. ToolTip — self-inflicted deprecation + unmanaged lifecycle
- **BUG (regression):** `tooltip.py:147,149` inject `overrideredirect`/`windowtype`
  → **two `DeprecationWarning`s per hover** (via `normalize_window_kwargs`). Fix =
  one-line-each rename to `override_redirect`/`window_type` (both accepted,
  keyword-only). First-party caller tripping its own compat shim.
- **CONTRACT:** `ttk.ToolTip` doesn't exist (exported from `widgets` but not top
  level); no `configure`/`cget` (text/position only via undocumented attr-poking).
- **LEAK/BUG:** bindings set without `add="+"` → a second ToolTip (or the user's own
  `<Enter>` handler) is silently clobbered; bindings never removed; a pending
  `after` isn't cancelled on destroy (orphan timer fires into a dead widget — the
  `master=widget` trick saves only the shown Toplevel).
- **ROT:** bare `except:`; an embedded `__main__` demo in package source; docstring
  omits `justify`/`delay`/`image`.
- **NAME:** clean.

### 3g. ToastNotification — self-inflicted deprecation + dead param
- **BUG (regression):** force-injects `overrideredirect=True` into the Toplevel
  kwargs → **every `show_toast()` emits a `DeprecationWarning`** (`alpha` is fine;
  toast does not pass `windowtype`). Fix = internal `override_redirect`.
- **NAME/BUG:** `iconfont` → `icon_font` (also **dead** — `__init__` clobbers it to
  `None` and `_setup` rebuilds the font unconditionally, so the user's value never
  renders); `titlefont` → `title_font`.
- **CONTRACT:** not top-level re-exported (`ttk.ToastNotification` missing);
  constructor not keyword-only; no `configure`/`cget`; `show_toast` returns no handle.
- **LEAK:** `after` ids never stored/cancelled (duration timer + fade loop can
  double-fire); `self.toplevel` never reset to `None`; bare `except:` masks the
  resulting `TclError`s.
- **ROT:** legacy PUA icon chars (``/`◰`) — not the 2.0 font-glyph engine
  (#1094 skipped toast); contradictory `"ne = top-left"` docstring; `set_geometry`
  public despite being internal.
- **Cross-widget:** `position` is a 3-tuple `(h,v,anchor)` vs `Window`'s 2-tuple.

### 3h. Cross-cutting patterns
- **Self-inflicted deprecation warnings** (ToolTip ×2/hover, Toast ×1/show) — the
  only *regressions*; trivially fixable; user-visible now.
- **Re-export gaps** — `ToolTip`, `ToastNotification`, `ScrolledText`,
  `ScrolledFrame` are not `ttk.<Name>`; Scrolled isn't even in `widgets.__all__`.
- **`configure`/`cget` non-parity** — Meter/DateEntry/Floodgauge/Scrolled each have
  custom options that don't round-trip through `cget` (or through `configure` at all).
- **`position` means three different things** — `Window`/`Toplevel` `(x,y)`, Toast
  `(h,v,anchor)`, ToolTip a `"top left"` string.
- **Constructors are fully positional** — none use the `*` keyword-only marker the
  normalized `Window`/dialogs adopted.
- **Concrete crashers** across Floodgauge/LabeledScale/Scrolled/DateEntry/Toast.
- **Bare `except:`** in Scrolled (×4), Toast, ToolTip.

## 4. Proposed decisions (gating forks — need author sign-off)

### 4.1 Posture = **Hybrid, per widget** (mirrors the first pass)
Fix bugs / leaks / dead code / re-exports **everywhere**; apply snake_case
renames (with `_compat` warn-and-normalize aliases) **only where the surface is
non-trivial and authored** — i.e. **Meter** (big) and **DateEntry** (3 names,
cross-layer) and the two **Scrolled** names (`autohide`, `scrollheight`) + the
`iconfont` on Toast. Floodgauge / LabeledScale / ToolTip need **no** renames.
*Rationale:* naming churn is only worth it where names actually violate the
convention; the majority of the value here is bug/leak/discoverability, not casing.

### 4.2 The two self-deprecation regressions = **fix immediately (PR 0)**
Land a tiny first PR that switches ToolTip's and Toast's internal Toplevel kwargs
to `override_redirect`/`window_type`, silencing the warnings ttkbootstrap emits
about itself. No public API change, no alias needed (internal callers). *Rationale:*
it's a live regression from PR B; cheap; unblocks warning-free tooltip/toast use.

### 4.3 Re-exports = **add `ttk.<Name>` for all four** + fix Scrolled's package export
Add `ToolTip`, `ToastNotification`, `ScrolledText`, `ScrolledFrame` to top-level
`ttkbootstrap` and ensure Scrolled is imported + in `widgets/__all__` (it's absent
today). Additive, matches PR C's Tableview re-export. Keep `ttkbootstrap.widgets.*`
paths valid.

### 4.4 `configure`/`cget` parity = **add `cget` where `configure` has custom options**
Give Meter, DateEntry, and Floodgauge a `cget` override covering their custom
options (round-trip parity), and make construction-only options
(`amountformat`; Floodgauge `mode`/`orient`) reconfigurable-or-explicitly-rejected
rather than silently `TclError`. Scrolled's configure/cget delegation is a bigger
question (which target — Frame vs Text vs container?) — propose: `ScrolledText`
delegates `configure`/`cget` to the inner Text for unknown options; `ScrolledFrame`
documents container-vs-content explicitly. *Rationale:* `cget` parity is core to
"standardized" — a widget you can set-but-not-get is half an API.

### 4.5 Latent bugs + leaks = **fix in each widget's PR**
Bundle the concrete crashers (Floodgauge `maximum=0`, LabeledScale `compound` +
double-init, ScrolledText `hbar/vbar`, ScrolledFrame div-by-zero + container leak,
DateEntry `state`/`width`/typed-input, Toast/ToolTip timer + binding-clobber) and
replace bare `except:` with typed catches. Add `destroy()` teardown where missing
(LabeledScale idle-cancel, Toast timer-cancel, ToolTip after-cancel + unbind,
ScrolledFrame container-destroy).

### 4.6 `FloodgaugeLegacy` = **leave the API; fix only the trace leak (optional)**
It warns at runtime and is 3.0-removal-bound; don't invest in its API. Its
`destroy()`-less trace leak is the one defensible fix (parity with the #1070
canvas fix) — propose **optional**, low priority.

### 4.7 Cross-widget consistency (the softer forks)
- **Keyword-only constructors** after required positionals (match Window/dialogs)?
  Proposed **yes** for the widget classes being touched anyway — documented breaking,
  low incidence. *Or* leave positional to minimize breakage. **AUTHOR PICK.**
- **`position` disambiguation** — three incompatible shapes. Proposed: **document,
  don't unify** (unifying is high-breakage for little gain; Toast/ToolTip placement
  semantics genuinely differ from Window). **AUTHOR PICK.**
- **Value-access convention** (Meter `*var` attrs vs Floodgauge attrs vs
  LabeledScale `.value` property vs DateEntry `get/set`) — proposed **leave as-is**
  (unifying is broad breakage; out of scope). **AUTHOR PICK.**
- **Toast icons onto the font-glyph engine** (retire the PUA chars, like #1094) —
  proposed **defer** to a visual-polish follow-up (needs a light↔dark eyeball).

## 5. Proposed PR sequence

Smallest-blast-radius first; each PR its own headless tests + (where visual) a
light↔dark gate.

- **PR 0 — self-deprecation hotfix.** §4.2. ToolTip + Toast internal
  `override_redirect`/`window_type`. Tests: constructing/showing a tooltip and a
  toast under `-W error::DeprecationWarning` stays clean. Tiny.
- **PR 1 — re-exports + Scrolled package export.** §4.3. `ttk.ToolTip`/
  `ToastNotification`/`ScrolledText`/`ScrolledFrame`; Scrolled into
  `widgets/__init__` + `__all__`. Tests: `ttk.<Name> is <impl>`, `__all__` membership.
- **PR 2 — Meter.** §4.1/4.4/4.5. snake_case rename (kwargs + configure strings +
  `*var` attrs) via `_compat` aliases; `cget` override; fix scale round-trip +
  `subtextstyle` + dead `<<Configure>>`; float support decision. Largest PR.
- **PR 3 — DateEntry.** snake_case (`date_format`/`first_weekday`/`start_date`) +
  aliases, **coordinated with `Querybox.get_date`/`DatePickerDialog`**; `cget`; fix
  `state`/`width`/typed-input/validation. Adopt `position=` passthrough.
- **PR 4 — Floodgauge.** `cget` + `mode`/`orient` handling; `maximum=0` guard;
  `cget("text")` fix; `start()` signature decision (align vs document). Optional
  `FloodgaugeLegacy` leak fix (§4.6).
- **PR 5 — Scrolled.** `configure`/`cget` delegation; `ScrolledFrame.destroy`
  container cleanup; `hbar/vbar` + div-by-zero + `yview` return fixes; `auto_hide`/
  `scroll_height` aliases; reconcile `autohide_scrollbar`; kill dead code + bare excepts.
- **PR 6 — LabeledScale + ToolTip lifecycle.** LabeledScale `compound`/double-init
  fix + idle-cancel; ToolTip `add="+"` binding + after-cancel + unbind on destroy +
  move `__main__` demo to `examples/`. (Grouped: both small, both mostly lifecycle.)
- **(Deferred) Toast font-glyph icons** — §4.7, visual-polish follow-up.

## 6. Compat & deprecation strategy

Same as the first pass: renames via `style/_compat.py` warn-and-normalize through
2.x, removed 3.0. Meter/DateEntry/Scrolled/Toast old kwarg **and** `configure`/
`__getitem__` option-string **and** public-attribute names accepted with a
`DeprecationWarning` naming the new form (attributes via `__getattr__`). Positional/
keyword-only changes and any behavior fixes (float support, `get_date` reading typed
text) are documented in `2_0_breaking_changes.md`. `import ttkbootstrap` stays
warning-free.

## 8. Borrowed bootstack mechanisms (per widget)

Six parallel comparison agents (2026-07-07) mined bootstack's equivalents for
mechanisms — **not** API — that resolve the §3 rough edges. Standing rule
(`borrow-bootstack-mechanisms-not-api`): borrow the technique, never the public
surface. Verdicts: **BORROW** (adopt the mechanism), **ADAPT** (borrow the idea,
re-express for ttkbootstrap), **SKIP** (bootstack no better / API-coupled).

### 8.0 The backbone: a shared configure-delegation mixin
bootstack's `_impl/mixins/configure_mixin.py` `ConfigureDelegationMixin` +
`@configure_delegate('name')` came back as the **#1 borrow for Meter, Floodgauge,
AND Scrolled** (and helps DateEntry). One decorated get+set method per option;
`__init_subclass__` walks the MRO once and builds a `key→handler` map at
class-creation; `configure`/`config`/`cget`/`__getitem__`/`__setitem__` all route
through it with a `super()` fallback and emit proper Tk **5-tuples**. **ADOPT as a
private `internal/` mixin** (e.g. `internal/configure_delegation.py`), registered
against ttkbootstrap's **existing option names** (not bootstack's). It gives `cget`
for free, get/set symmetry, reconfigurable options, and deletes the hand-maintained
`_configure_get`/`_configure_set` if/else ladders where the bugs live. **Caveat
(from the Scrolled agent):** the mixin only handles a class's *own* registered keys;
inner-widget pass-through (e.g. `ScrolledText.configure(font=…)` → the Text) is a
fallthrough ttkbootstrap must ADD (try `super()`, on unknown-option `TclError` retry
on the inner widget). This mixin is the spine of PRs 2/4/5 and part of 3.

### 8a. Meter
- **BORROW** the delegation mixin (§8.0) — kills the ladders, adds `cget`, makes
  `amountformat` settable.
- **BORROW (discipline)** single-seam scaling: store geometry logical, never write a
  scaled value back into an option field, scale only at render seams — dissolves the
  `metersize` double-scale + round-trip drift. *Caveat:* a literal port makes the
  meter DPI-size-independent (behavior change); confine scaling to the two draw
  methods if HiDPI growth must stay.
- **ADAPT (delete)** the dead `<<Configure>>` bind — bootstack has no resize-follow;
  redraw comes from the `metersize` option path.
- **SKIP** float default (bootstack still defaults `IntVar` — our unconditional
  `DoubleVar` is ahead) and the canvas-item text layer (nice but a big rewrite; note
  `_update_or_create_text` `itemconfig`-not-recreate for a future text-layer pass).

### 8b. Floodgauge
- **BORROW** the delegation mixin (§8.0) — fixes the malformed 4-tuple (→ 5-tuple in
  one place) and the construction-only `mode`/`orient` trap (make them live
  delegates that redraw; `orient` also swaps canvas w/h).
- **BORROW** the zero-range guard (`if range==0: ratio=0`) — the `maximum=0` crash.
- **BORROW** the value-vs-display split: authoritative numeric var + a *separate*
  derived display string for the mask; never `.set()` the masked string back onto the
  user's `textvariable` — fixes `cget("text")`.
- **SKIP** animation + teardown — bootstack's Gauge has no animation loop and a
  *thinner* teardown; Floodgauge's `_after_id` cancel + trace removal is already
  better. Don't regress. (`start()` signature realignment is an API call, §7 Q3.)

### 8c. DateEntry
- **BORROW (pattern)** read the value from the **live entry text**, not the
  `_startdate` shadow (shadow only as empty/unparseable fallback) — the fix for typed
  edits being ignored. bootstack proves the architecture; we write the parse.
- **BORROW** `_dateutils.coerce_date` — a tolerant, non-throwing multi-format→`date`
  parser; the engine behind read-from-text and a blur-time validator.
- **ADAPT** single canonical `state`: `cget("state")` returns the *entry's* state
  string; `configure(state=…)` fans out to entry+button through one path (drop the dict).
- **ADAPT** blur/manual validation (`<FocusOut>` + a `strptime`/`coerce_date` check
  marking the entry `invalid`) without importing the full `<<Valid>>`/`<<Invalid>>`
  event pipeline; and explicit kwarg partitioning (each kwarg → one widget) to kill
  the `width` double-apply; and a picker re-entrancy guard.
- **SKIP** `dateformat` reconfigure (bootstack uses ICU presets, no raw-strftime to
  re-validate) — fix with the existing `_validate_dateformat`.
- **Cross-layer:** the `start_date`/`first_weekday` rename must also touch
  `Querybox.get_date`/`DatePickerDialog` (which still carry the old names).

### 8d. Scrolled
- **BORROW (high value)** the class-tag mousewheel seam: bind the wheel handler once
  to a per-instance `bind_class` tag; enable/disable by inserting/removing the tag in
  a widget's `bindtags`. Fixes the O(subtree) per-crossing rebind, the `unbind`
  clobber of app wheel handlers, and gives location-independent teardown
  (`unbind_class` in `destroy()`).
- **BORROW** grid layout for viewport + bars instead of `place()` + manual relwidth
  math — deletes the `_on_configure` `AttributeError` (hbar/no-vbar) outright and is
  the substrate for a stable scrollbar gutter (`minsize` retained through
  `grid_remove` → no reflow-flicker).
- **BORROW** always return `(first,last)` from `yview`/`xview` (delegate to the real
  scroll source) — fixes the `None` return; guard fraction math with `max(1, outer)`
  + an unrealized-geometry early return — fixes `_measures` div-by-zero.
- **ADAPT + FORK** the container leak: the *deep* fix is outer-frame ownership + a
  Canvas/`create_window` viewport (content becomes a child → native destroy cascade;
  also gives native scroll fractions). That's an internal-structure change (§7 Q6).
  The *stopgap* is a flag-guarded `destroy()` that also destroys `self.container`.
- **ADAPT** a unified `scrollbar_visibility` mechanism shared by both classes (kills
  the two-meanings `autohide_scrollbar`) + a flicker-free timer `'scroll'` mode.
- **Caveat:** bootstack does **not** solve inner-widget `configure`/`cget`
  pass-through either — that fallthrough is ours to add (§8.0 caveat).

### 8e. ToolTip
- **BORROW** `add="+"` binds with stored funcids + paired `unbind` in `destroy()` —
  fixes the silent handler-clobber (~5 lines).
- **BORROW** a `<Destroy>` self-release handler with the `event.widget is not
  self._widget` guard + `winfo_exists()` re-check in `show_tip` — fixes the orphaned
  timer firing into a dead widget.
- **ADAPT** route placement through `internal/positioning.ensure_on_screen` + measure
  with `winfo_reqwidth/reqheight` — replaces the bare-`except` 200×50 guess with
  multi-monitor clamping. *Verify* `internal/positioning.py` carries the off-screen
  *flip* helpers (`_check_offscreen`/`_flip_anchor_*`), not just `place_window_center`
  — PR B took a "subset"; pull the clamp/flip helpers over if missing. Re-express
  bootstack's 160-line anchor ladder as a small offset table, don't copy it.
- **ADAPT** hold the `_label` ref and reconfigure a live popup on update (into our own
  `configure`/`cget`, not a bare `text` property).
- **SKIP** the Toplevel kwargs — bootstack injects the *same* legacy
  `overrideredirect`/`windowtype`; the PR-0 fix is ours. (Minor: it `.copy()`s kwargs
  before mutating — do that.)
- **Optional (out of scope):** container-hover (`_pointer_within_target` +
  subtree bindtag propagation) for tooltips on container widgets.

### 8f. Toast
- **BORROW** off-screen-measure-then-place (deiconify off-screen at 2×screen,
  `update_idletasks()`, *then* set geometry) — fixes the withdrawn-window
  `winfo_height()==1` mismeasure + reposition flash.
- **BORROW** `winfo_exists()` teardown guards + `destroy()` nulling the handle,
  replacing the bare `except:`. *Go further than bootstack:* store the duration + fade
  `after` ids and `after_cancel` them (bootstack never cancels its timers).
- **BORROW** render the icon via ttkbootstrap's **own** font-glyph engine
  (`Icon`/`icon_element`) — delete the dead `iconfont` param + the PUA chars.
- **BORROW** `show_toast()` returns a dismiss handle (`self`); a public idempotent
  `hide()`. **BORROW** explicit named window kwargs + `window_type='tooltip'` on aqua
  instead of self-injecting `overrideredirect`.
- **NOTE (no fade in bootstack):** it destroys instantly — so there's no cancellable
  -fade to borrow; dropping the fade to an instant destroy is a legit consolidation
  option (§7 Q7).
- **SCOPE-FORK — the toast STACK manager** (`toast_stack.py`: per-corner list +
  running-offset reflow + reflow-on-dismiss via a `place=` hook seam). Genuinely
  valuable (concurrent toasts overlap today) but **feature-grade** — gate against
  "no new features" (§7 Q7). If adopted: port the mechanism onto PR B's
  `internal/positioning.py` substrate; keep our `position=(x,y,anchor)` API.

### 8g. LabeledScale
No bootstack equivalent surveyed (it has a scale *builder* but no labeled-scale
composite). Its fixes (`compound` double-init, after_idle use-after-destroy) are
self-contained and don't need a bootstack mechanism — handled in PR 6.

## 7. Open questions (for author)

**Resolved (2026-07-07):** Meter/LabeledScale → `DoubleVar` (old Q2); constructors
→ keyword-only (§4.7); adopt the configure-delegation mixin as a shared
`internal/` backbone (§8.0). Remaining:

1. **Confirm the §4 forks** — esp. 4.1 (which widgets get renames) and 4.7's softer
   pair: `position` **unify or document** (three incompatible shapes)? value-access
   convention **leave-as-is**? (Proposed: document / leave-as-is.)
2. **Floodgauge `start()`** — realign to ttk's `start(interval)` (breaking, needs a
   shim) or keep the `step_size`-first signature and just document the divergence?
3. **ScrolledFrame container leak — deep fix vs stopgap (§8d).** The durable fix is
   the outer-frame + Canvas-`create_window` viewport rewrite (also fixes div-by-zero
   + `yview` contract, but an internal-structure change, arguably past "consolidation
   only"); the stopgap is a flag-guarded `destroy()` that tears down `self.container`.
   **Deep rewrite now, or stopgap now + rewrite as a later slice?** (Proposed:
   stopgap + grid/yview/wheel fixes now; Canvas-viewport rewrite is its own slice.)
4. **Toast — two scope calls (§8f).** (a) The **toast STACK manager** (concurrent
   non-overlapping toasts) — in scope, or defer as feature-grade? (b) Keep the fade
   animation (make it cancellable) or **drop it to an instant destroy** (bootstack
   has none)? (Proposed: defer the stack; keep a cancellable fade.)
5. **PR 0 now** — land the self-deprecation hotfix (ToolTip + Toast internal
   `override_redirect`/`window_type`) immediately as its own small PR? (Confirmed live
   regression; no API change.) You redirected this into the bootstack pass — which is
   now done and confirmed bootstack injects the *same* legacy kwargs, so the fix is
   ours regardless.