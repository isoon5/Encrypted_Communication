import socket

MODE = 'CBC'
KM_ADDRESS = '192.168.56.1'
B_ADDRESS = '192.168.56.1'
KM_PORT = 8090
B_PORT = 9090
IV = '1234567890abcdef'

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
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((KM_ADDRESS, KM_PORT))
    K1 = client.recv(16)
    client.close()
    print('K1: ', K1)
elif MODE == 'OFB':
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((KM_ADDRESS, KM_PORT))
    K2 = client.recv(16)
    client.close()
    print('K2: ', K2)

#client.close()