#!/usr/bin/env bash

set -euo pipefail -o posix

export ELASTICSEARCH_URL=localhost:9400

if [ ! -d output ]; then
  mkdir output
fi

esqa check --config sample/validations.json --index sample
