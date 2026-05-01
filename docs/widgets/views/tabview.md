---
title: TabView
---

# TabView

`TabView` is the canonical tabbed surface — a `Frame` that owns a
[`Tabs`](../navigation/tabs.md) bar wired to a
[`PageStack`](pagestack.md) so a click on a tab mounts the
corresponding page. Use it when navigation is **random-access** through
a visible tab strip (the user picks any tab at any time) and exactly
one page should be visible at a time.

TabView is a thin coordinator. The tab strip is a real `Tabs` widget
(orientation, variant, density, close / add affordances all inherited
from there); the content stack is a real `PageStack` (key-addressed
pages, history with back/forward). The only logic TabView adds is a
shared selection variable plumbed through both halves. For tab-driven
flows that's exactly what you want; for sequential / wizard navigation
without a tab strip, reach for [`PageStack`](pagestack.md) directly.

<figure markdown>
![tabview](../../assets/dark/widgets-tabview.png#only-dark)
![tabview](../../assets/light/widgets-tabview.png#only-light)
</figure>

---

## Basic usage

`add(key, text=...)` registers both a tab and a page in one call and
returns the page widget — populate it like any `Frame`. The first tab
added is auto-selected.

```python
import ttkbootstrap as ttk

app = ttk.App()

tabview = ttk.TabView(app, height=200)
tabview.pack(fill="both", expand=True, padx=10, pady=10)

home = tabview.add("home", text="Home", icon="house")
ttk.Label(home, text="Welcome to the Home page!").pack(padx=20, pady=20)

files = tabview.add("files", text="Files", icon="folder2")
ttk.Label(files, text="Browse your files here.").pack(padx=20, pady=20)

settings = tabview.add("settings", text="Settings", icon="gear")
ttk.Label(settings, text="Configure your settings.").pack(padx=20, pady=20)

app.mainloop()
```

---

## Navigation model

Tabs and pages are keyed by the same **string `key`**. `add(key, ...)`
registers a `TabItem` whose internal `value` equals the key, and a
page in the underlying `PageStack` under the same key. Picking a tab —
either by clicking or by `tabview.select(key)` — writes the key to
the shared `tk.StringVar`, and a variable trace forwards the change
to `pagestack.navigate(key)`.

**Auto-select on first add.** `add()` writes the first tab's key
through the variable, mounting that page immediately. This differs
from a bare PageStack, which stays empty until you call `navigate()`.

**Random-access selection.** Any tab can be picked at any time;
there's no "next" or "previous" tab in the bar itself. The underlying
PageStack still records each navigation in linear history, so
`back()` / `forward()` from outside the tab strip walk through past
selections in order:

```python
tabview.select("settings")
print(tabview.current)              # "settings"

tabview.page_stack_widget.back()    # go back one history step
print(tabview.current)              # whatever was active before "settings"
```

**Imperative API only.** TabView itself has no `signal=` or
`variable=` constructor argument; the selection variable is internal.
Observe selection via `on_page_changed(...)` (the `<<PageChange>>`
event from PageStack), or read `tabview.current` synchronously.

**Unknown keys are silent.** `select("phantom")` and
`navigate("phantom", ...)` are no-ops when the key isn't registered;
no exception, no event. Validate keys yourself if you depend on
strict behavior.

!!! warning "`navigate(key, data=...)` pushes history twice"
    `tabview.navigate(key, data={...})` first writes the key through
    the selection variable — that triggers the trace, which calls
    `pagestack.navigate(key)` with no data — and *then* calls
    `pagestack.navigate(key, data=data)` itself. History grows by two
    entries per call, and `<<PageChange>>` fires twice (once with an
    empty `data` payload, once with the caller's data).

    Workaround until fixed: avoid `tabview.navigate(...)` and use
    `tabview.page_stack_widget.navigate(key, data=...)` directly when
    you need to attach data; pair with `tabview.select(key)` if you
    also want the tab strip to repaint.

---

## Common options

| Option | Default | Notes |
|---|---|---|
| `orient` | `"horizontal"` | `"horizontal"` packs tabs above the page area; `"vertical"` packs them on the left. Construction-only on the inner `Tabs` widget. |
| `variant` | `"bar"` | Visual style. `"bar"` underlines the active tab and adds a divider; `"pill"` is **not implemented for `TabItem`** and crashes on the first `add()`. |
| `show_divider` | auto | Defaults to `True` for `variant="bar"` and `False` otherwise. Pass `True`/`False` to override. |
| `compound` | `"left"` | Icon position relative to tab text. Forwarded to every `TabItem`. |
| `tab_width` | `None` | `None` = auto-size, integer = fixed character width, `"stretch"` = expand horizontally to fill the bar. `"stretch"` is silently ignored in `orient="vertical"`. |
| `tab_padding` | `(12, 8)` | Internal `(padx, pady)` for every tab. |
| `tab_anchor` | auto | Defaults to `"w"` for vertical orientation, `"center"` for horizontal. |
| `enable_closing` | `False` | Default close-button visibility for all tabs: `True` (always), `False` (never), `"hover"` (on hover). Per-tab override via `closable=` in `add()`. **See the "Removing tabs" warning below — the default close handler is broken in current code.** |
| `enable_adding` | `False` | If `True`, shows an add button on the bar that fires `<<TabAdd>>` when clicked. The user is responsible for calling `tabview.add(...)` in the handler — clicking the button doesn't auto-create anything. |
| `accent` | `None` | Theme accent token forwarded to `Tabs` and through to every `TabItem`. |
| Frame kwargs | — | `padding`, `surface`, `show_border`, `width`, `height`, etc. all forwarded to the outer `Frame`. |

Per-tab options live in `add()`:

| `add()` kwarg | Notes |
|---|---|
| `text` | Tab label. |
| `icon` | Icon name (`"house"`) or `IconSpec` dict (`{"name": ..., "size": ..., "color": ..."}`). |
| `page` | Existing widget to use as the page. **If passed, kwargs are silently dropped** — same shape as the [`PageStack` bug](pagestack.md#common-options). Configure your page widget before passing it, or omit `page=` and let `add()` build the Frame. |
| `closable` | `True` / `False` / `"hover"` / `None`. `None` falls through to the widget-level `enable_closing`. |
| `close_command` | Custom handler for the X button. If omitted and `closable` is enabled, defaults to `lambda: tabview.remove(key)` — which is currently broken (see below). |
| `command` | Callback invoked when the tab is selected (in addition to the variable trace). Receives no arguments. |
| `**kwargs` | When `page=` is `None`, forwarded to the auto-created Frame (`padding`, `surface`, `show_border`, …). |

!!! warning "`variant=\"pill\"` crashes on the first `add()`"
    The constructor signature lists `"pill"` as a valid variant, and
    `TabView(variant="pill")` returns successfully — but the very
    next `add()` call raises
    `BootstyleBuilderError: Builder 'pill' not found for widget
    class 'TabItem.TFrame'`. Same root cause as the
    [Tabs `variant="pill"` bug](../navigation/tabs.md#common-options).
    Stick to `"bar"` until a `pill` builder is registered.

---

## Behavior

**Wiring.** Internally, TabView creates `self._tab_variable =
tk.StringVar()` and passes it as `variable=` to `Tabs`. A
`trace_add('write', ...)` on that variable fires `_on_tab_selected`,
which calls `self._page_stack.navigate(key)` whenever the key changes
and the page isn't already mounted. So any path that writes to the
variable — clicking a tab, calling `tabview.select(key)`, or
`tabs_widget.set(key)` — mounts the page; you don't need to drive
both halves explicitly.

**`select(key)`.** Validates `key` against the internal tab map
before writing the variable; an unknown key is a silent no-op (the
variable is not modified, no event fires).

**`current` property.** Returns the active tab key (and page key —
they're the same string), or `None` if no tab is selected (e.g. after
removing the only tab).

**Removing tabs.** This is currently broken in two ways:

!!! danger "`tabview.remove(key)` always raises `KeyError`"
    The implementation passes the *TabItem widget* to
    `Tabs.remove(...)`, which expects a *string key* — Tabs's
    auto-generated internal key (`tab_0`, `tab_1`, …) never matches
    that widget reference, so the membership check raises
    `KeyError: "No tab with key '<TabItem path>'"`.

    The same crash hits the X-click path: when `enable_closing`
    is set and no custom `close_command` is provided, `add()` wires
    the X button to `lambda: self.remove(key)`. Clicking it raises
    the same `KeyError` from inside Tk's button callback.

    There is no clean workaround for the bundled API today. The
    closest path that runs without crashing is:

    ```python
    # remove the page
    tabview.page_stack_widget.remove(key)
    # remove the tab — Tabs uses an auto-generated internal key,
    # so look it up from the TabItem we tracked
    tab = tabview.tab(key)
    for tabs_key, item in tabview.tabs_widget._tabs.items():
        if item is tab:
            tabview.tabs_widget.remove(tabs_key)
            break
    del tabview._tab_map[key]
    ```

    This reaches into private state and is recommended only as a
    stopgap. The `enable_closing` affordance should be considered
    unusable until the `tabview.py` fix lands.

**Auto-select fallback.** Once `remove()` is fixed, the implementation
already handles falling back to the next remaining tab when the
removed tab was active (it sets the variable to the first remaining
key, or to `""` when none remain).

**Coupling.** Tab and page lifetime are joined: every `add(key, ...)`
creates one of each, every `remove(key)` (when it works) destroys
both. There's no path to register a page without a tab — use a bare
`PageStack` if you need that.

**Component access.** The inner widgets are reachable as properties:

```python
tabs = tabview.tabs_widget          # the Tabs widget
pages = tabview.page_stack_widget   # the PageStack widget
```

Use these to apply Tabs- or PageStack-specific configuration that
TabView doesn't surface directly (e.g. `tabs.configure(show_divider=
False)` after construction, or
`pages.on_page_changed(callback)` if you want the helper without
TabView's wrapper).

**Methods worth knowing:**

- `tab(key) -> TabItem` and `page(key) -> Frame` — look up by key.
- `tabs() -> tuple[TabItem, ...]` and `pages() -> tuple[Frame, ...]`
  — all items in registration order.
- `tab_keys() -> tuple[str, ...]` and `page_keys() -> tuple[str,
  ...]` — same keys, returned by both halves.
- `configure_tab(key, **kwargs)` — reconfigure a specific tab
  (e.g. `configure_tab("home", text="Home / Welcome")`).

---

## Events

| Helper | Underlying event | Fired on | Payload |
|---|---|---|---|
| `on_page_changed(cb)` | `<<PageChange>>` | inner `PageStack` | full navigation payload (see [PageStack events](pagestack.md#events)) |
| `on_tab_added(cb)` | `<<TabAdd>>` | inner `Tabs` | `event.data is None` |

Both helpers are thin wrappers over the inner widget's helper —
`tabview.on_page_changed(cb)` calls `pagestack.on_page_changed(cb)`,
and `tabview.on_tab_added(cb)` calls `tabs_widget.on_tab_added(cb)`.

```python
def on_change(event):
    print("now showing:", event.data["page"])

tabview.on_page_changed(on_change)
```

!!! warning "`<<TabSelect>>` and `<<TabClose>>` do not fire on TabView"
    The class docstring (`composites/tabs/tabview.py:23-27`) lists
    `<<TabSelect>>`, `<<TabClose>>`, `<<TabAdd>>`, and `<<PageChange>>`
    under "Events", but **only `<<PageChange>>` and `<<TabAdd>>`
    actually reach the TabView**. `<<TabSelect>>` and `<<TabClose>>`
    are emitted on the individual `TabItem`, and Tk virtual events
    do not propagate up the parent chain — so binding them on
    `tabview` silently no-ops. Same shape as the
    [Tabs bubbling bug](../navigation/tabs.md#events).

    For per-tab events, bind on the TabItem itself:

    ```python
    tab = tabview.tab("home")
    tab.bind("<<TabSelect>>", on_select)
    tab.bind("<<TabClose>>", on_close)
    ```

    For aggregate "any tab changed" handling, prefer
    `on_page_changed` — it fires on every navigation regardless of
    which tab was clicked.

The page-level `<<PageWillMount>>` / `<<PageMount>>` /
`<<PageUnmount>>` events from
[PageStack](pagestack.md#events) also fire, on the page widget (not
on TabView). Bind those on the page returned by `add()` if you need
the mount lifecycle.

---

## When should I use TabView?

Use TabView when:

- a visible tab strip is the right navigation affordance (categorized
  content, document tabs, settings panes),
- the page count is small and equally weighted — users skim the
  labels and pick,
- you want random-access selection: any tab from any tab,
- exactly one page should be visible at a time.

Prefer [`PageStack`](pagestack.md) when navigation is sequential and
the affordance is custom (wizards, drill-in detail flows, app-shell
content driven by a side rail). Prefer
[`Tabs`](../navigation/tabs.md) when you want the tab strip alone
without bundled content (e.g. the tab bar drives external state, or
the content area is rendered from a different model). Prefer
[`Notebook`](notebook.md) for OS-styled tabs over a `ttk.Notebook`.
Prefer [`PanedWindow`](../layout/panedwindow.md) when multiple views
must be visible at once. Inside an
[`AppShell`](../application/appshell.md), the shell already owns its
own `PageStack` driven by the side rail — use
`shell.add_page(...)` instead of nesting a TabView at the top
level.

---

## Related widgets

- **[Tabs](../navigation/tabs.md)** — the standalone tab bar that
  TabView wraps; use directly when you want tab chrome without page
  coupling.
- **[PageStack](pagestack.md)** — the content half of TabView; use
  directly for wizards and other sequential flows.
- **[Notebook](notebook.md)** — `ttk.Notebook` wrapper for OS-styled
  tabs.
- **[AppShell](../application/appshell.md)** — application-level
  shell with its own page stack and side rail.
- **[PanedWindow](../layout/panedwindow.md)** — when multiple views
  should be visible simultaneously.

---

## Reference

- **API reference:** `ttkbootstrap.TabView`
- **Related guides:** Navigation, Layout, Application shell
