from ttkbootstrap.window import Window
from ttkbootstrap.widgets.button import Button


def main():
    app = Window(themename='flatly')
    Button(app, text="Danger", color="danger", command=lambda: print("Pushed")).pack(padx=20, pady=20)
    Button(app, text="Primary", color="primary", command=lambda: print("Pushed")).pack(padx=20, pady=20)
    Button(app, text="Secondary", color="secondary", command=lambda: print("Pushed")).pack(padx=20, pady=20)
    Button(app, text="Warning", color="warning", command=lambda: print("Pushed")).pack(padx=20, pady=20)
    Button(app, text="Outline", command=lambda: print("Pushed")).pack(padx=20, pady=20)
    Button(app, text="Link", color="success", variant="link", command=lambda: print("Pushed")).pack(padx=20, pady=20)
    app.mainloop()


if __name__ == "__main__":
    main()
