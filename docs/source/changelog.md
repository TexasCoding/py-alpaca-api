# Changelog

All notable changes to PyAlpacaAPI will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [3.0.0] - 2024-09-20

### Added
- Complete type safety with mypy strict mode
- Comprehensive caching system with LRU and Redis support
- Automatic feed detection and fallback (SIP → IEX → OTC)
- Batch operations for multi-symbol data fetching
- 350+ comprehensive tests
- ML predictions using Prophet
- Sentiment analysis and recommendations
- Corporate actions support
- Full Sphinx documentation

### Changed
- Complete rewrite of the codebase for better maintainability
- Improved error handling with custom exception hierarchy
- Better module organization and separation of concerns
- Enhanced performance with caching and batching
- Updated to Python 3.10+ requirement

### Fixed
- All type checking errors resolved
- Rate limiting issues in CI/CD
- DataFrame type preservation
- Prophet seasonality parameter handling

## [2.0.0] - 2024-08-15

### Added
- Initial support for caching
- Basic feed management
- Stock screener functionality
- News aggregation

### Changed
- Refactored API structure
- Improved error messages
- Better documentation

## [1.0.0] - 2024-06-01

### Added
- Initial release
- Basic trading operations
- Market data access
- Account management
- Order placement
- Position tracking
