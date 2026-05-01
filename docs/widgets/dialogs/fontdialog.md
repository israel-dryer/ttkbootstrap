---
title: FontDialog
---

# FontDialog

`FontDialog` is a modal font picker built on [`Dialog`](dialog.md). The
window is laid out with a scrollable family list, a fixed-size list,
weight (`normal` / `bold`) and slant (`roman` / `italic`) radio button
groups, underline / overstrike check buttons, and a live preview pane
that re-renders as the user changes any setting. On confirmation the
dialog returns a fully-configured `tkinter.font.Font` object suitable
for passing directly to any widget's `font=` option.

It's the right shape for occasional "let the user pick a font" tasks
inside a settings or preferences flow. For toolbars or other always-
visible font controls, build inline pickers from
[`Combobox`](../selection/combobox.md) and [`SpinnerEntry`](../inputs/spinnerentry.md)
instead — opening a modal on every interaction is overkill.

---

## Basic usage

Construct, `show()`, branch on `.result is not None`:

```python
import ttkbootstrap as ttk

app = ttk.App()

dlg = ttk.FontDialog(title="Choose a font")
dlg.show()

if dlg.result is not None:
    label = ttk.Label(app, text="Hello", font=dlg.result)
    label.pack(padx=20, pady=20)

app.mainloop()
```

`show()` blocks until the user clicks **OK**, clicks **Cancel**,
presses **Escape**, or closes the window. After it returns, `.result`
is either a `tkinter.font.Font` instance or `None` — branch on
`is not None` rather than truthiness.

---

## Result value

`.result` is a `tkinter.font.Font` when the user clicked **OK**, or
`None` on any cancel path:

```python
dlg.result  # tkinter.font.Font instance, or None
```

The returned `Font` is the **same object** the dialog used as its
internal preview font, fully configured with the family, size, slant,
weight, underline, and overstrike the user selected. It exposes the
standard `tkinter.font.Font` API:

```python
dlg.result.actual()      # {'family': 'Arial', 'size': 14, 'weight': 'bold', ...}
dlg.result.cget("size")  # 14
dlg.result.measure("W")  # pixel width of "W" at this font
```

The font remains valid after the dialog is destroyed — Tk keeps the
named-font registration alive as long as anything references it. Pass
it straight to a widget's `font=` option.

`.result` is set when the user clicks **OK**. Cancel, Escape, and the
window-close (`X`) button all leave it as `None`. The dialog does
**not** emit a `<<DialogResult>>` event — see [Events](#events).

---

## Common options

Only three constructor arguments are exposed:

| Option | Purpose |
|---|---|
| `title` | Window title. Default `"font.selector"` — a translation key auto-resolved by the framework's window setup. Pass an explicit string to override. |
| `master` | Parent widget. The dialog is modal-and-transient against this master. Defaults to the application root. |
| `default_font` | **Named-font name** to seed the dialog with — a string like `"TkDefaultFont"`, `"TkFixedFont"`, `"TkTextFont"`, `"TkHeadingFont"`, or any other font registered through `tkinter.font.nametofont`. **Not** a `Font` instance and **not** a family name. Defaults to `"TkDefaultFont"`. |

```python
dlg = ttk.FontDialog(
    master=app,
    title="Choose code font",
    default_font="TkFixedFont",
)
```

The dialog has a fixed UI; there is no `initial_font` Font-object
argument, no preview-text override, no buttons override, and no
`localize` flag. If you need a `Font` instance as the seed, register
it with a name first and pass that name:

```python
my_font = font.Font(family="Inter", size=14, weight="bold", name="UserDefault")
dlg = ttk.FontDialog(default_font="UserDefault")
```

The internal labels (`font.family`, `font.size`, `font.weight`,
`font.weight.normal`, `font.weight.bold`, `font.slant`,
`font.slant.roman`, `font.slant.italic`, `font.effects`,
`font.effects.underline`, `font.effects.overstrike`, `font.preview`)
and the preview sample text (`font.preview_text`) are translation
keys resolved against `MessageCatalog`. A locale that doesn't define
those keys will display the literal `font.foo` strings — supply the
keys in your catalog before shipping a translated build.

---

## Behavior

### Modality and presentation

`FontDialog` is **modal-only**. `show()` defaults to `modal=True` and
`anchor_to="screen"`, which centers the 800 × 600 window on the
screen rather than on the parent — different from most other
ttkbootstrap dialogs, which center on parent. Pass an explicit
`position=(x, y)` or `anchor_to=parent` to override:

```python
dlg.show(anchor_to=app, anchor_point="center", window_point="center")
```

Other [`Dialog.show()`](dialog.md#common-options) kwargs (`offset=`,
`auto_flip=`) are forwarded.

### Default and cancel bindings

Unlike [`ColorChooserDialog`](colorchooser.md), `FontDialog` does
register both a default button and a cancel button:

- **OK** has `default=True` and `role="primary"` — pressing
  **Enter** anywhere outside the family/size lists invokes it.
- **Cancel** has `role="cancel"` — pressing **Escape** invokes it
  cleanly (rather than going through Dialog's destroy-fallback path).

Inside the family or size `Treeview` lists, `<Return>` is captured by
the tree widget and won't propagate to the dialog-level Enter binding.
Click outside the list (e.g. on the preview pane) before pressing
Enter, or click OK directly.

The window-close (`X`) button destroys the toplevel directly without
invoking the Cancel command, but `.result` still ends up as `None`
since `show()` resets it to `None` at the start.

### Live preview

The preview pane shows the localized `font.preview_text` rendered in
the currently-selected font. Every selection change — family, size,
weight, slant, underline, overstrike — is wired through `Variable`
traces that mutate the **same** `tkinter.font.Font` object the dialog
will eventually return. Two consequences:

- The preview is always WYSIWYG against the returned `.result`.
- The font instance is reused; you don't get a fresh `Font` per
  `show()` call. This matters if you keep a reference to a previous
  `.result` and then re-open the dialog — the previous reference will
  reflect the new selections. If you need an immutable snapshot, copy
  it: `font.Font(**dlg.result.actual())`.

### Family list contents

The family list is built from `tkinter.font.families()` filtered to
exclude empty strings, names starting with `@` (Tk's vertical-text
aliases on some platforms), and any family whose name contains
`"emoji"` (case-insensitive). The currently-selected family is
guaranteed to appear even if the filter would otherwise drop it. The
list is sorted alphabetically.

---

## Events

`FontDialog` does **not** emit a `<<DialogResult>>` virtual event and
does **not** expose an `on_dialog_result` helper — unlike
[`MessageDialog`](messagedialog.md), [`DateDialog`](datedialog.md),
and [`ColorChooserDialog`](colorchooser.md), all of which fire that
event from their button-command paths.

Because `show()` blocks until the dialog closes, the canonical
pattern is the synchronous one:

```python
dlg = ttk.FontDialog(master=app)
dlg.show()                       # blocks
if dlg.result is not None:
    apply_font(dlg.result)       # post-close handling
```

If you need an event-driven shape (e.g. to chain multiple actions on
commit), drop down to [`Dialog`](dialog.md) directly with a custom
`content_builder` and add a button `command=` that runs your handler
before close.

---

## UX guidance

- **Pre-seed `default_font` to the user's current selection.** A
  "change editor font" preference should open on the editor's current
  font so the user can confirm rather than rebuild it. Register the
  current font under a name (`font.Font(..., name="EditorFont")`) and
  pass `default_font="EditorFont"`.
- **Keep the result reference scoped to the use site.** Because the
  returned `Font` is the dialog's live preview object, holding it
  past a second `show()` call gives you a font that reflects the
  *new* selections, not the old ones. If you need a snapshot, clone
  with `font.Font(**dlg.result.actual())` before storing.
- **Don't open this on every keystroke.** A modal font picker is a
  commit-once interaction. For continuously-varying font controls
  (toolbar font menus, live size sliders), build an inline picker
  from [`Combobox`](../selection/combobox.md) (family) plus
  [`SpinnerEntry`](../inputs/spinnerentry.md) (size) plus
  [`CheckButton`](../actions/buttongroup.md) (weight/slant) — the
  modal is the wrong shape for that.
- **Translate the catalog keys** before shipping a localized build.
  `font.family`, `font.size`, `font.weight`, the `font.weight.normal`
  / `font.weight.bold` / `font.slant.roman` / `font.slant.italic`
  radio labels, and the `font.preview_text` sample all come from
  `MessageCatalog` — supply translations or override
  `MessageCatalog.set("font.preview_text", "Your sample…")` once at
  startup.

---

## When should I use FontDialog?

Use `FontDialog` when:

- the user picks a font **occasionally** in a settings/preferences
  flow, and an explicit OK/Cancel commit is appropriate.
- you need a single dialog that exposes family, size, weight, slant,
  and effects together — without you building the listboxes or
  preview wiring.
- the result is a **persistent setting** (editor font, default label
  font, exported-document font), not a continuously-varying value.

Prefer a different control when:

- the user **changes font frequently and needs immediate feedback**
  (rich-text toolbars, live theme editors) → put a `Combobox` for
  family + `SpinnerEntry` for size + a couple of toggle buttons in
  the toolbar; the modal is the wrong shape.
- you only need to pick the **family** (size is fixed, no
  weight/slant) → a [`Combobox`](../selection/combobox.md) populated
  with `tkinter.font.families()` is lighter and inline.
- the dialog needs a **custom layout** (e.g. extra fields, a font-
  source picker, embedded license preview) → drop down to
  [`Dialog`](dialog.md) with a `content_builder` that lays out the
  primitives directly.
- you need the **OS-native font picker** for platform-consistency
  reasons → there is no stdlib equivalent on Tk, but
  `tkinter.font.Font` accepts strings parseable by Tk's font system,
  so a third-party native dialog can interoperate by returning a
  family/size/style tuple that you wrap in `font.Font(...)`.

---

## Additional resources

**Related widgets**

- [`Dialog`](dialog.md) — the generic builder underneath; reach for
  it directly when the picker's fixed layout doesn't fit.
- [`ColorChooserDialog`](colorchooser.md) — same "modal style picker"
  pattern for color selection.
- [`FormDialog`](formdialog.md) — multi-field structured input,
  useful when font choice is one of several settings.
- [`MessageBox`](messagebox.md) — message + button-row modal for
  simple confirmations.

**Framework concepts**

- [Windows](../../platform/windows.md)
- [Localization](../../capabilities/localization.md)

**API reference**

- **API reference:** [`ttkbootstrap.FontDialog`](../../reference/dialogs/FontDialog.md)
- **Related guides:** Dialogs, Localization, Theming
