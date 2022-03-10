from predicates import *
from connectives import *
from functions import *
from utils.dataset import *
from controller import Controller
from utils.dataset import TRECDataset

class TextFOL():

    def __init__(self, dataset, controller:Controller):
        self.dataset = dataset
        self.controller = controller

    def eval_ner_rule(self, rule):
        tp = 0
        fp = 0
        fn = 0
        samples = self.dataset.tag2sample[rule.head]
        for sample in samples:
            
            kb = self.dataset.create_kb(sample)
            res = rule.gmp(kb)
            
            ner = sample[1]
            if len(ner) == 0:
                if res != False:
                    fp += 1
            else:
                for ne in ner:
                    if res == False or res[0] != ne[0] or res[1] != ne[1]:
                        fn += 1
                    else:
                        tp += 1
                
        precision = tp/(tp+fp)
        recall = tp/(tp+fn)

        print(precision,recall)

    def eval_tc_rule(self, rule):
        tp = 0
        fp = 0
        fn = 0
        samples = self.dataset.train_data
        for sample in samples:
            
            kb = self.dataset.create_kb(sample)
            res = rule.gmp(kb)
            tag = sample[0]

            if res:
                if tag == rule.head:
                    tp += 1
                else:
                    fp += 1
            elif tag == rule.head:
                fn += 1
   
        precision = tp/(tp+fp) if tp+fp > 0 else 0
        recall = tp/(tp+fn) if tp+fn > 0 else 0

        print(precision,recall)

#datadir = 'data/bc5cdr/'
#dataset = NERDataset(datadir)
datadir = 'data/trec/'
dataset = TRECDataset(datadir)
constants = dataset.create_constants()
controller = Controller(predicates, connectives, functions, constants, tags=dataset.tags)
model = TextFOL(dataset, controller)
#rule = model.controller.rule_eg()
for _ in range(100):
    rule = model.controller.random_generate_rule()
    print(str(rule))
    model.eval_tc_rule(rule)