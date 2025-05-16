import tkinter as tk
from ttkbootstrap import Style
from ttkbootstrap.widgets.menubutton import Menubutton


def on_select(option: str):
    print(f"Selected: {option}")
    selected_var.set(f"Option: {option}")


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Menubutton Test")

    Style("litera")

    selected_var = tk.StringVar(value="Option: None")

    # Create Menubutton
    mb = Menubutton(root, text="Options", color="primary", width=15)
    mb.pack(padx=20, pady=20)

    # Attach tk.Menu
    menu = tk.Menu(mb, tearoff=0)
    menu.add_command(label="New", command=lambda: on_select("New"))
    menu.add_command(label="Open", command=lambda: on_select("Open"))
    menu.add_separator()
    menu.add_command(label="Exit", command=root.destroy)

    mb["menu"] = menu

    # Label to show selected option
    tk.Label(root, textvariable=selected_var, font="-size 12").pack(pady=(0, 20))

    root.mainloop()
