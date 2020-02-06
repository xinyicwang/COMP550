# The following are modified based on the code from Ashwin M. J. ------------------------------------ #
# https://medium.com/ymedialabs-innovation/next-word-prediction-using-markov-model-570fc0475f96 #

# Preamble
import string
import numpy as np
import os
import sys

# Parameter

order = 2   # Choose only among 2, 3, 4, 5
char_tokenization = False   # Choose between character tokenization and word tokenization

# Path of the text file containing the training data

training_data_file = os.path.join(sys.path[0], 'smsCorpus_Line_by_line_SG_only.txt')




# # Helper Function # #

def remove_punctuation(sentence):
    return sentence.translate(str.maketrans('','', string.punctuation))

def add2dict(dictionary, key, value):
    if key not in dictionary:
        dictionary[key] = []
    dictionary[key].append(value)

def list2probabilitydict(given_list):
    probability_dict = {}
    given_list_length = len(given_list)
    for item in given_list:
        probability_dict[item] = probability_dict.get(item, 0) + 1
    for key, value in probability_dict.items():
        probability_dict[key] = value / given_list_length
    return probability_dict

initial_word = {}
second_word = {}
third_word = {}
fourth_word = {}
fifth_word = {}
transitions = {}

def split_into_char (string1):
    return [char for char in string1]





# # Training Function # #

# Trains a Markov model based on the data in training_data_file
def train_markov_model(order):
    for line in open(training_data_file):
        if char_tokenization:
            tokens = split_into_char(remove_punctuation(line.rstrip().lower()))
        else: 
            tokens = remove_punctuation(line.rstrip().lower()).split()
        tokens_length = len(tokens)
        for i in range(tokens_length):
            token = tokens[i]
            if i == 0:
                initial_word[token] = initial_word.get(token, 0) + 1
            else:
                prev_token = tokens[i - 1]
                if i == tokens_length - 1:
                    if order == 2:
                        add2dict(transitions, (prev_token, token), 'END')
                    elif order == 3:                       
                        add2dict(transitions, (tokens[i - 2], prev_token, token), 'END')
                    elif (order == 4) or (order == 5 and tokens_length<=3):
                        add2dict(transitions, (tokens[i - 3], tokens[i - 2], prev_token, token), 'END')
                    elif order == 5:
                        add2dict(transitions, (tokens[i - 4], tokens[i - 3], tokens[i - 2], prev_token, token), 'END')
                    else: 
                        print('This order is not supported.')
                if i == 1:
                    add2dict(second_word, prev_token, token)
                elif i == 2 and order >= 3:
                    add2dict(third_word, (tokens[i - 2], prev_token), token)
                elif i == 3 and order >= 4:
                    add2dict(fourth_word, (tokens[i - 3], tokens[i - 2], prev_token), token)
                elif i == 4 and order >= 5:
                    add2dict(fifth_word, (tokens[i - 4], tokens[i - 3], tokens[i - 2], prev_token), token)
                else:
                    if order == 2:
                        prev_token_2 = tokens[i - 2]
                        add2dict(transitions, (prev_token_2, prev_token), token)
                    elif order == 3:
                        prev_token_2 = tokens[i - 2]
                        prev_token_3 = tokens[i - 3]
                        add2dict(transitions, (prev_token_3, prev_token_2, prev_token), token)
                    elif order == 4:
                        prev_token_2 = tokens[i - 2]
                        prev_token_3 = tokens[i - 3]
                        prev_token_4 = tokens[i - 4]
                        add2dict(transitions, (prev_token_4, prev_token_3, prev_token_2, prev_token), token)
                    elif order == 5:
                        prev_token_2 = tokens[i - 2]
                        prev_token_3 = tokens[i - 3]
                        prev_token_4 = tokens[i - 4]
                        prev_token_5 = tokens[i - 5]
                        add2dict(transitions, (prev_token_5, prev_token_4, prev_token_3, prev_token_2, prev_token), token)
    
    # Normalize the distributions
    initial_word_total = sum(initial_word.values())
    for key, value in initial_word.items():
        initial_word[key] = value / initial_word_total
        
    for prev_word, next_word_list in second_word.items():
        second_word[prev_word] = list2probabilitydict(next_word_list)

    for prev_word_list, next_word_list in third_word.items():
        third_word[prev_word_list] = list2probabilitydict(next_word_list)

    for prev_word_list4, next_word_list in fourth_word.items():
        fourth_word[prev_word_list4] = list2probabilitydict(next_word_list)

    for prev_word_list5, next_word_list in fifth_word.items():
        fifth_word[prev_word_list5] = list2probabilitydict(next_word_list)
        
    for word_pair, next_word_list in transitions.items():
        transitions[word_pair] = list2probabilitydict(next_word_list)
    
    print('Training successful.')
    print()

train_markov_model(order)

# # Helper Function # #

def sample_word(dictionary):
    p0 = np.random.random()
    cumulative = 0
    for key, value in dictionary.items():
        cumulative += value
        if p0 < cumulative:
            return key
    assert(False)






# # Test Function # #

number_of_sentences = 50
if char_tokenization:
    token_separator = ''
else:
    token_separator = ' '

# Function to generate sample text
def generate(order):
    for i in range(number_of_sentences):
        sentence = []
        # Initial word
        word0 = sample_word(initial_word)
        sentence.append(word0)
        # Second word
        word1 = sample_word(second_word[word0])
        sentence.append(word1)
        # if required, third word and more
        if order >=3:
            word2 = sample_word(third_word[(word0, word1)])
            if word2 == 'END':
                print(token_separator.join(sentence))
                continue
            sentence.append(word2)
        if order >=4:
            word3 = sample_word(fourth_word[(word0, word1, word2)])
            if word3 == 'END':
                print(token_separator.join(sentence))
                continue
            sentence.append(word3)
        if order >=5:
            word4 = sample_word(fifth_word[(word0, word1, word2, word3)])
            if word4 == 'END':
                print(token_separator.join(sentence))
                continue
            sentence.append(word4)
        # Subsequent words untill END
        if order == 2:
            while True:
                word2 = sample_word(transitions[(word0, word1)])
                if word2 == 'END':
                    break
                sentence.append(word2)
                word0 = word1
                word1 = word2
        if order == 3:
            while True:
                word3 = sample_word(transitions[(word0, word1, word2)])
                if word3 == 'END':
                    break
                sentence.append(word3)
                word0 = word1
                word1 = word2
                word2 = word3
        if order == 4:
            while True:
                word4 = sample_word(transitions[(word0, word1, word2, word3)])
                if word4 == 'END':
                    break
                sentence.append(word4)
                word0 = word1
                word1 = word2
                word2 = word3
                word3 = word4
        if order == 5:
            while True:
                word5 = sample_word(transitions[(word0, word1, word2, word3, word4)])
                if word5 == 'END':
                    break
                sentence.append(word5)
                word0 = word1
                word1 = word2
                word2 = word3
                word3 = word4
                word4 = word5
        print(token_separator.join(sentence))

generate(order)

# The above are modified based on the code from Ashwin M. J. ---------------------------------------- #