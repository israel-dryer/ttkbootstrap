import tkinter as tk
from ttkbootstrap import Style
from ttkbootstrap.widgets.toolcheckbutton import ToolCheckbutton


def on_toggle():
    print("Bold:", bold_var.get(), "Italic:", italic_var.get())


if __name__ == "__main__":
    root = tk.Tk()
    root.title("ToolCheckbutton Test")

    Style("minty")

    bold_var = tk.BooleanVar(value=False)
    italic_var = tk.BooleanVar(value=True)

    ToolCheckbutton(
        root,
        text="Bold",
        variable=bold_var,
        color="primary",
        variant="outline",
        command=on_toggle,
        padding=10,
        width=10
    ).pack(pady=10)

    ToolCheckbutton(
        root,
        text="Italic",
        variable=italic_var,
        color="secondary",
        variant="default",
        command=on_toggle,
        padding=10,
        width=10
    ).pack(pady=10)

    root.mainloop()
