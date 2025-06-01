from typing import NamedTuple, Union
from PIL import Image

from . import color_utils, image_utils, load_asset_image


class ColorPair(NamedTuple):
    color: str
    on_color: str


class ColorStates(NamedTuple):
    normal: ColorPair
    hover: ColorPair
    pressed: ColorPair
    selected: ColorPair
    disabled: ColorPair
    focused: ColorPair


def recolor_state_image(register_asset, image_path: str, color: str, is_light_theme: bool):
    img = load_asset_image(image_path)
    recolored = image_recolor(img, color, is_light_theme)
    register_asset(str(recolored), recolored)
    return recolored


def image_recolor(data: Union[str, Image.Image], color: str, is_light_theme: bool, overlay: Image.Image = None):
    white = color
    black = "#ffffff" if is_light_theme else "#000000"
    return image_utils.image_recolor_map(data, white, black, overlay)


def get_input_background(base_color: str, is_dark_theme: bool) -> str:
    return color_utils.adjust_color_lightness(base_color, -0.15 if is_dark_theme else 0.12)


def get_input_text_color(input_background: str) -> str:
    return color_utils.get_contrast_text_color(input_background)


def get_input_border_color(input_background: str, is_dark_theme: bool) -> str:
    return color_utils.adjust_color_lightness(input_background, 0.10 if is_dark_theme else -0.08)


def get_background_style(token: str, widget_class: str, container_bg: str, background: str = None):
    if background and background != container_bg:
        style = f'{background}.{token}.{widget_class}'
        container_bg = background
    else:
        style = f'{token}.{widget_class}'
    return container_bg, style


def get_foreground(
    color_name: str, *,
    dark: str, light: str, foreground: str, background: str, is_dark_theme: bool) -> str:
    match color_name:
        case "light":
            return dark
        case "dark":
            return light
        case "background":
            return foreground
        case "foreground":
            return background
        case "border":
            return foreground
        case _:
            return foreground if is_dark_theme else background


def get_disabled_color(fg: str, is_light_theme: bool, shift: float = 0.4) -> str:
    return color_utils.adjust_color_lightness(fg, shift if is_light_theme else -shift)


def blend_subtle_tint(base_color: str, surface_color: str, alpha: float) -> str:
    return color_utils.blend_colors(surface_color, base_color, alpha)


def adjust_for_contrast(base_color: str, surface_color: str, is_dark_theme: bool, min_ratio: float = 3.0) -> str:
    contrast = color_utils.get_contrast_ratio(base_color, surface_color)
    if contrast < min_ratio:
        return color_utils.adjust_color_for_theme_contrast(
            base_color, surface_color, is_dark_theme, min_ratio=min_ratio
        )
    return base_color


def get_default_color_states(
    base: ColorPair,
    surface_color: str,
    is_dark_theme: bool,
    token: str = "",
    adjust_contrast: bool = True
) -> ColorStates:
    hover_factor = 0.08
    pressed_factor = 0.16
    selected_factor = 0.10
    focused_factor = 0.12
    disabled_factor = 0.3
    foreground_shift = 0.4

    def lighten(c, f):
        return color_utils.adjust_color_lightness(c, abs(f))

    def darken(c, f):
        return color_utils.adjust_color_lightness(c, -abs(f))

    def adjust(c, f):
        return lighten(c, f) if is_dark_theme else darken(c, f)

    def fg_disabled(c):
        return lighten(c, foreground_shift) if not is_dark_theme else darken(c, foreground_shift)

    adjusted_color = base.color
    if adjust_contrast and token in {"light", "dark"}:
        contrast = color_utils.get_contrast_ratio(base.color, surface_color)
        if contrast < 3.0:
            adjusted_color = color_utils.adjust_color_for_theme_contrast(
                base.color, surface_color, is_dark_theme, min_ratio=3.0
            )

    hover_color = (
        lighten(base.color, 0.2)
        if (token == "light" and not is_dark_theme) or (token == "dark" and is_dark_theme)
        else adjust(adjusted_color, 0.08)
    )

    return ColorStates(
        normal=base,
        hover=ColorPair(hover_color, base.on_color),
        pressed=ColorPair(adjust(adjusted_color, pressed_factor), base.on_color),
        selected=ColorPair(adjust(adjusted_color, selected_factor), base.on_color),
        focused=ColorPair(adjust(adjusted_color, focused_factor), base.on_color),
        disabled=ColorPair(adjust(adjusted_color, disabled_factor), fg_disabled(base.on_color)),
    )


def get_outline_color_states(
    base: ColorPair,
    token: str,
    transparent_color: str,
    surface_color: str,
    is_dark_theme: bool
) -> ColorStates:
    solid = get_default_color_states(base, surface_color, is_dark_theme, token)

    def lighten(c, f): return color_utils.adjust_color_lightness(c, abs(f))

    def darken(c, f): return color_utils.adjust_color_lightness(c, -abs(f))

    def fg_disabled(c): return lighten(c, 0.4) if not is_dark_theme else darken(c, 0.4)

    return ColorStates(
        normal=ColorPair(transparent_color, base.color),
        hover=solid.hover,
        pressed=solid.pressed,
        selected=solid.selected,
        focused=solid.focused,
        disabled=ColorPair(transparent_color, fg_disabled(base.color)),
    )


def get_text_color_states(
    base: ColorPair,
    transparent_color: str,
    surface_color: str,
    is_light_theme: bool
) -> ColorStates:
    def fg_disabled(c): return color_utils.adjust_color_lightness(c, 0.4 if is_light_theme else -0.4)

    def tint(alpha): return blend_subtle_tint(base.color, surface_color, alpha)

    return ColorStates(
        normal=ColorPair(transparent_color, base.color),
        hover=ColorPair(tint(0.10), base.color),
        pressed=ColorPair(tint(0.20), base.color),
        selected=ColorPair(tint(0.18), base.color),
        focused=ColorPair(tint(0.14), base.color),
        disabled=ColorPair(transparent_color, fg_disabled(base.color)),
    )


def get_default_toolbutton_color_states(
    base: ColorPair,
    surface_color: str,
    is_dark_theme: bool,
    is_light_theme: bool,
    token: str
) -> ColorStates:
    return get_default_color_states(
        base=base,
        surface_color=surface_color,
        is_dark_theme=is_dark_theme,
        token=token
    )


def get_other_toolbutton_color_states(
    base: ColorPair,
    surface_color: str,
    is_light_theme: bool,
    transparent_color: str
) -> ColorStates:
    def fg_disabled(c): return color_utils.adjust_color_lightness(c, 0.4 if is_light_theme else -0.4)

    def tint(alpha): return blend_subtle_tint(base.color, surface_color, alpha)

    def solid(f): return color_utils.adjust_color_lightness(base.color, -f if is_light_theme else f)

    return ColorStates(
        normal=ColorPair(tint(0.08), base.color),
        hover=ColorPair(tint(0.20), base.color),
        pressed=ColorPair(solid(0.16), base.on_color),
        selected=ColorPair(solid(0.12), base.on_color),
        focused=ColorPair(solid(0.10), base.on_color),
        disabled=ColorPair(transparent_color, fg_disabled(base.color)),
    )
