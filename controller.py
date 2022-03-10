from base import *
from rule import *
import random

class Controller():

    def __init__(self, predicates, connectives, functions, constants, tags):

        self.state = 'SelectSentence'
        self.state_set = ['SelectSentence', 'SelectTerm', 'SelectPredicates', 'SelectFunction', 'SelectConstants', 'SelectConnectives', 'SelectHead']
        self.predicates = predicates
        self.connectives = connectives
        self.functions = functions
        self.constants = constants
        self.tags = tags

    def random_select(self, ls):
        while type(ls) == list:
            ls = random.sample(ls, 1)[0]
        return ls

    def random_generate_atom(self, node, vars):
        print("node now:" + str(node))
        print("state:" + self.state)
        valid_actions = self.valid_action()
        for _ in range(node.n_args):
            action = self.random_select(valid_actions)
            if not (isinstance(action, Constant) or isinstance(action, Variable)):
                action = action()
            node.children.append(action)
            action.father = node
            state = self.state_transition(action)
            action.state = state
            if state != 'RETURN':
                self.state = state
                vars = self.random_generate_atom(action, vars)
            elif action.type == 'variable' and action not in vars:
                vars.append(action)
        self.state = node.father.state
        return vars

    def random_generate_rule(self):
        valid_actions = self.valid_action()
        first = Node(father=None, state='BEGIN')
        self.state = 'SelectSentence'
        root = self.random_select(valid_actions)()
        root.father = first
        root.state = self.state
        node = root
        vars = []
        vars = self.random_generate_atom(node, vars)
        head = self.random_select(self.tags)
        rule = TCRule(root, vars, head)
        return rule

    def valid_action(self):
        # state -> valid action:
        # SelectSentence -> connectives, predicates
        # SelectTerm -> functions, constants, variables
        # SelectHead -> tags
        valid_actions = {'SelectSentence': [self.connectives, self.predicates], #learn to choose
                         'SelectTerm': [self.functions, [Variable('x')]], #learn to choose
                          'SelectConstant': self.constants}
        return valid_actions[self.state]

    def state_transition(self, action):
        # transitions:
        # SelectSentence -> connectives -> SelectSentence
        # SelectSentence -> predicates -> SelectTerm
        # SelectTerm -> functions -> SelectTerm
        # SelectTerm -> constants/variables -> RETURN
        if self.state == 'SelectSentence':
            if action.type == 'connective':
                return 'SelectSentence'
            elif action.type == 'predicate':
                if action.name == '==' and len(action.children) == 1:
                    return 'SelectConstant'
                else:
                    return 'SelectTerm'
        elif self.state == 'SelectTerm':
            if action.type == 'function':
                return 'SelectTerm'
            elif action.type == 'constant' or action.type == 'variable':
                return 'RETURN'
        elif self.state == 'SelectConstant':
            return 'RETURN'
    
    def rule_eg(self):
        vars = []
        root = self.connectives[0]()

        root1 = self.predicates[0]()

        child1 = self.functions[0]()
        x = Variable('x')
        child1.children.append(x)
        vars.append(x)

        child2 = Constant('how')
        root1.children.append(child1)
        root1.children.append(child2)

        root2 = self.predicates[0]()

        child25 = self.functions[0]()
        child3 = self.functions[3]()

        child3.children.append(x)
        child25.children.append(child3)

        child4 = Constant('did')
        root2.children.append(child25)
        root2.children.append(child4)        

        root.children.append(root1)
        root.children.append(root2)

        head = self.tags[0]
        
        idx = self.functions[1]()
        idx.children.append(x)
        #idxs = [idx, idx]
        idxs = None

        rule = TCRule(root, vars, head)

        return rule