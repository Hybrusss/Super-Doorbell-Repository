import socket
import time
import PiSubsys.webBackend as web

addr = web.getDoorbellIP()

clientSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSock.connect((addr[0], 8001))
while True:
	clientSock.sendall(bytes([0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 14, 0x70, 0x00]))
	data = clientSock.recv(256)
	print(repr(data))
	time.sleep(1)