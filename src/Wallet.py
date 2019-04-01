import pickle
import socket

from src.Utils import parse_recv, manageBuffer

BUFFER = 128

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_ip = socket.gethostbyname("localhost")
port = 8000

s.connect((server_ip, port))
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
            self.balance = float(options[0])
        elif command == "ADDRESS_EXISTS":
            print("Address already exists")
        elif command == "REQUEST_INPUT_ERROR":
            self.createWallet()
            self.getBalance()

    def createWallet(self):
        request = "CREATE_ADDRESS: " + self.address + ";\n"
        s.send(request.encode())
        res = manageBuffer(BUFFER, s)
        del res