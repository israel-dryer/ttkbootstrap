"""Interactive demo of the themed in-library file dialog (2.1).

Launches each of the four `Querybox` file operations through the *themed*
dialog (`native=False`) so you can see it follow the active theme. Toggle the
theme (top-right) and reopen a dialog to watch it re-render in light/dark.

Run:  python examples/themed_file_dialog.py
"""

import ttkbootstrap as ttk
from ttkbootstrap.constants import *


class Demo(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, padding=16)
        self.pack(fill=BOTH, expand=YES)

        header = ttk.Frame(self)
        header.pack(fill=X, pady=(0, 12))
        ttk.Label(header, text="Themed file dialog", font="-size 15 -weight bold").pack(side=LEFT)
        ttk.Button(header, text="Toggle theme", bootstyle="secondary outline",
                   command=self.toggle_theme).pack(side=RIGHT)

        ttk.Label(self, text="Each button opens the in-library dialog (native=False):",
                  bootstyle="secondary").pack(anchor=W, pady=(0, 8))

        grid = ttk.Frame(self)
        grid.pack(fill=X)
        for i in range(2):
            grid.columnconfigure(i, weight=1)
        self._btn(grid, "Open file…", self.open_one, 0, 0)
        self._btn(grid, "Open multiple…", self.open_many, 0, 1)
        self._btn(grid, "Save as…", self.save_as, 1, 0)
        self._btn(grid, "Choose directory…", self.choose_dir, 1, 1)

        self.result = ttk.StringVar(value="(no selection yet)")
        out = ttk.Labelframe(self, text="Result", padding=12, bootstyle="info")
        out.pack(fill=X, pady=(14, 0))
        ttk.Label(out, textvariable=self.result, wraplength=460,
                  justify=LEFT).pack(anchor=W)

    def _btn(self, master, text, cmd, r, c):
        ttk.Button(master, text=text, command=cmd, bootstyle=PRIMARY).grid(
            row=r, column=c, sticky=EW, padx=4, pady=4, ipady=4)

    def _show(self, value):
        self.result.set(repr(value))

    def open_one(self):
        self._show(ttk.Querybox.get_open_filename(
            parent=self.winfo_toplevel(), native=False,
            filetypes=[("Text files", "*.txt"), ("Python", "*.py *.pyw"),
                       ("All files", "*.*")]))

    def open_many(self):
        self._show(ttk.Querybox.get_open_filenames(
            parent=self.winfo_toplevel(), native=False))

    def save_as(self):
        self._show(ttk.Querybox.get_save_filename(
            parent=self.winfo_toplevel(), native=False,
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]))

    def choose_dir(self):
        self._show(ttk.Querybox.get_directory(
            parent=self.winfo_toplevel(), native=False))

    def toggle_theme(self):
        self.winfo_toplevel().toggle_theme()


if __name__ == "__main__":
    app = ttk.Window("Themed File Dialog — 2.1 demo", theme="bootstrap-light",
                     size=(520, 420))
    Demo(app)
    app.place_window_center()
    app.mainloop()