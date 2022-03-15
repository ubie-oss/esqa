#!/usr/bin/env bash

set -euo pipefail -o posix

curl -XDELETE "http://localhost:9200/sample?pretty=true"
curl -s -H "Content-Type: application/x-ndjson" -XPUT "http://localhost:9200/sample" --data-binary @sample/mapping.json
curl -s -H "Content-Type: application/x-ndjson" -XPOST "http://localhost:9200/_bulk" --data-binary @sample/sample-data.jsonl
