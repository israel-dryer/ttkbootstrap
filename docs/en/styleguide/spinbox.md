# Spinbox

This widget style features a input box with a styled border and arrows. The 
border color is muted by default and changes to **primary** or the 
[selected color](index.md#colors) on _hover_. The border increases in thickness on 
_focus_. The arrow color changes to the default or [selected color](index.md#colors) 
on _hover_ or on _focus_.

This widget also supports special styles for [disabled state](#disabled-spinbox), 
[readonly state](#readonly-spinbox), and [invalid state](#invalid-combobox).

![spinbox](../assets/widget-styles/spinbox.gif)

```python
# default spinbox style
Spinbox()

# danger colored spinbox style
Spinbox(bootstyle="danger")
```

## Other styles

#### Disabled spinbox

This widget supports a style reserved for the **disabled** state, which you 
can see in the exhibit above. This style _cannot be applied via keywords_. To 
apply the disabled style:

```python
# create the widget in a disabled state
Spinbox(state="disabled")

# disable the widget after creation
e = Spinbox()
e.configure(state="disabled")
```

#### Readonly spinbox

This widget supports a style reserved for the **readonly** state, which you 
can see in the exhibit above. This style _cannot be applied via keywords_.  To 
apply the readonly style:

```python
# create the widget in a readonly state
Spinbox(state="readonly")

# set the widget readonly state after creation
e = Spinbox()
e.configure(state="readonly")
```

#### Invalid spinbox

This style _cannot be applied via keywords_, but rather is the result of a 
validation process implemented on the widget. In the **Cookbook** you will find 
an example of [how to apply validation](../cookbook/validate-user-input.md) to an 
`Entry` based widget.
