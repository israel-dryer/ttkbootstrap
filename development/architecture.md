# ttkbootstrap architecture and import layering

This library is growing toward a framework-style surface. To keep imports sane, prevent circulars, and preserve a stable public API, we group modules into layers and keep dependencies flowing in one direction.

## Layer model
- Core: small, dependency-light helpers (`exceptions`, `logging`, `signals`, `types`). No imports from higher layers.
- Runtime: backend and integration (`style/theme_provider`, `style/utility`, `style/tk_patch`, image/asset loaders). Depends on Core only.
- Style: theming and bootstyle plumbing (`style/bootstyle`, `style/style`, `style/builders/*`). Depends on Runtime/Core, never on widgets.
- Widgets – primitives: thin wrappers over ttk (`widgets/frame`, `widgets/button`, `widgets/entry`, etc.). Depend on Style/Runtime/Core.
- Widgets – composites: higher-level widgets (`widgets/datepicker`, `widgets/tableview`, dialogs) that build on primitives and mixins.
- API: facades and re-exports for public consumption. Imports from lower layers only.

Import direction: Core → Runtime → Style → Widgets (primitives) → Widgets (composites) → API.

## Current modules mapped to layers
- Core: `ttkbootstrap.core.appconfig`, `ttkbootstrap.core.exceptions`, `ttkbootstrap.core.localization`, `ttkbootstrap.core.colorutils`, `ttkbootstrap.core.validation`, `ttkbootstrap.core.signals`, `ttkbootstrap.core.publisher`.
- Runtime: `ttkbootstrap.runtime.utility`, `ttkbootstrap.style.tk_patch`, (shims point to these layers).
- Runtime: `ttkbootstrap.style.theme_provider`, `ttkbootstrap.style.utility`, `ttkbootstrap.style.tk_patch`, `ttkbootstrap.style.element`, `ttkbootstrap.style.bootstyle_builder_base`.
- Style: `ttkbootstrap.style.bootstyle`, `ttkbootstrap.style.style`, `ttkbootstrap.style.builders.*`, `ttkbootstrap.style.bootstyle_builder_ttk`, `ttkbootstrap.style.token_maps`.
- Widgets – primitives: `ttkbootstrap.widgets.*` wrappers that subclass ttk directly (button, label, frame, entry, combobox, etc.).
- Widgets – composites: `ttkbootstrap.widgets` that compose primitives (datepicker, dateentry, tableview, toast, dialogs, form helpers).
- API: `ttkbootstrap.__init__` re-exports and any future `ttkbootstrap.api` facades.

## Rules to avoid circular imports
- Do not import widgets from Style or Runtime layers. Builders work only with style primitives and images, not widget classes.
- Primitives must not import composites. If you need shared behavior, extract a mixin into `widgets/mixins/`.
- Composites that need other composites should keep imports local inside functions/methods rather than at module top.
- Keep top-level imports light; prefer lazy loading or `TYPE_CHECKING` guards when a module only needs types.
- Cross-layer helpers should live in Core; if two modules start importing each other, extract the shared interface into Core and refactor both to depend on it.

## Public API guidance
- `ttkbootstrap.__init__` should import from API/lower layers only and remain free of implementation logic.
- Maintain an explicit `__all__` for the public surface. Anything not exported there is considered private.
- Examples and docs should import from `ttkbootstrap` (public API), not from deep modules, to keep the surface honest.

## Migration checkpoints
- When adding a new module, pick its layer and verify its imports point only to allowed lower layers.
- If a module needs something from a higher layer, pass it in (dependency injection) or move the shared code downward.
- Add local (function-level) imports only as a last resort; prefer restructuring to keep arrows flowing one way.
- Consider adding an import-linter configuration later to enforce the arrows above once the modules settle into these buckets.
