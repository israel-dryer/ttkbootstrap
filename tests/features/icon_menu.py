import ttkbootstrap as ttk

app = ttk.Window(size=(400, 300))


def change_theme(theme_name):
    app.style.theme_use(theme_name)
    # Manually trigger the event to ensure it fires
    app.event_generate('<<ThemeChanged>>')


menu_items = [
    {
        "label": "File",
        "items": [
            {"label": "Open", "icon": "folder2-open"},
            {"label": "Save", "icon": "save", "items": [
                {"label": "Save Now", "icon": "check-circle"},
                {"label": "Save Later", "icon": "clock"}
            ]},
            {"type": "separator"},
            {"label": "Exit", "command": app.quit, "icon": "x-circle"}
        ],
    },
    {
        "label": "Edit",
        "items": [
            {"label": "Undo", "icon": "arrow-counterclockwise"},
            {"label": "Redo", "icon": "arrow-clockwise"},
        ]
    },
    {
        "label": "Themes",
        "items": [
            {"label": theme, "type": "radiobutton",
             "command": lambda t=theme: change_theme(t)}
            for theme in ["superhero", "darkly", "flatly", "litera", "cosmo"]
        ]
    }
]

ttk.create_menu(app, menu_items)

# Add a menubutton as well
mb = ttk.MenuButton(app, bootstyle="danger", text="Menubutton")
mb['menu'] = ttk.create_menu(mb, menu_items)
mb.pack(padx=10, pady=10)

app.mainloop()