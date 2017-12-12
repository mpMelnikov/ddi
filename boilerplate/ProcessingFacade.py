from boilerplate.PreprocessingFacade import PreprocessingFacade
from boilerplate.Serialization import serialize
from boilerplate.Singleton import singleton
from models.WordFrequencies import WordFrequencies
from models.WordFrequency import WordFrequency

@singleton
class ProcessingFacade:
    def count_frequencies(self, input_path, output_path):
        print("ddi articles words processing...")
        no_ddi_texts = PreprocessingFacade().preprocess_articles(input_path)
        ddi_texts = PreprocessingFacade().preprocess_interactions(input_path)

        ddi_frequencies = self.get_frequencies(ddi_texts)
        no_ddi_frequencies = self.get_frequencies(no_ddi_texts)

        if output_path:
            serialize(ddi_frequencies, output_path + "/ddi_frequencies.xml")
            serialize(no_ddi_frequencies, output_path + "/random_article_frequencies.xml")

        return WordFrequencies(ddi_frequencies, no_ddi_frequencies)

    def get_frequencies(self, text_reports):
        print("calculating frequencies...")
        result = {}
        for text_report in text_reports:
            stems_array = text_report.get_stems_array()
            for word in stems_array:
                if word == "" or self.has_numbers(word):
                    continue
                count = result.get(word)
                if count is None:
                    count = 0
                count += 1
                result[word] = count

        frequencies = []
        for key, value in result.items():
            wf = WordFrequency()
            wf.init(key, value)
            frequencies.append(wf)

        return sorted(frequencies, key=WordFrequency.sort_key)

    @staticmethod
    def has_numbers(word):
        return any(char.isdigit() for char in word)
