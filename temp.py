import nltk
from nltk.stem.porter import PorterStemmer
from nltk.stem.lancaster import LancasterStemmer

def pos_tag(tokens):
    nltk.download('averaged_perceptron_tagger')
    tagged = nltk.pos_tag(tokens)
    print(tagged)

def tokenize(sentence):
    global tokens
    nltk.download('punkt')
    tokens = nltk.word_tokenize(sentence)
    print(tokens)
    return tokens

def stem(tokens):
    porter_stemmer = PorterStemmer()
    for i in tokens:
        print(porter_stemmer.stem(i))

def stem2(tokens):
    lancaster_stemmer = LancasterStemmer()
    for i in tokens:
        print(lancaster_stemmer.stem(i))



#	debug configuration parameters for different tasks
#
#	count tf-idf values
#	-l -c tfidf -output data/tfIdfResults.xml
#
#	learn by tfIdf
#	-l -c tfidfLearning -input data/tfIdfResults.xml
#
#	classification by tf-idf
#	-l -c tfidfClassification -input data/tfIdfResults.xml


