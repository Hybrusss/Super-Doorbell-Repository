from webBackend import *

pdThr = None
resetTimer = None

PIN_COL0 = 0
PIN_COL1 = 0
PIN_COL2 = 0
PIN_ROW0 = 0
PIN_ROW1 = 0
PIN_ROW2 = 0
PIN_ROW3 = 0

currentColumn = -1
currentPinStr = ""


def _resetPinStr():
	currentPinStr = ""

def _buttonHandler(currentRow:int):
	curBut = ''
	if currentColumn == 0:
		if currentRow == 0:
			curBut = '1'
		elif currentRow == 1:
			curBut = '4'
		elif currentRow == 2:
			curBut = '7'
		elif currentRow == 3:
			curBut = '*'
	if currentColumn == 1:
		if currentRow == 0:
			curBut = '2'
		elif currentRow == 1:
			curBut = '5'
		elif currentRow == 2:
			curBut = '8'
		elif currentRow == 3:
			curBut = '0'
	if currentColumn == 2:
		if currentRow == 0:
			curBut = '3'
		elif currentRow == 1:
			curBut = '6'
		elif currentRow == 2:
			curBut = '9'
		elif currentRow == 3:
			curBut = '#'
	if curBut == '':
		return
	global resetTimer
	if resetTimer == None:
		resetTimer = threading.Timer(5, _resetPinStr)
	resetTimer.cancel()

	global currentPinStr
	currentPinStr += curBut

	resetTimer.run()
	pass

def _pinpadDriverThread():
	import RPi.GPIO as GPIO

	GPIO.setmode(GPIO.BCM)
	GPIO.setup(PIN_COL0, GPIO.OUT)
	GPIO.setup(PIN_COL1, GPIO.OUT)
	GPIO.setup(PIN_COL2, GPIO.OUT)
	GPIO.setup(PIN_ROW0, GPIO.IN, GPIO.PUD_DOWN)
	GPIO.setup(PIN_ROW1, GPIO.IN, GPIO.PUD_DOWN)
	GPIO.setup(PIN_ROW2, GPIO.IN, GPIO.PUD_DOWN)
	GPIO.setup(PIN_ROW3, GPIO.IN, GPIO.PUD_DOWN)

	GPIO.add_event_detect(PIN_ROW0, GPIO.RISING, _buttonHandler, 1)
	GPIO.add_event_detect(PIN_ROW1, GPIO.RISING, _buttonHandler, 1)
	GPIO.add_event_detect(PIN_ROW2, GPIO.RISING, _buttonHandler, 1)
	GPIO.add_event_detect(PIN_ROW3, GPIO.RISING, _buttonHandler, 1)

	try:
		# The following loop iterates through each column and row to see which button is pressed
		# This orientation does not support multiple buttons and will
		while True:
			currentColumn = 0
			GPIO.output(PIN_COL0, GPIO.HIGH) # Set column 0 pin to HIGH
			time.sleep(0.001) # Wait for 1 millisecond for the hardware to react
			GPIO.output(PIN_COL0, GPIO.LOW) # Reset column pin
			time.sleep(0.001)

			currentColumn = 1
			GPIO.output(PIN_COL1, GPIO.HIGH) # Set column 1 pin to HIGH
			time.sleep(0.001) # Wait for 1 millisecond for the hardware to react
			GPIO.output(PIN_COL1, GPIO.LOW) # Reset column pin
			time.sleep(0.001)

			currentColumn = 2
			GPIO.output(PIN_COL2, GPIO.HIGH) # Set column 2 pin to HIGH
			time.sleep(0.001) # Wait for 1 millisecond for the hardware to react
			GPIO.output(PIN_COL2, GPIO.LOW) # Reset column pin
			time.sleep(0.001)
		
	finally:
		webRunning = False
		GPIO.cleanup()
		print("Exiting doorbell subsystem...")
		exit(0)


createUDPBroadcaster()
createRuntimeServer()
_pinpadDriverThread()