import tkinter as tk
from tkinter.messagebox import showinfo, showerror
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter.messagebox import askokcancel
import ttkbootstrap as ttk
from ttkbootstrap import utility
from tkinter.colorchooser import askcolor
from ttkbootstrap.themes import standard
from ttkbootstrap.themes import user
from ttkbootstrap.style import ThemeDefinition
from pathlib import Path
from uuid import uuid4
import shutil

utility.enable_high_dpi_awareness()


class ThemeCreator(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("TTK Creator")
        self.style = ttk.Style()

        self.root = ttk.Frame(self, padding=5)
        self.root.pack(fill=tk.BOTH, expand=tk.YES, padx=10, pady=10)

        self.configure_frame = ttk.Frame(self.root, padding=5)
        self.configure_frame.pack(
            side=tk.LEFT, fill=tk.BOTH, expand=tk.YES, padx=10, pady=10)

        self.demo_frame = ttk.Frame(self.root)
        self.demo_frame.pack(side=tk.LEFT, fill=tk.BOTH,
                             expand=tk.YES, padx=10, pady=10)

        setup_demo(self.demo_frame).pack(fill=tk.BOTH, expand=tk.YES)

        self.setup()

    def setup(self):
        # menu
        self.menu = tk.Menu()
        self.menu.add_command(label='Save', command=self.save_theme)
        self.menu.add_command(label='Reset', command=self.change_base_theme)
        self.menu.add_command(label='Import', command=self.import_user_themes)
        self.menu.add_command(label='Export', command=self.export_user_themes)
        self.configure(menu=self.menu)

        # user theme name
        f1 = ttk.Frame(self.configure_frame, padding=(5, 2))
        ttk.Label(f1, text="name", width=12).pack(side=tk.LEFT)
        self.theme_name = ttk.Entry(f1)
        self.theme_name.insert(tk.END, 'new theme')
        self.theme_name.pack(side=tk.LEFT, fill=tk.X, expand=tk.YES)
        f1.pack(fill=tk.X, expand=tk.YES)

        # base theme
        f2 = ttk.Frame(self.configure_frame, padding=(5, 2))
        ttk.Label(f2, text="base theme", width=12).pack(side=tk.LEFT)
        self.base_theme = ttk.Combobox(f2, values=self.style.theme_names())
        self.base_theme.insert(tk.END, 'flatly')
        self.base_theme.pack(side=tk.LEFT, fill=tk.X, expand=tk.YES)
        f2.pack(fill=tk.X, expand=tk.YES, pady=(0, 15))
        self.base_theme.bind('<<ComboboxSelected>>', self.change_base_theme)

        # color options
        self.color_rows = []
        for color in self.style.colors.label_iter():
            row = ColorRow(self.configure_frame, color)
            self.color_rows.append(row)
            row.pack(fill=tk.BOTH, expand=tk.YES)
            row.bind("<<ColorSelected>>", self.create_temp_theme)

    def create_temp_theme(self, *args):
        themename = str(uuid4()).replace('-', '')[:10]
        colors = {}
        for row in self.color_rows:
            colors[row.label['text']] = row.color_value
        definition = ThemeDefinition(themename, colors, self.style.theme.type)
        self.style.register_theme(definition)
        self.style.theme_use(themename)
        self.update_color_patches()

    def change_base_theme(self, *args):
        themename = self.base_theme.get()
        self.style.theme_use(themename)
        self.update_color_patches()

    def update_color_patches(self):
        for row in self.color_rows:
            row.color_value = self.style.colors.get(row.label['text'])
            row.update_patch_color()

    def export_user_themes(self):
        """Export user themes"""
        inpath = Path(user.__file__)
        outpath = asksaveasfilename(
            initialdir='/',
            initialfile='user.py',
            filetypes=[('python', '*.py')]
        )
        if outpath:
            shutil.copyfile(inpath, outpath)
            showinfo(
                parent=self,
                title='Export',
                message="User themes have been exported."
            )

    def import_user_themes(self):
        """Import user themes"""
        outpath = Path(user.__file__)
        inpath = askopenfilename(
            initialdir='/',
            initialfile='user.py',
            filetypes=[('python', '*.py')]
        )
        confirm = askokcancel(
            title="Import",
            message="This import will overwrite the existing user themes. Ok to import?"
        )
        if confirm and inpath:
            shutil.copyfile(inpath, outpath)
            showinfo(
                parent=self,
                title='Export',
                message="User themes have been imported."
            )

    def save_theme(self):
        """Save the current settings as a new theme. Warn using if 
        saving will overwrite existing theme."""
        name = self.theme_name.get().lower().replace(' ', '')

        if name in user.USER_THEMES:
            showerror(title='Save Theme',
                      message=f'The theme {name} already exists.')
            return

        colors = {}
        for row in self.color_rows:
            colors[row.label['text']] = row.color_value

        theme = {
            name: {
                "type": self.style.theme.type,
                "colors": colors
            }
        }
        filepath = Path(user.__file__)
        user.USER_THEMES.update(theme)
        standard.STANDARD_THEMES[name] = theme[name]
        output = f'USER_THEMES={str(user.USER_THEMES)}'
        filepath.write_text(output, encoding='utf-8')
        
        definition = ThemeDefinition(name, colors, self.style.theme.type)
        self.style.register_theme(definition)
        self.style.theme_use(name)
        self.base_theme.configure(values=self.style.theme_names())

        showinfo(title='Save Theme',
                 message=f'The theme {name} has been created')

    def run(self):
        self.configure_frame.mainloop()


class ColorRow(ttk.Frame):

    def __init__(self, master, color):
        super().__init__(master, padding=(5, 2))
        self.colorname = color
        self.style = ttk.Style()
        self.label = ttk.Label(self, text=color, width=12)
        self.label.pack(side=tk.LEFT)

        self.patch = tk.Frame(
            self, background=self.style.colors.get(color), width=15)
        self.patch.pack(side=tk.LEFT, fill=tk.BOTH, padx=2)

        self.entry = ttk.Entry(self, width=12)
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=tk.YES)
        self.entry.bind('<FocusOut>', self.enter_color)

        self.color_picker = ttk.Button(
            master=self,
            text='🎨',
            bootstyle='secondary',
            command=self.pick_color
        )
        self.color_picker.pack(side=tk.LEFT, padx=2)

        # initial setup
        self.color_value = self.style.colors.get(color)
        self.update_patch_color()

    def pick_color(self):
        color = askcolor(color=self.color_value)
        if color[1]:
            self.color_value = color[1]
            self.update_patch_color()
            self.event_generate("<<ColorSelected>>")

    def enter_color(self, *args):
        try:
            self.color_value = self.entry.get().lower()
            self.update_patch_color()
        except:
            self.color_value = self.style.colors.get(self.label['text'])
            self.update_patch_color()

    def update_patch_color(self):
        self.entry.delete(0, tk.END)
        self.entry.insert(tk.END, self.color_value)
        self.patch.configure(background=self.color_value)


def setup_demo(master):

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

    root = ttk.Frame(master)

    style = ttk.Style()
    theme_names = style.theme_names()

    lframe = ttk.Frame(root, padding=5)
    lframe.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.YES)

    rframe = ttk.Frame(root, padding=5)
    rframe.pack(side=tk.RIGHT, fill=tk.BOTH, expand=tk.YES)

    color_group = ttk.Labelframe(
        master=lframe,
        text="Theme color options",
        padding=10
    )
    color_group.pack(fill=tk.X, side=tk.TOP)

    for color in style.colors:
        cb = ttk.Button(color_group, text=color, bootstyle=color)
        cb.pack(side=tk.LEFT, expand=tk.YES, padx=5, fill=tk.X)

    rb_group = ttk.Labelframe(
        lframe, text="Checkbuttons & radiobuttons", padding=10)
    rb_group.pack(fill=tk.X, pady=10, side=tk.TOP)

    check1 = ttk.Checkbutton(rb_group, text="selected")
    check1.pack(side=tk.LEFT, expand=tk.YES, padx=5)
    check1.invoke()
    check2 = ttk.Checkbutton(rb_group, text="deselected")
    check2.pack(side=tk.LEFT, expand=tk.YES, padx=5)
    check3 = ttk.Checkbutton(rb_group, text="disabled", state=tk.DISABLED)
    check3.pack(side=tk.LEFT, expand=tk.YES, padx=5)

    radio1 = ttk.Radiobutton(rb_group, text="selected", value=1)
    radio1.pack(side=tk.LEFT, expand=tk.YES, padx=5)
    radio1.invoke()
    radio2 = ttk.Radiobutton(rb_group, text="deselected", value=2)
    radio2.pack(side=tk.LEFT, expand=tk.YES, padx=5)
    radio3 = ttk.Radiobutton(rb_group, text="disabled",
                             value=3, state=tk.DISABLED)
    radio3.pack(side=tk.LEFT, expand=tk.YES, padx=5)

    ttframe = ttk.Frame(lframe)
    ttframe.pack(pady=5, fill=tk.X, side=tk.TOP)

    table_data = [
        ('South Island, New Zealand', 1),
        ('Paris', 2),
        ('Bora Bora', 3),
        ('Maui', 4),
        ('Tahiti', 5)
    ]

    tv = ttk.Treeview(
        master=ttframe,
        columns=[0, 1],
        show='headings',
        height=5
    )
    for row in table_data:
        tv.insert('', tk.END, values=row)

    tv.selection_set('I001')
    tv.heading(0, text='City')
    tv.heading(1, text='Rank')
    tv.column(0, width=300)
    tv.column(1, width=70, anchor=tk.CENTER)
    tv.pack(side=tk.LEFT, anchor=tk.NE, fill=tk.X)

    # # notebook with table and text tabs
    nb = ttk.Notebook(ttframe)
    nb.pack(
        side=tk.LEFT,
        padx=(10, 0),
        expand=tk.YES,
        fill=tk.BOTH
    )
    nb_text = "This is a notebook tab.\nYou can put any widget you want here."
    nb.add(ttk.Label(nb, text=nb_text), text="Tab 1", sticky=tk.NW)
    nb.add(
        child=ttk.Label(nb, text="A notebook tab."),
        text="Tab 2",
        sticky=tk.NW
    )
    nb.add(ttk.Frame(nb), text='Tab 3')
    nb.add(ttk.Frame(nb), text='Tab 4')
    nb.add(ttk.Frame(nb), text='Tab 5')

    # text widget
    txt = tk.Text(
        master=lframe,
        height=5,
        width=50,
        wrap='none'
    )
    txt.insert(tk.END, ZEN)
    txt.pack(
        side=tk.LEFT,
        anchor=tk.NW,
        pady=5,
        fill=tk.BOTH,
        expand=tk.YES
    )
    lframe_inner = ttk.Frame(lframe)
    lframe_inner.pack(
        fill=tk.BOTH,
        expand=tk.YES,
        padx=10
    )
    s1 = ttk.Scale(
        master=lframe_inner,
        orient=tk.HORIZONTAL,
        value=75,
        from_=100,
        to=0
    )
    s1.pack(fill=tk.X, pady=5, expand=tk.YES)

    ttk.Progressbar(
        master=lframe_inner,
        orient=tk.HORIZONTAL,
        value=50,
    ).pack(fill=tk.X, pady=5, expand=tk.YES)

    ttk.Progressbar(
        master=lframe_inner,
        orient=tk.HORIZONTAL,
        value=75,
        bootstyle='success-striped'
    ).pack(fill=tk.X, pady=5, expand=tk.YES)

    m = ttk.Meter(
        master=lframe_inner,
        metersize=150,
        amountused=45,
        subtext='meter widget',
        bootstyle='info',
        interactive=True
    )
    m.pack(pady=10)

    sb = ttk.Scrollbar(
        master=lframe_inner,
        orient=tk.HORIZONTAL,
    )
    sb.set(0.1, 0.9)
    sb.pack(fill=tk.X, pady=5, expand=tk.YES)

    sb = ttk.Scrollbar(
        master=lframe_inner,
        orient=tk.HORIZONTAL,
        bootstyle='danger-round'
    )
    sb.set(0.1, 0.9)
    sb.pack(fill=tk.X, pady=5, expand=tk.YES)

    btn_group = ttk.Labelframe(
        master=rframe,
        text="Buttons",
        padding=(10, 5)
    )
    btn_group.pack(fill=tk.X)

    menu = tk.Menu(root)
    for i, t in enumerate(style.theme_names()):
        menu.add_radiobutton(label=t, value=i)

    default = ttk.Button(
        master=btn_group,
        text="solid button"
    )
    default.pack(fill=tk.X, pady=5)
    default.focus_set()

    mb = ttk.Menubutton(
        master=btn_group,
        text="solid menubutton",
        bootstyle="secondary", menu=menu
    )
    mb.pack(fill=tk.X, pady=5)

    cb = ttk.Checkbutton(
        master=btn_group,
        text="solid toolbutton",
        bootstyle="success-toolbutton",
    )
    cb.invoke()
    cb.pack(fill=tk.X, pady=5)

    ob = ttk.Button(
        master=btn_group,
        text="outline button",
        bootstyle='info-outline'
    )
    ob.pack(fill=tk.X, pady=5)

    mb = ttk.Menubutton(
        master=btn_group,
        text="outline menubutton",
        bootstyle="warning-outline",
        menu=menu
    )
    mb.pack(fill=tk.X, pady=5)

    cb = ttk.Checkbutton(
        master=btn_group,
        text="outline toolbutton",
        bootstyle="success-outline-toolbutton"
    )
    cb.pack(fill=tk.X, pady=5)

    lb = ttk.Button(
        master=btn_group,
        text="link button",
        bootstyle='link'
    )
    lb.pack(fill=tk.X, pady=5)

    cb1 = ttk.Checkbutton(
        master=btn_group,
        text="rounded toggle",
        bootstyle="success-round-toggle",
    )
    cb1.invoke()
    cb1.pack(fill=tk.X, pady=5)

    cb2 = ttk.Checkbutton(
        master=btn_group,
        text="squared toggle",
        bootstyle="square-toggle"
    )
    cb2.pack(fill=tk.X, pady=5)
    cb2.invoke()

    input_group = ttk.Labelframe(
        master=rframe,
        text="Other input widgets",
        padding=10
    )
    input_group.pack(
        fill=tk.BOTH,
        pady=(10, 5),
        expand=tk.YES
    )
    entry = ttk.Entry(input_group)
    entry.pack(fill=tk.X)
    entry.insert(tk.END, "entry widget")

    password = ttk.Entry(
        master=input_group,
        show="•"
    )
    password.pack(fill=tk.X, pady=5)
    password.insert(tk.END, "password")

    spinbox = ttk.Spinbox(
        master=input_group,
        from_=0,
        to=100
    )
    spinbox.pack(fill=tk.X)
    spinbox.set(45)

    cbo = ttk.Combobox(
        master=input_group,
        text=style.theme.name,
        values=theme_names,
    )
    cbo.pack(fill=tk.X, pady=5)
    cbo.current(theme_names.index(style.theme.name))

    de = ttk.DateEntry(input_group)
    de.pack(fill=tk.X)

    return root


if __name__ == '__main__':

    creator = ThemeCreator()
    creator.run()
