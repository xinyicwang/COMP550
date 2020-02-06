import json
import string
import os
import sys
import re
import numpy
# from keras.preprocessing.text import text_to_word_sequence
from statistics import mean, median, mode, stdev

# Parameters:

Singaporeans_only = True

# Helper functions

if Singaporeans_only:
    cleaned_corpus = os.path.join(sys.path[0], 'smsCorpus_Line_by_line_SG_only.txt')
else:     cleaned_corpus = os.path.join(sys.path[0], 'smsCorpus_Line_by_line.txt')

def remove_punctuation(sentence):
    return sentence.translate(str.maketrans('','', string.punctuation))


# Count


def get_list(list_of_sentences_file):

    list_of_lengths = []

    for line in open(list_of_sentences_file):
        tokens = remove_punctuation(line.rstrip().lower()).split()
        list_of_lengths.append(len(tokens))
    return list_of_lengths

def calculate_m_m_m(list1):
    print('Mean = ', mean(list1), '\nMedian = ', median (list1), '\nMode = ', mode (list1), '\nSD = ', stdev(list1))
    print('Quantiles divided at each 1/3 = ', numpy.quantile(list1, [0.3333333333,0.666666667]))

def calculate_no_of_sentences(list_of_sentences_file):
    no_of_sentences = 0
    for line in open(list_of_sentences_file):
        no_of_sentences +=1
    return no_of_sentences   

aaa = get_list(cleaned_corpus)

calculate_m_m_m(aaa)

# List of number of sentences with corresponding length
list_of_no = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
list_of_no_pc = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
no_of_sentences_with_extraneous_length = 0

for i in aaa:
    if 1<=i<=16:
        list_of_no[i-1] += 1
    elif i>16:
        list_of_no[16] += 1
    else:
        no_of_sentences_with_extraneous_length +=1
        continue

print ('number of sentences with extraneous lengths = ', no_of_sentences_with_extraneous_length)

print ('number of sentences with lengths 1, 2, 3, etc.: \n', list_of_no)

for i in range(0, 17):
    list_of_no_pc [i] = (list_of_no[i] / calculate_no_of_sentences(cleaned_corpus))*100

print ('percentage of sentences with lengths 1, 2, 3, etc.: \n', list_of_no_pc)

percentage1 = 0
percentage2 = 0
percentage3 = 0
for i in range(0, 6):
    percentage1 += list_of_no_pc [i]
for i in range(6, 12):
    percentage2 += list_of_no_pc [i]
for i in range(12, 17):
    percentage3 += list_of_no_pc [i]

print ('percentage of sentences <= 6 words ', percentage1)
print ('percentage of sentences 7-12 words ', percentage2)
print ('percentage of sentences >=13 words ', percentage3)