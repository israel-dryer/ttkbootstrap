from __future__ import annotations

from typing import TYPE_CHECKING

from ttkbootstrap.style.style_builder import StyleBuilder
from ttkbootstrap.style.style_element import Element, ElementImage

if TYPE_CHECKING:
    from ttkbootstrap.style.theme import Theme


class TTkSelectBoxStyle(StyleBuilder):

    def __init__(self, theme: Theme):
        super().__init__(theme)

    def invoke(self, color: str, **_):
        """Create the default button style"""

        style = f'{color}.TCombobox'

        if self.theme.has_style(style):
            return style

        ss = self.theme.scale_size
        color = color or "primary"

        # style colors
        shades = self.theme.get_shades(color)
        shades_lt = self.theme.get_shades('light')
        shades_bg = self.theme.get_shades('background')
        foreground = self.theme.background
        background = shades.base
        app_bg = self.theme.background
        disabled = shades_lt.d2 if self.theme.is_light_theme else shades_lt.d4
        outline = shades_lt.d3 if self.theme.is_dark_theme else shades_lt.d3
        hover_on = shades.l1 if self.theme.is_light_theme else shades.d1
        hover_off = shades_bg.l1 if self.theme.is_dark_theme else shades_lt.base
        pressed_off = shades_bg.l2 if self.theme.is_dark_theme else shades_lt.d1
        pressed_on = shades.l2 if self.theme.is_light_theme else shades.d2

        # create checkbutton assets
        img_size = ss(640, 640)
        final_size = ss(32, 32)
        rect_size = ss(10, 10, 630, 630)
        radius = img_size[0] * 0.12
        common = {'xy': rect_size, 'radius': radius}

        # off
        im, draw = self.theme.image_draw(img_size)
        draw.rounded_rectangle(
            **common, outline=outline, fill=app_bg,
            width=ss(24))
        img_off = self.theme.image_resize(im, final_size)
        self.theme.register_asset(str(img_off), img_off)

        # off/hover
        im, draw = self.theme.image_draw(img_size)
        draw.rounded_rectangle(
            **common, outline=outline, fill=hover_off,
            width=ss(24))
        img_off_hover = self.theme.image_resize(im, final_size)
        self.theme.register_asset(str(img_off_hover), img_off_hover)

        # off/pressed
        im, draw = self.theme.image_draw(img_size)
        draw.rounded_rectangle(
            **common, outline=outline, fill=pressed_off,
            width=ss(24))
        img_off_pressed = self.theme.image_resize(im, final_size)
        self.theme.register_asset(str(img_off_pressed), img_off_pressed)

        # on
        im, draw = self.theme.image_draw(img_size)
        draw.rounded_rectangle(
            **common, outline=shades_bg.d2, fill=background,
            width=ss(3))
        draw.line(
            ss(190, 330, 293, 433, 516, 210), width=ss(40),
            fill=foreground, joint='curve')
        img_on = self.theme.image_resize(im, final_size)
        self.theme.register_asset(str(img_on), img_on)

        # on/hover
        im, draw = self.theme.image_draw(img_size)
        draw.rounded_rectangle(
            **common, outline=shades_bg.d2, fill=hover_on,
            width=ss(3))
        draw.line(
            ss(190, 330, 293, 433, 516, 210), width=ss(40),
            fill=foreground, joint='curve')
        img_on_hover = self.theme.image_resize(im, final_size)
        self.theme.register_asset(str(img_on_hover), img_on_hover)

        # on/pressed
        im, draw = self.theme.image_draw(img_size)
        draw.rounded_rectangle(
            **common, outline=shades_bg.d2, fill=pressed_on,
            width=ss(3))
        draw.line(
            ss(190, 330, 293, 433, 516, 210), width=ss(40),
            fill=foreground, joint='curve')
        img_on_pressed = self.theme.image_resize(im, final_size)
        self.theme.register_asset(str(img_on_pressed), img_on_pressed)

        # on/disabled
        im, draw = self.theme.image_draw(img_size)
        draw.rounded_rectangle(
            **common, outline=disabled, fill=background,
            width=ss(3))
        draw.line(
            ss(190, 330, 293, 433, 516, 210), width=ss(40),
            fill=disabled, joint='curve')
        img_on_dis = self.theme.image_resize(im, final_size)
        self.theme.register_asset(str(img_on_dis), img_on_dis)

        # alt
        im, draw = self.theme.image_draw(img_size)
        draw.rounded_rectangle(
            **common, outline=shades_bg.d2, fill=background,
            width=ss(3))
        draw.line(ss(213, 320, 427, 320), width=ss(40), fill=foreground)
        img_alt = self.theme.image_resize(im, final_size)
        self.theme.register_asset(str(img_alt), img_alt)

        # alt
        im, draw = self.theme.image_draw(img_size)
        draw.rounded_rectangle(
            **common, outline=shades_bg.d2, fill=pressed_on,
            width=ss(3))
        draw.line(ss(213, 320, 427, 320), width=ss(40), fill=foreground)
        img_alt_pressed = self.theme.image_resize(im, final_size)
        self.theme.register_asset(str(img_alt_pressed), img_alt_pressed)

        # alt
        im, draw = self.theme.image_draw(img_size)
        draw.rounded_rectangle(
            **common, outline=shades_bg.d2, fill=hover_on,
            width=ss(3))
        draw.line(ss(213, 320, 427, 320), width=ss(40), fill=foreground)
        img_alt_hover = self.theme.image_resize(im, final_size)
        self.theme.register_asset(str(img_alt_hover), img_alt_hover)

        # alt/disabled
        im, draw = self.theme.image_draw(img_size)
        draw.rounded_rectangle(
            **common, outline=disabled, fill=background,
            width=ss(3))
        draw.line(ss(213, 320, 427, 320), width=ss(40), fill=disabled)
        img_alt_dis = self.theme.image_resize(im, final_size)
        self.theme.register_asset(str(img_alt_dis), img_alt_dis)

        # disabled
        im, draw = self.theme.image_draw(img_size)
        draw.rounded_rectangle(
            **common, outline=disabled, fill=foreground,
            width=ss(12))
        img_dis = self.theme.image_resize(im, final_size)
        self.theme.register_asset(str(img_dis), img_dis)

        # create image element
        element = style.replace('.TC', '.C')

        ind_elem = ElementImage(
            f'{element}.indicator', img_on,
            border=ss(24, 0), sticky="ns")
        ind_elem.add_spec('disabled selected', img_on_dis)
        ind_elem.add_spec('disabled alternate', img_alt_dis)
        ind_elem.add_spec('disabled', img_dis)
        ind_elem.add_spec('pressed alternate !disabled', img_alt_pressed)
        ind_elem.add_spec('pressed !selected !disabled', img_off_pressed)
        ind_elem.add_spec('pressed selected !disabled', img_on_pressed)
        ind_elem.add_spec('hover alternate !disabled', img_alt_hover)
        ind_elem.add_spec('hover !selected !disabled', img_off_hover)
        ind_elem.add_spec('hover selected !disabled', img_on_hover)
        ind_elem.add_spec('alternate', img_alt)
        ind_elem.add_spec('!selected', img_off)
        ind_elem.build()

        # normal state style
        self.theme.configure(
            style,
            foreground=self.theme.foreground,
            background=self.theme.background,
            focuscolor='')

        # state mapping
        self.theme.map(style, foreground=[('disabled', disabled)])

        # style layout
        Element(style).layout(
            [
                Element('Checkbutton.padding', sticky="nsew"), [
                Element(f'{element}.indicator', side="left", sticky=''),
                Element('Checkbutton.focus', side="left"), [
                    Element('Checkbutton.label', sticky="nsew")]]])

        self.theme.add_style(style)
        return style
