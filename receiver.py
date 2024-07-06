import socket
import sys
import os
import signal

def signal_handler(sig, frame):
    print('Connection closed by server...')
    server.close()
    sys.exit()

signal.signal(signal.SIGINT, signal_handler)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('0.0.0.0', 4444))
server.listen(5)
print('[+] Server is waiting for connection [+]')

try:
    conn, addr = server.accept()
    print('Connection received from: ' + addr[0])
    filename = 'spy.txt'
    with open(filename, 'wb') as file:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            file.write(data)

    print(f"[+] File received and saved as {filename}")
    conn.close()

except socket.timeout as e:
    print("[ERR] Socket timeout")
    server.close()
    sys.exit()
except Exception as e:
    print(f"[ERR] {e}")
    server.close()
    sys.exit()
