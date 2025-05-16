import tkinter as tk
from ttkbootstrap import Style
from ttkbootstrap.widgets.label import Label


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Label Test")

    Style("superhero")  # Try different themes like "cosmo", "flatly", etc.

    Label(root, text="Primary Label (Default)", color="primary", variant="default", padding=10).pack(pady=10)
    Label(root, text="Success Label (Inverse)", color="success", variant="inverse", padding=10).pack(pady=10)
    Label(root, text="Danger Label (Inverse)", color="danger", variant="inverse", padding=10).pack(pady=10)
    Label(root, text="Muted Label", color="secondary", variant="default", padding=10).pack(pady=10)

    root.mainloop()
