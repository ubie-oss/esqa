from abc import ABC
from typing import List

from esqa.asserts.base import BaseAssert
from esqa.validation_config import EsAssert
from esqa.error import ValidationError


class HigherAssert(BaseAssert, ABC):
    def __init__(self, config: EsAssert):
        self.rank = config.rank
        self.item = config.item

    def validate(self, es_results: dict, case_name: str) -> List[ValidationError]:
        errors = []
        is_found = False
        for i, candidate in enumerate(es_results["hits"]["hits"]):
            if i < self.rank:
                if self.item.value == candidate["_source"][self.item.field]:
                    is_found = True
                    break
            else:
                if self.item.value == candidate["_source"][self.item.field]:
                    is_found = True
                    errors.append(
                        ValidationError(
                            message=f'[{case_name}] Document with {self.item.field} = {self.item.value} is ranked lower than specified {self.rank} ({i}-th ranked).',
                            name="HigherAssert",
                        )
                    )
        if is_found is False:
            errors.append(
                ValidationError(
                    message=f"[{case_name}] Document with {self.item.field} = {self.item.value} is not ranked.",
                    name="HigherAssert",
                )
            )
        return errors
