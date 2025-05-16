# Button

This widget features a variety of button style types that have a **primary**
color by default, or the [selected color](index.md#colors).

This widget supports a special style for [disabled state](#other-button-styles).

## Solid button (default)

The default style features a solid background that lightens on _hover_ and 
darkens when _pressed_. A dashed ring appears inside the button when the widget
has focus.

![solid button](../assets/widget-styles/solid-buttons.gif)

```python
# default style
Button()

# success style
Button(bootstyle="success")
```

## Outline button

This style features a thin styled outline. When _pressed_ or on _hover_, the
button changes to a solid color similar to the default button style. A dashed
ring appears inside the button when the widget has focus.

![outline buttons](../assets/widget-styles/outline-buttons.gif)

```python
# default outline style
Button(bootstyle="outline")

# success outline style
Button(bootstyle="success-outline")
```

## Link button

This style features a button with the appearance of a label. The text color changes
to **info** on _hover_ or when _pressed_ to simulate the effect you would expect on
an HTML hyperlink. There is a slight shift-relief when the button is pressed that 
gives the appearance of movement. A dashed ring appears inside the button when the
widget has focus.

![link buttons](../assets/widget-styles/link-buttons.gif)

```python
# default link style
Button(bootstyle="link")

# success link style
Button(bootstyle="success-link")
```

## Other button styles

#### Disabled button
This style _cannot be applied via keywords_; it is configured through widget 
settings.

```python
# create the button in a disabled state
Button(state="disabled")

# disable a button after creation
b = Button()
b.configure(state="disabled")
```