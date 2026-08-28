import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from fastapi_keycloak import __version__

project = "FastAPI Keycloak Integration"
copyright = "fastapi-keycloak contributors"
author = "fastapi-keycloak contributors"
release = __version__

extensions = [
    "myst_parser",
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    "sphinx_copybutton",
]
myst_enable_extensions = ["colon_fence", "deflist"]
source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}
root_doc = "index"

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

html_theme = "furo"
html_static_path = ["_static"]
html_title = project
html_favicon = "_static/favicon.svg"
html_logo = "_static/logo.png"

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
}

autodoc_member_order = "bysource"
napoleon_google_docstring = True
napoleon_numpy_docstring = False
