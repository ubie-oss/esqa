import json
import dataclasses
import string
from typing import List, Union


@dataclasses.dataclass
class Item:
    field: str
    value: Union[int, str, float]


@dataclasses.dataclass
class EsAssert:
    type: str
    rank: int
    item: Item


@dataclasses.dataclass
class Case:
    name: str
    query: dict
    asserts: List[EsAssert]


@dataclasses.dataclass
class Configuration:
    cases: List[Case]


def _generate_item(item: dict):
    return Item(field=item["field"], value=item["value"])


def _generate_asserts(assert_config: list) -> List[EsAssert]:
    return [EsAssert(type=element["type"],
                     rank=element["rank"],
                     item=_generate_item(element["item"])) for element in assert_config]


def _load_template_query(template_query: dict) -> dict:
    template_file_path = template_query["template"]
    with open(template_file_path) as t:
        template = string.Template(t.read())
    return json.loads(template.substitute(**template_query))


def _load_query(query: dict) -> dict:
    if "template" in query:
        return _load_template_query(query)
    return query


def _generate_cases(cases: List[dict]) -> List[Case]:
    return [Case(element["name"],
                 _load_query(element["query"]),
                 _generate_asserts(element["asserts"])) for element in cases]


def generate(config: dict) -> Configuration:
    """Generate Configuration object from given dict object.

    :param config: dictionary object containing configuration settings
    :return: Configuration object
    """
    return Configuration(_generate_cases(config["cases"]))


def load(file_path: str) -> Configuration:
    """Generate Configuration object from given setting file.

    :param file_path: dictionary object containing configuration settings
    :return: Configuration object
    """
    with open(file_path) as f:
        config = json.load(f)
    return generate(config)
