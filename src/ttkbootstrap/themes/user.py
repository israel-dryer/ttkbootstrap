"""User-defined custom theme storage for ttkbootstrap.

This module provides a dictionary for storing user-created custom themes.
Users can define their own color schemes and save them for use in their
ttkbootstrap applications.

The USER_THEMES dictionary follows the same format as STANDARD_THEMES,
with each theme containing type and colors information.

Example:
    Creating and using a custom theme:
    ```python
    from ttkbootstrap.themes.user import USER_THEMES

    # Define custom theme
    USER_THEMES['mytheme'] = {
        "type": "light",
        "colors": {
            "primary": "#FF6B6B",
            "secondary": "#4ECDC4",
            "success": "#95E1D3",
            "info": "#38A3A5",
            "warning": "#F9CA24",
            "danger": "#EE5A6F",
            "light": "#F7F9FA",
            "dark": "#2C3E50",
            "bg": "#FFFFFF",
            "fg": "#2C3E50",
            "selectbg": "#4ECDC4",
            "selectfg": "#FFFFFF",
            "border": "#DEE2E6",
            "inputfg": "#2C3E50",
            "inputbg": "#FFFFFF",
            "active": "#F0F0F0",
        },
    }

    # Use in application
    import ttkbootstrap as ttk
    root = ttk.Window(themename="mytheme")
    root.mainloop()
    ```
"""

USER_THEMES={}