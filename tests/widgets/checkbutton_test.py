from ttkbootstrap.window import Window
from ttkbootstrap.widgets.checkbutton import Checkbutton


def main():
    app = Window(themename='flatly')
    Checkbutton(app, text="Default", command=lambda: print("Pushed")).pack(padx=20, pady=20)
    Checkbutton(app, text="Danger", color="danger", command=lambda: print("Pushed")).pack(padx=20, pady=20)
    Checkbutton(app, text="Primary", color="primary", command=lambda: print("Pushed")).pack(padx=20, pady=20)
    Checkbutton(app, text="Secondary", color="secondary", command=lambda: print("Pushed")).pack(padx=20, pady=20)
    Checkbutton(app, text="Warning", color="warning", command=lambda: print("Pushed")).pack(padx=20, pady=20)
    Checkbutton(app, text="Outline", command=lambda: print("Pushed")).pack(padx=20, pady=20)
    Checkbutton(app, text="Link", color="success", command=lambda: print("Pushed")).pack(padx=20, pady=20)
    app.mainloop()


if __name__ == "__main__":
    main()
