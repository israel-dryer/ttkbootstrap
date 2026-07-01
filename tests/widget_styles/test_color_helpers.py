'''Tests for private color ramps and StyleBuilderTTK color derivation.'''

import ast
from collections import Counter
from pathlib import Path

import pytest

from ttkbootstrap.style.theme import (
    _ON_COLOR_WHITE_FLOOR,
    _cached_color_ramp,
    _color_ramp,
    _contrast_ratio,
    _mix_colors,
    _relative_luminance,
    _state_color,
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


def test_light_theme_builder_helpers(root):
    style = root.style
    style.theme_use('flatly')
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
    style.theme_use('darkly')
    builder = style._get_builder()

    assert builder.on_color(builder.colors.primary) == '#ffffff'
    assert builder.on_color(builder.colors.light) == '#000000'
    assert builder.border(builder.colors.primary) == _mix_colors(
        builder.colors.primary, '#ffffff', 0.84
    )
    assert builder.disabled('text') == '#454749'
    assert builder.disabled() == '#2a2b2d'


def test_on_color_is_safe_and_independent_of_legacy_toggle(root):
    style = root.style
    previous = style.dynamic_foreground
    try:
        for theme in (
            'flatly',
            'minty',
            'morph',
            'darkly',
            'solar',
            'vapor',
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
    expected = Counter(
        {
            ('checkbutton.py', 'build_checkbutton_style', 'make_transparent'): 1,
            ('floodgauge.py', 'build_floodgauge_style', 'update_hsv'): 1,
            ('label.py', 'build_meter_label_style', 'update_hsv'): 1,
            ('progressbar.py', '_create_striped_progressbar_assets', 'update_hsv'): 1,
            ('progressbar.py', 'build_striped_progressbar_style', 'update_hsv'): 1,
            ('progressbar.py', '_create_recolored_progressbar_style', 'update_hsv'): 1,
            ('radiobutton.py', 'build_radiobutton_style', 'make_transparent'): 1,
            ('scale.py', '_create_scale_assets', 'update_hsv'): 1,
            ('toggle.py', 'build_round_toggle_style', 'make_transparent'): 1,
            ('toggle.py', 'build_square_toggle_style', 'make_transparent'): 1,
        }
    )
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
    [('flatly', 'warning'), ('darkly', 'primary')],
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
    # This clam recipe has no separately rendered border treatment: its
    # border/dark/light colors intentionally track the button face.
    assert config['bordercolor'].lower() == background
    assert background_map[('hover', '!disabled')].lower() == active
    assert background_map[('pressed', '!disabled')].lower() == pressed
    disabled = builder.disabled()
    assert foreground_map[('disabled',)].lower() == builder.disabled(
        'text', disabled
    )

    # Options named "border" are not automatically semantic borders. These
    # recipes deliberately paint their clam border/dark/light regions with the
    # same color as the current face.
    for family, variant in (
        ('menubutton', 'default'),
        ('toolbutton', 'default'),
        ('calendar', 'default'),
    ):
        builder.build_style(variant, family, colorname, required=True)

    menubutton = f'{colorname}.TMenubutton'
    assert style.configure(menubutton)['bordercolor'].lower() == background
    assert option_map(menubutton, 'bordercolor')[
        ('hover', '!disabled')
    ] == active

    toolbutton = f'{colorname}.Toolbutton'
    assert option_map(toolbutton, 'bordercolor')[
        ('selected', '!disabled')
    ] == background

    calendar = f'{colorname}.TCalendar'
    calendar_bg = option_map(calendar, 'background')
    calendar_border = option_map(calendar, 'bordercolor')
    assert calendar_border[('hover', '!disabled')] == calendar_bg[
        ('hover', '!disabled')
    ]
    assert calendar_border[('pressed', '!disabled')] == calendar_bg[
        ('pressed', '!disabled')
    ]

    # Input controls keep their theme-authored structural border and readonly
    # fill; only their disabled foreground moves to the helper contract.
    structural = (
        builder.colors.border
        if builder.is_light_theme
        else builder.colors.selectbg
    ).lower()
    readonly = (
        builder.colors.light
        if builder.is_light_theme
        else structural
    ).lower()
    for family, style_name in (
        ('entry', 'TEntry'),
        ('combobox', 'TCombobox'),
        ('spinbox', 'TSpinbox'),
    ):
        builder.build_style('default', family, '', required=True)
        assert style.configure(style_name)['bordercolor'].lower() == structural
        assert option_map(style_name, 'foreground')[
            ('disabled',)
        ] == builder.disabled('text', builder.colors.inputbg)
        assert option_map(style_name, 'fieldbackground')[
            ('readonly',)
        ] == readonly

    builder.build_style('date', 'button', colorname, required=True)
    assert option_map(f'{colorname}.Date.TButton', 'image')[('disabled',)]
