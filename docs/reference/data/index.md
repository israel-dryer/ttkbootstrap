# Data

Data source abstractions and implementations.

This section documents the data-source API used by data-driven widgets and utilities.
If you’re building a custom data source, start with the protocol/base types.

## Core types

- [DataSourceProtocol](DataSourceProtocol.md): expected interface
- [BaseDataSource](BaseDataSource.md): base implementation

## Implementations

- [MemoryDataSource](MemoryDataSource.md)
- [SqliteDataSource](SqliteDataSource.md)
- [FileDataSource](FileDataSource.md)
- [FileSourceConfig](FileSourceConfig.md): configuration for file-backed sources

