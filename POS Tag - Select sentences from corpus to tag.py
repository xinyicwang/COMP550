# Preamble
import string
import numpy as np
import os
import sys

original_file = os.path.join(sys.path[0], 'smsCorpus_Line_by_line_SG_only.txt')
selected_sentences = os.path.join(sys.path[0], '1207 Selected Sentences for tagging.txt')



no_of_sent = 0
no_of_selected_sent = 0
with open(selected_sentences, 'w') as ss:
    for line in open(original_file):
        no_of_sent +=1
        if no_of_sent % 34 == 1:
            ss.write('%s' % line)
            no_of_selected_sent +=1

print(no_of_sent, no_of_selected_sent)