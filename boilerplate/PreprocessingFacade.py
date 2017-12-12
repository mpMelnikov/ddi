import os
import xml.etree.ElementTree as ElementTree
from boilerplate.Singleton import singleton
from models.TextReport import TextReport


@singleton
class PreprocessingFacade:

    def get_all_sentence_nodes(self, path):
        tree = ElementTree.parse(path)
        sentences = tree.findall("./sentence")
        for sentence in sentences:
            yield sentence
        pass


    def iterate_files(self, path, is_included):
        directory = os.fsencode(path)
        directory_str = str(directory, 'utf-8')
        for file in os.listdir(directory):
            filename = os.fsdecode(file)
            if not filename.endswith(".xml"):
                continue

            file_path = os.path.join(directory_str, filename)
            for sentence_node in self.get_all_sentence_nodes(file_path):
                if not is_included(sentence_node):
                    continue
                yield TextReport(sentence_node.get("text"))

    def is_random(self, sentence_node):
        return len(sentence_node.findall("./pair[@ddi='true']")) == 0

    def is_interaction(self, sentence_node):
        return len(sentence_node.findall("./pair[@ddi='true']")) > 0

    def preprocess_articles(self, path):
        return self.iterate_files(path, self.is_random)

    def preprocess_interactions(self, path):
        return self.iterate_files(path, self.is_interaction)

    def get_learning_set(self, path):
        ddi = self.preprocess_interactions(path)
        no_ddi = self.preprocess_articles(path)
        result = []
        for i in ddi:
            i.is_ddi = True
            result.append(i)
        for i in no_ddi:
            i.is_ddi = False
            result.append(i)
        return result