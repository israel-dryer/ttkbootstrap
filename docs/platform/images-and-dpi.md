# Images & DPI

Images in Tk are first-class objects with lifetimes independent of widgets.
Understanding how images behave — especially under high-DPI displays — is essential
for building correct and visually consistent ttkbootstrap applications.

This page explains how Tk handles images, common pitfalls, and how ttkbootstrap
provides structure around image usage.

---

## Images as objects

In Tk, images are not owned by widgets.

Instead:

- images are created as named objects in the Tk interpreter
- widgets reference images by name
- images persist until explicitly destroyed or garbage-collected

If an image object is garbage-collected in Python, widgets that reference it
may stop displaying it.

This behavior is a common source of bugs.

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

Modern systems often use high-DPI displays.

Tk handles DPI scaling by:

- scaling fonts automatically
- scaling images only if explicitly configured

This means images that look correct on standard displays may appear blurry or
incorrectly sized on high-DPI screens.

---

## ttkbootstrap’s approach to images

ttkbootstrap introduces conventions and helpers to manage images consistently:

- centralized image creation and caching
- explicit DPI-aware sizing
- reuse of images across widgets

This avoids duplicating image-loading logic and reduces memory usage.

---

## Image caching

Creating images repeatedly is expensive.

Caching images:

- improves performance
- ensures consistent appearance
- simplifies lifetime management

ttkbootstrap provides an `Image` abstraction to manage caching and reuse.
See [Guides → Icons](../guides/icons.md) for using framework-managed icons.

---

## Image formats

Tk natively supports a limited set of image formats.

ttkbootstrap encourages using Pillow-backed images when broader format
support is required, while still integrating with Tk’s image model.

This allows applications to use modern image assets without sacrificing
compatibility.

---

## Common pitfalls

- creating images inside widget constructors
- failing to keep a reference to an image
- ignoring DPI scaling
- loading the same image repeatedly

Understanding image behavior helps avoid these problems.

---

## Next steps

- See [Capabilities → Icons & Images](../capabilities/icons/index.md) for user-facing image behavior.
- See [Design System → Icons](../design-system/icons.md) for icon design principles.
- See [Widgets](../widgets/index.md) for examples of image-backed controls.
