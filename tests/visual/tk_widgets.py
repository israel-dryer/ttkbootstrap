from ttkbootstrap.window import Window
from ttkbootstrap.widgets.tk_widgets import (
    TkButton,
    TkLabel,
    TkTextBox,
    TkFrame,
    TkCheckBox,
    TkLabelFrame,
    TkRadio,
    TkCanvas,
    TkText,
    TkSpinBox,
    TkListBox,
    TkTopLevel,
    TkMenu,
    TkMenuButton,
    TkScale
)
import tkinter as tk  # Needed for Menu integration


def show_toplevel():
    top = TkTopLevel()
    top.title("Themed Toplevel")
    TkLabel(top, text="This is a themed Toplevel window").pack(padx=10, pady=10)
    TkButton(top, text="Close", command=top.destroy).pack(pady=5)


def main():
    root = Window(themename="cosmo")
    root.title("Themed Tkinter Widgets Demo")

    # ---- Menu ----
    menubar = TkMenu(root)
    thememenu = TkMenu(menubar, tearoff=0)
    thememenu.add_command(label="Superhero", command=lambda: root.theme_manager.use_theme("superhero"))
    thememenu.add_command(label="Cosmo", command=lambda: root.theme_manager.use_theme("cosmo"))
    menubar.add_cascade(label="Themes", menu=thememenu)

    filemenu = TkMenu(menubar, tearoff=0)
    filemenu.add_command(label="Open Toplevel", command=show_toplevel)
    filemenu.add_separator()
    filemenu.add_command(label="Quit", command=root.destroy)
    menubar.add_cascade(label="File", menu=filemenu)

    root.config(menu=menubar)

    # ---- Frame (outside labeled frame) ----
    header_frame = TkFrame(root)
    header_frame.pack(padx=10, pady=10, fill="x")
    TkLabel(header_frame, text="Welcome to Themed Widgets Demo", font=("Helvetica", 14)).pack()

    # ---- Main Content ----
    frame = TkLabelFrame(root, text="Label Frame")
    frame.pack(padx=20, pady=10, fill="both", expand=True)

    TkLabel(frame, text="Name:").grid(row=0, column=0, sticky="e")
    entry = TkTextBox(frame)
    entry.grid(row=0, column=1, sticky="w")

    TkCheckBox(frame, text="Subscribe").grid(row=1, column=0, columnspan=2, sticky="w")

    gender = tk.IntVar()
    TkRadio(frame, text="Male", value=1, variable=gender).grid(row=2, column=0, sticky="w")
    TkRadio(frame, text="Female", value=2, variable=gender).grid(row=2, column=1, sticky="w")

    TkLabel(frame, text="Bio:").grid(row=3, column=0, sticky="ne")
    bio = TkText(frame, height=4, width=30)
    bio.grid(row=3, column=1)

    TkLabel(frame, text="Age:").grid(row=4, column=0, sticky="e")
    TkSpinBox(frame, from_=0, to=100).grid(row=4, column=1, sticky="w")

    TkLabel(frame, text="Favorites:").grid(row=5, column=0, sticky="ne")
    listbox = TkListBox(frame, height=4)
    for item in ["Python", "Tkinter", "ttkbootstrap", "Themed Widgets"]:
        listbox.insert("end", item)
    listbox.grid(row=5, column=1)

    TkButton(frame, text="Open Toplevel", command=show_toplevel).grid(row=6, column=0, pady=10)
    TkButton(frame, text="Quit", command=root.destroy).grid(row=6, column=1, pady=10)

    # ---- Canvas ----
    canvas = TkCanvas(root, width=200, height=100)
    canvas.create_oval(10, 10, 190, 90, fill="skyblue")
    canvas.pack(pady=10)

    # ---- MenuButton ----
    menubutton_frame = TkFrame(root)
    menubutton_frame.pack(pady=10)

    menubutton = TkMenuButton(menubutton_frame, text="Options")
    menubutton.pack()

    popup_menu = tk.Menu(menubutton, tearoff=0)
    popup_menu.add_command(label="Say Hello", command=lambda: print("Hello!"))
    popup_menu.add_command(label="Open Toplevel", command=show_toplevel)
    popup_menu.add_separator()
    popup_menu.add_command(label="Quit", command=root.destroy)

    menubutton["menu"] = popup_menu

    # ---- Scale ----
    scale_frame = TkFrame(root)
    scale_frame.pack(pady=10)

    TkLabel(scale_frame, text="Volume:").pack()
    volume = TkScale(scale_frame, from_=0, to=100, orient="horizontal", length=200)
    volume.set(50)
    volume.pack()

    root.mainloop()


if __name__ == "__main__":
    main()
