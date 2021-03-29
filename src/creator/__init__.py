"""
Author: Israel Dryer
License: MIT
Copyright (c) 2021 Israel Dryer
"""
from ttkbootstrap import Style, Colors, StylerTTK, ThemeSettings
import tkinter as tk
from tkinter.font import families
from tkinter import ttk
from tkinter.colorchooser import Chooser
from tkinter.messagebox import showinfo, showerror
import importlib.resources
import uuid
import json


class ThemeCreatorTTK(tk.Tk):
    """
    An application for designing and saving user-defined themes for ttk / tkinter.
    """

    def __init__(self):
        super().__init__()
        self.title('Theme Creator TTK')
        self.geometry('958x602')
        self.style = Style()
        self.style.theme_use('lumen')
        self.vars = {}
        self.setup()
        self.eval('tk::PlaceWindow . center')

    def setup(self):
        """
        Setup the application
        """
        self.window = ttk.Frame(self, name='window', padding=5)
        self.window.pack(expand=False)

        # widget container for selecting theme colors
        self.color_chooser = self.color_chooser(self.window)
        self.color_chooser.pack(side='left', padx=(0, 10))

        # widget container for displaying selected theme colors
        self.bagel = EverythingBagel(self.window)
        self.bagel.pack(side='left')

        # variables used to update selectors and theme values
        self.create_variables()

    def color_chooser(self, master):
        """
        Create widget used to select theme colors

        :param master: the parent widget
        :returns: ttk.Frame
        """
        chooser = ttk.Frame(master, name='color_chooser', padding=10)

        # Theme name
        name_frame = ttk.Frame(chooser)
        name_frame.pack(fill='x', pady=5)
        ttk.Label(name_frame, text='theme name', width=10).pack(side='left', padx=(0, 10))
        ttk.Entry(name_frame, textvariable='name').pack(fill='x', side='top')

        # Default font --> not ready to make this available yet. So, all will default to Helvetica
        # font_frame = ttk.Frame(chooser)
        # font_frame.pack(fill='x', pady=(5, 10))
        # ttk.Label(font_frame, text='default font', width=10).pack(side='left', padx=(0, 10))
        # fonts = sorted(families())
        # ttk.Combobox(font_frame, textvariable='font', values=fonts).pack(fill='x', expand='yes', side='left', padx=2)

        # Color selectors
        selector_frame = ttk.Frame(chooser, name='selectors')
        selector_frame.pack(fill='x', pady=5)
        for color in self.style.colors.color_label_iter():
            self.color_selector(selector_frame, color).pack(fill='x', pady=2, side='top')

        # Action Buttons
        button_frame = ttk.Frame(chooser)
        reset_btn = ttk.Button(button_frame, text="Reset", style='warning.TButton', command=self.reset_theme)
        reset_btn.pack(side='left', fill='x', expand='yes', padx=2)
        save_btn = ttk.Button(button_frame, text="Save", style='success.TButton', command=self.save_theme)
        save_btn.pack(side='left', fill='x', expand='yes', padx=2)
        button_frame.pack(fill='x', pady=10)
        return chooser

    def get_selectors(self):
        """
        Return a dictionary of all color selector objects
        """
        return (self.children
                ['window'].children
                ['color_chooser'].children
                ['selectors'].children)

    def color_selector(self, master, color_label):
        """
        A container widget that represents a color selector. This includes a label, a color patch, an entry field,
        and a button for invoking the built-in color chooser.

        :param master: the parent widget
        :param color_label: the name of the color represented by the selector (eg. primary, secondary, info, etc...)
        :returns: ttk.Frame
        """
        selector = ttk.Frame(master, name=color_label)
        color_value = self.style.colors.get(color_label)
        ttk.Label(selector, text=color_label, name='label', width=10).pack(side='left')
        tk.Frame(selector, name='patch', width=10, background=color_value).pack(side='left', fill='y', padx=2)
        ttk.Entry(selector, textvariable=color_label).pack(side='left', fill='x', expand='yes')
        btn = ttk.Button(selector, text="🎨", style='secondary.TButton', width=3)
        btn.configure(command=lambda s=selector: self.select_color(s))
        btn.pack(side='right', padx=2)
        return selector

    def select_color(self, selector):
        """
        Callback for selecting a new color in the color selector. Changes the color patch and updates the related
        theme variable.

        :param selector: the widget container for a color selector
        """
        color_label = selector.children.get('label').cget('text')
        color_patch = selector.children.get('patch')
        chooser = Chooser()
        color = chooser.show()
        if color[1]:
            color_value = color[1]
            color_patch.configure(background=color_value)
            self.setvar(color_label, color_value)

    def create_variables(self):
        """
        Create variables to store theme settings
        """
        self.vars['name'] = tk.StringVar(name='name', value='New Theme')
        self.vars['font'] = tk.StringVar(name='font', value='Helvetica')
        self.vars['type'] = tk.StringVar(name='type', value='light')

        for color in self.style.colors.color_label_iter():
            self.vars[color] = tk.StringVar(name=color, value=self.style.colors.get(color))
            self.vars[color].trace_add('write', self.update_theme)

    def save_theme(self):
        """
        Save the current settings as a new theme. Warn using if saving will overwrite existing theme.
        """
        name = self.getvar('name').lower().replace(' ', '')

        raw_json = importlib.resources.read_text('ttkbootstrap', 'user_themes.json')
        user_themes = json.loads(raw_json)

        theme_names = [t['name'] for t in user_themes['themes']]

        if name in theme_names:
            showerror(title='Save Theme', message=f'The theme {name} already exists.')
            return

        theme = {
            "name": name,
            "font": "Helvetica",
            "type": self.getvar('type'),
            "colors": {
                "primary": self.getvar('primary'),
                "secondary": self.getvar('secondary'),
                "success": self.getvar('success'),
                "info": self.getvar('info'),
                "warning": self.getvar('warning'),
                "danger": self.getvar('danger'),
                "bg": self.getvar('bg'),
                "fg": self.getvar('fg'),
                "selectbg": self.getvar('selectbg'),
                "selectfg": self.getvar('selectfg'),
                "light": self.getvar('light'),
                "border": self.getvar('border'),
                "inputfg": self.getvar('inputfg')
            }
        }
        user_themes['themes'].append(theme)

        with importlib.resources.path('ttkbootstrap', 'user_themes.json') as path:
            with open(path, 'w') as f:
                json.dump(user_themes, f, indent='\t')
        showinfo(title='Save Theme', message=f'The theme {name} has been created')

    def reset_theme(self):
        """
        Reset all values and variable to the default theme (dark='superhero', light='lumen')
        """
        self.style.theme_use('lumen')
        self.reset_variables()
        self.reset_color_patches()

    def reset_variables(self):
        """
        Reset all selector variables to the default theme values
        """
        self.vars['name'].set(value='New Theme')
        self.vars['font'].set('Helvetica')
        self.vars['type'].set('light')

        for color in self.style.colors.color_label_iter():
            var = self.vars[color]
            cbname = var.trace_info()[0][1]
            var.trace_remove('write', cbname)
            var.set(self.style.colors.get(color))
            var.trace_add('write', self.update_theme)

    def reset_color_patches(self):
        """
        Set all patch colors to match the current theme color values
        """
        selectors = self.get_selectors()
        for color in self.style.colors.color_label_iter():
            patch = selectors[color].children['patch']
            patch.configure(background=self.style.colors.get(color))

    def update_theme(self, var, index, mode):
        """
        A callback function on the variable observer. Update existing theme if existing, otherwise, create a new theme
        and apply to app

        :param var: the name of the tkinter variable observed
        :param index: the index of the item (if an array)
        :param mode: the mode of the trace observer
        """
        theme_id = uuid.uuid4()  # a unique (and temporary) identifier for the new theme
        colors = Colors(
            primary=self.getvar('primary'),
            secondary=self.getvar('secondary'),
            success=self.getvar('success'),
            info=self.getvar('info'),
            warning=self.getvar('warning'),
            danger=self.getvar('danger'),
            fg=self.getvar('fg'),
            bg=self.getvar('bg'),
            selectfg=self.getvar('selectfg'),
            selectbg=self.getvar('selectbg'),
            light=self.getvar('light'),
            border=self.getvar('border'),
            inputfg=self.getvar('inputfg'))

        settings = ThemeSettings(name=theme_id, type=self.getvar('inputfg'), font=self.getvar('font'), colors=colors)
        self.new_style = StylerTTK(self.style, settings)
        self.style.theme_use(theme_id)

        """
            This call is forcing the select foreground to turn black, even if foreground is not specified in
            the palette parameters. Calling this will set some of the residual tk colors, such as the combobox 
            popdown, etc... However, due to this select fg issue, I've decided to comment this out for now.
        """
        # self.tk_setPalette(
        #     foreground=self.getvar('fg'),
        #     background=self.getvar('bg'),
        #     activeBackground=self.getvar('selectbg'),
        #     activeForeground=self.getvar('selectfg'),
        #     selectBackground=self.getvar('selectbg'),
        #     selectForeground=self.getvar('selectfg'))


class EverythingBagel(ttk.Notebook):
    """
    A frame that contains all available widgets; themed by the ColorChooser
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tab = ttk.Frame(self, padding=20)
        self.setup()

    def setup(self):
        """Setup the Everything bagel"""
        self.tab.pack(fill='both')  # remove expand
        self.create_widgets()
        self.add(self.tab, text='Tab 1')
        self.add(ttk.Frame(self), text='Tab 2')
        self.add(ttk.Frame(self), text='Tab 3')

    def create_widgets(self):
        """
        Create all widgets contained in Tab 1
        """
        colors = ['Primary', 'Secondary', 'Success', 'Info', 'Warning', 'Danger']

        # Available Colors
        color_frame = ttk.Labelframe(self.tab, text='Colors available in this theme', padding=15)
        for color in colors:
            btn = ttk.Button(color_frame, text=color.title(), style=f'{color.lower()}.TButton')
            btn.pack(side='left', fill='x', expand='yes', padx=2)
        color_frame.pack(side='top', fill='x', pady=5)

        # Widget examples
        widget_frame = ttk.Labelframe(self.tab, padding=15, text='Widget examples')
        widget_frame.pack(fill='both')

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

        b2 = ttk.Button(btn_frame, text='Outline Button', style='Outline.TButton')
        b2.pack(side='left', fill='x', expand='yes')
        btn_frame.pack(fill='x', pady=5)

        # Option Menu
        om_var = tk.StringVar()
        om = ttk.OptionMenu(btn_frame, om_var, 'Option Menu', 'One', 'Two', 'Three')
        om.pack(side='right', fill='x', padx=(5, 0), pady=5)

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
        cb1 = ttk.Checkbutton(options_frame, text='Option 1')
        cb1.pack(side='left', fill='x', expand='yes')
        cb1.invoke()  # checked

        cb2 = ttk.Checkbutton(options_frame, text='Option 2')
        cb2.pack(side='left', fill='x', expand='yes')
        cb2.invoke()
        cb2.invoke()  # unchecked

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
        self.scale_var = tk.StringVar(value=25)
        scale = ttk.Scale(scale_frame, variable=self.scale_var, from_=0, to=100)
        scale.pack(side='left', fill='x', expand='yes', padx=(0, 2))
        scale_frame.pack(side='top', fill='x', pady=5)
        entry = ttk.Entry(scale_frame, textvariable=self.scale_var, width=4)
        entry.pack(side='right')

        # Combobox
        cbo = ttk.Combobox(widget_frame, values=colors)
        cbo.current(0)
        cbo.pack(fill='x', pady=5)

        # Progressbar
        ttk.Progressbar(widget_frame, variable=self.scale_var).pack(fill='x', pady=5)



