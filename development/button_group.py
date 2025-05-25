import tkinter as tk
from tkinter import ttk

from ttkbootstrap.window import Window
from ttkbootstrap.ttk_types import StyleColor
from ttkbootstrap.widgets import Frame, RadioToggle, CheckBoxToggle

# Copy in the ButtonGroup class here if using this as a standalone file.
# Otherwise, import from your module:
# from yourmodule import ButtonGroup

from typing import Literal, Sequence, Union, Callable

Mode = Literal["radio", "checkbox"]
Orientation = Literal["horizontal", "vertical"]

class ButtonGroup(Frame):
    def __init__(
        self,
        master=None,
        mode: Mode = "radio",
        options: Sequence[Union[str, tuple]] = (),
        value: Union[str, list] = None,
        color: StyleColor = "primary",
        variant: str = "solid",
        orient: Orientation = "horizontal",
        command: Callable = None,
        **kwargs
    ):
        super().__init__(master, color=color, **kwargs, padding=(2, 1))
        self.mode = mode
        self.command = command
        self.color = color
        self.variant = variant
        self._buttons = []

        if self.mode == "radio":
            self._var = tk.StringVar(value=value)
        else:
            self._var = {}  # per-button BooleanVar

        for option in options:
            text, val = option if isinstance(option, tuple) else (option, option)
            if self.mode == "radio":
                var = self._var
                btn = RadioToggle(
                    self,
                    text=text,
                    color=color,
                    value=val,
                    variable=var,
                    command=self._on_change,
                )
            else:
                var = tk.BooleanVar(value=val in (value or []))
                self._var[val] = var
                btn = CheckBoxToggle(
                    self,
                    color=color,
                    text=text,
                    variable=var,
                    command=self._on_change,
                )

            btn.pack(side="left" if orient == "horizontal" else "top", padx=1, pady=2)
            self._buttons.append((val, var, btn))

    def _on_change(self):
        if self.command:
            self.command(self.get())

    def get(self) -> Union[str, list]:
        if self.mode == "radio":
            return self._var.get()
        else:
            return [val for val, var, _ in self._buttons if var.get()]

    def set(self, value: Union[str, list]):
        if self.mode == "radio":
            self._var.set(value)
        else:
            for val, var, _ in self._buttons:
                var.set(val in value)

    def bind_variable(self, variable: Union[tk.StringVar, dict]):
        if self.mode == "radio":
            self._var = variable
            for _, _, btn in self._buttons:
                btn.configure(variable=self._var)
        else:
            for val, _, btn in self._buttons:
                if val in variable:
                    self._var[val] = variable[val]
                    btn.configure(variable=self._var[val])


# === DEMO ===
def main():
    root = Window()
    root.title("ButtonGroup Demo")

    ttk.Label(root, text="Radio Group").pack(pady=(10, 4))
    radio_group = ButtonGroup(
        root,
        mode="radio",
        options=[("Apple", "apple"), ("Banana", "banana"), ("Cherry", "cherry")],
        value="banana",
        color="primary",
        variant="solid",
        command=lambda val: print("Radio selected:", val)
    )
    radio_group.pack(pady=10)

    ttk.Label(root, text="Checkbox Group").pack(pady=(20, 4))
    checkbox_group = ButtonGroup(
        root,
        mode="checkbox",
        options=[("Email", "email"), ("SMS", "sms"), ("Push", "push")],
        value=["sms", "push"],
        orient="vertical",
        color="success",
        variant="outline",
        command=lambda val: print("Checkbox selected:", val)
    )
    checkbox_group.pack(pady=10)

    # External access
    def show_values():
        print("RadioGroup:", radio_group.get())
        print("CheckboxGroup:", checkbox_group.get())

    ttk.Button(root, text="Show Values", command=show_values).pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    main()
