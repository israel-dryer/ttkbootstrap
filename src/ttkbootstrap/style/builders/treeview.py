"""Treeview widget style builders.

This module contains style builders for ttk.Treeview widget and variants.

TODO there is a strange bug that causes the treeview to request more size when the custom border element is used.
"""
from tkinter import font

from ttkbootstrap_icons_bs import BootstrapIcon
from ttkbootstrap.style.bootstyle_builder_ttk import BootstyleBuilderTTk
from ttkbootstrap.style.element import Element, ElementImage
from ttkbootstrap.style.utility import create_transparent_image, recolor_image

TOKENS = ['primary', 'secondary', 'success', 'info', 'warning', 'danger', 'dark', 'light']


@BootstyleBuilderTTk.register_builder('default', 'Treeview')
@BootstyleBuilderTTk.register_builder('tree', 'Treeview')
def build_tree_style(b: BootstyleBuilderTTk, ttk_style: str, color: str = None, **options):
    """
    Create treeview style.

    Available options via `style_options`:
        * border_color
        * show_border
        * open_icon
        * close_icon
        * select_background
        * header_background
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

    if options.get('header_background'):
        heading_color = b.color(options.get('header_background'))
        heading_hover = b.active(heading_color)
    else:
        heading_color = b.elevate(surface, 3)
        heading_hover = b.active(heading_color)

    on_heading = b.on_color(heading_color)
    on_surface = b.on_color(surface)
    on_surface_disabled = b.disabled('text', surface)
    hover = b.active(surface)

    if options.get('select_background'):
        select_background = b.color(options.get('select_background'))
    else:
        if color in TOKENS:
            select_background = b.color(f"{color}[subtle]")
        else:
            select_background = b.color('primary[subtle]')

    select_hover = b.active(select_background)
    on_select = b.on_color(select_background)

    f = font.nametofont('TkDefaultFont')
    row_height = int(f.metrics()['linespace'] * 1.75)

    open_icon = options.get('open_icon', 'chevron-right')  # 'plus-square', plus-lg
    closed_icon = options.get('close_icon', 'chevron-down')  # 'dash-square', dash-lg
    icon_size = b.scale(16)
    expand_icon_normal = BootstrapIcon(open_icon, icon_size, on_surface).image
    expand_icon_selected = BootstrapIcon(open_icon, icon_size, on_select).image
    collapse_icon_normal = BootstrapIcon(closed_icon, icon_size, on_surface).image
    collapse_icon_selected = BootstrapIcon(closed_icon, icon_size, on_select).image
    leaf = create_transparent_image(icon_size, icon_size)

    b.create_style_element_image(
        ElementImage(
            f'{ttk_style}.indicator', expand_icon_normal,
            sticky='w', height=b.scale(14), width=b.scale(icon_size + 12)).state_specs(
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

    b.configure_style(f'{ttk_style}.Item', padding=b.scale((6, 0)))

    # customize the tree field
    border_img = recolor_image('border', surface, border_color, surface, surface)

    b.create_style_element_image(
        ElementImage(f'{ttk_style}.field', border_img, border=b.scale(6), padding=b.scale(6), width=0, height=0, sticky='nsew')
    )

    b.create_style_layout(
        ttk_style, Element(f'{ttk_style}.field', sticky="nsew").children(
            [
                Element('Treeview.padding', sticky="nsew").children(
                    [
                        Element('Treeview.treearea', sticky="nsew")
                    ]),
            ]))

    # configure header
    b.configure_style(
        f'{ttk_style}.Heading',
        font="label",
        background=heading_color,
        foreground=on_heading,
        padding=b.scale((8, 10))
    )
    b.map_style(
        f'{ttk_style}.Heading',
        foreground=[('disabled', on_surface_disabled), ('', on_heading)],
        background=[('active !disabled', heading_hover), ('', heading_color)]
    )
    # configure tree body
    b.configure_style(
        ttk_style,
        font="body",
        background=surface,
        fieldbackground=surface,
        foreground=on_surface,
        borderwidth=0,
        padding=0,
        rowheight=row_height,
        relief='flat'
    )

    b.map_style(
        ttk_style,
        font="body",
        background=[
            ('active !disabled', hover),
            ('selected active !disabled', select_hover),
            ('selected !disabled', select_background)
            # do not set fallback or it will override tag formats
        ],
        foreground=[
            ('disabled', on_surface_disabled),
            ('selected !disabled', on_select)
            # do not set fallback or it will override tag formats
        ]
    )

    # configure cell
    b.configure_style(f"{ttk_style}.Cell", font="body", padding=b.scale((6, 0)))
