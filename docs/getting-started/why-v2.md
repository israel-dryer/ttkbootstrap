---
icon: fontawesome/solid/star
---

# Why v2? (What's New)

ttkbootstrap 2 is the library overhaul you asked for: redesigned theming plus richer widget and interaction APIs, dialog/navigation/form upgrades, and stronger runtime/tooling support while keeping the underlying Tk/Ttk stability intact.

### Theming & typography
- **Library theming:** Tokens, accent palettes, and helpers such as `ttk.set_theme("...")` and `ttk.toggle_theme()` keep widgets, dialogs, and layouts aligned with light or dark palettes.
- **Typography system:** Font modifiers like `heading-md` and compound selectors such as `body[bold][underline]` simplify consistent, expressive typography across the UI.

### Widgets & interactions
- **New widget catalog:** Introduced TextEntry, PasswordEntry, PathEntry, TimeEntry, SelectBox, DropDownButton, SpinnerEntry, ScrollView, ContextMenu, a revamped TableView, Popup/Tooltip helpers, and more primitives that leverage the shared API surface.
- **Reactive signals:** Widgets that expose `textvariable`/`variable` hooks now emit subscribable/mappable signals so updates, validation, and computed state flow through the UI without imperative plumbing—just attach listeners or map to new values and let the framework handle propagation.
- **Virtual event upgrades:** The virtual event system can now carry payloads via `widget.event_generate("<<VirtualEvent>>", data={...})`, letting subscribers react with context-rich data instead of empty notifications.
- **Convenient event helpers:** Many widgets now expose `on_*`/`off_*` binding helpers (e.g., `Notebook.on_tab_changed(...)`) so wiring callbacks stays expressive.

### Navigation, dialogs & forms
- **Dialog system refresh:** `Dialog`, `MessageDialog`, and `QueryDialog` share a common base and ship with helpers such as MessageBox, QueryBox, and pickers so you can compose flows without rebuilding scaffolding.
- **Navigation & forms:** `ttk.PageStack` delivers stack-based navigation and the new `Form` widget simplifies complex data entry while staying compatible with the reactive signal surface.

### Runtime & tooling
- **Runtime helpers:** `ttk.App`, DPI-aware utilities, and updated localization modules simplify bootstrapping windows, theming, and localized text/formatting.
- **Packaging & tooling:** Updated CLI scaffolding, templates, learning materials, and docs guidance keep the community in sync for faster prototyping and deployment.
