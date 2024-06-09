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
| ⚙️  | **Architecture**  | The project has a modular architecture interfacing cleanly with Alpaca's financial APIs. It contains well-defined components for trading, stock management, and data analysis. |
| 🔩 | **Code Quality**  | The code is well-structured, follows consistent styling standards (possibly PEP 8), and uses code analysis tools like ruff for maintaining quality. |
| 📄 | **Documentation** | Significant documentation is present in code and configuration files, though expansion on code usage examples could strengthen usability. |
| 🔌 | **Integrations**  | Integrates with Alpaca API, Pandas, and uses Prophesy for data predictions. Utilizes GitHub Actions for CI/CD. |
| 🧩 | **Modularity**    | High level of modularity; each functionality (trading, stock management, data models) isolated for standalone use and simple integration. |
| 🧪 | **Testing**       | Uses pytest for unit and integration testing supported by GitHub Actions CI workflows, ensuring high code reliability. |
| ⚡️  | **Performance**   | Efficient data handling via Pandas and robust HTTP request management with retry/backoff strategies ensuring performance sustainability. |
| 🛡️ | **Security**      | Utilizes HTTP request validation, API key management, and securing communications with retries and backoff strategies for robust data protection. |
| 📦 | **Dependencies**  | pandas, requests, pendulum, plotly, prophe@appet, ruff, poetry for dependency management, tqdm for progress bar integration. |
| 🚀 | **Scalability**   | Utilizes scalable backend services (Alpaca API), combined with strong modular design to support increased load with simple component duplication/expansion. |

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
    │           ├── orders.py
    │           ├── positions.py
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
            ├── test_orders.py
            ├── test_positions.py
            ├── test_watchlists.py
            └── test_watchlists2.py
```

---

##  Modules

<details closed><summary>.</summary>

| File                                                                                      | Summary                                                                                                                                                                                                                                                                                                                                              |
| ---                                                                                       | ---                                                                                                                                                                                                                                                                                                                                                  |
| [pyproject.toml](https://github.com/TexasCoding/py-alpaca-api/blob/master/pyproject.toml) | Define the projects metadata and configurations, including dependencies, development tools, and documentation settings, ensuring robust setup and maintainability. Serve as the primary configuration file for the packaging and distribution of the py-alpaca-api' Python package, coordinating various aspects of development and build processes. |

</details>

<details closed><summary>src.py_alpaca_api.trading</summary>

| File                                                                                                              | Summary                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| ---                                                                                                               | ---                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| [watchlists.py](https://github.com/TexasCoding/py-alpaca-api/blob/master/src/py_alpaca_api/trading/watchlists.py) | Manage watchlists with functionalities to create, retrieve, update, and delete them. Provide methods to add or remove assets within watchlists based on various attributes such as ID or name, integrating seamlessly with the Alpaca API to facilitate streamlined trading operations within the repositorys architecture.                                                                                                                                                                                                                                                                                                                                             |
| [positions.py](https://github.com/TexasCoding/py-alpaca-api/blob/master/src/py_alpaca_api/trading/positions.py)   | Manage and retrieve Alpaca account positions by providing functionality to obtain details for specific positions or all positions in a users account. Utilize pandas DataFrames for data processing, sorting, and modification, ensuring integrations with account and request handling services within the broader repository architecture.                                                                                                                                                                                                                                                                                                                            |
| [orders.py](https://github.com/TexasCoding/py-alpaca-api/blob/master/src/py_alpaca_api/trading/orders.py)         | The `requests.py` file in the `src/py_alpaca_api/http` directory is responsible for facilitating HTTP request handling within the py-alpaca-api repository. This file plays a critical role in enabling communication between the client interfaces and Alpacas financial APIs by managing the creation, execution, and response processing of API requests. This functionality serves as the backbone for other modules within the project, such as those found in the `trading` and `stock` packages, by providing the essential capability to interact with Alpacas platform for activities such as trading operations, market data retrieval, and asset management. |
| [market.py](https://github.com/TexasCoding/py-alpaca-api/blob/master/src/py_alpaca_api/trading/market.py)         | Manage market-related data interactions by retrieving the current market clock and market calendar data for specified date ranges, converting responses into structured formats such as models and DataFrames to facilitate easy access and manipulation within the broader ecosystem of the repository.                                                                                                                                                                                                                                                                                                                                                                |
| [account.py](https://github.com/TexasCoding/py-alpaca-api/blob/master/src/py_alpaca_api/trading/account.py)       | Manages account-related functionalities by retrieving user account information, fetching account activities based on specified filters, and obtaining portfolio history as a pandas DataFrame. Plays a critical role in the trading module by integrating with Alpacas API to provide essential account insights.                                                                                                                                                                                                                                                                                                                                                       |

</details>

<details closed><summary>src.py_alpaca_api.stock</summary>

| File                                                                                                          | Summary                                                                                                                                                                                                                                                                                                                                                                                     |
| ---                                                                                                           | ---                                                                                                                                                                                                                                                                                                                                                                                         |
| [screener.py](https://github.com/TexasCoding/py-alpaca-api/blob/master/src/py_alpaca_api/stock/screener.py)   | Provide stock filtering capabilities based on given criteria such as price, volume, and trade count. Identify top gainers and losers by calculating percentage changes over specified timeframes, aiding in market analysis and decision making. Integrate seamlessly into broader Alpaca API, utilizing relevant data endpoints and trading functionalities for holistic stock management. |
| [predictor.py](https://github.com/TexasCoding/py-alpaca-api/blob/master/src/py_alpaca_api/stock/predictor.py) | Predictor class leverages historical stock data and the Prophet forecasting model to identify potential future stock gainers. It processes previous day stock losers, forecasts their future performance, and returns symbols most likely to achieve significant gains, enhancing stock screening and predictive analytics capabilities within the overall repository architecture.         |
| [history.py](https://github.com/TexasCoding/py-alpaca-api/blob/master/src/py_alpaca_api/stock/history.py)     | Provide historical stock data by interfacing with the data API, verifying assets as stocks, and preprocessing JSON responses into pandas DataFrames. Enhances the repositorys capacity to fetch detailed and time-specific historical trading information, crucial for analysis, modeling, and prediction tasks within the trading functionality.                                           |
| [assets.py](https://github.com/TexasCoding/py-alpaca-api/blob/master/src/py_alpaca_api/stock/assets.py)       | Assets management functionality is provided by enabling the retrieval of specific or all US equity assets. It ensures assets are active, fractionable, and tradable, excluding OTC exchanges, integrating seamlessly with the larger trading and analysis system within the repositorys architecture.                                                                                       |

</details>

<details closed><summary>src.py_alpaca_api.models</summary>

| File                                                                                                                                     | Summary                                                                                                                                                                                                                                                                                                                                                        |
| ---                                                                                                                                      | ---                                                                                                                                                                                                                                                                                                                                                            |
| [watchlist_model.py](https://github.com/TexasCoding/py-alpaca-api/blob/master/src/py_alpaca_api/models/watchlist_model.py)               | The **watchlist_model.py** file defines the WatchlistModel class and functions for converting watchlist data into WatchlistModel instances. It leverages asset processing to facilitate seamless integration within the parent repository, which focuses on managing and interfacing with financial market data and trading functionalities.                   |
| [position_model.py](https://github.com/TexasCoding/py-alpaca-api/blob/master/src/py_alpaca_api/models/position_model.py)                 | Define and encapsulate data representations for stock positions within the Alpaca trading API. Facilitate conversion between dictionary data and well-structured position objects to support efficient trading operations and analyses in the overall architecture. Enhance data processing consistency and accuracy across the application’s trading modules. |
| [order_model.py](https://github.com/TexasCoding/py-alpaca-api/blob/master/src/py_alpaca_api/models/order_model.py)                       | Define and manage the representation of orders, offering utility functions to convert data dictionaries into `OrderModel` instances and process multi-leg orders for seamless integration into the broader architecture focused on trading activities.                                                                                                         |
| [model_utils.py](https://github.com/TexasCoding/py-alpaca-api/blob/master/src/py_alpaca_api/models/model_utils.py)                       | Assist data processing within models by providing utility functions for extracting and transforming values from dictionaries into specified types such as strings, integers, floats, and dates. Facilitate the alignment of dictionary data with data class structures to streamline data manipulation and model instantiation within the repository.          |
| [clock_model.py](https://github.com/TexasCoding/py-alpaca-api/blob/master/src/py_alpaca_api/models/clock_model.py)                       | Facilitates the management and representation of stock market timing data by defining a ClockModel class. This model enables easy extraction and interpretation of market time information, including current market status and future open and close times, to assist with trading operations within the parent repositorys architecture.                     |
| [asset_model.py](https://github.com/TexasCoding/py-alpaca-api/blob/master/src/py_alpaca_api/models/asset_model.py)                       | In the parent repository, enable the management of asset data by defining the structure of AssetModel. Facilitate the conversion of dictionary data into an AssetModel instance, allowing for streamlined interaction with asset-specific information within the larger Alpaca API interface, thus supporting efficient data handling and manipulation.        |
| [account_model.py](https://github.com/TexasCoding/py-alpaca-api/blob/master/src/py_alpaca_api/models/account_model.py)                   | Facilitates the representation and manipulation of account data within the repository by providing a structured data model. Ensures accurate and efficient conversion of account information from raw dictionary data to a standard format, essential for maintaining consistency and reliability in account-related operations across the system.             |
| [account_activity_model.py](https://github.com/TexasCoding/py-alpaca-api/blob/master/src/py_alpaca_api/models/account_activity_model.py) | AccountActivityModel represents user account activities within the Alpaca trading API. It structures essential activity details and allows transformation from raw dictionary data into a cohesive model using validation and extraction utilities, thereby facilitating accurate data handling in broader trading applications.                               |

</details>

<details closed><summary>src.py_alpaca_api.http</summary>

| File                                                                                                       | Summary                                                                                                                                                                                             |
| ---                                                                                                        | ---                                                                                                                                                                                                 |
| [requests.py](https://github.com/TexasCoding/py-alpaca-api/blob/master/src/py_alpaca_api/http/requests.py) | Provides structured and resilient HTTP request functionality with retry and backoff mechanisms to handle transient errors. Essential for consistent and reliable communication with the Alpaca API. |

</details>

<details closed><summary>.github.workflows</summary>

| File                                                                                                              | Summary                                                                                                                                                                                                                                                                                                                            |
| ---                                                                                                               | ---                                                                                                                                                                                                                                                                                                                                |
| [test-package.yaml](https://github.com/TexasCoding/py-alpaca-api/blob/master/.github/workflows/test-package.yaml) | Automatically initiates and manages the CI pipeline for the py-alpaca-api project, ensuring the code quality across updates. Executes tests and validates code changes, supporting continuous integration practices and maintaining the reliability of the projects features as per specified workflows in the GitHub environment. |

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
