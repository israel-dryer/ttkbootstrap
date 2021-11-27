import math
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, ImageDraw
from ttkbootstrap.style.colors import Colors
import ttkbootstrap.style.utility as util

FULL = 'full'
SEMI = 'semi'
PRIMARY = 'primary'
DEFAULT = 'default'
SECONDARY = 'secondary'

class Meter(ttk.Frame):
    
    def __init__(
        self,
        master=None,
        bootstyle=DEFAULT,
        arcrange=None,
        arcoffset=None,
        amounttotal=100,
        amountused=0,
        wedgesize=0,
        metersize=200,
        metertype=FULL,
        meterthickness=10,
        showtext=True,
        interactive=False,
        stripethickness=0,
        textleft=None,
        textright=None,
        textfont='-size 25 -weight bold',
        subtext=None,
        subtextstyle=DEFAULT,
        subtextfont='-size 10',
        **kwargs
    ):
        """A radial meter that can be used to show progress of long 
        running operations or the amount of work completed; can also be 
        used as a dial when set to `interactive=True`.

        This widget is very flexible. There are two primary meter types 
        which can be set with the `metertype` parameter: 'full' and 
        'semi', which shows the arc of the meter in a full or 
        semi-circle. You can also customize the arc of the circle with 
        the `arcrange` and `arcoffset` parameters.

        The meter indicator can be displayed as a solid color or with 
        stripes using the `stripethickness` parameter. By default, the 
        `stripethickness` is 0, which results in a solid meter 
        indicator. A higher `stripethickness` results in larger wedges 
        around the arc of the meter.

        Various text and label options exist. The center text and 
        meter indicator is formatted with the `meterstyle` parameter. 
        You can set text on the left and right of this center label 
        using the `textleft` and `textright` parameters. This is most 
        commonly used for '$', '%', or other such symbols.

        If you need access to the variables that update the meter, you
        you can access these via the `amountusedvar`, `amounttotalvar`,
        and the `labelvar`. The value of these properties can also be
        retrieved via the `configure` method.

        Parameters
        ----------
        master : Widget
            The parent widget.

        arcrange : int
            The rnage of the arc if degrees from start to end. 
            Default = None.

        arcoffset : int
            The amount to offset the arc's starting position in degrees.
            0 is at 3 o'clock. Default = None.

        amounttotal : int
            The maximum value of the meter. Default = 100.

        amountused : int
            The current value of the meter; displayed in a center label
            if the `showtext` property is set to True. Default = 0.

        wedgesize : int
            Sets the length of the indicator wedge around the arc. If
            greater than 0, this wedge is set as an indicator centered
            on the current meter value. Default = 0.

        metersize : int
            The meter is square. This represents the size of one side
            if the square as measured in screen units. Default = 200.

        bootstyle : str
            Sets the indicator and center text color. One of primary, 
            secondary, success, info, warning, danger, light, dark. 
            Default = 'primary'

        metertype : { full, semi }
            Displays the meter as a full circle or semi-circle.
            Default = 'full'.

        meterthickness : int
            The thickness of the indicator. Default = 10.

        showtext : bool
            Indicates whether to show the left, center, and right text
            labels on the meter. Default = True.

        interactive : bool
            Indicates that the user may adjust the meter value with
            mouse interaction. Default = False.

        stripethickness : int
            The indicator can be displayed as a solid band or as
            striped wedges around the arc. If the value is greater than
            0, the indicator changes from a solid to striped, where the
            value is the thickness of the stripes (or wedges). 
            Default = 0.

        textleft : str
            A short string inserted to the left of the center text.

        textright: str
            A short string inserted to the right of the center text.

        textfont : Union[str, Font]
            The font used to render the center text.
            Default = '-size 25 -weight bold'

        subtext : str
            Supplemental text that appears below the center text.

        subtextstyle : str
            The bootstyle color of the subtext. One of primary, 
            secondary, success, info, warning, danger, light, dark.
            The default color is Theme specific and is a lighter 
            shade based on whether it is a 'light' or 'dark' theme.

        subtextfont : Union[str, Font]
            The font used to render the subtext.
            Default = '-size 10'

        **kwargs : Dict[str, Any]
            Other keyword arguments that are passed directly to the 
            `ttk.Frame` widget that contains the meter components.
        """    
        super().__init__(master=master, **kwargs)

        # widget variables
        self.amountusedvar = tk.IntVar(value=amountused)
        self.amountusedvar.trace_add('write', self._draw_meter)
        self.amounttotalvar = tk.IntVar(value=amounttotal)
        self.labelvar = tk.StringVar(value=subtext)

        # misc settings
        self._set_arc_offset_range(metertype, arcoffset, arcrange)
        self._towardsmaximum = True
        self._metersize = util.scale_size(self, metersize)
        self._meterthickness = util.scale_size(self, meterthickness)
        self._stripethickness = stripethickness
        self._showtext = showtext
        self._wedgesize = wedgesize
        
        self._textleft = textleft
        self._textright = textright
        self._textfont = textfont
        self._subtext = subtext
        self._subtextfont = subtextfont
        self._subtextstyle = subtextstyle
        self._bootstyle = bootstyle
        self._interactive = interactive
        self._bindids = {}
       
        self._setup_widget()

    def _setup_widget(self):
        self.meterframe = ttk.Frame(
            master=self,
            width=self._metersize, 
            height=self._metersize
        )
        self.indicator = ttk.Label(self.meterframe)
        self.textframe = ttk.Frame(self.meterframe)
        self.textleft = ttk.Label(
            master=self.textframe,
            text=self._textleft,
            font=self._subtextfont,
            bootstyle=(self._subtextstyle, 'metersubtxt'),
            anchor=tk.S,
            padding=(0, 5)
        )
        self.textcenter = ttk.Label(
            master=self.textframe,
            textvariable=self.amountusedvar,
            bootstyle=(self._bootstyle, 'meter'),
            font=self._textfont
        )
        self.textright = ttk.Label(
            master=self.textframe,
            text=self._textright,
            font=self._subtextfont,
            bootstyle=(self._subtextstyle, 'metersubtxt'),
            anchor=tk.S,
            padding=(0, 5)            
        )
        self.subtext = ttk.Label(
            master=self.meterframe,
            text=self._subtext,
            bootstyle=(self._subtextstyle, 'metersubtxt'),
            font=self._subtextfont
        )

        self.bind('<<ThemeChanged>>', self._on_theme_change)
        self.bind('<<Configure>>', self._on_theme_change)
        self._set_interactive_bind()
        self._draw_base_image()
        self._draw_meter()

        # set widget geometery
        self.indicator.place(x=0, y=0)
        self.meterframe.pack()
        self._set_show_text()

    def _set_widget_colors(self):
        bootstyle = (self._bootstyle, 'meter', 'label')
        ttkstyle = util.ttkstyle_name(string='-'.join(bootstyle))
        textcolor = self._lookup_style_option(ttkstyle, 'foreground')
        background = self._lookup_style_option(ttkstyle, 'background')
        troughcolor = self._lookup_style_option(ttkstyle, 'space')
        self._meterforeground = textcolor
        self._meterbackground = Colors.update_hsv(background, vd=-0.1)
        self._metertrough = troughcolor

    def _set_meter_text(self):
        """Setup and pack the widget labels in the appropriate order"""
        self._set_show_text()
        self._set_subtext()

    def _set_subtext(self):
        if self._subtextfont:
            if self._showtext:
                self.subtext.place(relx=0.5, rely=0.6, anchor=tk.CENTER)
            else:
                self.subtext.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    def _set_show_text(self):
        self.textframe.pack_forget()
        self.textcenter.pack_forget()
        self.textleft.pack_forget()
        self.textright.pack_forget()
        self.subtext.pack_forget()
        #self.update_idletasks()

        if self._showtext:
            if self._subtext:
                self.textframe.place(relx=0.5, rely=0.45, anchor=tk.CENTER)
            else:
                self.textframe.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self._set_text_left()
        self._set_text_center()
        self._set_text_right()            
        self._set_subtext()

    def _set_text_left(self):
        if self._showtext and self._textleft:
            self.textleft.pack(side=tk.LEFT, fill=tk.Y)

    def _set_text_center(self):
        if self._showtext:
            self.textcenter.pack(side=tk.LEFT, fill=tk.Y)

    def _set_text_right(self):
        self.textright.configure(text=self._textright)
        if self._showtext and self._textright:
            self.textright.pack(side=tk.RIGHT, fill=tk.Y)

    def _set_interactive_bind(self):
        seq1 = '<B1-Motion>'
        seq2 = '<Button-1>'

        if self._interactive:
            self._bindids[seq1] = self.indicator.bind(seq1, self._on_dial_interact)
            self._bindids[seq2] = self.indicator.bind(seq2, self._on_dial_interact)
            return
        
        if seq1 in self._bindids:
            self.indicator.unbind(seq1, self._bindids.get(seq1))
            self.indicator.unbind(seq2, self._bindids.get(seq2))
            self._bindids.clear()

    def _set_arc_offset_range(self, metertype, arcoffset, arcrange):
        if metertype == SEMI:
            self._arcoffset = 135 if arcoffset is None else arcoffset
            self._arcrange = 270 if arcrange is None else arcrange
        else:
            self._arcoffset = -90 if arcoffset is None else arcoffset
            self._arcrange = 360 if arcrange is None else arcrange
        self._metertype = metertype

    def _draw_meter(self, *_):
        """Draw a meter"""
        img = self._base_image.copy()
        draw = ImageDraw.Draw(img)
        if self._stripethickness > 0:
            self._draw_striped_meter(draw)
        else:
            self._draw_solid_meter(draw)
        
        self._meterimage = ImageTk.PhotoImage(
            img.resize((self._metersize, self._metersize), Image.CUBIC)
        )
        self.indicator.configure(image=self._meterimage)
    
    def _draw_base_image(self):
        """Draw base image to be used for subsequent updates"""
        self._set_widget_colors()
        self._base_image = Image.new(
            mode='RGBA',
            size=(self._metersize*5, self._metersize*5)
        )
        draw = ImageDraw.Draw(self._base_image)

        x1 = y1 = self._metersize * 5 - 20
        width = self._meterthickness * 5
        # striped meter
        if self._stripethickness > 0:
            _from = self._arcoffset
            _to = self._arcrange + self._arcoffset
            _step = 2 if self._stripethickness == 1 else self._stripethickness
            for x in range(_from, _to, _step):
                draw.arc(
                    xy=(0, 0, x1, y1),
                    start=x,
                    end=x + self._stripethickness - 1,
                    fill=self._metertrough,
                    width=width
                )
        # solid meter
        else:
            draw.arc(
                xy=(0, 0, x1, y1),
                start=self._arcoffset,
                end=self._arcrange+self._arcoffset,
                fill=self._metertrough,
                width=width
            )

    def _draw_solid_meter(self, draw):
        """Draw a solid meter.
        
        Parameters
        ----------
        draw : ImageDraw.Draw
            An object used to draw an arc on the meter.
        """
        x1 = y1 = self._metersize * 5 - 20
        width = self._meterthickness * 5
        
        if self._wedgesize > 0:
            meter_value = self._meter_value()
            draw.arc(
                xy=(0, 0, x1, y1),
                start=meter_value - self._wedgesize,
                end=meter_value + self._wedgesize,
                fill=self._meterforeground,
                width=width
            )
        else:
            draw.arc(
                xy=(0, 0, x1, y1),
                start=self._arcoffset,
                end=self._meter_value(),
                fill=self._meterforeground,
                width=width
            )

    def _draw_striped_meter(self, draw):
        """Draw a striped meter
        
        Parameters
        ----------
        draw : ImageDraw.Draw
            An object usd to draw an arc on the meter.
        """
        meter_value = self._meter_value()
        x1 = y1 = self._metersize * 5 - 20
        width = self._meterthickness * 5

        if self._wedgesize > 0:
            draw.arc(
                xy=(0, 0, x1, y1),
                start=meter_value - self._wedgesize,
                end=meter_value + self._wedgesize,
                fill=self._meterforeground,
                width=width
            )
        else:
            _from = self._arcoffset
            _to = meter_value - 1
            _step = self._stripethickness
            for x in range(_from, _to, _step):
                draw.arc(
                    xy=(0, 0, x1, y1),
                    start=x,
                    end=x + self._stripethickness - 1,
                    fill=self._meterforeground,
                    width=width
                )

    def _meter_value(self) -> int:
        """Calculate the value to be used to draw the arc length of
        the progress meter."""
        value = int(
            (self['amountused'] / self['amounttotal']) * 
            self._arcrange + 
            self._arcoffset
        )
        return value

    def _on_theme_change(self, *_):
        self._draw_base_image()
        self._draw_meter()

    def _on_dial_interact(self, e):
        """Callback for mouse drag motion on meter indicator
        
        Parameters
        ----------
        e : Event
            Event callback for drag motion.
        """
        dx = e.x - self._metersize // 2
        dy = e.y - self._metersize // 2
        rads = math.atan2(dy, dx)
        degs = math.degrees(rads)

        if degs > self._arcoffset:
            factor = degs - self._arcoffset
        else:
            factor = 360 + degs - self._arcoffset

        # clamp the value between 0 and `amounttotal`
        amounttotal = self.amounttotalvar.get()
        amountused = int(amounttotal / self._arcrange * factor)
        if amountused < 0:
            self.amountusedvar.set(0)
        elif amountused > amounttotal:
            self.amountusedvar.set(amounttotal)
        else:
            self.amountusedvar.set(amountused)

    def _lookup_style_option(self, style, option):
        """Wrapper around the tcl style lookup command
        
        Parameters
        ----------
        style : str
            The name of the style used for rendering the widget.

        option: str
            The option to lookup from the style option database.

        Returns
        -------
        Any
            The value of the option looked up.
        """
        value = self.tk.call(
            "ttk::style", "lookup", style, '-%s' % option, None, None
        )
        return value

    def _configure_get(self, cnf):
        """Override the configuration get method"""
        if cnf == 'arcrange':
            return self._arcrange
        elif cnf == 'arcoffset':
            return self._arcoffset
        elif cnf == 'amounttotal':
            return self.amounttotalvar.get()
        elif cnf == 'amountused':
            return self.amountusedvar.get()
        elif cnf == 'interactive':
            return self._interactive
        elif cnf == 'subtextfont':
            return self._subtextfont
        elif cnf == 'subtextstyle':
            return self._subtextstyle
        elif cnf == 'subtext':
            return self._subtext
        elif cnf == 'metersize':
            return self._metersize
        elif cnf == 'bootstyle':
            return self._bootstyle
        elif cnf == 'metertype':
            return self._metertype
        elif cnf == 'meterthickness':
            return self._meterthickness
        elif cnf == 'showtext':
            return self._showtext
        elif cnf == 'stripethickness':
            return self._stripethickness
        elif cnf == 'textleft':
            return self._textleft
        elif cnf == 'textright':
            return self._textright
        elif cnf == 'textfont':
            return self._textfont
        elif cnf == 'wedgesize':
            return self._wedgesize
        else:
            return super(ttk.Frame, self).configure(cnf)

    def _configure_set(self, **kwargs):
        """Override the configuration set method"""
        meter_text_changed = False

        if 'arcrange' in kwargs:
            self._arcrange = kwargs.pop('arcrange')
        if 'arcoffset' in kwargs:
            self._arcoffset = kwargs.pop('arcoffset')
        if 'amounttotal' in kwargs:
            amounttotal = kwargs.pop('amounttotal')
            self.amounttotalvar.set(amounttotal)
        if 'amountused' in kwargs:
            amountused = kwargs.pop('amountused')
            self.amountusedvar.set(amountused)
        if 'interactive' in kwargs:
            self._interactive = kwargs.pop('interactive')
            self._set_interactive_bind()
        if 'subtextfont' in kwargs:
            self._subtextfont = kwargs.pop('subtextfont')
            self.subtext.configure(font=self._subtextfont)
            self.textleft.configure(font=self._subtextfont)
            self.textright.configure(font=self._subtextfont)
        if 'subtextstyle' in kwargs:
            self._subtextstyle = kwargs.pop('subtextstyle')
            self.subtext.configure(bootstyle=[self._subtextstyle, 'meter'])
        if 'metersize' in kwargs:
            self._metersize = util.scale_size(kwargs.pop('metersize'))
            self.meterframe.configure(height=self._metersize, width=self._metersize)
        if 'bootstyle' in kwargs:
            self._bootstyle = kwargs.pop('bootstyle')
            self.textcenter.configure(bootstyle=[self._bootstyle, 'meter'])
        if 'metertype' in kwargs:
            self._metertype = kwargs.pop('metertype')
        if 'meterthickness' in kwargs:
            self._meterthickness = self.scale_size(kwargs.pop('meterthickness'))
        if 'stripethickness' in kwargs:
            self._stripethickness = kwargs.pop('stripethickness')
        if 'subtext' in kwargs:
            self._subtext = kwargs.pop('subtext')
            self.subtext.configure(text=self._subtext)
            meter_text_changed = True
        if 'textleft' in kwargs:
            self._textleft = kwargs.pop('textleft')
            self.textleft.configure(text=self._textleft)
            meter_text_changed = True
        if 'textright' in kwargs:
            self._textright = kwargs.pop('textright')
            meter_text_changed = True
        if 'showtext' in kwargs:
            self._showtext = kwargs.pop('showtext')
            meter_text_changed = True
        if 'textfont' in kwargs:
            self._textfont = kwargs.pop('textfont')
            self.textcenter.configure(font=self._textfont)
        if 'wedgesize' in kwargs:
            self._wedgesize = kwargs.pop('wedgesize')

        if meter_text_changed:
            self._set_meter_text()

        try:
            if self._metertype:
                self._set_arc_offset_range(
                    metertype=self._metertype, 
                    arcoffset=self._arcoffset, 
                    arcrange=self._arcrange
                )
        except AttributeError:
            return
        
        self._draw_base_image()
        self._draw_meter()
        
        # pass remaining configurations to `ttk.Frame.configure`
        super(ttk.Frame, self).configure(**kwargs)

    def __getitem__(self, key: str):
        return self._configure_get(key)

    def __setitem__(self, key: str, value) -> None:
        self._configure_set(**{key: value})

    def configure(self, cnf=None, **kwargs):
        if cnf is not None:
            return self._configure_get(cnf)
        else:
            self._configure_set(**kwargs)

    def step(self, delta=1):
        """Increase the indicator value by `delta`
        
        The default increment is 1. The indicator will reverse
        direction and count down once it reaches the maximum value.

        Parameters
        ----------
        delta : int
            The amount to change the indicator
        """
        amountused = self.amountusedvar.get()
        amounttotal = self.amounttotalvar.get()
        if amountused >= amounttotal:
            self._towardsmaximum = True
            self.amountusedvar.set(amountused - delta)
        elif amountused <= 0:
            self._towardsmaximum = False
            self.amountusedvar.set(amountused + delta)
        elif self._towardsmaximum:
            self.amountusedvar.set(amountused - delta)
        else:
            self.amountusedvar.set(amountused + delta)
