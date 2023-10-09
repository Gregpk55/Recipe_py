import os
import sys
import django

sys.path.insert(0, os.path.abspath('.'))  # This adds the src directory, which contains manage.py
sys.path.insert(0, os.path.abspath('..'))  # This ensures that the parent directory (which might have other required modules) is added
  # Ensure your project directory is in the PYTHONPATH.
os.environ['DJANGO_SETTINGS_MODULE'] = 'recipe_app.settings'

print(sys.path)
 # Use your project's settings.
django.setup()

project = 'Recipe-App'
copyright = '2023, Greg Kennedy'
author = 'Greg Kennedy'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx.ext.autodoc']

templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']
