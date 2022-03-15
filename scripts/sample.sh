#!/usr/bin/env bash

set -euo pipefail -o posix

esqa save --config sample/ranking.json --index sample > ~/Downloads/ranking.json
esqa ranking --config sample/ranking.json --index sample --ranking ~/Downloads/ranking.json
