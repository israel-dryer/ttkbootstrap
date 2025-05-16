import tkinter as tk

from ttkbootstrap.style import Style, Colors
from ttkbootstrap.colorutils import contrast_color
from ttkbootstrap.ttk_types import StyleColor


class Floodgauge(tk.Canvas):
    """
    A canvas-based progress gauge that supports themed coloring, label formatting,
    and both determinate and indeterminate animation modes.

    This widget provides a flexible and visually rich alternative to the
    standard `ttk.Progressbar`. It is fully theme-aware via ttkbootstrap’s
    `StyleColor` system and dynamically responds to theme changes.

    Features:
    ---------
    - Canvas-drawn fill and label for complete styling control
    - Lightened trough color based on primary bar color
    - Auto-contrast text color for legibility
    - Determinate progress and bounce-style indeterminate animation
    - Label can be bound to a `textvariable` or formatted using a `mask`
    - Theme updates via `<<ThemeChanged>>` event
    - Fully supports `configure`, `cget`, `__getitem__`, `__setitem__`

    Parameters:
    -----------
    master : Widget, optional
        Parent container.

    value : int, optional
        Initial value of the gauge. Default is 0.

    maximum : int, optional
        Maximum progress value. Default is 100.

    mode : str, optional
        Mode of the gauge: "determinate" (default) or "indeterminate".

    mask : str, optional
        A format string (e.g., "Loading {}%") used to format the label
        based on the current value.

    text : str, optional
        A static label used if `mask` is not provided.

    font : tuple or tkinter.Font, optional
        Font used to render the center label. Default is Helvetica 12.

    color : StyleColor, optional
        The theme color for the bar (e.g., "primary", "info", "danger").
        The trough and text will be derived from this color.

    orient : str, optional
        Orientation of the gauge: "horizontal" (default) or "vertical".

    length : int, optional
        Long axis dimension (width if horizontal, height if vertical).
        Default is 200.

    thickness : int, optional
        Short axis dimension (height if horizontal, width if vertical).
        Default is 50.

    variable : tk.IntVar, optional
        An optional `IntVar` bound to the gauge’s current value.
        The gauge updates when the variable changes.

    textvariable : tk.StringVar, optional
        An optional `StringVar` bound to the label text.

    Example:
    --------
        ```python
        fg = Floodgauge(root, value=25, maximum=100, color="info", mask="Progress: {}%")
        fg.pack(fill="x", padx=10, pady=10)
        fg.start()  # starts animation if mode is indeterminate
        ```
    """

    def __init__(
        self,
        master=None,
        value=0,
        maximum=100,
        mode="determinate",
        mask=None,
        text="",
        font=("Helvetica", 12),
        color: StyleColor = "primary",
        orient="horizontal",
        length=200,
        thickness=50,
        **kwargs
    ):
        self.variable = kwargs.pop("variable", tk.IntVar(value=value))
        self.textvariable = kwargs.pop("textvariable", tk.StringVar(value=text))

        self.length = length
        self.thickness = thickness
        self.orient = orient
        canvas_kwargs = dict(highlightthickness=0, **kwargs)

        if self.orient == "horizontal":
            canvas_kwargs.update(width=self.length, height=self.thickness)
        else:
            canvas_kwargs.update(width=self.thickness, height=self.length)

        super().__init__(master, **canvas_kwargs)

        self.variable.trace_add("write", lambda *_: self._on_var_change())
        self.textvariable.trace_add("write", lambda *_: self._on_text_change())

        self.value = self.variable.get()
        self.text = self.textvariable.get()
        self.maximum = maximum
        self.mode = mode
        self.mask = mask
        self.font = font
        self._step_size = 1
        self._running = False
        self._after_id = None
        self._pulse_pos = 0
        self._pulse_direction = 1
        self._color = color

        self._update_theme_colors()

        self.bind("<Configure>", self._on_resize)
        self.bind("<<ThemeChanged>>", lambda e: self._update_theme_colors())
        self._draw()

    def _update_theme_colors(self):
        style = Style.get_instance()
        self.bar_color = style.colors.get(self._color)
        self.trough_color = Colors.update_hsv(self.bar_color, 0, -0.5, 0.3)
        self.text_color = contrast_color(self.bar_color, 'hex')
        self._draw()

    def _on_resize(self, event):
        if self.orient == "horizontal":
            self.length = event.width
            self.thickness = event.height
        else:
            self.length = event.height
            self.thickness = event.width
        self._draw()

    def _draw(self):
        self.delete("all")
        w = self.winfo_width()
        h = self.winfo_height()

        self.create_rectangle(0, 0, w, h, fill=self.trough_color, width=0)

        if self.mode == "determinate":
            ratio = max(0, min(1, self.value / self.maximum))
            if self.orient == "horizontal":
                fill = int(ratio * w)
                self.create_rectangle(0, 0, fill, h, fill=self.bar_color, width=0)
            else:
                fill = int(ratio * h)
                self.create_rectangle(0, h - fill, w, h, fill=self.bar_color, width=0)
        else:
            if self.orient == "horizontal":
                pulse_width = max(10, int(w * 0.2))
                x = self._pulse_pos
                self.create_rectangle(x, 0, x + pulse_width, h, fill=self.bar_color, width=0)
            else:
                pulse_height = max(10, int(h * 0.2))
                y = self._pulse_pos
                self.create_rectangle(0, y - pulse_height, w, y, fill=self.bar_color, width=0)

        if self.mask:
            label = self.mask.format(int(self.value))
            self.textvariable.set(label)
        elif self.textvariable:
            label = self.textvariable.get()
        else:
            label = self.text

        if label:
            self.create_text(
                w // 2,
                h // 2,
                text=label,
                font=self.font,
                fill=self.text_color,
                anchor="center"
            )

    def _on_var_change(self):
        self.value = self.variable.get()
        self._draw()

    def _on_text_change(self):
        self.text = self.textvariable.get()
        self._draw()

    def step(self, amount=1):
        self.value = (self.value + amount) % (self.maximum + 1)
        self.variable.set(self.value)
        self._draw()

    def start(self, step_size=None, interval=None):
        if self.mode == "indeterminate":
            self._step_size = step_size if step_size is not None else 8
            interval = interval if interval is not None else 20
        else:
            self._step_size = step_size if step_size is not None else 1
            interval = interval if interval is not None else 50

        self._running = True
        self._pulse_direction = 1
        self._run_animation(interval)

    def stop(self):
        self._running = False
        if self._after_id:
            self.after_cancel(self._after_id)
            self._after_id = None

    def _run_animation(self, interval):
        if not self._running:
            return

        if self.mode == "indeterminate":
            self._animate_indeterminate(interval)
        else:
            self.step(self._step_size)
            self._after_id = self.after(interval, lambda: self._run_animation(interval))

    def _animate_indeterminate(self, interval):
        if not self._running:
            return

        if self.orient == "horizontal":
            w = self.winfo_width()
            pulse_width = max(10, int(w * 0.2))
            max_pos = w - pulse_width
            self._pulse_pos += self._step_size * self._pulse_direction
            if self._pulse_pos >= max_pos:
                self._pulse_pos = max_pos
                self._pulse_direction = -1
            elif self._pulse_pos <= 0:
                self._pulse_pos = 0
                self._pulse_direction = 1
        else:
            h = self.winfo_height()
            pulse_height = max(10, int(h * 0.2))
            max_pos = h
            self._pulse_pos += self._step_size * self._pulse_direction
            if self._pulse_pos >= max_pos:
                self._pulse_pos = max_pos
                self._pulse_direction = -1
            elif self._pulse_pos <= pulse_height:
                self._pulse_pos = pulse_height
                self._pulse_direction = 1

        self._draw()
        self._after_id = self.after(interval, lambda: self._animate_indeterminate(interval))

    def configure(self, cnf=None, **kwargs):
        if cnf is not None and not kwargs:
            custom = {
                "value": ("value", "value", "Value", self.variable.get()),
                "maximum": ("maximum", "maximum", "Maximum", self.maximum),
                "mask": ("mask", "mask", "Mask", self.mask),
                "text": ("text", "text", "Text", self.textvariable.get()),
                "font": ("font", "font", "Font", self.font),
                "color": ("color", "color", "Color", self._color),
                "variable": ("variable", "variable", "Variable", str(self.variable)),
                "textvariable": ("textvariable", "textvariable", "Textvariable", str(self.textvariable)),
                "length": ("length", "length", "Length", self.length),
                "thickness": ("thickness", "thickness", "Thickness", self.thickness),
            }
            if cnf in custom:
                return custom[cnf]
            else:
                raise tk.TclError(f"unknown option '{cnf}'")

        if "value" in kwargs:
            self.value = kwargs.pop("value")
            self.variable.set(self.value)
        if "maximum" in kwargs:
            self.maximum = kwargs.pop("maximum")
        if "mask" in kwargs:
            self.mask = kwargs.pop("mask")
        if "text" in kwargs:
            self.text = kwargs.pop("text")
            self.textvariable.set(self.text)
        if "font" in kwargs:
            self.font = kwargs.pop("font")
        if "color" in kwargs:
            self._color = kwargs.pop("color")
            self._update_theme_colors()
        if "length" in kwargs:
            self.length = kwargs.pop("length")
            if self.orient == "horizontal":
                self.configure(width=self.length)
            else:
                self.configure(height=self.length)
        if "thickness" in kwargs:
            self.thickness = kwargs.pop("thickness")
            if self.orient == "horizontal":
                self.configure(height=self.thickness)
            else:
                self.configure(width=self.thickness)
        if "variable" in kwargs:
            self.variable = kwargs.pop("variable")
            self.variable.trace_add("write", lambda *_: self._on_var_change())
        if "textvariable" in kwargs:
            self.textvariable = kwargs.pop("textvariable")
            self.textvariable.trace_add("write", lambda *_: self._on_text_change())

        self._draw()
        return super().configure(**kwargs)

    def cget(self, key):
        if key == "value":
            return self.variable.get()
        if key == "text":
            return self.textvariable.get()
        if key == "maximum":
            return self.maximum
        if key == "mask":
            return self.mask
        if key == "color":
            return self._color
        if key == "font":
            return self.font
        if key == "length":
            return self.length
        if key == "thickness":
            return self.thickness
        if key == "variable":
            return str(self.variable)
        if key == "textvariable":
            return str(self.textvariable)
        return super().cget(key)

    def keys(self):
        return [
            "value", "maximum", "mask", "text", "font",
            "color", "length", "thickness", "variable", "textvariable"
        ]

    def items(self):
        return {k: self.cget(k) for k in self.keys()}.items()

    __getitem__ = lambda self, key: self.cget(key)
    __setitem__ = lambda self, key, value: self.configure(**{key: value})
