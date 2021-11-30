# Label

This widget features two style types that can both be customized using any of
the [available colors](index.md#colors).

## Default label

The default style features a default theme defined foreground and background
color. The foreground can be changed using a [selected color](index.md#colors).

![normal label](../assets/widget-styles/label.png)

```python
# default label style
Label()

# danger colored label style
Label(bootstyle="danger")
```

## Inverse label

This style features a label with colors that are inverted versions of the default
colors. The [selected color](index.md#colors) changes the background color instead of the
foreground color. 

This is especially useful when you are adding labels to a styled `Frame`, or you 
want to add a [label heading](../gallery/mediaplayer.md) that does not have a default 
background color.

![inverse label](../assets/widget-styles/inverse-label.png)

```python
# default inverse label style
Label(bootstyle="inverse")

# danger colored inverse label style
Label(bootstyle="inverse-danger")
```
