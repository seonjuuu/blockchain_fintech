import hashlib
from ECDSA import *

class transaction:
    def __init__(self, fromAddr,toAddr, amount):
        self.fromAddr = fromAddr #str
        self.toAddr = toAddr #str
        self.amount = amount #int
        self.data = fromAddr+toAddr+hex(amount)[2:]
        self.sig =''

    def signTransaction(self,priv):
        r,s = ecdsa_siggen(self.data,priv)
        self.sig = hex(r)[2:]+hex(s)[2:]
        self.rlen = len(hex(r)[2:])
        self.slen = len(hex(s)[2:])