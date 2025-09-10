import hashlib
from ECDSA import *

class transaction:
    def __init__(self, fromAddr,toAddr, amount):
        self.fromAddr = fromAddr #str
        self.toAddr = toAddr #str
        self.amount = amount #int
        self.data = fromAddr+toAddr+hex(amount)[2:]
        self.sig =''