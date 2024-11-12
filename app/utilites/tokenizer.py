import pandas as pd
import nltk
from nltk.tokenize import TweetTokenizer

class Tokenizer():
    def __init__(self):
        self.tok = TweetTokenizer()
        
    def tokenizer(self, text):
        return self.tok.tokenize(text)