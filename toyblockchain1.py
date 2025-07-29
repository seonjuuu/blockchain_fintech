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
    #초기화(해시계산)
    def __init__(self,timestamp,data,prehash):
        self.timestamp = timestamp
        self.data = data
        self.prehash = prehash
        self.nonce=0
        self.hash = self.calchash()

    #채굴 과정
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

    #SHA-256 해시값 계산
    def calchash(self):
        #전체 string이라 가정
        nstr = hex(self.nonce)
        nstr = nstr[2:]
        msg=self.timestamp+self.data+self.prehash+nstr
        msg=msg.encode()
        msg=hashlib.sha256(msg).hexdigest()

        return msg
    

class blockchain:
    #제네시스 블록을 생성하고 체인을 초기화
    def __init__(self):
        self.chain=[]
        gen_block = block('231111','genesis','0')
        gen_block.mineblock(4)
        self.chain.append(gen_block)
        self.len =1

    #현재 체인에서 가장 마지막 블록을 반환 
    def getlatestblock(self):
        return self.chain[self.len-1]
    
    #새 블록을 생성하고 체인에 추가 (이전 블록의 해시값 연결)
    def addBlock(self,timestamp,data,difficulty):
        newblock = block(timestamp,data,'')
        newblock.prehash = self.getlatestblock().hash
        newblock.mineblock(difficulty)
        self.chain.append(newblock)
        self.len = self.len +1

    def isChainValid(self):
    