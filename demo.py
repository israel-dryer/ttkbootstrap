"""
    An application to demonstrate the available installed themes for TTK

    Author:
        Israel Dryer

    Modfied:
        March 21, 2021

    Themes available:
        - flatly
        - minty
        - litera
        - cosmo
        - lumen
        - simplex
        - sandstone
        - yeti
        - pulse
"""
from izzythemes import Style, ttk
import tkinter as tk


class Demo(Style):
    """An application class for demonstrating styles"""

    def __init__(self):
        super().__init__()
        self.theme_use('pulse')
        self.root = self.master
        self.root.title('Izzy Themes')
        self.root.geometry('600x675')
        self.theme_name = tk.StringVar()
        self.theme_name.set(self.theme_use())
        self.setup()

    def setup(self):
        ttk.Scrollbar(self.root).pack(side='right', fill='y')
        self.nb = ttk.Notebook(self.root)
        self.nb.pack(fill='both', expand='yes')
        tab = self.create_themed_tab()
        self.nb.add(tab, text='Tab 1')
        self.nb.add(ttk.Frame(self.nb), text='Tab 2')
        self.nb.add(ttk.Frame(self.nb), text='Tab 3')

    def change_theme(self, new_theme):
        self.theme_use(new_theme)
        self.theme_name.set(new_theme)

    def checked(self, btn):
        btn_text = "Unchecked" if btn['text'] == "Checked" else "Checked"
        btn.configure(text=btn_text)

    def create_themed_tab(self):
        """Create a return a frame containing themed widgets"""
        tab = ttk.Frame(self.nb, padding=20)
        colors = ['Primary', 'Secondary', 'Success', 'Info', 'Warning', 'Danger']

        header_frame = ttk.Frame(tab)
        header = ttk.Label(header_frame, textvariable=self.theme_name, font='-size 30')
        header.pack(side='left', fill='x', pady=5)
        header_frame.pack(fill='x')

        # Menubutton (select a theme)
        mb = ttk.Menubutton(header_frame, text='Select a theme to preview')
        mb.pack(side='right', fill='x', padx=(0, 5), pady=5)
        mb.menu = tk.Menu(mb)
        mb['menu'] = mb.menu
        for t in self.theme_names():
            mb.menu.add_command(label=t, command=lambda theme_name=t: self.change_theme(theme_name))

        # Available Colors
        color_frame = ttk.Labelframe(tab, text='Colors available in this theme', padding=15)
        for color in colors:
            ttk.Button(color_frame, text=color.title(), style=f'{color.lower()}.TButton').pack(side='left', fill='x',
                                                                                               expand='yes', padx=2)
        color_frame.pack(side='top', fill='x', pady=5)

        # Widget examples
        widget_frame = ttk.Labelframe(tab, padding=15, text='Widget examples')
        widget_frame.pack(fill='x', expand='yes')

        # Label
        ttk.Label(widget_frame, text='This is a label').pack(side='top', fill='x', pady=5)

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
        spinner.pack(side='left', fill='x', expand='yes', padx=(5, 0))

        # Button
        btn_frame = ttk.Frame(widget_frame)
        b1 = ttk.Button(btn_frame, text='Solid Button')
        b1.pack(side='left', fill='x', expand='yes', padx=(0, 5))
        b2 = ttk.Button(btn_frame, text='Outline Button', style='info.Outline.TButton')
        b2.pack(side='left', fill='x', expand='yes')
        btn_frame.pack(fill='x', pady=5)

        # Labelframe
        options_frame = ttk.Frame(widget_frame)
        options_frame.pack(fill='x', pady=5)

        # Radio
        r1 = ttk.Radiobutton(options_frame, value=1, text='Radio one')
        r1.pack(side='left', fill='x', expand='yes')
        r1.invoke()
        r2 = ttk.Radiobutton(options_frame, value=2, text='Radio two')
        r2.pack(side='left', fill='x', expand='yes')

        # Checkbutton
        cb1 = ttk.Checkbutton(options_frame, text='Unchecked')
        cb1.configure(command=lambda: self.checked(cb1))
        cb1.pack(side='left', fill='x', expand='yes')
        cb1.invoke()

        cb2 = ttk.Checkbutton(options_frame, text='Unchecked')
        cb2.configure(command=lambda: self.checked(cb2))
        cb2.pack(side='left', fill='x', expand='yes')

        # Treeview
        tv = ttk.Treeview(widget_frame, height=3)
        tv.pack(fill='x', pady=5)
        tv.heading('#0', text='Example heading')
        tv.insert('', 'end', 'example1', text='Example 1')
        tv.insert('', 'end', 'example2', text='Example 2')
        tv.insert('example2', 'end', text='Example 2 Child 1')
        tv.insert('example2', 'end', text='Example 2 Child 2')

        # Scale
        scale_frame = ttk.Frame(widget_frame)
        scale_var = tk.IntVar(value=25)
        scale = ttk.Scale(scale_frame, variable=scale_var, from_=1, to=100)
        scale.pack(side='left', fill='x', expand='yes', padx=(0, 2))
        scale_frame.pack(side='top', fill='x', pady=5)
        entry = ttk.Entry(scale_frame, textvariable=scale_var, width=4)
        entry.pack(side='right')

        # Combobox
        cbo = ttk.Combobox(widget_frame, values=colors)
        cbo.current(0)
        cbo.pack(fill='x', pady=5)

        # Progressbar
        ttk.Progressbar(widget_frame, value=30).pack(fill='x', pady=5)
        return tab

    def run(self):
        self.root.mainloop()


if __name__ == '__main__':
    demo = Demo()
    demo.run()
