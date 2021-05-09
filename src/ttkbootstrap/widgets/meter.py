"""
    A Meter widget that presents data and progress in a radial style gauge.

    Author: Israel Dryer, israel.dryer@gmail.com
    Modified: 2021-05-4

    Inspired by: https://www.jqueryscript.net/chart-graph/Customizable-Animated-jQuery-HTML5-Gauge-Meter-Plugin.html
"""
import math
from tkinter import StringVar, IntVar
from tkinter import ttk
from tkinter.font import Font
from tkinter.ttk import Frame, Widget

from PIL import Image, ImageTk, ImageDraw
from ttkbootstrap import Style, Colors


class Meter(Frame):
    """A radial meter that can be used to show progress of long running operations or the amount of work completed;
    can also be used as a `Dial` when set to ``interactive=True``.

    This widget is very flexible. There are two primary meter types which can be set with the ``metertype`` parameter:
    'full' and 'semi', which show the arc of the meter in a full or semi-circle. You can also customize the arc of the
    circle with the ``arcrange`` and ``arcoffset`` parameters.

    The progress bar indicator can be displayed as a solid color or with stripes using the ``stripethickness``
    parameter. By default, the ``stripethickness`` is 0, which results in a solid progress bar. A higher
    ``stripethickness`` results in larger wedges around the arc of the meter.

    Various text and label options exist. The center text and progressbar is formatted with the ``meterstyle`` parameter
    and uses the `TMeter` styles. You can prepend or append text to the center text using the ``textappend`` and
    ``textprepend`` parameters. This is most commonly used for '$', '%', or other such symbols.

    Variable are generated automatically for this widget and can be linked to other widgets by referencing them via
    the ``amountusedvariable`` and ``amounttotalvariable`` attributes.

    The variable properties allow you to easily get and set the value of these variables. For example:
    ``Meter.amountused`` or ``Meter.amountused = 55`` will get or set the amount used on the widget without having to
    call the ``get`` or ``set`` methods of the tkinter variable.
    """

    def __init__(self,
                 master=None,
                 arcrange=None,
                 arcoffset=None,
                 amounttotal=100,
                 amountused=0,
                 interactive=False,
                 labelfont='Helvetica 10 bold',
                 labelstyle='secondary.TLabel',
                 labeltext=None,
                 metersize=200,
                 meterstyle='TMeter',
                 metertype='full',
                 meterthickness=10,
                 showvalue=True,
                 stripethickness=0,
                 textappend=None,
                 textfont='Helvetica 25 bold',
                 textprepend=None,
                 wedgesize=0,
                 **kw):
        """
        Args:
            master (Widget): Parent widget
            arcoffset (int): The amount to offset the arc's starting position in degrees; 0 is at 3 o'clock.
            arcrange (int): The range of the arc in degrees from start to end.
            amounttotal (int): The maximum value of the meter.
            amountused (int): The current value of the meter; displayed if ``showvalue=True``.
            interactive (bool): Enables the meter to be adjusted with mouse interaction.
            labelfont(Font or str): The font of the supplemental label.
            labelstyle (str): The ttk style used to render the supplemental label.
            labeltext (str): Supplemental label text that appears `below` the center text.
            metersize (int): The size of the meter; represented by one side length of a square.
            meterstyle (str): The ttk style used to render the meter and center text.
            metertype (str): One of **full** or **semi**; displays a full-circle or semi-circle.
            meterthickness (int): The thickness of the meter's progress bar.
            showvalue (bool): Show the meter's value in the center text; default = True.
            stripethickness (int): The meter's progress bar can be displayed in solid or striped form. If the value is
                greater than 0, the meter's progress bar changes from a solid to striped, where the value is the
                thickness of the stripes.
            textappend (str): A short string appended to the center text.
            textfont (Font or str): The font of the center text.
            textprepend (str): A short string prepended to the center text.
            wedgesize (int): If greater than zero, the width of the wedge on either side of the current meter value.
        """
        super().__init__(master=master, **kw)

        self.box = ttk.Frame(self, width=metersize, height=metersize)

        if metertype == 'semi':
            self.arcoffset = arcoffset if arcoffset is not None else 135
            self.arcrange = arcrange if arcrange is not None else 270
        else:  # aka 'full'
            self.arcoffset = arcoffset if arcoffset is not None else -90
            self.arcrange = arcrange if arcrange is not None else 360

        # widget variables
        self.amountusedvariable = IntVar(value=amountused)
        self.amounttotalvariable = IntVar(value=amounttotal)
        self.labelvariable = StringVar(value=labeltext)
        self.amountusedvariable.trace_add('write', self.draw_meter)

        # misc widget settings
        self.towardsmaximum = True
        self.metersize = metersize
        self.meterthickness = meterthickness
        self.stripethickness = stripethickness
        self.showvalue = showvalue
        self.wedgesize = wedgesize

        # translate system colors if a ttkbootstrap style is not used
        if 'system' in self.lookup(meterstyle, 'foreground').lower():
            self.meterforeground = self.convert_system_color(self.lookup(meterstyle, 'foreground'))
        else:
            self.meterforeground = self.lookup(meterstyle, 'foreground')
        if 'system' in self.lookup(meterstyle, 'background').lower():
            self.meterbackground = Colors.update_hsv(self.convert_system_color(
                self.lookup(meterstyle, 'background')), vd=-0.1)
        else:
            self.meterbackground = Colors.update_hsv(self.lookup(meterstyle, 'background'), vd=-0.1)

        # meter image
        self.meter = ttk.Label(self.box)
        self.draw_base_image()
        self.draw_meter()

        # text & label widgets
        self.textcontainer = ttk.Frame(self.box)
        self.textprepend = ttk.Label(self.textcontainer, text=textprepend, font=labelfont, style=labelstyle)
        self.textprepend.configure(anchor='s', padding=(0, 5))
        self.text = ttk.Label(self.textcontainer, textvariable=self.amountusedvariable, style=meterstyle, font=textfont)
        self.textappend = ttk.Label(self.textcontainer, text=textappend, font=labelfont, style=labelstyle)
        self.textappend.configure(anchor='s', padding=(0, 5))
        self.label = ttk.Label(self.box, text=labeltext, style=labelstyle, font=labelfont)

        # set interactive mode
        if interactive:
            self.meter.bind('<B1-Motion>', self.on_dial_interact)
            self.meter.bind('<Button-1>', self.on_dial_interact)

        # geometry management
        self.meter.place(x=0, y=0)
        self.box.pack()
        if labeltext:
            self.textcontainer.place(relx=0.5, rely=0.45, anchor='center')
        else:
            self.textcontainer.place(relx=0.5, rely=0.5, anchor='center')
        if textprepend:
            self.textprepend.pack(side='left', fill='y')
        if showvalue:
            self.text.pack(side='left', fill='y')
        if textappend:
            self.textappend.pack(side='left', fill='y')
        self.label.place(relx=0.5, rely=0.6, anchor='center')

    @property
    def amountused(self):
        return self.amountusedvariable.get()

    @amountused.setter
    def amountused(self, value):
        self.amountusedvariable.set(value)

    @property
    def amounttotal(self):
        return self.amounttotalvariable.get()

    @amounttotal.setter
    def amounttotal(self, value):
        self.amounttotalvariable.set(value)

    def convert_system_color(self, systemcolorname):
        """Convert a system color name to a hexadecimal value

        Args:
            systemcolorname (str): a system color name, such as `SystemButtonFace`
        """
        r, g, b = [x >> 8 for x in self.winfo_rgb(systemcolorname)]
        return f'#{r:02x}{g:02x}{b:02x}'

    def draw_base_image(self):
        """Draw the base image to be used for subsequent updates"""
        self.base_image = Image.new('RGBA', (self.metersize * 5, self.metersize * 5))
        draw = ImageDraw.Draw(self.base_image)

        # striped meter
        if self.stripethickness > 0:
            for x in range(self.arcoffset, self.arcrange + self.arcoffset,
                           2 if self.stripethickness == 1 else self.stripethickness):
                draw.arc((0, 0, self.metersize * 5 - 20, self.metersize * 5 - 20),
                         x, x + self.stripethickness - 1, self.meterbackground, self.meterthickness * 5)
        # solid meter
        else:
            draw.arc((0, 0, self.metersize * 5 - 20, self.metersize * 5 - 20),
                     self.arcoffset, self.arcrange + self.arcoffset, self.meterbackground, self.meterthickness * 5)

    def draw_meter(self, *args):
        """Draw a meter

        Args:
            *args: if triggered by a trace, will be `variable`, `index`, `mode`.
        """
        im = self.base_image.copy()
        draw = ImageDraw.Draw(im)
        if self.stripethickness > 0:
            self.draw_striped_meter(draw)
        else:
            self.draw_solid_meter(draw)
        self.meterimage = ImageTk.PhotoImage(im.resize((self.metersize, self.metersize), Image.CUBIC))
        self.meter.configure(image=self.meterimage)

    def draw_solid_meter(self, draw):
        """Draw a solid meter

        Args:
            draw (ImageDraw.Draw): an object used to draw an arc on the meter
        """
        if self.wedgesize > 0:
            meter_value = self.meter_value()
            draw.arc((0, 0, self.metersize * 5 - 20, self.metersize * 5 - 20),
                     meter_value - self.wedgesize, meter_value + self.wedgesize,
                     self.meterforeground, self.meterthickness * 5)
        else:
            draw.arc((0, 0, self.metersize * 5 - 20, self.metersize * 5 - 20),
                     self.arcoffset, self.meter_value(), self.meterforeground, self.meterthickness * 5)

    def draw_striped_meter(self, draw):
        """Draw a striped meter

        Args:
            draw (ImageDraw.Draw): an object used to draw an arc on the meter
        """
        if self.wedgesize > 0:
            meter_value = self.meter_value()
            draw.arc((0, 0, self.metersize * 5 - 20, self.metersize * 5 - 20),
                     meter_value - self.wedgesize, meter_value + self.wedgesize,
                     self.meterforeground, self.meterthickness * 5)
        else:
            for x in range(self.arcoffset, self.meter_value() - 1, self.stripethickness):
                draw.arc((0, 0, self.metersize * 5 - 20, self.metersize * 5 - 20),
                         x, x + self.stripethickness - 1, self.meterforeground, self.meterthickness * 5)

    def lookup(self, style, option):
        """Wrapper around the tcl style lookup command

        Args:
            style (str): the name of the style used for rendering the widget.
            option (str): the option to lookup from the style option database.

        Returns:
            any: the value of the option looked up.
        """
        return self.tk.call("ttk::style", "lookup", style, '-%s' % option, None, None)

    def meter_value(self):
        """Calculate the meter value

        Returns:
            int: the value to be used to draw the arc length of the progress meter
        """
        return int((self.amountused / self.amounttotal) * self.arcrange + self.arcoffset)

    def on_dial_interact(self, e):
        """Callback for mouse drag motion on indicator

        Args:
            e (Event): event callback for drag motion.
        """
        dx = e.x - self.metersize // 2
        dy = e.y - self.metersize // 2
        rads = math.atan2(dy, dx)
        degs = math.degrees(rads)

        if degs > self.arcoffset:
            factor = degs - self.arcoffset
        else:
            factor = 360 + degs - self.arcoffset

        # clamp value between 0 and ``amounttotal``
        amountused = int(self.amounttotal / self.arcrange * factor)
        if amountused < 0:
            self.amountused = 0
        elif amountused > self.amounttotal:
            self.amountused = self.amounttotal
        else:
            self.amountused = amountused

    def step(self, delta=1):
        """Increase the indicator value by ``delta``.

        The default increment is 1. The indicator will reverse direction and count down once it reaches the maximum
        value.

        Keyword Args:
            delta (int): the amount to change the indicator.
        """
        if self.amountused >= self.amounttotal:
            self.towardsmaximum = True
            self.amountused = self.amountused - delta
        elif self.amountused <= 0:
            self.towardsmaximum = False
            self.amountused = self.amountused + delta
        elif self.towardsmaximum:
            self.amountused = self.amountused - delta
        else:
            self.amountused = self.amountused + delta


if __name__ == '__main__':
    style = Style()
    root = style.master
    root.title('ttkbootstrap')

    Meter(root, metersize=180, padding=20, amountused=25, metertype='semi', labeltext='miles per hour',
          interactive=True).grid(row=0, column=0)
    Meter(metersize=180, padding=20, amountused=1800, amounttotal=2600, labeltext='storage used', textappend='gb',
          meterstyle='info.TMeter', stripethickness=10, interactive=True).grid(row=0, column=1)
    Meter(metersize=180, padding=20, stripethickness=2, amountused=40, labeltext='project capacity', textappend='%',
          meterstyle='success.TMeter', interactive=True).grid(row=1, column=0)
    Meter(metersize=180, padding=20, amounttotal=280, arcrange=180, arcoffset=-180, amountused=75, textappend='°',
          labeltext='heat temperature', wedgesize=5, meterstyle='danger.TMeter', interactive=True).grid(row=1, column=1)

    root.mainloop()
