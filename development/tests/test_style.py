from tkinter import ttk
from ttkbootstrap import Style
from random import choice


# TODO for some reason I'm getting two instances of Style when I try to subclass it.

class Demo(Style):
    def __init__(self):
        super().__init__()
        self.setup()

    def setup(self):
        self.label = ttk.Label(text='Flatly')
        self.label.pack(padx=10, pady=10)

        self.btn = ttk.Button(text="OUTLINE", bootstyle='outline')
        self.btn['command'] = self.change_theme
        self.btn.pack(padx=10, pady=10)

        self.btn2 = ttk.Button(text="INFO", bootstyle='info')
        self.btn2.configure(command=self.change_theme)
        self.btn2.pack(padx=10, pady=10)

    def change_theme(self):
        theme = choice(self.theme_names())
        self.theme_use(theme)
        self.label['text'] = theme

    def run(self):
        self.master.mainloop()


if __name__ == '__main__':
    d = Demo()
    d.run()


