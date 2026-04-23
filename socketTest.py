import socket
import time

clientSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
clientSock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
clientSock.bind(("0.0.0.0", 8002))
data, addr = clientSock.recvfrom(1024)
print(data)

clientSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSock.connect((addr[0], 8001))
while True:
	clientSock.sendall(bytes([0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 14, 0x70, 0x00]))
	data = clientSock.recv(256)
	print(repr(data))
	time.sleep(1)