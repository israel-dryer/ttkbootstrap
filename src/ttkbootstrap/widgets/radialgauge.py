import tkinter as tk
from tkinter import ttk

from PIL import Image, ImageTk, ImageDraw
from ttkbootstrap import Style, Colors


class Radialgauge(ttk.Label):
    """
    A Radialgauge widget shows the amount completed relative to the total amount of work to be done.

    :param str background: the widget background color; may also be set with ``style``.
    :param str cursor: specify the appearance of the mouse cursor when it is over the widget.
    :param str font: font style for the displayed text; may also be set with ``style``.
    :param str foreground: the color of the displayed text; may also be set with ``style``.
    :param str indicatorcolor: the color of the indicator ring; default color is the `primary` theme color.
    :param int indicatorthickness: indicator thickness in pixels; default is 20.
    :param str justify: specifies how each line will be positioned horizontally if newline characters are used.
    :param int maximum: maximum value of the indicator; default is 100.
    :param any padding: adds space around all four sides of the gauge; may also be set with ``style``.
    :param str style: the style used to render the widget.
    :param int startangle: the starting angle of the indicator; default is 90 degrees.
    :param bool takefocus: enables the widget to be visited during focus traversal.
    :param str text: a string of text displayed in the widget.
    :param object textvariable: a ``StringVar`` instance; gets and sets the text of the widget; will be created by
        default if none is passed; can be accessed via the ``textvariable`` property.
    :param str troughcolor: the color of the trough; default is the theme input background color.
    :param str underline: creates an underline under the letters in the text; pass in the index of the letters.
    :param object variable: an ``IntVar`` instance; get and set the current value of the indicator; if none is passed,
        one will be created and can be accessed via the ``variable`` property.

    """

    def __init__(self, parent, **kwargs):
        excluded = ['anchor', 'theme', 'image', 'compound', 'relief', 'bordwidth', 'maximum', 'value', 'variable',
                    'indicatorcolor', 'troughcolor', 'textvariable', 'angle', 'indicatorthickness']
        kwargs_ = {k: v for k, v in kwargs.items() if k not in excluded}
        self.style = kwargs.get('style') or 'primary.TLabel'
        super().__init__(parent, class_='RadialGauge', style=self.style, **kwargs_)

        self.indicatorcolor = kwargs.get('indicatorcolor') or self._lookup(self.style, 'foreground')
        self.indicatorthickness = kwargs.get('indicatorthickness') or 20
        self.troughcolor = kwargs.get('troughcolor') or Colors.update_hsv(self._lookup('TCombobox', 'background'),
                                                                          vd=-0.03)
        self.size = kwargs.get('size') or 200
        self.startangle = kwargs.get('angle') or 90
        self.im = Image.new('RGBA', (self.size, self.size))
        self.arc = ImageTk.PhotoImage(self.im)

        self.textvariable = kwargs.get('textvariable') or tk.StringVar(value=kwargs.get('text'))
        self.configure(textvariable=self.textvariable)
        self.variable = kwargs.get('variable') or tk.IntVar(value=kwargs.get('value'))
        self.variable.trace_add('write', self.update_indicator)

        self.maximum = 100 if kwargs.get('maximum') == None or kwargs.get('maximum') <= 0 else kwargs.get('maximum')
        self.is_maximum = False

        self.configure(compound='center', anchor='center', image=self.arc)
        self.bind('<Configure>', self.resize)

    @property
    def text(self):
        return self.textvariable.get()

    @text.setter
    def text(self, value):
        self.textvariable.set(value)

    @property
    def value(self):
        return self.variable.get()

    @value.setter
    def value(self, value):
        self.variable.set(value)

    def _lookup(self, style, option):
        """
        Wrapper around the tcl style lookup command

        :param style: the name of the style used for rendering a widget
        :param option: the option to lookup from the style option database
        :return: the value of the option looked up
        :rtype: str
        """
        return self.tk.call("ttk::style", "lookup", style, '-%s' % option, None, None)

    def resize(self, event):
        """
        This is a callback for the widget's *<Configure>* event. This method enables the widget to shrink and grow when
        resized and if permitted by the `pack`, `grid`, or `place` geometry managers.

        :param event: the *<Configure>* event that is triggered when the gauge widget is resized.
        """
        padding = 4  # not sure why this is required, but if I don't include it it growths continually
        self.size = max(min(event.width - padding, event.height - padding), 200)
        self.update_indicator()

    def step(self, delta=1):
        """
        Increase the indicator value by ``delta``. The default increment is 1. The indicator will reverse direction and
        count down once it reaches the maximum value.

        :param delta: the amount to change the indicator.
        """
        var = float(self.variable.get())
        if var >= float(self.maximum):
            self.is_maximum = True
            self.variable.set(var - delta)
        elif var <= 0:
            self.is_maximum = False
            self.variable.set(var + delta)
        elif self.is_maximum:
            self.variable.set(var - delta)
        else:
            self.variable.set(var + delta)

    def update_indicator(self, *args):
        """
        Redraw the arc image based on the ``variable`` value.

        If invoked by a trace, the \*args include: `variable_name`, `array_index`, and `mode`. See tkinter.trace_add_
        for more information on this functionality.

        .. _tkinter.trace_add: https://docs.oracle.com/cd/E88353_01/html/E37839/trace-1t.html
        """
        var = float(self.variable.get()) / self.maximum
        scale_factor = 2
        endangle = (360 + self.startangle) if var >= 1.0 else (int(var * 360) + self.startangle)
        self.im = Image.new('RGBA', (self.size * scale_factor, self.size * scale_factor))
        draw = ImageDraw.Draw(self.im)
        draw.ellipse((0, 0, ((self.size * scale_factor) - 10), ((self.size * scale_factor) - 10)),
                     outline=self.troughcolor, width=self.indicatorthickness * scale_factor)
        draw.arc((0, 0, ((self.size * scale_factor) - 10), (self.size * scale_factor) - 10), self.startangle, endangle,
                 self.indicatorcolor, self.indicatorthickness * scale_factor)
        self.arc = ImageTk.PhotoImage(self.im.resize((self.size, self.size), Image.CUBIC))
        self.configure(image=self.arc)


def test_radial_gauge():
    """
    Run a visual test
    """
    # Create the main window
    root = tk.Tk()
    root.geometry('400x400')
    style = Style('minty')

    # Create the gauge widget
    gauge = Radialgauge(root, font='helvetica 14 bold', maximum=360, value=275, text='275 deg')
    gauge.pack(fill='both', expand='yes', padx=5, pady=20)
    gauge.variable.trace_add('write', lambda *args, g=gauge: g.textvariable.set(f'{g.variable.get()} deg'))

    # Setup some indicator controls
    ttk.Scale(root, from_=0, to=360, variable=gauge.variable).pack(fill='x', padx=10, pady=10)
    ttk.Button(root, text='Increment the Indicator', command=gauge.step).pack(padx=10, pady=10, fill='x')

    root.mainloop()


if __name__ == '__main__':
    test_radial_gauge()
