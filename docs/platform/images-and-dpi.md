---
title: Images & DPI
---

# Images & DPI

Tk images are first-class objects in the Tcl interpreter, with
lifetimes independent of the widgets that display them. They also
interact with platform DPI in surprising ways: macOS does the work
for you, Windows needs an awareness manifest before any window
opens, and Linux varies by desktop environment. This page covers
both halves — image lifetime and reference handling, plus per-OS
DPI behavior.

The framework provides two image abstractions that absorb most of
the boilerplate: the `Image` utility (file/bytes/PIL → cached
PhotoImage) and `BootstrapIcon` (theme-aware vector glyphs from
Bootstrap Icons). Use those rather than constructing `PhotoImage`
directly when you can.

---

## Images as Tcl objects

Tk images live in the Tcl interpreter, not the Python widget tree:

- An image is created as a named object inside Tcl
  (`tkinter.PhotoImage` is a thin wrapper around the Tcl handle).
- Widgets reference an image by passing the Python `PhotoImage`
  instance — Tk records the underlying Tcl name.
- The image persists in Tcl until explicitly destroyed, *but* if the
  Python wrapper is garbage-collected, Tcl's reference count drops
  and Tk frees the image even though widgets still point at it.

The result: a label that previously showed an icon goes blank, with
no exception, no log message, and no clue in the widget's
configuration. The fix is the **pinning idiom** — keep a Python
reference somewhere that outlives the widget:

```python
# Wrong — img is GC'd at end of build_ui; the label renders blank
def build_ui():
    img = ttk.PhotoImage(file="logo.png")
    ttk.Label(app, image=img).pack()

# Right — pin on the widget itself
img = ttk.PhotoImage(file="logo.png")
label = ttk.Label(app, image=img)
label.image_ref = img       # framework idiom: pin reference on widget
```

The `Image` utility (next section) handles this for you by keeping
its own cache.

See [Widget Lifecycle → Image and font references](widget-lifecycle.md#image-and-font-references)
for the same gotcha framed in terms of construction and destruction.

---

## DPI and scaling

Modern systems often use high-DPI displays. How Tk handles this differs significantly
per platform.

---

## macOS — Retina

On macOS with Retina displays, the OS handles pixel-doubling transparently via the
Aqua windowing system. Tk's coordinate system uses logical points, and the OS
renders at 2× (or higher) physical pixels automatically.

**You do not need to do anything special for Retina.** ttkbootstrap's `hdpi=True`
default has no effect on macOS because the OS already handles scaling.

Practical implications:

- Load images at **@1x (logical pixel) size** — the Aqua backend doubles them for
  Retina automatically.
- Do not load @2x assets and pass them at half their pixel dimensions — Tk will
  display them at the wrong size.
- Fonts scale correctly on Retina without any configuration.

---

## Windows — DPI manifest

On Windows, the application must declare DPI awareness before the first window is
created, or Windows will render it in a blurry compatibility mode.

ttkbootstrap handles this automatically. With `hdpi=True` (the default),
`App.__init__` calls `SetProcessDpiAwareness` via `ctypes` before creating the
Tk window:

```python
# hdpi=True is the default — no extra setup needed
app = ttk.App(title="My App")

# Opt out only if you have a specific reason
app = ttk.App(title="My App", hdpi=False)
```

After the window is created, ttkbootstrap detects the screen DPI and sets the Tk
scaling factor to match. The resulting scaling factor drives font and widget sizing.

**Providing scaled images on Windows:**

Tk does not scale `PhotoImage` objects automatically on Windows. On a 150% display
(144 DPI), a 32×32 image will appear as 21×21 logical pixels — noticeably small.
Supply a pre-scaled asset (e.g., a 64×64 version of a 32-point icon for 2× displays)
and load it with `Image.open`:

```python
import ttkbootstrap as ttk
from ttkbootstrap.api.utils import Image

app = ttk.App()

# Load image from disk; result is cached by path
icon = Image.open("icon@2x.png")
```

Scale factor can be read at runtime via `app.tk.call("tk", "scaling")` — multiply
your design-time pixel dimensions by that value to choose the right asset.

---

## Linux — X11 and fractional scaling

Linux DPI handling is the most variable. X11 reports a screen DPI, but fractional
scaling (e.g., 125%, 150%) is handled differently by different desktop environments
and compositors. Tk reads the X11 DPI at startup; it does not track runtime changes.

ttkbootstrap's `hdpi=True` default detects the X11 DPI at startup and applies a
scaling factor. For fractional scaling, pass `scaling` explicitly:

```python
# Let ttkbootstrap detect (works for most setups)
app = ttk.App(hdpi=True)

# Override with a specific factor (useful for HiDPI that isn't detected)
app = ttk.App(scaling=2.0)

# Common values: 1.0 (96 DPI), 1.5 (144 DPI), 2.0 (192 DPI / 4K)
```

A value between 1.6 and 2.0 is typical for HiDPI screens on Linux.

**Wayland:** Tk currently runs on Wayland via XWayland, which means DPI behavior
follows the X11 path above. Native Wayland support is a work-in-progress in the
upstream Tk project; behavior may improve in future Tk releases.

---

## Scaling factor summary

| Platform | Default behavior | When to override |
|---|---|---|
| macOS | OS handles Retina automatically | Never — leave `hdpi=True`, don't set `scaling` |
| Windows | DPI awareness set automatically; scaling detected | Rarely — only for multi-monitor edge cases |
| Linux (X11) | DPI detected from Xft.dpi / screen DPI | Often — set `scaling` for fractional DPI setups |

---

## Image formats

Tk natively supports a limited set of image formats (GIF, PNG, PPM).

For broader format support (JPEG, WebP, TIFF, SVG), install Pillow:

```
pip install Pillow
```

ttkbootstrap's `Image` utility uses Pillow when available. Without Pillow,
only Tk-native formats work.

---

## The `Image` utility

Constructing `PhotoImage` repeatedly is expensive (disk read +
decode) and creates the GC trap for free. The `Image` utility loads
once, caches by source, and keeps a strong reference so widgets
can't lose theirs:

```python
import ttkbootstrap as ttk
from ttkbootstrap.api.utils import Image

app = ttk.App()

logo = Image.open("logo.png")              # decode + cache
same_logo = Image.open("logo.png")         # cache hit — same object
label = ttk.Label(app, image=logo)
label.pack()
```

Constructors:

| Method | Source | Notes |
|---|---|---|
| `Image.open(path, *, key=None)` | File path (str / Path) | `~` expansion + path resolution; cache key is the absolute path |
| `Image.from_bytes(data, *, key=None)` | Raw bytes | Cache key is a content hash (so duplicate bytes deduplicate) |
| `Image.from_pil(pil_image, *, key=None)` | A PIL `Image` instance | Cache key is `id(pil_image)` — pass `key=` if you want stable identity |
| `Image.transparent(width, height)` | n/a | A blank transparent placeholder, useful for layout spacers |

Cache management:

| Method | Use |
|---|---|
| `Image.get_cached(key)` | Look up a cached image; returns `None` if missing |
| `Image.set_cached(key, img)` | Manually insert a key→image entry |
| `Image.clear_cache()` | Drop every cached image (existing widgets keep working until they're recreated) |
| `Image.cache_info()` | `ImageCacheInfo` with `items` count for diagnostics |

Pillow is required for everything except `Image.transparent`. Without
Pillow installed, `Image.open` and friends raise an `ImportError`
on first use.

---

## `BootstrapIcon`

For *icons* (as opposed to bitmap images), reach for `BootstrapIcon`
instead. It produces a themed glyph from the Bootstrap Icons font
that scales cleanly with DPI and re-renders on `<<ThemeChanged>>`:

```python
import ttkbootstrap as ttk

icon = ttk.BootstrapIcon("save", size=20, color="primary")
ttk.Button(app, text=" Save", image=icon, compound="left").pack()
```

The framework's widgets accept `BootstrapIcon` anywhere they accept
a `PhotoImage`. Most composites also accept an **icon spec dict**
(`{"name": "save", "size": 20, "color": "primary"}`) and construct
the icon for you — see Toolbar's `add_button(icon=...)` for example
usage. Color values must be PIL color names or hex strings; theme
tokens like `"success"` are *not* valid here. Pass the resolved color
via `get_theme_color("success")` if you need theme-driven coloring.

Cross-references:
[Capabilities → Icons](../capabilities/icons/icons.md) for the icon
mechanics. [Design System → Icons](../design-system/icons.md) for
icon design principles.

---

## Common pitfalls

**Image reference lost:**
```python
# Wrong — image is garbage collected before it's displayed
def build_ui():
    img = ttk.PhotoImage(file="logo.png")  # local variable, not kept
    ttk.Label(app, image=img).pack()
```

```python
# Correct — keep the reference on a persistent object
self.logo = ttk.PhotoImage(file="logo.png")
ttk.Label(app, image=self.logo).pack()
```

**Image created inside a constructor repeatedly:**
```python
# Wrong — creates a new image object on every call
def refresh_row(data):
    icon = ttk.PhotoImage(file="row-icon.png")  # N copies in memory
    ...
```

Use the `Image` utility with caching, or create the image once and reuse.

**Ignoring DPI on Windows:** loading a fixed-pixel image without accounting for
the scaling factor produces icons that look too small on HiDPI displays. Use
DPI-aware asset variants (e.g., `icon.png` at 1× and `icon@2x.png` at 2×)
and select the right one based on `app.tk.call("tk", "scaling")`.

---

## Next steps

- [Platform Differences](platform-differences.md) — per-OS DPI summary alongside other differences
- [Capabilities → Icons & Images](../capabilities/icons/index.md) — user-facing image behavior
- [Design System → Icons](../design-system/icons.md) — icon design principles
- [API Reference → Image](../reference/utils/Image.md) — `Image` utility API
