import tkinter as tk
from tkinter import ttk

from PIL import Image, ImageTk, ImageDraw
from ttkbootstrap import Style


class RadialGauge(ttk.Label):
    """
    A RadialGauge widget shows the amount completed relative to the total amount of work to be done.

    :param str background: use this option to set the background color. You may also use the ``style``.
    :param str cursor: use this option to specify the appearance of the mouse cursor when it is over the widget.
    :param str font: use this option to specify the font style for the displayed text. You man also use the ``style``.
    :param str foreground: use this option to specify the color of the displayed text. You may also use the ``style``.
    :param str indicator color: use this option to specify the indicator color. Default is style foreground color.
    :param str justify: if the text you provide contains newline ``\n`` characters, this option specifies how each line
        will be positioned horizontally: **left**, **center**, **right**. You may also use the ``style``.
    :param Union[Iterable[int], int] maximum: the maximum value of the indicator; default is 100.
    :param any padding: to add more space around all four sides of the gauge, set this option to the desired dimension.
        You may also use the ``style``.
    :param str style: the style to be used in rendering the widget.
    :param object styler: an instance of ``Style``. If not provided, it will be created and the default application
        theme will be used.
    :param str theme: the name of theme to use when styling the widget. Use any of the `TLabel` style classes.
    :param bool takefocus: use this option to specify whether the widget is visited during focus traversal.
    :param str text: a string of text to be displayed in the widget.
    :param object textvariable: a ``StringVar`` instance; get and set the text displayed in the widget; if a ``text``
        option is used, then ``text`` will be ignored. If not provided, it will be created and can be accessed via the
        ``textvariable`` property.
    :param str troughcolor: use this option to set the color of the trough: Default is theme border color.
    :param int underline: You can request that one of the letters in the text string be underlined by setting this
        option to the position of that letter.
    :param int value: the current value of the progressbar. If the variable is set to an existing value, this has no
        effect.
    :param object variable: an ``IntVar`` instance; get and set the current value of the indicator. If a variable is
        not provided, one will be created and can be accessed via the ``variable`` property``.

    ..note:: Because this is not strictly a `ttk` widget, you need to pass in a reference to a ``Style`` instance with
        the ``styler`` argument so that the widget knows what theme to extract the colors values from. If not provided,
        one will be created with the default application theme `flatly`.
    """

    def __init__(self, parent, styler=None, style='primary.TLabel', **kwargs):

        excluded = ['anchor', 'theme', 'image', 'compound', 'relief', 'bordwidth', 'maximum', 'value', 'variable',
                    'indicatorcolor', 'troughcolor', 'textvariable']
        kwargs_ = {k: v for k, v in kwargs.items() if k not in excluded}
        super().__init__(parent, class_='RadialGauge', style=style, **kwargs_)

        self.styler = Style() if not styler else styler
        self.indicatorcolor = kwargs.get('indicatorcolor') or self.styler.lookup(style, 'foreground')
        self.troughcolor = kwargs.get('troughcolor') or self.styler.lookup('Horizontal.TProgressbar', 'troughcolor')
        self.is_maximum = False  # used to control the forward and reverse on the ``step`` method

        # variable controls
        self.textvariable = kwargs.get('textvariable') or tk.StringVar(value=kwargs.get('text'))
        self.configure(textvariable=self.textvariable)
        self.variable = kwargs.get('variable') or tk.IntVar(value=kwargs.get('value'))
        self.variable.trace_add('write', self.update_indicator)
        self.maximum = 100 if kwargs.get('maximum') == None or kwargs.get('maximum') <= 0 else kwargs.get('maximum')

        # create the image for drawing the arc trough and indicator
        self.arc = None
        self.size = kwargs.get('size') or 100  # the eventual size of the widget
        self.im = Image.new('RGBA', (1000, 1000))  # create large and then subsample for higher quality image
        draw = ImageDraw.Draw(self.im)
        draw.arc((0, 0, 990, 990), 0, 360, self.troughcolor, 100)
        self.arc = ImageTk.PhotoImage(self.im.resize((self.size, self.size), Image.CUBIC))

        self.configure(compound='center', anchor='center', image=self.arc)
        self.bind('<Configure>', self.resize)

    def resize(self, event):
        """
        This is a callback for the widget's <Configure>. This method enables the widget to shrink and grow when resized
        and if permitted by the `pack`, `grid`, or `place` geometry managers.

        :param event: the <Configure> event that is triggered when the gauge widget is resized.
        """
        padding = 4  # not sure why this is required, but if I don't include it it growths continually
        self.size = max(min(event.width - padding, event.height - padding), 100)
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

        If invoked by a trace, the *args include: variable_name, array_index, mode. See ``tkinter.trace_add``
        for more information on this functionality. https://docs.oracle.com/cd/E88353_01/html/E37839/trace-1t.html

        """
        var = float(self.variable.get()) / self.maximum
        angle = 450 if var >= 1.0 else (int(var * 360) + 90)
        self.im = Image.new('RGBA', (1000, 1000))
        draw = ImageDraw.Draw(self.im)
        draw.arc((0, 0, 990, 990), 0, 360, self.troughcolor, 100)
        draw.arc((0, 0, 990, 990), 90, angle, self.indicatorcolor, 100)
        self.arc = ImageTk.PhotoImage(self.im.resize((self.size, self.size), Image.CUBIC))
        self.configure(image=self.arc)


def test_radial_gauge():
    """
    Run a visual test
    """
    # Create the main window
    root = tk.Tk()
    root.geometry('400x400')
    style = Style('cosmo')

    # Create the gauge widget
    gauge = RadialGauge(root, styler=style, font='helvetica 14 bold', maximum=360, value=275, text='275 deg')
    gauge.pack(fill='both', expand='yes', padx=5, pady=20)
    gauge.variable.trace_add('write', lambda *args, g=gauge: g.textvariable.set(f'{g.variable.get()} deg'))

    # Setup some indicator controls
    ttk.Scale(root, from_=0, to=360, variable=gauge.variable).pack(fill='x', padx=10, pady=10)
    ttk.Button(root, text='Increment the Indicator', command=gauge.step).pack(padx=10, pady=10, fill='x')

    root.mainloop()


if __name__ == '__main__':
    test_radial_gauge()
