import asyncio
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF
import numpy as np
import re

class MessageThreadSuggestion():
    def __init__(self):
        self.message_mention_terms = ["feature", "bug", "crash", "error", "load"]

    def extract_keywords(self, channel_message):
        messages = channel_message

        if messages is None or len(messages) == 0:
            print("No messages found.")
            return []
        
        content_list = []
        for msg in messages:
            content_list.append(msg.content)
            
        
        keyword_list = []
        for msg in content_list:
            for term in self.message_mention_terms:
                if term in msg:
                    keyword_list.append(f"# {term.capitalize()}")
                    
            feature_matches = re.findall(r"feature\s+#\s?(\w+)", msg, re.IGNORECASE)
            for  feature in feature_matches:
                keyword_list.append(f"Feature #{feature.capitalize()}")

        keyword_list = list(set(keyword_list))
        topic_keywords = self.process_topic_modeling(content_list)
        
        return list(set(keyword_list + topic_keywords))
    
    
    def process_topic_modeling(self, content_list):
        vectorizer = TfidfVectorizer(
            ngram_range=(1, 2),
            stop_words='english',
            max_features=1000
        )

        tfidf_matrix = vectorizer.fit_transform(content_list)
        nmf = NMF(n_components=1, random_state=1)
        nmf.fit(tfidf_matrix)
        
        return self.reflect_keywords(vectorizer, nmf)
        
                 
    def reflect_keywords(self, vectorizer, nmf, n_keywords=5):
        keywords = []
        
        feature_names = vectorizer.get_feature_names_out()
        for topic_idx, topic in enumerate(nmf.components_):
            for i in topic.argsort()[:-n_keywords - 1:-1]:
                topic_keywords = feature_names[i]
                keywords.extend(topic_keywords)   
        
        return list(set(keywords))
    
    