import pickle
import socket

from src.Utils import parse_recv, manageBuffer

BUFFER = 128
PORT = 8000
def setupSocket():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_ip = socket.gethostbyname("localhost")
    s.connect((server_ip, PORT))
    return s 

s = setupSocket()
rs = manageBuffer(BUFFER, s)
print("Connection:", rs)


class Wallet(object):
    def __init__(self, name, address, priv):
        self.name = name
        self.address = address
        self.priv = priv
        self.balance = 0

    def saveWallet(self):
        with open("wallets/" + self.name + ".wallet", "wb") as f:
            pickle.dump(self, f)

    def getBalance(self):
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

    def createAddress(self):
        request = "CREATE_ADDRESS: " + self.address + ";\n"
        s.send(request.encode())
        res = manageBuffer(BUFFER, s)
        del res

    def closeConnection(self):
        s.send("EXIT:;\n".encode())
        s.close()

    def sendTransaction(self, receiver, amount):
        self.getBalance()
        if amount <= self.balance:
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

