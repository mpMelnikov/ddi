import nltk

class TextReport:
    environment_ready = False

    def __init__(self, text):
        self._stems = None
        self.text = text

    def get_stems_array(self):
        if self._stems is None:
            self._stems = list(self.stem(self.tokenize()))
        return self._stems

    def tokenize(self):
        global tokens
        self.check_environment()
        tokens = nltk.word_tokenize(self.text)
        return tokens

    @staticmethod
    def check_environment():
        if TextReport.environment_ready:
            return
        TextReport.environment_ready = True
        nltk.download('punkt')

    def stem(self, tokens):
        porter_stemmer = nltk.PorterStemmer()
        for i in tokens:
            yield porter_stemmer.stem(i)

    def stem2(self, tokens):
        lancaster_stemmer = nltk.LancasterStemmer()
        for i in tokens:
            yield lancaster_stemmer.stem(i)