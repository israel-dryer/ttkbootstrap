# ttkbootstrap
A collection of modern flat themes inspired by Bootstrap.

## How to install (0.5 - stable)
```python
pip install ttkbootstrap
```

## Examples

**light theme example (1.0 - alpha)**

<img src="https://user-images.githubusercontent.com/42584742/141484763-7d6d4ce1-f162-4d4a-8cb0-8432763d149a.png" width=70%>

**dark theme example (1.0 - alpha)**

<img src="https://user-images.githubusercontent.com/42584742/141484689-80925a6e-4823-44d3-b59d-dbca9443ee4f.png" width=70%>

## Versions
### [0.5 - stable](https://github.com/israel-dryer/ttkbootstrap/tree/0.5)
- The latest stable version published to PIP
- Uses standard ttk style api
- https://ttkbootstrap.readthedocs.io/en/stable/

```python
import tkinter as tk
from tkinter import ttk
from ttkbootstrap import Style

root = tk.Tk()
style = Style()

b1 = ttk.Button(root, text="Submit", style='success.TButton')
b1.pack(side=tk.LEFT, padx=5, pady=10)

b2 = ttk.Button(root, text="Submit", style='info.Outline.TButton')
b2.pack(side=tk.LEFT, padx=5, pady=10)

root.mainloop()
```

### [1.0 - alpha](https://github.com/israel-dryer/ttkbootstrap/)
- Adds the new `bootstyle` parameter to set styles (legacy ttk style is also useable)
- Adds new themed styles for Labelframe, Scrollbar, 
- Saves memory by only building ttk styles that are used

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

The new keyword api is very flexible. The following examples all produce the same result:
- `bootstyle="info-outline"`
- `bootstyle="info outline"`
- `bootstyle=("info", "outline")`



