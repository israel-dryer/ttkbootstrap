# ttkbootstrap 2.0 — Shipped-Widget API Normalization (design pass)

> Design pass for the deferred **shipped-widget API normalization** workstream:
> `Window`/`Toplevel`, the `dialogs/` package, and `Tableview`. Follows the 2.0
> hard rule (design pass before implementation). Pair with `2_0_plan.md`,
> `2_0_handoff.md`, and the docs design `2_0_docs_design.md` §11a.
>
> **Status: CONFIRMED (author sign-off 2026-07-07).** The four gating forks (§4)
> were drafted from a full ground-truth survey while the author was away and then
> **approved as-is** ("I'm good with your defaults"). Implementation proceeds
> PR-by-PR per §8, starting with **PR A (dialogs)**.

## 1. Why this, why now

`Window`, the dialogs, and `Tableview` are the shipped widgets that never got a
2.0 API cleanup. The docs design (`2_0_docs_design.md` §11a) explicitly deferred
this and *accepted docs-first*. The author reversed that on 2026-07-07: do the
**API pass first** so the Workstream-H docs get written against normalized
signatures instead of provisional ones, avoiding the §11a rework tax (autogen
API Reference regenerates for free; the fragile hand-written catalog/How-To
examples get written once, correctly).

This is **its own workstream**, not Workstream H. It carries warn-and-normalize
compat through `style/_compat.py` per the tiered deprecation policy (new 2.0
standardizations warn-and-normalize through 2.x, removed in 3.0).

**Reference project:** per author steer (2026-07-07, memory
`prefer-bootstack-reference`), borrow **mechanisms** (not API) from bootstack at
`D:/Development/bootstack`, especially its cross-platform / Tcl-Tk quirk handling.
Relevant bootstack files are cited inline below.

## 2. Scope & non-goals

**In scope (3 surfaces):**
- `src/ttkbootstrap/window.py` — `Window`, `Toplevel`.
- `src/ttkbootstrap/dialogs/` — `base.py`, `message.py`, `query.py`,
  `colorchooser.py`, `colordropper.py`, `datepicker.py`, `fontdialog.py`, and the
  `Messagebox`/`Querybox` facades.
- `src/ttkbootstrap/widgets/tableview.py` — `Tableview` + `TableColumn`/`TableRow`.

**Non-goals:**
- No theming/style-engine changes (that work is complete — Workstreams A/E/D).
- No new widgets or features. Consolidation only.
- The Tableview method-verb *rename* is **deferred** to a later slice (see §4.4);
  this pass fixes bugs, dead code, discoverability, and re-exports.

## 3. Ground-truth inventory (summary)

Full per-surface inventories were produced by survey agents (2026-07-07). The
load-bearing findings:

### 3a. `Window` / `Toplevel`
- `size`/`position` are split tuple params (bootstack `App`/`Toplevel` use the
  same shape — validated); but `position` hardcodes `f"+{x}+{y}"` → cannot
  express edge-relative (`-x`/`-y`) offsets, and size+position are two separate
  `geometry()` calls.
- **`iconphoto` diverges** between the classes: `Window` treats `''`→brand icon,
  `None`→skip, path→load-with-fallback (typed `Optional[str]`); `Toplevel` types
  it plain `str=''`, `''`→skip, has no `None` path (so `iconphoto=None` →
  `PhotoImage(file=None)` crash) and no embedded default.
- `iconify` is smuggled through `**kwargs` on `Toplevel` (popped at
  `window.py:517-520`) instead of being a real param.
- `style` is a stored `self._style` on `Window` but a fresh `Style()` call on
  `Toplevel` — inconsistent implementation of the same property.
- No keyword-only marker on ~14-param constructors (everything positional-or-kw).
- Attribute params mirror raw Tk names (`overrideredirect`, `windowtype`,
  `toolwindow`, `topmost`, `hdpi`) rather than snake_case; `hdpi` **and**
  `scaling` both drive `enable_high_dpi_awareness`.
- `Window` has `themename`/`default_button`/`hdpi`/`scaling`; `Toplevel` has none
  (inherits app theme) — acceptable divergence, keep.
- Already-correct: the x11 `<Visibility>` alpha deferral is present in both (it
  mirrors bootstack's `on_visibility_alpha`); `place_window_center` +
  `position_center` alias exist in both.

### 3b. Dialogs
- Package is split (there is **no** `dialogs.py`). Base `Dialog(BaseWidget)` owns
  a lazily-built `Toplevel`. `MessageDialog`/`QueryDialog`/`FontDialog`/
  `ColorChooserDialog` subclass it; **`DatePickerDialog` and `ColorDropperDialog`
  do not** (plain classes; `DatePickerDialog` blocks inside `__init__` via
  `grab_set()`/`wait_window()`, so it has no `show()`).
- `parent` is **consistent** across the dialog surface (only the embeddable
  `ColorChooser` `ttk.Frame` uses `master`, which is defensible — it's a child
  widget, not a popup). **Note:** bootstack is *less* consistent here (its base
  `Dialog`=`parent`, all facades=`master`) — do **not** copy bootstack's drift;
  ttkbootstrap's `parent`-everywhere is the better target.
- Content arg splits `message` (MessageDialog/Messagebox) vs `prompt`
  (QueryDialog/Querybox). Arguably a real semantic distinction (told vs asked) —
  keep both, but document.
- **`Messagebox` positional order flips**: `show_*`/`ok` order `parent, alert`;
  `okcancel`/`yesno`/`yesnocancel`/`retrycancel` order `alert, parent`. A
  positional 3rd arg means `parent` in five methods and `alert` in four.
- `position`, `buttons`, `icon`, `localize` are **undiscoverable `**kwargs`** on
  the facades (not named params).
- **Return conventions diverge four ways**: `.result` property (Messagebox,
  `get_color`, `get_font`) vs private `._result` (`get_string`/`get_item`/
  `get_integer`/`get_float`, bypassing the property's `grab_release()`) vs bespoke
  `date_selected` (`get_date`) vs a traced `Variable` (`ColorDropperDialog`).
- **`get_date` can never signal cancellation** — `date_selected` defaults to
  `startdate or today()` and is never reset, so it always returns a `date`.
- `get_date` and `ColorDropperDialog.show()` are the only entry points with **no
  `position` support**.
- `MessageDialog.command` is typed `Optional[Tuple[Callable, str]]` but invoked as
  a zero-arg `command()` — tuple form vestigial.
- Two identical `ColorChoice` namedtuples (`colorchooser.py:75`,
  `colordropper.py:55`).
- **Dialogs are not re-exported at top level** (only via `ttkbootstrap.dialogs`).

### 3c. `Tableview`
- **Not re-exported** — no `ttk.Tableview` (every other widget is top-level);
  only `from ttkbootstrap.widgets.tableview import Tableview`.
- Verb sprawl: `get_`/`insert_`/`delete_`/`purge_`/`unload_`/`build_`;
  `move_selected_row_up` vs `move_row_down` (drops `selected` + the `_rows_`
  pattern); columns use `hide`/`unhide` while row/column objects use `show`/`hide`.
- `configure(cnf=...)` on `Tableview` vs `configure(opt=...)` on
  `TableColumn`/`TableRow`.
- **Dead/vestigial**: `reset_row_sort` body is literally `...`;
  `_build_table_rows`/`_build_table_columns` are superseded and unused;
  commented-out `_select_pagesize` (2525-2528); `get_columns` documented as a
  duplicate of the `tablecolumns` property; `maxwidth` in the `coldata` docstring
  has no implementation.
- **Latent bugs**: `delete_column` line 961 `self.cidmap(int(cid))` (calls a dict
  → `TypeError`); `TableHeaderRightClickMenu.__init__` line 2791
  `self.master = self.master` (self-assignment; never sets from arg); `insert_row`
  uses `print('[TableView] …')` for a diagnostic instead of raising/logging.
- `coldata`/`rowdata` are terse vs the stored `tablecolumns`/`tablerows`.

## 4. Proposed decisions (the four gating forks)

> **All four are PROPOSED defaults, pending author confirmation.** Rationale
> included so the author can accept or redirect quickly.

### 4.1 Posture = **Hybrid**
Aggressively normalize the small, high-value surfaces (`Window`/`Toplevel` +
dialogs) with warn-and-normalize aliases via `_compat`; on `Tableview`, fix
bugs / dead code / discoverability + add the re-export, but **keep established
method names** (the verb rename is a separate later slice). Rationale: Window and
dialogs are heavily used and their inconsistencies are cheap to fix behind
aliases; Tableview's method surface is huge (≈70 public methods) and a rename
there is mostly doc/example churn for modest gain — better as its own scoped slice
once the docs exist to update in lockstep.

### 4.2 Window = **port bootstack mechanisms**
Centralize the `winsys`-branched attribute handling and adopt a shared positioning
utility, rather than leaving per-attribute branching inline. Rationale: this is
exactly the cross-platform/Tcl-Tk-quirk surface the author flagged for bootstack
reuse, and bootstack has already solved the edge cases (aqua override-redirect
no-op, multi-monitor centering, on-screen clamping, the unified `windowtype`
switch). See §5a for the concrete shape.

### 4.3 Dialog returns = **unify + fix `get_date`**
Route every entry point through the `.result` property; make `get_date` return
`None` on cancel (BREAKING — currently always returns a date) so cancellation is
detectable like every other `get_*`. Rationale: the always-returns-a-date behavior
is a silent footgun (callers can't tell "user picked today" from "user cancelled").
This is the one genuinely breaking change in the pass; it gets a prominent
migration note. The `None`-vs-`""` distinction for `get_string`/`get_item` is kept
but documented.

### 4.4 Tableview = **fix + re-export, keep names; defer the verb rename**
This pass: add `ttk.Tableview` (+ `TableColumn`/`TableRow`) re-export, fix the
latent bugs, delete dead code (the `reset_row_sort` stub, the two unused private
builders, the commented method), replace `print()` diagnostics with a raised
error, and surface the hidden/undocumented params. The method-verb rename
(`move_row_down`→`move_selected_row_down`, `hide/unhide`→`hide/show`,
`coldata`/`rowdata` aliases, etc.) is deferred to its own slice with deprecated
aliases, tracked in §8.

## 5. Proposed normalized API

### 5a. `Window` / `Toplevel`

**Introduce a private `_BaseWindow` mixin** (mirrors bootstack's `BaseWindow`,
`bootstack/src/bootstack/_runtime/base_window.py`) holding the shared wm/geometry/
attribute/icon logic, so `Window` and `Toplevel` stop duplicating (and drifting
on) it. Keep the public `Window`/`Toplevel` split (bootstack keeps App/Toplevel
split too; ttkbootstrap's `Window`==root, `Toplevel`==secondary is the right
model — do **not** merge them).

Concrete changes:
1. **Unify `iconphoto` semantics** across both classes via one `_setup_icon`
   helper: `None`→skip, `''`→default (brand icon on `Window`, inherit on
   `Toplevel`), path→load-with-fallback. Fix the `Toplevel` `None` crash. (bootstack
   ref: `base_window.py:264-322`, incl. `.ico`→`wm_iconbitmap` on win32.)
2. **Promote `iconify` to a real keyword-only param** on `Toplevel`; stop popping
   it from `**kwargs`.
3. **Make the `style` property identical** in both (return the singleton
   consistently).
4. **Add a `*` keyword-only marker** after the first 1–2 positional params
   (`title`, and for `Window` `themename`) — the ~14-param positional surface is a
   fragility trap. This is technically breaking for anyone passing later args
   positionally; warn-and-normalize is not possible for positional args, so this
   is a documented breaking change (low real-world incidence — nobody passes
   `alpha` as the 14th positional).
5. **Snake_case the raw-Tk-mirroring params** with deprecated aliases via
   `_compat`: `overrideredirect`→`override_redirect`, `windowtype`→`window_type`,
   `toolwindow`→`tool_window`, `hdpi`→`high_dpi`. (bootstack public layer uses
   `override_redirect`; note bootstack's own runtime/public `minsize` vs
   `min_size` drift — we pick **one**: keep `minsize`/`maxsize` since they mirror
   the Tk method names the tuple wraps, and consistency-with-Tk wins here.)
6. **Fix the `+{x}+{y}` limitation**: accept negative offsets in `position`
   (emit `f"{x:+d}{y:+d}"`) so edge-relative placement works; optionally accept a
   single combined `geometry="WxH+X+Y"` passthrough. Apply size+position as one
   combined geometry string when both are given.
7. **Adopt a shared positioning utility** — a private
   `internal/positioning.py` (ported subset of bootstack's `WindowPositioning`,
   `bootstack/src/bootstack/_runtime/window_utilities.py`): `center_on_screen`,
   `center_on_parent`, `ensure_on_screen` (clamp into the monitor). Re-point
   `place_window_center` at it (it currently ignores titlebar height and is not
   multi-monitor aware). Establish the **priority `position > center_on_parent >
   center_on_screen`** (bootstack `base_window.py:169-179`). Multi-monitor via
   optional `screeninfo` with a graceful single-screen fallback (no new hard dep).
8. **Aqua `overrideredirect` no-op guard** (bootstack `base_window.py:619-639`) —
   `overrideredirect(True)` silently no-ops on macOS where it hangs/misbehaves.
9. **Consider the `windowtype` unified switch** (bootstack `toplevel.py:117-206`):
   `'splash'`/`'tooltip'`/`'dock'`/`'utility'` → the right native primitive per
   platform. *Optional for this pass* — flag as a stretch item; the minimum is
   the x11 `-type` passthrough that already exists.
10. **AppUserModelID taskbar fix** (bootstack `app.py:534-540`) — on win32 set
    the explicit AppUserModelID so the taskbar shows the app icon, not
    `python.exe`. Low-risk, high-polish; include.

### 5b. Dialogs

1. **Keep `parent` everywhere** (already consistent); leave `ColorChooser`'s
   `master` as-is (embeddable widget). Do not adopt bootstack's `master` facade
   convention.
2. **Fix `Messagebox` positional-order inconsistency**: make `(message, title,
   parent, alert, ...)` the uniform order; the four flipped methods
   (`okcancel`/`yesno`/`yesnocancel`/`retrycancel`) change. Since `parent`/`alert`
   are almost always passed by keyword, real breakage is low; document it. Add a
   `*` keyword-only marker after `message, title`.
3. **Promote `position`, `buttons`, `icon`, `localize` to named params** on the
   facades (discoverability); keep `**kwargs` passthrough for forward-compat.
4. **Unify the result convention on the `.result` property** for all
   `Dialog`-based entry points; route `get_string`/`get_item`/`get_integer`/
   `get_float` through `.result` (so `grab_release()` runs consistently).
5. **`get_date` returns `None` on cancel** (§4.3). Detect real selection vs
   window-close; return `None` when closed without a pick. Prominent migration note.
6. **Add `position` support to `get_date`** (it has none today) via the standard
   `show(position=...)` path. `DatePickerDialog` gains a `show()` and stops
   blocking inside `__init__` (align it to the `Dialog` lifecycle — makes it a
   proper `Dialog` subclass or at least gives it the same `show`/`result` seam).
   `ColorDropperDialog` stays fullscreen (no position — genuinely N/A).
7. **De-vestigialize `MessageDialog.command`**: accept a plain `Callable`; keep
   the tuple form working through `_compat` with a deprecation warning.
8. **Dedupe `ColorChoice`** — one definition, imported by both modules.
9. **Re-export the public dialog surface at top level** (`ttkbootstrap.Messagebox`,
   `ttkbootstrap.Querybox`, and the dialog classes) to match the widgets — resolves
   the "widgets exported, dialogs not" asymmetry. (Keep `ttkbootstrap.dialogs.*`
   valid.)

### 5c. `Tableview` (this pass — fixes only, per §4.4)

1. **Re-export** `Tableview`, `TableColumn`, `TableRow` from
   `widgets/__init__.py` and top-level `ttkbootstrap` (→ `ttk.Tableview`).
2. **Fix latent bugs**: `delete_column`'s `self.cidmap(int(cid))` →
   `self.cidmap[str(cid)]` (subscript, correct key type);
   `TableHeaderRightClickMenu` `self.master = self.master` → set from the arg.
3. **Delete dead code**: the `reset_row_sort` `...` stub (or implement it — decide
   during impl; leaning delete since `reset_column_sort` covers the real need),
   the unused `_build_table_rows`/`_build_table_columns`, the commented
   `_select_pagesize`.
4. **Replace `print()` diagnostics** (`insert_row` empty-values path) with a
   raised `ValueError` (or a no-op with a real warning) — library code must not
   print to stdout.
5. **Fix the `coldata` docstring** (drop the unimplemented `maxwidth`, or
   implement it — leaning doc-fix).
6. **Deprecated verb-rename aliases are OUT of this pass** — tracked in §8 as the
   follow-up slice.

## 6. Compat & deprecation strategy

All new-in-2.0 renames go through `style/_compat.py` (the existing quarantine),
warn-and-normalize through 2.x, removed in 3.0:
- Old kwarg names (`overrideredirect`, `windowtype`, `toolwindow`, `hdpi`, the
  `command` tuple form) accepted with a `DeprecationWarning` that names the new
  form. Implement as a small `_normalize_kwargs(old→new)` helper reused by
  `Window.__init__`, `Toplevel.__init__`, and `MessageDialog`.
- **Positional-order and keyword-only changes cannot be shimmed** (positional args
  carry no name) → these are documented breaking changes, kept to the few listed
  above, all low-incidence.
- `get_date` cancellation is a documented breaking behavior change (no shim
  possible for a return value).
- **`import ttkbootstrap` stays warning-free** — warnings fire only when a
  deprecated form is actually used.

All breaking/behavioral changes are recorded in
`development/2_0_breaking_changes.md` (the existing running log) and feed the
Workstream-H "Migrating to 2.0" page.

## 7. bootstack references (mechanisms borrowed)

| Concern | bootstack source | Adopt as |
|---|---|---|
| Shared window logic mixin | `_runtime/base_window.py` | private `_BaseWindow` in `window.py` |
| Positioning / clamping | `_runtime/window_utilities.py` (`WindowPositioning`) | private `internal/positioning.py` (subset) |
| Center priority (pos>parent>screen) | `base_window.py:169-179` | `_setup_window` ordering |
| x11 `<Visibility>` alpha deferral | `base_window.py:31-44,240-262` | already present — keep |
| aqua override-redirect no-op | `base_window.py:619-639` | guard in both classes |
| Unified `windowtype` switch | `toplevel.py:117-206` | *stretch* item (§5a.9) |
| win32 AppUserModelID taskbar | `app.py:534-540` | `Window.__init__` (win32) |
| Icon platform branching (.ico) | `base_window.py:264-322` | `_setup_icon` helper |

We borrow mechanisms only. We do **not** adopt bootstack's `master`-facade dialog
convention (ttkbootstrap's `parent` is more consistent) nor its `min_size`/`max_size`
public rename (we keep Tk-mirroring `minsize`/`maxsize`).

## 8. Proposed PR sequence

Three independently-reviewable PRs against `2.0`, each with its own visual/headless
gate. Recommended order (smallest-blast-radius first):

- **PR A — Dialogs normalization.** §5b. Result unification, `get_date` cancel fix
  + position, `Messagebox` order, named facade params, `ColorChoice` dedupe,
  top-level re-exports, `command` de-vestigialize. New/updated tests in a headless
  `tests/test_dialogs_api.py` (result conventions, cancel→None, kwarg normalization).
  Human spot-check: each dialog opens/positions/returns correctly light+dark.
- **PR B — Window/Toplevel normalization. OPEN — PR #1103 (branch
  `feat/2.0-shipped-api-window`).** §5a. `_BaseWindow` mixin (`Window(_BaseWindow,
  tk.Tk)` / `Toplevel(_BaseWindow, tk.Toplevel)`) holding the shared
  icon/geometry/alpha/positioning/`style` logic; `_setup_icon` (unified `None`/`''`/
  path semantics, fixes the `Toplevel(iconphoto=None)` crash, `.ico`→`wm_iconbitmap`
  on win32, bad-path → `UserWarning` not `print`); new private
  `internal/positioning.py` (subset of bootstack's `WindowPositioning`:
  `center_on_screen`/`center_on_parent`/`ensure_on_screen`, optional `screeninfo`,
  graceful single-screen fallback) re-pointing `place_window_center`; snake_case
  aliases via `_compat.normalize_window_kwargs` (`hdpi`/`overrideredirect`/
  `windowtype`/`toolwindow`); keyword-only constructors after the leading
  positional(s); `iconify` promoted to a real `Toplevel` kwarg; edge-relative +
  combined `geometry` (`f"{x:+d}{y:+d}"`); aqua `overrideredirect` no-op guard;
  win32 AppUserModelID. First-party caller `dialogs/base.py` migrated
  `windowtype`→`window_type`. New `tests/test_window_api.py` (+15). Suite **317
  passed** excl. the known `nl.msg` flake; warning-free import + end-to-end smoke
  (new API, legacy-kwarg warnings, centering, singleton `style`) verified.
  **Cross-platform is the residual risk — still wants a manual check on win32 +
  (if available) x11/aqua** before/at merge. **Deferred to a fast-follow (noted
  here, not done in PR B):** the richer bootstack positioning surface
  (`place_center_on`/`place_at`/`place_anchor`/`place_dropdown`/`place_cursor`),
  the `windowtype` unified switch (§5a.9), and routing the dialogs'
  `internal/utility.center_on_parent` through the new `positioning` module — all
  out of PR B's minimal scope.
- **PR C — Tableview fixes + re-export.** §5c. Bug fixes, dead-code removal,
  `print()`→error, re-export. Tests: re-export presence, the two bug regressions,
  no-stdout-on-empty-insert.

**Deferred follow-up slice (own design mini-pass):** Tableview method-verb rename
with deprecated aliases (`move_row_down`, `hide/unhide`, `coldata`/`rowdata`,
`configure(cnf=)` vs `(opt=)`, export-method naming). Do it once the Workstream-H
Tableview docs exist so names + docs move together.

## 9. Open questions (for author)

1. **Confirm the four §4 forks** (posture, window scope, `get_date` breaking fix,
   Tableview depth). These gate PR structure.
2. **`windowtype` unified switch** (§5a.9) — include now or leave as x11-only
   passthrough? (Leaning: leave for the follow-up to keep PR B focused.)
3. **`reset_row_sort`** — delete the stub or implement it? (Leaning: delete;
   `reset_column_sort` + `reset_table` cover the need.)
4. **`min_size`/`max_size`** — confirm we keep Tk-mirroring `minsize`/`maxsize`
   (not bootstack's public `min_size`). (Leaning: keep `minsize`/`maxsize`.)
5. **`new dep `screeninfo`** for multi-monitor centering — acceptable as an
   *optional* import (graceful fallback), or avoid entirely and single-screen
   only? (Leaning: optional import, no hard dep — matches "Pillow is the only
   runtime dep".)