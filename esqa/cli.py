# -*- coding: utf-8 -*-
"""Console script for esqa."""
import json
from dataclasses import is_dataclass, asdict

import click

from esqa.distance import load_rankings, compare_rankings
from esqa.save import RankingSaver
from esqa.validation_config import load
from esqa.validator import Validator


@click.group()
def main():
    pass


# To serialize class object
# Ref https://pod.hatenablog.com/entry/2018/09/29/222455
def custom_default(o):
    if is_dataclass(o):
        return asdict(o)
    raise TypeError(f"{o!r} is not JSON serializable")


def _dump(data):
    return json.dumps(
        data,
        indent=2,
        default=custom_default,
        ensure_ascii=False,
    )


@main.command()
@click.option("-c", "--config", type=str, help="configuration file")
@click.option("--index", type=str, help="target index name", required=True)
def assertion(config, index):
    runner = Validator()
    results = runner.run(config=load(config), index_name=index)
    print(_dump(results))


@main.command()
@click.option("-c", "--config", type=str, help="configuration file")
@click.option("--index", type=str, help="target index name", required=True)
def save(config, index):
    runner = RankingSaver()
    results = runner.run(config=load(config), index_name=index)
    print(_dump(list(results.values())))


@main.command()
@click.option("-r", "--ranking", type=str, help="ranking file")
@click.option("-c", "--config", type=str, help="configuration file")
@click.option("-t", "--threshold", type=float, help="threshold", default=0.7)
@click.option(
    "-f", "--target-field", type=str, help="field to compare the document", default="id"
)
@click.option("--index", type=str, help="target index name", required=True)
def distance(ranking, config, threshold, target_field, index):
    runner = RankingSaver()
    rankings = runner.run(config=load(config), index_name=index)
    compared_rankings = load_rankings(ranking)
    results = compare_rankings(rankings, compared_rankings, threshold, target_field)
    print(_dump(results))


@main.command()
@click.option("-r1", "--ranking1", type=str, help="first ranking file")
@click.option("-r2", "--ranking2", type=str, help="second ranking file")
@click.option("-t", "--threshold", type=float, help="threshold", default=0.7)
@click.option(
    "-f", "--target-field", type=str, help="field to compare the document", default="id"
)
def distance_rankings(ranking1, ranking2, threshold, target_field):
    rankings1 = load_rankings(ranking1)
    rankings2 = load_rankings(ranking2)
    results = compare_rankings(rankings1, rankings2, threshold, target_field)
    print(_dump(results))


if __name__ == "__main__":
    main()
