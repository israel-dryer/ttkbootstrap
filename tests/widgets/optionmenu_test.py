import tkinter as tk
from ttkbootstrap import Style
from ttkbootstrap.widgets.optionmenu import OptionMenu
from ttkbootstrap.widgets.label import Label


def on_change(*_):
    selected_label.config(text=f"Selected: {option_var.get()}")


if __name__ == "__main__":
    root = tk.Tk()
    root.title("OptionMenu Test")

    Style("morph")

    option_var = tk.StringVar(value="One")  # set initial value

    selected_label = Label(root, text="Selected: One", padding=10)
    selected_label.pack()

    OptionMenu(
        root,
        option_var,
        "One",  # default
        "One", "Two", "Three", "Four",
        color="info",
        width=20
    ).pack(pady=20)

    option_var.trace_add("write", on_change)  # trace AFTER label is defined

    root.mainloop()
