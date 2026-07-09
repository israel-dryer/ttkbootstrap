"""Floodgauge widget for ttkbootstrap.

A canvas-based progress indicator (a styled alternative to `ttk.Progressbar`)
with determinate and indeterminate modes and an optional text/percentage label.
"""
import warnings
from tkinter import Event, Misc, TclError
from typing import Any, Optional, Union

from ttkbootstrap import Canvas, DoubleVar, IntVar, Progressbar, StringVar
from ttkbootstrap.utils import contrast_color
from ttkbootstrap.constants import DETERMINATE, HORIZONTAL, PRIMARY
from ttkbootstrap.internal.configure_delegation import (
    ConfigureDelegationMixin,
    configure_delegate,
)
from ttkbootstrap.style import Colors, Style
from ttkbootstrap.style._compat import normalize_floodgauge_start_args, warn_deprecated


class Floodgauge(ConfigureDelegationMixin, Canvas):
    """
    A canvas-based widget that displays progress in determinate or indeterminate mode,
    styled using ttkbootstrap's color system.

    This widget mimics the behavior of ttk.Progressbar with additional features:
    - Canvas-based drawing for full styling control
    - Bounce-style animation for indeterminate mode
    - Lightened trough color based on the bootstyle
    - Support for variable and textvariable bindings
    - Auto-updating label based on mask or textvariable
    - Theme-reactive color updates via <<ThemeChanged>> event

    The widget's value is backed by a ``DoubleVar`` (matching ttk.Progressbar),
    so fractional values are honored. All options are reachable through the
    tk-native ``configure``/``cget``/item surface; ``value`` is also exposed as a
    read/write property.

    Parameters:
        master (Widget, optional):
            Parent widget.

        value (int or float):
            Initial value of the progress bar.

        maximum (int or float):
            The maximum value for the determinate range.

        mode (str):
            'determinate' or 'indeterminate' mode.

        mask (str, optional):
            A string with a '{}' placeholder for formatted text output, e.g. 'Progress: {}%'.

        text (str, optional):
            A static fallback label (used if no mask is specified).

        font (Font or tuple):
            The font used for the label (default: ("Helvetica", 12)).

        bootstyle (str):
            A ttkbootstrap style keyword such as 'primary', 'info', etc.

        orient (str):
            'horizontal' or 'vertical' orientation.

        length (int):
            The long dimension of the widget (width if horizontal, height if vertical). Defaults to 200.

        thickness (int):
            The short axis of the widget (height if horizontal, width if vertical). Defaults to 50.

        variable (tk.DoubleVar, optional):
            Bound variable for the current value.

        textvariable (tk.StringVar, optional):
            Bound variable for the display label.
    """

    def __init__(
            self,
            master: Optional[Misc] = None,
            value: Union[int, float] = 0,
            maximum: Union[int, float] = 100,
            mode: str = "determinate",
            mask: Optional[str] = None,
            text: str = "",
            font: Union[tuple[str, int], str] = ("Helvetica", 12),
            bootstyle: str = "primary",
            orient: str = "horizontal",
            length: int = 200,
            thickness: int = 50,
            **kwargs: Any
    ) -> None:
        self.variable = kwargs.pop("variable", DoubleVar(value=value))
        self.textvariable = kwargs.pop("textvariable", StringVar(value=text))

        self._length = length
        self._thickness = thickness
        self._orient = orient
        canvas_kwargs = dict(highlightthickness=0, **kwargs)

        if self._orient == "horizontal":
            canvas_kwargs.update(width=self._length, height=self._thickness)
        else:
            canvas_kwargs.update(width=self._thickness, height=self._length)

        super().__init__(master, **canvas_kwargs)

        self._var_traceid = None
        self._textvar_traceid = None
        self._bind_variable(self.variable)
        self._bind_textvariable(self.textvariable)

        self._maximum = maximum
        self._mode = mode
        self._mask = mask
        self._font = font
        self._step_size = 1
        self._running = False
        self._after_id = None
        self._pulse_pos = 0
        self._pulse_direction = 1
        self._bootstyle = bootstyle

        self._update_theme_colors()

        self.bind("<Configure>", self._on_resize)
        self.bind("<<ThemeChanged>>", lambda e: self._update_theme_colors())
        self._draw()

    # -- value access -------------------------------------------------------- #
    @property
    def value(self) -> float:
        """The current progress value."""
        return self.variable.get()

    @value.setter
    def value(self, amount: Union[int, float]) -> None:
        # Setting the bound variable fires its write trace -> redraw.
        self.variable.set(amount)

    #: Options that were bare public attributes before 2.0 -- now private,
    #: reachable through configure/cget. Read access is kept (deprecated) so
    #: nothing hard-breaks; the canonical surface is configure/cget.
    _LEGACY_OPTION_ATTRS = (
        "maximum", "mode", "orient", "mask", "font", "length", "thickness",
    )

    def __getattr__(self, name: str) -> Any:
        # Only reached when normal lookup fails. Keep the pre-2.0 bare-attribute
        # reads working (deprecated); the canonical read is cget.
        if name in type(self)._LEGACY_OPTION_ATTRS:
            warn_deprecated(
                f"reading the {name!r} Floodgauge attribute",
                f"cget({name!r})",
            )
            return getattr(self, f"_{name}")
        raise AttributeError(name)

    def __setattr__(self, name: str, value: Any) -> None:
        # Route pre-2.0 bare-attribute writes through configure (deprecated) so
        # they still take effect (redraw) instead of silently shadowing the
        # private field. Only triggers for a user setting the bare name -- we
        # only ever assign the private `_name` internally.
        if name in type(self)._LEGACY_OPTION_ATTRS:
            warn_deprecated(
                f"setting the {name!r} Floodgauge attribute",
                f"configure({name}=...)",
            )
            self.configure(**{name: value})
            return
        super().__setattr__(name, value)

    def _update_theme_colors(self) -> None:
        style = Style.get_instance()
        self.bar_color = style.colors.get(self._bootstyle)
        self.trough_color = Colors.update_hsv(self.bar_color, 0, -0.5, 0.3)
        self.text_color = contrast_color(self.bar_color, 'hex')
        self._draw()

    def _on_resize(self, event: Event) -> None:
        if self._orient == "horizontal":
            self._length = event.width
            self._thickness = event.height
        else:
            self._length = event.height
            self._thickness = event.width
        self._draw()

    def _apply_geometry(self) -> None:
        """Resize the canvas to match the current orient/length/thickness."""
        if self._orient == "horizontal":
            super().configure(width=self._length, height=self._thickness)
        else:
            super().configure(width=self._thickness, height=self._length)

    def _draw(self) -> None:
        self.delete("all")
        w = self.winfo_width()
        h = self.winfo_height()

        self.create_rectangle(0, 0, w, h, fill=self.trough_color, width=0)

        value = self.variable.get()
        if self._mode == "determinate":
            # Zero-range guard: a 0 maximum has no meaningful ratio.
            if self._maximum == 0:
                ratio = 0.0
            else:
                ratio = max(0.0, min(1.0, value / self._maximum))
            if self._orient == "horizontal":
                fill = int(ratio * w)
                self.create_rectangle(0, 0, fill, h, fill=self.bar_color, width=0)
            else:
                fill = int(ratio * h)
                self.create_rectangle(0, h - fill, w, h, fill=self.bar_color, width=0)
        else:
            if self._orient == "horizontal":
                pulse_width = max(10, int(w * 0.2))
                x = self._pulse_pos
                self.create_rectangle(x, 0, x + pulse_width, h, fill=self.bar_color, width=0)
            else:
                pulse_height = max(10, int(h * 0.2))
                y = self._pulse_pos
                self.create_rectangle(0, y - pulse_height, w, y, fill=self.bar_color, width=0)

        # Derive the display label. A mask formats the numeric value for
        # *display only* -- it must never be written back onto the user's
        # textvariable (that would clobber cget("text")).
        if self._mask:
            label = self._mask.format(int(value))
        else:
            label = self.textvariable.get()

        if label:
            self.create_text(
                w // 2,
                h // 2,
                text=label,
                font=self._font,
                fill=self.text_color,
                anchor="center"
            )

    def _on_var_change(self) -> None:
        self._draw()

    def _on_text_change(self) -> None:
        self._draw()

    def _bind_variable(self, variable: Union[IntVar, DoubleVar]) -> None:
        """Trace `variable` for value changes, dropping any prior trace.

        The trace id is retained so it can be removed when the variable is
        swapped via `configure` or when the widget is destroyed, preventing
        traces from accumulating (and from keeping an external variable's
        write callback pointed at a dead widget).
        """
        if self._var_traceid is not None:
            try:
                self.variable.trace_remove("write", self._var_traceid)
            except TclError:
                pass
        self.variable = variable
        self._var_traceid = variable.trace_add(
            "write", lambda n, i, m: self._on_var_change()
        )

    def _bind_textvariable(self, textvariable: StringVar) -> None:
        """Trace `textvariable` for changes, dropping any prior trace."""
        if self._textvar_traceid is not None:
            try:
                self.textvariable.trace_remove("write", self._textvar_traceid)
            except TclError:
                pass
        self.textvariable = textvariable
        self._textvar_traceid = textvariable.trace_add(
            "write", lambda n, i, m: self._on_text_change()
        )

    def destroy(self) -> None:
        """Cancel the animation loop and detach variable traces.

        Without this, a running `after()` loop keeps firing on the destroyed
        canvas (raising `TclError`) and an external `variable`/`textvariable`
        keeps the widget alive through its write trace.
        """
        self.stop()
        for variable, traceid in (
            (self.variable, self._var_traceid),
            (self.textvariable, self._textvar_traceid),
        ):
            if traceid is not None:
                try:
                    variable.trace_remove("write", traceid)
                except TclError:
                    pass
        self._var_traceid = None
        self._textvar_traceid = None
        super().destroy()

    def step(self, amount: Union[int, float] = 1) -> None:
        """Increment the progress value.

        Parameters:
            amount (int or float, optional): The amount to increment. Defaults
                to 1. Value wraps around after reaching maximum.
        """
        self.value = (self.value + amount) % (self._maximum + 1)

    def start(self, *args: Any, **kwargs: Any) -> None:
        """Start the progress animation.

        For indeterminate mode, starts the bouncing animation. For determinate
        mode, starts auto-incrementing the value.

        The signature mirrors ``ttk.Progressbar.start``:

            start(interval=None)

        where ``interval`` is the time in milliseconds between animation steps
        (defaults to 20ms for indeterminate mode, 50ms for determinate mode).

        The pre-2.0 ``start(step_size, interval)`` form is still accepted
        through 2.x with a ``DeprecationWarning`` (removed in 3.0); the per-mode
        step size is now an internal default.
        """
        interval, step_size = normalize_floodgauge_start_args(list(args), dict(kwargs))
        if step_size is not None:
            self._step_size = step_size
        else:
            self._step_size = 8 if self._mode == "indeterminate" else 1
        if interval is None:
            interval = 20 if self._mode == "indeterminate" else 50

        self._running = True
        self._pulse_direction = 1
        self._run_animation(interval)

    def stop(self) -> None:
        """Stop the progress animation.

        Cancels any running animation and halts auto-incrementing or bouncing.
        """
        self._running = False
        if self._after_id:
            self.after_cancel(self._after_id)
            self._after_id = None

    def _run_animation(self, interval: int) -> None:
        if not self._running:
            return

        if self._mode == "indeterminate":
            self._animate_indeterminate(interval)
        else:
            self.step(self._step_size)
            self._after_id = self.after(interval, lambda: self._run_animation(interval))

    def _animate_indeterminate(self, interval: int) -> None:
        if not self._running:
            return

        if self._orient == "horizontal":
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

    # -- configure delegates ------------------------------------------------- #
    # One get/set handler per option (value=None queries, else sets). The
    # ConfigureDelegationMixin wires these into configure/cget/keys/item access
    # and emits proper Tk 5-tuple specs.

    @configure_delegate("value")
    def _cfg_value(self, value):
        if value is None:
            return self.variable.get()
        self.variable.set(value)  # trace -> _on_var_change -> _draw

    @configure_delegate("maximum")
    def _cfg_maximum(self, value):
        if value is None:
            return self._maximum
        self._maximum = value
        self._draw()

    @configure_delegate("mode")
    def _cfg_mode(self, value):
        if value is None:
            return self._mode
        self._mode = value
        self._draw()

    @configure_delegate("orient")
    def _cfg_orient(self, value):
        if value is None:
            return self._orient
        self._orient = value
        self._apply_geometry()
        self._draw()

    @configure_delegate("mask")
    def _cfg_mask(self, value):
        if value is None:
            return self._mask
        self._mask = value
        self._draw()

    @configure_delegate("text")
    def _cfg_text(self, value):
        if value is None:
            return self.textvariable.get()
        self.textvariable.set(value)  # trace -> _on_text_change -> _draw

    @configure_delegate("font")
    def _cfg_font(self, value):
        if value is None:
            return self._font
        self._font = value
        self._draw()

    @configure_delegate("bootstyle")
    def _cfg_bootstyle(self, value):
        if value is None:
            return self._bootstyle
        self._bootstyle = value
        self._update_theme_colors()  # redraws

    @configure_delegate("length")
    def _cfg_length(self, value):
        if value is None:
            return self._length
        self._length = value
        self._apply_geometry()
        self._draw()

    @configure_delegate("thickness")
    def _cfg_thickness(self, value):
        if value is None:
            return self._thickness
        self._thickness = value
        self._apply_geometry()
        self._draw()

    @configure_delegate("variable")
    def _cfg_variable(self, value):
        # Queried: return the object; the mixin renders it as its Tcl name.
        if value is None:
            return self.variable
        self._bind_variable(value)
        self._draw()

    @configure_delegate("textvariable")
    def _cfg_textvariable(self, value):
        if value is None:
            return self.textvariable
        self._bind_textvariable(value)
        self._draw()

    def items(self) -> Any:
        """Get all configuration options as key-value pairs.

        Returns:
            dict_items: Iterator of (option, value) pairs.
        """
        return {k: self.cget(k) for k in self.keys()}.items()


class FloodgaugeLegacy(Progressbar):
    """
    DEPRECATED: This widget is retained for backward compatibility and will be
    removed in 3.0. Instantiating it emits a `DeprecationWarning`. Use the
    canvas-based `Floodgauge` instead.

    Use the canvas-based `Floodgauge` widget instead for:
    - Full control over styling and draw order
    - Support for theme responsiveness
    - Animated indeterminate mode
    - Automatic label updates with `mask` or `textvariable`

    This legacy version is based on `ttk.Progressbar` and does not support
    the same level of styling or animation flexibility.
    """

    def __init__(
            self,
            master: Optional[Misc] = None,
            cursor: Optional[str] = None,
            font: Optional[Union[tuple[str, int], str]] = None,
            length: Optional[int] = None,
            maximum: Union[int, float] = 100,
            mode: str = DETERMINATE,
            orient: str = HORIZONTAL,
            bootstyle: str = PRIMARY,
            takefocus: bool = False,
            text: Optional[str] = None,
            value: Union[int, float] = 0,
            mask: Optional[str] = None,
            **kwargs: Any,
    ) -> None:
        """
        Parameters:

            master (Widget, optional):
                Parent widget. Defaults to None.

            cursor (str, optional):
                The cursor that will appear when the mouse is over the
                progress bar. Defaults to None.

            font (Union[Font, str], optional):
                The font to use for the progress bar label.

            length (int, optional):
                Specifies the length of the long axis of the progress bar
                (width if orient = horizontal, height if if vertical);

            maximum (float, optional):
                A floating point number specifying the maximum `value`.
                Defaults to 100.

            mode ('determinate', 'indeterminate'):
                Use `indeterminate` if you cannot accurately measure the
                relative progress of the underlying process. In this mode,
                a rectangle bounces back and forth between the ends of the
                widget once you use the `Floodgauge.start()` method.
                Otherwise, use `determinate` if the relative progress can be
                calculated in advance.

            orient ('horizontal', 'vertical'):
                Specifies the orientation of the widget.

            bootstyle (str, optional):
                The style used to render the widget. Options include
                primary, secondary, success, info, warning, danger, light,
                dark.

            takefocus (bool, optional):
                This widget is not included in focus traversal by default.
                To add the widget to focus traversal, use
                `takefocus=True`.

            text (str, optional):
                A string of text to be displayed in the Floodgauge label.
                This is assigned to the attribute `Floodgauge.textvariable`

            value (float, optional):
                The current value of the progressbar. In `determinate`
                mode, this represents the amount of work completed. In
                `indeterminate` mode, it is interpreted modulo `maximum`;
                that is, the progress bar completes one "cycle" when the
                `value` increases by `maximum`.

            mask (str, optional):
                A string format that can be used to update the Floodgauge
                label every time the value is updated. For example, the
                string "{}% Storage Used" with a widget value of 45 would
                show "45% Storage Used" on the Floodgauge label. If a
                mask is set, then the `text` option is ignored.

            **kwargs:
                Other configuration options from the option database.
        """
        warnings.warn(
            "FloodgaugeLegacy is deprecated and will be removed in 3.0; "
            "use the canvas-based ttkbootstrap.Floodgauge instead.",
            DeprecationWarning,
            stacklevel=2,
        )

        # progress bar value variables
        if 'variable' in kwargs:
            self._variable = kwargs.pop('variable')
        else:
            self._variable = IntVar(value=value)
        if 'textvariable' in kwargs:
            self._textvariable = kwargs.pop('textvariable')
        else:
            self._textvariable = StringVar(value=text)

        # Retain the textvariable write trace id so it can be detached on
        # destroy (otherwise it leaks and pins the widget alive).
        self._textvar_traceid = self._textvariable.trace_add(
            "write", self._set_widget_text
        )
        self._bootstyle = bootstyle
        self._font = font or "helvetica 10"
        self._mask = mask
        self._traceid = None

        super().__init__(
            master=master,
            class_="Floodgauge",
            cursor=cursor,
            length=length,
            maximum=maximum,
            mode=mode,
            orient=orient,
            bootstyle=bootstyle,
            takefocus=takefocus,
            variable=self._variable,
            **kwargs,
        )
        self._set_widget_text(self._textvariable.get())
        self.bind("<<ThemeChanged>>", self._on_theme_change)
        self.bind("<<Configure>>", self._on_theme_change)

        if self._mask is not None:
            self._set_mask()

    def destroy(self) -> None:
        """Detach the value/text write traces before teardown.

        The traces' write callbacks hold a reference back to the widget, so
        leaving them attached keeps it alive after destroy (and, for an external
        variable, keeps firing a callback pointed at a dead widget).
        """
        for variable, traceid in (
            (self._textvariable, getattr(self, "_textvar_traceid", None)),
            (self._variable, self._traceid),
        ):
            if traceid is not None:
                try:
                    variable.trace_remove("write", traceid)
                except TclError:
                    pass
        self._textvar_traceid = None
        self._traceid = None
        super().destroy()

    def _set_widget_text(self, *_: Any) -> None:
        ttkstyle = self.cget("style")
        if self._mask is None:
            text = self._textvariable.get()
        else:
            value = self._variable.get()
            text = self._mask.format(value)
        self.tk.call("ttk::style", "configure", ttkstyle, "-text", text)
        self.tk.call("ttk::style", "configure", ttkstyle, "-font", self._font)

    def _set_mask(self) -> None:
        if self._traceid is None:
            self._traceid = self._variable.trace_add(
                "write", self._set_widget_text
            )

    def _unset_mask(self) -> None:
        if self._traceid is not None:
            self._variable.trace_remove("write", self._traceid)
        self._traceid = None

    def _on_theme_change(self, *_: Any) -> None:
        text = self._textvariable.get()
        self._set_widget_text(text)

    def _configure_get(self, cnf: str) -> Any:
        if cnf == "value":
            return self._variable.get()
        if cnf == "text":
            return self._textvariable.get()
        if cnf == "bootstyle":
            return self._bootstyle
        if cnf == "mask":
            return self._mask
        if cnf == "font":
            return self._font
        else:
            return super(Progressbar, self).configure(cnf=cnf)

    def _configure_set(self, **kwargs: Any) -> None:
        if "value" in kwargs:
            self._variable.set(kwargs.pop("value"))
        if "text" in kwargs:
            self._textvariable.set(kwargs.pop("text"))
        if "bootstyle" in kwargs:
            self._bootstyle = kwargs.get("bootstyle")
        if "mask" in kwargs:
            self._mask = kwargs.pop("mask")
        if "font" in kwargs:
            self._font = kwargs.pop("font")
        if "variable" in kwargs:
            self._variable = kwargs.get("variable")
            Progressbar.configure(self, cnf=None, **kwargs)
        if "textvariable" in kwargs:
            self.textvariable = kwargs.pop("textvariable")
        else:
            Progressbar.configure(self, cnf=None, **kwargs)

    def __getitem__(self, key: str) -> Any:
        return self._configure_get(cnf=key)

    def __setitem__(self, key: str, value: Any) -> None:
        self._configure_set(**{key: value})

    def configure(self, cnf: Optional[str] = None, **kwargs: Any) -> Any:
        """Configure the options for this widget.

        Parameters:

            cnf (dict[str, Any], optional):
                A dictionary of configuration options.

            **kwargs:
                Optional keyword arguments.
        """
        if cnf is not None:
            return self._configure_get(cnf)
        else:
            return self._configure_set(**kwargs)

    @property
    def textvariable(self) -> StringVar:
        """Get the text variable object.

        Returns:
            tk.StringVar: The variable controlling the display text.
        """
        return self._textvariable

    @textvariable.setter
    def textvariable(self, value: StringVar) -> None:
        """Set a new text variable.

        Parameters:
            value (tk.StringVar): The new text variable to bind.
        """
        self._textvariable = value
        self._set_widget_text(self._textvariable.get())

    @property
    def variable(self) -> IntVar:
        """Get the value variable object.

        Returns:
            tk.IntVar: The variable controlling the progress value.
        """
        return self._variable

    @variable.setter
    def variable(self, value: IntVar) -> None:
        """Set a new value variable.

        Parameters:
            value (tk.IntVar): The new variable to bind.
        """
        self._variable = value
        if self.cget('variable') != value:
            self.configure(variable=self._variable)