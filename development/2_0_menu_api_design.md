# ttkbootstrap 2.0 — Menu API extension (design pass)

> Design pass for a small, additive extension of the re-exported `Menu` widget
> so the **macOS application-menu integration** is reachable through Python
> instead of raw Tcl. Follows the 2.0 hard rule (design pass before
> implementation). Pair with `2_0_plan.md`, `2_0_handoff.md`,
> `2_0_shipped_widget_api_design.md` (the window/mac-chrome precedent), and the
> docs design `2_0_docs_design.md`.
>
> **Status: CONFIRMED (author sign-off 2026-07-11) — IMPLEMENTED.** Fork A =
> **Design 1** (thin/honest, mac-native slots only); B/C/D/E = the recommended
> defaults (§9). Shipped on the menus docs branch: `src/ttkbootstrap/menu.py`
> (`Menu` moved out of `__init__.py`) + `tests/test_menu_api.py` + the guide's
> macOS-section rewrite.

## 1. Why this, why now

While authoring the **Menus** feature guide (docs Workstream H) the guide had to
teach three raw Tcl reach-ins to cover a normal cross-platform menu bar:

1. platform detection — `app.tk.call("tk", "windowingsystem")`
2. the macOS special menus — `Menu(..., name="apple" | "window" | "help")`
3. the macOS standard commands — `app.createcommand("tk::mac::ShowPreferences", …)`,
   `tk::mac::Quit`, `tk::mac::ShowHelp`

The author's call (2026-07-11): *docs teaching Tcl is a symptom of a missing API
footprint; we should not expect the user to reach into Tcl.*

Triage of the three:

- **(1) is not a gap** — the public helper already exists
  (`windowing_system(widget)`, exported as `ttk.windowing_system`; also the
  `App`/`Toplevel` `.winsys` attribute). The guide simply wasn't using it. **Fixed
  in the docs already** (uses `ttk.windowing_system(app)`); out of scope here.
- **(2) and (3) are a real gap** — nothing in `src/ttkbootstrap` wraps the macOS
  application menu or the `tk::mac::*` commands (confirmed by grep). bootstack
  doesn't wrap them either (it has its own `ContextMenu`/`MenuButton`/appshell
  abstractions — its framework API, which we don't copy). So there is no
  mechanism to port; the wrapper is net-new but tiny.

**Precedent for adding this in the cleanup release:** the shipped-widget API pass
already ported **native macOS window chrome** into 2.0 (`MacWindowStyle` #1125,
`internal/positioning.py`). A macOS **menu** footprint is the same category —
native-integration parity, not a speculative feature — and it is menu-scoped and
additive.

## 2. Scope & non-goals

**In scope:** extend the re-exported `Menu` (`src/ttkbootstrap/__init__.py`
`class Menu(AutoStyleMixin, _tkMenu)`) with:

- factory methods that create + attach + return the macOS **special menus**
  (application / window / help) without magic `name=` strings, and
- **standard-command hooks** (`on_preferences`, `on_quit`) on the application-menu
  object, wrapping `createcommand("tk::mac::…")`.

All new surface **no-ops gracefully off macOS** so user code needs no `is_mac`
branch for the wiring.

**Non-goals:**

- A full `MenuBar` / declarative menu-builder abstraction — bootstack territory.
- A `ContextMenu` class — the raw `Menu` + `tk_popup` idiom stays (it is already
  clean; the guide teaches it fine).
- Restyling `Menu` beyond the current automatic theming.
- Cross-platform **placement** of About/Preferences on Windows/Linux (see §4, the
  main fork). This design wires the *mac-native* slots; where those commands live
  on other platforms stays the app author's choice.
- Any change to `windowing_system` / `.winsys` (already sufficient).

## 3. The gap, concretely (today's user code)

```python
app = ttk.App()
is_mac = app.tk.call("tk", "windowingsystem") == "aqua"   # (1) fixed via ttk.windowing_system

menubar = ttk.Menu(app)
if is_mac:
    app_menu = ttk.Menu(menubar, name="apple")            # (2) magic Tk name
    menubar.add_cascade(menu=app_menu)
    app_menu.add_command(label="About Editor", command=show_about)
    menubar.add_cascade(menu=ttk.Menu(menubar, name="window"), label="Window")
    menubar.add_cascade(menu=ttk.Menu(menubar, name="help"), label="Help")
    app.createcommand("tk::mac::ShowPreferences", open_prefs)  # (3) raw tk::mac
    app.createcommand("tk::mac::Quit", on_quit)
```

## 4. Proposed API

Methods on `Menu`:

| Method | Does | Off macOS |
|---|---|---|
| `add_application_menu() -> Menu` | Creates the `name="apple"` submenu, `add_cascade`s it, returns it. | Returns `None` (no app menu exists). |
| `add_window_menu(label="Window") -> Menu` | Creates the `name="window"` submenu, attaches it, returns it. | Returns `None`. |
| `add_help_menu(label="Help", command=None) -> Menu` | Creates the `name="help"` submenu; if `command` given, wires `tk::mac::ShowHelp`. Returns it. | Returns a **normal** cascade labeled `label` (Help is a real menu everywhere), no `ShowHelp`. |

Methods on the **application-menu object** returned by `add_application_menu()`
(mac-only, so these only exist to be called when it is non-`None`):

| Method | Wraps |
|---|---|
| `on_preferences(callback)` | `createcommand("tk::mac::ShowPreferences", callback)` — enables the **Preferences…** (⌘,) item and calls back. |
| `on_quit(callback)` | `createcommand("tk::mac::Quit", callback)` — ⌘Q / Quit hook. |

Resulting user code (mac-native, zero Tcl, zero magic names):

```python
menubar = ttk.Menu(app)

app_menu = menubar.add_application_menu()      # None off macOS
if app_menu:
    app_menu.add_command(label="About Editor", command=show_about)
    app_menu.on_preferences(open_prefs)
    app_menu.on_quit(confirm_quit)
    menubar.add_window_menu()

file_menu = ttk.Menu(menubar, tearoff=False)
file_menu.add_command(label="New", command=new_file)
menubar.add_cascade(label="File", menu=file_menu)

menubar.add_help_menu(command=open_help)       # normal Help menu off mac; ShowHelp on mac
app.configure(menu=menubar)
```

The `if app_menu:` guard replaces the `is_mac` branch and reads as *"if this
platform has an application menu."* No `windowingsystem`, no `name="apple"`, no
`tk::mac`.

### About / Preferences on Windows & Linux — the main fork (§9-A)

`About` is a plain `add_command` (no `tk::mac` hook), so it is trivially portable
— the author places it wherever fits the platform. `Preferences`/`Quit` are the
tension: on macOS they live in the app menu via the hooks above; on Windows/Linux
the conventional homes are *File → Exit* and *Edit → Preferences* (or a settings
button). Two ways to handle it:

- **Design 1 (thin/honest — recommended).** The API wires only the mac-native
  slots (above). On other platforms the author adds their own Exit/Preferences
  items where convention dictates. Truthful, menu-scoped, minimal. User still
  writes the (small) non-mac placement themselves.
- **Design 2 (opinionated).** A higher-level `menubar.add_standard_commands(about=…,
  preferences=…, quit=…)` that *places them per platform* — app menu on mac,
  Help/Edit/File on win/linux. More convenient, more magic, drifts toward the
  MenuBar abstraction we called a non-goal.

Recommendation: **Design 1** for 2.0; note Design 2 as a possible bootstack-level
convenience. Fork is in §9.

## 5. Cross-platform behavior

| Feature | Windows / Linux | macOS |
|---|---|---|
| `add_application_menu()` | returns `None` | bold app menu (`name="apple"`) |
| `add_window_menu()` | returns `None` | standard Window menu |
| `add_help_menu(command=)` | normal Help cascade; `command` is the author's to wire | Help menu + `tk::mac::ShowHelp` |
| `app_menu.on_preferences/on_quit` | n/a (app_menu is `None`) | enables ⌘, / ⌘Q slots |

## 6. Where the code lives

`Menu` is currently a one-line subclass in `__init__.py`
(`class Menu(AutoStyleMixin, _tkMenu)`). Adding ~5 methods there bloats the
public-exports module. **Move `Menu` into a dedicated `src/ttkbootstrap/menu.py`**
(still `AutoStyleMixin, tk.Menu`), carrying the new methods, and re-export from
`__init__.py` (blessed-tk-widget convention — stays a top-level `ttk.Menu`, not a
`widgets/` custom widget). No public import-path change.

Implementation notes:
- The special submenu is `type(self)(self, name="apple")` so it is *our* `Menu`
  subclass (carrying `on_preferences`/`on_quit`), themed like the rest.
- `on_preferences`/`on_quit` call `self.tk.createcommand(...)`. `createcommand` is
  interpreter-global, which is *why* they are surfaced only on the single
  application-menu object — there is exactly one app menu, so no ambiguity.
- Platform test uses the existing `windowing_system(self)`.

## 7. Compat

Purely **additive** — no renames, no deprecations, no `_compat` entries. Existing
raw-Tcl user code keeps working unchanged.

## 8. Docs & tests

- **Docs:** rewrite the Menus guide's *"macOS: the application menu"* section
  against this API (delete the `tk::mac`/`name=` teaching; keep a one-line "under
  the hood this wires the standard `tk::mac` commands" aside at most). The
  Ctrl/Command accelerator section keeps `ttk.windowing_system` (already fixed).
- **Tests (headless, `tests/`):** methods exist on `ttk.Menu`; on the current
  platform `add_help_menu` returns a usable menu; the returned special menus have
  the expected Tk `name`; `on_preferences`/`on_quit` register a Tcl command
  (assert via `tk.call("info", "commands", "::tk::mac::Quit")` is a no-op-safe
  check) without error; off-target methods return `None`/no-op without raising.
  (macOS-native *behavior* — the item actually appearing — is a manual Track-B
  check, like the other aqua items.)

## 9. Open forks for author

- **A. About/Preferences placement (the big one).** Design 1 (thin, mac-native
  only — recommended) vs Design 2 (opinionated per-platform placement). §4.
- **B. Naming.** `add_application_menu()` / `add_window_menu()` / `add_help_menu()`
  (verb, mirrors `add_cascade`) vs `application_menu` / `window_menu` (lazy
  properties). Recommend the `add_*` verbs — they *create and attach*, matching
  the existing `add_cascade`/`add_command` mental model.
- **C. Hook names.** `on_preferences` / `on_quit` (recommended, reads as
  "attach a handler") vs `set_preferences_command` / `preferences_command=`.
- **D. `App` mirror?** Also expose `App.on_quit(...)` for a truly app-global feel,
  or keep everything on the app-menu object (recommended — one home, no
  duplication)?
- **E. Module move.** Confirm moving `Menu` to `src/ttkbootstrap/menu.py` (vs
  keeping it in `__init__.py` and accepting the bloat).

## 10. PR plan

A single small PR once the forks are settled: the `menu.py` move + methods, the
guide's macOS-section rewrite, and the headless tests. Additive, no compat, low
risk.
