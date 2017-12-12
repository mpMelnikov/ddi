class TfIdfResult(object):
    def __init__(self, word="", documentsFromCategoryContainWord=0, documentsContainWord=0, documentsNumber=0):
        self.word = word
        self.documentsFromCategoryContainWord = documentsFromCategoryContainWord
        self.documentsContainWord = documentsContainWord
        self.documentsNumber = documentsNumber
        self.value = 0
        if not documentsNumber == 0:
            self.value = self.calculateValue()

    def addWordFromCategory(self):
        self.documentsFromCategoryContainWord += 1
        self.documentsContainWord += 1
        self.value = self.calculateValue()

    def addWordNotFromCategory(self):
        self.documentsContainWord += 1
        self.value = self.calculateValue()

    def calculateValue(self):
        return self.getConfidence() * self.getSupport()

    def getConfidence(self):
        self.confidence = self.documentsFromCategoryContainWord / self.documentsContainWord
        return self.confidence

    def getSupport(self):
        self.support = self.documentsContainWord / self.documentsNumber
        return self.support
