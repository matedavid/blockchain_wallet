import secrets
import socket
import pickle

BUFFER = 128

# Function that generates new public and private keys
def generate_key_pair():
    bits = secrets.randbits(256)
    publ_key = hex(bits)

    priv_key = publ_key[2:]

    return publ_key, priv_key

# Parses the receiver response from the blockchain to get command and options
def parse_recv(response):
    command = ""
    options = []
    lastLetter = 0    

    for letter in range(len(response)):
        
        if response[letter] == ":":
            command = response[0:letter]
            letter += 1
            lastLetter = letter + 1
        elif response[letter] == ";":
            options.append(response[lastLetter: letter])
            letter += 1
            lastLetter = letter
        elif response[letter] == " ":
            continue

        # lastLetter = letter

    return command, options

# Manager the buffer of the received message 
def manageBuffer(buffer, s):
    result = s.recv(buffer)
    
    res = result.decode()
    while res[len(result) - 1] != ";":
        try: 
            p = res[len(result)]
            del p
        except: 
            return result.decode()

        # print(result.decode())
        result += s.recv(buffer)
        
    return result.decode()

# Displays the commands for the cli version
def commandsHelp():
    hp = "Commands:\n"
    hp += "  - help display commands and information\n"
    hp += "  - exit exists the program\n"
    hp += "  - send send specified <amount> to specified <address>\n"
    hp += "  - balance gets the balance of current wallet\n"
    return hp


def getLocalHostName():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    sock = s.getsockname()[0]
    s.close()
    return sock

def loadWallet(name, s):
    with open("wallets/" + name, "rb") as f:
        wallet = pickle.load(f)
        wallet.getBalance(s)
    return wallet

def setupSocket(server_ip, PORT, connect=True):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(f"Listening on {server_ip}:{PORT}")
    if connect:
        s.connect((server_ip, PORT))
    return s 