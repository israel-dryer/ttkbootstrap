![](https://img.shields.io/github/release/israel-dryer/ttkbootstrap.svg)
[![Downloads](https://pepy.tech/badge/ttkbootstrap)](https://pepy.tech/project/ttkbootstrap)
[![Downloads](https://pepy.tech/badge/ttkbootstrap/month)](https://pepy.tech/project/ttkbootstrap)
![](https://img.shields.io/github/issues/israel-dryer/ttkbootstrap.svg)
![](https://img.shields.io/github/issues-closed/israel-dryer/ttkbootstrap.svg)
![](https://img.shields.io/github/license/israel-dryer/ttkbootstrap.svg)
![](https://img.shields.io/github/stars/israel-dryer/ttkbootstrap.svg)
![](https://img.shields.io/github/forks/israel-dryer/ttkbootstrap.svg)

# ttkbootstrap
English | [中文](README_zh.md)

A supercharged theme extension for tkinter that enables on-demand modern flat style themes inspired by Bootstrap. 

👀 Check out the [documentation](https://ttkbootstrap.readthedocs.io/en/latest/).


> **1.0+ is a complete rebuild of the library.** If you are using [version 0.5](https://github.com/israel-dryer/ttkbootstrap/tree/version-0.5)
   you may run into issues trying to import themes with the themes.json as this 
   has been removed from 1.0. You can now import and save themes directly using 
   the ttkcreator.

![](https://raw.githubusercontent.com/israel-dryer/ttkbootstrap/master/docs/assets/themes/themes.gif)

## Features

✔️ [**Built-in Themes**](https://ttkbootstrap.readthedocs.io/en/latest/themes/)   
Over a dozen curated dark and light themes.

✔️ [**Pre-defined Styles:**](https://ttkbootstrap.readthedocs.io/en/latest/styleguide/)  
Loads of beautiful pre-defined widget styles such as **outline** and **round toggle** buttons.

✔️ [**Simple keyword API:**](https://ttkbootstrap.readthedocs.io/en/latest/gettingstarted/tutorial/#use-themed-widgets)  
Apply colors and types using simple keywords such as **primary** and **striped** instead of the legacy approach of **primary.Striped.Horizontal.TProgressbar**. If you've used Bootstrap for web development, you are already familiar with this approach using css classes.

✔️ [**Lots of new Widgets:**](https://ttkbootstrap.readthedocs.io/en/latest/api/widgets/dateentry/)  
ttkbootstrap comes with several new beautifully designed widgets such as **Meter**, **DateEntry**, and **Floodgauge**. Additionally, **dialogs** are now themed and fully customizable.

✔️ [**Built-in Theme Creator:**](https://ttkbootstrap.readthedocs.io/en/latest/themes/themecreator/)  
Want to create your own theme? Easy! ttkboostrap includes a built-in **theme creator** that enables you to easily build, load, expore, and apply your own custom themes.

## Installation

```python
python -m pip install ttkbootstrap
```

## Simple Usage
Instead of using long, complicated ttk style classes, you can use simple keywords with the "bootstyle" parameter.

```python
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

root = ttk.Window(themename="superhero")

b1 = ttk.Button(root, text="Submit", bootstyle="success")
b1.pack(side=LEFT, padx=5, pady=10)

b2 = ttk.Button(root, text="Submit", bootstyle="info-outline")
b2.pack(side=LEFT, padx=5, pady=10)

root.mainloop()
```

The new keyword API is very flexible. The following examples all produce the same result:
- `bootstyle="info-outline"`
- `bootstyle="info outline"`
- `bootstyle=("info", "outline")`
- `bootstyle=(INFO, OUTLINE)`

## Links
- **Documentation:** https://ttkbootstrap.readthedocs.io/en/latest/  
- **GitHub:** https://github.com/israel-dryer/ttkbootstrap
