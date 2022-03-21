"""constants
"""
import os

ELASTICSEARCH_URL: str = os.getenv("ELASTICSEARCH_URL", "localhost:9200")
