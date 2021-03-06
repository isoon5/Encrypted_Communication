import socket
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES
from Crypto import Random
from Crypto.PublicKey import RSA

KM_ADDRESS = '192.168.56.1'
KM_PORT = 8090
B_PORT = 9090
B_ADDRESS = '192.168.56.1'

BLOCK_SIZE = 16
PADDING = chr(0)
IV = str.encode('1234567890abcdef')

K1 = get_random_bytes(16)
K2 = get_random_bytes(16)
K3 = get_random_bytes(16)

#server setting-up
serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv.bind((KM_ADDRESS, KM_PORT))
serv.listen()

#sendind K3 to A and B
for i in [0, 1]:
    conn, addr = serv.accept()
    conn.send(K3)
    print('Sent K3 to ', addr)
    conn.close()

conn, addr = serv.accept()
mode = conn.recv(3)
conn.close()
print('Received mode: ', mode)

if mode == b'CBC':
   #A
  
    cipher = AES.new(K3, AES.MODE_CFB, iv = IV)
    conn, addr = serv.accept()
    cryptedMsg = cipher.encrypt(K1)
    conn.send(cryptedMsg)
    print('Sent K1 to ', addr)
   #B
    conn, addr = serv.accept()
    conn.send(K1)
    print('Sent K1 to ', addr)
    

elif mode == b'OFB':
    #A
    cipher = AES.new(K3, AES.MODE_CFB, iv = IV)
    conn, addr = serv.accept()
    cryptedMsg = cipher.encrypt(K2)
    conn.send(cryptedMsg)
    print('Sent K2 to ', addr)
    #B
    conn, addr = serv.accept()
    conn.send(K2)
    print('Sent K2 to ', addr)



conn.close()





