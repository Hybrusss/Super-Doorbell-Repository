from webBackend import *
import codeAPI
import pygame

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
    # Called on button press
    with mutex: # Wait for the mutex
        global currentPinStr
        global lastPressTime
        
		# If the time is over 5 seconds, clear the code
        if time.time() - lastPressTime > 5:
            currentPinStr = ""
        
		# Determine the current row based on the channel pin
        if channel == PIN_ROW0: currentRow = 0
        elif channel == PIN_ROW1: currentRow = 1
        elif channel == PIN_ROW2: currentRow = 2
        elif channel == PIN_ROW3: currentRow = 3
        
		# Next, determine the actual button by using the global variable currentColumn
        curBut = ''
        if currentColumn == 0:
            if currentRow == 0: # The button for 4 also presses 1, so this prevents the multipress
                if time.time() - lastPressTime < .100:
                    curBut = ''
                else:
                    curBut = '1'
            elif currentRow == 1:
                curBut = '4'
            elif currentRow == 2: # The button for 7 also presses the *
                if time.time() - lastPressTime < .100:
                    currentPinStr = currentPinStr[:-1]
                curBut = '7'
            elif currentRow == 3:
                curBut = '*'
        elif currentColumn == 1:
            if currentRow == 0: # The button for 2 also presses 5
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
            elif currentRow == 2: # The button for # also presses 9
                if time.time() - lastPressTime < .100:
                    curBut = ''
                else:
                    curBut = '9'
            elif currentRow == 3:
                curBut = '#'
        if curBut == '':
            return
        if curBut == '*':
            currentPinStr = currentPinStr[:-1]
            print(currentPinStr)
            return

        currentPinStr += curBut
        print(currentPinStr)
        # Retrieve the sound and play it when # is pressed
        if currentPinStr[-1] == '#':
            print(currentPinStr[:-1])
            try:
                sndFile = codeAPI.retrieveSound(int(currentPinStr[:-1]))
                snd = pygame.mixer.Sound(sndFile)
                snd.play()
            finally:
                currentPinStr = ""
        
        lastPressTime = time.time()

def _pinpadDriverThread():
    # Initialize GPIO and sound mixer
    pygame.mixer.init()
    # pygame was the only library that really worked on the pi
    
    import RPi.GPIO as GPIO

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PIN_COL0, GPIO.OUT)
    GPIO.setup(PIN_COL1, GPIO.OUT)
    GPIO.setup(PIN_COL2, GPIO.OUT)
    GPIO.setup(PIN_ROW0, GPIO.IN, GPIO.PUD_DOWN) # Use the internal pull-down resistors
    GPIO.setup(PIN_ROW1, GPIO.IN, GPIO.PUD_DOWN)
    GPIO.setup(PIN_ROW2, GPIO.IN, GPIO.PUD_DOWN)
    GPIO.setup(PIN_ROW3, GPIO.IN, GPIO.PUD_DOWN)

	# Setup the buttonHandler for the row pins
    GPIO.add_event_detect(PIN_ROW0, GPIO.RISING, _buttonHandler, 50)
    GPIO.add_event_detect(PIN_ROW1, GPIO.RISING, _buttonHandler, 50)
    GPIO.add_event_detect(PIN_ROW2, GPIO.RISING, _buttonHandler, 50)
    GPIO.add_event_detect(PIN_ROW3, GPIO.RISING, _buttonHandler, 50)
    global currentColumn
    try:
        # The following loop iterates through each column and will trigger an 
		# event handler for when a button is pressed on the current column
        # This orientation does not support multiple button presses
        while True:
            currentColumn = 0
            GPIO.output(PIN_COL0, GPIO.HIGH) # Set column 0 pin to HIGH
            with mutex: # Wait for mutex: this lets the button press actually work without a race condition
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
        
    finally: # Cleanup the program and close
        webRunning = False
        GPIO.cleanup()
        print("Exiting doorbell subsystem...")
        import os
        os._exit(0)


codeAPI.loadMainCodesFile()
createUDPBroadcaster()
createRuntimeServer()
_pinpadDriverThread()

