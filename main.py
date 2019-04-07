import socket
import os
import pickle

from src.Wallet import Wallet
from src.Utils import generate_key_pair, commandsHelp, setupSocket, getLocalHostName, manageBuffer, BUFFER

PORT = 8000
server_ip = getLocalHostName()

s = setupSocket(server_ip, PORT)
_ = manageBuffer(BUFFER, s)


def loadWallet(name):
    with open("wallets/" + name, "rb") as f:
        wallet = pickle.load(f)
    wallet.getBalance(s)
    return wallet

def createNewWallet():
    name = input("Name of your new wallet: ")
    if name not in os.listdir('wallets'):
        publ, priv = generate_key_pair()
        wallet = Wallet(name, publ, priv)
        wallet.createAddress(s)
        wallet.getBalance(s)
        wallet.saveWallet()
        return wallet
    else: 
        print("Name of the wallet already exists")
        return createNewWallet()

def askReceiver():
    recv = input("Enter address to send coins: ")
    if recv.lower() == "back":
        return None
    return recv if len(recv) == 66 else askReceiver()

def askAmount():
    amount = input("Amount to send: ")
    try: 
        amount = int(amount)
        return amount
    except:
        print("Amount must be a number")
        return askAmount()

def showWallets(wallets, notShow=[]):
    for wallet in range(len(wallets)):
        walletName = wallets[wallet].split(".")[0] 
        if walletName not in notShow:
            print(wallet, "-", wallets[wallet])

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
            showWallets(wallets)
            num = int(input("What wallet do you want to load?: "))
            if num >= 0 and num <= len(wallets)-1:
                wallet = loadWallet(wallets[num])
        else:
            wallet = createNewWallet()

    # Create infinite loop to listen for actions
    print("Loaded wallet:", wallet.name + "; Balance:", wallet.getBalance(s), "coins")
    while True:
        ask = input("What do you want to do: ").lower()
        if ask == "exit":
            wallet.closeConnection(s)
            print("Closing wallet...")
            break
        elif ask == "balance":
            print("Balance of '{}' wallet: {} coins".format(wallet.name, wallet.getBalance(s)))
        elif ask == "send":
            receiver = askReceiver()
            if (receiver != None):
                amount = askAmount()

                wallet.sendTransaction(receiver, amount, s)

        elif ask == "delete":
            r = input(f"Are you sure you want to delete '{wallet.name}' wallet?: ")
            if r.lower() == "y" or r.lower() == "yes":
                os.system(f'rm wallets/{wallet.name}.wallet')
                print("Wallet deleted succesfully!")
                break

        elif ask == "change":
            showWallets(wallets, [wallet.name])
            r = input("To what wallet do you want to change?: ")
            wallet = loadWallet(wallets[int(r)])
            print(f"\nSuccesfully changed to wallet: {wallet.name}; Balance: {wallet.balance} coins")
 
        elif ask == "info":
            print(wallet.info(s))
        elif ask == "help":
            print(commandsHelp())
        else:
            print(commandsHelp())

    
