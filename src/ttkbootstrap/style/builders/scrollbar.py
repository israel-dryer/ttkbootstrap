"""Scrollbar style builders.

This module contains style builders for ttk.Scrollbar widget variants.
"""
from ttkbootstrap.appconfig import use_icon_provider
from ttkbootstrap.style.bootstyle_builder_ttk import BootstyleBuilderTTk
from ttkbootstrap.style.element import Element, ElementImage
from ttkbootstrap.style.utility import recolor_image


@BootstyleBuilderTTk.register_builder('square', 'TScrollbar')
def build_scrollbar_style(b: BootstyleBuilderTTk, ttk_style: str, color: str = None, **options):
    if options.get('orient', 'vertical') == 'vertical':
        build_vertical_scrollbar(b, ttk_style, color, **options)
    else:
        build_horizontal_scrollbar(b, ttk_style, color, **options)


def build_horizontal_scrollbar(b: BootstyleBuilderTTk, ttk_style: str, color: str = None, **options):
    surface_token = options.get('surface_color', 'background')
    surface = b.color(surface_token)
    border_color = b.border(surface)

    if color is not None:
        thumb_normal = b.color(color)
    else:
        thumb_normal = border_color

    thumb_active = b.active(thumb_normal)
    thumb_pressed = b.pressed(thumb_normal)

    show_arrows = options.get('show_arrows', True)
    if show_arrows:
        # arrow elements
        icon = use_icon_provider()
        arrow_size = b.scale(18)

        # arrow elements
        icon = use_icon_provider()
        arrow_size = b.scale(18)

        # arrow [left]
        arrow_left_normal = icon('caret-left-fill', arrow_size, thumb_normal)
        arrow_left_active = icon('caret-left-fill', arrow_size, thumb_active)
        arrow_left_pressed = icon('caret-left-fill', arrow_size, thumb_pressed)
        b.create_style_element_image(
            ElementImage(
                f'{ttk_style}.leftarrow', arrow_left_normal,
                padding=2, border=2, width=arrow_size, height=arrow_size).state_specs(
                [
                    ('pressed', arrow_left_pressed),
                    ('active', arrow_left_active),
                    ('', arrow_left_normal),
                ])
        )

        # arrow [right]
        arrow_right_normal = icon('caret-right-fill', arrow_size, thumb_normal)
        arrow_right_active = icon('caret-right-fill', arrow_size, thumb_active)
        arrow_right_pressed = icon('caret-right-fill', arrow_size, thumb_pressed)
        b.create_style_element_image(
            ElementImage(
                f'{ttk_style}.rightarrow', arrow_right_normal,
                padding=2, border=2, width=arrow_size, height=arrow_size).state_specs(
                [
                    ('pressed', arrow_right_pressed),
                    ('active', arrow_right_active),
                    ('', arrow_right_normal),
                ])
        )

    scrollbar_elements = [
        Element(f'{ttk_style}.leftarrow', side="left", sticky=""),
        Element(f'{ttk_style}.rightarrow', side="right", sticky=""),
        Element(f'{ttk_style}.thumb', sticky="ew"),
    ]

    b.create_style_layout(
        ttk_style,
        Element('Horizontal.Scrollbar.trough', sticky="we").children(
            scrollbar_elements if show_arrows else [scrollbar_elements[-1]])
    )

    b.configure_style(
        ttk_style,
        background=thumb_normal,
        troughcolor=surface,
        padding=0,
        bordercolor=surface,
        darkcolor=thumb_normal,
        lightcolor=thumb_normal,
        gripcount=0,
        relief='flat',
        arrowsize=12,
    )
    b.map_style(
        ttk_style,
        background=[('pressed', thumb_pressed), ('active', thumb_active)],
        darkcolor=[('pressed', thumb_pressed), ('active', thumb_active)],
        lightcolor=[('pressed', thumb_pressed), ('active', thumb_active)],
    )


def build_vertical_scrollbar(b: BootstyleBuilderTTk, ttk_style: str, color: str = None, **options):
    surface_token = options.get('surface_color', 'background')
    surface = b.color(surface_token)
    border_color = b.border(surface)

    if color is not None:
        thumb_normal = b.color(color)
    else:
        thumb_normal = border_color

    thumb_active = b.active(thumb_normal)
    thumb_pressed = b.pressed(thumb_normal)

    show_arrows = options.get('show_arrows', True)
    if show_arrows:
        # arrow elements
        icon = use_icon_provider()
        arrow_size = b.scale(18)

        # arrow [up]
        arrow_up_normal = icon('caret-up-fill', arrow_size, thumb_normal)
        arrow_up_active = icon('caret-up-fill', arrow_size, thumb_active)
        arrow_up_pressed = icon('caret-up-fill', arrow_size, thumb_pressed)
        b.create_style_element_image(
            ElementImage(
                f'{ttk_style}.uparrow', arrow_up_normal,
                padding=2, border=2, width=arrow_size, height=arrow_size).state_specs(
                [
                    ('pressed', arrow_up_pressed),
                    ('active', arrow_up_active),
                    ('', arrow_up_normal),
                ])
        )

        # arrow [down]
        arrow_down_normal = icon('caret-down-fill', arrow_size, thumb_normal)
        arrow_down_active = icon('caret-down-fill', arrow_size, thumb_active)
        arrow_down_pressed = icon('caret-down-fill', arrow_size, thumb_pressed)
        b.create_style_element_image(
            ElementImage(
                f'{ttk_style}.downarrow', arrow_down_normal,
                padding=2, border=2, width=arrow_size, height=arrow_size).state_specs(
                [
                    ('pressed', arrow_down_pressed),
                    ('active', arrow_down_active),
                    ('', arrow_down_normal),
                ])
        )

    scrollbar_elements = [
        Element(f'{ttk_style}.uparrow', side="top", sticky=""),
        Element(f'{ttk_style}.downarrow', side="bottom", sticky=""),
        Element(f'{ttk_style}.thumb', sticky="ns"),
    ]

    b.create_style_layout(
        ttk_style,
        Element('Vertical.Scrollbar.trough', sticky="ns").children(
            scrollbar_elements if show_arrows else [scrollbar_elements[-1]]),
    )

    b.configure_style(
        ttk_style,
        background=thumb_normal,
        troughcolor=surface,
        padding=0,
        bordercolor=surface,
        darkcolor=thumb_normal,
        lightcolor=thumb_normal,
        gripcount=0,
        relief='flat',
        arrowsize=12,
    )
    b.map_style(
        ttk_style,
        background=[('pressed', thumb_pressed), ('active', thumb_active)],
        darkcolor=[('pressed', thumb_pressed), ('active', thumb_active)],
        lightcolor=[('pressed', thumb_pressed), ('active', thumb_active)],
    )

@BootstyleBuilderTTk.register_builder('default', 'TScrollbar')
@BootstyleBuilderTTk.register_builder('round', 'TScrollbar')
@BootstyleBuilderTTk.register_builder('rounded', 'TScrollbar')
def build_rounded_scrollbar_style(b: BootstyleBuilderTTk, ttk_style: str, color: str = None, **options):
    """
    Builds the 'rounded' scrollbar style

    Style options:
        * show_arrows

    """
    if options.get('orient', 'vertical') == 'vertical':
        _build_rounded_vertical_scrollbar(b, ttk_style, color, **options)
    else:
        _build_rounded_horizontal_scrollbar(b, ttk_style, color, **options)


def _build_rounded_vertical_scrollbar(b: BootstyleBuilderTTk, ttk_style: str, color: str = None, **options):
    surface_token = options.get('surface_color', 'background')
    surface = b.color(surface_token)
    border_color = b.border(surface)

    if color is not None:
        thumb_normal = b.color(color)
    else:
        thumb_normal = border_color

    thumb_active = b.active(thumb_normal)
    thumb_pressed = b.pressed(thumb_normal)

    # thumb element
    thumb_normal_img = recolor_image('scrollbar-vertical-rounded', thumb_normal, thumb_active, surface, surface)
    thumb_active_img = recolor_image('scrollbar-vertical-rounded', thumb_active, thumb_active, surface, surface)
    thumb_pressed_img = recolor_image('scrollbar-vertical-rounded', thumb_pressed, thumb_pressed, surface, surface)

    b.create_style_element_image(
        ElementImage(
            f'{ttk_style}.thumb', thumb_normal_img,
            padding=b.scale(3), border=b.scale(6), width=b.scale(10), height=b.scale(30)).state_specs(
            [
                ('pressed', thumb_pressed_img),
                ('active', thumb_active_img),
                ('', thumb_normal_img),
            ]),
    )

    show_arrows = options.get('show_arrows', True)
    if show_arrows:
        # arrow elements
        icon = use_icon_provider()
        arrow_size = b.scale(18)

        # arrow [up]
        arrow_up_normal = icon('caret-up-fill', arrow_size, thumb_normal)
        arrow_up_active = icon('caret-up-fill', arrow_size, thumb_active)
        arrow_up_pressed = icon('caret-up-fill', arrow_size, thumb_pressed)
        b.create_style_element_image(
            ElementImage(
                f'{ttk_style}.uparrow', arrow_up_normal,
                padding=2, border=2, width=arrow_size, height=arrow_size).state_specs(
                [
                    ('pressed', arrow_up_pressed),
                    ('active', arrow_up_active),
                    ('', arrow_up_normal),
                ])
        )

        # arrow [down]
        arrow_down_normal = icon('caret-down-fill', arrow_size, thumb_normal)
        arrow_down_active = icon('caret-down-fill', arrow_size, thumb_active)
        arrow_down_pressed = icon('caret-down-fill', arrow_size, thumb_pressed)
        b.create_style_element_image(
            ElementImage(
                f'{ttk_style}.downarrow', arrow_down_normal,
                padding=2, border=2, width=arrow_size, height=arrow_size).state_specs(
                [
                    ('pressed', arrow_down_pressed),
                    ('active', arrow_down_active),
                    ('', arrow_down_normal),
                ])
        )

    scrollbar_elements = [
        Element(f'{ttk_style}.uparrow', side="top", sticky=""),
        Element(f'{ttk_style}.downarrow', side="bottom", sticky=""),
        Element(f'{ttk_style}.thumb', sticky="ns"),
    ]

    b.create_style_layout(
        ttk_style,
        Element('Vertical.Scrollbar.trough', sticky="ns").children(
            scrollbar_elements if show_arrows else [scrollbar_elements[-1]]),
    )

    b.configure_style(
        ttk_style,
        troughcolor=surface,
        bordercolor=surface,
        relief='flat'
    )


def _build_rounded_horizontal_scrollbar(b: BootstyleBuilderTTk, ttk_style: str, color: str = None, **options):
    surface_token = options.get('surface_color', 'background')
    surface = b.color(surface_token)
    border_color = b.border(surface)

    if color is not None:
        thumb_normal = b.color(color)
    else:
        thumb_normal = border_color

    thumb_active = b.active(thumb_normal)
    thumb_pressed = b.pressed(thumb_normal)

    # thumb element
    thumb_normal_img = recolor_image('scrollbar-horizontal-rounded', thumb_normal, thumb_active, surface, surface)
    thumb_active_img = recolor_image('scrollbar-horizontal-rounded', thumb_active, thumb_active, surface, surface)
    thumb_pressed_img = recolor_image('scrollbar-horizontal-rounded', thumb_pressed, thumb_pressed, surface, surface)

    b.create_style_element_image(
        ElementImage(
            f'{ttk_style}.thumb', thumb_normal_img,
            padding=b.scale(3), border=b.scale(6), width=b.scale(30), height=b.scale(10)).state_specs(
            [
                ('pressed', thumb_pressed_img),
                ('active', thumb_active_img),
                ('', thumb_normal_img),
            ]),
    )

    show_arrows = options.get('show_arrows', True)
    if show_arrows:
        # arrow elements
        icon = use_icon_provider()
        arrow_size = b.scale(18)

        # arrow elements
        icon = use_icon_provider()
        arrow_size = b.scale(18)

        # arrow [left]
        arrow_left_normal = icon('caret-left-fill', arrow_size, thumb_normal)
        arrow_left_active = icon('caret-left-fill', arrow_size, thumb_active)
        arrow_left_pressed = icon('caret-left-fill', arrow_size, thumb_pressed)
        b.create_style_element_image(
            ElementImage(
                f'{ttk_style}.leftarrow', arrow_left_normal,
                padding=2, border=2, width=arrow_size, height=arrow_size).state_specs(
                [
                    ('pressed', arrow_left_pressed),
                    ('active', arrow_left_active),
                    ('', arrow_left_normal),
                ])
        )

        # arrow [right]
        arrow_right_normal = icon('caret-right-fill', arrow_size, thumb_normal)
        arrow_right_active = icon('caret-right-fill', arrow_size, thumb_active)
        arrow_right_pressed = icon('caret-right-fill', arrow_size, thumb_pressed)
        b.create_style_element_image(
            ElementImage(
                f'{ttk_style}.rightarrow', arrow_right_normal,
                padding=2, border=2, width=arrow_size, height=arrow_size).state_specs(
                [
                    ('pressed', arrow_right_pressed),
                    ('active', arrow_right_active),
                    ('', arrow_right_normal),
                ])
        )

    scrollbar_elements = [
        Element(f'{ttk_style}.leftarrow', side="left", sticky=""),
        Element(f'{ttk_style}.rightarrow', side="right", sticky=""),
        Element(f'{ttk_style}.thumb', sticky="ew"),
    ]

    b.create_style_layout(
        ttk_style,
        Element('Horizontal.Scrollbar.trough', sticky="we").children(
            scrollbar_elements if show_arrows else [scrollbar_elements[-1]])
    )

    b.configure_style(
        ttk_style,
        troughcolor=surface,
        bordercolor=surface,
        relief='flat'
    )
