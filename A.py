import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('192.168.56.1', 8090))

message = 'Message'
client.send(message.encode())

from_server = client.recv(4096)

client.close()

print(from_server)