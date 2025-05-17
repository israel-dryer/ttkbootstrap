import ttkbootstrap as ttk
from ttkbootstrap.widgets import Button, ToolTip


def run_tooltip_test():
    app = ttk.Window(title="Tooltip Test", themename="flatly", size=(300, 200))

    btn_top = Button(app, text="Top Right")
    btn_top.pack(pady=10)
    ToolTip(btn_top, text="Tooltip at top right", position="top right", color="info")

    btn_bottom = Button(app, text="Bottom Center")
    btn_bottom.pack(pady=10)
    ToolTip(btn_bottom, text="Bottom center tooltip", position="bottom center", color="success")

    btn_mouse = Button(app, text="Follow Mouse")
    btn_mouse.pack(pady=10)
    ToolTip(btn_mouse, text="I follow the pointer", color="warning")

    app.mainloop()


if __name__ == "__main__":
    run_tooltip_test()
