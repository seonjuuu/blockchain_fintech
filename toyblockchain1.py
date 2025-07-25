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

############################ 

import hashlib
class block:
    def __init__(self,timestamp,data,prehash):
        self.timestamp = timestamp
        self.data = data
        self.prehash = prehash
        self.nonce=0
        self.hash = self.calchash()

    def mineblock(self,difficulty):
        start=0
        prefix = self.timestamp+self.data+self.prehash
        msg = prefix+'0'
        msg = msg.encode()
        msg = hashlib.sha256(msg).hexdigest()
        
        cmp=''
        for i in range(0,difficulty):
            cmp = cmp+'0' #if difficulty=4 -> '0000'
        while (msg[:difficulty]!=cmp):
            start=start+1
            nstr=hex(start)
            nstr = nstr[2:]
            msg = prefix+nstr
            msg = msg.encode()
            msg = hashlib.sha256(msg).hexdigest()
        self.hash = msg
        self.nonce = start

    def calchash(self):
    