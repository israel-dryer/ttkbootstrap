import math
from tkinter import Canvas, DoubleVar, IntVar, StringVar, font as tkfont
from typing import Any, Callable, Literal
from warnings import warn

from PIL import Image, ImageDraw, ImageTk
from PIL.Image import Resampling

from ttkbootstrap.core.exceptions import ConfigurationWarning
from ttkbootstrap.widgets.primitives.frame import Frame
from ttkbootstrap.widgets.mixins.configure_mixin import configure_delegate
from ttkbootstrap.widgets.types import Master

DEFAULT_IMAGE_SCALE = 6


class Meter(Frame):
    """A circular progress meter widget with customizable appearance and optional text display.

    The Meter widget displays a value as a circular arc indicator with optional value text,
    prefix/suffix labels, and subtitle. Supports both full circle and semi-circle styles,
    segmented or solid indicators, and interactive mode for user input.

    The meter value can be accessed and modified using:

    - ``get()`` / ``set(value)`` - Standard value-widget API methods
    - ``.value`` property - Direct property access
    - ``configure(value=x)`` - Via the configure interface

    !!! note "Events"

        ``<<Change>>``: Fired whenever the meter value changes.
          Provides ``event.data`` with keys: ``value``, ``prev_value``.
    """

    def __init__(
            self,
            master: Master = None,
            accent: str = None,
            bootstyle: str = None,

            # value parameters
            value: int | float = 0,
            minvalue: int | float = 0,
            maxvalue: int | float = 100,
            value_format: str = "{:.0f}",
            value_prefix: str = None,
            value_suffix: str = None,
            value_font: str = None,
            dtype: type[int] | type[float] = int,

            # secondary options
            secondary_font: str = None,
            secondary_style: str = None,
            subtitle: str = None,

            # appearance
            size: int = 200,
            thickness: int = 10,
            indicator_width: int = 0,
            segment_width: int = 0,
            arc_range: int = None,
            arc_offset: int = None,

            # other
            meter_type: Literal['semi', 'full'] = 'full',
            show_text: bool = True,
            interactive: bool = False,
            step_size: int | float = 1,
            **kwargs: Any
    ):
        """Initialize a Meter widget.

        Args:
            master: The parent widget.
            accent: Accent token for the meter indicator (e.g., 'primary', 'success').
            bootstyle: DEPRECATED - Use ``accent`` instead.

            value: Current meter value.
            minvalue: Minimum value for the meter range.
            maxvalue: Maximum value for the meter range.
            value_format: Format string for displaying the value (e.g., "{:.0f}", "{:.2f}").
            value_prefix: Text to display before the value (e.g., "$", "@").
            value_suffix: Text to display after the value (e.g., "%", "mph").
            value_font: Font specification for the value text (e.g., "-size 36 -weight bold").
            dtype: Data type for the value variable (int or float).

            secondary_font: Font specification for prefix, suffix, and subtitle text.
            secondary_style: Style name for prefix, suffix, and subtitle color.
            subtitle: Optional subtitle text displayed below the value.

            size: Width and height of the meter in pixels.
            thickness: Width of the meter arc in pixels.
            indicator_width: Width of the indicator segment when using a wedge-style indicator.
                           0 means fill from start to current value.
            segment_width: Width of each segment for a segmented meter style. 0 means solid.
            arc_range: Total arc range in degrees. None uses defaults (360 for full, 270 for semi).
            arc_offset: Starting angle offset in degrees. None uses defaults (-90 for full, 135 for semi).

            meter_type: Meter style - 'full' for full circle or 'semi' for semicircle.
            show_text: Whether to display the value text and labels.
            interactive: Whether the meter responds to mouse clicks/drags to change value.
            step_size: Increment step when in interactive mode.
            **kwargs: Additional keyword arguments passed to the Frame parent class.

        !!! note "Events"
            - ``<<Change>>``: Emitted when the value changes (see on_changed()).
        """
        legacy = Meter._coerce_legacy_params(kwargs)
        super().__init__(master, **kwargs)

        # configuration
        self._dtype = dtype
        self._size = legacy.get('size', size)
        self._thickness = legacy.get('thickness', thickness)
        self._indicator_width = legacy.get('indicator_width', indicator_width)
        self._segment_width = legacy.get('segment_width', segment_width)
        self._arc_range = legacy.get('arc_range', arc_range)
        self._arc_offset = legacy.get('arc_offset', arc_offset)
        self._minvalue = legacy.get('minvalue', minvalue)
        self._maxvalue = legacy.get('maxvalue', maxvalue)

        self._meter_type = legacy.get('meter_type', meter_type)
        self._show_text = legacy.get('show_text', show_text)
        self._interactive = interactive
        self._step_size = legacy.get('step_size', step_size)

        self._value_format = legacy.get('value_format', value_format)
        self._value_font = legacy.get('value_font', value_font or '-size 36 -weight bold')
        self._value_prefix = legacy.get('value_prefix', value_prefix)
        self._value_suffix = legacy.get('value_suffix', value_suffix)
        self._accent = accent or bootstyle or 'primary'

        self._subtitle = legacy.get('subtitle', subtitle)
        self._secondary_font = legacy.get('secondary_font', secondary_font or '-size 9')
        self._secondary_style = legacy.get('secondary_style', secondary_style or 'background[muted]')

        # color tokens (separate from resolved colors)
        self._surface_token = 'background'  # Token name for surface color

        # state tracking
        self._towards_maximum = True
        self._resolve_arc_range_offset(meter_type, arc_offset, arc_range)
        self._binding = {}

        # widget variables
        value = legacy.get('value', value)
        self._last_changed_value = value
        self._value_var = self._variable(value)
        self._value_var.trace_add('write', self._update_meter)  # Update meter when value changes
        self._value_display_var = StringVar(value=value_format.format(value))
        self._subtitle_var = StringVar(value=self._subtitle)

        # Resolve styles first to get colors
        self._resolve_meter_styles()

        # layout - use canvas for both meter and text
        self._canvas = Canvas(
            master=self,
            width=self._size,
            height=self._size,
            highlightthickness=0,
            background=self._surface
        )

        # Canvas text items (will be created/updated in _draw_meter)
        self._meter_image_id = None
        self._value_text_id = None
        self._prefix_text_id = None
        self._suffix_text_id = None
        self._subtitle_text_id = None

        # update bindings
        self._binding['<<ThemeChanged>>'] = self.bind('<<ThemeChanged>>', self._handle_theme_changed)
        self._binding['<<Configure>>'] = self.bind('<<Configure>>', self._handle_theme_changed)
        self._bind_interactive_events()
        self._draw_base_meter_images()
        self._draw_meter()

        # set widget geometry
        self._canvas.pack()

    # ----- Configuration Delegates -----

    @staticmethod
    def _coerce_legacy_params(options):
        param_map = dict(
            amountused="value",
            amountmin="minvalue",
            amounttotal="maxvalue",
            amountformat="value_format",
            textleft="value_prefix",
            textright="value_suffix",
            textfont="value_font",
            subtextfont="secondary_font",
            subtextstyle="secondary_style",
            subtext="subtitle",
            metersize="size",
            meterthickness="thickness",
            wedgesize="indicator_width",
            stripethickness="segment_width",
            arcrange="arc_range",
            arcoffset="arc_offset",
            metertype="meter_type",
            showtext="show_text",
            stepsize="step_size"
        )
        legacy_params = dict()
        legacy_keys = set()

        for k, v in options.items():
            if k in param_map:
                legacy_params[param_map[k]] = v
                legacy_keys.add(k)

        if legacy_params:
            for k in legacy_keys:
                del options[k]
            warn(
                f'You are using a param signature for Meter which is deprecated. {legacy_keys}. See reference map: {param_map}',
                DeprecationWarning)
        return legacy_params

    @property
    def value(self):
        return self._value_var.get()

    @value.setter
    def value(self, value: int | float):
        self._value_var.set(value)

    @property
    def subtitle(self):
        return self._subtitle_var.get()

    @subtitle.setter
    def subtitle(self, value: str):
        self._subtitle = value
        self._subtitle_var.set(value)

    # ------ Value API Methods ------

    def get(self):
        """Return the current meter value.

        This is part of the standard value-widget API. It is equivalent
        to accessing the ``.value`` property.

        Returns:
            The current meter value (int or float depending on dtype).
        """
        return self.value

    def set(self, value):
        """Set the meter value.

        This is part of the standard value-widget API. It is equivalent
        to setting the ``.value`` property.

        Args:
            value: The new meter value.
        """
        self.value = value

    # ------ Configuration Delegates ------

    @configure_delegate('accent')
    def _delegate_accent(self, value=None):
        if value is None:
            return self._accent
        else:
            self._accent = value
            self._resolve_meter_styles()
            self._draw_meter()
        return None

    @configure_delegate('value')
    def _delegate_value(self, value=None):
        if value is None:
            return self.value
        else:
            self.value = value
        return None

    @configure_delegate('minvalue')
    def _delegate_minvalue(self, value=None):
        if value is None:
            return self._minvalue
        else:
            self._minvalue = value
            self._draw_meter()
        return None

    @configure_delegate('maxvalue')
    def _delegate_maxvalue(self, value=None):
        if value is None:
            return self._maxvalue
        else:
            self._maxvalue = value
            self._draw_meter()
        return None

    @configure_delegate('value_format')
    def _delegate_value_format(self, value=None):
        if value is None:
            return self._value_format
        else:
            self._value_format = value
            self._draw_meter()
        return None

    @configure_delegate('value_prefix')
    def _delegate_value_prefix(self, value=None):
        if value is None:
            return self._value_prefix
        else:
            self._value_prefix = value
            self._draw_meter()
        return None

    @configure_delegate('value_suffix')
    def _delegate_value_suffix(self, value=None):
        if value is None:
            return self._value_suffix
        else:
            self._value_suffix = value
            self._draw_meter()
        return None

    @configure_delegate('value_font')
    def _delegate_value_font(self, value=None):
        if value is None:
            return self._value_font
        else:
            self._value_font = value
            self._draw_meter()
        return None

    @configure_delegate('dtype')
    def _delegate_dtype(self, value=None):
        if value is None:
            return self._dtype
        else:
            warn('dtype is only configurable in the widget constructor', ConfigurationWarning)
        return None

    @configure_delegate('secondary_font')
    def _delegate_secondary_font(self, value=None):
        if value is None:
            return self._secondary_font
        else:
            self._secondary_font = value
            self._draw_meter()
        return None

    @configure_delegate('secondary_style')
    def _delegate_secondary_style(self, value=None):
        if value is None:
            return self._secondary_style
        else:
            self._secondary_style = value
            self._resolve_meter_styles()
            self._draw_meter()
        return None

    @configure_delegate('subtitle')
    def _delegate_subtitle(self, value=None):
        if value is None:
            return self.subtitle
        else:
            self.subtitle = value
            self._draw_meter()
        return None

    @configure_delegate('size')
    def _delegate_size(self, value=None):
        if value is None:
            return self._size
        else:
            self._size = value
            self._canvas.configure(width=value, height=value)
            self._draw_base_meter_images()
            self._draw_meter()
        return None

    @configure_delegate('thickness')
    def _delegate_thickness(self, value=None):
        if value is None:
            return self._thickness
        else:
            self._thickness = value
            self._draw_base_meter_images()
            self._draw_meter()
        return None

    @configure_delegate('indicator_width')
    def _delegate_indicator_width(self, value=None):
        if value is None:
            return self._indicator_width
        else:
            self._indicator_width = value
            self._draw_meter()
        return None

    @configure_delegate('segment_width')
    def _delegate_segment_width(self, value=None):
        if value is None:
            return self._segment_width
        else:
            self._segment_width = value
            self._draw_base_meter_images()
            self._draw_meter()
        return None

    @configure_delegate('arc_range')
    def _delegate_arc_range(self, value=None):
        if value is None:
            return self._arc_range
        else:
            self._arc_range = value
            self._draw_base_meter_images()
            self._draw_meter()
        return None

    @configure_delegate('arc_offset')
    def _delegate_arc_offset(self, value=None):
        if value is None:
            return self._arc_offset
        else:
            self._arc_offset = value
            self._draw_base_meter_images()
            self._draw_meter()
        return None

    @configure_delegate('meter_type')
    def _delegate_meter_type(self, value=None):
        if value is None:
            return self._meter_type
        else:
            self._resolve_arc_range_offset(value, self._arc_offset, self._arc_range)
            self._draw_base_meter_images()
            self._draw_meter()
        return None

    @configure_delegate('show_text')
    def _delegate_show_text(self, value=None):
        if value is None:
            return self._show_text
        else:
            self._show_text = value
            self._draw_meter()
        return None

    @configure_delegate('interactive')
    def _delegate_interactive(self, value=None):
        if value is None:
            return self._interactive
        else:
            self._interactive = value
            self._bind_interactive_events()
        return None

    @configure_delegate('step_size')
    def _delegate_step_size(self, value=None):
        if value is None:
            return self._step_size
        else:
            self._step_size = value
        return None

    def _variable(self, value: int | float):
        return IntVar(value=value) if self._dtype is int else DoubleVar(value=value)

    def _update_meter(self, *_: Any):
        """Update meter display when value changes."""
        value = self._value_var.get()
        self._value_display_var.set(self._value_format.format(value))
        self._draw_meter()
        if value != self._last_changed_value:
            prev_value = self._last_changed_value
            self._last_changed_value = value
            self.event_generate('<<Change>>', data={"value": value, "prev_value": prev_value})

    def _resolve_meter_styles(self):
        """Resolve theme colors for meter indicator, trough, and text."""
        from ttkbootstrap.style.style import get_style
        style = get_style()
        b = style.style_builder

        # Resolve colors from tokens
        accent_token = self._accent or 'primary'
        accent_color = b.color(accent_token)

        # Use _surface_token to get the token name, resolve to actual color
        surface_token = getattr(self, '_surface_token', 'background')
        surface = b.color(surface_token)
        trough_color = b.border(surface)

        # Get text colors
        value_text_color = b.color(accent_token)
        secondary_text_color = b.color(self._secondary_style or 'background[muted]')

        self._image_scale = b.scale(DEFAULT_IMAGE_SCALE)
        self._accent_color = accent_color
        self._surface = surface  # Store resolved color
        self._trough_color = trough_color
        self._value_text_color = value_text_color
        self._secondary_text_color = secondary_text_color

    def _bind_interactive_events(self):
        seq1 = '<B1-Motion>'
        seq2 = '<Button-1>'

        if self._interactive:
            self._binding[seq1] = self._canvas.bind(seq1, self._handle_interaction)
            self._binding[seq2] = self._canvas.bind(seq2, self._handle_interaction)
            return

        if seq1 in self._binding:
            self._canvas.unbind(seq1, self._binding[seq1])
            self._canvas.unbind(seq2, self._binding[seq2])
            self._binding.clear()

    def _resolve_arc_range_offset(self, meter_type: str, arc_offset: int | None, arc_range: int | None):
        """Set default arc parameters based on meter type (full or semi)."""
        if meter_type == 'semi':
            self._arc_offset = 135 if arc_offset is None else arc_offset
            self._arc_range = 270 if arc_range is None else arc_range
        else:
            self._arc_offset = -90 if arc_offset is None else arc_offset
            self._arc_range = 360 if arc_range is None else arc_range
        self._meter_type = meter_type

    def _draw_meter(self):
        """Draw meter indicator and text on canvas."""
        # Draw meter indicator
        img = self._base_image.copy()
        draw = ImageDraw.Draw(img)
        if self._segment_width > 0:
            self._draw_segment_indicator(draw)
        else:
            self._draw_solid_indicator(draw)

        self._meter_image = ImageTk.PhotoImage(
            img.resize(
                (self._size, self._size),
                Resampling.BILINEAR
            )
        )

        # Update or create image on canvas
        if self._meter_image_id is None:
            self._meter_image_id = self._canvas.create_image(
                0, 0,
                image=self._meter_image,
                anchor='nw'
            )
        else:
            self._canvas.itemconfig(self._meter_image_id, image=self._meter_image)

        # Draw text if enabled
        if self._show_text:
            self._draw_text_on_canvas()
        else:
            # Hide text elements
            self._hide_text_items()
            # Show subtitle if it exists
            if self._subtitle:
                self._draw_subtitle_centered()

    def _draw_text_on_canvas(self):
        """Draw value text with optional prefix, suffix, and subtitle on canvas."""
        value_text = self._value_display_var.get()
        center_x = self._size / 2
        center_y = self._size / 2

        # Create font objects once
        value_font = tkfont.Font(font=self._value_font)
        secondary_font = tkfont.Font(font=self._secondary_font)

        # Get font metrics
        value_metrics = value_font.metrics()
        secondary_metrics = secondary_font.metrics()

        value_height = value_metrics['ascent'] + value_metrics['descent']
        secondary_height = secondary_metrics['ascent'] + secondary_metrics['descent']

        # Calculate max height of value line (value + prefix/suffix)
        max_text_height = max(value_height, secondary_height) if (
                self._value_prefix or self._value_suffix) else value_height

        # Calculate total block height including subtitle
        subtitle_height = secondary_height if self._subtitle else 0
        subtitle_gap = -4 if self._subtitle else 0
        total_height = max_text_height + subtitle_gap + subtitle_height

        # Position value text to center the entire block
        block_top = center_y - (total_height / 2)
        value_y = block_top + (max_text_height / 2)

        # Calculate value text baseline for prefix/suffix alignment
        value_baseline_y = value_y + (value_metrics['ascent'] - value_metrics['descent']) / 2

        # Draw value text
        self._value_text_id = self._update_or_create_text(
            self._value_text_id, center_x, value_y,
            value_text, self._value_font, self._value_text_color, 'center'
        )

        # Position and draw prefix/suffix
        if self._value_prefix or self._value_suffix:
            value_width = value_font.measure(value_text)
            horizontal_gap = 4
            value_left_x = center_x - (value_width / 2) - horizontal_gap
            value_right_x = center_x + (value_width / 2) + horizontal_gap - 1

            # Calculate y position for prefix/suffix (baseline aligned, slightly raised)
            secondary_y = value_baseline_y - (secondary_metrics['ascent'] - secondary_metrics['descent']) / 2 - 4

            if self._value_prefix:
                self._prefix_text_id = self._update_or_create_text(
                    self._prefix_text_id, value_left_x, secondary_y,
                    self._value_prefix, self._secondary_font, self._secondary_text_color, 'e'
                )
            elif self._prefix_text_id:
                self._canvas.itemconfig(self._prefix_text_id, state='hidden')

            if self._value_suffix:
                self._suffix_text_id = self._update_or_create_text(
                    self._suffix_text_id, value_right_x, secondary_y,
                    self._value_suffix, self._secondary_font, self._secondary_text_color, 'w'
                )
            elif self._suffix_text_id:
                self._canvas.itemconfig(self._suffix_text_id, state='hidden')

        # Draw subtitle
        if self._subtitle:
            subtitle_y = value_y + (max_text_height / 2) - 4
            self._subtitle_text_id = self._update_or_create_text(
                self._subtitle_text_id, center_x, subtitle_y,
                self._subtitle_var.get(), self._secondary_font, self._secondary_text_color, 'n'
            )
        elif self._subtitle_text_id:
            self._canvas.itemconfig(self._subtitle_text_id, state='hidden')

    def _update_or_create_text(self, item_id, x, y, text, font, fill, anchor):
        """Update existing canvas text item or create new one.

        Args:
            item_id: Existing canvas item ID or None to create new.
            x: X coordinate for text position.
            y: Y coordinate for text position.
            text: Text string to display.
            font: Font specification.
            fill: Text color.
            anchor: Text anchor position (e.g., 'center', 'e', 'w').

        Returns:
            Canvas item ID.
        """
        if item_id is None:
            return self._canvas.create_text(x, y, text=text, font=font, fill=fill, anchor=anchor)
        else:
            self._canvas.itemconfig(item_id, text=text, font=font, fill=fill, state='normal')
            self._canvas.coords(item_id, x, y)
            return item_id

    def _hide_text_items(self):
        """Hide all text items on canvas."""
        if self._value_text_id:
            self._canvas.itemconfig(self._value_text_id, state='hidden')
        if self._prefix_text_id:
            self._canvas.itemconfig(self._prefix_text_id, state='hidden')
        if self._suffix_text_id:
            self._canvas.itemconfig(self._suffix_text_id, state='hidden')
        if self._subtitle_text_id:
            self._canvas.itemconfig(self._subtitle_text_id, state='hidden')

    def _draw_subtitle_centered(self):
        """Draw subtitle centered when show_text is False."""
        center_x = self._size // 2
        center_y = self._size // 2

        if self._subtitle_text_id is None:
            self._subtitle_text_id = self._canvas.create_text(
                center_x, center_y,
                text=self._subtitle_var.get(),
                font=self._secondary_font,
                fill=self._secondary_text_color,
                anchor='center'
            )
        else:
            self._canvas.itemconfig(
                self._subtitle_text_id,
                text=self._subtitle_var.get(),
                font=self._secondary_font,
                fill=self._secondary_text_color,
                state='normal'
            )
            self._canvas.coords(self._subtitle_text_id, center_x, center_y)

    def _draw_base_meter_images(self):
        """Draw meter background trough at high resolution."""
        self._resolve_meter_styles()
        self._base_image = Image.new(
            mode='RGBA',
            size=(self._size * self._image_scale, self._size * self._image_scale),
        )
        draw = ImageDraw.Draw(self._base_image)

        # Center the arc with equal margins on all sides
        margin = 10
        x1 = y1 = self._size * self._image_scale - margin
        width = self._thickness * self._image_scale

        if self._segment_width > 0:
            # segmented meter
            minvalue = self._arc_offset
            maxvalue = self._arc_range + self._arc_offset
            step = 2 if self._segment_width == 1 else self._segment_width

            for x in range(minvalue, maxvalue, step):
                draw.arc(
                    xy=(margin, margin, x1, y1),
                    start=x,
                    end=x + self._segment_width - 1,
                    fill=self._trough_color,
                    width=width
                )
        else:
            # default meter
            draw.arc(
                xy=(margin, margin, x1, y1),
                start=self._arc_offset,
                end=self._arc_range + self._arc_offset,
                fill=self._trough_color,
                width=width
            )

    def _draw_solid_indicator(self, draw):
        """Draw solid arc indicator from start to current value."""
        margin = 10
        x1 = y1 = self._size * self._image_scale - margin
        width = self._thickness * self._image_scale
        value_degrees = self._meter_value_as_degrees()

        if self._indicator_width > 0:
            draw.arc(
                xy=(margin, margin, x1, y1),
                start=value_degrees - self._indicator_width,
                end=value_degrees + self._indicator_width,
                fill=self._accent_color,
                width=width
            )
        else:
            draw.arc(
                xy=(margin, margin, x1, y1),
                start=self._arc_offset,
                end=value_degrees,
                fill=self._accent_color,
                width=width
            )

    def _draw_segment_indicator(self, draw):
        """Draw segmented arc indicator from start to current value."""
        value_degrees = self._meter_value_as_degrees()
        margin = 10
        x1 = y1 = self._size * self._image_scale - margin
        width = self._thickness * self._image_scale

        if self._indicator_width > 0:
            draw.arc(
                xy=(margin, margin, x1, y1),
                start=value_degrees - self._indicator_width,
                end=value_degrees + self._indicator_width,
                fill=self._accent_color,
                width=width
            )
        else:
            # Draw segments from arc start to current value in degrees
            minvalue = self._arc_offset
            maxvalue = value_degrees - 1
            step = self._segment_width

            for x in range(minvalue, maxvalue, step):
                draw.arc(
                    xy=(margin, margin, x1, y1),
                    start=x,
                    end=x + self._segment_width - 1,
                    fill=self._accent_color,
                    width=width
                )

    def _meter_value_as_degrees(self):
        """Convert current meter value to arc degrees.

        Returns:
            Degree value for meter indicator position.
        """
        minvalue = self._minvalue
        maxvalue = self._maxvalue
        value = self._value_var.get()

        # normalize to 0-1 range to handle negative values
        range_size = maxvalue - minvalue
        if range_size == 0:
            normalized = 0
        else:
            normalized = (value - minvalue) / range_size

        return int(normalized * self._arc_range + self._arc_offset)

    def _handle_theme_changed(self, *_):
        self._resolve_meter_styles()
        self._canvas.configure(background=self._surface)
        self._draw_base_meter_images()
        self._draw_meter()

    def _handle_interaction(self, e):
        """Handle mouse clicks/drags to update meter value in interactive mode."""
        dx = e.x - self._size // 2
        dy = e.y - self._size // 2
        rads = math.atan2(dy, dx)
        degrees = math.degrees(rads)

        if degrees > self._arc_offset:
            factor = degrees - self._arc_offset
        else:
            factor = 360 + degrees - self._arc_offset

        # clamp the value between `minvalue` and `maxvalue`
        minvalue = self._minvalue
        maxvalue = self._maxvalue
        last_value = self._value_var.get()

        # calculate the value based on the range
        range_size = maxvalue - minvalue
        value = (range_size / self._arc_range * factor) + minvalue

        # calculate the value given the stepsize.
        if self._step_size > 0:
            # round to the nearest stepsize
            value = round(value / self._step_size) * self._step_size

        # if the number is the same, then do not redraw
        if last_value == value:
            return

        # update the value variable
        self._value_var.set(max(min(value, maxvalue), minvalue))

    def step(self, delta: int | float = 1):
        """Increment or decrement meter value with automatic bounce at limits.

        Args:
            delta: Amount to step by (default 1).
        """
        value = self._value_var.get()
        minvalue = self._minvalue
        maxvalue = self._maxvalue

        if self._towards_maximum:
            value_updated = value + delta
        else:
            value_updated = value - delta

        if value_updated >= maxvalue:
            self._towards_maximum = False
            self._value_var.set(maxvalue - (value_updated - maxvalue))
        elif value_updated < minvalue:
            self._towards_maximum = True
            self._value_var.set(minvalue + (minvalue - value_updated))
        else:
            self._value_var.set(value_updated)

    def on_changed(self, callback: Callable[[Any], Any]) -> str:
        """Bind a callback to the ``<<Change>>`` virtual event."""
        return self.bind('<<Change>>', callback, add="+")

    def off_changed(self, bind_id: str):
        """Remove a previously registered ``<<Change>>`` callback."""
        self.unbind('<<Change>>', bind_id)

