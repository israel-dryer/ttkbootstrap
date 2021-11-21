# Home

**ttkbootstrap** is a collection of modern, flat themes inspired by 
[Bootstrap](https://getbootstrap.com/) for tkinter/ttk. Each widget 
includes pre-defined widget styles that are easily accessible with 
easy to remember keywords that change the widget color and form.

![themes](./assets/themes/themes.gif)

## Installation

Installing ttkbootstrap is easy!

### PyPI

The best method for installing ttkbootstrap is from PyPI. 

```bash
python -m pip install ttkbootstrap
```

This also installed the required dependency `pillow`, which is used for image
processing.

### Source

You may also install directly from the GitHub repository.

```bash
python -m pip install git+https://github.com/israel-dryer/ttkbootstrap
```

!!! warning "Installing from GitHub"
    GitHub contains the most recent development version of this project, but 
    it may also contain potential bugs and other issues that you would not want 
    in a production project.

## Overview

### Why does this project exist?

The purpose of this project is create a set of beautifully designed and easy to 
apply styles for your tkinter applications. Tkinter/ttk can be very time-consuming to 
style if you are just a casual user. This project takes the pain out of getting 
a modern look and feel so that you can focus on _designing your application_. 

This project was created to harness the power of ttk’s (and thus Python’s) 
existing built-in theme engine to create modern and professional-looking user 
interfaces which are inspired by, and in many cases, whole-sale rip-off’s of the 
themes found on [Bootswatch](https://bootswatch.com/). 

### A bootstrap approach to style

Many people are familiar with bootstrap for web developement, as it comes 
pre-packaged with built-in css style classes that provide a professional and 
consistent api for quick development. I took a similar approach with this 
project by pre-defining styles for nearly all ttk widgets. 

Instead of having to subclass a button style using something that looks like 
**danger.Outline.TButton**, you can pass in the keywords **danger-outline** 
to create a red colored outline `Button`. Or, use **info** to create a blue 
colored solid `Button`. Or, use **success-striped** to create a green striped 
`Progressbar`. This simple keyword  based style api makes working with tkinter 
SO MUCH EASIER! 

### What about the old tkinter widgets?

Some of the ttk widgets utilize existing tkinter widgets. For example: there is 
a tkinter popdown list in the `Combobox` and a legacy tkinter widget inside 
the `OptionMenu`. To make sure these widgets didn’t stick out like a sore 
thumb, I have applied styling to these widgets as well, in order to make sure
the look and feel is consistent as much as possible. 

## Tutorial

**ttkbootstrap** turns style keywords into a ttk style that is created 
_on demand_ as needed and then applies that style to your widget.

### Basic usage

```python
import tkinter as tk
import ttkbootstrap as ttk

root = tk.Tk()
style = ttk.Style()  # use default style 'flatly'

b1 = ttk.Button(root, text="Button 1", bootstyle="success")
b1.pack(side=tk.LEFT, padx=5, pady=10)

b2 = ttk.Button(root, text="Button 2", bootstyle="info-outline")
b2.pack(side=tk.LEFT, padx=5, pady=10)

root.mainloop()
```

This results in the window below:

![simple usage window](./assets/tutorial/simple-usage.png)

### Choose a theme

By default, the **flatly** theme is applied to the application. If you prefer
to instantiate the application with another theme, you can pass the name of the
theme into the `Style` funtion.

```python
>>> style = Style(theme="darkly")
```

If the application has already been created, you can change the theme with the 
`theme_use` method:

```python
>>> style.theme_use("superhero")
```

You can see screenshots of all built-in themes [here](themes.md).

To see a list of all available themes:

```python
>>> style = Style()
>>> style.theme_name()
['cosmo', 'flatly', 'litera', 'minty', 'lumen', 'sandstone', 'yeti', 'pulse', 
'united', 'journal', 'darkly', 'superhero', 'solar', 'cyborg']
```

!!! warning "Style is not a class!"
    In ttkbootstrap, `Style` is _not_ a class as it is in `ttk` but rather 
    a function that  returns a singleton instance of the `StyleManager` class, 
    which itself inherits from the `ttk.Style` class. `StyleManger` is not 
    intended to be inherited.

### Use themed widgets

**ttkbootstrap** includes many [pre-defined widget styles](styleguide.md) that you 
can apply with the `bootstyle` parameter. All widgets can be colored using one of 
several color keywords that are defined for each theme.

- primary
- secondary
- success
- info
- warning
- danger
- light
- dark

These color keywords produce the following look and feel on a `ttk.Button`

```python
import tkinter as tk
import ttkbootstrap as ttk

root = tk.Tk()
style = ttk.Style()

for color in style.colors:
    b = ttk.Button(root, text=color, bootstyle=color)
    b.pack(side=tk.LEFT, padx=5, pady=5)

root.mainloop()
```

![button colors](./assets/tutorial/button-colors.png)

Consider the following example, which also shows the _outline_ style that is 
available for `Button`, and `Menubutton`

```python
import tkinter as tk
import ttkbootstrap as ttk

root = tk.Tk()
style = ttk.Style()  # use default style 'flatly'

b1 = ttk.Button(root, text="Solid Button", bootstyle="success")
b1.pack(side=tk.LEFT, padx=5, pady=10)

b2 = ttk.Button(root, text="Outline Button", bootstyle="success-outline")
b2.pack(side=tk.LEFT, padx=5, pady=10)

root.mainloop()
```
![button styles](./assets/tutorial/solid-outline-button-styles.png)

### Use themed colors

When you call the `Style` method a `StyleManager` object is returned. This
object is what you use to managed the styles and themes of the application.
This object also has access to the color palette of the theme currently being
used via a `Color` object, which can come in handy when you want to use those 
colors for something.

The colors can be access via dot notation, or use the `get` method.

```python
# create a style manager object
style = Style()

# dot notation
style.colors.primary

# get method
style.colors.get('border')
```

The `Color` object is an iterator, so you can iterate over the bootstyle colors
such as 'primary', 'secondary', etc...

```python
for color_name in style.colors:
    color_value = style.colors.get(color_name)
```

If for some reason you want to iterate over _all_ theme colors, including
'border', 'bg', 'fg', etc..., you can use the `label_iter` method:

```python
for color_name in style.colors.label_iter():
    color_value = style.colors.get(color_name)
```
