import pickle
import socket

from src.Utils import parse_recv, manageBuffer, getLocalHostName

BUFFER = 128
PORT = 8000
server_ip = getLocalHostName()

"""
def setupSocket():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(f"Listening on {server_ip}:{PORT}")
    s.connect((server_ip, PORT))
    return s 
"""

# s = setupSocket()
# rs = manageBuffer(BUFFER, s)
# print("Connection:", rs)


class Wallet(object):
    def __init__(self, name, address, priv):
        self.name = name
        self.address = address
        self.priv = priv
        self.balance = 0

    def getSocket(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((server_ip, PORT))
        rs = manageBuffer(BUFFER, s)
        del rs
        return s

    def closeConnection(self, s):
        s.send("EXIT:;\n".encode())

    def saveWallet(self):
        with open("wallets/" + self.name + ".wallet", "wb") as f:
            pickle.dump(self, f)

    def getBalance(self):
        s = self.getSocket()
        request = "GET_BALANCE: " + self.address + ";\n"
        s.send(request.encode())
        res = manageBuffer(BUFFER, s)

        command, options = parse_recv(res)

        if command == "SUCCESS":
            if self.balance != float(options[0]):
                self.saveWallet()
            self.balance = float(options[0])
        elif command == "ADDRESS_EXISTS":
            print("Address already exists")
        elif command == "REQUEST_INPUT_ERROR":
            self.createAddress()
            self.getBalance()

        self.closeConnection(s)
        return self.balance

    def createAddress(self):
        s = self.getSocket()

        request = "CREATE_ADDRESS: " + self.address + ";\n"
        s.send(request.encode())
        res = manageBuffer(BUFFER, s)
        del res

        self.closeConnection(s)

    

    def info(self):
        return f"Name: {self.name}\nBalance: {self.getBalance()}\nAddress: {self.address}"

    def sendTransaction(self, receiver, amount):
        s = self.getSocket()

        self.getBalance()
        if receiver == self.address:
            print("Address inputed is same address as wallet: aborting")
        elif amount <= self.balance and receiver != self.address:
            request = "CREATE_TRANSACTION: {}; {}; {};".format(self.address, receiver, float(amount))
            s.send(request.encode())
            res = manageBuffer(BUFFER, s)

            command, options = parse_recv(res)
            if command == "SUCCESS":
                print("Transaction sended succesfully")
                self.getBalance()
            else:
                print("[ERROR]: " + command)
                
        else:
            print("[ERROR]: Not enough funds")

        self.closeConnection(s)