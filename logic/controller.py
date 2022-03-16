from logic.base import *
from logic.rule import *
import random

class Controller():

    def __init__(self, predicates, connectives, functions, constants, tags):

        self.initialize()

        self.state_set = ['SelectHead', 'SelectSentence', 'SelectTerm', 
                          'SelectPredicate', 'SelectFunction', 'SelectConstant', 'SelectConnective', 'SelectVariable']
        self.predicates = predicates
        self.connectives = connectives
        self.functions = functions
        self.constants = constants
        self.variables = [Variable('x')]
        self.tags = tags

    def initialize(self):
        self.state = 'SelectSentence'
        self.head = None
        self.root = None
        self.node = None
        self.vars = []
        self.rule = None

    def random_select(self, ls):
        while type(ls) == list:
            ls = random.sample(ls, 1)[0]
        return ls

    def random_generate_atom(self, node, vars=[]):
        while len(node.children) < node.n_args:
            valid_actions = self.valid_action()
            if self.state == 'SelectTerm' and node.name == '==' and len(node.children) == 1:
                self.state = 'SelectConstant'
            elif self.state == 'SelectSentence' or self.state == 'SelectTerm':
                action = self.random_select(valid_actions)
                self.state = action
            else:
                action = self.random_select(valid_actions)
                if not (isinstance(action, Constant) or isinstance(action, Variable)):
                    action = action()
                node.children.append(action)
                action.father = node
                next_state = self.state_transition(action)
                action.state = next_state
                if next_state != 'RETURN':
                    self.state = next_state
                    vars = self.random_generate_atom(action, vars)
                else:
                    self.state = 'SelectTerm'
                    if action.type == 'variable' and len(vars) == 0:
                        vars.append(action)
        self.state = node.father.state
        return vars

    def random_generate_rule(self):
        self.initialize()
        head = self.random_select(self.tags)
        first = Node(state='BEGIN')
        root = Node(father=first, state=self.state)
        vars = self.random_generate_atom(root, vars=[])
        rule = TCRule(root, vars, head)
        return rule

    def take_action(self, action):
        if self.state == 'SelectSentence' or self.state == 'SelectTerm':
            self.state = action
        else:
            if not (isinstance(action, Constant) or isinstance(action, Variable)):
                action = action()
            self.node.children.append(action)
            action.father = self.node
            next_state = self.state_transition(action)
            action.state = next_state
            if next_state != 'RETURN':
                self.state = next_state
                self.node = action
                rule = TCRule(self.root, self.vars, self.head, self.state)
                return rule
            else:
                self.state = 'SelectTerm'
                if action.type == 'variable' and len(self.vars) == 0:
                    self.vars.append(action)
            if self.state == 'SelectTerm' and self.node.name == '==' and len(self.node.children) == 1:
                self.state = 'SelectConstant'
            while len(self.node.children) == self.node.n_args:
                self.state = self.node.father.state
                self.node = self.node.father
        rule = TCRule(self.root, self.vars, self.head, self.state)
        return rule

    def init_rule(self):
        self.initialize()
        self.head = self.random_select(self.tags)
        first = Node(state='BEGIN')
        self.root = Node(father=first, state=self.state)
        self.node = self.root
        rule = TCRule(self.root, [], self.head, self.state)
        return rule

    def valid_action(self):
        # state -> valid action:
        # SelectSentence -> connectives, predicates
        # SelectTerm -> functions, constants, variables
        # SelectHead -> tags
        valid_actions = {'SelectHead': self.tags,
                         'SelectSentence': ['SelectConnective', 'SelectPredicate'], #learn to choose
                         'SelectTerm': ['SelectFunction', 'SelectVariable'], #learn to choose
                         'SelectPredicate': self.predicates,
                         'SelectFunction': self.functions,
                         'SelectConnective': self.connectives, 
                         'SelectConstant': self.constants,
                         'SelectVariable': self.variables}
        return valid_actions[self.state]

    def state_transition(self, action):
        # transitions:
        # SelectSentence -> connectives -> SelectSentence
        # SelectSentence -> predicates -> SelectTerm
        # SelectTerm -> functions -> SelectTerm
        # SelectTerm -> constants/variables -> RETURN
        
        if self.state == 'SelectSentence':
            return action

        elif self.state == 'SelectTerm':
            return action

        elif self.state == 'SelectConnective':
            return 'SelectSentence'

        elif self.state == 'SelectPredicate':
            return 'SelectTerm'
        
        elif self.state == 'SelectFunction':
            return 'SelectTerm'

        elif self.state == 'SelectVariable' or 'SelectConstant':
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