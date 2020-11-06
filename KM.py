import socket

serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

serv.bind(('192.168.56.1', 8090))
serv.listen(5)

while True:
    conn, addr = serv.accept()
    print('Got connection from ', addr)
    from_client = ''

    while True:
        data = conn.recv(4096).decode()
        if not data: break
        from_client += data
        print(from_client)
        msg = 'Server'
        conn.send(msg.encode())

    conn.close
    print("client disconnected")