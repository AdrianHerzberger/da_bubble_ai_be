from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from ..storage.channel_message_manager import ChannelMessageManager
from ..utilites.tokenizer import Tokenizer

def detect_topics(n_topics=2):
    channel_messages_manager = ChannelMessageManager()
    messages = await channel_messages_manager.get_all_messages()
    
    tokenizer_instance = Tokenizer()
    
    if messages is None or len(messages) == 0:
        print("No messages found.")
        return []
    
    text_data = []
    for msg in messages:
        text_data.append(msg.content)
        
    vectorizer = CountVectorizer(
        ngram_range=(1,1), 
        stop_words='english', 
        tokenizer=tokenizer_instance.tokenizer, 
        max_features=1000
    )
    count_data = vectorizer.fit_transform(text_data)
    
    lda = LatentDirichletAllocation(n_components=n_topics, random_state=0)
    lda.fit(count_data)
    
    topic_keywords = []
    
    for topic in lda.components_:
        for i in topic.argsort()[-5:]:
            topic_keywords.append(vectorizer.get_feature_names_out()[i])
        return topic_keywords
    




    