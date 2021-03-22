# Izzy-Themes-TTK  (IN PROGRESS)
A collection of modern themes for Tkinter TTK built using only built-in standard themes ('clam', 'alt', 'classic', 'default').

## Light Themes
![](examples/light_themes.png)
  
## Dark Themes
![](examples/dark_themes.png)

## Basic Usage
```python
from izzythemes import Style, ttk
style = Style()
style.theme_use('flatly')
```

Add styled widgets to your window with ttk. Use the `style` argument to set other available colors.
```
root = style.master

# primary colors
ttk.Label(root, text='Hello world').pack()

# other colors
ttk.Label(root, text='Hello world', style='danger.TLabel').pack()
```
