---
title: Images & DPI
---

# Images & DPI

Images in Tk are first-class objects with lifetimes independent of widgets.
Understanding how images behave — especially under high-DPI displays — is essential
for building correct and visually consistent ttkbootstrap applications.

This page explains how Tk handles images, how DPI scaling works per platform, and
how ttkbootstrap provides structure around image usage.

---

## Images as objects

In Tk, images are not owned by widgets.

Instead:

- images are created as named objects in the Tk interpreter
- widgets reference images by name
- images persist until explicitly destroyed or garbage-collected

If an image object is garbage-collected in Python, widgets that reference it
may stop displaying it.

This behavior is a common source of bugs. Keep a reference to every image your
application uses — typically as an attribute on a long-lived object such as the
`App` or a view class.

---

## Image lifetime

Because images outlive widgets:

- the image must be kept alive for as long as it is displayed
- destroying a widget does not destroy its image
- losing the last Python reference can invalidate the image

ttkbootstrap encourages treating images as **application-level resources**
rather than widget-local objects.

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
Load a larger image and let the scaling factor inform the size:

```python
import ttkbootstrap as ttk
from ttkbootstrap.api.utils import Image

app = ttk.App()

# Image loads at the right size for the current DPI automatically
icon = Image.open("icon.png", size=(32, 32))
```

The `Image` utility accounts for the current scaling factor when interpreting
the `size` argument.

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

## Image caching

Creating images repeatedly is expensive and wastes memory.

ttkbootstrap provides an `Image` abstraction to manage caching and reuse.
Use it rather than creating `PhotoImage` objects directly:

```python
import ttkbootstrap as ttk
from ttkbootstrap.api.utils import Image

app = ttk.App()

# Cached — second call returns the same object
logo = Image.open("logo.png", size=(64, 64))
same_logo = Image.open("logo.png", size=(64, 64))

label = ttk.Label(app, image=logo)
label.pack()
```

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
`Image.open(..., size=(w, h))` and let the utility scale to the display.

---

## Next steps

- [Platform Differences](platform-differences.md) — per-OS DPI summary alongside other differences
- [Capabilities → Icons & Images](../capabilities/icons/index.md) — user-facing image behavior
- [Design System → Icons](../design-system/icons.md) — icon design principles
- [API Reference → Image](../reference/utils/Image.md) — `Image` utility API
