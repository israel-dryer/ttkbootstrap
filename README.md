# ttkbootstrap
A collection of modern themes for Tkinter TTK built using standard, cross-platform themes ('clam', 'alt', 'classic', 'default'). 
Most of these themes are adapted and or/inspired from the open source bootstrap themes published on https://bootswatch.com/  

## Installation
https://pypi.org/project/ttkbootstrap/
```python
pip install ttkbootstrap
```

## Demonstration
You check out the examples below in a live demonstration by executing the following code in the python interpreter
```python
>> from ttkbootstrap import Demo
>> Demo()
```

## Basic Usage

```python
from ttkbootstrap import BootStyle, ttk

style = BootStyle()
style.theme_use('flatly')
root = style.master

# create widget with primary colors
ttk.Label(root, text='Hello world').pack()

# create widget with other colors
ttk.Label(root, text='Hello world', style='danger.TLabel').pack()

# run the window
root.mainloop()
```
## Applying Styles
By default, the primary color for the theme will be used on widgets (See images below for examples of theme color options). All other themed colors can be used by applying the color prefix to the ttk widget class.
  
```python
ttk.Label(root, text='Hello World', style='info.TLabel')
ttk.Button(root, text='Hello World', style='info.TButton')
ttk.Button(root, text='Hello World', style='warning.Outline.TButton')
ttk.Radiobutton(root, text='Hello World', style='danger.TRadiobutton')
```

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

### Exceptions
- The **Scale** widget is built with an image set in the primary theme color; this cannot be changed via styles.
- The **Checkbutton** and **Radiobutton** colors are only changeable on Linux and MacOS. Windows uses the built-in "xpnative" themed elements to build the widgets.

## Light Themes
<img src="https://raw.githubusercontent.com/israel-dryer/Izzy-Themes-TTK/master/examples/cosmo.png" width="45%"/> <img src="https://raw.githubusercontent.com/israel-dryer/Izzy-Themes-TTK/master/examples/flatly.png" width="45%"/>  
<img src="https://raw.githubusercontent.com/israel-dryer/Izzy-Themes-TTK/master/examples/journal.png" width="45%"/> <img src="https://raw.githubusercontent.com/israel-dryer/Izzy-Themes-TTK/master/examples/litera.png" width="45%"/>  
<img src="https://raw.githubusercontent.com/israel-dryer/Izzy-Themes-TTK/master/examples/lumen.png" width="45%"/> <img src="https://raw.githubusercontent.com/israel-dryer/Izzy-Themes-TTK/master/examples/minty.png" width="45%"/>  
<img src="https://raw.githubusercontent.com/israel-dryer/Izzy-Themes-TTK/master/examples/pulse.png" width="45%"/> <img src="https://raw.githubusercontent.com/israel-dryer/Izzy-Themes-TTK/master/examples/sandstone.png" width="45%"/>  
<img src="https://raw.githubusercontent.com/israel-dryer/Izzy-Themes-TTK/master/examples/united.png" width="45%"/> <img src="https://raw.githubusercontent.com/israel-dryer/Izzy-Themes-TTK/master/examples/yeti.png" width="45%"/>  
  
## Dark Themes
<img src="https://raw.githubusercontent.com/israel-dryer/Izzy-Themes-TTK/master/examples/darkly.png" width="45%"/> <img src="https://raw.githubusercontent.com/israel-dryer/Izzy-Themes-TTK/master/examples/cyborg.png" width="45%"/>
<img src="https://raw.githubusercontent.com/israel-dryer/Izzy-Themes-TTK/master/examples/superhero.png" width="45%"/> <img src="https://raw.githubusercontent.com/israel-dryer/Izzy-Themes-TTK/master/examples/solar.png" width="45%"/>  


