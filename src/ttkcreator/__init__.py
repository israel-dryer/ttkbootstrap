"""
Author: Israel Dryer
License: MIT
Copyright (c) 2021 Israel Dryer
"""
import uuid
import json
from ttkbootstrap import Style, Colors, StylerTTK, ThemeDefinition
import tkinter as tk
from tkinter import ttk
from tkinter.colorchooser import askcolor
from tkinter.messagebox import showinfo, showerror
import importlib.resources
from PIL import Image, ImageGrab, ImageDraw, ImageFont, ImageTk
from tkinter.filedialog import asksaveasfilename
from tkinter.messagebox import showwarning
from pathlib import Path
from copy import deepcopy


class CreatorDesignWindow(tk.Toplevel):
    """
    An application for designing and saving user-defined themes for ttk / tkinter.

    DEV NOTES: press the <Insert> key to save a screenshot to images.
    """

    def __init__(self, master):
        super().__init__(master)
        self.title('TTK Creator')
        self.protocol('WM_DELETE_WINDOW', self.master.quit)
        self.style = self.master.style
        self.theme_name = self.master.style.theme_use()
        self.fallback_colors = deepcopy(self.style.colors)
        self.geometry_set = False
        self.bind("<Insert>", self.get_bounding_box)

        # setup application window
        self.window = ttk.Frame(self, name='window', padding=5)
        self.window.pack(expand=False)

        # widget container for selecting theme colors
        self.update_selector_image(color=self.style.colors.selectfg)
        self.color_chooser = self.color_chooser(self.window)
        self.color_chooser.pack(side='left', padx=(0, 10))

        # widget container for displaying selected theme colors
        self.bagel = EverythingBagel(self.window)
        self.bagel.pack(side='left')

        # variables used to update selectors and theme values
        self.vars = {}
        self.create_variables()

        # set screen size after window has been created
        self.after(1000, self.set_geometry)

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
        ttk.Label(name_frame, text='name', width=10).pack(side='left', padx=(0, 10))
        ttk.Entry(name_frame, textvariable='name').pack(fill='x', side='top')

        # Color selectors
        selector_frame = ttk.Frame(chooser, name='selectors')
        selector_frame.pack(fill='x', pady=5)
        for color in self.style.colors.label_iter():
            self.color_selector(selector_frame, color).pack(fill='x', pady=2, side='top')

        # Action Buttons
        button_frame = ttk.Frame(chooser)
        reset_btn = ttk.Button(button_frame, text="Reset", style='warning.TButton', command=self.reset_theme)
        reset_btn.pack(side='left', fill='x', expand='yes', padx=2)
        save_btn = ttk.Button(button_frame, text="Save", style='success.TButton', command=self.save_theme)
        save_btn.pack(side='left', fill='x', expand='yes', padx=2)
        button_frame.pack(fill='x', pady=10)
        return chooser

    def set_geometry(self):
        """
        Set the geometry after the window has been created to fix the size at the appropriate size to fit all
        widgets.
        """
        if not self.geometry_set:
            width = self.winfo_width()
            height = self.winfo_height()
            if width != 1:
                self.geometry(f'{width}x{height}')
                self.geometry_set = True
            else:
                self.after(1000, self.set_geometry)

    def get_selectors(self):
        """
        Return a dictionary of all color selector objects
        """
        return (self.children
                ['window'].children
                ['color_chooser'].children
                ['selectors'].children)

    def update_selector_image(self, color=None):
        """
        Draw the selector image using the packaged `Symbola` font.
        """
        font_size = 16
        with importlib.resources.open_binary('ttkbootstrap', 'Symbola.ttf') as font_path:
            fnt = ImageFont.truetype(font_path, font_size)

        im = Image.new('RGBA', (font_size, font_size))
        draw = ImageDraw.Draw(im)
        draw.text((1, 1), "🎨", font=fnt, fill=color or self.getvar('selectfg'))
        self.image = ImageTk.PhotoImage(im)

        try:
            selectors = self.get_selectors()
            if selectors:
                for color in self.style.colors.label_iter():
                    selectors[color].children['button'].configure(image=self.image)
        except KeyError:
            # selectors have not been created yet
            pass


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
        entry = ttk.Entry(selector, name='entry', textvariable=color_label)
        entry.pack(side='left', fill='x', expand='yes')
        entry.bind('<FocusOut>', lambda event, selector=selector: self.select_color(selector, event))
        btn = ttk.Button(selector, name='button', image=self.image, style='secondary.TButton')
        btn.configure(command=lambda s=selector: self.select_color(s))
        btn.pack(side='right', padx=2)
        return selector

    def select_color(self, selector, event=None):
        """
        Callback for selecting a new color in the color selector. Changes the color patch and updates the related
        theme variable.

        :param selector: the widget container for a color selector
        :param event: the event triggering the select color function
        """
        color_label = selector.children.get('label').cget('text')
        color_patch = selector.children.get('patch')

        if not event:
            # color was changed with palette button
            color = askcolor()
            if color[1]:
                color_value = color[1]
                color_patch.configure(background=color_value)
                self.setvar(color_label, color_value)
                return
        else:
            # color was changed with user input
            color_value = self.getvar(color_label)
            if len(color_value) == 4 or len(color_value) == 7:
                # hex color is the correct length
                self.setvar(color_label, color_value)
                try:
                    color_patch.configure(background=color_value)
                except Exception:
                    # Not a valid color, assign default
                    color_value = self.fallback_colors.get(color_label)
                    color_patch.configure(background=color_value)
                    self.setvar(color_label, color_value)
            else:
                # hex color is not the correct length, assign default color
                color_value = self.fallback_colors.get(color_label)
                color_patch.configure(background=color_value)
                self.setvar(color_label, color_value)

    def create_variables(self):
        """
        Create variables to store theme settings
        """
        themename = self.style.theme_use()
        themesettings = self.style._theme_definitions.get(themename)
        self.vars['name'] = tk.StringVar(name='name', value='New Theme')
        self.vars['font'] = tk.StringVar(name='font', value=themesettings.font)
        self.vars['type'] = tk.StringVar(name='type', value=themesettings.type)

        for color in self.style.colors.label_iter():
            self.vars[color] = tk.StringVar(name=color, value=self.style.colors.get(color))
            self.vars[color].trace_add('write', self.update_theme)

    def save_theme(self):
        """
        Save the current settings as a new theme. Warn using if saving will overwrite existing theme.
        """
        name = self.getvar('name').lower().replace(' ', '')

        raw_json = importlib.resources.read_text('ttkbootstrap', 'themes.json')
        settings = json.loads(raw_json)

        with open(settings['userpath'], encoding='utf-8') as f:
            user_themes = json.load(f)

        theme_names = [t['name'] for t in user_themes['themes']]

        if name in theme_names:
            showerror(title='Save Theme', message=f'The theme {name} already exists.')
            return

        theme = {
            "name": name,
            "font": self.getvar('font'),
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
                "border": self.getvar('border'),
                "inputfg": self.getvar('inputfg'),
                "inputbg": self.getvar('inputbg')
            }}

        user_themes['themes'].append(theme)

        with open(settings['userpath'], 'w', encoding='utf-8') as f:
            json.dump(user_themes, f, indent='\t')
        showinfo(title='Save Theme', message=f'The theme {name} has been created')

    def reset_theme(self):
        """
        Reset all values and variable to the default theme (dark='superhero', light='flatly')
        """
        self.style.theme_use(themename=self.theme_name)
        self.reset_variables()
        self.update_selector_image()
        self.reset_color_patches()

    def reset_variables(self):
        """
        Reset all selector variables to the default theme values
        """
        self.vars['name'].set(value='New Theme')

        for color in self.style.colors.label_iter():
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
        for color in self.style.colors.label_iter():
            selectors[color].children['patch'].configure(background=self.style.colors.get(color))
            selectors[color].children['button'].configure(image=self.image)

    def update_theme(self, var, index, mode):
        """
        A callback function on the variable observer. Update existing theme if existing, otherwise, create a new theme
        and apply to app

        :param var: the name of the tkinter variable observed
        :param index: the index of the item (if an array)
        :param mode: the mode of the trace observer
        """
        theme_id = str(uuid.uuid4())  # a unique (and temporary) identifier for the new theme
        self.update_selector_image()

        try:
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
                border=self.getvar('border'),
                inputfg=self.getvar('inputfg'),
                inputbg=self.getvar('inputbg')
            )
        except Exception:
            return

        try:
            self.style.register_theme(
                ThemeDefinition(
                    name=theme_id,
                    themetype=self.getvar('type'),
                    font=self.getvar('font'),
                    colors=colors))

            # # attach the new theme to the style so that it is not garbage collected!!
            # self.new_style = StylerTTK(self.style, definition)
            self.style.theme_use(themename=theme_id)
        except Exception:
            return

    def get_bounding_box(self, event):
        """
        Take a screenshot of the current demo window and save to images
        """
        # bounding box
        titlebar = 31
        x1 = self.winfo_rootx() - 1
        y1 = self.winfo_rooty() - titlebar
        x2 = x1 + self.winfo_width() + 2
        y2 = y1 + self.winfo_height() + titlebar + 1
        self.save_screenshot([x1, y1, x2, y2])

    def save_screenshot(self, bbox):
        # screenshot
        img = ImageGrab.grab(bbox=bbox)

        # image name
        filename = f'../docs/images/ttkcreator.png'
        print(filename)
        img.save(filename, 'png')


class EverythingBagel(ttk.Notebook):
    """
    A frame that contains all available widgets; themed by the ColorChooser
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tab = ttk.Frame(self, padding=10)
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

        # Widget images
        widget_frame = ttk.Labelframe(self.tab, text='Styled widgets', padding=15)
        widget_frame.pack(fill='both')

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
        spinner.pack(side='left', fill='x', expand='yes', padx=(5, 0))

        # Button
        btn_frame = ttk.Frame(widget_frame)
        b1 = ttk.Button(btn_frame, text='Solid Button')
        b1.pack(side='left', fill='x', expand='yes', padx=(0, 5))

        b2 = ttk.Button(btn_frame, text='Outline Button', style='Outline.TButton')
        b2.pack(side='left', fill='x', expand='yes')
        btn_frame.pack(fill='x', pady=(10, 5))

        # Option Menu
        om_var = tk.StringVar()
        om = ttk.OptionMenu(btn_frame, om_var, 'Option Menu', 'One', 'Two', 'Three')
        om.pack(side='right', fill='x', padx=(5, 0), pady=5)

        # Labelframe
        options_frame = ttk.Frame(widget_frame)
        options_frame.pack(fill='x', pady=10)

        # Radio
        r1 = ttk.Radiobutton(options_frame, value=1, text='Radio 1')
        r1.pack(side='left', fill='x', expand='yes')
        r1.invoke()
        ttk.Radiobutton(options_frame, value=2, text='Radio 2').pack(side='left', fill='x', expand='yes')

        # Checkbutton
        cb1 = ttk.Checkbutton(options_frame, text='Check 1')
        cb1.pack(side='left', fill='x', expand='yes')
        cb1.invoke()  # checked

        cb2 = ttk.Checkbutton(options_frame, text='Check 2')
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
        self.scale_var = tk.StringVar(value=25)  # assign to self so that it's not garbage collected
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
        ttk.Progressbar(widget_frame, variable=self.scale_var).pack(fill='x', pady=(10, 0))


class CreatorBaseChooser(tk.Tk):
    def __init__(self):
        super().__init__()
        self.style = Style()
        self.title('TTK Creator')
        self.geometry(f'819x543')
        self.frame = ttk.Frame(self)
        self.setup()
        # self.eval('tk::PlaceWindow . center')
        self.bind("<Insert>", self.get_bounding_box)

    def setup(self):
        self.frame.pack(fill='both', expand='yes')

        lbl = ttk.Label(self.frame, text='What kind of theme do you want to create?', font='-size 16 -slant italic')
        lbl.pack(side='top', pady=(35, 40))

        self.style.configure('light.Outline.TButton', font='-size 20')
        self.style.configure('dark.TButton', font='-size 20')
        light = ttk.Button(self.frame, text='Light', style='light.Outline.TButton', command=self.create_light_theme)
        light.pack(side='left', expand='yes', fill='both')

        dark = ttk.Button(self.frame, text='Dark', style='dark.TButton', command=self.create_dark_theme)
        dark.pack(side='right', expand='yes', fill='both')

    def create_dark_theme(self):
        """
        Startup the design window with the 'flatly' theme
        """
        valid_user_path = self.check_user_themes_path()
        if not valid_user_path:
            return

        self.style.theme_use(themename='darkly')
        CreatorDesignWindow(self)
        self.withdraw()

    def create_light_theme(self):
        """
        Startup the design window with the 'superhero' theme
        """
        valid_user_path = self.check_user_themes_path()
        if not valid_user_path:
            return

        CreatorDesignWindow(self)
        self.withdraw()

    def save_screenshot(self, bbox):
        # screenshot
        img = ImageGrab.grab(bbox=bbox)

        # image name
        filename = '../../docs/images/ttkcreator-splash.png'
        print(filename)
        img.save(filename, 'png')

    def get_bounding_box(self, event):
        """
        Take a screenshot of the current demo window and save to images
        """
        # bounding box
        titlebar = 31
        x1 = self.winfo_rootx() - 1
        y1 = self.winfo_rooty() - titlebar
        x2 = x1 + self.winfo_width() + 2
        y2 = y1 + self.winfo_height() + titlebar + 1
        self.save_screenshot([x1, y1, x2, y2])

    def check_user_themes_path(self):
        """
        If the user defined themes path does not exists, ask for one

        :returns: is there a valid path for themes or not?
        :rtype: bool
        """
        json_string = importlib.resources.read_text('ttkbootstrap', 'themes.json')
        settings = json.loads(json_string)

        if settings['userpath'] and Path(settings['userpath']).exists():
            return True

        showwarning(title="User Defined Themes", message='Please supply a path to save user-defined themes')
        userpath = asksaveasfilename(parent=self, title='User Defined Themes', defaultextension='json',
                                     initialfile='ttkbootstrap_themes.json', confirmoverwrite=False, )
        if not userpath:
            showwarning(title='User Defined Themes', message='Cannot save user-defined themes without a valid path')
            return False
        else:
            # set the new userpath
            settings['userpath'] = userpath
            with importlib.resources.path('ttkbootstrap', 'themes.json') as path:
                with open(path, 'w', encoding='utf-8') as f:
                    json.dump(settings, f, indent='\t')
            # create the new file if not exists
            if not Path(userpath).exists():
                template = {"themes": []}
                with open(userpath, 'w', encoding='utf-8') as f:
                    json.dump(template, f, indent='\t')
            return True
