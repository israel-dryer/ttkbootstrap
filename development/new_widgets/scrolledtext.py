"""
    This widget is adapted from `tkinter.scrolledtext.ScrolledText`

    The ttkbootstrap.widgets.scrolledtext module provides a class of 
    the same name which implements a text widget with a vertical
    scrollbar that can be styled using the `bootstyle` parameter.
"""

from tkinter import Pack, Grid, Place
from ttkbootstrap import Frame, Text, Scrollbar
from tkinter.constants import RIGHT, LEFT, Y, BOTH

class ScrolledText(Text):
    """A text widget that contains a vertical scrollbar on the right
    which can be styled with the `bootstyle` parameter. You can add
    a focus color border effect by setting the `highlightbackground` 
    option.

    Configuration options are passed to the `Text` widget. A `Frame` 
    widget is inserted between the `master` and the `Text` to hold the 
    `Scrollbar` widget. Most method calls are inherited from the `Text` 
    widget; however, `Pack`, `Grid`, and `Place` methods are redirected
    to the `Frame` widget.

    See the original [Python documentation](https://docs.python.org/3/library/tkinter.scrolledtext.html)
    for additional information on usage and settings.

    _This widget is adapted from `tkinter.scrolledtext.ScrolledText`_
    """
    def __init__(self, master=None, **kw):
        if 'bootstyle' in kw:
            bootstyle = kw.pop('bootstyle')
        else:
            bootstyle = None
        self.frame = Frame(master)
        self.vbar = Scrollbar(self.frame, bootstyle=bootstyle)
        self.vbar.pack(side=RIGHT, fill=Y)

        kw.update({'yscrollcommand': self.vbar.set})
        #if 'font' not in 
        Text.__init__(self, self.frame, highlightthickness=0, **kw)
        self.pack(side=LEFT, fill=BOTH, expand=True)
        self.vbar['command'] = self.yview

        text_meths = vars(Text).keys()
        methods = vars(Pack).keys() | vars(Grid).keys() | vars(Place).keys()
        methods = methods.difference(text_meths)

        for m in methods:
            if m[0] != '_' and m != 'config' and m != 'configure':
                setattr(self, m, getattr(self.frame, m))

        self.config = self.configure # alias

    def __str__(self):
        return str(self.frame)

    def configure(self, cnf=None, **kwargs):
        # get configuration
        if cnf == 'bootstyle':
            return self.vbar.cget('style')
        elif cnf is not None:
            return self.cget(cnf)

        # set configuration
        if 'bootstyle' in kwargs:
            bootstyle = kwargs.pop('bootstyle')
        self.vbar.configure(bootstyle=bootstyle)
        self.configure(cnf=cnf, **kwargs)

