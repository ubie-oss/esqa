from abc import ABC
from typing import List

from esqa.asserts.base import BaseAssert
from esqa.config import EsAssert
from esqa.error import ValidationError


class EqualAssert(BaseAssert, ABC):
    def __init__(self, config: EsAssert):
        self.rank = config.rank
        self.item = config.item

    def validate(self, es_results: dict, case_name: str) -> List[ValidationError]:
        errors = []
        value = es_results["hits"]["hits"][self.rank]["_source"][self.item.field]
        if value != self.item.value:
            errors.append(
                ValidationError(
                    message=f'[{case_name}] Document with {self.item.field} = {self.item.value} is not ranked in {self.rank}. {self.item.field} field value of {self.rank}-th item is {value}',
                                name="EqualAssert")
            )
        return errors
