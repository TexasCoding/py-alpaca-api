# Changelog

All notable changes to py-alpaca-api will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [3.0.0] - Unreleased

### Overview
Major release adding complete Alpaca Stock API coverage, performance improvements, and real-time data support.

### Added
- 📋 Comprehensive development plan (DEVELOPMENT_PLAN.md)
- 🏗️ New v3.0.0 branch structure for organized development

### Planned Features (In Development)
#### Phase 1: Critical Missing Features
- [ ] Corporate Actions API - Track dividends, splits, mergers
- [ ] Trade Data Support - Access to individual trade data
- [ ] Market Snapshots - Current market overview for symbols

#### Phase 2: Important Enhancements
- [ ] Account Configuration Management
- [ ] Enhanced Order Management (replace, extended hours)
- [ ] Market Metadata (condition codes, exchange codes)

#### Phase 3: Performance & Quality
- [ ] Batch Operations for multiple symbols
- [ ] Feed Management System (IEX/SIP/OTC)
- [ ] Caching System with configurable TTL

#### Phase 4: Advanced Features
- [ ] WebSocket Streaming Support
- [ ] Async/Await Implementation

### Changed
- Restructured project for v3.0.0 development

### Deprecated
- None

### Removed
- None

### Fixed
- None

### Security
- None

## [2.2.0] - 2024-12-15

### Added
- Stock analysis tools with ML predictions
- Market screener for gainers/losers
- News aggregation from multiple sources
- Sentiment analysis for stocks
- Prophet integration for price forecasting

### Changed
- Improved error handling across all modules
- Enhanced DataFrame operations
- Better type safety with mypy strict mode

### Fixed
- Yahoo Finance news fetching reliability
- DataFrame type preservation issues
- Prophet seasonality parameter handling

## [2.1.0] - 2024-11-01

### Added
- Watchlist management functionality
- Portfolio history tracking
- Market calendar support
- Extended order types (bracket, trailing stop)

### Changed
- Improved pagination for large datasets
- Better rate limit handling

### Fixed
- Order validation for fractional shares
- Timezone handling in market hours

## [2.0.0] - 2024-09-15

### Added
- Complete rewrite with modular architecture
- Full type hints and mypy support
- Comprehensive test suite (109+ tests)
- Separate trading and stock modules

### Changed
- Breaking: New API structure with PyAlpacaAPI class
- Breaking: All methods now return typed dataclasses
- Improved error handling with custom exceptions

### Removed
- Legacy API methods
- Deprecated authentication methods

## [1.0.0] - 2024-06-01

### Added
- Initial release
- Basic trading operations
- Market data retrieval
- Account management

---

*For detailed migration guides between versions, see [MIGRATION.md](MIGRATION.md)*
