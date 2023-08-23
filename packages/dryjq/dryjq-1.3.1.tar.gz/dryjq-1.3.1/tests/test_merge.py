# -*- coding: utf-8 -*-

"""

tests.test_merge

Unit test the 'dryjq.merge' command line interface

Copyright (C) 2023 Rainer Schwarzbach

This file is part of dryjq.

dryjq is free software: you can redistribute it and/or modify
it under the terms of the MIT License.

dryjq is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the LICENSE file for more details.

"""


import io
import os
import secrets
import tempfile

from unittest import TestCase
from unittest.mock import patch

import dryjq

from dryjq import merge

from . import data
from .commons import GenericCallResult


class ConvertResult(GenericCallResult):

    """Conversion result"""

    @classmethod
    def do_call(cls, *args, **kwargs):
        """Do the real function call"""
        del kwargs
        return merge.main(list(args))


class TestSimple(TestCase):

    """Simple test module using patched stdin and stdout"""

    def setUp(self):
        """Create a temporary directory"""
        # pylint: disable=consider-using-with
        self.tempdir = tempfile.TemporaryDirectory()
        # pylint: enable=consider-using-with
        self.testfile_name = os.path.join(
            self.tempdir.name, f"{secrets.token_urlsafe(6)}.yaml"
        )

    def tearDown(self):
        """Cleanup the temporary directory"""
        self.tempdir.cleanup()

    def __create_file(self, content=None):
        """Create a file in the temporary directory"""
        if content:
            with open(
                self.testfile_name,
                mode="w",
                encoding="utf-8",
            ) as testdata_file:
                testdata_file.write(content)
            #
        #

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_merge_via_stdin(self, mock_stdout):
        """Convert JSON to YAML"""
        self.__create_file(content=data.INPUT_YAML_ANIMALS)
        result = ConvertResult.from_call(
            self.testfile_name,
            stdin_data=data.INPUT_ANIMAL_MERGER_1,
            stdout=mock_stdout,
        )
        self.assertEqual(result.stdout, data.EXPECT_MERGED_ANIMALS_1)
        self.assertEqual(result.returncode, data.RETURNCODE_OK)

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_print_version(self, mock_stdout):
        """Print version"""
        with self.assertRaises(SystemExit) as sys_exit:
            result = ConvertResult.from_call(
                "--version",
                stdout=mock_stdout,
            )
            self.assertEqual(
                result.stdout, f"dryjq.convert {dryjq.__version__}\n"
            )
            self.assertEqual(result.returncode, data.RETURNCODE_OK)
        #
        self.assertEqual(sys_exit.exception.code, data.RETURNCODE_OK)


# vim: fileencoding=utf-8 ts=4 sts=4 sw=4 autoindent expandtab syntax=python:
