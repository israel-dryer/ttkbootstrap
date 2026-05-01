---
title: Tabs
---

# Tabs

`Tabs` is a themed **tab bar** — a horizontal or vertical strip of
clickable items that drives selection state. It is pure navigation
chrome: it does not own a page-stack and does not switch content
panes. Its only output is the **selected value**, exposed as a
`Signal` / `tk.Variable` and emitted as a `<<TabSelect>>` event on
the active tab. Pair it with a `PageStack`, a `Notebook`, or any
content widget you observe via the same signal.

If you want tabs that automatically swap content panes, use
[`TabView`](../views/tabview.md) — it composes `Tabs` with a
`PageStack`. Reach for `Tabs` directly when the content lives in a
custom layout, when you want to drive a non-page concern (tool mode,
filter set, view preset), or when you need fine-grained control over
each tab's lifecycle.

<figure markdown>
![tabs](../../assets/dark/widgets-tabs.png#only-dark)
![tabs](../../assets/light/widgets-tabs.png#only-light)
</figure>

---

## Basic usage

Create a tab bar, add tabs by key, and observe the selection.

```python
import ttkbootstrap as ttk

app = ttk.App()

tabs = ttk.Tabs(app)
tabs.pack(fill="x", padx=10, pady=10)

tabs.add(text="Home", icon="house", key="home")
tabs.add(text="Files", icon="folder2", key="files")
tabs.add(text="Settings", icon="gear", key="settings")

tabs.on_tab_changed(lambda value: print(f"Selected: {value}"))

app.mainloop()
```

The first tab added is selected automatically (the underlying
variable is set to that tab's value on the first `add()` call).

---

## Navigation model

`Tabs` is a **random-access selection surface**. Every tab carries a
`key` (the unique identifier within the bar) and a `value` (what gets
written to the variable / signal when the tab is clicked). When
`value` is omitted, it defaults to `key`, so the simplest setup
treats keys as the public selection identifier:

```python
tabs.add(text="Home", key="home")
tabs.add(text="Files", key="files")

tabs.set("files")          # programmatic selection
print(tabs.get())          # "files"
```

The selection writes flow through one channel:

| Channel | Read | Write | Reactivity |
|---|---|---|---|
| `Signal` (preferred) | `tabs.signal.get()` | `tabs.signal.set(v)` | `tabs.signal.subscribe(cb)` → `cb(value)` |
| `tk.Variable` | `tabs.variable.get()` | `tabs.variable.set(v)` | `tabs.variable.trace_add("write", cb)` |
| Convenience | `tabs.get()` / `tabs.value` | `tabs.set(v)` / `tabs.value = v` / `tabs.configure(value=v)` | `tabs.on_tab_changed(cb)` → `cb(value)` |

Pass an existing `signal=` (or `variable=`) at construction to share
state with another widget. If neither is provided, `Tabs` creates an
internal `StringVar` + `Signal` pair.

!!! warning "Auto-select clobbers external state"
    The first call to `add()` writes that tab's value to the
    variable unconditionally — even if the variable already held a
    meaningful value. If you pass `signal=external_signal` with a
    pre-set value, that value is replaced when the first tab is
    added. Add tabs first, then write the desired initial value, or
    call `tabs.set(...)` after `add()`.

`Tabs` does not own pages. Tab keys are scoped to the bar; if you
want to drive a content pane, observe `tabs.signal` and switch the
pane yourself (or use [`TabView`](../views/tabview.md), which does
this for you).

---

## Common options

| Option | Default | Effect |
|---|---|---|
| `orient` | `"horizontal"` | Tab strip axis. **Construction-only** — `configure(orient=…)` raises `ValueError`. |
| `variant` | `"bar"` | Visual style. Only `"bar"` is registered (the underline-and-divider look); see the warning below. **Construction-only**. |
| `show_divider` | depends on `variant` | Thin separator below (or beside) the bar. Defaults to `True` for `"bar"`, `False` otherwise. Reconfigurable live. |
| `compound` | `"left"` | Icon position relative to text in every tab (forwarded to each `TabItem`). |
| `tab_width` | `None` | `None` auto-sizes; an `int` gives a fixed character width; `"stretch"` expands tabs to fill the bar. **`"stretch"` is honored only for horizontal orientation** — vertical packs have `expand=False` regardless. |
| `tab_padding` | `(12, 8)` | `(horizontal, vertical)` padding inside each tab. |
| `tab_anchor` | orient-dependent | Default text/icon alignment per tab. `None` resolves to `"w"` for vertical, `"center"` for horizontal. |
| `enable_closing` | `False` | Close-button affordance for newly added tabs: `True` (always visible), `False` (no button), `"hover"` (visible on hover only — space is reserved either way). Per-tab `closable=` on `add()` overrides. |
| `enable_adding` | `False` | Show a `+` button at the trailing edge that fires `<<TabAdd>>`. |
| `signal` | internal | Shared `Signal` for selection state. Mutually substitutes for `variable=`. |
| `variable` | internal | Shared `tk.Variable` for selection state. Wrapped into a `Signal` internally. |
| `accent` | `None` | Theme token for the active-tab indicator (the underline in the `bar` variant). Defaults to `primary` when omitted. |

!!! warning "`variant='pill'` is not implemented"
    The constructor accepts `"pill"` and the docstring lists it, but
    no `pill` builder is registered for `TabItem.TFrame`. Passing
    `variant="pill"` raises
    `BootstyleBuilderError: Builder 'pill' not found for widget
    class 'TabItem.TFrame'. Available variants: default, bar`. Use
    `"bar"` (or omit `variant`) until the builder ships.

The bar inherits standard `Frame` chrome (`surface`, `padding`,
`show_border`, `density`); the active-tab underline color is driven
by `accent`. To restyle individual tabs after construction, use
`tabs.configure_item(key, …)` or `tabs.item(key).configure(…)` and
target the same options that `TabItem` accepts (`text`, `icon`,
`compound`, `value`, `closable`, `command`, `close_command`).

---

## Behavior

**Selection.** Clicking a tab writes its `value` to the bound
variable, fires that tab's `command` callback, and emits
`<<TabSelect>>` on the tab. The bar itself observes the variable and
re-paints whichever tab matches the current value as `selected`. The
pattern means programmatic writes (`tabs.set(value)`,
`tabs.signal.set(value)`, or even `tabs.variable.set(value)` from a
peer widget) all round-trip through the same code path and re-paint
the active tab.

**Adding and removing.** `tabs.add(...)` appends a tab; `key` is
auto-generated as `tab_<n>` if omitted. `tabs.remove(key)` destroys
the tab; you can also iterate via `tabs.keys()` or `tabs.items()`.
`tabs.add(key=...)` raises `ValueError` on duplicate keys.

!!! warning "`remove()` does not reset selection"
    Removing the currently-selected tab leaves the variable holding
    an orphan value that no longer matches any tab. The bar paints
    nothing as selected, but `tabs.get()` still returns the stale
    key. Call `tabs.set(...)` (or read `tabs.keys()` and pick a
    fallback) after removing the active tab.

**Per-tab control.** `tabs.item(key)` returns the underlying
`TabItem` (which is not a publicly-constructable type — you only ever
get one back from `add()`). It exposes its own properties
(`is_selected`, `value`) and `configure` keys for `text`, `icon`,
`compound`, `closable`, `command`, `close_command`. `tabs.item(key)
.select()` is equivalent to `tabs.set(value)`.

**Closing.** When `closable` is set on a tab, clicking the close
button emits `<<TabClose>>` on the tab and invokes its
`close_command` callback (if any). The widget does **not**
auto-`remove()` — your handler decides whether to remove, hide, or
reuse.

**Adding (the +-button).** With `enable_adding=True`, the bar shows
a `+` button (horizontal) or a `New` button (vertical) at the
trailing edge. Clicking it fires `<<TabAdd>>` on the bar. Your
handler typically calls `tabs.add(...)` to insert a new tab.

**Hover-only close.** With `closable="hover"`, the close button is
laid out (so spacing is stable) but its glyph foreground matches the
tab background; on hover, the glyph fades in via the ttk state map.

**Construction-only options.** `orient` and `variant` cannot be
changed after construction — both raise `ValueError`. `tab_width`,
`tab_padding`, and `tab_anchor` are baked into newly-added tabs;
existing tabs keep their original layout.

---

## Events

The event surface splits across two widgets — `Tabs` and the
individual `TabItem` returned by `add()`.

| Event | Fired on | When | `event.data` |
|---|---|---|---|
| `<<TabSelect>>` | the **TabItem** clicked | tab is clicked or `tab.select()` is called | `{"value": <tab.value>}` |
| `<<TabClose>>` | the **TabItem** | close button is clicked | `{"value": <tab.value>}` |
| `<<TabAdd>>` | the **Tabs** widget | the `+` / `New` button is clicked (with `enable_adding=True`) | *none* |

!!! warning "`<<TabSelect>>` does not bubble to `Tabs`"
    Tk virtual events do not propagate through the parent chain, and
    `Tabs` does not forward them. `tabs.bind("<<TabSelect>>", ...)`
    silently registers a callback that never fires. To observe
    selection at the bar level, use `tabs.on_tab_changed(...)` or
    `tabs.signal.subscribe(...)`. To observe a single tab, bind on
    that `TabItem`:

    ```python
    home = tabs.add(text="Home", key="home")
    home.bind("<<TabSelect>>", lambda e: print("home clicked", e.data))
    ```

`Tabs` exposes two `on_*` helpers, each with a different callback
shape — choose by what you want delivered:

| Helper | Backed by | Callback receives | Unbind |
|---|---|---|---|
| `tabs.on_tab_changed(cb)` | `signal.subscribe` | `cb(value)` — the new selected value | `tabs.off_tab_changed(sub_id)` |
| `tabs.on_tab_added(cb)` | `bind("<<TabAdd>>")` | `cb(event)` — a Tk event | `tabs.off_tab_added(bind_id)` |

`on_tab_changed` is the right hook for "do something with the new
selection" — it fires for both user clicks and programmatic writes.
`on_tab_added` is a thin alias for the underlying virtual event;
prefer it when you also need the event object (e.g. to read
`event.widget`).

```python
def handle_change(value):
    print(f"Now showing: {value}")

sub_id = tabs.on_tab_changed(handle_change)
# tabs.off_tab_changed(sub_id)  # later
```

---

## When should I use Tabs?

Use `Tabs` when:

- you want a tab strip that drives **external** state — a content
  pane in a custom layout, a tool-mode switch, a filter preset
- you need fine-grained control over each tab (per-tab `command`,
  `close_command`, `closable`, custom keys)
- you want closable tabs or an add affordance and you'll handle the
  side effects yourself

Prefer [`TabView`](../views/tabview.md) when:

- you want tabs that automatically swap a content pane — `TabView`
  composes `Tabs` with a `PageStack` and wires the selection through
  for you

Prefer [`SideNav`](sidenav.md) when:

- the navigation is the primary structural element of an app shell
  (a vertical destination list with sections / icons), not a
  contextual tab strip

Prefer [`Notebook`](../views/notebook.md) when:

- you specifically need the platform's native ttk `Notebook` widget
  (e.g. tab-drag-rearrange that the OS provides for free)

---

## Related widgets

- [`TabView`](../views/tabview.md) — `Tabs` plus a `PageStack` with
  the selection wired through; reach for this when each tab maps
  one-to-one to a content pane.
- [`PageStack`](../views/pagestack.md) — the content half of
  `TabView`; pair with `Tabs` directly if you want bespoke chrome.
- [`SideNav`](sidenav.md) — vertical destination list for top-level
  navigation in an app shell.
- [`Notebook`](../views/notebook.md) — thin themed wrapper over
  `ttk.Notebook` if you need the platform-native tab control.

---

## Reference

- **API reference:** `ttkbootstrap.Tabs`
- **Related guides:** Navigation, Signals & Events, Design System
