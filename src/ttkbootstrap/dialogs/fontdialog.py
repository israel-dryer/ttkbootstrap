"""FontDialog implementation for selecting and previewing fonts."""

import tkinter
from tkinter import font
from typing import Any, Optional

import ttkbootstrap as ttk
from ttkbootstrap import utility
from ttkbootstrap.constants import *
from ttkbootstrap.localization import MessageCatalog
from ttkbootstrap.dialogs.base import Dialog


class FontDialog(Dialog):
    """A dialog that displays a variety of options for choosing a font.

    This dialog constructs and returns a `Font` object based on the
    options selected by the user. The initial font is based on OS
    settings and will vary.

    The font object is returned when the OK button is pressed and
    can be passed to any widget that accepts a `font` configuration
    option.
    """

    def __init__(
            self, title: str = "Font Selector", parent: Optional[tkinter.Misc] = None,
            default_font: str = "TkDefaultFont") -> None:
        """Create a font selection dialog.

        The dialog provides a comprehensive interface for selecting and
        previewing fonts, including family, size, weight, slant, and effects
        (underline, overstrike). The selected font is returned as a
        tkinter.font.Font object when OK is pressed.

        Parameters:

            title (str):
                The dialog window title (default='Font Selector', will be
                localized).

            parent (Widget):
                Parent widget. The dialog will be modal and centered on this
                widget.

            default_font (str):
                Name of the initial font to display. Can be any valid tkinter
                font name (e.g., 'TkDefaultFont', 'TkFixedFont', 'TkTextFont',
                'TkHeadingFont', etc.) or a custom font name (default='TkDefaultFont').

        Returns:
            The result property contains a tkinter.font.Font object with the
            selected settings, or None if the dialog was cancelled.
        """
        title = MessageCatalog.translate(title)
        super().__init__(parent=parent, title=title)
        self._style = ttk.Style()
        self._default = font.nametofont(default_font)
        self._actual = self._default.actual()
        self._size = ttk.Variable(value=self._actual["size"])
        self._family = ttk.Variable(value=self._actual["family"])
        self._slant = ttk.Variable(value=self._actual["slant"])
        self._weight = ttk.Variable(value=self._actual["weight"])
        self._overstrike = ttk.Variable(value=self._actual["overstrike"])
        self._underline = ttk.Variable(value=self._actual["underline"])
        self._preview_font = font.Font()
        self._slant.trace_add("write", self._update_font_preview)
        self._weight.trace_add("write", self._update_font_preview)
        self._overstrike.trace_add("write", self._update_font_preview)
        self._underline.trace_add("write", self._update_font_preview)

        _headingfont = font.nametofont("TkHeadingFont")
        _headingfont.configure(weight="bold")

        self._update_font_preview()
        self._families = set([self._family.get()])
        for f in font.families():
            if all([f, not f.startswith("@"), "emoji" not in f.lower()]):
                self._families.add(f)

    def create_body(self, master: tkinter.Misc) -> None:
        width = utility.scale_size(master, 600)
        height = utility.scale_size(master, 500)
        self._toplevel.geometry(f"{width}x{height}")

        family_size_frame = ttk.Frame(master, padding=10)
        family_size_frame.pack(fill=X, anchor=N)
        self._initial_focus = self._font_families_selector(family_size_frame)
        self._font_size_selector(family_size_frame)
        self._font_options_selectors(master, padding=10)
        self._font_preview(master, padding=10)

    def create_buttonbox(self, master: tkinter.Misc) -> None:
        container = ttk.Frame(master, padding=(5, 10))
        container.pack(fill=X)

        ok_btn = ttk.Button(
            master=container,
            bootstyle="primary",
            text=MessageCatalog.translate("OK"),
            command=self._on_submit,
        )
        ok_btn.pack(side=RIGHT, padx=5)
        ok_btn.bind("<Return>", lambda _: ok_btn.invoke())

        cancel_btn = ttk.Button(
            master=container,
            bootstyle="secondary",
            text=MessageCatalog.translate("Cancel"),
            command=self._on_cancel,
        )
        cancel_btn.pack(side=RIGHT, padx=5)
        cancel_btn.bind("<Return>", lambda _: cancel_btn.invoke())

        self._toplevel.bind("<Escape>", func=lambda _: cancel_btn.invoke())
        self._toplevel.protocol("WM_DELETE_WINDOW", func=cancel_btn.invoke)

    def _font_families_selector(self, master: tkinter.Misc) -> ttk.Treeview:
        container = ttk.Frame(master)
        container.pack(fill=BOTH, expand=YES, side=LEFT)

        header = ttk.Label(
            container,
            text=MessageCatalog.translate("Family"),
            font="TkHeadingFont",
        )
        header.pack(fill=X, pady=(0, 2), anchor=N)

        listbox = ttk.Treeview(
            master=container,
            height=5,
            show="",
            columns=[0],
        )
        listbox.column(0, width=utility.scale_size(listbox, 250))
        listbox.pack(side=LEFT, fill=BOTH, expand=YES)

        listbox_vbar = ttk.Scrollbar(
            container,
            command=listbox.yview,
            orient=VERTICAL,
            bootstyle="rounded",
        )
        listbox_vbar.pack(side=RIGHT, fill=Y)
        listbox.configure(yscrollcommand=listbox_vbar.set)

        for f in sorted(self._families):
            listbox.insert("", iid=f, index=END, tags=[f], values=[f])
            listbox.tag_configure(f, font=(f, self._size.get()))

        iid = self._family.get()
        listbox.selection_set(iid)  # select default value
        listbox.see(iid)  # ensure default is visible
        listbox.bind("<<TreeviewSelect>>", lambda e: self._on_select_font_family(e))
        return listbox

    def _font_size_selector(self, master: tkinter.Misc) -> None:
        container = ttk.Frame(master)
        container.pack(side=LEFT, fill=Y, padx=(10, 0))

        header = ttk.Label(
            container,
            text=MessageCatalog.translate("Size"),
            font="TkHeadingFont",
        )
        header.pack(fill=X, pady=(0, 2), anchor=N)

        sizes_listbox = ttk.Treeview(container, height=7, columns=[0], show="")
        sizes_listbox.column(0, width=utility.scale_size(sizes_listbox, 24))

        sizes = [*range(8, 13), *range(13, 30, 2), 36, 48, 72]
        for s in sizes:
            sizes_listbox.insert("", iid=s, index=END, values=[s])

        iid = self._size.get()
        sizes_listbox.selection_set(iid)
        sizes_listbox.see(iid)
        sizes_listbox.bind("<<TreeviewSelect>>", lambda e: self._on_select_font_size(e))

        sizes_listbox_vbar = ttk.Scrollbar(
            master=container,
            orient=VERTICAL,
            command=sizes_listbox.yview,
            bootstyle="round",
        )
        sizes_listbox.configure(yscrollcommand=sizes_listbox_vbar.set)
        sizes_listbox.pack(side=LEFT, fill=Y, expand=YES, anchor=N)
        sizes_listbox_vbar.pack(side=LEFT, fill=Y, expand=YES)

    def _font_options_selectors(self, master: tkinter.Misc, padding: int) -> None:
        container = ttk.Frame(master, padding=padding)
        container.pack(fill=X, padx=2, pady=2, anchor=N)

        weight_lframe = ttk.Labelframe(container, text=MessageCatalog.translate("Weight"), padding=5)
        weight_lframe.pack(side=LEFT, fill=X, expand=YES)
        opt_normal = ttk.Radiobutton(
            master=weight_lframe,
            text=MessageCatalog.translate("normal"),
            value="normal",
            variable=self._weight,
        )
        opt_normal.invoke()
        opt_normal.pack(side=LEFT, padx=5, pady=5)
        opt_bold = ttk.Radiobutton(
            master=weight_lframe,
            text=MessageCatalog.translate("bold"),
            value="bold",
            variable=self._weight,
        )
        opt_bold.pack(side=LEFT, padx=5, pady=5)

        slant_lframe = ttk.Labelframe(container, text=MessageCatalog.translate("Slant"), padding=5)
        slant_lframe.pack(side=LEFT, fill=X, padx=10, expand=YES)
        opt_roman = ttk.Radiobutton(
            master=slant_lframe,
            text=MessageCatalog.translate("roman"),
            value="roman",
            variable=self._slant,
        )
        opt_roman.invoke()
        opt_roman.pack(side=LEFT, padx=5, pady=5)
        opt_italic = ttk.Radiobutton(
            master=slant_lframe,
            text=MessageCatalog.translate("italic"),
            value="italic",
            variable=self._slant,
        )
        opt_italic.pack(side=LEFT, padx=5, pady=5)

        effects_lframe = ttk.Labelframe(container, text=MessageCatalog.translate("Effects"), padding=5)
        effects_lframe.pack(side=LEFT, padx=(2, 0), fill=X, expand=YES)
        opt_underline = ttk.Checkbutton(
            master=effects_lframe,
            text=MessageCatalog.translate("underline"),
            variable=self._underline,
        )
        opt_underline.pack(side=LEFT, padx=5, pady=5)
        opt_overstrike = ttk.Checkbutton(
            master=effects_lframe,
            text=MessageCatalog.translate("overstrike"),
            variable=self._overstrike,
        )
        opt_overstrike.pack(side=LEFT, padx=5, pady=5)

    def _font_preview(self, master: tkinter.Misc, padding: int) -> None:
        container = ttk.Frame(master, padding=padding)
        container.pack(fill=BOTH, expand=YES, anchor=N)

        header = ttk.Label(
            container,
            text=MessageCatalog.translate("Preview"),
            font="TkHeadingFont",
        )
        header.pack(fill=X, pady=2, anchor=N)

        content = MessageCatalog.translate("The quick brown fox jumps over the lazy dog.")
        self._preview_text = ttk.Text(
            master=container,
            height=3,
            font=self._preview_font,
            highlightbackground=self._style.colors.primary,
        )
        self._preview_text.insert(END, content)
        self._preview_text.pack(fill=BOTH, expand=YES)
        container.pack_propagate(False)

    def _on_select_font_family(self, e: tkinter.Event) -> None:
        tree: ttk.Treeview = self._toplevel.nametowidget(e.widget)
        fontfamily = tree.selection()[0]
        self._family.set(value=fontfamily)
        self._update_font_preview()

    def _on_select_font_size(self, e: tkinter.Event) -> None:
        tree: ttk.Treeview = self._toplevel.nametowidget(e.widget)
        fontsize = tree.selection()[0]
        self._size.set(value=fontsize)
        self._update_font_preview()

    def _on_submit(self) -> font.Font:
        self._toplevel.destroy()
        return self.result

    def _on_cancel(self) -> None:
        self._result = None
        self._toplevel.destroy()

    def _update_font_preview(self, *_: Any) -> None:
        family = self._family.get()
        size = self._size.get()
        slant = self._slant.get()
        overstrike = self._overstrike.get()
        underline = self._underline.get()
        weight = self._weight.get()

        self._preview_font.config(
            family=family,
            size=size,
            slant=slant,
            overstrike=overstrike,
            underline=underline,
            weight=weight,
        )
        try:
            self._preview_text.configure(font=self._preview_font)
        except Exception:
            pass
        self._result = self._preview_font
