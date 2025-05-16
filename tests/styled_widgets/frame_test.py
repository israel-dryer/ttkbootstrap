import tkinter as tk
from ttkbootstrap import Style
from ttkbootstrap.widgets.frame import Frame
from ttkbootstrap.widgets.button import Button

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Frame Test")

    Style("litera")

    outer = Frame(root, color="warning", padding=20)
    outer.pack(padx=30, pady=30, fill="both", expand=True)

    Button(outer, text="Click Me", color="primary").pack()

    root.mainloop()
