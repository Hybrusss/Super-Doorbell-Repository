from codes import *

ADD_FAIL = 0x00000002
REM_FAIL = 0x00000003
IMP_FAIL = 0x00000004
EXP_FAIL = 0x00000005
UNK_FAIL = 0xFFFFFFFF


mainCodes = []

def loadMainCodesFile():
	'''Loads mainCodes.cd from the disk.'''
	mainCodes = code.createListFromFile("mainCodes.cd")

def saveMainCodesFile():
	'''Saves mainCodes.cd to the disk.'''
	code.createFileFromList("mainCodes.cd")

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
	for cd in mainCodes:
		if (cd.val == pin):
			return ADD_FAIL
	newCode = code(pin, f"{Path.home()}/doorbell/sounds/" + sound)
	mainCodes.append(newCode)
	return 0

def delCode(pin:int) -> int:
	'''Removes the specified code {pin} from the list.'''
	for cd in mainCodes:
		if (cd.val == pin):
			mainCodes.remove(cd)
			return 0
	return REM_FAIL

def retrieveSound(pin:int) -> str:
	'''
	Searches for the specified pin and returns the sound file.\n
	Returns an empty string if no file was found.
	'''
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