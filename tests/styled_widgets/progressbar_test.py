import tkinter as tk
from ttkbootstrap import Style
from ttkbootstrap.widgets.progressbar import Progressbar
from ttkbootstrap.widgets.button import Button


def toggle_indeterminate():
    if pb2["mode"] == "indeterminate":
        if pb2.running:
            pb2.stop()
        else:
            pb2.start()


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Progressbar Test")

    Style("cyborg")  # Try themes like "litera", "superhero", "solar"

    # Default determinate progressbar
    pb1 = Progressbar(root, color="primary", variant="default", length=250, mode="determinate")
    pb1.pack(pady=10)
    pb1["value"] = 50

    # Striped indeterminate progressbar
    pb2 = Progressbar(root, color="success", variant="striped", length=250, mode="indeterminate")
    pb2.pack(pady=10)
    pb2.running = False

    def toggle():
        if pb2.running:
            pb2.stop()
            pb2.running = False
        else:
            pb2.start()
            pb2.running = True

    Button(root, text="Toggle Indeterminate", command=toggle, color="secondary").pack(pady=20)

    root.mainloop()
