"""
    Reference: https://www.jqueryscript.net/chart-graph/Customizable-Animated-jQuery-HTML5-Gauge-Meter-Plugin.html

"""
import tkinter as tk
from ttkbootstrap import Style, Colors
from PIL import Image, ImageTk, ImageDraw
from collections import namedtuple
from tkinter import StringVar, IntVar
from tkinter import ttk
from tkinter.ttk import Frame

Arch = namedtuple('Arch', ['start', 'end', 'range'])


class Meter(Frame):

    def __init__(self,
                 master=None,
                 amountused=0,
                 amounttotal=100,
                 labeltext='',
                 labelfont='Helvetica 10',
                 labelstyle='secondary.TLabel',
                 metersize=200,
                 meterstyle='full',
                 meterthickness=10,
                 stripethickness=0,
                 showvalue=True,
                 textfont='Helvetica 25 bold',
                 textstyle='primary.TLabel',
                 **kw):
        """
        Args:
              master (Widget): parent widget

        Keyword Args:
            amountused (int): the value to display on the meter.
            amounttotal (int): the maximum value of the meter.
            labeltext (str): supplemental text that can appear below the central text of the meter.
            labelfont(int): the font size of the supplemental label.
            metersize (int): the length and width of the square meter; represented by a single number.
            meterstyle (str): `full`, or `semi`; displays a full-circle or semi-circle.
            meterthickness (int): the thickness of the meter's progress bar in pixels.
            showvalue (bool): whether to show the value of the meter.
            stripethickness (int): shows the meter's progressbar in solid or striped form. If the value is greater than
                0, the meter's progressbar changes from a solid to a stripe, where the value is the thickness of the
                stripes.
            style (str): the ttk style used to render the meter. Any style of the form `Horizontal.TProgressbar` can be
                used with this widget.
            textfont (int): the font size of the central text shown on the meter.
        """
        meterstyles = {
            'full': Arch(-90, 270, 360),
            'semi': Arch(-220, 40, 260)
        }

        super().__init__(master=master, **kw)
        self.box = ttk.Frame(self, width=metersize, height=metersize)
        self.box.pack()

        # widget variables
        self.amountusedvariable = IntVar(value=amountused)
        self.amounttotalvariable = IntVar(value=amounttotal)
        self.textvariable = StringVar(value='75')
        self.labelvariable = StringVar(value=labeltext)

        # keyword arguments
        self.style = style
        self.metersize = metersize
        self.meterthickness = meterthickness
        self.meterstyle = meterstyle
        self.meterforeground = self.lookup(textstyle, 'foreground')
        self.meterbackground = Colors.update_hsv(self.lookup(textstyle, 'background'), vd=-0.1)
        self.stripethickness = stripethickness
        self.showvalue = showvalue
        self.arch = meterstyles[self.meterstyle]

        # meter image
        self.meter = ttk.Label(self.box)
        self.base_image = Image.new('RGBA', (metersize * 5, metersize * 5))
        self.draw_meter()

        # text & Label widgets
        self.text = ttk.Label(self.box, textvariable=self.textvariable, style=textstyle, font=textfont)
        self.label = ttk.Label(self.box, text=labeltext, style=labelstyle, font=labelfont)

        # geometry manager
        self.meter.place(x=0, y=0)
        self.text.place(relx=0.5, rely=0.5, anchor='center')
        self.text.lift()
        self.label.place(relx=0.5, rely=0.65, anchor='center')
        self.label.lift()

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

    def lookup(self, style, option):
        """Wrapper around the tcl style lookup command

        Args:
            style (str): the name of the style used for rendering the widget.
            option (str): the option to lookup from the style option database.

        Returns:
            any: the value of the option looked up.
        """
        return self.tk.call("ttk::style", "lookup", style, '-%s' % option, None, None)

    def draw_meter(self):

        draw = ImageDraw.Draw(self.base_image)

        if self.stripethickness > 0:
            for x in range(self.arch.start, self.arch.end - 1, self.stripethickness):
                draw.arc((0, 0, self.metersize * 5 - 20, self.metersize * 5 - 20),
                         x, x + self.stripethickness - 1, self.meterbackground, self.meterthickness * 5)

            for x in range(self.arch.start, self.indicator_value() - 1, self.stripethickness):
                draw.arc((0, 0, self.metersize * 5 - 20, self.metersize * 5 - 20),
                         x, x + self.stripethickness - 1, self.meterforeground, self.meterthickness * 5)
        else:
            draw.arc((0, 0, self.metersize * 5 - 20, self.metersize * 5 - 20),
                     self.arch.start, self.arch.end, self.meterbackground, self.meterthickness * 5)

            draw.arc((0, 0, self.metersize * 5 - 20, self.metersize * 5 - 20),
                     self.arch.start, self.indicator_value(), self.meterforeground, self.meterthickness * 5)

        # create tkinter image
        self.meterimage = ImageTk.PhotoImage(self.base_image.resize((self.metersize, self.metersize), Image.CUBIC))

        # set new image into master label
        self.meter.configure(image=self.meterimage)

    def indicator_value(self):

        return int((self.amountused / self.amounttotal) * self.arch.range + self.arch.start)


style = Style('pulse')
g = Meter(style.master, padding=20, meterstyle='semi', amountused=25, labeltext='% complete')

g.pack()
style.master.mainloop()
