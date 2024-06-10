<p align="center">
  <img src="https://raw.githubusercontent.com/PKief/vscode-material-icon-theme/ec559a9f6bfd399b82bb44393651661b08aaf7ba/icons/folder-markdown-open.svg" width="100" alt="project-logo">
</p>
<p align="center">
    <h1 align="center">PY-ALPACA-API</h1>
</p>
<p align="center">
    <em>Streamline Trading with Seamless Alpaca Integration</em>
</p>
<p align="center">
    <img alt="GitHub Actions Workflow Status" src="https://img.shields.io/github/actions/workflow/status/TexasCoding/py-alpaca-api/.github%2Fworkflows%2Ftest-package.yaml">
	<img src="https://img.shields.io/github/license/TexasCoding/py-alpaca-api?style=flat-square&logo=opensourceinitiative&logoColor=white&color=0080ff" alt="license">
	<img src="https://img.shields.io/github/last-commit/TexasCoding/py-alpaca-api?style=flat-square&logo=git&logoColor=white&color=0080ff" alt="last-commit">
	<img src="https://img.shields.io/github/languages/top/TexasCoding/py-alpaca-api?style=flat-square&color=0080ff" alt="repo-top-language">
	<img src="https://img.shields.io/github/languages/count/TexasCoding/py-alpaca-api?style=flat-square&color=0080ff" alt="repo-language-count">
<p>
<p align="center">
		<em>Developed with the software and tools below.</em>
</p>
<p align="center">
	<img src="https://img.shields.io/badge/tqdm-FFC107.svg?style=flat-square&logo=tqdm&logoColor=black" alt="tqdm">
	<img src="https://img.shields.io/badge/precommit-FAB040.svg?style=flat-square&logo=pre-commit&logoColor=black" alt="precommit">
	<img src="https://img.shields.io/badge/Poetry-60A5FA.svg?style=flat-square&logo=Poetry&logoColor=white" alt="Poetry">
	<img src="https://img.shields.io/badge/Plotly-3F4F75.svg?style=flat-square&logo=Plotly&logoColor=white" alt="Plotly">
	<img src="https://img.shields.io/badge/Python-3776AB.svg?style=flat-square&logo=Python&logoColor=white" alt="Python">
	<img src="https://img.shields.io/badge/GitHub%20Actions-2088FF.svg?style=flat-square&logo=GitHub-Actions&logoColor=white" alt="GitHub%20Actions">
	<img src="https://img.shields.io/badge/pandas-150458.svg?style=flat-square&logo=pandas&logoColor=white" alt="pandas">
</p>

<br><!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary><br>

- [ Overview](#-overview)
- [ Features](#-features)
- [ Repository Structure](#-repository-structure)
- [ Modules](#-modules)
- [ Getting Started](#-getting-started)
  - [ Installation](#-installation)
  - [ Usage](#-usage)
  - [ Tests](#-tests)
- [ Project Roadmap](#-project-roadmap)
- [ Contributing](#-contributing)
- [ License](#-license)
- [ Acknowledgments](#-acknowledgments)
</details>
<hr>

##  Overview

### V2.0.0 is not compatible with previous versions.
Use the [V1.0.3](https://github.com/TexasCoding/py-alpaca-api/tree/master) branch for the previous version.

The py-alpaca-api project provides a comprehensive Python interface for executing financial trading operations via the Alpaca API. It enables the management of watchlists, account positions, market data, and stock portfolios. It includes functionalities for order processing, stock screening, and predictive analytics leveraging historical data, enhancing market analysis and trading efficiencies. By abstracting complex API interactions into user-friendly Python modules, the project supports streamlined, data-driven trading decisions, making it a valuable tool for both developers and traders aiming for effective financial market engagement.

This project is mainly for fun and my personal use. Hopefully others find it helpful as well. Alpaca has a great Python SDK that provides a robust API interface, just more complex than I need for my uses. Checkout it out here [Alpaca-py](https://alpaca.markets/sdks/python/).

---

##  Features

|    |   Feature         | Description |
|----|-------------------|---------------------------------------------------------------|
| ⚙️  | **Architecture**  | The project is organized into modular packages, primarily dealing with stock trading, interactions with APIs (mainly Alpaca), and data handling. The trading modules handle various operations like watchlists, positions, accounts, news, and market interactions. |
| 🔩 | **Code Quality**  | The codebase appears to follow a structured and modular approach with the usage of dataclasses for models ensuring clarity. The presence of utility functions indicates clean separation of concerns for data transformation tasks. |
| 📄 | **Documentation** | Documentation includes code comments and descriptive docstrings for functions and classes. The `pyproject.toml` and `requirements.txt` files provide clear dependency management information. However, project-wide documentation and usage examples may need enhancement. |
| 🔌 | **Integrations**  | The code integrates with prominent financial data services like Yahoo Finance and Benzinga. It also utilizes Prophet for stock prediction and leverages the Alpaca trading API for executing trading operations. Matplotlib and Plotly are employed for data visualization. |
| 🧩 | **Modularity**    | The project is highly modular with distinct packages and sub-packages handling specific responsibilities such as historical data retrieval, predictive analysis, trading functions, and account management. Reusability is evident through the use of utility modules. |
| 🧪 | **Testing**       | Utilizes continuous integration via GitHub Actions, as seen in the `.github/workflows/test-package.yaml` workflow file. Testing practices appear to include automated tests for multiple environments which help catch issues early in the development process. |
| ⚡️  | **Performance**   | Performance optimization measures include efficient HTTP request handling with retry mechanisms. The Prophet model ensures efficient stock prediction by leveraging historical data with advanced forecasting techniques. Explicit attention to modular detailed design suggests minimalistic performance overheads. |
| 🛡️ | **Security**      | Security measures such as data validation within utility functions and thorough modeling for user and trading data are in place. However, explicit security practices regarding API key management or data encryption could be better detailed. |
| 📦 | **Dependencies**  | Key external libraries include `pandas` for data manipulation, `requests` for HTTP communication, `matplotlib` and `plotly` for visualization, `beautifulsoup4` for web scraping, `numpy` for numerical operations, and `prophet` for predictive modeling. |
| 🚀 | **Scalability**   | The architecture supports scalable operations given its modularity and use of robust libraries like `pandas` and `numpy`. The reliance on scalable cloud-hosted APIs such as Alpaca further enhances the capability to handle increased load. |

---

##  Repository Structure

```sh
└── py-alpaca-api/
    ├── src
    │   └── py_alpaca_api
    │       ├── __init__.py
    │       ├── http
    │       │   └── requests.py
    │       ├── models
    │       │   ├── account_activity_model.py
    │       │   ├── account_model.py
    │       │   ├── asset_model.py
    │       │   ├── clock_model.py
    │       │   ├── model_utils.py
    │       │   ├── order_model.py
    │       │   ├── position_model.py
    │       │   └── watchlist_model.py
    │       ├── stock
    │       │   ├── __init__.py
    │       │   ├── assets.py
    │       │   ├── history.py
    │       │   ├── predictor.py
    │       │   └── screener.py
    │       └── trading
    │           ├── __init__.py
    │           ├── account.py
    │           ├── market.py
    │           ├── news.py
    │           ├── orders.py
    │           ├── positions.py
    │           ├── recommendations.py
    │           └── watchlists.py
    └── tests
        ├── __init__.py
        ├── test_http
        │   └── test_requests.py
        ├── test_models
        │   ├── test_account_activity_model.py
        │   ├── test_account_model.py
        │   ├── test_asset_model.py
        │   ├── test_clock_model.py
        │   ├── test_order_model.py
        │   ├── test_position_model.py
        │   └── test_watchlist_model.py
        ├── test_stock
        │   ├── test_assets.py
        │   ├── test_history.py
        │   ├── test_history2.py
        │   ├── test_predictor.py
        │   └── test_screener.py
        └── test_trading
            ├── test_account.py
            ├── test_account2.py
            ├── test_news.py
            ├── test_orders.py
            ├── test_positions.py
            ├── test_recommendations.py
            ├── test_watchlists.py
            └── test_watchlists2.py
```

---

##  Modules

<details closed><summary>.</summary>

| File                                                                                          | Summary                                                                                                                                                                                                                                                                                                                                                                                      |
| ---                                                                                           | ---                                                                                                                                                                                                                                                                                                                                                                                          |
| [requirements.txt](https://github.com/TexasCoding/py-alpaca-api/blob/master/requirements.txt) | Specify all required dependencies for the `py-alpaca-api` project, ensuring compatibility with Python versions 3.12 to 4.0. Critical dependencies facilitate functionalities for data visualization, time series analysis, HTTP requests, date manipulation, and prophet, among others, reinforcing seamless integrations and optimal performance across various platforms and environments. |
| [pyproject.toml](https://github.com/TexasCoding/py-alpaca-api/blob/master/pyproject.toml)     | Defines metadata and dependency management for the py-alpaca-api project using Poetry, ensuring compatibility and functionality with specified Python and library versions, alongside configuring development, testing, and documentation dependencies for streamlined project maintenance and collaboration. Serves as the foundational setup for the project's environment.                |

</details>

<details closed><summary>src.py_alpaca_api.trading</summary>

| File                                                                                                                        | Summary                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| ---                                                                                                                         | ---                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| [watchlists.py](https://github.com/TexasCoding/py-alpaca-api/blob/master/src/py_alpaca_api/trading/watchlists.py)           | Facilitates complete management of watchlists in the trading module, handling operations such as retrieval, creation, updating, deletion, and manipulation of assets, seamlessly integrating with HTTP requests and watchlist model handling for comprehensive API interaction. Part of a structured trading architecture within the py-alpaca-api repository.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| [recommendations.py](https://github.com/TexasCoding/py-alpaca-api/blob/master/src/py_alpaca_api/trading/recommendations.py) | Provide stock recommendations and generate sentiment analysis for given symbols, integrating with external APIs and popular stock data sources like Yahoo Finance. Enhance trading strategy modules in the parent repositorys architecture, supporting informed investment decisions for users.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| [positions.py](https://github.com/TexasCoding/py-alpaca-api/blob/master/src/py_alpaca_api/trading/positions.py)             | Manage user positions, providing retrieval and organization of Alpaca trading account positions. Enhance data with comprehensive market details, sorting capabilities, and support for tracking cash positions alongside asset positions, ensuring accurate portfolio analysis and streamlined access to current trading statuses.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| [orders.py](https://github.com/TexasCoding/py-alpaca-api/blob/master/src/py_alpaca_api/trading/orders.py)                   | Py-alpaca-api/src/py_alpaca_api/http/requests.py`The `requests.py` file is a critical component within the `py_alpaca_api` package of the repository. This file primarily handles the HTTP requests specific to the Alpaca API, facilitating communication between the user's application and Alpaca's endpoint services. It encapsulates the necessary methods to perform various operations such as querying market data, submitting orders, and retrieving account information. By abstracting and managing these interactions, `requests.py` serves as a foundational module that enables other parts of the repository, such as models and higher-level structures, to function seamlessly without directly managing the complexities of HTTP transactions. Overall, it plays a pivotal role in ensuring that the API communicates effectively and reliably with Alpacas systems, serving as an backbone for the integration functionalities of the entire `py-alpaca-api` repository. |
| [news.py](https://github.com/TexasCoding/py-alpaca-api/blob/master/src/py_alpaca_api/trading/news.py)                       | Retrieves and processes financial news articles related to specific market symbols from sources like Yahoo Finance and Benzinga, integrating them into the trading module to provide real-time, relevant news updates. Enables article scraping, HTML stripping, content truncation, and organized presentation with options to filter by date and content presence.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| [market.py](https://github.com/TexasCoding/py-alpaca-api/blob/master/src/py_alpaca_api/trading/market.py)                   | Facilitates interaction with the market data endpoints. Provides methods to retrieve the current market clock and market calendar within a specified date range, returning structured data. This is essential for ensuring the core trading functionality operates with accurate market timing, enhancing decision-making and automation capabilities.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| [account.py](https://github.com/TexasCoding/py-alpaca-api/blob/master/src/py_alpaca_api/trading/account.py)                 | Manage user account information, activities, and portfolio history within the Alpaca API trading module. Offer seamless data retrieval, including user account details, activity logs filtered by type and date, and detailed portfolio history with configurable periods, timeframes, and intraday reporting, presented in a structured and analyzable format.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |

</details>

<details closed><summary>src.py_alpaca_api.stock</summary>

| File                                                                                                          | Summary                                                                                                                                                                                                                                                                                                                                |
| ---                                                                                                           | ---                                                                                                                                                                                                                                                                                                                                    |
| [screener.py](https://github.com/TexasCoding/py-alpaca-api/blob/master/src/py_alpaca_api/stock/screener.py)   | Streamlines the identification and filtering of stock market gainers and losers based on specific criteria such as price, change, volume, and trade count. Leverages Alpaca Data API to retrieve and evaluate stocks, efficiently categorizing them for further decision-making processes in trading applications.                     |
| [predictor.py](https://github.com/TexasCoding/py-alpaca-api/blob/master/src/py_alpaca_api/stock/predictor.py) | Predicts future stock gainers by leveraging historical stock data and the Prophet model for forecasting. Collects data on previous day losers, trains a model, and generates a forecast to identify stocks expected to yield high future returns, aiding in strategic stock trading decisions.                                         |
| [history.py](https://github.com/TexasCoding/py-alpaca-api/blob/master/src/py_alpaca_api/stock/history.py)     | Retrieve and preprocess historical stock data, ensuring the asset is a valid stock before fetching. Offer end-users rich, structured financial data in customizable parameters to aid in stock analysis within the overarching Alpaca API-based trading platform architecture.                                                         |
| [assets.py](https://github.com/TexasCoding/py-alpaca-api/blob/master/src/py_alpaca_api/stock/assets.py)       | Provide functionality for retrieving asset information from the Alpaca API. Supports fetching individual asset details and obtaining a filtered DataFrame of multiple assets, focusing on active, fractionable, and tradable US equities while excluding specified exchanges. Integrates with asset models to ensure data consistency. |

</details>

<details closed><summary>src.py_alpaca_api.models</summary>

| File                                                                                                                                     | Summary                                                                                                                                                                                                                                                                                                                                                                           |
| ---                                                                                                                                      | ---                                                                                                                                                                                                                                                                                                                                                                               |
| [watchlist_model.py](https://github.com/TexasCoding/py-alpaca-api/blob/master/src/py_alpaca_api/models/watchlist_model.py)               | Facilitates the conversion and management of watchlist data for the Alpaca API by defining the `WatchlistModel` data class, processing asset lists into `AssetModel` objects, and providing functions to transform raw data dictionaries into fully-formed `WatchlistModel` instances, thus ensuring compatibility with the repositorys overall architecture.                     |
| [position_model.py](https://github.com/TexasCoding/py-alpaca-api/blob/master/src/py_alpaca_api/models/position_model.py)                 | Model investor positions, capturing attributes like asset details, market value, and performance metrics. Ensure seamless data transformation through a utility function that converts dictionaries into structured PositionModel instances. Central to monitoring and analyzing financial portfolios within the broader repository focused on trading and stock data management. |
| [order_model.py](https://github.com/TexasCoding/py-alpaca-api/blob/master/src/py_alpaca_api/models/order_model.py)                       | Manages the definition and creation of order data models within the API context. Facilitates the processing, conversion, and organization of order-related information, supporting detailed order data extraction and representation in a standardized model crucial for trading operations and strategies in the parent repository.                                              |
| [model_utils.py](https://github.com/TexasCoding/py-alpaca-api/blob/master/src/py_alpaca_api/models/model_utils.py)                       | Facilitates data extraction and transformation for various data models within the Alpaca API by providing utility functions to retrieve and process dictionary values. Ensures consistent and type-safe data parsing for integers, floats, strings, and dates, optimizing data handling across the repositorys different model layers.                                            |
| [clock_model.py](https://github.com/TexasCoding/py-alpaca-api/blob/master/src/py_alpaca_api/models/clock_model.py)                       | Define a data model for market clock information, encapsulating the market status and key timestamps. Include functions for creating model instances from dictionaries, facilitating structured and efficient data handling within the broader API.                                                                                                                               |
| [asset_model.py](https://github.com/TexasCoding/py-alpaca-api/blob/master/src/py_alpaca_api/models/asset_model.py)                       | Provide a structured abstraction for financial asset data, utilizing dataclass to define essential asset attributes. Facilitate transformation of data dictionaries to asset model instances, aiding in seamless interaction and manipulation within the broader trading API ecosystem. Boosts integration efficiency with other models and API endpoints.                        |
| [account_model.py](https://github.com/TexasCoding/py-alpaca-api/blob/master/src/py_alpaca_api/models/account_model.py)                   | Define and structure the properties and behavior of account-related data within the context of the API. Enables conversion of dictionary data into AccountModel instances for seamless data management and interaction with Alpaca’s trading platform.                                                                                                                            |
| [account_activity_model.py](https://github.com/TexasCoding/py-alpaca-api/blob/master/src/py_alpaca_api/models/account_activity_model.py) | Models account activity data in a structured format, enabling easy conversion from dictionary inputs. Facilitates efficient data encapsulation and retrieval for handling account-related events within the trading application. Integrates with existing model utilities for standardized processing and consistency within the repository’s architecture.                       |

</details>

<details closed><summary>src.py_alpaca_api.http</summary>

| File                                                                                                       | Summary                                                                                                                                                                                        |
| ---                                                                                                        | ---                                                                                                                                                                                            |
| [requests.py](https://github.com/TexasCoding/py-alpaca-api/blob/master/src/py_alpaca_api/http/requests.py) | Handle HTTP requests with configurable retry strategies, ensuring resilient communication with APIs, essential for robust data exchanges and integrations within the py-alpaca-api repository. |

</details>

<details closed><summary>.github.workflows</summary>

| File                                                                                                              | Summary                                                                                                                                                                                                                                                                     |
| ---                                                                                                               | ---                                                                                                                                                                                                                                                                         |
| [test-package.yaml](https://github.com/TexasCoding/py-alpaca-api/blob/master/.github/workflows/test-package.yaml) | Define the continuous integration workflow for the repository by automating the testing process. Configure multi-environment tests for the software package to ensure reliability and catch issues early by automatically running tests on every code push or pull request. |

</details>

---

##  Getting Started

**System Requirements:**

* **Python**: `version 3.12.0`

###  Installation

<h4>From <code>source</code></h4>

> 1. Clone the py-alpaca-api repository:
>
> ```console
> $ git clone https://github.com/TexasCoding/py-alpaca-api
> ```
>
> 2. Change to the project directory:
> ```console
> $ cd py-alpaca-api
> ```
>
> 3. Install the dependencies:
> ```console
> $ pip install -r requirements.txt
> ```

###  Usage

<h4>From <code>source</code></h4>

> Run py-alpaca-api using the command below:
> ```python
> import os
> from py_alpaca_api import PyAlpacaAPI
>
> api_key = os.environ.get("ALPACA_API_KEY") 
> api_key = os.environ.get("ALPACA_SECRET_KEY") 
>
> api = PyAlpacaAPI(api_key=api_key, api_secret=api_secret)
>
> # Get the account information for the authenticated account.
> account = api.trading.account.get()
> 
> # Get stock asset information
> asset = api.stock.assets.get("AAPL")
>
> # Get stock historical data
> historical_data = api.stock.history.get_stock_data("AAPL", start="2021-01-01", end="2021-01-10")
> ```

###  Tests

> Run the test suite using the command below:
> Export your API key and secret key as environment variables:
> Or use .env file (recommended)
> ```console
> $ export ALPACA_API_KEY="YOUR_API_KEY"
> $ export ALPACA_SECRET_KEY="YOUR_SECRET_KEY"
>
> $ pytest
> ```


##  Contributing

Contributions are welcome! Here are several ways you can contribute:

- **[Report Issues](https://github.com/TexasCoding/py-alpaca-api/issues)**: Submit bugs found or log feature requests for the `py-alpaca-api` project.
- **[Submit Pull Requests](https://github.com/TexasCoding/py-alpaca-api/blob/main/CONTRIBUTING.md)**: Review open PRs, and submit your own PRs.
- **[Join the Discussions](https://github.com/TexasCoding/py-alpaca-api/discussions)**: Share your insights, provide feedback, or ask questions.

<details closed>
<summary>Contributing Guidelines</summary>

1. **Fork the Repository**: Start by forking the project repository to your github account.
2. **Clone Locally**: Clone the forked repository to your local machine using a git client.
   ```sh
   git clone https://github.com/TexasCoding/py-alpaca-api
   ```
3. **Create a New Branch**: Always work on a new branch, giving it a descriptive name.
   ```sh
   git checkout -b new-feature-x
   ```
4. **Make Your Changes**: Develop and test your changes locally.
5. **Commit Your Changes**: Commit with a clear message describing your updates.
   ```sh
   git commit -m 'Implemented new feature x.'
   ```
6. **Push to github**: Push the changes to your forked repository.
   ```sh
   git push origin new-feature-x
   ```
7. **Submit a Pull Request**: Create a PR against the original project repository. Clearly describe the changes and their motivations.
8. **Review**: Once your PR is reviewed and approved, it will be merged into the main branch. Congratulations on your contribution!
</details>

<details closed>
<summary>Contributor Graph</summary>
<br>
<p align="center">
   <a href="https://github.com{/TexasCoding/py-alpaca-api/}graphs/contributors">
      <img src="https://contrib.rocks/image?repo=TexasCoding/py-alpaca-api">
   </a>
</p>
</details>

---

##  License

This project is protected under the [MIT](https://choosealicense.com/licenses/mit/) License. For more details, refer to the [LICENSE](https://choosealicense.com/licenses/mit/) file.

---

##  Acknowledgments

- List any resources, contributors, inspiration, etc. here.

[**Return**](#-overview)

---
