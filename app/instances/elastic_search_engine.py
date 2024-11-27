import asyncio
from elasticsearch import AsyncElasticsearch
from config import Config

HOST_URL = Config.ELASTIC_SEARCH_HOST
ELASTIC_KEY = Config.ELASTIC_KEY

es_elastic_search_engine = AsyncElasticsearch(
    [{'host': 'localhost', 'port':9200, 'scheme':'http'}],
    verify_certs=False,
    timeout=30,
    max_retries=10,
    retry_on_timeout=True
)

async def test_connection():
    try:
        health = await es_elastic_search_engine.cluster.health()
        print("ElasticSearch Cluster Health:", health)
    except Exception as e:
        print("Error connecting to ElasticSearch:", e)
