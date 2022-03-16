class Tokenizer():

    def __init__(self, predicates, connectives, functions, constants, tags):
        self.tags = tags #1
        self.predicates = predicates #2
        self.connectives = connectives #3 
        self.functions = functions #4
        self.constants = constants #5

        self.n_tags = len(tags)
        self.n_predicates = len(predicates) 
        self.n_connectives = len(connectives) 
        self.n_functions = len(functions)
        self.n_constants = len(constants)
        self.pad_id = self.n_tags + self.n_predicates + self.n_connectives + self.n_functions + self.n_constants
        self.vocab_size = self.pad_id + 1

    def symbol2idx(self, symbol):
        n = 1
        if type(symbol) == str:
            return self.tags.index(symbol)
        elif symbol.type == 'predicate':
            for predicate in self.predicates:
                if isinstance(symbol, predicate):
                    return self.n_tags + n
                n += 1
        elif symbol.type == 'connective':
            for connective in self.connectives:
                if isinstance(symbol, connective):
                    return self.n_tags + self.n_predicates + n
                n += 1
        elif symbol.type == 'function':
            for function in self.functions:
                if isinstance(symbol, function):
                    return self.n_tags + self.n_predicates + self.n_connectives + n
                n += 1
        elif symbol.type == 'constant':
            for constant in self.constants:
                if symbol.name == constant.name:
                    return self.n_tags + self.n_predicates + self.n_connectives + self.n_functions + n
                n += 1
    
    def encode(self, rule):
        head = rule.head
        idx = [self.symbol2idx(head)]
        if len(rule.root.children) > 0:
            root = rule.root.children[0]
            for symbol in root.LDR(ls=[]):
                idx.append(self.symbol2idx(symbol))
            idx = list(filter(None, idx))
        return idx