---
icon: fontawesome/solid/icons
---

# Iconography

ttkbootstrap 2 uses the `ttkbootstrap-icons` provider, which exposes the Bootstrap Icons library as the built-in source for every internal widget icon and the default provider when you pass the `icon` parameter to buttons, labels, toolbuttons, menus, SelectBox dropdowns, and other controls. Look up names on the Bootstrap Icons site (`https://icons.getbootstrap.com`) or run the built-in browser (`ttkbootstrap-icons`) to explore every glyph, then plug the names directly into widgets such as `ttk.Button(..., icon='arrow-right-square')`. Treat icons as supporting elements (affordances, status indicators, navigation cues) so keep them aligned with the current color tokens and typography sizes (icons should match the surrounding `body` or `label` text).

### Guidelines
- Reserve icons for meaning (actions, states, callouts) and avoid crowding text blocks.
- Combine icons with `bootstyle` tokens so their fills follow theme colors like `success`, `info`, or `danger`.
- Prefer semantic icon names (`rocket`, `palette`, `table`) that reinforce the copy and are easy to search.

If you need custom glyphs, render them as `ttk.Label` children and pair them with the typography tokens for consistent sizing.

## Icon specs and state helpers

The `icon` option accepts either a string (the name of the glyph) or a dictionary that describes `name`, `size`, and `color`. For example:

```python
ttk.Button(..., icon={"name": "arrow-up-square", "size": 25, "color": "red"})
```

The dictionary form plugs directly into the icon mixin and builder helpers, which normalize sizes, keep Bootstyle tokens intact, and rebuild the style when the icon changes.

You can also configure per-state overrides inside the spec using the `state` key (a list of `(state, override)` tuples). Each override can supply a new `name` or `color` (or both) for the requested state, so you can animate hover, pressed, or selected icons without writing extra bindings:

```python
ttk.Button(
    ...,
    icon={
        "name": "play-fill",
        "state": [
            ("hover", {"name": "play-circle"}),
            ("pressed", {"color": "#f0ad4e"}),
        ],
    },
)
```

The builders translate these overrides into image state maps so the icon updates automatically when Tk reports the selected, pressed, or hovered states.  
Use this surface to keep Bootstyle colors, typography, and iconography harmonized across every widget.

## Browsing icons

`ttkbootstrap-icons` ships with a built-in browser that lists every glyph, previews colors, and shows the exact name you pass to the `icon` parameter. Run the `ttkbootstrap-icons` CLI command to open the browser locally and copy names into widget constructors, or use the screenshot below for a quick reference when you cannot run the CLI.

![Icon browser](https://github.com/israel-dryer/ttkbootstrap-icons/raw/main/packages/ttkbootstrap-icons/browser.png)
