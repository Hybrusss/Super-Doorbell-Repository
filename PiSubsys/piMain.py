from webBackend import *

pdThr = None

def _pinpadDriverThread():
	import RPi.GPIO 
	while True:
		time.sleep(0.01)

def createPinpadThread():
	global pdThr
	pdThr = threading.Thread(target=_pinpadDriverThread)
	pdThr.start()

createUDPBroadcaster()
createRuntimeServer()