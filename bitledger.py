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


    def isTransValid(self, pub):