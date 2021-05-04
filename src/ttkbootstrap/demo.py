"""
Author: Israel Dryer
License: MIT
Copyright (c) 2021 Israel Dryer
"""
from ttkbootstrap import Style
import tkinter
from tkinter import ttk

# for taking screenshots
from PIL import ImageGrab


class Demo(Style):
    """
    An application class for demonstrating styles
    """

    def __init__(self):
        super().__init__()
        self.theme_use('lumen')
        self.root = self.master
        self.root.geometry('500x695')
        self.root.protocol("WM_DELETE_WINDOW", self.quit)
        self.root.title('TTK Bootstrap')
        self.theme_name = tkinter.StringVar()
        self.theme_name.set(self.theme_use())
        self.setup()
        self.root.eval('tk::PlaceWindow . center')
        self.root.bind("<Insert>", self.get_bounding_box)
        self.run()

    def __repr__(self):
        return "Demo Application"

    def setup(self):
        sb = ttk.Scrollbar(self.root)
        sb.set(0.1, 0.55)

        sb.pack(side='right', fill='y')
        self.nb = ttk.Notebook(self.root)
        self.nb.pack(fill='both', expand='yes')
        self.tab = self.create_themed_tab()
        self.nb.add(self.tab, text='Tab 1')
        self.nb.add(ttk.Frame(self.nb), text='Tab 2')
        self.nb.add(ttk.Frame(self.nb), text='Tab 3')

    def change_theme(self, new_theme):
        """
        Destroying the widget isn't strictly necessary with pure TTK widgets. However, for this demo, I'm
        explicitly allowing the changing of colors, etc... and because I want the styles to be consistent on underlying
        standard tk widgets, I've choosing to redraw all the widgets in the main tab. You can use other methods or
        avoid this altogether if you're not switch between light and dark themes.
        """
        self.tab.destroy()
        self.theme_use(new_theme)
        self.tab = self.create_themed_tab()
        self.nb.insert(0, self.tab, text='Tab 1')
        self.nb.select(self.nb.tabs()[0])
        self.theme_name.set(new_theme)

    def create_themed_tab(self):
        """
        Create a return a frame containing themed widgets
        """
        tab = ttk.Frame(self.nb, padding=10)
        colors = ['Primary', 'Secondary', 'Success', 'Info', 'Warning', 'Danger']

        header_frame = ttk.Frame(tab, padding=10)
        header = ttk.Label(header_frame, textvariable=self.theme_name, font='-size 30')
        header.pack(side='left', fill='x', pady=5)
        header_frame.pack(fill='x')

        # Menubutton (select a theme)
        mb = ttk.Menubutton(header_frame, text='Select a theme to preview')
        mb.pack(side='right', fill='x', pady=5)
        mb.menu = tkinter.Menu(mb)
        mb['menu'] = mb.menu
        for t in sorted(self._theme_definitions.keys()):
            mb.menu.add_command(label=t, command=lambda theme_name=t: self.change_theme(theme_name))

        # Separator
        ttk.Separator(tab, orient='horizontal').pack(fill='x', pady=(10, 15))

        # Paned Window
        pw = ttk.PanedWindow(tab)
        pw.pack(fill='x')

        # Available Colors
        color_frame = ttk.Labelframe(pw, text='Colors available in this theme', padding=(5, 15))
        for color in colors:
            btn = ttk.Button(color_frame, text=color.title(), style=f'{color.lower()}.TButton')
            btn.pack(side='left', fill='x', expand='yes', padx=2, pady=5)

        pw.add(color_frame)

        # This outer frame will provide an internal buffer between the widget images and the window pane,
        # there is no other way to add internal padding
        widget_outer_frame = ttk.Frame(pw, padding=(0, 10))
        pw.add(widget_outer_frame)

        # Widget images
        widget_frame = ttk.LabelFrame(widget_outer_frame, text='Styled Widgets', padding=10)
        widget_frame.pack(fill='x')

        # Label
        ttk.Label(widget_frame, text='This is a label').pack(side='top', fill='x')

        entry_spin_frame = ttk.Frame(widget_frame)
        entry_spin_frame.pack(fill='x', pady=5)

        # Entry
        entry = ttk.Entry(entry_spin_frame)
        entry.insert('end', 'An entry field with focus ring')
        entry.pack(side='left', fill='x', expand='yes')

        # Spinbox
        spinner_options = ['Spinner option 1', 'Spinner option 2', 'Spinner option 3']
        spinner = ttk.Spinbox(entry_spin_frame, values=spinner_options)
        spinner.set('Spinner option 1')
        spinner.pack(side='right', fill='x', expand='yes', padx=(5, 0))

        # Button
        btn_frame = ttk.Frame(widget_frame)
        b1 = ttk.Button(btn_frame, text='Solid Button')
        b1.pack(side='left', fill='x', expand='yes', padx=(0, 5))

        b2 = ttk.Button(btn_frame, text='Outline Button', style='Outline.TButton')
        b2.pack(side='left', fill='x', expand='yes')
        btn_frame.pack(fill='x', pady=5)

        # Option Menu
        om_var = tkinter.StringVar()
        om = ttk.OptionMenu(btn_frame, om_var, 'Option Menu', *list(self._theme_names))
        om.pack(side='right', fill='x', padx=(5, 0), pady=5)

        # Labelframe
        options_frame = ttk.Frame(widget_frame, padding=(0, 10))
        options_frame.pack(fill='x', pady=5)

        # Radio
        r1 = ttk.Radiobutton(options_frame, value=1, text='Radio one')
        r1.pack(side='left', fill='x', expand='yes')
        r1.invoke()
        r2 = ttk.Radiobutton(options_frame, value=2, text='Radio two')
        r2.pack(side='left', fill='x', expand='yes')

        # Checkbutton
        cb1 = ttk.Checkbutton(options_frame, text='Option 1')
        cb1.pack(side='left', fill='x', expand='yes')
        cb1.invoke()

        cb2 = ttk.Checkbutton(options_frame, text='Option 2')
        cb2.pack(side='left', fill='x', expand='yes')
        cb2.invoke()
        cb2.invoke()

        # Treeview
        tv = ttk.Treeview(widget_frame, height=3)
        tv.pack(fill='x', pady=5)
        tv.heading('#0', text='Example heading')
        tv.insert('', 'end', 'example1', text='Example 1')
        tv.insert('', 'end', 'example2', text='Example 2')
        tv.insert('example2', 'end', text='Example 2 Child 1')
        tv.insert('example2', 'end', text='Example 2 Child 2')
        tv.selection_set('example1')

        # Scale
        scale_frame = ttk.Frame(widget_frame)
        self.scale_var = tkinter.IntVar(value=25)
        scale = ttk.Scale(scale_frame, variable=self.scale_var, from_=1, to=100)
        scale.pack(side='left', fill='x', expand='yes', padx=(0, 2))
        scale_frame.pack(side='top', fill='x', pady=5)
        entry = ttk.Entry(scale_frame, textvariable=self.scale_var, width=4)
        entry.pack(side='right')

        # Combobox
        cbo = ttk.Combobox(widget_frame, values=colors)
        cbo.current(0)
        cbo.pack(fill='x', pady=5)

        # Progressbar
        ttk.Progressbar(widget_frame, variable=self.scale_var, style='Striped.Horizontal.TProgressbar').pack(fill='x', pady=10)
        return tab

    def run(self):
        self.root.mainloop()

    def quit(self):
        # I'm getting an error when closing the application without switching a standard theme ??
        self.root.destroy()

    def get_bounding_box(self, event):
        """
        Take a screenshot of the current demo window and save to images
        """
        # bounding box
        titlebar = 31
        x1 = self.root.winfo_rootx() - 1
        y1 = self.root.winfo_rooty() - titlebar
        x2 = x1 + self.root.winfo_width() + 2
        y2 = y1 + self.root.winfo_height() + titlebar + 1

        self.root.after_idle(self.save_screenshot, [x1, y1, x2, y2])

    def save_screenshot(self, bbox):
        # screenshot
        img = ImageGrab.grab(bbox=bbox)

        # image name
        filename = f'../../docs/images/{self.theme_name.get()}.png'
        img.save(filename, 'png')
        print(filename)  # print for confirmation


if __name__ == '__main__':
    Demo()
