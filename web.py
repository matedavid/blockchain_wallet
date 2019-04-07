from flask import Flask, render_template
import os

from src.Wallet import Wallet
from src.Utils import generate_key_pair, loadWallet

"""
/ = display wallets; if exists, ask to load or to create, else, only create GET
/create = create a wallet GET, POST
/wallet/<walletname> = load given wallet GET
/delete/<walletname> = delete given wallet POST
/trainsaction = send transaction POST
"""

app = Flask(__name__)

currentWallet = None

@app.route("/")
def index():
    wallets = os.listdir('wallets')
    return render_template('index.html', wallets=wallets, title="Home")

@app.route("/wallet/<name>")
def wallet(name):
    path = f"wallets/{name}.wallet"
    if os.path.isfile(path):
        currentWallet = loadWallet((name+".wallet"))
        _ = currentWallet.getBalance()
        return render_template('wallet.html', wallet=currentWallet,title=currentWallet.name)
    else:
        return "<h1>Wallet does not exist</h1><a href='/'>Return to home</a>"

if __name__ == "__main__":
    app.run(debug=True)
