class calc:
    def __init__(self,first,second):
        self.first=first
        self.second=second

    #self.first+self.second
    def add(self):
        return self.first+self.second
    def sub(self):
        return self.first-self.second
    def mul(self):
        return self.first * self.second
    def div(self):
        q=self.first//self.second
        r=self.first%self.second
        return q,r
    
a=calc(2,3)
#a.set(2,3)
print("add:",a.add())
print("sub:",a.sub())
print("mul:",a.mul())
print("div:",a.div())
    