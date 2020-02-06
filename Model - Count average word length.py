import json
import string
import os
import sys
import re
# from keras.preprocessing.text import text_to_word_sequence
from statistics import mean, median, mode

# Parameters:

Singaporeans_only = True

# Helper functions

if Singaporeans_only:
    cleaned_corpus = os.path.join(sys.path[0], 'smsCorpus_Line_by_line_SG_only.txt')
else:     cleaned_corpus = os.path.join(sys.path[0], 'smsCorpus_Line_by_line.txt')

def remove_punctuation(sentence):
    return sentence.translate(str.maketrans('','', string.punctuation))


# Count



def get_word_list(list_of_sentences_file):

    list_of_all_tokens = []

    for line in open(list_of_sentences_file):
        tokens = remove_punctuation(line.rstrip().lower()).split()
        no_of_tokens = len(tokens)
        for i in range(no_of_tokens):
            list_of_all_tokens.append(tokens[i])
    return list_of_all_tokens

def calculate_m_m_m(list_of_words):
    lengths = [len(token) for token in list_of_words]
    print('Mean = ', mean(lengths), '\nMedian = ', median (lengths), '\nMode = ', mode (lengths))

calculate_m_m_m(get_word_list(cleaned_corpus))

