"""FontDialog implementation for selecting and previewing fonts."""

import tkinter
from tkinter import font, Text, Variable
from types import SimpleNamespace
from typing import Any, Optional

from ttkbootstrap.api.style import use_style
from ttkbootstrap.widgets.primitives import (
    Checkbutton,
    Frame,
    Label,
    Labelframe,
    Radiobutton,
    Scrollbar,
    Treeview,
)
from ttkbootstrap.api.window import Window
from ttkbootstrap.runtime.utility import scale_size
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs.dialog import Dialog, DialogButton
from ttkbootstrap.core.localization import MessageCatalog

ttk = SimpleNamespace(
    Checkbutton=Checkbutton,
    Frame=Frame,
    Label=Label,
    Labelframe=Labelframe,
    Radiobutton=Radiobutton,
    Scrollbar=Scrollbar,
    Treeview=Treeview,
    Text=Text,
    Variable=Variable,
    Window=Window,
    use_style=use_style,
)


class FontDialog:
    """A dialog for selecting and previewing fonts.

    This dialog provides a comprehensive interface for selecting fonts,
    including family, size, weight, slant, and effects (underline, overstrike).
    The selected font is returned as a tkinter.font.Font object when OK is
    pressed, or None if cancelled.

    Example:
        ```python
        import ttkbootstrap as ttk
        from ttkbootstrap.dialogs import FontDialog

        root = ttk.Window()
        dialog = FontDialog(master=root, title="Select Font")
        dialog.show()

        if dialog.result:
            label = ttk.Label(root, text="Sample Text", font=dialog.result)
            label.pack()
        ```
    """

    def __init__(
            self,
            title: str = "Font Selector",
            master: Optional[tkinter.Misc] = None,
            default_font: str = "TkDefaultFont"
    ):
        """Create a font selection dialog.

        Args:
            title: The dialog window title. Will be localized automatically.
            master: Parent widget. The dialog will be modal and centered on this widget.
            default_font: Name of the initial font to display. Can be any valid tkinter
                font name (e.g., 'TkDefaultFont', 'TkFixedFont', 'TkTextFont',
                'TkHeadingFont', etc.) or a custom font name.
        """
        title = MessageCatalog.translate(title)
        self._style = ttk.use_style()
        self._default = font.nametofont(default_font)
        self._actual = self._default.actual()
        self._size = ttk.Variable(value=self._actual["size"])
        self._family = ttk.Variable(value=self._actual["family"])
        self._slant = ttk.Variable(value=self._actual["slant"])
        self._weight = ttk.Variable(value=self._actual["weight"])
        self._overstrike = ttk.Variable(value=self._actual["overstrike"])
        self._underline = ttk.Variable(value=self._actual["underline"])
        self._preview_font = font.Font()
        self._preview_text: Optional[ttk.Text] = None

        self._slant.trace_add("write", self._update_font_preview)
        self._weight.trace_add("write", self._update_font_preview)
        self._overstrike.trace_add("write", self._update_font_preview)
        self._underline.trace_add("write", self._update_font_preview)

        self._update_font_preview()
        self._families = {self._family.get()}
        for f in font.families():
            if all([f, not f.startswith("@"), "emoji" not in f.lower()]):
                self._families.add(f)

        # Create the underlying dialog
        self._dialog = Dialog(
            master=master,
            title=title,
            content_builder=self._create_content,
            buttons=[
                DialogButton(
                    text=MessageCatalog.translate("Cancel"),
                    role="cancel",
                    result=None,
                ),
                DialogButton(
                    text=MessageCatalog.translate("OK"),
                    role="primary",
                    default=True,
                    command=lambda dlg: self._on_submit(),
                    result=self._preview_font,
                ),
            ],
        )

    def _create_content(self, master: tkinter.Widget) -> None:
        """Create the dialog body with font selection controls."""
        # Set dialog size
        width = scale_size(master, 800)
        height = scale_size(master, 600)
        if self._dialog.toplevel:
            self._dialog.toplevel.geometry(f"{width}x{height}")

        family_size_frame = ttk.Frame(master, padding=10)
        family_size_frame.pack(fill=X, anchor=N)
        initial_focus = self._font_families_selector(family_size_frame)
        self._font_size_selector(family_size_frame)
        self._font_options_selectors(master, padding=10)
        self._font_preview(master, padding=10)

        # Set initial focus
        if initial_focus and self._dialog.toplevel:
            self._dialog.toplevel.after(100, initial_focus.focus_set)

    def _font_families_selector(self, master: tkinter.Misc) -> ttk.Treeview:
        """Create and populate the font family selection list."""
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
        listbox.column(0, width=scale_size(listbox, 250))
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
            listbox.insert("", iid=f, index='end', tags=[f], values=[f])
            listbox.tag_configure(f, font=(f, self._size.get()))

        iid = self._family.get()
        listbox.selection_set(iid)  # select default value
        listbox.see(iid)  # ensure default is visible
        listbox.bind("<<TreeviewSelect>>", lambda e: self._on_select_font_family(e))
        return listbox

    def _font_size_selector(self, master: tkinter.Misc) -> None:
        """Create and populate the font size selection list."""
        container = ttk.Frame(master)
        container.pack(side=LEFT, fill=Y, padx=(10, 0))

        header = ttk.Label(
            container,
            text=MessageCatalog.translate("Size"),
            font="TkHeadingFont",
        )
        header.pack(fill=X, pady=(0, 2), anchor=N)

        sizes_listbox = ttk.Treeview(container, height=7, columns=[0], show="")
        sizes_listbox.column(0, width=scale_size(sizes_listbox, 48))

        sizes = [*range(8, 13), *range(13, 30, 2), 36, 48, 72]
        for s in sizes:
            sizes_listbox.insert("", iid=s, index='end', values=[s])

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
        """Create font option controls (weight, slant, effects)."""
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
        """Create the font preview text widget."""
        container = ttk.Frame(master, padding=padding, height=scale_size(master, 150))
        container.pack(fill=BOTH, expand=YES, anchor=N)
        container.pack_propagate(False)

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
        )
        self._preview_text.insert(END, content)
        self._preview_text.pack(fill=BOTH, expand=YES)

    def _on_select_font_family(self, e: tkinter.Event) -> None:
        """Handle font family selection event."""
        if not self._dialog.toplevel:
            return
        tree: ttk.Treeview = self._dialog.toplevel.nametowidget(e.widget)
        font_family = tree.selection()[0]
        self._family.set(value=font_family)
        self._update_font_preview()

    def _on_select_font_size(self, e: tkinter.Event) -> None:
        """Handle font size selection event."""
        if not self._dialog.toplevel:
            return
        tree: ttk.Treeview = self._dialog.toplevel.nametowidget(e.widget)
        fontsize = tree.selection()[0]
        self._size.set(value=fontsize)
        self._update_font_preview()

    def _on_submit(self) -> None:
        """Handle OK button - update result with current font."""
        self._dialog.result = self._preview_font

    def _update_font_preview(self, *_: Any) -> None:
        """Update the preview font based on current selections."""
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
        if self._preview_text:
            try:
                self._preview_text.configure(font=self._preview_font)
            except Exception:
                pass

    def show(self, position: Optional[tuple[int, int]] = None) -> None:
        """Show the dialog."""
        self._dialog.show(position=position, modal=True)

    @property
    def result(self) -> Optional[font.Font]:
        """The selected font, or None if cancelled."""
        return self._dialog.result
