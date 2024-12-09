import asyncio
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF
import spacy

class MessageThreadSuggestion:
    def __init__(self):
        self.message_mention_terms = ["feature", "bug", "crash", "error", "load"]
        self.nlp = spacy.load("en_core_web_sm") 
            
    def extract_keywords(self, channel_message):
        messages = channel_message

        if messages is None or len(messages) == 0:
            print("No messages found.")
            return []
        
        content_list = []
        for msg in messages:
            content_list.append(msg.content)
            
        keyword_list = self._extract_basic_keywords(content_list)
        topic_keywords = self._generate_topic_keywords(content_list)
        
        return list(set(keyword_list + topic_keywords))

            
    def _extract_basic_keywords(self, content_list):
        keyword_list = []
        
        for msg in content_list:
            for term in self.message_mention_terms:
                if term in msg.lower():
                    keyword_list.append(f"# {term.capitalize()}")
                    
            doc = self.nlp(msg)
            for ent in doc.ents:
                if ent.label_ in {"ORG", "PRODUCT"}:
                    keyword_list.append(f"# {ent.text.capitalize()}")
                     
        return list(set(keyword_list))
    
    
    def _generate_topic_keywords(self, content_list):
        vectorizer = TfidfVectorizer(
            ngram_range=(1, 2),
            stop_words='english',
            max_features=1000
        )

        tfidf_matrix = vectorizer.fit_transform(content_list)
        nmf = NMF(n_components=min(len(content_list), 5), random_state=1)
        nmf.fit(tfidf_matrix)
        
        keywords = []
        
        feature_names = vectorizer.get_feature_names_out()
        for topic in enumerate(nmf.components_):
            for i in topic.argsort()[:-6:-1]:
                topic_keywords = feature_names[i]
                keywords.extend(topic_keywords)   
        
        return list(set(keywords))
    
    