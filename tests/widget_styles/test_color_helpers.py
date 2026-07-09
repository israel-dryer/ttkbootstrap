'''Tests for private color ramps and StyleBuilderTTK color derivation.'''

import ast
from collections import Counter
from pathlib import Path

import pytest

from ttkbootstrap.style.theme import (
    Colors,
    _ON_COLOR_WHITE_FLOOR,
    _cached_color_ramp,
    _color_ramp,
    _contrast_ratio,
    _mix_colors,
    _relative_luminance,
    _shade,
    _state_color,
    _tint,
)


RAMP_STOPS = tuple(range(50, 1000, 50))
BUILDERS_DIR = (
    Path(__file__).parents[2] / 'src' / 'ttkbootstrap' / 'style' / 'builders'
)


def test_ramp_matches_bootstrap_scale_and_is_immutable():
    ramp = _color_ramp('#0d6efd')

    assert tuple(ramp) == RAMP_STOPS
    assert [ramp[stop] for stop in range(100, 1000, 100)] == [
        '#cfe2ff',
        '#9ec5fe',
        '#6ea8fe',
        '#3d8bfd',
        '#0d6efd',
        '#0a58ca',
        '#084298',
        '#052c65',
        '#031633',
    ]
    with pytest.raises(TypeError):
        ramp[500] = '#ffffff'


def test_ramp_normalizes_equivalent_colors_and_is_monotonic():
    short = _color_ramp('#abc')
    named = _color_ramp('white')

    assert short is _color_ramp('#aabbcc')
    assert named[500] == '#ffffff'
    assert all(
        _relative_luminance(short[left]) >= _relative_luminance(short[right])
        for left, right in zip(RAMP_STOPS, RAMP_STOPS[1:])
    )
    with pytest.raises(ValueError):
        _color_ramp('not-a-color')


def test_ramp_cache_is_bounded():
    _cached_color_ramp.cache_clear()
    try:
        for value in range(300):
            _color_ramp(f'#{value:06x}')
        info = _cached_color_ramp.cache_info()
        assert info.maxsize == 256
        assert info.currsize == 256
    finally:
        _cached_color_ramp.cache_clear()


@pytest.mark.parametrize(
    ('color', 'active', 'pressed', 'direction'),
    [
        ('#2780e3', '#388ae5', '#408fe6', 'lighter'),
        ('#f8f9fa', '#e0e5e9', '#d5dbe1', 'darker'),
    ],
)
def test_state_colors_match_bootstack_hls_policy(
    color, active, pressed, direction
):
    actual_active = _state_color(color, 'active')
    actual_pressed = _state_color(color, 'pressed')

    assert actual_active == active
    assert actual_pressed == pressed
    base_lum = _relative_luminance(color)
    active_lum = _relative_luminance(actual_active)
    pressed_lum = _relative_luminance(actual_pressed)
    if direction == 'lighter':
        assert base_lum < active_lum < pressed_lum
    else:
        assert base_lum > active_lum > pressed_lum


def test_mix_and_contrast_primitives():
    assert _mix_colors('#000000', '#ffffff', 0.5) == '#808080'
    assert _contrast_ratio('#000000', '#ffffff') == pytest.approx(21.0)


def test_tint_and_shade_move_toward_white_and_black():
    color = '#2780e3'
    tinted = _tint(color, 0.2)
    shaded = _shade(color, 0.2)

    assert tinted == _mix_colors('#ffffff', color, 0.2)
    assert shaded == _mix_colors('#000000', color, 0.2)
    # tint lightens, shade darkens, regardless of the color
    assert _relative_luminance(tinted) > _relative_luminance(color)
    assert _relative_luminance(shaded) < _relative_luminance(color)
    # zero weight is a no-op; full weight reaches the target
    assert _tint(color, 0.0) == color
    assert _shade(color, 1.0) == '#000000'


def _channels(hex_color):
    return Colors.hex_to_rgb(hex_color)


def test_shade_tint_mute_builder_helpers(root):
    style = root.style
    style.theme_use('bootstrap-dark')
    builder = style._get_builder()

    # shade() darkens a fill toward black (the recessed-trough recipes)
    fill = builder.colors.selectbg
    assert builder.shade(fill) == _shade(fill, 0.2)
    assert _relative_luminance(builder.shade(fill)) < _relative_luminance(fill)

    # tint() lightens a fill toward white (progress stripe / floodgauge wash)
    bar = builder.colors.primary
    assert builder.tint(bar) == _tint(bar, 0.2)
    assert builder.tint(bar, 0.7) == _tint(bar, 0.7)
    assert _relative_luminance(builder.tint(bar)) > _relative_luminance(bar)

    # mute() reproduces the old make_transparent(0.4) alpha blend within 1/255
    fg, bg = builder.colors.fg, builder.colors.bg
    muted = builder.mute(fg)
    legacy = Colors.make_transparent(0.4, fg, bg)
    assert muted == _mix_colors(fg, bg, 0.4)
    assert all(
        abs(m - l) <= 1
        for m, l in zip(_channels(muted), _channels(legacy))
    )


def test_light_theme_builder_helpers(root):
    style = root.style
    style.theme_use('bootstrap-light')
    builder = style._get_builder()

    assert builder.active('#2780e3') == '#388ae5'
    assert builder.pressed('#2780e3') == '#408fe6'
    assert builder.on_color(builder.colors.primary) == '#ffffff'
    assert builder.on_color(builder.colors.warning) == '#000000'
    assert builder.border(builder.colors.primary) == _mix_colors(
        builder.colors.primary, '#ffffff', 0.84
    )
    assert builder.disabled('text') == '#cccfd2'
    assert builder.disabled() == '#fafbfb'
    assert builder.disabled('text', '#eeeeee') == '#c0c4c6'
    with pytest.raises(ValueError, match='Invalid role'):
        builder.disabled('icon')


def test_dark_theme_builder_helpers(root):
    style = root.style
    style.theme_use('bootstrap-dark')
    builder = style._get_builder()

    assert builder.on_color(builder.colors.primary) == '#ffffff'
    assert builder.on_color(builder.colors.light) == '#000000'
    assert builder.border(builder.colors.primary) == _mix_colors(
        builder.colors.primary, '#ffffff', 0.84
    )
    # dark disabled blends: 25% #adb5bd (text) / 20% #495057 (bg) over the
    # surface; computed from the documented weights so the check is
    # theme-robust rather than pinned to one theme's background.
    assert builder.disabled('text') == _mix_colors('#adb5bd', builder.colors.bg, 0.25)
    assert builder.disabled() == _mix_colors('#495057', builder.colors.bg, 0.20)


def test_on_color_is_safe_and_independent_of_legacy_toggle(root):
    style = root.style
    previous = style.dynamic_foreground
    try:
        for theme in (
            'bootstrap-light',
            'minty-light',
            'catppuccin-light',
            'bootstrap-dark',
            'solarized-dark',
            'vapor-dark',
        ):
            style.theme_use(theme)
            builder = style._get_builder()
            style.use_dynamic_foreground(False)
            disabled_result = {
                label: builder.on_color(builder.colors.get(label))
                for label in builder.colors
            }
            style.use_dynamic_foreground(True)
            enabled_result = {
                label: builder.on_color(builder.colors.get(label))
                for label in builder.colors
            }
            assert enabled_result == disabled_result
            for label, foreground in enabled_result.items():
                # White is preferred on vivid accents even where WCAG contrast
                # understates it, so the guaranteed floor is the white floor,
                # not the 3:1 bold-text target. See `_accent_on_color`.
                assert _contrast_ratio(
                    foreground, builder.colors.get(label)
                ) >= _ON_COLOR_WHITE_FLOOR, label
    finally:
        style.use_dynamic_foreground(previous)


def test_direct_color_math_is_limited_to_special_effects():
    # After the color-math fast-follow, ttk recipes carry ZERO direct
    # Colors.update_hsv / Colors.make_transparent calls: state and surface
    # derivation goes through the builder helpers (active/pressed/border/
    # disabled/on_color/shade/tint/mute). A genuinely new special effect that
    # needs raw HSV/alpha must be re-added here with a reason.
    expected = Counter()
    actual = Counter()
    for path in BUILDERS_DIR.glob('*.py'):
        tree = ast.parse(path.read_text(encoding='utf-8'))
        parents = {
            child: node
            for node in ast.walk(tree)
            for child in ast.iter_child_nodes(node)
        }
        for node in ast.walk(tree):
            if not (
                isinstance(node, ast.Call)
                and isinstance(node.func, ast.Attribute)
                and isinstance(node.func.value, ast.Name)
                and node.func.value.id == 'Colors'
                and node.func.attr in {'update_hsv', 'make_transparent'}
            ):
                continue
            owner = node
            while owner in parents and not isinstance(owner, ast.FunctionDef):
                owner = parents[owner]
            actual[(path.name, owner.name, node.func.attr)] += 1

    assert actual == expected


@pytest.mark.parametrize(
    ('theme', 'colorname'),
    [('bootstrap-light', 'warning'), ('bootstrap-dark', 'primary')],
)
def test_solid_button_recipe_uses_helper_state_contract(
    root, theme, colorname
):
    style = root.style
    style.theme_use(theme)
    builder = style._get_builder()
    builder.build_style('default', 'button', colorname, required=True)
    ttkstyle = f'{colorname}.TButton'
    background = builder.colors.get(colorname)
    active = builder.active(background)
    pressed = builder.pressed(background)

    config = style.configure(ttkstyle)
    def option_map(style_name, option):
        return {
            tuple(item[:-1]): str(item[-1]).lower()
            for item in style.map(style_name, option)
        }

    background_map = option_map(ttkstyle, 'background')
    foreground_map = option_map(ttkstyle, 'foreground')
    assert config['foreground'].lower() == builder.on_color(background)
    # Every solid button has a subtle 1px border derived from its own fill.
    # At rest the clam dark/light regions track the fill, so the resting edge is
    # just the distinct `bordercolor`; the face stays the fill.
    assert config['bordercolor'].lower() == builder.border(background)
    assert config['darkcolor'].lower() == background
    assert config['lightcolor'].lower() == background
    assert background_map[('hover', '!disabled')].lower() == active
    assert background_map[('pressed', '!disabled')].lower() == pressed
    disabled = builder.disabled()
    assert foreground_map[('disabled',)].lower() == builder.disabled(
        'text', disabled
    )

    # The button-family solid recipes (button/menubutton/toolbutton) now share
    # the hairline-border treatment: a `bordercolor` derived from the fill, with
    # the clam dark/light regions tracking the fill (no two-tone bevel).
    for family, variant in (
        ('menubutton', 'default'),
        ('toolbutton', 'default'),
        ('calendar', 'default'),
    ):
        builder.build_style(variant, family, colorname, required=True)

    menubutton = f'{colorname}.TMenubutton'
    assert style.configure(menubutton)['bordercolor'].lower() == builder.border(background)
    # dark/light follow the fill; bordercolor is the fill's derived border
    assert option_map(menubutton, 'darkcolor')[('hover', '!disabled')] == active
    assert option_map(menubutton, 'bordercolor')[('hover', '!disabled')] == builder.border(active)

    # The solid toolbutton now carries the same border; its selected state fills
    # with the accent and dark/light track that fill.
    toolbutton = f'{colorname}.Toolbutton'
    assert 'bordercolor' in style.configure(toolbutton)
    assert option_map(toolbutton, 'background')[('selected', '!disabled')] == background
    assert option_map(toolbutton, 'darkcolor')[('selected', '!disabled')] == background

    calendar = f'{colorname}.TCalendar'
    calendar_bg = option_map(calendar, 'background')
    calendar_border = option_map(calendar, 'bordercolor')
    assert calendar_border[('hover', '!disabled')] == calendar_bg[
        ('hover', '!disabled')
    ]
    assert calendar_border[('pressed', '!disabled')] == calendar_bg[
        ('pressed', '!disabled')
    ]

    # Input controls now use the derived `colors.border` in BOTH modes: the old
    # dark-mode `selectbg` border workaround (needed when authored dark themes
    # had border == bg) is retired, since `colors.border` is a proper visible
    # border in dark themes too. The readonly fill stays a neutral (light: the
    # `light` accent; dark: `selectbg`).
    border = builder.colors.border.lower()
    # readonly fields read like normal fields now (fieldbackground == inputbg).
    readonly = builder.colors.inputbg.lower()
    for family, style_name in (
        ('entry', 'TEntry'),
        ('combobox', 'TCombobox'),
        ('spinbox', 'TSpinbox'),
    ):
        builder.build_style('default', family, '', required=True)
        assert style.configure(style_name)['bordercolor'].lower() == border
        assert option_map(style_name, 'foreground')[
            ('disabled',)
        ] == builder.disabled('text', builder.colors.inputbg)
        assert option_map(style_name, 'fieldbackground')[
            ('readonly',)
        ] == readonly
