

"""
    A Windows OS style color chooser that is cross-platform and which
    presents the palette of theme based colors.

    TODO add spectrum and luminance indicators
    TODO fix bug that is preventing the themed buttons from working
"""
from ttkbootstrap.validation import add_range_validation, add_validation, validator
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import Frame as tkFrame
from tkinter import Button as tkButton
from tkinter import Label as tkLabel
from ttkbootstrap import utility
from collections import namedtuple
from ttkbootstrap import colorutils
from PIL import ImageColor

HUE = 360
SAT = 100
LUM = 100

STD_SHADES = [0.9, 0.8, 0.7, 0.4, 0.3]
STD_COLORS = [
    '#FF0000', '#FFC000', '#FFFF00', '#00B050', 
    '#0070C0', '#7030A0', '#FFFFFF', '#000000'
]

ColorValues = namedtuple('ColorValues', 'h s l r g b hex')

@validator
def validate_color(event):
    try:
        ImageColor.getrgb(event.postchangetext)
        return True
    except:
        return False


class ColorModel:
    RGB = 1
    HSL = 2
    HEX = 3


class ColorChooserFrame(ttk.Frame):

    def __init__(self, master, initialcolor=None, padding=None):
        super().__init__(master, padding=padding)
        self.tframe = ttk.Frame(self, padding=5)
        self.tframe.pack(fill=X)
        self.bframe = ttk.Frame(self, padding=(5, 0, 5, 5))
        self.bframe.pack(fill=X)

        self.notebook = ttk.Notebook(self.tframe)
        self.notebook.pack(fill=BOTH)

        self.style = ttk.Style.get_instance()
        self.colors = self.style.colors
        self.initialcolor = initialcolor or self.colors.bg
        # border color will not change on theme change
        self.bordercolor = self.style.lookup('TNotebook', 'bordercolor')
        
        # color variables
        self.hue = ttk.IntVar(value=0)
        self.sat = ttk.IntVar(value=0)
        self.lum = ttk.IntVar(value=100)
        self.red = ttk.IntVar(value=255)
        self.grn = ttk.IntVar(value=255)
        self.blu = ttk.IntVar(value=255)
        self.hex = ttk.StringVar(value='#FFFFFF')

        # widget sizes (adjusted by widget scaling)
        self.spectrum_height = utility.scale_size(self, 240)
        self.spectrum_width = utility.scale_size(self, 480)
        self.spectrum_point = utility.scale_size(self, 12)

        # build widgets
        spectrum_frame = ttk.Frame(self.notebook)
        self.color_spectrum = self.create_color_spectrum(spectrum_frame)
        self.color_spectrum.pack(fill=X, side=TOP)
        self.luminance_scale = self.create_luminance_scale(self.tframe)
        self.luminance_scale.pack(fill=X)
        self.notebook.add(spectrum_frame, text='Advanced')
        
        themed_colors = [self.colors.get(c) for c in self.style.colors]
        self.themed_swatches = self.create_color_swatches(self.notebook, themed_colors)
        self.standard_swatches = self.create_color_swatches(self.notebook, STD_COLORS)
        self.notebook.add(self.themed_swatches, text='Themed')
        self.notebook.add(self.standard_swatches, text='Standard')
        preview_frame = self.create_color_preview(self.bframe)
        preview_frame.pack(side=LEFT, fill=BOTH, expand=YES, padx=(0, 5))
        self.color_entries = self.create_color_entries(self.bframe)
        self.color_entries.pack(side=RIGHT)

    # widget builder methods
    def create_color_swatches(self, master, colors):

        boxpadx = 2
        boxpady = 0
        padxtotal = len(STD_COLORS)*(boxpadx*2)
        boxwidth = int((self.spectrum_width-padxtotal) / len(STD_COLORS))
        boxheight = int((self.spectrum_height-boxpady) / (len(STD_SHADES)+1))
        self._empty = ttk.PhotoImage(width=boxwidth, height=boxheight)
        container = ttk.Frame(master)

        # create color combinations
        color_rows = [colors]
        lastcol = len(colors)-1
        for l in STD_SHADES:
            lum = int(l*LUM)
            row = []
            for color in colors:
                color = colorutils.update_hsl_value(
                    color=color, 
                    lum=lum, 
                    inmodel='hex', 
                    outmodel='hex'
                )
                row.append(color)
            color_rows.append(row)

        # themed colors - regular colors
        for row in color_rows:
            rowframe = ttk.Frame(container)
            for j, color in enumerate(row):
                swatch = tkButton(
                    master=rowframe, 
                    bg=color, 
                    bd=0, 
                    autostyle=False, 
                    activebackground=color,
                    highlightthickness=0,
                    image=self._empty, 
                    overrelief=FLAT
                )
                swatch['command'] = lambda x=swatch: self.on_press_color_swatch(x)
                if j == 0:
                    swatch.pack(side=LEFT, padx=(0, boxpadx))
                elif j == lastcol:
                    swatch.pack(side=LEFT, padx=(boxpadx, 0))
                else:
                    swatch.pack(side=LEFT, padx=boxpadx)
            rowframe.pack(fill=X, expand=YES)

        return container

    def create_color_preview(self, master):
        container = ttk.Frame(master)
        old = tkFrame(
            master=container, 
            relief=FLAT, 
            bd=2, 
            highlightthickness=1,
            highlightbackground=self.bordercolor,
            bg=self.initialcolor, 
            autostyle=False
        )
        old.pack(side=LEFT, fill=BOTH, expand=YES, padx=(0, 2))
        contrastfg = colorutils.contrast_color(
            color=self.initialcolor, 
            model='hex', 
            darkcolor=self.colors.selectfg, 
            lightcolor=self.colors.fg
        )
        tkLabel(
            master=old, 
            text='Current', 
            background=self.initialcolor, 
            foreground=contrastfg, 
            autostyle=False,
            width=7
        ).pack(anchor=NW)
        self.color_preview = tkFrame(
            master=container, 
            relief=FLAT, 
            bd=2, 
            highlightthickness=1,
            highlightbackground=self.bordercolor,
            bg=self.initialcolor, 
            autostyle=False
        )
        self.color_preview.pack(side=LEFT, fill=BOTH, expand=YES, padx=(2, 0))
        self.color_preview_lbl = tkLabel(
            master=self.color_preview, 
            text='New', 
            background=self.initialcolor, 
            foreground=contrastfg, 
            autostyle=False,
            width=7
        )
        self.color_preview_lbl.pack(anchor=NW)
    
        return container

    def create_color_entries(self, master):
        container = ttk.Frame(master)
        for x in range(4):
            container.columnconfigure(x, weight=1)
        # value labels
        lbl_cnf = {'master': container, 'anchor': E}
        ttk.Label(**lbl_cnf, text='Hue:').grid(row=0, column=0, sticky=E)
        ttk.Label(**lbl_cnf, text='Sat:').grid(row=1, column=0, sticky=E)
        ttk.Label(**lbl_cnf, text='Lum:').grid(row=2, column=0, sticky=E)
        ttk.Label(**lbl_cnf, text='Hex:').grid(row=3, column=0, sticky=E)
        ttk.Label(**lbl_cnf, text='Red:').grid(row=0, column=2, sticky=E)
        ttk.Label(**lbl_cnf, text='Green:').grid(row=1, column=2, sticky=E)
        ttk.Label(**lbl_cnf, text='Blue:').grid(row=2, column=2, sticky=E)
        # value spinners
        rgb_cnf = {'master': container, 'from_': 0, 'to': 255, 'width': 3}
        sl_cnf = {'master': container, 'from_': 0, 'to': 100, 'width': 3}
        hue_cnf = {'master': container, 'from_': 0, 'to': 360, 'width': 3}
        sb_hue = ttk.Spinbox(**hue_cnf, textvariable=self.hue)
        sb_hue.grid(row=0, column=1, padx=4, pady=2, sticky=EW)
        sb_sat = ttk.Spinbox(**sl_cnf, textvariable=self.sat)
        sb_sat.grid(row=1, column=1, padx=4, pady=2, sticky=EW)
        sb_lum = ttk.Spinbox(**sl_cnf, textvariable=self.lum)
        sb_lum.grid(row=2, column=1, padx=4, pady=2, sticky=EW)
        sb_red = ttk.Spinbox(**rgb_cnf, textvariable=self.red)
        sb_red.grid(row=0, column=3, padx=4, pady=2, sticky=EW)
        sb_grn = ttk.Spinbox(**rgb_cnf, textvariable=self.grn)
        sb_grn.grid(row=1, column=3, padx=4, pady=2, sticky=EW)
        sb_blu = ttk.Spinbox(**rgb_cnf, textvariable=self.blu)
        sb_blu.grid(row=2, column=3, padx=4, pady=2, sticky=EW)
        ent_hex = ttk.Entry(container, textvariable=self.hex)
        ent_hex.grid(row=3, column=1, padx=4, columnspan=3, pady=2, sticky=EW)
        add_range_validation(sb_hue, 0, 360)
        add_range_validation(sb_sat, 0, 100)
        add_range_validation(sb_lum, 0, 100)
        add_validation(ent_hex, validate_color)
        
        # event binding for updating colors on value change
        for sb in [sb_hue, sb_sat, sb_lum]:
            for sequence in ['<<Increment>>', '<<Decrement>>', '<Return>', '<KP_Enter>']:
                sb.bind(
                    sequence=sequence, 
                    func=lambda _, w=sb: self.on_entry_value_change(w, ColorModel.HSL), 
                    add="+"
                )
        for sb in [sb_red, sb_grn, sb_blu]:
            for sequence in ['<<Increment>>', '<<Decrement>>', '<Return>', '<KP_Enter>']:
                sb.bind(
                    sequence=sequence, 
                    func=lambda _, w=sb: self.on_entry_value_change(w, ColorModel.RGB), 
                    add="+"
                )
            add_range_validation(sb, 0, 255)
        for sequence in ['<Return>', '<KP_Enter>']:
            ent_hex.bind(
                sequence=sequence,
                func=lambda _, w=ent_hex: self.on_entry_value_change(w, ColorModel.HEX),
                add="+"
            )
        return container

    def create_color_spectrum(self, master):
        width = self.spectrum_width
        height = self.spectrum_height
        xf = yf = self.spectrum_point
        canvas = ttk.Canvas(master, width=width, height=height)
        canvas.bind("<B1-Motion>", self.on_spectrum_interaction, add="+")
        for x, colorx in enumerate(range(0, width, xf)):
            for y, colory in enumerate(range(0, height, yf)):
                values = self.color_from_coords(colorx, colory)
                fill = values.hex
                bbox = [x*xf, y*yf, (x*xf)+xf, (y*yf)+yf]
                canvas.create_rectangle(*bbox, fill=fill, width=0)
        return canvas

    def create_button_box(self, master):
        ...

    def create_luminance_scale(self, master):
        height = xf = self.spectrum_point
        width = self.spectrum_width
        values = self.get_variables()
        canvas = ttk.Canvas(master, height=height, width=width)
        for x, l in enumerate(range(0, width, xf)):
            lum = l/width*LUM
            fill = colorutils.update_hsl_value(
                color=values.hex, 
                lum=lum, 
                inmodel='hex', 
                outmodel='hex'
            )
            bbox = [x*xf, 0, (x*xf)+xf, height]
            tag = f'color{x}'
            canvas.create_rectangle(*bbox, fill=fill, width=0, tags=[tag])
            canvas.bind("<B1-Motion>", self.on_luminance_interaction, add="+")
        return canvas

    # update methods

    def coords_from_color(self, hexcolor):
        h, s, _ = colorutils.color_to_hsl(hexcolor)
        x = (h / HUE) * self.spectrum_width
        y = (s / SAT) * self.spectrum_height
        return x, y

    def color_from_coords(self, x, y):
        """Get the color value from the mouse position in the color 
        spectrum
        """
        HEIGHT = self.spectrum_height
        WIDTH = self.spectrum_width
        h = int(min(HUE, max(0, (HUE/WIDTH) * x)))
        s = int(min(SAT, max(0, SAT - ((SAT/HEIGHT) * y))))
        l = 50
        hx = colorutils.color_to_hex([h, s, l], 'hsl')
        r, g, b = colorutils.color_to_rgb(hx)
        return ColorValues(h, s, l, r, g, b, hx)

    def set_variables(self, h, s, l, r, g, b, hx):
        self.hue.set(h)
        self.sat.set(s)
        self.lum.set(l)
        self.red.set(r)
        self.grn.set(g)
        self.blu.set(b)
        self.hex.set(hx)

    def get_variables(self):
        """Get the values of all color models and return a 
        tuple of color values"""
        h = self.hue.get()
        s = self.sat.get()
        l = self.lum.get()
        r = self.red.get()
        g = self.grn.get()
        b = self.blu.get()
        hx = self.hex.get()
        return ColorValues(h, s, l, r, g, b, hx)

    def update_color_preview(self):
        hx = self.hex.get()
        fg = colorutils.contrast_color(
            color=hx, 
            model='hex', 
            darkcolor=self.colors.selectfg, 
            lightcolor=self.colors.fg
        )
        self.color_preview.configure(bg=hx)
        self.color_preview_lbl.configure(bg=hx, fg=fg)
        
    def update_luminance_scale(self):
        values = self.get_variables()
        width = self.spectrum_width
        xf = self.spectrum_point
        for x, l in enumerate(range(0, width, xf)):
            lum = l/width*LUM
            fill = colorutils.update_hsl_value(
                color=values.hex, 
                lum=lum, 
                inmodel='hex', 
                outmodel='hex'
            )
            tag = f'color{x}'
            self.luminance_scale.itemconfig(tag, fill=fill)

    # color events
    def sync_color_values(self, model):
        """Callback for when a color value changes"""
        values = self.get_variables()
        if model == ColorModel.HEX:
            hx = values.hex
            r, g, b = colorutils.color_to_rgb(hx)
            h, s, l = colorutils.color_to_hsl(hx)
        elif model == ColorModel.RGB:
            r, g, b = values.r, values.g, values.b
            h, s, l = colorutils.color_to_hsl([r, g, b], 'rgb')
            hx = colorutils.color_to_hex([r, g, b])
        elif model == ColorModel.HSL:
            h, s, l = values.h, values.s, values.l
            r, g, b = colorutils.color_to_rgb([h, s, l], 'hsl')
            hx = colorutils.color_to_hex([h, s, l], 'hsl')
        self.set_variables(h, s, l, r, g, b, hx)
        self.update_color_preview()

    def on_entry_value_change(self, widget: ttk.Spinbox, model):
        is_valid = widget.validate()
        if is_valid:
            self.sync_color_values(model)
            self.update_luminance_scale()

    def on_press_color_swatch(self, button: tkButton):
        color = button.cget('background')
        self.hex.set(color)
        self.sync_color_values(ColorModel.HEX)
        self.update_luminance_scale()

    def on_spectrum_interaction(self, event):
        values = self.color_from_coords(event.x, event.y)
        self.hue.set(values.h)
        self.sat.set(values.s)
        self.lum.set(values.l)
        self.sync_color_values(ColorModel.HSL)
        self.update_luminance_scale()

    def on_luminance_interaction(self, event):
        l = max(0, min(LUM, int((event.x / self.spectrum_width) * LUM)))
        self.lum.set(l)
        self.sync_color_values(ColorModel.HSL)


if __name__ == '__main__':

    app = ttk.Window(themename='superhero', hdpi=0)

    cf = ColorChooserFrame(app)
    cf.pack()

    app.mainloop()