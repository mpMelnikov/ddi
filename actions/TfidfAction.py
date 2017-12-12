import re

from actions.Action import Action
from boilerplate.PreprocessingFacade import PreprocessingFacade
from boilerplate.Serialization import serialize
from models.TfIdfResult import TfIdfResult


class TfidfAction(Action):
    def make(self):
        print("Counting TF-IDF values started...")

        no_ddi_texts = list(PreprocessingFacade().preprocess_articles(self._input_path))
        ddi_texts = list(PreprocessingFacade().preprocess_interactions(self._input_path))
        documents_number = len(no_ddi_texts) + len(ddi_texts)

        stem_tfidf_dict = {}
        ignore_pattern = re.compile("\\d")

        self.calculate(ddi_texts, stem_tfidf_dict, True, documents_number, ignore_pattern)
        self.calculate(no_ddi_texts, stem_tfidf_dict, False, documents_number, ignore_pattern)

        tfIdfResults = self.calculate_tfidf(stem_tfidf_dict)
        serialize(tfIdfResults, self._output_path)
# 		calculateInteractions(learningSet, stemTfIdfHashTable, numberPattern);
# 		calculateArticles(learningSet, stemTfIdfHashTable, numberPattern);
#
#       ArrayList<TfIdfResult> tfIdfResults = calculateTfIdf(stemTfIdfHashTable);
#       (new UniversalSerializationFacade<TfIdfResult>(_outputFile)).serialize(tfIdfResults);

    def calculate_tfidf(self, stem_tfidf_dict):
        # tfIdfResults = []
        tfidf_result = []
        for tfidf_item in stem_tfidf_dict.values():
            tfidf_result.append(tfidf_item)
        tfidf_result.sort(key=lambda i: i.value, reverse=True)
        return tfidf_result


    def calculate(self, texts, stem_tfidf_dict, is_ddi, documents_number, ignore_pattern):
        for text in texts:
            thisArticleWordsSet = {}
            for stem in text.get_stems_array():
                if stem == "" or ignore_pattern.match(stem):
                    continue
                if stem in stem_tfidf_dict:
                    if not stem in thisArticleWordsSet:
                        tfidf_result = stem_tfidf_dict[stem]
                        if is_ddi:
                            tfidf_result.addWordFromCategory()
                        else:
                            tfidf_result.addWordNotFromCategory()
                else:
                    stem_tfidf_dict[stem] = TfIdfResult(stem, 1, 1, documents_number)

