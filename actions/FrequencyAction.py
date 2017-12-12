from actions.Action import Action
from boilerplate.ProcessingFacade import ProcessingFacade


class FrequencyAction(Action):
    # def __init__(self, inputFile, outputFile):
    #     super().__init__(inputFile, outputFile)

    def make(self):
        super().make()
        print("FrequencyAction...")
        ProcessingFacade().count_frequencies(self._input_path, self._output_path)



