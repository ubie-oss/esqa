"""constants
"""
import os

ELASTICSEARCH_URL: str = os.getenv('ES_URI', 'localhost:9200')
