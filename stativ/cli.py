#! /usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=line-too-long
"""Visit prefix and backup store folder trees of some binary repository management system and create delta."""
import sys

import stativ.stativ


# pylint: disable=expression-not-assigned
def main(argv=None):
    """Delegate processing to the implementation."""
    argv = sys.argv[1:] if argv is None else argv
    stativ.main(argv)
