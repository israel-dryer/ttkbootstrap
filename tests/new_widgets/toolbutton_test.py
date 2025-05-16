from ttkbootstrap.window import Window
from ttkbootstrap.widgets.toolbutton import Toolbutton


def main():
    app = Window(themename='flatly')
    Toolbutton(app, text="Danger", color="danger", command=lambda: print("Pushed")).pack(padx=20, pady=20)
    Toolbutton(app, text="Primary", color="primary", command=lambda: print("Pushed")).pack(padx=20, pady=20)
    Toolbutton(app, text="Secondary", color="secondary", command=lambda: print("Pushed")).pack(padx=20, pady=20)
    Toolbutton(app, text="Warning", color="warning", command=lambda: print("Pushed")).pack(padx=20, pady=20)
    Toolbutton(app, text="Outline", command=lambda: print("Pushed")).pack(padx=20, pady=20)
    Toolbutton(app, text="Link", color="success", variant="outline", command=lambda: print("Pushed")).pack(padx=20, pady=20)
    app.mainloop()


if __name__ == "__main__":
    main()
