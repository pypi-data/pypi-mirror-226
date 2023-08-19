from __future__ import absolute_import
import bioat
import datetime
import os

project_toml: str = os.path.join(bioat.__path__[0], 'version.py')
sec = os.path.getmtime(project_toml)
__upgrade_date__ = datetime.date.fromtimestamp(sec)
__version__ = "0.4.6"

__author__ = 'Hua-nan ZHAO @ Tsinghua University'
__email__ = 'hermanzhaozzzz@gmail.com'
__doc_format__ = "restructuredtext"
__doc_address__ = "https://github.com/hermanzhaozzzz/bioat/tree/master/docs"
__repo_address__ = "https://github.com/hermanzhaozzzz/bioat"