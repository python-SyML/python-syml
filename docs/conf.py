extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.coverage",
    "sphinx.ext.doctest",
    "sphinx.ext.extlinks",
    "sphinx.ext.ifconfig",
    "sphinx.ext.napoleon",
    "sphinx.ext.todo",
    "sphinx.ext.viewcode",
]
source_suffix = ".rst"
master_doc = "contents"
project = "SyML"
year = "2024"
author = "Killian Varescon"
copyright = f"{year}, {author}"
version = release = "0.7.10"

pygments_style = "lightbulb"
templates_path = ["source/_templates"]
extlinks = {
    "issue": ("https://github.com/KillianVar/python-syml/issues/%s", "#%s"),
    "pr": ("https://github.com/KillianVar/python-syml/pull/%s", "PR #%s"),
}

html_theme = "pydata_sphinx_theme"
html_logo = "source/img/logo.png"
html_theme_options = {"navbar_align": "left"}
html_sidebars = {"quickstart": []}
html_additional_pages = {"index": "index.html"}
html_static_path = ["source/img", "source/_static/css"]
html_css_files = ["index.css"]

html_use_smartypants = True
html_last_updated_fmt = "%b %d, %Y"
html_split_index = False
html_short_title = f"{project}-{version}"

napoleon_use_ivar = True
napoleon_use_rtype = False
napoleon_use_param = False
