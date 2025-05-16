import tkinter as tk
from ttkbootstrap import Style
from ttkbootstrap.widgets.labelframe import LabelFrame
from ttkbootstrap.widgets.entry import Entry
from ttkbootstrap.widgets.button import Button

if __name__ == "__main__":
    root = tk.Tk()
    root.title("LabelFrame Test")

    Style("solar")

    lf = LabelFrame(
        root,
        text="User Info",
        color="info",
        padding=15,
        labelanchor="nw"
    )
    lf.pack(padx=30, pady=30, fill="both", expand=True)

    Entry(lf, width=30).pack(pady=(0, 10))
    Button(lf, text="Submit", color="primary").pack()

    root.mainloop()
