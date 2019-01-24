# NOTE: this must be imported first
from ._version import __version__

from .core import (
    get_dist, 
    get_dist_full, 
    get_dm, 
    get_dm_full, 
    get_galactic_dm
)

from .tests import test

__all__ = [
    'get_dist', 
    'get_dist_full', 
    'get_dm', 
    'get_dm_full', 
    'get_galactic_dm',
    'test',
    '__version__'
    ]