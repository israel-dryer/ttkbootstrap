"""Type definitions and configuration normalizers for TableView widget."""

from __future__ import annotations

from typing import Any
from typing_extensions import Literal, TypedDict


class EditingOptions(TypedDict, total=False):
    """Configure add/update/delete support and form dialog options."""
    adding: bool
    updating: bool
    deleting: bool
    form: dict[str, Any]


class SelectionOptions(TypedDict, total=False):
    """Control selection mode (single/multiple/none) and select-all allowance."""
    mode: Literal['single', 'multiple', 'none']
    allow_select_all: bool  # not yet supported


class ExportingOptions(TypedDict, total=False):
    """Configure export availability and formats."""
    enabled: bool
    allow_export_selected: bool
    export_all_mode: Literal['page', 'all']
    formats: list[Literal['csv', 'xlsx']]


class PagingOptions(TypedDict, total=False):
    """Paging mode and sizing; toggles x/y scrollbars."""
    mode: Literal['standard', 'virtual']
    page_size: int
    page_index: int
    cache_size: int
    xscroll: bool
    yscroll: bool


class RowAlternationOptions(TypedDict, total=False):
    """Alternating row striping (enabled flag and color token)."""
    enabled: bool
    color: str


class FilteringOptions(TypedDict, total=False):
    """Toggle filtering and which menus expose filter actions."""
    enabled: bool
    header_menu_filtering: bool
    row_menu_filtering: bool


class SearchOptions(TypedDict, total=False):
    """Configure searchbar visibility, advanced mode, and trigger timing."""
    enabled: bool
    mode: Literal['standard', 'advanced']
    event: Literal['input', 'enter']


# ------ Helper methods --------

def parse_selection_mode(mode: str):
    """Convert TableView selection mode to Treeview selectmode."""
    if mode == 'single':
        return 'browse'
    elif mode == 'multiple':
        return 'extended'
    else:
        return 'none'


def normalize_row_alternation_options(options: RowAlternationOptions | None) -> RowAlternationOptions:
    """Normalize row alternation options with defaults."""
    if options is None:
        return dict(enabled=False, color='background[+1]')
    options.setdefault('enabled', False)
    options.setdefault('color', 'background[+1]')
    return options


def normalize_selection_options(options: SelectionOptions | None) -> SelectionOptions:
    """Normalize selection options with defaults."""
    if options is None:
        return dict(
            mode="single",
            allow_select_all=False,
        )
    options.setdefault('mode', 'single')
    options.setdefault('allow_select_all', False)
    return options


def normalize_filtering_options(options: FilteringOptions | None) -> FilteringOptions:
    """Normalize filtering options with defaults."""
    if options is None:
        return dict(
            enabled=True,
            header_menu_filtering=True,
            row_menu_filtering=True,
        )
    options.setdefault('enabled', True)
    options.setdefault('header_menu_filtering', True)
    options.setdefault('row_menu_filtering', True)
    return options


def normalize_editing_options(options: EditingOptions | None) -> EditingOptions:
    """Normalize editing options with defaults."""
    if options is None:
        return dict(
            adding=False,
            updating=False,
            deleting=False,
            form={}
        )
    options.setdefault('adding', False)
    options.setdefault('updating', False)
    options.setdefault('deleting', False)
    options.setdefault('form', {})
    return options


def normalize_exporting_options(options: ExportingOptions | None) -> ExportingOptions:
    """Normalize exporting options with defaults."""
    if options is None:
        return dict(
            enabled=False,
            allow_export_selected=False,
            export_all_mode='page',
            formats=['csv']
        )
    options.setdefault('enabled', False)
    options.setdefault('allow_export_selected', False)
    options.setdefault('export_all_mode', 'page')
    options.setdefault('formats', ['csv'])
    return options


def normalize_paging_options(options: PagingOptions | None) -> PagingOptions:
    """Normalize paging options with defaults."""
    if options is None:
        return dict(
            mode='standard',
            page_size=250,
            page_index=0,
            cache_size=5,
            xscroll=True,
            yscroll=True,
        )
    options.setdefault('mode', 'standard')
    options.setdefault('page_size', 250)
    options.setdefault('page_index', 0)
    options.setdefault('cache_size', 5)
    options.setdefault('xscroll', True)
    options.setdefault('yscroll', True)
    return options


def normalize_searchbar_options(options: SearchOptions | None) -> SearchOptions:
    """Normalize searchbar options with defaults."""
    if options is None:
        return dict(
            enabled=True,
            mode='standard',
            event='enter'
        )
    options.setdefault('enabled', True)
    options.setdefault('mode', 'standard')
    options.setdefault('event', 'enter')
    # Normalize event to allowed values
    trig = str(options.get('event', 'enter')).lower()
    if trig not in ('input', 'enter'):
        trig = 'enter'
    options['event'] = trig
    return options