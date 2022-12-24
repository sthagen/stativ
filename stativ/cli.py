#! /usr/bin/env python
"""Visit prefix and backup store folder trees of some binary repository management system and create delta."""
import sys
from typing import no_type_check

import stativ.stativ


@no_type_check
def main(argv=None):
    """Delegate processing to the implementation."""
    argv = sys.argv[1:] if argv is None else argv
    stativ.main(argv)
