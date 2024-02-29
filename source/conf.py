# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys


sys.path.insert(0, os.path.abspath('../'))

project = 'RT2_assignment1'
copyright = '2024, Enrico Dondero'
author = 'Enrico Dondero'
release = '1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.doctest',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'sphinx.ext.coverage',
    'sphinx.ext.mathjax',
    'sphinx.ext.ifconfig',
    'sphinx.ext.viewcode',
    'sphinx.ext.githubpages',
    "sphinx.ext.napoleon",
    'sphinx.ext.inheritance_diagram',
    'breathe'
]

highlight_language = 'python3'
source_suffix = '.rst'
master_doc = 'index'
html_theme = 'sphinx_rtd_theme'

templates_path = ['_templates']
exclude_patterns = []
autodoc_mock_imports = ["rospy", "std_msgs", "geometry_msgs", "actionlib", "actionlib_msgs", "rt2_assignment1.msg", "rt2_assignment1.srv","nav_msgs","assign_2"]  



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_static_path = ['_static']

# -- Options for intersphinx extension ---------------------------------------
# Example configuration for intersphinx: refer to the Python standard library.

intersphinx_mapping = {'python': ('https://docs.python.org/3', None)}

# -- Options for todo extension ----------------------------------------------
# If true, `todo` and `todoList` produce output, else they produce nothing.

todo_include_todos = True

# -- Options for breathe extension -------------------------------------------

breathe_projects = {
    "RT2_assignment1": "../build/xml"
}

breathe_default_project = "RT2_assignment1"
breath_default_members = ('members', 'undoc-members')
