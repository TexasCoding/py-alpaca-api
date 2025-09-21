import os
import sys

# Add the source directory to the path
sys.path.insert(0, os.path.abspath("../../src"))
sys.path.insert(0, os.path.abspath("../../src/py_alpaca_api"))

project = "PyAlpacaAPI"
copyright = "MIT 2024, TexasCoding"
author = "TexasCoding"
release = "3.0.1"

extensions = [
    "myst_parser",
    "sphinx.ext.duration",
    "sphinx.ext.autosectionlabel",
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    "autoapi.extension",
    "nbsphinx",
]

# AutoAPI configuration
autoapi_type = "python"
autoapi_dirs = [os.path.abspath("../../src/py_alpaca_api")]
autoapi_options = [
    "members",
    "undoc-members",
    "show-inheritance",
    "show-module-summary",
    "special-members",
    "imported-members",
]
autoapi_ignore = ["*/tests/*", "*/__pycache__/*", "*/test_*.py", "*_test.py"]
autoapi_python_use_implicit_namespaces = True
autoapi_keep_files = True
autoapi_root = "api"
autoapi_add_toctree_entry = True

# Intersphinx configuration
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "pandas": ("https://pandas.pydata.org/pandas-docs/stable/", None),
    "numpy": ("https://numpy.org/doc/stable/", None),
}

templates_path = ["_templates"]
exclude_patterns: list[str] = []

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
