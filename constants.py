from base import Constant
import os

def create_const(datadir = './data/bc5cdr/'):
    vocab_file = datadir + 'vocab.txt'
    constants = []
    with open(vocab_file) as f:
        lines = f.readlines()
        for line in lines:
            constants.append(Constant(line[:-1]))

    return constants