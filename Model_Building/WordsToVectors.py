from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class WordsToVecotrs:
    def __init__(self, max_features, stop_words='english'):
        self.max_features = max_features
        self.stop_words = stop_words
        self.cv = CountVectorizer(max_features=self.max_features, stop_words=self.stop_words)

    def getVectors(self, data, column):
        self.vectors = self.cv.fit_transform(data[column]).toarray()
        return self.vectors

    def getVecotrNames(self):
        return self.cv.get_feature_names()

    def getSimilarity(self):
        self.similarity = cosine_similarity(self.vectors)
        return self.similarity