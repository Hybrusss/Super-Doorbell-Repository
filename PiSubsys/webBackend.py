import threading
import socket
import time

bcThr = None
wsThr = None

UDP_PORT = 8002
RTS_PORT = 8001
PACKET_MAX = 10485760

class rqPacket:
	def __init__(self, data:bytes):
		self.backingData = data

	@property
	def kind(self) -> int:
		return int.from_bytes(self._data[0:4])
	
	@kind.setter
	def kind(self, val:int):
		newBytes = val.to_bytes(4)
		self._data = bytes(newBytes + self._data[12:self.size])

	@property
	def size(self) -> int:
		return 12 - int.from_bytes(self._data[4:12])
	
	@size.setter
	def size(self, val:int):
		newBytes = (12 + val).to_bytes(8)
		self._data = bytes(self._data[0:4] + newBytes + self._data[12:self.size])
	
	@property
	def mainData(self) -> bytes:
		return self._data[12:self.size]
	
	@mainData.setter
	def mainData(self, data:bytes):
		self._data = bytes(self._data[0:12] + data)
			
	@property
	def backingData(self) -> bytes:
		return self._data
	
	@backingData.setter
	def backingData(self, data:bytes):
		self._data = data

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
	# Broadcast the message HONK to broadcast the IP address of this system on the local network via UDP
	while True:
		serverSocket.sendto(bytes("HONK", "ASCII"), ("255.255.255.255", UDP_PORT))
		time.sleep(2)

def _runtimeServerThread():
	runtimeSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	runtimeSocket.bind(("0.0.0.0", RTS_PORT))
	while True:
		# Accept only one incomming connection for the runtime API
		runtimeSocket.listen(1)
		connection, addr = runtimeSocket.accept()
		print("Incomming connection from " + addr[0])
		connection.settimeout(30)
		while True:
			try:
				# Receive a request packet from the connected computer
				import codeAPI
				getPacket = rqPacket(connection.recv(PACKET_MAX))
				retPacket = rqPacket(bytes(PACKET_MAX))
				status = 0

				if getPacket.size == 12:
					connection.close()
					break
				if getPacket.kind == 1:
					if getPacket.size < 72:
						status = codeAPI.UNK_FAIL
					else:	
						try:
							code = int.from_bytes(getPacket.mainData, 8)
							soundName = str(getPacket.mainData[8:71])
							fileBytes = getPacket.mainData[72:getPacket.size]
							codeAPI.writeSoundFile(soundName, fileBytes)
							status = codeAPI.addCode(code, soundName)
						except Exception as ex:
							print(ex)
							status = codeAPI.UNK_FAIL
				elif getPacket.kind == 2:
					if getPacket.size < 8:
						status = codeAPI.UNK_FAIL
					else:
						status = codeAPI.delCode()
				elif getPacket.kind == 3:
					if getPacket.size == 0:
						status = codeAPI.IMP_FAIL
					else:
						status = codeAPI.importCodesFile(
							getPacket.mainData[0:getPacket.size])
				if getPacket.kind == 4: # special case
					fileBytes = codeAPI.exportCodesFile()
					if fileBytes == None:
						retPacket.size = 1
						retPacket.mainData = b'\0'
					else:
						retPacket.size = len(fileBytes)
						retPacket.mainData = fileBytes
					retPacket.kind = 4
				else:
					retPacket.kind = 0
					retPacket.size = 4
					retPacket.mainData = int.to_bytes(status, 4)

				connection.sendto(retPacket.backingData, addr)
			except:
				connection.close()
				break
		print("Severed connection to " + addr[0])

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

def getDoorbellIP() -> str:
	'''

	'''
	clientSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	clientSock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
	clientSock.bind(("0.0.0.0", 8002))
	clientSock.settimeout(1)
	data, addr = clientSock.recvfrom(1024)
	if data == b"HONK":
		return addr[0]
	return "127.0.0.1"

def connectToPi(ip:str) -> socket.socket:
	clientSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	clientSock.connect((ip, 8001))
	return clientSock

def pcSendPacket(sock:socket.socket, packet:rqPacket) -> rqPacket:
	sock.sendall(packet.backingData)
	data = sock.recv(PACKET_MAX)
	return rqPacket(data)
