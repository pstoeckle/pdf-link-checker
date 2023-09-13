# -*- coding: utf-8 -*-
"""
Main module.
"""
from pkg_resources import DistributionNotFound, get_distribution

try:
    # Change here if project is renamed and does not equal the package name
    dist_name = "python-pdf-link-checker"
    __version__ = get_distribution(dist_name).version
except DistributionNotFound:
    __version__ = "unknown"
finally:
    del get_distribution, DistributionNotFound
__author__ = "Matt Briggs, Patrick Stöckle"
__copyright__ = "Matt Briggs, Patrick Stöckle"
__license__ = "mit"
