class WordFrequency(object):
    def __init__(self):
        pass

    def init(self, word, count):
        self.word = word
        self.count = count

    def sort_key(self):
        return self.count