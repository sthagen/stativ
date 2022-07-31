#! /usr/bin/env python
"""Visit prefix and backup store folder trees of some binary repository management system and create delta."""
import sys

import stativ.stativ


def main(argv=None):
    """Delegate processing to the implementation."""
    argv = sys.argv[1:] if argv is None else argv
    stativ.main(argv)
