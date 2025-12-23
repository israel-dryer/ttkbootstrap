"""Public data source API surface.

Provides unified interface for data management with multiple backend implementations.
"""

from __future__ import annotations

from ttkbootstrap.datasource.base import BaseDataSource
from ttkbootstrap.datasource.memory_source import MemoryDataSource
from ttkbootstrap.datasource.sqlite_source import SqliteDataSource
from ttkbootstrap.datasource.file_source import FileDataSource, FileSourceConfig
from ttkbootstrap.datasource.types import DataSourceProtocol

__all__ = [
    "BaseDataSource",
    "MemoryDataSource",
    "SqliteDataSource",
    "FileDataSource",
    "FileSourceConfig",
    "DataSourceProtocol",
]