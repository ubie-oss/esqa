import dataclasses
from typing import List, Dict

from elasticsearch import Elasticsearch

from esqa.constants import ELASTICSEARCH_URL
from esqa.validation_config import Configuration, Case, EsAssert


@dataclasses.dataclass
class Ranking:
    name: str
    query: dict
    ranking: List[dict]


class RankingSaver:
    client: Elasticsearch

    def __init__(self):
        self.client = Elasticsearch([ELASTICSEARCH_URL])

    def run(self, config: Configuration, index_name: str) -> Dict[str, Ranking]:
        results = {}
        for case in config.cases:
            ranking = self._get(case, index_name)
            results[ranking.name] = ranking
        return results

    def _get(self, case: Case, index_name: str) -> Ranking:
        search_results = self.client.search(body=case.query, index=index_name)
        return self._format(search_results, case)

    def _format(self, search_results: dict, case: Case) -> Ranking:
        return Ranking(
            case.name,
            case.query,
            [{"id": candidate["_id"], "source": candidate["_source"]} for i, candidate in enumerate(search_results["hits"]["hits"])]
        )
