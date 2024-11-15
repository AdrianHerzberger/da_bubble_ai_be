class Summarization:
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Summarization, cls).__new__(cls, *args, **kwargs)
            cls._instance.filtered_keywords = []
        return cls._instance

    def filter_summarization(self, keywords):
        unique_keywords = set(self.filtered_keywords)
        for kw in keywords:
            if kw.strip() and len(kw) > int(1):
                print(kw)
                unique_keywords.add(kw.strip())
        self.filtered_keywords = list(unique_keywords)
        return self.filtered_keywords

    def summarization_result(self):
        return self.filtered_keywords  

