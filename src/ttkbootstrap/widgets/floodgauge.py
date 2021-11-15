import tkinter as tk
from tkinter.ttk import Progressbar

DETERMINATE = 'determinate'
HORIZONTAL = tk.HORIZONTAL
PRIMARY = 'primary'


class Floodgauge(Progressbar):

    def __init__(
        self,
        master=None,
        cursor=None,
        font=None,
        length=None,
        maximum=100,
        mode=DETERMINATE,
        orient=HORIZONTAL,
        bootstyle=PRIMARY,
        takefocus=False,
        text=None,
        value=0,
        mask=None,
        **kwargs
    ):
        """A widget that shows the status of a long-running operation 
        with an optional text indicator. 

        Similar to the `ttk.Progressbar`, this widget can operate in 
        two modes. *determinate* mode shows the amount completed 
        relative to the total amount of work to be done, and 
        *indeterminate* mode provides an animated display to let the 
        user know that something is happening.

        Variable are generated automatically for this widget and can be 
        linked to other widgets by referencing them via the 
        `textvariable` and `variable` attributes.

        Parameters
        ----------
        master : Widget
            Parent widget

        cursor : str
            The cursor that will appear when the mouse is over the 
            progress bar.

        font Union[Font, str]
            The font to use for the progress bar label.

        length : int
            Specifies the length of the long axis of the progress bar 
            (width if orient = horizontal, height if if vertical); 
            Default = 300.

        maximum : float
            A floating point number specifying the maximum `value`. 
            Default = 100.

        mode : { determinate, indeterminate }
            Use `indeterminate` if you cannot accurately measure the 
            relative progress of the underlying process. In this mode, 
            a rectangle bounces back and forth between the ends of the 
            widget once you use the `Floodgauge.start()` method.  
            Otherwise, use `determinate` if the relative progress can be 
            calculated in advance. Default = 'determinate'.

        orient : { horizontal, vertical }
            Specifies the orientation of the widget.

        bootstyle : str
            The style used to render the widget. Options include
            primary, secondary, success, info, warning, danger, light, 
            dark.

        takefocus : bool
            This widget is not included in focus traversal by default. 
            To add the widget to focus traversal, use 
            `takefocus=True`.

        text : str
            A string of text to be displayed in the Floodgauge label. 
            This is assigned to the attribute `Floodgauge.textvariable`

        value : float
            The current value of the progressbar. In `determinate`
            mode, this represents the amount of work completed. In 
            `indeterminate` mode, it is interpreted modulo `maximum`; 
            that is, the progress bar completes one "cycle" when the 
            `value` increases by `maximum`.

        mask : str
            A string format that can be used to update the Floodgauge
            label every time the value is updated. For example, the 
            string "{}% Storage Used" with a widget value of 45 would 
            show "45% Storage Used" on the Floodgauge label. If a
            mask is set, then the `text` option is ignored.

        **kwargs : Dict[str, Any]
            Other configuration options from the option database.
        """
        # progress bar value variable
        self.variable = tk.IntVar(value=value)
        self.textvariable = tk.StringVar(value=text)
        self._bootstyle = bootstyle
        self._font = font or 'helvetica 10'
        self._mask = mask
        self._traceid = None

        super().__init__(
            master=master,
            class_='Floodgauge',
            cursor=cursor,
            length=length,
            maximum=maximum,
            mode=mode,
            orient=orient,
            bootstyle=bootstyle,
            takefocus=takefocus,
            variable=self.variable,
            **kwargs
        )
        self._set_widget_text(self.textvariable.get())
        self.bind('<<ThemeChanged>>', self._on_theme_change)
        self.bind('<<Configure>>', self._on_theme_change)

        if self._mask is not None:
            self._set_mask()

    def _set_widget_text(self, *_):
        ttkstyle = self.cget('style')
        if self._mask is None:
            text = self.textvariable.get()
        else:
            value = self.variable.get()
            text = self._mask.format(value)
        self.tk.call("ttk::style", "configure", ttkstyle, '-text', text)
        self.tk.call("ttk::style", "configure", ttkstyle, '-font', self._font)

    def _set_mask(self):
        if self._traceid is None:
            self._traceid = self.variable.trace_add(
                'write', self._set_widget_text)

    def _unset_mask(self):
        if self._traceid is not None:
            self.variable.trace_remove('write', self._traceid)
        self._traceid = None

    def _on_theme_change(self, *_):
        text = self.textvariable.get()
        self._set_widget_text(text)

    def _configure_get(self, cnf):
        if cnf == 'value':
            return self.variable.get()
        if cnf == 'text':
            return self.textvariable.get()
        if cnf == 'bootstyle':
            return self._bootstyle
        if cnf == 'mask':
            return self._mask
        if cnf == 'font':
            return self._font
        else:
            return super(Progressbar, self).configure(cnf=cnf)

    def _configure_set(self, **kwargs):
        if 'value' in kwargs:
            self.variable.set(kwargs.pop('value'))
        if 'text' in kwargs:
            self.textvariable.set(kwargs.pop('text'))
        if 'bootstyle' in kwargs:
            self._bootstyle = kwargs.get('bootstyle')
        if 'mask' in kwargs:
            self._mask = kwargs.pop('mask')
        if 'font' in kwargs:
            self._font = kwargs.pop('font')
        else:
            super(Progressbar, self).configure(cnf=None, **kwargs)

    def __getitem__(self, key: str):
        return self._configure_get(cnf=key)

    def __setitem__(self, key: str, value):
        self._configure_set(**{key: value})

    def configure(self, cnf=None, **kwargs):
        if cnf is not None:
            return self._configure_get(cnf)
        else:
            self._configure_set(**kwargs)
