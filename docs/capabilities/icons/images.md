# Images

`Image` is the framework's class-method utility for loading and caching
arbitrary raster images — anything that isn't a Bootstrap icon. It wraps
Pillow as the decoder, returns `PIL.ImageTk.PhotoImage` objects (the same
type Tk widgets accept on `image=`), and keeps every loaded image in a
process-wide cache to solve Tk's reference-keeping problem.

The constructor surface and a basic example live on the
[Icons & Images overview](index.md#image-general-image-utility). This page
goes deeper on the parts users hit when caching becomes load-bearing:
cache identity, cache lifetime, the GC contract, and when `Image` is the
wrong tool.

---

## At a glance

| Method | Cache key | Returns |
|---|---|---|
| `Image.open(path)` | `('file', resolved_absolute_path)` | `PhotoImage` decoded from a file |
| `Image.from_pil(pil_image)` | `('pil', id(pil_image))` | `PhotoImage` wrapping an in-memory PIL image |
| `Image.from_bytes(data)` | `('bytes', md5(data))` | `PhotoImage` decoded from raw bytes |
| `Image.transparent(w, h)` | `('transparent', w, h)` | Fully-transparent RGBA spacer |
| `Image.cache_info()` | — | `ImageCacheInfo(items=N)` snapshot |
| `Image.clear_cache()` | — | Empties the cache (see warning below) |
| `Image.get_cached(key)` | — | Cached image or `None` |
| `Image.set_cached(key, img)` | — | Stores `img` under `key`; returns `img` |

Every constructor accepts an optional `key=` argument that overrides the
default cache key — useful for versioning, sharing identity across
otherwise-distinct sources, or pinning a single image under a stable
name.

---

## Constructing images

Call any of the four constructors with the source you have on hand:

```python
import ttkbootstrap as ttk
from ttkbootstrap import Image

app = ttk.App()

# From a file path on disk
logo = Image.open('logo.png')

# From raw bytes (embedded resources, downloads)
icon = Image.from_bytes(b'<png-bytes>')

# From an existing PIL image (after manipulation)
from PIL import Image as PILImage
pil = PILImage.open('photo.jpg').resize((100, 100))
photo = Image.from_pil(pil)

# Transparent spacer (compound padding, layout placeholder)
spacer = Image.transparent(16, 16)

ttk.Label(app, image=logo).pack(padx=20, pady=20)
app.mainloop()
```

Pillow handles the decoding, so every format Pillow reads (PNG, JPEG,
GIF, BMP, TIFF, WebP, ICO, …) works through `Image.open` and
`Image.from_bytes`. Tk's stock `PhotoImage` only handles GIF and PNG
natively, so routing through `Image` is also how you get JPEG / WebP /
TIFF support without writing the Pillow conversion yourself.

Each constructor returns a `PIL.ImageTk.PhotoImage`, which is the same
type Tk widgets accept on the `image=` kwarg. There's no separate
ttkbootstrap-specific image class — `Image` is purely a loader and cache,
not a widget-side wrapper.

---

## Cache identity

Each constructor uses a different default key shape, chosen to match how
identity actually works for that source:

- **`Image.open(path)`** keys by the resolved absolute path. Repeated
  calls with `'logo.png'`, `'./logo.png'`, and `'~/proj/logo.png'` all
  collapse to the same cache slot when they resolve to the same file.
  The file is decoded once, no matter how many widgets reference it.
- **`Image.from_pil(pil_image)`** keys by `id(pil_image)`. The cache
  hits only when the *same* PIL object is passed back in. Two PIL
  images with identical pixel content but different object identities
  (e.g., one is `pil_a.copy()`) get separate cache slots. This is
  intentional — content-hashing every PIL image on every call would be
  expensive.
- **`Image.from_bytes(data)`** keys by `md5(data)` hex digest. Identical
  byte sequences hit the same slot regardless of where they came from
  (file read, network download, embedded resource).
- **`Image.transparent(w, h)`** keys by the `(w, h)` pair. One spacer
  per unique size, shared across all callers.

When the default key isn't right, pass an explicit `key=`:

```python
import ttkbootstrap as ttk
from ttkbootstrap import Image

app = ttk.App()

# Version a file across releases
v1 = Image.open('icons/save.png', key=('save', 'v1'))
v2 = Image.open('icons/save.png', key=('save', 'v2'))  # forced reload

# Force two PIL objects to share identity
from PIL import Image as PILImage
pil_a = PILImage.new('RGBA', (10, 10), (255, 0, 0, 255))
pil_b = pil_a.copy()
img_a = Image.from_pil(pil_a, key='red-square')
img_b = Image.from_pil(pil_b, key='red-square')
print(img_a is img_b)  # → True (same cache slot)

# Stash a manually-constructed PhotoImage
custom = ttk.PhotoImage(width=32, height=32)
Image.set_cached('logo:32', custom)
later = Image.get_cached('logo:32')
print(later is custom)  # → True
```

The cache key is any `Hashable`. Tuples, strings, integers, frozensets
all work; dicts and lists do not.

---

## Cache lifetime

The cache lives on the `Image` class itself (`Image._cache`) and persists
for the lifetime of the Python process. Inspect, populate, or empty it
with the four management methods:

```python
import ttkbootstrap as ttk
from ttkbootstrap import Image

app = ttk.App()
Image.transparent(16, 16)
Image.transparent(32, 32)

print(Image.cache_info())          # ImageCacheInfo(items=2)
print(Image.cache_info().items)    # 2

Image.clear_cache()
print(Image.cache_info().items)    # 0
```

`ImageCacheInfo` is a frozen dataclass — its `items` field is read-only.
Future versions may add hit/miss counters; rely on the field name, not
the order or count.

`get_cached(key)` returns the cached image or `None` if missing.
`set_cached(key, img)` writes any `PhotoImage` under any hashable key
and returns the image (handy for chaining). Use these to share images
loaded outside the constructors — for example, when an existing helper
already gave you a `PhotoImage` and you want it findable by name.

!!! danger "`clear_cache()` breaks widgets currently displaying cached images"

    The cache is the *strong* Python reference that keeps the underlying
    Tcl image alive. Tk widgets only retain the Tcl image *name* on
    `image=`, not a Python reference to the `PhotoImage` object. Once
    nothing holds a Python ref, garbage collection drops the
    `PhotoImage`, which in turn destroys the Tcl image — and any widget
    still pointing at that Tcl image goes blank, with no exception.

    Verified at runtime (Python 3.13, Tk 8.6):

    ```python
    img = Image.transparent(20, 20)
    label = ttk.Label(app, image=img)   # Tcl image name pinned on widget
    label.pack()
    Image.clear_cache()                  # drops the only strong ref
    import gc; gc.collect()              # PhotoImage finalized; Tcl image freed
    label.update_idletasks()             # widget now references a dead Tcl name
    ```

    Don't call `clear_cache()` while widgets are alive and using cached
    images. If you need to free memory, scope the cache to a window's
    lifetime: clear after the window is destroyed, never while it's
    open.

---

## The pinning idiom

Tk's reference-keeping issue affects every `PhotoImage`, not just ones
loaded through `Image`. The minimal idiom for raw `tkinter.PhotoImage` is
to attach the image to a long-lived object — typically the widget itself
or a module-level container:

```python
import ttkbootstrap as ttk
import tkinter as tk

app = ttk.App()
label = ttk.Label(app)
label.image = tk.PhotoImage(width=20, height=20)   # pin via attribute
label.configure(image=label.image)                  # then wire it
label.pack()
```

`Image.*` does the equivalent automatically by stashing every loaded
image in `Image._cache`. As long as the cache outlives the widgets —
the default behavior — you can drop the local Python variable freely:

```python
import ttkbootstrap as ttk
from ttkbootstrap import Image

app = ttk.App()
ttk.Label(app, image=Image.open('logo.png')).pack()
# No local variable; the cache keeps the PhotoImage alive.
app.mainloop()
```

The only failure modes are explicit ones: `clear_cache()`, replacing the
cached image at the same key (the previous one becomes unreachable), or
overwriting `Image._cache` directly. None of these can be triggered by
ordinary code paths, so most apps treat `Image.*` as zero-effort
pinning. See [Platform → Images & DPI](../../platform/images-and-dpi.md)
for the wider explanation of Tk image lifetime.

---

## When `Image` is the wrong tool

`Image` is a general-purpose loader; it doesn't integrate with the
framework's styling pipeline. Specifically:

- **For Bootstrap icons** (the framework's bundled glyph set), use
  `BootstrapIcon` directly or pass a string / `IconSpec` dict to a
  widget's `icon=` kwarg. That path lets the style engine swap the
  glyph and color per widget state and re-render after `<<ThemeChanged>>`
  — none of which `Image.*` does. See [Icons](icons.md) for the full
  pipeline.
- **For state-aware imagery** (an image that should change between
  default / hover / disabled), build the per-state map yourself and
  call `Style.element_create(...)` with a list of `(state, image)`
  tuples. There's no first-class mechanism for swapping `Image.*`
  results based on widget state.
- **For one-shot raw `PhotoImage`** that doesn't need caching at all
  (e.g., a generated image you're about to throw away), use
  `tkinter.PhotoImage` or `PIL.ImageTk.PhotoImage` directly and pin it
  yourself. `Image.*` adds a cache slot you don't need.

Use `Image.*` when you have arbitrary raster content (logos,
photographs, custom illustrations, raster icons that aren't Bootstrap
glyphs) and want a single line that loads, decodes, caches, and pins
the result.

---

## Where to read next

| Question | Page |
|---|---|
| What's the constructor surface of `BootstrapIcon` and the `IconSpec` shape? | [Icons & Images overview](index.md) |
| How does the icon pipeline resolve a widget's `icon=` kwarg, and what changes on theme switch? | [Icons](icons.md) |
| Why does my image disappear after the function that loaded it returns? | [Platform → Images & DPI](../../platform/images-and-dpi.md) |
| How does ttkbootstrap handle DPI scaling, and why does the same image render at different physical sizes per OS? | [Platform → Images & DPI](../../platform/images-and-dpi.md) |
| How do I use icons day-to-day (string form, dict form, common patterns)? | [Guides → Icons](../../guides/icons.md) |
