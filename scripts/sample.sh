#!/usr/bin/env bash

set -euo pipefail -o posix

export ELASTICSEARCH_URL=localhost:9400

esqa save --config sample/ranking.json --index sample > ~/Downloads/ranking.json
esqa ranking --config sample/ranking.json --index sample --ranking ~/Downloads/ranking.json
