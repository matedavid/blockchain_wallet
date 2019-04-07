from flask import Flask, render_template, request
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
    - wallet address (for security)
    - receiver address
    - amount to send
}
"""

app = Flask(__name__)

# Setup socket
PORT = 8000
server_ip = getLocalHostName()
s = setupSocket(server_ip, PORT, connect=False)

# Wallet selected in server
currentWallet = None

def connectSocket(s):
    s.connect((server_ip, PORT))
    _ = manageBuffer(BUFFER, s)
    return s

def close(s):
    s.send("EXIT:;\n".encode())
    s.shutdown(socket.SHUT_WR)
    s.close()
    s = setupSocket(server_ip, PORT, connect=False)
    return s


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
        _ = currentWallet.getBalance(sock)
        close(sock)
        return render_template('wallet.html', wallet=currentWallet,title=currentWallet.name)
    else:
        close(s)
        return "<h1>Wallet does not exist</h1><a href='/'>Return to home</a>"

@app.route("/transaction", methods=["POST"])
def transaction():
    pass

if __name__ == "__main__":
    _ = connectSocket(s)
    s = close(s)
    app.run(debug=True)
