from base import Connective

class Conjuct(Connective):

    def __init__(self):
        super().__init__('and', 2)
    
    def function(self, bools):
        return bools[0] and bools[1]

class Disjuct(Connective):
    
    def __init__(self):
        super().__init__('or', 2)

    def function(self, bools):
        return bools[0] or bools[1]

class Negate(Connective):
    
    def __init__(self):
        super().__init__('not', 1)

    def function(self, bools):
        return not bools[0]

connectives = [Conjuct, Disjuct, Negate]