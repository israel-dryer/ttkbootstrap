import tkinter as tk
from ttkbootstrap import Style
from ttkbootstrap.widgets.separator import Separator
from ttkbootstrap.widgets.label import Label
from ttkbootstrap.widgets.frame import Frame


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Separator Test")

    Style("sandstone")

    # Horizontal separator section
    top = Frame(root, padding=10)
    top.pack(fill="x", padx=20, pady=(20, 10))

    Label(top, text="Above the line", color="primary").pack()
    Separator(top, orient="horizontal", color="info").pack(fill="x", pady=10)
    Label(top, text="Below the line", color="secondary").pack()

    # Vertical separator section
    middle = Frame(root, padding=10)
    middle.pack(pady=20)

    left = Frame(middle)
    right = Frame(middle)

    Label(left, text="Left", color="success").pack()
    Label(right, text="Right", color="danger").pack()

    left.grid(row=0, column=0, padx=(0, 10))
    Separator(middle, orient="vertical", color="warning").grid(row=0, column=1, sticky="ns")
    right.grid(row=0, column=2, padx=(10, 0))

    root.mainloop()
