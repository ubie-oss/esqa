#!/usr/bin/env bash

set -euo pipefail -o posix

curl -XDELETE "http://localhost:9400/sample?pretty=true"
curl -s -H "Content-Type: application/x-ndjson" -XPUT "http://localhost:9400/sample" --data-binary @sample/mapping.json
curl -s -H "Content-Type: application/x-ndjson" -XPOST "http://localhost:9400/_bulk" --data-binary @sample/sample-data.jsonl
