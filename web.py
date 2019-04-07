from flask import Flask, render_template
from src.Wallet import Wallet

from src.Wallet import Wallet
from src.Utils import generate_key_pair, load_wallet

"""
/ = display wallets; if exists, ask to load or to create, else, only create GET
/create = create a wallet GET, POST
/wallet/<walletname> = load given wallet GET
/delete/<walletname> = delete given wallet POST
/trainsaction = send transaction POST
"""

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
