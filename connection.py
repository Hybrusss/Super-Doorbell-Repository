from PiSubsys.webBackend import rqPacket, getDoorbellIP, connectToPi, pcSendPacket, PACKET_MAX
from functions import beautify_path
from pathlib import Path
import screens
import os


doorbell_ip = '127.0.0.1'
the_socket = None

def setup_connection():
    global doorbell_ip, the_socket
    doorbell_ip = getDoorbellIP()
    if doorbell_ip != '127.0.0.1':
        the_socket = connectToPi(doorbell_ip)
        #the_element = [x for x in screens.container_dict["title"].elements if x.name == "Connection Box"][0]
        #the_element.text = "Connected"
    else:
        the_socket = None

def send_packet_data():
    packet = rqPacket(bytes(256))
    packet.kind = 1
    packet.size = 17
    packet.mainData = b"123456789\x00{SOUND FILE AS BYTES LAOLOOOl}"
    retPack = pcSendPacket(the_socket, packet)
    print(retPack.mainData)

def keep_alive_packet():
    packet = rqPacket(bytes(256))
    packet.kind = 0
    packet.size = 4
    packet.mainData = int.to_bytes(0x00000001, 4)
    pcSendPacket(the_socket, packet)

def upload_data(the_data: dict):

    print(the_data)

    def output_func():

        packet = rqPacket(bytes(1))
        packet.kind = 2
        packet.size = 1
        packet.mainData = b"0"

        pcSendPacket(the_socket, packet)


        for code in the_data:
            
            sound_path = the_data[code]["Sound"]
            sound_pathOb = Path(sound_path)

            sound_file_as_bytes = ""

            with open(sound_path, 'rb') as f:
                sound_file_as_bytes = f.read()
            

            # size of sound in bytes
            
            sound_size = os.path.getsize(sound_path)
            soundNameBytes = bytes(sound_pathOb.stem + sound_pathOb.suffix, 'utf-8')
            nameLen = len(soundNameBytes)
            if nameLen > 64:
                raise ValueError()
            elif nameLen < 64:
                soundNameBytes += b'\x00' * (64 - nameLen)
            print(sound_size)
            packet = rqPacket(bytes(12))
            packet.kind = 1
            packet.size = 8 + 64 + sound_size
            code = int(code)
            packet.mainData = int.to_bytes(code, 8, 'big') + soundNameBytes + sound_file_as_bytes
            
            pcSendPacket(the_socket, packet)
    
    return output_func

# setup_connection()
# upload_data({14234: {"Name": "Balls", "Sound": "/Users/gabrielphilippi/5080.wav"}})