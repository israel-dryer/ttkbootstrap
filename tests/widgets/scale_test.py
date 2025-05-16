import tkinter as tk
from ttkbootstrap import Style
from ttkbootstrap.widgets.scale import Scale
from ttkbootstrap.widgets.label import Label


def on_slide(val):
    value_label.config(text=f"Value: {float(val):.1f}")


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Scale Test")

    Style("flatly")

    Label(root, text="Adjust the slider:", padding=10).pack()

    scale = Scale(
        root,
        from_=0,
        to=100,
        length=300,
        orient="horizontal",
        color="success",
        command=on_slide
    )
    scale.pack(pady=10)

    value_label = Label(root, text="Value: 0.0", padding=10)
    value_label.pack()

    root.mainloop()
