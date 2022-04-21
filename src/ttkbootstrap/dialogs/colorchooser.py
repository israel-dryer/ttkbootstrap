import ttkbootstrap as ttk
from ttkbootstrap.validation import add_range_validation, add_validation, validator
from ttkbootstrap.constants import *
from tkinter import Frame as tkFrame
from tkinter import Label as tkLabel
from ttkbootstrap import utility
from collections import namedtuple
from ttkbootstrap import colorutils
from ttkbootstrap.colorutils import RGB, HSL, HEX, HUE, SAT, LUM
from PIL import ImageColor
from ttkbootstrap.dialogs.colordropper import ColorDropperDialog
from ttkbootstrap.tooltip import ToolTip
from ttkbootstrap.localization import MessageCatalog

STD_SHADES = [0.9, 0.8, 0.7, 0.4, 0.3]
STD_COLORS = [
    '#FF0000', '#FFC000', '#FFFF00', '#00B050',
    '#0070C0', '#7030A0', '#FFFFFF', '#000000'
]

ColorValues = namedtuple('ColorValues', 'h s l r g b hex')
ColorChoice = namedtuple('ColorChoice', 'rgb hsl hex')

PEN = '✛'


@validator
def validate_color(event):
    try:
        ImageColor.getrgb(event.postchangetext)
        return True
    except:
        return False


class ColorChooser(ttk.Frame):
    """A class which creates a color chooser widget
    
    ![](../../assets/dialogs/querybox-get-color.png)    
    """

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

        # color variables
        r, g, b = ImageColor.getrgb(self.initialcolor)
        h, s, l = colorutils.color_to_hsl((r, g, b), RGB)
        hx = colorutils.color_to_hex((r, g, b), RGB)
        
        self.hue = ttk.IntVar(value=h)
        self.sat = ttk.IntVar(value=s)
        self.lum = ttk.IntVar(value=l)
        self.red = ttk.IntVar(value=r)
        self.grn = ttk.IntVar(value=g)
        self.blu = ttk.IntVar(value=b)
        self.hex = ttk.StringVar(value=hx)

        # widget sizes (adjusted by widget scaling)
        self.spectrum_height = utility.scale_size(self, 240)
        self.spectrum_width = utility.scale_size(self, 530) # looks better on Mac OS
        #self.spectrum_width = utility.scale_size(self, 480)
        self.spectrum_point = utility.scale_size(self, 12)

        # build widgets
        spectrum_frame = ttk.Frame(self.notebook)
        self.color_spectrum = self.create_spectrum(spectrum_frame)
        self.color_spectrum.pack(fill=X, side=TOP)
        self.luminance_scale = self.create_luminance_scale(self.tframe)
        self.luminance_scale.pack(fill=X)
        self.notebook.add(spectrum_frame, text=MessageCatalog.translate('Advanced'))

        themed_colors = [self.colors.get(c) for c in self.style.colors]
        self.themed_swatches = self.create_swatches(
            self.notebook, themed_colors)
        self.standard_swatches = self.create_swatches(
            self.notebook, STD_COLORS)
        self.notebook.add(self.themed_swatches, text=MessageCatalog.translate('Themed'))
        self.notebook.add(self.standard_swatches, text=MessageCatalog.translate('Standard'))
        preview_frame = self.create_preview(self.bframe)
        preview_frame.pack(side=LEFT, fill=BOTH, expand=YES, padx=(0, 5))
        self.color_entries = self.create_value_inputs(self.bframe)
        self.color_entries.pack(side=RIGHT)

        self.create_spectrum_indicator()
        self.create_luminance_indicator()

    def create_spectrum(self, master):
        """Create the color spectrum canvas"""
        # canvas and point dimensions
        width = self.spectrum_width
        height = self.spectrum_height
        xf = yf = self.spectrum_point

        # create canvas widget and binding
        canvas = ttk.Canvas(master, width=width, height=height, cursor='tcross')
        canvas.bind("<B1-Motion>", self.on_spectrum_interaction, add="+")
        canvas.bind("<Button-1>", self.on_spectrum_interaction, add="+")

        # add color points
        for x, colorx in enumerate(range(0, width, xf)):
            for y, colory in enumerate(range(0, height, yf)):
                values = self.color_from_coords(colorx, colory)
                fill = values.hex
                bbox = [x*xf, y*yf, (x*xf)+xf, (y*yf)+yf]
                canvas.create_rectangle(*bbox, fill=fill, width=0)
        return canvas

    def create_spectrum_indicator(self):
        """Create a square indicator that displays in the position of 
        the selected color"""
        s = utility.scale_size(self, 10)
        width = utility.scale_size(self, 2)
        values = self.get_variables()
        x1, y1 = self.coords_from_color(values.hex)
        colorutils.contrast_color(values.hex, 'hex')
        tag = ['spectrum-indicator']
        self.color_spectrum.create_rectangle(
            x1, y1, x1+s, y1+s, width=width, tags=[tag])
        self.color_spectrum.tag_lower('spectrum-indicator')

    # widget builder methods
    def create_swatches(self, master, colors):
        """Create a grid of color swatches"""
        boxpadx = 2
        boxpady = 0
        padxtotal = (boxpadx*15)
        boxwidth = int((self.spectrum_width-padxtotal)) / len(STD_COLORS)
        boxheight = int((self.spectrum_height-boxpady) / (len(STD_SHADES)+1))
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
                swatch = tkFrame(
                    master=rowframe,
                    bg=color,
                    width=boxwidth,
                    height=boxheight,
                    autostyle=False
                )
                swatch.bind('<Button-1>', self.on_press_swatch)
                if j == 0:
                    swatch.pack(side=LEFT, padx=(0, boxpadx))
                elif j == lastcol:
                    swatch.pack(side=LEFT, padx=(boxpadx, 0))
                else:
                    swatch.pack(side=LEFT, padx=boxpadx)
            rowframe.pack(fill=X, expand=YES)

        return container

    def create_preview(self, master):
        """Create the preview frame for original and new colors"""
        nbstyle = self.notebook.cget('style')
        # set the border color to match the notebook border color
        bordercolor = self.style.lookup(nbstyle, 'bordercolor')
        container = ttk.Frame(master)

        # the frame and label for the original color (current)
        old = tkFrame(
            master=container,
            relief=FLAT,
            bd=2,
            highlightthickness=1,
            highlightbackground=bordercolor,
            bg=self.initialcolor,
            autostyle=False
        )
        old.pack(side=LEFT, fill=BOTH, expand=YES, padx=(0, 2))
        contrastfg = colorutils.contrast_color(
            color=self.initialcolor,
            model='hex',
        )
        tkLabel(
            master=old,
            text=MessageCatalog.translate('Current'),
            background=self.initialcolor,
            foreground=contrastfg,
            autostyle=False,
            width=7
        ).pack(anchor=NW)
        
        # the frame and label for the new color
        self.preview = tkFrame(
            master=container,
            relief=FLAT,
            bd=2,
            highlightthickness=1,
            highlightbackground=bordercolor,
            bg=self.initialcolor,
            autostyle=False
        )
        self.preview.pack(side=LEFT, fill=BOTH, expand=YES, padx=(2, 0))
        self.preview_lbl = tkLabel(
            master=self.preview,
            text=MessageCatalog.translate('New'),
            background=self.initialcolor,
            foreground=contrastfg,
            autostyle=False,
            width=7
        )
        self.preview_lbl.pack(anchor=NW)

        return container

    def create_value_inputs(self, master):
        """Create color value input widgets"""
        container = ttk.Frame(master)
        for x in range(4):
            container.columnconfigure(x, weight=1)

        # value labels
        lbl_cnf = {'master': container, 'anchor': E}
        ttk.Label(**lbl_cnf, text=f'''{MessageCatalog.translate('Hue')}:''').grid(row=0, column=0, sticky=E)
        ttk.Label(**lbl_cnf, text=f'''{MessageCatalog.translate('Sat')}:''').grid(row=1, column=0, sticky=E)
        ttk.Label(**lbl_cnf, text=f'''{MessageCatalog.translate('Lum')}:''').grid(row=2, column=0, sticky=E)
        ttk.Label(**lbl_cnf, text=f'''{MessageCatalog.translate('Hex')}:''').grid(row=3, column=0, sticky=E)
        ttk.Label(**lbl_cnf, text=f'''{MessageCatalog.translate('Red')}:''').grid(row=0, column=2, sticky=E)
        ttk.Label(**lbl_cnf, text=f'''{MessageCatalog.translate('Green')}:''').grid(row=1, column=2, sticky=E)
        ttk.Label(**lbl_cnf, text=f'''{MessageCatalog.translate('Blue')}:''').grid(row=2, column=2, sticky=E)

        # value spinners and entry widgets
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

        # add input validation
        add_validation(ent_hex, validate_color)
        add_range_validation(sb_hue, 0, 360)
        for sb in [sb_sat, sb_lum]:
            add_range_validation(sb, 0, 100)
        for sb in [sb_red, sb_grn, sb_blu]:
            add_range_validation(sb, 0, 255)

        # event binding for updating colors on value change
        for sb in [sb_hue, sb_sat, sb_lum]:
            for sequence in ['<<Increment>>', '<<Decrement>>', '<Return>', '<KP_Enter>']:
                sb.bind(
                    sequence=sequence,
                    func=lambda _, w=sb: self.on_entry_value_change(
                        w, HSL),
                    add="+"
                )
        for sb in [sb_red, sb_grn, sb_blu]:
            for sequence in ['<<Increment>>', '<<Decrement>>', '<Return>', '<KP_Enter>']:
                sb.bind(
                    sequence=sequence,
                    func=lambda _, w=sb: self.on_entry_value_change(
                        w, RGB),
                    add="+"
                )
        for sequence in ['<Return>', '<KP_Enter>']:
            ent_hex.bind(
                sequence=sequence,
                func=lambda _, w=ent_hex: self.on_entry_value_change(
                    w, HEX),
                add="+"
            )  

        return container

    def create_luminance_scale(self, master):
        """Create the color luminance canvas"""
        # widget dimensions
        height = xf = self.spectrum_point
        width = self.spectrum_width

        values = self.get_variables()
        canvas = ttk.Canvas(master, height=height, width=width)

        # add color points to scale
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
            canvas.bind("<Button-1>", self.on_luminance_interaction, add="+")
        return canvas

    def create_luminance_indicator(self):
        """Create an indicator that displays in the position of the
        luminance value"""
        lum = 50
        x1 = int(lum / LUM * self.spectrum_width) - \
            ((self.spectrum_point - 2)//2)
        y1 = 0
        x2 = x1 + self.spectrum_point
        y2 = self.spectrum_point - 3
        tag = 'luminance-indicator'
        bbox = [x1, y1, x2, y2]
        self.luminance_scale.create_rectangle(
            *bbox, fill='white', outline='black', tags=[tag])
        self.luminance_scale.tag_lower(tag)

    def coords_from_color(self, hexcolor):
        """Get the coordinates on the color spectrum from the color 
        value"""
        h, s, _ = colorutils.color_to_hsl(hexcolor)
        x = (h / HUE) * self.spectrum_width
        y = (1-(s / SAT)) * self.spectrum_height
        return x, y

    def color_from_coords(self, x, y):
        """Get the color value from the mouse position in the color 
        spectrum"""
        HEIGHT = self.spectrum_height
        WIDTH = self.spectrum_width
        h = int(min(HUE, max(0, (HUE/WIDTH) * x)))
        s = int(min(SAT, max(0, SAT - ((SAT/HEIGHT) * y))))
        l = 50
        hx = colorutils.color_to_hex([h, s, l], 'hsl')
        r, g, b = colorutils.color_to_rgb(hx)
        return ColorValues(h, s, l, r, g, b, hx)

    def set_variables(self, h, s, l, r, g, b, hx):
        """Update the color value variables"""
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

    def update_preview(self):
        """Update the color in the preview frame"""
        hx = self.hex.get()
        fg = colorutils.contrast_color(
            color=hx,
            model='hex',
        )
        self.preview.configure(bg=hx)
        self.preview_lbl.configure(bg=hx, fg=fg)

    def update_luminance_scale(self):
        """Update the luminance scale with the change in hue and saturation"""
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

    def update_luminance_indicator(self):
        """Update the position of the luminance indicator"""
        lum = self.lum.get()
        x = int(lum / LUM * self.spectrum_width) - \
            ((self.spectrum_point - 2)//2)
        self.luminance_scale.moveto('luminance-indicator', x, 0)
        self.luminance_scale.tag_raise('luminance-indicator')

    def update_spectrum_indicator(self):
        """Move the spectrum indicator to a new location"""
        values = self.get_variables()
        x, y = self.coords_from_color(values.hex)
        # move to the new color location
        self.color_spectrum.moveto('spectrum-indicator', x, y)
        self.color_spectrum.tag_raise('spectrum-indicator')
        # adjust the outline color based on contrast of background
        color = colorutils.contrast_color(values.hex, 'hex')
        self.color_spectrum.itemconfig('spectrum-indicator', outline=color)

    # color events
    def sync_color_values(self, model):
        """Callback for when a color value changes. A change in one
        value will automatically update the other values so that all 
        color models remain in sync."""
        values = self.get_variables()
        if model == HEX:
            hx = values.hex
            r, g, b = colorutils.color_to_rgb(hx)
            h, s, l = colorutils.color_to_hsl(hx)
        elif model == RGB:
            r, g, b = values.r, values.g, values.b
            h, s, l = colorutils.color_to_hsl([r, g, b], 'rgb')
            hx = colorutils.color_to_hex([r, g, b])
        elif model == HSL:
            h, s, l = values.h, values.s, values.l
            r, g, b = colorutils.color_to_rgb([h, s, l], 'hsl')
            hx = colorutils.color_to_hex([h, s, l], 'hsl')
        self.set_variables(h, s, l, r, g, b, hx)
        self.update_preview()
        self.update_luminance_indicator()

    def on_entry_value_change(self, widget: ttk.Spinbox, model):
        """Update the widget colors when the color value input is 
        changed"""
        is_valid = widget.validate()
        if is_valid:
            self.sync_color_values(model)
            self.update_luminance_scale()
            self.update_spectrum_indicator()

    def on_press_swatch(self, event):
        """Update the widget colors when a color swatch is clicked."""
        button: tkFrame = self.nametowidget(event.widget)
        color = button.cget('background')
        self.hex.set(color)
        self.sync_color_values(HEX)
        self.update_luminance_scale()
        self.update_spectrum_indicator()

    def on_spectrum_interaction(self, event):
        """Update the widget colors when the color spectrum canvas is
        pressed"""
        values = self.color_from_coords(event.x, event.y)
        self.hue.set(values.h)
        self.sat.set(values.s)
        self.lum.set(values.l)
        self.sync_color_values(HSL)
        self.update_luminance_scale()
        self.update_spectrum_indicator()

    def on_luminance_interaction(self, event):
        """Update the widget colors when the color luminance scale is
        pressed"""
        l = max(0, min(LUM, int((event.x / self.spectrum_width) * LUM)))
        self.lum.set(l)
        self.sync_color_values(HSL)


from ttkbootstrap.dialogs import Dialog

class ColorChooserDialog(Dialog):
    """A class which displays a color chooser dialog. When a color
    option is selected and the "OK" button is pressed, the dialog will
    return a namedtuple that contains the color values for rgb, hsl, and
    hex. These values can be accessed by indexing the tuple or by using
    the named fields.

    ![](../../assets/dialogs/querybox-get-color.png)        
    
    Examples:

        ```python
        >>> cd = ColorChooserDialog()
        >>> cd.show()
        >>> colors = cd.result
        >>> colors.hex
        '#5fb04f'
        >>> colors[2]
        '#5fb04f
        >>> colors.rgb
        (95, 176, 79)
        >>> colors[0]
        (95, 176, 79)
        ```
    """

    def __init__(self, parent=None, title="Color Chooser", initialcolor=None):
        title = MessageCatalog.translate(title)
        super().__init__(parent=parent, title=title)
        self.initialcolor = initialcolor
        self.dropper = ColorDropperDialog()
        self.dropper.result.trace_add('write', self.trace_dropper_color)

    def create_body(self, master):
        self.colorchooser = ColorChooser(master, self.initialcolor)
        self.colorchooser.pack(fill=BOTH, expand=YES)

    def create_buttonbox(self, master):
        frame = ttk.Frame(master, padding=(5, 5))
        
        # OK button
        ok = ttk.Button(frame, bootstyle=PRIMARY, width=6, text=MessageCatalog.translate('OK'))
        ok.bind("<Return>", lambda _: ok.invoke())
        ok.configure(command=lambda b=ok: self.on_button_press(b))
        ok.pack(padx=2, side=RIGHT)

        # Cancel button
        cancel = ttk.Button(frame, bootstyle=SECONDARY, width=6, text=MessageCatalog.translate('Cancel'))
        cancel.bind("<Return>", lambda _: cancel.invoke())
        cancel.configure(command=lambda b=cancel: self.on_button_press(b))
        cancel.pack(padx=2, side=RIGHT)

        # color dropper (not supported on Mac OS)
        if self._toplevel.winsys != 'aqua':
            dropper = ttk.Label(frame, text=PEN, font=('-size 16'))
            ToolTip(dropper, MessageCatalog.translate('color dropper')) # add tooltip
            dropper.pack(side=RIGHT, padx=2)
            dropper.bind("<Button-1>", self.on_show_colordropper)
                
        frame.pack(side=BOTTOM, fill=X, anchor=S)

    def on_show_colordropper(self, event):
        self.dropper.show()

    def trace_dropper_color(self, *_):
        values = self.dropper.result.get()
        self.colorchooser.hex.set(values[2])
        self.colorchooser.sync_color_values('hex')

    def on_button_press(self, button):
        if button.cget('text') == 'OK':
            values = self.colorchooser.get_variables()
            self._result = ColorChoice(
                rgb=(values.r, values.g, values.b), 
                hsl=(values.h, values.s, values.l), 
                hex=values.hex
            )
            self._toplevel.destroy()            
        self._toplevel.destroy()            
