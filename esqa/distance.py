import json
import rbo
from typing import Dict, List

from esqa.save import Ranking


def load_rankings(path: str) -> Dict:
    with open(path) as f:
        rankings = json.load(f)
    results = {}
    for ranking in rankings:
        results[ranking["name"]] = Ranking(ranking["name"], ranking["query"], ranking["ranking"])
    return results


def _extract(ranking: Ranking) -> List[str]:
    return [e["id"] for e in ranking.ranking]


def compare(ranking_a, ranking_b):
    return rbo.rbo.RankingSimilarity(ranking_a, ranking_b).rbo()


def compare_rankings(rankings_a: Dict[str, Ranking], rankings_b: Dict[str, Ranking]):
    for ranking_name in rankings_a:
        print(compare(_extract(rankings_a[ranking_name]), _extract(rankings_b[ranking_name])))
