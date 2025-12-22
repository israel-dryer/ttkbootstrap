# API Reference

Auto-generated API documentation for ttkbootstrap.

## Modules

| Module | Description |
|--------|-------------|
| [App](app/index.md) | Application, window management, and menus |
| [Style](style/index.md) | Theme and style management |
| [Widgets](widgets/index.md) | UI components |
| [Dialogs](dialogs/index.md) | Dialog windows for common interactions |
| [Data](data/index.md) | Data sources for widgets |
| [i18n](i18n/index.md) | Internationalization and localization |
| [Utils](utils/index.md) | Core utilities for reactive programming and validation |

## Usage

All exports are available from the top-level package:

```python
import ttkbootstrap as ttk

# App
app = ttk.App(title="My App", theme="darkly")

# Widgets
button = ttk.Button(app, text="Click", bootstyle="success")

# Style
ttk.set_theme("cosmo")

# Localization
from ttkbootstrap import L
label = ttk.Label(app, text=L("Hello"))

app.mainloop()
```