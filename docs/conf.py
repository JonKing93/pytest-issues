# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html
import tomllib
from pathlib import Path

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "pytest-issues"
author = "Jonathan King"
copyright = f"%Y, {author}"

# Parse the release string from pyproject.toml
_pyproject = Path(__file__).parents[1] / "pyproject.toml"
with open(_pyproject, "rb") as file:
    _pyproject = tomllib.load(file)
release = _pyproject["project"]["version"]
version = ".".join(release.split(".")[:-1])


# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ["sphinx_design", "sphinx_copybutton"]
highlight_language = "python"
pygments_style = "sphinx"


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_copy_source = False
html_theme = "furo"
html_title = f"{project} {release}"
