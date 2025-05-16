import tkinter as tk
from ttkbootstrap import Style
from ttkbootstrap.widgets.sizegrip import Sizegrip
from ttkbootstrap.widgets.label import Label
from ttkbootstrap.widgets.frame import Frame


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Sizegrip Test")
    root.geometry("400x250")

    Style("morph")

    # Main content area
    content = Frame(root, padding=20)
    content.pack(fill="both", expand=True)

    Label(content, text="Resize the window using the sizegrip →", color="info").pack(anchor="center", pady=20)

    # Sizegrip in bottom-right corner
    grip = Sizegrip(root, color="success")
    grip.pack(side="right", anchor="se", padx=2, pady=2)

    root.mainloop()
