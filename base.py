from abc import ABCMeta, abstractmethod

class Node():

    def __init__(self, father=None, state=None):
        self.children = []
        self.father = father
        self.state = state

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
        if self.children == []:
            return '%s(%s)' % (self.name, ','.join(self.named_args))
        else:
            return '%s(%s)' % (self.name, ','.join([str(child) for child in self.children]))

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
        if self.children == []:
            return '%s(%s)' % (self.name, ','.join(self.named_args))
        else:
            return '%s(%s)' % (self.name, ','.join([str(child) for child in self.children]))

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
        if self.children == []:
            return '%s(%s)' % (self.name, ','.join(self.named_args))
        else:
            return '%s(%s)' % (self.name, ','.join([str(child) for child in self.children]))

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


class Atom():

    def __init__(self, predicate, args):
        if len(args) != predicate.n_args:
            print("wrong number of arguments")
            raise Exception
        else:
            self.predicate = predicate
            self.args = [str(arg) for arg in args]

    def __str__(self):
        return '%s(%s)' % (self.predicate.name, ','.join(self.args))

if __name__ == '__main__':
    equ = Predicate('==', 2, lambda x: x[0]==x[1])
    one = Constant('1')
    times2 = Function('*2', 1, lambda x: '2')
    two = Constant('2')
    equ12 = Atom(equ,[times2([one]),two])
    print(str(equ12))
