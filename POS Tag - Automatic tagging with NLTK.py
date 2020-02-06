# Preamble
import nltk 
import string
import numpy as np
import os
import sys

# original_file = os.path.join(sys.path[0], 'smsCorpus_Line_by_line_SG_only.txt')
selected_sentences = os.path.join(sys.path[0], '1207 Selected Sentences for tagging.txt')
auto_tag_sent = os.path.join(sys.path[0], '1207 Automatically tagged sentences.txt')

with open(auto_tag_sent, 'w') as auto:
    for line in open(selected_sentences):
        tokens = nltk.word_tokenize (line)
        tokens = nltk.pos_tag(tokens)

        # Convert from list of tuples [('fly, 'VB')] to string fly/VB and write to file

        newstr = []
        leng = len(tokens)
        for i in range(0, leng-1):
            newstr.append(tokens[i][0])
            newstr.append('/')
            newstr.append(tokens[i][1])
            newstr.append(' ')
        newstr.append(tokens[leng-1][0])
        newstr.append('/')
        newstr.append(tokens[leng-1][1])
        newstr.append('\n')

        auto.write('%s' % ''.join(newstr))
