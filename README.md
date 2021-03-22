# Izzy-Themes-TTK  (IN PROGRESS)
A collection of modern themes for Tkinter TTK built using standard, cross-platform themes ('clam', 'alt', 'classic', 'default'). 
Most of these themes are adapted and or/inspired from the open source bootstrap themes published on https://bootswatch.com/  

This is a work-in-progress. Soon this will be published as a Python package. But, until then, you can clone the repo and use per below.

## Basic Usage
```python
from izzythemes import Style, ttk

style = Style()
style.theme_use('flatly')
root = style.master

# create widget with primary colors
ttk.Label(root, text='Hello world').pack()

# create widget with other colors
ttk.Label(root, text='Hello world', style='danger.TLabel').pack()
```
## Applying Styles
By default, the colors will be primary. Any other themed colors can be used by applying the color prefix to the ttk widget class.
  
For example: `style = 'danger.TLabel'` or `style = 'success.TButton'` or `style = 'info.Outline.TButton'`

### Color prefixes
- primary <i>(default)</i>
- secondary
- success
- info
- warning
- danger

### Defined ttk widget classes
- TButton
- Outline.TButton
- TSpinbox
- Horizontal.TScale
- Vertical.TScale
- Horizontal.TScrollbar
- Vertical.TScrollbar
- TCombobox
- TFrame
- TCheckbutton
- TEntry
- TLabel
- TLabelframe
- TNotebook
- TMenubutton
- Outline.TMenubutton
- Horizontal.TProgressbar
- Vertical.TProgressbar
- TRadiobutton
- Treeview

## Light Themes
![](examples/light_themes.png)
  
## Dark Themes
![](examples/dark_themes.png)


