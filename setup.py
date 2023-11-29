import setuptools

long_description = """
![](https://img.shields.io/github/release/israel-dryer/ttkbootstrap.svg)
[![Downloads](https://pepy.tech/badge/ttkbootstrap)](https://pepy.tech/project/ttkbootstrap)
[![Downloads](https://pepy.tech/badge/ttkbootstrap/month)](https://pepy.tech/project/ttkbootstrap)
![](https://img.shields.io/github/issues/israel-dryer/ttkbootstrap.svg)
![](https://img.shields.io/github/issues-closed/israel-dryer/ttkbootstrap.svg)
![](https://img.shields.io/github/license/israel-dryer/ttkbootstrap.svg)
![](https://img.shields.io/github/stars/israel-dryer/ttkbootstrap.svg)
![](https://img.shields.io/github/forks/israel-dryer/ttkbootstrap.svg)

A supercharged theme extension for tkinter that enables on-demand modern flat style themes inspired by Bootstrap. 

👀 Check out the [documentation](https://ttkbootstrap.readthedocs.io/en/latest/).

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
"""

setuptools.setup(
    name="ttkbootstrap",
    version="1.10.1",
    author="Israel Dryer",
    author_email="israel.dryer@gmail.com",
    description="A supercharged theme extension for tkinter that enables on-demand modern flat style themes inspired by Bootstrap.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    url="https://github.com/israel-dryer/ttkbootstrap",
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    install_requires=["pillow==10.0.1"],
    python_requires=">=3.7",
    # include_package_data=True,
    # package_data={'ttkbootstrap': ['localization/msgs/*.msg']}
)
