from transformers import pipeline
from sentence_transformers import SentenceTransformer, util
from ..configuartions.sentiment_analyzes_values import SENTIMENT_ANALYZES_VALUES
import numpy as np


class SentimentSuggestion:
    def __init__(self):
        self.sentiment_model = pipeline(
            "sentiment-analysis",
            model="distilbert-base-uncased-finetuned-sst-2-english",
            revision="714eb0f"
        )
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.sentiment__analyzes_values = SENTIMENT_ANALYZES_VALUES

    def analyze_sentiment(self, channel_messages):
        messages = channel_messages

        if messages is None or len(messages) == 0:
            print("No messages found.")
            return []

        content_list = []
        for msg in messages:
            content_list.append(msg.content)

        sentiments_to_process = self.sentiment_model(content_list)
        sentiment_suggestions = []

        for idx, result in enumerate(sentiments_to_process):
            sentiment_suggestions.append({
                "message": content_list[idx],
                "sentiment": result['label'],
                "score": result['score']
            })

        preprocessed_sentiment_results = self.preprocess_sentiments(content_list)
        similarity_results = self.check_similarity(content_list)

        return {
            "sentiment_analysis": list({frozenset(item.items()): item for item in (sentiment_suggestions + preprocessed_sentiment_results)}.values()),
            "similarity_analysis": similarity_results
        }

    def preprocess_sentiments(self, content_list):
        sentiment_results = []
        for message in content_list:
            if any(keyword.lower() in message.lower() for keyword in self.sentiment__analyzes_values):
                sentiment_results.append({
                    "message": message,
                    "sentiment": "NEUTRAL",
                    "score": 1.0
                })
        return sentiment_results

    def check_similarity(self, content_list):
        if not content_list or len(content_list) < 2:
            print("Not enough issues for similarity comparison.")
            return []

        issue_embeddings = self.embedding_model.encode(content_list)
        similarities = util.pytorch_cos_sim(issue_embeddings, issue_embeddings)

        similarity_results = []
        for i in range(len(content_list)):
            similarities[i, i] = -1

            most_similar_index = np.argmax(similarities[i])
            similarity_score = similarities[i, most_similar_index].item()

            similarity_results.append({
                "issue": content_list[i],
                "most_similar_to": content_list[most_similar_index],
                "similarity_score": similarity_score
            })

        return similarity_results




    