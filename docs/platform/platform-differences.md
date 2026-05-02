---
title: Platform Differences
---

# Platform Differences

ttkbootstrap runs on macOS, Windows, and Linux. Most behavior is identical across platforms, but several areas behave differently by design. This page collects those differences in one place.

---

## Quick reference

| Feature | macOS | Windows | Linux (X11) |
|---|---|---|---|
| `Mod` key | ⌘ Command | Ctrl | Ctrl |
| Right-click gesture | Button-3 **and** Ctrl+click | Button-3 | Button-3 |
| ContextMenu backend | Native NSMenu | Themed Toplevel | Themed Toplevel |
| Toast default position | Bottom-right | Bottom-right | Top-right |
| Window close button | Hides app (dock stays) | Destroys window | Destroys window |
| Quit shortcut | Cmd+Q (destroys) | Alt+F4 (destroys) | (varies by WM) |
| `window_style` effects | Ignored | `mica`, `acrylic`, etc. | Ignored |
| System appearance sync | Supported | Not supported (silent no-op) | Not supported (silent no-op) |
| Config/state directory | `~/Library/Application Support/<app>` | `%APPDATA%\<app>` | `$XDG_CONFIG_HOME/<app>` |
| ttkbootstrap dialog style | Themed Tk window | Themed Tk window | Themed Tk window |
| Native file picker | `tkinter.filedialog` | `tkinter.filedialog` | `tkinter.filedialog` |

---

## Keyboard shortcuts

### The `Mod` key

The `Shortcuts` service uses `Mod` as a portable modifier that resolves to the platform-conventional primary modifier:

- **macOS** — `Mod` → Command (⌘)
- **Windows / Linux** — `Mod` → Control (Ctrl)

```python
import ttkbootstrap as ttk

app = ttk.App()
shortcuts = ttk.get_shortcuts()

def save_file():
    print("Save triggered")

# Registers as Cmd+S on macOS, Ctrl+S on Windows/Linux
shortcuts.register("save", "Mod+S", save_file)
shortcuts.bind_to(app)
```

When displaying shortcut text in menus or labels, the `Shortcuts` service renders the platform symbol automatically — `⌘S` on macOS, `Ctrl+S` elsewhere.

Tk binding strings for the same shortcut differ per platform:

| Platform | Binding string |
|---|---|
| macOS | `<Command-s>` |
| Windows / Linux | `<Control-s>` |

Use the `Shortcuts` service rather than hardcoding binding strings to keep your code portable. See [Events & Bindings → Modifier keys](events-and-bindings.md#modifier-keys) for the broader bindings model.

!!! link "API Reference"
    See [`ttkbootstrap.Shortcuts`](../reference/app/Shortcuts.md) and [`ttkbootstrap.Shortcut`](../reference/app/Shortcut.md).

---

## Context menus

### Trigger gesture

`ContextMenu` with `trigger='right-click'` (the default) binds the portable right-click gesture automatically:

- **Windows / Linux** — `<Button-3>`
- **macOS** — `<Button-2>` and `<Control-Button-1>` (macOS uses Ctrl+click as the context-menu gesture in addition to a two-finger or right click)

No code change is needed — the `trigger='right-click'` default handles both.

### Backend

The visual implementation differs by windowing system:

- **macOS (Aqua)** — uses a native `tk.Menu` (NSMenu). This avoids the key-window and activation issues that affect a reused `overrideredirect` Toplevel on Aqua. The popup looks and behaves like a standard macOS context menu. Some options (`minwidth`, `width`) are ignored on this backend.
- **Windows / Linux** — uses the themed Toplevel-backed implementation. All `ContextMenu` options apply, including density and accent.

The public API is identical on both backends. Do not rely on `item()` returning a Tk widget on macOS — the native backend returns the original spec dict.

!!! link "Widget docs"
    See [Widgets → ContextMenu](../widgets/actions/contextmenu.md).

---

## Toast notifications

When `position` is not set, `Toast` chooses a default anchor based on the windowing system:

- **macOS (Aqua) / Windows** — bottom-right corner, inset 25 px from the right edge and 75 px from the bottom
- **Linux (X11)** — top-right corner, inset 25 px from the right edge and 25 px from the top

This matches the notification conventions of each platform. Pass `position` explicitly to override:

```python
# Force a specific position on any platform
ttk.Toast(message="Done", position="-25-75").show()
```

!!! link "Widget docs"
    See [Widgets → Toast](../widgets/overlays/toast.md).

---

## Application quit behavior

### macOS

On macOS, `App` installs native quit behavior by default (`AppSettings.macos_quit_behavior = 'native'`):

- Clicking the window **close button** hides the app (withdraws). The app stays in the Dock and Cmd+Tab list.
- **Cmd+Q** (or Dock → Quit) actually destroys the app and exits.
- **Cmd+H** hides the app.
- **Cmd+W** fires the standard window-close action.

This matches macOS application conventions. To restore cross-platform destroy-on-close behavior:

```python
import ttkbootstrap as ttk

app = ttk.App(settings={"macos_quit_behavior": "classic"})
```

### Windows / Linux

The window close button destroys the application. No special handling is installed.

---

## Window style effects (Windows only)

The `window_style` parameter on `App` and `Toplevel` enables visual effects via `pywinstyles`:

```python
# Windows only — ignored silently on macOS and Linux
app = ttk.App(window_style="mica")
app = ttk.App(window_style="acrylic")
app = ttk.App(window_style="aero")
```

Available values: `mica`, `acrylic`, `aero`, `transparent`, `win7`.

This parameter is silently ignored on macOS and Linux.

---

## System appearance (macOS only)

`AppSettings.follow_system_appearance = True` makes the app track the OS light/dark mode and switch themes automatically. This is currently only effective on macOS, where Tk exposes a light/dark signal at the windowing-system level.

On Windows and Linux, the setting has no effect — theme switching must be done manually via `ttk.toggle_theme()` or `ttk.set_theme()`.

---

## Application state directory

`App.state_path` returns the platform-appropriate directory for persisting application state:

| Platform | Path |
|---|---|
| macOS | `~/Library/Application Support/<app_name>` |
| Windows | `%APPDATA%\<app_name>` |
| Linux | `$XDG_CONFIG_HOME/<app_name>` (falls back to `~/.config/<app_name>`) |

The directory is not created automatically — create it on first use if needed.

---

## Dialogs: themed vs native

All `ttkbootstrap` dialogs (`MessageDialog`, `QueryDialog`, `FormDialog`, etc.) are **themed Tk windows**, not OS-native dialogs. They look consistent across platforms but do not inherit the native system chrome.

For file and directory pickers, use `tkinter.filedialog` — those are genuinely native on all platforms:

```python
import tkinter.filedialog as fd

path = fd.askopenfilename(title="Open file")
path = fd.askdirectory(title="Choose folder")
```

`PathEntry` uses `tkinter.filedialog` internally, so its picker button is always native.

For color picking, `tkinter.colorchooser` provides a native picker:

```python
import tkinter.colorchooser as cc

color = cc.askcolor(title="Choose color")
```

!!! link "Widget docs"
    See [Widgets → Dialogs](../widgets/dialogs/index.md) for a full overview of ttkbootstrap's dialog classes.

---

## Next steps

- [Images & DPI](images-and-dpi.md) — per-OS scaling and high-DPI asset handling
- [Build & Distribute](build-and-ship.md) — packaging for macOS, Windows, and Linux
- [App](../reference/app/App.md) — `App` API reference including `window_style`, `macos_quit_behavior`, and `state_path`
- [Shortcuts](../reference/app/Shortcuts.md) — portable keyboard shortcut API
