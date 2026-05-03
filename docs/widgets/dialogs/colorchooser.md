---
title: ColorChooser
---

# ColorChooser

`ColorChooserDialog` is a modal color-picker dialog wrapping the
[`ColorChooser`](#) widget in a `Dialog` shell with an OK/Cancel
footer. The chooser exposes three input modes — a hue/saturation
spectrum with a luminance slider, a swatch grid for the active
theme's accent palette, and a swatch grid for a fixed standard
palette — plus synchronized RGB / HSL / Hex spinners for direct
numeric entry. On Windows and Linux the footer also gets an
**eyedropper** that opens a [`ColorDropperDialog`](colordropper.md)
to sample a screen pixel.

It's the right shape for an occasional pick-a-color task — theming a
panel, choosing a label color, configuring a drawing tool. For
**screen sampling without a picker UI**, use
[`ColorDropper`](colordropper.md) directly. For **frequent recolor**
flows that need immediate feedback (paint apps, theme editors), an
inline swatch palette beats a modal — open this dialog on demand
rather than every interaction.

The page slug is `ColorChooser` for historical reasons; the actual
class is `ttk.ColorChooserDialog`. The bare `ttk.ColorChooser` is
the embedded chooser widget, intended for cases where you want the
spectrum + swatches inline (without OK/Cancel chrome).

---

## Basic usage

Construct, `show()`, read `.result`:

```python
import ttkbootstrap as ttk

app = ttk.App()

dlg = ttk.ColorChooserDialog(
    title="Choose a color",
    initial_color="#3b82f6",
)
dlg.show()

if dlg.result is not None:
    print("hex:", dlg.result.hex)
    print("rgb:", dlg.result.rgb)
    print("hsl:", dlg.result.hsl)

app.mainloop()
```

`show()` blocks until the user clicks OK, clicks Cancel, presses
Escape, or closes the window. After it returns, `.result` is either
a `ColorChoice` namedtuple or `None` — branch on `is not None`
rather than truthiness (a fully-zero RGB is still a valid choice).

---

## Result value

`.result` is a `ColorChoice` namedtuple when the user confirmed, or
`None` on any cancel path:

```python
dlg.result  # ColorChoice(rgb=(r, g, b), hsl=(h, s, l), hex='#rrggbb')
            # or None
```

The same color is exposed in **all three representations** so
callers don't have to convert. `.rgb` is a `(0–255, 0–255, 0–255)`
tuple of ints, `.hsl` is a `(0–360, 0–100, 0–100)` tuple of ints,
and `.hex` is a `'#rrggbb'` string. Read whichever the rest of the
code needs.

`.result` is set when the user clicks **OK**. All other dismissal
paths — Cancel button, Escape, the window close button — leave it
as `None`. `<<DialogResult>>` fires once after `show()` returns
regardless of which path closed the dialog (see [Events](#events)).

---

## Common options

The dialog has a fixed UI; only three constructor arguments are
exposed:

| Option | Purpose |
|---|---|
| `title` | Window title. Default `"color.chooser"` — a translation key auto-resolved by the framework's window setup. Pass an explicit string to override. |
| `initial_color` | Starting color, accepted as any string `ImageColor.getrgb` understands (`'#rrggbb'`, `'rgb(r, g, b)'`, named CSS colors, etc.). Defaults to the active theme's `bg` token, so a freshly-opened dialog reflects the surrounding app. |
| `master` | Parent window used for transient placement and as the `<<DialogResult>>` event target. Defaults to the application root. |

```python
dlg = ttk.ColorChooserDialog(
    master=app,
    title="Pick an accent",
    initial_color="primary",  # also accepts theme tokens via ImageColor
)
```

There is **no** `format` / `output` option (the old page documented
one — it doesn't exist), no `buttons` override, no width/padding
knobs, and no `localize` flag. The dialog is a fixed UI; reach for
[`Dialog`](dialog.md) directly if you need a custom footer or a
different layout.

The internal labels (tab names like `color.advanced` /
`color.themed` / `color.standard`, the field labels
`color.hue:` / `color.sat:` / `color.lum:` / `color.hex:` /
`color.red:` / `color.green:` / `color.blue:`, and the preview
captions `color.current` / `color.new`) are translation keys
resolved against `MessageCatalog`. A locale that doesn't define
those keys will display the literal `color.foo:` strings — supply
the keys in your catalog before shipping a translated build.

---

## Behavior

### Modality and presentation

`ColorChooserDialog` is **modal-only**. `show()` accepts a
`position=(x, y)` tuple to override placement and a `modal=True`
flag (default), but no anchor-based popover mode — unlike most
other dialogs it doesn't integrate with `anchor_to=`. With no
`position`, the dialog centers on its parent.

The dialog is built with `Dialog`'s `content_builder` /
`footer_builder` hooks rather than the higher-level `buttons=`
shape. Two consequences follow from that, and both differ from
`MessageDialog` / `FormDialog`:

- **No Enter binding.** The OK button is styled `accent=PRIMARY`
  but is **not** registered as the Dialog's default button, so
  pressing Enter does nothing on the dialog level. (Enter does
  still commit values inside the spinboxes — that's a Spinbox
  binding, not a dialog binding.)
- **Escape destroys without invoking the cancel callback.** Since
  no button has `role="cancel"`, Escape goes through the Dialog's
  fallback path and just calls `toplevel.destroy()`. `.result`
  ends up as `None` either way (it's reset to `None` at the start
  of `show()`), but `_on_cancel` itself is skipped — if you need a
  hook on dismissal, bind `<<DialogResult>>` instead of patching
  the cancel button.

The window-close (`X`) button behaves identically to Escape.

### The three tabs

The chooser sits in a notebook with three tabs:

- **Advanced** — a 530 × 240 pixel hue/saturation spectrum with a
  luminance scale below it. Clicking or dragging on the spectrum
  selects hue + saturation; clicking on the luminance bar adjusts
  brightness.
- **Themed** — a swatch grid built from the active theme's accent
  tokens (`primary`, `secondary`, `success`, `info`, `warning`,
  `danger`, `light`, `dark`) plus five lightness shades of each.
- **Standard** — a fixed eight-color palette (`#FF0000`, `#FFC000`,
  `#FFFF00`, `#00B050`, `#0070C0`, `#7030A0`, `#FFFFFF`,
  `#000000`) with the same five shades.

The themed tab reflects the **current theme at construction time**;
re-open the dialog after a theme switch to see the new palette.

### Synchronized RGB / HSL / Hex inputs

Below the tab area sit two columns of spinboxes (HSL on the left,
RGB on the right) and a hex `Entry`. All three representations are
kept in sync: typing a new red value updates HSL and Hex, dragging
the spectrum updates RGB and Hex, and so on. The spinbox commit
events (`<<Increment>>`, `<<Decrement>>`, `<Return>`, `<KP_Enter>`)
push changes back into the model — out-of-range entries are
caught by the spinbox `validate()` call and simply not propagated.

### Color dropper (Windows/Linux only)

When the runtime windowing system is **not** `aqua`, the footer
shows a small pen-glyph (`✛`) button at the left. Clicking it
opens a [`ColorDropperDialog`](colordropper.md) that captures a
single pixel anywhere on the screen and feeds the sampled hex back
into the chooser. On macOS the dropper button is omitted entirely
(the underlying screen-grab implementation isn't available on
aqua) — design any cross-platform UI assuming the dropper might
not be present.

---

## Events

| Hook | Fires |
|---|---|
| `<<DialogResult>>` | Once per `show()` call, after the dialog closes. Payload is `{"result": ColorChoice \| None, "confirmed": bool}`. The event is generated on `master` when one was passed; otherwise on the dialog's own toplevel. |
| `on_dialog_result(cb)` | Helper that binds `<<DialogResult>>` and calls `cb(event.data)` — the **payload dict**, not the unwrapped color. Returns the bind id (or `None` if no event target exists yet — see gotcha below). |
| `off_dialog_result(funcid)` | Unbinds a callback registered via `on_dialog_result`. |

```python
dlg = ttk.ColorChooserDialog(master=app, initial_color="#3b82f6")

def on_color(payload):
    if payload["confirmed"]:
        apply_color(payload["result"].hex)

dlg.on_dialog_result(on_color)
dlg.show()
```

`confirmed=True` only when the user clicked **OK**. Cancel, Escape,
and window-close paths all fire with `confirmed=False` and
`result=None`. The dialog guarantees the event fires **exactly
once** per `show()` — there's a fallback at the end of `show()` that
emits the event itself if neither OK nor Cancel ran (e.g. when the
user pressed Escape and Dialog's own destroy path took over).

!!! note "Register `on_dialog_result` after passing `master=`"
    `on_dialog_result` binds against `self._master or
    self._dialog.toplevel`. If you didn't pass `master=` and call
    `on_dialog_result` *before* `show()`, the toplevel doesn't
    exist yet — the helper returns `None` silently and your
    callback is never wired up. The same gotcha exists on
    `DateDialog` and `QueryDialog`. Either pass `master=app` (or
    any parent widget) at construction, or call
    `on_dialog_result` after `show()` has built the toplevel.

---

## UX guidance

- **Set `initial_color` to whatever the user is already looking
  at.** A "change accent" dialog should open on the current accent;
  a "label color" prompt should open on the label's existing color.
  Letting it default to the theme background is fine for one-off
  pickers but feels disconnected when the user is editing
  something with a known starting color.
- **Read the representation you actually need.** `.result.hex`
  is the most portable form (CSS, image libraries, settings
  files); `.result.rgb` skips the parse if you're handing it
  straight to a graphics API; `.result.hsl` is the right one for
  building shade/tint variations programmatically.
- **Don't gate critical functionality on the eyedropper.** The
  dropper is hidden on macOS, and "click outside the app to
  capture a pixel" is also a heavyweight interaction on
  Windows/Linux. Treat it as a convenience for
  user-can-already-see-the-color cases, not a primary input
  pathway.
- **For frequent recolor flows, don't open this every time.** A
  toolbar with the last few used colors plus a "more…" button that
  opens the dialog is a better fit than re-opening the modal on
  every adjustment.
- **Translate the catalog keys** before shipping a localized
  build. A vanilla en_US locale will display the literal
  `color.advanced` / `color.hue:` strings — the keys exist but
  ttkbootstrap's bundled catalogs may not yet cover them all.

---

## When should I use ColorChooser?

Use `ColorChooserDialog` when:

- the user picks a color **occasionally** and an explicit
  commit/cancel choice is appropriate.
- you want a single dialog that exposes spectrum, themed swatches,
  standard swatches, and direct numeric entry — without you
  building any of those UIs.
- the result is a **persistent setting** (saved theme color, label
  color, default tag color), not a continuously-varying value.

Prefer a different control when:

- you only need to **sample a pixel from the screen** → use
  [`ColorDropper`](colordropper.md) directly. The chooser already
  embeds it as a convenience, but if pixel sampling is the whole
  task, the chooser is overkill.
- the user **changes color frequently and needs immediate
  feedback** (paint apps, live theme editors, drawing tools) → put
  swatches inline in the toolbar; only fall back to this dialog
  for the "more colors…" case.
- you need the **OS-native color picker** for platform-consistency
  reasons → use `tkinter.colorchooser.askcolor()` from the stdlib;
  it returns a `(rgb_tuple, hex_string)` pair instead of a
  `ColorChoice`, but it integrates with the system dialog.
- the dialog needs a **custom footer** (extra buttons, embedded
  widgets beside OK/Cancel) → drop down to [`Dialog`](dialog.md)
  with a `content_builder` that builds a `ColorChooser` inline.

---

## Additional resources

**Related widgets**

- [`ColorDropper`](colordropper.md) — modal pixel-sampler used as
  this dialog's eyedropper button; available standalone for
  capture-only flows.
- [`Dialog`](dialog.md) — the generic builder underneath; reach
  for it directly when the chooser's fixed footer doesn't fit.
- [`FontDialog`](fontdialog.md) — the same "modal style picker"
  pattern for font selection.
- [`MessageBox`](messagebox.md) — message + button-row modal for
  simple confirmations.

**Framework concepts**

- [Windows](../../platform/windows.md)
- [Localization](../../capabilities/localization.md)
- [Colors and tokens](../../design-system/colors.md)

**API reference**

- **API reference:** [`ttkbootstrap.ColorChooserDialog`](../../reference/dialogs/ColorChooserDialog.md)
- **Related guides:** Dialogs, Theming, Localization
