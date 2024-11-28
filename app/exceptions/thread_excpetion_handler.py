def validate_thread_inputs(thread_type, channel_message_id=None, direct_message_id=None):
    if thread_type not in ["channel", "direct"]:
        raise ValueError("Invalid thread_type. Must be 'channel' or 'direct'.")
    
    if not (channel_message_id or direct_message_id):
            raise ValueError("Either channel_message_id or direct_message_id must be provided.")
        
    if channel_message_id and direct_message_id:
        raise ValueError("Only one of channel_message_id or direct_message_id can be provided.")
    
    if thread_type == "channel" and not channel_message_id:
        raise ValueError("channel_message_id is required for a 'channel' thread.")
    
    if thread_type == "direct" and not direct_message_id:
        raise ValueError("direct_message_id is required for a 'direct' thread.")

    