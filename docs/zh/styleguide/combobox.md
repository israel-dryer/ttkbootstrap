# Combobox

This widget style features a input box with a styled border and arrow. The 
border color is muted by default and changes to **primary** or the 
[selected color](index.md#colors) on _hover_. The border increases in thickness on 
_focus_. The arrow color changes to the default or [selected color](index.md#colors) 
on _hover_ or on _focus_.

This widget also supports special styles for [disabled state](#disabled-combobox), 
[readonly state](#readonly-combobox), and [invalid state](#invalid-combobox).

![combobox](../assets/widget-styles/combos.gif)

```python
# default combobox style
Combobox()

# danger colored combobox style
Combobox(bootstyle="danger")
```

## Other combobox styles

#### Disabled combobox

This style _cannot be applied via keywords_; it is configured through widget 
settings.

```python
# create the combobox in a disabled state
Combobox(state="disabled")

# disable a combobox after creation
cb = Combobox()
cb.configure(state="disabled")
```

#### Readonly combobox

This style _cannot be applied via keywords_; it is configured through widget 
settings.


```python
# create the combobox in a readonly state
Combobox(state="readonly")

# set the combobox readonly state after creation
cb = Combobox()
cb.configure(state="readonly")
```

#### Invalid combobox

This style _cannot be applied via keywords_, but rather is the result of a 
validation process implemented on the widget. In the **Cookbook** you will find 
an example of [how to apply validation](../cookbook/validate-user-input.md) to an 
`Entry` based widget.
