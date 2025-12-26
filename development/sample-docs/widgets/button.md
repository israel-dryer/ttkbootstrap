---
title: Button
---

# Button

A widget that issues a command when pressed.

---

## Overview

You create a button by providing text and a command. The command is a function that is called when the user clicks the button. The label describes the button's action and can also be accompanied or replaced by an icon.

```python
import ttkbootstrap as ttk

ttk.Button(text='Submit', command=submit)
```

Accompanied by an icon:

```python
ttk.Button(text='Submit', icon='check', command=submit)
```

Or as icon only:

```python
ttk.Button(icon='check', icon_only=True, command=submit)
```

---

## Basic usage

```python
import ttkbootstrap as ttk

app = ttk.App()


def on_save():
    print("Saved!")


ttk.Button(app, text="Save", command=on_save).pack(padx=20, pady=20)

app.mainloop()
```

---

## Styling buttons

You can customize the button's appearance by using **semantic color** and **variant** tokens.
Variants describe the button’s visual weight and interaction style, not its meaning.

The supported variants for the button are solid (default), outline, ghost, link, and text:

```python
ttk.Button(text='Submit')
ttk.Button(text='Submit', bootstyle='outline')
ttk.Button(text='Submit', bootstyle='ghost')
ttk.Button(text='Submit', bootstyle='link')
ttk.Button(text='Submit', bootstyle='text')
```

**Color** and **variant** tokens can be combined to create the desired result (`color-variant`):

```python
ttk.Button(text='Submit', bootstyle='primary')
ttk.Button(text='Submit', bootstyle='secondary-outline')
ttk.Button(text='Submit', bootstyle='info-link')
```

---

## Using icons

Buttons support [Bootstrap Icons](https://icons.getbootstrap.com/) with the `icon` and `icon_only` options.

For standard use, add the icon name:

```python
ttk.Button(icon='plus-lg', text='Add')
```

Or set the `icon_only` flag if you do not want to show a label. This removes the additional padding reserved for text and
increases the size of the icon slightly.

```python
ttk.Button(icon='plus-lg', icon_only=True)
```

See the article about [Customizing your Icons](#) for more icon features and customization options.

---

## Disabled state

The button can be disabled by setting the disabled state in the constructor:

```python
ttk.Button(text='Submit', state='disabled')
```

Or at runtime:

```python
btn.configure(state='disabled')
```

You can also remove the disabled state:

```python
btn.configure(state='normal')
```

!!! tip "Shortcut"
    You can also use item assignment: `btn["state"] = "disabled"` or `"normal"`.

---

## Localization

Localization behavior is controlled by the **global application settings**.

By default, widgets use `localize="auto"`. In this mode, the `text` value is treated as a localization
key **when a matching translation exists**. If the key is not found in the active message catalog, the
widget falls back to using the value as **plain text**. You can override this behavior per widget if needed.

Use the global localization settings:

```python
ttk.Button(text="button.ok")
```

Enable localization explicitly:
```python
ttk.Button(text="button.ok", localize=True)
```

Disable localization explicitly (always treat the text as a literal):
```python
ttk.Button(text="OK", localize=False)
```

!!! tip "Literal text is safe"
    With `localize="auto"`, you can pass either a localization key or a literal label.
    If no translation is found, the label is shown as-is.


---

## Reactive text

You can bind the label text to a signal (so the button text updates automatically).

```python
import ttkbootstrap as ttk

app = ttk.App()

label = ttk.Signal("Start")

btn = ttk.Button(app, bootstyle="primary", textsignal=label)
btn.pack(padx=20, pady=20)

label.set("Stop")

app.mainloop()
```