import importlib.metadata

# ---------------------------------------------------------------------------
# Project
# ---------------------------------------------------------------------------

project   = "ttkbootstrap"
author    = "Israel Dryer"
copyright = f"2026, {author}"

release = importlib.metadata.version("ttkbootstrap")
version = ".".join(release.split(".")[:2])

# ---------------------------------------------------------------------------
# Extensions
# ---------------------------------------------------------------------------

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.intersphinx",
    "sphinx.ext.autosummary",
    "sphinx_design",
    "sphinx_copybutton",
    "myst_parser",
]

# ---------------------------------------------------------------------------
# Autodoc
# ---------------------------------------------------------------------------
# ttkbootstrap documents constructor parameters in each widget's ``__init__``
# docstring (napoleon Google ``Parameters:`` blocks), NOT in the class docstring
# or as attribute docstrings. ``autoclass_content = "both"`` concatenates the
# class docstring with the ``__init__`` docstring so those parameter tables
# render on the class page. (This is the one place the ttkbootstrap docstring
# convention diverges from bootstack's, which documents params on the class.)
autoclass_content = "both"

# Render autodoc objects with bare names (``class Validation``, not
# ``class ttkbootstrap.Validation``) to match the hand-written reference pages,
# which use unqualified names throughout.
add_module_names = False

autodoc_member_order        = "groupwise"
autodoc_typehints           = "description"
autodoc_typehints_format    = "short"
python_use_unqualified_type_names = True
autodoc_default_options     = {
    "members":          True,
    "undoc-members":    False,
    "show-inheritance": True,
    # Never leak the ~200 inherited tkinter/ttk widget members into our pages —
    # docs-design §5c: API pages document only what ttkbootstrap authors.
    "inherited-members": False,
}

autosummary_generate = True

# Single backticks in docstrings render as inline code (the project convention)
# and, unlike the default interpreted-text role, are colon-safe (e.g. `h:mm`).
default_role = "code"

# ---------------------------------------------------------------------------
# Napoleon (Google-style docstrings)
# ---------------------------------------------------------------------------

napoleon_google_docstring       = True
napoleon_numpy_docstring        = False
napoleon_include_init_with_doc  = False
napoleon_use_param              = True
napoleon_use_rtype              = False
napoleon_attr_annotations       = True

# ---------------------------------------------------------------------------
# Intersphinx
# ---------------------------------------------------------------------------

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
}

# ---------------------------------------------------------------------------
# HTML / PyData theme
# ---------------------------------------------------------------------------

html_theme = "pydata_sphinx_theme"

html_theme_options = {
    # Permanent banner pointing app-builders to the sibling framework.
    "announcement": (
        "Building a whole app, not just theming one? "
        '<a href="https://bootstack.org">Try bootstack →</a>'
    ),
    "github_url": "https://github.com/israel-dryer/ttkbootstrap",
    "logo": {
        "image_light": "_static/ttkbootstrap-wordmark-light.svg",
        "image_dark": "_static/ttkbootstrap-wordmark-dark.svg",
        "alt_text": "ttkbootstrap",
    },
    "navbar_start": ["navbar-logo"],
    "navbar_center": ["navbar-nav"],
    "navbar_end": ["navbar-icon-links", "theme-switcher"],
    "secondary_sidebar_items": ["page-toc"],
    "navigation_with_keys": True,
    "show_nav_level": 1,
}

html_static_path = ["_static"]
templates_path   = ["_templates"]
html_css_files   = ["custom.css"]
html_title       = "ttkbootstrap"
html_short_title = "ttkbootstrap"

# Browser-tab icon — the packaged square brand mark (blue-circle feather),
# copied from src/ttkbootstrap/assets/app_icons/ttkbootstrap.ico (multi-res 16..256).
html_favicon = "_static/favicon.ico"

# Hide reST source exposure — the docs are the interface, not the page source.
html_show_sourcelink = False
html_copy_source     = False

# `_generated/` holds committed rST *include partials* emitted by the offline
# tools/ generators (e.g. the bootstyle reference table). They are folded into
# real pages via `.. include::`, so they must not be treated as standalone
# documents (that would raise a "not in any toctree" warning under -W).
exclude_patterns = [
    "_build",
    "_generated",
    "shared",
    # Include-only styling partials pulled into each widget's API page; not
    # standalone documents.
    "reference/api/_style",
    # Include-only window-method partials shared by the App/Toplevel/Tk pages.
    "reference/windows/_wm-1.rst",
    "reference/windows/_wm-2.rst",
    "reference/windows/_theme.rst",
    "reference/windows/_lifecycle.rst",
    "reference/windows/_positioning.rst",
    "Thumbs.db",
    ".DS_Store",
]

# ---------------------------------------------------------------------------
# Autodoc mock imports (Pillow is the only runtime dep; keep as a backstop so a
# minimal RTD builder still imports ttkbootstrap for autodoc).
# ---------------------------------------------------------------------------

autodoc_mock_imports = []

# ---------------------------------------------------------------------------
# Markdown code-fence shim
# ---------------------------------------------------------------------------
# ttkbootstrap's docstrings were authored for mkdocstrings (Markdown): their
# ``Examples:`` blocks use Markdown triple-backtick fences (```python … ```),
# which napoleon/reStructuredText does not understand and renders as broken
# inline literals. Rather than rewrite every docstring, translate the fences to
# ``.. code-block::`` at build time — so the source docstrings feed autodoc
# unchanged (the docs-design goal) while rendering correctly under Sphinx.


def _convert_markdown_fences(app, what, name, obj, options, lines):
    out = []
    in_fence = False
    base_indent = 0
    for line in lines:
        stripped = line.lstrip()
        if stripped.startswith("```"):
            if not in_fence:
                lang = stripped[3:].strip() or "python"
                indent = line[: len(line) - len(stripped)]
                base_indent = len(indent)
                out.append(f"{indent}.. code-block:: {lang}")
                out.append("")
                in_fence = True
            else:
                in_fence = False
                out.append("")
            continue
        if in_fence:
            inner = line[base_indent:] if len(line) >= base_indent else line.lstrip()
            out.append((" " * base_indent + "   " + inner) if inner.strip() else "")
        else:
            out.append(line)
    lines[:] = out


def setup(app):
    # Run after napoleon (default priority 500) has expanded the Google
    # sections, so the fences are converted in the final docstring text.
    app.connect("autodoc-process-docstring", _convert_markdown_fences, priority=600)
