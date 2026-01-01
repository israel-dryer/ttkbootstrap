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
    """Control selection mode (single/multi/none) and select-all allowance."""
    mode: Literal['single', 'multi', 'none']
    allow_select_all: bool


class ExportingOptions(TypedDict, total=False):
    """Configure export availability and formats."""
    enabled: bool
    allow_export_selection: bool
    export_scope: Literal['page', 'all']
    formats: tuple[str, ...]


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
    elif mode == 'multi':
        return 'extended'
    else:
        return 'none'


# ------ Build internal dicts from flattened kwargs --------

def build_editing_options(
    enable_adding: bool = False,
    enable_editing: bool = False,
    enable_deleting: bool = False,
    form_options: dict | None = None,
) -> EditingOptions:
    """Build editing options dict from flattened kwargs."""
    return dict(
        adding=enable_adding,
        updating=enable_editing,
        deleting=enable_deleting,
        form=form_options or {}
    )


def build_selection_options(
    selection_mode: Literal['none', 'single', 'multi'] = 'single',
    allow_select_all: bool = True,
) -> SelectionOptions:
    """Build selection options dict from flattened kwargs."""
    return dict(
        mode=selection_mode,
        allow_select_all=allow_select_all,
    )


def build_filtering_options(
    enable_filtering: bool = True,
    enable_header_filtering: bool = True,
    enable_row_filtering: bool = True,
) -> FilteringOptions:
    """Build filtering options dict from flattened kwargs."""
    return dict(
        enabled=enable_filtering,
        header_menu_filtering=enable_header_filtering,
        row_menu_filtering=enable_row_filtering,
    )


def build_exporting_options(
    enable_exporting: bool = False,
    allow_export_selection: bool = True,
    export_scope: Literal['page', 'all'] = 'page',
    export_formats: tuple[str, ...] | None = None,
) -> ExportingOptions:
    """Build exporting options dict from flattened kwargs."""
    return dict(
        enabled=enable_exporting,
        allow_export_selection=allow_export_selection,
        export_scope=export_scope,
        formats=export_formats or ('csv',)
    )


def build_paging_options(
    paging_mode: Literal['standard', 'virtual'] = 'standard',
    page_size: int = 25,
    page_index: int = 0,
    page_cache_size: int = 3,
    show_vscrollbar: bool = True,
    show_hscrollbar: bool = False,
) -> PagingOptions:
    """Build paging options dict from flattened kwargs."""
    return dict(
        mode=paging_mode,
        page_size=page_size,
        page_index=page_index,
        cache_size=page_cache_size,
        xscroll=show_hscrollbar,
        yscroll=show_vscrollbar,
    )


def build_search_options(
    enable_search: bool = True,
    search_mode: Literal['standard', 'advanced'] = 'standard',
    search_trigger: Literal['enter', 'input'] = 'enter',
) -> SearchOptions:
    """Build search options dict from flattened kwargs."""
    return dict(
        enabled=enable_search,
        mode=search_mode,
        event=search_trigger,
    )


def build_row_alternation_options(
    striped: bool = False,
    striped_background: str = 'background[+1]',
) -> RowAlternationOptions:
    """Build row alternation options dict from flattened kwargs."""
    return dict(
        enabled=striped,
        color=striped_background,
    )