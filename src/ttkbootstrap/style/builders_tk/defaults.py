from __future__ import annotations

from typing_extensions import Any

from ttkbootstrap.style.bootstyle_builder_tk import BootstyleBuilderBuilderTk


@BootstyleBuilderBuilderTk.register_builder('Tk')
def build_tk_root(builder: BootstyleBuilderBuilderTk, widget: Any, **options: Any) -> None:
    bg = builder.color(options.get('surface', 'background'))
    widget.configure(background=bg)
    widget.option_add('*Text*Font', 'TkDefaultFont')


@BootstyleBuilderBuilderTk.register_builder('Toplevel')
def build_tk_toplevel(builder: BootstyleBuilderBuilderTk, widget: Any, **options: Any) -> None:
    bg = builder.color(options.get('surface', 'background'))
    widget.configure(background=bg)


@BootstyleBuilderBuilderTk.register_builder('Frame')
def build_tk_frame(builder: BootstyleBuilderBuilderTk, widget: Any, **options: Any) -> None:
    bg = builder.color(options.get('surface', 'background'))
    widget.configure(background=bg)


@BootstyleBuilderBuilderTk.register_builder('Label')
def build_tk_label(builder: BootstyleBuilderBuilderTk, widget: Any, **options: Any) -> None:
    bg = builder.color(options.get('surface', 'background'))
    fg = builder.on_color(bg)
    widget.configure(background=bg, foreground=fg)


@BootstyleBuilderBuilderTk.register_builder('Button')
def build_tk_button(builder: BootstyleBuilderBuilderTk, widget: Any, **options: Any) -> None:
    bg = builder.color('primary')
    fg = builder.on_color(bg)
    widget.configure(
        relief='flat',
        background=bg,
        activebackground=bg,
        foreground=fg,
        activeforeground=fg,
        highlightbackground=bg,
    )


@BootstyleBuilderBuilderTk.register_builder('Entry')
def build_tk_entry(builder: BootstyleBuilderBuilderTk, widget: Any, **options: Any) -> None:
    bg = builder.color('background')
    fg = builder.colors.get('foreground')
    accent = builder.color('primary')
    border = builder.border(bg)
    widget.configure(
        relief='flat',
        highlightthickness=1,
        highlightbackground=border,
        highlightcolor=accent,
        foreground=fg,
        background=bg,
        insertbackground=accent,
        insertwidth=1
    )


@BootstyleBuilderBuilderTk.register_builder('Text')
def build_tk_text(builder: BootstyleBuilderBuilderTk, widget: Any, **options: Any) -> None:
    bg = builder.color('background')
    fg = builder.colors.get('foreground')
    border = builder.border(bg)
    accent = builder.color('primary')
    accent_fg = builder.on_color(accent)
    widget.configure(
        background=bg,
        foreground=fg,
        highlightcolor=accent,
        highlightbackground=border,
        highlightthickness=0,
        insertbackground=fg,
        selectbackground=accent,
        selectforeground=accent_fg,
        insertwidth=1,
        relief='flat',
        padx=5,
        pady=5
    )


@BootstyleBuilderBuilderTk.register_builder('Canvas')
def build_tk_canvas(builder: BootstyleBuilderBuilderTk, widget: Any, **options: Any) -> None:
    bg = builder.color(options.get('surface', 'background'))
    widget.configure(background=bg, highlightthickness=0)


@BootstyleBuilderBuilderTk.register_builder('Checkbutton')
def build_tk_checkbutton(builder: BootstyleBuilderBuilderTk, widget: Any, **options: Any) -> None:
    bg = builder.color(options.get('surface', 'background'))
    fg = builder.colors.get('foreground')
    accent = builder.color('primary')
    widget.configure(
        activebackground=bg,
        activeforeground=accent,
        background=bg,
        foreground=fg,
        selectcolor=bg
    )


@BootstyleBuilderBuilderTk.register_builder('Radiobutton')
def build_tk_radiobutton(builder: BootstyleBuilderBuilderTk, widget: Any, **options: Any) -> None:
    accent = builder.color('primary')
    bg = builder.color(options.get('surface', 'background'))
    fg = builder.colors.get('foreground')
    widget.configure(
        background=bg,
        foreground=fg,
        activebackground=bg,
        activeforeground=accent,
        highlightbackground=bg,
        selectcolor=bg
    )


@BootstyleBuilderBuilderTk.register_builder('Scale')
def build_tk_scale(builder: BootstyleBuilderBuilderTk, widget: Any, **options: Any) -> None:
    accent = builder.color('primary')
    hover = builder.active(accent)
    border = builder.color('border')
    widget.configure(
        background=accent,
        showvalue=False,
        sliderrelief='flat',
        borderwidth=0,
        activebackground=hover,
        highlightthickness=1,
        highlightcolor=border,
        highlightbackground=border,
        troughcolor=border
    )


@BootstyleBuilderBuilderTk.register_builder('Listbox')
def build_tk_listbox(builder: BootstyleBuilderBuilderTk, widget: Any, **options: Any) -> None:
    bg = builder.color('background')
    fg = builder.color('foreground')
    accent = builder.subtle('primary', bg)
    on_accent = builder.on_color(accent)
    border = builder.border(bg)
    widget.configure(
        foreground=fg,
        background=bg,
        selectbackground=accent,
        selectforeground=on_accent,
        highlightbackground=border,
        highlightcolor=accent,
        highlightthickness=1,
        activestyle="none",
        relief='flat'
    )


@BootstyleBuilderBuilderTk.register_builder('Menu')
def build_tk_menu(builder: BootstyleBuilderBuilderTk, widget: Any, **options: Any) -> None:
    bg = builder.color('background')
    fg = builder.color('foreground')
    accent = builder.elevate(bg, 2)
    on_accent = builder.on_color(accent)

    widget.configure(
        tearoff=False,
        borderwidth=1,
        foreground=fg,
        activeforeground=on_accent,
        selectcolor=fg,
        activebackground=accent,
        background=bg,
    )


@BootstyleBuilderBuilderTk.register_builder('Menubutton')
def build_tk_menubutton(builder: BootstyleBuilderBuilderTk, widget: Any, **options: Any) -> None:
    bg = builder.color('primary')
    fg = builder.on_color(bg)
    hover = builder.active(bg)

    widget.configure(
        background=bg,
        foreground=fg,
        activebackground=hover,
        activeforeground=fg,
        borderwidth=0
    )


@BootstyleBuilderBuilderTk.register_builder('Labelframe')
def build_tk_labelframe(builder: BootstyleBuilderBuilderTk, widget: Any, **options: Any) -> None:
    bg = builder.color(options.get('surface', 'background'))
    fg = builder.on_color(bg)
    border = builder.border(bg)
    widget.configure(
        background=bg,
        foreground=fg,  # does not work on Aqua or Windows
        borderwidth=1,
        highlightthickness=0,
        highlightcolor=border,
    )


@BootstyleBuilderBuilderTk.register_builder('Spinbox')
def build_tk_spinbox(builder: BootstyleBuilderBuilderTk, widget: Any, **options: Any) -> None:
    bg = builder.color('background')
    fg = builder.color('foreground')
    border = builder.border(bg)
    accent = builder.subtle('primary', bg)
    insert_background = builder.color('primary')

    widget.configure(
        relief='flat',
        foreground=fg,
        background=bg,
        insertbackground=insert_background,
        insertwidth=1,
        highlightcolor=accent,
        highlightthickness=1,
        highlightbackground=border,
        # button relief ignored by Windows and macOS
        buttonuprelief='flat',
        buttondownrelief='flat',
    )
