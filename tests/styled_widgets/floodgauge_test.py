import tkinter as tk
from ttkbootstrap import Style
from ttkbootstrap.widgets import Frame, Button
from ttkbootstrap.widgets.floodgauge import Floodgauge


def test_floodgauge():
    root = tk.Tk()
    root.title("Floodgauge Test")
    root.geometry("400x300")
    style = Style("litera")

    frame = Frame(root, padding=10)
    frame.pack(fill="both", expand=True)

    fg = Floodgauge(
        frame,
        value=0,
        maximum=100,
        orient="horizontal",
        color="success",
        mask="Loading {}%",
        thickness=30,
        length=300,
        mode="determinate",
    )
    fg.pack(pady=10)

    def increase():
        fg.step(10)

    def reset():
        fg.configure(value=0)

    def toggle_mode():
        if fg.mode == "determinate":
            fg.mode = "indeterminate"
            fg.start()
            btn_toggle.config(text="Stop Indeterminate")
        else:
            fg.mode = "determinate"
            fg.stop()
            fg.configure(value=0)
            btn_toggle.config(text="Start Indeterminate")

    btns = Frame(frame)
    btns.pack(pady=10, fill="x")

    Button(btns, text="Step +10", command=increase).pack(side="left", expand=True, padx=5)
    Button(btns, text="Reset", command=reset).pack(side="left", expand=True, padx=5)
    btn_toggle = Button(btns, text="Start Indeterminate", command=toggle_mode)
    btn_toggle.pack(side="left", expand=True, padx=5)

    # Vertical Floodgauge for completeness
    vertical = Floodgauge(
        frame,
        value=60,
        maximum=100,
        orient="vertical",
        color="info",
        mask="{}%",
        thickness=30,
        length=150,
    )
    vertical.pack(pady=10, side="right", padx=20)

    root.mainloop()


if __name__ == "__main__":
    test_floodgauge()
