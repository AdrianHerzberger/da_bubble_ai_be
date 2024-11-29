from ..instances.elastic_search_engine import es_elastic_search_engine as es

async def mapping_direct_message_indexs(messages):
    for message in messages:
            try:
                await es.index(
                    index="messages",
                    id=message.id,  
                    body={
                        "sender_id": message.sender_id,
                        "receiver_id": message.receiver_id,
                        "content": message.content,
                        "timestamp": message.timestamp.isoformat()
                    }
                )
            except Exception as e:
                print(f"Error indexing message {message.id}: {e}")
                return []