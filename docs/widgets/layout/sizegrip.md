---
title: SizeGrip
---

# SizeGrip

`SizeGrip` is a thin themed wrapper over `ttk.Sizegrip`. It draws a
small dotted triangle (the platform's window-resize affordance) that
the user drags with the mouse to resize the toplevel window. It's the
classic desktop "tug the corner" cue, surfaced as a widget so you can
pin it to a status bar, footer, or any region inside a layout.

`SizeGrip` is non-focusable and non-keyboard — the only interaction is
mouse drag. It's a structural primitive in the same family as
[Separator](separator.md): no `signal`, no `on_*` helpers, no virtual
events. The drag itself is wired by ttk at the class level, and it
only does anything useful when the parent toplevel is resizable.

<figure markdown>
![sizegrip](../../assets/dark/widgets-sizegrip.png#only-dark)
![sizegrip](../../assets/light/widgets-sizegrip.png#only-light)
</figure>

---

## Basic usage

```python
import ttkbootstrap as ttk

app = ttk.App()
app.resizable(True, True)  # required for the grip to do anything

content = ttk.Frame(app, padding=20)
content.pack(fill="both", expand=True)

status = ttk.Frame(app, padding=(8, 4))
status.pack(side="bottom", fill="x")

ttk.Label(status, text="Ready").pack(side="left")
ttk.SizeGrip(status).pack(side="right")

app.mainloop()
```

The grip appears as a small dotted triangle pinned to the right edge of
the status bar. Dragging it resizes the app window from the bottom-right
corner, exactly as if the user grabbed the toplevel's corner directly.

---

## Common options

`SizeGrip`'s configuration surface is intentionally thin — it's a
platform-drawn affordance, not a styled glyph. The only knob that
visibly changes its appearance is `surface` (the fill behind the dots).

| Option       | Type | Default     | Notes                                                        |
| ------------ | ---- | ----------- | ------------------------------------------------------------ |
| `surface`    | str  | inherited   | Background fill behind the dot pattern; inherits parent surface, otherwise `"content"` |
| `accent`     | str  | `None`      | Accepted but **silently ignored** by the style builder — the dot color is platform-drawn |
| `variant`    | str  | `"default"` | Only `"default"` is registered; other values raise `BootstyleBuilderError` |
| `cursor`     | str  | `""`        | Standard Tk cursor option; usually left as the platform default |
| `style`      | str  | derived     | Explicit ttk style name; overrides `surface`                 |
| `bootstyle`  | str  | —           | **Deprecated.** Has no useful effect on SizeGrip — the builder ignores accent |

### `surface` — background fill

```python
status_bar = ttk.Frame(app, surface="card", padding=(8, 4))
status_bar.pack(side="bottom", fill="x")
ttk.SizeGrip(status_bar).pack(side="right")
```

The grip's background fill follows the parent surface so it sits flush
on whatever container hosts it. To break the inheritance and force a
specific fill, pass `surface=` explicitly. The dot glyph itself is
drawn by Tk's native `Sizegrip.sizegrip` element and isn't tinted by
the builder, so changing `surface` only changes the rectangle behind
the dots — the dot color stays platform-determined.

### `accent` is a no-op

```python
ttk.SizeGrip(app, accent="primary")  # accepted, but renders identically
```

The SizeGrip style builder reads `surface` and writes `background`; it
does not consume `accent`. Passing one resolves a unique style name
(`bs[…].primary.TSizegrip`) but the configured tokens are the same as
the default — the rendered grip is unchanged. Treat `accent` as a
silent no-op until the builder is extended to recolor the dot pattern.

### `style_options.show_arrows` and similar

`SizeGrip` exposes none of the per-element style hooks that
`Scrollbar` does. The dot pattern is opaque to the framework — there's
no built-in way to swap it for a different glyph or tint it
independently of the platform theme.

---

## Behavior

**Mouse drag is the only interaction.** Tk binds `<Button-1>`,
`<B1-Motion>`, and `<ButtonRelease-1>` on the `TSizegrip` bind class.
Pressing on the grip and dragging walks the toplevel's geometry
(`wm geometry`) to match the cursor offset. There are no
ttkbootstrap-level virtual events; the drag is a side-effect of the
class-level Tk handlers.

**Non-focusable.** `takefocus` defaults to auto, which ttk.Sizegrip
evaluates as non-focusable — the grip never enters Tab order and
ignores keyboard input. There's no Enter/Space affordance to "trigger"
it.

**Requires a resizable toplevel.** If the parent toplevel has
`resizable(False, False)` (or `(True, False)` / `(False, True)` along
the wrong axis), the drag has no effect — the grip still tracks the
mouse but the toplevel ignores the geometry write. Set
`resizable(True, True)` on the toplevel before relying on the grip.

**Platform parity.** On most platforms (macOS, modern Windows, modern
Linux WMs) users can already resize a window by dragging its border or
corner without a sizegrip. The widget is primarily a visible *cue*
that resizing is permitted, not the only path to do it. On
window-manager themes that hide window borders or use thin chrome, the
grip becomes more functional.

**Reconfiguring `surface` after construction is broken.**
`sizegrip.configure(surface=...)` raises `TclError: unknown option
"-surface"` because `SizeGrip` doesn't lift `surface` into a configure
delegator (unlike Frame, which routes the option through
`configure_style_options` for the container-cascade path). Calling
`sizegrip.configure_style_options(surface=...)` directly does not
raise but produces an unstyled `Default.TSizegrip` style without the
hash prefix, effectively reverting to the platform default. Treat
`surface` as construction-time only.

---

## Events

`SizeGrip` has no `on_*` event helpers and emits no virtual events.
The class-level mouse bindings (`<Button-1>`, `<B1-Motion>`,
`<ButtonRelease-1>`) are reserved for Tk's internal resize logic — do
not override them or you'll break the drag. If you need to react to
resize, bind `<Configure>` on the toplevel itself:

```python
def on_resize(event):
    print(event.widget.winfo_geometry())

app.bind("<Configure>", on_resize)
```

`<Configure>` fires for *every* size change of `app`, including ones
not driven by the grip — wrap the handler in a debounce or compare
against the prior geometry if you only care about user-driven
resizes.

---

## When should I use SizeGrip?

Use `SizeGrip` when:

- you're building a desktop-style app with a status bar or footer
  and want an explicit visual cue that the window is resizable
- the active window-manager theme hides window borders or uses thin
  chrome where the corner-drag affordance isn't obvious
- you're matching the look of legacy desktop applications where the
  dotted triangle is part of the expected chrome

Skip `SizeGrip` when:

- the app is fixed-size or modal (`resizable(False, False)`) — the
  grip would render but do nothing
- the platform's native window-resize affordance is already prominent
  enough (most modern macOS / Windows themes)
- you need a *draggable splitter* between two regions inside the
  window — that's [PanedWindow](panedwindow.md), not SizeGrip

---

## Related widgets

- **Separator** — the other purely structural primitive in the layout
  family; non-interactive, themeable, used for in-window dividers
- **Frame** — common host for a status bar / footer where SizeGrip
  lives
- **PanedWindow** — draggable sash between two resizable panes inside
  a window; SizeGrip resizes the toplevel itself, not in-window splits

---

## Reference

- **API reference:** [`ttkbootstrap.SizeGrip`](../../reference/widgets/SizeGrip.md)
- **Related guides:** [Layout](../../platform/geometry-and-layout.md),
  [Layout Properties](../../capabilities/layout-props.md),
  [Design System](../../design-system/index.md)
