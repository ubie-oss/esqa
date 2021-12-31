# -*- coding: utf-8 -*-
"""Console script for esqa."""

import click

from esqa.config import Configuration, load
from esqa.runner import Runner


@click.command()
@click.option('-c', '--config', type=str, help="configuration file")
@click.option('--es-host', type=str, help="Host name of Elasticsearch host", required=False)
@click.option('--es-port', type=int, help="Port number of Elasticsearch host", required=False)
@click.option('--index', type=str, help="target index name", required=True)
def main(config, es_port, es_host, index):
    runner = Runner()
    results = runner.run(config=load(config), index_name=index)
    print(results)


if __name__ == '__main__':
    main()
