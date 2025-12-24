# API Reference

This section documents the **public API surface** of ttkbootstrap v2.

Use these pages when you need exact signatures, supported options, and return values.
For conceptual explanations and patterns, see **Platform** and **Capabilities**.

## How this reference is organized

- **App**: application runtime, windows, menus, and app-scoped settings
- **Style**: themes, bootstyle tokens, builders, and theme utilities
- **Capabilities (Widget Interface)**: capability slices that describe **facets of widget behavior**
  (implemented via internal capability modules / mixins, exposed through widgets)
- **Widgets**: widget classes and composites
- **Dialogs**: dialog windows and message/query helpers
- **Data**: data source abstractions and implementations
- **i18n**: localization, translation, and formatting helpers
- **Utils**: small reusable primitives (signals, validation, variables, images)

## Sections

- [App](app/index.md)
- [Style](style/index.md)
- [Capabilities (Widget Interface)](capabilities/index.md)
- [Widgets](widgets/index.md)
- [Dialogs](dialogs/index.md)
- [Data](data/index.md)
- [i18n](i18n/index.md)
- [Utils](utils/index.md)

## Notes

- Reference pages target the **public import path** (for example `ttkbootstrap.Button`) even when
  the implementation lives in internal modules.
- Capability pages document behavior built into widgets; you typically won’t import capability mixins directly.
