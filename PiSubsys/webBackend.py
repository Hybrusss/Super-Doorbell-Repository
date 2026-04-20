import threading
import socket
import time
import rqPacket

bcThr = None
wsThr = None

UDP_PORT = 8002
RTS_PORT = 8001

def _broadcastThread():
	interfaces = socket.getaddrinfo(host=socket.gethostname(), port=None,
								family=socket.AF_INET, type=socket.SOCK_DGRAM)
	serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 
							  socket.IPPROTO_UDP)
	ip = ""
	# Iterate through the interfaces and find the one we'd actually be broadcasting on 
	for i in range(0, len(interfaces)):
		if (interfaces[i][4][0] == "127.0.0.1"): continue
		ip = interfaces[i][4][0]
	serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
	serverSocket.settimeout(0.2)
	# Broadcast that IP address of this system on the local network via UDP
	while True:
		serverSocket.sendto(bytes(ip, "ASCII"), ("255.255.255.255", UDP_PORT))
		time.sleep(2)

def _runtimeServerThread():
	runtimeSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	runtimeSocket.bind(("0.0.0.0", RTS_PORT))
	while True:
		# Accept only one incomming connection for the runtime API
		runtimeSocket.listen(1)
		connection, addr = runtimeSocket.accept()
		print("Incomming connection from " + addr[0])
		connection.settimeout(1)
		while True:
			try:
				# Receive a request packet from the connected computer
				getPacket = rqPacket.rqPacket(connection.recv(256))
				retPacket = rqPacket.rqPacket(bytes(256))
				if getPacket.size == 0:
					connection.close()
					break
				if getPacket.kind == 1:
					print(getPacket.mainData[0:4])
					print(getPacket.size)
					retPacket.kind = 123
					retPacket.size = 19
					retPacket.mainData = b"chicken"

				connection.sendto(retPacket.backingData, addr)
			except:
				connection.close()
				break

def createUDPBroadcaster():
	global bcThr
	bcThr = threading.Thread(target=_broadcastThread)
	bcThr.start()
	return

def createRuntimeServer():
	global wsThr
	wsThr = threading.Thread(target=_runtimeServerThread)
	wsThr.start()
	return

createUDPBroadcaster()
createRuntimeServer()

