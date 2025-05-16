import tkinter as tk
from ttkbootstrap import Style
from ttkbootstrap.widgets.spinbox import Spinbox
from ttkbootstrap.widgets.label import Label


def update_value():
    current = var.get()
    value_label.config(text=f"Selected: {current}")


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Spinbox Test")

    Style("litera")

    var = tk.IntVar(value=5)

    Label(root, text="Choose a number:", padding=10).pack()

    Spinbox(
        root,
        from_=0,
        to=10,
        increment=1,
        textvariable=var,
        command=update_value,
        color="primary",
        width=10
    ).pack(pady=10)

    value_label = Label(root, text="Selected: 5", padding=10)
    value_label.pack()

    root.mainloop()
