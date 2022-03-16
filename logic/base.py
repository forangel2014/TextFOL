from abc import ABCMeta, abstractmethod

class Node():

    def __init__(self, n_args=1, father=None, state=None):
        self.children = []
        self.father = father
        self.state = state
        self.n_args = n_args

    def LDR(self, ls=[]):
        ls.append(self)
        for child in self.children:
            child.LDR(ls)
        return ls


class Variable(Node):
    '''Variable'''
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.type = 'variable'
        self.instance = None

    def __str__(self):
        return self.name
    
    def __call__(self):
        if self.instance == None:
            print("not grounded yet")
            raise Exception
        else:
            return self.instance

    def bind(self, ins):
        self.instance = ins


class Constant(Node):
    '''Constant'''

    def __init__(self, name):
        super().__init__()
        self.name = name
        self.type = 'constant'

    def __str__(self):
        return '\"' + self.name + '\"'

    def __call__(self):
        return self.name


class Predicate(Node):

    __metaclass__ = ABCMeta

    def __init__(self, name, n_args):
        super().__init__()
        self.name = name
        self.type = 'predicate'
        self.n_args = n_args
        self.named_args = []
        for i in range(self.n_args):
            self.named_args.append('x_' + str(i))

    @abstractmethod
    def funtion(self):
        pass

    def __str__(self):
        #string = self.symbol + '('
        args = self.children + self.named_args[len(self.children):]
        return '%s(%s)' % (self.name, ','.join([str(arg) for arg in args]))

    def __call__(self):
        terms = self.children
        if len(terms) != self.n_args:
            print("wrong number of arguments")
            raise Exception
        else:
            ts = []
            for t in terms:
                ts.append(t())
            return self.function(ts) 

class Connective(Node):

    __metaclass__ = ABCMeta

    def __init__(self, name, n_args):
        super().__init__()
        self.name = name
        self.type = 'connective'
        self.n_args = n_args
        self.named_args = []
        for i in range(self.n_args):
            self.named_args.append('x_' + str(i))

    @abstractmethod
    def funtion(self):
        pass

    def __str__(self):
        #string = self.symbol + '('
        args = self.children + self.named_args[len(self.children):]
        return '%s(%s)' % (self.name, ','.join([str(arg) for arg in args]))

    def __call__(self):
        terms = self.children
        if len(terms) != self.n_args:
            print("wrong number of arguments")
            raise Exception
        else:
            ts = []
            for t in terms:
                ts.append(t())
            return self.function(ts) 

class Function(Node):

    __metaclass__ = ABCMeta

    def __init__(self, name, n_args):
        super().__init__()
        self.name = name
        self.type = 'function'
        self.n_args = n_args
        self.named_args = []
        for i in range(self.n_args):
            self.named_args.append('x_' + str(i))

    @abstractmethod
    def funtion(self):
        pass

    def __str__(self):
        #string = self.symbol + '('
        args = self.children + self.named_args[len(self.children):]
        return '%s(%s)' % (self.name, ','.join([str(arg) for arg in args]))

    def __call__(self):
        terms = self.children
        if len(terms) != self.n_args:
            print("wrong number of arguments")
            raise Exception
        else:
            ts = []
            for t in terms:
                ts.append(t())
            return self.function(ts) 
