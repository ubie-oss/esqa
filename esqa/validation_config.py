import json
import dataclasses
import string
from typing import List, Union, Dict, Optional


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
    name: Optional[str]
    query: dict
    asserts: List[EsAssert]
    original: dict


@dataclasses.dataclass
class Configuration:
    cases: List[Case]


def _generate_item(item: dict):
    return Item(field=item["field"], value=item["value"])


def _generate_asserts(case: dict) -> List[EsAssert]:
    if "asserts" not in case:
        return []

    return [
        EsAssert(
            type=element["type"],
            rank=element["rank"],
            item=_generate_item(element["item"]),
        )
        for element in case["asserts"]
    ]


def _load_template_query(template_query: dict, templates: Dict[str, string.Template]) -> dict:
    template_name = template_query["template"]
    return json.loads(templates[template_name].substitute(**template_query))


def _load_query(query: dict, templates: Dict[str, string.Template]) -> dict:
    if "template" in query:
        return _load_template_query(query, templates)
    return query


def _generate_cases(cases: List[dict], templates: Dict[str, string.Template]) -> List[Case]:
    return [
        Case(
            element["name"],
            _load_query(element["query"], templates),
            _generate_asserts(element),
            element
        )
        for element in cases
    ]


def _load_templates(template_settings: dict) -> Dict[str, string.Template]:
    templates: Dict[str, string.Template] = {}
    for setting in template_settings:
        template_file_path = setting["path"]
        with open(template_file_path) as t:
            template = string.Template(t.read())
        templates[setting["name"]] = template
    return templates


def generate(config: dict) -> Configuration:
    """Generate Configuration object from given dict object.

    :param config: dictionary object containing configuration settings
    :return: Configuration object
    """
    if "templates" in config:
        templates = _load_templates(config["templates"])
    else:
        templates = []
    return Configuration(_generate_cases(config["cases"], templates))


def load(file_path: str) -> Configuration:
    """Generate Configuration object from given setting file.

    :param file_path: dictionary object containing configuration settings
    :return: Configuration object
    """
    with open(file_path) as f:
        config = json.load(f)
    return generate(config)
