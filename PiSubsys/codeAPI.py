from codes import *

ADD_FAIL = 0x00000002
REM_FAIL = 0x00000003
IMP_FAIL = 0x00000004
EXP_FAIL = 0x00000005
UNK_FAIL = 0xFFFFFFFF


mainCodes = []

def loadMainCodesFile():
	'''Loads mainCodes.cd from the disk.'''
	global mainCodes
	try:
		mainCodes = code.createListFromFile("mainCodes.cd")
		print(mainCodes)
	finally:
		return

def saveMainCodesFile():
	'''Saves mainCodes.cd to the disk.'''
	code.createFileFromList("mainCodes.cd", mainCodes)

def importCodesFile(file:bytes):
	fileHandle = None
	try:
		fileHandle = open(f"{Path.home()}/doorbell/settings/mainCodes.cd", "bw+")
		fileHandle.write(file)
		fileHandle.close()
	except Exception as ex:
		print(ex)
		if fileHandle != None:
			fileHandle.close()
		return UNK_FAIL
	return 0

def exportCodesFile() -> bytes:
	'''
	Exports the entire binary file
	'''
	fileHandle = None
	try:
		fileHandle = open(f"{Path.home()}/doorbell/settings/mainCodes.cd", "br")
		ret = fileHandle.read()
		fileHandle.close()
	except Exception as ex:
		print(ex)
		if fileHandle != None:
			fileHandle.close()
		return None
	return ret

def addCode(pin:int, sound:str) -> int:
	'''Adds the code {pin} to the list with the specified sound file {sound}.'''
	global mainCodes
	for cd in mainCodes:
		if (cd.val == pin):
			mainCodes.remove(cd)
			break
	newCode = code(pin, f"{Path.home()}/doorbell/sounds/" + sound)
	mainCodes.append(newCode)
	saveMainCodesFile()
	return 0

def delCodes() -> int:
	'''Removes all codes from the list.'''
	global mainCodes
	mainCodes = []
	return 0

def retrieveSound(pin:int) -> str:
	'''
	Searches for the specified pin and returns the sound file.\n
	Returns an empty string if no file was found.
	'''
	print(mainCodes)
	for cd in mainCodes:
		if (cd.val == pin):
			return cd.soundFile
		
	return ""

def writeSoundFile(path:str, file:bytes) -> int:
	'''
	Writes the sound file to the specific path on the filesystem.
	'''
	fileHandle = None
	try:
		fileHandle = open(f"{Path.home()}/doorbell/sounds/" + path, "bw+")
		fileHandle.write(file)
		fileHandle.close()
	except Exception as ex:
		print(ex)
		if fileHandle != None:
			fileHandle.close()
		return UNK_FAIL
	return 0
