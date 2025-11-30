"""Notebook widget style builders.

This module contains style builders for ttk.Notebook widget and variants.

# TODO add styles in the future that are geared towards left direction navigation
"""

from __future__ import annotations

from ttkbootstrap.style.bootstyle_builder_ttk import BootstyleBuilderTTk
from ttkbootstrap.style.element import Element, ElementImage
from ttkbootstrap.style.utility import recolor_image


def _client_border_image(surface: str, accent: str, show_border: bool) -> object:
    border_accent = accent if show_border else surface
    return recolor_image(
        "notebook-client-border",
        surface,
        border_accent,
        surface,
        surface,
    )


def _border_image(surface: str, accent: str, border: str, show_border: bool) -> object:
    border_accent = border if show_border else surface
    return recolor_image(
        "border",
        accent,
        border_accent,
        surface,
        surface,
    )


def _notebook_layout(ttk_style: str) -> Element:
    return Element(f"{ttk_style}.Notebook.border").children(
        [
            Element(f"{ttk_style}.Tab", side="top", expand=True),
            Element(f"{ttk_style}.Notebook.client", sticky="nsew"),
        ]
    )


@BootstyleBuilderTTk.register_builder('default', 'TNotebook')
@BootstyleBuilderTTk.register_builder('tab', 'TNotebook')
def build_tabs_notebook(b: BootstyleBuilderTTk, ttk_style: str, color: str = None, **options):
    surface_token = options.get('surface_color') or "background"
    surface = b.color(surface_token)
    border_color = b.border(surface)
    show_border = options.get('show_border', True)

    # notebook colors
    tab_active_color = surface
    tab_accent_color = b.color(color or 'background[+1]')
    tab_accent_hover = b.active(tab_accent_color)

    tab_active_foreground = b.on_color(surface)
    tab_accent_foreground = b.on_color(tab_accent_color)
    tab_disabled_foreground = b.disabled('text')
    tab_active_border = b.border(surface)

    # notebook border assets, style and layout
    client_border_img = _client_border_image(surface, tab_accent_color, show_border)

    b.create_style_element_image(
        ElementImage(
            f'{ttk_style}.Notebook.client', client_border_img,
            border=b.scale(6)
        )
    )

    tab_border_img = _border_image(surface, tab_accent_color, border_color, show_border)

    b.create_style_element_image(
        ElementImage(f"{ttk_style}.Notebook.border", tab_border_img, border=b.scale(6))
    )

    b.create_style_layout(
        ttk_style,
        _notebook_layout(ttk_style),
    )

    tab_active_img = recolor_image(
        'notebook-tab-border', tab_active_color, tab_active_border)
    tab_normal_img = recolor_image(
        'notebook-tab-normal', tab_accent_color, tab_accent_color, tab_active_border, tab_accent_color)
    tab_hover_img = recolor_image(
        'notebook-tab-normal', tab_accent_hover, tab_accent_hover, tab_active_border, tab_accent_color)

    b.create_style_element_image(
        ElementImage(
            f'{ttk_style}.Notebook.tab', tab_normal_img,
            sticky='nsew', padding=b.scale(8), border=b.scale(8), height=b.scale(24)).state_specs(
            [
                ('selected', tab_active_img),
                ('active', tab_hover_img),
                ('', tab_normal_img),
            ])
    )

    b.create_style_layout(
        f"{ttk_style}.Tab",
        Element(f"{ttk_style}.Notebook.tab").children(
            [
                Element("Notebook.padding", side="top").children(
                    [
                        Element("Notebook.label")
                    ]
                )
            ]
        )
    )

    b.configure_style(
        f"{ttk_style}.Tab",
        font="label",
        foreground=tab_accent_foreground,
        padding=b.scale((14, 0)))

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
    b.configure_style(ttk_style, padding=b.scale((3, 6, 3, 3)), tabmargins=(*b.scale([6, 4, 0]), -1))


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
    pill_normal_hover = b.subtle(color or 'primary', surface)

    # notebook border assets & style
    notebook_border = b.border(surface)
    show_border = options.get('show_border', True)

    notebook_border_img = _border_image(surface, surface, notebook_border, show_border)
    b.create_style_element_image(
        ElementImage(f'{ttk_style}.Notebook.border', notebook_border_img, border=b.scale(6))
    )

    # notebook border assets, style and layout
    client_border_img = _client_border_image(surface, surface, False)
    b.create_style_element_image(
        ElementImage(
            f'{ttk_style}.Notebook.client', client_border_img,
            border=b.scale(6)
        )
    )

    b.create_style_layout(
        ttk_style,
        _notebook_layout(ttk_style),
    )

    # notebook tab assets & style
    pill_active_img = recolor_image(
        'notebook-pill-active', pill_active_color, pill_active_border_color, surface, surface)
    pill_normal_img = recolor_image('notebook-pill-inactive', pill_normal_color, pill_normal_color, surface, surface)
    pill_normal_hover_img = recolor_image(
        'notebook-pill-inactive', pill_normal_hover, pill_normal_hover, surface, surface)

    b.create_style_element_image(
        ElementImage(
            f'{ttk_style}.Notebook.tab', pill_normal_img,
            sticky='nsew', padding=b.scale(8), border=b.scale(8), height=b.scale(24)).state_specs(
            [
                ('selected', pill_active_img),
                ('active !selected', pill_normal_hover_img),
                ('', pill_normal_img),
            ])
    )

    b.create_style_layout(
        f'{ttk_style}.Tab',
        Element(f'{ttk_style}.Notebook.tab', sticky="nsew").children(
            [
                Element('Notebook.padding', side='top').children(
                    [
                        Element('Notebook.label')
                    ])
            ])
    )

    b.configure_style(
        f"{ttk_style}.Tab",
        foreground=pill_normal_foreground,
        font="label",
        padding=b.scale((14, 0)))

    b.map_style(
        f"{ttk_style}.Tab",
        foreground=[
            ('disabled', pill_disabled_foreground),
            ('selected !disabled', pill_active_foreground),
            ('active !selected !disabled', pill_normal_foreground),
            ('', pill_normal_foreground),
        ]
    )

    b.configure_style(ttk_style, padding=b.scale(3), tabmargins=b.scale((6, 6, 0, 0)))


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
    hover = b.subtle(color or 'primary', surface)

    client_border_img = _client_border_image(surface, border_color, show_border)

    b.create_style_element_image(
        ElementImage(
            f"{ttk_style}.Notebook.client",
            client_border_img,
            border=b.scale(6),
        )
    )

    tab_border_img = _border_image(surface, surface, border_color, show_border)

    b.create_style_element_image(
        ElementImage(
            f"{ttk_style}.Notebook.border",
            tab_border_img,
            border=b.scale(6)
        )
    )

    b.create_style_layout(
        ttk_style,
        _notebook_layout(ttk_style),
    )

    active_img = recolor_image("notebook-underline", surface, surface, accent_color, surface)
    active_hover_img = recolor_image("notebook-underline", hover, surface, accent_color, surface)
    normal_img = recolor_image("notebook-underline", surface, surface, surface, surface)
    hover_img = recolor_image("notebook-underline", hover, surface, hover, surface)

    b.create_style_element_image(
        ElementImage(
            f"{ttk_style}.Notebook.tab", normal_img, sticky="nsew",
            padding=b.scale(8), border=b.scale(8), height=b.scale(24)
        ).state_specs(
            [
                ("selected !disabled", active_img),
                ("active selected !disabled", active_hover_img),
                ("active !selected !disabled", hover_img),
                ("", normal_img),
            ]
        )
    )

    b.create_style_layout(
        f"{ttk_style}.Tab",
        Element(f"{ttk_style}.Notebook.tab").children(
            [
                Element("Notebook.padding", side="top").children(
                    [
                        Element("Notebook.label")
                    ]
                )
            ]
        )
    )

    b.configure_style(
        f"{ttk_style}.Tab",
        foreground=foreground,
        font="label",
        focuscolor="",
        padding=b.scale((14, 0)),
    )

    b.map_style(
        f"{ttk_style}.Tab",
        foreground=[
            ("disabled", disabled),
            ("", foreground),
        ],
    )

    # General notebook style (similar to Forest's: -padding 2 + margins)
    b.configure_style(
        ttk_style,
        background=surface,
        padding=b.scale(3),
        tabmargins=b.scale((4, 6, 0, 0)),
    )
