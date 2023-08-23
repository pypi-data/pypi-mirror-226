# -*- coding: utf-8 -*-

"""

dryjq.merge

dryjq.merge (or python3 -m dryjq.merge) command line script

Copyright (C) 2023 Rainer Schwarzbach

This file is part of dryjq.

dryjq is free software: you can redistribute it and/or modify
it under the terms of the MIT License.

dryjq is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the LICENSE file for more details.

"""


import sys

from typing import List, Optional

from dryjq import commons
from dryjq import commandline


#
# Classes
#


class MergeProgram(commandline.Program):

    """Merge program
    commandline.Program subclass with less command line arguments
    """

    name: str = "dryjq.merge"
    description: str = "Drastically Reduced YAML / JSON Query: merge files"
    query_option: bool = False
    merge_program: bool = True
    modify_in_place_option: bool = True
    default_output_format: str = commons.FORMAT_INPUT


#
# Functions
#


def main(args: Optional[List[str]] = None) -> int:
    """Execute the program using the provided command line arguments

    :param args: the list of command line arguments,
        or None to go with the default (sys.argv).
    :returns: the script returncode
    """
    program = MergeProgram(args)
    return program.execute()


if __name__ == "__main__":
    sys.exit(main())


# vim: fileencoding=utf-8 ts=4 sts=4 sw=4 autoindent expandtab syntax=python:
