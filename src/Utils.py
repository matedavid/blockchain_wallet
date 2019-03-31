import secrets

# Function that generates new public and private keys
def generate_key_pair():
    bits = secrets.randbits(256)
    publ_key = hex(bits)

    priv_key = publ_key[2:]

    #print(publ_key)
    #print(priv_key)

    return publ_key, priv_key
