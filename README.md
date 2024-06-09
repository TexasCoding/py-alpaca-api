<p align="center">
  <img src="https://raw.githubusercontent.com/PKief/vscode-material-icon-theme/ec559a9f6bfd399b82bb44393651661b08aaf7ba/icons/folder-markdown-open.svg" width="100" alt="project-logo">
</p>
<p align="center">
    <h1 align="center">PY-ALPACA-API</h1>
</p>
<p align="center">
    <em>Trade Smart, Analyze Swiftly, Invest Confidently.</em>
</p>
<p align="center">
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

The py-alpaca-api project provides a comprehensive Python interface for interacting with the Alpaca Markets REST API. It enables users to manage trading positions, watchlists, assets, orders, and account information. Additionally, it supports historical data retrieval, market analysis, stock screening, and predictive analytics based on historical patterns. By facilitating robust communication with Alpacas endpoints, py-alpaca-api enhances automated trading functionalities, ensuring developers have the tools necessary for sophisticated market operations and data-driven trading strategies. The project leverages seamless integration, making it a valuable asset for both individual traders and automated trading systems.

---

##  Features

|    | Feature            | Description                                                                                          |
|----|--------------------|------------------------------------------------------------------------------------------------------|
| ⚙️  | **Architecture**  | The project features a modular design emphasizing REST API interactions with Alpaca Markets for trading. |
| 🔩 | **Code Quality**  | Adopts consistent style conventions and processing patterns, ensuring readability and maintainable structure. |
| 📄 | **Documentation** | Thorough documentation including function docstrings and detailed README.md to aid user understanding. |
| 🔌 | **Integrations**  | Integrates with Alpaca Markets REST API, utilizes `pandas` for data handling, and `requests` for HTTP communication. |
| 🧩 | **Modularity**    | Divided into numerous specialized modules, enhancing code reusability and separation of concerns.  |
| 🧪 | **Testing**       | Employs automated testing through GitHub Actions; unit tests for key functionalities present.  |
| ⚡️  | **Performance**   | Focuses on efficient HTTP request handling; no significant performance bottlenecks observed in transaction processing. |
| 🛡️ | **Security**      | Leverages credentials management best practices; ensures HTTPS for secure API calls to enforce data protection. |
| 📦 | **Dependencies**  | Relies on `pandas`, `requests`, `prophet`, `plotly`, and others managed via Poetry dependency management. |
| 🚀 | **Scalability**   | Capable of handling increased API requests smoothly, benefiting from efficient HTTP request management. |
```

---

##  Repository Structure

```sh
└── py-alpaca-api/
    ├── .github
    │   └── workflows
    ├── README.md
    ├── docs
    │   ├── Makefile
    │   ├── make.bat
    │   └── source
    ├── poetry.lock
    ├── pyproject.toml
    ├── pytest.ini
    ├── src
    │   └── py_alpaca_api
    └── tests
        ├── __init__.py
        ├── test_http
        ├── test_models
        ├── test_stock
        └── test_trading
```

---

##  Modules

<details closed><summary>.</summary>

| File                                                                                      | Summary                                                                                                                                                                                                                                                                                            |
| ---                                                                                       | ---                                                                                                                                                                                                                                                                                                |
| [pyproject.toml](https://github.com/TexasCoding/py-alpaca-api/blob/master/pyproject.toml) | Define project metadata, dependencies, and configuration for the py-alpaca-api package, which facilitates interaction with Alpaca Markets REST API. Ensure consistent build, development, and testing environments using specific tools and dependencies outlined under poetrys management system. |

</details>

<details closed><summary>src.py_alpaca_api.trading</summary>

| File                                                                                                              | Summary                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| ---                                                                                                               | ---                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| [watchlists.py](https://github.com/TexasCoding/py-alpaca-api/blob/master/src/py_alpaca_api/trading/watchlists.py) | Facilitate the management of watchlists by providing functionalities to create, retrieve, update, delete watchlists, and manage associated assets within the py-alpaca-api repository. Ensure seamless communication with the trading API via HTTP requests, handling responses, and adhering to specified parameters and conditions.                                                                                                                                                                                                                                                                              |
| [positions.py](https://github.com/TexasCoding/py-alpaca-api/blob/master/src/py_alpaca_api/trading/positions.py)   | Positions retrieval and management for a users Alpaca account is the core function, featuring symbol-specific position lookups, a comprehensive DataFrame of all asset positions, data modification, sorting, and incorporation of cash position details to provide a holistic view of the accounts holdings and performance metrics.                                                                                                                                                                                                                                                                              |
| [orders.py](https://github.com/TexasCoding/py-alpaca-api/blob/master/src/py_alpaca_api/trading/orders.py)         | The `src/py_alpaca_api/trading/orders.py` file is an integral component of the overall repository, focusing on managing trading orders within the `py-alpaca-api`. This file includes the `Orders` class, which initializes with essential connection details. Its primary role is to facilitate the creation, retrieval, management, and cancellation of trading orders through interactions with the Alpaca trading API. This fits into the larger architecture by providing crucial functionality for handling order-based operations, a key aspect for users leveraging the Alpaca API for trading activities. |
| [market.py](https://github.com/TexasCoding/py-alpaca-api/blob/master/src/py_alpaca_api/trading/market.py)         | Facilitates market data retrieval by offering functions to access the current market clock and the market calendar within a specified date range. Integrates with the Alpaca API to provide formatted data crucial for trading decisions, harmonizing with the repositorys broader architecture aimed at robust and reliable trading functionalities.                                                                                                                                                                                                                                                              |
| [account.py](https://github.com/TexasCoding/py-alpaca-api/blob/master/src/py_alpaca_api/trading/account.py)       | Facilitates user interaction with Alpaca API by enabling retrieval of account information, querying of specific account activities with optional date filters, and collection of portfolio history data, transformed into a pandas DataFrame for further analysis. Efficiently acts as an intermediary between user requests and Alpacas endpoints.                                                                                                                                                                                                                                                                |

</details>

<details closed><summary>src.py_alpaca_api.stock</summary>

| File                                                                                                          | Summary                                                                                                                                                                                                                                                                                                                                                               |
| ---                                                                                                           | ---                                                                                                                                                                                                                                                                                                                                                                   |
| [screener.py](https://github.com/TexasCoding/py-alpaca-api/blob/master/src/py_alpaca_api/stock/screener.py)   | Provides functionality to filter and retrieve specific stock data from the Alpaca API based on various criteria such as price, volume, and trade counts. It enables users to get lists of stock gainers or losers over specific timeframes by processing and sorting the data accordingly.                                                                            |
| [predictor.py](https://github.com/TexasCoding/py-alpaca-api/blob/master/src/py_alpaca_api/stock/predictor.py) | Predicts future stock gainers based on historical data analysis using Prophet. Uses historical data retrieval, prophetic model training, and forecast generation to evaluate potential gains for previous day losers. Integrates tightly with the History and Screener modules to streamline scanning and prediction processes within the py-alpaca-api architecture. |
| [history.py](https://github.com/TexasCoding/py-alpaca-api/blob/master/src/py_alpaca_api/stock/history.py)     | Facilitates retrieving and preprocessing historical stock data by verifying if a given asset is a stock, fetching historical data through specific parameters, and converting the raw data into structured pandas DataFrames. Integrates seamlessly into the APIs architecture for efficient data handling and analysis.                                              |
| [assets.py](https://github.com/TexasCoding/py-alpaca-api/blob/master/src/py_alpaca_api/stock/assets.py)       | Manage and retrieve asset information for US equities within the Alpaca API, ensuring assets are active, fractionable, and tradable, and they do not belong to excluded exchanges like OTC. Integrates with the broader py-alpaca-api architecture by handling API requests and processing responses into structured formats such as pandas DataFrames.               |

</details>

<details closed><summary>src.py_alpaca_api.models</summary>

| File                                                                                                                                     | Summary                                                                                                                                                                                                                                                                                                                                                                                              |
| ---                                                                                                                                      | ---                                                                                                                                                                                                                                                                                                                                                                                                  |
| [watchlist_model.py](https://github.com/TexasCoding/py-alpaca-api/blob/master/src/py_alpaca_api/models/watchlist_model.py)               | Defines the WatchlistModel for representing a users watchlist, and provides utility functions to convert dictionary data into WatchlistModel and AssetModel instances, facilitating structured data usage and manipulation within the Alpaca API system.                                                                                                                                             |
| [position_model.py](https://github.com/TexasCoding/py-alpaca-api/blob/master/src/py_alpaca_api/models/position_model.py)                 | Define the structure and attributes of a trading position within the Alpaca API, encapsulating essential properties such as asset details, quantity, price metrics, profitability, and intraday performance. Implement a function to generate PositionModel instances from dictionaries, facilitating data handling for financial computations and API interactions within the broader architecture. |
| [order_model.py](https://github.com/TexasCoding/py-alpaca-api/blob/master/src/py_alpaca_api/models/order_model.py)                       | Define data structure and transformation logic for stock trade orders within the Alpaca API wrapper. Streamline instance creation from dictionaries and process nested order components. Facilitate interaction and integration with Alpacas trading functionalities by organizing order data cohesively within the broader repository.                                                              |
| [model_utils.py](https://github.com/TexasCoding/py-alpaca-api/blob/master/src/py_alpaca_api/models/model_utils.py)                       | Model utility functions assist in processing and extracting data from dictionaries. Enhance data manipulation consistency and accuracy of operations involving string, date, float, and integer values based on defined field processors and data classes within the larger py-alpaca-api architecture for streamlined API interactions.                                                             |
| [clock_model.py](https://github.com/TexasCoding/py-alpaca-api/blob/master/src/py_alpaca_api/models/clock_model.py)                       | Defines the `ClockModel` data class, representing market clock information such as market status and timings. Translates dictionary data to `ClockModel` instances, ensuring seamless integration with the parent repository’s framework for handling market-related data in a type-safe manner. Enhances API responses with structured clock-based insights.                                        |
| [asset_model.py](https://github.com/TexasCoding/py-alpaca-api/blob/master/src/py_alpaca_api/models/asset_model.py)                       | Define and manage asset structures within the `py-alpaca-api` for interaction with financial data. Ensure accurate and efficient data transformation from dictionaries to AssetModel instances, supporting critical functions related to asset attributes and enabling compatibility with Alpacas trading platform APIs.                                                                             |
| [account_model.py](https://github.com/TexasCoding/py-alpaca-api/blob/master/src/py_alpaca_api/models/account_model.py)                   | Represent the AccountModel domain entity in the Alpaca API, capturing account details and financial metrics. Enable transformation between dictionary data and AccountModel instances, facilitating data integration within the APIs ecosystem through structured data definitions. Optimize account data handling and validation within the larger repository architecture.                         |
| [account_activity_model.py](https://github.com/TexasCoding/py-alpaca-api/blob/master/src/py_alpaca_api/models/account_activity_model.py) | Provide a structured representation of account activity with attributes such as type, ID, quantities, symbol, dates, and financial details, and convert dictionary data into AccountActivityModel instances, enhancing the core functionality of data handling within the py_alpaca_api ecosystem.                                                                                                   |

</details>

<details closed><summary>src.py_alpaca_api.http</summary>

| File                                                                                                       | Summary                                                                                                                                                                                                                                                                               |
| ---                                                                                                        | ---                                                                                                                                                                                                                                                                                   |
| [requests.py](https://github.com/TexasCoding/py-alpaca-api/blob/master/src/py_alpaca_api/http/requests.py) | Implements robust HTTP request handling with retry strategy to ensure reliable communication with APIs, boasting features like customizable headers, parameters, and payloads. Integral to `py-alpaca-api` for consistent API interaction, boosting reliability and error management. |

</details>

<details closed><summary>.github.workflows</summary>

| File                                                                                                              | Summary                                                                                                                                                                                                                                                                                                                                       |
| ---                                                                                                               | ---                                                                                                                                                                                                                                                                                                                                           |
| [test-package.yaml](https://github.com/TexasCoding/py-alpaca-api/blob/master/.github/workflows/test-package.yaml) | Automates the testing process for the py-alpaca-api repository, ensuring code quality and reliability by running predefined tests. Integrates continuous integration (CI) practices into the development workflow, streamlining contributions and confirming that modifications meet project standards before merging into the main codebase. |

</details>

---

##  Getting Started

**System Requirements:**

* **Python**: `version x.y.z`

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
> ```console
> $ python main.py
> ```

###  Tests

> Run the test suite using the command below:
> ```console
> $ pytest
> ```

---

##  Project Roadmap

- [X] `► INSERT-TASK-1`
- [ ] `► INSERT-TASK-2`
- [ ] `► ...`

---

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

This project is protected under the [SELECT-A-LICENSE](https://choosealicense.com/licenses) License. For more details, refer to the [LICENSE](https://choosealicense.com/licenses/) file.

---

##  Acknowledgments

- List any resources, contributors, inspiration, etc. here.

[**Return**](#-overview)

---
