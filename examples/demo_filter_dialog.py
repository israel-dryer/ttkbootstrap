"""Demo of the FilterDialog widget.

Shows how to use FilterDialog with and without the frameless option.
"""
import ttkbootstrap as ttk
from ttkbootstrap.dialogs import FilterDialog


app = ttk.Window(themename="dark", size=(500, 500))

# Test button to show the filter dialog with window chrome
def show_filter():
    dialog = FilterDialog(
        master=app,
        title="Select Colors",
        items=[
            "Red",
            "Green",
            {"text": "Blue", "selected": True},
            "Orange",
            "Purple",
            "Yellow",
            "Pink",
            "Brown",
            "Black",
            "White"
        ],
        allow_search=True,
        allow_select_all=True
    )
    result = dialog.show()
    print(f"Selected items: {result}")
    if result:
        result_label.config(text=f"Selected: {', '.join(map(str, result))}")


# Test button to show the filter dialog frameless
def show_filter_frameless():
    dialog = FilterDialog(
        master=app,
        title="Select Colors",
        items=[
            "Red",
            "Green",
            {"text": "Blue", "selected": True},
            "Orange",
            "Purple",
            "Yellow",
            "Pink",
            "Brown",
            "Black",
            "White"
        ],
        allow_search=True,
        allow_select_all=True,
        frameless=True
    )
    result = dialog.show()
    print(f"Selected items (frameless): {result}")
    if result:
        result_label.config(text=f"Selected: {', '.join(map(str, result))}")


# UI
ttk.Label(app, text="FilterDialog Demo", font=("", 16, "bold")).pack(pady=20)
ttk.Button(app, text="Show Filter Dialog", command=show_filter).pack(pady=10)
ttk.Button(app, text="Show Filter Dialog (Frameless)", command=show_filter_frameless).pack(pady=10)
result_label = ttk.Label(app, text="No items selected", bootstyle="secondary")
result_label.pack(pady=10)

app.mainloop()
