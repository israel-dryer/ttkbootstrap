# Icons & Images

Icons and images are core visual resources in ttkbootstrap applications.
They require careful handling to ensure consistent appearance, good performance,
and correct behavior across platforms and DPI settings.

This section documents icons and images as **capabilities**, describing how
widgets consume visual assets rather than how those assets are implemented
internally.

---

## Icons vs images

Icons and images serve different roles:

- **Icons** represent symbolic actions or states
- **Images** represent content or decoration

Both are managed as shared resources rather than widget-owned objects.

---

## Icons as a capability

Icons are used across many widgets:
- buttons
- menus
- toggles
- indicators

Rather than embedding icon logic into each widget, ttkbootstrap treats icon usage
as a shared capability with consistent behavior.

---

## Images as a capability

Images require careful lifecycle management.

As a capability, image usage defines:
- how images are loaded
- how they are cached
- how they scale
- how they are reused

Widgets consume images without owning their lifetime.

---

## Relationship to styling

Icons and images interact closely with styling:

- icons may change color based on state
- images may be recolored or scaled
- assets must align with theme tokens

Treating them as capabilities ensures consistent behavior across widgets.

---

## Performance considerations

Visual assets are expensive to recreate.

Centralized management:
- reduces memory usage
- improves rendering performance
- avoids subtle bugs

ttkbootstrap’s abstractions exist to address these concerns.

---

## ttkbootstrap guidance

ttkbootstrap encourages:

- centralized asset management
- reuse over recreation
- explicit ownership and lifetime
- DPI-aware scaling

These practices improve correctness and visual quality.

---

## Common pitfalls

- creating images inside widget constructors
- losing references to image objects
- inconsistent icon usage
- ignoring DPI scaling

Understanding icons and images as capabilities helps avoid these issues.

---

## Next steps

- See **Icons** for symbolic asset usage
- See **Images** for image lifecycle and caching
- See **Platform → Images & DPI** for underlying behavior
