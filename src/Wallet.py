import pickle
import socket

class Wallet(object):
    def __init__(self, name, address, priv):
        self.name = name
        self.address = address
        self.priv = priv
        self.balance = self.getBalance()

    def saveWallet(self):
        with open(self.name + ".wallet", "wb") as f:
            pickle.dump(self, f)

    def getBalance(self):
        balance = 0
        return balance