import os
import random
import re

from nltk import WhitespaceTokenizer, bigrams

tokens = []
file_bigrams = []
vocabulary = {}
t = WhitespaceTokenizer()

filename = input().strip()


def tokenize_line(line):
    global tokens
    for token in t.tokenize(line):
        tokens.append(token)


def create_file_birgrams(items):
    global file_bigrams
    file_bigrams = list(bigrams(items))


def create_freq_vocabulary(file_bigrams):
    global vocabulary
    for item in file_bigrams:
        vocabulary.setdefault(item[0], {})
        vocabulary[item[0]].setdefault(item[1], 0)
        vocabulary[item[0]][item[1]] += 1


if not os.access(filename, os.F_OK):
    print('File does not exist.')
else:
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file.readlines():
            tokenize_line(line)
    
    create_file_birgrams(tokens)
    create_freq_vocabulary(file_bigrams)
    
    possible_starts = []
    for token in vocabulary.keys():
        if re.match('^[A-Z].*[^.!?]$', token):
            possible_starts.append(token)
    
    selected_tokens = random.choices(population=possible_starts, k=10)
    
    for token in selected_tokens:
        sentence = [token]
        valid_length = 1
        isValid = False
        while not isValid:
            prev_token = sentence[-1]
            
            possible_tokens = {}
            for t in vocabulary[prev_token]:
                possible_tokens[t] = vocabulary[prev_token][t]
            
            choice = random.choices(k=1, population=list(possible_tokens.keys()), weights=list(possible_tokens.values()))
            sentence += choice
            valid_length += 1
            if re.match('.*[.!?]$', choice[0]) is not None:
                if valid_length >= 5:
                    isValid = True
        print(" ".join(sentence))
