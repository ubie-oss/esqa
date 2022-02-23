# -*- coding: utf-8 -*-
"""Console script for esqa."""

import click

from esqa.config import load
from esqa.validator import Validator


@click.group()
def main():
    pass


@main.command()
@click.option("-c", "--config", type=str, help="configuration file")
@click.option("--index", type=str, help="target index name", required=True)
def check(config, index):
    runner = Validator()
    results = runner.run(config=load(config), index_name=index)
    print(results)


if __name__ == "__main__":
    main()
