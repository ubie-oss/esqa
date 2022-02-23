# -*- coding: utf-8 -*-

"""Tests for esqa.config."""
import json
import unittest

from esqa.validation_config import EsAssert, Item, Case
from esqa.validator import Validator


class TestConfig(unittest.TestCase):
    def test_check(self):
        runner = Validator()
        with open("tests/fixtures/sample_es_results.json") as f:
            search_results = json.load(f)
        es_assert = EsAssert(type="equal", rank=0, item=Item(field="id", value="6"))
        errors = runner._check(
            search_results=search_results, case=Case("sample", {}, [es_assert])
        )
        assert len(errors) == 1
        assert (
            errors[0].message
            == "[sample] Document with id = 6 is not ranked in 0. id field value of 0-th item is 6"
        )
