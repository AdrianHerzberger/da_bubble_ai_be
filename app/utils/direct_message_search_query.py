from elasticsearch import Elasticsearch
from ..instances.elastic_search_engine import es_elastic_search_engine as es
import pprint 

async def search_direct_messages(receiver_id, keyword):
    query_body = {
        "query": {
            "bool": {
                "must" : [
                    {"match": {"content": keyword}}
                ],
                "filter": [
                    {"term": {"receiver_id.keyword": receiver_id}}
                ]
            }
        }
    }

    try: 
        response = await es.search(index="messages", body=query_body)
        pprint.pprint(f"Elastic searchg response query: {response}")
        hit_list = []
        for hit in response["hits"]["hits"]:
            print(f"hits found: {hit}")
            hit_data = {
                "id" : hit["_id"],
                "content": hit["_source"]["content"],
                "timestamp": hit["_source"]["timestamp"]
            }
            hit_list.append(hit_data)
        return hit_list
    except Exception as e:
        print(f"Error querying elastic search: {e}")
        return []

