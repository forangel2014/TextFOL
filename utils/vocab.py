import os
import json

def word_norm(word):
    word = ''.join([c for c in word if c!=' '])
    return word.lower()

def create_vocab(data_dir = '../data/'):

    for dir in os.listdir(data_dir):
        train_file = data_dir + dir + '/train.json'
        vocab_file = data_dir + dir + '/vocab.txt'
        vocab = []
        with open(train_file) as f:
            lines = f.readlines()
            for line in lines:
                data = json.loads(line)
                sentence = data['sentences'][0]
                for word in sentence:
                    norm_word = word_norm(word)
                    if not norm_word in vocab:
                        vocab.append(norm_word)
        with open(vocab_file, 'w') as g:
            for word in vocab:
                g.writelines(word + '\n')