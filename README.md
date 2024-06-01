<p align="center">
  <img src="https://raw.githubusercontent.com/PKief/vscode-material-icon-theme/ec559a9f6bfd399b82bb44393651661b08aaf7ba/icons/folder-markdown-open.svg" width="100" alt="project-logo">
</p>
<p align="center">
    <h1 align="center">PY-ALPACA-API</h1>
</p>
<p align="center">
    <em>Empower Trading with Seamless Alpaca API Integration</em>
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
   <img alt="Python" src="https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54">
   <img alt="Poetry" src="https://img.shields.io/badge/Poetry-%233B82F6.svg?style=for-the-badge&logo=poetry&logoColor=0B3D8D">
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

The py-alpaca-api project provides a comprehensive Python interface for seamless interaction with the Alpaca API, offering functionalities such as accessing account information, retrieving asset data, managing market details, executing orders, and analyzing stock performance. By encapsulating key components like account, asset, order, and market classes, this project facilitates efficient data retrieval, trading operations, and market analysis within the Alpaca ecosystem. Integrated with GitHub Actions for testing integrity, py-alpaca-api enhances developers capabilities in integrating Alpacas features into diverse projects, emphasizing simplicity and reliability in financial data processing and trading activities.

---

##  Features

|    |   Feature         | Description |
|----|-------------------|---------------------------------------------------------------|
| ⚙️  | **Architecture**  | The project follows a modular architecture, with key components like `account.py`, `asset.py`, `market.py`, etc., encapsulating specific functionalities. This design enhances code organization and maintainability. |
| 🔩 | **Code Quality**  | The codebase maintains high quality and follows PEP8 style conventions. It leverages tools like `black`, `flake8`, and `isort` for consistent formatting and clean code practices. |
| 📄 | **Documentation** | The project includes detailed documentation in `pyproject.toml`, outlining metadata, dependencies, and structure. Inline code comments and docstrings enhance readability and understanding for developers. |
| 🔌 | **Integrations**  | Key integrations include `requests`, `pandas`, `numpy`, etc., for data processing, HTTP requests, and financial analysis. External services like Alpaca API are seamlessly integrated for trading operations. |
| 🧩 | **Modularity**    | The codebase exhibits high modularity, allowing for code reuse and easy maintenance. Each module focuses on specific tasks, promoting separation of concerns and enhancing scalability. |
| 🧪 | **Testing**       | Testing frameworks such as `pytest` and `pytest-mock` are employed for unit testing. `pre-commit` ensures code quality checks before commits, maintaining robust test coverage. |
| ⚡️  | **Performance**   | The project emphasizes efficiency and resource optimization, ensuring swift data retrieval and processing. Performance tuning techniques are implemented to enhance speed and responsiveness. |
| 🛡️ | **Security**      | Security measures are in place for data protection and access control. Proper handling of API credentials and secure HTTP communication safeguard sensitive information. |
| 📦 | **Dependencies**  | Key dependencies include `certifi`, `requests`, `pytz`, etc., facilitating API interaction, data manipulation, and time zone handling. These libraries enhance the project's functionality. |

---

##  Repository Structure

```sh
py_alpaca_api 
├── __init__.py
├── alpaca.py
└── src
   ├── __init__.py
   ├── account.py
   ├── asset.py
   ├── data_classes.py
   ├── history.py
   ├── market.py
   ├── order.py
   ├── position.py
   ├── screener.py
   └── watchlist.py
```

---

##  Modules

<details closed><summary>.</summary>

| File                                                                                          | Summary                                                                                                                                                                                                                                      |
| ---                                                                                           | ---                                                                                                                                                                                                                                          |
| [pyproject.toml](https://github.com/TexasCoding/py-alpaca-api/blob/master/pyproject.toml)     | Defines dependencies and metadata for Python Alpaca API package.-Specifies version, description, authors, license, homepage, and repository.-Lists development, testing, and documentation dependencies.                                     |
| [requirements.txt](https://github.com/TexasCoding/py-alpaca-api/blob/master/requirements.txt) | Specifies Python package dependencies for the repository based on version compatibility. Essential libraries for API integration and data processing are outlined, ensuring proper functioning and alignment with specified Python versions. |

</details>

<details closed><summary>py_alpaca_api</summary>

| File                                                                                          | Summary                                                                                                                                                                                                                                               |
| ---                                                                                           | ---                                                                                                                                                                                                                                                   |
| [alpaca.py](https://github.com/TexasCoding/py-alpaca-api/blob/master/py_alpaca_api/alpaca.py) | Defines PyAlpacaApi class central to Alpaca API interaction. Initializes key components like account, asset, history, position, order, market, watchlist, and screener with API credentials and URLs for seamless data access and trading operations. |

</details>

<details closed><summary>.github.workflows</summary>

| File                                                                                                            | Summary                                                                                                                           |
| ---                                                                                                             | ---                                                                                                                               |
| [test-package.yml](https://github.com/TexasCoding/py-alpaca-api/blob/master/.github/workflows/test-package.yml) | Verifies Python package build and tests integrity using GitHub Actions workflow test-package.yml in the py-alpaca-api repository. |

</details>

<details closed><summary>py_alpaca_api.src</summary>

| File                                                                                                          | Summary                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| ---                                                                                                           | ---                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| [account.py](https://github.com/TexasCoding/py-alpaca-api/blob/master/py_alpaca_api/src/account.py)           | Retrieves account activities for a specific type, ensuring valid date usage. Fetches account information from Alpaca API and portfolio history data, transforming timestamps. Maintains DataFrame consistency and raises exceptions for failed requests.                                                                                                                                                                                                                        |
| [asset.py](https://github.com/TexasCoding/py-alpaca-api/blob/master/py_alpaca_api/src/asset.py)               | Retrieves asset information from Alpaca API using given parameters. Utilizes requests to fetch data, then processes and returns it in a structured format. Maps API responses to custom AssetClass objects for ease of use.                                                                                                                                                                                                                                                     |
| [data_classes.py](https://github.com/TexasCoding/py-alpaca-api/blob/master/py_alpaca_api/src/data_classes.py) | This code file, `alpaca.py`, serves as a crucial component within the `py-alpaca-api` repository. It encapsulates functionalities related to interacting with the Alpaca API, including handling account information, managing assets, and executing orders. By providing a streamlined interface for accessing Alpacas services, this module enhances the overall capability of the repository, enabling seamless integration of Alpacas features into broader projects.       |
| [history.py](https://github.com/TexasCoding/py-alpaca-api/blob/master/py_alpaca_api/src/history.py)           | Retrieves historical stock data, validates if an asset is a stock, and preprocesses data. Supports fetching data based on symbol, timeframe, and date range. Ensures data integrity and format consistency for analysis within the parent repositorys Alpaca API integration.                                                                                                                                                                                                   |
| [market.py](https://github.com/TexasCoding/py-alpaca-api/blob/master/py_alpaca_api/src/market.py)             | Implements Market class with methods for retrieving calendar data and market clock status from Alpaca API. Provides functionalities to fetch, process, and return market-related information in a structured format.                                                                                                                                                                                                                                                            |
| [order.py](https://github.com/TexasCoding/py-alpaca-api/blob/master/py_alpaca_api/src/order.py)               | Watchlist.py`The `watchlist.py` file in the `py-alpaca-api` repository is crucial for managing and tracking user-defined watchlists of assets within the Alpaca trading platform. It enables users to create, update, and retrieve custom watchlists, providing a streamlined approach to monitor specific assets of interest. By utilizing this module, users can easily curate and monitor their preferred assets, enhancing their trading experience on the Alpaca platform. |
| [position.py](https://github.com/TexasCoding/py-alpaca-api/blob/master/py_alpaca_api/src/position.py)         | Retrieves, processes, and manages Alpaca account positions, providing data in DataFrame format, individual position details, and options to close positions individually or all at once. Maintains accuracy and consistency in position-related actions within the Alpaca API ecosystem.                                                                                                                                                                                        |
| [screener.py](https://github.com/TexasCoding/py-alpaca-api/blob/master/py_alpaca_api/src/screener.py)         | Analyzes stock winners and losers by filtering data based on preset criteria. Retrieves and ranks stock performances for the previous day, with options to customize filter thresholds. Requires asset and market context for accurate analysis.                                                                                                                                                                                                                                |
| [watchlist.py](https://github.com/TexasCoding/py-alpaca-api/blob/master/py_alpaca_api/src/watchlist.py)       | Retrieval, creation, updating, deletion, and asset management. Encapsulates request handling, response processing, and error management. conforms to the parent repositorys architecture by structuring functionality into distinct modules.                                                                                                                                                                                                                                    |

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
