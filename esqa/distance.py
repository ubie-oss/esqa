import dataclasses
import json
import rbo
from typing import Dict, List

from esqa.save import Ranking


@dataclasses.dataclass
class FailedRanking:
    name: str
    similarity: float
    ranking_pair: List[tuple]


def load_rankings(path: str) -> Dict:
    with open(path) as f:
        rankings = json.load(f)
    results = {}
    for ranking in rankings:
        results[ranking["name"]] = Ranking(ranking["name"], ranking["query"], ranking["ranking"])
    return results


def _extract(ranking: Ranking) -> List[str]:
    return [e["source"]["id"] for e in ranking.ranking]


def _compare(ranking_a, ranking_b):
    print(ranking_a)
    print(ranking_b)
    return rbo.rbo.RankingSimilarity(ranking_a, ranking_b).rbo()


def _generate(ranking_a: Ranking, ranking_b: Ranking, similarity: float):
    #print(_extract(ranking_a))
    #print(_extract(ranking_b))
    #print(list(zip(_extract(ranking_a), _extract(ranking_b))))
    return FailedRanking(
        name=ranking_a.name,
        similarity=similarity,
        ranking_pair=list(zip(_extract(ranking_a), _extract(ranking_b)))
    )


def compare_rankings(rankings_a: Dict[str, Ranking], rankings_b: Dict[str, Ranking], threshold: float) -> List[FailedRanking]:
    results = []
    for ranking_name in rankings_a:
        similarity = _compare(_extract(rankings_a[ranking_name]), _extract(rankings_b[ranking_name]))
        if similarity > threshold:
            continue
        results.append(_generate(rankings_a[ranking_name], rankings_b[ranking_name], similarity))
    return results
