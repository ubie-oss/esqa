#!/usr/bin/env bash

set -euo pipefail -o posix

export ELASTICSEARCH_URL=localhost:9400

if [ ! -d output ]; then
  mkdir output
fi

esqa save --config sample/ranking.json --index sample > output/previous_ranking.json
esqa distance --config sample/compared_ranking.json --index sample --ranking output/previous_ranking.json
