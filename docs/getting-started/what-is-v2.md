---
icon: fontawesome/solid/circle-info
---

# What is ttkbootstrap 2?

ttkbootstrap 2 is the next-generation documentation and component framework for building modern Tkinter apps. It preserves the stability of `ttk` while layering on refined theming, responsive layout helpers, and opinionated defaults inspired by modern UI systems.

![ttkbootstrap concept](https://placehold.co/800x800/FFFFFF/333333.webp?text=Concept%20Vision&font=lato)

### Design pillars
- **Tk-native:** Still uses `ttk` widgets and the Tk event loop, so the learning curve stays gentle.
- **Theming-first:** Built-in light/dark palettes plus runtime theme switching, accent customization, and token-aware styles.
- **Pattern-rich:** Structured guidance for inputs, feedback, dialogs, layouts, and navigation controls.
- **Documentation-first:** Story-driven docs with catalog-style navigation so each widget and dialog is directly reachable.

### Architecture at a glance

1. **Application shell** — `ttkbootstrap.App` boots a themed window, handles DPI, and provides a safe entry point for your Tk logic.
2. **Widget catalog** — Grouped components (inputs, data display, feedback, layout, navigation, dialogs) share consistent naming and helper APIs.
3. **Utilities & dialogs** — Shared helpers for tray-style notifications, dialog scaffolding, theme utilities, and CLI utilities that automate scaffolding tasks.

Read the rest of the Getting Started section for hands-on commands, preview apps, and templates that leverage this structure.
