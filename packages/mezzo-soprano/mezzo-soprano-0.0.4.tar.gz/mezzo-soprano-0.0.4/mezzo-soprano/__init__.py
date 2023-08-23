# -*- coding: utf-8 -*-

"""Top-level package for tenor."""

__author__ = """J. Michael Burgess"""
__email__ = 'jburgess@mpe.mpg.de'


from .model import Hadronic, Leptonic, LogParabola
from .utils.configuration import show_configuration, tenor_config
from .utils.logging import (
    activate_warnings,
    silence_warnings,
    update_logging_level,
)

from . import _version
__version__ = _version.get_versions()['version']
