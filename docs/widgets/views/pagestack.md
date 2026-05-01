---
title: PageStack
---

# PageStack

`PageStack` is a stacked-views container — a `Frame` that owns a set of
keyed pages and shows exactly one of them at a time. It is *pure*: no
tab bar, no chrome, no built-in switching UI. The caller decides when
to navigate, either by computing a target key or by walking the
back / forward history.

PageStack is the foundation for the rest of the views surface.
[`TabView`](tabview.md) pairs a `Tabs` bar with a `PageStack` so tab
clicks drive navigation; [`AppShell`](../application/appshell.md)
exposes `shell.pages` directly so app-level routing reuses the same
push-pop history. Use PageStack on its own when navigation is driven
from somewhere other than a tab strip — wizards, breadcrumbs, custom
buttons, or model-state changes.

<figure markdown>
![pagestack](../../assets/dark/widgets-pagestack.png#only-dark)
![pagestack](../../assets/light/widgets-pagestack.png#only-light)
</figure>

---

## Basic usage

Create a stack, add a few pages, then call `navigate()` to mount one:

```python
import ttkbootstrap as ttk

app = ttk.App()
stack = ttk.PageStack(app, padding=10)
stack.pack(fill="both", expand=True)

start = stack.add("start")
details = stack.add("details")
confirm = stack.add("confirm")

ttk.Label(start, text="Start").pack()
ttk.Button(start, text="Next", command=lambda: stack.navigate("details")).pack()

ttk.Label(details, text="Details").pack()
ttk.Button(details, text="Next", command=lambda: stack.navigate("confirm")).pack()
ttk.Button(details, text="Back", command=stack.back).pack()

ttk.Label(confirm, text="Confirm").pack()
ttk.Button(confirm, text="Back", command=stack.back).pack()

stack.navigate("start")  # the first page must be navigated to explicitly

app.mainloop()
```

`add()` registers a page and returns its widget; it does **not** mount
it. Until `navigate()` is called the stack is empty — `current()`
returns `None` and no page is visible.

---

## Navigation model

A PageStack is addressed by **string keys**, navigated **sequentially**
(push / back / forward), and observed **imperatively** (events on the
stack and on the individual pages — there is no `signal=` or
`variable=` channel).

**Key registration.** `add(key)` takes a unique string and returns the
page widget. An empty key raises `ValueError`; a duplicate key raises
`NavigationError`. When `page=` is omitted, PageStack creates a
`Frame` parented to the stack and returns it; when `page=` is passed,
the caller supplies an existing widget.

**History.** Each `navigate(key, data=...)` pushes a new entry onto a
linear history of `(key, data)` pairs. `back()` and `forward()` move
the index without truncating; a fresh `navigate()` after `back()`
truncates the forward portion (matches browser semantics). Pass
`replace=True` to overwrite the current entry instead of pushing — use
this for redirects (e.g. login → dashboard, where the login screen
shouldn't sit in the back stack).

**Data round-trip.** The `data` dict you pass to `navigate()` is
stored in history alongside the key, replayed when you walk back or
forward to that entry, and merged into the navigation event payload.

**No reactive channel.** PageStack does not accept `signal=` or
`variable=`. To observe navigation, bind `<<PageChange>>` on the
stack or use `on_page_changed(...)`. To observe the current page's
mount lifecycle, bind events on the page widget — see *Events* below
for the asymmetry.

```python
stack.navigate("settings", data={"section": "billing"})
print(stack.current())     # ("settings", {"section": "billing"})
print(stack.can_back())    # True
stack.back()
print(stack.current())     # whatever was active before "settings"
```

---

## Common options

PageStack has no widget-specific configuration of its own — it
inherits the standard `Frame` surface.

| Option | Type | Notes |
|---|---|---|
| `width` / `height` | `int` | Pixel dimensions. Useful when content is variable-size and the stack should reserve space. |
| `padding` | `int` / 2-tuple / 4-tuple | Border padding inside the stack frame. |
| `takefocus` | `bool` | Whether the stack itself can receive keyboard focus (rarely needed — pages handle focus). |
| `accent` / `surface` / `show_border` | tokens | Inherited from `Frame`. Container-rerouting applies (`accent="primary"` is treated as `surface="primary"`). See [Frame](../layout/frame.md). |

Per-page options are passed to `add()` when no `page=` is supplied:

```python
page = stack.add("settings", padding=12, surface="card", show_border=True)
```

These reach the auto-created `Frame`. Use them to apply theming or
layout to individual pages.

!!! warning "Kwargs are silently dropped if `page=` is passed"
    When you pass an existing widget as `page=`, the keyword arguments
    are discarded — `add()`'s signature is
    `add(key, page=None, **kwargs)`, and the kwargs only feed the
    auto-created Frame in the `page is None` branch.

    ```python
    custom = ttk.Frame(stack)
    stack.add("foo", custom, padding=99)  # padding=99 is silently ignored
    ```

    Configure your widget before passing it, or omit `page=` and let
    `add()` build the Frame.

!!! warning "Pages must be parented to the stack"
    `add(key, widget)` does **not** reparent `widget`. If
    `widget.master` is some other frame, the registration succeeds
    but the page is never visually attached to the stack — calling
    `widget.pack(...)` packs into the original master, not into
    `self`. Always construct page widgets with `master=stack`.

---

## Behavior

**No auto-mount.** `add()` registers a page but does not show it.
The stack stays empty until `navigate()` is called explicitly. This
differs from `Tabs.add()`, which writes the first added value to its
selection variable.

**History truncation.** Calling `navigate(key)` while the index is
not at the end (i.e. after a `back()`) drops the forward portion of
history before pushing the new entry — the user's "future" is lost,
matching browser behavior. To preserve history when re-navigating to
an existing key, use the `replace=True` form.

**`replace=True`.** Replaces the current history entry's `(key,
data)` pair in place, leaving `index` and history length unchanged.
With no current page (e.g. before the first `navigate()`), `replace=`
is ignored and the call behaves as a normal push.

**Mount sequence.** `navigate(key, data=...)` runs:

1. Mutate history (push or replace).
2. `<<PageUnmount>>` on the previous page (if any), then unpack it.
3. `<<PageWillMount>>` on the incoming page (data attached).
4. Pack the incoming page with `fill="both", expand=True`.
5. `<<PageMount>>` on the stack.
6. `<<PageChange>>` on the stack.

`<<PageWillMount>>` therefore fires *before* the page is geometry-
managed — DOM-style "the page is in the tree but not yet visible."
`<<PageMount>>` fires after pack, so widget sizes are valid by then.

**Removing pages.** `remove(key)` destroys the page widget and drops
it from the page registry, but does **not** rewrite the history list.
If the removed page sits in the middle of history, walking through
that index later raises `NavigationError` from `navigate()`'s
existence check.

!!! warning "`remove()` orphans history; back/forward can crash"
    `stack.remove(key)` deletes the widget and removes it from
    `_pages`, but `_history` and `_index` are untouched (with one
    exception: if the removed key happens to be `_current`, only
    `_current` is cleared to `None`). Subsequent `back()` /
    `forward()` calls that step onto the orphan entry raise
    `NavigationError: Page <key> does not exist`.

    ```python
    # history=[a, b, c], current=c, index=2
    stack.remove("b")
    stack.back()   # NavigationError: Page b does not exist
    ```

    Workaround: clear and rebuild history after removal, or only
    remove pages at the head/tail of history. (Logged on the bugs
    list — `remove()` should rewrite history to drop the orphan
    entry and adjust `_index`.)

**Data merge collisions.** The dict passed to `navigate(data=...)` is
merged with the navigation keys at the top level of `event.data`.
Caller keys that collide with `page`, `prev_page`, `prev_data`,
`nav`, `index`, `length`, `can_back`, or `can_forward` are silently
overridden. Avoid those names in your data payload.

**Mount semantics under reorder.** PageStack does not support page
reordering — each page is registered once at `add()` time and stays
in its registry slot until `remove()`. The `_history` list is the
order of *navigation*, not the order of registration.

---

## Events

| Event | Fired on | `event.data` | Notes |
|---|---|---|---|
| `<<PageUnmount>>` | the outgoing page widget | `None` | Fires before unpack. Bind on the page returned by `add()`. |
| `<<PageWillMount>>` | the incoming page widget | full payload | Fires before pack. |
| `<<PageMount>>` | the PageStack | full payload | Fires after pack. |
| `<<PageChange>>` | the PageStack | full payload | Fires last; preferred hook for "navigation completed" listeners. |

Full payload shape (where present):

```python
{
    "page": str,            # key just navigated to
    "prev_page": str | None,  # previously-active key (None for first navigate)
    "prev_data": dict,        # data dict from the previous history entry
    "nav": "push" | "back" | "forward",
    "index": int,             # current history index after the move
    "length": int,            # total history length
    "can_back": bool,
    "can_forward": bool,
    # …caller-supplied keys from data=, merged at the top level
}
```

The asymmetry in the table is significant: **two of the four events
fire on the page widget, two on the stack**, and Tk virtual events do
not propagate up the parent chain. Binding `<<PageWillMount>>` or
`<<PageUnmount>>` on the stack itself silently no-ops.

```python
# WRONG — these never fire
stack.bind("<<PageUnmount>>", on_unmount)
stack.bind("<<PageWillMount>>", on_will_mount)

# RIGHT — bind on the page returned by add()
page = stack.add("settings")
page.bind("<<PageUnmount>>", on_unmount)
page.bind("<<PageWillMount>>", on_will_mount)
```

The `on_page_changed(callback) -> bind_id` /
`off_page_changed(bind_id)` helpers wrap `<<PageChange>>` only — the
other three events have no helper and require explicit `bind()`.

!!! warning "`<<PageUnmount>>` has no payload"
    `<<PageMount>>`, `<<PageWillMount>>`, and `<<PageChange>>` all
    carry the full navigation payload via `event.data`.
    `<<PageUnmount>>` is fired without a `data=` argument, so
    handlers receive `event.data is None`. Read state from the
    stack itself (`stack.current()`, `stack.can_back()`) inside the
    unmount handler. (Logged on the bugs list — should pass the
    same payload as the other three for consistency.)

---

## When should I use PageStack?

Use PageStack when:

- navigation is **sequential** and history-driven (wizards, drill-in
  detail flows, multi-step forms with back-tracking),
- exactly one page should be visible at a time,
- the navigation surface is custom — the buttons or breadcrumbs that
  drive the stack live in your code, not on a tab bar.

Prefer [`TabView`](tabview.md) when you want a tab strip wired to the
stack out of the box. Prefer [`Notebook`](notebook.md) when you want
the OS-native tabbed look. Prefer
[`PanedWindow`](../layout/panedwindow.md) when multiple views must be
visible at once. Inside an [`AppShell`](../application/appshell.md),
the shell already owns a PageStack at `shell.pages` — use that
instead of constructing your own.

---

## Related widgets

- **[TabView](tabview.md)** — `Tabs` + `PageStack` composed; the
  common case when you want tab-driven navigation.
- **[Notebook](notebook.md)** — wraps `ttk.Notebook` for OS-styled
  tabs over a similar one-page-at-a-time model.
- **[AppShell](../application/appshell.md)** — owns a PageStack at
  `shell.pages`; `shell.add_page(...)` forwards to it.
- **[Frame](../layout/frame.md)** — the per-page container that
  `add()` creates by default.

---

## Reference

- **API reference:** `ttkbootstrap.PageStack`
- **Related guides:** Navigation, Layout, Application shell
