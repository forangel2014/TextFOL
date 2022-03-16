from logic.predicates import *
from logic.connectives import *
from logic.functions import *
from logic.controller import Controller
from utils.dataset import *

class TextFOL():

    def __init__(self, dataset, controller:Controller):
        self.dataset = dataset
        self.controller = controller

    def get_reward(self, rule):
        if rule.state == 'BEGIN':
            precision, recall = self.eval_tc_rule(rule)
            return precision*100
        else:
            return -1

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

        return precision, recall

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

        return precision, recall