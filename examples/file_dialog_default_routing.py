"""File-dialog default routing — what each platform shows out of the box (2.1).

The `Querybox.get_*` file dialogs pick native-vs-themed automatically:

    * X11 (Linux/Unix) -> the **themed** in-library dialog (Tk has no native
      chooser there; its fallback ignores the theme).
    * Windows / macOS   -> the **native** OS chooser.

Run this on Linux and the "default" buttons open the themed dialog with no
`native=` argument at all. The bottom row forces each dialog so you can compare
them on any platform.

Run:  python examples/file_dialog_default_routing.py
"""

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.utils import windowing_system


class Demo(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, padding=16)
        self.pack(fill=BOTH, expand=YES)

        winsys = windowing_system(self)
        default = "themed (in-library)" if winsys == "x11" else "native OS chooser"

        header = ttk.Frame(self)
        header.pack(fill=X, pady=(0, 10))
        ttk.Label(header, text="File dialog — default routing",
                  font="-size 15 -weight bold").pack(side=LEFT)
        ttk.Button(header, text="Toggle theme", bootstyle="secondary outline",
                   command=self.toggle_theme).pack(side=RIGHT)

        info = ttk.Labelframe(self, text="This platform", padding=12, bootstyle="info")
        info.pack(fill=X, pady=(0, 12))
        ttk.Label(info, text=f"Windowing system:  {winsys}").pack(anchor=W)
        ttk.Label(info, text=f"Default file dialog here:  {default}").pack(anchor=W)

        # Default routing — NO native= argument (this is the out-of-the-box path).
        ttk.Label(self, text="Default (no native= argument):",
                  bootstyle="secondary").pack(anchor=W)
        row1 = ttk.Frame(self)
        row1.pack(fill=X, pady=(4, 12))
        self._btn(row1, "Open file…", lambda: self.open(None))
        self._btn(row1, "Save as…", lambda: self.save(None))
        self._btn(row1, "Choose directory…", lambda: self.directory(None))

        # Forced, for side-by-side comparison on any platform.
        ttk.Label(self, text="Forced (compare on any platform):",
                  bootstyle="secondary").pack(anchor=W)
        row2 = ttk.Frame(self)
        row2.pack(fill=X, pady=(4, 0))
        self._btn(row2, "Open — force themed", lambda: self.open(False),
                  bootstyle="success")
        self._btn(row2, "Open — force native", lambda: self.open(True),
                  bootstyle="secondary")

        self.result = ttk.StringVar(value="(no selection yet)")
        out = ttk.Labelframe(self, text="Result", padding=12)
        out.pack(fill=X, pady=(14, 0))
        ttk.Label(out, textvariable=self.result, wraplength=520,
                  justify=LEFT).pack(anchor=W)

    def _btn(self, master, text, cmd, bootstyle=PRIMARY):
        ttk.Button(master, text=text, command=cmd, bootstyle=bootstyle).pack(
            side=LEFT, expand=YES, fill=X, padx=4, ipady=3)

    def _show(self, value):
        self.result.set(repr(value))

    def open(self, native):
        self._show(ttk.Querybox.get_open_filename(
            parent=self.winfo_toplevel(), native=native,
            filetypes=[("Text files", "*.txt"), ("Python", "*.py *.pyw"),
                       ("All files", "*.*")]))

    def save(self, native):
        self._show(ttk.Querybox.get_save_filename(
            parent=self.winfo_toplevel(), native=native, defaultextension=".txt"))

    def directory(self, native):
        self._show(ttk.Querybox.get_directory(
            parent=self.winfo_toplevel(), native=native))

    def toggle_theme(self):
        self.winfo_toplevel().toggle_theme()


if __name__ == "__main__":
    app = ttk.Window("File Dialog Default Routing — 2.1 demo",
                     themename="bootstrap-light", size=(560, 460))
    Demo(app)
    app.place_window_center()
    app.mainloop()