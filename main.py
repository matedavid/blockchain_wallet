import socket
import os
import pickle

from src.Wallet import Wallet
from src.Utils import generate_key_pair

def loadWallet(name):
    with open(name, "rb") as f:
        wallet = pickle.load(f)
    return wallet

def createNewWallet():
    name = input("Name of your new wallet")
    if name not in os.listdir('wallets'):
        publ, priv = generate_key_pair()
        wallet = Wallet(name, publ, priv)
        wallet.saveWallet()
        return wallet
    else: 
        print("Name of the wallet already exists")
        return createNewWallet()

if __name__ == '__main__':
    wallet = None
    wallets = os.listdir('wallets')
    if len(wallets) <= 0:
        res = input("You don't own any wallets, create a new one?: ")
        if res.lower() == "y" or res.lower() == "yes":
            wallet = createNewWallet()
    else:
        res = input("Do you want to create a new wallet or load an existing one?: (c, l) ")
        if res.lower() == "l":
            for wallet in range(len(wallets)):
                print(wallet, "-", wallets[wallet])
            num = input("What wallet do you want to load? ")
            if num > 0 and num < len(wallets)-1:
                wallet = loadWallet(wallets[num])
        else:
            wallet = createNewWallet()

    # Create infinite loop to listen for actions
    while True:
        break
    

    