# -*- coding: utf-8 -*-
#
# Configuration file for the Sphinx documentation builder.
#
# This file does only contain a selection of the most common options. For a
# full list see the documentation:
# http://www.sphinx-doc.org/en/master/config

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))

import git
import github
import requests

import io
import os
import subprocess
import sys
import tempfile
import zipfile

on_rtd = os.environ.get('READTHEDOCS') == 'True'

# -- General configuration ---------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#
# needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
sys.path.insert(1, os.path.abspath(os.path.dirname(__file__)))
extensions = [
    'sphinx.ext.napoleon',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.doctest',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'sphinx.ext.coverage',
    'sphinx.ext.mathjax',
    'sphinx.ext.ifconfig',
    'sphinx.ext.viewcode',
    'sphinx.ext.githubpages',
    'sphinx_autodoc_typehints',  # Automatically document param types (less noise in class signature)
    'recommonmark',
    'nbsphinx',
    'pybind11_docstrings',
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
# source_suffix = ['.rst', '.md']
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# -- Project information -----------------------------------------------------

project = 'EGTtools'
copyright = '2019-2021, Elias Fernández'
author = 'Elias Fernández'

if on_rtd:
    rtd_version = os.environ.get('READTHEDOCS_VERSION')
    branch = 'master' if rtd_version == 'latest' else rtd_version

    github_token = os.environ['GITHUB_TOKEN']
    head_sha = git.Repo(search_parent_directories=True).head.commit.hexsha
    g = github.Github()
    runs = g.get_repo('Socrats/EGTTools').get_workflow("wheels.yml").get_runs(branch=branch)
    artifacts_url = next(r for r in runs if r.head_sha == head_sha).artifacts_url

    archive_download_url = \
        next(artifact for artifact in requests.get(artifacts_url).json()['artifacts'] if
             artifact['name'] == 'rtd-wheel')[
            'archive_download_url']
    artifact_bin = io.BytesIO(
        requests.get(archive_download_url, headers={'Authorization': f'token {github_token}'}, stream=True).content)

    with zipfile.ZipFile(artifact_bin) as zf, tempfile.TemporaryDirectory() as tmpdir:
        assert len(zf.namelist()) == 1
        zf.extractall(tmpdir)
        subprocess.check_call(
            [sys.executable, '-m', 'pip', 'install', '--force-reinstall', tmpdir + '/' + zf.namelist()[0]])
html_css_files = ["readthedocs-custom.css"]  # Override some CSS settings
import egttools

# The short X.Y version
version = '.'.join(egttools.__version__.split('.')[:2])
# The full version, including alpha/beta/rc tags
release = egttools.__version__

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = 'en'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store', '**.ipynb_checkpoints']

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = True

# enable imported members
autosummary_imported_members = True
# autosummary_implicit_namespaces = True
# Autodoc configuration
autodoc_member_order = 'groupwise'

# Intersphinx configuration
intersphinx_mapping = {'python': ('https://docs.python.org/3', None),
                       'numpy': ('https://numpy.org/doc/stable/', None),
                       'scipy': ('https://numpy.org/doc/stable/', None),
                       'networkx': ('https://networkx.org/documentation/stable/', None)
                       }

autosummary_generate = True  # Turn on sphinx.ext.autosummary
autoclass_content = "both"  # Add __init__ doc (ie. params) to class summaries
html_show_sourcelink = False  # Remove 'view source code' from top of page (for html, not python)
autodoc_inherit_docstrings = True  # If no docstring, inherit from base class
set_type_checking_flag = True  # Enable 'expensive' imports for sphinx_autodoc_typehints
nbsphinx_allow_errors = True  # Continue through Jupyter errors
# autodoc_typehints = "description" # Sphinx-native method. Not as good as sphinx_autodoc_typehints
add_module_names = False  # Remove namespaces from class/method signatures

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

default_role = 'py:obj'
nitpicky = True
nitpick_ignore = [('py:class', 'pybind11_builtins.pybind11_object'),
                  ('py:class', 'List'),
                  ('py:class', 'Positive'),
                  ('py:class', 'NonNegative'),
                  ('py:class', 'numpy.uint64'),
                  ('py:class', 'numpy.int64'),
                  ('py:class', 'numpy.float64'),
                  ('py:class', 'numpy.complex128'),
                  ('py:obj', 'List'),
                  ('py:class', 'm'),
                  ('py:class', 'n'),
                  ('py:class', '1')]

if on_rtd:
    branch_or_tag = branch or 'v{}'.format(release)
else:
    rev_parse_name = subprocess.check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD']).decode('ascii').strip()
    branch_or_tag = rev_parse_name if rev_parse_name != 'HEAD' else 'v{}'.format(release)

# nbsphinx_prolog = """
# {{% set docname = 'docs/' + env.doc2path(env.docname, base=False) %}}
#
# .. only:: html
#
# """
# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'default' if on_rtd else 'sphinx_rtd_theme'
html_logo = "images/logo.png"

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#
# html_theme_options = {}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# Custom sidebar templates, must be a dictionary that maps document names
# to template names.
#
# The default sidebars (for documents that don't match any pattern) are
# defined by theme itself.  Builtin themes are using these templates by
# default: ``['localtoc.html', 'relations.html', 'sourcelink.html',
# 'searchbox.html']``.
#
# html_sidebars = {}


# -- Options for HTMLHelp output ---------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = 'EGTtoolsdoc'

# -- Options for LaTeX output ------------------------------------------------

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    #
    # 'papersize': 'letterpaper',

    # The font size ('10pt', '11pt' or '12pt').
    #
    # 'pointsize': '10pt',

    # Additional stuff for the LaTeX preamble.
    #
    # 'preamble': '',

    # Latex figure (float) alignment
    #
    # 'figure_align': 'htbp',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (master_doc, 'EGTtools.tex', 'EGTtools Documentation',
     'Elias Fernández', 'manual'),
]

# -- Options for manual page output ------------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (master_doc, 'egttools', 'EGTtools Documentation',
     [author], 1)
]

# -- Options for Texinfo output ----------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (master_doc, 'EGTtools', 'EGTtools Documentation',
     author, 'EGTtools', 'One line description of project.',
     'Miscellaneous'),
]

latex_logo = "images/logo-full.pdf"

# -- Options for Epub output -------------------------------------------------

# Bibliographic Dublin Core info.
epub_title = project
epub_author = author
epub_publisher = author
epub_copyright = copyright

# The unique identifier of the text. This can be a ISBN number
# or the project homepage.
#
# epub_identifier = ''

# A unique identification for the text.
#
# epub_uid = ''

# A list of files that should not be packed into the epub file.
epub_exclude_files = ['search.html']

# -- Extension configuration -------------------------------------------------

# -- Options for intersphinx extension ---------------------------------------
