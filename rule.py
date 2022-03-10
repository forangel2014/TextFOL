# horn clause
# body -> head(RE:realtion tag/NER:entity)
# body

# run time:
# parse a sample(sentence text (+ anotated entities)) into a set of facts(KB)
# inference by forward chaining with given rules

import itertools

class TCRule():

    def __init__(self, root, vars, head):
        self.root = root
        self.vars = vars
        self.head = head

    def __str__(self) -> str:
        return str(self.root) + ' -> ' + self.head

    def gmp(self, kb):
        ins_set = kb
        n = len(self.vars)
        for _ in range(n-1):
            ins_set = itertools.product(ins_set, kb)
        for inss in ins_set:
            try:
                for i in range(n):
                    var = self.vars[i]
                    ins = inss[i] if type(inss) == list else inss
                    var.bind(ins)
                if self.root():
                    return True
            except:
                continue
        return False

class NERRule():

    def __init__(self, root, vars, head, idxs):
        self.root = root
        self.vars = vars
        self.head = head
        self.idxs = idxs

    def __str__(self) -> str:
        return str(self.root) + ' -> ' + self.head + str([str(idx) for idx in self.idxs])

    def gmp(self, kb):
        ins_set = kb
        n = len(self.vars)
        for _ in range(n-1):
            ins_set = itertools.product(ins_set, kb)
        for inss in ins_set:
            try:
                for i in range(n):
                    var = self.vars[i]
                    ins = inss[i] if type(inss) == list else inss
                    var.bind(ins)
                if self.root():
                    return [idx() for idx in self.idxs]
            except:
                continue
        return False
