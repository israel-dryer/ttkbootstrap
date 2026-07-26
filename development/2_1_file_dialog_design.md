# ttkbootstrap 2.1 — in-house themed file dialog (design brief)

> Design brief for a **themed, in-library file dialog** that replaces Tk's
> unstyled `tkfbox.tcl` chooser on X11 (opt-in elsewhere). Tracked 2.1 issue
> **#1242** (milestone 2.1). The last remaining 2.1 build and the designated
> drop-candidate if the milestone must close sooner.
>
> **Status: CONFIRMED — design session held 2026-07-26; §10 settled (see below).**
> Direction: **reproduce `tkfbox.tcl`'s layout with themed ttk widgets** rather
> than invent a new dialog or lift the `development/filedialogs/` prior art.
> Additive and backward-compatible — the native OS dialogs stay the default on
> Windows/macOS. Implementation proceeds per the §9 PR shape.

## 1. Motivation & author intent

Every standard dialog ttkbootstrap surfaces is themed **except** the file
dialog, because on Windows and macOS the OS draws it natively (and beautifully).
On **X11 there is no native chooser** — Tk falls back to `tkfbox.tcl`, whose
central file listing is a `::tk::IconList` **Canvas** with a hardcoded white
panel that no ttk styling can reach. In a dark theme it's a jarring white slab;
in any theme it ignores the palette entirely. (#1224 fixed the *surrounding*
ttk chrome's dark-mode base styles; the Canvas itself remained unreachable,
which is why #1224 was closed as subsumed by this issue.)

The author's scoping call (verbatim intent): *"imitate what is already produced
from `tkfbox.tcl` but with themed widgets."* So this is **not** a from-scratch
dialog design — it is a faithful re-implementation of a layout users already
know, with the one un-themeable widget swapped out and the backend moved from
Tcl into Python.

`Querybox` already exposes the four file operations as wrappers over
`tkinter.filedialog` (`get_open_filename` / `get_open_filenames` /
`get_save_filename` / `get_directory`, `dialogs/query.py:391`), each normalizing
the stdlib `""`-on-cancel to `None`. Those stay the public entry points; only
what they *call* changes on X11.

## 2. The target — what `tkfbox.tcl` renders

Three stacked regions inside a `ttk::frame` (from `tkfbox.tcl` `::tk::dialog::file::Create`):

| Region | Contents | Themed today? |
|---|---|---|
| **Top bar** (`f1`, pack top fill-x) | `Directory:` label · path **menubutton** (`-direction flush`, textvariable = current path, dropdown of parent dirs) · **up-dir** button (image) | ✅ ttk |
| **Center** (pack expand fill-both) | `::tk::IconList` — a **Canvas** icon grid of folder/file entries | ❌ **the white panel — the whole problem** |
| **Bottom form** (`f2`, pack bottom fill-x, a `grid`) | Row 0: `File name:` label · **entry** · **OK** ; Row 1: `Files of type:` label · type **menubutton** · **Cancel** ; Row 2: `Show hidden` **checkbutton** (columnspan) | ✅ ttk |

So "imitate with themed widgets" collapses to a small statement: **keep the
layout, replace the one Canvas, drive it from Python.** Directory-chooser mode
(`TkChooseDir`) is the same skeleton minus the filetype menubutton, with the
name caption relabeled `Selection:`.

## 3. The one hotspot — the center listing

The only widget that must change is the `::tk::IconList` Canvas. **Recommended
replacement: `ttk.Treeview` in details view** (columns: Name / Size / Modified),
because:

- It is already fully themed in-repo (`style/builders/treeview.py`) — palette,
  hover, selection, row height all follow the active theme for free.
- Folder/file glyphs come from the existing icon engine (`Assets.icon` /
  `icon_element`), no new assets.
- Details view is *more* informative than tkfbox's icon grid, and matches what
  users expect from a modern chooser.
- Multi-select (for `get_open_filenames`) is native to Treeview
  (`selectmode="extended"`).

The alternative — reproducing the icon-grid look with a themed Canvas/flow of
labels — carries all the un-themed-Canvas risk we're trying to escape and buys
nothing. **§10 decision, but Treeview is the strong default.**

## 4. Widget mapping (tkfbox → themed)

| tkfbox piece | ttkbootstrap themed equivalent |
|---|---|
| `::tk::IconList` (Canvas) | `ttk.Treeview` details view (Name/Size/Modified) |
| path `ttk::menubutton` + `menu` | `ttk.Menubutton` + themed `ttk.Menu` (parent-path dropdown) |
| up-dir `ttk::button` | `ttk.Button` with an icon glyph |
| `File name:` `ttk::entry` | `ttk.Entry` |
| `Files of type:` menubutton + menu | `ttk.Menubutton` / `OptionMenu` + themed `Menu` |
| OK / Cancel `ttk::button` | `ttk.Button` (OK = default/accent) |
| `Show hidden` `ttk::checkbutton` | `ttk.Checkbutton` |
| toplevel `-class TkFDialog` | `ttk.Toplevel` (transient/modal to parent, `place_window_center`) |

Everything on the right is already themed — the dialog inherits the active theme
with no per-widget styling work.

## 5. Backend logic (Python, not ported Tcl)

Re-implement tkfbox's behaviors in Python (`os` / `pathlib`) rather than porting
the Tcl globbing — it's cleaner and testable:

- **Directory listing** — dirs first, then files; each row = glyph + name +
  formatted size + mtime.
- **Filetype filtering** — parse the standard `filetypes=[("Label", "*.ext"), …]`
  contract (must match `tkinter.filedialog` exactly so callers don't change);
  drive it from the type menubutton; support the `*`/`*.*` all-files entry.
- **Hidden-file toggle** — the `Show hidden` checkbutton filters dotfiles (and
  Windows hidden-attribute files) live.
- **Navigation** — double-click a dir to descend; up-dir button; the path
  menubutton lists ancestors for quick jumps; typing a path/name in the entry
  and pressing Return navigates or selects (tkfbox `ActivateEnt`/`CompleteEnt`).
- **Save mode** — `defaultextension`, `initialfile`, overwrite-confirm prompt
  (reuse `Messagebox`).
- **Directory mode** — no filetype row, listing shows dirs only, `Selection:`
  caption.

## 6. Public surface & routing

No new public API surface if we can avoid it — the four `Querybox.get_*`
wrappers stay the entry points and keep their `None`-on-cancel contract. What
changes is the dispatch inside them:

- **X11 → in-house dialog by default.** `tk.windowing_system() == "x11"` routes
  to `dialogs/filedialog.py`.
- **Windows / macOS → native OS dialog by default** (unchanged).
- **Opt-in override** so anyone can force the themed dialog anywhere (its whole
  point is theme consistency). Mechanism is a §10 decision — leading option: a
  `native: bool | None` kwarg on each `Querybox.get_*` wrapper (`None` = per-
  platform default, `False` = force in-house, `True` = force native), mirroring
  the snake_case + Tk-passthrough conventions. A module-level default flag
  (`set_native_filedialog(False)`) is the alternative / complement.

New code lives in **`dialogs/filedialog.py`**; the class is not re-exported as a
widget (it's reached through the facade), matching how `datepicker.py` sits
behind `Querybox.get_date`.

## 7. Return contracts (unchanged)

| Wrapper | Returns | Cancel |
|---|---|---|
| `get_open_filename` | `str` path | `None` |
| `get_open_filenames` | `tuple[str, …]` | `None` |
| `get_save_filename` | `str` path | `None` |
| `get_directory` | `str` path | `None` |

The in-house dialog must produce byte-identical return values to the stdlib
wrappers for the same selection, so callers are agnostic to which path drew the
dialog.

## 8. Risks & mitigations

- **Scope creep into a file *manager*.** tkfbox has no bookmarks, no places
  sidebar, no rename/delete. **Match that minimalism** for 2.1 (§10) — a places
  sidebar is a 2.2+ enhancement, not a blocker.
- **Filetype-contract drift.** The `filetypes` parsing must accept exactly what
  `tkinter.filedialog` accepts, or existing callers break. Pin with tests over
  the documented forms (extensions, `*`, macOS-style, multiple patterns).
- **Modality / focus.** The dialog must be transient + grab-set to its parent
  and return control cleanly (tkfbox uses a Tcl `vwait`; we use the same
  wait-window pattern our other dialogs use, e.g. `Querybox`/`DatePickerDialog`).
- **Headless testing.** The heavy lifting (listing, filtering, filetype parse,
  path nav) is pure-Python and unit-testable without a display; the GUI wiring
  gets the usual `root`-fixture smoke tests. Keep logic separable from widgets
  for exactly this reason.
- **Testability of the X11 route on this box.** Windows can't exercise the
  auto-route, only the forced (`native=False`) path — so the opt-in override is
  also our test seam. Worth an actual X11 eyeball before close.

## 9. Suggested PR shape

1. **PR 1 — backend + dialog, forced-only.** `dialogs/filedialog.py`: the
   Treeview-based dialog + Python listing/filter/nav logic, reachable **only**
   via a forced opt-in (`native=False`), all four modes. Headless tests for the
   pure logic + smoke tests for construction. Native default unchanged, so zero
   risk to existing callers.
2. **PR 2 — platform routing.** Wire the X11-default / native-elsewhere dispatch
   into the `Querybox.get_*` wrappers; document the `native=` override.
3. **PR 3 — docs.** Fold into the Dialogs feature guide + `Querybox` reference:
   the themed dialog, when it appears, and the override. Screenshots via the
   harness (X11 render is the point).

Splitting the forced dialog (PR 1) from the auto-route (PR 2) lets the build
land and get reviewed without changing any default behavior.

## 10. Open questions — SETTLED (design session, 2026-07-26)

1. **Center widget → `ttk.Treeview` details view** (Name / Size / Modified),
   per §3. The icon-grid reproduction is rejected — it re-imports the un-themed
   Canvas risk we're escaping.
2. **Chrome → match tkfbox's minimalism for 2.1** (path menu + up-dir only; no
   places/bookmarks sidebar). A sidebar is explicitly wanted as a **future
   update** (2.2+), not a 2.1 blocker.
3. **Routing → per-platform default with a `native: bool | None` kwarg override.**
   The in-house themed dialog is **NOT** the default everywhere. Matrix:

   | Platform | Default | `native=True` | `native=False` |
   |---|---|---|---|
   | X11 | **themed (in-house)** | stdlib tkfbox | themed |
   | Windows / macOS | **native OS** | native | themed (in-house) |

   `native=None` (the default) selects the per-platform default; `native=False`
   forces the themed dialog anywhere (for callers who want full theme
   consistency); `native=True` forces the OS/stdlib dialog. Rationale: native
   pickers on Win/macOS are the better citizen (OS recent-files, cloud, network
   places, muscle memory, accessibility) and replacing them by default would be
   a capability regression for a cosmetic gain — the same "good tkinter citizen /
   native parity" posture as native menus and window chrome. X11 is pure upside
   (no native chooser exists). A module-level global flag is **not** added now;
   the kwarg is the single seam (and doubles as the test seam on Windows).
4. **Save mode → reuse ttkbootstrap's `Messagebox`** for the overwrite-confirm;
   `filetypes` / `defaultextension` behavior must match `tkinter.filedialog`
   exactly (pinned by tests, §8).

## 11. Out of scope

- Replacing the native OS dialogs on Windows/macOS by default (native stays
  default there; the themed dialog is opt-in).
- A file *manager* feature set (rename/delete/new-folder, bookmarks sidebar,
  network places) — 2.2+ if ever.
- The color-dropper / other Canvas-based dialogs.
- Any change to the `Querybox.get_*` return contracts.