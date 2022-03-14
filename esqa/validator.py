from typing import List

from elasticsearch import Elasticsearch

from esqa.asserts.base import BaseAssert
from esqa.asserts.equal import EqualAssert
from esqa.asserts.higher import HigherAssert
from esqa.asserts.lower import LowerAssert
from esqa.validation_config import Configuration, Case
from esqa.constants import ELASTICSEARCH_URL
from esqa.error import ValidationError


def _load_assert(a) -> BaseAssert:
    if a.type == "equal":
        return EqualAssert(a)
    if a.type == "higher":
        return HigherAssert(a)
    if a.type == "lower":
        return LowerAssert(a)
    else:
        raise ValueError(f"Assertion Type: {a.type} is not supported")


def _load_asserts(case) -> List[BaseAssert]:
    return [_load_assert(a) for a in case.asserts]


class Validator:
    host: str
    port: int
    client: Elasticsearch

    def __init__(self):
        self.client = Elasticsearch([ELASTICSEARCH_URL])

    def run(self, config: Configuration, index_name: str) -> List[ValidationError]:
        errors = []
        for case in config.cases:
            errors.extend(self.check(case, index_name))
        return errors

    def check(self, case: Case, index_name: str) -> List[ValidationError]:
        search_results = self.client.search(body=case.query, index=index_name)
        return self._check(search_results, case)

    def _check(self, search_results: dict, case: Case) -> List[ValidationError]:
        asserts = _load_asserts(case)
        errors = []
        for a in asserts:
            errors.extend(a.validate(es_results=search_results, case_name=case.name))
        return errors
