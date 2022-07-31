"""Tripod (Denish: stativ) - manage the back end of Binaries Repository Management (BRM) systems like a tripod."""
import os
from typing import List

APP_NAME = (
    'Tripod (Denish: stativ) - manage the back end of Binaries Repository Management (BRM) systems like a tripod.'
)
APP_ALIAS = 'stativ'
APP_ENV = 'STATIV'
DEBUG = bool(os.getenv(f'{APP_ENV}_DEBUG', ''))
VERBOSE = bool(os.getenv(f'{APP_ENV}_VERBOSE', ''))
QUIET = False
STRICT = bool(os.getenv(f'{APP_ENV}_STRICT', ''))
ENCODING = 'utf-8'
ENCODING_ERRORS_POLICY = 'ignore'
DEFAULT_CONFIG_NAME = '.stativ.json'
DEFAULT_LF_ONLY = 'YES'

# [[[fill git_describe()]]]
__version__ = '2022.7.31+parent.12b228ee'
# [[[end]]] (checksum: a8220c43ffb3a4c7c1320d5f3eaf7b50)
__version_info__ = tuple(
    e if '-' not in e else e.split('-')[0] for part in __version__.split('+') for e in part.split('.') if e != 'parent'
)
__all__: List[str] = []
