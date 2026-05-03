# Virtual Events

Virtual events are the framework's bus for **"something happened"**
notifications. A widget calls `event_generate("<<Name>>", data=...)`,
listeners that bound `<<Name>>` on that widget receive a Tk event with
`event.data` set to the payload. Unlike a `command=` callback (which
fires only on user invocation) or a Signal (which mirrors a value), a
virtual event broadcasts a discrete transition — *the row was deleted*,
*the dialog returned a result*, *the locale changed* — to any number of
loosely-coupled listeners.

Tk treats virtual events as a special case of the generic event-binding
machinery, so almost everything from
[Platform → Events & Bindings](../../platform/events-and-bindings.md)
applies (bindtag walk, `add="+"` semantics, `event.widget`).
ttkbootstrap layers two things on top:

1. **Arbitrary Python payloads.** Stock Tcl/Tk constrains
   `event_generate -data` to a string. ttkbootstrap's
   [`BindingsMixin`](../../reference/capabilities/bind.md) preserves
   the Python object intact so listeners receive the original `dict`,
   `list`, or `tuple` on `event.data`.
2. **A naming convention** for built-in events the framework emits —
   listed in the table below — so apps can subscribe by name without
   inspecting widget internals.

For the imperative-callback surface (`command=`, `widget.bind`,
`on_*` helpers), see [Callbacks](callbacks.md). For the section
overview comparing all three mechanisms, see
[Signals & Events](index.md).

---

## Subscribing

Bind to a virtual event the same way you bind to a physical one:

```python
import ttkbootstrap as ttk

app = ttk.App()
table = ttk.TableView(app, columns=[{"text": "Name"}], rows=[["Alice"]])

def on_row_click(event):
    rec = event.data["record"]
    print("row clicked:", rec)

table.bind("<<RowClick>>", on_row_click, add="+")

app.destroy()
```

Two rules carry over from the platform layer:

- **Always pass `add="+"`** unless you specifically want to *replace*
  any existing handler. The framework's own helpers (`on_dialog_result`,
  `on_changed`, etc.) all use `add="+"` internally, so mixing them with
  raw `bind` calls is safe; mixing two raw `bind` calls without `add="+"`
  is the bug.
- **Bind on the widget that emits**, not on a parent. Virtual events do
  not propagate up the parent chain — see
  [Virtual events do not bubble](#virtual-events-do-not-bubble) below.

For ergonomic alternatives the framework provides per-widget helpers
that wrap `bind` for you:

```python
dlg.on_dialog_result(lambda payload: print("got:", payload))
```

`on_*` helpers are not uniform in their callback shape (some pass the
event, some unwrap `event.data`, some pass derived values) — see the
`on_* / off_*` helpers section in [Callbacks](callbacks.md) for the
per-flavor table.

---

## Emitting

Generate a virtual event with `event_generate`:

```python
widget.event_generate("<<Saved>>", data={"path": "/tmp/doc.txt"})
```

Two arguments matter:

- `data=` — any Python object. The framework's `BindingsMixin` stores
  it on the C-level event record so the listener's `event.data`
  is `==` the value you passed. Verified at runtime — `dict`, `list`,
  `tuple`, custom classes, and primitives all round-trip:

  ```python
  app.bind("<<X>>", lambda e: print(type(e.data).__name__, e.data))
  app.event_generate("<<X>>", data={"k": 1, "n": [1, 2, 3]})
  # dict {'k': 1, 'n': [1, 2, 3]}
  ```

  Non-virtual events ignore `data=` and dispatch with `event.data is
  None`.

- `when=` — controls dispatch timing. Default is `"now"` (fire
  synchronously inside the `event_generate` call); `"tail"` queues to
  the regular event queue (drained by `update()`, NOT
  `update_idletasks`); `"head"` jumps ahead of pending events; `"mark"`
  is documented but rarely used.

  ```python
  order = []
  app.bind("<<Tail>>", lambda e: order.append("handler"))
  app.event_generate("<<Tail>>", when="tail")
  order.append("after generate")
  app.update()
  # order == ['after generate', 'handler']
  ```

  The framework's own emit sites use the default `when="now"` for
  user-invocation events (so the listener has run by the time
  `event_generate` returns) and `when="tail"` only when the emit is
  inside a Tk callback that is itself in the middle of the dispatch
  loop (e.g. `MessageCatalog.locale()` uses `when="tail"` to avoid
  re-entering ttk's style cascade mid-`<<ThemeChanged>>`).

**Generating an unbound virtual event is silent.** If no handler is
registered, `event_generate` returns normally with no warning. This is
how the framework can emit `<<Selected>>` on every selection-aware
widget without forcing every host to register a handler.

---

## Virtual events do not bubble

This is the single most common source of "I bound the event but my
handler never runs" bugs in framework code. **A virtual event emitted
on a child widget does not propagate to its parent.** Tk's bindtag walk
runs only on the receiving widget's bindtags — there is no parent
chain.

Verified at runtime:

```python
parent = ttk.Frame(app)
child = ttk.Frame(parent)

got = []
parent.bind("<<X>>", lambda e: got.append("parent"))

child.event_generate("<<X>>")
# got == []   — parent's listener never fires
```

To reach a parent listener, the emitter (or a relay registered on the
child) must call `event_generate` *on the parent* explicitly:

```python
def relay(event):
    parent.event_generate("<<X>>", data=event.data)

child.bind("<<X>>", relay, add="+")
```

Several composites in the codebase document virtual events as
"bubbled from child" but don't actually re-emit. Confirmed cases worth
calling out — bind on the emitting child until the framework forwards
them:

| Documented on | Actually emitted on | Workaround |
|---|---|---|
| `Tabs.<<TabSelect>>`, `Tabs.<<TabClose>>` | the inner `TabItem` returned by `Tabs.add(...)` | `tabs.item(key).bind(...)` |
| `TabView.<<TabSelect>>`, `<<TabClose>>` | the inner `TabItem` (Tabs's child) | `tabview.tabs_widget.item(key).bind(...)` |
| `SideNav.<<ItemInvoked>>`, `<<GroupExpanding>>` / `<<GroupCollapsed>>` | the `SideNavItem` / `SideNavGroup` | `sidenav.node(key).bind(...)` |
| `PageStack.<<PageWillMount>>`, `<<PageUnmount>>` | the page widget itself | `page.bind(...)` |
| `SelectBox.<<Change>>` | the inner `entry_widget` | `selectbox.entry_widget.bind(...)` or use `on_changed(cb)` |

The `on_*` helpers built around these events do work (they bind on the
correct emitter internally) — the gotcha is only when you call
`bind('<<...>>')` directly on the composite itself.

---

## Framework-emitted events

The events the framework emits in v2. Bind on the widget that emits;
many have an `on_*` helper that wraps the bind for you. This is not
exhaustive — see the per-widget Events sections in
[`docs/widgets/`](../../widgets/index.md) for the full payload contract
of each event.

### Cross-cutting

These fire on the root window (or any widget under it that bound them
with `add="+"`).

| Event | Fired by | Payload (`event.data`) |
|---|---|---|
| `<<ThemeChanged>>` | Tk, when `Style.theme_use(...)` is called | none — read theme via `Style.theme_use()` |
| `<<LocaleChanged>>` | `MessageCatalog.locale(new_locale)` | `{"locale": new_locale}` |

`<<ThemeChanged>>` is Tk's stock event — it's how the framework's own
style-builders, image cache, and `MenuItem` icon cache stay in sync
across a runtime theme switch. Most apps don't bind it directly; reach
for it when you embed canvas-drawn content (Meter, FloodGauge, custom
canvas widgets) that needs to repaint with new theme colors.

`<<LocaleChanged>>` is framework-emitted (by
`MessageCatalog.locale(new_locale)`). The framework's
`LocalizationMixin` and several composites (`Notebook`, `Calendar`,
`TextEntry`, `SpinnerEntry`) bind it internally to refresh translated
labels.

### Selection and value changes

| Event | Common emitters | Payload |
|---|---|---|
| `<<Change>>` | `OptionMenu`, `SelectBox` (on `entry_widget`), `Meter`, `Tabs` (via signal trace) | varies — most carry no payload (read widget state instead) |
| `<<Selected>>` | `Expander` (on header click), various selection composites | `{"value": ...}` |
| `<<SelectionChange>>` | `TableView`, `ListView`, `FilterDialog` | `TableView`: `{"records": [...], "iids": [...]}`; `ListView`: none; `FilterDialog`: `{"selected": [...]}` |
| `<<SelectionChanged>>` | `SideNav` | `{"key": str}` |

The `Change` / `Selected` / `SelectionChange` / `SelectionChanged`
naming inconsistency is a known bug.

### Lifecycle and navigation

| Event | Emitter | Payload |
|---|---|---|
| `<<DialogResult>>` | every `Dialog` subclass on close | `{"result": ..., "confirmed": bool}` |
| `<<PageWillMount>>`, `<<PageMount>>`, `<<PageUnmount>>` | `PageStack` (the first two on the *page* widget; the third with no payload) | `{"page": str, "prev_page": str | None, "prev_data": dict, "nav": str, "index": int, "length": int, "can_back": bool, "can_forward": bool}` |
| `<<PageChange>>` | `PageStack`, `AppShell` (forwarded) | same as `<<PageMount>>` plus caller-supplied `data=...` keys merged in at the top level |
| `<<TabSelect>>`, `<<TabClose>>` | individual `TabItem` (NOT Tabs/TabView itself) | none — read `tabs.get()` |
| `<<TabAdd>>` | `Tabs`, `TabView` | `{"value": str}` |

### Data-bound widgets

`TableView` emits 7 events; `ListView` emits 9. The full payload tables
live on those widget pages — see
[TableView § Events](../../widgets/data-display/tableview.md#events) and
[ListView § Events](../../widgets/data-display/listview.md#events). The
event names follow the pattern `<<RowClick>>` / `<<RowInsert>>` /
`<<RowUpdate>>` / `<<RowDelete>>` / `<<RowMove>>` for TableView and
`<<ItemClick>>` / `<<ItemInsert>>` / `<<ItemUpdate>>` / `<<ItemDelete>>`
/ `<<ItemDeleteFail>>` / `<<ItemDrag>>` etc. for ListView.

### Widget-specific

A scattering of one-off events worth knowing about:

| Event | Emitter | Payload |
|---|---|---|
| `<<Toggle>>` | `Expander` | `{"expanded": bool}` |
| `<<Increment>>`, `<<Decrement>>` | `NumericEntry` | none |
| `<<Input>>` | `TextEntry`, `SpinnerEntry` parts | the value as string |
| `<<DisplayModeChanged>>`, `<<PaneToggled>>` | `SideNav` | `{"mode": str}` / `{"open": bool}` |
| `<<AccordionChange>>` | `Accordion` | `{"expanded": [str]}` |
| `<<TableViewExportAll>>`, `<<TableViewExportSelection>>`, `<<TableViewExportPage>>` | the `TableView`'s inner `_tree` (not the TableView!) | rows |

The export-events emit on the TableView's private inner widget — a
known bug. Bind on `tv._tree` until fixed.

---

## Tk's stock virtual events

Tk pre-registers a small set of cross-platform virtual events that map
to the right keyboard shortcuts on each OS. They show up in
`widget.event_info()`:

| Event | Default sequence (varies by platform) |
|---|---|
| `<<Cut>>`, `<<Copy>>`, `<<Paste>>` | `Cmd-X` / `Cmd-C` / `Cmd-V` on macOS; `Ctrl-X` / `Ctrl-C` / `Ctrl-V` elsewhere |
| `<<Undo>>`, `<<Redo>>` | `Cmd-Z` / `Shift-Cmd-Z` on macOS; `Ctrl-Z` / `Ctrl-Y` elsewhere |
| `<<SelectAll>>`, `<<Clear>>`, `<<ToggleSelection>>` | platform-specific |
| `<<PrevChar>>`, `<<NextChar>>`, `<<PrevWord>>`, `<<NextWord>>`, `<<PrevLine>>`, `<<NextLine>>`, `<<LineStart>>`, `<<LineEnd>>` | navigation in text widgets |
| `<<SelectPrevChar>>` ... `<<SelectLineEnd>>` | shifted versions of the above |
| `<<ContextMenu>>` | right-click on most platforms; `Ctrl-click` on macOS |
| `<<NextWindow>>`, `<<PrevWindow>>` | focus traversal |

For app-wide cross-platform shortcuts beyond this set, use the
[`Shortcuts`](../../platform/events-and-bindings.md#modifier-keys)
service — it expands `Mod+S` into `<Command-s>` on macOS and
`<Control-s>` everywhere else.

---

## Naming conventions

Framework-emitted events follow these conventions. Apply them to
custom events you add:

- **PascalCase, double angle brackets**: `<<DialogResult>>`,
  `<<RowClick>>`, never `<<dialog_result>>` or `<<row-click>>`.
- **Past-tense or completion-form**: `<<Selected>>` (the act
  completed), not `<<Select>>` (an imperative). The framework's own
  `<<Change>>` is an exception kept for back-compat.
- **Domain-prefix when the same noun is reused across widgets**:
  `<<RowClick>>` (TableView) vs `<<ItemClick>>` (ListView). Both
  produce a "click" notification but the row vs item naming makes the
  payload shape unambiguous.
- **Don't reference input devices**: `<<Saved>>` not
  `<<EnterPressed>>`. Multiple inputs may produce the same semantic
  action.
- **Carry payload over re-reads**: prefer
  `event_generate("<<RowMove>>", data={"records": moved})` over
  emitting first and then expecting listeners to query state — the
  state may have already mutated again by the time they run.

---

## Pitfalls

**Default `when="now"` fires synchronously, inside `event_generate`.**
Listeners run on the calling thread before `event_generate` returns,
so a slow listener blocks the call site. If the emit happens during
another callback (mid-dispatch), use `when="tail"` to defer to the next
queue drain.

**`update_idletasks()` does not drain `when="tail"` events.** Tail
events sit on the regular event queue, not the idle queue. Use
`update()` to drain them.

**`widget.unbind(seq, fid)` is broken for `add="+"` bindings on
Python 3.13 / Tk 8.6.** A CPython tkinter bug filters bind script
lines with the wrong prefix; `add="+"` bindings produce raw script
lines that never match, so `unbind(seq, fid)` deletes the bound proc
without removing it from the binding sequence — *every* handler on
`seq` then stops firing on subsequent `event_generate` calls. The
framework's `off_*` helpers are all implicated. Workaround: call
`widget.unbind(seq)` (no fid) to detach all handlers, then re-bind the
ones you want to keep. See [Callbacks](callbacks.md) under the
`widget.bind` section for the full description (the `!!! danger`
block).

**Type silently passed through.** `event.data` arrives as the same
Python object you emitted — no copy, no defensive coercion. Listeners
that mutate a passed `dict` or `list` mutate the emitter's payload;
listeners that compare `is` rather than `==` may match across emits if
the emitter reuses the dict.

**Generating an event with `data=` on a non-virtual sequence does
nothing visible.** `widget.event_generate("<Configure>", data={"x":1})`
silently discards the data — `event.data` arrives as `None` on
non-virtual events. Use a `<<Name>>` sequence for any payload-carrying
emit.

---

## Next steps

- [Platform → Events & Bindings](../../platform/events-and-bindings.md)
  — the underlying bindtag walk, `add="+"` semantics, and the
  `event` object.
- [Callbacks](callbacks.md) — `command=`, `widget.bind`, and the
  `on_*` / `off_*` helpers; the three callback shapes for `bind`-based
  helpers.
- [Signals](signals.md) — the value-tracking surface that complements
  virtual events. Signals mirror state; virtual events mark
  transitions.
- [Capabilities → Localization](../localization.md) for
  `<<LocaleChanged>>` listener patterns.
- The Events section of any widget page (e.g.
  [TableView](../../widgets/data-display/tableview.md#events),
  [PageStack](../../widgets/views/pagestack.md#events)) for the full
  per-widget event table.
