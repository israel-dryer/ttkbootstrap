from ttkbootstrap.window import Window
from ttkbootstrap.widgets.switch import Switch


def main():
    app = Window(themename='flatly')
    Switch(app, text="Danger", color="danger", command=lambda: print("Pushed")).pack(padx=20, pady=20)
    Switch(app, text="Primary", color="primary", command=lambda: print("Pushed")).pack(padx=20, pady=20)
    Switch(app, text="Secondary", color="secondary", command=lambda: print("Pushed")).pack(padx=20, pady=20)
    Switch(app, text="Warning", color="warning", command=lambda: print("Pushed")).pack(padx=20, pady=20)
    Switch(app, text="Outline", command=lambda: print("Pushed")).pack(padx=20, pady=20)
    Switch(app, text="Link", color="success", variant="square", command=lambda: print("Pushed")).pack(padx=20, pady=20)
    app.mainloop()


if __name__ == "__main__":
    main()
