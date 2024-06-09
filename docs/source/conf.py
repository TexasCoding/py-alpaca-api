from pathlib import Path


project = "PyAlpacaAPI"
copyright = "MIT 2024, TexasCoding"
author = "TexasCoding"
release = "2.0.0"

extensions = [
    "myst_parser",
    "sphinx.ext.duration",
    "sphinx.ext.autosectionlabel",
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "autoapi.extension",
    "nbsphinx",
]
autoapi_type = "python"
autoapi_dirs = [f"{Path(__file__).parents[2]}/src"]

templates_path = ["_templates"]
exclude_patterns = []

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
