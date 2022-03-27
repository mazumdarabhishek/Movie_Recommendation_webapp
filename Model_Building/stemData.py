from nltk.stem.porter import PorterStemmer


class stemIT:

    def __init__(self, columns, data):
        self.columns = columns
        self.data = data
        self.ps = PorterStemmer()

    def helper_function(self, text):
        y = []
        try:
            for i in text.split():
                y.append(self.ps.stem(i))

            return " ".join(y)

        except Exception as e:
            return "Error occured while running stemIT() :: %s" % e

    def stem_apply(self):
        return self.data[self.columns].apply(self.helper_function) 