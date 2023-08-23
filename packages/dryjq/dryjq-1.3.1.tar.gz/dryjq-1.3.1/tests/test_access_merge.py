# -*- coding: utf-8 -*-

"""

test_access_merge

Unit test the access.simple_merge() function

Copyright (C) 2023 Rainer Schwarzbach

This file is part of dryjq.

dryjq is free software: you can redistribute it and/or modify
it under the terms of the MIT License.

dryjq is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the LICENSE file for more details.

"""


from unittest import TestCase

import yaml

from dryjq import access

from . import data


class Merger(TestCase):

    """Merge function tests"""

    def test_simple_merge(self):
        """Test a simple merge"""
        source_ds = yaml.safe_load(data.INPUT_YAML_ANIMALS)
        ds_to_be_merged = yaml.safe_load(data.INPUT_ANIMAL_MERGER_1)
        expected_result = yaml.dump(
            yaml.safe_load(data.EXPECT_MERGED_ANIMALS_1),
            indent=2,
            default_flow_style=False,
            sort_keys=True,
        )
        serialized_result = yaml.dump(
            access.simple_merge(source_ds, ds_to_be_merged),
            indent=2,
            default_flow_style=False,
            sort_keys=True,
        )
        self.assertEqual(serialized_result, expected_result)


# vim: fileencoding=utf-8 ts=4 sts=4 sw=4 autoindent expandtab syntax=python:
