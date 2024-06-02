<p align="center">
  <img src="https://raw.githubusercontent.com/PKief/vscode-material-icon-theme/ec559a9f6bfd399b82bb44393651661b08aaf7ba/icons/folder-markdown-open.svg" width="100" alt="project-logo">
</p>
<p align="center">
    <h1 align="center">PY-ALPACA-API</h1>
</p>
<p align="center">
    <em>Empower Seamless Trading with Comprehensive API Control</em>
</p>
<p align="center">
   <img alt="GitHub Actions Workflow Status" src="https://img.shields.io/github/actions/workflow/status/TexasCoding/py-alpaca-api/.github%2Fworkflows%2Ftest-package.yml?logo=github">
	<img src="https://img.shields.io/github/license/TexasCoding/py-alpaca-api?style=flat-square&logo=opensourceinitiative&logoColor=white&color=0080ff" alt="license">
	<img src="https://img.shields.io/github/last-commit/TexasCoding/py-alpaca-api?style=flat-square&logo=git&logoColor=white&color=0080ff" alt="last-commit">
	<img src="https://img.shields.io/github/languages/top/TexasCoding/py-alpaca-api?style=flat-square&color=0080ff" alt="repo-top-language">
	<img src="https://img.shields.io/github/languages/count/TexasCoding/py-alpaca-api?style=flat-square&color=0080ff" alt="repo-language-count">
<p>
<p align="center">
		<em>Developed with the software and tools below.</em>
</p>
<p align="center">
	<img src="https://img.shields.io/badge/precommit-FAB040.svg?style=flat-square&logo=pre-commit&logoColor=black" alt="precommit">
	<img src="https://img.shields.io/badge/Poetry-60A5FA.svg?style=flat-square&logo=Poetry&logoColor=white" alt="Poetry">
	<img src="https://img.shields.io/badge/Python-3776AB.svg?style=flat-square&logo=Python&logoColor=white" alt="Python">
	<img src="https://img.shields.io/badge/GitHub%20Actions-2088FF.svg?style=flat-square&logo=GitHub-Actions&logoColor=white" alt="GitHub%20Actions">
	<img src="https://img.shields.io/badge/pandas-150458.svg?style=flat-square&logo=pandas&logoColor=white" alt="pandas">
	<img src="https://img.shields.io/badge/Pytest-0A9EDC.svg?style=flat-square&logo=Pytest&logoColor=white" alt="Pytest">
	<img src="https://img.shields.io/badge/NumPy-013243.svg?style=flat-square&logo=NumPy&logoColor=white" alt="NumPy">
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

The py-alpaca-api project offers a comprehensive interface for algorithmic trading and data retrieval using Alpacas APIs. It centralizes key functionalities such as managing accounts, assets, orders, positions, and watchlists, while also supporting market screening, historical data analysis, and efficient HTTP request handling. By integrating streamlined configurations and continuous testing workflows, py-alpaca-api ensures a reliable, robust, and consistent trading experience for developers, enhancing their financial market engagements with seamless programmatic access and transaction management. Designed for interoperability, the project fosters smooth trading operations, accommodating diverse financial strategies and requirements.

---

##  Features

|    |   Feature         | Description                                                                                                  |
|----|-------------------|--------------------------------------------------------------------------------------------------------------|
| ⚙️  | **Architecture**  | The project follows a modular architecture with isolated components for various API interactions such as `orders`, `positions`, and `market data`. The structure is organized under the `py_alpaca_api/src/` directory, reflecting single-responsibility principles. |
| 🔩 | **Code Quality**  | Code maintains high standards with tools like `black`, `isort`, and `flake8` enforcing coding style, formatting, and linting rules. The repositories structure and coding practices foster readability and maintainability.            |
| 📄 | **Documentation** | The repository includes `pyproject.toml` and `README.md` with good initial documentation. However, additional inline documentation and comprehensive examples could benefit users, enhancing understandability.                      |
| 🔌 | **Integrations**  | Integrates with Alpaca Trading and Data APIs, supporting diverse functionalities related to stock market data and account management. Uses `Github Actions` for CI/CD and includes dependencies like `requests` and `pandas`.            |
| 🧩 | **Modularity**    | Highly modular with components such as `account`, `asset`, and `order` encapsulated separately for improved reusability. Each component performs discrete tasks consistent with single-responsibility principles.                        |
| 🧪 | **Testing**       | Utilizes `pytest` and `pytest-mock` for testing, ensuring reliability with unit tests and mocking capabilities. Continuous integration is set up in `.github/workflows/test-package.yml` ensuring automated testing on commits.       |
| ⚡️  | **Performance**   | The project leverages efficient data structures provided by `pandas` for performance in data retrieval and manipulation. Network operations are facilitated by efficient HTTP request handling techniques minimizing latency.                   |
| 🛡️ | **Security**      | Secure access to Alpaca APIs is handled through customizable credential management enabling differentiating between live and paper trading. Data interactions are confinably validated and authenticated with reliable libraries.         |
| 📦 | **Dependencies**  | Relies on several key libraries like `requests`, `pandas`, `numpy`, `pytz`, and `python-dateutil` for its core operations, ensuring extensive functionality dealing with web requests, timezones, and data manipulation.                  |
| 🚀 | **Scalability**   | Designed to scale by handling increased API requests for market data and trade executions. Its modular architectural decisions enable easy upgrades and horizontal scaling capabilities that mitigate bottlenecks efficiently.               |

---

##  Repository Structure

```sh
└── py-alpaca-api/
    ├── py_alpaca_api
    │   ├── __init__.py
    │   ├── alpaca.py
    │   └── src
    │       ├── __init__.py
    │       ├── account.py
    │       ├── asset.py
    │       ├── data_classes.py
    │       ├── history.py
    │       ├── market.py
    │       ├── order.py
    │       ├── position.py
    │       ├── requests.py
    │       ├── screener.py
    │       └── watchlist.py
    └── tests
        ├── __init__.py
        ├── test_account.py
        ├── test_alpaca.py
        ├── test_asset.py
        ├── test_historical_data.py
        ├── test_market.py
        ├── test_orders.py
        ├── test_position2.py
        ├── test_positions.py
        ├── test_screener.py
        └── test_watchlist.py
```

---

##  Modules

<details closed><summary>.</summary>

| File                                                                                          | Summary                                                                                                                                                                                                                                                                                                                                                          |
| ---                                                                                           | ---                                                                                                                                                                                                                                                                                                                                                              |
| [requirements.txt](https://github.com/TexasCoding/py-alpaca-api/blob/master/requirements.txt) | Define and manage package dependencies for the py-alpaca-api project. Highlight compatibility requirements with Python versions between 3.12 and 4.0, ensuring smooth operation and interoperability of necessary packages for executing various functionalities, such as data manipulation, HTTP requests, and time zone management, within the APIs framework. |
| [pyproject.toml](https://github.com/TexasCoding/py-alpaca-api/blob/master/pyproject.toml)     | Defines the configuration for the py-alpaca-api Python package, including metadata, dependencies, and development tools. It enables streamlined building, testing, and documenting, forming the backbone for package management and ensuring consistency and standardization across the development and deployment processes within the repository.              |

</details>

<details closed><summary>py_alpaca_api</summary>

| File                                                                                          | Summary                                                                                                                                                                                                                                                                                                                                               |
| ---                                                                                           | ---                                                                                                                                                                                                                                                                                                                                                   |
| [alpaca.py](https://github.com/TexasCoding/py-alpaca-api/blob/master/py_alpaca_api/alpaca.py) | Centralizes access to Alpacas trading and data APIs, encapsulating various modules such as accounts, assets, orders, and markets. Simplifies interaction by setting up API credentials and differentiating live from paper trading environments, providing a unified interface for all functions required for algorithmic trading and data retrieval. |

</details>

<details closed><summary>py_alpaca_api.src</summary>

| File                                                                                                          | Summary                                                                                                                                                                                                                                                                                                                                                             |
| ---                                                                                                           | ---                                                                                                                                                                                                                                                                                                                                                                 |
| [watchlist.py](https://github.com/TexasCoding/py-alpaca-api/blob/master/py_alpaca_api/src/watchlist.py)       | Facilitates the management of watchlists within the Alpaca trading API, enabling functionalities such as creating, retrieving, updating, and deleting watchlists. Supports handling of assets in watchlists, including adding or removing symbols, and performing API requests to ensure appropriate data retrieval and manipulation.                               |
| [screener.py](https://github.com/TexasCoding/py-alpaca-api/blob/master/py_alpaca_api/src/screener.py)         | Provide functionality for filtering stocks including identifying gainers and losers by leveraging stock prices, volumes, trade counts, and percentage changes. Utilizes the Alpaca Data API and integrates market data to empower stock screening and investment decision-making within the repositorys architecture.                                               |
| [requests.py](https://github.com/TexasCoding/py-alpaca-api/blob/master/py_alpaca_api/src/requests.py)         | Implement a robust utility for handling HTTP requests. The utility incorporates retry logic and provides methods for GET, POST, and DELETE requests, ensuring stable communication with endpoints across the py-alpaca-api library, which supports Alpacas trading platform. This component enhances interaction reliability with the API infrastructure.           |
| [position.py](https://github.com/TexasCoding/py-alpaca-api/blob/master/py_alpaca_api/src/position.py)         | Manages and interacts with user trading positions, enabling retrieval of position data, closing specific or all positions, and converting this information into structured data formats. Integral to handling Alpaca trading account portfolios dynamically, ensuring up-to-date position reporting and trading actions within the broader API architecture.        |
| [order.py](https://github.com/TexasCoding/py-alpaca-api/blob/master/py_alpaca_api/src/order.py)               | Define functionality for managing various types of orders within the Alpaca API, including market, limit, stop, and trailing stop orders. Include methods for retrieving and canceling orders by ID or all at once, ensuring comprehensive order validation and appropriate handling of request parameters for accurate order processing within the trading system. |
| [market.py](https://github.com/TexasCoding/py-alpaca-api/blob/master/py_alpaca_api/src/market.py)             | Facilitates access to Alpacas market calendar and clock services, enabling users to retrieve market schedules and current market status efficiently. It plays a critical role in the repository by providing reliable methods to interact with Alpacas API, ensuring accurate and timely trading data.                                                              |
| [history.py](https://github.com/TexasCoding/py-alpaca-api/blob/master/py_alpaca_api/src/history.py)           | Provide historical stock data retrieval capabilities within the repositorys architecture, ensuring data validation, fetching, and preprocessing for various timeframes and conditions, enabling seamless integration and usage in broader API functionalities demonstrated through structured, efficient methods.                                                   |
| [data_classes.py](https://github.com/TexasCoding/py-alpaca-api/blob/master/py_alpaca_api/src/data_classes.py) | Data class definitions for core entities (Clock, Position, Order, Asset, Account, Watchlist) facilitate structured data representation and conversion from dictionary formats. Key utilities streamline extraction and processing of data fields, enhancing internal readability and maintainability within the overall API architecture.                           |
| [asset.py](https://github.com/TexasCoding/py-alpaca-api/blob/master/py_alpaca_api/src/asset.py)               | Facilitates retrieval and processing of asset information from the Alpaca API, converting it into structured formats for further use. Ensures adjustable querying capabilities for asset status, class, and exchange specifics, and provides an interface for detailed symbol-specific asset information.                                                           |
| [account.py](https://github.com/TexasCoding/py-alpaca-api/blob/master/py_alpaca_api/src/account.py)           | Handle Alpaca API interactions related to account management, activity retrieval, and portfolio history. Retrieve specified account activities, current account details, and portfolio history. Return structured data as pandas DataFrames for further analysis and use in financial trading operations.                                                           |

</details>

<details closed><summary>.github.workflows</summary>

| File                                                                                                            | Summary                                                                                                                                                                                                                                                                                                                   |
| ---                                                                                                             | ---                                                                                                                                                                                                                                                                                                                       |
| [test-package.yml](https://github.com/TexasCoding/py-alpaca-api/blob/master/.github/workflows/test-package.yml) | Enables continuous integration by defining the automated testing workflows for the py-alpaca-api project, ensuring code changes are properly tested before being merged. It specifies the testing environment and dependencies to maintain code quality and reliability through systematic test execution on each commit. |

</details>

---

##  Getting Started

**System Requirements:**

* **Python**: `version 3.12.3`

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
> # OR USE POETRY (Recommended)
> $ poetry install --sync
> ```

###  Usage

<h4>From <code>source</code></h4>

> Run py-alpaca-api using the command below:
> ```python
> from py_alpaca_api.alpaca import PyAlpacaApi
> 
> api = PyAlpacaApi(api_key='YOUR_API_KEY', api_secret='YOUR_API_SECRET',)
> api.order.market(symbol='AAPL', qty=1)
> ```

###  Tests

> Run the test suite using the command below:
> ```console
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

This project is protected under the [MIT]() License. For more details, refer to the [LICENSE](https://github.com/TexasCoding/py-alpaca-api/blob/master/LICENSE) file.

---

##  Acknowledgments

- List any resources, contributors, inspiration, etc. here.

[**Return**](#-overview)

---
