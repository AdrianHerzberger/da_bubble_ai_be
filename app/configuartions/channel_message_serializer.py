class ChannelMessageSerializer:
    @staticmethod
    def serialize(instance):
        return {
            "message_id": str(instance.id),
            "channel_id": str(instance.channel_id),
            "sender_id": str(instance.sender_id),
            "content": instance.content,
            "message_time": instance.timestamp.isoformat(),
        }
    
    @staticmethod    
    def serialize_many(instances):
        return [ChannelMessageSerializer.serialize(instance) for instance in instances]
