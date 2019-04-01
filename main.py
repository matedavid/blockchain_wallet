import socket
import os
import pickle

from src.Wallet import Wallet
from src.Utils import generate_key_pair, commandsHelp

def loadWallet(name):
    with open("wallets/" + name, "rb") as f:
        wallet = pickle.load(f)
    wallet.getBalance()
    return wallet

def createNewWallet():
    name = input("Name of your new wallet: ")
    if name not in os.listdir('wallets'):
        publ, priv = generate_key_pair()
        wallet = Wallet(name, publ, priv)
        wallet.createAddress()
        wallet.getBalance()
        wallet.saveWallet()
        return wallet
    else: 
        print("Name of the wallet already exists")
        return createNewWallet()

def askReceiver():
    recv = input("Enter address to send coins: ")

    return recv if len(recv) == 66 else askReceiver()

def askAmount():
    amount = input("Amount to send: ")
    try: 
        amount = int(amount)
        return amount
    except:
        print("Amount must be a number")
        return askAmount()

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
            num = int(input("What wallet do you want to load?: "))
            if num >= 0 and num <= len(wallets)-1:
                wallet = loadWallet(wallets[num])
        else:
            wallet = createNewWallet()

    # Create infinite loop to listen for actions
    print("Loaded wallet:", wallet.name + "; Balance:", wallet.balance, "coins")
    while True:
        ask = input("What do you want to do: ").lower()
        if ask == "exit":
            wallet.closeConnection()
            print("Closing wallet...")
            break
        elif ask == "balance":
            print("Balance of '{}' wallet: {} coins".format(wallet.name, wallet.balance))
        elif ask == "send":
            receiver = askReceiver()
            amount = askAmount()

            wallet.sendTransaction(receiver, amount)
        elif ask == "help":
            print(commandsHelp())
        else:
            print(commandsHelp())

    