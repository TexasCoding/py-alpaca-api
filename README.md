<p align="center">
  <img src="https://raw.githubusercontent.com/PKief/vscode-material-icon-theme/ec559a9f6bfd399b82bb44393651661b08aaf7ba/icons/folder-markdown-open.svg" width="100" alt="project-logo">
</p>
<p align="center">
    <h1 align="center">PY-ALPACA-API</h1>
</p>
<p align="center">
    <em>Unlock Alpacas Power with Seamless API Integration"</em>
</p>
<p align="center">
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

The py-alpaca-api project is a Python library that simplifies interaction with the Alpaca API. It provides a robust interface, encapsulated in the `PyAlpacaApi` class, enabling developers to access Alpaca Market API trading functionalities effortlessly. By utilizing data classes for orders, assets, and accounts, the project abstracts away complexities, enhancing flexibility in processing API responses. With clear metadata management through Poetry, this project serves as a valuable tool for those looking to integrate Alpaca trading capabilities seamlessly into their applications.

This project is still in development. New functionality will be added and updated daily. Hopefully this project will help make communicating with Alpaca Markets API, much easier for some. Any input or help would be appreciated.

---

##  Features

|    |   Feature         | Description |
|----|-------------------|---------------------------------------------------------------|
| ⚙️  | **Architecture**  | Designed with a clear separation of concerns, utilizing data classes for enhanced abstraction and maintainability. Follows a modular approach to interact with the Alpaca API efficiently. |
| 🔩 | **Code Quality**  | Maintains high code quality standards with consistent use of Python best practices. Codebase is well-formatted, follows PEP8 guidelines, and includes automated code formatting and linting with tools like black, flake8, and isort. |
| 📄 | **Documentation** | Provides thorough documentation with a focus on API usage, setup instructions, and data class definitions. Utilizes Sphinx for generating documentation to support developers in understanding and integrating the project. |
| 🔌 | **Integrations**  | Relies on key external dependencies such as requests for handling HTTP requests and numpy for numerical computations. Also integrates with pre-commit for code quality checks and pytest for testing. |
| 🧩 | **Modularity**    | Emphasizes modularity and reusability with well-defined data classes that abstract API responses. Offers developers flexibility in handling different aspects of Alpaca trading functionalities. |
| 🧪 | **Testing**       | Utilizes pytest as the primary testing framework along with requests-mock for mocking API requests. Ensures reliable testing for validating the behavior of the PyAlpacaApi class. |
| ⚡️  | **Performance**   | Demonstrates efficiency in API communication and data processing. Optimizes speed by handling requests and responses effectively, contributing to overall performance. |
| 🛡️ | **Security**      | Implements secure data handling by requiring Alpaca API Key and Secret for authentication. Employs measures to protect sensitive information and control access to the Alpaca trading functionalities. |
| 📦 | **Dependencies**  | Depends on various libraries including requests, pandas, and numpy for API interactions, data processing, and numerical computations. Managed efficiently using Poetry for dependency management. |
| 🚀 | **Scalability**   | Shows potential for scalability with its modular design and efficient data processing. Capable of handling increased traffic and load by abstracting API interactions and ensuring maintainability. |

---

##  Repository Structure

```sh
└── py-alpaca-api/
    ├── .github
    │   └── ISSUE_TEMPLATE
    ├── CODE_OF_CONDUCT.md
    ├── LICENSE
    ├── README.md
    ├── SECURITY.md
    ├── poetry.lock
    ├── py_alpaca_api
    │   ├── __init__.py
    │   ├── alpaca.py
    │   └── src
    ├── pyproject.toml
    └── tests
        ├── __init__.py
        └── test_alpaca.py
```

---

##  Modules

<details closed><summary>.</summary>

| File                                                                                      | Summary                                                                                                                                                                                                                                                 |
| ---                                                                                       | ---                                                                                                                                                                                                                                                     |
| [pyproject.toml](https://github.com/TexasCoding/py-alpaca-api/blob/master/pyproject.toml) | Defines metadata and dependencies for py-alpaca-api. Manages project details, such as name, version, description, homepage, repository, and dependencies like pandas, requests, and numpy. Organizes development and testing dependencies using Poetry. |

</details>

<details closed><summary>py_alpaca_api</summary>

| File                                                                                          | Summary                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| ---                                                                                           | ---                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| [alpaca.py](https://github.com/TexasCoding/py-alpaca-api/blob/master/py_alpaca_api/alpaca.py) | The `alpaca.py` file in the `py-alpaca-api` repository contains a class called `PyAlpacaApi`, designed to interact with the Alpaca API. This class facilitates communication by handling API requests and responses, leveraging data classes for account, asset, and order information. The constructor requires the Alpaca API Key and Secret, with an option to specify the usage of the Alpaca Paper Trading API. This component serves as a fundamental interface for developers to access and manage Alpaca trading functionalities within the broader project architecture. |

</details>

<details closed><summary>py_alpaca_api.src</summary>

| File                                                                                                          | Summary                                                                                                                                                                            |
| ---                                                                                                           | ---                                                                                                                                                                                |
| [data_classes.py](https://github.com/TexasCoding/py-alpaca-api/blob/master/py_alpaca_api/src/data_classes.py) | Defines data classes for Orders, Assets, and Accounts to map JSON data to Python objects. Abstracts data processing from API responses, enhancing flexibility and maintainability. |

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
> Recommended way is to use poetry, to install all dependencies including dev
> ```console
> $ poetry install
> ```
> Using pip, this does not include -dev dependencies:
> ```console
> $ pip install -r requirements.txt
> ```

###  Usage

<h4>Include PyAlpacaAPI In Your App</h4>

> ```python
> from py_alpaca_api.alpaca import PyAlpacaApi
>
> api_key = 'your_api_key'
> api_secret = 'your_api_secret'
>
> alpaca = PyAlpacaApi(api_key=api_key, api_secret=api_secret, api_paper=True)
>
> asset = alpaca.get_asset('AAPL')
>
> print(asset)
> ```

###  Tests

> Run the test suite using the command below:
> ```console
> $ pytest
> ```

---

##  Project Roadmap

- [X] `► Adding all functionality from Alpaca's API`

---

##  Contributing

Contributions are welcome! Here are several ways you can contribute:

- **[Report Issues](https://github.com/TexasCoding/py-alpaca-api/issues)**: Submit bugs found or log feature requests for the `py-alpaca-api` project.
- **[Submit Pull Requests](https://github.com/TexasCoding/py-alpaca-api/blob/master/CONTRIBUTING.md)**: Review open PRs, and submit your own PRs.
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

This project is protected under the [MIT](https://choosealicense.com/licenses/mit/) License. For more details, refer to the [LICENSE](https://github.com/TexasCoding/py-alpaca-api/blob/master/LICENSE) file.

---

##  Acknowledgments



[**Return**](#-overview)

---
