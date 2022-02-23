# -*- coding: utf-8 -*-
"""
Main module.
"""
from pkg_resources import get_distribution, DistributionNotFound

try:
    # Change here if project is renamed and does not equal the package name
    dist_name = "pdf-link-checker"
    __version__ = get_distribution(dist_name).version
except DistributionNotFound:
    __version__ = "unknown"
finally:
    del get_distribution, DistributionNotFound
__author__ = "Matt Briggs"
__copyright__ = "Matt Briggs"
__license__ = "mit"
