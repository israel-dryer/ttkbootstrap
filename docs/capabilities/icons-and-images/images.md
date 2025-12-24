# Images

Images represent visual content and decorative assets used throughout
ttkbootstrap applications.

Because Tk treats images as global interpreter objects with independent
lifetimes, image usage requires careful management. ttkbootstrap formalizes
image usage as a capability to ensure correctness, performance, and consistency.

---

## Images as shared resources

In Tk, images are not owned by widgets.

Instead:
- images are created as named objects
- widgets reference images by name
- images persist independently of widgets

If an image object is garbage-collected, widgets referencing it may stop
displaying it.

Treat images as shared, application-level resources.

---

## Image lifetime management

Correct image usage requires:
- keeping a Python reference to the image
- controlling when images are created
- avoiding premature destruction

ttkbootstrap encourages centralized image creation and reuse to make lifetime
explicit and predictable.

---

## Image caching

Creating images repeatedly is expensive.

Caching:
- improves performance
- reduces memory usage
- avoids subtle rendering bugs

ttkbootstrap provides an `Image` abstraction to manage caching and reuse of
images across widgets.

---

## DPI awareness

High-DPI displays introduce additional complexity.

Images may:
- appear blurry if not scaled correctly
- render at incorrect sizes
- require different assets for different scales

ttkbootstrap integrates image usage with DPI awareness to provide consistent
visual results across platforms.

---

## Image formats

Tk natively supports a limited set of image formats.

For broader format support:
- Pillow-backed images may be used
- images are still exposed to Tk as PhotoImage objects

This allows modern asset pipelines while preserving Tk compatibility.

---

## Images and styling

Images often interact with styling:

- icons may be recolored to match theme state
- images may change based on widget state
- visual assets must align with design tokens

Treating images as a capability ensures consistent behavior.

---

## Performance considerations

Image performance depends on:
- size and resolution
- recoloring frequency
- caching strategy

Avoid:
- loading images in tight loops
- scaling images repeatedly
- creating per-widget image instances

Centralized management improves responsiveness.

---

## ttkbootstrap guidance

ttkbootstrap promotes:

- centralized image creation
- explicit caching
- DPI-aware scaling
- reuse over recreation

These practices reduce bugs and improve visual quality.

---

## Common pitfalls

- losing references to images
- recreating images unnecessarily
- ignoring DPI scaling
- mixing raw PhotoImage usage with cached images

Understanding image behavior avoids these issues.

---

## Next steps

- See **Icons** for symbolic assets
- See **Platform → Images & DPI** for low-level behavior
- See **Widgets** for image usage in components
