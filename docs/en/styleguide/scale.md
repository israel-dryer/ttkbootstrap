# Scale

This widget style features a thin gray trough with a round slider handle that is 
**primary** color by default or the [selected color](index.md#colors). The 
slider handle lightens on _hover_ and darkens when _pressed_. 

This widget supports a special style for 
[disabled state](#other-scale-styles).

![scale](../assets/widget-styles/scale.gif)

```python
# default Scale style
Scale()

# info colored label style
Scale(bootstyle="info")
```

## Other scale styles

#### Disabled scale
This style _cannot be applied via keywords_; it is configured through widget 
settings.

```python
# create the scale in a disabled state
Scale(state="disabled")

# disable a scale after creation
scale = Scale()
scale.configure(state="disabled")
```