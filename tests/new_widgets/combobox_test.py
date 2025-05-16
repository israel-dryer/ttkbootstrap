import tkinter as tk
from ttkbootstrap import Style
from ttkbootstrap.widgets.combobox import Combobox


def on_select(event):
    print("Selected:", combo.get())


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Combobox Test")

    # Apply ttkbootstrap theme
    Style("darkly")

    combo = Combobox(
        root,
        values=["Option 1", "Option 2", "Option 3"],
        color="primary",
        state="readonly",
        width=20
    )
    combo.pack(padx=20, pady=20)
    combo.bind("<<ComboboxSelected>>", on_select)

    root.mainloop()
