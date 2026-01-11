"""Treeview widget style builders.

This module contains style builders for ttk.Treeview widget and variants.

TODO there is a strange bug that causes the treeview to request more size when the custom border element is used.
"""
import tkinter as tk
from tkinter import font

from ttkbootstrap_icons_bs import BootstrapIcon
from ttkbootstrap.style.bootstyle_builder_ttk import BootstyleBuilderTTk
from ttkbootstrap.style.element import Element, ElementImage
from ttkbootstrap.style.utility import create_transparent_image, recolor_element_image
from ttkbootstrap.style.builders.utils import normalize_button_density


def _tk_version_at_least(major: int, minor: int, patch: int) -> bool:
    """Check if the current Tk version is at least the specified version.

    This is used to work around a regression in Tk 8.6.13+ where user1/user2
    states don't work properly with custom image elements for treeview indicators.
    See: https://core.tcl-lang.org/tk/timeline?r=rfe-d632d28ba4
    """
    try:
        version_str = tk._default_root.tk.call('info', 'patchlevel')
        parts = version_str.split('.')
        current = (int(parts[0]), int(parts[1]), int(parts[2]))
        return current >= (major, minor, patch)
    except Exception:
        # If we can't determine version, assume newer Tk (safer fallback)
        return True


def _treeview_font(density: str) -> str:
    """Get font token based on density."""
    return 'caption' if density == 'compact' else 'body'


def _treeview_row_height(density: str) -> float:
    """Get row height multiplier based on density."""
    return 1.6 if density == 'compact' else 1.75


def _treeview_indicator_size(density: str) -> int:
    """Get indicator size based on density."""
    return 10 if density == 'compact' else 12


def _treeview_icon_size(density: str) -> int:
    """Get custom icon size based on density."""
    return 12 if density == 'compact' else 16


def _treeview_item_padding(density: str) -> tuple[int, int]:
    """Get item padding based on density."""
    return (4, 0) if density == 'compact' else (6, 0)


def _treeview_heading_padding(density: str) -> tuple[int, int]:
    """Get heading padding based on density."""
    return (4, 4) if density == 'compact' else (8, 10)


def _treeview_cell_padding(density: str) -> tuple[int, int]:
    """Get cell padding based on density."""
    return (2, 0) if density == 'compact' else (6, 0)


@BootstyleBuilderTTk.register_builder('default', 'Treeview')
@BootstyleBuilderTTk.register_builder('tree', 'Treeview')
def build_tree_style(b: BootstyleBuilderTTk, ttk_style: str, **options):
    """
    Create treeview style.

    Available options via `style_options`:
        * border_color
        * show_border
        * open_icon
        * close_icon
        * select_background
        * header_background
        * density ('default' or 'compact')
    """
    surface_token = options.get('surface', 'content')
    density = normalize_button_density(options.get('density', 'default'))
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

    select_background_token = options.get('select_background', 'primary')
    select_background = b.color(select_background_token)
    select_hover = b.active(select_background)
    on_select = b.on_color(select_background)

    # Density-based sizing
    body_font = _treeview_font(density)
    row_multiplier = _treeview_row_height(density)
    indicator_size = _treeview_indicator_size(density)
    item_padding = _treeview_item_padding(density)
    heading_padding = _treeview_heading_padding(density)
    cell_padding = _treeview_cell_padding(density)

    # Calculate row height - use TkDefaultFont for metrics when using font spec
    metrics_font = 'TkDefaultFont' if body_font.startswith('-') else body_font
    f = font.nametofont(metrics_font)
    row_height = int(f.metrics()['linespace'] * row_multiplier)

    # Tk 8.6.13+ has a regression where user1/user2 states don't work with
    # custom image elements for treeview indicators. Use native indicator on
    # newer Tk versions until TIP #719 lands with proper open/leaf states.
    # See: https://core.tcl-lang.org/tk/timeline?r=rfe-d632d28ba4
    use_native_indicator = _tk_version_at_least(8, 6, 13)

    if use_native_indicator:
        # Use native Treeitem.indicator with custom foreground colors
        # The native indicator uses triangles that rotate based on open/closed state
        # Create a spacer element to add space between indicator and text
        spacer_width = 8 if density == 'compact' else 8
        spacer = create_transparent_image(b.scale(spacer_width), 1)
        b.create_style_element_image(
            ElementImage(f'{ttk_style}.spacer', spacer, sticky='', width=b.scale(spacer_width))
        )

        b.create_style_layout(
            f'{ttk_style}.Item',
            Element('Treeitem.padding').children(
                [
                    Element('Treeitem.indicator', side='left', sticky=''),
                    Element(f'{ttk_style}.spacer', side='left', sticky=''),
                    Element('Treeitem.image', side='left', sticky=''),
                    Element('Treeitem.text', side='left', sticky='w')
                ])
        )

        indicator_margins = (0, 0, 0, 2) if density == 'compact' else (0, 0, 0, 2)
        b.configure_style(
            f'{ttk_style}.Item',
            padding=b.scale(item_padding),
            foreground=on_surface,
            indicatorsize=b.scale(indicator_size),
            indicatormargins=b.scale(indicator_margins)
        )
        b.map_style(
            f'{ttk_style}.Item',
            foreground=[
                ('selected', on_select),
                ('', on_surface)
            ]
        )
    else:
        # Use custom image indicator with user1/user2 states (works on Tk < 8.6.13)
        open_icon = options.get('open_icon', 'chevron-right')
        closed_icon = options.get('close_icon', 'chevron-down')
        icon_size = b.scale(_treeview_icon_size(density))

        expand_icon_normal = BootstrapIcon(open_icon, icon_size, on_surface).image
        expand_icon_selected = BootstrapIcon(open_icon, icon_size, on_select).image
        collapse_icon_normal = BootstrapIcon(closed_icon, icon_size, on_surface).image
        collapse_icon_selected = BootstrapIcon(closed_icon, icon_size, on_select).image
        leaf = create_transparent_image(icon_size, icon_size)

        indicator_height = 12 if density == 'compact' else 14
        b.create_style_element_image(
            ElementImage(
                f'{ttk_style}.indicator', expand_icon_normal,
                sticky='w', height=b.scale(indicator_height), width=b.scale(icon_size + 10)).state_specs(
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

        b.configure_style(f'{ttk_style}.Item', padding=b.scale(item_padding))

    # customize the tree field
    border_img = recolor_element_image('border', surface, border_color, surface, surface)

    b.create_style_element_image(
        ElementImage(
            f'{ttk_style}.field', border_img.image, sticky='nsew',
            border=border_img.meta.border, padding=border_img.meta.border,
            width=0, height=0
        )
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
    heading_font = 'caption' if density == 'compact' else 'label'
    b.configure_style(
        f'{ttk_style}.Heading',
        font=heading_font,
        background=heading_color,
        foreground=on_heading,
        padding=b.scale(heading_padding)
    )
    b.map_style(
        f'{ttk_style}.Heading',
        foreground=[('disabled', on_surface_disabled), ('', on_heading)],
        background=[('active !disabled', heading_hover), ('', heading_color)]
    )

    # configure tree body
    b.configure_style(
        ttk_style,
        font=body_font,
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
    b.configure_style(f"{ttk_style}.Cell", font=body_font, padding=b.scale(cell_padding))
