class Summarization:
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Summarization, cls).__new__(cls, *args, **kwargs)
            cls._instance.filtered_keywords = []
        return cls._instance

    def filter_summarization(self, keywords):
        for kw in keywords:
            if kw.strip():
                self.filtered_keywords.append(kw.strip())
        unique_keywords = list(set(self.filtered_keywords))
        return self.filtered_keywords

    def summarization_result(self):
        return self.filtered_keywords  

