# Checkbutton

This widget features a variety of checkbutton style types that are **primary**
colored by default or the [selected color](index.md#colors).

This widget supports a special style for 
[disabled state](#other-checkbutton-styles).

## Checkbutton (default)

The default style features a square checkbox and label. The checkbox has a
muted color outline when not selected, and a filled square with checkmark when
selected.

![checkbutton](../assets/widget-styles/checkbuttons.png)

```python
# default checkbutton style
Checkbutton()

# success checkbutton style
Checkbutton(bootstyle="success")
```

## Toolbutton

This style features a solid rectangular button that toggles between an _off_ 
and _on_ color. The background is a muted gray when _off_ and a default
or [selected color](index.md#colors) when _on_ or _active_.

![solid toolbuttons](../assets/widget-styles/solid-toolbuttons.gif)

```python
# default toolbutton style
Checkbutton(bootstyle="toolbutton")

# success toolbutton style
Checkbutton(bootstyle="success-toolbutton")
```

## Outline toolbutton

This style features a rectangular button that toggles between a styled 
**outline** when _off_ and a **solid** background when _on_ or 
_active_.

![outline toolbuttons](../assets/widget-styles/outline-toolbuttons.gif)

```python
# default outline toolbutton style
Checkbutton(bootstyle="outline-toolbutton")

# success outline toolbutton style
Checkbutton(bootstyle="success-outline-toolbutton")
```

## Round toggle button

This style features a rounded button with a **round** indicator that changes
color and position when toggled _off_ and _on_. The button is a muted outline
with a muted color indicator when _off_. The button is filled with the default
or [selected color](index.md#colors) with an accented indicator when _on_.

![round toggles](../assets/widget-styles/round-toggles.gif)

```python
# default round toggle style
Checkbutton(bootstyle="round-toggle")

# success round toggle style
Checkbutton(bootstyle="success-round-toggle")
```

## Square toggle button

This style features a squared button with a **square** indicator that changes
color and position when toggled _off_ and _on_. The button is a muted outline
with a muted color indicator when _off_. The button is filled with the default
or [selected color](index.md#colors) with an accented indicator when _on_.

![square toggles](../assets/widget-styles/square-toggles.gif)

```python
# default square toggle style
Checkbutton(bootstyle="square-toggle")

# success square toggle style
Checkbutton(bootstyle="success-square-toggle")
```

## Other checkbutton styles

#### Disabled checkbutton
This style _cannot be applied via keywords_; it is configured through widget 
settings.

```python
# create the checkbutton in a disabled state
Checkbutton(state="disabled")

# disable a checkbutton after creation
cb = Checkbutton()
cb.configure(state="disabled")
```