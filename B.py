import socket

KM_ADDRESS = '192.168.56.1'
B_ADDRESS = '192.168.56.1'
KM_PORT = 8090
B_PORT = 9090
IV = '1234567890abcdef'

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

