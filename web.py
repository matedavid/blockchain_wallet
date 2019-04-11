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

def createWallet(name, s):
    if name not in os.listdir('wallets'):
        publ, priv = generate_key_pair()
        wallet = Wallet(name, publ, priv)
        wallet.createAddress(s)
        _ = wallet.getBalance(s)
        wallet.saveWallet()
        return True, wallet

    else:
        return False, "Name of the wallet already exists"


@app.route("/")
def index():
    wallets = os.listdir('wallets')
    return render_template('index.html', wallets=wallets, title="Home")

@app.route("/wallet/<name>")
def wallet(name):
    sock = connectSocket(s)
    path = f"wallets/{name}.wallet"
    if os.path.isfile(path):
        currentWallet = loadWallet((name+".wallet"), sock)
        print(currentWallet)
        _ = currentWallet.getBalance(sock)

        # TODO: fix complaint 's not defined' in line 51 when only using s as the variable 
        globals()['s'] = close(sock)
        return render_template('wallet.html', wallet=currentWallet,title=currentWallet.name)
    else:
        globals()['s'] = close(s)
        return "<h1>Wallet does not exist</h1><a href='/'>Return to home</a>"

# TODO: change current validation methoq and enable repsonse to javascript make the change without having to refresh 
@app.route("/transaction", methods=["POST"])
def transaction():
    sock = connectSocket(s)
    req = request.get_data().decode()
    data = json.loads(req)
    name, sender, receiver, amount = data['name'], data['sender'], data['receiver'], float(data['amount'])

    currentWallet = loadWallet("{}.wallet".format(name), sock)
    
    if receiver == currentWallet.address:
        globals()['s'] = close(sock)
        return json.dumps({'status': False, "message": "Input address is the same as current wallet"})

    if sender != "" and sender != " " and sender != None and len(sender) == 66:
        if receiver != "" and receiver != " " and receiver != None and len(receiver) == 66:
            if amount > 0 and amount <= currentWallet.balance:
                currentWallet.sendTransaction(receiver, amount, sock)
            else:
                globals()['s'] = close(sock)
                return json.dumps({"status": False, "message": "The balance does not have enough funds"})
        else:
            globals()['s'] = close(sock)
            return json.dumps({"status": False, "message": "Receiver not valid"})
    else:
        globals()['s'] = close(sock)
        return json.dumps({"status": False, "message": "Sender not valid"})
    
    newBalance = currentWallet.getBalance(sock)

    globals()['s'] = close(sock)
    return json.dumps({'status': True, "balance": float(newBalance)})

@app.route("/create", methods=["POST"])
def createPost():
    sock = connectSocket(s)
    req = request.get_data().decode() 
    data = json.loads(req)
    print(data)
    
    ok, newWallet = createWallet(data['name'], sock)

    if ok == False:
        globals()['s'] = close(sock)
        return json.dumps({"status": False, "message": newWallet});
    
    currentWallet = newWallet
    globals()['s'] = close(sock)
    return json.dumps({"status": True, "message": ""});

@app.route("/delete/<name>", methods=['POST'])
def delete(name):
    sock = connectSocket(s)

    name = name + ".wallet"
    if name in os.listdir('wallets'):
        try:
            os.remove(f"wallets/{name}")
        except:
            globals()['s'] = close(sock)
            return json.dumps({"status": False, "message": "Error happened while deleting file"})
    else:
        globals()['s'] = close(sock)
        return json.dumps({"status": False, "message": "File name does not exist"})

    globals()['s'] = close(sock)
    return json.dumps({"status": True, "message": ""})

if __name__ == "__main__":
    _ = connectSocket(s)
    s = close(s)
    app.run(debug=True)
