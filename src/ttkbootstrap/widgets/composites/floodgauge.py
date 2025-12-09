from tkinter import Canvas, Event, IntVar, Misc, StringVar
from typing import Any, Optional, Union

from ttkbootstrap.widgets.mixins.configure_mixin import ConfigureDelegationMixin, configure_delegate


class FloodGauge(ConfigureDelegationMixin, Canvas):
    """A canvas-based progress widget with support for determinate and indeterminate modes.

    This widget provides an enhanced alternative to ttk.Progressbar with full styling control
    through ttkbootstrap's color system. It supports both horizontal and vertical orientations,
    customizable text overlays with format masks, and smooth animations for indeterminate mode.

    Features:
        - Canvas-based rendering for complete style customization
        - Bounce-style animation for indeterminate progress
        - Dynamic theme-aware color updates
        - Variable and textvariable bindings for reactive updates
        - Customizable text overlay with format masks
        - Horizontal and vertical orientation support

    Examples:
        Basic usage with determinate mode::

            gauge = FloodGauge(
                master=root,
                bootstyle='success',
                value=75,
                mask='{}% Complete'
            )
            gauge.pack()

        Indeterminate mode with animation::

            gauge = FloodGauge(
                master=root,
                mode='indeterminate',
                bootstyle='info'
            )
            gauge.start()

        Using variable bindings::

            progress_var = tk.IntVar(value=0)
            gauge = FloodGauge(
                master=root,
                variable=progress_var,
                mask='Processing: {}%'
            )
            # Update progress
            progress_var.set(50)
    """

    def __init__(
            self,
            master: Optional[Misc] = None,
            value: int = 0,
            maximum: int = 100,
            mode: str = "determinate",
            mask: Optional[str] = None,
            text: str = "",
            font: Union[tuple[str, int], str] = ("Helvetica", 12),
            bootstyle: str = "primary",
            orient: str = "horizontal",
            length: int = 200,
            thickness: int = 50,
            increment: int = 1,
            **kwargs: Any
    ) -> None:
        """Initialize a FloodGauge widget.

        Args:
            master: Parent widget. If None, uses the default root window.
            value: Initial progress value (0-maximum). Default is 0.
            maximum: Maximum value for determinate range. Default is 100.
            mode: Progress mode - 'determinate' for known progress or 'indeterminate'
                for unknown duration. Default is 'determinate'.
            mask: Format string for text overlay with '{}' placeholder for the value.
                Example: '{}% Complete' or 'Progress: {}/100'. If None, no automatic
                text formatting is applied. Default is None.
            text: Static text label shown when no mask is specified. Default is empty string.
            font: Font specification as tuple (family, size) or string like 'Arial 12 bold'.
                Default is ('Helvetica', 12).
            bootstyle: Color theme from ttkbootstrap (e.g., 'primary', 'success', 'info',
                'warning', 'danger'). Default is 'primary'.
            orient: Widget orientation - 'horizontal' or 'vertical'. Default is 'horizontal'.
            length: Size in pixels along the main axis (width if horizontal, height if
                vertical). Default is 200.
            thickness: Size in pixels along the minor axis (height if horizontal, width if
                vertical). Default is 50.
            increment: Step size for value changes when using step() method or during
                animations. Default is 1.
            **kwargs: Additional keyword arguments passed to the Canvas constructor,
                including 'variable' (tk.IntVar for value binding) and 'textvariable'
                (tk.StringVar for text binding).

        Note:
            The widget automatically updates colors when the theme changes via the
            <<ThemeChanged>> event. When using variable or textvariable bindings,
            the widget redraws automatically when the variables change.
        """

        self._variable = kwargs.pop("variable", IntVar(value=value))
        self._value = self._variable.get()

        self._textvariable = kwargs.pop("textvariable", StringVar(value=text))
        self._text = self._textvariable.get()

        self._mode = mode
        self._mask = mask
        self._font = font
        self._bootstyle = bootstyle
        self._orient = orient
        self._length = length
        self._thickness = thickness
        self._maximum = maximum
        self._increment = increment

        self._running = False
        self._after_id = None
        self._pulse_pos = 0
        self._pulse_direction = 1

        canvas_kwargs = dict(highlightthickness=0, **kwargs)
        if self._orient == "horizontal":
            canvas_kwargs.update(width=self._length, height=self._thickness)
        else:
            canvas_kwargs.update(width=self._thickness, height=self._length)

        super().__init__(master, **canvas_kwargs)

        self._variable_trace_id = self._variable.trace_add("write", lambda n, i, m: self._on_var_change())
        self._textvariable_trace_id = self._textvariable.trace_add("write", lambda n, i, m: self._on_text_change())

        self._update_theme_colors()

        self.bind("<Configure>", self._on_resize)

        # Bind to root to receive theme change events
        root = self.nametowidget('.')
        root.bind('<<ThemeChanged>>', lambda e: self._update_theme_colors(), add='+')

        self._draw()

    def destroy(self) -> None:
        """Clean up resources before destroying the widget."""
        self.stop()

        # Remove traces to prevent memory leaks
        if hasattr(self, '_variable') and hasattr(self, '_variable_trace_id'):
            try:
                self._variable.trace_remove('write', self._variable_trace_id)
            except Exception:
                pass

        if hasattr(self, '_textvariable') and hasattr(self, '_textvariable_trace_id'):
            try:
                self._textvariable.trace_remove('write', self._textvariable_trace_id)
            except Exception:
                pass

        super().destroy()

    # ----- Configuration Delegates ------

    @configure_delegate('mode')
    def _delegate_mode(self, value=None):
        if value is None:
            return self._mode
        self._mode = value
        self._draw()

    @configure_delegate('mask')
    def _delegate_mask(self, value=None):
        if value is None:
            return self._mask
        self._mask = value
        self._draw()

    @configure_delegate('font')
    def _delegate_font(self, value=None):
        if value is None:
            return self._font
        self._font = value
        self._draw()

    @configure_delegate('bootstyle')
    def _delegate_bootstyle(self, value=None):
        if value is None:
            return self._bootstyle
        self._bootstyle = value
        self._update_theme_colors()  # calls _draw()

    @configure_delegate('orient')
    def _delegate_orient(self, value=None):
        if value is None:
            return self._orient
        self._orient = value
        self._draw()

    @configure_delegate('length')
    def _delegate_length(self, value=None):
        if value is None:
            return self._length
        self._length = value
        if self._orient == "horizontal":
            self.configure(width=self._length)
        else:
            self.configure(height=self._length)
        self._draw()

    @configure_delegate('thickness')
    def _delegate_thickness(self, value=None):
        if value is None:
            return self._thickness
        self._thickness = value
        if self._orient == "horizontal":
            self.configure(height=self._thickness)
        else:
            self.configure(width=self._thickness)
        self._draw()

    @configure_delegate('maximum')
    def _delegate_maximum(self, value=None):
        if value is None:
            return self._maximum
        self._maximum = value
        self._draw()

    @configure_delegate('increment')
    def _delegate_increment(self, value=None):
        if value is None:
            return self._increment
        self._increment = value
        self._draw()

    @configure_delegate('value')
    def _delegate_value(self, value=None):
        if value is None:
            return self._value
        # Variable trace triggers redraw
        self._variable.set(value)

    @configure_delegate('text')
    def _delegate_text(self, value=None):
        if value is None:
            return self._text
        # Textvariable trace triggers redraw
        self._textvariable.set(value)

    @configure_delegate('variable')
    def _delegate_variable(self, value=None):
        if value is None:
            return self._variable
        self._variable.trace_remove('write', self._variable_trace_id)
        self._variable = value
        self._variable_trace_id = self._variable.trace_add("write", lambda n, i, m: self._on_var_change())
        self._value = self._variable.get()
        self._draw()

    @configure_delegate('textvariable')
    def _delegate_textvariable(self, value=None):
        if value is None:
            return self._textvariable
        self._textvariable.trace_remove('write', self._textvariable_trace_id)
        self._textvariable = value
        self._textvariable_trace_id = self._textvariable.trace_add("write", lambda n, i, m: self._on_text_change())
        self._text = self._textvariable.get()
        self._draw()

    def _update_theme_colors(self) -> None:
        """Update widget colors based on current theme and bootstyle."""
        from ttkbootstrap.style.style import get_style
        style = get_style()
        b = style.style_builder
        surface = b.color('background')
        self._bar_color = b.color(self._bootstyle)
        self._trough_color = b.border(b.subtle(self._bootstyle, surface))
        self._text_color = b.on_color(self._bar_color)
        self._draw()

    def _on_resize(self, event: Event) -> None:
        """Handle widget resize events and update dimensions."""
        if self._orient == "horizontal":
            self._length = event.width
            self._thickness = event.height
        else:
            self._length = event.height
            self._thickness = event.width
        self._draw()

    def _draw(self) -> None:
        """Render the progress bar and text overlay on the canvas."""
        self.delete("all")
        # Fallback to configured dimensions if widget not yet mapped
        w = self.winfo_width() or (self._length if self._orient == "horizontal" else self._thickness)
        h = self.winfo_height() or (self._thickness if self._orient == "horizontal" else self._length)

        self.create_rectangle(0, 0, w, h, fill=self._trough_color, width=0)

        if self._mode == "determinate":
            ratio = max(0.0, min(1.0, self._value / self._maximum)) if self._maximum > 0 else 0.0
            if self._orient == "horizontal":
                fill = int(ratio * w)
                self.create_rectangle(0, 0, fill, h, fill=self._bar_color, width=0)
            else:
                fill = int(ratio * h)
                self.create_rectangle(0, h - fill, w, h, fill=self._bar_color, width=0)
        else:
            if self._orient == "horizontal":
                pulse_width = max(10, int(w * 0.2))
                x = self._pulse_pos
                self.create_rectangle(x, 0, x + pulse_width, h, fill=self._bar_color, width=0)
            else:
                pulse_height = max(10, int(h * 0.2))
                y = self._pulse_pos
                self.create_rectangle(0, y - pulse_height, w, y, fill=self._bar_color, width=0)

        if self._mask:
            try:
                label = self._mask.format(int(self._value))
            except (ValueError, KeyError, IndexError):
                label = str(int(self._value))
            # Remove trace to avoid recursive redraw
            self._textvariable.trace_remove('write', self._textvariable_trace_id)
            self._textvariable.set(label)
            self._textvariable_trace_id = self._textvariable.trace_add("write", lambda n, i, m: self._on_text_change())
        elif self._textvariable:
            label = self._textvariable.get()
        else:
            label = self._text

        if label:
            self.create_text(
                w // 2,
                h // 2,
                text=label,
                font=self._font,
                fill=self._text_color,
                anchor="center"
            )

    def _on_var_change(self) -> None:
        """Handle changes to the value variable."""
        self._value = self._variable.get()
        self._draw()

    def _on_text_change(self) -> None:
        """Handle changes to the text variable."""
        self._text = self._textvariable.get()
        self._draw()

    def step(self, amount: int = 1) -> None:
        """Increment the progress value by the specified amount.

        Args:
            amount: Amount to increment. Value wraps around after reaching maximum.
                Default is 1.
        """
        self._value = (self._value + amount) % (self._maximum + 1)
        self._variable.set(self._value)
        self._draw()

    def start(self, step_size: Optional[int] = None, interval: Optional[int] = None) -> None:
        """Start the progress animation.

        For indeterminate mode, starts bouncing animation. For determinate mode,
        auto-increments the value at regular intervals.

        Args:
            step_size: Amount to increment per animation step. Defaults to 8 for
                indeterminate mode, 1 for determinate mode.
            interval: Time in milliseconds between animation steps. Defaults to 20ms
                for indeterminate mode, 50ms for determinate mode.
        """
        if self._mode == "indeterminate":
            self._increment = step_size if step_size is not None else 8
            interval = interval if interval is not None else 20
        else:
            self._increment = step_size if step_size is not None else 1
            interval = interval if interval is not None else 50

        self._running = True
        self._pulse_pos = 0  # Reset position
        self._pulse_direction = 1
        self._run_animation(interval)

    def stop(self) -> None:
        """Stop the progress animation and cancel any scheduled updates."""
        self._running = False
        if self._after_id:
            self.after_cancel(self._after_id)
            self._after_id = None

    def _run_animation(self, interval: int) -> None:
        """Execute one animation frame and schedule the next."""
        if not self._running:
            return

        if self._mode == "indeterminate":
            self._animate_indeterminate(interval)
        else:
            self.step(self._increment)
            self._after_id = self.after(interval, lambda: self._run_animation(interval))

    def _animate_indeterminate(self, interval: int) -> None:
        """Animate the bouncing pulse for indeterminate mode."""
        if not self._running:
            return

        if self._orient == "horizontal":
            w = self.winfo_width()
            pulse_width = max(10, int(w * 0.2))
            max_pos = w - pulse_width
            self._pulse_pos += self._increment * self._pulse_direction
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
            self._pulse_pos += self._increment * self._pulse_direction
            if self._pulse_pos >= max_pos:
                self._pulse_pos = max_pos
                self._pulse_direction = -1
            elif self._pulse_pos <= pulse_height:
                self._pulse_pos = pulse_height
                self._pulse_direction = 1

        self._draw()
        self._after_id = self.after(interval, lambda: self._animate_indeterminate(interval))

