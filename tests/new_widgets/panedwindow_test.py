import tkinter as tk
from ttkbootstrap import Style
from ttkbootstrap.widgets.panedwindow import PanedWindow
from ttkbootstrap.widgets.frame import Frame
from ttkbootstrap.widgets.label import Label


if __name__ == "__main__":
    root = tk.Tk()
    root.title("PanedWindow Test")

    Style("litera")

    pw = PanedWindow(root, orient="horizontal", color="light")
    pw.pack(fill="both", expand=True, padx=20, pady=20)

    left = Frame(pw, color="secondary", padding=10, width=200)
    right = Frame(pw, color="primary", padding=10, width=200)

    Label(left, text="Left Pane", color="dark", variant="inverse").pack()
    Label(right, text="Right Pane", color="primary", variant="inverse").pack()

    pw.add(left)
    pw.add(right)

    root.mainloop()
