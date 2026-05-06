from webBackend import *
import codeAPI
import playsound

pdThr = None
mutex = threading.Lock()

PIN_COL0 = 18
PIN_COL1 = 19
PIN_COL2 = 20
PIN_ROW0 = 17
PIN_ROW1 = 16
PIN_ROW2 = 13
PIN_ROW3 = 12
WAIT_TIME = 0.055

currentColumn = -1
currentPinStr = ""
lastPressTime = 0

def _buttonHandler(channel:int):
    with mutex:
        global currentPinStr
        global lastPressTime
        
        if time.time() - lastPressTime > 5:
            currentPinStr = ""
        
        if channel == PIN_ROW0: currentRow = 0
        elif channel == PIN_ROW1: currentRow = 1
        elif channel == PIN_ROW2: currentRow = 2
        elif channel == PIN_ROW3: currentRow = 3
        curBut = ''
        if currentColumn == 0:
            if currentRow == 0:
                if time.time() - lastPressTime < .100:
                    curBut = ''
                else:
                    curBut = '1'
            elif currentRow == 1:
                curBut = '4'
            elif currentRow == 2:
                if time.time() - lastPressTime < .100:
                    currentPinStr = currentPinStr[:-1]
                curBut = '7'
            elif currentRow == 3:
                curBut = '*'
        elif currentColumn == 1:
            if currentRow == 0:
                if time.time() - lastPressTime < .100:
                    currentPinStr = currentPinStr[:-1]
                curBut = '2'
            elif currentRow == 1:
                curBut = '5'
            elif currentRow == 2:
                curBut = '8'
            elif currentRow == 3:
                curBut = '0'
        elif currentColumn == 2:
            if currentRow == 0:
                curBut = '3'
            elif currentRow == 1:
                curBut = '6'
            elif currentRow == 2:
                if time.time() - lastPressTime < .100:
                    curBut = ''
                else:
                    curBut = '9'
            elif currentRow == 3:
                curBut = '#'
        if curBut == '':
            return

        currentPinStr += curBut
        if currentPinStr[-1] == '#':
            sndFile = codeAPI.retrieveSound(int(currentPinStr[:-1]))
            try:
                playsound.playsound(sndFile)
            finally:
                currentPinStr = ""
        
        lastPressTime = time.time()

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
    global currentColumn
    try:
        # The following loop iterates through each column and row to see which button is pressed
        # This orientation does not support multiple buttons and will
        while True:
            currentColumn = 0
            GPIO.output(PIN_COL0, GPIO.HIGH) # Set column 0 pin to HIGH
            with mutex:
                GPIO.output(PIN_COL0, GPIO.LOW) # Reset column pin
            time.sleep(WAIT_TIME)

            currentColumn = 1
            GPIO.output(PIN_COL1, GPIO.HIGH) # Set column 1 pin to HIGH
            with mutex:
                GPIO.output(PIN_COL1, GPIO.LOW) # Reset column pin
            time.sleep(WAIT_TIME)

            currentColumn = 2
            GPIO.output(PIN_COL2, GPIO.HIGH) # Set column 2 pin to HIGH
            with mutex:
                GPIO.output(PIN_COL2, GPIO.LOW) # Reset column pin
            time.sleep(WAIT_TIME)
        
    finally:
        webRunning = False
        GPIO.cleanup()
        print("Exiting doorbell subsystem...")
        exit(0)


createUDPBroadcaster()
createRuntimeServer()
_pinpadDriverThread()

