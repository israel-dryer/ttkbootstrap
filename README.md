# Izzy-Themes-TTK  (IN PROGRESS)
A collection of modern themes for Tkinter TTK built using only built-in standard themes ('clam', 'alt', 'classic', 'default').

## Light Themes
![](examples/light_themes.png)
  
## Dark Themes
![](examples/dark_themes.png)

## Usage
Exactly the same API as built-in ttk.
```python
from izzythemes import Style, ttk
```
create a style object
```python
style = Style()
```

set the theme
```python
style.theme_use('flatly')
```

access the root window created by the style
```
root = style.master

# alternatively, you can create one directly from tkinter
import tkinter as tk
root = tk.Tk()
```

create a styled widget (primary color)
```python
ttk.Label(root, text='Hello world').pack()
```

create a styled widget in another available color
```python
ttk.Label(root, text='Hello world', style='danger.TLabel').pack()
```
