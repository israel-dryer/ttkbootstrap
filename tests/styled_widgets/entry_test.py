import tkinter as tk
from ttkbootstrap import Style
from ttkbootstrap.widgets.entry import Entry


def on_key_release(event):
    print("Current value:", var.get())


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Entry Test")

    # Apply ttkbootstrap theme
    Style("flatly")

    var = tk.StringVar(value="Hello")

    entry = Entry(root, textvariable=var, color="success", width=30)
    entry.pack(padx=20, pady=20)
    entry.bind("<KeyRelease>", on_key_release)

    root.mainloop()
