# Changelog

All notable changes to py-alpaca-api will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [3.0.1] - 2025-09-20

### Overview
Complete implementation of all Alpaca Market Data API endpoints, achieving 100% API coverage for both Trading and Market Data APIs.

### Added
- ✅ **Complete Market Data API Coverage** - All 11 endpoints now implemented
  - Historical Quotes API (`quotes.get_historical_quotes()`) - Bid/ask quotes with spread calculations
  - Historical Auctions API (`auctions.get_auctions()`, `auctions.get_daily_auctions()`) - Opening and closing auction data
  - Company Logos API (`logos.get_logo()`, `logos.save_logo()`, `logos.get_logo_url()`) - Company logo retrieval
  - Latest Bars API (`history.get_latest_bars()`) - Get the most recent bar for symbols
- ✅ **Complete Trading API Coverage** - All 28 endpoints fully implemented
  - `get_all_orders()` method for comprehensive order retrieval with filtering
- 📚 **Enhanced Documentation**
  - Complete documentation for all new modules
  - Code examples for quotes, auctions, and logos
  - Updated README with all new features
- 🧪 **Comprehensive Testing** - 350+ tests with full coverage
  - 18 tests for logos functionality
  - 11 tests for historical quotes
  - 14 tests for historical auctions
  - 8 tests for latest bars

### Changed
- Extended `Requests` class to support raw binary responses for logo retrieval
- Updated documentation structure to include all new modules

### Fixed
- Type checking issues in auctions module with DataFrame aggregation
- Control flow in logos module for better error handling

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
