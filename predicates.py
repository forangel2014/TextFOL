from base import Predicate

class Equal(Predicate):

    def __init__(self):
        super().__init__('==', 2)

    def function(self, strs):
        return strs[0]==strs[1]

class Before(Predicate):
    
    def __init__(self):
        super().__init__('before', 2)
    
    def function(self, tokens):
        return tokens[0].idx < tokens[1].idx

class After(Predicate):
    
    def __init__(self):
        super().__init__('after', 2)
    
    def function(self, tokens):
        return tokens[0].idx > tokens[1].idx

predicates = [Equal, Before, After]
