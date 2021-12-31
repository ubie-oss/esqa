from abc import ABCMeta, abstractmethod
from typing import List

from esqa.error import ValidationError


class BaseAssert(metaclass=ABCMeta):
    @abstractmethod
    def validate(self, es_results: dict, case_name: str) -> List[ValidationError]:
        pass
