from codes import *

mainCodes = []

def loadMainCodesFile():
	'''Loads mainCodes.cd from the disk.'''
	mainCodes = code.createListFromFile("mainCodes.cd")

def saveMainCodesFile():
	'''Saves mainCodes.cd to the disk.'''
	code.createFileFromList("mainCodes.cd")

def addCode(pin:str, sound:str):
	'''Adds the code {pin} to the list with the specified sound file {sound}.'''
	pinInt = int(pin)
	for cd in mainCodes:
		if (cd.val == pinInt):
			return
	newCode = code(pinInt, sound)
	mainCodes.append(newCode)

def delCode(pin:str):
	'''Removes the specified code {pin} from the list.'''
	pinInt = int(pin)
	for cd in mainCodes:
		if (cd.val == pinInt):
			mainCodes.remove(cd)
			return

def retrieveSound(pin:str) -> str:
	'''
	Searches for the specified pin and returns the sound file.\n
	Returns an empty string if no file was found.
	'''
	pinInt = int(pin)
	for cd in mainCodes:
		if (cd.val == pinInt):
			return cd.soundFile
		
	return ""
