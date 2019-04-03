import secrets
import socket

# Function that generates new public and private keys
def generate_key_pair():
    bits = secrets.randbits(256)
    publ_key = hex(bits)

    priv_key = publ_key[2:]

    #print(publ_key)
    #print(priv_key)

    return publ_key, priv_key

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


def manageBuffer(buffer, s):
    result = s.recv(buffer)
    
    res = result.decode()
    while res[len(result) - 1] != ";":
        try: 
            p = res[len(result)]
        except: 
            return result.decode()

        # print(result.decode())
        result += s.recv(buffer)
        
    return result.decode()


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