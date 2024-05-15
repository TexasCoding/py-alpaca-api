<p align="center">
  <img src="https://raw.githubusercontent.com/PKief/vscode-material-icon-theme/ec559a9f6bfd399b82bb44393651661b08aaf7ba/icons/folder-markdown-open.svg" width="100" alt="project-logo">
</p>
<p align="center">
    <h1 align="center">PY-ALPACA-API</h1>
</p>
<p align="center">
    <em>Empowering traders with precision and control.</em>
</p>
<p align="center">
<img alt="GitHub Actions Workflow Status" src="https://img.shields.io/github/actions/workflow/status/TexasCoding/py-alpaca-api/.github%2Fworkflows%2Ftest-package.yml?logo=github">
	<img src="https://img.shields.io/github/license/TexasCoding/py-alpaca-api?style=default&logo=opensourceinitiative&logoColor=white&color=0080ff" alt="license">
	<img src="https://img.shields.io/github/last-commit/TexasCoding/py-alpaca-api?style=default&logo=git&logoColor=white&color=0080ff" alt="last-commit">
	<img src="https://img.shields.io/github/languages/top/TexasCoding/py-alpaca-api?style=default&color=0080ff" alt="repo-top-language">
	<img src="https://img.shields.io/github/languages/count/TexasCoding/py-alpaca-api?style=default&color=0080ff" alt="repo-language-count">
<p>
<p align="center">
	<!-- default option, no dependency badges. -->
</p>

<br><!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary><br>

- [Overview](#overview)
- [Features](#features)
- [Repository Structure](#repository-structure)
- [Modules](#modules)
- [Getting Started](#getting-started)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Tests](#tests)
- [Project Roadmap](#project-roadmap)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)
</details>
<hr>

##  Overview

Py-alpaca-api is a robust Python library facilitating seamless interaction with the Alpaca Markets REST API. It empowers developers to manage accounts, assets, market data, orders, and positions efficiently. By leveraging key modules like position, order, and history, users can access historical market data, analyze trends, and make informed trading decisions. With a focus on modularity and ease of use, this open-source project delivers essential functionalities for enhancing trading platforms and enabling strategic decision-making within the financial realm.

---

##  Features

|    |   Feature         | Description |
|----|-------------------|---------------------------------------------------------------|
| ⚙️  | **Architecture**  | The project follows a modular architecture design, allowing for separate components such as Account, Asset, Market, and Order handling. It initializes with API Key, Secret, and Paper Trading options. |
| 🔩 | **Code Quality**  | The codebase maintains good code quality with consistent style and formatting. It integrates tools like Black for code formatting and Flake8 for linting. |
| 📄 | **Documentation** | The project has extensive documentation covering various modules such as Account, Asset, and History. It provides detailed explanations of methods, parameters, and usage instructions. |
| 🔌 | **Integrations**  | Key integrations include requests for HTTP requests, pandas for data manipulation, and pytest for testing. It also leverages Alpaca Markets REST API for financial data interaction. |
| 🧩 | **Modularity**    | The codebase is highly modular, with separate modules for different functionalities like Position, Order, and Market data retrieval. This promotes code reusability and maintainability. |
| 🧪 | **Testing**       | The project utilizes pytest for unit testing and requests-mock for mocking HTTP requests. GitHub Actions automate testing workflows for ensuring code integrity. |
| ⚡️  | **Performance**   | The codebase efficiently handles data retrieval and processing, ensuring smooth interaction with the Alpaca API endpoints. Performance optimizations are achieved through streamlined historical data retrieval and market status updates. |
| 🛡️ | **Security**      | Security measures include handling authentication securely through API Key and Secret. The project emphasizes data protection and access control by managing account and asset information securely. |
| 📦 | **Dependencies**  | Key external libraries and dependencies include requests, pandas, numpy for data manipulation, and pytest for testing. Additional tools like pre-commit and poetry enhance development workflows. |

---

##  Repository Structure

```sh
└── py-alpaca-api/
    ├── .github
    │   ├── ISSUE_TEMPLATE
    │   │   ├── bug_report.md
    │   │   ├── custom.md
    │   │   └── feature_request.md
    │   └── workflows
    │       └── test-package.yml
    ├── CODE_OF_CONDUCT.md
    ├── CONTRIBUTING.md
    ├── LICENSE
    ├── README.md
    ├── SECURITY.md
    ├── docs
    │   ├── Makefile
    │   ├── make.bat
    │   ├── rtd_requirements.txt
    │   └── source
    │       ├── conf.py
    │       ├── index.md
    │       └── notebooks
    ├── poetry.lock
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
    │       └── position.py
    ├── pyproject.toml
    ├── requirements.txt
    └── tests
        ├── __init__.py
        ├── test_account.py
        ├── test_alpaca.py
        ├── test_asset.py
        ├── test_historical_data.py
        ├── test_market.py
        ├── test_orders.py
        └── test_positions.py
```

---

##  Modules

<details closed><summary>.</summary>

| File                                                                                          | Summary                                                                                                                                                                                                                |
| ---                                                                                           | ---                                                                                                                                                                                                                    |
| [requirements.txt](https://github.com/TexasCoding/py-alpaca-api/blob/master/requirements.txt) | Ensures Python dependencies are managed for the repository, restricting versions to specific ranges. Facilitates compatibility and stable functioning by defining required packages for the Alpaca API project.        |
| [pyproject.toml](https://github.com/TexasCoding/py-alpaca-api/blob/master/pyproject.toml)     | Enables interaction with Alpaca Markets REST API. Manages account, asset, market data, orders, and positions. Supports Python 3.12, pandas, requests, and numpy. Integrates testing, linting, and documentation tools. |

</details>

<details closed><summary>py_alpaca_api</summary>

| File                                                                                          | Summary                                                                                                                                                                                                                                         |
| ---                                                                                           | ---                                                                                                                                                                                                                                             |
| [alpaca.py](https://github.com/TexasCoding/py-alpaca-api/blob/master/py_alpaca_api/alpaca.py) | Defines PyAlpacaApi class, initializing with API Key, Secret, and Paper Trading option. Sets URLs based on trading mode and initializes Account, Asset, History, Position, Order, and Market objects for interacting with Alpaca API endpoints. |

</details>

<details closed><summary>py_alpaca_api.src</summary>

| File                                                                                                          | Summary                                                                                                                                                                                                                                                                                                                                                                                                          |
| ---                                                                                                           | ---                                                                                                                                                                                                                                                                                                                                                                                                              |
| [position.py](https://github.com/TexasCoding/py-alpaca-api/blob/master/py_alpaca_api/src/position.py)         | Retrieves and processes account positions from Alpaca API. Includes functions to get all positions as a DataFrame, retrieve a specific position, close all positions, and close a specific position by symbol or ID.                                                                                                                                                                                             |
| [order.py](https://github.com/TexasCoding/py-alpaca-api/blob/master/py_alpaca_api/src/order.py)               | SummaryThis code file, `history.py`, plays a crucial role in the `py-alpaca-api` repository by providing essential functionalities related to historical market data retrieval and analysis within the Alpaca API ecosystem. By leveraging this module, developers can efficiently access and process historical data for strategic decision-making, enhancing the overall capabilities of the trading platform. |
| [market.py](https://github.com/TexasCoding/py-alpaca-api/blob/master/py_alpaca_api/src/market.py)             | Retrieves market clock status via HTTP GET request, handling successful and failed responses. Integrated with Alpaca API for real-time market data.                                                                                                                                                                                                                                                              |
| [history.py](https://github.com/TexasCoding/py-alpaca-api/blob/master/py_alpaca_api/src/history.py)           | Retrieve historical stock data from Alpaca API based on specified parameters. Validates asset information, handles timeframe conversions, sends API request with required parameters, and converts response to a structured DataFrame. Ensures error handling for data availability, asset validation, and API response.                                                                                         |
| [data_classes.py](https://github.com/TexasCoding/py-alpaca-api/blob/master/py_alpaca_api/src/data_classes.py) | This code file, `data_classes.py`, plays a critical role in defining the data structures and classes essential for modeling various financial assets and market data within the `py-alpaca-api` repository. By encapsulating the core data elements and relationships, this module sets the foundation for consistent and organized representation of data throughout the project.                               |
| [asset.py](https://github.com/TexasCoding/py-alpaca-api/blob/master/py_alpaca_api/src/asset.py)               | Retrieves asset information from the Alpaca API based on the provided symbol. Parses the response into an AssetClass object containing essential details like ID, exchange, status, and more. Signals errors if retrieval fails.                                                                                                                                                                                 |
| [account.py](https://github.com/TexasCoding/py-alpaca-api/blob/master/py_alpaca_api/src/account.py)           | Retrieves account information from Alpaca API, mapping it to an AccountClass object in JSON format. Handles successful and failed responses gracefully within the repositorys modular architecture.                                                                                                                                                                                                              |

</details>

<details closed><summary>.github.workflows</summary>

| File                                                                                                            | Summary                                                                                                                                                                                                                                              |
| ---                                                                                                             | ---                                                                                                                                                                                                                                                  |
| [test-package.yml](https://github.com/TexasCoding/py-alpaca-api/blob/master/.github/workflows/test-package.yml) | Tests package dependencies and ensures code integrity through automated workflows. Orchestrates testing for account, asset, historical data, market, orders, and positions modules. Facilitates CI/CD integration for robust repository maintenance. |

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
> $ poetry install
> ```

###  Usage

<h4>From <code>source</code></h4>

> Run py-alpaca-api using the command below:
> ```python
> from py_alpaca_api import PyAlpacaApi
> api = PyAlpacaApi(api_key='YOUR_KEY', api_secret='YOUR_SECRET', api_paper=True)
> positions = api.position.get_all()
> orders = api.order.get_all()
> # Create new order
> order = api.order.market(symbol='AAPL', qty=1.034, side='buy')
> ```

###  Tests

> Run the test suite using the command below:
> ```console
> $ pytest
> ```

---

##  Project Roadmap

- [X] `► Create functionality for all Alpaca API resources`

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
