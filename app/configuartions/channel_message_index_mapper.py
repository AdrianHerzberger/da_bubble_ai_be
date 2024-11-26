from elasticsearch.helpers import async_bulk
from elasticsearch import Elasticsearch
from ..instances.elastic_search_engine import es_elastic_search_engine as es

async def mapping_channel_message_index(messages):
    for message in messages:
            try:
                await es.index(
                    index="messages",
                    id=message.id,  
                    body={
                        "channel_id": message.channel_id,
                        "sender_id": message.sender_id,
                        "content": message.content,
                        "timestamp": message.timestamp.isoformat()
                    }
                )
            except Exception as e:
                print(f"Error indexing message {message.id}: {e}")
                return []




