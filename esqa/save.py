import dataclasses
from typing import List

from elasticsearch import Elasticsearch

from esqa.constants import ELASTICSEARCH_URL
from esqa.validation_config import Configuration, Case, EsAssert


@dataclasses.dataclass
class Ranking:
    name: str
    query: dict
    asserts: List[EsAssert]
    ranking: List[dict]


class RankingSaver:
    client: Elasticsearch

    def __init__(self):
        self.client = Elasticsearch([ELASTICSEARCH_URL])

    def run(self, config: Configuration, index_name: str):
        results = []
        for case in config.cases:
            results.append(self._get(case, index_name))
        return results

    def _get(self, case: Case, index_name: str):
        search_results = self.client.search(body=case.query, index=index_name)
        return self._format(search_results, case)

    def _format(self, search_results: dict, case: Case) -> Ranking:
        return Ranking(
            case.name,
            case.query,
            case.asserts,
            [{"id": candidate["_id"], "source": candidate["_source"]} for i, candidate in enumerate(search_results["hits"]["hits"])]
        )
