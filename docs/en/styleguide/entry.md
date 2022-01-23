# Entry

This widget style features a input box with a styled border. The border color 
is muted by default and changes to **primary** or the 
[selected color](index.md#colors) on _hover_. The border increases in thickness 
on _focus_. 

This widget also supports special styles for [disabled state](#disabled-entry), 
[readonly state](#readonly-entry), and [invalid state](#invalid-entry).

![entry](../assets/widget-styles/entries.gif)

```python
# default entry style
Entry()

# danger colored entry style
Entry(bootstyle="danger")
```

## Other entry styles

#### Disabled entry

This style _cannot be applied via keywords_; it is configured through widget 
settings.

```python
# create the widget in a disabled state
Entry(state="disabled")

# disable the widget after creation
e = Entry()
e.configure(state="disabled")
```

#### Readonly entry

This style _cannot be applied via keywords_; it is configured through widget 
settings.

```python
# create the widget in a readonly state
Entry(state="readonly")

# set the widget readonly state after creation
e = Entry()
e.configure(state="readonly")
```

#### Invalid entry

This style _cannot be applied via keywords_, but rather is the result of a 
validation process implemented on the widget. In the **Cookbook** you will find 
an example of [how to apply validation](../cookbook/validate-user-input.md) to an 
`Entry` based widget.
