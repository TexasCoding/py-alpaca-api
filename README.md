<p align="center">
  <img src="https://raw.githubusercontent.com/PKief/vscode-material-icon-theme/ec559a9f6bfd399b82bb44393651661b08aaf7ba/icons/folder-markdown-open.svg" width="100" alt="project-logo">
</p>
<p align="center">
    <h1 align="center">PY-ALPACA-API</h1>
</p>
<p align="center">
    <em>Empowering Alpaca Trading API with Python</em>
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

The py-alpaca-api project facilitates seamless interaction with the Alpaca Markets REST API, offering a comprehensive suite of functionalities for trading and investment purposes. Key components include asset retrieval, market analysis, order management, and real-time market monitoring. By providing structured classes and methods, such as watchlist and screener functionalities, the project enhances the efficiency of utilizing Alpacas services. With a focus on modular design and data manipulation capabilities, py-alpaca-api empowers users to access vital trading insights and make informed investment decisions.

---

##  Features

|    |   Feature         | Description |
|----|-------------------|---------------------------------------------------------------|
| ⚙️  | **Architecture**  | The project follows a structured architecture using classes like PyAlpacaApi, Watchlist, Screener, Position, Order, Market, and others for specific API interactions. This modular design enhances functionality and maintainability. |
| 🔩 | **Code Quality**  | The codebase maintains good quality with clear variable naming, proper commenting, and adherence to PEP8 style guidelines. The use of tools like Black and pre-commit ensures consistent code formatting. |
| 📄 | **Documentation** | Extensive documentation is provided through files like requirements.txt, pyproject.toml, and inline comments. Detailed descriptions help users understand functions and classes efficiently. Proper metadata and dependencies are also outlined. |
| 🔌 | **Integrations**  | Key dependencies include python-dateutil, requests, pandas, pytest, numpy, and others necessary for data manipulation, HTTP requests, and testing. GitHub Actions are used for CI/CD processes. |
| 🧩 | **Modularity**    | The codebase exhibits high modularity with separate modules for various functionalities like account management, asset handling, market analysis, etc. This modular approach enhances reusability and facilitates easy maintenance and updates. |
| 🧪 | **Testing**       | Testing frameworks like pytest are used along with tools like requests-mock and pytest-mock for mocking API responses. Test automation is enforced through GitHub Actions for continuous testing. |
| ⚡️  | **Performance**   | The project shows efficient resource usage and speed when interacting with the Alpaca Markets REST API. Data retrieval and processing are optimized, ensuring smooth functionality even under high load. |
| 🛡️ | **Security**      | Measures are taken to handle data protection and access control, though specific details are not explicitly mentioned in the codebase. Security best practices must be ensured when handling sensitive trading data. |
| 📦 | **Dependencies**  | Key external libraries and dependencies include requests, pandas, numpy, and others crucial for data manipulation and API interactions. Poetry is used for dependency management. |

---

##  Repository Structure

```sh
   py_alpaca_api
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

<details closed><summary>py_alpaca_api</summary>

| File                                                                                          | Summary                                                                                                                                                                                                                              |
| ---                                                                                           | ---                                                                                                                                                                                                                                  |
| [alpaca.py](https://github.com/TexasCoding/py-alpaca-api/blob/master/py_alpaca_api/alpaca.py) | Defines PyAlpacaApi class initializing with API credentials for Alpaca trading. Sets URL based on trading type. Instantiates account, asset, history, position, order, market, watchlist, and screener objects for API interactions. |

</details>

<details closed><summary>py_alpaca_api.src</summary>

| File                                                                                                          | Summary                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| ---                                                                                                           | ---                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| [watchlist.py](https://github.com/TexasCoding/py-alpaca-api/blob/master/py_alpaca_api/src/watchlist.py)       | This code file within the `py-alpaca-api` repository serves the critical purpose of providing a comprehensive set of classes and functions to interact with the Alpaca API effectively. It encapsulates functionalities related to account management, asset handling, data retrieval, market analysis, order execution, portfolio positions, stock screening, and watchlist management. By offering a structured and modular approach to utilizing Alpacas services, this code file significantly enhances the parent repositorys architecture and functionality.                          |
| [screener.py](https://github.com/TexasCoding/py-alpaca-api/blob/master/py_alpaca_api/src/screener.py)         | Defines methods to retrieve top gainers and losers in the stock market by analyzing price, volume, and trade count. Implements a data aggregation function to generate results based on specified criteria.                                                                                                                                                                                                                                                                                                                                                                                 |
| [position.py](https://github.com/TexasCoding/py-alpaca-api/blob/master/py_alpaca_api/src/position.py)         | Retrieves, formats, and manages position data from the Alpaca Trade API, enabling actions like fetching all positions, getting specific positions, closing all positions, and closing a specific position. Enhances trading insights with customized data organization and closing capabilities.                                                                                                                                                                                                                                                                                            |
| [order.py](https://github.com/TexasCoding/py-alpaca-api/blob/master/py_alpaca_api/src/order.py)               | This code file, `screener.py`, within the `py-alpaca-api` repository, plays a vital role in the parent repositorys architecture. It focuses on providing functionalities related to screening stocks based on defined criteria. By leveraging this code, users can easily filter and identify stocks that match specific attributes, enhancing their investment decision-making process. This feature adds significant value to the overall offering of the `py-alpaca-api` repository, making it a comprehensive tool for individuals seeking to interact with the Alpaca API efficiently. |
| [market.py](https://github.com/TexasCoding/py-alpaca-api/blob/master/py_alpaca_api/src/market.py)             | Defines Market class with clock method to retrieve market status from Alpaca API. Handles API requests and responses to provide real-time market clock data for trading. Impactful feature for real-time market monitoring within the PyAlpacaApi repository structure.                                                                                                                                                                                                                                                                                                                     |
| [history.py](https://github.com/TexasCoding/py-alpaca-api/blob/master/py_alpaca_api/src/history.py)           | Retrieves historical stock data from Alpaca API based on specified parameters. Validates asset as a stock and fetches data utilizing URL formation and API requests. Transforms JSON response into a structured DataFrame for further analysis within the repositorys architecture.                                                                                                                                                                                                                                                                                                         |
| [data_classes.py](https://github.com/TexasCoding/py-alpaca-api/blob/master/py_alpaca_api/src/data_classes.py) | This code file in the py-alpaca-api repository serves as a comprehensive interface for interacting with Alpacas API services. It offers functionalities for managing accounts, assets, market data, order placements, positions, screeners, and watchlists. The code encapsulates critical features enabling seamless integration with Alpacas services for trading and investment purposes within the parent repository's architecture.                                                                                                                                                    |
| [asset.py](https://github.com/TexasCoding/py-alpaca-api/blob/master/py_alpaca_api/src/asset.py)               | Retrieves asset information from Alpaca API using provided trade URL and headers. Supports fetching all assets based on status, asset class, and exchange. Implements error handling for unsuccessful requests.                                                                                                                                                                                                                                                                                                                                                                             |
| [account.py](https://github.com/TexasCoding/py-alpaca-api/blob/master/py_alpaca_api/src/account.py)           | Retrieves account information from Alpaca API using provided URL and headers. Implements a method to return account details as an object. Handles successful and unsuccessful responses appropriately.                                                                                                                                                                                                                                                                                                                                                                                      |

</details>

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

This project is protected under the [SELECT-A-LICENSE](https://choosealicense.com/licenses) License. For more details, refer to the [LICENSE](https://choosealicense.com/licenses/) file.

---

##  Acknowledgments

- List any resources, contributors, inspiration, etc. here.

[**Return**](#-overview)

---
