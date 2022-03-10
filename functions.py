from base import Function

class TokenString(Function):
    
    def __init__(self):
        super().__init__('TokenString', 1)
    
    def function(self, token):
        return token[0].string

class TokenIdx(Function):
    
    def __init__(self):
        super().__init__('TokenIdx', 1)
    
    def function(self, token):
        return token[0].idx

class PreToken(Function):

    def __init__(self):
        super().__init__('PreToken', 1)

    def function(self, token):
        return token[0].preToken

class PostToken(Function):

    def __init__(self):
        super().__init__('PostToken', 1)

    def function(self, token):
        return token[0].postToken

class POSTag(Function):
    
    def __init__(self):
        super().__init__('POSTag', 1)

    def function(self, token):
        return token[0].POSTag

functions = [TokenString, TokenIdx, PreToken, PostToken, POSTag]