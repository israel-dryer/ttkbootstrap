"""Field widget style builders.

This module contains style builders for ttk.Frame widget and field variants used to build
the Entry containers.
"""

from __future__ import annotations

from ttkbootstrap_icons_bs import BootstrapIcon

from ttkbootstrap.style.bootstyle_builder_ttk import BootstyleBuilderTTk
from ttkbootstrap.style.element import Element, ElementImage
from ttkbootstrap.style.utility import recolor_image


@BootstyleBuilderTTk.register_builder('default', 'TField')
def build_field_style(b: BootstyleBuilderTTk, ttk_style: str, accent: str = None, **options):
    surface_token = options.get('surface', 'background')

    surface = b.color(surface_token)
    accent_color = b.color(accent or 'primary')
    normal = surface
    border = b.border(surface)
    disabled = b.disabled('text')
    focused_border = b.focus_border(accent_color)
    focused_ring = b.focus_ring(accent_color, surface)

    # input element images
    normal_img = recolor_image(f'input', normal, border, surface)
    focused_img = recolor_image(f'input', normal, focused_border, focused_ring)
    disabled_img = recolor_image(f'input', normal, disabled, surface, surface)

    # input element
    b.create_style_element_image(
        ElementImage(f'{ttk_style}.border', normal_img, sticky="nsew", border=b.scale(8)).state_specs(
            [
                ('disabled', disabled_img),
                ('focus', focused_img),
            ]
        )
    )
    b.create_style_layout(
        ttk_style, Element(f'{ttk_style}.border', sticky="nsew").children(
            [
                Element(f'{ttk_style}.padding', sticky="")
            ]))
    b.configure_style(ttk_style, background=surface)


@BootstyleBuilderTTk.register_builder('input', 'TField')
def build_field_input_style(b: BootstyleBuilderTTk, ttk_style: str, accent: str = None, **options):
    surface_token = options.get('surface', 'background')
    surface = b.color(surface_token)
    disabled_bg = b.disabled('background')
    disabled_fg = b.disabled('text')
    foreground = b.on_color(surface)

    normal_img = recolor_image('field', surface)
    b.create_style_element_image(ElementImage(f'{ttk_style}.field', normal_img, sticky="nsew", height=b.scale(31)))
    b.create_style_layout(
        ttk_style, Element(f'{ttk_style}.field').children(
            [
                Element('Entry.padding', sticky="ew").children(
                    [
                        Element('Entry.textarea', sticky="nsew")
                    ])
            ]))

    b.configure_style(
        ttk_style,
        relief='flat',
        foreground=foreground,
        background=surface,
        fieldbackground=surface,
        selectborderwidth=0,
        bordercolor=surface,
        darkcolor=surface,
        lightcolor=surface,
        insertcolor=foreground,
        padding=(7, 0),
        selectforeground=b.on_color(b.color('primary')),
        selectbackground=b.color('primary')
    )

    b.map_style(
        ttk_style,
        background=[('disabled', disabled_bg), ('readonly', disabled_bg)],
        fieldbackground=[('disabled', disabled_bg)],
        selectforeground=[],
        selectbackground=[],
        bordercolor=[('disabled', disabled_bg)],
        darkcolor=[('disabled', disabled_bg)],
        lightcolor=[('disabled', disabled_bg)],
        foreground=[('disabled !readonly', disabled_fg), ('', foreground)],
    )

@BootstyleBuilderTTk.register_builder('spinner', 'TField')
def build_spinner_input_style(b: BootstyleBuilderTTk, ttk_style: str, accent: str = None, **options):
    surface_token = options.get('surface', 'background')

    surface = b.color(surface_token)
    disabled_bg = b.disabled('background')
    disabled_fg = b.disabled('text')
    foreground = b.on_color(surface)

    normal_img = recolor_image('field', surface)
    b.create_style_element_image(ElementImage(f'{ttk_style}.field', normal_img, sticky="nsew", height=b.scale(31)))

    # add chevron image
    icon_size = b.scale(14)
    arrow_up_normal_img = BootstrapIcon('caret-up-fill', color=foreground, size=icon_size).image
    arrow_up_disabled_img = BootstrapIcon('caret-up-fill', color=disabled_fg, size=icon_size).image
    arrow_down_normal_img = BootstrapIcon('caret-down-fill', color=foreground, size=icon_size).image
    arrow_down_disabled_img = BootstrapIcon('caret-down-fill', color=disabled_fg, size=icon_size).image

    b.create_style_element_image(
        ElementImage(f'{ttk_style}.uparrow', arrow_up_normal_img, sticky='nsew', width=b.scale(16)).state_specs(
            [
                ('disabled', arrow_up_disabled_img),
                ('', arrow_up_normal_img),
            ])
    )

    b.create_style_element_image(
        ElementImage(f'{ttk_style}.downarrow', arrow_down_normal_img, sticky='nsew', width=b.scale(16)).state_specs(
            [
                ('disabled', arrow_down_disabled_img),
                ('', arrow_down_normal_img),
            ])
    )


    b.create_style_layout(
        ttk_style,
        Element(f'{ttk_style}.field', sticky="ew", side="top").children(
            [
                Element('null', side='right', sticky='').children(
                    [
                        Element(f'{ttk_style}.uparrow', side='top', sticky='e'),
                        Element(f'{ttk_style}.downarrow', side='bottom', sticky='e'),
                    ]),
                Element('Spinbox.padding', sticky='nsew').children(
                    [
                        Element('Spinbox.textarea', sticky='nsew'),
                    ])
            ]),
    )

    b.configure_style(
        ttk_style,
        relief='flat',
        foreground=foreground,
        background=surface,
        fieldbackground=surface,
        selectborderwidth=0,
        bordercolor=surface,
        darkcolor=surface,
        lightcolor=surface,
        insertcolor=foreground,
        padding=(7, 0),
        selectforeground=b.on_color(b.color('primary')),
        selectbackground=b.color('primary')
    )

    b.map_style(
        ttk_style,
        background=[('disabled', disabled_bg), ('readonly', disabled_bg)],
        fieldbackground=[('disabled', disabled_bg)],
        selectforeground=[],
        selectbackground=[],
        bordercolor=[('disabled', disabled_bg)],
        darkcolor=[('disabled', disabled_bg)],
        lightcolor=[('disabled', disabled_bg)],
        foreground=[('disabled !readonly', disabled_fg), ('', foreground)],
    )


@BootstyleBuilderTTk.register_builder('prefix', 'TField')
def build_field_prefix_style(b: BootstyleBuilderTTk, ttk_style: str, accent: str = None, **options):
    build_field_addon_style(b, ttk_style, accent, 'prefix', **options)


@BootstyleBuilderTTk.register_builder('suffix', 'TField')
def build_field_suffix_style(b: BootstyleBuilderTTk, ttk_style: str, accent: str = None, **options):
    build_field_addon_style(b, ttk_style, accent, 'suffix', **options)


def build_field_addon_style(b: BootstyleBuilderTTk, ttk_style: str, _: str, variant: str, **options):
    surface_token = options.get('surface', 'background')
    use_active_states = options.get('use_active_states', False)
    surface = b.color(surface_token)

    if use_active_states:
        surface_active = b.active(surface)
        surface_pressed = b.pressed(surface)
    else:
        surface_active = surface_pressed = surface

    border = b.border(surface)
    foreground = b.on_color(surface)
    foreground_disabled = b.disabled('text')
    normal = b.disabled(surface=surface)

    # button element images
    normal_img = recolor_image(f'input-{variant}', normal, border)

    if use_active_states:
        active_img = recolor_image(f'input-{variant}', surface_active, border)
        pressed_img = recolor_image(f'input-{variant}', surface_pressed, border)
    else:
        active_img = pressed_img = normal_img

    # button element
    b.create_style_element_image(

        ElementImage(f'{ttk_style}.border', normal_img, height=b.scale(31), border=b.scale(8)).state_specs([
            ('pressed', pressed_img),
            ('active', active_img),
            ('', normal_img)
        ]))

    b.create_style_layout(
        ttk_style, Element(f"{ttk_style}.border", sticky="nsew").children(
            [
                Element("Button.padding", sticky="nsew").children(
                    [
                        Element("Button.label", sticky="nsew")
                    ])
            ]))

    b.configure_style(
        ttk_style,
        background=surface,
        foreground=foreground,
        relief='flat',
        stipple="gray12",
        padding=0
    )

    # map icon if available
    icon = options.get('icon')

    state_spec = dict(
        foreground=[
            ('disabled', foreground_disabled),
            ('pressed !disabled', foreground),
            ('hover !disabled', foreground),
            ('', foreground)
        ])

    if icon is not None:
        icon = b.normalize_icon_spec(icon)
        icon['size'] = b.scale(17)
        state_spec['image'] = b.map_stateful_icons(icon, state_spec['foreground'])

    b.map_style(ttk_style, **state_spec)
