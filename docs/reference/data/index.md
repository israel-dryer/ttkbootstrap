# Data

Data source abstractions and implementations.

This section documents the data-source API used by data-driven widgets and utilities.
If you're building a custom data source, start with the protocol/base types.

See the [DataSource Guide](../../guides/datasource.md) for usage examples and patterns.

## Core types

- [DataSourceProtocol](DataSourceProtocol.md): expected interface
- [BaseDataSource](BaseDataSource.md): base implementation with hooks

## Implementations

- [MemoryDataSource](MemoryDataSource.md): in-memory storage
- [SqliteDataSource](SqliteDataSource.md): SQLite-backed persistence
- [FileDataSource](FileDataSource.md): CSV, JSON, JSONL file loading
- [FileSourceConfig](FileSourceConfig.md): configuration for file-backed sources

