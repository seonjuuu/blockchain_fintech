import hashlib
from ECDSA import *

class transaction:

    # 송신자, 수신자, 금액을 입력받아 트랜잭션 데이터 생성
    def __init__(self, fromAddr,toAddr, amount):
        self.fromAddr = fromAddr #str
        self.toAddr = toAddr #str
        self.amount = amount #int
        self.data = fromAddr+toAddr+hex(amount)[2:]
        self.sig =''

    # 개인 키를 사용해 트랜잭션에 ECDSA 서명을 생성
    def signTransaction(self,priv):
        r,s = ecdsa_siggen(self.data,priv)
        self.sig = hex(r)[2:]+hex(s)[2:]
        self.rlen = len(hex(r)[2:])
        self.slen = len(hex(s)[2:])


    # 공개 키로 트랜잭션의 서명을 검증
    def isTransValid(self, pub):
        if len(self.sig) == 0:
            print('no signature')
            return 0
        
        r = int(self.sig[:self.rlen],16)%n
        s = int(self.sig[self.rlen:],16)%n

        qx = pub[:44]
        qy = pub[44:]

        qx = base58_to_hex(qx)
        qy = base58_to_hex(qy)

        qx = int(qx, 16)%n
        qy = int(qy, 16)%n

        if ecdsa_verify(self.data, r, s, qx, qy) == 0:
            return 0

        return 1
        
        
        ####(r,s)->검증
        # r = self.sig[:self.rlen] -> integer
        # s = self.sig[sig.rlen:] -> integer
        # pub -> base58로 인코딩되어있는것을 다시 디코딩 / qx,qy 분해해서 넣어줌
        #if ecdsa_verify(self.data,r,s,qx,qy)==0:
        # 검증실패        
        # return 0 


class block:
    def __init__(self,timestamp,trans,prehash):
        self.timestamp = timestamp
        self.trans = trans
        self.prehash = prehash
        self.nonce=0
        self.hash = self.calchash()


    # 현재 블록의 해시값(SHA256)을 계산
    def calchash(self):
        #전체 string이라 가정
        nstr = hex(self.nonce)
        nstr = nstr[2:]

        data = ''
        for i in self.trans:
            data = data + i.data
            
        msg=self.timestamp+data+self.prehash+nstr
        msg=msg.encode()
        msg=hashlib.sha256(msg).hexdigest()

        return msg
    

    def merkleroot(self):