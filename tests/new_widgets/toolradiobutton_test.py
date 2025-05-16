import tkinter as tk
from ttkbootstrap import Style
from ttkbootstrap.widgets.toolradiobutton import ToolRadiobutton


def on_change():
    print("Alignment:", align_var.get())


if __name__ == "__main__":
    root = tk.Tk()
    root.title("ToolRadiobutton Test")

    Style("cyborg")

    align_var = tk.StringVar(value="left")

    ToolRadiobutton(
        root,
        text="Left",
        value="left",
        variable=align_var,
        color="info",
        variant="outline",
        command=on_change,
        padding=10,
        width=10
    ).pack(pady=10)

    ToolRadiobutton(
        root,
        text="Center",
        value="center",
        variable=align_var,
        color="info",
        variant="default",
        command=on_change,
        padding=10,
        width=10
    ).pack(pady=10)

    ToolRadiobutton(
        root,
        text="Right",
        value="right",
        variable=align_var,
        color="info",
        variant="outline",
        command=on_change,
        padding=10,
        width=10
    ).pack(pady=10)

    root.mainloop()
