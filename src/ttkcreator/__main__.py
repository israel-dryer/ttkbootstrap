"""Standalone Tk app for authoring `Theme` definitions: edit accent/neutral
colors and light/dark background/foreground, preview the result live, and
export or save the theme.
"""

import sys
import shutil
import json
from uuid import uuid4
from pathlib import Path
import ttkbootstrap as ttk
from tkinter import Frame
from tkinter.colorchooser import askcolor
from tkinter.filedialog import askopenfilename, asksaveasfilename
from ttkbootstrap.themes import user
from ttkbootstrap.themes.builtin import CURATED_THEMES
from ttkbootstrap.style import Theme
from ttkbootstrap.style.theme import _DEFAULT_NEUTRAL
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox


# The editable Theme inputs, grouped for the UI. Each entry is
# (field-key, display label). The field keys map onto `Theme` (or its
# light/dark blocks) in `_spec()`.
_ACCENT_FIELDS = [
    ("primary", "primary"),
    ("secondary", "secondary"),
    ("success", "success"),
    ("info", "info"),
    ("warning", "warning"),
    ("danger", "danger"),
    ("neutral", "neutral"),
]
_LIGHT_FIELDS = [
    ("light_bg", "background"),
    ("light_fg", "foreground"),
]
_DARK_FIELDS = [
    ("dark_bg", "background"),
    ("dark_fg", "foreground"),
]


class ThemeCreator(ttk.Window):
    """Author a semantic-anchor `Theme`: edit the accent anchors + neutral and
    the light/dark background/foreground blocks; the full palette (and both mode
    variants) is generated. Preview live, then export a `Theme(...).register()`
    snippet or save it to your user theme store.
    """

    def __init__(self):
        """Build the main window: menu, configuration panel, and live preview."""
        super().__init__("TTK Creator")
        self._families = {t.name: t for t in CURATED_THEMES}
        self.rows = {}
        self.configure_frame = ttk.Frame(self, padding=(10, 10, 5, 10))
        self.configure_frame.pack(side=LEFT, fill=BOTH, expand=YES)
        self.demo_frame = ttk.Frame(self, padding=(5, 10, 10, 10))
        self.demo_frame.pack(side=LEFT, fill=BOTH, expand=YES)
        self.setup_theme_creator()
        self.demo_widgets = DemoWidgets(self, self.style)
        self.demo_widgets.pack(fill=BOTH, expand=YES)

    def setup_theme_creator(self):
        """Build the file menu and the accent/light/dark color-row sections."""
        # application menu
        self.menu = ttk.Menu()
        commands = [
            ("Save", self.save_theme),
            ("Reset", self.change_base_theme),
            ("Import", self.import_user_themes),
            ("Export all themes", self.export_user_themes),
            ("Export theme definition", self.export_theme_as_python_file),
        ]
        if sys.platform == 'darwin':
            self.file_submenu = ttk.Menu(self.menu)
            for label, command in commands:
                self.file_submenu.add_command(label=label, command=command)
            self.menu.add_cascade(menu=self.file_submenu, label="File")
        else:
            for label, command in commands:
                self.menu.add_command(label=label, command=command)
        self.configure(menu=self.menu)

        cf = self.configure_frame

        ## user theme name
        f1 = ttk.Frame(cf, padding=(5, 2))
        ttk.Label(f1, text="name", width=14).pack(side=LEFT)
        self.theme_name = ttk.Entry(f1)
        self.theme_name.insert(END, "new theme")
        self.theme_name.pack(side=LEFT, fill=X, expand=YES)
        f1.pack(fill=X, expand=YES)

        ## base family + preview mode
        f2 = ttk.Frame(cf, padding=(5, 2))
        ttk.Label(f2, text="base family", width=14).pack(side=LEFT)
        self.base_theme = ttk.Combobox(
            f2, values=list(self._families), state="readonly")
        self.base_theme.set("bootstrap")
        self.base_theme.pack(side=LEFT, fill=X, expand=YES)
        self.base_theme.bind("<<ComboboxSelected>>", self.change_base_theme)
        f2.pack(fill=X, expand=YES)

        f3 = ttk.Frame(cf, padding=(5, 2))
        ttk.Label(f3, text="preview mode", width=14).pack(side=LEFT)
        self.preview_mode = ttk.Combobox(
            f3, values=["light", "dark"], state="readonly")
        self.preview_mode.set("light")
        self.preview_mode.pack(side=LEFT, fill=X, expand=YES)
        self.preview_mode.bind("<<ComboboxSelected>>", self.create_temp_theme)
        f3.pack(fill=X, expand=YES, pady=(0, 10))

        ## anchor + block color rows, grouped under headers
        self._add_section("Accents & neutral", _ACCENT_FIELDS)
        self._add_section("Light background/foreground", _LIGHT_FIELDS)
        self._add_section("Dark background/foreground", _DARK_FIELDS)

        # seed the rows from the base family
        self._load_family(self.base_theme.get())

    def _add_section(self, title, fields):
        ttk.Label(
            self.configure_frame, text=title, font="-weight bold",
            padding=(5, 8, 0, 2),
        ).pack(fill=X)
        for key, label in fields:
            row = ColorRow(self.configure_frame, key, label)
            row.pack(fill=X, expand=YES)
            row.bind("<<ColorSelected>>", self.create_temp_theme)
            self.rows[key] = row

    # ----- theme spec / generation ------------------------------------------

    def _mode(self):
        return self.preview_mode.get() or "light"

    def _spec(self):
        """Build the `Theme(**spec)` keyword dict from the current rows."""
        def v(key):
            return (self.rows[key].color_value or "").strip() or None

        light = {"background": v("light_bg"), "foreground": v("light_fg")}
        dark = {"background": v("dark_bg"), "foreground": v("dark_fg")}
        return {
            "primary": v("primary"),
            "success": v("success"),
            "info": v("info"),
            "warning": v("warning"),
            "danger": v("danger"),
            "secondary": v("secondary"),
            "neutral": v("neutral") or _DEFAULT_NEUTRAL,
            "light": light if light["background"] and light["foreground"] else None,
            "dark": dark if dark["background"] and dark["foreground"] else None,
        }

    def create_temp_theme(self, *_):
        """Generate a throwaway Theme from the current settings and preview the
        selected mode. A fresh name each time forces a rebuild (an already-built
        Tcl theme would otherwise show stale colors)."""
        spec = self._spec()
        themename = "temp" + uuid4().hex[:10]
        try:
            definitions = Theme(name=themename, **spec).to_definitions()
        except ValueError:
            return  # incomplete/invalid spec (e.g. a blank accent) -- skip
        if not definitions:
            return
        for definition in definitions:
            self.style.register_theme(definition)
        names = {d.name for d in definitions}
        target = f"{themename}-{self._mode()}"
        if target not in names:
            target = definitions[0].name  # only one block defined
        self.style.theme_use(target)

    def change_base_theme(self, *_):
        """Load the selected base family's anchors/blocks into the rows."""
        self._load_family(self.base_theme.get())

    def _load_family(self, name):
        family = self._families.get(name)
        if family is None:
            return
        self.rows["primary"].set_value(family.primary)
        self.rows["success"].set_value(family.success)
        self.rows["info"].set_value(family.info)
        self.rows["warning"].set_value(family.warning)
        self.rows["danger"].set_value(family.danger)
        self.rows["secondary"].set_value(family.secondary or "")
        self.rows["neutral"].set_value(family.neutral)
        light = family.light or {}
        dark = family.dark or {}
        self.rows["light_bg"].set_value(light.get("background", ""))
        self.rows["light_fg"].set_value(light.get("foreground", ""))
        self.rows["dark_bg"].set_value(dark.get("background", ""))
        self.rows["dark_fg"].set_value(dark.get("foreground", ""))
        self.create_temp_theme()
        # A family without a colored `secondary` derives it from the neutral
        # ramp; show that resolved color so the field is populated (and
        # editable) rather than blank. Clear it to go back to neutral-derived.
        if not family.secondary:
            self.rows["secondary"].set_value(self.style.colors.secondary)

    # ----- save / export -----------------------------------------------------

    def _theme_key(self):
        return self.theme_name.get().lower().replace(" ", "")

    def save_theme(self):
        """Persist the current Theme spec to the user theme store (user.py) and
        register it live as `<name>-light` / `<name>-dark`."""
        name = self._theme_key()
        if not name:
            Messagebox.ok("Please enter a theme name.", "Save theme", parent=self)
            return
        if name in user.USER_THEME_SPECS:
            result = Messagebox.okcancel(
                title="Save Theme", alert=True,
                message=f"Overwrite existing theme {name}?",
            )
            if result == "Cancel":
                return

        spec = self._spec()
        user.USER_THEME_SPECS[name] = spec
        self._write_user_file()

        for definition in Theme(name=name, **spec).to_definitions():
            self.style.register_theme(definition)
        target = f"{name}-{self._mode()}"
        if target in self.style.theme_names():
            self.style.theme_use(target)
        Messagebox.ok(f"The theme {name} has been saved.", "Save theme", parent=self)

    def _write_user_file(self):
        """Rewrite themes/user.py with the current spec + legacy dict stores."""
        header = (
            '"""User-defined custom theme storage for ttkbootstrap.\n\n'
            'USER_THEME_SPECS holds 2.0 semantic-anchor Theme specs (managed by\n'
            'ttkcreator); USER_THEMES holds legacy 16-key dicts. Both are loaded\n'
            'at startup. You may also hand-edit this file.\n"""\n\n'
        )
        content = (
            header
            + "USER_THEME_SPECS = "
            + json.dumps(user.USER_THEME_SPECS, indent=4)
            + "\n\nUSER_THEMES = "
            + json.dumps(user.USER_THEMES, indent=4)
            + "\n"
        )
        with open(user.__file__, "w", encoding="utf-8") as f:
            f.write(content)

    def export_user_themes(self):
        """Export the user theme store file (user.py)."""
        inpath = Path(user.__file__)
        outpath = asksaveasfilename(
            initialdir="/", initialfile="user.py",
            filetypes=[("python", "*.py")],
        )
        if outpath:
            shutil.copyfile(inpath, outpath)
            Messagebox.ok(
                parent=self, title="Export",
                message="User themes have been exported.",
            )

    def import_user_themes(self):
        """Import a user theme store file over the current user.py."""
        inpath = askopenfilename(
            initialdir="/", initialfile="user.py",
            filetypes=[("python", "*.py")],
        )
        confirm = Messagebox.okcancel(
            title="Import",
            message="This import will overwrite the existing user themes. Ok to import?",
        )
        if confirm == "OK" and inpath:
            shutil.copyfile(inpath, Path(user.__file__))
            Messagebox.ok(
                parent=self, title="Import",
                message="User themes have been imported. Restart to load them.",
            )

    def theme_to_source(self, name):
        """Render the current spec as a `Theme(...).register()` Python snippet."""
        spec = self._spec()
        lines = ["import ttkbootstrap as ttk", "", "ttk.Theme(", f'    name="{name}",']
        for role in ("primary", "success", "info", "warning", "danger"):
            if spec[role]:
                lines.append(f'    {role}="{spec[role]}",')
        if spec.get("secondary"):
            lines.append(f'    secondary="{spec["secondary"]}",')
        lines.append(f'    neutral="{spec["neutral"]}",')
        for mode in ("light", "dark"):
            block = spec.get(mode)
            if block:
                lines.append(
                    f'    {mode}=dict(background="{block["background"]}", '
                    f'foreground="{block["foreground"]}"),'
                )
        lines.append(").register()")
        return "\n".join(lines)

    def export_theme_as_python_file(self):
        """Export the current theme as a `Theme(...)` Python file."""
        name = self._theme_key()
        code = self.theme_to_source(name)
        filepath = asksaveasfilename(
            defaultextension=".py",
            initialfile=f"{name}_theme.py",
            filetypes=[("Python files", "*.py")],
            title="Save Theme As Python File",
        )
        if not filepath:
            return
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(code + "\n")
            Messagebox.ok(
                parent=self, title="Export Successful",
                message=f"Theme exported to {filepath}",
            )
        except Exception as e:
            Messagebox.ok(
                parent=self, title="Export Failed",
                message=f"Failed to save file: {e}", alert=True,
            )


class ColorRow(ttk.Frame):
    """One editable color: a swatch, a hex entry, and a color picker. `key` maps
    onto a Theme field in `ThemeCreator._spec()`. An empty value is allowed
    (e.g. an omitted `secondary`)."""

    def __init__(self, master, key, label):
        """Build the label, color patch, hex entry, and picker button for `key`."""
        super().__init__(master, padding=(5, 2))
        self.key = key
        self.color_value = ""

        ttk.Label(self, text=label, width=14).pack(side=LEFT)
        # A fixed color sample. It must NOT follow the theme (it shows the color
        # being edited), so opt it out of the theme walk -- otherwise every
        # temp-theme switch repaints this tk.Frame to the theme background.
        self.patch = Frame(
            master=self, width=24, highlightthickness=1,
            highlightbackground="#888888",
        )
        self.patch._tb_no_autostyle = True
        self.patch.pack(side=LEFT, fill=Y, padx=4, pady=2)
        self.entry = ttk.Entry(self, width=12)
        self.entry.pack(side=LEFT, fill=X, expand=YES)
        self.entry.bind("<FocusOut>", self.enter_color)
        self.entry.bind("<Return>", self.enter_color)
        ttk.Button(
            self, text="...", bootstyle=SECONDARY, command=self.pick_color,
        ).pack(side=LEFT, padx=2)

    def set_value(self, value):
        """Set the color without firing <<ColorSelected>> (bulk load)."""
        self.color_value = value or ""
        self.update_patch_color()

    def pick_color(self):
        """Open the OS color picker and apply the chosen color."""
        color = askcolor(color=self.color_value or None)
        if color[1]:
            self.color_value = color[1].lower()
            self.update_patch_color()
            self.event_generate("<<ColorSelected>>")

    def enter_color(self, *_):
        """Apply the hex value typed into the entry."""
        self.color_value = self.entry.get().strip().lower()
        self.update_patch_color()
        self.event_generate("<<ColorSelected>>")

    def update_patch_color(self):
        """Sync the entry text and swatch color to `color_value`."""
        self.entry.delete(0, END)
        self.entry.insert(END, self.color_value)
        if self.color_value:
            try:
                self.patch.configure(background=self.color_value)
            except Exception:
                pass


class DemoWidgets(ttk.Frame):
    """Builds a frame containing an example of most ttkbootstrap widgets
    with various styles and states applied.
    """

    ZEN = """Beautiful is better than ugly. 
    Explicit is better than implicit. 
    Simple is better than complex. 
    Complex is better than complicated.
    Flat is better than nested. 
    Sparse is better than dense.  
    Readability counts.
    Special cases aren't special enough to break the rules.
    Although practicality beats purity.
    Errors should never pass silently.
    Unless explicitly silenced.
    In the face of ambiguity, refuse the temptation to guess.
    There should be one-- and preferably only one --obvious way to do it.
    Although that way may not be obvious at first unless you're Dutch.
    Now is better than never.
    Although never is often better than *right* now.
    If the implementation is hard to explain, it's a bad idea.
    If the implementation is easy to explain, it may be a good idea.
    Namespaces are one honking great idea -- let's do more of those!"""

    def __init__(self, master, style):
        """Build the left and right preview panels."""
        super().__init__(master)

        self.style: ttk.Style = style
        self.create_left_frame()
        self.create_right_frame()

    def create_right_frame(self):
        """Create the button and input-widget preview column."""
        container = ttk.Frame(self)
        container.pack(side=RIGHT, fill=BOTH, expand=YES, padx=5)

        # demonstrates various button styles
        btn_group = ttk.Labelframe(
            master=container, text="Buttons", padding=(10, 5)
        )
        btn_group.pack(fill=X)

        menu = ttk.Menu(self)
        for i, t in enumerate(self.style.theme_names()):
            menu.add_radiobutton(label=t, value=i)

        default = ttk.Button(master=btn_group, text="solid button")
        default.pack(fill=X, pady=5)
        default.focus_set()

        mb = ttk.Menubutton(
            master=btn_group,
            text="solid menubutton",
            bootstyle=SECONDARY,
            menu=menu,
        )
        mb.pack(fill=X, pady=5)

        cb = ttk.Checkbutton(
            master=btn_group,
            text="solid toolbutton",
            bootstyle="success-toolbutton",
        )
        cb.invoke()
        cb.pack(fill=X, pady=5)

        ob = ttk.Button(
            master=btn_group, text="outline button", bootstyle="info-outline"
        )
        ob.pack(fill=X, pady=5)

        mb = ttk.Menubutton(
            master=btn_group,
            text="outline menubutton",
            bootstyle="warning-outline",
            menu=menu,
        )
        mb.pack(fill=X, pady=5)

        cb = ttk.Checkbutton(
            master=btn_group,
            text="outline toolbutton",
            bootstyle="success-outline-toolbutton",
        )
        cb.pack(fill=X, pady=5)

        lb = ttk.Button(master=btn_group, text="link button", bootstyle=LINK)
        lb.pack(fill=X, pady=5)

        cb1 = ttk.Checkbutton(
            master=btn_group,
            text="rounded toggle",
            bootstyle="success-round-toggle",
        )
        cb1.invoke()
        cb1.pack(fill=X, pady=5)

        cb2 = ttk.Checkbutton(
            master=btn_group, text="squared toggle", bootstyle="square-toggle"
        )
        cb2.pack(fill=X, pady=5)
        cb2.invoke()

        input_group = ttk.Labelframe(
            master=container, text="Other input widgets", padding=10
        )
        input_group.pack(fill=BOTH, pady=(10, 5), expand=YES)
        entry = ttk.Entry(input_group)
        entry.pack(fill=X)
        entry.insert(END, "entry widget")

        password = ttk.Entry(master=input_group, show="•")
        password.pack(fill=X, pady=5)
        password.insert(END, "password")

        spinbox = ttk.Spinbox(master=input_group, from_=0, to=100)
        spinbox.pack(fill=X)
        spinbox.set(45)

        cbo = ttk.Combobox(
            master=input_group,
            text=self.style.theme.name,
            values=self.style.theme_names(),
        )
        cbo.pack(fill=X, pady=5)
        cbo.current(self.style.theme_names().index(self.style.theme.name))

        de = ttk.DateEntry(input_group)
        de.pack(fill=X)

    def create_left_frame(self):
        """Create all the left frame widgets"""
        container = ttk.Frame(self)
        container.pack(side=LEFT, fill=BOTH, expand=YES, padx=5)

        # demonstrates all color options inside a label
        color_group = ttk.Labelframe(
            master=container, text="Theme color options", padding=10
        )
        color_group.pack(fill=X, side=TOP)
        for color in self.style.colors:
            cb = ttk.Button(color_group, text=color, bootstyle=color)
            cb.pack(side=LEFT, expand=YES, padx=5, fill=X)

        # demonstrates all radiobutton widgets active and disabled
        cr_group = ttk.Labelframe(
            master=container, text="Checkbuttons & radiobuttons", padding=10
        )
        cr_group.pack(fill=X, pady=10, side=TOP)
        cr1 = ttk.Checkbutton(cr_group, text="selected")
        cr1.pack(side=LEFT, expand=YES, padx=5)
        cr1.invoke()
        cr2 = ttk.Checkbutton(cr_group, text="deselected")
        cr2.pack(side=LEFT, expand=YES, padx=5)
        cr3 = ttk.Checkbutton(cr_group, text="disabled", state=DISABLED)
        cr3.pack(side=LEFT, expand=YES, padx=5)
        cr4 = ttk.Radiobutton(cr_group, text="selected", value=1)
        cr4.pack(side=LEFT, expand=YES, padx=5)
        cr4.invoke()
        cr5 = ttk.Radiobutton(cr_group, text="deselected", value=2)
        cr5.pack(side=LEFT, expand=YES, padx=5)
        cr6 = ttk.Radiobutton(
            cr_group, text="disabled", value=3, state=DISABLED
        )
        cr6.pack(side=LEFT, expand=YES, padx=5)

        # demonstrates the treeview and notebook widgets
        ttframe = ttk.Frame(container)
        ttframe.pack(pady=5, fill=X, side=TOP)
        table_data = [
            ("South Island, New Zealand", 1),
            ("Paris", 2),
            ("Bora Bora", 3),
            ("Maui", 4),
            ("Tahiti", 5),
        ]
        tv = ttk.Treeview(
            master=ttframe, columns=[0, 1], show="headings", height=5
        )
        for row in table_data:
            tv.insert("", END, values=row)
        tv.selection_set("I001")
        tv.heading(0, text="City")
        tv.heading(1, text="Rank")
        tv.column(0, width=300)
        tv.column(1, width=70, anchor=CENTER)
        tv.pack(side=LEFT, anchor=NE, fill=X)

        nb = ttk.Notebook(ttframe)
        nb.pack(side=LEFT, padx=(10, 0), expand=YES, fill=BOTH)
        nb_text = (
            "This is a notebook tab.\nYou can put any widget you want here."
        )
        nb.add(ttk.Label(nb, text=nb_text), text="Tab 1", sticky=NW)
        nb.add(
            child=ttk.Label(nb, text="A notebook tab."),
            text="Tab 2",
            sticky=NW,
        )
        nb.add(ttk.Frame(nb), text="Tab 3")
        nb.add(ttk.Frame(nb), text="Tab 4")
        nb.add(ttk.Frame(nb), text="Tab 5")

        # text widget
        txt = ttk.Text(master=container, height=5, width=50, wrap="none")
        txt.insert(END, DemoWidgets.ZEN)
        txt.pack(side=LEFT, anchor=NW, pady=5, fill=BOTH, expand=YES)

        # demonstrates scale, progressbar, and meter, and scrollbar widgets
        lframe_inner = ttk.Frame(container)
        lframe_inner.pack(fill=BOTH, expand=YES, padx=10)
        scale = ttk.Scale(
            master=lframe_inner, orient=HORIZONTAL, value=75, from_=100, to=0
        )
        scale.pack(fill=X, pady=5, expand=YES)

        ttk.Progressbar(
            master=lframe_inner,
            orient=HORIZONTAL,
            value=50,
        ).pack(fill=X, pady=5, expand=YES)

        ttk.Progressbar(
            master=lframe_inner,
            orient=HORIZONTAL,
            value=75,
            bootstyle="success-striped",
        ).pack(fill=X, pady=5, expand=YES)

        m = ttk.Meter(
            master=lframe_inner,
            metersize=150,
            amountused=45,
            subtext="meter widget",
            bootstyle="info",
            interactive=True,
        )
        m.pack(pady=10)

        sb = ttk.Scrollbar(
            master=lframe_inner,
            orient=HORIZONTAL,
        )
        sb.set(0.1, 0.9)
        sb.pack(fill=X, pady=5, expand=YES)

        sb = ttk.Scrollbar(
            master=lframe_inner, orient=HORIZONTAL, bootstyle="danger-round"
        )
        sb.set(0.1, 0.9)
        sb.pack(fill=X, pady=5, expand=YES)


if __name__ == "__main__":
    creator = ThemeCreator()
    creator.mainloop()
