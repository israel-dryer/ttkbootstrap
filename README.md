# ttkbootstrap
A collection of modern flat themes inspired by Bootstrap.

Check out the [documentation](https://ttkbootstrap.readthedocs.io/en/latest/) _under development_.

![](https://github.com/israel-dryer/ttkbootstrap/blob/master/docs/assets/themes/themes.gif)

## Installation

Version 1.0 is currently unpublished; for the moment you must install from source.
```shell
python -m pip install git+https://github.com/israel-dryer/ttkbootstrap
```

[Version 0.5](https://github.com/israel-dryer/ttkbootstrap/tree/0.5) is currently on PyPI.
```python
pip install ttkbootstrap
```

## Simple Usage
The new API adds style keywords. Instead of using `style="info.Outline.TButton"`, 
you can use `info-outline` to create an info colored outline button.

```python
import tkinter as tk
import ttkbootstrap as ttk

root = tk.Tk()
style = ttk.Style()

b1 = ttk.Button(root, text="Submit", bootstyle='success')
b1.pack(side=tk.LEFT, padx=5, pady=10)

b2 = ttk.Button(root, text="Submit", bootstyle='info-outline')
b2.pack(side=tk.LEFT, padx=5, pady=10)

root.mainloop()
```

The new keyword API is very flexible. The following examples all produce the same result:
- `bootstyle="info-outline"`
- `bootstyle="info outline"`
- `bootstyle=("info", "outline")`
