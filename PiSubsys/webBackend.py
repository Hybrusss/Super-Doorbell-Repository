import threading
import socket
import time

bcThr = None

def _broadcastThread():
	interfaces = socket.getaddrinfo(host=socket.gethostname(), port=None,
								family=socket.AF_INET, type=socket.SOCK_DGRAM)
	serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 
							  socket.IPPROTO_UDP)
	ip = ""
	for i in range(0, len(interfaces)):
		if (interfaces[i][4][0] == "127.0.0.1"): continue
		ip = interfaces[i][4][0]
	print(ip)
	serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
	serverSocket.settimeout(0.2)
	while True:
		serverSocket.sendto(bytes(ip, "ASCII"), ("255.255.255.255", 8002))
		time.sleep(2)
	return

def createUDPBroadcaster():
	global bcThr
	bcThr = threading.Thread(target=_broadcastThread)
	bcThr.start()
	return

createUDPBroadcaster()