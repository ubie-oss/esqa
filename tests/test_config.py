# -*- coding: utf-8 -*-
"""Tests for esqa.config."""

import unittest
from esqa.validation_config import load


class TestConfig(unittest.TestCase):
    def test_config_load(self):
        config = load("tests/fixtures/sample_config.json")
        assert len(config.cases) == 1
        assert config.cases[0].name == "match all query"
        assert len(config.cases[0].asserts) == 1
        assert config.cases[0].asserts[0].type == "equal"
        assert config.cases[0].asserts[0].rank == 0
        assert config.cases[0].asserts[0].item.field == "id"
        assert config.cases[0].asserts[0].item.value == "24343"

    def test_template_config_load(self):
        config = load("tests/fixtures/sample_template_config.json")
        assert len(config.cases) == 2

        assert config.cases[0].name == "match identical"
        assert len(config.cases[0].asserts) == 1
        assert config.cases[0].asserts[0].type == "equal"
        assert config.cases[0].asserts[0].rank == 0
        assert config.cases[0].asserts[0].item.field == "id"
        assert config.cases[0].asserts[0].item.value == "2324"
        assert config.cases[0].query == {
            "query": {"match": {"message": {"query": "engineer"}}}
        }

        assert config.cases[1].name == "match prefix"
        assert len(config.cases[1].asserts) == 1
        assert config.cases[1].asserts[0].type == "equal"
        assert config.cases[1].asserts[0].rank == 0
        assert config.cases[1].asserts[0].item.field == "id"
        assert config.cases[1].asserts[0].item.value == "2324"
        assert config.cases[1].query == {
            "query": {"match": {"message": {"query": "enginee"}}}
        }
