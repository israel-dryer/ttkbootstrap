"""Treeview widget style builders.

This module contains style builders for ttk.Treeview widget and variants.

TODO there is a strange bug that causes the treeview to request more size when the custom border element is used.
"""
from tkinter import font

from ttkbootstrap.appconfig import use_icon_provider
from ttkbootstrap.style.bootstyle_builder_ttk import BootstyleBuilderTTk
from ttkbootstrap.style.element import Element, ElementImage
from ttkbootstrap.style.utility import create_transparent_image, recolor_image

TOKENS = ['primary', 'secondary', 'success', 'info', 'warning', 'danger', 'dark', 'light']


@BootstyleBuilderTTk.register_builder('default', 'Treeview')
@BootstyleBuilderTTk.register_builder('tree', 'Treeview')
def build_tree_style(b: BootstyleBuilderTTk, ttk_style: str, color: str = None, **options):
    """
    Create tree style.

    style_options:
        border_color
        show_border
        open_icon
        close_icon
        select_background
    """
    surface_token = options.get('surface_color', 'background')

    surface = b.color(surface_token)
    if options.get('show_border', True):
        if options.get('border_color'):
            border_color = b.color(options.get('border_color'))
        else:
            border_color = b.border(surface)
    else:
        border_color = surface

    on_surface = b.on_color(surface)
    on_surface_disabled = b.disabled('text', surface)
    hover = b.hover(surface)

    if options.get('select_background'):
        select_background = b.color(options.get('select_background'))
    else:
        if color in TOKENS:
            select_background = b.color(f"{color}[subtle]")
        else:
            select_background = b.color('primary')

    select_hover = b.hover(select_background)
    on_select = b.on_color(select_background)

    f = font.nametofont('TkDefaultFont')
    row_height = int(f.metrics()['linespace'] * 1.75)

    # customize indicator
    icon = use_icon_provider()

    open_icon = options.get('open_icon', 'plus-lg')  # 'plus-square'
    closed_icon = options.get('close_icon', 'dash-lg')  # 'dash-square'

    expand_icon_normal = icon(open_icon, 14, on_surface)
    expand_icon_selected = icon(open_icon, 14, on_select)
    collapse_icon_normal = icon(closed_icon, 14, on_surface)
    collapse_icon_selected = icon(closed_icon, 14, on_select)
    leaf = create_transparent_image(14, 14)

    b.create_style_element_image(
        ElementImage(f'{ttk_style}.indicator', expand_icon_normal, sticky='w', height=14, width=18).state_specs(
            [
                ('user2', leaf),
                ('user1 selected', collapse_icon_selected),
                ('user1', collapse_icon_normal),
                ('!user1 selected', expand_icon_selected),
            ])
    )

    b.create_style_layout(
        f'{ttk_style}.Item',
        Element('Treeitem.padding').children(
            [
                Element(f'{ttk_style}.indicator', side='left', sticky=''),
                Element('Treeitem.image', side='left', sticky=''),
                Element('Treeitem.text', side='left', sticky='w')
            ])
    )

    b.configure_style(f'{ttk_style}.Item', padding=(8, 0))

    # customize the tree field
    border_img = recolor_image('border', surface, border_color, surface, surface)

    b.create_style_element_image(
        ElementImage(f'{ttk_style}.border', border_img, border=8, padding=8, width=86, height=86, sticky="nsew")
    )

    b.create_style_layout(
        ttk_style, Element(f'{ttk_style}.border').children(
            [
                Element('Treeview.padding', sticky="nsew").children(
                    [
                        Element('Treeview.treearea', sticky="nsew")
                    ]),
            ]))

    # configure header
    b.configure_style(
        f'{ttk_style}.Heading',
        background=surface,
        foreground=on_surface,
        relief='flat',
        padding=5)

    b.map_style(
        f'{ttk_style}.Heading',
        foreground=[('disabled', on_surface_disabled), ('', on_surface)],
        background=[('active !disabled', hover), ('', surface)])

    # configure tree body
    b.configure_style(
        ttk_style,
        background=surface,
        fieldbackground=surface,
        foreground=on_surface,
        bordercolor=border_color,
        lightcolor=surface,
        darkcolor=surface,
        borderwidth=2,
        padding=0,
        rowheight=row_height,
        relief='raised'
    )

    b.map_style(
        ttk_style,
        background=[
            ('active !disabled', hover),
            ('selected active !disabled', select_hover),
            ('selected !disabled', select_background),
            ('', surface)
        ],
        foreground=[
            ('disabled', on_surface_disabled),
            ('selected !disabled', on_select),
            ('', on_surface)
        ]
    )


@BootstyleBuilderTTk.register_builder('table', 'Treeview')
def build_tree_style(b: BootstyleBuilderTTk, ttk_style: str, color: str = None, **options):
    """
    Create table style.

    style_options:
        border_color
        show_border
        open_icon
        close_icon
        select_background
    """
    surface_token = options.get('surface_color', 'background')

    surface = b.color(surface_token)
    if options.get('show_border', True):
        if options.get('border_color'):
            border_color = b.color(options.get('border_color'))
        else:
            border_color = b.border(surface)
    else:
        border_color = surface

    on_surface = b.on_color(surface)
    on_surface_disabled = b.disabled('text', surface)
    hover = b.hover(surface)

    if options.get('select_background'):
        select_background = b.color(options.get('select_background'))
    else:
        if color in TOKENS:
            select_background = b.color(f"{color}[subtle]")
        else:
            select_background = b.color('primary')

    select_hover = b.hover(select_background)
    on_select = b.on_color(select_background)

    f = font.nametofont('TkDefaultFont')
    row_height = int(f.metrics()['linespace'] * 1.75)

    # customize indicator
    icon = use_icon_provider()

    open_icon = options.get('open_icon', 'plus-lg')  # 'plus-square'
    closed_icon = options.get('close_icon', 'dash-lg')  # 'dash-square'

    expand_icon_normal = icon(open_icon, 14, on_surface)
    expand_icon_selected = icon(open_icon, 14, on_select)
    collapse_icon_normal = icon(closed_icon, 14, on_surface)
    collapse_icon_selected = icon(closed_icon, 14, on_select)
    leaf = create_transparent_image(14, 14)

    b.create_style_element_image(
        ElementImage(f'{ttk_style}.indicator', expand_icon_normal, sticky='w', height=14, width=18).state_specs(
            [
                ('user2', leaf),
                ('user1 selected', collapse_icon_selected),
                ('user1', collapse_icon_normal),
                ('!user1 selected', expand_icon_selected),
            ])
    )

    b.create_style_layout(
        f'{ttk_style}.Item',
        Element('Treeitem.padding').children(
            [
                Element(f'{ttk_style}.indicator', side='left', sticky=''),
                Element('Treeitem.image', side='left', sticky=''),
                Element('Treeitem.text', side='left', sticky='w')
            ])
    )

    b.configure_style(f'{ttk_style}.Item', padding=(8, 0))

    # customize the tree field
    border_img = recolor_image('border', surface, border_color, surface, surface)

    b.create_style_element_image(
        ElementImage(f'{ttk_style}.border', border_img, border=8, padding=8, width=86, height=86, sticky="nsew")
    )

    b.create_style_layout(
        ttk_style, Element(f'{ttk_style}.border').children(
            [
                Element('Treeview.padding', sticky="nsew").children(
                    [
                        Element('Treeview.treearea', sticky="nsew")
                    ]),
            ]))

    # configure header
    b.configure_style(
        f'{ttk_style}.Heading',
        background=surface,
        foreground=on_surface,
        relief='flat',
        padding=5)

    b.map_style(
        f'{ttk_style}.Heading',
        foreground=[('disabled', on_surface_disabled), ('', on_surface)],
        background=[('active !disabled', hover), ('', surface)])

    # configure tree body
    b.configure_style(
        ttk_style,
        background=surface,
        fieldbackground=surface,
        foreground=on_surface,
        bordercolor=border_color,
        lightcolor=surface,
        darkcolor=surface,
        borderwidth=2,
        padding=0,
        rowheight=row_height,
        relief='raised'
    )

    b.map_style(
        ttk_style,
        background=[
            ('active !disabled', hover),
            ('selected active !disabled', select_hover),
            ('selected !disabled', select_background),
            ('', surface)
        ],
        foreground=[
            ('disabled', on_surface_disabled),
            ('selected !disabled', on_select),
            ('', on_surface)
        ]
    )
