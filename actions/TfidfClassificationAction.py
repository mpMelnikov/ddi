from actions.Action import Action
from boilerplate.PreprocessingFacade import PreprocessingFacade
from boilerplate.Serialization import deserialize


class TfidfClassificationAction(Action):
    def make(self):
        print("TfidfClassificationAction")
        confidenceThreshold = 0.6
        supportThreshold = 0
        countThreshold = 3

        # todo: Get the test set path from command line arguments
        learning_set = list(PreprocessingFacade().get_learning_set("data\DDICorpus\Test\Test for DDI Extraction task\DrugBank"))

        tfIdfResults = deserialize(self._input_path)
        tfIdfDict = self.to_dict(tfIdfResults)
        self.classify(learning_set, tfIdfDict, confidenceThreshold, supportThreshold, countThreshold)
        estimate = self.estimate(learning_set, True)
        print(estimate["precision"])
        print(estimate["recall"])
        print(estimate["f1"])


    def classify(self, learning_set, tfIdfResults, confidenceThreshold, supportThreshold, countThreshold):
        print("classify " + str(confidenceThreshold) + " " + str(supportThreshold) + " " + str(countThreshold))
        keyWords = set()
        for text_report in learning_set:
            count = 0
            keyWordsInTheArticle = set()
            text_report.classified_is_ddi = False
            for stem in text_report.get_stems_array():
                if not stem in tfIdfResults.keys():
                    continue
                tfIdfResult = tfIdfResults[stem]
                # text_report.classified_is_ddi = False
                if tfIdfResult.getConfidence() > confidenceThreshold and tfIdfResult.getSupport() > supportThreshold:
                    # text_report.classified_is_ddi = True
                    if stem not in keyWordsInTheArticle:
                        count += 1
                        keyWordsInTheArticle.add(stem)
                        if not stem in keyWords:
                            keyWords.add(stem)
            if count > countThreshold:
                text_report.classified_is_ddi = True
        # for stem in keyWords:
        #     print(stem)
        if len(keyWords) > 0:
            print("keyWords = " + str(len(keyWords)))

    def estimate(self, learning_set, targetTextClass):
        retrievedDocuments = 0
        correctRetrievedDocuments = 0
        relevantDocuments = 0
        for text_report in learning_set:
            realTextClass = text_report.is_ddi
            classifiedTextClass = text_report.classified_is_ddi
            if realTextClass == targetTextClass:
                relevantDocuments += 1
                if realTextClass == classifiedTextClass:
                    correctRetrievedDocuments += 1
            if classifiedTextClass == targetTextClass:
                retrievedDocuments += 1

        precision = 0
        if retrievedDocuments > 0:
            precision = correctRetrievedDocuments / retrievedDocuments
        recall = 0
        if relevantDocuments > 0:
            recall = correctRetrievedDocuments / relevantDocuments
        f1 = 0
        if precision + recall > 0:
            f1 = 2 * precision * recall / (precision + recall)

        result = {}
        result["precision"] = precision
        result["recall"] = recall
        result["f1"] = f1
        return result


    def to_dict(self, tfIdfResults):
        # todo: try to avoid these operations
        result = {}
        for i in tfIdfResults:
            result[i.word] = i
        return result