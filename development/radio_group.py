import tkinter as tk
from tkinter import ttk


class VerticalRadioGroup(ttk.Frame):
    def __init__(self, master=None, options=None, value=None, command=None):
        super().__init__(master)
        self._buttons = {}
        self._value = tk.StringVar(value=value)
        self._command = command

        for i, label in enumerate(options):
            b = ttk.Button(
                self,
                text=label,
                style="danger.toggle.TButton",
                command=lambda v=label: self._on_select(v)
            )
            b.pack(fill="x", ipadx=6, ipady=6)

            # Optional separator line between Radio 1 and Radio 2
            if i == 0:
                sep = ttk.Separator(self, orient="horizontal")
                sep.pack(fill="x")

            self._buttons[label] = b

        self._update_styles()

    def _on_select(self, value):
        self._value.set(value)
        self._update_styles()
        if self._command:
            self._command(value)

    def _update_styles(self):
        selected = self._value.get()
        for val, btn in self._buttons.items():
            if val == selected:
                btn.state(["pressed"])
            else:
                btn.state(["!pressed"])

    def get(self):
        return self._value.get()


def create_styles():
    style = ttk.Style()
    style.theme_use("clam")  # or "alt" for better styling base

    style.configure("danger.toggle.TButton",
                    background="white",
                    foreground="#d33",
                    relief="solid",
                    borderwidth=1,
                    anchor="center",
                    padding=6)

    style.map("danger.toggle.TButton",
              background=[("pressed", "#d33")],
              foreground=[("pressed", "white")],
              relief=[("pressed", "flat")])

    # Optional: Rounded corners could be added here with images or element layout


def main():
    root = tk.Tk()
    root.title("Vertical Toggle Button Group")

    create_styles()

    ttk.Label(root, text="Choose an option:", padding=10).pack()

    group = VerticalRadioGroup(
        root,
        options=["Radio 1", "Radio 2", "Radio 3"],
        value="Radio 3",
        command=lambda val: print("Selected:", val)
    )
    group.pack(padx=20, pady=20, fill="x")

    root.mainloop()


if __name__ == "__main__":
    main()
