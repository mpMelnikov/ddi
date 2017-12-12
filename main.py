import argparse

from actions.TfidfLearningAction import TfidfLearningAction
from actions.FrequencyAction import FrequencyAction
from actions.TfidfClassificationAction import TfidfClassificationAction
from actions.TfidfAction import TfidfAction
from actions.PreprocessAction import PreprocessAction

commands = dict(frequency=FrequencyAction,
                # preprocess=PreprocessAction,
                tfidf=TfidfAction,
                tfidfLearning=TfidfLearningAction,
                tfidfClassification=TfidfClassificationAction)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='DDI NLP program')
    parser.add_argument('command', action="store", help='command name')
    parser.add_argument('-log', '-l', action="store", help='turn on log', default=False)
    parser.add_argument('-input', action="store", help='input file')
    parser.add_argument('-output', action="store", help='output file')
    args = parser.parse_args()
    command = commands[args.command](args.input, args.output)
    command.make()
    input("Press Enter to continue...")


# sequency for tf-idf:
# don't need it: frequency -input "data\DDICorpus\Train\DrugBank" -output "data\frequencies"
# 1. tfidf -input "data\DDICorpus\Train\DrugBank" -output "data\tfidf\tfidf_results.xml"
# 2. tfidfLearning -input "data\tfidf\tfidf_results.xml" -output ""
# 3. tfidfClassification -input "data\tfidf\tfidf_results.xml" -output ""


#	параметры debug configuration для разных задач:
#
#	посчитать значения tfIdf
#	-l -c tfidf -output data/tfIdfResults.xml
#   tfidf -output data/tfIdfResults.xml
#
#	обучение по tfIdf
#	-l -c tfidfLearning -input data/tfIdfResults.xml
#
#	классификация по tfIdf
#	-l -c tfidfClassification -input data/tfIdfResults.xml

