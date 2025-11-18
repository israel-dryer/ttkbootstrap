"""Scrollbar style builders.

This module contains style builders for ttk.Scrollbar widget variants.
"""
from ttkbootstrap.style.bootstyle_builder_ttk import BootstyleBuilderTTk
from ttkbootstrap.style.element import Element


@BootstyleBuilderTTk.register_builder('default', 'TScrollbar')
def build_scrollbar_style(b: BootstyleBuilderTTk, ttk_style: str, color: str = None, **options):
    if options.get('orient', 'vertical') == 'vertical':
        build_vertical_scrollbar(b, ttk_style, color, **options)
    else:
        build_horizontal_scrollbar(b, ttk_style, color, **options)


def build_horizontal_scrollbar(b: BootstyleBuilderTTk, ttk_style: str, color: str = None, **options):
    surface_token = options.get('surface_color', 'background')

    background_color = b.color(surface_token)
    trough_color = b.elevate(background_color, 1)
    thumb_color = b.border(background_color)
    thumb_hover = b.active(thumb_color)
    thumb_pressed = b.pressed(thumb_color)

    b.create_style_layout(
        ttk_style, Element(f'{ttk_style}.Scrollbar.trough', sticky="ew").children(
            [
                Element(f'{ttk_style}.Scrollbar.thumb', side="left", expand=True, sticky="ew")
            ]))

    b.configure_style(
        ttk_style,
        background=thumb_color,
        troughcolor=background_color,
        padding=0,
        bordercolor=background_color,
        darkcolor=thumb_color,
        lightcolor=thumb_color,
        gripcount=0,
        relief='flat',
        arrowsize=12,
    )
    b.map_style(
        ttk_style,
        background=[('pressed', thumb_pressed), ('hover', thumb_hover)],
        bordercolor=[('active', trough_color), ('hover', trough_color)],
        darkcolor=[('pressed', thumb_pressed), ('hover', thumb_hover)],
        lightcolor=[('pressed', thumb_pressed), ('hover', thumb_hover)],
        troughcolor=[('active', trough_color), ('hover', trough_color)]
    )


def build_vertical_scrollbar(b: BootstyleBuilderTTk, ttk_style: str, color: str = None, **options):
    surface_token = options.get('surface_color', 'background')

    background_color = b.color(surface_token)
    trough_color = b.elevate(background_color, 1)
    thumb_color = b.border(background_color)
    thumb_hover = b.active(thumb_color)
    thumb_pressed = b.pressed(thumb_color)

    b.create_style_layout(
        ttk_style, Element(f'{ttk_style}.Scrollbar.trough', sticky="ns").children(
            [
                Element(f'{ttk_style}.Scrollbar.thumb', side="top", expand=True, sticky="ns")
            ]))

    b.configure_style(
        ttk_style,
        background=thumb_color,
        troughcolor=background_color,
        padding=0,
        bordercolor=background_color,
        darkcolor=thumb_color,
        lightcolor=thumb_color,
        gripcount=0,
        relief='flat',
        arrowsize=12,
    )
    b.map_style(
        ttk_style,
        background=[('pressed', thumb_pressed), ('hover', thumb_hover)],
        bordercolor=[('active', trough_color), ('hover', trough_color)],
        darkcolor=[('pressed', thumb_pressed), ('hover', thumb_hover)],
        lightcolor=[('pressed', thumb_pressed), ('hover', thumb_hover)],
        troughcolor=[('active', trough_color), ('hover', trough_color)]
    )
