import socket
from Crypto.Cipher import AES

#change the mode from here
MODE = 'OFB'
KM_ADDRESS = '192.168.56.1'
B_ADDRESS = '192.168.56.1'
KM_PORT = 8090
B_PORT = 9090
FILE_PATH = r'C:\Users\scurt\Desktop\input.txt'
IV = str.encode('1234567890abcdef')
BLOCK_SIZE = 16
PADDING = chr(0)
ok = False

def pad(x):
    if len(x) % BLOCK_SIZE != 0:
        if isinstance(x, (bytes, bytearray)):
            x = x.decode()
        return x + ((BLOCK_SIZE - len(x) % BLOCK_SIZE) - 1) * PADDING + (chr(BLOCK_SIZE - len(x) % BLOCK_SIZE))
    return x

def byte_xor(byte_array1, byte_array2):
    result = bytearray()
    for b1, b2 in zip(byte_array1, byte_array2):
        result.append(b1 ^ b2)
    return bytes(result)

def encrypt(text, key):
    cipher = AES.new(key, AES.MODE_CFB, iv = IV)
    encrypted_text = cipher.encrypt(text)
    return encrypted_text

def decrypt(encrypted_text, key):
    cipher = AES.new(key, AES.MODE_CFB, iv = IV)
    return cipher.decrypt(encrypted_text)


# get K3 from KM

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((KM_ADDRESS, KM_PORT))
K3 = client.recv(16)
print('K3: ', K3)
client.close()

#communicating the encrypted mode to KM, B
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((KM_ADDRESS, KM_PORT))
client.send(MODE.encode('utf-8'))
print('A sent the mode to KM:', MODE)
client.close()
#B
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((B_ADDRESS, B_PORT))
client.send(MODE.encode('utf-8'))
print('A sent the mode to B:', MODE)
client.close()

# receiving confirmation from B
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((B_ADDRESS, B_PORT))
message = client.recv(2).decode()
print('B said ', message)
client.close()

#receiving key 
if MODE == 'CBC':
    print('s')
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((KM_ADDRESS, KM_PORT))
    K1 = client.recv(16)
    client.close()
    print('K1: ', K1)
    ok = True
elif MODE == 'OFB':
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((KM_ADDRESS, KM_PORT))
    K2 = client.recv(16)
    client.close()
    print('K2: ', K2)
    ok = True


#start communication
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((B_ADDRESS, B_PORT))

if ok == True:
    with open(FILE_PATH, 'rt+') as file:
        if MODE == 'CBC':
            block = file.read(BLOCK_SIZE)
            while len(block) != 0:
                block = pad(block)
                xor = byte_xor(IV, str.encode(block))
                encrypted_block = encrypt(xor, K1)
                client.send(encrypted_block)
                print('A sent: ', encrypted_block)
                IV = encrypted_block
                block = file.read(BLOCK_SIZE)
        elif MODE == 'OFB':
            block = file.read(BLOCK_SIZE)
            prev_cipher_block = IV
            while len(block) != 0:
                block = pad(block)
                cipher_block = encrypt(IV, K2)
                xor = byte_xor(str.encode(block), cipher_block)
                client.send(xor)
                print('A sent: ', xor)
                IV = cipher_block
                block = file.read(BLOCK_SIZE)

client.close()

