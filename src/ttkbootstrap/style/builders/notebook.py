"""Notebook widget style builders.

This module contains style builders for ttk.Notebook widget and variants.

# TODO add styles in the future that are geared towards left direction navigation
"""

from __future__ import annotations

from ttkbootstrap.style.bootstyle_builder_ttk import BootstyleBuilderTTk
from ttkbootstrap.style.element import Element, ElementImage
from ttkbootstrap.style.utility import recolor_image


@BootstyleBuilderTTk.register_builder('default', 'TNotebook')
@BootstyleBuilderTTk.register_builder('tab', 'TNotebook')
def build_tabs_notebook(b: BootstyleBuilderTTk, ttk_style: str, color: str = None, **options):
    surface_token = options.get('surface_color') or "background"
    surface = b.color(surface_token)
    show_border = options.get('show_border', True)

    # notebook colors
    tab_active_color = surface
    tab_accent_color = b.color(color or 'background[+1]')
    tab_accent_hover = b.hover(tab_accent_color)

    tab_active_foreground = b.on_color(surface)
    tab_accent_foreground = b.on_color(tab_accent_color)
    tab_disabled_foreground = b.disabled('text')

    tab_active_border = b.border(surface)

    # notebook border assets, style and layout
    if show_border:
        # draw the border no matter what, just make it surface color.
        notebook_border = recolor_image('border', tab_accent_color, tab_active_border, tab_accent_color, surface)
    else:
        notebook_border = recolor_image('border', surface, surface, surface, surface)

    b.create_style_element_image(
        ElementImage(f'{ttk_style}.border', notebook_border, border=2, padding=2, sticky="nsew")
    )

    b.create_style_layout(
        ttk_style,
        Element(f'{ttk_style}.border', sticky="nsew", border=8).children(
            [
                Element('Notebook.client', sticky='nsew')
            ])
    )

    # notebook tab image assets, style and layout
    tab_active_img = recolor_image(
        'notebook-tab-active', tab_active_color, tab_active_border)
    tab_normal_img = recolor_image(
        'notebook-tab-normal', tab_accent_color, tab_active_border, tab_accent_color, tab_accent_color)
    tab_hover_img = recolor_image(
        'notebook-tab-normal', tab_accent_hover, tab_active_border, tab_accent_color, tab_accent_color)

    b.create_style_element_image(
        ElementImage(f'{ttk_style}.tab', tab_normal_img, sticky='nsew', padding=8, border=8, height=28).state_specs(
            [
                ('selected', tab_active_img),
                ('active', tab_hover_img),
                ('', tab_normal_img),
            ])
    )

    b.create_style_layout(
        f'{ttk_style}.Tab',
        Element(f'{ttk_style}.tab', sticky="nsew").children(
            [
                Element('Notebook.padding', side='top', sticky='nsew').children(
                    [
                        Element('Notebook.focus', side='top', sticky='nsew').children(
                            [
                                Element('Notebook.label', side='top', sticky='')
                            ])
                    ])
            ])
    )

    b.configure_style(f"{ttk_style}.Tab", foreground=tab_accent_foreground, focuscolor='', padding=(8, 0))

    b.map_style(
        f"{ttk_style}.Tab",
        foreground=[
            ('disabled', tab_disabled_foreground),
            ('selected !disabled', tab_active_foreground),
            ('active !selected !disabled', tab_accent_foreground),
            ('', tab_accent_foreground),
        ]
    )

    # general notebook style
    b.configure_style(ttk_style, padding=0, tabmargins=(2, 6, 0, -2))


@BootstyleBuilderTTk.register_builder('pill', 'TNotebook')
def build_pill_notebook(b: BootstyleBuilderTTk, ttk_style: str, color: str = None, **options):
    surface_token = options.get('surface_color') or "background"
    surface = b.color(surface_token)

    # notebook pill colors
    pill_active_color = b.color(color or 'primary')
    pill_active_border_color = b.border(pill_active_color)
    pill_active_foreground = b.on_color(pill_active_color)
    pill_normal_color = surface
    pill_normal_foreground = b.on_color(pill_normal_color)
    pill_disabled_foreground = b.disabled('text', surface)
    pill_normal_hover = b.hover(surface)

    # notebook border assets & style
    notebook_border = b.border(surface)
    show_border = options.get('show_border', True)

    if show_border:
        notebook_border_img = recolor_image('border', surface, notebook_border, surface, surface)
    else:
        notebook_border_img = recolor_image('border', surface, surface, surface, surface)

    b.create_style_element_image(
        ElementImage(f'{ttk_style}.border', notebook_border_img, border=2, padding=2, sticky="nsew")
    )

    b.create_style_layout(
        ttk_style,
        Element(f'{ttk_style}.border', sticky="nsew", border=8).children(
            [
                Element('Notebook.client', sticky='nsew')
            ])
    )

    # notebook tab assets & style
    pill_active_img = recolor_image(
        'notebook-pill-active', pill_active_color, pill_active_border_color, surface, surface)
    pill_normal_img = recolor_image('notebook-pill-inactive', pill_normal_color, pill_normal_color, surface, surface)
    pill_normal_hover_img = recolor_image(
        'notebook-pill-inactive', pill_normal_hover, pill_normal_hover, surface, surface)

    b.create_style_element_image(
        ElementImage(f'{ttk_style}.tab', pill_normal_img, sticky='nsew', padding=8, border=8, height=28).state_specs(
            [
                ('selected', pill_active_img),
                ('active !selected', pill_normal_hover_img),
                ('', pill_normal_img),
            ])
    )

    b.create_style_layout(
        f'{ttk_style}.Tab',
        Element(f'{ttk_style}.tab', sticky="nsew").children(
            [
                Element('Notebook.padding', side='top', sticky='nsew').children(
                    [
                        Element('Notebook.focus', side='top', sticky='nsew').children(
                            [
                                Element('Notebook.label', side='top', sticky='')
                            ])
                    ])
            ])
    )

    b.configure_style(ttk_style, padding=0, tabmargins=(6, 6, 4, 0))

    b.configure_style(f"{ttk_style}.Tab", foreground=pill_normal_foreground, focuscolor='', padding=(8, 0))

    b.map_style(
        f"{ttk_style}.Tab",
        foreground=[
            ('disabled', pill_disabled_foreground),
            ('selected !disabled', pill_active_foreground),
            ('active !selected !disabled', pill_normal_foreground),
            ('', pill_normal_foreground),
        ]
    )


@BootstyleBuilderTTk.register_builder('underline', 'TNotebook')
def build_underline_notebook(b: BootstyleBuilderTTk, ttk_style: str, color: str = None, **options):
    surface_token = options.get('surface_color') or "background"
    surface = b.color(surface_token)
    border_color = b.border(surface)
    show_border = options.get('show_border', True)

    # notebook colors
    accent_color = b.color(color or 'primary')
    foreground = b.on_color(surface)
    disabled = b.disabled('text', surface)
    hover = b.hover(surface)

    # notebook border assets, style and layout
    if show_border:
        # draw the border no matter what, just make it surface color.
        notebook_border = recolor_image('border', surface, border_color, surface, surface)
    else:
        notebook_border = recolor_image('border', surface, surface, surface, surface)

    b.create_style_element_image(
        ElementImage(f'{ttk_style}.border', notebook_border, border=2, padding=2, sticky="nsew")
    )

    b.create_style_layout(
        ttk_style,
        Element(f'{ttk_style}.border', sticky="nsew", border=8).children(
            [
                Element('Notebook.client', sticky='nsew')
            ])
    )

    # notebook tab image assets, style and layout
    active_img = recolor_image('notebook-underline', surface, border_color, accent_color, surface)
    active_hover_img = recolor_image('notebook-underline', hover, border_color, accent_color, surface)
    normal_img = recolor_image('notebook-underline', surface, border_color, surface, surface)
    hover_img = recolor_image('notebook-underline', hover, border_color, hover, surface)

    b.create_style_element_image(
        ElementImage(f'{ttk_style}.tab', normal_img, sticky='nsew', padding=8, border=8, height=28).state_specs(
            [
                ('selected !disabled', active_img),
                ('active selected !disabled', active_hover_img),
                ('active !selected !disabled', hover_img),
                ('', normal_img),
            ])
    )

    b.create_style_layout(
        f'{ttk_style}.Tab',
        Element(f'{ttk_style}.tab', sticky="nsew").children(
            [
                Element('Notebook.padding', side='top', sticky='nsew').children(
                    [
                        Element('Notebook.focus', side='top', sticky='nsew').children(
                            [
                                Element('Notebook.label', side='top', sticky='')
                            ])
                    ])
            ])
    )

    b.configure_style(f"{ttk_style}.Tab", foreground=foreground, focuscolor='', padding=(8, 0))

    b.map_style(
        f"{ttk_style}.Tab",
        foreground=[
            ('disabled', disabled),
            ('', foreground),
        ]
    )

    # general notebook style
    b.configure_style(ttk_style, padding=0, tabmargins=(2, 6, 0, -2))
