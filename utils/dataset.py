import json
from base import Constant
from mytoken import Token
from utils.vocab import word_norm
from abc import ABCMeta, abstractmethod

class Dataset():

    def __init__(self, data_dir):
        self.datadir = data_dir
        self.train_data, self.n_train = self.load_dataset(data_dir+'train')
        self.dev_data, self.n_dev = self.load_dataset(data_dir+'dev')
        self.test_data, self.n_test = self.load_dataset(data_dir+'test')
        self.tags = self.create_tags()
        self.tag2sample = self.create_tag2sample()

    @abstractmethod
    def load_dataset(self, filename):
        pass

    @abstractmethod
    def create_tags(self):
        pass

    @abstractmethod
    def create_tag2sample(self):
        pass

    @abstractmethod
    def create_kb(self, sample):
        pass

    @abstractmethod
    def create_constants(self, sample):
        pass


class NERDataset(Dataset):

    def __init__(self, data_dir):
        super().__init__(data_dir)

    def load_dataset(self, filename):
        
        dataset = []
        with open(filename) as f:
            lines = f.readlines()
            for line in lines:
                data = json.loads(line)
                dataset.append(data)

        return dataset, len(dataset)

    def create_tags(self):
        ne_ls = []
        for sample in self.train_data:
            nes = sample['ner'][0]
            for ne in nes:
                ne = ne[2]
                if ne not in ne_ls:
                    ne_ls.append(ne)
        return ne_ls

    def create_tag2sample(self):
        ne2sample = {}
        for ne in self.tags:
            ne2sample[ne] = []
        for sample in self.train_data:
            sentence = sample['sentences'][0]
            nes = sample['ner'][0]
            for ne in self.tags:
                idx = []
                for ne_res in nes:
                    if ne_res[2] == ne:
                       idx.append(ne_res[:2]) 
                ne2sample[ne].append([sentence, idx])
        return ne2sample

    def create_constants(self):
        vocab = []
        for sample in self.train_data:
            sentence = sample['sentences'][0]
            for word in sentence:
                word = word_norm(word)
                if word not in vocab:
                    vocab.append(word)
        constants = [Constant(word) for word in vocab]
        return constants

    def create_kb(self, sample):
        sentence = sample['sentences'][0] if type(sample) == dict else sample[0]
        sentence = [word_norm(word) for word in sentence]
        n = len(sentence)
        tokens = [Token(i,sentence[i],None) for i in range(n)]
        for i in range(n):
            if i == 0:
                tokens[i].link(None, tokens[i+1])
            elif i == n-1:
                tokens[i].link(tokens[i-1], None)
            else:
                tokens[i].link(tokens[i-1], tokens[i+1])
        return tokens

class CHIPSTSDataset(Dataset):

    def __init__(self, data_dir):
        super().__init__(data_dir)

    def load_dataset(self, filename):
        
        with open(filename) as f:
            dataset = json.load(f)

        return dataset, len(dataset)

    def create_tags(self):
        tags = []
        for sample in self.train_data:
            tag = sample['label']
            if tag not in tags:
                tags.append(tag)
        return tags

    def create_tag2sample(self):
        tag2sample = {}
        for tag in self.tags:
            tag2sample[tag] = []
        for sample in self.train_data:
            sentence = [sample['text1'], sample['text2']]
            tag = sample['label']
            tag2sample[tag].append(sentence)
        return tag2sample

    def create_constants(self):
        vocab = []
        for sample in self.train_data:
            sentence = sample['text1'] + sample['text2']
            for word in sentence:
                word = word_norm(word)
                if word not in vocab:
                    vocab.append(word)
        constants = [Constant(word) for word in vocab]
        return constants

    def create_kb(self, sample):
        sentence = sample['text1'] + sample['text2']
        sentence = [word_norm(word) for word in sentence]
        n = len(sentence)
        tokens = [Token(i,sentence[i],None) for i in range(n)]
        for i in range(n):
            if i == 0:
                tokens[i].link(None, tokens[i+1])
            elif i == n-1:
                tokens[i].link(tokens[i-1], None)
            else:
                tokens[i].link(tokens[i-1], tokens[i+1])
        return tokens

class SNLIDataset(Dataset):

    def __init__(self, data_dir):
        super().__init__(data_dir)

    def load_dataset(self, filename):
        
        dataset = []
        with open(filename) as f:
            lines = f.readlines()
            for line in lines:
                data = json.loads(line)
                dataset.append(data)

        return dataset, len(dataset)

    def create_tags(self):
        ne_ls = []
        for sample in self.train_data:
            nes = sample['ner'][0]
            for ne in nes:
                ne = ne[2]
                if ne not in ne_ls:
                    ne_ls.append(ne)
        return ne_ls

    def create_tag2sample(self):
        ne2sample = {}
        for ne in self.tags:
            ne2sample[ne] = []
        for sample in self.train_data:
            sentence = sample['sentences'][0]
            nes = sample['ner'][0]
            for ne in self.tags:
                idx = []
                for ne_res in nes:
                    if ne_res[2] == ne:
                       idx.append(ne_res[:2]) 
                ne2sample[ne].append([sentence, idx])
        return ne2sample

    def create_constants(self):
        vocab = []
        for sample in self.train_data:
            sentence = sample['text1'] + sample['text2']
            for word in sentence:
                word = word_norm(word)
                if word not in vocab:
                    vocab.append(word)
        constants = [Constant(word) for word in vocab]
        return constants

    def create_kb(self, sample):
        sentence = sample['sentences'][0] if type(sample) == dict else sample[0]
        sentence = [word_norm(word) for word in sentence]
        n = len(sentence)
        tokens = [Token(i,sentence[i],None) for i in range(n)]
        for i in range(n):
            if i == 0:
                tokens[i].link(None, tokens[i+1])
            elif i == n-1:
                tokens[i].link(tokens[i-1], None)
            else:
                tokens[i].link(tokens[i-1], tokens[i+1])
        return tokens

class TRECDataset(Dataset):

    def __init__(self, data_dir):
        super().__init__(data_dir)

    def load_dataset(self, filename):
        
        dataset = []
        with open(filename) as f:
            lines = f.readlines()
            for line in lines:
                for i in range(len(line)):
                    if line[i] == ':':
                        tag = line[:i]
                        sentence = line[i+1:-1].split(' ')
                        break
                data = [tag, sentence]
                dataset.append(data)

        return dataset, len(dataset)

    def create_tags(self):
        tags = []
        for sample in self.train_data:
            tag = sample[0]
            if tag not in tags:
                tags.append(tag)
        return tags

    def create_tag2sample(self):
        tag2sample = {}
        for tag in self.tags:
            tag2sample[tag] = []
        for sample in self.train_data:
            sentence = sample[1]
            tag = sample[0]
            tag2sample[tag].append(sentence)
        return tag2sample

    def create_constants(self):
        vocab = []
        for sample in self.train_data:
            sentence = sample[1]
            for word in sentence:
                word = word_norm(word)
                if word not in vocab:
                    vocab.append(word)
        constants = [Constant(word) for word in vocab]
        return constants

    def create_kb(self, sample):
        sentence = sample[1]
        sentence = [word_norm(word) for word in sentence]
        n = len(sentence)
        tokens = [Token(i,sentence[i],None) for i in range(n)]
        for i in range(n):
            if i == 0:
                tokens[i].link(None, tokens[i+1])
            elif i == n-1:
                tokens[i].link(tokens[i-1], None)
            else:
                tokens[i].link(tokens[i-1], tokens[i+1])
        return tokens