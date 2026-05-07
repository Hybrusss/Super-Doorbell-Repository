import threading
import socket
import time

webRunning = True

bcThr = None
wsThr = None

UDP_PORT = 8002
RTS_PORT = 8001
PACKET_MAX = 104857600

class rqPacket:
	def __init__(self, data:bytes):
		self.backingData = data

	@property
	def kind(self) -> int:
		return int.from_bytes(self._data[0:4], 'big')
	
	@kind.setter
	def kind(self, val:int):
		newBytes = val.to_bytes(4, 'big')
		self._data = bytes(newBytes + self._data[12:self.size - 12])

	@property
	def size(self) -> int:
		return int.from_bytes(self._data[4:12], 'big')
	
	@size.setter
	def size(self, val:int):
		newBytes = (val).to_bytes(8, 'big')
		self._data = bytes(self._data[0:4] + newBytes + self._data[12:self.size - 12])
	
	@property
	def mainData(self) -> bytes:
		return self._data[12:self.size - 12]
	
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
	while webRunning:
		serverSocket.sendto(bytes("HONK", "ASCII"), ("255.255.255.255", UDP_PORT))
		time.sleep(2)
	serverSocket.close()

def _runtimeServerThread():
	runtimeSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	runtimeSocket.bind(("0.0.0.0", RTS_PORT))
	while webRunning:
		# Accept only one incomming connection for the runtime API
		runtimeSocket.listen(1)
		connection, addr = runtimeSocket.accept()
		print("Incomming connection from " + addr[0])
		connection.settimeout(30)
		while True:
			try:
				# Receive a request packet from the connected computer
				import codeAPI
				getPacket = rqPacket(connection.recv(12))
				retPacket = rqPacket(bytes(PACKET_MAX))
				status = 0

				if getPacket.size == 0:
					connection.close()
					break
				
				lastSize = getPacket.size - len(getPacket.mainData)
				while getPacket.size != len(getPacket.mainData):
					getPacket.mainData += connection.recv(PACKET_MAX)
					if lastSize == 24:
						break
					if getPacket.size - len(getPacket.mainData) == lastSize:
						break
					lastSize = getPacket.size - len(getPacket.mainData)
				
				print(getPacket.kind)
				print(getPacket.size)
				if getPacket.kind == 1:
					if getPacket.size < 72:
						status = codeAPI.UNK_FAIL
					else:	
						try:
							code = int.from_bytes(getPacket.mainData[0:8])
							rawName = getPacket.mainData[8:72]
							idx = 0
							while rawName[idx] != 0 and idx < 64:
								idx += 1
							soundName = bytes.decode(rawName[0:idx], 'utf-8')
							soundName.strip()
							fileBytes = getPacket.mainData[72:-1]
							codeAPI.writeSoundFile(soundName, fileBytes)
							status = codeAPI.addCode(code, soundName)
						except Exception as ex:
							print(ex)
							status = codeAPI.UNK_FAIL
				elif getPacket.kind == 2:
					if getPacket.size < 1:
						status = codeAPI.UNK_FAIL
					else:
						status = codeAPI.delCodes()
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
			except Exception as h:
				print(h)
				break
			connection.close()
		print("Severed connection to " + addr[0])
	runtimeSocket.close()

def createUDPBroadcaster():
	'''
	Create the broadcasting service that allows devices to find this pi.
	'''
	global bcThr
	bcThr = threading.Thread(target=_broadcastThread)
	bcThr.start()
	return

def createRuntimeServer():
	'''
	Create the server for processing doorbell edit requests.
	'''
	global wsThr
	wsThr = threading.Thread(target=_runtimeServerThread)
	wsThr.start()
	return

def getDoorbellIP() -> str:
	'''
	Returns the IP of the doorbell Pi for the GUI to use.
	'''
	clientSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	clientSock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
	clientSock.bind(("0.0.0.0", 8002))
	clientSock.settimeout(5)
	data, addr = clientSock.recvfrom(1024)
	if data == b"HONK":
		return addr[0]
	return "127.0.0.1"

def connectToPi(ip:str) -> socket.socket:
	'''
	Returns a socket containing the connection to the doorbell Pi
	'''
	clientSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	clientSock.connect((ip, 8001))
	return clientSock

def pcSendPacket(sock:socket.socket, packet:rqPacket) -> rqPacket:
	'''
	Sends a packet to the Pi and waits for a response.\n
	Returns the packet sent back.
	'''
	sock.sendall(packet.backingData)
	data = sock.recv(12)
	retPack = rqPacket(data)
	try:
		lastSize = retPack.size - len(retPack.mainData)
		while retPack.size != len(retPack.mainData):
			retPack.mainData += sock.recv(lastSize)
			if retPack.size - len(retPack.mainData) == lastSize:
				break
			else:
				lastSize = retPack.size - len(retPack.mainData)
	finally:
		pass
	return retPack
