---
icon: fontawesome/solid/grip
---

# Layout System

This section explains how ttkbootstrap embraces Tkinter's native layout model so you deliver responsive, structured interfaces without reinventing the geometry managers.

We rely on **pack**, **grid**, and (when required) **place** to organize content inside frames while keeping hierarchies shallow (three levels max) so layouts stay predictable. Think about the intent of each section - how the UI should flow and expand - rather than locking widgets to fixed coordinates.

## Layout foundations

- **Containers control layout**: Every widget's geometry is dictated by its parent frame. Compose complex interfaces by nesting simple frames, each owning its own geometry manager, spacing rules, and children.
- **Intent over pixels**: Define how widgets relate, how space should flex, and how sections should respond to resizing instead of hardcoding coordinates or absolute placements.
- **Pack vs grid**: Use `pack` for linear flows (toolbars, stacked controls) and `grid` for structured content (forms, dashboards). Mixing both is fine so long as one geometry manager controls each individual container. When you need absolute positioning, `place` is available but should only be used for tightly controlled overlays or pixel-specific details that cannot stretch or reflow.

## Building responsive sections

- **Frames + padding**: Wrap related widgets in `ttk.Frame` or `ttk.Labelframe`, apply theme-aware padding (`padding=16`), and control spacing through `grid(padx, pady)` or `pack(padx, pady)` instead of scattering placeholder widgets.
- **Grid weights**: Pair `grid` with `columnconfigure`/`rowconfigure` so fields stretch evenly. Use `sticky="ew"` for horizontal growth and `sticky="nsew"` for full coverage, and only assign weights to rows/columns that should expand.
- **Scroll containers**: Wrap long tables or forms in `ScrollView`/`ScrolledText` with autohide scrollbars so overflow stays usable without dominating the layout. Combine with `sticky="nsew"` so the scrollable area flexes with the window.
- **Panedwindow**: Use `ttk.Panedwindow` when you want resizable panes; give each pane a `stretch="always"` weight so dividers move smoothly.

## Navigation & overlays

- **PageStack & Notebook**: Present alternate screens via `PageStack` (stack-based flows) or `Notebook` (tabs). Reuse shared frames between pages instead of recreating widgets to keep state and performance steady.
- **Overlays**: `ContextMenu` and `MenuButton` deliver contextual actions without shifting the grid. Pair them with matching `bootstyle` tokens so they share the same visual weight as neighboring controls.
- **Dialogs & forms**: Use `Dialog`, `Form`, or `FormDialog` for focused workflows; each inherits the same layout behaviors so modals feel like natural extensions of inline forms.

## Layout habits

- **Avoid deep trees**: Keep layout depth to three levels so documentation navigation and maintenance stay manageable.
- **Favor tokens**: Apply shared `bootstyle` colors, typography, and spacing tokens rather than pixel nudges for dividers, backgrounds, or grouping surfaces.
- **Stay adaptive**: Declare expansion rules, avoid fixed dimensions unless essential, and test with longer text or different DPI so localization and resizing behave well.

These conventions keep ttkbootstrap layouts predictable, responsive, and aligned with the shared design system tokens.
