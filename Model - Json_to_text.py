import json
import os
import sys
import re
# from keras.preprocessing.text import text_to_word_sequence
from statistics import mean, median, mode

# Parameters:

Singaporeans_only = True


# Helper Functions:

OnlyAscii = lambda s: re.match('^[\x00-\x7F]+$', s) != None

corpus_file = os.path.join(sys.path[0], 'smsCorpus_en_2015.03.09_all.json')

if Singaporeans_only:
    cleaned_corpus = os.path.join(sys.path[0], 'smsCorpus_Line_by_line_SG_only2.txt')
else:     cleaned_corpus = os.path.join(sys.path[0], 'smsCorpus_Line_by_line.txt')

def isSingaporean (regionStr):
    if regionStr in ['SG', 'Singapore', 'Spore', 'sg', 'singapore', 'spore']:
        return True
    else: return False


# Convert json file to a txt file with message texts line by line

with open(corpus_file) as f:
    corpus = json.load(f)

    users = set()
    texts = []
    for text in corpus['smsCorpus']['message']:
        if (Singaporeans_only and isSingaporean(text['source']['userProfile']['country']['$'])):
            users.add(text['source']['userProfile']['userID']['$'])
            texts.append(str(text['text']['$']))

    lengths = [len(text) for text in texts]
    sequence_length = mode(lengths)

    print("Number of Users:", len(users))
    print("Number of Texts:", len(corpus['smsCorpus']['message']))
    print("Mode of sentence length: ", sequence_length)

    with open(cleaned_corpus, 'w') as filehandle:
        no_of_sentences = 0
        for sentence in texts:
            if OnlyAscii(sentence):
                filehandle.write('%s\n' % sentence)
                no_of_sentences += 1
        
        print('New Number of Sentences:', no_of_sentences)