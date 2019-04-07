from flask import Flask, render_template, request
import json
import os
import socket

from src.Wallet import Wallet
from src.Utils import generate_key_pair, loadWallet, getLocalHostName, setupSocket, manageBuffer, BUFFER

"""
/ = display wallets; if exists, ask to load or to create, else, only create GET
/create = create a wallet GET, POST
/wallet/<walletname> = load given wallet GET
/delete/<walletname> = delete given wallet POST
/transaction = send transaction POST
{
    - sender address (for security)
    - receiver address
    - amount to send
}
"""

app = Flask(__name__)

# Setup socket
PORT = 8000
server_ip = getLocalHostName()

global s
s = setupSocket(server_ip, PORT, connect=False)

# Wallet selected in server
currentWallet = None

def connectSocket(s):
    s.connect((server_ip, PORT))
    _ = manageBuffer(BUFFER, s)
    return s

def close(sock):
    sock.send("EXIT:;\n".encode())
    sock.shutdown(socket.SHUT_WR)
    return setupSocket(server_ip, PORT, connect=False)


@app.route("/")
def index():
    wallets = os.listdir('wallets')
    return render_template('index.html', wallets=wallets, title="Home")

@app.route("/wallet/<name>")
def wallet(name):
    sock = connectSocket(s)
    path = f"wallets/{name}.wallet"
    if os.path.isfile(path):
        globals()['currentWallet'] = loadWallet((name+".wallet"), sock)
        print(currentWallet.balance)
        _ = currentWallet.getBalance(sock)
        # TODO: fix complaint 's not defined' in line 51 when only using s as the variable 
        globals()['s'] = close(sock)
        return render_template('wallet.html', wallet=currentWallet,title=currentWallet.name)
    else:
        close(s)
        return "<h1>Wallet does not exist</h1><a href='/'>Return to home</a>"

@app.route("/transaction", methods=["POST"])
def transaction():
    sock = connectSocket(s)
    req = request.get_data().decode()
    data = json.loads(req)
    sender, receiver, amount = data['sender'], data['receiver'], float(data['amount'])
    print(amount, currentWallet.balance)
    if sender != "" and sender != " " and sender != None and len(sender) == 66:
        if receiver != "" and receiver != " " and receiver != None and len(receiver) == 66:
            if amount > 0 and amount <= currentWallet.balance:
                print("All ok")
                globals()['currentWallet'].sendTransaction(receiver, amount, sock)
            else:
                globals()['s'] = close(sock)
                return "Amount not valid"
        else:
            globals()['s'] = close(sock)
            print("Receiver not valid")
            return "Receiver not valid"
    else:
        globals()['s'] = close(sock)
        print("Sender not valid")
        return "Sender not valid"

    globals()['s'] = close(sock)
    return "Success"

if __name__ == "__main__":
    _ = connectSocket(s)
    s = close(s)
    app.run(debug=True)
