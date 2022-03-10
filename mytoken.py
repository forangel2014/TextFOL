class Token():

    def __init__(self, idx, string, POSTag):
        self.idx = idx
        self.string = string
        self.POSTag = POSTag
        self.preToken = None
        self.postToken = None
    
    def link(self, preToken, postToken):
        self.preToken = preToken
        self.postToken = postToken