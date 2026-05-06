from PiSubsys.webBackend import rqPacket, getDoorbellIP, connectToPi, pcSendPacket

def setup_connection():
    global doorbell_ip, the_socket
    doorbell_ip = getDoorbellIP()
    if doorbell_ip != '127.0.0.1':
        the_socket = connectToPi(doorbell_ip)
    else:
        the_socket = None

# setup_connection()

def send_packet_data():
    packet = rqPacket(bytes(256))
    packet.kind = 1
    packet.size = 17
    packet.mainData = b"123456789\x00{SOUND FILE AS BYTES LAOLOOOl}"
    retPack = pcSendPacket(the_socket, packet)
    print(retPack.mainData)