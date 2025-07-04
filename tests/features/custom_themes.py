from ttkbootstrap import Window, Button
from ttkbootstrap.style import ThemeDefinition

root = Window()

# create custom theme
theme = ThemeDefinition(
    name="custom",
    themetype="dark",
    colors={
        "primary": "#4bb731",
        "secondary": "#444444",
        "success": "#00bc8c",
        "info": "#3498db",
        "warning": "#f39c12",
        "danger": "#e74c3c",
        "light": "#ADB5BD",
        "dark": "#303030",
        "bg": "#222222",
        "fg": "#ffffff",
        "selectbg": "#555555",
        "selectfg": "#ffffff",
        "border": "#222222",
        "inputfg": "#ffffff",
        "inputbg": "#2f2f2f",
        "active": "#1F1F1F",
    },
)

# load custom theme in memory
root.style.load_user_theme(theme)

Button(root,
       text="Change to custom theme",
       command=lambda: root.style.theme_use("custom")
       ).pack(padx=16, pady=16)

root.mainloop()