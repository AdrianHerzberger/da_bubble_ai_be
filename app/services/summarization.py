import asyncio
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF
from ..storage.channel_message_manager import ChannelMessageManager
from ..utilites.tokenizer import Tokenizer
import numpy as np

async def extract_keywords(n_keywords=5):
    channel_messages_manager = ChannelMessageManager()
    messages = await channel_messages_manager.get_all_messages()
    
    tokenizer_instance = Tokenizer()
    
    if messages is None or len(messages) == 0:
        print("No messages found.")
        return []
    
    content_list = []
    for msg in messages:
        content_list.append(msg.content)
        
    joined_text = " ".join(content_list)
        
    vectorizer = TfidfVectorizer(
        ngram_range=(1,1), 
        stop_words='english', 
        max_features=1000
    )
    tfidf_matrix = vectorizer.fit_transform([joined_text])
    
    nmf = NMF(n_components=1, random_state=1)
    nmf.fit(tfidf_matrix)
    
    keywords = np.array(vectorizer.get_feature_names_out())[
        np.argsort(-nmf.components_[0])[:n_keywords]
    ]
    
    return keywords
    
    