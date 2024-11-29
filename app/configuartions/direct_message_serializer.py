class DirectMessageSerializer:
    @staticmethod
    def serialize(instance):
        return {
            "message_id": str(instance.id),
            "sender_id": str(instance.sender_id),
            "receiver_id": str(instance.receiver_id),
            "content": instance.content,
            "message_time": instance.timestamp.isoformat(),
        }

    @staticmethod
    def serialize_many(instances):
        return [DirectMessageSerializer.serialize(instance) for instance in instances]