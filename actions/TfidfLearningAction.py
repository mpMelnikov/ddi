
from actions.TfidfClassificationAction import TfidfClassificationAction
from boilerplate.PreprocessingFacade import PreprocessingFacade
from boilerplate.Serialization import deserialize


class TfidfLearningAction(TfidfClassificationAction):
    def make(self):
        print("TfidfLearningAction")

        tfIdfResults = deserialize(self._input_path)
        tfIdfDict = self.to_dict(tfIdfResults)

        # todo: Get the learning set path from command line arguments
        learning_set = list(PreprocessingFacade().get_learning_set("data\DDICorpus\Train\DrugBank"))
        self.learn(learning_set, tfIdfDict)

    def learn(self, learning_set, tfIdfResults):
        maxF1Score = 0
        maxEstimate = {}
        maxEstimate["f1"] = 0
        maxEstimate["precision"] = 0
        maxEstimate["recall"] = 0

        iteration = 0
        confidenceThreshold = 0

        best_confidenceThreshold = 0
        best_supportThreshold = 0
        best_countThreshold = 0
        while confidenceThreshold <= 1:
            supportThreshold = 0
            while supportThreshold <= 1:
                for countThreshold in range(0, 4):
                    print("========")
                    self.classify(learning_set, tfIdfResults, confidenceThreshold, supportThreshold, countThreshold)
                    estimate = self.estimate(learning_set, True)

                    print(estimate["precision"])
                    print(estimate["recall"])
                    print(estimate["f1"])

                    if estimate["f1"] > maxF1Score:
                        maxF1Score = estimate["f1"]
                        maxEstimate = estimate
                        best_confidenceThreshold = confidenceThreshold
                        best_supportThreshold = supportThreshold
                        best_countThreshold = countThreshold
                    iteration += 1
                supportThreshold += 0.1
            confidenceThreshold += 0.1

        print("Maximum: ")
        print("precision: " + str(maxEstimate["precision"]))
        print("recall: " + str(maxEstimate["recall"]))
        print("f1: " + str(maxEstimate["f1"]))
        print("best_confidenceThreshold: " + str(best_confidenceThreshold))
        print("best_supportThreshold: " + str(best_supportThreshold))
        print("best_countThreshold: " + str(best_countThreshold))
