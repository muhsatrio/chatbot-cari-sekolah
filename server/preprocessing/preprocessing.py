import string
import re
import nltk
nltk.download('punkt')
from nltk.tokenize import word_tokenize
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory, ArrayDictionary, StopWordRemover
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import sys

class Preprocessing:

    def execute(self, teks):
        teks = self.__case_folding(teks)

        tokens = self.__tokenizing(teks)

        tokens = self.__stopward_removal(tokens)

        tokens = self.__stemming(tokens)

        return tokens

    def __case_folding(self, teks):
        teks = teks.lower()

        teks = teks.translate(str.maketrans("", "", string.punctuation))

        teks = re.sub(r"\d+", "", teks)

        return teks

    def __tokenizing(self, teks):

        tokens = word_tokenize(teks)

        return tokens

    def __stopward_removal(self, tokens):
        stop_factory = StopWordRemoverFactory().get_stop_words()

        more_stopword = ['dong', 'atuh', 'plis']

        data = stop_factory + more_stopword

        dictionary = ArrayDictionary(data)

        str_remove = StopWordRemover(dictionary)

        tokens = word_tokenize(str_remove.remove(' '.join(tokens)))

        return tokens

    def __stemming(self, tokens):
        factory = StemmerFactory()

        stemmer = factory.create_stemmer()

        tokens = word_tokenize(stemmer.stem(" ".join(tokens)))

        return tokens