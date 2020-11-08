import socket
from Crypto.Cipher import AES

KM_ADDRESS = '192.168.56.1'
B_ADDRESS = '192.168.56.1'
KM_PORT = 8090
B_PORT = 9090
IV = str.encode('1234567890abcdef')
BLOCK_SIZE = 16
PADDING = chr(0)
FILE_PATH = r'C:\Users\scurt\Desktop\output.txt'


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


#server setting-up
serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv.bind((B_ADDRESS, B_PORT))
serv.listen()

# get K3 from KM
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((KM_ADDRESS, KM_PORT))
K3 = client.recv(16)
print('K3: ', K3)
client.close()

#getting the mode from A
client, addr = serv.accept()
print('Got connection from ', addr)
MODE = client.recv(4).decode()
print('Received mode: ', MODE)
client.close()

#confirming to A 
client, addr = serv.accept()
message = 'OK'
client.send(message.encode())
print('Sent ok to A')
client.close()

#receiving key 

with open(FILE_PATH, "wb+") as file:
    print("Mode " + MODE)
    if MODE == 'CBC':
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((KM_ADDRESS, KM_PORT))
        K1 = client.recv(16)
        print('K1: ', K1)
        client.close()

        client, addr = serv.accept()
        encrypted_block = client.recv(BLOCK_SIZE)

        while(len(encrypted_block) != 0):
            print("Got the following message : ", end="")
            print(encrypted_block)

            decrypted_block = decrypt(encrypted_block, K1)
            decrypted_block = byte_xor(IV, decrypted_block)
            print(decrypted_block)
            file.write(decrypted_block)
            IV = encrypted_block
            encrypted_block = client.recv(BLOCK_SIZE)
            client.close()

    elif MODE == "OFB":
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((KM_ADDRESS, KM_PORT))
        K2 = client.recv(16)
        print('K2: ', K2)
        client.close()
        client, addr = serv.accept()
        block = client.recv(BLOCK_SIZE)

        while len(block) != 0:
            print("received this : ", end="")
            print(block)
            cipher_block = encrypt(IV, K2)
            xor_block = byte_xor(cipher_block, block)
            file.write(xor_block)
            IV = cipher_block
            block = client.recv(BLOCK_SIZE)
        client.close()

        

#client.close()

