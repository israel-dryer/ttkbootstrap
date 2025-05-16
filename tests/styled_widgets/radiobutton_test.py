import tkinter as tk
from ttkbootstrap import Style
from ttkbootstrap.widgets.radiobutton import Radiobutton
from ttkbootstrap.widgets.label import Label


def on_select():
    print("Selected:", var.get())


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Radiobutton Test")

    Style("pulse")  # Try "litera", "cyborg", "superhero", etc.

    var = tk.StringVar(value="a")

    Label(root, text="Choose an option:", padding=10).pack()

    Radiobutton(
        root,
        text="Option A",
        value="a",
        variable=var,
        color="primary",
        command=on_select
    ).pack(pady=5)

    Radiobutton(
        root,
        text="Option B",
        value="b",
        variable=var,
        color="success",
        command=on_select
    ).pack(pady=5)

    root.mainloop()
